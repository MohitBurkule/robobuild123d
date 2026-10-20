#!/bin/bash
# [fix-G] Every fix-* head passes gate() (below) before it is merged; see robot/tools/ci_gate.py.
# Bounded integration loop: at most MAX_ITERS passes of
#   fetch origin; merge every fix-* head (local or origin/, whichever is newer) into rvrn2-ci
#   (conflicts aborted and logged as `[ci] conflict fix-X`); push rvrn2-ci:rvrn2 with retries;
#   regenerate the spec, full verify through /tmp/heavy.sh streaming blockers, write a [ci] summary line.
# Renders (robot/tools/ci_render.sh) run in the background in the shared slots after each verify.
# Stops early on 0 blockers or when $CI_STOP exists. Run from a worktree checked out on rvrn2-ci.
MAX_ITERS=${MAX_ITERS:-20}
P=${PROGRESS_DIR:-/mnt/project-files/robot-cad/b123d/progress}
SPEC=${SPEC:-robots/revron/spec.json}
log() { echo "$(date -Is) [ci] $*" >> "$P/builder.log"; }
[ "$(git rev-parse --abbrev-ref HEAD)" = "rvrn2-ci" ] || { log "not on rvrn2-ci, exiting"; exit 1; }
push() { for d in 0 2 4 8 16; do sleep $d; git push -q -u origin rvrn2-ci:rvrn2 2>>"$P/ci_push.err" && { log "pushed $(git rev-parse --short HEAD) to origin/rvrn2"; return 0; }; done; log "push FAILED after retries"; }
heads() { # newest of local fix-X and origin/fix-X per branch
  for n in $( (git for-each-ref --format='%(refname:lstrip=2)' 'refs/heads/fix-*'; git for-each-ref --format='%(refname:lstrip=3)' 'refs/remotes/origin/fix-*') | grep -v -e '-local$' | sort -u); do
    l=refs/heads/$n; r=refs/remotes/origin/$n
    if git rev-parse -q --verify $l >/dev/null && git rev-parse -q --verify $r >/dev/null; then
      if git merge-base --is-ancestor $l $r; then echo origin/$n; else echo $n; git merge-base --is-ancestor $r $l || echo origin/$n; fi
    elif git rev-parse -q --verify $l >/dev/null; then echo $n; else echo origin/$n; fi
  done; }
render() { # async, one at a time, from a snapshot worktree of the verified sha so merges do not move it
  pgrep -f "robot/tools/ci_render.sh" >/dev/null && { log "renders still running, skipping renders for $(git rev-parse --short HEAD)"; return; }
  rd=${RENDER_WT:-/tmp/claude-0/-home-user/6d647ed2-7427-59f3-8ab5-ba663cdaf3d4/scratchpad/ci_render_wt}
  [ -d "$rd" ] || git worktree add -q --detach "$rd" HEAD
  git -C "$rd" checkout -q --detach "$(git rev-parse HEAD)" && (cd "$rd" && nohup setsid bash robot/tools/ci_render.sh >/dev/null 2>&1 < /dev/null &)
}
# [fix-G] merge gate: trial-merge $1 into a temp worktree of HEAD, run assembly + interference (one process each,
# one at a time, fresh ROBOT_CACHE per run) and reject when either blocker count rises vs the cached baseline of HEAD.
# Branches touching only robot/checks/ or docs skip the verify but must pass the pytest files they touch.
# *-param branches / commits mentioning param|refactor must also pass robots/revron/tools/geom_equal.py vs HEAD.
# GATE=0 disables. Returns 0 = merge, 1 = rejected (already logged).
GWT=${GATE_WT:-/tmp/claude-0/-home-user/6d647ed2-7427-59f3-8ab5-ba663cdaf3d4/scratchpad/ci_gate}
GPY="python3 $PWD/robot/tools/ci_gate.py"
gwt() { # dir rev; rev resolved in THIS worktree (a bare "HEAD" inside -C dir would be dir's own HEAD)
  local r; r=$(git rev-parse "$2^{commit}") || return 1
  [ -d "$1" ] || git worktree add -q --detach "$1" "$r"; git -C "$1" merge --abort 2>/dev/null; git -C "$1" reset -q --hard; git -C "$1" clean -fdq
  git -C "$1" checkout -q --detach "$r" && [ "$(git -C "$1" rev-parse HEAD)" = "$r" ] || { log "gate worktree $1 not at $r"; return 1; }; }
gcount() { # dir group -> blocker count (-1 = did not finish)
  local c; c=$(mktemp -d "${TMPDIR:-/tmp}/ci_gate_cache.XXXX")  # c: log dir only; cache is the shared content-keyed one (fix-K)
  local fc=; [ $(( ${i:-1} % ${FRESH_EVERY:-3} )) -eq 0 ] && fc="ROBOT_CACHE=$c"   # every 3rd round: fresh cache spot check
  (cd "$1" && env $fc HEAVY_CI=1 /tmp/heavy.sh timeout "${GATE_TIMEOUT:-3000}" python3 -m robot verify "$SPEC" --full --only "$2" > "$c.log" 2>&1)
  $GPY count "$c.log"; rm -rf "$c" "$c.log"; }
gfail() { log "gate rejected ${1#origin/} $2: $3"; printf '{"t":"%s","sha":"%s","group":"ci_gate","id":"ci_gate.rejected","parts":[],"branch":"%s","message":"[ci] gate rejected %s %s: %s"}\n' \
  "$(date -Is)" "$2" "${1#origin/}" "${1#origin/}" "$2" "$3" >> "$P/blockers_live_$(echo "${1#origin/}" | sed -E 's/^fix-(.).*/\1/' | tr a-z A-Z).jsonl"; return 1; }
gate() {
  [ "${GATE:-1}" = 1 ] || return 0
  local b=$1 s; s=$(git rev-parse --short "$b"); local head; head=$(git rev-parse --short HEAD)
  local files; files=$(git diff --name-only HEAD..."$b")
  gwt "$GWT/trial" HEAD || return 0
  git -C "$GWT/trial" merge -q --no-edit "$b" >/dev/null 2>&1 || { git -C "$GWT/trial" merge --abort; return 0; }  # conflicts: normal path logs them
  if [ "$($GPY kind $files)" = verifier-only ]; then
    local t; t=$(echo "$files" | grep -E '^robot/tests/test_.*\.py$'); for f in $(echo "$files" | grep '^robot/checks/'); do
      m=$(basename "$f" .py); [ -f "$GWT/trial/robot/tests/test_$m.py" ] && t="$t robot/tests/test_$m.py"; done
    [ -z "$t" ] && t=robot/tests/test_checks.py
    (cd "$GWT/trial" && timeout 1800 python3 -m pytest $(echo $t | tr ' ' '\n' | sort -u | while read x; do [ -f "$x" ] && echo "$x"; done) -q -x > "$P/ci_gate_pytest.log" 2>&1) \
      || { gfail "$b" "$s" "unit tests failed ($(tail -1 "$P/ci_gate_pytest.log" | cut -c1-100))"; return 1; }
    log "gate passed ${b#origin/} $s (verifier-only, tests ok)"; return 0
  fi
  local bf="$P/ci_gate_baseline_$head" a0 i0 a1 i1
  if [ ! -s "$bf" ]; then gwt "$GWT/base" HEAD || return 0; echo "$(gcount "$GWT/base" assembly) $(gcount "$GWT/base" interference)" > "$bf"; log "gate baseline $head (measured $(git -C "$GWT/base" rev-parse --short HEAD)): $(cat "$bf")"; fi
  read a0 i0 < "$bf"
  a1=$(gcount "$GWT/trial" assembly); i1=$(gcount "$GWT/trial" interference)
  $GPY decide "$b" "$s" "$a0" "$a1" "$i0" "$i1" "$P" >/dev/null || return 1
  if [[ "$b" == *-param ]] || git log --format=%B HEAD.."$b" | grep -qiE 'param|refactor'; then
    local ge=robots/revron/tools/geom_equal.py
    if [ -f "$GWT/trial/$ge" ]; then
      gwt "$GWT/base" HEAD; cp "$GWT/trial/$ge" "$GWT/base/$ge"; rm -rf "$GWT/snap"
      (cd "$GWT/base" && HEAVY_CI=1 /tmp/heavy.sh timeout 3000 python3 -u "$ge" snap "$GWT/snap") > "$P/ci_gate_geom.log" 2>&1 \
        && (cd "$GWT/trial" && HEAVY_CI=1 /tmp/heavy.sh timeout 3000 python3 -u "$ge" check "$GWT/snap"; r=$?; echo "geom_equal check exit $r"; exit $r) >> "$P/ci_gate_geom.log" 2>&1 \
        || { git -C "$GWT/base" checkout -q -- . ; git -C "$GWT/base" clean -qfd robots/revron/tools; gfail "$b" "$s" "geom_equal failed ($(tail -1 "$P/ci_gate_geom.log" | cut -c1-100))"; return 1; }
      git -C "$GWT/base" checkout -q -- . ; git -C "$GWT/base" clean -qfd robots/revron/tools
    fi
  fi
  log "gate passed ${b#origin/} $s: assembly $a0->$a1, interference $i0->$i1"; return 0
}
gated() { # skip branches already rejected at this exact sha (re-gated once HEAD moves)
  local k="${1#origin/} $(git rev-parse --short "$1") $(git rev-parse --short HEAD)"
  grep -qxF "$k" "$P/ci_gate_rejected" 2>/dev/null && return 1
  gate "$1" || { echo "$k" >> "$P/ci_gate_rejected"; return 1; }; }
[ "${RENDER_FIRST:-0}" = 1 ] && render
for i in $(seq "${START_ITER:-1}" "$MAX_ITERS"); do
  git fetch -q origin "+refs/heads/fix-*:refs/remotes/origin/fix-*" 2>>"$P/ci_push.err" || log "fetch failed"
  for b in $(heads); do
    git merge-base --is-ancestor "$b" HEAD && continue
    gated "$b" || continue
    if git merge -q --no-edit "$b" >/dev/null 2>&1; then log "iter $i merged $b $(git rev-parse --short "$b")"
    else
      f=$(git diff --name-only --diff-filter=U | grep -v -e 'spec.json$' -e 'templates/revron.json$')
      if [ -z "$f" ]; then git checkout --theirs robots/revron/spec.json robot/templates/revron.json 2>/dev/null; git add robots/revron/spec.json robot/templates/revron.json; git commit -qm "Merge $b"; log "iter $i merged $b (spec-only conflict)"
      else git merge --abort; log "conflict ${b#origin/}: $(echo $f)"; fi
    fi
  done
  (cd robots/revron/src && python3 build_revron.py >/dev/null 2>&1) && git add robots/revron/spec.json robot/templates/revron.json && git commit -qm "Revron: regenerate spec (ci loop)" >/dev/null 2>&1
  push
  sha=$(git rev-parse --short HEAD)
  if [ "$sha" = "$(cat "$P/ci_last_verified" 2>/dev/null)" ]; then  # nothing new: wait without spending an iteration
    while [ "$(git rev-parse --short HEAD)" = "$sha" ]; do
      sleep "${POLL:-120}"; git fetch -q origin "+refs/heads/fix-*:refs/remotes/origin/fix-*" 2>/dev/null
      for b in $(heads); do git merge-base --is-ancestor "$b" HEAD || ! gated "$b" || git merge -q --no-edit "$b" >/dev/null 2>&1 || { git merge --abort; log "conflict ${b#origin/}"; }; done
      [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
    done
    push; sha=$(git rev-parse --short HEAD); log "iter $i new head $sha"
  fi
  [ -f "$P/blockers_live.jsonl" ] && mv "$P/blockers_live.jsonl" "$P/blockers_live.prev.jsonl"
  out="$P/ci_verify_${i}_$sha.log"
  # full verify, one fresh process per group: an OOM in one group skips only that group, not the round
  all=$(python3 -m robot verify --list-groups 2>/dev/null | grep -E '^[a-z_]+$' | grep -v -x -e threat -e fastener_seat | paste -sd' ')
  : > "$out"; rc=0; done_n=0; failed=
  chunks="$all fastener_seat"; [ -f "${SKIP_THREAT_FILE:-/tmp/ci_skip_threat}" ] || chunks="$all threat fastener_seat"
  need=$(echo $chunks | wc -w)
  # groups run PAR at a time (own process each, shared content-keyed cache); an OOM still only loses its own group
  mkdir -p "$out.d"; rm -f "$out.d"/*
  printf '%s\n' $chunks | xargs -P "${PAR:-3}" -I{} sh -c 'ROBOT_RUN_SHA=$0 ROBOT_PROGRESS_LOG="$1/verify.log" timeout 6000 python3 -m robot verify "$2" --full --only {} --jobs 1 > "$3/{}.log" 2>&1; echo $? > "$3/{}.rc"' "$sha" "$P" "$SPEC" "$out.d"
  for chunk in $chunks; do
    cat "$out.d/$chunk.log" >> "$out" 2>/dev/null
    grep -q 'blockers,' "$out.d/$chunk.log" 2>/dev/null && done_n=$((done_n+1)) || { rc=$(cat "$out.d/$chunk.rc" 2>/dev/null); failed="$failed $chunk"; }
  done
  rm -rf "$out.d"
  rm -f "$out.part"
  if [ "$done_n" -eq 0 ]; then
    log "iter $i sha $sha: verify did not finish (rc $rc: $(grep -m1 -e Killed -e Traceback -e Error "$out" | cut -c1-120)); not counted"
    continue
  fi
  n=$(grep -c '^\[BLOCKER\]' "$out")
  groups=$(grep '^\[BLOCKER\]' "$out" | awk '{print $2}' | cut -d. -f1 | sort | uniq -c | awk '{printf "%s %s, ",$2,$1}')
  note=""; [ -n "$failed" ] && note=" (did not finish:$failed)"
  log "iter $i sha $sha: $n blockers$note (${groups%, })"
  echo "$i $sha" > "$P/ci_iter_done"; echo "$sha" > "$P/ci_last_verified"
  [ "${CI_RENDER:-1}" = 1 ] && render
  [ "$n" -eq 0 ] && [ -z "$note" ] && { log "0 blockers at $sha, stopping"; exit 0; }
  [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
done
log "reached $MAX_ITERS iterations, exiting"

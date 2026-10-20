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
# Fail closed: the trial and the baseline both regenerate the spec first; a baseline run that does not finish is
# re-measured once and otherwise holds the branch (never an accept).
# Branches touching only robot/checks/ or docs run the full robot/tests suite AND verify the check groups their modules
# feed on HEAD and on the trial; blockers that disappear are held for review (listed in the log), not auto-merged.
# *-param branches / commits starting [param] or [refactor] must also pass robots/revron/tools/geom_equal.py vs HEAD.
# GATE=0 disables. Returns 0 = merge, 1 = rejected (already logged), 2 = gate infra failure (held, retried next pass).
GWT=${GATE_WT:-/tmp/claude-0/-home-user/6d647ed2-7427-59f3-8ab5-ba663cdaf3d4/scratchpad/ci_gate}
GPY="python3 $PWD/robot/tools/ci_gate.py"
gwt() { # dir rev; rev resolved in THIS worktree (a bare "HEAD" inside -C dir would be dir's own HEAD)
  local r; r=$(git rev-parse "$2^{commit}") || return 1
  [ -d "$1" ] || git worktree add -q --detach "$1" "$r"; git -C "$1" merge --abort 2>/dev/null; git -C "$1" reset -q --hard; git -C "$1" clean -fdq
  git -C "$1" checkout -q --detach "$r" && [ "$(git -C "$1" rev-parse HEAD)" = "$r" ] || { log "gate worktree $1 not at $r"; return 1; }; }
# SHARD=1: hand groups to robot/tools/shard_worker.sh on any container sharing $P (plus PAR local workers).
# Workers rewrite their claim's content every HB s. A claim is requeued only when its content has not
# changed across two polls spanning more than STALE s of this host's clock (mtime is never trusted: on a
# network mount it comes from the server's clock/attribute cache and was judged stale ~2 min after claiming).
# Sets done_n/failed/rc and appends results to $3 in group order, exactly like the serial path.
regen() { # dir: regenerate spec.json in that worktree; non-zero (and a log line) when the build fails
  (cd "$1/robots/revron/src" && timeout "${REGEN_TIMEOUT:-3000}" python3 build_revron.py) > "$P/ci_regen.log" 2>&1 \
    || { log "regen FAILED in $1 ($(tail -1 "$P/ci_regen.log" | cut -c1-100))"; return 1; }; }
merge_one() { # branch: merge into this worktree; spec-only conflicts take the branch's spec (regen rewrites it)
  if git merge -q --no-edit "$1" >/dev/null 2>&1; then log "iter $i merged $1 $(git rev-parse --short "$1")"; return 0; fi
  local f; f=$(git diff --name-only --diff-filter=U | grep -v -e 'spec.json$' -e 'templates/revron.json$')
  if [ -z "$f" ] && [ -n "$(git diff --name-only --diff-filter=U)" ]; then
    git checkout --theirs robots/revron/spec.json robot/templates/revron.json 2>/dev/null; git add robots/revron/spec.json robot/templates/revron.json; git commit -qm "Merge $1"; log "iter $i merged $1 (spec-only conflict)"
  else git merge --abort 2>/dev/null; log "conflict ${1#origin/}: $(echo $f)"; return 1; fi; }
merge_all() { local b; for b in $(heads); do git merge-base --is-ancestor "$b" HEAD && continue; gated "$b" || continue; merge_one "$b"; done; }
regen_commit() { # regenerate the spec here and commit it; returns 1 (logged) when the build failed: do not verify
  regen . || return 1
  git add robots/revron/spec.json robot/templates/revron.json && { git diff --cached --quiet || git commit -qm "Revron: regenerate spec (ci loop)" >/dev/null; }; }
shard_verify() { # sha "groups" out
  local S="$P/shards/$1" g w pids= now m c k cur
  local -A seen=() since=()
  rm -rf "$S"; mkdir -p "$S/queue" "$S/claimed" "$S/results"
  git rev-parse HEAD > "$S/sha"
  for g in $2; do echo "$1" > "$S/queue/$g"; done
  for w in $(seq "${PAR:-1}"); do
    WORKER_ID="local$w-$$" SHARDS="$P/shards" STOP="$S/done" IDLE=999999 robot/tools/shard_worker.sh 2>>"$P/shard_local.log" & pids="$pids $!"
  done
  while :; do
    m=0; for g in $2; do [ -f "$S/results/$g.rc" ] || m=$((m+1)); done
    [ "$m" -eq 0 ] && break
    touch "$S/.now"; now=$(stat -c %Y "$S/.now" 2>/dev/null || date +%s)   # the share's clock, not ours (NFS skew)
    for c in "$S"/claimed/*; do
      [ -f "$c" ] || continue
      k=${c##*/}; g=${k##*.}; cur=$(cat "$c" 2>/dev/null)
      [ -f "$S/results/$g.rc" ] && { rm -f "$c"; continue; }
      if [ -z "${since[$k]+x}" ] || [ "${seen[$k]}" != "$cur" ]; then seen[$k]=$cur; since[$k]=$now; continue; fi
      if [ $((now - ${since[$k]})) -gt "${STALE:-900}" ]; then
        unset "seen[$k]" "since[$k]"
        [ -f "$S/results/$g.rc" ] && { rm -f "$c"; continue; }
        mv "$c" "$S/queue/$g" 2>/dev/null && log "shard $g: stale claim $k requeued"
        [ -f "$S/results/$g.rc" ] && rm -f "$S/queue/$g"  # result landed during the move
      fi
    done
    for g in $2; do [ -f "$S/results/$g.rc" ] && rm -f "$S/queue/$g"; done
    [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && break
    sleep "${SHARD_POLL:-15}"
  done
  touch "$S/done"; wait $pids 2>/dev/null
  for g in $2; do
    if [ -f "$S/results/$g.log" ]; then cat "$S/results/$g.log" >> "$3"; fi
    if grep -q 'blockers,' "$S/results/$g.log" 2>/dev/null; then done_n=$((done_n+1))
    else rc=$(cat "$S/results/$g.rc" 2>/dev/null || echo 99); failed="$failed $g"; fi
  done
}
gmode() { [ $(( ${i:-1} % ${FRESH_EVERY:-3} )) -eq 0 ] && echo fresh || echo cached; }   # every 3rd round: fresh cache
gcount() { # dir group [keep-log] -> blocker count (-1 = did not finish or a bad exit code); same cache mode for base and trial
  local c rc; c=$(mktemp -d "${TMPDIR:-/tmp}/ci_gate_cache.XXXX")  # c: log dir; cache is the shared content-keyed one (fix-K)
  local fc=; [ "$(gmode)" = fresh ] && fc="ROBOT_CACHE=$c"
  (cd "$1" && env $fc HEAVY_CI=1 /tmp/heavy.sh timeout "${GATE_TIMEOUT:-3000}" python3 -m robot verify "$SPEC" --full --only "$2" > "$c.log" 2>&1); rc=$?
  [ -n "$3" ] && cp "$c.log" "$3"
  cp "$c.log" "$P/ci_gate_$(basename "$1")_$2.log" 2>/dev/null   # kept so a rejected fixer can read the blocker lines
  $GPY count "$c.log" "$rc"; rm -rf "$c" "$c.log"; }
ginfra() { log "gate infra failure ${1#origin/} $2: $3 (held, not merged)"; return 2; }
gfail() { log "gate rejected ${1#origin/} $2: $3 (blocker lines: $P/ci_gate_trial_{assembly,interference}.log)"; printf '{"t":"%s","sha":"%s","group":"ci_gate","id":"ci_gate.rejected","parts":[],"branch":"%s","message":"[ci] gate rejected %s %s: %s"}\n' \
  "$(date -Is)" "$2" "${1#origin/}" "${1#origin/}" "$2" "$3" >> "$P/blockers_live_$(echo "${1#origin/}" | sed -E 's/^fix-(.).*/\1/' | tr a-z A-Z).jsonl"; return 1; }
gate() {
  [ "${GATE:-1}" = 1 ] || return 0
  local b=$1 s; s=$(git rev-parse --short "$b"); local head; head=$(git rev-parse --short "HEAD^{tree}")   # baselines keyed by tree: a merged trial is already measured
  local files; files=$(git diff --name-only HEAD..."$b")
  gwt "$GWT/trial" HEAD || { ginfra "$b" "$s" "trial worktree"; return; }
  if ! git -C "$GWT/trial" merge -q --no-edit "$b" >/dev/null 2>&1; then
    local u; u=$(git -C "$GWT/trial" diff --name-only --diff-filter=U); git -C "$GWT/trial" merge --abort 2>/dev/null
    [ -n "$u" ] && { log "gate: ${b#origin/} $s conflicts with HEAD ($(echo $u)); not merged"; return 1; }
    ginfra "$b" "$s" "trial merge failed without conflicts"; return
  fi
  if [ "$($GPY kind $files)" = verifier-only ]; then
    (cd "$GWT/trial" && timeout "${GATE_PYTEST_TIMEOUT:-3600}" python3 -m pytest robot/tests -q -p no:cacheprovider > "$P/ci_gate_pytest.log" 2>&1) \
      || { gfail "$b" "$s" "unit tests failed ($(tail -1 "$P/ci_gate_pytest.log" | cut -c1-100))"; return 1; }
    local known vg; known=$(python3 -m robot verify --list-groups 2>/dev/null | grep -E '^[a-z_]+$' | paste -sd' ')
    vg=$(cd "$GWT/trial" && $GPY groups "$known" $files)
    [ "$vg" = all ] && vg=$(echo "$known" | tr ' ' '\n' | grep -v -x -e threat -e claims | paste -sd' ')
    [ -z "$vg" ] && { log "gate passed ${b#origin/} $s (docs-only, tests ok)"; return 0; }
    gwt "$GWT/base" HEAD || { ginfra "$b" "$s" "base worktree"; return; }
    regen "$GWT/base" || { ginfra "$b" "$s" "base regen"; return; }
    regen "$GWT/trial" || { gfail "$b" "$s" "spec regeneration failed on the trial merge"; return 1; }
    local g bl tl; bl="$P/ci_gate_vbase.log"; tl="$P/ci_gate_vtrial.log"; : > "$bl"; : > "$tl"
    for g in $vg; do
      [ "$(gcount "$GWT/base" "$g" "$bl.g")" -ge 0 ] || { ginfra "$b" "$s" "baseline verify of $g did not finish"; return; }
      cat "$bl.g" >> "$bl"
      [ "$(gcount "$GWT/trial" "$g" "$tl.g")" -ge 0 ] || { cat "$tl.g" >> "$tl"; gfail "$b" "$s" "verify of $g did not finish on the trial"; return 1; }
      cat "$tl.g" >> "$tl"
    done
    rm -f "$bl.g" "$tl.g"
    if ! $GPY vanished "$bl" "$tl" > "$P/ci_gate_vanished.log"; then
      gfail "$b" "$s" "needs review: $(grep -c . "$P/ci_gate_vanished.log") blockers disappeared on [$vg] ($(head -3 "$P/ci_gate_vanished.log" | cut -c1-80 | paste -sd'|'))"; return 1
    fi
    log "gate passed ${b#origin/} $s (verifier-only, full tests + verify of [$vg]: no blocker disappeared)"; return 0
  fi
  regen "$GWT/trial" || { gfail "$b" "$s" "spec regeneration failed on the trial merge"; return 1; }
  local bf="$P/ci_gate_baseline_${head}_$(gmode)" a0 i0 a1 i1 k
  if [ ! -s "$bf" ]; then
    gwt "$GWT/base" HEAD || { ginfra "$b" "$s" "base worktree"; return; }
    regen "$GWT/base" || { ginfra "$b" "$s" "base regen"; return; }
    for k in 1 2; do   # a baseline that did not finish is re-measured once, then the branch is held (never accepted)
      a0=$(gcount "$GWT/base" assembly); i0=$(gcount "$GWT/base" interference)
      [ "$a0" -ge 0 ] && [ "$i0" -ge 0 ] && break
    done
    log "gate baseline $head ($(gmode), measured $(git -C "$GWT/base" rev-parse --short HEAD)): $a0 $i0"
    [ "$a0" -ge 0 ] && [ "$i0" -ge 0 ] || { ginfra "$b" "$s" "baseline did not finish twice ($a0 $i0)"; return; }
    echo "$a0 $i0" > "$bf"
  fi
  read a0 i0 < "$bf"
  a1=$(gcount "$GWT/trial" assembly); i1=$(gcount "$GWT/trial" interference)
  [ "$a1" -ge 0 ] && [ "$i1" -ge 0 ] && echo "$a1 $i1" > "$P/ci_gate_baseline_$(git -C "$GWT/trial" rev-parse --short "HEAD^{tree}")_$(gmode)"
  $GPY decide "$b" "$s" "$a0" "$a1" "$i0" "$i1" "$P" >/dev/null || return 1
  if [[ "$b" == *-param ]] || ! git log --no-merges --format=%s HEAD.."$b" | grep -qvE '^\[(param|refactor)\]'; then
    local ge=robots/revron/tools/geom_equal.py
    if [ -f "$GWT/trial/$ge" ]; then
      gwt "$GWT/base" HEAD || { ginfra "$b" "$s" "base worktree (geom_equal)"; return; }
      cp "$GWT/trial/$ge" "$GWT/base/$ge"; rm -rf "$GWT/snap"
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
  gate "$1"; local r=$?
  [ $r -eq 0 ] && return 0
  [ $r -eq 1 ] && echo "$k" >> "$P/ci_gate_rejected"   # infra failures (2) are held and re-gated next pass
  return 1; }
[ "${RENDER_FIRST:-0}" = 1 ] && render
for i in $(seq "${START_ITER:-1}" "$MAX_ITERS"); do
  git fetch -q origin "+refs/heads/fix-*:refs/remotes/origin/fix-*" 2>>"$P/ci_push.err" || log "fetch failed"
  merge_all
  regen_commit || { push; continue; }   # build failed (logged): never verify a stale spec
  push
  sha=$(git rev-parse --short HEAD)
  if [ "$sha" = "$(cat "$P/ci_last_verified" 2>/dev/null)" ]; then  # nothing new: wait without spending an iteration
    while [ "$(git rev-parse --short HEAD)" = "$sha" ]; do
      sleep "${POLL:-120}"; git fetch -q origin "+refs/heads/fix-*:refs/remotes/origin/fix-*" 2>/dev/null
      merge_all
      [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
    done
    regen_commit || { push; continue; }   # same regeneration and conflict handling as the main pass
    push; sha=$(git rev-parse --short HEAD); log "iter $i new head $sha"
  fi
  [ -f "$P/blockers_live.jsonl" ] && mv "$P/blockers_live.jsonl" "$P/blockers_live.prev.jsonl"
  out="$P/ci_verify_${i}_$sha.log"
  # full verify, one fresh process per group: an OOM in one group skips only that group, not the round
  all=$(python3 -m robot verify --list-groups 2>/dev/null | grep -E '^[a-z_]+$' | grep -v -x -e threat -e fastener_seat | paste -sd' ')
  : > "$out"; rc=0; done_n=0; failed=
  chunks="$all fastener_seat"; [ -f "${SKIP_THREAT_FILE:-/tmp/ci_skip_threat}" ] || chunks="$all threat fastener_seat"
  need=$(echo $chunks | wc -w)
  if [ "${SHARD:-0}" = 1 ]; then shard_verify "$sha" "$chunks" "$out"; else
  # groups run PAR at a time (own process each, shared content-keyed cache); an OOM still only loses its own group
  mkdir -p "$out.d"; rm -f "$out.d"/*
  printf '%s\n' $chunks | xargs -P "${PAR:-3}" -I{} sh -c 'ROBOT_RUN_SHA=$0 ROBOT_PROGRESS_LOG="$1/verify.log" timeout 6000 python3 -m robot verify "$2" --full --only {} --jobs 1 > "$3/{}.log" 2>&1; echo $? > "$3/{}.rc"' "$sha" "$P" "$SPEC" "$out.d"
  for chunk in $chunks; do
    cat "$out.d/$chunk.log" >> "$out" 2>/dev/null
    grep -q 'blockers,' "$out.d/$chunk.log" 2>/dev/null && done_n=$((done_n+1)) || { rc=$(cat "$out.d/$chunk.rc" 2>/dev/null); failed="$failed $chunk"; }
  done
  rm -rf "$out.d"
  fi
  rm -f "$out.part"
  if [ "$done_n" -eq 0 ]; then
    log "iter $i sha $sha: verify did not finish (rc $rc: $(grep -m1 -e Killed -e Traceback -e Error "$out" | cut -c1-120)); not counted"
    continue
  fi
  n=$(grep -c '^\[BLOCKER\]' "$out")
  groups=$(grep '^\[BLOCKER\]' "$out" | awk '{print $2}' | cut -d. -f1 | sort | uniq -c | awk '{printf "%s %s, ",$2,$1}')
  note=""; [ -n "$failed" ] && note=" (did not finish:$failed)"
  log "iter $i sha $sha: $n blockers$note (${groups%, })"
  echo "$i $sha" > "$P/ci_iter_done"
  # only a complete round marks the sha verified; groups that did not finish are retried on the same sha
  [ -z "$failed" ] && echo "$sha" > "$P/ci_last_verified"
  [ "${CI_RENDER:-1}" = 1 ] && render
  [ "$n" -eq 0 ] && [ -z "$note" ] && { log "0 blockers at $sha, stopping"; exit 0; }
  [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
done
log "reached $MAX_ITERS iterations, exiting"

#!/bin/bash
# [fix-G] All fix-* heads pass the combined gate_all() (below) before it is merged; see robot/tools/ci_gate.py.
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
# [fix-G] combined merge gate (gate_all): ONE trial merge of all updated fix-* heads, one spec build (cached by input
# tree hash), assembly + interference in parallel; not worse than HEAD's tree-keyed baseline -> all merge, else bisect
# with halves gated in parallel until the offenders are found (rejected; blocker lines in $P/ci_gate_<branch>_<group>.log).
# Branches touching only robot/checks/ or docs skip the verify but must pass the pytest files they touch.
# *-param / all-[refactor] branches must also pass robots/revron/tools/geom_equal.py vs HEAD.
# Infra failures hold a branch (neither merged nor rejected). GATE=0 disables.
GWT=${GATE_WT:-/tmp/claude-0/-home-user/6d647ed2-7427-59f3-8ab5-ba663cdaf3d4/scratchpad/ci_gate}
GPY="python3 $PWD/robot/tools/ci_gate.py"
gwt() { # dir rev; rev resolved in THIS worktree (a bare "HEAD" inside -C dir would be dir's own HEAD)
  local r; r=$(git rev-parse "$2^{commit}") || return 1
  [ -d "$1" ] || for t in 1 2 3 4 5; do git worktree add -q --detach "$1" "$r" 2>/dev/null && break; sleep $t; done; git -C "$1" merge --abort 2>/dev/null; git -C "$1" reset -q --hard; git -C "$1" clean -fdq
  git -C "$1" checkout -q --detach "$r" && [ "$(git -C "$1" rev-parse HEAD)" = "$r" ] || { log "gate worktree $1 not at $r"; return 1; }; }
# SHARD=1: hand groups to robot/tools/shard_worker.sh on any container sharing $P (plus PAR local workers).
# Workers rewrite their claim's content every HB s. A claim is requeued only when its content has not
# changed across two polls spanning more than STALE s of this host's clock (mtime is never trusted: on a
# network mount it comes from the server's clock/attribute cache and was judged stale ~2 min after claiming).
# Sets done_n/failed/rc and appends results to $3 in group order, exactly like the serial path.
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
    now=$(date +%s)
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
gcount() { # dir group label -> blocker count (-1 = did not finish); log kept at $P/ci_gate_<label>_<group>.log
  local c; c=$(mktemp -d "${TMPDIR:-/tmp}/ci_gate_cache.XXXX")  # c: log dir only; cache is the shared content-keyed one (fix-K)
  local fc=; [ $(( ${i:-1} % ${FRESH_EVERY:-3} )) -eq 0 ] && fc="ROBOT_CACHE=$c"   # every 3rd round: fresh cache spot check
  (cd "$1" && env $fc HEAVY_CI=1 /tmp/heavy.sh timeout "${GATE_TIMEOUT:-3000}" python3 -m robot verify "$SPEC" --full --only "$2" > "$c.log" 2>&1)
  cp "$c.log" "$P/ci_gate_${3:-$(basename "$1")}_$2.log" 2>/dev/null   # kept so a rejected fixer can read the blocker lines
  $GPY count "$c.log"; rm -rf "${c:?}" "${c:?}.log"; }
gpair() { # dir label -> "assembly interference", both groups in parallel
  local t; t=$(mktemp -d "${TMPDIR:-/tmp}/ci_gpair.XXXX")
  gcount "$1" assembly "$2" > "$t/a" & gcount "$1" interference "$2" > "$t/i" & wait
  echo "$(cat "$t/a") $(cat "$t/i")"; rm -rf "${t:?}"; }
# spec regeneration cached by the git tree hashes of robots/revron/src and robot (the build inputs) of dir's HEAD
spec_build() { # dir
  local k; k=$(echo "$(git -C "$1" rev-parse HEAD:robots/revron/src) $(git -C "$1" rev-parse HEAD:robot)" | sha1sum | cut -c1-16)
  local C="$P/spec_cache/$k"
  if [ -s "$C/spec.json" ] && [ -s "$C/revron.json" ]; then cp "$C/spec.json" "$1/robots/revron/spec.json"; cp "$C/revron.json" "$1/robot/templates/revron.json"; return 0; fi
  (cd "$1/robots/revron/src" && python3 build_revron.py >/dev/null 2>&1) || return 0   # build failure: verify what is committed
  mkdir -p "$P/spec_cache"; local t; t=$(mktemp -d "$P/spec_cache/.tmp.XXXX") || return 0
  if cp "$1/robots/revron/spec.json" "$t/spec.json" && cp "$1/robot/templates/revron.json" "$t/revron.json" && mv -T "$t" "$C" 2>/dev/null; then :; else rm -rf "${t:?}"; fi; }
gfail() { log "gate rejected ${1#origin/} $2: $3 (blocker lines: $P/ci_gate_${1#origin/}_{assembly,interference}.log)"; printf '{"t":"%s","sha":"%s","group":"ci_gate","id":"ci_gate.rejected","parts":[],"branch":"%s","message":"[ci] gate rejected %s %s: %s"}\n' \
  "$(date -Is)" "$2" "${1#origin/}" "${1#origin/}" "$2" "$3" >> "$P/blockers_live_$(echo "${1#origin/}" | sed -E 's/^fix-(.).*/\1/' | tr a-z A-Z).jsonl"; return 1; }
baseline() { # -> "a0 i0" for HEAD's tree (cached by tree hash; a merged trial is already measured)
  local bf="$P/ci_gate_baseline_$(git rev-parse --short "HEAD^{tree}")"
  if [ ! -s "$bf" ]; then gwt "$GWT/base" HEAD || return 1; spec_build "$GWT/base"; gpair "$GWT/base" base > "$bf.tmp" && mv "$bf.tmp" "$bf"; log "gate baseline $(git rev-parse --short "HEAD^{tree}"): $(cat "$bf")"; fi
  cat "$bf"; }
gverifier() { # branch -> 0 pass, 1 rejected, 2 infra. checks-only branches: the pytest files they touch
  local b=$1 s d="$GWT/v_${1#origin/}" files t m f; s=$(git rev-parse --short "$b"); files=$(git diff --name-only HEAD..."$b")
  gwt "$d" HEAD || return 2; git -C "$d" merge -q --no-edit "$b" >/dev/null 2>&1 || { git -C "$d" merge --abort; return 2; }
  t=$(echo "$files" | grep -E '^robot/tests/test_.*\.py$'); for f in $(echo "$files" | grep '^robot/checks/'); do
    m=$(basename "$f" .py); [ -f "$d/robot/tests/test_$m.py" ] && t="$t robot/tests/test_$m.py"; done
  [ -z "$t" ] && t=robot/tests/test_checks.py
  (cd "$d" && timeout 1800 python3 -m pytest $(echo $t | tr ' ' '\n' | sort -u | while read x; do [ -f "$x" ] && echo "$x"; done) -q -x > "$P/ci_gate_pytest_${b#origin/}.log" 2>&1) \
    || { gfail "$b" "$s" "unit tests failed ($(tail -1 "$P/ci_gate_pytest_${b#origin/}.log" | cut -c1-100))"; return 1; }
  log "gate passed ${b#origin/} $s (verifier-only, tests ok)"; return 0; }
ggeom() { # branch -> 0 ok; [param]/[refactor] branches must be geometry-identical vs HEAD (own single-branch trial)
  local b=$1 s ge=robots/revron/tools/geom_equal.py d="$GWT/geom"; s=$(git rev-parse --short "$b")
  [[ "$b" == *-param ]] || ! git log --no-merges --format=%s HEAD.."$b" | grep -qvE '^\[refactor\]' || return 0
  gwt "$d" HEAD || return 2; git -C "$d" merge -q --no-edit "$b" >/dev/null 2>&1 || { git -C "$d" merge --abort; return 2; }
  [ -f "$d/$ge" ] || return 0; spec_build "$d"
  gwt "$GWT/base" HEAD || return 2; spec_build "$GWT/base"; cp "$d/$ge" "$GWT/base/$ge"; rm -rf "${GWT:?}/snap"
  (cd "$GWT/base" && HEAVY_CI=1 /tmp/heavy.sh timeout 3000 python3 -u "$ge" snap "$GWT/snap") > "$P/ci_gate_geom.log" 2>&1 \
    && (cd "$d" && HEAVY_CI=1 /tmp/heavy.sh timeout 3000 python3 -u "$ge" check "$GWT/snap"; r=$?; echo "geom_equal check exit $r"; exit $r) >> "$P/ci_gate_geom.log" 2>&1
  local r=$?; git -C "$GWT/base" checkout -q -- . ; git -C "$GWT/base" clean -qfd robots/revron/tools
  [ $r = 0 ] || { cp "$P/ci_gate_geom.log" "$P/ci_gate_${b#origin/}_geom.log"; gfail "$b" "$s" "geom_equal failed ($(tail -1 "$P/ci_gate_geom.log" | cut -c1-100))"; return 1; }; }
# gate_set LABEL A0 I0 B...: trial-merge B... into $GWT/t_LABEL, regenerate the spec (cached), run assembly+interference
# in parallel. Not worse than A0/I0 -> "pass b" for all. Worse -> a single branch is rejected, a set is split in two
# halves gated in PARALLEL (own worktrees), recursively (mirrors bisect() in ci_gate.py). Writes "pass|reject|hold|skip b" to $GR/LABEL.
gate_set() {
  local L=$1 a0=$2 i0=$3; shift 3; local out="$GR/$L" d="$GWT/t_$L" b m=
  : > "$out"
  gwt "$d" HEAD || { for b; do echo "hold $b"; done > "$out"; return; }
  for b; do
    if git -C "$d" merge -q --no-edit "$b" >/dev/null 2>&1; then m="$m $b"
    else git -C "$d" merge --abort 2>/dev/null; [ "$L" = r ] && log "conflict ${b#origin/} (in combined gate trial)"; echo "skip $b" >> "$out"; fi
  done
  set -- $m; [ $# -eq 0 ] && return
  spec_build "$d"
  local lab="set$L"; [ $# -eq 1 ] && lab=${1#origin/}
  local a1 i1; read a1 i1 < <(gpair "$d" "$lab")
  [ -n "$i1" ] || { for b; do echo "hold $b"; done >> "$out"; return; }
  if $GPY ok "$a0" "$a1" "$i0" "$i1"; then
    echo "$a1 $i1" > "$P/ci_gate_baseline_$(git -C "$d" rev-parse --short "HEAD^{tree}")"
    log "gate set $L passed ($#: $(echo ${*#origin/})): assembly $a0->$a1, interference $i0->$i1"
    for b; do echo "pass $b"; done >> "$out"; return
  fi
  log "gate set $L worse ($#: $(echo ${*#origin/})): assembly $a0->$a1, interference $i0->$i1"
  if [ $# -eq 1 ]; then
    $GPY decide "$1" "$(git rev-parse --short "$1")" "$a0" "$a1" "$i0" "$i1" "$P" >/dev/null
    log "gate rejected ${1#origin/}: blocker lines in $P/ci_gate_${1#origin/}_{assembly,interference}.log"
    echo "reject $1" >> "$out"; return
  fi
  local h1 h2; { read h1; read h2; } < <($GPY halves "$@")
  gate_set "${L}0" "$a0" "$i0" $h1 & gate_set "${L}1" "$a0" "$i0" $h2 & wait
  cat "$GR/${L}0" >> "$out"
  if ! grep -qv '^pass ' "$GR/${L}0" "$GR/${L}1"; then sed 's/^pass /hold /' "$GR/${L}1" >> "$out"; log "gate set $L: halves pass alone but not together, holding: $(echo $h2)"
  else cat "$GR/${L}1" >> "$out"; fi
}
# combined gate for all candidate heads; prints the branches approved for merging. GATE=0 disables.
gate_all() {
  [ "${GATE:-1}" = 1 ] || { printf '%s\n' "$@"; return; }
  local b k geo= ok=
  for b; do
    k="${b#origin/} $(git rev-parse --short "$b") $(git rev-parse --short HEAD)"
    grep -qxF "$k" "$P/ci_gate_rejected" 2>/dev/null && continue   # rejected at this exact sha (re-gated once HEAD moves)
    if [ "$($GPY kind $(git diff --name-only HEAD..."$b"))" = verifier-only ]; then
      gverifier "$b"; case $? in 0) ok="$ok $b";; 1) echo "$k" >> "$P/ci_gate_rejected";; *) log "gate hold ${b#origin/}: infra failure";; esac
    else geo="$geo $b"; fi
  done
  if [ -n "$geo" ]; then
    local base; base=$(baseline) || { log "gate hold (baseline infra failure):$geo"; printf '%s\n' $ok; return; }
    GR=$(mktemp -d "${TMPDIR:-/tmp}/ci_gr.XXXX")
    gate_set r $base $geo
    for b in $(awk '$1=="reject"{print $2}' "$GR/r"); do echo "${b#origin/} $(git rev-parse --short "$b") $(git rev-parse --short HEAD)" >> "$P/ci_gate_rejected"; done
    for b in $(awk '$1=="hold"{print $2}' "$GR/r"); do log "gate hold ${b#origin/} (infra failure or interaction; retried next round)"; done
    for b in $(awk '$1=="pass"{print $2}' "$GR/r"); do
      ggeom "$b"; case $? in 0) ok="$ok $b";; 1) echo "${b#origin/} $(git rev-parse --short "$b") $(git rev-parse --short HEAD)" >> "$P/ci_gate_rejected";; *) log "gate hold ${b#origin/}: geom infra failure";; esac
    done
    rm -rf "${GR:?}"
  fi
  printf '%s\n' $ok; }
mergeb() { # branch: merge into HEAD (spec-only conflicts take theirs; real conflicts aborted and logged)
  local b=$1 f
  if git merge -q --no-edit "$b" >/dev/null 2>&1; then log "iter $i merged $b $(git rev-parse --short "$b")"
  else
    f=$(git diff --name-only --diff-filter=U | grep -v -e 'spec.json$' -e 'templates/revron.json$')
    if [ -z "$f" ]; then git checkout --theirs robots/revron/spec.json robot/templates/revron.json 2>/dev/null; git add robots/revron/spec.json robot/templates/revron.json; git commit -qm "Merge $b"; log "iter $i merged $b (spec-only conflict)"
    else git merge --abort; log "conflict ${b#origin/}: $(echo $f)"; fi
  fi; }
cands() { for b in $(heads); do git merge-base --is-ancestor "$b" HEAD || echo "$b"; done; }
[ "${RENDER_FIRST:-0}" = 1 ] && render
for i in $(seq "${START_ITER:-1}" "$MAX_ITERS"); do
  git fetch -q origin "+refs/heads/fix-*:refs/remotes/origin/fix-*" 2>>"$P/ci_push.err" || log "fetch failed"
  c=$(cands); [ -n "$c" ] && for b in $(gate_all $c); do mergeb "$b"; done
  (cd robots/revron/src && python3 build_revron.py >/dev/null 2>&1) && git add robots/revron/spec.json robot/templates/revron.json && git commit -qm "Revron: regenerate spec (ci loop)" >/dev/null 2>&1
  push
  sha=$(git rev-parse --short HEAD)
  if [ "$sha" = "$(cat "$P/ci_last_verified" 2>/dev/null)" ]; then  # nothing new: wait without spending an iteration
    while [ "$(git rev-parse --short HEAD)" = "$sha" ]; do
      sleep "${POLL:-120}"; git fetch -q origin "+refs/heads/fix-*:refs/remotes/origin/fix-*" 2>/dev/null
      c=$(cands); [ -n "$c" ] && for b in $(gate_all $c); do mergeb "$b"; done
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
  echo "$i $sha" > "$P/ci_iter_done"; echo "$sha" > "$P/ci_last_verified"
  [ "${CI_RENDER:-1}" = 1 ] && render
  [ "$n" -eq 0 ] && [ -z "$note" ] && { log "0 blockers at $sha, stopping"; exit 0; }
  [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
done
log "reached $MAX_ITERS iterations, exiting"

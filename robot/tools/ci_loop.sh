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
# Fail closed: every run must finish (a -1 count, baseline or trial, is never an accept; an unfinished baseline is
# re-measured once, then the round's geometry branches are held); a failed spec build holds, never verifies stale.
# Branches touching only robot/checks/ or docs run the full robot/tests suite AND verify the check groups their modules
# feed on HEAD and on the trial; blockers that disappear are rejected as "needs review" (listed in the log).
# *-param / all-[param]/[refactor] branches must also pass robots/revron/tools/geom_equal.py vs HEAD.
# Infra failures hold a branch (neither merged nor rejected). GATE=0 disables.
GWT=${GATE_WT:-/tmp/claude-0/-home-user/6d647ed2-7427-59f3-8ab5-ba663cdaf3d4/scratchpad/ci_gate}
GPY="python3 $PWD/robot/tools/ci_gate.py"
gwt() { # dir rev; rev resolved in THIS worktree (a bare "HEAD" inside -C dir would be dir's own HEAD)
  local r; r=$(git rev-parse "$2^{commit}") || return 1
  [ -d "$1" ] || for t in 1 2 3 4 5; do git worktree add -q --detach "$1" "$r" 2>/dev/null && break; sleep $t; done; git -C "$1" merge --abort 2>/dev/null; git -C "$1" reset -q --hard; git -C "$1" clean -fdq
  git -C "$1" checkout -q --detach "$r" && [ "$(git -C "$1" rev-parse HEAD)" = "$r" ] || { log "gate worktree $1 not at $r"; return 1; }; }
# SHARD=1 (default; SHARD=0 = serial): hand groups to robot/tools/shard_worker.sh on any container sharing $P (plus PAR local workers).
# Workers rewrite their claim's content every HB s. A claim is requeued only when its content has not
# changed across two polls spanning more than STALE s of this host's clock (mtime is never trusted: on a
# network mount it comes from the server's clock/attribute cache and was judged stale ~2 min after claiming).
# Extra workers on a fixer container (one command, from any checkout of the repo with /mnt/project-files mounted):
#   nohup robot/tools/shard_worker.sh >> /mnt/project-files/robot-cad/b123d/progress/shard_$(hostname).log 2>&1 &
# Sets done_n/failed/rc and appends results to $3 in group order, exactly like the serial path.
# $4: full sha the workers check out (default HEAD). RESUME=1 with a shard dir already for that sha (a restarted loop):
# keep its results and claims (dead claims are requeued by the STALE check below) and queue only groups with neither.
shard_verify() { # sha "groups" out [fullsha]
  local S="$P/shards/$1" g w pids= now m c k cur f=${4:-$(git rev-parse HEAD)}
  local -A seen=() since=()
  if [ "${RESUME:-0}" = 1 ] && [ "$(cat "$S/sha" 2>/dev/null)" = "$f" ]; then
    rm -f "$S/done"; mkdir -p "$S/queue" "$S/claimed" "$S/results"
    for g in $2; do [ -f "$S/results/$g.rc" ] || [ -f "$S/queue/$g" ] || ls "$S/claimed/"*".$g" >/dev/null 2>&1 || echo "$1" > "$S/queue/$g"; done
  else
    rm -rf "$S"; mkdir -p "$S/queue" "$S/claimed" "$S/results"
    echo "$f" > "$S/sha"
    for g in $2; do echo "$1" > "$S/queue/$g"; done
  fi
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
      if [ $((now - ${since[$k]})) -gt "${STALE:-180}" ]; then
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
  touch "$S/done"; [ -n "$pids" ] && wait $pids 2>/dev/null
  for g in $2; do
    if [ -f "$S/results/$g.log" ]; then cat "$S/results/$g.log" >> "$3"; fi
    if grep -q 'blockers,' "$S/results/$g.log" 2>/dev/null; then done_n=$((done_n+1))
    else rc=$(cat "$S/results/$g.rc" 2>/dev/null || echo 99); failed="$failed $g"; fi
  done
}
gmode() { [ $(( ${i:-1} % ${FRESH_EVERY:-3} )) -eq 0 ] && echo fresh || echo cached; }   # every 3rd round: fresh cache
gcount() { # dir group label -> blocker count (-1 = did not finish or bad exit code); log kept at $P/ci_gate_<label>_<group>.log
  local c rc; c=$(mktemp -d "${TMPDIR:-/tmp}/ci_gate_cache.XXXX")  # c: log dir only; cache is the shared content-keyed one (fix-K)
  local fc=; [ "$(gmode)" = fresh ] && fc="ROBOT_CACHE=$c"   # base and trial of one round use the same mode
  (cd "$1" && env $fc HEAVY_CI=1 /tmp/heavy.sh timeout "${GATE_TIMEOUT:-3000}" python3 -m robot verify "$SPEC" --full --only "$2" > "$c.log" 2>&1); rc=$?
  cp "$c.log" "$P/ci_gate_${3:-$(basename "$1")}_$2.log" 2>/dev/null   # kept so a rejected fixer can read the blocker lines
  $GPY count "$c.log" "$rc"; rm -rf "${c:?}" "${c:?}.log"; }
gpair() { # dir label -> "assembly interference", both groups in parallel
  local t; t=$(mktemp -d "${TMPDIR:-/tmp}/ci_gpair.XXXX")
  gcount "$1" assembly "$2" > "$t/a" & gcount "$1" interference "$2" > "$t/i" & wait
  echo "$(cat "$t/a") $(cat "$t/i")"; rm -rf "${t:?}"; }
# spec regeneration cached by the git tree hashes of robots/revron/src and robot (the build inputs) of dir's HEAD
spec_build() { # dir
  local k; k=$(echo "$(git -C "$1" rev-parse HEAD:robots/revron/src) $(git -C "$1" rev-parse HEAD:robot)" | sha1sum | cut -c1-16)
  local C="$P/spec_cache/$k"
  if [ -s "$C/spec.json" ] && [ -s "$C/revron.json" ]; then cp "$C/spec.json" "$1/robots/revron/spec.json"; cp "$C/revron.json" "$1/robot/templates/revron.json"; return 0; fi
  (cd "$1/robots/revron/src" && timeout "${REGEN_TIMEOUT:-3000}" python3 build_revron.py) > "$P/ci_regen_$(basename "$1").log" 2>&1 \
    || { log "regen FAILED in $1 ($(tail -1 "$P/ci_regen_$(basename "$1").log" | cut -c1-100))"; return 1; }   # never verify a stale spec
  mkdir -p "$P/spec_cache"; local t; t=$(mktemp -d "$P/spec_cache/.tmp.XXXX") || return 0
  if cp "$1/robots/revron/spec.json" "$t/spec.json" && cp "$1/robot/templates/revron.json" "$t/revron.json" && mv -T "$t" "$C" 2>/dev/null; then :; else rm -rf "${t:?}"; fi; }
gfail() { log "gate rejected ${1#origin/} $2: $3 (blocker lines: $P/ci_gate_${1#origin/}_{assembly,interference}.log)"; printf '{"t":"%s","sha":"%s","group":"ci_gate","id":"ci_gate.rejected","parts":[],"branch":"%s","message":"[ci] gate rejected %s %s: %s"}\n' \
  "$(date -Is)" "$2" "${1#origin/}" "${1#origin/}" "$2" "$3" >> "$P/blockers_live_$(echo "${1#origin/}" | sed -E 's/^fix-(.).*/\1/' | tr a-z A-Z).jsonl"; return 1; }
baseline() { # -> "a0 i0" for HEAD's tree (cached by tree hash + cache mode; a merged trial is already measured)
  # an unfinished run (-1) is re-measured once; still -1 -> return 1 (hold), never cached, never an accept
  local bf="$P/ci_gate_baseline_$(git rev-parse --short "HEAD^{tree}")_$(gmode)" a i k
  if [ ! -s "$bf" ]; then
    gwt "$GWT/base" HEAD || return 1; spec_build "$GWT/base" || return 1
    for k in 1 2; do read a i < <(gpair "$GWT/base" base); [ "${a:--1}" -ge 0 ] && [ "${i:--1}" -ge 0 ] && break; done
    log "gate baseline $(git rev-parse --short "HEAD^{tree}") ($(gmode)): $a $i"
    [ "${a:--1}" -ge 0 ] && [ "${i:--1}" -ge 0 ] || { log "gate baseline did not finish twice ($a $i)"; return 1; }
    echo "$a $i" > "$bf.tmp" && mv "$bf.tmp" "$bf"
  fi
  cat "$bf"; }
# unit_tests DIR LOG -> 0 pass, 1 failed, 2 infra. robot/tests of DIR's HEAD (a local trial merge) run as a 'unit' shard
# ticket, so any shard worker can take it: the commit is pushed to origin ci-unit/<tree> for remote checkouts. The result is
# cached by the merged TREE hash ($P/ci_unit_cache/<tree>), so a candidate set already tested (e.g. before a container
# restart; a re-made merge commit has a new sha but the same tree) is never re-tested. Only pass/fail is cached, never infra.
unit_tests() {
  local d=$1 lg=$2 tr c cf r ref done_n=0 failed= rc=0
  tr=$(git -C "$d" rev-parse "HEAD^{tree}") || return 2; c=$(git -C "$d" rev-parse HEAD); cf="$P/ci_unit_cache/$tr"
  if [ -s "$cf" ] && [ -f "$cf.log" ]; then cp "$cf.log" "$lg"; log "unit tests of tree ${tr:0:12}: cached result $(cat "$cf")"; return "$(cat "$cf")"; fi
  ref=ci-unit/${tr:0:16}
  [ "${UNIT_PUSH:-1}" = 1 ] && { git -C "$d" push -q -f origin "$c:refs/heads/$ref" 2>>"$P/ci_push.err" || log "unit: push of $ref failed (local workers only)"; }
  # split into UNIT_SHARDS tickets unit-0..unit-N-1 by test file, balanced by past per-file durations
  # ($P/ci_unit_durations.json, learned from each shard's --durations output); combined: any fail -> 1, else any infra -> 2
  local S="$P/shards/unit-${tr:0:16}" k gs= rs=
  if [ "$(cat "$S/sha" 2>/dev/null)" != "$c" ] || [ ! -d "$S/unit_files" ]; then
    rm -rf "$S"; mkdir -p "$S/unit_files"; echo "$c" > "$S/sha"; echo "${UNIT_TIMEOUT:-14400}" > "$S/unit_timeout"
    k=0; while read -r l; do [ -n "$l" ] && echo "$l" > "$S/unit_files/unit-$k" && k=$((k+1)); done \
      < <(cd "$d" && $GPY unitsplit "${UNIT_SHARDS:-8}" "$P/ci_unit_durations.json" $(ls robot/tests/test_*.py))
  fi
  gs=$(ls "$S/unit_files" | sort -t- -k2 -n | paste -sd' ')
  : > "$lg"; RESUME=1 shard_verify "unit-${tr:0:16}" "$gs" "$lg" "$c"
  for k in $gs; do rs="$rs $k=$(cat "$S/results/$k.rc" 2>/dev/null || echo 99)"; done
  $GPY unitdur "$P/ci_unit_durations.json" "$S"/results/unit-*.log 2>/dev/null
  $GPY unitcombine "$S/results" $rs; r=$?; log "unit tests of tree ${tr:0:12}:$rs -> $r"
  [ $r -lt 2 ] && { mkdir -p "$P/ci_unit_cache"; cp "$lg" "$cf.log.$$" && mv -f "$cf.log.$$" "$cf.log" && echo $r > "$cf.$$" && mv -f "$cf.$$" "$cf"; }
  rm -rf "${P:?}/shards/unit-${tr:0:16}"   # collected (an infra result is retried with a fresh ticket next time)
  [ "${UNIT_PUSH:-1}" = 1 ] && git -C "$d" push -q origin ":refs/heads/$ref" 2>/dev/null
  return $r; }
gverifier() { # branch -> 0 pass, 1 rejected, 2 infra. checks-only: full robot/tests, then verify the touched groups on
  # HEAD and on the trial; a blocker present on HEAD that is gone on the trial needs review (rejected, listed)
  local b=$1 s d="$GWT/v_${1#origin/}" bd="$GWT/vb_${1#origin/}" files u; s=$(git rev-parse --short "$b"); files=$(git diff --name-only HEAD..."$b")
  gwt "$d" HEAD || return 2
  if ! git -C "$d" merge -q --no-edit "$b" >/dev/null 2>&1; then
    u=$(git -C "$d" diff --name-only --diff-filter=U); git -C "$d" merge --abort 2>/dev/null
    [ -n "$u" ] && log "conflict ${b#origin/} (verifier gate): $(echo $u)"; return 2; fi
  unit_tests "$d" "$P/ci_gate_pytest_${b#origin/}.log"; case $? in 0) ;; 1)
    gfail "$b" "$s" "unit tests failed ($(tail -1 "$P/ci_gate_pytest_${b#origin/}.log" | cut -c1-100))"; return 1;; *) log "gate hold ${b#origin/}: unit tests did not finish"; return 2;; esac
  local known vg g x bl="$P/ci_gate_vbase_${b#origin/}.log" tl="$P/ci_gate_vtrial_${b#origin/}.log"
  known=$(python3 -m robot verify --list-groups 2>/dev/null | grep -E '^[a-z_]+$' | paste -sd' ')
  vg=$(cd "$d" && $GPY groups "$known" $files)
  [ "$vg" = all ] && vg=$(echo "$known" | tr ' ' '\n' | grep -v -x -e threat -e claims | paste -sd' ')
  [ -z "$vg" ] && { log "gate passed ${b#origin/} $s (docs-only, tests ok)"; return 0; }
  gwt "$bd" HEAD || return 2; spec_build "$bd" || return 2
  spec_build "$d" || { gfail "$b" "$s" "spec regeneration failed on the trial merge"; return 1; }
  : > "$bl"; : > "$tl"
  for g in $vg; do
    x=$(gcount "$bd" "$g" "vbase_${b#origin/}"); cat "$P/ci_gate_vbase_${b#origin/}_$g.log" >> "$bl" 2>/dev/null
    [ "$x" -ge 0 ] || { log "gate hold ${b#origin/}: baseline verify of $g did not finish"; return 2; }
    x=$(gcount "$d" "$g" "${b#origin/}"); cat "$P/ci_gate_${b#origin/}_$g.log" >> "$tl" 2>/dev/null
    [ "$x" -ge 0 ] || { gfail "$b" "$s" "verify of $g did not finish on the trial"; return 1; }
  done
  if ! $GPY vanished "$bl" "$tl" > "$P/ci_gate_vanished_${b#origin/}.log"; then
    gfail "$b" "$s" "needs review: $(grep -c . "$P/ci_gate_vanished_${b#origin/}.log") blockers disappeared on [$vg] ($(head -3 "$P/ci_gate_vanished_${b#origin/}.log" | cut -c1-80 | paste -sd'|'))"; return 1
  fi
  log "gate passed ${b#origin/} $s (verifier-only, full tests + verify of [$vg]: no blocker disappeared)"; return 0; }
ggeom() { # branch -> 0 ok; [param]/[refactor] branches must be geometry-identical vs HEAD (own single-branch trial)
  local b=$1 s ge=robots/revron/tools/geom_equal.py d="$GWT/geom"; s=$(git rev-parse --short "$b")
  [[ "$b" == *-param ]] || ! git log --no-merges --format=%s HEAD.."$b" | grep -qvE '^\[(param|refactor)\]' || return 0
  gwt "$d" HEAD || return 2; git -C "$d" merge -q --no-edit "$b" >/dev/null 2>&1 || { git -C "$d" merge --abort; return 2; }
  [ -f "$d/$ge" ] || return 0; spec_build "$d" || return 2
  gwt "$GWT/base" HEAD || return 2; spec_build "$GWT/base" || return 2; cp "$d/$ge" "$GWT/base/$ge"; rm -rf "${GWT:?}/snap"
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
  spec_build "$d" || { for b; do echo "hold $b"; done >> "$out"; return; }
  local lab="set$L"; [ $# -eq 1 ] && lab=${1#origin/}
  local a1 i1; read a1 i1 < <(gpair "$d" "$lab")
  [ -n "$i1" ] || { for b; do echo "hold $b"; done >> "$out"; return; }
  if $GPY ok "$a0" "$a1" "$i0" "$i1"; then
    echo "$a1 $i1" > "$P/ci_gate_baseline_$(git -C "$d" rev-parse --short "HEAD^{tree}")_$(gmode)"
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
    f=$(git diff --name-only --diff-filter=U | grep -v -e 'spec.json$' -e 'templates/revron.json$' -e '^robots/revron/renders/')
    if [ -z "$f" ]; then git checkout --theirs robots/revron/spec.json robot/templates/revron.json robots/revron/renders 2>/dev/null; git add robots/revron/spec.json robot/templates/revron.json robots/revron/renders; git commit -qm "Merge $b"; log "iter $i merged $b (spec-only conflict)"
    else git merge --abort; log "conflict ${b#origin/}: $(echo $f)"; fi
  fi; }
render_declared() { # re-render the spec's declared `renders` views (with wire routes + record) so wire.render_present never sees stale ends
  local d v; d=$(python3 -c "import json; r=json.load(open('robots/revron/spec.json')).get('renders') or {}; print(r.get('dir','renders'), ' '.join(r.get('views') or []))") || return 0
  set -- $d; local dir="robots/revron/$1"; shift
  for v in "$@"; do
    timeout 1800 python3 -m robot render robots/revron/spec.json "${v%.png}" "$dir/$v" --no-checks --jobs 1 >/dev/null 2>>"$P/ci_render_declared.err" \
      || log "declared render $v failed"
  done
  git add "$dir"; }
regen_commit() { # regenerate the spec here (cached) and commit it with fresh declared renders; 1 (logged) when the build failed: do not verify
  spec_build . || return 1
  git add robots/revron/spec.json robot/templates/revron.json || return 0
  git diff --cached --quiet && return 0
  [ "${CI_DECLARED_RENDERS:-1}" = 1 ] && render_declared
  git commit -qm "Revron: regenerate spec and declared renders (ci loop)" >/dev/null; }
# Round state on the share ($ST): iter, sha, phase gate|verify|done, plus the last gate's key and approved branches, so a
# restarted container (killed every 30-60 min) neither redoes a gate it finished nor a verify round already sharded.
ST="$P/ci_state.json"
sget() { $GPY state "$ST" get "$1"; }
sset() { $GPY state "$ST" set "$@"; }
merge_all() { # gate key = HEAD + every candidate's sha: the same candidate set on the same HEAD reuses the recorded gate result
  local c b k ok; c=$(cands); [ -n "$c" ] || return 0
  k="$(git rev-parse --short HEAD) $(for b in $c; do echo "$b=$(git rev-parse --short "$b")"; done | paste -sd' ')"
  if [ "$(sget gate_key)" = "$k" ]; then ok=$(sget gate); log "gate: reusing recorded result for this candidate set ($(echo ${ok:-none}))"
  else sset "iter=${i:-0}" phase=gate "sha=$(git rev-parse --short HEAD)"; ok=$(gate_all $c | paste -sd' '); sset "gate_key=$k" "gate=$ok"; fi
  for b in $ok; do mergeb "$b"; done; }
# summary line of a verify round, written exactly once per (iter, sha) by whichever process collected the results
summarize() { # iter sha out -> 0 written here, 1 already written / not counted
  local n groups note=""
  mkdir "$P/shards/$2/summary.$1" 2>/dev/null || [ "${SHARD:-1}" != 1 ] || { log "iter $1 sha $2: summary already written"; return 1; }
  if [ "$done_n" -eq 0 ]; then
    log "iter $1 sha $2: verify did not finish (rc $rc: $(grep -m1 -e Killed -e Traceback -e Error "$3" | cut -c1-120)); not counted"; return 1; fi
  n=$(grep -c '^\[BLOCKER\]' "$3")
  groups=$(grep '^\[BLOCKER\]' "$3" | awk '{print $2}' | cut -d. -f1 | sort | uniq -c | awk '{printf "%s %s, ",$2,$1}')
  [ -n "$failed" ] && note=" (did not finish:$failed)"
  log "iter $1 sha $2: $n blockers$note (${groups%, })"
  echo "$1 $2" > "$P/ci_iter_done"
  # only a complete round marks the sha verified; groups that did not finish are retried on the same sha
  [ -z "$failed" ] && echo "$2" > "$P/ci_last_verified"
  sset "iter=$1" "sha=$2" phase=done "blockers=$n" "failed=${failed# }"
  [ "$n" -eq 0 ] && [ -z "$note" ] && { log "0 blockers at $2, stopping"; exit 0; }
  return 0; }
# resume: the state says a verify round of a sha that is still origin/rvrn2's tip -> skip merge+gate, collect its shards
resume=
if [ "${SHARD:-1}" = 1 ] && [ "$(sget phase)" = verify ]; then
  rs=$(sget sha); git fetch -q origin rvrn2 2>>"$P/ci_push.err"
  if [ -n "$rs" ] && [ "$(git rev-parse --short origin/rvrn2)" = "$rs" ]; then
    [ "$(git rev-parse --short HEAD)" = "$rs" ] || git merge -q --ff-only origin/rvrn2 2>/dev/null
    if [ "$(git rev-parse --short HEAD)" = "$rs" ]; then resume=$rs; START_ITER=$(sget iter); log "restart: resuming iter $START_ITER verify of $rs (gate skipped)"
    else log "restart: HEAD $(git rev-parse --short HEAD) is not $rs, starting a fresh round"; fi
  else log "restart: state sha $rs is no longer origin/rvrn2's tip, starting a fresh round"; fi
fi
cands() { for b in $(heads); do git merge-base --is-ancestor "$b" HEAD || echo "$b"; done; }
[ "${RENDER_FIRST:-0}" = 1 ] && render
for i in $(seq "${START_ITER:-1}" "$MAX_ITERS"); do
  if [ -n "$resume" ]; then sha=$resume; else
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
    regen_commit || { push; continue; }   # same regeneration as the main pass
    push; sha=$(git rev-parse --short HEAD); log "iter $i new head $sha"
  fi
  [ -f "$P/blockers_live.jsonl" ] && mv "$P/blockers_live.jsonl" "$P/blockers_live.prev.jsonl"
  fi
  sset "iter=$i" "sha=$sha" phase=verify
  out="$P/ci_verify_${i}_$sha.log"
  # full verify, one fresh process per group: an OOM in one group skips only that group, not the round
  all=$(python3 -m robot verify --list-groups 2>/dev/null | grep -E '^[a-z_]+$' | grep -v -x -e threat -e fastener_seat | paste -sd' ')
  : > "$out"; rc=0; done_n=0; failed=
  chunks="$all fastener_seat"; [ -f "${SKIP_THREAT_FILE:-/tmp/ci_skip_threat}" ] || chunks="$all threat fastener_seat"
  need=$(echo $chunks | wc -w)
  if [ "${SHARD:-1}" = 1 ]; then RESUME=${resume:+1} shard_verify "$sha" "$chunks" "$out"; resume=; else
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
  [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && [ "${SHARD:-1}" = 1 ] && [ "$(( $(echo $chunks | wc -w) ))" -gt "$(ls "$P/shards/$sha/results/"*.rc 2>/dev/null | wc -l)" ] \
    && { log "stop file seen mid-verify, exiting (state kept: a restart resumes $sha)"; exit 0; }
  summarize "$i" "$sha" "$out" || { [ "$(sget phase)" = verify ] && sset phase=done; continue; }
  [ "${CI_RENDER:-1}" = 1 ] && render
  [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
done
log "reached $MAX_ITERS iterations, exiting"

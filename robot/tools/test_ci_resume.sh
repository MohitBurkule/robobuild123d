#!/bin/bash
# Shell test for restart-proof CI rounds (robot/tools/ci_loop.sh): a verify round is killed mid-way (loop AND its shard
# worker, like a container restart, leaving a dead claim); the restarted loop must skip merge/gate, resume the same
# shard dir, requeue only the dead claim, never re-run a finished group, and write the 'iter N sha X: K blockers'
# line exactly once. Also: the gate's unit tests run as a 'unit' shard ticket taken by a worker, cached by tree hash.
# Uses a throwaway repo with a fake robot CLI/spec build and the RUN hook. Run from the repo root.
set -u
SRC=$PWD; T=$(mktemp -d); trap 'touch "$T/p/shards/stop" "$T/stop"; pkill -9 -f "$T/" 2>/dev/null; wait 2>/dev/null; rm -rf "$T"' EXIT
export P=$T/p PROGRESS_DIR=$T/p; mkdir -p "$P"
git init -q --bare "$T/origin.git"
git init -q "$T/w"; cd "$T/w"; git config user.email t@t; git config user.name t
mkdir -p robot/tools robot/templates robots/revron/src robot/tests
for t in a b c; do echo "def test_x(): pass" > robot/tests/test_$t.py; done
cp "$SRC"/robot/tools/{ci_loop.sh,ci_gate.py,shard_worker.sh} robot/tools/
cat > robot/__main__.py <<'F'
import sys
if "--list-groups" in sys.argv: print("a\nb\nc\nd\nthreat\nfastener_seat")
F
cat > robots/revron/src/build_revron.py <<'F'
open("../spec.json", "w").write("{}\n"); open("../../../robot/templates/revron.json", "w").write("{}\n")
F
git add -A; git commit -qm init; git branch -M rvrn2-ci; git remote add origin "$T/origin.git"; git push -q origin rvrn2-ci:rvrn2
cat > "$T/fake" <<'F'
#!/bin/bash
echo "$2" >> "$P/runs"
if [[ "$2" == unit* ]]; then echo "files: $(cat "$SHARD_DIR/unit_files/$2")"; for f in $(cat "$SHARD_DIR/unit_files/$2"); do echo "0.50s call $f::test_x"; done
  grep -q bad "$SHARD_DIR/unit_files/$2" && { echo "1 failed, 1 passed in 0.1s"; exit 1; }; echo "2 passed in 0.1s"; exit 0; fi
case "$2" in c|d|fastener_seat) [ -f "$P/phase1" ] && sleep 300;; esac
sleep 1; echo "[BLOCKER] $2.x thing"; echo "done: 1 blockers, 0 warnings"; exit 2
F
chmod +x "$T/fake"; : > "$T/skipthreat"
export RUN=$T/fake POLL=1 SHARD_POLL=1 STALE=3 HB=1 CI_STOP=$T/stop SKIP_THREAT_FILE=$T/skipthreat \
  CI_RENDER=0 CI_DECLARED_RENDERS=0 MAX_ITERS=1 GATE=0 SHARDS=$T/p/shards
fail=0; ok() { "$@" || { echo "FAIL: $*"; fail=1; }; }
wait_for() { for _ in $(seq 120); do eval "$1" && return 0; sleep 0.5; done; echo "FAIL timeout: $1"; fail=1; return 1; }

# --- round 1: no local workers; one "remote" worker finishes a, b then hangs on c; then the container dies
touch "$P/phase1"
PAR=0 setsid bash robot/tools/ci_loop.sh > "$T/loop1.out" 2>&1 & L1=$!
wait_for '[ "$(python3 robot/tools/ci_gate.py state "$P/ci_state.json" get phase)" = verify ]'
sha=$(python3 robot/tools/ci_gate.py state "$P/ci_state.json" get sha); S=$P/shards/$sha
WORKER_ID=remote1 IDLE=600 setsid robot/tools/shard_worker.sh 2>>"$T/w1.log" & W1=$!
wait_for '[ -f "$S/results/a.rc" ] && [ -f "$S/results/b.rc" ] && ls "$S"/claimed/remote1.* >/dev/null 2>&1'
kill -9 -- -$L1 -$W1 2>/dev/null; kill -9 $L1 $W1 2>/dev/null; wait $L1 $W1 2>/dev/null; pkill -9 -f "$T/fake"; sleep 0.5
pushes1=$(grep -c 'pushed' "$P/builder.log")
ok [ "$(grep -c 'blockers' "$P/builder.log")" = 0 ]
ok [ "$(python3 robot/tools/ci_gate.py state "$P/ci_state.json" get phase)" = verify ]

# --- restart: must resume, not regenerate/push/gate again
rm -f "$P/phase1"
PAR=1 setsid bash robot/tools/ci_loop.sh > "$T/loop2.out" 2>&1 & L2=$!
wait_for '! kill -0 $L2 2>/dev/null'
ok grep -q "restart: resuming iter 1 verify of $sha" "$P/builder.log"
ok [ "$(grep -c 'pushed' "$P/builder.log")" = "$pushes1" ]
ok grep -q "stale claim remote1\.[a-z_]* requeued" "$P/builder.log"
ok [ "$(grep -c "iter 1 sha $sha: 5 blockers" "$P/builder.log")" = 1 ]
for g in a b d; do ok [ "$(grep -c -x $g "$P/runs")" = 1 ]; done
ok [ "$(python3 robot/tools/ci_gate.py state "$P/ci_state.json" get phase)" = done ]
ok [ "$(cat "$P/ci_last_verified")" = "$sha" ]
# a second collector of the same round (e.g. the old process coming back) must not write the line again
( eval "$(sed -n '/^summarize() {/,/^  return 0; }/p' robot/tools/ci_loop.sh)"; log() { echo "$*" >> "$P/builder.log"; }
  sset() { :; }; done_n=5; failed=; rc=0; out=$T/o; echo "[BLOCKER] a.x" > "$out"; summarize 1 "$sha" "$out" ) && { echo "FAIL: summary written twice"; fail=1; }
ok [ "$(grep -c "iter 1 sha $sha:.*blockers (" "$P/builder.log")" = 1 ]

# --- restart with a stale state (origin moved on): no resume
python3 robot/tools/ci_gate.py state "$P/ci_state.json" set phase=verify sha=0000000
GPY="python3 robot/tools/ci_gate.py"; log() { echo "$*" >> "$P/builder.log"; }; sget() { $GPY state "$P/ci_state.json" get "$1"; }; ST=$P/ci_state.json
eval "$(sed -n '/^# resume: the state says/,/^fi$/p' robot/tools/ci_loop.sh)"
ok [ -z "$resume" ]; ok grep -q 'state sha 0000000 is no longer' "$P/builder.log"

# --- unit ticket: run by a (remote) shard worker, cached by merged tree hash (a re-made merge commit hits the cache)
eval "$(sed -n '/^shard_verify() {/,/^}/p;/^unit_tests() {/,/^  return \$r; }/p' robot/tools/ci_loop.sh)"
git worktree add -q --detach "$T/trial" HEAD; echo x > "$T/trial/x"; git -C "$T/trial" add x; git -C "$T/trial" commit -qm trial
git -C "$T/trial" push -q origin HEAD:refs/heads/ci-unit-src  # stand-in for the ci-unit push (UNIT_PUSH=0 below)
WORKER_ID=remote2 IDLE=600 setsid robot/tools/shard_worker.sh 2>>"$T/w2.log" & W2=$!
PAR=0 UNIT_PUSH=0 UNIT_SHARDS=2 unit_tests "$T/trial" "$T/u1.log"; ok [ $? = 0 ]
ok grep -q 'claimed unit-0' "$T/w2.log"; ok grep -q 'claimed unit-1' "$T/w2.log"; ok grep -q passed "$T/u1.log"
ok grep -q 'files: .*test_' "$T/u1.log"
ok [ "$(cat "$T/u1.log" | grep -o 'robot/tests/test_[a-c].py::' | sort -u | wc -l)" = 3 ]   # every file ran, in some shard
ok grep -q '"robot/tests/test_a.py": 0.5' "$P/ci_unit_durations.json"
git -C "$T/trial" commit -q --amend -m "same tree, new sha"
PAR=0 UNIT_PUSH=0 unit_tests "$T/trial" "$T/u2.log"; ok [ $? = 0 ]
ok [ "$(grep -c -x 'unit-[0-9]' "$P/runs")" = 2 ]; ok grep -q 'cached result 0' "$P/builder.log"
# one failing shard fails the combined result (cached as a fail); timeouts/no summary are infra (2), not cached
echo "def test_bad(): pass" > "$T/trial/robot/tests/test_bad.py"; git -C "$T/trial" add -A; git -C "$T/trial" commit -qm bad
PAR=0 UNIT_PUSH=0 UNIT_SHARDS=2 unit_tests "$T/trial" "$T/u3.log"; ok [ $? = 1 ]
ok [ "$(cat "$P/ci_unit_cache/$(git -C "$T/trial" rev-parse 'HEAD^{tree}')")" = 1 ]
kill -9 $W2 2>/dev/null
[ $fail = 0 ] && echo PASS; exit $fail

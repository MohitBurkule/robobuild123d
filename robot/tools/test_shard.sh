#!/bin/bash
# Shell test for SHARD=1: two "remote" workers plus one local worker, and one stale claim that must be
# requeued and finished locally. Uses the RUN hook instead of real verifies. Run from the repo root.
set -u
T=$(mktemp -d); trap 'touch "$T/p/shards/stop"; wait; rm -rf "$T"' EXIT
export P=$T/p; mkdir -p "$P"
cat > "$T/fake" <<'F'
#!/bin/bash
sleep 1; [ "$2" = bad ] && { echo Traceback; exit 3; }; echo "[BLOCKER] $2.x thing"; echo "done: 1 blockers, 0 warnings"
F
chmod +x "$T/fake"; export RUN=$T/fake POLL=1 SHARD_POLL=1 STALE=3 HB=1 PAR=1 CI_STOP=$T/nostop
log() { echo "$*" >> "$P/builder.log"; }
eval "$(sed -n '/^shard_verify() {/,/^}/p' robot/tools/ci_loop.sh)"
sha=$(git rev-parse --short HEAD); groups="a b c d bad e"
# a stale claim of group e by a dead host, written before the coordinator starts
( sleep 0.5; mkdir -p "$P/shards/$sha/claimed"; mv "$P/shards/$sha/queue/e" "$P/shards/$sha/claimed/deadhost.e" && touch -d '-1 hour' "$P/shards/$sha/claimed/deadhost.e" ) &
for w in 1 2; do WORKER_ID=remote$w SHARDS=$P/shards IDLE=5 robot/tools/shard_worker.sh 2>>"$T/remote.log" & done
out=$T/out.log; : > "$out"; done_n=0; failed=; rc=0
shard_verify "$sha" "$groups" "$out"
fail=0
[ "$done_n" = 5 ] || { echo "FAIL done_n=$done_n"; fail=1; }
[ "$failed" = " bad" ] || { echo "FAIL failed='$failed'"; fail=1; }
[ "$rc" = 3 ] || { echo "FAIL rc=$rc"; fail=1; }
[ "$(grep -c '^\[BLOCKER\]' "$out")" = 5 ] || { echo "FAIL blockers"; fail=1; }
grep -q 'stale claim deadhost.e requeued' "$P/builder.log" || { echo "FAIL no requeue"; fail=1; }
grep -q claimed "$T/remote.log" || { echo "FAIL remotes claimed nothing"; fail=1; }
wait
[ $fail = 0 ] && echo "PASS"; exit $fail

#!/bin/bash
# Shard worker: claims verify-group tickets from $SHARDS/<sha>/queue/ and writes results/<group>.{log,rc}.
# Usage (from any checkout of this repo): robot/tools/shard_worker.sh
# Env: SHARDS (default /mnt/project-files/robot-cad/b123d/progress/shards), IDLE (exit after this many s
# with an empty queue, default 600), STOP (stop file, default $SHARDS/stop), GROUP_TIMEOUT (6000),
# HB (heartbeat interval, 60), RUN (test hook: command run as `$RUN <worktree> <group>`).
# Layout per sha: sha (full sha), queue/<g>, claimed/<host>.<g> (content = "<worker epoch> <beat n>",
# rewritten every HB s; readers judge staleness by content changes on their own clock, never by mtime,
# because a network mount's mtimes come from the server's clock/attribute cache), results/<g>.log|.rc.
# Claims are a rename (atomic on one filesystem, NFS included); results are written to a temp name and renamed.
SHARDS=${SHARDS:-/mnt/project-files/robot-cad/b123d/progress/shards}
IDLE=${IDLE:-600}; STOP=${STOP:-$SHARDS/stop}; HB=${HB:-60}
HOST=${WORKER_ID:-$(hostname)-$$}
REPO=$(git rev-parse --show-toplevel 2>/dev/null) || REPO=
TMP=$(mktemp -d); trap 'cd /; [ -n "$REPO" ] && git -C "$REPO" worktree remove --force "$TMP/wt" 2>/dev/null; rm -rf "$TMP"' EXIT
wlog() { echo "$(date -Is) [shard $HOST] $*" >&2; }

checkout() { # full sha -> $TMP/wt at that sha
  [ "$(git -C "$TMP/wt" rev-parse HEAD 2>/dev/null)" = "$1" ] && return 0
  [ -n "$REPO" ] || { wlog "not in a git checkout"; return 1; }
  git -C "$REPO" worktree remove --force "$TMP/wt" 2>/dev/null; rm -rf "$TMP/wt"
  for d in 0 2 4 8 16; do sleep $d
    git -C "$REPO" cat-file -e "$1^{commit}" 2>/dev/null || git -C "$REPO" fetch -q origin rvrn2 "$1" 2>/dev/null || git -C "$REPO" fetch -q origin rvrn2 2>/dev/null
    git -C "$REPO" cat-file -e "$1^{commit}" 2>/dev/null && git -C "$REPO" worktree add -q --detach "$TMP/wt" "$1" 2>/dev/null && return 0
  done; wlog "cannot check out $1"; return 1
}

run_group() { # worktree group -> stdout/rc
  if [ -n "$RUN" ]; then $RUN "$1" "$2"; return; fi
  local h=; [ -x /tmp/heavy.sh ] && h="/tmp/heavy.sh"
  (cd "$1" && HEAVY_CI=1 $h timeout "${GROUP_TIMEOUT:-6000}" python3 -m robot verify "${SPEC:-robots/revron/spec.json}" --full --only "$2" --jobs 1)
}

beat() { echo "$(date +%s) $1" > "$C" 2>/dev/null; }  # heartbeat: content changes every HB s

claim() { # -> sets D (shard dir), G (group), C (claim path); 0 if claimed
  local q
  for q in "$SHARDS"/*/queue/*; do
    [ -f "$q" ] || continue
    D=${q%/queue/*}; G=${q##*/}; C="$D/claimed/$HOST.$G"
    [ -f "$D/results/$G.rc" ] && { rm -f "$q"; continue; }  # already done (late requeue): never run twice
    mkdir -p "$D/claimed" 2>/dev/null
    mv "$q" "$C" 2>/dev/null && [ -f "$C" ] || continue  # lost the race
    [ -f "$D/results/$G.rc" ] && { rm -f "$C"; continue; }
    beat 0; return 0
  done; return 1
}

idle_since=$(date +%s)
while [ ! -f "$STOP" ]; do
  if ! claim; then
    [ $(( $(date +%s) - idle_since )) -ge "$IDLE" ] && { wlog "queue empty for ${IDLE}s, exiting"; exit 0; }
    sleep "${POLL:-10}"; continue
  fi
  wlog "claimed $G in $D"
  sha=$(cat "$D/sha" 2>/dev/null)
  ( n=0; while [ -f "$C" ]; do sleep "$HB"; n=$((n+1)); [ -f "$C" ] && beat $n; done ) & hb=$!
  mkdir -p "$D/results"
  if [ -n "$sha" ] && checkout "$sha"; then run_group "$TMP/wt" "$G" > "$TMP/$G.log" 2>&1; rc=$?
  else echo "shard worker $HOST: checkout of '$sha' failed" > "$TMP/$G.log"; rc=97; fi
  kill $hb 2>/dev/null; wait $hb 2>/dev/null
  # copy to a temp name on the share, then rename: readers never see a half-written log
  cp "$TMP/$G.log" "$D/results/.$G.log.$HOST" && mv -f "$D/results/.$G.log.$HOST" "$D/results/$G.log"
  echo $rc > "$D/results/.$G.rc.$HOST" && mv -f "$D/results/.$G.rc.$HOST" "$D/results/$G.rc"
  rm -f "$C"; wlog "$G rc $rc"; idle_since=$(date +%s)
done
wlog "stop file seen, exiting"

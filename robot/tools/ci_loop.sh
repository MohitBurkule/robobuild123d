#!/bin/bash
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
[ "${RENDER_FIRST:-0}" = 1 ] && render
for i in $(seq "${START_ITER:-1}" "$MAX_ITERS"); do
  git fetch -q origin "+refs/heads/fix-*:refs/remotes/origin/fix-*" 2>>"$P/ci_push.err" || log "fetch failed"
  for b in $(heads); do
    git merge-base --is-ancestor "$b" HEAD && continue
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
      for b in $(heads); do git merge-base --is-ancestor "$b" HEAD || git merge -q --no-edit "$b" >/dev/null 2>&1 || { git merge --abort; log "conflict ${b#origin/}"; }; done
      [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
    done
    push; sha=$(git rev-parse --short HEAD); log "iter $i new head $sha"
  fi
  [ -f "$P/blockers_live.jsonl" ] && mv "$P/blockers_live.jsonl" "$P/blockers_live.prev.jsonl"
  out="$P/ci_verify_${i}_$sha.log"
  # full verify in fresh processes per chunk (one process for all groups grew past 11 GB at `threat` and was OOM-killed)
  all=$(python3 -m robot verify --list-groups 2>/dev/null | grep -E '^[a-z_]+$' | grep -v -x -e threat -e fastener_seat | paste -sd,)
  : > "$out"; rc=0; done_n=0
  chunks="$all fastener_seat"; [ -f "${SKIP_THREAT_FILE:-/tmp/ci_skip_threat}" ] || chunks="$all threat fastener_seat"
  need=$(echo $chunks | wc -w)
  for chunk in $chunks; do
    ROBOT_RUN_SHA=$sha ROBOT_PROGRESS_LOG="$P/verify.log" HEAVY_CI=1 /tmp/heavy.sh timeout 6000 python3 -m robot verify "$SPEC" --full --only "$chunk" --jobs "${JOBS:-2}" > "$out.part" 2>&1
    r=$?; cat "$out.part" >> "$out"; grep -q 'blockers,' "$out.part" && done_n=$((done_n+1)) || rc=$r
  done
  rm -f "$out.part"
  if [ "$done_n" -lt "$need" ]; then
    log "iter $i sha $sha: verify did not finish (rc $rc: $(grep -m1 -e Killed -e Traceback -e Error "$out" | cut -c1-120)); not counted"
    continue
  fi
  n=$(grep -c '^\[BLOCKER\]' "$out")
  groups=$(grep '^\[BLOCKER\]' "$out" | awk '{print $2}' | cut -d. -f1 | sort | uniq -c | awk '{printf "%s %s, ",$2,$1}')
  note=""; [ "$need" -lt 3 ] && note=" (threat not run)"
  log "iter $i sha $sha: $n blockers$note (${groups%, })"
  echo "$i $sha" > "$P/ci_iter_done"; echo "$sha" > "$P/ci_last_verified"
  [ "${CI_RENDER:-1}" = 1 ] && render
  [ "$n" -eq 0 ] && [ -z "$note" ] && { log "0 blockers at $sha, stopping"; exit 0; }
  [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
done
log "reached $MAX_ITERS iterations, exiting"

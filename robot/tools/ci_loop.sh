#!/bin/bash
# Bounded integration loop: at most MAX_ITERS passes of
#   fetch origin; merge every fix-* head (local or origin/, whichever is newer) into rvrn2-ci
#   (conflicts aborted and logged as `[ci] conflict fix-X`); push rvrn2-ci:rvrn2 with retries;
#   regenerate the spec, full verify through /tmp/heavy.sh streaming blockers, write a [ci] summary line.
# Stops early on 0 blockers or when $CI_STOP exists. Run from a worktree checked out on rvrn2-ci.
MAX_ITERS=${MAX_ITERS:-20}
P=${PROGRESS_DIR:-/mnt/project-files/robot-cad/b123d/progress}
SPEC=${SPEC:-robots/revron/spec.json}
log() { echo "$(date -Is) [ci] $*" >> "$P/builder.log"; }
[ "$(git rev-parse --abbrev-ref HEAD)" = "rvrn2-ci" ] || { log "not on rvrn2-ci, exiting"; exit 1; }
push() { for d in 0 2 4 8 16; do sleep $d; git push -q -u origin rvrn2-ci:rvrn2 2>>"$P/ci_push.err" && { log "pushed $(git rev-parse --short HEAD) to origin/rvrn2"; return 0; }; done; log "push FAILED after retries"; }
heads() { # newest of local fix-X and origin/fix-X per branch
  for n in $( (git for-each-ref --format='%(refname:lstrip=2)' 'refs/heads/fix-*'; git for-each-ref --format='%(refname:lstrip=3)' 'refs/remotes/origin/fix-*') | sort -u); do
    l=refs/heads/$n; r=refs/remotes/origin/$n
    if git rev-parse -q --verify $l >/dev/null && git rev-parse -q --verify $r >/dev/null; then
      if git merge-base --is-ancestor $l $r; then echo origin/$n; else echo $n; git merge-base --is-ancestor $r $l || echo origin/$n; fi
    elif git rev-parse -q --verify $l >/dev/null; then echo $n; else echo origin/$n; fi
  done; }
for i in $(seq "${START_ITER:-1}" "$MAX_ITERS"); do
  git fetch -q origin 2>>"$P/ci_push.err" || log "fetch failed"
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
  [ -f "$P/blockers_live.jsonl" ] && mv "$P/blockers_live.jsonl" "$P/blockers_live.prev.jsonl"
  out="$P/ci_verify_${i}_$sha.log"
  ROBOT_RUN_SHA=$sha ROBOT_PROGRESS_LOG="$P/verify.log" /tmp/heavy.sh timeout 6000 python3 -m robot verify "$SPEC" --full --jobs "${JOBS:-2}" > "$out" 2>&1
  rc=$?
  if ! grep -q 'blockers,' "$out"; then
    log "iter $i sha $sha: verify did not finish (rc $rc: $(grep -m1 -e Killed -e Traceback -e Error "$out" | cut -c1-120)); not counted"
    continue
  fi
  n=$(grep -c '^\[BLOCKER\]' "$out")
  groups=$(grep '^\[BLOCKER\]' "$out" | awk '{print $2}' | cut -d. -f1 | sort | uniq -c | awk '{printf "%s %s, ",$2,$1}')
  log "iter $i sha $sha: $n blockers (${groups%, })"
  echo "$i $sha" > "$P/ci_iter_done"
  [ "$n" -eq 0 ] && { log "0 blockers at $sha, stopping"; exit 0; }
  [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
done
log "reached $MAX_ITERS iterations, exiting"

#!/bin/bash
# Bounded, local-only integration loop (no push): at most MAX_ITERS passes of
#   merge every local fix-* head into the local branch rvrn2-ci (conflicting branches skipped and logged),
#   regenerate the spec, full verify through /tmp/heavy.sh streaming blockers, write a [ci] summary line.
# Stops early on 0 blockers or when $CI_STOP exists. Run from a worktree checked out on rvrn2-ci.
MAX_ITERS=${MAX_ITERS:-20}
P=${PROGRESS_DIR:-/mnt/project-files/robot-cad/b123d/progress}
SPEC=${SPEC:-robots/revron/spec.json}
log() { echo "$(date -Is) [ci] $*" >> "$P/builder.log"; }
[ "$(git rev-parse --abbrev-ref HEAD)" = "rvrn2-ci" ] || { log "not on rvrn2-ci, exiting"; exit 1; }
for i in $(seq 1 "$MAX_ITERS"); do
  for b in $(git for-each-ref --format='%(refname:short)' 'refs/heads/fix-*'); do
    git merge-base --is-ancestor "$b" HEAD && continue
    if git merge -q --no-edit "$b" >/dev/null 2>&1; then log "iter $i merged $b $(git rev-parse --short "$b")"
    else
      f=$(git diff --name-only --diff-filter=U | grep -v -e 'spec.json$' -e 'templates/revron.json$')
      if [ -z "$f" ]; then git checkout --theirs robots/revron/spec.json robot/templates/revron.json 2>/dev/null; git add robots/revron/spec.json robot/templates/revron.json; git commit -qm "Merge $b"; log "iter $i merged $b (spec-only conflict)"
      else git merge --abort; log "iter $i CONFLICT skipping $b: $(echo $f)"; fi
    fi
  done
  (cd robots/revron/src && python3 build_revron.py >/dev/null 2>&1) && git add robots/revron/spec.json robot/templates/revron.json && git commit -qm "Revron: regenerate spec (ci loop)" >/dev/null 2>&1
  sha=$(git rev-parse --short HEAD)
  [ -f "$P/blockers_live.jsonl" ] && mv "$P/blockers_live.jsonl" "$P/blockers_live.prev.jsonl"
  out="$P/ci_verify_${i}_$sha.log"
  ROBOT_RUN_SHA=$sha ROBOT_PROGRESS_LOG="$P/verify.log" /tmp/heavy.sh timeout 6000 python3 -m robot verify "$SPEC" --full --jobs 4 > "$out" 2>&1
  n=$(grep -c '^\[BLOCKER\]' "$out")
  groups=$(grep '^\[BLOCKER\]' "$out" | awk '{print $2}' | cut -d. -f1 | sort | uniq -c | awk '{printf "%s %s, ",$2,$1}')
  log "iter $i/$MAX_ITERS $sha $(grep -m1 'blockers,' "$out" | sed 's/^Revron: //') | $groups"
  grep -q 'blockers,' "$out" && [ "$n" -eq 0 ] && { log "0 blockers at $sha, stopping"; exit 0; }
  [ -f "${CI_STOP:-/tmp/ci_loop.stop}" ] && { log "stop file seen, exiting"; exit 0; }
done
log "reached $MAX_ITERS iterations, exiting"

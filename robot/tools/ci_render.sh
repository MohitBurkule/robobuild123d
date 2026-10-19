#!/bin/bash
# Sequential presentation renders of the current checkout into $FINAL (and $FINAL/diff heat maps), each in the
# shared heavy slots (2,3) by default so it runs beside the CI verify in slot 1; RENDER_HEAVY_CI=1 uses slot 1. Order: top lid-off, top section under the deck, other lid-off views, lid-on views, heat maps.
FINAL=${FINAL:-/mnt/project-files/robot-cad/b123d/final}
SPEC=${SPEC:-robots/revron/spec.json}
P=${PROGRESS_DIR:-/mnt/project-files/robot-cad/b123d/progress}
R="env HEAVY_CI=${RENDER_HEAVY_CI:-0} /tmp/heavy.sh timeout 1800 python3 -m robot render $SPEC"
mkdir -p "$FINAL/diff"
ok=0; bad=""
run() { if $R "$@" --quick --jobs 1 >/dev/null 2>"$P/ci_render.err"; then ok=$((ok+1)); else bad="$bad $(basename "$2")"; fi; }
run top "$FINAL/rvrn2_top_nolid.png" --no-lid
run top "$FINAL/rvrn2_top_section_z17.png" --no-lid --section-z 17
for v in side iso front; do run $v "$FINAL/rvrn2_${v}_nolid.png" --no-lid; done
for v in top side iso front; do run $v "$FINAL/rvrn2_$v.png"; done
d=$(dirname "$SPEC")/.ci_diff.json
python3 -c "import json,sys; s=json.load(open('$SPEC')); s['reference_cad']['diff_render_dir']='$FINAL/diff'; json.dump(s,open('$d','w'))"
HEAVY_CI=${RENDER_HEAVY_CI:-0} /tmp/heavy.sh timeout 3000 python3 -m robot verify "$d" --only reference_cad --jobs 1 >/dev/null 2>&1 || bad="$bad diff"
rm -f "$d"
echo "$(date -Is) [ci] renders $(git rev-parse --short HEAD): $ok/8 views ok${bad:+, failed:$bad}; heat maps in $FINAL/diff" >> "$P/builder.log"

# Disector: tooling struggles

Pain points hit while taking Disector from 36 blockers to 0 (newest last).

- **Full tier is ~10 minutes, of which `practice` is ~4.** `--tier full --except practice --json out.json` is ~3 min and was the real
  fix loop. `--llm` only prints the first 12 root causes ("... 21 more"), so I had to drop `--llm` (or read the JSON) to see them all.
- **`param.literals` was invisible in the headline.** 14 of the 36 blockers were "unexplained numeric literals" per build function
  (limit 3). The only way out is to move every dimension to module-level constants; the lint counts tuple/list literals inside
  functions too, so data tables (channel boxes, wire waypoints) must live at module level in `params.py`.
- **Wire router only routes inside the AABB of `structure` parts** (`wiring.Router`: everything outside lo+0.4..hi-0.4 of the union of
  structure AABBs is solid). A wire to a motor on an overhead arm can never route unless the arm is declared `structure`.
  Not documented in the wiring failure text ("no clear path ... panel_top blocks it" points at the wrong culprit).
- **`weapon.spin_axis` is in the part's local frame**, `joint.axis` is in the parent frame. Disc meshes built in XY with `rot [0,90,0]`
  need `spin_axis [0,0,1]`; `[1,0,0]` silently made `electrical.wire_rotating_clearance` use a disc slab along world Z.
- **Rotor membership for the sweep check follows `parent`, not `rotates_with`.** Bell/shaft/disc had to be restructured so the bell
  carries the revolute joint and the disc is its child (frames compose: the disc `at` becomes bell-relative).
- **`robot.cad.holes` thread-side bore depth**: `side="thread"` with default `engage` bores the full screw length (+0.5) from the
  grip plane, i.e. `grip` mm too deep (and cap-head `seat` is not in the record's engagement). Pad screws then broke into the cavity
  and the underside (thin walls 0.03-0.5 mm). `fasteners._thread_depth` now asks the record for the exact depth.
- **Thin-wall check is a whack-a-mole**: each channel/bay move exposed a new 0.35-0.5 mm sliver between two cuts
  (bay vs. switch pit, ESC bay vs. hollow, slot vs. motor pocket). Fix is to make cuts overlap or keep a >= 0.9 mm wall by relation.
- **`contain.line_of_sight` samples ~8 vertices per box part**, so one corner vertex peeking through a panel slot is 12 % of the part
  (limit 10 %). Slot edges must stay off the footprint of ESC/battery corners.
- **Edge-distance / cantilever rules interact with tap-drill depth**: skid screws have to be low enough for lever/spacing <= 3 and high
  enough for a 0.9 mm wall above the underside; solved by staggering the two screws across the skid.
- **`render --no-lid` finds lids by id words** (`lid`, `cover`, `top_panel`, `top_plate`); `panel_top` matched none, so the render was
  byte-identical to `iso`. Fixed with a `tags: ["lid"]` label on the part. The render cache also returns the plain iso for a flagged
  render unless `--no-cache` is used.
- **Parallel part builds fail intermittently** ("parallel build failed (RuntimeError); building the rest serially") when several
  `robot` processes start at once; renders raced each other, so I ran them with `--no-checks`.

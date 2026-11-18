
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends rear_wall, side_wall to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 100x100x24 mm, ramp 0; wheels 4 r11 inboard; weapon none; extra parts: rear_wall, side_wall; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok).

## Round 2 (looks)
Decisions: type wedge; body box rect 100x100x24 mm, ramp 0; wheels 4 r11 inboard; weapon none; extra parts: rear_wall, side_wall; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 100x100x24 mm, ramp 0; wheels 4 r11 inboard; weapon none; extra parts: rear_wall, side_wall; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok).

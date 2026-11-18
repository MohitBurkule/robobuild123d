
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type drum; body box rect 62x112x34 mm, ramp 0; wheels 2 r17 outboard; weapon drum r15 axis x teeth 2; extra parts: lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.82 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type drum; body box rect 62x112x34 mm, ramp 0; wheels 2 r17 outboard; weapon drum r15 axis x teeth 2; extra parts: lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.72 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/recycler.aws67.webp` is declared `front_left_iso` (IoU 0.72 there) but the model matches it better from rear_right_iso (elevati

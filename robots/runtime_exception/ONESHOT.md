
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends spine to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box pentagon 80x92x22 mm, ramp 0; wheels 2 r13 inboard; weapon none; extra parts: scoop, spine; photos skipped (cluttered): indices [0].

Likeness: aws72 0.79 (FAIL), aws74 0.80 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box pentagon 80x92x22 mm, ramp 0; wheels 2 r13 inboard; weapon none; extra parts: scoop, spine; photos skipped (cluttered): indices [0].

Likeness: aws72 0.79 (FAIL), aws74 0.80 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box pentagon 80x92x22 mm, ramp 0; wheels 2 r15 inboard; weapon none; extra parts: spine, scoop; photos skipped (cluttered): indices [0].

Likeness: aws72 0.59 (FAIL), aws74 0.66 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/runtime_exception.aws72.webp` is declared `front_left_iso` (IoU 0.59 there) but the model matches it better from rear_left_iso ; [FAIL] likeness.view: `reference/runtime_exception.aws74.webp` is declared `front_left_iso` (IoU 0.66 there) but the model matches it better from front_left_iso

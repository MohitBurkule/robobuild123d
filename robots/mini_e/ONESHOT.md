
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (wedge), guessing the tilt maths by hand. ~3 min.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 72x100x22 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: wedge; photos skipped (cluttered): indices [0].

Likeness: aws72 0.81 (FAIL), aws76 0.81 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box rect 72x100x22 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: wedge; photos skipped (cluttered): indices [0].

Likeness: aws72 0.81 (FAIL), aws76 0.81 (FAIL).

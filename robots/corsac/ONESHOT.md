
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (face), guessing the tilt maths by hand. ~3 min.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 80x100x26 mm, ramp 0; wheels 2 r12 inboard; weapon none; 6 forks 14 mm; extra parts: face.

Likeness: aws72 0.82 (ok), aws74 0.81 (ok), aws76 0.80 (ok).

## Round 2 (looks)
Decisions: type wedge; body box rect 80x100x26 mm, ramp 0; wheels 2 r12 inboard; weapon none; 6 forks 14 mm; extra parts: face.

Likeness: aws72 0.82 (ok), aws74 0.81 (ok), aws76 0.80 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 80x100x26 mm, ramp 0; wheels 2 r12 inboard; weapon none; 6 forks 16 mm; extra parts: face.

Likeness: aws72 0.66 (FAIL), aws74 0.68 (FAIL), aws76 0.63 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/corsac.aws72.webp` is declared `front_left_iso` (IoU 0.66 there) but the model matches it better from rear_right_iso (elevation; [FAIL] likeness.view: `reference/corsac.aws74.webp` is declared `front_right_iso` (IoU 0.68 there) but the model matches it better from rear_left_iso (elevation; [FAIL] likeness.view: `reference/corsac.aws76.webp` is declared `front_left_iso` (IoU 0.63 there) but the model matches it better from rear_left_iso (elevation 

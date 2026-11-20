
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 95x54x26 mm, ramp 0; wheels 6 r12 outboard; weapon none; extra parts: scoop.

Likeness: aws72 0.79 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box rect 95x54x26 mm, ramp 0; wheels 6 r12 outboard; weapon none; extra parts: scoop.

Likeness: aws72 0.81 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 95x54x26 mm, ramp 0; wheels 6 r12 outboard; weapon none; extra parts: scoop.

Likeness: aws72 0.60 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/blue-terror.aws72.webp` is declared `front_left_iso` (IoU 0.60 there) but the model matches it better from front_right_iso (ele

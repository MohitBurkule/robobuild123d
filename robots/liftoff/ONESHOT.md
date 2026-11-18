
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (wedge, lift_plate), guessing the tilt maths by hand. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 72x80x24 mm, ramp 0; wheels 2 r13 outboard; weapon none; extra parts: wedge, lift_plate.

Likeness: aws76 0.66 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 72x80x24 mm, ramp 0; wheels 2 r13 outboard; weapon none; extra parts: wedge, lift_plate.

Likeness: aws76 0.66 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 72x80x24 mm, ramp 0; wheels 2 r13 outboard; weapon none; extra parts: wedge, lift_plate.

Likeness: aws76 0.37 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/liftoff.aws76.webp` is declared `front` (IoU 0.37 there) but the model matches it better from front_left_iso (elevation 25, azi

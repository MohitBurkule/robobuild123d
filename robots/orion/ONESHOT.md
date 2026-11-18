
## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (flipper), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends spring to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type flipper; body box trapezoid 110x92x46 mm, ramp 85; wheels 2 r11 inboard; weapon none; extra parts: flipper, spring; photos skipped (cluttered): indices [0, 1].

Likeness: aws72 0.74 (FAIL).

## Round 2 (looks)
Decisions: type flipper; body box trapezoid 110x92x46 mm, ramp 85; wheels 2 r11 inboard; weapon none; extra parts: flipper, spring; photos skipped (cluttered): indices [0, 1].

Likeness: aws72 0.74 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box trapezoid 110x92x46 mm, ramp 85; wheels 2 r11 inboard; weapon none; extra parts: flipper, spring; photos skipped (cluttered): indices [0, 1].

Likeness: aws72 0.57 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/orion.aws72.webp` is declared `front_right_iso` (IoU 0.57 there) but the model matches it better from front_left_iso (elevation

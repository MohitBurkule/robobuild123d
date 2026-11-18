
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends servo to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 62x72x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; extra parts: scoop, servo; photos skipped (cluttered): indices [0].

Likeness: aws74 0.77 (FAIL), aws76 0.78 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 62x72x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; extra parts: scoop, servo; photos skipped (cluttered): indices [0].

Likeness: aws74 0.77 (FAIL), aws76 0.78 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 62x72x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; extra parts: scoop, servo, servo_plate; photos skipped (cluttered): indices [0].

Likeness: aws74 0.62 (FAIL), aws76 0.58 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/unorthodox.aws74.webp` is declared `front_right_iso` (IoU 0.62 there) but the model matches it better from front_right_iso (ele; [FAIL] likeness.view: `reference/unorthodox.aws76.webp` is declared `front_left_iso` (IoU 0.58 there) but the model matches it better from front_left_iso (eleva

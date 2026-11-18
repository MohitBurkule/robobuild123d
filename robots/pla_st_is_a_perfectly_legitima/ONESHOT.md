
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box round_nose 95x104x28 mm, ramp 0; wheels 4 r9 inboard; weapon none; extra parts: arm, scoop; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.82 (ok).

## Round 2 (looks)
Decisions: type lifter; body box round_nose 95x104x28 mm, ramp 0; wheels 4 r11 inboard; weapon none; extra parts: arm, scoop; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.82 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box round_nose 95x104x28 mm, ramp 0; wheels 4 r11 inboard; weapon none; extra parts: arm, scoop; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.72 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/pla-st_is_a_perfectly_legitimate_choice_of_material.aws67.webp` is declared `front_left_iso` (IoU 0.72 there) but the model mat

## Round 3c (user angle picks applied; shape fixed per user remarks)
Decisions: type lifter; body box round_nose 95x104x28 mm, ramp 0; wheels 4 r11 inboard; weapon none; extra parts: arm, wedge, wedge_wing; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.72 (FAIL).

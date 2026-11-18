# stagnant: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 62x130x30 mm, ramp 22; wheels 2 r13 inboard; weapon none; extra parts: front_plate; textured masks for indices [0].

Likeness: aws62 0.87 (ok), aws67 0.82 (ok).

## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 62x130x30 mm, ramp 22; wheels 2 r13 inboard; weapon none; extra parts: front_plate; textured masks for indices [0].

Likeness: aws62 0.87 (ok), aws67 0.82 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 62x130x30 mm, ramp 22; wheels 2 r13 inboard; weapon none; extra parts: front_plate; textured masks for indices [0].

Likeness: aws62 0.53 (FAIL), aws67 0.66 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/stagnant.aws62.webp` is declared `front` (IoU 0.53 there) but the model matches it better from front_right_iso (elevation 45, a; [FAIL] likeness.view: `reference/stagnant.aws67.webp` is declared `front` (IoU 0.66 there) but the model matches it better from front_left_iso (elevation 25, az

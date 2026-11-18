# speed_demon: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 95x96x30 mm, ramp 32; wheels 4 r13 outboard; weapon none; extra parts: front_plate.

Likeness: 71 0.80 (FAIL), aws72 0.82 (ok), aws74 0.88 (ok).

## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 95x96x30 mm, ramp 32; wheels 4 r13 outboard; weapon none; extra parts: front_plate.

Likeness: 71 0.80 (FAIL), aws72 0.82 (ok), aws74 0.88 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 95x96x30 mm, ramp 32; wheels 4 r14 outboard; weapon none; 2 forks 24 mm; extra parts: front_plate.

Likeness: 71 0.68 (FAIL), aws72 0.77 (FAIL), aws74 0.66 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/speed_demon.aws.71.webp` is declared `front_left_iso` (IoU 0.68 there) but the model matches it better from front_left_iso (ele; [FAIL] likeness.view: `reference/speed_demon.aws74.webp` is declared `front` (IoU 0.66 there) but the model matches it better from front_right_iso (elevation 25

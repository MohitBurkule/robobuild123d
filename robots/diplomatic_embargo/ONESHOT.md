# diplomatic_embargo: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 95x66x24 mm, ramp 0; wheels 4 r11 outboard as treads; weapon none; 3 forks 30 mm; extra parts: front_plate.

Likeness: aws72 0.85 (ok), aws76 0.70 (FAIL).

## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 95x66x24 mm, ramp 0; wheels 4 r11 outboard as treads; weapon none; 3 forks 30 mm; extra parts: front_plate.

Likeness: aws72 0.85 (ok), aws76 0.70 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 95x66x24 mm, ramp 0; wheels 4 r11 outboard; weapon none; 3 forks 46 mm; extra parts: front_plate.

Likeness: aws72 0.68 (FAIL), aws76 0.49 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/diplomatic_embargo.aws76.webp` is declared `front_left_iso` (IoU 0.49 there) but the model matches it better from rear_left_iso


## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends arm to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type vertical_spinner; body box rect 62x60x28 mm, ramp 0; wheels 2 r13 outboard; weapon disc r27 axis x teeth 8; 2 forks 62 mm; extra parts: arm.

Likeness: aws76 0.57 (FAIL).

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 62x60x28 mm, ramp 0; wheels 2 r13 outboard; weapon disc r28 axis x teeth 8; extra parts: arm, jaw.

Likeness: aws76 0.55 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 62x60x28 mm, ramp 0; wheels 2 r13 outboard; weapon disc r34 axis x teeth 8; extra parts: arm, jaw.

Likeness: aws76 0.36 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/i_saw_that_.aws76.webp` is declared `front_left_iso` (IoU 0.36 there) but the model matches it better from rear_left_iso (eleva

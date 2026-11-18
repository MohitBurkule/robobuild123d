
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends upright to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type vertical_spinner; body box rect 80x66x20 mm, ramp 0; wheels 2 r13 outboard; weapon disc r30 axis x teeth 2; 2 forks 55 mm; extra parts: upright.

Likeness: aws72 0.55 (FAIL), aws74 0.58 (FAIL), aws76 0.63 (FAIL).

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 80x66x20 mm, ramp 0; wheels 2 r14 outboard; weapon disc r36 axis x teeth 2; extra parts: upright, fork.

Likeness: aws72 0.56 (FAIL), aws74 0.54 (FAIL), aws76 0.60 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 80x66x20 mm, ramp 0; wheels 2 r11 outboard; weapon disc r26 axis x teeth 2; extra parts: upright, fork, hook.

Likeness: aws72 0.46 (FAIL), aws74 0.31 (FAIL), aws76 0.39 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/verty_big_secret.aws74.webp` is declared `front_right_iso` (IoU 0.31 there) but the model matches it better from right (elevati; [FAIL] likeness.view: `reference/verty_big_secret.aws76.webp` is declared `front_left_iso` (IoU 0.39 there) but the model matches it better from right (elevatio

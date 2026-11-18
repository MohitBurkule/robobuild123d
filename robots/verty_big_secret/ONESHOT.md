
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

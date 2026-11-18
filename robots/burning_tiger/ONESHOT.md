
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 70x80x24 mm, ramp 0; wheels 4 r12 outboard; weapon none; 3 forks 32 mm; extra parts: lid, arm.

Likeness: aws74 0.71 (FAIL), aws76 0.66 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 70x80x24 mm, ramp 0; wheels 4 r12 outboard; weapon none; 3 forks 32 mm; extra parts: lid, arm.

Likeness: aws74 0.71 (FAIL), aws76 0.66 (FAIL).

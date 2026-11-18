
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends side_fin to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 60x112x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; 4 forks 44 mm; extra parts: side_fin, arm.

Likeness: aws76 0.58 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 60x112x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; 4 forks 32 mm; extra parts: side_fin, arm.

Likeness: aws76 0.56 (FAIL).

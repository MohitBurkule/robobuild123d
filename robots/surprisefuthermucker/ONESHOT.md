
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 85x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: lid; textured masks for indices [0].

Likeness: likeness crashed (see STRUGGLES).

## Round 2 (looks)
Decisions: type wedge; body box rect 85x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: lid.

Likeness: aws63 0.82 (FAIL).

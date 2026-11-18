
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends claw to the kit spec. ~2 min per robot plus the script.
- Body side-profile / plan polygon keys. Did instead: replaced the chassis shape in the generator. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 80x70x32 mm, ramp 0; wheels 2 r14 outboard; weapon none; extra parts: roller, claw; photos skipped (cluttered): indices [1].

Likeness: aws71 0.71 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 80x70x32 mm, ramp 0; wheels 2 r16 outboard; weapon none; extra parts: roller, claw; photos skipped (cluttered): indices [1].

Likeness: aws71 0.68 (FAIL).

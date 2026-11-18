
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends bumper to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type drum; body box rect 72x84x32 mm, ramp 0; wheels 2 r14 inboard; weapon drum r9 axis x teeth 2; extra parts: bumper; photos skipped (cluttered): indices [1].

Likeness: aws67 0.75 (FAIL).

## Round 2 (looks)
Decisions: type drum; body box rect 72x84x32 mm, ramp 0; wheels 2 r14 inboard; weapon drum r9 axis x teeth 2; extra parts: bumper; photos skipped (cluttered): indices [1].

Likeness: aws67 0.75 (FAIL).

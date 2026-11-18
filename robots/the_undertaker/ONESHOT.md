# the_undertaker: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type horizontal_spinner; body box trapezoid 75x95x24 mm, ramp 0; wheels 2 r15 outboard; weapon disc r46 axis z teeth 1; extra parts: leg; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.78 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends leg, spoke, tooth to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type horizontal_spinner; body box trapezoid 75x95x24 mm, ramp 0; wheels 2 r15 outboard; weapon ring r46 axis z teeth 1; extra parts: leg, spoke, tooth; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.72 (FAIL).

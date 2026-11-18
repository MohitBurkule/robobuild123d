# grandmaster_smash: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type other; body box rect 120x34x22 mm, ramp 0; wheels 2 r19 outboard; weapon none; 2 forks 30 mm; extra parts: barrel, tail; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.62 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends barrel, tail to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type other; body box rect 120x34x22 mm, ramp 0; wheels 2 r19 outboard; weapon none; 2 forks 30 mm; extra parts: barrel, tail; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.62 (FAIL).

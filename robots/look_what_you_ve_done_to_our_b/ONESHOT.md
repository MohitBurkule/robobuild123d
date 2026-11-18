# look_what_you_ve_done_to_our_b: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)


Likeness: aws71 0.81 (ok), aws74 0.84 (ok).

## Tools I wanted
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 95x78x28 mm, ramp 40; wheels 4 r14 outboard; weapon none; photos skipped (cluttered): indices [0].

Likeness: aws71 0.81 (ok), aws74 0.84 (ok).

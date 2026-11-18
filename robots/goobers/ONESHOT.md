# goobers: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 62x76x28 mm, ramp 52; wheels 2 r15 outboard; weapon none; extra parts: ear; clusterbot, one of 4 modelled (count read from photos, unsure).

Likeness: aws71 0.77 (FAIL), aws72 0.76 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends ear to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `cluster` in kit.json and a way to confirm the bot count. Did instead: guessed N from the photos.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 62x76x28 mm, ramp 52; wheels 2 r15 outboard; weapon none; extra parts: ear; clusterbot, one of 4 modelled (count read from photos, unsure).

Likeness: aws71 0.80 (FAIL), aws72 0.74 (FAIL).

# smashie_tip: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type vertical_spinner; body box rect 55x42x18 mm, ramp 8; wheels 2 r9 outboard; weapon disc r12 axis x teeth 2; 2 forks 25 mm; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws73 0.61 (FAIL), aws74 0.63 (FAIL), aws76 0.73 (FAIL).

## Tools I wanted
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `cluster` in kit.json and a way to confirm the bot count. Did instead: guessed N from the photos.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 55x42x18 mm, ramp 8; wheels 2 r9 outboard; weapon disc r12 axis x teeth 2; 2 forks 25 mm; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws73 0.61 (FAIL), aws74 0.63 (FAIL), aws76 0.73 (FAIL).

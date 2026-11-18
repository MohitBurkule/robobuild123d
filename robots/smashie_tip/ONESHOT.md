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

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 55x42x18 mm, ramp 24; wheels 2 r8 outboard; weapon disc r12 axis x teeth 2; 1 forks 22 mm; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws73 0.52 (FAIL), aws74 0.44 (FAIL), aws76 0.52 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/smashie_1.aws73.webp` is declared `left` (IoU 0.52 there) but the model matches it better from front_left_iso (elevation 45, az; [FAIL] likeness.view: `reference/smashie_1.aws74.webp` is declared `front` (IoU 0.44 there) but the model matches it better from front_left_iso (elevation 25, a; [FAIL] likeness.view: `reference/smashie_1.aws76.webp` is declared `front_left_iso` (IoU 0.52 there) but the model matches it better from rear_right_iso (elevat

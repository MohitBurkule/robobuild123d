# slice_and_dice: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box trapezoid 70x84x22 mm, ramp 0; wheels 2 r11 outboard; weapon none; extra parts: clamp, eye_l, eye_r; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws64 0.72 (FAIL), aws72 0.81 (ok).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends eye_l, eye_r to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `cluster` in kit.json and a way to confirm the bot count. Did instead: guessed N from the photos.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box trapezoid 70x84x22 mm, ramp 0; wheels 2 r11 outboard; weapon none; extra parts: clamp, eye_l, eye_r; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws64 0.72 (FAIL), aws72 0.81 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box trapezoid 70x84x22 mm, ramp 0; wheels 2 r11 outboard; weapon none; extra parts: clamp, eye_l, eye_r; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws64 0.10 (FAIL), aws72 0.08 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/slice_and_dice.aws64.webp` is declared `front` (IoU 0.10 there) but the model matches it better from front_left_iso (elevation ; [FAIL] likeness.view: `reference/slice_and_dice.aws72.webp` is declared `front` (IoU 0.08 there) but the model matches it better from front_right_iso (elevation

## Round 3b (rebuilt by eye from the photos: parts moved to where the photo shows them, camera set per photo)
Decisions: type lifter; body box trapezoid 70x84x22 mm, ramp 0; wheels 2 r11 outboard; weapon none; extra parts: clamp, eye_l, eye_r; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws64 0.10 (FAIL), aws72 0.08 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/slice_and_dice.aws64.webp` is declared `front` (IoU 0.10 there) but the model matches it better from front_left_iso (elevation ; [FAIL] likeness.view: `reference/slice_and_dice.aws72.webp` is declared `front` (IoU 0.08 there) but the model matches it better from front_right_iso (elevation

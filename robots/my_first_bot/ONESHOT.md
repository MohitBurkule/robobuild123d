# my_first_bot: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 105x100x36 mm, ramp 95; wheels 2 r10 inboard; weapon none; extra parts: eye_l, eye_r, post, post_top; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok), aws71 0.84 (ok).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends eye_l, eye_r, post, post_top to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 105x100x36 mm, ramp 95; wheels 2 r10 inboard; weapon none; extra parts: eye_l, eye_r, post, post_top; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok), aws71 0.84 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 105x100x36 mm, ramp 95; wheels 2 r10 inboard; weapon none; extra parts: eye_l, eye_r, post, post_top; photos skipped (cluttered): indices [0].

Likeness: aws67 0.75 (FAIL), aws71 0.46 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/my_first_bot.aws67.webp` is declared `front_left_iso` (IoU 0.75 there) but the model matches it better from rear_right_iso (ele; [FAIL] likeness.view: `reference/my_first_bot.aws71.webp` is declared `front` (IoU 0.46 there) but the model matches it better from rear_left_iso (elevation 45,

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

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 95x78x28 mm, ramp 40; wheels 4 r14 outboard; weapon none; photos skipped (cluttered): indices [0].

Likeness: aws71 0.60 (FAIL), aws74 0.67 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/look_what_you_ve_done_to_our_breakfast.aws71.webp` is declared `front_left_iso` (IoU 0.60 there) but the model matches it bette; [FAIL] likeness.view: `reference/look_what_you_ve_done_to_our_breakfast.aws74.webp` is declared `front_left_iso` (IoU 0.67 there) but the model matches it bette

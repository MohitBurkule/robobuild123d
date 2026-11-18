
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 70x56x24 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: scoop; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws68 0.52 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box rect 70x56x24 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: scoop; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws68 0.52 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 70x56x24 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: scoop; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws68 0.33 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/bzwroink.aws68.webp` is declared `front_left_iso` (IoU 0.33 there) but the model matches it better from rear_left_iso (elevatio

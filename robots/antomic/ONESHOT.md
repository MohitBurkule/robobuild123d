# antomic: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 85x80x40 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: scoop, frame; photos skipped (cluttered): indices [0, 2].

Likeness: aws67 0.80 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 85x80x40 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: scoop, frame; photos skipped (cluttered): indices [0, 2].

Likeness: aws67 0.80 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 85x80x40 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: scoop, frame; photos skipped (cluttered): indices [0, 2].

Likeness: aws67 0.41 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/antomic.aws67.webp` is declared `front` (IoU 0.41 there) but the model matches it better from front (elevation 45, azimuth 90) 

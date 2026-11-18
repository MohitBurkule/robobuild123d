# time_for_crab: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 60x92x24 mm, ramp 0; wheels 2 r13 outboard; weapon none; extra parts: claw, shaft; photos skipped (cluttered): indices [2].

Likeness: aws67 0.72 (FAIL), aws71 0.66 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends shaft to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 60x92x24 mm, ramp 0; wheels 2 r13 outboard; weapon none; extra parts: claw, shaft; photos skipped (cluttered): indices [2].

Likeness: aws67 0.72 (FAIL), aws71 0.66 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 60x92x24 mm, ramp 0; wheels 2 r13 outboard; weapon none; extra parts: claw, shaft; photos skipped (cluttered): indices [2].

Likeness: aws67 0.55 (FAIL), aws71 0.38 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/time_for_crab_.aws67.webp` is declared `front_right_iso` (IoU 0.55 there) but the model matches it better from front (elevation; [FAIL] likeness.view: `reference/time_for_crab_.aws71.webp` is declared `front` (IoU 0.38 there) but the model matches it better from front (elevation 25, azimu

# nightwish: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 80x70x26 mm, ramp 30; wheels 2 r12 outboard; weapon none; 2 forks 30 mm; extra parts: claw; photos skipped (cluttered): indices [2]; textured masks for indices [0, 1].

Likeness: aws63 0.61 (FAIL), nightwish_aws62 0.31 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 80x70x26 mm, ramp 30; wheels 2 r12 outboard; weapon none; 2 forks 22 mm; extra parts: claw; photos skipped (cluttered): indices [2]; textured masks for indices [0, 1].

Likeness: aws63 0.62 (FAIL), nightwish_aws62 0.31 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 78x62x28 mm, ramp 26; wheels 2 r12 outboard; weapon none; 2 forks 24 mm; extra parts: claw; photos skipped (cluttered): indices [2]; textured masks for indices [0, 1].

Likeness: aws63 0.54 (FAIL), nightwish_aws62 0.27 (FAIL).

## Round 3b (rebuilt by eye from the photos: parts moved to where the photo shows them, camera set per photo)
Decisions: type lifter; body box rect 78x62x28 mm, ramp 26; wheels 2 r12 outboard; weapon none; 2 forks 40 mm; extra parts: claw; photos skipped (cluttered): indices [2]; textured masks for indices [0, 1].

Likeness: aws63 0.47 (FAIL), nightwish_aws62 0.27 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/nightwish.aws63.webp` is declared `top` (IoU 0.47 there) but the model matches it better from front (elevation 25, azimuth 90) 

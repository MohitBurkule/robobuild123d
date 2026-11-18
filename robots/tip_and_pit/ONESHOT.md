# tip_and_pit: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 40x70x26 mm, ramp 0; wheels 2 r16 outboard; weapon none; extra parts: plate; clusterbot, one of 2 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0]; textured masks for indices [1].

Likeness: aws63 0.34 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (plate), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `cluster` in kit.json and a way to confirm the bot count. Did instead: guessed N from the photos.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 34x60x30 mm, ramp 0; wheels 2 r17 outboard; weapon none; extra parts: plate; clusterbot, one of 2 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0]; textured masks for indices [1].

Likeness: aws63 0.34 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 34x60x30 mm, ramp 0; wheels 2 r15 outboard; weapon none; extra parts: plate; clusterbot, one of 2 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0]; textured masks for indices [1].

Likeness: aws63 0.17 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/tip_pit.aws63.webp` is declared `front` (IoU 0.17 there) but the model matches it better from rear_right_iso (elevation 45, azi

## Round 3b (rebuilt by eye from the photos: parts moved to where the photo shows them, camera set per photo)
Decisions: type lifter; body box rect 34x60x30 mm, ramp 0; wheels 2 r15 outboard; weapon none; extra parts: plate; clusterbot, one of 2 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0]; textured masks for indices [1].

Likeness: aws63 0.16 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/tip_pit.aws63.webp` is declared `front` (IoU 0.16 there) but the model matches it better from rear_right_iso (elevation 45, azi

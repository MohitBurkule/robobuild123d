# termite_cluster: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 70x72x18 mm, ramp 0; wheels 4 r9 outboard as treads; weapon none; extra parts: scoop, lid; clusterbot, one of 3 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0].

Likeness: aws68 0.62 (FAIL), aws69 0.81 (FAIL).

## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `cluster` in kit.json and a way to confirm the bot count. Did instead: guessed N from the photos.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 70x72x18 mm, ramp 0; wheels 4 r9 outboard as treads; weapon none; extra parts: scoop, lid; clusterbot, one of 3 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0].

Likeness: aws68 0.62 (FAIL), aws69 0.81 (FAIL).

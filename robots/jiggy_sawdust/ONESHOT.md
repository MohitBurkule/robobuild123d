# jiggy_sawdust: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type other; body box rect 70x70x55 mm, ramp 0; wheels 2 r14 outboard; weapon none; extra parts: front_plate, saw_blade; photos skipped (cluttered): indices [0]; textured masks for indices [1, 2].

Likeness: likeness crashed (see STRUGGLES).

## Tools I wanted
- Kit weapon kind `saw` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type other; body box rect 70x70x55 mm, ramp 0; wheels 2 r14 outboard; weapon none; extra parts: front_plate, saw_blade; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws63 0.87 (ok).

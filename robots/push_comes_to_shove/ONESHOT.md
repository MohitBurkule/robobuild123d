
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 90x82x28 mm, ramp 30; wheels 4 r11 inboard; weapon none; extra parts: front_plate; textured masks for indices [0, 1].

Likeness: push_mk_1 0.53 (FAIL), push_mk_2 0.29 (FAIL).

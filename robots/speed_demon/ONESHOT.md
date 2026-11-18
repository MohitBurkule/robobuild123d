# speed_demon: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 95x96x30 mm, ramp 32; wheels 4 r13 outboard; weapon none; extra parts: front_plate.

Likeness: 71 0.80 (FAIL), aws72 0.82 (ok), aws74 0.88 (ok).

## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 95x96x30 mm, ramp 32; wheels 4 r13 outboard; weapon none; extra parts: front_plate.

Likeness: 71 0.80 (FAIL), aws72 0.82 (ok), aws74 0.88 (ok).

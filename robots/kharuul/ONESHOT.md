# kharuul: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 80x78x24 mm, ramp 0; wheels 4 r12 outboard; weapon none; extra parts: scoop, label.

Likeness: aws67 0.75 (FAIL).

## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends label to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 80x78x24 mm, ramp 0; wheels 4 r12 outboard; weapon none; extra parts: scoop, label.

Likeness: aws67 0.75 (FAIL).

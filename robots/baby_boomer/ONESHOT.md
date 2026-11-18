# baby_boomer: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type flipper; body box rect 80x84x24 mm, ramp 0; wheels 4 r11 outboard; weapon none; 2 forks 38 mm; extra parts: flipper; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.67 (FAIL).

## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (flipper), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type flipper; body box rect 72x84x24 mm, ramp 0; wheels 4 r11 outboard; weapon none; 2 forks 38 mm; extra parts: flipper; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.70 (FAIL).

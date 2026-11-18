# auger_the_top: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type other; body box rect 95x48x24 mm, ramp 0; wheels 4 r10 outboard; weapon none; 4 forks 50 mm; extra parts: axe_arm, ?; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.54 (FAIL).

## Tools I wanted
- Kit weapon kind `axe` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends ? to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type other; body box rect 95x52x22 mm, ramp 0; wheels 4 r10 outboard; weapon none; 4 forks 80 mm; extra parts: axe_arm, ?; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.48 (FAIL).

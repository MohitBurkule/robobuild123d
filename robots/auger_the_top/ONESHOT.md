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

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type other; body box rect 46x112x22 mm, ramp 0; wheels 2 r12 inboard; weapon none; 4 forks 60 mm; extra parts: endcap, boss_in, boss_out, servo_house, arm_a, arm_b, arm_pivot_pin, head_block, auger_motor, auger_bit; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.60 (FAIL).
Other likeness findings: [FAIL] likeness.weapon: Photos: axe turns about x; `arm_a` turns about y (axis [0.0, 1.0, 0.0]). x = across the robot (horizontal drum/vertical disc), z = up (h


## Tools I wanted
- Kit weapon kind `axe` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends side_pod to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type vertical_spinner; body box rect 80x80x22 mm, ramp 0; wheels 4 r11 outboard; weapon disc r15 axis x teeth 2; 2 forks 62 mm; extra parts: tail_arm, side_pod.

Likeness: aws74 0.68 (FAIL), aws76 0.69 (FAIL), aws77 0.69 (FAIL).
Other likeness findings: [FAIL] likeness.weapon: Photos show a disc; `tail_arm` is a `axe` (`weapon.kind`).; [FAIL] likeness.weapon: Photos: disc turns about x; `tail_arm` turns about z (axis [0.0, 0.0, 1.0]). x = across the robot (horizontal drum/vertical disc), z = u; [FAIL] likeness.weapon: Photos show 2 teeth; `tail_arm` declares None (`weapon.teeth`; shape.weapon_profile measures it).

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 80x80x22 mm, ramp 0; wheels 4 r11 outboard; weapon disc r15 axis x teeth 2; 2 forks 62 mm; extra parts: tail_arm, side_pod.

Likeness: aws74 0.68 (FAIL), aws76 0.69 (FAIL), aws77 0.69 (FAIL).
Other likeness findings: [FAIL] likeness.weapon: Photos show a disc; `tail_arm` is a `axe` (`weapon.kind`).; [FAIL] likeness.weapon: Photos: disc turns about x; `tail_arm` turns about z (axis [0.0, 0.0, 1.0]). x = across the robot (horizontal drum/vertical disc), z = u; [FAIL] likeness.weapon: Photos show 2 teeth; `tail_arm` declares None (`weapon.teeth`; shape.weapon_profile measures it).

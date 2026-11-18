
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends side_fin to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 60x112x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; 4 forks 44 mm; extra parts: side_fin, arm.

Likeness: aws76 0.58 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 60x112x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; 4 forks 32 mm; extra parts: side_fin, arm.

Likeness: aws76 0.56 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 60x112x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; 4 forks 34 mm; extra parts: arm, side_fin.

Likeness: aws76 0.29 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/whopper.aws76.webp` is declared `front_right_iso` (IoU 0.29 there) but the model matches it better from front_left_iso (elevati


## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends motor to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type vertical_spinner; body twin_pods rect 70x130x24 mm, ramp 0; wheels 2 r11 inboard; weapon disc r28 axis x teeth 2; 4 forks 40 mm; extra parts: motor; photos skipped (cluttered): indices [1].

Likeness: aws72 0.62 (FAIL).

## Round 2 (looks)
Decisions: type vertical_spinner; body twin_pods rect 60x140x24 mm, ramp 0; wheels 2 r11 inboard; weapon disc r28 axis x teeth 2; 4 forks 46 mm; extra parts: motor; photos skipped (cluttered): indices [1].

Likeness: aws72 0.61 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body twin_pods rect 60x126x24 mm, ramp 0; wheels 2 r11 inboard; weapon disc r28 axis x teeth 2; 4 forks 46 mm; extra parts: motor; photos skipped (cluttered): indices [1].

Likeness: aws72 0.59 (FAIL).

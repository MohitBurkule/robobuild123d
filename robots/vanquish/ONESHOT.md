
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends motor, upright to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type vertical_spinner; body box rect 75x46x24 mm, ramp 0; wheels 2 r11 inboard; weapon bar r42 axis x teeth 2; 2 forks 62 mm; extra parts: motor, upright.

Likeness: aws76 0.52 (FAIL).

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 90x40x24 mm, ramp 0; wheels 2 r11 inboard; weapon bar r44 axis x teeth 2; extra parts: motor, upright, fork.

Likeness: aws76 0.45 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 90x40x24 mm, ramp 0; wheels 2 r11 inboard; weapon bar r52 axis x teeth 2; extra parts: motor, upright, fork.

Likeness: aws76 0.38 (FAIL).

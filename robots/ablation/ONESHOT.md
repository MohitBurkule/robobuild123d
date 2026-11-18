
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends arm, arm_base to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 72x92x26 mm, ramp 0; wheels 4 r11 outboard; weapon disc r11 axis x teeth 2; 4 forks 62 mm; extra parts: arm, arm_base.

Likeness: aws72 0.65 (FAIL), aws74 0.61 (FAIL), aws76 0.53 (FAIL).


## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends fork, motor to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body twin_pods rect 70x120x22 mm, ramp 0; wheels 2 r12 outboard; weapon disc r22 axis x teeth 2; extra parts: fork, motor.

Likeness: aws72 0.67 (FAIL), aws74 0.62 (FAIL), aws76 0.61 (FAIL).

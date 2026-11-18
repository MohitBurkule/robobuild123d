
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (top_plate), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends weapon_arm, weapon_shaft, drum_flange, weapon_motor_can to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type drum; body box pentagon 86x104x24 mm, ramp 0; wheels 2 r17 inboard; weapon drum r11 axis x teeth 2; 2 forks 46 mm; extra parts: weapon_arm, weapon_shaft, drum_flange, top_plate, weapon_motor_can.

Likeness: aws74 0.69 (FAIL), aws76 0.72 (FAIL), aws77 0.76 (FAIL).

# unstoppable_force: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type drum; body box round_nose 100x100x30 mm, ramp 0; wheels 2 r17 inboard; weapon drum r14 axis x teeth 2; extra parts: drum_arm.

Likeness: aws69 0.86 (ok), aws71 0.90 (ok), aws72 0.88 (ok).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends drum_arm to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type drum; body box round_nose 100x100x30 mm, ramp 0; wheels 2 r17 inboard; weapon drum r14 axis x teeth 2; extra parts: drum_arm.

Likeness: aws69 0.86 (ok), aws71 0.90 (ok), aws72 0.88 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type drum; body box round_nose 100x100x30 mm, ramp 0; wheels 2 r17 inboard; weapon drum r14 axis x teeth 2; extra parts: drum_arm.

Likeness: aws69 0.81 (ok), aws71 0.71 (FAIL), aws72 0.80 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/unstoppable_force.aws71.webp` is declared `front_left_iso` (IoU 0.71 there) but the model matches it better from front_left_iso; [FAIL] likeness.view: `reference/unstoppable_force.aws72.webp` is declared `front_left_iso` (IoU 0.80 there) but the model matches it better from front_right_is

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **56 -> 10** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): unstoppable_force.aws69.webp 0.81 -> 0.81, unstoppable_force.aws71.webp 0.71 -> 0.71, unstoppable_force.aws72.webp 0.80 -> 0.80

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch sunk in the top skin, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm, hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- weapon motor inside weapon (outrunner-in-drum), bore cut
- dt_shaft_weapon: split into two stub axles round the in-drum motor
- chassis: hollowed (box wall round pockets), 184895 -> 83133 mm3
- drum_arm_l: hollowed (exact wall round pockets), 8314 -> 7166 mm3 (4 thin spots kept solid)
- drum_arm_r: hollowed (exact wall round pockets), 8298 -> 7201 mm3 (5 thin spots kept solid)
- wire w_phases: no via round the rotor found
- drum_arm_l: printed with the weapon axis as build direction
- drum_arm_r: printed with the weapon axis as build direction

Left (one line each):
- likeness.view x2: looks (photo view label; not part of this pass)
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- retention.loose x1: in-drum outrunner: the stator end plate that holds it is declared, not modelled
- process.geometry x1: kit weapon shape is not a pure 2D/3-axis profile for its process (look)
- mfg.layer_load x1: the main chassis carries the weapon axle but prints flat (+z); printing it on its side along the axle is a separate redesign
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- wire.rotor_clearance x1: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found

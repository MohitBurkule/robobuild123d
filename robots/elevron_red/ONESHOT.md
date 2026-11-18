# elevron_red: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box pentagon 90x92x26 mm, ramp 25; wheels 2 r13 inboard; weapon none; 2 forks 30 mm; extra parts: lift_arm, pod.

Likeness: aws72 0.70 (FAIL), aws74 0.70 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends pod to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box pentagon 92x78x20 mm, ramp 22; wheels 2 r13 inboard; weapon none; 2 forks 30 mm; extra parts: lift_arm, pod.

Likeness: aws72 0.69 (FAIL), aws74 0.64 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box pentagon 92x78x20 mm, ramp 22; wheels 4 r12 inboard; weapon none; 2 forks 48 mm; extra parts: lift_arm, pod.

Likeness: aws72 0.70 (FAIL), aws74 0.54 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/elevron_red.aws74.webp` is declared `front_right_iso` (IoU 0.54 there) but the model matches it better from front_right_iso (el

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **70 -> 20** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): elevron_red.aws72.webp 0.702 -> 0.702, elevron_red.aws74.webp 0.544 -> 0.544

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- dt_axle_wheel_l1 replaced by the gearmotor shaft
- dt_axle_wheel_r1 replaced by the gearmotor shaft
- joint lift_arm sweeps 3.8 mm into chassis: too deep to clear without changing the look
- chassis: hollowed (box wall round pockets), 81839 -> 59278 mm3 (11 thin spots kept solid)
- pod_l: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- pod_r: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- wire w_bat_sw: no via round the rotor found
- wire w_sw_esc: no via round the rotor found
- wire w_m1: no via round the rotor found
- wire w_m2: no via round the rotor found
- wire w_m3: no via round the rotor found
- wire w_m4: no via round the rotor found
- fork_0: 2.5 mm titanium is not a stock gauge; material -> steel (same 2.5 mm plate)
- fork_1: 2.5 mm titanium is not a stock gauge; material -> steel (same 2.5 mm plate)

Left (one line each):
- wire.rotor_clearance x6: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- proxy.interference x3: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- connection.floating x2: part does not touch the print anywhere (kit geometry); no honest joint to declare
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- proxy.sweep x1: moving part runs into the chassis more than a running clearance can take without changing the look
- power.weapon_motor x1: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- process.weapon_printed x1: toolchain: printed lifter/flipper arms are judged like spinner teeth (metal inserts required)
- electrical.battery_weapon_gap x1: battery pocket close to the weapon envelope; no other room inside the print
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- likeness.view x1: looks (photo view label; not part of this pass)

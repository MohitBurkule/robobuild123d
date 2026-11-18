# step_up: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 80x66x22 mm, ramp 0; wheels 4 r14 outboard; weapon none; extra parts: lifter; photos skipped (cluttered): indices [0, 1].

Likeness: aws72 0.75 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 80x66x22 mm, ramp 0; wheels 4 r14 outboard; weapon none; extra parts: lifter; photos skipped (cluttered): indices [0, 1].

Likeness: aws72 0.76 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 80x66x22 mm, ramp 0; wheels 4 r14 outboard; weapon none; extra parts: lifter; photos skipped (cluttered): indices [0, 1].

Likeness: aws72 0.70 (FAIL).

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **60 -> 15** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): step_up.aws72.webp 0.705 -> 0.706

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
- joint lifter: its sweep would cut a 8 mm deep slot into the outside of chassis (8 mm for the poses at 0..80 deg alone); left out (look kept)
- chassis: hollowed (box wall round pockets), 86705 -> 56390 mm3
- wire w_bat_sw: no via round the rotor found
- wire w_sw_esc: no via round the rotor found
- wire w_m1: no via round the rotor found
- wire w_m2: no via round the rotor found
- wire w_m3: no via round the rotor found
- wire w_m4: no via round the rotor found

Left (one line each):
- wire.rotor_clearance x6: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- integrity.volume x1: volume store from an earlier run differs (tool-side baseline)
- proxy.interference x1: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- proxy.sweep x1: moving part runs into the chassis more than a running clearance can take without changing the look
- power.weapon_motor x1: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- process.weapon_printed x1: toolchain: printed lifter/flipper arms are judged like spinner teeth (metal inserts required)
- electrical.battery_weapon_gap x1: battery pocket close to the weapon envelope; no other room inside the print
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)
- battery.rotor_gap x1: toolchain for lifters: the arm's full-turn envelope is used, which covers the whole chassis

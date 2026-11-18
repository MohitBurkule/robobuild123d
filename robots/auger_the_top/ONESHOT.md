# auger_the_top: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type other; body box rect 95x48x24 mm, ramp 0; wheels 4 r10 outboard; weapon none; 4 forks 50 mm; extra parts: axe_arm, ?; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.54 (FAIL).

## Tools I wanted
- Kit weapon kind `axe` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends ? to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type other; body box rect 95x52x22 mm, ramp 0; wheels 4 r10 outboard; weapon none; 4 forks 80 mm; extra parts: axe_arm, ?; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.48 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type other; body box rect 46x112x22 mm, ramp 0; wheels 2 r12 inboard; weapon none; 4 forks 60 mm; extra parts: endcap, boss_in, boss_out, servo_house, arm_a, arm_b, arm_pivot_pin, head_block, auger_motor, auger_bit; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.60 (FAIL).
Other likeness findings: [FAIL] likeness.weapon: Photos: axe turns about x; `arm_a` turns about y (axis [0.0, 1.0, 0.0]). x = across the robot (horizontal drum/vertical disc), z = up (h

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **108 -> 17** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): auger_the_top.aws72.webp 0.615 -> 0.615

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- endcap_l: hidden 3 mm key into chassis (one print)
- endcap_r: hidden 3 mm key into chassis (one print)
- servo_house: hidden 3 mm key into chassis (one print)
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- joint arm_a: its sweep would cut a 6 mm deep slot into the outside of servo_house (6 mm for the poses at 0..80 deg alone); left out (look kept)
- joint arm_a: 0.9 mm sweep clearance cut in chassis
- chassis: hollowed (box wall round pockets), 72911 -> 47710 mm3
- servo_house: hollowed (exact wall round pockets), 15452 -> 13328 mm3 (19 thin spots kept solid)
- head_block: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- auger_motor: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- auger_bit: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- wire w_m2: no via round the rotor found

Left (one line each):
- proxy.interference x7: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- integrity.solids x2: tessellation of round/revolved shapes (open pole shells) or a boolean in the kit shape
- integrity.volume x2: volume store from an earlier run differs (tool-side baseline)
- proxy.sweep x1: moving part runs into the chassis more than a running clearance can take without changing the look
- power.weapon_motor x1: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- electrical.battery_weapon_gap x1: battery pocket close to the weapon envelope; no other room inside the print
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- wire.rotor_clearance x1: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

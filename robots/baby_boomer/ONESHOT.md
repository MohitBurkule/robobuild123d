# baby_boomer: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type flipper; body box rect 80x84x24 mm, ramp 0; wheels 4 r11 outboard; weapon none; 2 forks 38 mm; extra parts: flipper; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.67 (FAIL).

## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (flipper), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type flipper; body box rect 72x84x24 mm, ramp 0; wheels 4 r11 outboard; weapon none; 2 forks 38 mm; extra parts: flipper; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.70 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box rect 72x84x24 mm, ramp 0; wheels 4 r11 outboard; weapon none; 2 forks 40 mm; extra parts: flipper; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.60 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/baby_boomer.aws72.webp` is declared `front` (IoU 0.60 there) but the model matches it better from front_right_iso (elevation 45

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **81 -> 13** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): baby_boomer.aws72.webp 0.598 -> 0.598

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
- joint flipper: its sweep would cut a 5 mm deep slot into the outside of chassis; left out (look kept)
- chassis: hollowed (box wall round pockets), 117207 -> 63043 mm3
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
- proxy.interference x1: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- proxy.sweep x1: moving part runs into the chassis more than a running clearance can take without changing the look
- power.weapon_motor x1: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- process.weapon_printed x1: toolchain: printed lifter/flipper arms are judged like spinner teeth (metal inserts required)
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

## Round 3e (strict photo differences: real openings, hinge, plates, screws where the photo shows them)
Decisions: type flipper; body box rect 72x84x24 mm, ramp 0; wheels 4 r11 outboard; weapon none; 2 forks 40 mm; extra parts: flipper, ramp_tip, top_plate, hinge_leaf, hinge_pin, scr0, scr1, scr2, scr3, scr4; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.80 (FAIL).

# flippant: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type flipper; body box rect 95x100x28 mm, ramp 35; wheels 2 r14 inboard; weapon none; extra parts: hoop, lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws69 0.88 (ok).

## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type flipper; body box rect 95x100x28 mm, ramp 35; wheels 2 r14 inboard; weapon none; extra parts: hoop, lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws69 0.88 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box rect 95x100x28 mm, ramp 35; wheels 2 r14 inboard; weapon none; extra parts: hoop, lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws69 0.85 (ok).

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **63 -> 12** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): flippant.aws69.webp 0.850 -> 0.849

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- joint hoop_l: 0.9 mm sweep clearance cut in chassis
- joint hoop_l: 0.9 mm sweep clearance cut in lid
- joint hoop_r: 0.9 mm sweep clearance cut in chassis
- joint hoop_r: 0.9 mm sweep clearance cut in lid
- chassis: hollowed (box wall round pockets), 186793 -> 79058 mm3
- wire w_bat_sw: no via round the rotor found
- wire w_sw_esc: no via round the rotor found
- wire w_m1: no via round the rotor found
- wire w_m2: no via round the rotor found

Left (one line each):
- wire.rotor_clearance x5: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- power.weapon_motor x2: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- process.weapon_printed x2: toolchain: printed lifter/flipper arms are judged like spinner teeth (metal inserts required)
- geom.tiny_edge x2: see verify_r4.txt root causes
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes

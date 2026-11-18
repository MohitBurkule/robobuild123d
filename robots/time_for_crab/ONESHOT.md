# time_for_crab: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 60x92x24 mm, ramp 0; wheels 2 r13 outboard; weapon none; extra parts: claw, shaft; photos skipped (cluttered): indices [2].

Likeness: aws67 0.72 (FAIL), aws71 0.66 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends shaft to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 60x92x24 mm, ramp 0; wheels 2 r13 outboard; weapon none; extra parts: claw, shaft; photos skipped (cluttered): indices [2].

Likeness: aws67 0.72 (FAIL), aws71 0.66 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 60x92x24 mm, ramp 0; wheels 2 r13 outboard; weapon none; extra parts: claw, shaft; photos skipped (cluttered): indices [2].

Likeness: aws67 0.55 (FAIL), aws71 0.38 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/time_for_crab_.aws67.webp` is declared `front_right_iso` (IoU 0.55 there) but the model matches it better from front (elevation; [FAIL] likeness.view: `reference/time_for_crab_.aws71.webp` is declared `front` (IoU 0.38 there) but the model matches it better from front (elevation 25, azimu

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **58 -> 21** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): time_for_crab_.aws67.webp 0.552 -> 0.552, time_for_crab_.aws71.webp 0.381 -> 0.381

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- joint claw_l sweeps 6.7 mm into chassis: too deep to clear without changing the look
- joint claw_l sweeps 3.6 mm into shaft: too deep to clear without changing the look
- joint claw_r sweeps 6.7 mm into chassis: too deep to clear without changing the look
- joint claw_r sweeps 3.6 mm into shaft: too deep to clear without changing the look
- chassis: hollowed (box wall round pockets), 113863 -> 56461 mm3
- shaft: hollowed (exact wall round pockets), 5477 -> 4078 mm3
- wire w_m1: no via round the rotor found
- wire w_m2: no via round the rotor found

Left (one line each):
- proxy.interference x4: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- proxy.sweep x2: moving part runs into the chassis more than a running clearance can take without changing the look
- power.weapon_motor x2: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- process.weapon_printed x2: toolchain: printed lifter/flipper arms are judged like spinner teeth (metal inserts required)
- wire.rotor_clearance x2: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- likeness.view x2: looks (photo view label; not part of this pass)
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- battery.rotor_gap x2: toolchain for lifters: the arm's full-turn envelope is used, which covers the whole chassis
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- electrical.battery_weapon_gap x1: battery pocket close to the weapon envelope; no other room inside the print
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes

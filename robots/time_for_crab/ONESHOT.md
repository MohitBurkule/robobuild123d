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
Blockers r3 -> r4: **58 -> 16** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): time_for_crab_.aws67.webp 0.567 -> 0.567, time_for_crab_.aws71.webp 0.381 -> 0.381

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (6 of 7 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- el_battery: placed with 4.0 mm of lead room round it
- el_rx_esc: placed with 4.0 mm of lead room round it
- claw_l: no room for a micro servo; driven by an N10 300 rpm gearmotor (catalog n10_300rpm_6v, 900 g.cm stall) in a closed pocket 4 mm from the hinge, on a dual brushed ESC (esc_dual_brushed) fed from the receiver's weapon channel; the gear link to the arm is declared, not modelled
- claw_r: no room inside the print for a micro servo (32 x 12 x 22.7 mm) or an N10 gearmotor; actuator left out
- joint claw_l sweeps 6.7 mm into chassis: too deep to clear without changing the look
- joint claw_l sweeps 3.6 mm into shaft: too deep to clear without changing the look
- joint claw_r sweeps 6.7 mm into chassis: too deep to clear without changing the look
- joint claw_r sweeps 3.6 mm into shaft: too deep to clear without changing the look
- chassis: hollowed (box wall round pockets), 107712 -> 59014 mm3
- shaft: hollowed (exact wall round pockets), 4998 -> 4416 mm3 (4 thin spots kept solid)
- wiring channels: 7 of 7 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin

Left (one line each):
- proxy.interference x4: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- proxy.sweep x2: moving part runs into the chassis more than a running clearance can take without changing the look
- likeness.view x2: looks (photo view label; not part of this pass)
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- proxy.wiring x1: see verify_r4.txt root causes
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- retention.loose x1: in-drum outrunner: the stator end plate that holds it is declared, not modelled
- power.weapon_motor x1: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- wire.render_wires x1: a robot render does not draw every wire: at least one wire has no route through the print
- wire.render_count x1: render record lists fewer routes than the spec has wires (a wire found no route)

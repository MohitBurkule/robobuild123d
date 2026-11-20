# grandmaster_smash: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type other; body box rect 120x34x22 mm, ramp 0; wheels 2 r19 outboard; weapon none; 2 forks 30 mm; extra parts: barrel, tail; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.62 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends barrel, tail to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type other; body box rect 120x34x22 mm, ramp 0; wheels 2 r19 outboard; weapon none; 2 forks 30 mm; extra parts: barrel, tail; photos skipped (cluttered): indices [0, 2].

Likeness: aws72 0.62 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type drum; body box rect 44x124x18 mm, ramp 0; wheels 2 r16 inboard; weapon drum r20 axis x teeth 2; 2 forks 62 mm; extra parts: endcap, hub, flywheel, weapon_shaft, upright_a, upright_b, weapon_rail, end_wedge; photos skipped (cluttered): indices [0].

Likeness: aws72 0.76 (FAIL), aws73 0.49 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/grandmaster_smash.aws73.webp` is declared `front_left_iso` (IoU 0.49 there) but the model matches it better from right (elevati

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **97 -> 29** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): grandmaster_smash.aws72.webp 0.76 -> 0.76, grandmaster_smash.aws73.webp 0.49 -> 0.49

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- dm_wheel_l0: gearmotor pocket is only 73% inside the print (pocket opens the skin there)
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dm_wheel_r0: gearmotor pocket is only 73% inside the print (pocket opens the skin there)
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- weapon motor inside weapon (outrunner-in-drum), bore cut
- dt_shaft_weapon: split into two stub axles round the in-drum motor
- chassis: hollowed (box wall round pockets), 54232 -> 40845 mm3
- hub_l: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- hub_r: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- weapon_shaft: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- upright_a: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- wire w_phases: no via round the rotor found

Left (one line each):
- proxy.interference x13: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- proxy.sweep x2: moving part runs into the chassis more than a running clearance can take without changing the look
- mfg.layer_load x2: the main chassis carries the weapon axle but prints flat (+z); printing it on its side along the axle is a separate redesign
- fit.interference x2: catalog part pocket overlaps another body
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- retention.loose x1: in-drum outrunner: the stator end plate that holds it is declared, not modelled
- process.geometry x1: kit weapon shape is not a pure 2D/3-axis profile for its process (look)
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- wire.rotor_clearance x1: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- wire.exterior_support x1: see verify_r4.txt root causes
- likeness.view x1: looks (photo view label; not part of this pass)
- wire.outside x1: see verify_r4.txt root causes

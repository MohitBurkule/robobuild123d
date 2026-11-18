# counterinsurgency: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 50x120x14 mm, ramp 0; wheels 2 r9 inboard; weapon none; 3 forks 36 mm; extra parts: side_arm.

Likeness: aws76 0.67 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends side_arm to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 50x120x14 mm, ramp 0; wheels 2 r9 inboard; weapon none; 3 forks 36 mm; extra parts: side_arm.

Likeness: aws76 0.61 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 50x120x14 mm, ramp 0; wheels 2 r9 inboard; weapon none; 3 forks 36 mm; extra parts: side_arm, deck.

Likeness: aws76 0.39 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/counterinsurgency.aws76.webp` is declared `front_left_iso` (IoU 0.39 there) but the model matches it better from front_right_is

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **82 -> 4** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): counterinsurgency.aws76.webp 0.389 -> 0.389

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- deck: hidden 3 mm key into chassis (one print)
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- el_battery: pocket wall only 1.0 mm
- side_arm_l: cuts split it into 2 pieces, each joined to the print
- side_arm_r: cuts split it into 2 pieces, each joined to the print
- chassis: hollowed (box wall round pockets), 61942 -> 41518 mm3
- side_arm_l: hollowed (exact wall round pockets), 11591 -> 9062 mm3
- side_arm_r: hollowed (exact wall round pockets), 11591 -> 9062 mm3
- deck: hollowed (exact wall round pockets), 16814 -> 11925 mm3

Left (one line each):
- legal.footprint x1: see verify_r4.txt root causes
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

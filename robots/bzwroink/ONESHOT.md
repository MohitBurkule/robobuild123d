
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 70x56x24 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: scoop; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws68 0.52 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box rect 70x56x24 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: scoop; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws68 0.52 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 70x56x24 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: scoop; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws68 0.33 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/bzwroink.aws68.webp` is declared `front_left_iso` (IoU 0.33 there) but the model matches it better from rear_left_iso (elevatio

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **55 -> 5** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): bzwroink.aws68.webp 0.326 -> 0.326

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
- chassis: hollowed (box wall round pockets), 66910 -> 48611 mm3

Left (one line each):
- proxy.interference x2: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

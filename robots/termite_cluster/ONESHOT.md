# termite_cluster: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 70x72x18 mm, ramp 0; wheels 4 r9 outboard as treads; weapon none; extra parts: scoop, lid; clusterbot, one of 3 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0].

Likeness: aws68 0.62 (FAIL), aws69 0.81 (FAIL).

## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `cluster` in kit.json and a way to confirm the bot count. Did instead: guessed N from the photos.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 70x72x18 mm, ramp 0; wheels 4 r9 outboard as treads; weapon none; extra parts: scoop, lid; clusterbot, one of 3 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0].

Likeness: aws68 0.62 (FAIL), aws69 0.81 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 66x70x16 mm, ramp 0; wheels 4 r9 outboard; weapon none; extra parts: scoop, lid; clusterbot, one of 3 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0].

Likeness: aws68 0.61 (FAIL), aws69 0.61 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/termite_cluster.aws69.webp` is declared `top` (IoU 0.61 there) but the model matches it better from rear (elevation 45, azimuth

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **61 -> 7** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): termite_cluster.aws68.webp 0.611 -> 0.611, termite_cluster.aws69.webp 0.614 -> 0.614

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
- chassis: hollowed (box wall round pockets), 47281 -> 39665 mm3
- scoop: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- lid: does not sit in any print part (no overlap to cut a seat from); left without a declared joint

Left (one line each):
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- proxy.interference x1: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- connection.floating x1: part does not touch the print anywhere (kit geometry); no honest joint to declare
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- likeness.view x1: looks (photo view label; not part of this pass)

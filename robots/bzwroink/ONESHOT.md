
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
Blockers r3 -> r4: **55 -> 1** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): bzwroink.aws68.webp 0.452 -> 0.451

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (6 of 6 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- dt_axle_wheel_l1 replaced by the gearmotor shaft
- dt_axle_wheel_r1 replaced by the gearmotor shaft
- el_battery: placed with 4.0 mm of lead room round it
- el_rx_esc: placed with 4.0 mm of lead room round it
- chassis: hollowed (box wall round pockets), 66910 -> 48810 mm3
- wiring channels: 6 of 6 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin
- wiring channels: a piece of ['w_bat_sw'] left out where it would come within 2 mm of the outside (port close to the skin)
- drive gearmotors moved 0.5 mm outboard so the back-to-back pair does not touch at the middle; switch pocket keeps 4 mm free above the switch for its pins and leads (the switch no longer sits under a motor)

Left (one line each):
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

## Round 5 (photo / DESCRIPTION.md)
- The clear scoop now runs from just under the body's top front edge down to the floor at 32 degrees (aws61 / aws65), instead of a flat plate on the floor. Its narrow root (32 mm) is keyed in a slot between the front lid screws.
- Wheels: pale-pink tyres with hot-pink hubs (aws61).
- Blockers 1 (r4) / 2 after the dev merge (new `likeness.view`: REFERENCE.json declares aws68 front_left_iso, but the photo shows the robot from the rear-left; collector file, not edited) -> 2. IoU 0.33 -> 0.34.

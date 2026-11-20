# diplomatic_embargo: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 95x66x24 mm, ramp 0; wheels 4 r11 outboard as treads; weapon none; 3 forks 30 mm; extra parts: front_plate.

Likeness: aws72 0.85 (ok), aws76 0.70 (FAIL).

## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 95x66x24 mm, ramp 0; wheels 4 r11 outboard as treads; weapon none; 3 forks 30 mm; extra parts: front_plate.

Likeness: aws72 0.85 (ok), aws76 0.70 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 95x66x24 mm, ramp 0; wheels 4 r11 outboard; weapon none; 3 forks 46 mm; extra parts: front_plate.

Likeness: aws72 0.68 (FAIL), aws76 0.49 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/diplomatic_embargo.aws76.webp` is declared `front_left_iso` (IoU 0.49 there) but the model matches it better from rear_left_iso

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **100 -> 5** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): diplomatic_embargo.aws72.webp 0.699 -> 0.699, diplomatic_embargo.aws76.webp 0.527 -> 0.527

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
- chassis: hollowed (box wall round pockets), 122359 -> 66397 mm3
- wiring channels: 6 of 6 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin
- wiring channels: a piece of ['w_bat_sw'] left out where it would come within 2 mm of the outside (port close to the skin)
- fork_0: 2.5 mm titanium is not a stock gauge; material -> steel (same 2.5 mm plate)
- fork_1: 2.5 mm titanium is not a stock gauge; material -> steel (same 2.5 mm plate)
- fork_2: 2.5 mm titanium is not a stock gauge; material -> steel (same 2.5 mm plate)

Left (one line each):
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- connection.cover_fasteners x1: see verify_r4.txt root causes
- likeness.view x1: looks (photo view label; not part of this pass)
- geom.tiny_edge x1: see verify_r4.txt root causes

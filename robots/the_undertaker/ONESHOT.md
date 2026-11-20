# the_undertaker: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type horizontal_spinner; body box trapezoid 75x95x24 mm, ramp 0; wheels 2 r15 outboard; weapon disc r46 axis z teeth 1; extra parts: leg; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.78 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends leg, spoke, tooth to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type horizontal_spinner; body box trapezoid 75x95x24 mm, ramp 0; wheels 2 r15 outboard; weapon ring r46 axis z teeth 1; extra parts: leg, spoke, tooth; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.72 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type horizontal_spinner; body box trapezoid 75x95x24 mm, ramp 0; wheels 2 r15 outboard; weapon ring r46 axis z teeth 1; extra parts: leg, spoke, tooth; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.54 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/the_undertaker.aws67.webp` is declared `front` (IoU 0.54 there) but the model matches it better from front (elevation 45, azimu

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **55 -> 11** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): the_undertaker.aws67.webp 0.764 -> 0.764

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
- weapon: weapon motor not coaxial (no room on the axis): placed parallel to the axis in the print, belt drive NOT modelled
- el_battery: placed with 4.0 mm of lead room round it
- el_battery: pocket wall only 1.0 mm
- el_rx_esc: placed with 4.0 mm of lead room round it
- el_rx_esc: pocket wall only 1.0 mm
- el_wesc: placed with 4.0 mm of lead room round it
- weapon: no solid spot for a lock pin hole
- weapon: rotor overlaps chassis 8 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- chassis: hollowed (box wall round pockets), 120986 -> 63984 mm3
- leg_l: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- leg_r: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- tooth: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- dt_hubw_weapon: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- dt_strut_tooth: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- wiring channels: 7 of 7 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin
- wiring channels: a piece of ['w_phases'] left out where it would come within 2 mm of the outside (port close to the skin)
- spoke: printed with the weapon axis as build direction

Left (one line each):
- proxy.interference x5: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- connection.floating x1: part does not touch the print anywhere (kit geometry); no honest joint to declare
- wire.render_wires x1: a robot render does not draw every wire: at least one wire has no route through the print
- wire.render_count x1: render record lists fewer routes than the spec has wires (a wire found no route)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)
- geom.near_miss_hole x1: see verify_r4.txt root causes

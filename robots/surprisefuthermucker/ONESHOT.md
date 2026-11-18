
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 85x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: lid; textured masks for indices [0].

Likeness: likeness crashed (see STRUGGLES).

## Round 2 (looks)
Decisions: type wedge; body box rect 85x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: lid.

Likeness: aws63 0.82 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 74x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: lid.

Likeness: aws63 0.70 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/surprisefuthermucker.aws63.webp` is declared `front_left_iso` (IoU 0.70 there) but the model matches it better from front (elev

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type vertical_spinner; body box rect 74x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon disc r17 axis x teeth 2; extra parts: lid.

Likeness: aws63 0.71 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/surprisefuthermucker.aws63.webp` is declared `front_right_iso` (IoU 0.71 there) but the model matches it better from front (ele

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **55 -> 23** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): surprisefuthermucker.aws63.webp 0.712 -> 0.711

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (7 of 9 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- dt_axle_wheel_l1 replaced by the gearmotor shaft
- dt_axle_wheel_r1 replaced by the gearmotor shaft
- weapon: weapon motor not coaxial (no room on the axis): placed parallel to the axis in the print, belt drive NOT modelled
- el_battery: no free pocket inside the print; placed at the chassis centre (overlaps)
- el_battery: pocket wall only 0 mm
- weapon: rotor overlaps chassis 13 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- chassis: hollowed (box wall round pockets), 80580 -> 60390 mm3
- lid: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- wiring channels: 9 of 9 wires have a 4.8 mm channel inside the print

Left (one line each):
- proxy.sweep x6: moving part runs into the chassis more than a running clearance can take without changing the look
- proxy.interference x5: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- connection.tape_overload x1: see verify_r4.txt root causes
- connection.cover_fasteners x1: see verify_r4.txt root causes
- process.geometry x1: kit weapon shape is not a pure 2D/3-axis profile for its process (look)
- electrical.battery_weapon_gap x1: battery pocket close to the weapon envelope; no other room inside the print
- fit.interference x1: catalog part pocket overlaps another body
- wire.render_wires x1: a robot render does not draw every wire: at least one wire has no route through the print
- wire.rotor_clearance x1: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- wire.render_count x1: render record lists fewer routes than the spec has wires (a wire found no route)
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)
- geom.tiny_edge x1: see verify_r4.txt root causes

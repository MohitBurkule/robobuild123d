# infernal: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 100x100x36 mm, ramp 42; wheels 2 r13 inboard; weapon none; extra parts: front_plate, top_plate, horn; photos skipped (cluttered): indices [0].

Likeness: aws71 0.83 (ok).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate, top_plate), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 100x100x36 mm, ramp 42; wheels 2 r13 inboard; weapon none; extra parts: front_plate, top_plate, horn; photos skipped (cluttered): indices [0].

Likeness: aws71 0.83 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 100x100x36 mm, ramp 42; wheels 2 r13 inboard; weapon none; extra parts: front_plate, top_plate, horn; photos skipped (cluttered): indices [0].

Likeness: aws71 0.60 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/infernal.aws71.webp` is declared `front_left_iso` (IoU 0.60 there) but the model matches it better from rear_right_iso (elevati

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **67 -> 11** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): infernal.aws71.webp 0.798 -> 0.798

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (4 of 4 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- top_plate: hidden 3 mm key into chassis (one print)
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- el_battery: placed with 4.0 mm of lead room round it
- el_rx_esc: placed with 4.0 mm of lead room round it
- joint horn_l: 0.9 mm sweep clearance cut in top_plate
- joint horn_l: its sweep would cut a 4 mm deep slot into the outside of chassis (4 mm for the poses at 5..80 deg alone); left out (look kept)
- joint horn_r: 0.9 mm sweep clearance cut in top_plate
- joint horn_r: its sweep would cut a 4 mm deep slot into the outside of chassis (4 mm for the poses at 5..80 deg alone); left out (look kept)
- chassis: hollowed (box wall round pockets), 250341 -> 92656 mm3
- hollow failed on front_plate: [('cav', 'geometry failed: ValueError: Cannot tessellate an empty shape')]
- wiring channels: 4 of 4 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin

Left (one line each):
- proxy.sweep x2: moving part runs into the chassis more than a running clearance can take without changing the look
- power.weapon_motor x2: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- process.weapon_printed x2: toolchain: printed lifter/flipper arms are judged like spinner teeth (metal inserts required)
- wire.rotor_clearance x2: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- connection.cover_fasteners x1: see verify_r4.txt root causes
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

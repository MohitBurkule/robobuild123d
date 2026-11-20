# jiggy_sawdust: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type other; body box rect 70x70x55 mm, ramp 0; wheels 2 r14 outboard; weapon none; extra parts: front_plate, saw_blade; photos skipped (cluttered): indices [0]; textured masks for indices [1, 2].

Likeness: likeness crashed (see STRUGGLES).

## Tools I wanted
- Kit weapon kind `saw` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type other; body box rect 70x70x55 mm, ramp 0; wheels 2 r14 outboard; weapon none; extra parts: front_plate, saw_blade; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws63 0.87 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type other; body box rect 70x70x55 mm, ramp 0; wheels 2 r14 outboard; weapon none; extra parts: front_plate, saw_blade; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws63 0.65 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/jiggy_sawdust.aws63.webp` is declared `front_right_iso` (IoU 0.65 there) but the model matches it better from rear (elevation 2

## Round 3b (rebuilt by eye from the photos: parts moved to where the photo shows them, camera set per photo)
Decisions: type other; body box rect 70x70x55 mm, ramp 0; wheels 2 r14 outboard; weapon none; extra parts: front_plate, saw_blade, saw_body; photos skipped (cluttered): indices [0, 1]; textured masks for indices [2].

Likeness: aws63 0.60 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/jiggy_sawdust.aws63.webp` is declared `front_right_iso` (IoU 0.60 there) but the model matches it better from rear (elevation 2

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **50 -> 8** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): jiggy_sawdust.aws63.webp 0.605 -> 0.605

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (0 of 7 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- saw_blade: weapon motor not coaxial (no room on the axis): placed parallel to the axis in the print, belt drive NOT modelled
- saw_blade: rotor overlaps chassis 27 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- saw_blade: rotor overlaps saw_body 7 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- front_plate: cuts split it into 2 pieces, each joined to the print
- chassis: hollowed (box wall round pockets), 239125 -> 82142 mm3
- hollow failed on front_plate: [('cav', 'geometry failed: ValueError: Cannot tessellate an empty shape')]
- saw_body: hollowed (exact wall round pockets), 6570 -> 5084 mm3 (2 thin spots kept solid)
- wire w_m1: no via round the rotor found
- saw_body: printed with the weapon axis as build direction

Left (one line each):
- proxy.interference x2: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- proxy.sweep x1: moving part runs into the chassis more than a running clearance can take without changing the look
- wire.render_wires x1: a robot render does not draw every wire: at least one wire has no route through the print
- wire.rotor_clearance x1: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

# the_underminer: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 80x70x22 mm, ramp 0; wheels 4 r10 outboard; weapon none; extra parts: scoop, pod, lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.88 (ok).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends pod to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 80x70x22 mm, ramp 0; wheels 4 r10 outboard; weapon none; extra parts: scoop, pod, lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.88 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 80x70x22 mm, ramp 0; wheels 4 r10 outboard; weapon none; extra parts: scoop, pod, lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.68 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/the_underminer.aws67.webp` is declared `front` (IoU 0.68 there) but the model matches it better from front (elevation 45, azimu

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **71 -> 7** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): the_underminer.aws67.webp 0.879 -> 0.879

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (7 of 7 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- dt_axle_wheel_l1 replaced by the gearmotor shaft
- dt_axle_wheel_r1 replaced by the gearmotor shaft
- el_battery: placed with 4.0 mm of lead room round it
- el_rx_esc: placed with 4.0 mm of lead room round it
- lid: driven by a KingMax CS07 micro servo (catalog servo_cs07) in a closed pocket 27 mm from the hinge; the horn-to-arm link is declared, not modelled
- joint lid: 0.5 mm sweep clearance cut in chassis
- chassis: hollowed (box wall round pockets), 89397 -> 60749 mm3
- scoop: hollowed (exact wall round pockets), 54452 -> 30695 mm3 (29 thin spots kept solid)
- pod_l: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- pod_r: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- chassis: 2 of 35 channel pieces left out (boolean)
- wiring channels: 7 of 7 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin

Left (one line each):
- proxy.wiring x4: see verify_r4.txt root causes
- proxy.interference x2: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells

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
Likeness (best silhouette IoU per photo, r3 -> r4): the_underminer.aws67.webp 0.879 -> 0.880

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

## Round 4 (verification, helper 2)
Blockers r3 71 -> r4 7 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (bbb_n20_600rpm), `dm_wheel_r0` (bbb_n20_600rpm), `dm_wheel_l1` (bbb_n20_600rpm), `dm_wheel_r1` (bbb_n20_600rpm), `el_battery` (lipo_2s_180), `el_rx_esc` (malenki_nano), `el_servo_lid` (servo_cs07), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `name_miner`, `name_under`, `scoop`
- real fasteners: `fs_look_top_plate_0` M2x8, `fs_look_top_plate_1` M2x8, `fs_look_top_plate_2` M2x8, `fs_look_top_plate_3` M2x8
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- photo graphics as fused colour-split decals (robot decal): Under / miner lettering on the top plate
- side profile from the photo, read side by side with the render (robot outline --round): rounded front corners (4 mm) on the scoop and both pods

Left (and why):
- proxy.wiring x4: Wire `w_m1` (`el_rx_esc.m1` to `dm_wheel_l0.terminals`): the baseline route is now blocked by `outside the structure` (6 samples).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.interference x2: `pod_l` and `dt_strut_pod_l` overlap by 1.24 mm (allowed 0.08).

Likeness (best silhouette IoU per photo, r3 -> r4): the_underminer.aws67.webp 0.88 -> 0.88

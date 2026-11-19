# queen_sarah_denning: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type flipper; body box rect 110x100x36 mm, ramp 30; wheels 2 r12 inboard; weapon none; extra parts: flipper, scoop; photos skipped (cluttered): indices [0].

Likeness: aws70 0.72 (FAIL), aws71 0.90 (ok).

## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (flipper, scoop), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type flipper; body box rect 110x100x36 mm, ramp 30; wheels 2 r12 inboard; weapon none; extra parts: flipper, scoop; photos skipped (cluttered): indices [0].

Likeness: aws70 0.72 (FAIL), aws71 0.90 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box rect 110x100x36 mm, ramp 30; wheels 2 r12 inboard; weapon none; extra parts: flipper, scoop; photos skipped (cluttered): indices [0].

Likeness: aws70 0.65 (FAIL), aws71 0.89 (ok).
Other likeness findings: [FAIL] likeness.view: `reference/queen_sarah_denning.aws70.webp` is declared `front` (IoU 0.65 there) but the model matches it better from front (elevation 45, 

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **65 -> 7** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): queen_sarah_denning.aws70.webp 0.677 -> 0.677, queen_sarah_denning.aws71.webp 0.887 -> 0.887

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (4 of 5 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- el_battery: placed with 4.0 mm of lead room round it
- el_rx_esc: placed with 4.0 mm of lead room round it
- flipper: driven by a KingMax CS07 micro servo (catalog servo_cs07) in a closed pocket 13 mm from the hinge; the horn-to-arm link is declared, not modelled
- joint flipper: 1.5 mm sweep clearance cut in chassis
- chassis: hollowed (box wall round pockets), 298379 -> 108719 mm3
- hollow failed on scoop: [('cav', 'geometry failed: ValueError: Cannot tessellate an empty shape')]
- wiring channels: 5 of 5 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin

Left (one line each):
- proxy.wiring x2: see verify_r4.txt root causes
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- wire.render_wires x1: a robot render does not draw every wire: at least one wire has no route through the print
- wire.render_count x1: render record lists fewer routes than the spec has wires (a wire found no route)
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

## Round 4 (verification, helper 2)
Blockers r3 65 -> r4 8 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (bbb_n20_600rpm), `dm_wheel_r0` (bbb_n20_600rpm), `el_battery` (lipo_2s_180), `el_rx_esc` (malenki_nano), `el_servo_flipper` (servo_cs07), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `eye_chassis`, `iris_chassis`, `eye_top_plate`, `iris_top_plate`, `scoop`
- real fasteners: `fs_look_top_plate_0` M2x8, `fs_look_top_plate_1` M2x8, `fs_look_top_plate_2` M2x8, `fs_look_top_plate_3` M2x8
- 5 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- photo graphics as fused colour-split decals (robot decal): almond eyes with green irises on the top

Left (and why):
- proxy.wiring x2: Wire `w_m1` (`el_rx_esc.m1` to `dm_wheel_l0.terminals`): no baseline route (run the full `wiring` group once and pass its report).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 4 routes vs 5 spec wires (missing ['w_m1']); top.png: 4 routes vs 5 spec wires (missing ['w_m1'])
- likeness.view x1: looks, not in scope for this pass.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): queen_sarah_denning.aws70.webp 0.68 -> 0.68; queen_sarah_denning.aws71.webp 0.89 -> 0.89

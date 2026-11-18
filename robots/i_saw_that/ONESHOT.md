
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends arm to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type vertical_spinner; body box rect 62x60x28 mm, ramp 0; wheels 2 r13 outboard; weapon disc r27 axis x teeth 8; 2 forks 62 mm; extra parts: arm.

Likeness: aws76 0.57 (FAIL).

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 62x60x28 mm, ramp 0; wheels 2 r13 outboard; weapon disc r28 axis x teeth 8; extra parts: arm, jaw.

Likeness: aws76 0.55 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 62x60x28 mm, ramp 0; wheels 2 r13 outboard; weapon disc r34 axis x teeth 8; extra parts: arm, jaw.

Likeness: aws76 0.36 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/i_saw_that_.aws76.webp` is declared `front_left_iso` (IoU 0.36 there) but the model matches it better from rear_left_iso (eleva

## Round 4 (verification, helper 2)
Blockers r3 54 -> r4 8 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (brotherhobby_tc1404_3800kv)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `arm`, `jaw_l`, `jaw_r`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- weapon drive: motor not coaxial, belt drive implied
- weapon: no locking pin added (weapon sits 33.0 mm from the frame; a pin across that gap would change the outside)
- chassis: dm_wheel_l0 pocketed to its own outline (0.2 mm clear, so it stays captive); only its shaft bore passes the wall to wheel_l0
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 201 g over 150: walls 2 mm -> 194 g
- mass estimate 194 g over 150: walls 1.6 mm -> 186 g
- hollowed chassis (wall 1.6, form 0): 104.2 -> 43.5 cm3
- hollowed arm (wall 1.6, form 0): 3.2 -> 2.4 cm3
- hollowed jaw_l (wall 1.6, form 0): 22.7 -> 8.6 cm3
- hollowed jaw_r (wall 1.6, form 0): 22.7 -> 8.3 cm3

Left (and why):
- proxy.wiring x1: Wire `w_sw_esc` (`el_switch.out` to `el_esc.bat`): no baseline route (run the full `wiring` group once and pass its report).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- legal.locking_bar x1: Rule 5f: every spinner needs a locking bar that physically stops the weapon from turning.
- dynamics.balance x1: `weapon` mass centre is 0.104 mm off the spin axis: grade G346.4 at 31920 rpm, a 63 N rotating load on the bearings and frame. That is 34.3x the robot's weight. It will shake the robot and the bearing
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 6 routes vs 7 spec wires (missing ['w_sw_esc']); top.png: 6 routes vs 7 spec wires (missing ['w_sw_esc'])
- likeness.view x1: looks, not in scope for this pass.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): i_saw_that_.aws76.webp 0.41 -> 0.41

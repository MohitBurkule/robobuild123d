
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (top_plate), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends weapon_arm, weapon_shaft, drum_flange, weapon_motor_can to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type drum; body box pentagon 86x104x24 mm, ramp 0; wheels 2 r17 inboard; weapon drum r11 axis x teeth 2; 2 forks 46 mm; extra parts: weapon_arm, weapon_shaft, drum_flange, top_plate, weapon_motor_can.

Likeness: aws74 0.69 (FAIL), aws76 0.72 (FAIL), aws77 0.76 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 88 -> r4 14 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (brotherhobby_tc1404_3800kv), `lock_pin` (made)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `weapon_arm_l`, `weapon_arm_r`, `drum_flange_l`, `drum_flange_r`, `top_plate`, `weapon_motor_can`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_arm_weapon_0`, `dt_arm_weapon_1`, `dt_mount_fork_0`, `dt_mount_fork_1`
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- weapon_shaft: steel cannot be fdm -> turned steel rod / printed
- weapon drive: motor not coaxial, belt drive implied
- weapon: running-clearance well in drum_flange_l not carved (it would open 118 mm2 of outside face)
- weapon: running-clearance well in drum_flange_r not carved (it would open 116 mm2 of outside face)
- no screw line found for fork_0
- no screw line found for fork_1
- no screw line found for weapon_shaft
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 237 g over 150: walls 2 mm -> 228 g
- mass estimate 228 g over 150: walls 1.6 mm -> 221 g
- hollowed chassis (wall 1.6, form 0): 169.9 -> 64.2 cm3
- hollowed weapon_arm_l (wall 1.6, form 0): 5.8 -> 3.3 cm3
- hollowed weapon_arm_r (wall 1.6, form 0): 5.8 -> 4.0 cm3
- hollowed weapon_motor_can (wall 1.6, form 0): 5.1 -> 2.5 cm3

Left (and why):
- integrity.solids x1: `chassis` has 0 closed solid(s) and 1 open/invalid shell(s), expected 1 (63081 mm3). A boolean or fillet probably collapsed the build.
- proxy.wiring x2: Wire `w_bat_sw` (`el_battery.xt30` to `el_switch.in`): no baseline route (run the full `wiring` group once and pass its report).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- mfg.stock x2: `fork_0` (laser): thickness 2.50 mm is not a stock titanium gauge (0.5, 0.8, 0.9, 1, 1.5, 2, 3, 4, 5, 6, 8, 10); nearest 2 mm.
- mfg.layer_load x2: `dt_arm_weapon_0` carries the `weapon` axle but is printed with build direction +z (world [0.0, 0.0, 1.0]), not along the spin axis [1.0, 0.0, 0.0]: impact load peels layers apart.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 5 routes vs 7 spec wires (missing ['w_bat_sw', 'w_sw_esc']); top.png: 5 routes vs 7 spec wires (missing ['w_bat_sw', 'w_sw_esc'])
- likeness.silhouette x3: looks, not in scope for this pass.
- likeness.view x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): baphomet.aws74.webp 0.69 -> 0.69; baphomet.aws76.webp 0.69 -> 0.69; baphomet.aws77.webp 0.76 -> 0.76

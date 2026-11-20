
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends upright to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type vertical_spinner; body box rect 80x66x20 mm, ramp 0; wheels 2 r13 outboard; weapon disc r30 axis x teeth 2; 2 forks 55 mm; extra parts: upright.

Likeness: aws72 0.55 (FAIL), aws74 0.58 (FAIL), aws76 0.63 (FAIL).

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 80x66x20 mm, ramp 0; wheels 2 r14 outboard; weapon disc r36 axis x teeth 2; extra parts: upright, fork.

Likeness: aws72 0.56 (FAIL), aws74 0.54 (FAIL), aws76 0.60 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 80x66x20 mm, ramp 0; wheels 2 r11 outboard; weapon disc r26 axis x teeth 2; extra parts: upright, fork, hook.

Likeness: aws72 0.46 (FAIL), aws74 0.31 (FAIL), aws76 0.39 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/verty_big_secret.aws74.webp` is declared `front_right_iso` (IoU 0.31 there) but the model matches it better from right (elevati; [FAIL] likeness.view: `reference/verty_big_secret.aws76.webp` is declared `front_left_iso` (IoU 0.39 there) but the model matches it better from right (elevatio

## Round 3b (rebuilt by eye from the photos: parts moved to where the photo shows them, camera set per photo)
Decisions: type vertical_spinner; body box rect 80x66x20 mm, ramp 0; wheels 2 r14 outboard; weapon disc r26 axis x teeth 2; extra parts: upright, hook, fork.

Likeness: aws72 0.59 (FAIL), aws74 0.45 (FAIL), aws76 0.51 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/verty_big_secret.aws74.webp` is declared `front_right_iso` (IoU 0.45 there) but the model matches it better from front_right_is; [FAIL] likeness.view: `reference/verty_big_secret.aws76.webp` is declared `front_left_iso` (IoU 0.51 there) but the model matches it better from rear_right_iso 

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type vertical_spinner; body box rect 80x66x20 mm, ramp 0; wheels 2 r14 outboard; weapon disc r26 axis x teeth 2; extra parts: upright, hook, fork, motor_can, side_spike, rear_guard.

Likeness: aws72 0.63 (FAIL), aws74 0.65 (FAIL), aws76 0.60 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/verty_big_secret.aws76.webp` is declared `front_left_iso` (IoU 0.60 there) but the model matches it better from rear_right_iso 

## Round 4 (verification, helper 2)
Blockers r3 75 -> r4 9 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (brotherhobby_tc1404_3800kv), `lock_pin` (made)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `upright_l`, `upright_r`, `hook_l`, `hook_r`, `fork_l`, `fork_r`, `motor_can`, `side_spike_l`, `side_spike_r`, `rear_guard`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_mount_fork_l`, `dt_mount_fork_r`
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- weapon drive: motor not coaxial, belt drive implied
- weapon: running-clearance well in chassis not carved (it would open 34 mm2 of outside face)
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 211 g over 150: walls 2 mm -> 205 g
- mass estimate 205 g over 150: walls 1.6 mm -> 199 g
- hollowed chassis (wall 1.6, form 0): 105.6 -> 48.2 cm3
- hollowed upright_l (wall 1.6, form 0): 6.1 -> 3.7 cm3
- hollowed upright_r (wall 1.6, form 0): 6.1 -> 2.7 cm3
- hollowed fork_l (wall 1.6, form 0): 3.5 -> 2.2 cm3
- hollowed fork_r (wall 1.6, form 0): 3.5 -> 2.2 cm3
- hollowed motor_can (wall 1.6, form 0): 3.5 -> 1.6 cm3

Left (and why):
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.sweep x2: joint `weapon`: `weapon` turning a full revolution may reach `chassis`.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 5 routes vs 7 spec wires (missing ['w_bat_sw', 'w_sw_esc']); top.png: 5 routes vs 7 spec wires (missing ['w_bat_sw', 'w_sw_esc'])
- likeness.silhouette x3: looks, not in scope for this pass.
- likeness.view x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): verty_big_secret.aws72.webp 0.63 -> 0.63; verty_big_secret.aws74.webp 0.65 -> 0.65; verty_big_secret.aws76.webp 0.6 -> 0.6


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

## Round 4 (verification, helper 2)
Blockers r3 76 -> r4 7 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (brotherhobby_tc1404_3800kv), `lock_pin` (made)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `upright_l`, `upright_r`, `fork_l`, `fork_r`, `hook_l`, `hook_r`
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- weapon drive: motor not coaxial, belt drive implied
- rod dt_axle_wheel_l0: 2.2 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.2 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- wheel_l0: one cut dropped (split the part into 2 solids)
- wheel_r0: one cut dropped (split the part into 2 solids)
- hollowed chassis (wall 2.5, form 0): 105.7 -> 55.0 cm3

Left (and why):
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- likeness.silhouette x3: looks, not in scope for this pass.
- likeness.view x2: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): verty_big_secret.aws72.webp 0.46 -> 0.46; verty_big_secret.aws74.webp 0.31 -> 0.31; verty_big_secret.aws76.webp 0.39 -> 0.39

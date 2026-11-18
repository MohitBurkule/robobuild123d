# valkyrie: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Flat 100 mm box with chamfered rear corners and clear top plate, two side cheeks carrying a full-width beater/drum (r 8, 80 wide) at the front with blue hubs; 2 wheels r 13 inboard at the rear. robot_type drum.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| valkyrie.aws71.webp | 0.74 | 0.80 | revron_ant 0.73 | FAIL |
| valkyrie.aws74.webp | 0.76 | 0.80 | wedge_2wd 0.80 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Model is too tall/short in the rear third (photo body is longer and flatter); wheels are buried in the solid body instead of showing in corner cut-outs; beater is a plain toothed cylinder, not the bolted bar/cage; no translucent lid look.

## Missing tool / hint
Kit has no 'inboard wheel in a corner notch' and no beater-bar weapon; a fit-photo for body length/height from iso masks would have fixed the proportions.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Corner notches expose the wheels, beater bar with square windows replaces the round drum, body lower and longer, sensor windows on a clear lid.

Likeness: aws71 0.74 (FAIL), aws74 0.79 (FAIL).

## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type drum; body box rect 75x104x20 mm, ramp 0; wheels 2 r13 inboard; weapon drum r8 axis x teeth 2.

Likeness: aws71 0.74 (FAIL), aws74 0.79 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type drum; body box rect 75x104x20 mm, ramp 0; wheels 2 r13 inboard; weapon drum r8 axis x teeth 2.

Likeness: aws71 0.60 (FAIL), aws74 0.62 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/valkyrie.aws71.webp` is declared `left` (IoU 0.60 there) but the model matches it better from front_right_iso (elevation 45, az; [FAIL] likeness.view: `reference/valkyrie.aws74.webp` is declared `front_left_iso` (IoU 0.62 there) but the model matches it better from rear_right_iso (elevati

## Round 4 (verification, helper 2)
Blockers r3 83 -> r4 25 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (brotherhobby_tc1404_3800kv), `lock_pin` (made)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `cheek_l`, `cheek_r`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_arm_weapon_0`, `dt_arm_weapon_1`
- real fasteners: `fs_top_plate_0` M2x8, `fs_top_plate_1` M2x8
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- weapon drive: motor not coaxial, belt drive implied
- weapon: running-clearance well in hub_l not carved (it would open 175 mm2 of outside face)
- weapon: running-clearance well in hub_r not carved (it would open 184 mm2 of outside face)
- overlaps left: dm_wheel_r0/el_wesc 0.14, weapon_motor/lock_pin 1.18
- no screw line found for hub_l
- no screw line found for hub_r
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 186 g over 150: walls 2 mm -> 178 g
- mass estimate 178 g over 150: walls 1.6 mm -> 172 g
- hollowed chassis (wall 1.6, form 0): 123.7 -> 49.0 cm3
- hollowed cheek_l (wall 1.6, form 0): 4.0 -> 2.4 cm3
- hollowed cheek_r (wall 1.97, form 1): 4.0 -> 2.8 cm3
- window_l: not touching the chassis, left undeclared
- window_r: not touching the chassis, left undeclared

Left (and why):
- integrity.solids x1: `chassis` has 0 closed solid(s) and 1 open/invalid shell(s), expected 1 (48309 mm3). A boolean or fillet probably collapsed the build.
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.interference x5: `weapon` and `hub_l` overlap by 1.39 mm (allowed 0.08).
- proxy.sweep x4: joint `weapon`: `weapon` turning a full revolution may reach `hub_l`.
- connection.floating x2: `window_l` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis. Nearest part is `top_plate`, 0.0 mm away.
- connection.cover_fasteners x2: `cheek_l` is an armour / cover panel held by 0 fastener(s); it needs >= 2 real screws. Snap, press-fit or tape retention alone lets it peel off on the first hit.
- process.geometry x2: `weapon` (cnc): 16 sharp internal corner(s) parallel to every reachable tool axis: an end mill leaves r >= 1 mm there.
- mfg.layer_load x2: `dt_arm_weapon_0` carries the `weapon` axle but is printed with build direction +z (world [0.0, 0.0, 1.0]), not along the spin axis [1.0, 0.0, 0.0]: impact load peels layers apart.
- combat.R051 x1: `weapon`: Weapon sweep above the floor is -0.66 mm (needs 0.3 mm).
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 4 routes vs 7 spec wires (missing ['w_bat_sw', 'w_m2', 'w_sw_esc']); top.png: 4 routes vs 7 spec wires (missing ['w_bat_sw', 'w_m2', 'w_sw_esc'])
- likeness.silhouette x2: looks, not in scope for this pass.
- likeness.view x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): valkyrie.aws71.webp 0.74 -> 0.74; valkyrie.aws74.webp 0.62 -> 0.62

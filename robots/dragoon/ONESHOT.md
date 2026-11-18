# dragoon: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Blue box with centre slot, open ring disc (r 34, one tooth) offset left with black motor pod beside it, 2 wheels r 15 rear outside, 4 black forks on a front bar.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| dragoon.aws72.webp | 0.68 | 0.80 | revron 0.72 | FAIL |
| dragoon.aws74.webp | 0.75 | 0.80 | revron 0.78 | FAIL |
| dragoon.aws76.webp | 0.72 | 0.80 | wedge_2wd 0.70 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Photos show three fork setups (4 forks, 2 wedgelets, long tines); ring is higher/further forward in the real robot and pods are split; side polycarbonate plates missing.

## Missing tool / hint
Kit weapon is always centred on x and solid; needed manual ring + x offset.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Wider body with sloped side edges and disc slot, larger offset ring with one tooth, bigger motor pod, long angled forks, taller wheels, clear side plates.

Likeness: aws72 0.71 (FAIL), aws74 0.73 (FAIL), aws76 0.71 (FAIL).

## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 84x108x28 mm, ramp 0; wheels 2 r15 outboard; weapon disc r40 axis x teeth 1; 4 forks 50 mm.

Likeness: aws72 0.68 (FAIL), aws74 0.76 (FAIL), aws76 0.72 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 84x108x28 mm, ramp 0; wheels 2 r15 outboard; weapon disc r40 axis x teeth 1; 4 forks 50 mm.

Likeness: aws72 0.66 (FAIL), aws74 0.43 (FAIL), aws76 0.56 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/dragoon.aws74.webp` is declared `front` (IoU 0.43 there) but the model matches it better from rear_right_iso (elevation 45, azi; [FAIL] likeness.view: `reference/dragoon.aws76.webp` is declared `front_left_iso` (IoU 0.56 there) but the model matches it better from front_right_iso (elevati

## Round 4 (verification, helper 2)
Blockers r3 142 -> r4 33 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (bbb_be1806_2300kv), `lock_pin` (made)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `fork_0`, `fork_1`, `fork_2`, `fork_3`, `motor_pod`, `pod_base`, `fork_block_l`, `fork_block_r`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_mount_fork_0`, `dt_mount_fork_1`, `dt_mount_fork_2`, `dt_mount_fork_3`, `dt_mount_fork_block_l`, `dt_mount_fork_block_r`
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- weapon drive: motor not coaxial, belt drive implied
- weapon: running-clearance well in chassis not carved (it would open 225 mm2 of outside face)
- weapon: running-clearance well in fork_1 not carved (it would open 107 mm2 of outside face)
- weapon: running-clearance well in fork_block_r not carved (it would open 110 mm2 of outside face)
- weapon: running-clearance well in dt_mount_fork_1 not carved (it would open 64 mm2 of outside face)
- no screw line found for side_plate_l
- no screw line found for side_plate_r
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 289 g over 150: walls 2 mm -> 278 g
- mass estimate 278 g over 150: walls 1.6 mm -> 268 g
- hollowed chassis (wall 1.6, form 0): 220.1 -> 76.4 cm3
- hollowed fork_0 (wall 1.6, form 0): 2.6 -> 1.8 cm3
- hollowed fork_1 (wall 1.6, form 0): 2.6 -> 1.8 cm3
- hollowed fork_2 (wall 1.6, form 0): 2.6 -> 1.8 cm3
- hollowed fork_3 (wall 1.6, form 0): 2.6 -> 1.8 cm3
- hollowed motor_pod (wall 1.6, form 0): 25.6 -> 6.7 cm3
- hollowed pod_base (wall 1.6, form 0): 11.6 -> 7.0 cm3
- hollowed fork_block_l (wall 1.6, form 0): 5.6 -> 3.4 cm3
- hollowed fork_block_r (wall 1.6, form 0): 5.6 -> 3.4 cm3
- hollowed dt_mount_fork_block_l (wall 1.6, form 0): 3.2 -> 1.9 cm3
- hollowed dt_mount_fork_block_r (wall 1.6, form 0): 3.2 -> 1.8 cm3
- side_plate_l: no screw line and no slot, left undeclared (needs a real mount)
- side_plate_r: no screw line and no slot, left undeclared (needs a real mount)

Left (and why):
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.interference x3: `chassis` and `weapon` overlap by 1.39 mm (allowed 0.08).
- proxy.sweep x8: joint `weapon`: `weapon` turning a full revolution may reach `chassis`.
- connection.fused_mismatch x2: `fork_1` is fused to `chassis` but they share 0.83 mm3 (need >= 1 mm3); faces that only touch print as two pieces or a paper-thin seam.
- connection.floating x4: `fork_1` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis. Nearest part is `chassis`, 0.0 mm away.
- dynamics.balance x1: `weapon` mass centre is 4.835 mm off the spin axis: grade G9781.5 at 19320 rpm, a 1293 N rotating load on the bearings and frame. That is 486.9x the robot's weight. It will shake the robot and the bea
- process.geometry x2: `weapon` (laser): 6 sharp internal corner(s): radius 0 < kerf 0.1 mm (add a fillet >= kerf or the mating part will not seat).
- mfg.layer_load x1: `motor_pod` carries the `weapon` axle but is printed with build direction +z (world [0.0, 0.0, 1.0]), not along the spin axis [1.0, 0.0, 0.0]: impact load peels layers apart.
- combat.R051 x1: `weapon`: Weapon sweep above the floor is -10.50 mm (needs 0.3 mm).
- physics.runtime x1: ~160 s at ~6.3 A average from 350 mAh; a fight is 180 s.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.rotor_clearance x3: toolchain: same full-revolution assumption; wires cannot leave a cylinder that covers the chassis.
- likeness.silhouette x3: looks, not in scope for this pass.
- likeness.view x2: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): dragoon.aws72.webp 0.66 -> 0.66; dragoon.aws74.webp 0.43 -> 0.43; dragoon.aws76.webp 0.56 -> 0.56

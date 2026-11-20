
## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body twin_pods rect 120x94x40 mm, ramp 65; wheels 2 r15 outboard; weapon disc r37 axis x teeth 1; 2 forks 35 mm.

Likeness: aws72 0.73 (FAIL), aws74 0.68 (FAIL), aws76 0.74 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 99 -> r4 43 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (bbb_be1806_2300kv)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `pod_r`, `bridge`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_mount_fork_0`, `dt_mount_fork_1`
- real fasteners: `fs_bolt_fork_0` M2x6, `fs_bolt_fork_1` M2x6, `fs_screw_0` M2x6, `fs_screw_1` M2x6, `fs_screw_4` M2x6, `fs_screw_5` M2x6
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- looks FROZEN (approved): no outside change at all; every cut that would have opened an outside face was skipped (outside-face audit: 0 mm2 opened), no switch slot, no locking pin; screw heads of the photo are now real M2 button-head screws at the same spots
- weapon drive: motor not coaxial, belt drive implied
- weapon: no locking pin added (looks frozen: a visible pin would change the outside)
- pod_l: a cut was not made (it would open 189 mm2 of outside face; the overlap stays as a finding)
- pod_l: a cut was not made (it would open 5 mm2 of outside face; the overlap stays as a finding)
- pod_r: a cut was not made (it would open 42 mm2 of outside face; the overlap stays as a finding)
- weapon: running-clearance well in bridge not carved (it would open 1548 mm2 of outside face)
- dt_bolt_fork_0: real 6 mm M2 button-head screw into dt_mount_fork_0
- dt_bolt_fork_1: real 6 mm M2 button-head screw into dt_mount_fork_1
- dt_screw_0: real 6 mm M2 button-head screw into pod_l
- dt_screw_1: real 6 mm M2 button-head screw into pod_l
- dt_screw_2: no material to thread into under the head, dropped
- dt_screw_3: no material to thread into under the head, dropped
- dt_screw_4: real 6 mm M2 button-head screw into pod_l
- dt_screw_5: real 6 mm M2 button-head screw into pod_l
- no screw line found for fork_0
- no screw line found for fork_1
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- el_switch: no access slot (looks frozen); legal.switch stays open until a slot position is approved
- mass estimate 436 g over 150: walls 2 mm -> 419 g
- mass estimate 419 g over 150: walls 1.6 mm -> 409 g
- hollowed pod_l (wall 1.6, form 0): 99.4 -> 31.2 cm3
- hollowed pod_r (wall 1.6, form 0): 99.4 -> 33.2 cm3
- hollowed bridge (wall 1.6, form 0): 76.4 -> 18.9 cm3
- fork_0: no screw line and no slot, left undeclared (needs a real mount)
- fork_1: no screw line and no slot, left undeclared (needs a real mount)

Left (and why):
- proxy.wiring x7: Wire `w_bat_sw` (`el_battery.xt30` to `el_switch.in`): its ports moved 86.17 mm since the baseline route.
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.interference x3: `pod_l` and `fs_bolt_fork_1` overlap by 0.84 mm (allowed 0.08).
- proxy.sweep x2: joint `weapon`: `weapon` turning a full revolution may reach `bridge`.
- connection.floating x2: `fork_0` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis. Nearest part is `pod_r`, 0.4 mm away.
- legal.switch x1: Rule 4a needs an externally accessible way to shut down that works without tools and is clearly marked on/off.
- legal.locking_bar x1: Rule 5f: every spinner needs a locking bar that physically stops the weapon from turning.
- legal.footprint x1: Smallest square that holds the robot is 158.0 mm; the limit is 150 mm with no overhang at any height.
- power.runtime x1: 350 mAh x 80% usable lasts about 3.4 min of fighting (per 3 min fight: drive 49 mAh, weapon spin-ups and hold 192 mAh, electronics 5 mAh = 246 mAh). A fight is 3 min and the pack must cover it with 25
- dynamics.balance x1: `weapon` mass centre is 0.322 mm off the spin axis: grade G651.9 at 19320 rpm, a 309 N rotating load on the bearings and frame. That is 76.4x the robot's weight. It will shake the robot and the bearin
- process.geometry x3: `weapon` (laser): 4 planar levels along the plate normal (0.00, 15.00, 19.00, 34.00 mm): a blind pocket, step or a feature standing proud of the plate; a cut part has exactly two faces.
- mfg.stock x1: `weapon` (laser): thickness 34.00 mm is not a stock steel gauge (0.5, 0.8, 1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10); nearest 10 mm.
- physics.runtime x1: ~160 s at ~6.3 A average from 350 mAh; a fight is 180 s.
- proxy.assembly x10: `pod_r`: the baseline teardown never took it off.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.rotor_clearance x3: toolchain: same full-revolution assumption; wires cannot leave a cylinder that covers the chassis.
- wire.render_count x1: iso.png: 5 routes vs 7 spec wires (missing ['w_bat_sw', 'w_sw_esc']); top.png: 5 routes vs 7 spec wires (missing ['w_bat_sw', 'w_sw_esc'])
- likeness.silhouette x3: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): delta_v.aws72.webp 0.73 -> 0.73; delta_v.aws74.webp 0.68 -> 0.68; delta_v.aws76.webp 0.74 -> 0.74

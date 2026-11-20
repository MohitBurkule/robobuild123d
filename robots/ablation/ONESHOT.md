
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends arm, arm_base to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 72x92x26 mm, ramp 0; wheels 4 r11 outboard; weapon disc r11 axis x teeth 2; 4 forks 62 mm; extra parts: arm, arm_base.

Likeness: aws72 0.65 (FAIL), aws74 0.61 (FAIL), aws76 0.53 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 110 -> r4 11 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (pololu_hpcb6v_50to1), `dm_wheel_r1` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (bbb_be1806_2300kv)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `arm`, `arm_base`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`, `dt_arm_weapon_0`, `dt_arm_weapon_1`, `dt_mount_fork_0`, `dt_mount_fork_1`, `dt_mount_fork_2`, `dt_mount_fork_3`
- real fasteners: `fs_screw_0` M2x6, `fs_screw_1` M2x6, `fs_screw_2` M2x6, `fs_screw_3` M2x6, `fs_screw_4` M2x6, `fs_screw_5` M2x6
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- looks FROZEN (approved): no outside change at all; every cut that would have opened an outside face was skipped (outside-face audit: 0 mm2 opened), no switch slot, no locking pin; screw heads of the photo are now real M2 button-head screws at the same spots
- weapon drive: motor not coaxial, belt drive implied
- weapon: no locking pin added (looks frozen: a visible pin would change the outside)
- chassis: a cut was not made (it would open 35 mm2 of outside face; the overlap stays as a finding)
- chassis: a cut was not made (it would open 37 mm2 of outside face; the overlap stays as a finding)
- chassis: a cut was not made (it would open 31 mm2 of outside face; the overlap stays as a finding)
- chassis: a cut was not made (it would open 26 mm2 of outside face; the overlap stays as a finding)
- dt_bolt_fork_0: head has nothing under it, dropped
- dt_bolt_fork_1: head has nothing under it, dropped
- dt_bolt_fork_2: head has nothing under it, dropped
- dt_bolt_fork_3: head has nothing under it, dropped
- dt_screw_0: real 6 mm M2 button-head screw into chassis
- dt_screw_1: real 6 mm M2 button-head screw into chassis
- dt_screw_2: real 6 mm M2 button-head screw into chassis
- dt_screw_3: real 6 mm M2 button-head screw into chassis
- dt_screw_4: real 6 mm M2 button-head screw into arm
- dt_screw_5: real 6 mm M2 button-head screw into chassis
- no screw line found for fork_0
- no screw line found for fork_1
- no screw line found for fork_2
- no screw line found for fork_3
- rod dt_axle_wheel_l1: 2.8 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 2.8 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- el_switch: no access slot (looks frozen); legal.switch stays open until a slot position is approved
- arm: 1 of 2 cuts dropped (they broke the solid: 2)
- mass estimate 187 g over 150: walls 2 mm -> 177 g
- mass estimate 177 g over 150: walls 1.6 mm -> 171 g
- hollowed chassis (wall 1.6, form 0): 172.2 -> 61.8 cm3
- hollowed arm (wall 1.6, form 0): 4.5 -> 3.1 cm3
- hollowed arm_base (wall 2.51, form 2): 3.5 -> 2.8 cm3

Left (and why):
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.interference x1: `arm` and `arm_base` overlap by 0.88 mm (allowed 0.08).
- legal.switch x1: Rule 4a needs an externally accessible way to shut down that works without tools and is clearly marked on/off.
- legal.locking_bar x1: Rule 5f: every spinner needs a locking bar that physically stops the weapon from turning.
- legal.footprint x1: Smallest square that holds the robot is 156.9 mm; the limit is 150 mm with no overhang at any height.
- physics.runtime x1: ~160 s at ~6.3 A average from 350 mAh; a fight is 180 s.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 6 routes vs 7 spec wires (missing ['w_sw_esc']); top.png: 6 routes vs 7 spec wires (missing ['w_sw_esc'])
- likeness.silhouette x3: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): ablation.aws72.webp 0.65 -> 0.65; ablation.aws74.webp 0.61 -> 0.61; ablation.aws76.webp 0.53 -> 0.53

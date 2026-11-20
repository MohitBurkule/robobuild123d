
## Tools I wanted
- This robot was built before the kit extras existed: all shapes were hand-written prisms in a private generator (`oneshot.py`/`gen.py`), ~15 min. Wanted: body side/top polygons, hinged weapons, scoop, wheel notches, colours (see refprs/fable_tool_wishlist.md).
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)


Likeness: aws72 0.66 (FAIL), aws74 0.64 (FAIL), aws76 0.84 (ok).

## Round 4 (verification, helper 2)
Blockers r3 126 -> r4 43 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `weapon_motor` (bl_1806_2300kv)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `handle_bar`, `handle_l`, `handle_r`, `wall_l`, `wall_r`, `eye_l`, `eye_r`, `dt_hub_wheel_l`, `dt_hub_wheel_r`, `dt_strut_eye_l`, `dt_strut_eye_r`
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- weapon: no locking pin added (weapon sits 6.0 mm from the frame; a pin across that gap would change the outside)
- chassis_bottom: a cut was not made (it would open 149 mm2 of outside face; the overlap stays as a finding)
- hub: a cut was not made (it would open 353 mm2 of outside face; the overlap stays as a finding)
- weapon: running-clearance well in hub not carved (it would open 294 mm2 of outside face)
- rod dt_axle_wheel_l: 2.8 mm stub clear of ['motor_l'] printed as the wheel's hub boss
- rod dt_axle_wheel_r: 2.8 mm stub clear of ['motor_r'] printed as the wheel's hub boss
- rod dt_shaft_weapon shortened to 28.0 mm clear of ['battery']
- mass estimate 172 g over 150: walls 2 mm -> 166 g
- mass estimate 166 g over 150: walls 1.6 mm -> 161 g
- hollowed chassis_bottom (wall 1.6, form 0): 148.6 -> 63.7 cm3
- hollow skipped hub: solids 1 vol 1.00
- hub: not touching the chassis, left undeclared
- dt_hubw_weapon: no screw line and no slot, left undeclared (needs a real mount)

Left (and why):
- proxy.wiring x3: Wire `w_sw_esc` (`power_switch.out` to `esc.bat`): the baseline route is now blocked by `chassis_bottom` (1 samples).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.interference x6: `chassis_bottom` and `motor_l` overlap by 4.88 mm (allowed 0.08).
- proxy.sweep x11: joint `weapon`: `dt_shaft_weapon` turning a full revolution may reach `chassis_bottom`.
- connection.screw_missing x1: `weapon_motor`-`chassis_bottom` says screw but no fastener passes through both.
- legal.locking_bar x1: `weapon`: unknown part(s) `lock_plate`.
- dynamics.balance x1: `weapon` mass centre is 1.050 mm off the spin axis: grade G2123.5 at 19320 rpm, a 76 N rotating load on the bearings and frame. That is 47.7x the robot's weight. It will shake the robot and the bearin
- process.geometry x1: `weapon` (laser): 1 sharp internal corner(s): radius 0 < kerf 0.1 mm (add a fillet >= kerf or the mating part will not seat).
- combat.R051 x1: `weapon`: Weapon sweep above the floor is -2.00 mm (needs 0.3 mm).
- fit.interference x5: `motor_l` overlaps wall `chassis_bottom` by 4.88 mm: it will not go in. No side has 5.08 mm free (free room per side {'-x': 1.35, '+x': 0.0, '-y': 0.36, '+y': 0.36, '+z': 2.75}): grow the pocket or pi
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.rotor_clearance x5: toolchain: same full-revolution assumption; wires cannot leave a cylinder that covers the chassis.
- wire.render_count x1: iso.png: 6 routes vs 7 spec wires (missing ['w_wesc_m']); top.png: 6 routes vs 7 spec wires (missing ['w_wesc_m'])
- likeness.silhouette x2: looks, not in scope for this pass.
- retention.axial x1: `dt_hubw_weapon` rotates but no fastener clamps or threads into it and it declares no reasoned press fit, pin, shaft or fuse hold.
- battery.armour_gap x1: `battery` sits 0.1 mm inside the armour envelope; a hit dents the wall into the cell.
- battery.rotor_gap x1: toolchain: same full-revolution assumption for a limited-range arm.

Likeness (best silhouette IoU per photo, r3 -> r4): relativity.aws72.webp 0.66 -> 0.66; relativity.aws74.webp 0.64 -> 0.64; relativity.aws76.webp 0.84 -> 0.84

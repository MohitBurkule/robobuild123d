
## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 74x88x22 mm, ramp 12; wheels 2 r17 outboard; weapon disc r20 axis x teeth 3; 2 forks 45 mm.

Likeness: aws74 0.76 (FAIL), aws76 0.57 (FAIL), aws77 0.64 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 71 -> r4 21 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (brotherhobby_tc1404_3800kv), `lock_pin` (made)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_mount_fork_0`, `dt_mount_fork_1`
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- weapon drive: motor not coaxial, belt drive implied
- weapon: running-clearance well in chassis not carved (it would open 194 mm2 of outside face)
- no screw line found for fork_0
- no screw line found for fork_1
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 478 g over 150: walls 2 mm -> 474 g
- mass estimate 474 g over 150: walls 1.6 mm -> 470 g
- hollowed chassis (wall 1.6, form 0): 132.4 -> 50.2 cm3

Left (and why):
- proxy.wiring x7: Wire `w_bat_sw` (`el_battery.xt30` to `el_switch.in`): no baseline route (run the full `wiring` group once and pass its report).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.interference x1: `chassis` and `weapon` overlap by 1.22 mm (allowed 0.08).
- proxy.sweep x2: joint `weapon`: `weapon` turning a full revolution may reach `chassis`.
- power.runtime x1: 350 mAh x 80% usable lasts about 2.4 min of fighting (per 3 min fight: drive 49 mAh, weapon spin-ups and hold 295 mAh, electronics 5 mAh = 349 mAh). A fight is 3 min and the pack must cover it with 25
- dynamics.balance x1: `weapon` mass centre is 0.047 mm off the spin axis: grade G156.4 at 31920 rpm, a 170 N rotating load on the bearings and frame. That is 36.5x the robot's weight. It will shake the robot and the bearin
- mfg.stock x1: `weapon` (laser): thickness 36.00 mm is not a stock steel gauge (0.5, 0.8, 1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10); nearest 10 mm.
- process.geometry x2: `weapon` (laser): 1 hole(s) of dia 4.00 mm < 36.00 mm (1 x thickness): cut holes that small distort or do not pierce; drill/ream them as a secondary op or enlarge.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.rotor_clearance x1: toolchain: same full-revolution assumption; wires cannot leave a cylinder that covers the chassis.
- likeness.silhouette x3: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): ice_breaker_junior.aws74.webp 0.76 -> 0.76; ice_breaker_junior.aws76.webp 0.57 -> 0.57; ice_breaker_junior.aws77.webp 0.64 -> 0.64

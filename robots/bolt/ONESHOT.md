
## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 104x100x26 mm, ramp 44; wheels 4 r11 inboard; weapon none; 2 forks 20 mm.

Likeness: aws57 0.81 (FAIL), aws63 0.81 (ok).

## Round 4 (verification, helper 2)
Blockers r3 84 -> r4 6 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (pololu_hpcb6v_50to1), `dm_wheel_r1` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- real fasteners: `fs_fork_0_0` M2x8, `fs_fork_1_0` M2x8, `fs_fork_1_1` M2x8
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- wheel_l1 moved by [0, -42, 0]: second wheel pair moved from beside the wedge (where it broke through the ramp) to the rear half, so the front of the body is closed as in the photos (coordinator request)
- wheel_r1 moved by [0, -42, 0]: same as wheel_l1
- fork_0 moved by [0, 0, 0.45]: seated on its printed mount (was 0.45 mm below it, floating) so a real M2 screw can hold it
- fork_1 moved by [0, 0, 0.45]: same as fork_0
- rod dt_axle_wheel_l1: 2.2 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 2.2 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- chassis: 0 of 15 cuts dropped (they broke the solid: -10)
- hollowed chassis (wall 2.87, form 1): 218.4 -> 88.2 cm3

Left (and why):
- proxy.wiring x4: Wire `w_bat_sw` (`el_battery.xt30` to `el_switch.in`): its ports moved 57.66 mm since the baseline route.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): bolt.aws57.webp 0.81 -> 0.81; bolt.aws63.webp 0.81 -> 0.8

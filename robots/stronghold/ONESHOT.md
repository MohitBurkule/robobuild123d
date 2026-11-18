
## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 64x82x34 mm, ramp 0; wheels 2 r13 inboard; weapon none; 2 forks 42 mm.

Likeness: aws72 0.73 (FAIL), aws74 0.74 (FAIL), aws76 0.77 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 76 -> r4 16 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `pcb`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_mount_fork_0`, `dt_mount_fork_1`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- no screw line found for fork_0
- no screw line found for arch_0
- no screw line found for foot_0
- no screw line found for fork_1
- no screw line found for arch_1
- no screw line found for foot_1
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- hollowed chassis (wall 2.5, form 0): 178.4 -> 62.2 cm3
- foot_0: no screw line and no slot, left undeclared (needs a real mount)
- foot_1: no screw line and no slot, left undeclared (needs a real mount)

Left (and why):
- proxy.wiring x4: Wire `w_bat_sw` (`el_battery.xt30` to `el_switch.in`): its ports moved 26.96 mm since the baseline route.
- connection.floating x2: `foot_0` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis. Nearest part is `chassis`, 0.0 mm away.
- connection.cover_fasteners x3: `arch_0` is an armour / cover panel held by 0 fastener(s); it needs >= 2 real screws. Snap, press-fit or tape retention alone lets it peel off on the first hit.
- process.geometry x2: `fork_0` (laser): 1 sharp internal corner(s): radius 0 < kerf 0.1 mm (add a fillet >= kerf or the mating part will not seat).
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 5 routes vs 4 spec wires (extra ['w_esc_ml', 'w_esc_mr', 'w_rx_esc']) (missing ['w_m1', 'w_m2'])
- likeness.silhouette x3: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): stronghold.aws72.webp 0.73 -> 0.73; stronghold.aws74.webp 0.74 -> 0.74; stronghold.aws76.webp 0.77 -> 0.77

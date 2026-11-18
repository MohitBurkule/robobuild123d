
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type drum; body box rect 62x112x34 mm, ramp 0; wheels 2 r17 outboard; weapon drum r15 axis x teeth 2; extra parts: lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.82 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type drum; body box rect 62x112x34 mm, ramp 0; wheels 2 r17 outboard; weapon drum r15 axis x teeth 2; extra parts: lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws67 0.72 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/recycler.aws67.webp` is declared `front_left_iso` (IoU 0.72 there) but the model matches it better from rear_right_iso (elevati

## Round 4 (verification, helper 2)
Blockers r3 52 -> r4 11 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (brotherhobby_tc1404_3800kv), `lock_pin` (made)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `lid`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_arm_weapon_0`, `dt_arm_weapon_1`
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- weapon drive: motor not coaxial, belt drive implied
- weapon: running-clearance well in chassis not carved (it would open 291 mm2 of outside face)
- chassis: dm_wheel_l0 pocketed to its own outline (0.3 mm clear); only its shaft bore passes the wall to wheel_l0
- chassis: dm_wheel_r0 pocketed to its own outline (0.3 mm clear); only its shaft bore passes the wall to wheel_r0
- weapon: running-clearance well in dt_arm_weapon_0 not carved (it would open 26 mm2 of outside face)
- weapon: running-clearance well in dt_arm_weapon_1 not carved (it would open 35 mm2 of outside face)
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 351 g over 150: walls 2 mm -> 339 g
- mass estimate 339 g over 150: walls 1.6 mm -> 331 g
- hollowed chassis (wall 1.6, form 0): 236.1 -> 64.4 cm3
- hollowed lid (wall 1.97, form 1): 10.8 -> 7.8 cm3

Left (and why):
- proxy.wiring x1: Wire `w_sw_esc` (`el_switch.out` to `el_esc.bat`): no baseline route (run the full `wiring` group once and pass its report).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.interference x1: `chassis` and `weapon` overlap by 1.33 mm (allowed 0.08).
- proxy.sweep x2: joint `weapon`: `weapon` turning a full revolution may reach `chassis`.
- mfg.layer_load x2: `dt_arm_weapon_0` carries the `weapon` axle but is printed with build direction +z (world [0.0, 0.0, 1.0]), not along the spin axis [1.0, 0.0, 0.0]: impact load peels layers apart.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 6 routes vs 7 spec wires (missing ['w_sw_esc']); top.png: 6 routes vs 7 spec wires (missing ['w_sw_esc'])
- likeness.view x1: looks, not in scope for this pass.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): recycler.aws67.webp 0.59 -> 0.59

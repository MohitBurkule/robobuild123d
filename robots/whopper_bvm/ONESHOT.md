
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends side_fin to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 60x112x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; 4 forks 44 mm; extra parts: side_fin, arm.

Likeness: aws76 0.58 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 60x112x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; 4 forks 32 mm; extra parts: side_fin, arm.

Likeness: aws76 0.56 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 60x112x26 mm, ramp 0; wheels 2 r11 inboard; weapon none; 4 forks 34 mm; extra parts: arm, side_fin.

Likeness: aws76 0.29 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/whopper.aws76.webp` is declared `front_right_iso` (IoU 0.29 there) but the model matches it better from front_left_iso (elevati

## Round 4 (verification, helper 2)
Blockers r3 90 -> r4 14 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `side_fin`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- arm sweeps through chassis at 41 poses: not carved (would change the outside)
- no screw line found for fork_0
- no screw line found for fork_1
- no screw line found for fork_2
- no screw line found for fork_3
- rod dt_axle_wheel_l0: 2.2 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.2 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- hollowed chassis (wall 2.87, form 1): 174.7 -> 75.0 cm3

Left (and why):
- connection.cover_fasteners x1: `side_fin` is an armour / cover panel held by 0 fastener(s); it needs >= 2 real screws. Snap, press-fit or tape retention alone lets it peel off on the first hit.
- power.weapon_motor x1: toolchain: lifters/flippers are servo or gear driven; the check wants a brushless kV for every weapon.
- mfg.stock x4: `fork_0` (laser): thickness 2.50 mm is not a stock titanium gauge (0.5, 0.8, 0.9, 1, 1.5, 2, 3, 4, 5, 6, 8, 10); nearest 2 mm.
- process.weapon_printed x1: toolchain: a printed lifter/flipper arm is judged like a spinner (needs hardened teeth); adding metal teeth changes the look.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.rotor_clearance x4: toolchain: same full-revolution assumption; wires cannot leave a cylinder that covers the chassis.
- likeness.view x1: looks, not in scope for this pass.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): whopper.aws76.webp 0.29 -> 0.29

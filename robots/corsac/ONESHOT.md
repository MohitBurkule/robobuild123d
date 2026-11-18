
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (face), guessing the tilt maths by hand. ~3 min.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 80x100x26 mm, ramp 0; wheels 2 r12 inboard; weapon none; 6 forks 14 mm; extra parts: face.

Likeness: aws72 0.82 (ok), aws74 0.81 (ok), aws76 0.80 (ok).

## Round 2 (looks)
Decisions: type wedge; body box rect 80x100x26 mm, ramp 0; wheels 2 r12 inboard; weapon none; 6 forks 14 mm; extra parts: face.

Likeness: aws72 0.82 (ok), aws74 0.81 (ok), aws76 0.80 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 80x100x26 mm, ramp 0; wheels 2 r12 inboard; weapon none; 6 forks 16 mm; extra parts: face.

Likeness: aws72 0.66 (FAIL), aws74 0.68 (FAIL), aws76 0.63 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/corsac.aws72.webp` is declared `front_left_iso` (IoU 0.66 there) but the model matches it better from rear_right_iso (elevation; [FAIL] likeness.view: `reference/corsac.aws74.webp` is declared `front_right_iso` (IoU 0.68 there) but the model matches it better from rear_left_iso (elevation; [FAIL] likeness.view: `reference/corsac.aws76.webp` is declared `front_left_iso` (IoU 0.63 there) but the model matches it better from rear_left_iso (elevation 

## Round 4 (verification, helper 2)
Blockers r3 109 -> r4 16 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_mount_fork_0`, `dt_mount_fork_1`, `dt_mount_fork_2`, `dt_mount_fork_3`, `dt_mount_fork_4`, `dt_mount_fork_5`
- real fasteners: `fs_face_0` M2x10, `fs_face_1` M2x10
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- no screw line found for fork_0
- no screw line found for fork_1
- no screw line found for fork_2
- no screw line found for fork_3
- no screw line found for fork_4
- no screw line found for fork_5
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- chassis: 0 of 16 cuts dropped (they broke the solid: -10)
- mass estimate 165 g over 150: walls 2 mm -> 156 g
- mass estimate 156 g over 150: walls 1.6 mm -> 148 g
- hollowed chassis (wall 1.6, form 0): 189.2 -> 61.5 cm3

Left (and why):
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- mfg.stock x6: `fork_0` (laser): thickness 2.50 mm is not a stock titanium gauge (0.5, 0.8, 0.9, 1, 1.5, 2, 3, 4, 5, 6, 8, 10); nearest 2 mm.
- process.geometry x2: `face` (laser): 24 oblique planar face(s): chamfer/bevel; declare `secondary_ops: ["chamfer"]` or remove.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- likeness.view x3: looks, not in scope for this pass.
- likeness.silhouette x3: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): corsac.aws72.webp 0.66 -> 0.66; corsac.aws74.webp 0.68 -> 0.68; corsac.aws76.webp 0.63 -> 0.63

## Round 3c (user angle picks applied; shape fixed per user remarks)
Decisions: type wedge; body box rect 80x100x26 mm, ramp 0; wheels 2 r12 inboard; weapon none; 6 forks 16 mm; extra parts: face.

Likeness: aws72 0.63 (FAIL), aws74 0.65 (FAIL), aws76 0.62 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/corsac.aws72.webp` is declared `front_left_iso` (IoU 0.63 there) but the model matches it better from front_right_iso (elevatio; [FAIL] likeness.view: `reference/corsac.aws74.webp` is declared `front_right_iso` (IoU 0.65 there) but the model matches it better from front_left_iso (elevatio; [FAIL] likeness.view: `reference/corsac.aws76.webp` is declared `front_left_iso` (IoU 0.62 there) but the model matches it better from front_left_iso (elevation

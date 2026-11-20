
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 80x84x30 mm, ramp 32; wheels 4 r10 outboard as treads; weapon none; 6 forks 36 mm; extra parts: lid.

Likeness: aws72 0.69 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box rect 80x84x30 mm, ramp 32; wheels 4 r10 outboard as treads; weapon none; 6 forks 46 mm; extra parts: lid.

Likeness: aws72 0.66 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 80x84x30 mm, ramp 32; wheels 4 r12 outboard; weapon none; 6 forks 34 mm; extra parts: lid.

Likeness: aws72 0.47 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/pingu.aws72.webp` is declared `front` (IoU 0.47 there) but the model matches it better from rear_right_iso (elevation 45, azimu

## Round 4 (verification, helper 2)
Blockers r3 107 -> r4 1 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (pololu_hpcb6v_50to1), `dm_wheel_r1` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `lid`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`, `dt_mount_fork_0`, `dt_mount_fork_1`, `dt_mount_fork_2`, `dt_mount_fork_3`, `dt_mount_fork_4`, `dt_mount_fork_5`
- real fasteners: `fs_look_lid_0` M2x8, `fs_look_lid_1` M2x8, `fs_look_lid_2` M2x8, `fs_look_lid_3` M2x8
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- chassis: dm_wheel_l1 pocketed to its own outline (0.3 mm clear); only its shaft bore passes the wall to wheel_l1
- chassis: dm_wheel_r1 pocketed to its own outline (0.3 mm clear); only its shaft bore passes the wall to wheel_r1
- no screw line found for fork_0
- no screw line found for fork_1
- no screw line found for fork_2
- no screw line found for fork_3
- no screw line found for fork_4
- no screw line found for fork_5
- rod dt_axle_wheel_l1: 2.8 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 2.8 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- hollowed chassis (wall 2.5, form 0): 163.3 -> 61.2 cm3

Left (and why):
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): pingu.aws72.webp 0.64 -> 0.64

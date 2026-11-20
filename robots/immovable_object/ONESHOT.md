# immovable_object: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Black box chassis, 4 red wheels (rear r 15, front r 11) outside, wide red front shield (112 wide, sloped) and 4 steel spikes.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| immovable_object.aws69.webp | 0.71 | 0.80 | revron 0.76 | FAIL |
| immovable_object.aws71.webp | 0.70 | 0.80 | wedge_2wd 0.77 | FAIL |
| immovable_object.aws72.webp | 0.72 | 0.80 | vspin_drisk 0.75 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Shield is a flat-topped extrusion, real one is arched in front view and curved; spikes are flat strips not barbed points; wheels lack spokes. Front third IoU 0.43-0.48.

## Missing tool / hint
Kit wheels share one radius; no arched shield primitive; forks cannot be pointed.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Arched shield (side profile intersected with a front arch), barbed arrow spikes, bigger spoked-hub wheels further outboard, top block.

Likeness: aws69 0.73 (FAIL), aws71 0.73 (FAIL), aws72 0.75 (FAIL).

## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 85x64x26 mm, ramp 0; wheels 4 r15 outboard; weapon none; 4 forks 38 mm.

Likeness: aws69 0.73 (FAIL), aws71 0.73 (FAIL), aws72 0.75 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 85x64x26 mm, ramp 0; wheels 4 r15 outboard; weapon none; 4 forks 38 mm.

Likeness: aws69 0.57 (FAIL), aws71 0.33 (FAIL), aws72 0.71 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/immovable_object.aws69.webp` is declared `front_right_iso` (IoU 0.57 there) but the model matches it better from front_left_iso; [FAIL] likeness.view: `reference/immovable_object.aws71.webp` is declared `front` (IoU 0.33 there) but the model matches it better from front_left_iso (elevatio

## Round 4 (verification, helper 2)
Blockers r3 105 -> r4 10 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (pololu_hpcb6v_50to1), `dm_wheel_r1` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `shield`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`, `dt_mount_fork_0`, `dt_mount_fork_1`, `dt_mount_fork_2`, `dt_mount_fork_3`
- real fasteners: `fs_look_chassis_0` M2x6, `fs_look_chassis_1` M2x6, `fs_look_chassis_2` M2x6, `fs_look_chassis_3` M2x6
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- no screw line found for fork_0
- no screw line found for fork_1
- no screw line found for fork_2
- no screw line found for fork_3
- rod dt_axle_wheel_l1: 2.8 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 2.8 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- mass estimate 166 g over 150: walls 2 mm -> 155 g
- mass estimate 155 g over 150: walls 1.6 mm -> 146 g
- hollowed chassis (wall 1.6, form 0): 142.1 -> 49.0 cm3
- hollowed shield (wall 1.6, form 0): 68.4 -> 22.7 cm3

Left (and why):
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- connection.cover_fasteners x1: `shield` is an armour / cover panel held by 0 fastener(s); it needs >= 2 real screws. Snap, press-fit or tape retention alone lets it peel off on the first hit.
- process.geometry x4: `fork_0` (laser): 2 sharp internal corner(s): radius 0 < kerf 0.1 mm (add a fillet >= kerf or the mating part will not seat).
- likeness.silhouette x3: looks, not in scope for this pass.
- likeness.view x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): immovable_object.aws69.webp 0.73 -> 0.73; immovable_object.aws71.webp 0.33 -> 0.33; immovable_object.aws72.webp 0.71 -> 0.71


## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 92x80x24 mm, ramp 0; wheels 4 r10 outboard as treads; weapon none; extra parts: front_plate.

Likeness: aws71 0.83 (ok).

## Round 2 (looks)
Decisions: type wedge; body box rect 92x80x24 mm, ramp 0; wheels 4 r10 outboard as treads; weapon none; extra parts: front_plate.

Likeness: aws71 0.83 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 92x80x24 mm, ramp 0; wheels 4 r12 outboard; weapon none; extra parts: front_plate.

Likeness: aws71 0.70 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/i_never_asked_for_this.aws71.webp` is declared `front_left_iso` (IoU 0.70 there) but the model matches it better from rear_left

## Round 4 (verification, helper 2)
Blockers r3 62 -> r4 4 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (pololu_hpcb6v_50to1), `dm_wheel_r1` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`
- real fasteners: `fs_front_plate_0` M2x10, `fs_front_plate_1` M2x10
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- rod dt_axle_wheel_l1: 2.8 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 2.8 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- chassis: 1 of 19 cuts dropped (they broke the solid: 2)
- mass estimate 157 g over 150: walls 2 mm -> 149 g
- mass estimate 149 g over 150: walls 1.6 mm -> 143 g
- hollowed chassis (wall 1.6, form 0): 176.6 -> 55.2 cm3

Left (and why):
- proxy.interference x1: `chassis` and `front_plate` overlap by 1.12 mm (allowed 0.08).
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- likeness.view x1: looks, not in scope for this pass.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): i_never_asked_for_this.aws71.webp 0.7 -> 0.7

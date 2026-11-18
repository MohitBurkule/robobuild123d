
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 90x82x28 mm, ramp 30; wheels 4 r11 inboard; weapon none; extra parts: front_plate; textured masks for indices [0, 1].

Likeness: push_mk_1 0.53 (FAIL), push_mk_2 0.29 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box rect 90x82x28 mm, ramp 30; wheels 4 r11 inboard; weapon none; extra parts: front_plate.

Likeness: push_mk_1 0.67 (FAIL), push_mk_2 0.68 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 90x82x20 mm, ramp 26; wheels 4 r12 inboard; weapon none; extra parts: front_plate.

Likeness: push_mk_1 0.69 (FAIL), push_mk_2 0.71 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 49 -> r4 5 (`verify --tier inner`).

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
- chassis: 1 of 15 cuts dropped (they broke the solid: 2)
- hollowed chassis (wall 2.5, form 0): 105.1 -> 51.8 cm3

Left (and why):
- proxy.interference x1: `chassis` and `front_plate` overlap by 1.38 mm (allowed 0.08).
- process.geometry x1: `front_plate` (laser): thinnest web between cut features is 0.22 mm < 3.00 mm (1.00 x thickness 3.00 mm).
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- likeness.silhouette x2: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): push_mk_1.webp 0.69 -> 0.69; push_mk_2.webp 0.71 -> 0.71

## Round 3c (user angle picks applied; shape fixed per user remarks)
Decisions: type wedge; body box rect 90x82x22 mm, ramp 0; wheels 4 r12 inboard; weapon none; extra parts: front_plate.

Likeness: push_mk_1 0.65 (FAIL), push_mk_2 0.71 (FAIL).

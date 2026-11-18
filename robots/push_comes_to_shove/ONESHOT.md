
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

## Round 3c (user angle picks applied; shape fixed per user remarks)
Decisions: type wedge; body box rect 90x82x22 mm, ramp 0; wheels 4 r12 inboard; weapon none; extra parts: front_plate.

Likeness: push_mk_1 0.65 (FAIL), push_mk_2 0.71 (FAIL).

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type wedge; body box rect 78x72x3 mm, ramp 0; wheels 4 r12 inboard; weapon none; extra parts: side_plate, top_plate, front_plate, rear_plate, motor_rear, motor_front, battery_pack, receiver, standoff_r, standoff_f.

Likeness: push_mk_1 0.69 (FAIL), push_mk_2 0.68 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 52 -> r4 18 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (bbb_n10_600rpm), `dm_wheel_r1` (bbb_n10_600rpm), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `motor_rear_l`, `motor_rear_r`, `motor_front_l`, `motor_front_r`, `battery_pack`, `receiver`, `standoff_r_l`, `standoff_r_r`, `standoff_f_l`, `standoff_f_r`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- front_plate: aluminium laser is not a flat plate -> printed nylon
- rear_plate: aluminium laser is not a flat plate -> printed nylon
- dm_wheel_l1/dm_wheel_r1: N10 gearmotors (shorter) so the pair fits across
- dm_wheel_l1/dm_wheel_r1: slid 1.3 mm out into the wheel hubs so they do not meet (still short)
- no free space for ['el_battery', 'el_esc']
- motor_front_l: a cut was not made (it would open 52 mm2 of outside face; the overlap stays as a finding)
- motor_front_r: a cut was not made (it would open 45 mm2 of outside face; the overlap stays as a finding)
- overlaps left: dm_wheel_l1/dm_wheel_r1 0.14
- no screw line found for top_plate
- rod dt_axle_wheel_l1: 1.5 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 1.5 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- wheel_l1: 1 of 1 cuts dropped (they broke the solid: 2)
- wheel_r1: 1 of 1 cuts dropped (they broke the solid: 2)
- hollow skipped front_plate: solids 1 vol 1.00
- hollow skipped rear_plate: solids 1 vol 0.99
- hollowed motor_rear_l (wall 2.5, form 0): 2.6 -> 2.0 cm3
- hollowed motor_rear_r (wall 2.5, form 0): 2.6 -> 2.0 cm3
- hollow skipped motor_front_l: solids 1 vol 0.93
- hollow skipped motor_front_r: solids 1 vol 0.93
- hollowed battery_pack (wall 2.5, form 0): 5.2 -> 4.0 cm3
- side_plate_l: no screw line and no slot, left undeclared (needs a real mount)
- side_plate_r: no screw line and no slot, left undeclared (needs a real mount)
- top_plate: no screw line and no slot, left undeclared (needs a real mount)
- front_plate: not touching the chassis, left undeclared
- rear_plate: not touching the chassis, left undeclared

Left (and why):
- integrity.solids x2: `wheel_l1` has 2 closed solid(s) and 0 open/invalid shell(s), expected 1 (3630 mm3). A boolean or fillet probably collapsed the build.
- proxy.interference x5: `wheel_l1` and `dm_wheel_l1` overlap by 1.16 mm (allowed 0.08).
- connection.floating x5: `side_plate_l` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis. Nearest part is `top_plate`, 0.0 mm away.
- connection.cover_fasteners x1: `rear_plate` is an armour / cover panel held by 0 fastener(s); it needs >= 2 real screws. Snap, press-fit or tape retention alone lets it peel off on the first hit.
- electrical.receiver_supply x1: No receiver: no part of kind `receiver` and no combined ESC/receiver.
- fit.interference x2: `dm_wheel_l1` overlaps wall `motor_front_l` by 3.38 mm: it will not go in. No side has 3.58 mm free (free room per side {'-x': 2.8, '+x': 0.0, '-y': -0.0, '+y': -0.0, '-z': 0.91, '+z': 0.91}): grow th
- likeness.silhouette x2: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): push_mk_1.webp 0.69 -> 0.69; push_mk_2.webp 0.68 -> 0.68

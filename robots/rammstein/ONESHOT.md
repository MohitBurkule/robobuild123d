
## Tools I wanted
- This robot was built before the kit extras existed: all shapes were hand-written prisms in a private generator (`oneshot.py`/`gen.py`), ~15 min. Wanted: body side/top polygons, hinged weapons, scoop, wheel notches, colours (see refprs/fable_tool_wishlist.md).
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)


Likeness: aws71 0.76 (FAIL), aws72 0.80 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 76 -> r4 21 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `chassis_bottom`, `wedge`, `carbon_plate`, `dt_hub_wheel_l`, `dt_hub_wheel_r`, `dt_hub_wheel_fl`, `dt_hub_wheel_fr`
- real fasteners: `bolt_c0` M2x8, `bolt_c1` M2x8, `bolt_c2` M2x8, `bolt_c3` M2x8, `bolt_w0` M2x6, `bolt_w1` M2x6, `bolt_w2` M2x6, `bolt_w3` M2x6
- 5 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- rod dt_axle_wheel_l shortened to 4.8 mm clear of ['motor_l']
- rod dt_axle_wheel_r shortened to 4.8 mm clear of ['motor_r']
- hollowed chassis_bottom (wall 3.41, form 2): 18.5 -> 16.5 cm3
- hollowed chassis_top (wall 2.87, form 1): 16.7 -> 15.3 cm3
- hollow skipped wedge: solids -10 vol 1.00

Left (and why):
- integrity.solids x2: `chassis_top` has 0 closed solid(s) and 1 open/invalid shell(s), expected 1 (15338 mm3). A boolean or fillet probably collapsed the build.
- proxy.interference x6: `motor_l` and `carbon_plate` overlap by 0.37 mm (allowed 0.08).
- connection.fused_mismatch x2: `chassis_bottom` is fused to `chassis_top` but they share 0.00 mm3 (need >= 1 mm3); faces that only touch print as two pieces or a paper-thin seam.
- connection.tape_overload x1: `battery` weighs 12.5 g on 4.15 cm2 of contact (3.0 g/cm2); velcro holds at most 2 g/cm2 through a hit.
- connection.floating x1: `battery` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis. Nearest part is `chassis_bottom`, 0.4 mm away.
- fastener.access x4: `bolt_c0` (hex1.5) is blocked by `carbon_plate` 0.0 mm above the head; the driver needs a clear 2.5 mm wide, 14 mm long path straight out of the head.
- fit.interference x2: `motor_l` overlaps wall `carbon_plate` by 0.37 mm: it will not go in. No side has 0.57 mm free (free room per side {'-x': 0.15, '+x': 0.25, '-y': 0.11, '+y': 0.12, '-z': 0.28, '+z': 0.28}): grow the p
- likeness.silhouette x2: looks, not in scope for this pass.
- geom.tiny_edge x1: `chassis_top`: 12 edge(s) shorter than 0.05 mm, shortest 0.0026 mm. World mm: [27.8, 30.0, 0.77] 0.0026 mm; [-27.8, 30.0, 0.77] 0.0026 mm; [27.79, 30.0, 4.5] 0.0112 mm; [-27.79, 30.0, 4.5] 0.0112 mm; 

Likeness (best silhouette IoU per photo, r3 -> r4): rammstein.aws71.png 0.76 -> 0.76; rammstein.aws72.png 0.8 -> 0.8

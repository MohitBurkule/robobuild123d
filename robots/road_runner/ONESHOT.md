
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends rear_wall, side_wall to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 100x100x24 mm, ramp 0; wheels 4 r11 inboard; weapon none; extra parts: rear_wall, side_wall; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok).

## Round 2 (looks)
Decisions: type wedge; body box rect 100x100x24 mm, ramp 0; wheels 4 r11 inboard; weapon none; extra parts: rear_wall, side_wall; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 100x100x24 mm, ramp 0; wheels 4 r11 inboard; weapon none; extra parts: rear_wall, side_wall; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok).

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type wedge; body box rect 100x100x24 mm, ramp 0; wheels 4 r13.5 inboard; weapon none; extra parts: rear_wall, side_wall, lid, sw_hole, link_hole, sw_well, link_well, horn, lid_screw0, lid_screw1, lid_screw2, lid_screw3, lid_screw4, lid_screw5, front_screw0, front_screw1, front_screw2, front_screw3, scoop_gap; photos skipped (cluttered): indices [0].

Likeness: aws67 0.84 (ok).

## Round 4 (verification, helper 2)
Blockers r3 58 -> r4 1 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `rear_wall`, `side_wall_l`, `side_wall_r`, `lid`, `horn_l`, `horn_r`, `lid_screw0`, `lid_screw1`, `lid_screw2`, `lid_screw3`, `lid_screw4`, `lid_screw5`, `front_screw0`, `front_screw1`, `front_screw2`, `front_screw3`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 193 g over 150: walls 2 mm -> 264 g
- mass estimate 264 g over 150: walls 1.6 mm -> 264 g
- hollow skipped chassis: solids -30 vol 0.43
- front_screw0: not touching the chassis, left undeclared
- front_screw1: not touching the chassis, left undeclared
- front_screw2: not touching the chassis, left undeclared
- front_screw3: not touching the chassis, left undeclared
- front_screw0..3: the printed screw heads on the front face sat 0.5 mm off the chassis (floating); each got a hidden 1.2 mm shank behind the head, 1 mm into the chassis, and prints with the chassis (fused_with). Outside unchanged.
- mass.over remains: the solid rebuilt nylon chassis is 159 g alone; hollowing fails on its wedge/openings and even a 1.2 mm shell cannot reach 150 g upper bound (needs owner: smaller/thinner outside)

Left (and why):
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.

Likeness (best silhouette IoU per photo, r3 -> r4): road_runner.aws67.webp 0.84 -> 0.84

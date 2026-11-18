
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (lip), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box trapezoid 100x84x46 mm, ramp 88; wheels 2 r14 outboard; weapon none; extra parts: lip; photos skipped (cluttered): indices [0, 2]; textured masks for indices [1].

Likeness: aws61 0.81 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box trapezoid 100x84x46 mm, ramp 88; wheels 2 r14 outboard; weapon none; extra parts: lip; photos skipped (cluttered): indices [0, 2]; textured masks for indices [1].

Likeness: aws61 0.81 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box trapezoid 92x78x44 mm, ramp 82; wheels 2 r14 outboard; weapon none; extra parts: lip; photos skipped (cluttered): indices [0, 2]; textured masks for indices [1].

Likeness: aws61 0.83 (ok).

## Round 4 (verification, helper 2)
Blockers r3 39 -> r4 1 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_strut_lip`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- no screw line found for lip
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- hollowed chassis (wall 2.5, form 0): 179.8 -> 67.7 cm3

Left (and why):
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.

Likeness (best silhouette IoU per photo, r3 -> r4): smart_ant_5_.aws61.webp 0.83 -> 0.82

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type wedge; body box trapezoid 92x78x44 mm, ramp 82; wheels 2 r14 outboard; weapon none; extra parts: lip, slot00, slot01, slot02, slot03, slot04, slot05, slot10, slot11, slot12, slot13, slot14, slot15, slot20, slot21, slot22, slot23, slot24, slot25, bay, battery_pack, receiver, hinge_block, hinge_pin; photos skipped (cluttered): indices [0, 2]; textured masks for indices [1].

Likeness: aws61 0.83 (ok).

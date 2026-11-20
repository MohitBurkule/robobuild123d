
## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (flipper), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type flipper; body box rect 100x100x42 mm, ramp 62; wheels 2 r12 inboard; weapon none; extra parts: lid, flipper; photos skipped (cluttered): indices [1].

Likeness: aws76 0.77 (FAIL).

## Round 2 (looks)
Decisions: type flipper; body box rect 100x100x42 mm, ramp 62; wheels 2 r12 inboard; weapon none; extra parts: lid, flipper; photos skipped (cluttered): indices [1].

Likeness: aws76 0.77 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box rect 100x100x42 mm, ramp 62; wheels 2 r12 inboard; weapon none; extra parts: lid, flipper; photos skipped (cluttered): indices [1].

Likeness: aws76 0.58 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/brisk.aws76.webp` is declared `front_left_iso` (IoU 0.58 there) but the model matches it better from front_right_iso (elevation

## Round 4 (verification, helper 2)
Blockers r3 56 -> r4 3 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `lid`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- real fasteners: `fs_look_lid_0` M2x8, `fs_look_lid_1` M2x8, `fs_look_lid_2` M2x8, `fs_look_lid_3` M2x8
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- flipper: heel running clearance (0.3 mm, 41 poses, within 14.4 mm of the pivot) carved in chassis; opens 0 mm2 of outside face
- flipper: heel running clearance (0.3 mm, 41 poses, within 16.9 mm of the pivot) carved in lid; opens 11 mm2 of outside face
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- hollowed chassis (wall 2.5, form 0): 294.4 -> 93.5 cm3

Left (and why):
- proxy.sweep x1: joint `flipper`: `flipper` hits `chassis` 0.23 mm deep at 7.3 (declared range 0..80; allowed 0.08). `robot probe spec.json --joint flipper` lists the closest approach to every part.
- power.weapon_motor x1: toolchain: lifters/flippers are servo or gear driven; the check wants a brushless kV for every weapon.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): brisk.aws76.webp 0.77 -> 0.77

## Round 5 (user notes)
- Front wedge is now its own printed plate (`wedge_plate`, 2.5 mm nylon), not part of the chassis: hexagonal outline (full-width foot, 30 mm chamfers to a 56 mm top edge) with a 14 x 28 mm slot open at the top.
- The yellow arm (`flipper`) lies in that slot and shares the plate's top hinge pin; the plate `rotates_with` the arm, so the arm holds it down and lifts it (0..80 deg).
- Chassis ramp face recedes 3.5 mm behind the plate (1 mm running gap); lid shortened 5 mm at the front so the hinge clears it; lid screws moved back with it.
Blockers 3 -> 2 (flipper actuator, likeness; the flipper-vs-chassis sweep is gone), IoU 0.77 -> 0.77.

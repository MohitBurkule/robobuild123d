
## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (flipper), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type flipper; body box rect 90x80x20 mm, ramp 0; wheels 2 r10 inboard; weapon none; extra parts: flipper; textured masks for indices [0].

Likeness: aws63 0.65 (FAIL).

## Round 2 (looks)
Decisions: type flipper; body box rect 90x80x20 mm, ramp 0; wheels 2 r10 inboard; weapon none; extra parts: flipper; textured masks for indices [0].

Likeness: aws63 0.65 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box rect 90x80x20 mm, ramp 0; wheels 2 r10 inboard; weapon none; extra parts: flipper; textured masks for indices [0].

Likeness: aws63 0.62 (FAIL).

## Round 4 (verification, helper 1)
S1: flipper hollowed with a closed internal 48x100x5 mm cavity (3.5 mm walls), mass 165 -> ~142 g.

## Round 4 (verification, helper 2)
Blockers r3 52 -> r4 2 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- real fasteners: `fs_look_chassis_0` M2x6, `fs_look_chassis_1` M2x6, `fs_look_chassis_2` M2x6, `fs_look_chassis_3` M2x6
- 5 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- flipper: joint axis reversed so positive travel lifts the tip (it drove into the chassis)
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 174 g over 150: walls 2 mm -> 169 g
- mass estimate 169 g over 150: walls 1.6 mm -> 164 g
- hollowed chassis (wall 1.6, form 0): 144.0 -> 48.5 cm3

Left (and why):
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): io.aws63.webp 0.62 -> 0.63

## Round 5 (photo / DESCRIPTION.md)
- The flipper is now a 3 mm plate (the photo's thin aluminium plate), not a 12 mm hollow slab: 53.9 -> about 19 g, which clears the mass blocker. `volume_mm3` is declared.
- A white printed triangular bracket (`flipper_bracket`, fused with the flipper) runs from the hinge to the plate's underside, as in the photo.
- Not done:
  - 4 wheels: the photo shows 4, but REFERENCE.json says 2 (a collector file).
  - White deck inside the yellow rim: a decal is refused, because the top face is cut by the flipper sweep.
- Blockers 2 -> 1, IoU 0.63 -> 0.63, mass 151.0 -> 121.2 g.

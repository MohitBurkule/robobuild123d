
## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop, flipper), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type flipper; body box pentagon 85x92x42 mm, ramp 30; wheels 2 r11 inboard; weapon none; extra parts: scoop, flipper; photos skipped (cluttered): indices [0].

Likeness: aws72 0.85 (ok), aws77 0.87 (ok).

## Round 2 (looks)
Decisions: type flipper; body box pentagon 85x92x42 mm, ramp 30; wheels 2 r11 inboard; weapon none; extra parts: scoop, flipper; photos skipped (cluttered): indices [0].

Likeness: aws72 0.85 (ok), aws77 0.87 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box pentagon 85x92x42 mm, ramp 30; wheels 2 r11 inboard; weapon none; extra parts: scoop, flipper; photos skipped (cluttered): indices [0].

Likeness: aws72 0.85 (ok), aws77 0.85 (ok).

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type flipper; body box pentagon 85x92x42 mm, ramp 30; wheels 2 r11 inboard; weapon none; extra parts: scoop, flipper; photos skipped (cluttered): indices [0].

Likeness: aws72 0.85 (ok), aws77 0.86 (ok).

## Round 4 (verification, helper 2)
Blockers r3 44 -> r4 7 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `scoop`, `ripper_remix_name`, `ripper_name`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 317 g over 150: walls 2 mm -> 312 g
- mass estimate 312 g over 150: walls 1.6 mm -> 308 g
- hollow skipped chassis: solids 2 vol 0.30
- hollowed scoop (wall 1.6, form 0): 78.6 -> 19.7 cm3
- photo graphics as fused colour-split decals (robot decal): RIPPER / REMIX lettering on the flipper's front slope

Left (and why):
- proxy.wiring x2: Wire `w_sw_esc` (`el_switch.out` to `el_esc.bat`): no baseline route (run the full `wiring` group once and pass its report).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- power.weapon_motor x1: toolchain: lifters/flippers are servo or gear driven; the check wants a brushless kV for every weapon.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 3 routes vs 4 spec wires (missing ['w_sw_esc']); top.png: 3 routes vs 4 spec wires (missing ['w_sw_esc'])

Likeness (best silhouette IoU per photo, r3 -> r4): ripper_remix.aws72.webp 0.85 -> 0.85; ripper_remix.aws77.webp 0.86 -> 0.86

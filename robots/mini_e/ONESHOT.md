
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (wedge), guessing the tilt maths by hand. ~3 min.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 72x100x22 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: wedge; photos skipped (cluttered): indices [0].

Likeness: aws72 0.81 (FAIL), aws76 0.81 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box rect 72x100x22 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: wedge; photos skipped (cluttered): indices [0].

Likeness: aws72 0.81 (FAIL), aws76 0.81 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 72x100x22 mm, ramp 0; wheels 2 r14 inboard; weapon none; extra parts: wedge; photos skipped (cluttered): indices [0].

Likeness: aws72 0.70 (FAIL), aws76 0.66 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/mini_e.aws72.webp` is declared `front_left_iso` (IoU 0.70 there) but the model matches it better from rear_right_iso (elevation; [FAIL] likeness.view: `reference/mini_e.aws76.webp` is declared `front_right_iso` (IoU 0.66 there) but the model matches it better from rear_right_iso (elevatio

## Round 4 (verification, helper 2)
Blockers r3 46 -> r4 5 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `wedge`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- rod dt_axle_wheel_l0: 2.2 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.2 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- hollowed chassis (wall 2.5, form 0): 128.6 -> 68.3 cm3
- hollowed wedge (wall 2.5, form 0): 73.5 -> 30.8 cm3

Left (and why):
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- likeness.view x2: looks, not in scope for this pass.
- likeness.silhouette x2: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): mini_e.aws72.webp 0.7 -> 0.7; mini_e.aws76.webp 0.66 -> 0.66

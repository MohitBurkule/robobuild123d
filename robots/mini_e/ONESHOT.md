
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

## Round 3c (user angle picks applied; shape fixed per user remarks)
Decisions: type other; body box rect 72x100x22 mm, ramp 0; wheels 2 r14 inboard; weapon none; extra parts: bumper, skirt; photos skipped (cluttered): indices [0].

Likeness: aws72 0.69 (FAIL), aws76 0.66 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/mini_e.aws72.webp` is declared `front_left_iso` (IoU 0.69 there) but the model matches it better from front_right_iso (elevatio; [FAIL] likeness.view: `reference/mini_e.aws76.webp` is declared `front_right_iso` (IoU 0.66 there) but the model matches it better from rear_right_iso (elevatio

## Round 4 (verification, helper 2)
Blockers r3 50 -> r4 9 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `skirt`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- real fasteners: `fs_bumper_0` M2x10
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- skirt: polycarbonate laser is not a flat plate -> printed nylon
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- skirt: 1 of 1 cuts dropped (they broke the solid: 2)
- hollowed chassis (wall 2.5, form 0): 128.6 -> 59.1 cm3
- hollow skipped skirt: solids 1 vol 1.01

Left (and why):
- integrity.solids x1: `chassis` has 0 closed solid(s) and 1 open/invalid shell(s), expected 1 (58748 mm3). A boolean or fillet probably collapsed the build.
- proxy.interference x2: `bumper` and `skirt` overlap by 0.40 mm (allowed 0.08).
- connection.cover_fasteners x1: `bumper` is an armour / cover panel held by 1 fastener(s); it needs >= 2 real screws. Snap, press-fit or tape retention alone lets it peel off on the first hit.
- process.geometry x1: `bumper` (laser): thinnest web between cut features is 0.09 mm < 3.00 mm (1.00 x thickness 3.00 mm).
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 2 routes vs 4 spec wires (missing ['w_bat_sw', 'w_sw_esc']); top.png: 2 routes vs 4 spec wires (missing ['w_bat_sw', 'w_sw_esc'])
- likeness.view x1: looks, not in scope for this pass.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): mini_e.aws72.webp 0.8 -> 0.8; mini_e.aws76.webp 0.66 -> 0.66

## Round 5 (user notes)
- Wheel guards: the wheel slots are now top windows (16.5 x 33 mm, 1.5 mm corner radius) with a 4 mm side wall outboard of each wheel, so the wheels sit inside the body as in the photo (the corner radius also closes the open mesh shell the square slots gave).
- Front wedge: bumper raised to the deck (12 mm, top flush), two M2 countersunk screws at x = +-18 into 6 mm printed bosses (was 1 screw on a 0.09 mm web); skirt is longer (to y = 62) and flares to 118 mm with chamfered front corners: the triangular side facets.
- Wiring: battery turned so its lead faces the switch; channels cut between the gearmotors and over them, all 4 wires route.
Blockers 11 -> 2 (likeness on aws76 only); IoU aws72 0.804 -> 0.808, aws76 0.662 -> 0.700.


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

## Round 4 (verification, helper 2)
Blockers r3 58 -> r4 1 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `rear_wall`, `side_wall_l`, `side_wall_r`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- rod dt_axle_wheel_l0: 2.2 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.2 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 155 g over 150: walls 2 mm -> 146 g
- hollowed chassis (wall 2, form 0): 198.5 -> 70.5 cm3

Left (and why):
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.

Likeness (best silhouette IoU per photo, r3 -> r4): road_runner.aws67.webp 0.87 -> 0.87

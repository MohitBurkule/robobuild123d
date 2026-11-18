# refined_for_the_roboteers_plea: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Black box chassis, wide red plough at the front, 2 wheels r 13 rear outside, white gear + tall white arm with a small 6-tooth saw disc at the tip. robot_type other (overhead saw arm).

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| refined_for_the_roboteers_pleasure.aws74.webp | 0.76 | 0.80 | revron_ant 0.72 | FAIL |
| refined_for_the_roboteers_pleasure.aws76.webp | 0.73 | 0.80 | hspin_bar 0.73 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Plough should wrap around the sides with angled wings; arm is a straight blade (real one is curved with a servo saddle); aws76 shows an axe head instead of the saw; gear has no teeth.

## Missing tool / hint
No 'arm with tool at tip' weapon in the kit; robot_type list has no axe/saw type.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Toothed gear, thicker forward-leaning arm with servo saddle, longer plough with angled wings.

Likeness: aws74 0.70 (FAIL), aws76 0.66 (FAIL).

## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type other; body box rect 75x70x22 mm, ramp 0; wheels 2 r13 outboard; weapon disc r11 axis x teeth 6.

Likeness: aws74 0.69 (FAIL), aws76 0.67 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type other; body box rect 75x70x22 mm, ramp 0; wheels 2 r13 outboard; weapon disc r11 axis x teeth 6.

Likeness: aws74 0.56 (FAIL), aws76 0.51 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/refined_for_the_roboteers_pleasure.aws74.webp` is declared `front_left_iso` (IoU 0.56 there) but the model matches it better fr; [FAIL] likeness.view: `reference/refined_for_the_roboteers_pleasure.aws76.webp` is declared `front_left_iso` (IoU 0.51 there) but the model matches it better fr

## Round 4 (verification, helper 2)
Blockers r3 60 -> r4 10 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (brotherhobby_tc1404_3800kv)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `plough`, `gear`, `arm`, `gear_mount`, `servo_saddle`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- 7 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- weapon drive: motor not coaxial, belt drive implied
- weapon: no locking pin added (weapon sits 84.0 mm from the frame; a pin across that gap would change the outside)
- weapon: running-clearance well in arm not carved (it would open 98 mm2 of outside face)
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- chassis: 0 of 12 cuts dropped (they broke the solid: -10)
- mass estimate 178 g over 150: walls 2 mm -> 168 g
- mass estimate 168 g over 150: walls 1.6 mm -> 160 g
- hollowed chassis (wall 1.6, form 0): 105.0 -> 51.1 cm3
- hollowed plough (wall 1.6, form 0): 77.3 -> 20.8 cm3
- hollowed gear (wall 1.6, form 0): 8.3 -> 4.5 cm3
- hollowed arm (wall 1.6, form 0): 9.1 -> 6.2 cm3
- hollowed gear_mount (wall 1.6, form 0): 4.8 -> 2.6 cm3
- hollowed servo_saddle (wall 1.6, form 0): 3.7 -> 1.9 cm3

Left (and why):
- proxy.wiring x3: Wire `w_sw_esc` (`el_switch.out` to `el_esc.bat`): the baseline route is now blocked by `chassis` (5 samples).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- connection.cover_fasteners x1: `plough` is an armour / cover panel held by 0 fastener(s); it needs >= 2 real screws. Snap, press-fit or tape retention alone lets it peel off on the first hit.
- legal.locking_bar x1: Rule 5f: every spinner needs a locking bar that physically stops the weapon from turning.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 5 routes vs 7 spec wires (missing ['w_m1', 'w_sig_wesc']); top.png: 5 routes vs 7 spec wires (missing ['w_m1', 'w_sig_wesc'])
- likeness.silhouette x2: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): refined_for_the_roboteers_pleasure.aws74.webp 0.69 -> 0.69; refined_for_the_roboteers_pleasure.aws76.webp 0.66 -> 0.66

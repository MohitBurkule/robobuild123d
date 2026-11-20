# gyronino: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Gyro walker, so kit wheels were removed. Pale body box with orange tail cap, orange gyro block, vertical orange ring (r 40) with cross spoke, black bevel gear, big blue double-ended bar (r 62) spinning about y at the front, two blue feet wedges.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| gyronino.aws72.webp | 0.65 | 0.80 | revron_ant 0.71 | FAIL |
| gyronino.aws74.webp | 0.62 | 0.80 | revron 0.66 | FAIL |
| gyronino.aws76.webp | 0.64 | 0.80 | revron_ant 0.66 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Body sits level instead of tilted on its tail; blade is a straight bar not the hooked axe heads; ring/gear proportions approximate; struts crude. Rear third IoU poor (0.33-0.45).

## Missing tool / hint
Kit cannot do wheel-less walkers, y-axis weapons, rings or a pitched body; needs a 'pitch' body param and a walker locomotion kind.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Whole robot pitched 18 deg tail-down, S-curved bar with hooked axe heads (kit bar curve), bevel gear as a cone, steeper feet, tapered tail cap.

Likeness: aws72 0.64 (FAIL), aws74 0.64 (FAIL), aws76 0.62 (FAIL).
Other likeness findings: [FAIL] likeness.weapon: Photos: bar turns about y; `weapon` turns about z (axis [0.0, 0.0, 1.0]). x = across the robot (horizontal drum/vertical disc), z = up (

## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 80x44x36 mm, ramp 0; wheels 2 r32 outboard; weapon bar r76 axis z teeth 2.

Likeness: aws72 0.63 (FAIL), aws74 0.65 (FAIL), aws76 0.60 (FAIL).
Other likeness findings: [FAIL] likeness.weapon: Photos: bar turns about y; `weapon` turns about z (axis [0.0, 0.0, 1.0]). x = across the robot (horizontal drum/vertical disc), z = up (

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 80x44x36 mm, ramp 0; wheels 2 r32 outboard; weapon bar r76 axis z teeth 2.

Likeness: aws72 0.43 (FAIL), aws74 0.51 (FAIL), aws76 0.25 (FAIL).
Other likeness findings: [FAIL] likeness.weapon: Photos: bar turns about y; `weapon` turns about z (axis [0.0, 0.0, 1.0]). x = across the robot (horizontal drum/vertical disc), z = up (; [FAIL] likeness.view: `reference/gyronino.aws72.webp` is declared `front_right_iso` (IoU 0.43 there) but the model matches it better from right (elevation 45, a; [FAIL] likeness.view: `reference/gyronino.aws74.webp` is declared `front_right_iso` (IoU 0.51 there) but the model matches it better from right (elevation 25, a; [FAIL] likeness.view: `reference/gyronino.aws76.webp` is declared `front_right_iso` (IoU 0.25 there) but the model matches it better from rear_right_iso (elevat

## Round 3c (user angle picks applied; shape fixed per user remarks)
Decisions: type vertical_spinner; body box rect 60x44x44 mm, ramp 0; wheels 2 r10 outboard; weapon bar r62 axis y teeth 2; extra parts: tail_cap, gyro_block, gyro_ring, spoke_h, spoke_v, bevel_gear, bevel_hub, nose_hub, foot, tail_skid.

Likeness: aws72 0.62 (FAIL), aws74 0.60 (FAIL), aws76 0.34 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/gyronino.aws76.webp` is declared `front_right_iso` (IoU 0.34 there) but the model matches it better from rear_right_iso (elevat

## Round 4 (verification, helper 2)
Blockers r3 59 -> r4 16 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `el_battery` (lipo_2s_350), `el_esc` (bbb_malenki_nano), `el_wesc` (bbb_brushless_esc_20a), `el_switch` (switch_slide_12x4), `weapon_motor` (bbb_be1806_2300kv), `lock_pin` (made)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `tail_cap`, `gyro_block`, `gyro_ring`, `spoke_h`, `spoke_v`, `foot_l`, `foot_r`, `tail_skid`
- 5 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- nose_hub: turns with weapon (rotates_with), kept uncut where it sits on it
- weapon drive: motor not coaxial, belt drive implied
- weapon: running-clearance well in bevel_hub not carved (it would open 166 mm2 of outside face)
- overlaps left: weapon/nose_hub 0.46
- no screw line found for bevel_gear
- spoke_h: 1 of 2 cuts dropped (they broke the solid: 2)
- hollowed chassis (wall 2.87, form 1): 116.2 -> 51.5 cm3
- hollowed gyro_block (wall 2.5, form 0): 14.3 -> 7.9 cm3
- hollowed bevel_gear (wall 2.5, form 0): 12.4 -> 8.1 cm3
- hollowed bevel_hub (wall 2.5, form 0): 3.6 -> 2.7 cm3
- bevel_gear: not touching the chassis, left undeclared
- bevel_hub: not touching the chassis, left undeclared
- nose_hub: not touching the chassis, left undeclared

Left (and why):
- proxy.interference x2: `weapon` and `nose_hub` overlap by 0.46 mm (allowed 0.08).
- proxy.sweep x5: joint `weapon`: `weapon` turning a full revolution may reach `nose_hub`.
- mfg.layer_load x1: `nose_hub` carries the `weapon` axle but is printed with build direction +z (world [0.0, 0.0, 1.0]), not along the spin axis [0.0, 1.0, 0.0]: impact load peels layers apart.
- combat.R051 x1: `weapon`: Weapon sweep above the floor is -22.36 mm (needs 0.3 mm).
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 2 routes vs 5 spec wires (missing ['w_sig_wesc', 'w_sw_esc', 'w_wm']); top.png: 2 routes vs 5 spec wires (missing ['w_sig_wesc', 'w_sw_esc', 'w_wm'])
- likeness.silhouette x3: looks, not in scope for this pass.
- likeness.view x1: looks, not in scope for this pass.
- retention.axial x1: `nose_hub` rotates but no fastener clamps or threads into it and it declares no reasoned press fit, pin, shaft or fuse hold.

Likeness (best silhouette IoU per photo, r3 -> r4): gyronino.aws72.webp 0.62 -> 0.62; gyronino.aws74.webp 0.6 -> 0.6; gyronino.aws76.webp 0.34 -> 0.34

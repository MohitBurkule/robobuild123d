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

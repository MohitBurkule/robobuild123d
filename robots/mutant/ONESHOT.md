# mutant: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Twin pods with 8 mm centre slot, thin vertical disc in the slot, wheels r 21 poking through the pod tops, grey front plates and clear ramp skirts.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| mutant.aws72.webp | 0.78 | 0.80 | vspin_drisk 0.74 | FAIL |
| mutant.aws74.webp | 0.83 | 0.80 | revron_ant 0.78 | ok |
| mutant.aws76.webp | 0.65 | 0.80 | wedge_2wd 0.64 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
aws76 is the newer white version with rounded pod noses (0.65); pods here are square. Top wheel windows and side fins missing; disc should be a curved hook blade.

## Missing tool / hint
Kit twin_pods has no rounded nose and no wheel windows; versions across years differ, a per-photo variant flag would help.

## Verdict
Looks alike: **yes**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Now a shuffler: wheels removed, leg cams poke through top windows, chamfered pods, wider slot with axle housing, longer skirts, side fins, switch.

Likeness: aws72 0.74 (FAIL), aws74 0.80 (ok), aws76 0.68 (FAIL).

## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type vertical_spinner; body twin_pods rect 76x134x38 mm, ramp 12; wheels 2 r21 inboard; weapon disc r21 axis x teeth 2.

Likeness: aws72 0.76 (FAIL), aws74 0.77 (FAIL), aws76 0.63 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body twin_pods rect 76x134x38 mm, ramp 12; wheels 2 r21 inboard; weapon disc r21 axis x teeth 2.

Likeness: aws72 0.76 (FAIL), aws74 0.72 (FAIL), aws76 0.49 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/mutant.aws76.webp` is declared `front` (IoU 0.49 there) but the model matches it better from rear_right_iso (elevation 45, azim

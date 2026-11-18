# wendsleydale: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Light-blue body with sloped front, centre lifter arm strip with a cylindrical hump (weapon kind lifter), clear side plates, orange corner blocks, 2 wheels r 14 at the rear between body and side plates.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| wendsleydale.aws65.webp | 0.34 | 0.80 | revron_ant 0.39 | FAIL |
| wendsleydale.aws68.webp | 0.75 | 0.80 | hspin_bar 0.80 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Only cluttered photos exist; aws65 (wood table) mask is poor so IoU 0.34 says little. Front slope is too long versus photo; arm in raised pose not modelled.

## Missing tool / hint
Photos have hands/wood/arena backgrounds: needs manual crop/mask tooling beyond --textured. Same likeness weapon.axis crash (axis dropped).

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Shorter steeper ramp, rounded tail, full-length lifter ridge with hump, orange blocks at all four corners. Axis restored.

Likeness: aws65 0.35 (FAIL), aws68 0.76 (FAIL).

## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 100x74x28 mm, ramp 40; wheels 2 r14 outboard; weapon none.

Likeness: aws65 0.35 (FAIL), aws68 0.76 (FAIL).

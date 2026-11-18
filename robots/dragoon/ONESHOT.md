# dragoon: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Blue box with centre slot, open ring disc (r 34, one tooth) offset left with black motor pod beside it, 2 wheels r 15 rear outside, 4 black forks on a front bar.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| dragoon.aws72.webp | 0.68 | 0.80 | revron 0.72 | FAIL |
| dragoon.aws74.webp | 0.75 | 0.80 | revron 0.78 | FAIL |
| dragoon.aws76.webp | 0.72 | 0.80 | wedge_2wd 0.70 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Photos show three fork setups (4 forks, 2 wedgelets, long tines); ring is higher/further forward in the real robot and pods are split; side polycarbonate plates missing.

## Missing tool / hint
Kit weapon is always centred on x and solid; needed manual ring + x offset.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Wider body with sloped side edges and disc slot, larger offset ring with one tooth, bigger motor pod, long angled forks, taller wheels, clear side plates.

Likeness: aws72 0.71 (FAIL), aws74 0.73 (FAIL), aws76 0.71 (FAIL).

## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 84x108x28 mm, ramp 0; wheels 2 r15 outboard; weapon disc r40 axis x teeth 1; 4 forks 50 mm.

Likeness: aws72 0.68 (FAIL), aws74 0.76 (FAIL), aws76 0.72 (FAIL).

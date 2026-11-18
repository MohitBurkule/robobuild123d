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

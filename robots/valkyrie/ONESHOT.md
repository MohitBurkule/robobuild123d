# valkyrie: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Flat 100 mm box with chamfered rear corners and clear top plate, two side cheeks carrying a full-width beater/drum (r 8, 80 wide) at the front with blue hubs; 2 wheels r 13 inboard at the rear. robot_type drum.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| valkyrie.aws71.webp | 0.74 | 0.80 | revron_ant 0.73 | FAIL |
| valkyrie.aws74.webp | 0.76 | 0.80 | wedge_2wd 0.80 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Model is too tall/short in the rear third (photo body is longer and flatter); wheels are buried in the solid body instead of showing in corner cut-outs; beater is a plain toothed cylinder, not the bolted bar/cage; no translucent lid look.

## Missing tool / hint
Kit has no 'inboard wheel in a corner notch' and no beater-bar weapon; a fit-photo for body length/height from iso masks would have fixed the proportions.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

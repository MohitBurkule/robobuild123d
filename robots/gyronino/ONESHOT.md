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

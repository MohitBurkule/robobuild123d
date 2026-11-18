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

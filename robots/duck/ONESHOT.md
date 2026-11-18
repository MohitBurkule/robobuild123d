# duck: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Orange wedge body with rounded-ish tail, white flipper panel on the slope (weapon kind flipper, hinge x), two blue rear hooks, steel front lip. 2 hidden wheels.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| duck_ling_.aws67.webp | 0.76 | 0.85 | revron_ant 0.85 | FAIL |
| duck_ling_.aws71.webp | 0.69 | 0.80 | vspin_drisk 0.78 | FAIL |
| duck_ling_.aws72.webp | 0.81 | 0.81 | wedge_2wd 0.81 | ok |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Photos show three different front ends (plain lip, forks, plate); only the plain lip is modelled so aws71 (forks) scores 0.69. Hooks are blocks not curved horns; body side walls are straight, real ones curve.

## Missing tool / hint
likeness crashed on REFERENCE weapon.axis for a non-spinner weapon (`p.joint.get` on an Obj) so axis was dropped from REFERENCE.json. Per-photo configuration variants are not expressible.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

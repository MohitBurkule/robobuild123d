# immovable_object: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Black box chassis, 4 red wheels (rear r 15, front r 11) outside, wide red front shield (112 wide, sloped) and 4 steel spikes.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| immovable_object.aws69.webp | 0.71 | 0.80 | revron 0.76 | FAIL |
| immovable_object.aws71.webp | 0.70 | 0.80 | wedge_2wd 0.77 | FAIL |
| immovable_object.aws72.webp | 0.72 | 0.80 | vspin_drisk 0.75 | FAIL |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Shield is a flat-topped extrusion, real one is arched in front view and curved; spikes are flat strips not barbed points; wheels lack spokes. Front third IoU 0.43-0.48.

## Missing tool / hint
Kit wheels share one radius; no arched shield primitive; forks cannot be pointed.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Arched shield (side profile intersected with a front arch), barbed arrow spikes, bigger spoked-hub wheels further outboard, top block.

Likeness: aws69 0.73 (FAIL), aws71 0.73 (FAIL), aws72 0.75 (FAIL).

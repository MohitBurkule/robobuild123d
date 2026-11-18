
## Tools I wanted
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 62x150x24 mm, ramp 10; wheels 4 r10 inboard; weapon none.

Likeness: aws71 0.83 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box rect 62x150x24 mm, ramp 10; wheels 4 r10 inboard; weapon none.

Likeness: aws71 0.83 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 62x150x22 mm, ramp 10; wheels 4 r14 inboard; weapon none.

Likeness: aws71 0.74 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/for_box_sake.aws71.webp` is declared `front` (IoU 0.74 there) but the model matches it better from front (elevation 45, azimuth

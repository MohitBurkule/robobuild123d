
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 85x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: lid; textured masks for indices [0].

Likeness: likeness crashed (see STRUGGLES).

## Round 2 (looks)
Decisions: type wedge; body box rect 85x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: lid.

Likeness: aws63 0.82 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 74x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon none; extra parts: lid.

Likeness: aws63 0.70 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/surprisefuthermucker.aws63.webp` is declared `front_left_iso` (IoU 0.70 there) but the model matches it better from front (elev

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type vertical_spinner; body box rect 74x58x26 mm, ramp 0; wheels 4 r13 outboard; weapon disc r17 axis x teeth 2; extra parts: lid.

Likeness: aws63 0.71 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/surprisefuthermucker.aws63.webp` is declared `front_right_iso` (IoU 0.71 there) but the model matches it better from front (ele

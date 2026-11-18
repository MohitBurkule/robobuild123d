
## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 80x84x30 mm, ramp 32; wheels 4 r10 outboard as treads; weapon none; 6 forks 36 mm; extra parts: lid.

Likeness: aws72 0.69 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box rect 80x84x30 mm, ramp 32; wheels 4 r10 outboard as treads; weapon none; 6 forks 46 mm; extra parts: lid.

Likeness: aws72 0.66 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 80x84x30 mm, ramp 32; wheels 4 r12 outboard; weapon none; 6 forks 34 mm; extra parts: lid.

Likeness: aws72 0.47 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/pingu.aws72.webp` is declared `front` (IoU 0.47 there) but the model matches it better from rear_right_iso (elevation 45, azimu

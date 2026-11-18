
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lifter_nose to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 95x66x24 mm, ramp 20; wheels 6 r12 outboard; weapon none; extra parts: lifter, lifter_nose.

Likeness: aws67 0.80 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 95x66x24 mm, ramp 20; wheels 6 r12 outboard; weapon none; extra parts: lifter, lifter_nose.

Likeness: aws67 0.80 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 95x66x24 mm, ramp 20; wheels 6 r12 outboard; weapon none; extra parts: lifter, lifter_nose.

Likeness: aws67 0.69 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/the_golden_nugget.aws67.webp` is declared `front_right_iso` (IoU 0.69 there) but the model matches it better from front_right_i


## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 72x70x24 mm, ramp 18; wheels 2 r16 outboard; weapon none; 2 forks 48 mm; extra parts: arm.

Likeness: aws71 0.59 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 72x70x24 mm, ramp 18; wheels 2 r16 outboard; weapon none; extra parts: arm, fork, post.

Likeness: aws71 0.55 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 72x70x24 mm, ramp 18; wheels 2 r16 outboard; weapon none; extra parts: arm, post, fork.

Likeness: aws71 0.47 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/vector.aws71.webp` is declared `front_left_iso` (IoU 0.47 there) but the model matches it better from front_right_iso (elevatio

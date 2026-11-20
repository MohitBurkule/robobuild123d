
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body twin_pods rect 100x104x26 mm, ramp 22; wheels 2 r13 inboard; weapon none; 2 forks 26 mm; extra parts: shovel.

Likeness: aws71 0.79 (FAIL), aws72 0.76 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body twin_pods rect 100x104x26 mm, ramp 22; wheels 2 r13 inboard; weapon none; 2 forks 26 mm; extra parts: shovel.

Likeness: aws71 0.79 (FAIL), aws72 0.76 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body twin_pods rect 100x104x26 mm, ramp 22; wheels 2 r16 inboard; weapon none; 2 forks 34 mm; extra parts: shovel.

Likeness: aws71 0.37 (FAIL), aws72 0.19 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/shoveron.aws71.webp` is declared `front` (IoU 0.37 there) but the model matches it better from rear_left_iso (elevation 45, azi; [FAIL] likeness.view: `reference/shoveron.aws72.webp` is declared `front` (IoU 0.19 there) but the model matches it better from front (elevation 25, azimuth 90)

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type lifter; body twin_pods rect 100x104x26 mm, ramp 22; wheels 2 r16 inboard; weapon none; 2 forks 34 mm; extra parts: shovel; photos skipped (cluttered): indices [1].

Likeness: aws71 0.72 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/shoveron.aws71.webp` is declared `front_left_iso` (IoU 0.72 there) but the model matches it better from rear_left_iso (elevatio

# elevron_red: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box pentagon 90x92x26 mm, ramp 25; wheels 2 r13 inboard; weapon none; 2 forks 30 mm; extra parts: lift_arm, pod.

Likeness: aws72 0.70 (FAIL), aws74 0.70 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends pod to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box pentagon 92x78x20 mm, ramp 22; wheels 2 r13 inboard; weapon none; 2 forks 30 mm; extra parts: lift_arm, pod.

Likeness: aws72 0.69 (FAIL), aws74 0.64 (FAIL).

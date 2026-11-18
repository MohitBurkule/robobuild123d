# rbmk: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type horizontal_spinner; body box pentagon 70x80x30 mm, ramp 0; wheels 2 r11 inboard; weapon bar r34 axis z teeth 2; extra parts: bar2, motor.

Likeness: aws71 0.64 (FAIL), aws74 0.63 (FAIL), aws76 0.73 (FAIL).

## Tools I wanted
- Kit weapon kind `bar` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends motor, skid to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type horizontal_spinner; body box pentagon 75x84x34 mm, ramp 0; wheels 2 r14 outboard; weapon bar r46 axis z teeth 2; extra parts: bar2, motor, skid.

Likeness: aws71 0.66 (FAIL), aws74 0.60 (FAIL), aws76 0.72 (FAIL).

# pyro: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type vertical_spinner; body twin_pods rect 90x112x36 mm, ramp 35; wheels 2 r13 outboard; weapon disc r44 axis x teeth 2; 2 forks 24 mm; extra parts: motor, upright.

Likeness: aws71 0.76 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends motor, upright to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type vertical_spinner; body twin_pods rect 90x112x36 mm, ramp 35; wheels 2 r13 outboard; weapon disc r44 axis x teeth 2; 2 forks 24 mm; extra parts: motor, upright.

Likeness: aws71 0.72 (FAIL).

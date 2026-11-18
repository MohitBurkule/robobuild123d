# counterinsurgency: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 50x120x14 mm, ramp 0; wheels 2 r9 inboard; weapon none; 3 forks 36 mm; extra parts: side_arm.

Likeness: aws76 0.67 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends side_arm to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 50x120x14 mm, ramp 0; wheels 2 r9 inboard; weapon none; 3 forks 36 mm; extra parts: side_arm.

Likeness: aws76 0.61 (FAIL).

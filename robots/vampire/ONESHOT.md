# vampire: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type horizontal_spinner; body box rect 100x112x22 mm, ramp 0; wheels 2 r11 inboard; weapon bar r64 axis z teeth 2; extra parts: hub.

Likeness: aws71 0.66 (FAIL), aws74 0.72 (FAIL), aws76 0.56 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends hub to the kit spec. ~2 min per robot plus the script.
- Body side-profile / plan polygon keys. Did instead: replaced the chassis shape in the generator. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type horizontal_spinner; body box rect 100x112x28 mm, ramp 0; wheels 2 r11 inboard; weapon bar r64 axis z teeth 2; extra parts: hub.

Likeness: aws71 0.64 (FAIL), aws74 0.71 (FAIL), aws76 0.52 (FAIL).

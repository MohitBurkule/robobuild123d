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

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type horizontal_spinner; body box rect 100x112x28 mm, ramp 0; wheels 2 r14 inboard; weapon bar r64 axis z teeth 2; extra parts: hub.

Likeness: aws71 0.46 (FAIL), aws74 0.50 (FAIL), aws76 0.44 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/vampire.aws71.webp` is declared `top` (IoU 0.46 there) but the model matches it better from rear_left_iso (elevation 25, azimut; [FAIL] likeness.view: `reference/vampire.aws74.webp` is declared `front_right_iso` (IoU 0.50 there) but the model matches it better from rear_right_iso (elevati; [FAIL] likeness.view: `reference/vampire.aws76.webp` is declared `left` (IoU 0.44 there) but the model matches it better from front (elevation 25, azimuth 90) (

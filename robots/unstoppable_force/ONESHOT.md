# unstoppable_force: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type drum; body box round_nose 100x100x30 mm, ramp 0; wheels 2 r17 inboard; weapon drum r14 axis x teeth 2; extra parts: drum_arm.

Likeness: aws69 0.86 (ok), aws71 0.90 (ok), aws72 0.88 (ok).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends drum_arm to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type drum; body box round_nose 100x100x30 mm, ramp 0; wheels 2 r17 inboard; weapon drum r14 axis x teeth 2; extra parts: drum_arm.

Likeness: aws69 0.86 (ok), aws71 0.90 (ok), aws72 0.88 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type drum; body box round_nose 100x100x30 mm, ramp 0; wheels 2 r17 inboard; weapon drum r14 axis x teeth 2; extra parts: drum_arm.

Likeness: aws69 0.81 (ok), aws71 0.71 (FAIL), aws72 0.80 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/unstoppable_force.aws71.webp` is declared `front_left_iso` (IoU 0.71 there) but the model matches it better from front_left_iso; [FAIL] likeness.view: `reference/unstoppable_force.aws72.webp` is declared `front_left_iso` (IoU 0.80 there) but the model matches it better from front_right_is

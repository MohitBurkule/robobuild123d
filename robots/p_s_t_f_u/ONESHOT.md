# p_s_t_f_u: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 80x112x26 mm, ramp 28; wheels 2 r10 inboard; weapon none; extra parts: rail.

Likeness: aws69 0.83 (ok).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends rail to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 80x112x26 mm, ramp 28; wheels 2 r10 inboard; weapon none; extra parts: rail.

Likeness: aws69 0.83 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 80x112x20 mm, ramp 22; wheels 4 r11 inboard; weapon none; extra parts: rail, front_plate.

Likeness: aws69 0.76 (FAIL).

# trappist_1: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 70x112x20 mm, ramp 0; wheels 4 r9 inboard; weapon none; extra parts: wire, wire_x, front_bar; textured masks for indices [0].

Likeness: aws63 0.78 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends wire_x, front_bar to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 70x112x20 mm, ramp 0; wheels 4 r9 inboard; weapon none; extra parts: wire, wire_x, front_bar; textured masks for indices [0].

Likeness: aws63 0.78 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 70x112x20 mm, ramp 0; wheels 4 r9 inboard; weapon none; extra parts: wire, wire_x, front_bar; textured masks for indices [0].

Likeness: aws63 0.00 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/trappist_1.aws63.webp` is declared `rear` (IoU 0.00 there) but the model matches it better from front (elevation 45, azimuth 90

# sawcon: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type vertical_spinner; body twin_pods rect 90x96x22 mm, ramp 0; wheels 4 r11 outboard; weapon disc r18 axis x teeth 8; extra parts: arm, plow, plow_face; photos skipped (cluttered): indices [0, 2].

Likeness: aws67 0.80 (ok).

## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (plow, plow_face), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends arm to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type vertical_spinner; body twin_pods rect 90x96x22 mm, ramp 0; wheels 4 r11 outboard; weapon disc r18 axis x teeth 8; extra parts: arm, plow, plow_face; photos skipped (cluttered): indices [0, 2].

Likeness: aws67 0.80 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body twin_pods rect 90x96x22 mm, ramp 0; wheels 4 r11 outboard; weapon disc r17 axis x teeth 8; extra parts: plow, plow_face, arm; photos skipped (cluttered): indices [0, 2].

Likeness: aws67 0.75 (FAIL).

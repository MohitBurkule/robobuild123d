# my_first_bot: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 105x100x36 mm, ramp 95; wheels 2 r10 inboard; weapon none; extra parts: eye_l, eye_r, post, post_top; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok), aws71 0.84 (ok).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends eye_l, eye_r, post, post_top to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 105x100x36 mm, ramp 95; wheels 2 r10 inboard; weapon none; extra parts: eye_l, eye_r, post, post_top; photos skipped (cluttered): indices [0].

Likeness: aws67 0.87 (ok), aws71 0.84 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 105x100x36 mm, ramp 95; wheels 2 r10 inboard; weapon none; extra parts: eye_l, eye_r, post, post_top; photos skipped (cluttered): indices [0].

Likeness: aws67 0.75 (FAIL), aws71 0.46 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/my_first_bot.aws67.webp` is declared `front_left_iso` (IoU 0.75 there) but the model matches it better from rear_right_iso (ele; [FAIL] likeness.view: `reference/my_first_bot.aws71.webp` is declared `front` (IoU 0.46 there) but the model matches it better from rear_left_iso (elevation 45,

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **65 -> 10** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): my_first_bot.aws67.webp 0.75 -> 0.75, my_first_bot.aws71.webp 0.46 -> 0.46

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- chassis: hollowed (box wall round pockets), 189724 -> 82102 mm3
- hollow failed on eye_l: [('cav', 'geometry failed: ValueError: Cannot tessellate an empty shape')]
- hollow failed on eye_r: [('cav', 'geometry failed: ValueError: Cannot tessellate an empty shape')]
- post: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- post_top: does not sit in any print part (no overlap to cut a seat from); left without a declared joint

Left (one line each):
- integrity.solids x2: tessellation of round/revolved shapes (open pole shells) or a boolean in the kit shape
- connection.floating x2: part does not touch the print anywhere (kit geometry); no honest joint to declare
- likeness.view x2: looks (photo view label; not part of this pass)
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- proxy.interference x1: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes

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

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **89 -> 8** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): sawcon.aws67.webp 0.750 -> 0.751

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- plow_face: hidden 3 mm key into pod_l (one print)
- arm: hidden 3 mm key into bridge (one print)
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- dt_axle_wheel_l1 replaced by the gearmotor shaft
- dt_axle_wheel_r1 replaced by the gearmotor shaft
- weapon: no room for a weapon motor inside the print; weapon.motor left empty
- pod_l: hollowed (box wall round pockets), 58608 -> 41058 mm3
- pod_r: hollowed (box wall round pockets), 69104 -> 35964 mm3
- bridge: hollowed (exact wall round pockets), 8910 -> 5102 mm3
- plow_face: hollowed (exact wall round pockets), 18969 -> 14234 mm3 (9 thin spots kept solid)
- arm: hollowed (exact wall round pockets), 10758 -> 7268 mm3

Left (one line each):
- connection.floating x3: part does not touch the print anywhere (kit geometry); no honest joint to declare
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- power.weapon_motor x1: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- process.geometry x1: kit weapon shape is not a pure 2D/3-axis profile for its process (look)
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

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

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **51 -> 11** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): vampire.aws71.webp 0.51 -> 0.47, vampire.aws74.webp 0.53 -> 0.49, vampire.aws76.webp 0.40 -> 0.44

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- chassis: kit cut-outs removed (owner request)
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- chassis: hollowed (box wall round pockets), 233340 -> 96724 mm3
- dt_hubw_weapon: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- hub: printed with the weapon axis as build direction

Left (one line each):
- likeness.view x3: looks (photo view label; not part of this pass)
- likeness.silhouette x3: looks (not part of this pass; outside shape kept as round 3)
- proxy.sweep x2: moving part runs into the chassis more than a running clearance can take without changing the look
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- proxy.interference x1: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes

# pyro: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type vertical_spinner; body twin_pods rect 90x112x36 mm, ramp 35; wheels 2 r13 outboard; weapon disc r44 axis x teeth 2; 2 forks 24 mm; extra parts: motor, upright.

Likeness: aws71 0.76 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends motor, upright to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type vertical_spinner; body twin_pods rect 90x112x36 mm, ramp 35; wheels 2 r13 outboard; weapon disc r44 axis x teeth 2; 2 forks 24 mm; extra parts: motor, upright.

Likeness: aws71 0.72 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body twin_pods rect 90x112x36 mm, ramp 35; wheels 2 r13 outboard; weapon disc r40 axis x teeth 2; 2 forks 24 mm; extra parts: motor, upright.

Likeness: aws71 0.65 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/pyro.aws71.webp` is declared `front_right_iso` (IoU 0.65 there) but the model matches it better from front_right_iso (elevation

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **78 -> 10** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): pyro.aws71.webp 0.652 -> 0.653

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- weapon: weapon motor not coaxial (no room on the axis): placed parallel to the axis in the print, belt drive NOT modelled
- weapon: rotor overlaps bridge 8 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- weapon: rotor overlaps motor 10 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- upright_l: cuts split it into 2 pieces, each joined to the print
- motor: trimmed where it overlapped pod_r (same print)
- motor: trimmed where it overlapped upright_l (same print)
- pod_l: hollowed (box wall round pockets), 107122 -> 51616 mm3
- pod_r: hollowed (box wall round pockets), 121790 -> 42715 mm3
- bridge: hollowed (exact wall round pockets), 12780 -> 7076 mm3
- motor: hollowed (exact wall round pockets), 8484 -> 6521 mm3 (12 thin spots kept solid)

Left (one line each):
- proxy.sweep x4: moving part runs into the chassis more than a running clearance can take without changing the look
- proxy.interference x2: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

# goobers: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type wedge; body box rect 62x76x28 mm, ramp 52; wheels 2 r15 outboard; weapon none; extra parts: ear; clusterbot, one of 4 modelled (count read from photos, unsure).

Likeness: aws71 0.77 (FAIL), aws72 0.76 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends ear to the kit spec. ~2 min per robot plus the script.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `cluster` in kit.json and a way to confirm the bot count. Did instead: guessed N from the photos.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type wedge; body box rect 62x76x28 mm, ramp 52; wheels 2 r15 outboard; weapon none; extra parts: ear; clusterbot, one of 4 modelled (count read from photos, unsure).

Likeness: aws71 0.80 (FAIL), aws72 0.74 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 62x76x28 mm, ramp 56; wheels 2 r17 outboard; weapon none; extra parts: ear; clusterbot, one of 4 modelled (count read from photos, unsure).

Likeness: aws71 0.81 (ok), aws72 0.66 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/goobers.aws72.webp` is declared `front` (IoU 0.66 there) but the model matches it better from front_right_iso (elevation 45, az

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **38 -> 9** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): goobers.aws71.webp 0.808 -> 0.802, goobers.aws72.webp 0.659 -> 0.656

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (0 of 4 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- el_battery: no free pocket inside the print; placed at the chassis centre (overlaps)
- el_battery: pocket wall only 0 mm
- chassis: hollowed (box wall round pockets), 63217 -> 38770 mm3

Left (one line each):
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- proxy.interference x1: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- connection.tape_overload x1: see verify_r4.txt root causes
- fit.interference x1: catalog part pocket overlaps another body
- wire.render_wires x1: a robot render does not draw every wire: at least one wire has no route through the print
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)
- wire.outside x1: see verify_r4.txt root causes
- battery.armour_gap x1: see verify_r4.txt root causes

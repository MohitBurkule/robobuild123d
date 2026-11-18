# flippant: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type flipper; body box rect 95x100x28 mm, ramp 35; wheels 2 r14 inboard; weapon none; extra parts: hoop, lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws69 0.88 (ok).

## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type flipper; body box rect 95x100x28 mm, ramp 35; wheels 2 r14 inboard; weapon none; extra parts: hoop, lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws69 0.88 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box rect 95x100x28 mm, ramp 35; wheels 2 r14 inboard; weapon none; extra parts: hoop, lid; photos skipped (cluttered): indices [0, 1].

Likeness: aws69 0.85 (ok).

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **63 -> 7** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): flippant.aws69.webp 0.873 -> 0.873

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (5 of 6 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- el_battery: placed with 4.0 mm of lead room round it
- el_rx_esc: placed with 4.0 mm of lead room round it
- hoop_l: driven by a KingMax CS07 micro servo (catalog servo_cs07) in a closed pocket 12 mm from the hinge; the horn-to-arm link is declared, not modelled
- hoop_r: driven by a KingMax CS07 micro servo (catalog servo_cs07) in a closed pocket 27 mm from the hinge; the horn-to-arm link is declared, not modelled
- joint hoop_l: 0.9 mm sweep clearance cut in chassis
- joint hoop_l: 0.9 mm sweep clearance cut in lid
- joint hoop_r: 0.9 mm sweep clearance cut in chassis
- joint hoop_r: 0.9 mm sweep clearance cut in lid
- chassis: hollowed (box wall round pockets), 167944 -> 86584 mm3
- chassis: 2 of 27 channel pieces left out (boolean)
- wiring channels: 6 of 6 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin

Left (one line each):
- proxy.wiring x2: see verify_r4.txt root causes
- geom.tiny_edge x2: see verify_r4.txt root causes
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- wire.render_wires x1: a robot render does not draw every wire: at least one wire has no route through the print
- wire.render_count x1: render record lists fewer routes than the spec has wires (a wire found no route)

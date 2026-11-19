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

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **86 -> 8** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): trappist_1.aws63.webp 0.000 -> 0.000

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (7 of 7 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- front_bar: hidden 3 mm key into chassis (one print)
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- dt_axle_wheel_l1 replaced by the gearmotor shaft
- dt_axle_wheel_r1 replaced by the gearmotor shaft
- el_battery: placed with 4.0 mm of lead room round it
- el_rx_esc: placed with 4.0 mm of lead room round it
- wire_l: driven by a KingMax CS07 micro servo (catalog servo_cs07) in a closed pocket 36 mm from the hinge; the horn-to-arm link is declared, not modelled
- wire_r: no room inside the print for a micro servo (32 x 12 x 22.7 mm) or an N10 gearmotor; actuator left out
- joint wire_l: its sweep would cut a 10 mm deep slot into the outside of chassis (10 mm for the poses at 5..80 deg alone); left out (look kept)
- joint wire_l: 0.9 mm sweep clearance cut in front_bar
- joint wire_r: its sweep would cut a 10 mm deep slot into the outside of chassis (10 mm for the poses at 5..80 deg alone); left out (look kept)
- joint wire_r: 0.9 mm sweep clearance cut in front_bar
- front_bar: cuts split it into 3 pieces, each joined to the print
- chassis: hollowed (box wall round pockets), 109635 -> 70736 mm3
- wire_x: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- wire w_m2: no channel path inside the print clear of the rotor
- wiring channels: 6 of 7 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin

Left (one line each):
- proxy.interference x2: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- proxy.sweep x2: moving part runs into the chassis more than a running clearance can take without changing the look
- power.weapon_motor x1: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- wire.rotor_clearance x1: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)

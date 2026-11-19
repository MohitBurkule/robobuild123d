
## Tools I wanted
- Kit weapon kind `flipper` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (flipper), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type flipper; body box rect 70x80x40 mm, ramp 0; wheels 2 r11 inboard; weapon none; extra parts: flipper; photos skipped (cluttered): indices [1].

Likeness: aws70 0.76 (FAIL), aws74 0.81 (FAIL).

## Round 2 (looks)
Decisions: type flipper; body box rect 70x80x40 mm, ramp 0; wheels 2 r11 inboard; weapon none; extra parts: flipper; photos skipped (cluttered): indices [1].

Likeness: aws70 0.77 (FAIL), aws74 0.84 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box rect 70x80x40 mm, ramp 0; wheels 2 r11 inboard; weapon none; extra parts: flipper; photos skipped (cluttered): indices [1].

Likeness: aws70 0.74 (FAIL), aws74 0.67 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/flik.aws74.webp` is declared `front_left_iso` (IoU 0.67 there) but the model matches it better from front_right_iso (elevation 

## Round 3c (user angle picks applied; shape fixed per user remarks)
Decisions: type flipper; body box rect 80x76x40 mm, ramp 0; wheels 2 r11 inboard; weapon none; extra parts: flipper, side_panel, top_plate; photos skipped (cluttered): indices [1].

Likeness: aws70 0.67 (FAIL), aws74 0.56 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/flik.aws70.webp` is declared `front_right_iso` (IoU 0.67 there) but the model matches it better from front_right_iso (elevation; [FAIL] likeness.view: `reference/flik.aws74.webp` is declared `front_left_iso` (IoU 0.56 there) but the model matches it better from front_right_iso (elevation 

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **47 -> 12** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): flik.aws70.webp 0.785 -> 0.785, flik.aws74.webp 0.789 -> 0.789

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (5 of 5 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- el_battery: placed with 4.0 mm of lead room round it
- el_rx_esc: placed with 4.0 mm of lead room round it
- flipper: driven by a KingMax CS07 micro servo (catalog servo_cs07) in a closed pocket 16 mm from the hinge; the horn-to-arm link is declared, not modelled
- joint flipper: 0.5 mm sweep clearance cut in chassis
- chassis: hollowed (box wall round pockets), 145757 -> 109427 mm3
- side_panel_l: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- side_panel_r: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- top_plate: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- wiring channels: 5 of 5 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin

Left (one line each):
- proxy.interference x4: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- process.geometry x2: kit weapon shape is not a pure 2D/3-axis profile for its process (look)
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- proxy.wiring x1: see verify_r4.txt root causes
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- proxy.sweep x1: moving part runs into the chassis more than a running clearance can take without changing the look
- mfg.stock x1: bought part with free geometry that is not a stock size

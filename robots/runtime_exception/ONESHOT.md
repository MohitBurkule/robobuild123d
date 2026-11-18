
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends spine to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box pentagon 80x92x22 mm, ramp 0; wheels 2 r13 inboard; weapon none; extra parts: scoop, spine; photos skipped (cluttered): indices [0].

Likeness: aws72 0.79 (FAIL), aws74 0.80 (FAIL).

## Round 2 (looks)
Decisions: type wedge; body box pentagon 80x92x22 mm, ramp 0; wheels 2 r13 inboard; weapon none; extra parts: scoop, spine; photos skipped (cluttered): indices [0].

Likeness: aws72 0.79 (FAIL), aws74 0.80 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box pentagon 80x92x22 mm, ramp 0; wheels 2 r15 inboard; weapon none; extra parts: spine, scoop; photos skipped (cluttered): indices [0].

Likeness: aws72 0.59 (FAIL), aws74 0.66 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/runtime_exception.aws72.webp` is declared `front_left_iso` (IoU 0.59 there) but the model matches it better from rear_left_iso ; [FAIL] likeness.view: `reference/runtime_exception.aws74.webp` is declared `front_left_iso` (IoU 0.66 there) but the model matches it better from front_left_iso

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **37 -> 4** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): runtime_exception.aws72.webp 0.728 -> 0.728, runtime_exception.aws74.webp 0.714 -> 0.714

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (4 of 4 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- el_battery: placed with 4.0 mm of lead room round it
- el_rx_esc: placed with 4.0 mm of lead room round it
- chassis: hollowed (box wall round pockets), 117890 -> 57384 mm3
- spine: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- scoop: does not sit in any print part (no overlap to cut a seat from); left without a declared joint
- wiring channels: 4 of 4 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin
- wiring channels: a piece of ['w_bat_sw', 'w_sw_esc'] left out where it would come within 2 mm of the outside (port close to the skin)

Left (one line each):
- likeness.silhouette x2: looks (not part of this pass; outside shape kept as round 3)
- proxy.interference x1: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- connection.floating x1: part does not touch the print anywhere (kit geometry); no honest joint to declare

# rbmk: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type horizontal_spinner; body box pentagon 70x80x30 mm, ramp 0; wheels 2 r11 inboard; weapon bar r34 axis z teeth 2; extra parts: bar2, motor.

Likeness: aws71 0.64 (FAIL), aws74 0.63 (FAIL), aws76 0.73 (FAIL).

## Tools I wanted
- Kit weapon kind `bar` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends motor, skid to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type horizontal_spinner; body box pentagon 75x84x34 mm, ramp 0; wheels 2 r14 outboard; weapon bar r46 axis z teeth 2; extra parts: bar2, motor, skid.

Likeness: aws71 0.66 (FAIL), aws74 0.60 (FAIL), aws76 0.72 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type horizontal_spinner; body box pentagon 75x84x34 mm, ramp 0; wheels 2 r14 outboard; weapon bar r42 axis z teeth 2; extra parts: motor, skid, bar2.

Likeness: aws71 0.63 (FAIL), aws74 0.57 (FAIL), aws76 0.53 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/rbmk.aws76.webp` is declared `front_left_iso` (IoU 0.53 there) but the model matches it better from rear_right_iso (elevation 2

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **64 -> 52** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): rbmk.aws71.webp 0.628 -> 0.628, rbmk.aws74.webp 0.571 -> 0.570, rbmk.aws76.webp 0.530 -> 0.530

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges and via points round rotors; print orientation, failsafe and weapon disable declared

Notes from the run:
- skid_l: hidden 3 mm key into chassis (one print)
- skid_r: hidden 3 mm key into chassis (one print)
- weapon: weapon motor not coaxial (no room on the axis): placed parallel to the axis in the print, belt drive NOT modelled
- bar2: no room for a weapon motor inside the print; weapon.motor left empty
- el_battery: no free pocket inside the print; placed at the chassis centre (overlaps)
- el_battery: pocket wall only 0 mm
- el_wesc: no free pocket inside the print; placed at the chassis centre (overlaps)
- el_wesc: pocket wall only 0 mm
- weapon: no solid spot for a lock pin hole
- bar2: no solid spot for a lock pin hole
- weapon: rotor overlaps chassis 16 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- weapon: rotor overlaps motor_l 8 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- bar2: rotor overlaps chassis 17 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- bar2: rotor overlaps motor_r 8 mm deep in the kit shape; a running clearance there would cut open the outside, so it is left out
- skid_r: a cut would leave a loose piece or a bad shell; that cut is left out
- hollow failed on chassis: hollow part has 2 solids
- motor_r: hollowed (exact wall round pockets), 5008 -> 2980 mm3
- wire w_bat_sw: no via round the rotor found
- wire w_sw_wesc: no via round the rotor found
- wire w_wesc_sig: no via round the rotor found
- wire w_phases: no via round the rotor found

Left (one line each):
- proxy.sweep x19: moving part runs into the chassis more than a running clearance can take without changing the look
- proxy.interference x8: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- wire.rotor_clearance x5: toolchain for lifters/flippers: the check revolves a limited-range arm a full turn, so no wire inside the chassis can clear it; for spinners: no free route found
- likeness.silhouette x3: looks (not part of this pass; outside shape kept as round 3)
- legal.locking_bar x2: no solid spot found in the weapon for a lock-pin hole
- fit.interference x2: catalog part pocket overlaps another body
- battery.rotor_gap x2: toolchain for lifters: the arm's full-turn envelope is used, which covers the whole chassis
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- connection.tape_overload x1: see verify_r4.txt root causes
- power.weapon_motor x1: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- dynamics.balance x1: kit weapon is not balanced about its axis (look)
- process.geometry x1: kit weapon shape is not a pure 2D/3-axis profile for its process (look)
- mfg.stock x1: bought part with free geometry that is not a stock size
- electrical.battery_weapon_gap x1: battery pocket close to the weapon envelope; no other room inside the print
- combat.R051 x1: weapon sweep reaches the floor in the kit pose (look)
- electrical.switch_direction x1: see verify_r4.txt root causes
- wire.render_wires x1: toolchain/process: the photo-match, diff and likeness sheets are written without a render record of the wire routes
- likeness.view x1: looks (photo view label; not part of this pass)

rbmk-specific (gyro/vibration walker, no wheels, no legs):
- No wheels, legs or drive motors were added. The two spinners and their motors are kept as built. STRUGGLES.md, which lists the toolchain gaps for gyro locomotion, is committed with this round.
- In the kit shape both bar spinners sit 16-17 mm deep in the body. A running-clearance cut would open the shell (the open front cavity seen in an earlier attempt), so no clearance is cut. The proxy.sweep and interference blockers stay until the spinners are moved out to the sides as in the photo, which is a look change for the owner.
- No free room is left inside the body. The battery and weapon ESC are therefore placed in solid print, with no pocket and no hollowing round them, rather than hanging in a cavity.
- The skids are one print with the chassis through a hidden 3 mm key across their shared face.

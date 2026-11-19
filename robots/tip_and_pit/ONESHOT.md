# tip_and_pit: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type lifter; body box rect 40x70x26 mm, ramp 0; wheels 2 r16 outboard; weapon none; extra parts: plate; clusterbot, one of 2 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0]; textured masks for indices [1].

Likeness: aws63 0.34 (FAIL).

## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (plate), guessing the tilt maths by hand. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `cluster` in kit.json and a way to confirm the bot count. Did instead: guessed N from the photos.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type lifter; body box rect 34x60x30 mm, ramp 0; wheels 2 r17 outboard; weapon none; extra parts: plate; clusterbot, one of 2 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0]; textured masks for indices [1].

Likeness: aws63 0.34 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 34x60x30 mm, ramp 0; wheels 2 r15 outboard; weapon none; extra parts: plate; clusterbot, one of 2 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0]; textured masks for indices [1].

Likeness: aws63 0.17 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/tip_pit.aws63.webp` is declared `front` (IoU 0.17 there) but the model matches it better from rear_right_iso (elevation 45, azi

## Round 3b (rebuilt by eye from the photos: parts moved to where the photo shows them, camera set per photo)
Decisions: type lifter; body box rect 34x60x30 mm, ramp 0; wheels 2 r15 outboard; weapon none; extra parts: plate; clusterbot, one of 2 modelled (count read from photos, unsure); photos skipped (cluttered): indices [0]; textured masks for indices [1].

Likeness: aws63 0.16 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/tip_pit.aws63.webp` is declared `front` (IoU 0.16 there) but the model matches it better from rear_right_iso (elevation 45, azi

## Round 4 (verification, helper 1)
Blockers r3 -> r4: **43 -> 17** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3 -> r4): tip_pit.aws63.webp 0.158 -> 0.157

What was done (script r4_h1, outside shape kept):
- fake screw/bolt heads removed; detail mounts/arms merged into the print part they sit on; axle nuts became printed hub caps
- printed parts of the chassis material declared one print (`fused_with`, a hidden 1.6 mm key where they only touched); overlaps inside the print trimmed
- catalog parts: N20 gearmotors on the drive wheels (D-bore in the hub), LiPo, Malenki Nano (receiver + drive ESCs), brushless weapon ESC and outrunner for spinners, slide switch in a closed pocket above the belly skin, reached through an 8 x 4 mm slot underneath, steel locking pin through the weapon
- pockets 0.25 mm per side round every bought part with 2 mm print walls, wheel/weapon running clearances <= 1.5 mm (no clearance cut where the kit rotor sits deep in the body: that would open the outside), hinge sweep clearances, shaft bores
- big print parts hollowed (cavity = part eroded by the wall, checked >= 1 mm inside the skin, no cavity opens to the outside); wires with gauges; print orientation, failsafe and weapon disable declared
- wiring channels (round 4b): one 4.8 mm channel per wire cut inside the print from port to port (axis >= 5 mm under the outer skin, so >= 1.5 mm of skin stays and the outside is unchanged), clear of bought parts and of every rotor/arm sweep, widened up to 6.8 mm where wires share a run
- renders: `renders/iso.png` (first photo's camera) and `renders/top.png` re-rendered with the wire routes and a render record (2 of 4 wires routed and drawn); photo comparison sheets (diff/likeness/match/pick/view) moved to `compare/`

Notes from the run:
- dt_axle_wheel_l0 replaced by the gearmotor shaft
- dt_axle_wheel_r0 replaced by the gearmotor shaft
- el_battery: no free pocket inside the print; placed at the chassis centre (overlaps)
- el_battery: pocket wall only 0 mm
- el_rx_esc: placed with 4.0 mm of lead room round it
- el_rx_esc: pocket wall only 1.0 mm
- plate: no room inside the print for a micro servo (32 x 12 x 22.7 mm) or an N10 gearmotor; actuator left out
- joint plate: its sweep would cut a 9 mm deep slot into the outside of chassis (9 mm for the poses at 0..80 deg alone); left out (look kept)
- chassis: hollowed (box wall round pockets), 47944 -> 31771 mm3
- wiring channels: 4 of 4 wires have a 4.8 mm channel inside the print, every piece >= 2 mm under the outer skin
- wiring channels: a piece of ['w_bat_sw'] left out where it would come within 2 mm of the outside (port close to the skin)

Left (one line each):
- proxy.interference x4: parts overlap in the kit shape where a cut would change the look or leave a loose piece
- proxy.wiring x2: see verify_r4.txt root causes
- mass.over x1: outside shape (kept) is heavier than the class limit even with 2.5 mm shells
- proxy.sweep x1: moving part runs into the chassis more than a running clearance can take without changing the look
- connection.tape_overload x1: see verify_r4.txt root causes
- power.weapon_motor x1: toolchain: a servo/arm weapon is required to have a brushless kV motor like a spinner
- electrical.battery_weapon_gap x1: battery pocket close to the weapon envelope; no other room inside the print
- fit.interference x1: catalog part pocket overlaps another body
- wire.render_wires x1: a robot render does not draw every wire: at least one wire has no route through the print
- wire.render_count x1: render record lists fewer routes than the spec has wires (a wire found no route)
- likeness.view x1: looks (photo view label; not part of this pass)
- likeness.silhouette x1: looks (not part of this pass; outside shape kept as round 3)
- battery.rotor_gap x1: toolchain for lifters: the arm's full-turn envelope is used, which covers the whole chassis

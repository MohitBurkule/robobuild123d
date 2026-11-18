
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends claw to the kit spec. ~2 min per robot plus the script.
- Body side-profile / plan polygon keys. Did instead: replaced the chassis shape in the generator. ~3 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 80x70x32 mm, ramp 0; wheels 2 r14 outboard; weapon none; extra parts: roller, claw; photos skipped (cluttered): indices [1].

Likeness: aws71 0.71 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 80x70x32 mm, ramp 0; wheels 2 r16 outboard; weapon none; extra parts: roller, claw; photos skipped (cluttered): indices [1].

Likeness: aws71 0.68 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 80x70x32 mm, ramp 0; wheels 2 r16 outboard; weapon none; extra parts: roller, claw; photos skipped (cluttered): indices [1].

Likeness: aws71 0.68 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 46 -> r4 6 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `claw_l`, `claw_r`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- roller sweeps through chassis at 41 poses: not carved (would change the outside)
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 151 g over 150: walls 2 mm -> 144 g
- hollowed chassis (wall 2, form 0): 148.4 -> 56.7 cm3
- hollowed claw_l (wall 2, form 0): 4.8 -> 3.8 cm3
- hollowed claw_r (wall 2, form 0): 4.8 -> 3.8 cm3

Left (and why):
- proxy.sweep x1: joint `roller`: `roller` hits `chassis` 0.12 mm deep at 7.3 (declared range 0..80; allowed 0.08). `robot probe spec.json --joint roller` lists the closest approach to every part.
- power.weapon_motor x1: toolchain: lifters/flippers are servo or gear driven; the check wants a brushless kV for every weapon.
- process.weapon_printed x1: toolchain: a printed lifter/flipper arm is judged like a spinner (needs hardened teeth); adding metal teeth changes the look.
- electrical.battery_weapon_gap x1: toolchain: a limited-range arm is judged as a full revolution about its pivot; that cylinder covers the whole chassis.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): tritongue.aws71.webp 0.68 -> 0.68

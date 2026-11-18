
## Tools I wanted
- Kit weapon kind `axe` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends gear to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type other; body box pentagon 100x110x30 mm, ramp 30; wheels 2 r12 inboard; weapon none; extra parts: arm, gear; photos skipped (cluttered): indices [0, 2].

Likeness: aws67 0.84 (ok).

## Round 2 (looks)
Decisions: type other; body box pentagon 100x110x30 mm, ramp 30; wheels 2 r12 inboard; weapon none; extra parts: arm, gear; photos skipped (cluttered): indices [0, 2].

Likeness: aws67 0.84 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type other; body box rect 100x110x30 mm, ramp 30; wheels 2 r12 inboard; weapon none; extra parts: arm, gear; photos skipped (cluttered): indices [0, 2].

Likeness: aws67 0.56 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/upgraded_for_the_roboteers_pleasure.aws67.webp` is declared `top` (IoU 0.56 there) but the model matches it better from rear_ri

## Round 4 (verification, helper 2)
Blockers r3 50 -> r4 7 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `gear`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- arm: joint axis reversed so positive travel lifts the tip (it drove into the chassis)
- arm sweeps through chassis at 41 poses: not carved (would change the outside)
- arm sweeps through gear at 41 poses: not carved (would change the outside)
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- hollowed chassis (wall 2.5, form 0): 292.5 -> 96.2 cm3
- hollowed gear (wall 2.5, form 0): 3.8 -> 2.5 cm3

Left (and why):
- proxy.sweep x1: joint `arm`: `arm` hits `chassis` 0.39 mm deep at 7.3 (declared range 0..80; allowed 0.08). `robot probe spec.json --joint arm` lists the closest approach to every part.
- power.weapon_motor x1: toolchain: lifters/flippers are servo or gear driven; the check wants a brushless kV for every weapon.
- process.weapon_printed x1: toolchain: a printed lifter/flipper arm is judged like a spinner (needs hardened teeth); adding metal teeth changes the look.
- wire.rotor_clearance x4: toolchain: same full-revolution assumption; wires cannot leave a cylinder that covers the chassis.

Likeness (best silhouette IoU per photo, r3 -> r4): upgraded_for_the_roboteers_pleasure.aws67.webp 0.83 -> 0.83

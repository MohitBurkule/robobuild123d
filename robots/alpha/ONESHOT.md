
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (scoop), guessing the tilt maths by hand. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends link to the kit spec. ~2 min per robot plus the script.
- Wheel track (`wheels.x`), per-axle radius, or `n: 0` for no-wheel robots. Did instead: patched wheel parts after `robot kit`. ~2 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 85x92x30 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: scoop, link.

Likeness: aws72 0.84 (ok).

## Round 2 (looks)
Decisions: type lifter; body box rect 85x92x30 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: scoop, link.

Likeness: aws72 0.84 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 85x92x30 mm, ramp 0; wheels 2 r12 inboard; weapon none; extra parts: scoop, link.

Likeness: aws72 0.28 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/alpha.aws72.webp` is declared `front` (IoU 0.28 there) but the model matches it better from rear (elevation 45, azimuth 270) (I

## Round 4 (verification, helper 2)
Blockers r3 49 -> r4 13 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `link_l`, `link_r`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- scoop sweeps through chassis: 9 of 12 poses not carved (they would open the outside face)
- scoop sweeps through link_l at 34 poses: not carved (would change the outside)
- scoop sweeps through link_r at 35 poses: not carved (would change the outside)
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- chassis: 3 of 11 cuts dropped (they broke the solid: 2)
- hollowed chassis (wall 2.5, form 0): 216.3 -> 76.0 cm3

Left (and why):
- proxy.interference x1: `chassis` and `scoop` overlap by 0.91 mm (allowed 0.08).
- proxy.sweep x1: joint `scoop`: `scoop` hits `chassis` 0.91 mm deep at 0.0 (declared range 0..80; allowed 0.08). `robot probe spec.json --joint scoop` lists the closest approach to every part.
- power.weapon_motor x1: toolchain: lifters/flippers are servo or gear driven; the check wants a brushless kV for every weapon.
- process.weapon_printed x1: toolchain: a printed lifter/flipper arm is judged like a spinner (needs hardened teeth); adding metal teeth changes the look.
- electrical.battery_weapon_gap x1: toolchain: a limited-range arm is judged as a full revolution about its pivot; that cylinder covers the whole chassis.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.rotor_clearance x4: toolchain: same full-revolution assumption; wires cannot leave a cylinder that covers the chassis.
- likeness.view x1: looks, not in scope for this pass.
- likeness.silhouette x1: looks, not in scope for this pass.
- battery.rotor_gap x1: toolchain: same full-revolution assumption for a limited-range arm.

Likeness (best silhouette IoU per photo, r3 -> r4): alpha.aws72.webp 0.28 -> 0.29

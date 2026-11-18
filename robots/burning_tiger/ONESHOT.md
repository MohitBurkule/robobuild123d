
## Tools I wanted
- Kit weapon kind `lifter` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends lid to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type lifter; body box rect 70x80x24 mm, ramp 0; wheels 4 r12 outboard; weapon none; 3 forks 32 mm; extra parts: lid, arm.

Likeness: aws74 0.71 (FAIL), aws76 0.66 (FAIL).

## Round 2 (looks)
Decisions: type lifter; body box rect 70x80x24 mm, ramp 0; wheels 4 r12 outboard; weapon none; 3 forks 32 mm; extra parts: lid, arm.

Likeness: aws74 0.71 (FAIL), aws76 0.66 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type lifter; body box rect 70x80x24 mm, ramp 0; wheels 4 r14 outboard; weapon none; 3 forks 34 mm; extra parts: lid, arm.

Likeness: aws74 0.55 (FAIL), aws76 0.62 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/burning_tiger.aws74.webp` is declared `front` (IoU 0.55 there) but the model matches it better from rear_left_iso (elevation 45

## Round 4 (verification, helper 2)
Blockers r3 94 -> r4 12 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (pololu_hpcb6v_50to1), `dm_wheel_r1` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `lid`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`, `dt_mount_fork_0`, `dt_mount_fork_1`, `dt_mount_fork_2`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- arm sweeps through chassis at 33 poses: not carved (would change the outside)
- arm sweeps through lid at 41 poses: not carved (would change the outside)
- no screw line found for fork_0
- no screw line found for fork_1
- no screw line found for fork_2
- rod dt_axle_wheel_l1: 2.8 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 2.8 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- mass estimate 162 g over 150: walls 2 mm -> 155 g
- mass estimate 155 g over 150: walls 1.6 mm -> 150 g
- hollowed chassis (wall 1.6, form 0): 134.4 -> 50.1 cm3

Left (and why):
- integrity.solids x1: `arm` has 2 closed solid(s) and 0 open/invalid shell(s), expected 1 (7542 mm3). A boolean or fillet probably collapsed the build.
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.sweep x1: joint `arm`: `arm` hits `chassis` 1.12 mm deep at 7.3 (declared range 0..80; allowed 0.08). `robot probe spec.json --joint arm` lists the closest approach to every part.
- power.weapon_motor x1: toolchain: lifters/flippers are servo or gear driven; the check wants a brushless kV for every weapon.
- process.geometry x2: `fork_0` (laser): 1 face(s) (17 mm2) are neither the two plate faces nor walls perpendicular to them: 3D features (bumps, drum surfaces, raised teeth) cannot be laser/waterjet cut.
- process.weapon_printed x1: toolchain: a printed lifter/flipper arm is judged like a spinner (needs hardened teeth); adding metal teeth changes the look.
- electrical.battery_weapon_gap x1: toolchain: a limited-range arm is judged as a full revolution about its pivot; that cylinder covers the whole chassis.
- wire.rotor_clearance x2: toolchain: same full-revolution assumption; wires cannot leave a cylinder that covers the chassis.
- likeness.silhouette x2: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): burning_tiger.aws74.webp 0.66 -> 0.66; burning_tiger.aws76.webp 0.65 -> 0.65


## Tools I wanted
- Kit weapon kind `axe` (hinged plate/arm with pivot). Did instead: a hand-written extra prism/box marked kind weapon with a revolute joint. ~3 min.
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends hump to the kit spec. ~2 min per robot plus the script.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type other; body box rect 85x100x30 mm, ramp 25; wheels 2 r12 inboard; weapon none; 4 forks 28 mm; extra parts: hump, fin.

Likeness: aws72 0.77 (FAIL), aws74 0.72 (FAIL), aws76 0.77 (FAIL).

## Round 2 (looks)
Decisions: type other; body box rect 85x100x30 mm, ramp 25; wheels 2 r12 inboard; weapon none; 4 forks 28 mm; extra parts: hump, fin.

Likeness: aws72 0.77 (FAIL), aws74 0.72 (FAIL), aws76 0.77 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type other; body box rect 85x100x30 mm, ramp 25; wheels 2 r12 inboard; weapon none; 4 forks 28 mm; extra parts: hump, fin.

Likeness: aws72 0.77 (FAIL), aws74 0.69 (FAIL), aws76 0.68 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/shark_attack.aws76.webp` is declared `front_right_iso` (IoU 0.68 there) but the model matches it better from front_right_iso (e

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type other; body box rect 85x100x30 mm, ramp 25; wheels 2 r12 inboard; weapon none; 4 forks 28 mm; extra parts: hump, fin, hammer_tip, hinge_block.

Likeness: aws72 0.77 (FAIL), aws74 0.69 (FAIL), aws76 0.68 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/shark_attack.aws76.webp` is declared `front_right_iso` (IoU 0.68 there) but the model matches it better from front_right_iso (e

## Round 4 (verification, helper 2)
Blockers r3 88 -> r4 10 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `hump_l`, `hump_r`, `hinge_block`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_mount_fork_0`, `dt_mount_fork_1`, `dt_mount_fork_2`, `dt_mount_fork_3`
- 5 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- fin: joint axis reversed so positive travel lifts the tip (it drove into the chassis)
- fin sweeps through chassis at 41 poses: not carved (would change the outside)
- fin sweeps through hinge_block at 41 poses: not carved (would change the outside)
- no screw line found for fork_0
- no screw line found for fork_1
- no screw line found for fork_2
- no screw line found for fork_3
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 154 g over 150: walls 2 mm -> 149 g
- mass estimate 149 g over 150: walls 1.6 mm -> 134 g
- hollowed chassis (wall 1.6, form 0): 219.4 -> 64.2 cm3
- hollowed hump_l (wall 1.6, form 0): 14.4 -> 6.2 cm3
- hollowed hump_r (wall 1.97, form 1): 14.4 -> 7.4 cm3
- hammer_tip: no screw line and no slot, left undeclared (needs a real mount)

Left (and why):
- proxy.wiring x1: Wire `w_bat_sw` (`el_battery.xt30` to `el_switch.in`): no baseline route (run the full `wiring` group once and pass its report).
- proxy.sweep x1: joint `fin`: `fin` hits `chassis` 0.18 mm deep at 7.3 (declared range 0..80; allowed 0.08). `robot probe spec.json --joint fin` lists the closest approach to every part.
- process.geometry x1: `hammer_tip` (laser): 5 sharp internal corner(s): radius 0 < kerf 0.1 mm (add a fillet >= kerf or the mating part will not seat).
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- wire.render_count x1: iso.png: 4 routes vs 5 spec wires (missing ['w_bat_sw']); top.png: 4 routes vs 5 spec wires (missing ['w_bat_sw'])
- likeness.silhouette x3: looks, not in scope for this pass.
- likeness.view x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): shark_attack.aws72.webp 0.77 -> 0.77; shark_attack.aws74.webp 0.69 -> 0.7; shark_attack.aws76.webp 0.68 -> 0.68


## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 104x100x26 mm, ramp 44; wheels 4 r11 inboard; weapon none; 2 forks 20 mm.

Likeness: aws57 0.81 (FAIL), aws63 0.81 (ok).

## Round 3b (rebuilt by eye from the photos: parts moved to where the photo shows them, camera set per photo)
Decisions: type lifter; body box rect 104x92x24 mm, ramp 0; wheels 4 r12 inboard; weapon none; extra parts: front_flap, cheek, rail_a, rail_b, rail_c, rear_bar.

Likeness: aws57 0.67 (FAIL), aws60 0.77 (FAIL), aws63 0.72 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 69 -> r4 14 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (pololu_hpcb6v_50to1), `dm_wheel_r1` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `front_flap`, `cheek_l`, `cheek_r`, `rail_a`, `rail_b`, `rail_c`, `rear_bar`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- front_flap: polycarbonate laser is not a flat plate -> printed nylon
- chassis: a cut was not made (it would open 111 mm2 of outside face; the overlap stays as a finding)
- chassis: a cut was not made (it would open 116 mm2 of outside face; the overlap stays as a finding)
- rod dt_axle_wheel_l1: 2.8 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 2.8 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- mass estimate 189 g over 150: walls 2 mm -> 173 g
- mass estimate 173 g over 150: walls 1.6 mm -> 159 g
- hollowed chassis (wall 1.6, form 0): 201.9 -> 74.6 cm3
- hollowed front_flap (wall 1.6, form 0): 35.6 -> 12.4 cm3
- hollowed cheek_l (wall 1.6, form 0): 6.9 -> 4.3 cm3
- hollowed cheek_r (wall 1.6, form 0): 6.9 -> 4.3 cm3
- hollowed rail_a (wall 1.6, form 0): 3.9 -> 2.9 cm3
- hollowed rail_b (wall 1.6, form 0): 3.9 -> 2.9 cm3
- hollowed rail_c (wall 1.6, form 0): 3.9 -> 2.9 cm3
- hollowed rear_bar (wall 1.6, form 0): 2.5 -> 2.0 cm3

Left (and why):
- proxy.wiring x4: Wire `w_bat_sw` (`el_battery.xt30` to `el_switch.in`): its ports moved 51.39 mm since the baseline route.
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- proxy.interference x2: `chassis` and `dm_wheel_l1` overlap by 4.88 mm (allowed 0.08).
- fit.interference x2: `dm_wheel_l1` overlaps wall `chassis` by 4.88 mm: it will not go in. No side has 5.08 mm free (free room per side {'-x': 1.2, '+x': 0.0, '-y': 0.01, '+y': 0.01, '-z': 0.91, '+z': 0.91}): grow the pock
- likeness.view x2: looks, not in scope for this pass.
- likeness.silhouette x3: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): bolt.aws57.webp 0.66 -> 0.66; bolt.aws60.webp 0.62 -> 0.62; bolt.aws63.webp 0.72 -> 0.72

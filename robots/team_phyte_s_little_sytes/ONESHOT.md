
## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 118x112x24 mm, ramp 90; wheels 2 r8 outboard; weapon none.

Likeness: aws74 0.73 (FAIL), aws76 0.85 (ok), aws77 0.79 (FAIL).

## Round 3b (rebuilt by eye from the photos: parts moved to where the photo shows them, camera set per photo)
Decisions: type wedge; body box rect 96x112x30 mm, ramp 0; wheels 2 r10 inboard; weapon none; extra parts: fin, lip, electronics_tray; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws74 0.62 (FAIL), aws76 0.41 (FAIL), aws77 0.66 (FAIL).

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type wedge; body box rect 96x112x30 mm, ramp 0; wheels 2 r10 inboard; weapon none; extra parts: fin, lip, electronics_tray, ear; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws74 0.59 (FAIL), aws76 0.40 (FAIL), aws77 0.64 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/team_phyte_s_little_sytes.aws76.webp` is declared `front_left_iso` (IoU 0.40 there) but the model matches it better from rear_r

## Round 4 (verification, helper 2)
Blockers r3 57 -> r4 7 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_1s_300), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `fin_l`, `fin_r`, `electronics_tray`, `ear_l`, `ear_r`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- no screw line found for lip
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- hollowed chassis (wall 2.5, form 0): 118.0 -> 71.5 cm3

Left (and why):
- integrity.solids x1: `chassis` has 0 closed solid(s) and 1 open/invalid shell(s), expected 1 (70312 mm3). A boolean or fillet probably collapsed the build.
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- electrical.cells_consistent x1: Cell counts: battery 1S, electronics.cells 2S.
- likeness.silhouette x3: looks, not in scope for this pass.
- likeness.view x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): team_phyte_s_little_sytes.aws74.webp 0.59 -> 0.6; team_phyte_s_little_sytes.aws76.webp 0.4 -> 0.4; team_phyte_s_little_sytes.aws77.webp 0.64 -> 0.64

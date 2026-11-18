
## Tools I wanted
- Kit `scoop`/front-plate key (width, height, angle, curve). Did instead: tilted box / side-profile prism (front_plate), guessing the tilt maths by hand. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 1 (one-shot)
Decisions: type wedge; body box rect 92x80x24 mm, ramp 0; wheels 4 r10 outboard as treads; weapon none; extra parts: front_plate.

Likeness: aws71 0.83 (ok).

## Round 2 (looks)
Decisions: type wedge; body box rect 92x80x24 mm, ramp 0; wheels 4 r10 outboard as treads; weapon none; extra parts: front_plate.

Likeness: aws71 0.83 (ok).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body box rect 92x80x24 mm, ramp 0; wheels 4 r12 outboard; weapon none; extra parts: front_plate.

Likeness: aws71 0.70 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/i_never_asked_for_this.aws71.webp` is declared `front_left_iso` (IoU 0.70 there) but the model matches it better from rear_left

## Round 3c (user angle picks applied; shape fixed per user remarks)
Decisions: type wedge; body box rect 92x80x24 mm, ramp 0; wheels 4 r12 outboard; weapon none; extra parts: front_plate.

Likeness: aws71 0.64 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/i_never_asked_for_this.aws71.webp` is declared `front_left_iso` (IoU 0.64 there) but the model matches it better from front_rig

## Round 4 (verification, helper 2)
Blockers r3 64 -> r4 1 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (pololu_hpcb6v_50to1), `dm_wheel_r1` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `front_plate`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- front_plate: aluminium laser is not a flat plate -> printed nylon
- rod dt_axle_wheel_l1: 2.8 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 2.8 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- hollowed chassis (wall 2.5, form 0): 176.6 -> 72.4 cm3
- hollow skipped front_plate: solids 1 vol 1.00

Left (and why):
- likeness.silhouette x1: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): i_never_asked_for_this.aws71.webp 0.72 -> 0.72

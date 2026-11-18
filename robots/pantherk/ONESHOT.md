
## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type wedge; body twin_pods rect 102x86x22 mm, ramp 30; wheels 4 r12 outboard; weapon none.

Likeness: aws67 0.79 (FAIL).
Other likeness findings: [FAIL] likeness.mask_source: `reference/pantherk_ii.aws66.webp_mask.png` matches `robot mask reference/pantherk_ii.aws66.webp --thr 130 --textured` at IoU 0.26 

## Round 3b (rebuilt by eye from the photos: parts moved to where the photo shows them, camera set per photo)
Decisions: type wedge; body twin_pods rect 102x86x22 mm, ramp 30; wheels 4 r12 outboard; weapon none; extra parts: top_plate, picture.

Likeness: aws66 0.71 (FAIL), aws67 0.79 (FAIL), aws68 0.66 (FAIL).

## Round 4 (verification, helper 2)
Blockers r3 86 -> r4 32 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l1` (pololu_hpcb6v_50to1), `dm_wheel_r1` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `pod_l`, `bridge`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`, `dt_hub_wheel_l1`, `dt_hub_wheel_r1`
- 4 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- no screw line found for top_plate
- rod dt_axle_wheel_l1: 2.8 mm stub clear of ['dm_wheel_l1'] printed as the wheel's hub boss
- rod dt_axle_wheel_r1: 2.8 mm stub clear of ['dm_wheel_r1'] printed as the wheel's hub boss
- hollowed pod_l (wall 2.5, form 0): 62.0 -> 28.8 cm3
- hollowed pod_r (wall 2.5, form 0): 62.0 -> 29.3 cm3
- hollowed bridge (wall 2.5, form 0): 29.3 -> 13.8 cm3
- top_plate: no screw line and no slot, left undeclared (needs a real mount)
- picture: no screw line and no slot, left undeclared (needs a real mount)

Left (and why):
- proxy.wiring x4: Wire `w_bat_sw` (`el_battery.xt30` to `el_switch.in`): its ports moved 43.85 mm since the baseline route.
- connection.floating x2: `top_plate` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis. Nearest part is `pod_l`, 0.0 mm away.
- process.geometry x2: `top_plate` (laser): 3 planar levels along the plate normal (0.00, 0.10, 2.00 mm): a blind pocket, step or a feature standing proud of the plate; a cut part has exactly two faces.
- mfg.stock x1: `picture` (laser): thickness 0.80 mm is not a stock polycarbonate gauge (0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 6); nearest 0.75 mm.
- proxy.assembly x19: `pod_r`: the baseline teardown never took it off.
- wire.render_wires x1: toolchain: the likeness group writes diff/match/view PNGs into renders/ without a wire sidecar, so any robot with wires fails; likeness renders should write sidecars or be excluded.
- likeness.silhouette x3: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): pantherk_ii.aws66.webp 0.71 -> 0.71; pantherk_ii.aws67.webp 0.79 -> 0.79; pantherk_ii.aws68.webp 0.66 -> 0.66

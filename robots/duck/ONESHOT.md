# duck: one-shot looks pass

One pass, looks only (no verification, fasteners, mass). Built with `robot kit kit.json` then patched parts (see `kit_patch.json`; final shapes are in `spec.json`).

## Decisions
Orange wedge body with rounded-ish tail, white flipper panel on the slope (weapon kind flipper, hinge x), two blue rear hooks, steel front lip. 2 hidden wheels.

## Likeness (`robot likeness`, run once)

| photo | IoU | need | closest template | result |
|---|---|---|---|---|
| duck_ling_.aws67.webp | 0.76 | 0.85 | revron_ant 0.85 | FAIL |
| duck_ling_.aws71.webp | 0.69 | 0.80 | vspin_drisk 0.78 | FAIL |
| duck_ling_.aws72.webp | 0.81 | 0.81 | wedge_2wd 0.81 | ok |

No type / weapon / template-copy findings.

`robot diff-photo` ran once: sheets in `renders/diff_*.png` (no API key, so no auto-listed differences).

## What still looks wrong
Photos show three different front ends (plain lip, forks, plate); only the plain lip is modelled so aws71 (forks) scores 0.69. Hooks are blocks not curved horns; body side walls are straight, real ones curve.

## Missing tool / hint
likeness crashed on REFERENCE weapon.axis for a non-spinner weapon (`p.joint.get` on an Obj) so axis was dropped from REFERENCE.json. Per-photo configuration variants are not expressible.

## Verdict
Looks alike: **partly**. Renders: `renders/iso.png`, `renders/top.png`.

## Round 2 (looks)
Dark body with rounded tail plan, curved rear hooks, salmon front pad plus steel lip. Weapon axis restored in REFERENCE.json.

Likeness: aws67 0.80 (FAIL), aws71 0.66 (FAIL), aws72 0.75 (FAIL).

## Tools I wanted
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type flipper; body box rect 120x110x31 mm, ramp 85; wheels 2 r12 inboard; weapon none.

Likeness: aws67 0.80 (FAIL), aws71 0.66 (FAIL), aws72 0.75 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type flipper; body box rect 120x110x31 mm, ramp 85; wheels 2 r12 inboard; weapon none.

Likeness: aws67 0.80 (FAIL), aws71 0.66 (FAIL), aws72 0.64 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/duck_ling_.aws72.webp` is declared `front_left_iso` (IoU 0.64 there) but the model matches it better from front_right_iso (elev

## Round 4 (verification, helper 1)
S1: printed parts nylon -> abs (lighter) and flipper plate hollowed with a closed 50x62x2.2 mm void (mass 160.6 -> under 150 g); front_lip 1.2 -> 1.0 mm stock gauge, bottom face kept.

## Round 4 (verification, helper 2)
Blockers r3 60 -> r4 5 (`verify --tier inner`).

Fixed / changed (inside only, outside kept):
- detail parts made integral (bosses into their part, fake screw heads removed, short axle stubs printed with the wheel hub)
- catalog parts added in free space inside the printed parts with 0.25 mm pockets: `dm_wheel_l0` (pololu_hpcb6v_50to1), `dm_wheel_r0` (pololu_hpcb6v_50to1), `el_battery` (lipo_2s_180), `el_esc` (bbb_malenki_nano), `el_switch` (switch_slide_12x4)
- overlaps resolved by cuts that keep the union of the parts (pockets, bores, wheel and spinner running clearance)
- one print with the chassis (same material, `fused_with`): `duckname_2`, `duckname_1`, `duckface_beak`, `duckface_head`, `duckface_bg`, `duckface_rim`, `front_plate`, `hook_l`, `hook_r`, `dt_hub_wheel_l0`, `dt_hub_wheel_r0`
- 5 wires declared (battery - switch - ESC - motors)
- print orientation on every printed part, failsafe / weapon disable declared, design volumes declared where this pass changed a part on purpose
- power switch on the floor of the body, slider facing down to a 7 x 3 mm slot in the underside (no slot on the top or sides; hollow cavities stay closed behind a wall at every outside face)
- no screw line found for front_lip
- rod dt_axle_wheel_l0: 2.8 mm stub clear of ['dm_wheel_l0'] printed as the wheel's hub boss
- rod dt_axle_wheel_r0: 2.8 mm stub clear of ['dm_wheel_r0'] printed as the wheel's hub boss
- mass estimate 304 g over 150: walls 2 mm -> 167 g
- mass estimate 167 g over 150: walls 1.6 mm -> 159 g
- hollowed chassis (wall 1.6, form 0): 262.9 -> 84.1 cm3
- hollowed front_plate (wall 1.6, form 0): 7.9 -> 7.1 cm3
- hollowed hook_l (wall 1.6, form 0): 3.9 -> 2.2 cm3
- hollowed hook_r (wall 1.6, form 0): 3.9 -> 2.2 cm3
- photo graphics as fused colour-split decals (robot decal): duck face card (ring, blue disc, head, beak) and DUCK LING lettering on the flipper

Left (and why):
- proxy.wiring x1: Wire `w_sw_esc` (`el_switch.out` to `el_esc.bat`): the baseline route is now blocked by `chassis` (6 samples).
- mass.over x1: the photo-sized outside (steel weapon / big printed shell) is heavier than 150 g even hollowed; only a smaller outside would fix it.
- likeness.silhouette x3: looks, not in scope for this pass.

Likeness (best silhouette IoU per photo, r3 -> r4): duck_ling_.aws67.webp 0.8 -> 0.8; duck_ling_.aws71.webp 0.66 -> 0.66; duck_ling_.aws72.webp 0.76 -> 0.76

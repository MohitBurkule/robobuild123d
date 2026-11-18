# vampire: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type horizontal_spinner; body box rect 100x112x22 mm, ramp 0; wheels 2 r11 inboard; weapon bar r64 axis z teeth 2; extra parts: hub.

Likeness: aws71 0.66 (FAIL), aws74 0.72 (FAIL), aws76 0.56 (FAIL).

## Tools I wanted
- Free primitives in kit.json (`extras`). Did instead: private generator script that appends hub to the kit spec. ~2 min per robot plus the script.
- Body side-profile / plan polygon keys. Did instead: replaced the chassis shape in the generator. ~3 min.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type horizontal_spinner; body box rect 100x112x28 mm, ramp 0; wheels 2 r11 inboard; weapon bar r64 axis z teeth 2; extra parts: hub.

Likeness: aws71 0.64 (FAIL), aws74 0.71 (FAIL), aws76 0.52 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type horizontal_spinner; body box rect 100x112x28 mm, ramp 0; wheels 2 r14 inboard; weapon bar r64 axis z teeth 2; extra parts: hub.

Likeness: aws71 0.46 (FAIL), aws74 0.50 (FAIL), aws76 0.44 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/vampire.aws71.webp` is declared `top` (IoU 0.46 there) but the model matches it better from rear_left_iso (elevation 25, azimut; [FAIL] likeness.view: `reference/vampire.aws74.webp` is declared `front_right_iso` (IoU 0.50 there) but the model matches it better from rear_right_iso (elevati; [FAIL] likeness.view: `reference/vampire.aws76.webp` is declared `left` (IoU 0.44 there) but the model matches it better from front (elevation 25, azimuth 90) (

## Round 4 (verification, helper 1)

Started from the owner's round-3b spec (which already carries the catalog motors, electronics, pockets and wiring). Running the generic round-4 script on it made it worse (16), so this is a targeted pass instead.

Blockers r3b -> r4: **14 -> 9** (`verify --tier inner`, full output in verify_r4.txt).
Likeness (best silhouette IoU per photo, r3b -> r4, exact): vampire.aws71 0.512 -> 0.512, vampire.aws74 0.530 -> 0.530, vampire.aws76 0.402 -> 0.402.

What was done (outside shape unchanged):
- `dt_hubw_weapon` is now two turned collars above and below the weapon bar (the bar passes between them), parented to the weapon and turning with it; press fit on the live shaft. This removes the weapon/hub overlap and the "full revolution reaches the hub" sweep.
- the live shaft is declared to run in the bore of the printed hub (method `shaft`), which closes the rotor's path back to the chassis.
- `deck`: material id `carbon` -> `carbon_fibre` (a real id, so its mass is counted); a hole under the printed hub, hidden by the hub, removes the deck/hub overlap.

Left (one line each):
- mass.over x1: 185.7 g against 150 g. Now that the deck's mass is counted the total is higher; the kit outline (steel bar 42.8 g, chassis 68.7 g) is over the limit.
- power.weapon_motor x1: no room for a brushless outrunner inside the print without changing the outside.
- wire.render_wires x1: toolchain/process. The photo-match, diff and likeness sheets are written without a render record of the wire routes.
- likeness.view / likeness.silhouette x6: looks; not part of this pass.

## Round 3d (user camera picks batch 2 + shape remarks applied; round 4 to be re-run on the new outside)
Decisions: type horizontal_spinner; body box rect 100x112x20 mm, ramp 0; wheels 2 r12 inboard; weapon bar r72 axis z teeth 2; extra parts: hub, deck, green_wall.

Likeness: aws71 0.63 (FAIL), aws74 0.67 (FAIL), aws76 0.40 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/vampire.aws76.webp` is declared `left` (IoU 0.40 there) but the model matches it better from rear (elevation 25, azimuth 270) (

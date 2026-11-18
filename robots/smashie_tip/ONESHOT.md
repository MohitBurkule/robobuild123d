# smashie_tip: looks-first build notes

Built from `kit.json` (`robot kit`, plus the `extras`/`colors`/`ref` keys a small generator turns into patched parts, REFERENCE.json and masks).

## Round 1 (one-shot)
Decisions: type vertical_spinner; body box rect 55x42x18 mm, ramp 8; wheels 2 r9 outboard; weapon disc r12 axis x teeth 2; 2 forks 25 mm; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws73 0.61 (FAIL), aws74 0.63 (FAIL), aws76 0.73 (FAIL).

## Tools I wanted
- A mask tool for cluttered photos (rectangle-seeded grabcut, preview). Did instead: skipped photos / `--textured` / left-half crop, unchecked. ~2 min, and the IoU on those photos is not trustworthy.
- Colours in kit.json and `--palette spec` by default. Did instead: generator recolours parts. ~1 min.
- `cluster` in kit.json and a way to confirm the bot count. Did instead: guessed N from the photos.
- `robot looks SPEC` (build + iso/top + likeness + diff sheets in one pass, batchable). Did instead: four CLI calls per robot, ~3-4 min wall each.

## Round 2 (looks)
Decisions: type vertical_spinner; body box rect 55x42x18 mm, ramp 8; wheels 2 r9 outboard; weapon disc r12 axis x teeth 2; 2 forks 25 mm; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws73 0.61 (FAIL), aws74 0.63 (FAIL), aws76 0.73 (FAIL).

## Round 3 (looks: photo-matched views, attachment + detail pass: hubs, axles, shafts, bearing arms, fork mounts, screw heads; verify blockers rise because detail parts are not yet integral, fixed in round 4)
Decisions: type vertical_spinner; body box rect 55x42x18 mm, ramp 24; wheels 2 r8 outboard; weapon disc r12 axis x teeth 2; 1 forks 22 mm; clusterbot, one of 2 modelled (count read from photos, unsure).

Likeness: aws73 0.52 (FAIL), aws74 0.44 (FAIL), aws76 0.52 (FAIL).
Other likeness findings: [FAIL] likeness.view: `reference/smashie_1.aws73.webp` is declared `left` (IoU 0.52 there) but the model matches it better from front_left_iso (elevation 45, az; [FAIL] likeness.view: `reference/smashie_1.aws74.webp` is declared `front` (IoU 0.44 there) but the model matches it better from front_left_iso (elevation 25, a; [FAIL] likeness.view: `reference/smashie_1.aws76.webp` is declared `front_left_iso` (IoU 0.52 there) but the model matches it better from rear_right_iso (elevat

## Round 4 (verification, helper 1)

Started from the owner's round-3b spec, which already carries the catalog motors, electronics, pockets and wiring (29 blockers). Running the generic round-4 script on it made it worse (50): it skips running-clearance cuts that would open the outside. So this is a minimal targeted pass.

Blockers r3b -> r4: **29 -> 28** (`verify --tier inner`, full output in verify_r4.txt). Likeness is unchanged (exact per-photo IoU: aws73 0.521, aws74 0.444, aws76 0.611).

Done:
- `fork_0` / `fork_1`: `volume_mm3: 126` declared. That is the real volume of the rebuilt 6 x 14 x 1.5 mm plates; the volume store still held the old 792 mm3 forks.

Left, and why it needs a design change rather than a verification pass:
- The two N20 gearmotors overlap each other by 4.9 mm. The 36 mm track has no room for two coaxial 36 mm gearmotors.
- The LiPo 2S 350 overlaps the chassis, the disc posts and the weapon sweep. The class mass is 75 g and the robot is at 90 g. A smaller pack (2S 180, 28 x 18 x 10) needs a new pocket that the rebuilt chassis has no room for without changing the outside.
- No power switch: there is no flat belly skin. Fixing this clears 2 blockers (legal.switch, electrical.switch_in_series).
- The weapon has no brushless motor (no room on the axis). It has a 0.84 mm web, which is the kit shape.
- render_wires: toolchain/process. likeness: looks.

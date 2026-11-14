# Limpet XXT: build spec (UNTESTED)

**UNTESTED.** Nothing in this folder has been run: no build, test or render. The code was written from photos and
repo source alone. Treat every number as a starting point. `params.check()` lists the packaging relations to assert first.

## What it is
A UK antweight (150 g) from **Team 13** (John Denny, Hinckley), a small replica of Team 13's 1998 Robot Wars
heavyweight *Limpet*. It is a four-wheeled, invertible box with a full-width front-hinged flipper/wedge and clear
polycarbonate armour with zebra decals. This copy follows the latest look, AWS 71–76 (2023–2025). See REFERENCE.md.

## Rules
- `RULE_ERA = "aws_2025"` (default): the robot must fit a 150 mm floor square with no overhang at any height. There is
  no height limit, and the mass limit is 150 g (repo draft PR #77).
- `RULE_ERA = "aws_v4_3"`: the older rule. The robot must fit inside a 101.6 mm cube at the start, in any orientation,
  and may expand only after the start. Most Limpet XXT versions were built under this rule, so this copy keeps
  `OVERALL_L`/`OVERALL_W` under 101.6 mm and fits both eras.
- Expansion is the flipper joint angle (`START_FLIP_DEG` = 0 at rest, up to `FLIP_OPEN_DEG`). At the start the flipper
  is at rest.

## Frame
X is forward (the flipper end), Y is left and Z is up. The floor is Z = 0.

## Masters (params.py, MASTERS block)
| name | value | basis |
|---|---|---|
| OVERALL_L × OVERALL_W | 100 × 96 mm | PHOTO proportions, GUESS scale |
| FLIPPER_SHARE | 0.32 of length | PHOTO |
| WHEEL_D × WHEEL_W | 24 × 8 mm | GUESS (PHOTO: tyre just proud of the body, top and bottom) |
| WHEEL_PROUD | 1.5 mm | GUESS |
| SHEET_T / LID_T | 2.0 / 1.5 mm PC | GUESS (PHOTO: clear sheet) |
| PLATE_CHAMFER_FRAC, FLIP_CHAMFER_FRAC | 0.5 / 0.12 | PHOTO outline |
| FLIP_OPEN_DEG | 90° | GUESS |
| catalogue ids | n10_300rpm_6v ×4, servo_cs07, lipo_2s_180, malenki_nano, switch_bbb_ant_rvrn2 | GUESS choice, CAT dims |
| WALL, CLEAR, RUN_CLEAR | from robot/cad/bay.py | STD |
| screws | M2 button, from robot/cad/fastener_catalog.py | STD |

Derived at the default values (hand-computed, not run): tub 68 × 72 × 19.5 mm; flipper 90 wide × 38.3 long, resting
at 33° and hinged on the tub's top front edge; axles at X = +3.4 and −35.4; 10 mm side-plate standoffs.

## Parts as manufactured
| part | qty | process | notes |
|---|---|---|---|
| tub | 1 | FDM PLA | open top. 4 through-wall motor pockets, servo pocket, battery and ESC bays (`bay.derive_bay`), switch slot, 2 outer hinge knuckles, side standoff columns and lid bosses with M2 heat-sets |
| lid_r / lid_l | 2 | 1.5 mm PC, 2D cut | mirrored pair. The slot between them shows the flipper tail and battery (PHOTO) |
| side_r / side_l | 2 | 2 mm PC, 2D cut | hexagonal plate outboard of the wheels; mirror pair |
| flipper | 1 | 2 mm PC, 2D cut | chamfered front corners |
| hinge_block | 1 | FDM PLA | centre knuckle, flipper seat (2 × M2) and the tail lever with the pin slot |
| horn | 1 | FDM or servo horn | drive pin runs in the tail slot |
| wheel | 4 | printed hub + tyre | from PR #68 `robot.modules.wheel.Wheel` if present, otherwise the same relation built locally |
| COTS | – | catalogue | 4 N10 motors, SG90-class servo, 2S 180 mAh LiPo, Malenki Nano, BBB switch, M2 screws/inserts, M2 hinge pin |

## Reused repo code
- `robots/revron/src/revron/hw.py`: catalogue part sizes. Loaded by path so the whole Revron rig isn't built.
- `robot/cad/bay.py`: `derive_bay` for the battery and ESC cut solids, plus the `DEFAULT_WALL`, `PRINTED_FIT_CLEARANCE`,
  `RUNNING_CLEARANCE` and `CUT_OVERSHOOT` constants.
- `robot/cad/fastener_catalog.py`: clearance, tap, insert and head sizes.
- `robot/catalog.py`: part ids, masses and material densities.
- PR #68 `robot/modules/wheel.py`: the wheel, imported if available. A fallback is in `parts.wheel()`.
- The Revron `joints.py` pattern: tub as datum, moving parts on build123d Revolute/Rigid joints.

## Known weak spots (fix after the first real build)
- The servo position and flipper linkage are inferred, not seen. `horn_angle()` aims the pin at the slot, but the horn
  reach and the pin path have not been solved as a four-bar.
- The ends of the side plates have no screws. The photos show end screws, but their seat is hidden by the wheels.
- `tub()` cuts the motor pockets from the catalogue bounding box, not from a clamp. Check the motor retention.
- The mass is an estimate from catalogue masses and part volumes (`assembly.mass_report`). It has not been weighed.
- Wire routing between the side zones and the centre channel is not modelled.

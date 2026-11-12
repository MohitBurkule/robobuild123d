# Undertow: 150 g 4WD invertible control bot

> **UNTESTED: never built, run, rendered or verified.** No code in this folder has been executed. Every number below
> is a hand calculation from params.py masters and catalogue values; estimates are marked *(est.)*.

## Rules (masters in `src/undertow/params.py`)
- Mass: `MASS_LIMIT_G = Profile().mass_limit(roller=True)` = 150 g (aws2025), design margin `MASS_MARGIN_G` = 5 g.
- Size: `CUBE = 101.6` mm, AWS rules v4.3 sec 2b: the robot must fit fully inside a 4 in cube **in its start
  configuration**. `ENVELOPE_MARGIN = 1.0` per side -> `ENVELOPE_MAX = 99.6`. (`robot/profile.py footprint_mm = 150` is a
  different, looser figure and is NOT used for sizing.)
- Start config: the front attachment (forks or plough) is folded **up**, vertical, against the front-wall stop
  (`UP_STOP_DEG = 90`). It is free on its pin and drops forward onto the floor the first time the robot drives or brakes.
  Whether the event accepts a gravity-deployed attachment that exceeds the cube once running must be confirmed with the
  organisers (risk R1).

| envelope (start) | value | relation |
|---|---|---|
| width | 96.9 mm | 2 x (HALF_W_TUB 44.6 + skirt gap/t 1.0 + skirt lean 2.84) |
| length | 98.2 mm (plough) / 96.0 (forks) | PIN_Y 46.4 + folded thickness 6.6 + rear 45.24 |
| height | 45.0 mm | PIN_Z 11 + FORK_REACH 34 (folded fork); body 19 mm + tyres 22 mm |
| running length (forks down) | ~125.6 mm | PIN_Y + FORK_REACH + rear |

## Architecture
- **Drive**: 4WD, four `bbb_n10_1000rpm` direct drive (setting `motor`; `bbb_n10_600rpm` is the one-line variant), four
  `bbb_wheel_22x10` (setting `wheel`; `durahubs_25` alternative needs WHEEL_OD 25 -> taller body, re-check cube).
  Axles on the mid-plane (`Z_AXLE = WHEEL_OD/2`), tyres `WHEEL_PROUD = 1.5` past both plates: drives either way up.
  Wheels fully inside the plan outline (`HALF_W_TUB = X_WHEEL_OUT + WHEEL_RUN + WALL`). Motor backs on a 11 mm centre
  spine (`SPINE_HALF = 5.5`); one corner built, mirrored X and Y (`drive.QUADRANTS`).
- **Electronics**: `tattu_2s_300_75c_hv` in front of the centre rib, ESC behind it, receiver and `fingertech_mini_switch`
  either side of the ESC; all pockets from `robot/cad/bay.py:derive_bay` (insert -z, never trapped). Switch access hole
  in both plates.
- **Chassis**: TPU 95A tub (unibody spring), 0.8 mm carbon top and base plates, six M2 aluminium standoffs through the
  tub, M2x4 CSK from both plates (Revron's standoff-and-CSK scheme; TPU cannot hold Revron's heat-sets).
  Plan corners `CORNER_R = 9`.
- **Armour**: 0.5 mm Ti gr5 skirts on both sides and the rear, rolled knuckle on a 1 mm music-wire pin on the mid-plane.
  They hang to whichever side is down and rest on the tub's V flank (`FLANK_DEG = 15`), edge `SKIRT_DROP = 0.4` over
  the floor. No fixed edge for a tooth; sloped face for wedges.
- **Front (ONE setting `front`)**: common M3x85 pivot pin through two tub cheeks (`front_mount.py`).
  (a) `forks`: 5 x 0.8 mm hardened spring-steel forks, `FORK_REACH = 34`, rest slope asin(10.7/34) = 18.3 deg,
  independent on the pin with TPU spacers (self-levelling). (b) `plough`: TPU wedge 6 mm thick + 0.6 mm hardened-steel
  face, `PLOUGH_REACH = 26`, rest slope 24.3 deg. Both inside the rules wedge-angle band 6..30 deg.

## Load paths
- Push: opponent -> fork/plough -> pin -> TPU cheeks -> front wall -> motor pocket walls -> plate stacks -> tyres -> floor.
- Top hit (vertical spinner): carbon plate spreads -> TPU tub compresses -> standoffs share clamp load -> base plate.
- Side hit / horizontal spinner: skirt swings in (absorbs) -> V flank -> 2.4 mm TPU wall -> wheel-well walls + standoffs.
- Fragile parts (pack, ESC, Rx, switch, wires) are inboard of the wheel rows and between the plates.

## Mass budget (g)
| item | g | source |
|---|---|---|
| 4 x bbb_n10_1000rpm | 32.0 | catalogue 8.0 each |
| 4 x bbb_wheel_22x10 | 14.0 | catalogue 3.5 each |
| bbb_dual_esc_v31 | 7.0 | catalogue |
| rx_fs_ia6_decased | 4.5 | catalogue |
| tattu_2s_300_75c_hv | 16.0 | catalogue |
| fingertech_mini_switch | 2.15 | catalogue |
| wiring + connectors | 4.0 | *(est.)* |
| TPU tub | 18.0 | *(est.)* ~15 cm3 x 1.21 |
| 2 x carbon plate 0.8 | 15.2 | *(est.)* 6167 mm2 x 0.8 x 1.55 each |
| Ti skirts 3 + pins | 6.3 | *(est.)* |
| standoffs + screws | 3.6 | *(est.)* |
| **core** | **122.8** | |
| forks (5 + spacers + M3x85 pin + nut) | 10.7 | *(est.)* |
| or plough (TPU 8 + steel 7 + pin 4.8) | 19.8 | *(est.)* |
| profile allowance (glue/tape) | 1.2 | robot/profile.py |
| **total forks / plough** | **134.7 / 143.8** | margin 15.3 / 6.2 g (target >= 5) |

With `esc = bbb_malenki_nano` (2.3 g, built-in Rx): -9.2 g.

## Drive numbers (estimates; formulas shown)
- Top speed v = pi x D x n / 60 = pi x 0.022 x 1000 / 60 = **1.15 m/s** at the catalogue 6 V rating; on 2S (~7.6 V)
  scale ~x1.27 -> ~1.46 m/s no-load *(est.)*. 600 rpm variant: 0.69 / ~0.88 m/s.
- Traction limit F_t = mu x m x g = 1.0 x 0.150 x 9.81 = **1.47 N** (mu ~1.0 rubber on painted steel *(est.)*; all the
  mass is on driven wheels).
- Motor limit F_m = 4 x T_stall / r. Catalogue `stall_torque_gcm` is None; assumed T_stall ~ 300 g.cm = 0.029 N.m
  *(est.)* -> F_m = 4 x 0.029 / 0.011 = **~10.7 N** >> F_t: traction limited, so the 1000 rpm motors are not torque
  starved and the 600 rpm option buys only speed control, not push.
- Current: 4 x 1.0 A stall (catalogue "~1 A at 7.8 V") = 4 A worst case; pack 300 mAh x 75 C = 22.5 A. Runtime at a
  1.5 A mean *(est.)*: 12 min >> 3 min x 1.25 (profile `runtime_margin`).

## Why it beats Revron (robots/revron README / params.json)
Revron is a vertical spinner on 2WD (rear N10s, O-ring driven front micro wheels), spending ~1/3 of its mass on the
GR1507 + discs, not invertible-by-design on the drive side. Undertow spends that mass on 4WD traction (all weight on
driven tyres: ~2x Revron's traction share), floor skirts all round, and invertibility. Against Revron itself: the long
forks get under its wedgelets, a 4WD pusher out-pushes a 2WD spinner, and it keeps driving after being flipped.

## Risks / unsure
- R1 start-cube interpretation for the gravity-deployed attachment; plough start length 98.2 leaves only 1.4 mm.
- R2 ESC: brief's `bbb_malenki_nano` is 1 A cont / 1.8 A peak per channel; two N10s per side stall at ~2 A -> over
  rating when pushing (the job of this robot). Default is therefore `bbb_dual_esc_v31` (2 A cont / 4 A peak per side)
  + separate Rx; Malenki is a one-setting option with the risk noted.
- R3 shaft engagement only 8 mm of a 10.7 mm hub; wheel side-load on a bare 3 mm D shaft.
- R4 switch: fingertech mini needs a hex key, profile `require_tool_free_switch` may flag it.
- R5 skirt flip-over on inversion is a guess (needs the leaf to swing 180 deg past the wall; may stick).
- R6 TPU tub mass and stiffness, carbon plate mass, wiring mass are estimates. Stall torque assumed.
- Geometry gaps: rear-wall hinge bore and rear V flank not cut yet in `tub.py`; fork tip kick-down bend not modelled;
  plough fillet edge selection guessed; motor catalogue-frame origin assumed from `hw.reach`.

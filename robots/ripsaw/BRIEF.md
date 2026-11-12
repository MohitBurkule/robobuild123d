# Ripsaw: design brief

> **UNTESTED: never built, run, rendered or verified.** No code in `robots/ripsaw/` has been executed. Every number below is a
> hand estimate from `src/ripsaw/params.py` relations and catalogue values; run `robot verify spec.json` before trusting any of it.

## Architecture
- Vertical single-tooth disc on the robot centreline (X = 0), spinning up at the front. 60 mm OD, 3 mm hardox, laser cut.
- Hub motor: Repeat DirectDrive 2004 2800 kV (`repeat_2004_2800kv`). Disc bolts to the bell face (3x M3 on 15, catalogue pattern).
- Double shear: stator base bolted (3x M3, catalogue base pattern) to the LEFT rail; the 3 mm through shaft runs on into an
  MR63 bearing (`weapon_motor.pick_bearing(3.0)`) pressed blind into the RIGHT rail. The rails are prongs of the printed tub.
- Asymmetric rails on purpose: the motor body is all on one side of the disc, so the disc can sit on the centreline.
- 2WD: BBB N10 1000 rpm, DuraHubs 30 inside the tub outline behind the side walls, axle WHEEL_REAR_BIAS (14 mm default) ahead of the rear wall.
- Ground game: two Revron fork_5 parts (1.5 mm Ti, reused from `revron/fork.py`), hinged on M3 pins on the rail outer faces,
  free to swing, tips resting on the floor (self-levelling), up-stop FORK_LIFT above.
- Tub: printed nylon unibody, open top and bottom; printed base and top panels on M2 screws into heat-set inserts (as Revron).
  COTS pockets from `robot.cad.bay.derive_bay` (battery, both ESCs, switch).

## Load path / what rotates
| Rotates (weapon) | Fixed |
|---|---|
| disc, bell, 2004 shaft, MR63 inner race | stator, both rails, tub, MR63 outer race, panels, forks (hinge only) |

Hit on tooth -> disc -> 3 bell screws (shear) -> bell -> shaft -> (a) stator -> 3 M3 through left rail, (b) shaft end ->
MR63 -> right rail boss -> both rails -> tub floor ring and walls.

## Size rule
The limit is one setting, `RULES_SIZE`, in params.py:
- **Default `"aws2025"`**: AWS 2025 (robot/profile.py `footprint_mm`), a 150 mm floor square with no overhang at any height and
  no height limit. The envelope is 148 x 148 mm (ENVELOPE_MARGIN 2 mm). Sizing: TUB_BODY_L 62, RAIL_L 24, WHEEL_REAR_BIAS 14.
- Optional `"aws_v43_cube"`: a 101.6 mm cube, so the envelope is 99.6 mm on every side. Sizing: TUB_BODY_L 52, RAIL_L 18,
  WHEEL_REAR_BIAS 12. This gives about 94 x 80 x 45 mm with the forks down. That fits, so no fork hinge-up is needed.
- The disc stays 60 mm in both variants: mass limits it before size does. params.py asserts L, W and H against the envelope.

| Extent (default) | Relation | Value (est.) |
|---|---|---|
| Length | disc front (Y_AX + R) - tub rear | 79 - (-31) = 110 mm (limit 148) |
| Width | TUB_W (wheels inside) | 80 mm |
| Height | rail top = Z_AX + bell_r + wall | 31.5 + 12.35 + 1.5 = 45.4 mm (no limit) |
| Fork tips | pin Y_AX + FK_TIP 26 | y = 75, behind disc front 79 |

## Masters (params.py)
Rules: MASS_LIMIT_G (profile), CUBE_MM, ENVELOPE_MARGIN, TIP_LIMIT_MPH, MOVING_CLR, MIN_WALL.
COTS settings: WEAPON_MOTOR, BATTERY (+ BATTERY_ALTS), WEAPON_ESC, DRIVE_ESC (+ DRIVE_ESC_3S), SWITCH, DRIVE_MOTOR, WHEEL.
Disc: DISC_OD 60, DISC_T 3, FLOOR_GAP 1.5, TOOTH_STEP 8, RAMP_DEG 90, RIM 7, HUB_LAND 3.5, WIN_N 3, WIN_HALF_DEG 28.
Rails: DISC_RAIL_CLR 1.5, RAIL_T 4, BOSS_WALL 1.5, RAIL_L 18, RAIL_NOSE 1.5.
Tub: TUB_BODY_L 52, TUB_W 80, TUB_FLOOR_Z 3, TUB_H 24, WALL 1.6, CORNER_R 6, WHEEL_REAR_BIAS 12, panels 1.0 / 1.0, M2 x 3 per side.
Derived: Z_AX = R + FLOOR_GAP = 31.5, Y_AX = 38, balance window extra half-angle (numeric notch moment), rail X spans from
catalogue body length and shaft protrusion, wheel X/Y/Z, insert hole from `fastener_catalog.insert(2)`.

## Mass budget (default 2S build)
| Item | g | Source |
|---|---|---|
| Repeat 2004 2800 kV | 18.0 | cots_alts (BBB page ~18 g incl. wires) |
| Disc (hardox, 1716 mm2 x 3 mm x 7.9) | 40.7 | estimate from outline area |
| MR63 bearing | 0.3 | estimate |
| GNB 2S 350 HV XT30 | 17.0 | cots_alts |
| BBB brushless ESC 20 A | 5.0 | cots_alts |
| Malenki-Nano (Rx + drive) | 2.3 | cots_alts |
| 2x N10 1000 rpm | 16.0 | cots_alts (8.0 each) |
| 2x DuraHubs 30 | 8.0 | cots_alts (4.0 each) |
| FingerTech mini switch | 2.15 | cots_alts |
| Wires + XT30 | 4.0 | estimate |
| 2x fork (1.5 Ti) + pins | 4.6 | estimate |
| Tub (about 15.9 cm3 nylon x 1.12 x 0.85) | 15.1 | estimate |
| Base + top panel (1 mm nylon, 62 x 80) | 9.4 | estimate |
| Fasteners, heat-sets | 3.5 | estimate |
| Allowance (profile) | 1.2 | robot/profile.py |
| **Total (default 150 mm layout)** | **147.3** | margin about 2.7 g to 150 g: tight |

The cube variant comes to about 143.9 g, because its tub and panels are 3.4 g lighter. The 3S variant uses
`gnb_3s_300_80c_hv` (28 g) and `bbb_dual_esc_v31` (7 g) plus a separate Rx (about 1.5 g) in place of the Malenki. It comes to
about **164 g, roughly 14 g over**. That is why the default master is the 2S XT30 pack; `tattu_2s_300_75c_hv` is lighter (16 g) but uses JST-PH,
too small for the weapon current.

## Energy (estimates; formulas shown)
- Disc MOI: I = rho t [pi R^4 / 2 - sum(windows: theta (ro^4 - ri^4)/4) - notch A r^2], rho t = 2.37e-5 kg/mm2:
  30.15 - 6.94 - 2.88 = 20.3 kg mm2; + bell about 1.2 -> **I about 2.15e-5 kg m2**.
- rpm = kV x V x 0.8. omega = rpm x 2 pi / 60. E = I omega^2 / 2. Tip = omega R.

| Pack | V | rpm | E (J) | tip (m/s / mph) |
|---|---|---|---|---|
| 2S HV nominal | 7.6 | 17,024 | 34 | 53.5 / 120 |
| 2S HV full | 8.7 | 19,488 | 45 | 61.2 / 137 |
| 3S HV nominal (over weight) | 11.4 | 25,536 | 77 | 80.2 / 179 |

All far below the 600 mph limit. Bite (one tooth): bite = v_close / (rpm / 60). Drive: N10 1000 rpm at 6 V scaled to 7.6 V,
about 1267 rpm, 30 mm wheel -> about 2.0 m/s. Own speed: 2.0 / 283.7 Hz = **7.0 mm**; 4 m/s closing: 14 mm, so the
8 mm TOOTH_STEP limits it. Spin-up time not estimated (2004 at 20 A unknown).

## Why it beats Revron 2.0
Revron (robots/revron/REPORT.md): 42 mm disc, 19,320 rpm, verifier about **7.5 J** per blade; 149.5 g. Ripsaw: 60 mm
single disc, about **34 J** (estimated; different method, 0.8 vs 0.85 speed factor), about 4x Revron's energy, with
more bite per tooth, double-shear support (Revron: printed mounts), and forks reused from Revron so the ground game is no
worse. These numbers are not checked.

## Risks
- Nothing run. Spec positions hand-derived; build123d calls (Wire from arc + spline + line, Plane.YZ prisms, derive_bay
  placements) not tried.
- Robot is not truly invertible: the rails (45 mm) stand above the wheels (30 mm). Upside down it rests nose-high; it
  relies on the disc kick against the floor to self-right.
- MR63 is a small bearing for a 34 J disc; the brief said bushing; check the shaft and bearing load.
- 3 M3 into the bell carry all the torque; the hole fit is clearance only, so expect slip and wear.
- The balance window is from a numeric notch moment, not a mass-properties run.
- The Revron fork geometry (26 mm tip) was not re-sized for Ripsaw's axle height; the opponent's path from fork to disc
  is not checked.
- Catalogue frame orientations (battery long axis, N10 shaft direction, wheel axis) are assumed in tub.py and drive.py.
- The locking pin position is a placeholder.

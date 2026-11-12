# Scythe - 150 g horizontal undercutter bar spinner (AWS 2025)

> **UNTESTED: never built, run, rendered or verified.** No code in `src/` has been executed. Every number below
> is hand-computed from the `src/scythe/params.py` relations using research/cots/INDEX.md values. Treat all of
> them as estimates.

## Size rule: one setting
- **Default (`RULES = "aws2025"`):** read from `robot/profile.py`. A 150 mm floor square
  (`Profile.footprint_mm`), no overhang at any height, no height limit, 150 g.
- **Optional `rules="aws_v43_cube"`:** a 101.6 mm cube in the start configuration (AWS v4.3, 2b). Select it with
  `params.use_rules(...)`, `variants.set_variants("aws_v43_cube")` or the env variable `SCYTHE_RULES`.
- **Sizing chain** (params.py, all relations):
  - `BAR_L = floor(2 x min(bar_r_mass, bar_r_geom, bar_r_tip))`
  - then `POD_W` (track), `WPN_AXIS_Y` and `TUB_R` follow from `BAR_L`.

| | 150 mm square (default, 2S) | 150 mm square, 3S | 101.6 mm cube, 2S |
|---|---|---|---|
| bar_r_geom (tyres outside the sweep, inside the envelope) | 73.5 (bar across the full 147 mm) | 73.5 | 45 |
| bar_r_mass (150 - 6 g margin - rest) | 58.4 | 38.9 | 64 |
| bar_r_tip (600 mph at full HV) | 129 | 86 | 129 |
| **BAR_L** | **116 (mass limited)** | 77 | 90 (tyre limited) |
| POD_W / track (tyre inner faces) | 52 (POD_W_MIN) | 52 | 83.6 |
| WPN_AXIS_Y | 15.5 | 35.0 | 4.3 |
| Extent W x L (envelope minus margin) | 116 x 142.2 (147) | - | 98.6 x 97.6 (98.6) |

## Architecture
- **Weapon:** 3 mm Hardox 500 two-tooth bar, 116 mm, 16 mm root tapering to 10 mm, bite step on each leading
  edge, laser cut, constant thickness. Spins horizontally **under** the tub, underside 2 mm above the floor. Bolted
  (2x M3) to a turned 7075 hub, which bolts to the GR1507 bell-top screws.
- **Weapon motor:** catalogue `gr1507` (Revron's motor), shaft down, stator screwed up into a 3 mm printed boss
  under the top panel. All fit features come from `revron/weapon_motor.py:describe()`.
- **Drive:** 2WD `bbb_n10_1000rpm` + `bbb_wheel_34x6_5` behind the sweep. The relation `wheel_y()` puts the tyre's
  plan footprint at bar-top height 3 mm outside the sweep circle, so the bar never touches its own tyres. At
  150 mm the track is just the 52 mm pod. Only the cube variant forces a wide track.
- **Front support:** a POM foot on the shaft end on the axis (it spins with the bar) when upright, and a POM dome
  on the top panel when inverted.
- **Invertible:** the body top is at 30 mm and the tyres are 34 mm. Inverted, the bar is at 29-32 mm and works as
  an overhead bar.
- **Electronics** (inside the pod walls): `tattu_2s_300_75c_hv` (variant `gnb_3s_300_80c_hv`),
  `bbb_brushless_esc_20a`, `bbb_malenki_nano` (alt `bbb_dual_esc_v31`), `fingertech_mini_switch` (reached through
  a top-panel key hole), XT30.
- **Chassis:** printed PA tub: a disc (TUB_R = 50) unioned with the rear pod. Sides slope 35 deg. The teeth reach
  8 mm past the rim. 1 mm top panel with Revron-style M2 button screws (`robot/cad/holes.py:hole_tool`).

## Rotating vs fixed
| Rotating (one revolute joint, weapon axis) | Fixed |
|---|---|
| bar, hub, GR1507 bell + shaft, POM foot | tub, top panel, dome, stator, N10s (wheels rotate on their own axes), electronics |

## Load paths
1. **Weapon hit (the bar strikes an opponent):** tooth -> bar root bending (16 x 3) -> 2x M3 shear plus the shaft
   pilot -> hub -> 4x M2 bell-top screws and the shaft -> bell -> motor bearings -> stator -> 4x M2 base screws ->
   3 mm boss -> top panel (tension skin) and the walls.
2. **Hit to the body:** sloped wall -> deflected upward. Tyres are behind the sweep.
3. **Landing:** wheels -> N10s -> pod. Front -> POM foot -> shaft -> axial load on the motor bearings.

## Masters
- **Envelope:** `ENVELOPES` / `RULES`, `FOOTPRINT_MARGIN` 1.5, `MASS_MARGIN` 6.
- **Bar:** `BAR_T` 3, `BAR_W_ROOT` 16, `BAR_W_TIP` 10, `BAR_TOOTH_STEP` 4, `BAR_Z0` 2.
- **Weapon stack:** `GAP_BAR_TUB` 1.5, `HUB_OD` 17, `HUB_H` 5, `BOSS_T` 3, `BAR_BITE_REACH` 8.
- **Body and drive:** `TUB_SLOPE_DEG` 35, `POD_W_MIN` 52, `BAR_TYRE_CLR` 3, `CELL_HV_V` 4.35.
- **Mass:** `MASS_OTHER_G` (the table below).

## Mass budget (estimate, g, 150 mm default, 2S)
| Item | g | Source |
|---|---|---|
| Bar (1434 mm^2 x 3 x 7.85e-3) | 33.8 | bar_mass_g |
| gr1507 | 19.6 | INDEX.md |
| 2x bbb_n10_1000rpm | 16.0 | INDEX.md |
| 2x bbb_wheel_34x6_5 | 8.2 | INDEX.md |
| tattu_2s_300_75c_hv | 16.0 | INDEX.md |
| bbb_brushless_esc_20a | 5.0 | INDEX.md |
| bbb_malenki_nano | 2.3 | INDEX.md |
| fingertech_mini_switch | 2.15 | INDEX.md |
| XT30 | 1.5 | estimate |
| 7075 hub | 3.0 | estimate |
| Screws + heat-sets | 3.5 | estimate |
| Wires | 4.0 | estimate |
| Tub (PA12, 60 % solid) | 19.0 | estimate |
| Top panel, 1 mm PA-CF | 8.0 | estimate |
| Skids | 0.5 | estimate |
| Allowance (`Profile.allowance_g`) | 1.2 | profile.py |
| **Total** | **143.8** | margin 6.2 g (the bar is sized to leave `MASS_MARGIN`) |
With 3S the pack is 28 g, so the relation shortens the bar to 77 mm (21.8 g), for a total of about 143.8 g.

## Energy (estimates)
- I = 1/12 m L^2 = 1/12 x 0.0338 x 0.116^2 = **3.79e-5 kg m^2** (the taper is ignored)
- rpm = 0.8 x kV x V with kV 2850
- **2S HV full, 8.7 V:** 19 840 rpm, w = 2077 rad/s, **E = 1/2 I w^2 = 82 J**, tip 120 m/s (270 mph, under 600)
- 2S nominal, 7.6 V: 17 330 rpm, E = 62 J
- 3S (77 mm bar, 13.05 V): 29 750 rpm, I = 1.08e-5, E = 52 J, tip 268 mph. **This is less than 2S**, because the
  pack mass comes out of the bar. 2S is the default.
- Cube variant (90 mm, 2S): E = 37.5 J
- Bite at 2 m/s closing and 19 840 rpm: 2000 / (2 x 331) = **3.0 mm**
- Gyro: the spin axis is vertical, so turning produces no gyroscopic lift.

## Why it beats Revron (robots/revron/params.json, README)
- Revron has 31 g of 40 mm discs. As a disc, I is about 6.2e-6 kg m^2, giving about 13 J at the same rpm.
- Scythe has about 6x Revron's energy (82 J) with roughly the same steel mass, because the mass sits at a 58 mm
  radius.
- Scythe attacks at 2 mm (wheels, forks, skirt hinges) where Revron's vertical drisk can't reach.
- There is no gyroscopic penalty, and it still fights inverted.
- It uses the same motor, catalogue fit code, fasteners and electronics.

## Risks
- **Self-destabilising hits:** the reaction from 82 J hits will throw or spin a 144 g 2WD robot.
- **Bar hitting the floor:** the gap is only 2 mm. Seams, a lost foot or a bent bar make it gouge. `BAR_Z0` is a
  master that can go up.
- **Shaft bending:** the M5 shaft is cantilevered below the bearings, and a 116 mm bar gives longer lever hits
  than Revron's discs. Mitigation: the dead-shaft variant (a fixed M5 12.9 bolt with the bar and hub on MR85
  bearings). This is not modelled.
- **Long spin-up:** I is about 6x Revron's on a 19.6 g motor. Check the ESC current and the spin-up time.
- **Hub clash:** the bell-top screw circle may clash with the bar M3 PCD (11 mm).
- **Rule voltage:** `CELL_HV_V` 4.35 exceeds `Profile.max_cell_v` 4.2. Confirm whether LiHV is allowed.

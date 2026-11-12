# Scythe - 150 g horizontal undercutter bar spinner (AWS 2025)

> **UNTESTED: never built, run, rendered or verified.** No code in `src/` has been executed. Every number
> below is an estimate from `src/scythe/params.py` formulas and research/cots/INDEX.md values.

## Size rule
The robot must fit fully inside a **101.6 mm (4 in) cube** in its start configuration (AWS rules v4.3, 2b). This is
the master `CUBE = 101.6`. The 150 mm `footprint_mm` in `robot/profile.py` is superseded and is not used for sizing.
- The geometric upper bound on the bar is the cube floor diagonal: `BAR_L_GEOM_MAX = CUBE*sqrt2 - BAR_DIAG_MARGIN`
  = 143.7 - 8 = 135.7 mm. **A bar longer than `BAR_L_SQUARE` = CUBE - 2*1.5 = 98.6 mm must be parked on the
  diagonal at the start.**
- The binding limit is our own tyres. Wheels touch the floor, so they cannot sit inside the sweep circle in the
  bar plane. They must sit outside it, inside the cube. A wide track (tyre inner faces at x = +-41.8) with the
  axis pushed to the front (`WPN_AXIS_Y = CUBE/2 - margin - BAR_L/2` = 4.3) gives the largest bar of **90 mm**
  (`BAR_L_TYRE_MAX`).
- At 90 mm the bar fits the cube in **any** clocking, so diagonal parking is not needed. If the drive is ever
  moved out of the bar plane (for example a raised drive on a tall chassis), the bar can grow to 135.7 mm parked
  diagonally.
- Fit check (estimate): width 2 x (45.05 + 3.25 + 1) = 98.6 mm. Length from the bar tip (y = 49.3) to the tyre
  back (y = -31.3 - 17 = -48.3) = 97.6 mm. Height 31 mm. All of these fit inside 101.6 with the 1.5 mm margin.
  This is checked by the asserts in `params.check()`, which have not been run.

## Architecture
- **Weapon:** 3 mm hardened steel (Hardox 500) two-tooth bar, 90 mm tip to tip, 16 mm root tapering to 10 mm,
  bite step on each leading edge, laser cut, constant thickness. Spins horizontally **under** the tub, underside
  2 mm above the floor. Bolted (2x M3) to a turned 7075 hub, which bolts to the GR1507 bell-top screws.
- **Weapon motor:** catalogue `gr1507` (Revron's motor), **shaft down**, stator screwed up into a printed boss
  under the top panel. All fit features come from `revron/weapon_motor.py:describe()`.
- **Drive:** 2WD `bbb_n10_1000rpm` + `bbb_wheel_34x6_5`, wide track, behind the sweep. The relation
  `params.wheel_y()` puts the tyre's plan footprint at bar-top height 3 mm (`BAR_TYRE_CLR`) outside the sweep
  circle. The tub disc (r = 37 mm) is inside the sweep and the teeth reach 8 mm past it.
- **Front support:** a turned POM foot on the shaft end on the axis (it spins with the bar) when upright, and a
  POM dome on the top panel when inverted.
- **Invertible:** the body top is at 30 mm and the tyres are 34 mm. Inverted, the bar sits at 29-32 mm and works as
  an overhead bar.
- **Electronics** (all inside the pod walls): `tattu_2s_300_75c_hv` (variant `gnb_3s_300_80c_hv`),
  `bbb_brushless_esc_20a`, `bbb_malenki_nano` (alt `bbb_dual_esc_v31`), `fingertech_mini_switch` (reached through a
  key hole in the top panel), XT30.
- **Chassis:** printed PA tub: a disc on the weapon axis unioned with the wide rear pod (83.6 mm, between the
  tyres). Sides slope 35 deg so verticals glance off. 1 mm top panel with Revron-style M2 button screws
  (`robot/cad/holes.py:hole_tool`).

## Rotating vs fixed
| Rotating (one revolute joint, weapon axis) | Fixed |
|---|---|
| bar, hub, GR1507 bell + shaft, POM foot | tub, top panel, dome, stator, N10s (wheels rotate on their own axes), electronics |

## Load paths
1. **Weapon hit (the bar strikes an opponent):** tooth -> bar root bending (16 x 3 section) -> 2x M3 in shear plus
   the shaft pilot bore -> hub -> 4x M2 bell-top screws (torque) and the shaft (radial) -> bell -> motor bearings
   -> stator -> 4x M2 base screws -> 3 mm boss -> top panel (tension skin) and the walls.
2. **Hit to the body:** sloped wall -> deflected upward. Tyres are behind the sweep at the pod corners.
3. **Landing:** wheels -> N10s -> pod walls. Front -> POM foot -> shaft -> axial load on the motor bearings.

## Masters (params.py)
`CUBE` = 101.6, `FOOTPRINT_MARGIN` = 1.5, `BAR_DIAG_MARGIN` = 8, `BAR_L_TYRE_MAX` = 90 (`BAR_L` = 90),
`BAR_T` = 3, `BAR_W_ROOT` = 16, `BAR_W_TIP` = 10, `BAR_TOOTH_STEP` = 4, `BAR_Z0` = 2, `GAP_BAR_TUB` = 1.5,
`HUB_OD` = 17, `HUB_H` = 5, `BAR_BITE_REACH` = 8, `TUB_SLOPE_DEG` = 35, `WHEEL_BOSS` = 1, `POD_L` = 24,
`BAR_TYRE_CLR` = 3, `TOP_PANEL_T` = 1, `BOSS_T` = 3.
Derived: `WPN_AXIS_Y`, `POD_W`, `TUB_R`, `wheel_x()`, `wheel_y()`, `overall_extent()`, `bar_mass_g()`,
`bar_moi_kgm2()`, `energy_j()`, `bite_mm()`, `check()`.

## Mass budget (estimate, g)
| Item | g | Source |
|---|---|---|
| Bar (1096 mm^2 x 3 mm x 7.85e-3) | 25.8 | params.bar_mass_g |
| gr1507 | 19.6 | INDEX.md |
| 2x bbb_n10_1000rpm | 16.0 | INDEX.md |
| 2x bbb_wheel_34x6_5 | 8.2 | INDEX.md |
| tattu_2s_300_75c_hv | 16.0 | INDEX.md |
| bbb_brushless_esc_20a | 5.0 | INDEX.md |
| bbb_malenki_nano | 2.3 | INDEX.md |
| fingertech_mini_switch | 2.15 | INDEX.md |
| XT30 pair | 1.5 | estimate |
| 7075 hub | 3.0 | estimate |
| Screws + heat-sets | 3.5 | estimate |
| Wires | 4.0 | estimate |
| Tub, PA12 at 60 % solid (wide pod) | 17.0 | estimate |
| Top panel, 1 mm PA-CF (about 6000 mm^2) | 6.5 | estimate |
| Skids (POM) | 0.5 | estimate |
| Glue, tape, solder (`Profile.allowance_g`) | 1.2 | profile.py |
| **Total, 2S** | **132.3** | margin **17.7 g (11.8 %)** |
| **Total, 3S** (pack 28 g instead of 16 g) | **144.3** | margin 5.7 g (3.8 %) |

## Energy (estimates; formulas in params.py)
- I = 1/12 m L^2 = 1/12 x 0.0258 x 0.090^2 = **1.74e-5 kg m^2** (the taper is ignored)
- rpm = 0.8 x kV x V with kV 2850
- 2S HV full, 8.7 V: 19 840 rpm, w = 2077 rad/s, **E = 1/2 I w^2 = 37.5 J**, tip 93 m/s (209 mph)
- 2S nominal, 7.6 V: 17 330 rpm, E = 28.7 J
- 3S HV, 13.05 V: 29 750 rpm, w = 3116 rad/s, **E = 84 J**, tip 140 m/s (314 mph, under the 600 mph rule)
- Bite = v_close / (teeth x rev/s): at 2 m/s and 19 840 rpm, 2000 / (2 x 331) = **3.0 mm**
- Gyro: the spin axis is vertical, so turning (yaw) produces no gyroscopic lift. The drive is unaffected.

## Why it beats Revron (robots/revron/params.json, README)
- Revron has 31 g of 40 mm discs. As a disc, I is about 6.2e-6 kg m^2, so it stores about 13 J at 19 840 rpm.
  Scythe stores about 37 J on 2S, roughly 2.8x, and about 84 J on 3S, which fits the mass budget (estimates).
- Scythe attacks at 2 mm: wheels, forks and skirt hinges that a vertical drisk cannot reach.
- There is no gyroscopic penalty, and it still fights inverted.
- It reuses the same motor, catalogue fit code, fasteners and electronics.

## Risks
- **Self-destabilising hits:** the horizontal reaction spins or throws a light 2WD robot. The wide track helps.
- **Bar hitting the floor:** the gap is only 2 mm. Seams, a lost foot or a bent bar make it gouge. Mitigation: the
  foot sits on the axis, and `BAR_Z0` is a master that can go up.
- **Shaft bending:** the M5 shaft is cantilevered below the bearings. Mitigation: the dead-shaft variant (a fixed
  M5 12.9 bolt from the top panel, with the bar and hub on two MR85 bearings from `weapon_motor.pick_bearing(5.0)`).
  This is not modelled.
- **Tight cube fit:** the width is 98.6 mm against a 98.6 mm limit (zero slack inside the margin). Measure the
  wheels and bosses before printing.
- The bell-top screw circle may clash with the bar M3 PCD (11 mm). Spin-up is slow on a 19.6 g motor.

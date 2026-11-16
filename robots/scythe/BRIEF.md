# Scythe - 150 g horizontal undercutter bar spinner (AWS 2025)

> Verified: `robot verify robots/scythe/spec.json` -> **0 blockers, 0 parity blockers** (237 warnings).
> Not yet built or fought; printed-part masses are model-derived estimates.

## Size rule: one setting
- **Default (`RULES = "aws2025"`):** 150 mm floor square, no overhang at any height, no height limit, 150 g
  (`robot/profile.py`).
- **Sizing chain** (params.py, all relations): `BAR_L = 2 * min(bar_r_mass, bar_r_geom, bar_r_energy,
  bar_r_tip, bar_r_pitch)` rounded down to 1 mm -> **57 mm** (energy/pitch limited: the cantilevered undercutter
  must stay under the 20 J spinner escalation threshold and clear the floor at a 5 deg nose-down hop);
  `POD_W` (track, master `POD_W_MIN` 70), `WPN_AXIS_Y` 45 and `TUB_R` 20.5 follow from `BAR_L`.

| | 150 mm square, 2S (default) |
|---|---|
| BAR_L | 57 (energy/pitch limited) |
| POD_W / track | 70 |
| WPN_AXIS_Y | 45.0 |
| Extent W x L | 80.5 x 85.75 (footprint 85.75 mm, well inside 150) |
| Mass (model) | 114.6 g |
| Stored energy | 9.0 J at bar rpm (cap 18 J, spinner threshold 20 J) |

## Architecture
- **Weapon:** 3 mm Hardox two-tooth bar, 57 mm, spinning horizontally **under** the tub (nut top at z 4, floor
  bore r13). Motor-as-hub: the `bl_1806_stator` flange is screwed up through the printed boss and top panel
  (4x M2 on the 16 mm flange circle); the `bl_1806_can` bell carries the rotor, and the motor's own 3 mm
  shaft (`wshaft`, press fit in the bell core) runs down through hub and bar to an M3 clamp nut. An MR83ZZ
  (`wbearing`) in the boss bore is the rotor's second support: outer race press-fit in the boss (seat on the
  stator flange face), inner race a slide fit on the shaft.
- **Drive:** 2WD `bbb_n10_1000rpm` + `bbb_wheel_34x6_5` behind the sweep, nested against the pod walls at
  (+-21.75, 31.25, 17); the wheel boss clamps the pod wall between itself and the gearbox face (U-slot axle
  holes open at the top so the motors drop in from above). Cradle pads + side ribs locate each N10.
- **Front/rear support:** two printed skid pads at the pod rear (bottom z 0.2) join the wheels in the stance
  polygon; the wheels alone carry the robot on the floor.
- **Invertible:** wheels (34 mm) protrude above the body top (30 mm) and below the floor.
- **Electronics** (inside the pod): 2S 300 mAh HV pack in the rear bay (strap + velcro), `bbb_brushless_esc_20a`
  on the floor, `bbb_malenki_nano` under the panel, `fingertech_mini_switch` mid-pod under a panel key hole.
- **Chassis:** printed PA tub: sloped disc (15 deg) over the bar unioned with a vertical-wall rear pod
  (70 mm wide), motor housing tube (bore r13) rising from the floor bore, boss ring (r4..14) to the panel,
  4 diagonal wire slots (45/135/225/315 deg) through boss + tube + panel, panel posts, 1 mm PA-CF top panel
  on 8x M2 button screws.
- **Weapon lock:** a 3 mm pit pin through the panel/floor lock hole (r 1.6 at x 17) and the bar's lock hole
  rests on the floor slab - a pit tool, made safe outside the robot with the XT30 unplugged.

## Rotating vs fixed
| Rotating (one revolute joint on the weapon axis) | Fixed |
|---|---|
| bar, weapon_hub, wshaft, shaft_nut, weapon_motor_bell | tub, top_panel, stator, wbearing, N10s (wheels on their own axes), electronics |

## Load paths
1. **Weapon hit:** tooth -> bar root -> 2x M2.5 csk (shear) + shaft pilot -> hub -> clamped bell cap face /
   shaft press fit -> bell -> motor bearings -> stator -> 4x M2 into the printed boss -> top panel (tension
   skin) + walls.
2. **Hit to the body:** sloped disc wall (15 deg) deflects upward. Tyres sit behind the bar sweep.
3. **Landing:** wheels -> N10 shafts -> gearbox faces -> pod wall (clamped); skid pads take the rear.

## Masters (params.py)
- **Envelope:** `FOOTPRINT` 150, `FOOTPRINT_MARGIN` 1.5.
- **Bar:** `BAR_T` 3, `BAR_BOLT_D` 2.5 (M2.5 csk x2 on r7.5), `BAR_LOCK_X` 17, `BAR_LOCK_D` 3.2.
- **Weapon stack:** `BOSS_ID_R` 4 (MR83ZZ seat), `BOSS_OD_R` 14, `BOSS_T` 3, `BEARING_*` (MR83ZZ 3x8x3),
  `SHAFT_D` 3, `HUB_OD_R` 11.5, `HUB_H` 5, `MOTOR_BELL_CLR` 1.5 (housing bore r13 = hub r11.5 + 1.5).
- **Wire slots:** `SLOT_ANGLE_DEG` 45 (+ the other three diagonals), `WIRE_SLOT_IN_R` 2 (merges into the boss
  bore), `WIRE_SLOT_OUT_R` 20, `WIRE_SLOT_W` 5.5, `WIRE_SLOT_TUBE_Z0` 12 (internal channel down the tube wall
  for the phase lead).
- **Body and drive:** `TUB_SLOPE_DEG` 15, `TUB_WALL` 1.5, `POD_W_MIN` 70 (jiggle-measured: bell clears each N10
  by 2.57 mm, kin.rub_gap needs 1.0), `N10_*`, `CRADLE_*`, `RELIEF_*` (annular-sector motor reliefs),
  `SKID_PAD_*`, `WHEEL_D` 34.

## Mass budget (model-derived, g)
Bar + hub + shaft + nut + bell ~ 20; stator 6.5; 2x N10 16; 2x wheels 8.2; pack 16; ESC 5; rx 2.3; switch
2.15; tub + panel + fasteners + wires ~ 40. **Total 114.6 g** (limit 150 g).

## Energy
- I ~ 1/12 m (L^2 + W^2) with the 57 mm bar; rpm from kV 2300 at 2S HV; **E = 9.0 J** at bar rpm - under the
  18 J self-cap and the 20 J escalation threshold, so the cantilevered undercutter stays in the normal class.
- Bite and gyro: vertical spin axis, no gyroscopic lift; the bar clears the floor at the 5 deg hop pitch
  (`PITCH_CLR_MM` 0.3).

## Verification workflow
- `make_spec.py` regenerates `spec.json` from `params.py` (run from the repo root; `SCYTHE_EXPR_SPEC=...`
  also writes an expr-placement variant for the PR #84 param jiggle).
- `robot verify robots/scythe/spec.json` -> 0 blockers; `robot render robots/scythe/spec.json iso
  robots/scythe/renders/iso.png` draws all 7 wires.
- Repairs were driven by the measured solvers: `robot jiggle` part moves (PR #83) and
  `robot jiggle --param <file>:<NAME>=lo:hi:step --write-params` (PR #84) - e.g. `POD_W_MIN` 65 -> 70 from a
  min-gap probe of bell vs N10 (0.64 -> 2.57 mm).

## Risks
- Cantilevered bar on a 3 mm shaft: hit loads bend the shaft; the MR83ZZ second support limits runout, but a
  hard hit on the tooth is still the peak shaft load.
- 114 g leaves 35 g of margin - room for a thicker bar or armour if the arena allows.
- The four diagonal wire slots and the motor-relief sectors remove part of the housing-tube wall; the boss
  still ties the stator to the tension skin through the panel screws.

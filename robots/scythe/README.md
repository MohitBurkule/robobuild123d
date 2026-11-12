# Scythe

**UNTESTED: never built, run, rendered or verified.**

Scythe is a 150 g UK antweight (AWS 2025: 150 mm floor square from robot/profile.py; optional 101.6 mm cube variant) horizontal undercutter. A 116 mm (mass-limited, derived), 3 mm Hardox two-tooth bar spins 2 mm
off the floor under a sloped printed tub. It is driven by a shaft-down GR1507 (Revron's motor). The robot has 2WD
on N10s behind the bar sweep and is invertible: upside down, the bar becomes an overhead bar. Design, load paths,
mass and energy are in [BRIEF.md](BRIEF.md).

Code: `src/build_scythe.py` provides `build(part=...)`, built from `src/scythe/`:

| File | Contents |
|---|---|
| `params.py` | masters and relations |
| `bar.py` | the bar |
| `weapon_hub.py` | the hub |
| `tub.py` | the tub |
| `drive.py` | the drive |
| `skids.py` | the skids |
| `panels.py` | the panels |
| `assembly.py` | the assembly, with joints |
| `variants.py` | the variants |
| `_reuse.py` | loads Revron's `plate.py`, `weapon_motor.py` and `hw.py` |

## Unsure
- The build123d calls were not executed. Several need checking in a session that is allowed to run code:
  - the `Polygon(..., align=None)` call
  - lofting faces through `Plane * Face`
  - `RevoluteJoint.connect_to(angle=)`
  - `Compound(children=)`
- `robot.shapes.place` and `xform.pose` Euler order: `hw.placed` is used for the GR1507 with rot (0, 90, 0), which
  is assumed to turn +X to -Z.
- The format of the `describe()['top_holes']` and `['base_holes']` tuples is read from the code: (r, deg, d).
  Their clash with the bar's M3 circle has not been checked.
- Pockets for the battery, ESC, receiver and switch are not cut yet. `robot/cad/bay.py` should fit them. Their
  `at` values in `spec.json` are null.
- `spec.json` is hand-written and partial. There is no `robot/templates/scythe.json` yet, because it has not been
  confirmed that the template engine can express a horizontal under-bar.
- The masses of the tub, panel, wires and screws are estimates. The energy figures use the thin-bar MOI and
  0.8 x kV x V.
- The size envelope is one setting: `params.RULES`. The default `aws2025` takes 150 mm from
  `robot/profile.py`; `aws_v43_cube` is 101.6 mm. Switching it reloads the module (`params.use_rules`,
  `variants.set_variants`, env `SCYTHE_RULES` / `SCYTHE_BATTERY`). I have not checked that the reload reaches every
  module.
- `BAR_L` = 116, track = 52, axis y = 15.5 and wheels at (+-29.25, -51.72) are hand-evaluated from the relations,
  not computed by running them.
- `CELL_HV_V` 4.35 is above `Profile.max_cell_v` 4.2. Confirm whether LiHV packs are allowed.

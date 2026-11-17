# Scythe Classic

150 g horizontal undercutter for the AWS 2025 rules (150 mm floor square, no height limit). The look is kept: a
sloped printed cone tub, a 1 mm PA-CF top disc, and a vertical rear pod carrying two N10 drive motors on 2 wheels.
Design, load paths and the mass budget are in [BRIEF.md](BRIEF.md). `make_spec.py` writes `spec.json`; edit the
masters in `src/scythe_classic/params.py` and regenerate, never the JSON.

## Status (last verify, this branch)
| tier | blockers | notes |
|---|---|---|
| inner | 3 | `dynamics.spinup_kick`, `physics.runtime`, and `proxy.wiring` before a full wiring re-route (wiring group itself: 0 blockers) |
| full | 35 (27 root causes) | structural: shafts and bearings not modelled, joint topology, wheel drive coverage, motor stator face, weapon `joint` missing |
| `--tier full --only <all groups but visual>` | run without `visual` (it hung last time) | |

Measured mass (verifier): 125.1 g of the 150 g limit.

## Design (from the masters)
- **Bar:** 3 mm steel, 116 mm tip to tip, underside 4.0 mm above the floor (`BAR_Z0`; 0.5 mm tyre squash plus a 3 deg
  seam over the 58 mm reach needs 3.6 mm, `dynamics.floor_margin`). Two M3 countersunk bolts on a 13 mm PCD into the hub,
  countersink 6.2 mm (M3 head 6.0 + 0.1). Rule 5f lock: a removable 3 mm pin through a 3 mm hole in the +X arm at
  r = 20, seated in the tub floor (`lock_pin`, orange, tethered).
- **Hub:** 7075, 1.0 mm washer gap above the bar (the sweep proxy touches it otherwise), 4.5 mm tall, bolts engage 4.5 mm.
- **Weapon motor:** GR1507 shaft down, stator clamped between the top panel and a printed seat plate (pocket ring, ribs to the cone wall) in the tub.
- **Tub:** cone (TUB_R 50, 35 deg slope) with a rear pod 70.8 mm wide. Floor at z = 8.5 (2 mm floor), top panel at
  z = 29.6 to 30.6 (TUB_TOP_Z = 30.6).
- **Drive:** 2 x N10 1000 rpm inside the pod, 34 mm wheels on the outside; wheels behind the sweep.
- **Power:** `lipo_2s_350` (36x17x11, 21.5 g, 350 mAh; the 180 mAh pack failed the 3 min fight). Strapped in the pod
  (`retained: strap`). Switch in the cone interior with a snap cradle (its key hole is in the top panel at
  SWITCH_XY); ESC velcro; RX on the floor (tape); XT30 in the pod rear with a snap holder.
- **Skid:** `skid_foot` is a caster puck on the shaft end on the axis, kind `caster`, 0.5 mm above the floor and
  0.5 mm under the bar. It is the front contact that `ground.pitch_rest` needs (the verifier passes without any
  caster placed elsewhere). It is modelled as riding a bearing on the shaft end; no bearing part exists in the catalogue.

## Not done / open
- Inner tier: `dynamics.spinup_kick` (0.10 N m spin-up beats 0.05 N m tyre grip; see STRUGGLES.md for the ESC key
  mismatch), `physics.runtime` (about 160 s against the 180 s fight: the pack that fits the pod does not carry it on the
  check's peak model).
- Full tier: the 35 blockers above. They need a shaft through the bar, two bearings, a revolute `joint` on the weapon
  group, a driven pulley or motor link for each wheel, and a stator face on the motor. That changes the look and was
  out of scope here.
- Renders in `renders/` were regenerated from this spec (`--no-checks`).

Struggle log: [STRUGGLES.md](STRUGGLES.md).

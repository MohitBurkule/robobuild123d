# Generated Revron-like robot vs the hand-built Revron

**Hypothesis.** The inputs come only from `research/revron_deconstruction.md`; no part of `robots/revron/spec.json` was used. The hypothesis is `weapon=vspin_drisk, front=wedgelets, drive_layout=2WD, transmission=direct, wheel_dia=22, battery=lipo_2s_180`, with an N10 drive, a BE1806 in the drisk, a Malenki Nano and a BBB ESC.

**Spec and result.** The spec is `/mnt/project-files/robot-cad/gen/revron_like.json`. It passes full `robot verify` with 0 blockers at 140.0 g.

**What it leaves out.** The engine cannot yet build the 4WD O-ring belt drive (front F1 tyre, belt groove on the rear hub). The rules also price a 4WD belt build at 153 g, which is over budget, so this hypothesis uses 2WD direct drive. That difference is the biggest architectural gap below.

**Diff command.** The counts come from `python3 -m robot.gen.diff revron_like.json robots/revron/spec.json` (`robot/gen/diff.py`).

| category | count |
|---|---|
| parts added (in Revron, not generated) | 19 |
| parts removed (generated, not in Revron) | 7 |
| moved > 2 mm | 16 |
| rotated > 2° | 6 |
| reshaped | 17 |
| material / process changed | 10 |
| fasteners | 39 |
| wires | 0 |
| connections | 24 |
| **total** | **138** (11 architectural, 127 detail) |

## Architectural changes (11)

- **Belts and front wheels (7):** Revron adds `belt_l` and `belt_r`, `wheel_fl` and `wheel_fr`, and four pulley hubs `whub_*`.
- **Top armour (1):** Revron adds a separate `top_armour` part.
- **Chassis halves (1):** Revron joins its two chassis parts with screws, where the generated clamshell uses an interlock.
- **Drisk to motor (1):** Revron screws the drisk to the motor can, where the generated drisk is a keyed press fit.
- **Rear wheels (1 entry):** Revron puts its rear wheels on pulley hubs, with no direct wheel-on-motor fit.

## Top gaps and the engine work that would close each

1. **4WD O-ring belt drive (belts, front wheels, pulley hubs, about 20 changes).**
   - Add a `drive.add_belt_4wd` generator. It would build:
     - rear hubs with a groove, pressed onto the N10;
     - front hubs turning on standoff axles;
     - the O-ring belt, sized from the centre distance.
   - Make `transmission=belt` buildable.
   - Re-price `budget.py`: Revron shows that 4WD belt fits in 148.9 g, so the 153 g estimate is pessimistic.
2. **Chassis architecture (structure parts moved, reshaped, rejoined, 17 material changes).**
   - Revron is an open tub with a screwed base panel, and the uprights are bolted on with M3 aluminium standoffs.
   - The engine only makes a two-half clamshell with uprights printed in place.
   - Add a `chassis_style` axis (`clamshell` | `tub_base_panel`) and a standoff-module front (uprights + standoffs + wedgelets).
3. **Fasteners (39).**
   - Revron uses M3 standoffs, aluminium nuts pressed into hex pockets, and countersunk M2 screws into a base panel.
   - The engine uses heat-set inserts everywhere.
   - Add hardware choices per joint (insert / press nut / standoff) to the shell and front generators.
4. **Weapon stack (`disc_f`, `spacer`, `prop_mount`, `bspacer` added).**
   - Revron's drisk is two Hardox discs with a spacer and a prop mount, carried on a bearing at both ends.
   - The engine makes a single steel disc with a solid hub.
   - Add a `disc_count` parameter and the spacer/prop-mount stack to `weapon_drisk.py`.
5. **Materials (10).**
   - Revron uses PLA-ST for its prints, TPU for the wedgelets and forks, rubber tyres and Hardox discs.
   - The engine uses nylon, titanium forks and PLA wheels.
   - Make the material choice per part a hypothesis axis, with the rule set checking each choice against the verifier's material table.
6. **Front.**
   - The hypothesis asked for wedgelets, but the drisk module still builds its own titanium forks.
   - Revron's wedgelets are TPU and slide over the front standoffs.
   - `add_front` should honour `front=wedgelets` for the drisk.

The wire count is 0: both robots wire the same parts together.

Renders are in `/mnt/project-files/robot-cad/gen/renders/`: `revron_compare_{iso,side}.png` (generated on the left, real Revron on the right), plus `revron_like_*` and `revron_real_*`.

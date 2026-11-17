# Expandabot: build spec

Parametric build123d design and verification spec for **Expandabot** (*Expanda-bot*), Adam Stanley's 8-time Antweight World Series champion (AWS 64, 67, 69, 70, 71, 72, 74, 76) from **Team Bits Everywhere**.

## What it is
A 150 g UK antweight from **Team Bits Everywhere** (Adam Stanley), styled after Team Lobster's *Robot Wars* heavyweight **Thermidor 2**. It is a two-wheeled, rear-hinged flipper and horizontal clamping pincer robot:
- **Central rear-hinged flipper (`flipper`):** 2 mm polycarbonate front scoop hinged on the front deck (`hinge_pin`) on a 3-knuckle hinge (`tub` outer knuckles + `hinge_block` centre knuckle). Driven by an SG90-class servo (`servo_cs07`) via a printed horn (`horn`) and steel pin (`drive_pin`) bearing on the hinge block's tail lever. Fires upward (`+42°` travel) to launch opponents captured between the claws.
- **Flanking clamping pincers (`clamp_l`, `clamp_r`):** Mirrored 2 mm polycarbonate lobster-claw wedge arms bolted to the tub's sloped front mounts via 3 × M2 button screws into brass heat-set inserts per side (`0.45 mm` front tip height). The claws funnel opponents onto the central flipper scoop while supporting the front stance.
- **Two-wheel drive (`wheel_l`, `wheel_r`) & side guards (`side_l`, `side_r`):** Rear-positioned Ø26 × 8 mm TPU tyres driven directly on the D-shafts of two N10 micro-metal gearmotors (`n10_300rpm_6v`) housed in snug closed-top pockets, guarded outboard by 2 mm polycarbonate side plates on four printed standoff columns per side.

See [`REFERENCE.md`](REFERENCE.md) for the full source table and `SEEN-IN-PHOTO` vs `GUESS` breakdown.

## Rules
- `RULE_ERA = "aws_2025"` (default): fits inside the 150 mm floor square with no overhang at any height and weighs <= 150 g (`robot/profile.py` `aws2025`).
- `RULE_ERA = "aws_v4_3"`: fits inside the historical 101.6 mm (4 in) start cube in any orientation (`100.5 × 96.0 × 26.0 mm`).

## Frame
Follows `robot/GUIDE.md` and `robot/checks/combat_ground.py`:
- **+X:** Left (`wheel_l`, `side_l`, `clamp_l`, `lid_l` on `+X`; `wheel_r`, `side_r`, `clamp_r`, `lid_r` on `-X`)
- **+Y:** Forward (front scoop lip and claw tips at `+Y`; rear wheels toward `-Y`)
- **+Z:** Up (floor at `Z = 0`)

## Masters (`src/expandabot/params.py`, `MASTERS` block)
| Name | Value | Basis |
|---|---|---|
| `OVERALL_L × OVERALL_W` | `98.0 × 96.0 mm` | PHOTO proportions, GUESS scale (fits 101.6 mm v4.3 cube & 150 mm aws2025 square) |
| `FLIPPER_SHARE` | `0.305` of length | PHOTO: front weapon / claw run as a share of `OVERALL_L` |
| `WHEEL_D × WHEEL_W` | `26.0 × 8.0 mm` | PHOTO/GUESS: rear foam/TPU wheels standing `2.05 mm` proud of floor/lid |
| `SHEET_T / LID_T` | `2.0 / 1.5 mm` PC | GUESS: polycarbonate side plates, flipper, claws, and split top lids |
| `FLIP_OPEN_DEG` | `42.0°` | GUESS: usable flipper travel before tail approaches servo tray |
| Catalogue IDs | `n10_300rpm_6v` ×2, `servo_cs07`, `lipo_2s_180`, `malenki_nano`, `switch_bbb_ant_rvrn2` | GUESS choice, CAT dims |
| `WALL`, `CLEAR`, `RUN_CLEAR` | from `robot/cad/bay.py` | STD |
| Fasteners | M2 button/socket + brass heat-set inserts (`heatset_m2`) | STD |

## Parts as manufactured
| Part | Qty | Process | Notes |
|---|---|---|---|
| `tub` | 1 | FDM PLA (`+z`) | Open top shell with servo tray, 2 snug closed-top N10 motor pockets, battery & ESC bays (`bay.derive_bay`), switch tray, 2 outer hinge knuckles, sloped front clamp mounts (3 × M2 heat-sets per side), 8 side-plate standoff columns, and lid pads with M2 heat-sets |
| `lid_l` / `lid_r` | 2 | 1.5 mm PC, laser | Top lids covering the left/right electronics zones; `lid_l` carries the horn slot and `lid_r` carries the rounded switch actuator slot |
| `side_l` / `side_r` | 2 | 2.0 mm PC, laser | Mirrored hexagonal side guard plates mounted outboard of the rear wheels on 4 standoff columns per side |
| `clamp_l` / `clamp_r` | 2 | 2.0 mm PC, laser | Mirrored lobster-claw clamping arms bolted to the sloped front mounts (3 × M2 into heat-sets per side) |
| `flipper` | 1 | 2.0 mm PC, laser | Central flipper blade between the lobster claws, sloping from the front hinge to the tip |
| `hinge_block` | 1 | FDM PLA (`+z`) | Centre hinge knuckle, flipper seat (2 × M2 into heat-sets), and full-width tail lever with downward shield skirt driven by the servo horn pin |
| `horn` | 1 | FDM PLA (`+x`) | Servo horn with hub, arm, and drive-pin tab |
| `wheel_l` / `wheel_r` | 2 | FDM TPU (`+x`) | Ø26 × 8 mm grippy TPU wheels with D-bore on the N10 output shafts |
| `hinge_pin`, `drive_pin` | 2 | COTS steel | M2 hinge pin and M2 drive pin |

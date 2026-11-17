# Expandabot (Team Bits Everywhere — Adam Stanley)

Parametric `build123d` CAD model and verifier spec for **Expandabot** (*Expanda-bot*), Adam Stanley's 8-time Antweight World Series champion (AWS 64, 67, 69, 70, 71, 72, 74, 76) from **Team Bits Everywhere**.

See [`REFERENCE.md`](REFERENCE.md) for the online research record, photo/wiki sources, and the strict `SEEN-IN-PHOTO` vs `GUESS` breakdown.

## Overview
Expandabot is a 150 g UK antweight two-wheeled clamp- and rear-hinged flipper robot styled after the *Robot Wars* heavyweight **Thermidor 2**:
- **Drive:** 2WD rear axle (`n10_300rpm_6v` micro-metal gearmotors driving Ø26 × 8 mm TPU wheels `wheel_l` / `wheel_r`), protected outboard by 2 mm polycarbonate hexagonal side guard plates (`side_l` / `side_r`) mounted on four printed standoff columns per side.
- **Primary Weapon (Rear-Hinged Flipper):** A 2 mm polycarbonate front-scooping central flipper (`flipper`) hinged at the front of the chassis deck (`hinge_pin`) on a 3-knuckle hinge (`tub` outer knuckles + `hinge_block` centre knuckle). Driven by an SG90-class servo (`servo_cs07`) via a printed horn (`horn`) and steel pin (`drive_pin`) bearing against the hinge block's tail lever. Fires upward (`+42°` travel) to launch opponents captured between the claws.
- **Flanking Clamping Pincers (`clamp_l`, `clamp_r`):** Mirrored 2 mm polycarbonate lobster-claw wedge arms bolted to the tub's sloped front seats via 3 × M2 button screws into brass heat-set inserts per side (`0.45 mm` floor tip clearance), corralling opponents onto the central flipper scoop while supporting the front stance.
- **Serviceability & Electronics:** One-piece 1.5 mm polycarbonate top lid (`lid`) screwed into 4 × M2 brass heat-set inserts allows drop-in access to the 2S 180 mAh LiPo (`lipo_2s_180`), Malenki-Nano ESC/Rx (`malenki_nano`), and BBB antweight switch (`switch_bbb_ant_rvrn2`, accessible through the elongated switch travel slot in `lid`).

## Frame Convention
Follows the repository standard (`robot/GUIDE.md` & `robot/checks/combat_ground.py`):
- **+X:** Left (lateral; `wheel_l` and `clamp_l` on `+X`, `wheel_r` and `clamp_r` on `-X`)
- **+Y:** Forward (front flipper scoop lip and claw tips at `+Y`, rear hinge and wheels toward `-Y`)
- **+Z:** Up (floor at `Z = 0`)

## Commands
Regenerate `spec.json` from `src/expandabot/params.py`:
```bash
python robots/expandabot/make_spec.py
```

Build STEP assembly and per-part STLs directly:
```bash
python robots/expandabot/src/build_expandabot.py
```

Run the verifier:
```bash
python -m robot verify robots/expandabot/spec.json --tier inner --llm
python -m robot verify robots/expandabot/spec.json --llm
```

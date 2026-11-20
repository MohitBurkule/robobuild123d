# Verty Little Secret: full rebuild description from the reference photos

Source photos (three):
- `robots/verty_little_secret/reference/verty_little_secret.aws72.webp` (1305 × 1079 px): AWS 72. Camera at the **front-left**, about 35° down. The forks point to the image lower left. The weapon motor is a **red/black BE1806-2300** with its white label readable.
- `robots/verty_little_secret/reference/verty_little_secret.aws74.webp` (1238 × 801 px): AWS 74. Camera at the robot's **left side / rear-left**, about 30° down. The forks point to the image right. This build has **gear-toothed wheels** and a **red/black motor labelled "...HOBBY"** on a black mount plate with four socket screws.
- `robots/verty_little_secret/reference/verty_little_secret.aws76.webp` (1705 × 1129 px): AWS 76. Camera at the **front-left**, about 30° down, like 72. The motor is a **gold/black BE1806-2300**. An **ON/OFF sticker** sits beside the switch.

All three photos are cut out onto white. The dark parts carry a **strong green cast**, and the metal edges look bright green; the real colours are **black printed parts** and steel.

**Verty Little Secret is a small two-pod vertical spinner.** Two separate black **side pods** each carry:
- a drive wheel at the rear outer corner;
- two **printed forks** at the front;
- an **inner upright** with a **curved shark-fin horn** on top.

Between the pods, a **BE1806 outrunner** lies along X. Its bell carries a compact **two-toothed steel weapon** (Ø ≈ 44) that spins in the gap between the pods. The shaft end is held in the opposite pod by a **bearing and a nyloc nut**.

Facts are read from the photos; inferences are marked **(guess)**. Sizes are **estimates in mm**, from:
- the AWS limits (150 g, 101.6 mm cube);
- the **BE1806 motor** (can Ø 23, about 18 long, stator body to 26 long with mount) as the main scale;
- the **M3 nuts (5.5 AF)** on the fork bolts;
- the spec draft (pods 70 × 45 × 22 profile, a bridge 30 × 25 × 22, wheels r 12 × 8, weapon r 22, forks ending near y 94, motor r 9 × 24 at y 8, z 14).

Ratios are against **W = overall width ≈ 100**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the gap between the pods, at the weapon axis's Y.
- **+X** = robot right, **+Y** = forward (fork tips), **+Z** = up. mm.
- In 72 and 76 (camera front-left), robot right is the **image left pod**, which carries the motor. In 74 (camera at the left side), the near pod is the robot's left pod.
- Extents (reconciled §12):
  - pods x ∈ ±[13, 50], y ∈ [−36, +18], z ∈ [3, 25];
  - weapon axle along X at (y +2, z 23) (reconciled §13);
  - weapon swept r 21;
  - horns to z ≈ 44;
  - forks from y +18 to y +52, at the floor;
  - wheels at (±44, −24, 13).

| ID | Part |
|---|---|
| PD-L, PD-R | left and right side pods (black printed boxes) |
| LD-L, LD-R | pod lids: flat plates, chamfered, each with 2 large-washer screws |
| UP-L, UP-R | inner uprights of the pods (weapon supports), each crowned by a horn |
| HN-L, HN-R | curved shark-fin horns on top of the uprights |
| BR | bridge joining the pods behind/under the weapon (hidden; spec) |
| MW | BE1806-2300 outrunner along X (gold/black or red/black), stator on UP-R |
| MP | motor mount plate (74: black plate with 4 socket screws around the shaft) |
| WP | weapon rotor: 2 stacked steel plates with crescent cut-outs and 2 hooked teeth |
| BG / NY | bearing boss in UP-L with an M4/M3 nyloc nut on the shaft end |
| FK-L1, FK-L2, FK-R1, FK-R2 | four printed forks, 2 per pod, at the pod fronts |
| B-FK | 2 M3 bolts + nuts per fork through the pod front wall |
| WH-L, WH-R | drive wheels (ribbed black tyres in 72/76; spur-gear-toothed wheels in 74) |
| EH | hexagonal outer end faces of the pods with an access hole |
| SW | switch with an ON/OFF sticker (76) / red link plug (72) on the left pod top |
| S-x | lid screws with washers |
| M-L, M-R, BAT, ESC, WESC, RX | hidden motors and electronics |

---

## 1. Overall description in one paragraph

Verty Little Secret is a **compact black vertical spinner built as two side pods**. Each pod is a boxy printed module about 37 wide, 54 deep and 22 tall:
- a **sloped hexagonal outer end** with a round access hole;
- a **drive wheel** set into a notch at its rear outer corner (Ø 26, ribbed black tyre or a gear-toothed printed wheel);
- a **flat lid** held by two large-washer screws;
- at the front, **two narrow printed forks**, each bolted through the front wall with two M3 bolts and nuts, sloping down to sharp points about 34 mm ahead.

The pods face each other across a **26 mm gap**. On the inner side of each pod, an **upright** rises to carry the weapon axle at about 17 mm height, topped by a **curved backward-sweeping horn** about 20 mm tall.

In the gap, a **BE1806 outrunner** (Ø 23) is bolted to the right pod's upright. Its bell carries a **small steel rotor** (Ø ≈ 44) made of two stacked plates with crescent cut-outs, giving **two hooked teeth**. The shaft passes into a bearing in the left upright and is locked with a **nyloc nut**. The robot's power switch sits on the left pod beside the nut, with an ON/OFF sticker.

---

## 2. Part-by-part description

### 2.1 Pods (PD-L, PD-R)
- **Shape**: each pod is a printed shell, about **37 (X) × 54 (Y) × 22 (Z)**, x from ±13 (inner face) to ±50 (outer end), y −36 to +18, z 3 to 25.
- **Plan**: a rectangle with a **notch at the rear outer corner** for the wheel (about 14 × 30). The **outer end** is a **hexagonal prism face**: its upper and lower edges are chamfered at about 35°, so the end looks like a flattened hexagon in front view (76 (1240–1460, 640–830): the right pod's (robot left) outer end with a **Ø 10 round hole**).
- **Front face**: vertical, about 22 tall. Two **fork roots** stand on it, each with **two M3 bolts** whose threaded ends and nuts stick out of the front (76: (230–270, 545–585), (385–440, 585–640), (820–870, 680–730), (1025–1075, 760–810)).
- **Material**: black PLA/PETG with fine lines and a **diagonal infill texture** on the lids. Some layer delamination is visible on the front-right pod's lower edge in 74 (300–600, 560–600).

### 2.2 Lids (LD-L, LD-R)
- **Shape**: flat plates about **33 × 50 × 2**, inset in the pod tops. The inner front corner is **chamfered/stepped** into a V where the lid meets the upright (76 (300–480, 290–480)).
- **Screws**: **two** per lid, **M3 button or pan heads with large flat washers** (Ø 10), at the front inner and rear outer corners (76: (230, 420), (1170, 650), (1130, 290); 72: (150, 375), (900, 290), (950, 680)).

### 2.3 Uprights (UP-L, UP-R) and horns (HN-L, HN-R)
- **Uprights**: the inner walls of the pods rise as **rounded bosses**, about **8 thick (X) × 30 long (Y)**, to **z ≈ 28**. The top is a semicircle of r 11 about the axle (y +2, z 17).
  - The left upright (image right in 72/76) has a **black bearing boss** with the **nyloc nut** visible (76 (850–960, 330–420); 72 (690–760, 380–450)).
  - The right upright (image left) carries the motor stator: 74 shows a **black mount plate** about 30 × 30 × 3 with **four socket screws** on a 16 mm square and a central bearing/shaft hole (74 (600–770, 220–360)).
- **Horns**: one on each upright, a **curved fin** about **4 thick × 14 wide at the base × 20 tall**, sweeping **back** (a shark fin: straight front edge, concave rear edge, pointed tip). They stand at y ≈ −4, z 25 to 45, at x ±15 (76 (700–780, 45–230), (990–1070, 90–300); 72 (550–610, 85–200), (815–870, 125–270); 74 (350–440, 120–220), (480–560, 30–130)).
- **Static, not weapon**: the horns are in the same place in all three photos while the weapon is at different angles, so they are fixed parts of the uprights. (In 74 the right horn appears to be the outer face of the motor mount plate, extended up.)

### 2.4 Weapon motor (MW) and mount (MP)
- **MW**: a **BE1806-2300** outrunner (the white label "BE1806-23…" is readable in 72 and 76). It is **Ø 23 × 18** (can) plus the stator base, **26 long** overall, lying **along X** in the gap with its base on the right upright and its **bell facing left**. Can colours: **red** (72), **gold** (76), red with a "HOBBY" logo (74, a different brand: "Racerstar/…Hobby" class) (guess).
- **MP**: the mount plate seen in 74. The stator screws into it with 4 M2/M2.5 screws. Read as the inner face of UP-R (it may be a separate printed plate) (medium).

### 2.5 Weapon rotor (WP)
- **Material**: **two steel plates**, each about **2 mm thick**, black (painted/oxidised) with **bright edges**, stacked on the bell with a gap of about 4 mm between them, or **one plate plus a printed spacer** (guess).
- **Outline (each plate, in YZ)**:
  - a **disc of r ≈ 16**;
  - with **two crescent cut-outs** (concave arcs of r ≈ 10 cut into the rim at 180° apart);
  - each cut leaves a **hooked tooth** that rises to r ≈ 22, its tip curving forward in the spin direction, like a claw (76 (620–870, 160–600): plate edges with crescent notches; 72 (520–700, 270–580)).
- The **plates are clocked** about 90° apart (76 shows a tooth at the top and another at the lower front), giving **four strikes per revolution** across the two plates, or two per plate (guess).
- **Hub**: bolted to the bell face (the BE1806's prop adapter thread/M5 nut, or the bell's M2 holes).
- **Swept circle**: r 22 about (y +2, z 17), giving a lowest point **z −5**, which is below the floor. **Conflict → §13.**

### 2.6 Bearing and nyloc (BG, NY)
- The motor shaft (Ø 5 prop shaft or a through-bolt) runs into **a flanged bearing** in UP-L. It is retained by a **silver nyloc nut** (M5 or M4, about 8 AF, with a blue/white nylon insert visible in 76 (880–960, 340–410); 72 (700–760, 395–450)).
- **Purpose**: supports the bell end so the weapon is held at both ends.

### 2.7 Forks (FK)
- **Shape**: **printed tapered prongs**, about **36 long × 8 wide (root) → 3 (tip) × 6 thick**. The root is a **vertical tab** 14 tall that sits against the pod front wall, with **two M3 bolts** through it. The prong slopes down at about **25°** to a **chisel point** on the floor.
- **Plan**: two forks per pod at x ≈ ±18 and ±40 (the inner fork near the gap, the outer near the end). They are parallel and point straight forward. In 74 the forks splay slightly outward.
- **Surface**: rough top layers, with **chewed and frayed tips** in 76 (the left fork tips (60–200, 700–870)).
- **Count**: 4 forks, 8 bolts with nuts.

### 2.8 Wheels (WH)
- **72 / 76**: **Ø 26 × 10**, a **black ribbed tyre** (about 36 transverse ribs, 1 mm deep) on a **black hub** with **lightening holes / spoke cut-outs** (72 (1115–1255, 350–560): the hub shows a Y-shaped spoke pattern).
- **74**: **printed spur-gear-profile wheels**, about **Ø 30 × 8** with about **50 teeth** (the "gear wheels" in 74 (60–310, 360–560), (520–690, 30–80)). Fine teeth are used as grip ribs. The hub has two kidney holes.
- **Position**: in the rear outer notch of each pod, axis along X at **(±44, −24, 13)**, tyre bottom on the floor. The tyres stick up **about 4 mm above** the lid level, so the robot can drive inverted.

### 2.9 Outer end faces (EH)
- The **hexagonal end** of each pod ahead of the wheel. It has a **Ø 10 round hole**, either the drive motor's rear end showing / a cooling hole, or a hole for a hex key to reach a wheel grub screw (76 (1330–1450, 720–830); 74 (400–470, 640–710)).

### 2.10 Switch (SW)
- On the **left pod** top near the upright:
  - in 76, a **slide switch** with a **steel mounting plate** (2 screw ears) and a **red/green ON-OFF sticker** (76 (960–1100, 300–520));
  - in 72, a **red 2-pin link plug** (a removable link) (72 (750–800, 360–490)).

### 2.11 Bridge (BR, hidden)
- The pods must be joined. The spec puts a **bridge 30 × 25 × 22** behind the weapon at y −22.5. In the photos the gap under and behind the motor is dark, so a **bridge at the rear** (y −36 to −14, below the motor) is likely (medium). In 74 a **slotted top bridge** with a rectangular opening and wires shows behind the motor (74 (450–700, 300–400)).

---

## 3. Per-view descriptions

### 3.1 Front-left iso (72, 76)
- Two dark boxes with a gap between them. The motor's coloured can lies across the gap, with the label facing up. The weapon plates are on the left of the gap (robot left), against the nut boss.
- Two shark-fin horns stand up above the gap.
- Four forks reach toward the viewer, with bolts through the pod fronts.
- Wheels at the rear outer corners; the left pod's hexagonal end with its hole.

### 3.2 Left side iso (74)
- The near (left) pod with a gear-toothed wheel at the rear. The pod's top with the slotted bridge and wires.
- The motor mount plate with 4 socket screws, the red motor can and the weapon behind it. The horns, the far pod's gear wheel.
- The forks to the right.

### 3.3 Front view (inferred)
- Two 37 wide pods, 22 tall, a 26 gap. Forks as eight bolt-nut points and four prongs. The weapon's teeth showing in the gap between z 0 and 39. The horns rising to z 45.

### 3.4 Top view (inferred)
- Two rectangles with wheel notches at the rear outer corners. The motor 26 long across the gap at y +2. The weapon as a thin bar (two plates) in the gap. The horns as small fins. The forks reaching forward 34 mm from the pod fronts.

### 3.5 Rear view (inferred)
- The pods' rear walls, the wheels at the outer corners, the bridge in the middle, the horns sweeping back toward the viewer.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| PD | box with hex end and wheel notch | 37 × 54 × 22 | 0.37 × 0.54 × 0.22 | black PLA | — | 2 |
| LD | plate | 33 × 50 × 2 | — | black | 2 washer screws | 2 |
| UP | boss | 8 × 30 × 28 | — | black | integral | 2 |
| HN | curved fin | 4 × 14 × 20 | 0.20 tall | black | integral | 2 |
| MW | BE1806 outrunner | Ø 23 × 26 | 0.23 | gold/red/black | 4 screws to MP | 1 |
| WP | 2 claw plates | Ø 44 × 2 each | 0.44 | steel | to bell | 2 |
| NY | nyloc nut | M5, 8 AF | — | steel | on shaft | 1 |
| FK | tapered prong | 36 × 8 × 6 (+14 tab) | 0.36 | black PLA | 2 × M3 + nut | 4 |
| WH | ribbed / gear wheel | Ø 26 × 10 (Ø 30 × 8 in 74) | 0.26 | black PLA/TPU | drive shaft | 2 |
| BR | bridge | 26 × 22 × 10 | — | black | screws/integral | 1 |
| SW | slide switch / link | 12 × 6 | — | — | plate + 2 screws | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| WH ↔ floor | contact | 0 |
| FK tips ↔ floor | contact | 0 |
| PD bottom ↔ floor | clearance | 3 |
| WP teeth (r 22) ↔ floor | clearance | 1–2 (after §13) |
| WP ↔ UP-L inner face | clearance | 1.5 |
| MW can ↔ UP-R | screwed (stator) | 0 |
| MW bell ↔ WP | bolted | 0 |
| WP tips ↔ HN | clearance (the horns sit outside the swept disc in X) | 2+ |
| WP ↔ BR | clearance (the bridge sits behind the swept circle) | 3 |
| FK tab ↔ PD front | bolted (2) | 0 |
| LD ↔ PD | screwed | 0 |
| WH ↔ PD notch | clearance | 1.5 |

---

## 6. Mechanism

1. **Drive**: two wheels at the **rear outer corners**, skid steer. The forks drag at the front. The centre of mass sits between the wheels and the forks, which keeps the forks loaded on the floor.
2. **Weapon**: the BE1806 (2300 kV) on 3S spins at up to about **25,000 rpm unloaded**, realistically 18,000.
   - The rotor (two plates Ø 44, about 2 × 8 g = 16 g) has I ≈ ½·0.016·0.018² ≈ 2.6 × 10⁻⁶ kg·m² (plus the bell, about 0.4 × 10⁻⁶).
   - At 18,000 rpm (1885 rad/s): E ≈ ½·3 × 10⁻⁶·1885² ≈ 5.3 J. Tip speed ≈ 41 m/s.
   - Small but fast: a "little secret" hidden between the pods.
3. **Spin direction**: the hooked teeth curl toward the front-top in 76, so the front of the weapon moves **upward** (uppercut) (guess, medium).
4. **Forks**: lift and present the opponent to the weapon in the gap. The four forks set the robot's front at floor level across its whole width.

---

## 7. Assembly order (suggested rebuild)

1. Print the two pods (the right pod with the motor-mount upright; the left with the bearing boss), the bridge, the lids, the four forks and the wheels.
2. Fit the drive motors (N20 or N10) in the pods along X, with shafts out to the wheel notches. Fit the wheels.
3. Fit the electronics: battery in the right pod (guess); ESCs and receiver in the left pod with the switch.
4. Join the pods with the bridge (screws through the inner walls).
5. Bolt the BE1806 stator to the right upright (4 screws). Bolt the claw plates to the bell. Pass the shaft into the left upright's bearing. Fit the nyloc.
6. Bolt the forks on (2 M3 bolts + nuts each).
7. Screw on the lids.

---

## 8. Hidden / uncertain list
- How the pods are joined (bridge position and shape).
- The weapon plates' exact outline and whether there are one or two.
- The drive motor type and wiring between the pods (wires must cross the gap via the bridge).
- The hole in the hexagonal end face.
- Sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin on the floor under the gap centre, at the axle's Y. +X right, +Y forward, +Z up. mm.
- Pods x ±[13, 50], y [−36, +18], z [3, 25]. Uprights x ±[13, 21], top z 28.
- Axle along X at (y +2, z 23) (reconciled §13). Motor x [−13, +13] → base at +13 (right upright), bell at −1. Weapon plates x ≈ −4 and −9.
- Horns at (±15, −4, 28–48). Forks from (±18/±40, +18, 14) to (±18/±40, +52, 0). Wheels (±44, −24, 13).

## 10. Profiles as math

**10.1 Weapon plate (YZ, polar about the axle).**
- Base disc r 16.
- Two teeth at θ₀ = 0° and 180°. Each tooth's outer edge is an arc of r 22 for θ ∈ [θ₀ − 30°, θ₀]. Then the hook tip is a 40° point.
- A crescent cut-out follows: a circle of r 9 centred at r 20, θ₀ + 25°, removed from the plate. This makes the concave throat in front of each tooth.
- Bore Ø 5. Thickness 2. Two plates, clocked 90°.

**10.2 Horn (YZ, extruded 4).**
- Front edge: straight from (y +4, z 28) to (−8, 48).
- Rear edge: concave arc of r 18 centred (y −22, z 36) from (−10, 28) to the tip.
- Tip r 1.

**10.3 Pod end (XZ).** A hexagon about x ∈ [37, 50], with z: z = 3 + (50 − x)·0.7 for the lower chamfer and z = 25 − (50 − x)·0.7 for the upper chamfer, over x ∈ [43, 50]. Hole: circle r 5 at (x 50, y +4, z 13).

**10.4 Fork (YZ).** Prong top edge: z = 14 − 0.41·(y − 18) for y ∈ [18, 52]. Width w(y) = 8 − 5·(y − 18)/34. Root tab z ∈ [3, 17], 4 thick.

**10.5 Wheel (74 gear type).** r(φ) = 15 − 0.6·(1 − cos(50φ)).

## 11. Pixel-based measurements

- **76 (1705 × 1129)**:
  - motor can (gold band + black body): (480–640, 190–540); can Ø ≈ 160 px tall in the image;
  - weapon plates (620–870, 160–600);
  - horns (700–780, 45–230), (990–1070, 90–300);
  - pods: right (robot) (130–700, 140–690), left (770–1560, 250–1000);
  - forks: (60–360, 490–880), (720–1000, 640–1090);
  - fork-bolt nut ≈ 45 px across.
- **72 (1305 × 1079)**: motor (360–560, 220–520), Ø ≈ 145 px. Nut (690–760, 380–450). Pods: (60–520, 70–620), (600–1260, 270–790). Forks (40–320, 450–760), (570–830, 620–1000).
- **74 (1238 × 801)**: mount plate (600–770, 220–360). Gear wheel (60–310, 360–560).

## 12. Several independent estimates of key sizes

| Quantity | Method A (known part / spec) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Scale (76) | BE1806 can Ø 23 | — | 160 px / 23 = 7.0 px/mm | 7 px/mm (mid) |
| Scale check | M3 nut 5.5 AF | — | 45 px / 5.5 = 8.2 px/mm (nearer the camera) | consistent |
| Weapon Ø | 44 (spec r 22) | 1.9 × can | 76: 440 px / 7 ≈ 63 (includes both plates offset in perspective) → 44–50 | **44** |
| Gap between pods | motor length 26 | 0.26 W | 72: (520 → 600 at the upright faces) ≈ 80 px / 5.5 ≈ 15 (muddled by overlap; see §13) | **26** |
| Pod width X | 45 (spec) | 0.37 W | 76: right pod outer end to upright ≈ 380 px along X (foreshortened) / 7 / cos ≈ 38 | **37** |
| Pod depth Y | 70 (spec) | 0.54 W | 72: 400 px / 7 ≈ 57 | **54** |
| Height | 22 (spec) | — | 76: front wall 150 px / 7 ≈ 21 | **22** |
| Horn height | — | 0.2 W | 76: 190 px / 7 ≈ 27 incl. the upright top | **20 above the upright** |
| Fork length | 64 (spec 30 → 94) | — | 76: 330 px / 8 ≈ 41 (foreshortened, slope) | **36** |
| Wheel Ø | 24 (spec) | — | 72: 210 px / 7.5 ≈ 28 | **26** |

## 13. Consistency check: conflicts and reconciliation
1. **Gap pixel estimate**: the 72 gap measurement is muddled by the motor overlapping the near upright in perspective. The motor (26 long) must fit between the uprights, so the **gap is 26–28**. Use 26.
2. **Weapon floor clearance**: with the axle at z 17 and r 22, the teeth reach z −5. So **the axle is at z ≈ 24** or the weapon is r 16 at the teeth.
   - The uprights' top is at z ≈ 28 and the bearing boss centre sits about 8 below the top, so **axle z ≈ 21**. The teeth then reach **z −1**, which is still too low.
   - **Reconciled**: **axle z 23, weapon r 21**, giving clearance 2. The uprights rise to z 32 (the bosses look taller than the pods in 76, consistent).
   - The motor can (r 11.5) then spans z 11.5 to 34.5, which matches 72/76 where the can's top is level with the horn bases.
3. **Spec forks to y 94**: too long for the cube; the reconciled 36 mm forks from y 18 give a total length of −36 to +52 = **88**. This fits.
4. **Width**: pods ±50 → 100. This fits inside 101.6 with the wheels inside the notches (the tyre's outer face at x ±49).
5. **Mass**: §16 totals about 148 g.

---

## 14. Why the designer did it (per part, adversarial first)

- **Two separate pods with the weapon between**
  - Fight: the weapon is **recessed** inside the robot's footprint, protected on both sides by the pods and in front by the forks. Opponents can only reach it by being lifted onto it, which is the job of the forks. The pods are **independent modules**: a destroyed pod can be swapped, and the wide stance resists the vertical spinner's tendency to tip on gyroscopic turns.
  - Threats: the gap is an opening for a vertical spinner or a drum to reach the weapon from above or the motor from the front. The horns guard the top.
- **Small, fast weapon (Ø 44 on a BE1806)**
  - Fight: a small rotor at high rpm gives a lot of hits per second and spins up fast (under 1 s), which suits a robot that must hit, back off and re-hit. The hooked teeth bite under an opponent's front edge after the forks have lifted it.
  - Threats: low stored energy (about 5 J) means it will not knock out heavy robots in one hit. Weapon-to-weapon hits can stall it.
- **Weapon held at both ends (motor on one upright, bearing and nyloc on the other)**
  - Construction: a single BE1806 bearing system cannot take side impacts. The outboard bearing stops the bell from being bent off the stator. The nyloc does not shake loose.
- **Shark-fin horns**
  - Fight: they stop a vertical spinner from reaching straight down into the gap and protect the motor can from top hits. When inverted they act as **self-righting points / skids** that lift the robot's top off the floor so the wheels (which protrude above the lid) touch.
  - The backward sweep lets opponents slide off rather than catch.
- **Four printed forks bolted through the front**
  - Fight: the forks win "getting under" contests at the front. Four of them across the width mean no wedge can slip between them without hitting a fork, and anything lifted slides up straight into the weapon's path in the gap.
  - Bolted with two M3 bolts each, they are sacrificial and quick to change (the 76 tips are chewed). Printed forks are lighter than steel but less sharp, which is a compromise for the 150 g budget.
- **Wheels at the rear outer corners, in notches**
  - Fight: the wheels sit behind the forks and inside the pods' footprint, partly covered by the hexagonal end faces. They protrude above the lids so the robot drives both ways up. The gear-tooth wheels (74) were probably an experiment in grip.
- **Hexagonal chamfered ends**
  - Fight: the chamfers deflect side hits from horizontal spinners up or down rather than square on.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 (or N10) gearmotors along X | 12 × 10 × 24 | (±32, −24, 13) | medium |
| Battery | 3S 300 mAh LiPo | 45 × 17 × 13 | right pod (+32, −8, 12) along Y | medium |
| Weapon ESC | 12–20 A BLHeli | 22 × 12 × 5 | right pod (+28, +10, 10) | medium |
| Drive ESC + receiver | combo board | 25 × 15 × 6 | left pod (−32, −4, 10) | medium |
| Switch | slide switch / link | 12 × 6 × 6 | left pod (−22, +6, 22) | high |
| Bridge | printed block with a wire channel | 26 × 22 × 10 | (0, −25, 8) | medium |
| Bearing | 5 × 10 × 4 flanged (MR105) | Ø 10 | left upright (−17, +2, 23) | medium |
| Wires | battery/ESC/motor crossing via the bridge; motor phases on the right side | — | — | high |

## 16. Mass budget (est. g)

| Item | Mass |
|---|---|
| BE1806 motor | 19 |
| Weapon plates × 2 + bolts | 18 |
| Pods × 2 + lids + bridge | 40 |
| Forks × 4 + 8 bolts/nuts | 12 |
| Drive motors × 2 + wheels | 24 |
| Battery 3S 300 | 24 |
| ESCs + receiver + switch | 10 |
| Wires + screws + nyloc + bearing | 6 |
| **Total** | **≈ 153** |

This is just over 150; a 2S pack or lighter infill fixes it. So the weapon is a small fraction of the mass. The design favours armour (two thick pods), forks and drive.

## 17. Variant notes
- **72**: red-can BE1806; ribbed tyres with Y-spoke hubs; a red link plug instead of a slide switch; the weapon plates' crescents and teeth clearly visible; neat forks.
- **74**: a red-can motor of a different brand on a separate mount plate with 4 socket screws; printed **gear-toothed wheels** (Ø 30, about 50 teeth); a top bridge with a cut-out showing wires; slightly splayed forks; delamination at the front-right pod's lower edge.
- **76**: gold-can BE1806; ribbed tyres; a slide switch on a steel plate with an ON/OFF sticker; fork tips chewed; motor mount side the same as 72.
- The mirrored-looking motor mount in 74 is most likely the camera angle (we see the inner face of the far upright through the gap) rather than a mirrored build (medium).

## 18. Matchups
- **Vs wedges**: four forks at floor level make the front hard to get under. If a wedge gets past the forks, it is lifted directly into the weapon. From the side, the pods' hexagonal ends present a chamfer, but a low wedge can get under the 3 mm clearance.
- **Vs horizontal spinners**: the pods' outer ends take the hits. The wheels sit in notches behind the end faces, protected from the front but exposed from behind.
- **Vs vertical spinners/drums**: the horns and forks meet the opponent's weapon first. Verty's own weapon is low-energy, so it does better hitting the opponent's sides after manoeuvring.
- **Vs pushers/control bots**: the forks and the fast weapon combine: a lifted pusher gets chewed underneath. The wide stance resists being turned.

## 19. Wear reading
- Chewed fork tips (76): fork-on-fork and floor wear.
- Scuffed lid edges and a slightly cracked inner lid corner (76 (300–480, 280–330)).
- Weapon plates' edges bright: sharpened or worn.
- Replaced motors (red → gold) and wheels (ribbed → gear → ribbed) across events: these were the parts that failed or were experimented with.

# Pingu: full rebuild description from reference photos

Source photo (cut out onto white by the AWS wiki):
- `robots/pingu/reference/pingu.aws72.webp`: AWS 72, 1427 × 1160 px. Camera at the robot's **front-right, high**: about **35–40° above the floor** and about **35–40° round from the front toward the right side**. The front (orange forks) points to the **lower-left**, the right side faces the **lower-right**. Moderate perspective (forks nearest the camera look larger). Visible: the whole front (front wall, all eight orange forks), the right side plate's outer face, the top (white lid, all four wheels' tops), the left side plate's top/front edge. Not visible: left side outer face, rear wall, underside.

**User notes (authoritative)**: the robot has **8 forks**, **2 of them long**, and they are **hinged**; the **wheels are not outside the body** (they sit inside the side plates). The photo agrees: eight orange forks hang from a hinge row, the 3rd and 6th (counting from the robot's left) are much longer, and the wheels are inboard of two full-length black side plates.

Only one photo exists, so the left side, rear and underside are inferred by symmetry and function. Facts are read from the photo; inferences are marked **(guess)**. Dimensions are **estimates**. Scale: the AWS 150 g / 101.6 mm cube, the **M2 button-head lid screws** (head Ø ≈ 3.8 mm), the wheel (Ø ≈ 26 mm TPU), and the kit draft (`kit.json`: wedge, body 80 × 84 × 30, ramp 32, 4 wheels r 12 × 9 at y −28 and +20, forks n 6 [should be 8], length 34, width 10, spread 68, tilt 22°, a 56 × 44 × 2 lid at (0, −12, 33)). Ratios are given against **W = overall width ≈ 84 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the fork tips), **+Z** = up. Units mm.
- **Origin O** = floor point under the centre of the body (mid-width between the side plates' outer faces, mid-length of the side plates' bottom edges excluding forks).
- In the photo +Y points lower-left (about 30° below horizontal), +X points lower-right (about 25° below horizontal), +Z up.
- Forks numbered **F1…F8 from the robot's left (−X) to right (+X)**. In the image F1 is at the upper-left of the row and F8 at the lower-right next to the right side plate.

| ID | Part |
|---|---|
| CH | central chassis tub (black, between the wheel wells) |
| SP-L, SP-R | black side plates (outer walls, wedge-shaped at the front) |
| FW | black front wall (inclined), between the side plates |
| HR | hinge row at the foot of FW (black knuckles + hidden pin) |
| KN | black hinge knuckles/spacers between forks (7 inner + 2 end) |
| HP | hinge pin (hidden, along X) |
| F1, F2, F4, F5, F7, F8 | six short orange hinged forks |
| F3, F6 | two long orange hinged forks |
| PK | recessed pocket on each short fork's top |
| LID | white lid plate |
| S-LID | four black M2 button-head screws in the lid |
| GAP | slot between the lid's front edge and FW (electronics visible) |
| WH-FL, WH-FR, WH-RL, WH-RR | four black TPU treaded wheels (inside) |
| WW | wheel wells (spaces between CH and SP) |
| H-SP | holes and screws in the side plates |
| M (×4 or ×2) | drive gearmotors (hidden) |
| BAT, ESC, RX, SW | electronics (hidden; red/black wires glimpsed) |

---

## 1. Overall description in one paragraph

Pingu is a **four-wheel-drive wedge robot with a "comb" of eight hinged forks**. Its body is a **black printed box about 84 mm wide, 75 mm long and 30 mm tall**, closed at each side by a **full black side plate** whose front part extends forward and slopes down to the floor like a sledge runner, so that the two side plates frame the front like the cheeks of a dustpan. Between the side plates at the front stands a **black inclined front wall** (about 25 mm tall, leaning back about 15°), and from a **hinge row at its foot** hang **eight orange printed forks**, each about **7.5 mm wide**, separated by **black hinge knuckles**. Six forks are **short (about 26 mm)** with a **recessed rectangular pocket** on top; two (the **3rd and 6th**) are **long (about 46 mm)** with a **stepped (two-tier) profile**, reaching about 20 mm beyond the others. The forks rest on the floor by gravity and can swing up individually over obstacles (hinged wedgelets). On top, a **white lid** (about 56 × 44 mm) with **four black screws** sits between **four black treaded wheels (Ø ≈ 26 mm)** that run in **wheel wells inside the side plates**; the wheel tops stick up a few millimetres above the side plates. A gap at the lid front shows **red and black wiring** inside.

---

## 2. Part-by-part description

### 2.1 Side plates (SP-L, SP-R)
- **Shape**: flat **black plates about 3.5–4 mm thick** (x from ±38 to ±42), each with a **side profile like a sledge/trapezoid**:
  - **Bottom edge**: on the floor (z ≈ 0.5–1) from the rear at about **y −40** to the front tip at about **y +40**.
  - **Top edge**: roughly **horizontal at z ≈ 28** from the rear (y −40) forward to about **y +8** (just above the front wall's top), slightly lower than the wheel tops.
  - **Front edge**: a **straight slope** from (y +8, z 28) down and forward to the tip at (y +40, z 1): about **40°** from the floor (35–45°). The front edge face is a 4 mm wide band (the plate thickness), visible on both plates, slightly rounded/chamfered at the outer corner.
  - **Rear edge**: vertical (guess; rear not seen), with the rear corner at (y −40, z 0–28).
- **Top edge texture**: the top edges are **rough and slightly melted/frayed** (the photo shows ragged black strands along the right plate top edge): stringing or wear from wheel/opponent contact, or the plate top was printed facing up with a poor top layer.
- **Outer face (SP-R)**: flat with visible print texture (fine diagonal lines) and **four features** (H-SP):
  - A small **black screw head** (Ø ≈ 3.5 mm) near the rear-top, about **(+42, −22, 22)** (native px (1215, 445)).
  - A **round hole Ø ≈ 3.5 mm** below/behind it, about **(+42, −28, 15)** (px (1240, 525)): the **rear wheel axle/motor shaft support** or a motor clamp screw (guess).
  - Two **holes Ø ≈ 5 mm** near the front-bottom, about **(+42, +8, 13)** and **(+42, +12, 7)** (px (1095, 760), (1065, 830)): the **front motor/axle** and the **hinge pin end** respectively (guess, medium). A small screw head also sits near the top front at about (+42, +4, 24) (px (1065, 590)).
- **SP-L**: mirror image (only its sloping front edge and the inside are seen).

### 2.2 Front wall (FW)
- **Shape**: a black plate about **76 mm wide** (spanning between the side plates, x ±38), **3 mm thick**, from the hinge row at about **z 6** up to **z 28**, **leaning back** about **15°** from vertical (its top edge at y ≈ +6, its bottom at y ≈ +12). Fine **horizontal layer lines** across it (printed upright).
- The top edge of FW is flush with the side plates' top and slightly above the lid's front edge.
- A thin **horizontal groove/seam** about 3 mm below its top (px (300–950, 380)) marks a separate top lip or a layer change.

### 2.3 Hinge row (HR), knuckles (KN), pin (HP)
- At the foot of FW, along X at about **(y +13, z 4)**, a row of **cylindrical black knuckles**, each about **Ø 6 × 1.5–2 mm** wide, alternate with the forks' own (orange) hinge barrels. Visible: one black knuckle between every pair of forks (7) plus end knuckles at both side plates (2): **9 black knuckles**. They are part of the chassis (printed with FW) or separate spacers on the pin (guess: printed as fingers of the FW/floor).
- **Hinge pin HP**: hidden, about **Ø 2 mm steel rod** (or M2 threaded rod / filament), running the full inner width (about 80 mm) through the knuckles and fork barrels, its ends held in the side plates (the lower front hole on SP-R).

### 2.4 Short forks (F1, F2, F4, F5, F7, F8)
- **Shape**: orange printed (PLA/PETG, bright orange-red) **wedge blades**, each about **7.5 mm wide (X)**, **26 mm long (Y)** from the hinge axis to the tip, with:
  - A **hinge barrel** at the rear (Ø ≈ 6 mm, 7.5 wide, coaxial with HP).
  - A **top surface** sloping from the barrel top (z ≈ 6.5) down to a **thin front tip** (z ≈ 0.5) at a **slope of about 12°** relative to the floor when the fork rests on its tip; the fork's underside is flat and rests at about **22°** to the hinge line (kit tilt 22°).
  - A **recessed pocket (PK)** on the top: a rectangle about **3.5 mm wide × 14 mm long × 1 mm deep**, centred, with a **rounded rear end and squared front end**, leaving a **2 mm rim** around it. Lightening/flex, or a print-layer save (guess).
  - A short **front bevel** (the last 4 mm): a slightly steeper flat at the tip (visible as a light line across each fork near the tip).
  - The front tip is straight across, about **0.5 mm** thick.
- **Gaps**: forks are separated by the black knuckles, gap about **1.5 mm** between adjacent forks.

### 2.5 Long forks (F3, F6)
- **Shape**: same width (7.5 mm) and barrel, but about **46 mm long** (tip about **20 mm beyond** the short forks' tips). The top has **no pocket**; instead it shows **fine transverse ribs** (print lines) and a **two-tier stepped profile**:
  - **Rear tier**: from the barrel, a thick section (about 5 mm thick) sloping gently down for about **24 mm**.
  - **Step**: a short steeper ramp (about 45°, about 2 mm drop) at about 26 mm from the hinge.
  - **Front tier**: a thinner blade (about 2.5–3 mm thick at its root) tapering to a thin front tip over the last **18–20 mm**, the last 4 mm bevelled.
- **Position**: F3 is the 3rd from the robot's left, F6 the 3rd from the right: **symmetric** about the centre line at about **x = −13.5 and x = +13.5**.
- **Purpose**: they reach out ahead of the comb to get under and **lift** an opponent first (the long lever tips it), and to **catch** it; they also act as long probes when the robot turns.

### 2.6 Fork positions (centre lines)
- With pitch 9.0 mm and the row centred: F1 −31.5, F2 −22.5, F3 −13.5, F4 −4.5, F5 +4.5, F6 +13.5, F7 +22.5, F8 +31.5. Outer edges of F1/F8 at ±35.25, leaving about **2.75 mm** to the side plate inner faces (±38) for the end knuckles.
- Short fork tips at about **y +38** (hinge y +13 + 26 × cos 12°... ≈ +38); long fork tips at about **y +57**.

### 2.7 Lid (LID) and screws (S-LID)
- **Shape**: a **flat white plate** about **56 mm (X) × 44 mm (Y) × 2 mm**, with **slightly rounded corners** (r ≈ 2), sitting on top of CH between the four wheels at **z 28–30**, centred at about (0, −14). Its front edge is about 5 mm behind FW; its rear edge near the rear of the side plates (y ≈ −36).
- **Material**: white printed (matt, slightly grainy) or white plastic sheet (styrene/PVC, guess low).
- **Screws**: **4 black M2 button-head socket screws** (head Ø ≈ 3.8), one near each corner, about 4 mm in from the edges: at about (±24, −33) and (±24, +5). Seen at native px (655, 158), (475, 290), (1105, 305), (955, 458).

### 2.8 Front gap (GAP)
- Between the lid's front edge and FW, a **slot about 40 mm wide × 5 mm deep** reveals the interior: a **black rectangular component** (connector or ESC), **red and black wires**, a small **white/cream part** (switch body or connector) (px (590–800, 350–440)). This is probably the **switch/link access** or simply a cable gap (guess).

### 2.9 Wheels (WH ×4) and wheel wells (WW)
- **Shape**: **Ø ≈ 26 mm × 8–9 mm wide**, black **TPU** with **straight axial ribs** (about 36 ribs, 1 mm tall) on the tread; the face has a **raised rim** about 2 mm wide and a **recessed centre** with a **hub boss** (Ø ≈ 8).
- **Positions (centres)**: front wheels at about **(±31, +2, 13)**, rear wheels at about **(±31, −30, 13)** (wheelbase ≈ 32 mm). Wheel outer faces at x ≈ ±35.5, i.e. **inside** the side plates (inner face x ±38) with about **2.5 mm** clearance. Wheel tops at **z ≈ 26–27**; they appear to stick up **a little above the side plates' top edge** near the rear of the photo because the plate top is slightly lower there (z ≈ 25) (medium).
- **Wells (WW)**: the space between the central tub CH (outer faces at x ≈ ±26) and the side plates, about **12 mm wide**, open at the top. A **black horizontal cylinder** lies between front and rear right wheels at about (+31, −14, 18) (px (1100, 390)): possibly a **motor body or an axle/spacer** (guess).

### 2.10 Central tub (CH)
- **Shape**: a black box between the wheel wells, about **52 mm wide (x ±26) × 72 mm long × 28 mm tall**, closed by the lid; the front wall FW joins it and the side plates via a floor plate and cross members (guess). Probably one print with the side plates and floor (or the side plates screw onto it; the screws on SP-R suggest **bolted side plates**, medium).

---

## 3. Per-view sections

### 3.1 The photo view (front-right, high)
- **Lower-left half**: the comb of eight orange forks hanging from the black hinge row at the foot of the black front wall; the two long forks (F3, F6) sticking out further toward the lower-left; the left side plate's sloping front edge running from FW's top-left down to the floor at the far left (px (295, 300) → (60, 720)).
- **Upper middle**: the white lid with 4 black screws, the dark gap with wires in front of it.
- **Right**: the right side plate's outer face (front edge from px (1030, 580) down to the tip at (850, 1090), rear end at (1390, 415)), its holes and screws; the two right wheels sticking up above it; the two left wheels at the top-left behind the lid.

### 3.2 Top view (synthesised)
- An 84 × 80 rectangle (side plates to their tips at y +40), the white 56 × 44 lid centred toward the rear, four wheels in 12 mm wells along both sides, FW across the front at y +6…+12, the comb of 8 forks (pitch 9) from y +13 to +38 with F3/F6 to +57.

### 3.3 Right side view
- The side plate as a **flat-topped sledge** shape: 28 tall, 80 long at the floor, the front 32 mm sloping at 40° to the tip; wheel tops just showing above; the forks hidden behind the plate except the long ones' tips sticking out ahead of the plate tip (+57 vs +40).

### 3.4 Front view
- Two side plates (4 mm) at the outer edges, the inclined FW between them, the hinge row at its foot, the 8 fork tips at the floor; wheels hidden behind FW; lid and wheel tops above.

### 3.5 Rear and underside (not photographed)
- Rear: flat black rear wall (guess), wheels visible in the wells, probably the switch. Underside: flat floor about 1 mm above the ground, four wheel contact patches, fork tips at the front.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| SP | sledge-profile plate | 80 × 28 × 4 | 0.95 × 0.33 | black FDM | screws to CH | 2 |
| FW | inclined plate | 76 × 22 × 3, 15° lean | 0.9 | black FDM | integral/screws | 1 |
| KN | knuckles | Ø 6 × 1.5–2 | — | black | integral | 9 |
| HP | pin | Ø 2 × 80 | — | steel | in SP holes | 1 |
| F-short | wedge blade + barrel + pocket | 7.5 × 26 × 6.5, pocket 3.5 × 14 × 1 | 0.09 × 0.31 | orange FDM | on HP | 6 |
| F-long | stepped wedge blade + barrel | 7.5 × 46 × 6.5 | 0.09 × 0.55 | orange FDM | on HP | 2 |
| LID | flat plate | 56 × 44 × 2 | 0.67 × 0.52 | white | 4 × M2 | 1 |
| S-LID | button head | M2, head Ø 3.8 | — | black | into CH | 4 |
| WH | ribbed TPU wheel | Ø 26 × 8.5 | 0.31 | black TPU | motor shaft | 4 |
| CH | central tub | 52 × 72 × 28 | 0.62 × 0.86 | black FDM | — | 1 |
| H-SP | screws/holes | Ø 3.5–5 | — | — | — | ≈ 5 per side |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| Fork barrels ↔ HP | rotate on | 0.1–0.2 |
| Fork ↔ adjacent knuckle | side clearance | 0.2–0.3 |
| Fork ↔ fork (beside a knuckle) | gap | ≈ 1.5–2 |
| F1 ↔ SP-L inner face | end knuckle between | ≈ 2.75 |
| Fork tips ↔ floor (rest) | resting | 0 |
| Fork top ↔ FW (fully raised, guess) | stop | 0 (rotation ≈ 70°) |
| FW ↔ SP inner faces | joined | 0 |
| LID ↔ CH | screwed | 0 |
| LID front edge ↔ FW | slot | ≈ 5 |
| LID side edges ↔ wheel treads | beside | 2–3 |
| WH outer face ↔ SP inner face | inside | 2–3 |
| WH inner face ↔ CH side | inside | 1–2 |
| WH top ↔ SP top edge | wheel above | +0…+2 |
| WH bottom ↔ floor | touching | 0 |
| SP bottom edge ↔ floor | skims | 0.5–1 |
| SP tip ↔ floor | touching | 0–0.5 |
| Long fork tip ↔ SP tip (Y) | fork ahead | ≈ 17 |
| Short fork tips ↔ SP tip (Y) | fork slightly behind | ≈ −2 |

---

## 6. Mechanism
1. **Drive**: four wheels (4WD) in two wells; skid steering. All four wheels are driven (guess, medium): either 4 N20 motors or 2 motors with the front/rear wheel pairs geared/belted (the cylinder between the right wheels may be a second motor).
2. **Hinged comb**: each fork hangs freely on the pin and rests on the floor by gravity. On uneven floors or when it meets a seam, each fork lifts independently, so **every fork tip stays in contact with the floor**. An opponent's wedge pushing on the comb lifts the forks (up to about 70° until they hit FW, guess) rather than pushing under the robot.
3. **Long forks**: their tips are the first contact; they slip under an opponent and lift its edge as it is pushed onto them, then the short comb and the side plate ramps take over.
4. **Side plates** act as runners and side wedges at the front corners.
5. **Invertibility**: wheel tops are at about the side plate top; inverted, the robot would sit on the plates and the lid; the wheels may just touch (0–2 mm) so inverted driving is marginal (guess). The forks would hang upward (useless) when inverted.

---

## 7. Assembly order (suggested rebuild)
1. Print CH with floor, FW and knuckles (black), two SP plates (black), eight forks (orange: 6 short, 2 long, printed on their sides for strong hinge barrels), lid (white), four wheels (TPU).
2. Fit motors into CH; mount wheels.
3. Fit battery, ESC/receiver, switch; route wires.
4. Thread the hinge pin through end knuckle, forks and knuckles in order F1…F8 (long ones in slots 3 and 6).
5. Screw the side plates onto CH, capturing the hinge pin ends and the motor/axle supports.
6. Screw on the lid (4 × M2).

---

## 8. Coordinate frame (restated)
- SP: x ±38…±42, y −40…+40, z 0…28 (front slope from (y +8, z 28) to (y +40, z 1)).
- FW: x ±38, base (y +12, z 6) to top (y +6, z 28).
- HP axis: along X at (y +13, z 4).
- Wheels: (±31, +2, 13) and (±31, −30, 13), Ø 26.
- Lid: centre (0, −14, 29), 56 × 44.

## 9. Profiles as math

**9.1 Side plate profile (YZ).**
- Polygon: (−40, 0) → (40, 0) → (8, 28) → (−40, 28) → close. Front edge line: z = 28·(40 − y)/32 for y ∈ [8, 40] (41.2°).

**9.2 Short fork (side profile in the fork's own frame; hinge at the origin, u forward along the floor, v up).**
- Barrel: circle r 3 at (0, 0) (hinge axis), tip on the floor means the fork rests rotated by α ≈ atan(4/26) relative to its flat underside.
- Underside: line from (0, −3) to (26, −4) (contact at the tip, z = 0 there).
- Top: line from (2, 3) to (22, −2.5), then bevel to (26, −3.5).
- Pocket: rectangle u ∈ [6, 20], width 3.5, depth 1, rear end semicircle r 1.75.

**9.3 Long fork.**
- Top: (2, 3) → (24, 0) (rear tier), (24, 0) → (26.5, −2) (step at 40–45°), (26.5, −2) → (42, −3.6), bevel (42, −3.6) → (46, −4.1). Underside: (0, −3) → (46, −4.5).

**9.4 Comb layout.**
- Fork k (k = 1…8) centre x_k = −31.5 + 9(k − 1); long if k ∈ {3, 6}. Knuckle j (j = 0…8) centre x = −36 + 9j, width 1.5–2 (end knuckles slightly wider).

**9.5 Wheel.**
- r(φ) = 13 + 0.5·[sin(36φ) > 0]; width 8.5; face rim 2 wide, centre recess 1.5 deep, hub r 4.

**9.6 Front wall.**
- Plane through (y 12, z 6) and (y 6, z 28): y = 12 − 0.273·(z − 6) (15.3° lean back).

## 10. Pixel-based measurements (native 1427 × 1160, ±8 px)
- Fork row hinge line: from (215, 545) (F1 rear) to (900, 800) (F8 rear): 735 px for 8 pitches ≈ 92 px per fork near the middle.
- Short fork F5: rear (575, 680), tip (480, 905): ≈ 245 px; width ≈ 75 px.
- Long fork F6: rear (660, 715), tip (410, 1085): ≈ 445 px.
- Long fork F3: tip (120, 945).
- Lid screws: (655, 158), (475, 290), (1105, 305), (955, 458); head ≈ 25 px.
- Wheels: front-right (1060, 470) top; rear-right top (1230, 250); right wheels ≈ 160 px tall where visible (≈ Ø).
- SP-R tip (850, 1090); SP-R top-front (1030, 580); SP-R rear top (1390, 415).

## 11. Several independent estimates of key quantities

| Quantity | Method A (kit / rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Scale near the lid front | — | — | screw head 25 px / 3.8 mm → 6.6 px/mm (lid, mid-depth) | 6.6 px/mm (lid), ≈ 9 px/mm (forks, nearer) |
| Fork pitch | kit spread 68 / 5 (6 forks) = 13.6 | row of 8 across 76 inner width → 9.5 | 92 px / 9.5 px/mm → 9.7 | **9.0–9.5 (use 9.0 with knuckles)** |
| Fork width | kit 10 | ≈ 0.8 × pitch → 7.5 | 75 / 9.5 → 7.9 | **7.5** |
| Short fork length | kit 34 | ≈ 3.3 × fork width → 25 | 245 px / 9.5 → 26 | **26** |
| Long fork length | — | ≈ 1.8 × short → 46 | 445 / 9.5 → 47 | **46** |
| Width | kit 84 | lid 56 + 2 × (12 well + 4 plate) = 88 | — | **84** |
| Lid | kit 56 × 44 | ≈ 2/3 W | screw spacing 48 × 38 + margins → 56 × 46 | **56 × 44** |
| Wheel Ø | kit 24 | ≈ 0.9 × height → 26 | 160 px / 6.6 → 24; nearer wheel ≈ 26 | **26** |
| Height | kit 30 | ≈ wheel Ø + 2 | — | **28 (plates), 30 (lid top)** |
| Length | kit 80 | plates 80 + long forks 17 | — | **97 overall (−40 to +57)** |

## 12. Consistency check
1. **Fork count**: kit says 6; the photo and the user's notes say **8** (6 short + 2 long). **8 used.**
2. **Wheels outside?** The ONESHOT rounds placed wheels outboard; the photo and user note say **inside** the side plates. Reconciled: wheel wells between CH (±26) and SP (±38).
3. **Overall length**: −40 to +57 = 97 < 101.6. Width 84. Height 30. Fits.
4. **Fork hinging**: hinge knuckles visible as separate black cylinders between orange forks, and forks of different lengths at slightly different angles in the photo (F6 sits a little higher at its rear than F5): consistent with free hinging.
5. **Mass**: plates + tub + FW ≈ 50 g, forks 8 × 1.5 = 12 g, lid 5 g, wheels 4 × 3 = 12 g, 4 N20 motors 40 g (or 2 = 20 g), battery 12 g, ESC 5 g, pin/screws 3 g: 120–140 g, under 150 (4 motors is tight; 2 motors with front-rear coupling fits more easily).

---

## 13. Why the designer did it (per part, adversarial)

- **Comb of eight hinged forks**
  - Getting under vs contact: a single rigid wedge touches the floor only at its high points; independent hinged forks each drop to the floor, so the whole front edge is always "on the floor" even over arena seams, and an opponent's wedge **can't find a gap** under it. In a wedge-vs-wedge contest, the hinged forks also **lift up** if the opponent gets lower, then fall back.
  - Against spinners: thin individual forks are cheap sacrificial parts; one broken fork leaves seven working; spares slide onto the pin.
  - Orange forks: visibility and identity.
- **Two long forks**
  - Reach: the first point of contact, sliding under the opponent before it touches the comb; they also lift it higher thanks to their length, making it lose traction. Placed symmetrically at ±13.5 so a centred opponent sits on both.
- **Pockets on the short forks / stepped long forks**
  - Lighten the forks and make them flex less at the barrel (thick root, thin tip); the step on the long forks keeps the root stiff and the tip thin.
- **Full side plates with sloped fronts**
  - Protect the wheels from horizontal spinners and from being pushed sideways by wedges; the sloped front ends act as **corner wedges** beside the comb so opponents hitting the corners also ride up.
  - Wheels inside = nothing to grab or rip off; the plates take side hits.
- **Inclined front wall**
  - Stops the forks from swinging too far and backs them up; deflects an opponent riding up the forks upward rather than letting it hit the electronics.
- **Four-wheel drive**
  - Pushing power and traction (four TPU wheels); the wheelbase gives stability against tipping forward when an opponent is on the forks.
- **White lid with four screws**
  - Quick access; contrasting colour for judges/drivers to see orientation (white top = right way up).
- **Gap at the lid front**
  - Probably for the switch/link access or cable routing; small target.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 6 V 50:1 (or 2 driving front+rear via shared axles/gears) | 12 × 10 × 25 | along X behind each wheel, (±18, +2, 13), (±18, −30, 13) | medium |
| Battery | 2S LiPo 180 mAh | 30 × 18 × 9 | centre (0, −14, 8) between motors | medium |
| ESC/receiver | combined ant board (e.g. Malenki-style) | 25 × 20 × 5 | under the lid front (0, +0, 20) | medium |
| Switch | slide switch in the front gap or under the floor | 12 × 4 | (0, +4, 20) | low |
| Hinge pin | Ø 2 steel rod or filament | 80 | (y +13, z 4) | medium |
| Side plate screws | M2 into CH bosses | — | as H-SP | medium |
| Wiring | battery → switch → ESC → 4 motor leads (paralleled per side) | — | inside | medium |

## 15. What the photo cannot show
- The left side, rear, underside, the exact fork underside and range of rotation, motor count, and the switch position.
- All mm values are estimates (±10–15%).

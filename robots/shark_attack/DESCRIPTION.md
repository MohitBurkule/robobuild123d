# Shark Attack: full rebuild description from reference photos

Source photos (in `robots/shark_attack/reference/`), all cut out onto white with a **green backdrop fringe** (green on edges and on clear parts is spill, not paint):
- `shark_attack.aws72.webp` (1210 × 1070 px): **front-right three-quarter, about 35° above horizontal**. Fitted with **four clear polycarbonate forks** under clear tape. The arm's **fin tip is a green-tinted clear plate with a silver edge**.
- `shark_attack.aws74.webp` (1043 × 854 px): **front-left three-quarter, about 25° above horizontal**. Same four forks, here showing **wire hinge loops** at each fork root.
- `shark_attack.aws76.webp` (1479 × 1093 px): **front-left three-quarter, about 25° above**. Fitted with **two grey barbed forks** through slots in the front plate; the fin tip is **blue printed**. The robot's **left side panel** (green FR4 with screws) is seen almost square.

Everything stated as fact is read from those photos. Anything inferred is marked **(guess)** with a confidence. Dimensions are **estimates in mm**, scaled from the AWS antweight limits (150 g, fits a 101.6 mm cube) and photo proportions, and checked against the project spec draft (`spec.json`: chassis, two wheels with two drive motors, four forks with mounts, two humps, a fin, a hammer tip, a hinge block, battery, ESC, switch, and a weapon actuator `wa_act`). **W = side-panel to side-panel width ≈ 92 mm** is the ratio base.

Shark Attack is an **overhead hammer/axe robot** with a **fork front**: a blue printed body with **two raised hoods ("humps")** either side of a central channel, in which a **hammer arm** lies, hinged near the front and ending at the rear in an upright **"shark fin"**. When fired, the arm swings **up and forward over the hinge** to bring the fin down on an opponent held on the forks **(guess on the swing direction, high)**.

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) under the centre of the body (mid-width between the side panels, mid-length of the body excluding the forks).
- **+X** = robot's right, **+Y** = forward (toward the forks), **+Z** = up. Units mm.
- AWS72: camera at the **front-right** (the robot's right side panel is at the image right). AWS74 and AWS76: camera at the **front-left** (the robot's left panel is at the image left).

Part IDs:

| ID | Part |
|---|---|
| CH | blue printed chassis (deck, floor, front plate) |
| FP | blue sloped front plate with a central notch |
| FN | notch in the top of FP |
| S-FP | front plate Phillips screws (4) |
| HM-L / HM-R | blue humps (hollow hood boxes on the deck) |
| S-HM | hump corner screws |
| SP-L / SP-R | green FR4 side panels (wheel guards) |
| SE | aluminium edge strip on the side panels' front edges |
| S-SP | side-panel screws and nuts |
| CHN | central channel between the humps |
| HG | hinge: three blue knuckles on a steel pin |
| HP | hinge pin |
| AR | hammer arm (blue printed beam) |
| AS | aluminium strip along the arm's top |
| CB | clear acrylic clamp block with 4 screws on the arm (AWS72) |
| FIN | upright fin at the arm's rear end (hammer tip) |
| FC-1…4 | clear polycarbonate forks (AWS72/74) |
| FT | clear tape over the fork roots |
| FH | wire hinge loops at the fork roots (AWS74) |
| FG-L / FG-R | grey barbed forks (AWS76) |
| FS | vertical slots in FP for FG |
| WH-L / WH-R | drive wheels (hidden) |
| DM, ACT, BAT, ESC, SWT | hidden internals (guess) |

---

## 1. Overall description in one paragraph

Shark Attack is a **blue, boxy fork-and-hammer robot** about **92 mm wide, ≈ 80 mm long in the body (≈ 105 mm with forks) and ≈ 40 mm tall at the humps**, with a **fin** reaching **≈ 70 mm** when the arm is at rest. Its front is a **steep blue printed plate** (≈ 60–65°) with a **rectangular notch** at the top centre and **four Phillips screws** in two pairs. Along the lower front edge, it carries either **four clear polycarbonate forks** (≈ 12 mm wide, taped over and hinged on wire loops) or **two grey barbed forks** sticking out through slots in the plate. The **sides are flat green FR4 plates** (circuit-board material) with **silver screws and nuts** and an **aluminium edge strip** at the front; they hide the wheels completely. On top, two **hollow blue hoods** (humps) about **30 mm wide × 55 mm long × 15 mm tall** sit left and right, each with a **chamfered front edge** and an opening on its inner side. Between them runs a **central channel ≈ 24 mm wide**, where the **hammer arm** lies: it is **hinged near the front** on **three blue knuckles** on a **steel pin**, runs back along the channel with an **aluminium strip** on its top and a **clear acrylic clamp block** with four screws, and turns **up at the rear** into the **fin**, a **≈ 30 mm tall upright blade** with a hooked tip.

---

## 2. Part-by-part description

### 2.1 Chassis deck and floor (CH)
- **Shape**: a rectangular base **x ∈ [−44, +44]**, **y ∈ [−40, +40]**, with a deck at **z ≈ 24** on which the humps sit, and a floor at **z ≈ 3** **(guess)**. Between the side panels, the blue body is about **84 mm wide**.
- **Colour / material**: **mid-blue** FDM with a diagonal top-skin texture and horizontal wall layer lines.
- **Corner screws**: black Phillips pan heads at the deck corners, at the humps' outer front corners (AWS72 px (310, 330), (965, 535); AWS74 px (180, 380), (825, 320); AWS76 px (325, 450)).

### 2.2 Front plate (FP) and notch (FN)
- **Shape**: a **flat plate ≈ 3 mm thick**, sloping back at **≈ 60–65° from the floor**, spanning the full body width (**≈ 88 mm**), from the floor line (z ≈ 3, y ≈ +40) up to the deck (z ≈ 24, y ≈ +30). Its **top edge** has a **rectangular notch FN ≈ 26 mm wide × 8 mm deep** in the centre, aligned with the channel (AWS72 px (490–690, 490–540); AWS74 px (430–640, 405–440); AWS76 px (720–860, 375–490)).
- **Ends**: the outer ends of FP are **angled back ≈ 30° in plan** in AWS76 (the right end sweeps back at the image right, px (1150–1300, 290–610)), so FP's outline wraps slightly around the front corners.
- **Screws S-FP**: **four black Phillips pan heads** (Ø ≈ 4.5) in **two vertical pairs**, one pair each side of the notch at **x ≈ ±22**, **z ≈ 12 and 18** (AWS72 px (390, 505)/(380, 550) and (745, 620)/(725, 680); AWS74 px (360, 500)/(360, 545) and (715, 460)/(720, 510); AWS76 px (670, 560)/(690, 625) and (970, 455)/(995, 505)).
- **Slots FS (AWS76)**: two **vertical slots ≈ 3 × 14 mm** in FP at **x ≈ ±22**, below the screw pairs, through which the grey forks pass (px (620–640, 660–720) and (1040–1060, 510–560)).

### 2.3 Humps (HM-L, HM-R)
- **Shape**: two **hollow printed hoods**, each about **30 mm wide (X) × 55 mm long (Y) × 15 mm tall above the deck** (tops at **z ≈ 39–40**). The top is flat; the **front edge is chamfered** at ≈ 45° (a ≈ 6 mm facet) and the outer sides are vertical, flush with the body side.
- **Positions**: HM-L x ∈ [−44, −14], HM-R x ∈ [+14, +44], **y ∈ [−35, +20]**.
- **Openings**: each hump is **open on its inner side** (facing the channel) for part of its length: AWS74 shows the robot-right hump (image right) open at its inner front, revealing **orange/red wires and a dark board** (px (450–600, 210–440)); AWS76 shows the same (px (520–830, 140–430)) with a **red wire, a white connector and a circuit board**. AWS72 shows the robot-right hump's inner wall with a gap revealing **a red part** (px (540–720, 230–310)).
- **Marking**: AWS74 shows **hand-written blue letters "TQ" or "10"** on the robot-left hump's top (px (300–330, 250–300)) **(a label or an event number)**.

### 2.4 Side panels (SP-L, SP-R) and edge strips (SE)
- **Material**: **green FR4 / G10 fibreglass sheet** (the green with fine white marks looks like **bare circuit-board laminate**, ≈ 1.6 mm thick).
- **Shape**: a **flat rectangle ≈ 80 mm long × 28 mm tall**, covering the full side of the body from z ≈ 2 to z ≈ 30, **outboard of the wheels**, at **x = ±46**.
- **Edge strip SE**: the front vertical edge of each panel carries an **aluminium angle strip** (≈ 4 mm wide, silver) that wraps the corner where the panel meets FP (AWS76 px (240–360, 450–790)).
- **Fasteners S-SP**: on the robot-left panel (AWS76): **three silver Phillips screws with nuts/spacers** near the front-lower area (px (275, 600), (295, 690), (350, 715)) and **two small holes** (px (165, 520), (180, 605)). AWS72's right panel shows **black screws** at (1090, 605) and (1000, 735). AWS74's left panel shows **silver nuts** at (95–110, 460–470) and (125, 555).
- **Function**: wheel guards and side armour. The screws near the bottom probably hold the **wheel axle/motor brackets** or **spacers** that hold the panel off the body **(guess, medium)**.

### 2.5 Wheels (WH-L, WH-R), hidden
- **Not visible.** Hidden behind the side panels. The spec has **two wheels** (`wheel_l0/r0`) with two drive motors. They must reach the floor **under** the panels or through cut-outs in the panel bottoms **(guess)**.
- **Reconciled guess**: **Ø ≈ 26 mm** wheels at **(±40, −10, 13)**, between the body's inner wall and the FR4 panel, with ≈ 1 mm clearance under the panel's lower edge **(medium)**.

### 2.6 Central channel (CHN)
- **≈ 24 mm wide** between the humps (x ∈ [−12, +12]), with its floor at the deck level (z ≈ 24) or lower (z ≈ 15) at the hinge **(guess)**. The channel holds the arm, the hinge and, below them, the actuator and wiring.
- Visible in the channel (AWS72): a **red component** (px (560–700, 270–310)), a **yellow disc with green rim** (px (515–565, 435–480)), and **dark parts**. The yellow-green disc is likely the **end of a motor/servo** **(guess, low)**.

### 2.7 Hinge (HG) and pin (HP)
- **HG**: **three blue printed knuckles**, each **≈ Ø 12 × 5 mm**, side by side on a **steel pin HP (Ø ≈ 3 mm)** across the channel, at about **(y +12, z 26)** (AWS72 px (570–690, 380–480); AWS74 px (430–550, 310–420); AWS76 px (690–760, 300–370)). The **pin ends** stick out ≈ 3 mm on both sides (AWS72 px (545, 405) and (690, 440)).
- **Interpretation**: the **middle knuckle is part of the arm** and the two outer knuckles are **fixed to the chassis**, or the reverse; the arm pivots on HP **(guess, high)**.

### 2.8 Hammer arm (AR), strip (AS), clamp block (CB)
- **AR**: a **blue printed beam** about **10 mm wide × 8 mm tall**, from the hinge **back along the channel** for about **45 mm**, lying at deck level (top at z ≈ 34), then **curving up** into the fin at the rear (y ≈ −35).
- **AS**: a **thin aluminium strip** (≈ 4 mm wide, ≈ 0.5 mm thick) running along the arm's top and up the fin's front edge, **kinked** (zig-zag) where it follows the arm's steps (AWS72 px (780–900, 60–270); AWS74 px (320–400, 50–220)). It is an **impact edge** and stiffener **(guess)**.
- **CB (AWS72)**: a **clear acrylic block ≈ 18 × 14 × 4 mm** on the arm just behind the hinge (px (590–790, 260–370)), with **four black screws** in a 2 × 2 pattern. It **clamps the arm to the actuator output** (a servo horn) or **sandwiches** the two halves of the arm **(guess, medium)**. Not visible in AWS74/76 (covered or replaced).
- **Side brackets**: near the rear, the arm passes between **two small blue brackets** (AWS72 px (820–940, 150–230); AWS74 px (290–440, 120–200)) with **pins** (black/steel ends at px (820, 180) and (940, 185)). These look like a **rear rest** or a **second pivot/link** **(guess: the actuator's pushrod joint, low–medium)**.

### 2.9 Fin (FIN)
- **Shape**: an **upright blade** at the arm's rear end, **≈ 30 mm tall × 12 mm long (Y) × 3 mm thick**, with a **rounded top** and a **hook** at the rear top (AWS76 px (285–330, 45–180)).
- **AWS72**: the fin's top is a **green-tinted clear plate** (polycarbonate) with a **silver aluminium edge** wrapped over its front (px (860–915, 40–200)).
- **AWS74**: a **light green/clear** fin top with the aluminium edge (px (310–350, 40–140)).
- **AWS76**: a **blue printed** fin with a rear hook (px (285–330, 45–180)).
- **Top height**: z ≈ **68–72** at rest.
- **Function**: the **hammer head / striking tip**. When the arm swings forward over the hinge, the fin's top comes down on the opponent in front.

### 2.10 Clear forks (FC-1…4), tape (FT), hinge loops (FH), AWS72/74
- **Shape**: **four flat clear polycarbonate strips**, each **≈ 12 mm wide × 30 mm long (beyond the plate) × 1.5 mm thick**, with square tips, evenly spaced at **x ≈ −33, −11, +11, +33** (gaps ≈ 10 mm).
- **Mount**: the forks hang from the **lower edge of FP** on **wire hinge loops FH** (AWS74 shows a **copper/steel wire loop** at each fork's root, px (150–170, 655–700), (370–390, 640–690), (630–645, 615–665), (850–865, 590–640)) and lie **on the floor**, sloping **≈ 10–15°** down from the plate.
- **Tape FT**: a band of **clear packing tape** (≈ 18 mm wide) covers the fork roots and the plate's lower edge across the whole width (AWS72 px (190–920, 530–840); AWS74 px (140–980, 510–640)). Tape is wrinkled and scuffed.
- **Function**: **free-hinged forks** that drop to the floor and get under opponents.

### 2.11 Grey barbed forks (FG-L, FG-R), AWS76
- **Shape**: two **bent flat strips** (grey metal, ≈ **2 × 4 mm** section; aluminium or grey-painted steel, or grey printed **(guess)**), each exiting a slot FS, running **down and forward** at ≈ 35°, then **flattening** near the floor, ending in a **barbed sawtooth tip**: a forward-pointing triangle with a **notch** behind it (AWS76 px (630–990, 650–1040) and (1040–1420, 510–830)).
- **Length**: ≈ **45 mm** from the slot to the tip; tips at **y ≈ +78**.
- **Spacing**: at **x ≈ ±22**.

---

## 3. Per-view sections

### 3.1 AWS72 (front-right)
- **Silhouette**: a blue box with two humps, a fin sticking up at the rear right of centre, four forks at the bottom front, the green right panel at the image right.
- Details: the clear block with 4 screws on the arm, the hinge knuckles, the tape band over the forks, the front screws, the red and yellow parts in the channel.

### 3.2 AWS74 (front-left)
- The same with the forks' wire hinge loops visible; the left green panel at the image left with silver nuts; the robot-right hump open at its inner front showing wiring; the fin with its aluminium edge.

### 3.3 AWS76 (front-left)
- The two grey barbed forks through slots; the left FR4 panel with aluminium edge strip and 3 screws; the humps (the right one's inner side open showing a board and wires); the blue fin with hook at the rear.

### 3.4 Top view (synthesised)
- A 92 × 80 rectangle: two humps (30 × 55) at the sides, a 24 mm channel with the hinge at y +12 and the arm running back to the fin at y −35; FP across the front with the notch; forks ahead (4 × 12 mm or 2 thin barbs).

### 3.5 Side view (synthesised, left)
- A flat green FR4 rectangle (80 × 28) with screws; the hump's profile above it (to z 40, chamfered front); FP sloping at the front; forks to the floor ahead; the fin rising at the rear to z ≈ 70.

### 3.6 Rear view (not photographed)
- The two humps, the fin in the middle, the side panels; probably the switch **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | base box | 88 × 80 × 24 | 0.96 × 0.87 | blue FDM | — | 1 |
| FP | notched sloped plate | 88 × 24 (slope) × 3 | 0.96 | blue FDM | 4 Phillips | 1 |
| HM | hollow hood | 30 × 55 × 15 | 0.33 × 0.6 | blue FDM | corner screws | 2 |
| SP | flat plate | 80 × 28 × 1.6 | 0.87 × 0.3 | green FR4 | 3–5 screws + nuts | 2 |
| SE | angle strip | 4 × 28 | — | aluminium | with SP | 2 |
| HG | 3 knuckles | Ø 12 × 5 each | — | blue FDM | on HP | 1 set |
| HP | pin | Ø 3 × 30 | — | steel | press fit | 1 |
| AR | beam with upturn | 10 × 8 × 45 + fin | 0.49 | blue FDM | on HP | 1 |
| AS | strip | 4 × 0.5 × 70 | — | aluminium | glued/taped (guess) | 1 |
| CB | clamp block | 18 × 14 × 4 | — | clear acrylic | 4 black screws | 1 (AWS72) |
| FIN | upright blade | 12 × 30 × 3 | 0.33 tall | clear PC + Al edge / blue FDM | integral or screwed to AR | 1 |
| FC | flat strip fork | 12 × 30 × 1.5 | 0.13 | clear PC | wire loop hinge + tape | 4 (AWS72/74) |
| FG | barbed bent strip | 2 × 4 × 45 | 0.49 long | grey metal | through slot | 2 (AWS76) |

---

## 5. Contact / gap matrix (estimated mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| FP ↔ CH front | screwed | 0 |
| HM ↔ CH deck | screwed | 0 |
| SP ↔ CH sides | screwed (with spacers, guess) | 0–2 |
| SE ↔ SP / FP corner | wrapped | 0 |
| HG outer knuckles ↔ CH | fixed | 0 |
| AR ↔ HP | rotates on | 0 |
| AR sides ↔ HM inner walls | running gap | ≈ 5 each side |
| AR bottom ↔ channel floor (rest) | rests on (down stop) | 0 |
| FIN ↔ AR | integral / screwed | 0 |
| CB ↔ AR | clamped | 0 |
| FC root ↔ FP lower edge | hinged on wire | 0 |
| FC tips ↔ floor | rest on | 0 |
| FG ↔ FS | through slot | 0.5 |
| FG tips ↔ floor | touch | 0 |
| WH ↔ SP inner face (hidden) | running gap | 1–2 |
| SP bottom ↔ floor | clearance | ≈ 2 |

---

## 6. Mechanism

1. **Hammer**: the arm pivots on HP at the front of the channel. At rest it lies back along the channel with the fin up at the rear. The actuator swings the arm **up and forward** through ≈ 180°, so the fin crosses over the hinge and **strikes down ahead of the front plate**, where the forks hold the opponent. With the hinge at y ≈ +12 and the fin tip ≈ 55 mm from the hinge, the strike lands at **y ≈ +60**, just over the fork tips. The actuator is likely a **servo** (a strong digital one) or a **geared motor** (`wa_act`) **(guess, medium)**.
2. **Forks**: passive; the clear forks are hinged and fall to the floor; the barbed ones are fixed.
3. **Drive**: two hidden wheels, skid steer.
4. **Self-righting**: the arm swinging 180° pushes against the floor when the robot is inverted, so it can **self-right** **(guess, high)**.

---

## 7. Assembly order (suggested rebuild)

1. Print the **chassis** (floor, walls, deck), the **front plate**, the **humps** and the **arm/fin**.
2. Fit the **drive motors** in **printed clamps** at the sides; mount the **wheels**.
3. Install the **hammer actuator** under the channel; fit its output to the arm via the **clear clamp block** (4 screws).
4. Install **battery, ESC, receiver, switch**; route the wires under the humps.
5. Fit the **hinge knuckles** and **pin**, the **arm**, the **aluminium strip**.
6. Screw on the **front plate** (4 screws) and the **humps**.
7. Screw on the **FR4 side panels** with their **edge strips**.
8. Attach the **forks**: the clear ones on wire loops + tape, or the barbed ones through the slots.

---

## 8. Profiles as math (for rebuilding curves)

**8.1 Front plate (YZ side section).** A line from (y +40, z 3) to (y +30, z 24): **z = 3 + 2.1·(40 − y)** (≈ 64.5°), thickness 3 inward. Plan outline: front face width 88, ends angled back 30° over the last 6 mm. Notch: x ∈ [−13, +13], top 8 mm.

**8.2 Hump (YZ section, constant along X over 30 mm).** (y −35, z 24) → (−35, 39) → (+14, 39) → (+20, 33) → (+20, 24): a rectangle with a **6 × 6 chamfer** at the top front.

**8.3 Arm + fin (YZ centreline, x = 0, at rest).** Hinge H = (+12, 26). Beam: from H back to (−28, 30) (slightly rising, ≈ 6°), then a **fillet r = 6** turning up, then the fin's front edge vertically to (−34, 66), a **rounded top r = 6** centred at (−40, 66), and the fin's rear edge down to (−46, 62), with a **rear hook**: a notch from (−46, 62) to (−42, 58) to (−46, 54). Fin thickness 3 (X). Arm section 10 × 8.
Swing: P(θ) = H + R(θ)·(P₀ − H), rotation about the X axis through H, θ from 0 (rest) to −180° (strike).

**8.4 Clear fork.** Rectangle 12 × 30 in a plane tilted 12° down from horizontal, hinged at (y +40, z 3).

**8.5 Barbed fork (YZ, in its own plane x = ±22).** Polyline: slot exit (y +36, z 12) → (+58, 2) → (+72, 0) (flat) → barb tip (+80, 0) → back up to (+74, 6) → (+72, 2): a forward-pointing sawtooth 8 long × 6 tall.

---

## 9. Pixel-based measurements (independent check)

**AWS72 (1210 × 1070):** body front-plate width px (180 → 970) ≈ 790 (oblique); humps: left px (310–720, 140–390), right (690–1080, 230–540); fin top px (870, 40); hinge px (570–690, 380–480); forks ≈ 85 px wide each.
**AWS74 (1043 × 854):** FP px (140–980) ≈ 840 px; fork width ≈ 80–90 px; hump right px (450–870, 140–330); fin top px (325, 40).
**AWS76 (1479 × 1093):** left panel px (40–400, 330–860) ≈ 360 × 430; FP front face px (370–1300); hump left px (110–700, 210–470); fin px (285–330, 45–180); barbed fork right px (1040–1420, 510–830).

---

## 10. Several independent estimates of key quantities

| Quantity | Method A (limits/spec) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | ≤ 101.6 | — | AWS74: FP 840 px ≈ fork width 85 px × (88/12) → 12 mm forks give 870 px ✔ | **92** (panels), 88 (FP) |
| Fork width | — | ≈ 0.13 W | AWS74 85 px / (840/88) = 8.9; AWS72 85 / (790/88) = 9.5 | **10–12 → 11** |
| Hump height above deck | — | ≈ 0.5 × deck height | AWS76 left hump side ≈ 120 px vs panel 430 px for 28 → ≈ 8? (the hump side is foreshortened); AWS74 hump front ≈ 140 px vs FP 840 px → 15 | **15** |
| Fin height (top z) | under the cube height | ≈ 1.75 × hump top | AWS74 fin top px 40 vs deck px ≈ 330 vs floor px ≈ 700 → (700 − 40)/(700 − 330) × 24 ≈ 43?? (perspective) | **≈ 65–70** (see §11) |
| Side panel length | — | 0.87 W | AWS76 360 px foreshortened ≈ 0.85 → 424 / (FP 930 px / 88) = 40?? | **80** (see §11) |
| FP slope | — | AWS76 FP looks ≈ 60–65° | rise 21 over run 10 → 64° | **64°** |

---

## 11. Consistency check: conflicts and reconciliation

1. **Fin height.** The AWS74 pixel ratio (≈ 43) ignores that the fin is at the **rear**, far from the camera, and that the camera is 25° above: the deck appears higher in the image than it is. In AWS72 the fin top sits ≈ 1.6 × above the hump top relative to the deck. **Reconciled: fin top z ≈ 65**, hump top 39.
2. **Side panel length.** AWS76 sees the panel at a steep angle (≈ 65° from face-on), so 360 px corresponds to ≈ 360/cos 65°… that overstates. Using AWS72 (right panel px (970–1170, 330–950), about 2/3 the hump length in the image) gives ≈ 80 mm. **Reconciled: 80.**
3. **Wheels hidden but needed.** FR4 panels from z ≈ 2: the wheels must be inside and reach the floor. **Consistent with the spec's two hidden wheels.**
4. **Four vs two forks.** Different events. Build **four clear forks** as default (two photos) and barbed forks as a variant.
5. **Strike point vs fork reach.** Strike at y ≈ +60 (hinge +12, fin tip ≈ 55 from the hinge after a 180° swing: +12 + 48 = +60). Clear fork tips at +70, barbed at +78. **Consistent: the fin hits on the forks.**

---

## 12. Why the designer did it (per part, mostly adversarial)

- **Forks (clear hinged or barbed fixed)**: getting under is the robot's first job; the hammer only works on an opponent held in front. Free-hinged forks stay on the floor even when the robot rocks; four narrow forks find gaps under opponents. Clear polycarbonate flexes instead of snapping. The tape protects the roots and stops the forks rotating up too far. Barbed forks **catch** an opponent's edge so it cannot back off before the hammer lands.
- **Steep front plate with notch**: a steep plate is a **pushing face** (not a wedge; the forks do the getting under). The notch lets the arm/fin pass down to the front. Screws in pairs spread hit loads.
- **FR4 side panels**: **wheel guards and side armour**. FR4 is very tough for its weight and does not crack like print; it shields the hidden wheels from horizontal spinners. The aluminium edge strip protects the panel's exposed front edge from chipping. **Weakness**: if a panel is bent inward it may rub a wheel.
- **Humps (hollow hoods)**: house the electronics and **flank the arm**, protecting it from side hits and giving the robot a "shark back" look. Their open inner sides let wires reach the channel.
- **Hammer arm hinged at the front, fin at the rear**: the longest possible swing (≈ 180°) builds speed before impact; at rest the fin sits at the back, away from frontal attacks. The arm also **self-rights** the robot.
- **Aluminium strip on the arm**: protects and stiffens the printed arm's striking edge.
- **Clear clamp block**: a stiff, light way to clamp the arm to a servo horn with four screws (more grip than a single horn screw).
- **Hidden wheels**: nothing for spinners to catch; **weakness**: the robot cannot run inverted on its wheels unless the panels are trimmed (the wheels are shorter than the humps), so self-righting is needed.

---

## 13. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors DM | 2 × N20 gearmotors | 12 × 10 × 25 | along X at (±28, −10, 13) | medium |
| Motor mounts | printed **plastic clamps** with 2 × M2 each; outer support by the FR4 panel screws | 14 × 14 × 14 | at each motor | medium |
| Wheels | Ø 26 × 8 rubber/TPU | — | (±40, −10, 13) | medium |
| Hammer actuator ACT | high-torque servo (e.g. 25 kg-class micro/mini), output on the hinge axis | 40 × 20 × 38 or 23 × 12 × 30 | under the channel, (0, 0, 14) | medium |
| Battery | 2S LiPo, 300 mAh | 40 × 18 × 10 | under HM-L | medium |
| ESC / RX | dual brushed ESC + RX board (the circuit board seen in AWS76) | 30 × 20 × 6 | under HM-R | medium |
| Switch | slide switch on the rear | 10 × 5 × 5 | (0, −40, 15) | low |
| Wiring | battery → switch → ESC → motors; RX → servo; the red/orange leads seen under HM-R | — | — | high (exists) |

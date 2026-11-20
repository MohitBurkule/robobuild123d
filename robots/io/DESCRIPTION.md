# Io: full rebuild description from reference photos

Source photo:
- `robots/io/reference/io.aws63.webp`: AWS 63, 675 × 777 px, **not cut out**. Taken at an event on a white speckled table, looking down from about **55–65° above the floor**, from the robot's **front-left**. Another robot (carbon-fibre deck, red frame, black foam wheels) is at the top-left, and blue plastic boxes and a "Competitor/Robot/T…" card are at the right: **background, not part of Io**. The photo is small. Io's **flipper is raised** (about 55–60° from the deck), which hides the middle of the robot.

Only one small photo exists, so the **rear, the right side, the underside and the area under the flipper are partly or fully hidden**. This description is therefore shorter on hidden detail than the 4000-word target, and says so where it applies. Facts are read from the photo; inferences are marked **(guess)**. Dimensions are estimates scaled from the 150 g / 101.6 mm cube limit and the project kit draft (`kit.json`: flipper, body 90 × 80 × 20, wheels r 10 × 8, plate pivot near the rear). An earlier short note read the same photo; where this description differs (which axis is long, which white block is which) the reasoning is in section 12. Ratios are against **W = frame width across the axles ≈ 92 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the flipper's free lip at rest), **+Z** = up. mm.
- **Origin O** = the floor point under the centre of the yellow frame's footprint.
- **Photo-to-robot mapping** (derived in section 10): the yellow frame's outer corners are at native px (30, 550), (350, 720), (640, 310) and a hidden one under the plate at about (320, 140). In the image the frame is a parallelogram with sides along (320, 170) (≈ 362 px) and (290, −410) (≈ 502 px).
  - The two wheels along the lower edge show their **red hub faces pointing down-left**, outward from that edge, so the **axles run along (290, −410)**: the **X direction**. (320, 170) is the **Y direction**.
  - The flipper plate's long edges are parallel to X, and its **dot-textured lip** leans toward the image's left end. So the image's **left end is the front (+Y)** and the lower edge is the robot's **left side (−X)**.

| ID | Part |
|---|---|
| FR | yellow perimeter frame/bumper (FR-F, FR-L, FR-R, FR-B bars) |
| BL-L | white left side block (between the left wheels) |
| BL-B | white rear block (across the rear, carries the pivot) |
| BL-R | white right side block |
| NT | notch in BL-L with wires |
| S-BL | silver button-head screws on the blocks |
| WH-FL, WH-RL, WH-FR, WH-RR | black foam tyres on red flanged hubs |
| FP | aluminium flipper plate |
| GS | dot-texture grip strip on FP's lip |
| S-FP | 3 silver dome screws on FP |
| BK | white printed flipper bracket/gusset |
| PV | flipper pivot (silver screw through a white tab) |
| MB | small grey metal block on the bracket |
| WR | wires |
| ACT | flipper actuator (hidden, guess servo) |
| M-x, BAT, ESC, RX, SW | motors and electronics (hidden, guess) |

---

## 1. Overall description in one paragraph

Io is a **small, low, wide flipper**. Its outline is a **bright saffron-yellow printed frame**, a thin bumper bar about 4 mm wide and 10 mm tall running all round, about **92 mm wide (across the axles) × 72 mm long**, with rounded corners. Inside it, at each corner, sits a **chunky black foam tyre on a red flanged hub** (about Ø 20 × 13 mm), so the wheels are **enclosed by the frame**. Between the wheels, **glossy white printed blocks** form the body: one along each side and one across the rear, closed by flat lids held with **silver button-head screws**. A **brushed aluminium flipper plate**, about 88 mm wide and 42 mm deep, lies over the front and middle at rest; in the photo it is **raised about 55–60°**. It has a **strip of fine dot texture along its front lip** and **three silver dome screws** along a line near its centre, fixing it to a **white triangular printed bracket** that pivots on a **silver screw through a white tab** on the front face of the rear block. Black/red wires with a white plug show under the raised plate.

---

## 2. Part-by-part description

### 2.1 Yellow frame (FR)
- **Shape**: a closed rectangular ring of **printed yellow bar**, about **4 mm wide × 10 mm tall**, outer size **92 × 72 mm**, outer corner radii about **6 mm** (front) and **8 mm** (rear). The bars stand from **z ≈ 1 to 11**: a **low bumper** whose top is below the white blocks.
  - **FR-F** (front, outer face at y +36): visible from the front-left corner until the plate hides it.
  - **FR-L** (left, x −46 to −42): fully visible along the image's lower edge; about 25 px of vertical face, i.e. about **10 mm** tall.
  - **FR-R**, **FR-B**: mostly hidden; bits show at the rear-right corner (native (600–640, 285–335)) and rear-left corner (330–360, 700–730).
- **Colour**: saturated yellow (≈ RGB 240, 200, 40), slightly glossy PLA/PETG.
- **Joins**: no visible screws; probably **printed with a floor plate** or screwed from inside to the white blocks **(guess)**.

### 2.2 White body blocks (BL-L, BL-B, BL-R)
- **Colour**: glossy cream-white (≈ RGB 225, 215, 200), soft highlights, flat tops.
- **BL-L**: between WH-FL and WH-RL, about **36 (Y) × 22 (X) × 18 mm** (top z ≈ 19), along FR-L's inside. **Two silver button heads** (Ø ≈ 4, M2) on top, near its front (native (220, 607)) and rear (360, 590). A **rectangular notch NT** (≈ 8 × 6 mm) at its outer rear corner shows **red and blue wires** and a **small white part** (connector or switch, guess) (native (300–345, 600–640)).
- **BL-B**: across the rear, about **70 (X) × 14 (Y) × 18 mm**, between WH-RL and WH-RR (native (380, 640) to (600, 380)). On its **front face** at about **x ≈ +12**, a **white printed tab** carries the **pivot screw PV** (silver pan head Ø ≈ 4.5, native (480, 467)). Another screw at its right end (530, 355).
- **BL-R**: between WH-RR and the hidden WH-FR, about 36 × 22 × 18; top at native (470–600, 230–380) with a screw at (505, 250).
- **Middle**: partly open under the plate; a **black part** (wheel or gearbox, guess) and the wires show through.

### 2.3 Wheels
- **Shape**: **black foam tyres** about **Ø 20 × 13 mm** on **red printed hubs** with **flanges** (≈ Ø 16 × 1.5) showing as red rings. WH-RR shows a red ring on its visible inner side too, so the hubs are probably **flanged both sides** **(guess)**. Foam is porous and worn.
- **Centres**: WH-FL (−33, +24, 10), WH-RL (−33, −24, 10), WH-FR (+33, +24, 10), WH-RR (+33, −24, 10). Seen: WH-FL at native (95–185, 485–575), WH-RL (320–410, 640–720), WH-RR (560–640, 300–390); WH-FR hidden.
- **Fit**: each tyre sits in a **corner bay** between the frame (≈ 2 mm outside it) and the side block. Tyre tops (z 20) are level with the block tops; the frame covers the lower half of each tyre's outer face.
- **Drive (guess)**: four N20-class gearmotors, one per wheel, in the side blocks; or two motors with coupled pairs.

### 2.4 Flipper plate (FP) and grip strip (GS)
- **Shape**: flat **aluminium, about 88 (X) × 42 (Y) × 2 mm**, brushed and scratched. Its **lip corners** are **chamfered ≈ 4 × 4 mm** (native (115, 400)); the rear corners are square.
- **GS**: along the lip, a strip about **8 mm wide** of **fine dot texture** (a grid of small dimples/dots, like grip tape or a perforated pattern), full width.
- **S-FP**: **three silver dome heads** (Ø ≈ 5, M3) **in a line along Y**, slightly right of centre (x ≈ +6), at about **6, 20 and 34 mm** from the rear edge (native (435, 177), (330, 242), (285, 370)), clamping FP to BK.
- **At rest (guess)**: flat on the side blocks at z 19–21, from y ≈ −8 (rear edge, just ahead of BL-B) to y ≈ +34 (lip, just inside the front bar).

### 2.5 Bracket (BK), pivot (PV), metal block (MB)
- **BK**: a **white printed triangular gusset**, about **45 long × 25 tall × 8 thick**, standing on edge in a YZ plane at **x ≈ +10**; its top edge is screwed under FP; its lower corner reaches back and down to the pivot boss on BL-B. Its lower edge is a concave curve.
- **PV**: a silver pan screw through a **white tab** (≈ 10 × 10 × 4, rounded top) on BL-B's front face, at about **(+12, −10, 12)**, axis X.
- **MB**: a **grey metal part** (≈ 6 × 6 × 8, rounded top) on the bracket near the plate's rear edge (native (385–420, 295–340)): a hinge-pin housing, stop or servo coupling **(guess)**. A **dark cylinder** near the pivot (native (430–470, 330–360)) may be the actuator output **(guess)**.

### 2.6 Wires (WR)
- Under the plate: **black and red wires** with a **white JST-style plug** (native (285–345, 460–530)). At the notch: **red and blue wires** and a small white part.

### 2.7 Actuator (hidden)
- **Guess**: a **micro servo** (9 g / MG90 class, 23 × 12 × 23) in the middle under the plate, output along X coupled to the bracket near the pivot.

---

## 3. Per-view sections

### 3.1 The photo (front-left, high, plate raised)
- The yellow L of the frame along the left and lower-left; black-and-red wheels at the corners; white blocks with silver screws; the big grey plate leaning toward the upper-left, dotted lip and three screws; the white bracket under it; wires in the shadow.

### 3.2 Top view (synthesised, plate at rest)
- A 92 × 72 yellow-rimmed rectangle; four 20 × 13 tyre rectangles at the corners; white side blocks (36 × 22) between each side's wheels; the white rear block (70 × 14); the aluminium plate (88 × 42) over the front-middle, dotted lip at the front, three screws in a line slightly right of centre.

### 3.3 Front view (plate at rest)
- The yellow front bar (92 × 10); the plate lip edge at z ≈ 21 behind it; tyres at the ends; total height about 22 mm.

### 3.4 Left side view
- The yellow left bar (72 × 10) covering the lower halves of two tyres; tyre tops, the white side block and the plate above. Raised, the plate stands up at the front, hinged near the rear block.

### 3.5 Rear and underside (not photographed)
- Rear: yellow rear bar, white rear block, rear tyres at the corners. Underside: flat floor with four tyre contacts **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| FR | ring bar | 92 × 72 outer; bar 4 × 10 | 1 × 0.78 | yellow FDM | integral floor / hidden | 1 |
| BL-L/R | side block | 36 × 22 × 18 | 0.39 × 0.24 | white FDM | 2 × M2 each | 2 |
| BL-B | rear block | 70 × 14 × 18 | 0.76 × 0.15 | white FDM | screws | 1 |
| WH | foam tyre + red hub | Ø 20 × 13 | 0.22 × 0.14 | black foam / red FDM | motor shaft | 4 |
| FP | chamfered plate | 88 × 42 × 2 | 0.96 × 0.46 | aluminium | 3 × M3 dome | 1 |
| GS | dot strip | 88 × 8 | — | textured | on FP | 1 |
| BK | gusset | 45 × 25 × 8 | 0.49 | white FDM | 3 screws + pivot | 1 |
| PV | screw + tab | M3; 10 × 10 × 4 | — | silver / white | on BL-B | 1 (+1 hidden?) |
| MB | metal block | 6 × 6 × 8 | — | grey metal | on BK | 1 |
| ACT | micro servo | 23 × 12 × 23 | — | — | pocket | 1 (guess) |

---

## 5. Contact / gap matrix (est. mm; plate at rest unless stated)

| A ↔ B | Relation | Gap |
|---|---|---|
| FR bottom ↔ floor | above | 1 |
| FR inner face ↔ tyre outer face | near | 2 |
| FR ↔ BL blocks | joined (guess) | 0 |
| BL ends ↔ tyres | near | 1–2 |
| Tyre ↔ floor | touching | 0 |
| Tyre top ↔ BL top | level | 0 |
| FP ↔ BL-L/R tops | resting on | 0 |
| FP lip ↔ FR-F top | resting on / just above | 0–1 |
| FP rear edge ↔ BL-B front face | near | 2 |
| FP ↔ BK | screwed (3) | 0 |
| BK ↔ PV | pivot | 0 |
| FP lip (raised 57°) ↔ deck | above | ≈ 35 |
| Front tyre ↔ rear tyre (each side) | fore-aft gap | 28 |

---

## 6. Mechanism
1. **Drive**: four-wheel skid steer (motors guessed), tyres inside the frame.
2. **Flipper**: the actuator rotates BK and FP about PV (axis X at y −10, z 12). The lip, about 46 mm from the pivot, rises about 35–40 mm at the photo's 57°. With a servo this is a **lift/flip**, not an explosive flip.
3. **Inverted**: tyre tops are level with the deck, so inverted it rests on its plate and blocks; the flipper can **self-right** **(guess)**.

---

## 7. Assembly order
1. Print the yellow frame (with floor, guess) and white blocks.
2. Fit the motors in the side blocks; press on red hubs with foam tyres.
3. Fit the servo in the middle, the battery, ESC/receiver, switch (perhaps at the notch NT); route wires.
4. Screw down the block lids.
5. Bolt BK to FP with three dome screws; stick the dot strip on the lip.
6. Mount BK on PV in the white tab on BL-B; couple to the servo.

---

## 8. Coordinate frame (restated)
- Origin O on the floor under the frame centre; +X along the axles (right), +Y toward the lip, +Z up; mm.
- Frame x ∈ [−46, 46], y ∈ [−36, 36], z ∈ [1, 11]. Blocks to z 19. Plate at rest z 19–21, y ∈ [−8, +34], x ∈ [−44, +44]. Pivot (+12, −10, 12), axis X.

## 9. Profiles as math
- **Frame (plan)**: rounded rectangle, outer corners r 6 (front) and r 8 (rear); inner offset 4.
- **Plate (u across, v from the rear edge)**: polygon (−44, 0), (44, 0), (44, 38), (40, 42), (−40, 42), (−44, 38). Screws at (6, 6), (6, 20), (6, 34). Grip strip v ∈ [34, 42].
- **Plate rotation** about P = (y −10, z 12) by θ: (y, z) → P + [[cos θ, −sin θ], [sin θ, cos θ]]·((y, z) − P). The lip (34, 20) at θ = 57° goes to (−10 + 44 cos 57° − 8 sin 57°, 12 + 44 sin 57° + 8 cos 57°) = (7.3, 53.3).
- **Bracket (YZ at x +12)**: triangle (−10, 12), (−6, 19), (30, 19); lower edge a concave arc centred (14, 40), r 28, from the pivot to (30, 19).
- **Tyre**: (y − y_c)² + (z − 10)² = 10², width 13.

## 10. Pixel-based measurements
Native 675 × 777, ±8 px.
- Frame corners: front-left (30, 550); rear-left (350, 720); rear-right (640, 310); front-right hidden ≈ (320, 140), from the parallelogram completion (30, 550) + (640, 310) − (350, 720).
- Y side: (320, 170), 362 px. X side: (290, −410), 502 px.
- Plate corners: (115, 400), (420, 30), (530, 120), (200, 515). Long edges 480 and 515 px; short edges 142–143 px (foreshortened by the tilt).
- WH-FL tyre: (95–185, 485–545), ≈ 90 px along Y.
- Screws: BL-L (220, 607), (360, 590); BL-R (505, 250); BL-B (530, 355); PV (480, 467); plate (435, 177), (330, 242), (285, 370).

## 11. Several independent estimates

| Quantity | Method A (kit / rules) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Frame width (X) | kit 80 (on the other axis) | plate long edge ≈ frame width (480–515 vs 502 px); plates are typically 85–90 | 502 px, corrected for ≈ 0.9 foreshortening → 558 px vs Y 362 → ratio 1.54 | **92** |
| Frame length (Y) | kit 90 | 92 / 1.54 = 60 | tyre 90 px of 362 → Ø/L = 0.25; with Ø 18–20 → 72–80 | **72** (see 12.1) |
| Tyre Ø | kit 20 | 0.25 × L → 18 | 90 px at ≈ 5 px/mm → 18; plus the visible height → 20 | **20** |
| Plate depth | — | short edge 142 px at 57° tilt: true ≈ 142 / 0.68 = 209 px → 42 at 5 px/mm | — | **42** |
| Frame bar height | — | ≈ 0.5 × tyre → 10 | ≈ 25 px vertical at ≈ 2.5 px/mm (vertical scale at this view) → 10 | **10** |
| Body height | kit 20 | tyre top ≈ block top → 20 | — | **19–21** |

## 12. Consistency check
1. **Width vs length**: the corrected pixel ratio suggests 92 × 60, but four Ø 20 tyres with a 28 mm gap and a 36 mm side block need about 72 mm. The small photo makes the foreshortening uncertain. **Reconciled 92 × 72.**
2. **Versus the earlier note**: the earlier note took the long lower bar as the left side and the short lower-left bar as the front (same as here) but sized the robot 95 long × 80 wide. Here the **long frame sides run along the axles** (the wheels on the lower edge face outward from it), so the robot is **wider than long**. Its "right rail" is here the **rear block** BL-B (it runs along the axle direction, between WH-RL and WH-RR), and its "rear block" is the **right side block** BL-R. The hinge result is the same: axis along X, plate across the robot.
3. **Wheel count**: the photo shows four (three visible, the fourth implied under the plate); the kit and REFERENCE.json say two. **Reconciled four** for a likeness build.
4. **Plate width vs frame inside (84)**: the plate rests on the block tops above the frame, so 88 can overhang the frame's inner edge. Consistent.
5. **Plate thickness**: about 2 mm at the raised far edge; the kit's 12 mm slab is wrong.

---

## 13. Why the designer did it (per part, mostly adversarial)

- **Yellow perimeter bumper (FR)**
  - Fight: a full ring round the wheels means **no tyre is exposed** to a horizontal spinner, wedge or flipper from any side. Low (10 mm, under the tyre tops), it doesn't stop the robot driving when tilted and gives a wedge only a thin edge. Side pushes land on the bumper, not the foam.
  - Getting under vs contact: the bumper sits 1 mm off the floor and is not a wedge, so an opponent can still get under it; Io relies on the plate, not the bumper, for getting under.
  - Construction: bright yellow for visibility and identity; a ring is stiff for little mass.
- **Foam tyres on flanged hubs**
  - Fight: foam grips smooth arena floors for pushing; flanges stop the foam peeling off sideways. Foam tears when hit, which is why the frame shields it.
- **White blocks with screwed lids**
  - Construction: one block per function (sides: motors; rear: pivot and probably the battery); M2 lids give quick pit access.
  - Fight: they make a rigid box with the frame; the rear block takes the flipper's reaction loads.
- **Aluminium plate with grip strip (FP, GS)**
  - Getting under vs contact: at rest the lip sits just behind the low front bumper; Io must slip it under an opponent's edge (or let the opponent ride onto the bumper). The **dot texture** grips the opponent's underside so it doesn't slide off while lifted.
  - Fight: the plate also **armours the top** against overhead hits; 88 mm wide, it works on an opponent met anywhere across the front.
  - Construction: a cut aluminium off-cut with three screws into a printed bracket: cheap, strong, quick to replace.
- **Triangular bracket on a low rear pivot (BK, PV)**
  - Fight: a low pivot toward the rear gives a ≈ 46 mm lever, so the lip travels ≈ 40 mm for a modest servo rotation; the triangle keeps the arm stiff so the plate doesn't twist when lifting off-centre.
  - Weak point: one pivot screw and a printed tab take the whole lift load; a hit on the raised plate can crack the tab.
- **Servo actuator (guess)**
  - Construction: cheap, light, self-contained, enough to lift a 150 g opponent with this lever; also self-rights.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors | 12 × 10 × 25 | in the side blocks, shafts at (±26, ±24, 10) | medium |
| Flipper servo | 9 g metal-gear micro servo | 23 × 12 × 23 | middle (0, +4, 10), output along X at (+12, −10, 12) | medium |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 10 | in BL-B, (0, −27, 10) | medium |
| ESC + receiver | combined board | 30 × 17 × 5 | front-middle under the plate, (0, +18, 6) | low |
| Switch | slide switch at the notch NT | 10 × 5 × 5 | (−36, −12, 12) | low |
| Floor | yellow floor printed with the frame | 92 × 72 × 1.5 | z 1–2.5 | low |
| Second pivot | a screw on the bracket's left or a pin through BL-B | — | (−12, −10, 12) | low |
| Wires | battery → switch → ESC → motors and servo | — | seen under the plate and at the notch | high (some seen) |

## 15. What the photo cannot show
- The rear, right side, underside and everything under the plate.
- Actuator type, motor count, pivot details.
- Exact proportions (one small, high photo with uncertain foreshortening).
- All mm values ±15%.

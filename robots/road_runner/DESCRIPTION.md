# Road Runner: full rebuild description from reference photos

Source photos (in `robots/road_runner/reference/`):
- `road_runner.aws63.webp` (1335 × 1116 px): a home photo on a **dark wooden table**, not cut out. A **three-quarter view from the front-left, about 40° above horizontal**. The front bumper runs from the image left to the lower middle, the robot's left side (blue) runs up the image right. The whole top is visible.
- `road_runner.aws67.webp` (1280 × 928 px): cut out onto white. A **straight-on front view, about 35° above horizontal**. The bumper face is square to the camera, the top lid is seen foreshortened above it. This version has a **taped lower front panel** and an **extra round hole** in the lid.

Everything stated as fact is read from those photos. Anything inferred is marked **(guess)** with a confidence. Dimensions are **estimates in mm**, scaled from the AWS antweight limits (150 g, fits a 101.6 mm cube) and the photo proportions, and cross-checked against the project spec draft (`spec.json`: a chassis tub with rear wall and side walls, a lid, four wheels with two drive motors at the front pair and idler axles on the rear pair, a scoop, bumper ends, two horns and three sticker parts). **W = blue tub outer width ≈ 92 mm** is the ratio base.

**Evidence limits**: the rear and the underside are never seen, and the right side is seen only from inside the tub frame. So the rear wall, floor and inner layout are inferred. Otherwise the two photos are sharp and show the top and front in detail.

Road Runner is a **flat four-wheel box pusher / wedge** in two colours: a **blue printed tub** whose walls surround all four wheels, a **purple cross-shaped lid** with a **Road Runner cartoon sticker**, and a **purple full-width front bumper** with two small **conical horns**.

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) under the centre of the blue tub (mid-width, mid-length, **bumper excluded**).
- **+X** = robot's right, **+Y** = forward (toward the purple bumper), **+Z** = up. Units mm.
- In AWS67 the camera faces the front, so the **robot's right is on the image left**. In AWS63 the camera is at the **front-left**: the bumper runs across the lower left, the robot's **left side** is the blue wall running up the image right, and the robot's right side is at the far upper left.

Part IDs:

| ID | Part |
|---|---|
| TB | blue printed tub (floor + four walls) |
| SW-L / SW-R | blue side walls (also the outer wheel guards) |
| RW | blue rear wall |
| LD | purple cross-shaped lid |
| LC-1…4 | lid corner cut-outs over the wheels |
| SQ | square hole in the lid (switch access) |
| RH | round hole in the lid (AWS67 only) |
| ST | Road Runner sticker |
| BP | purple front bumper (vertical plate) |
| BE-L / BE-R | bumper angled end pieces |
| HN-L / HN-R | small purple conical horns on the bumper's top corners |
| LP | lower front panel with purple tape (AWS67 only) / scoop |
| TP | purple tape on LP |
| WH-FL, WH-FR, WH-RL, WH-RR | four black gear-tread wheels |
| S-LD | lid screws (black Phillips) |
| S-BP | bumper screws (black, on the bumper face) |
| DM-x, AX-x, MM-x | drive motors, idler axles, motor mounts (hidden, guess) |
| BAT, ESC, RX, SWT | electronics (hidden, guess) |

---

## 1. Overall description in one paragraph

Road Runner is a **low, square, two-colour box pusher** about **92 mm wide, ≈ 96 mm long (incl. bumper) and ≈ 26 mm tall**. The base is a **bright blue tub** (blue PLA/PETG) with **thin, straight walls** about 2.5 mm thick, open at the top, whose **four inside corners are wheel wells**: each of the **four black gear-tread wheels (Ø ≈ 26)** sits inside the blue wall, so the **side walls are full-length wheel guards**. The top is closed by a **purple lid** shaped like a **plus/cross**: full width in a central band and between the wheels at front and back, with the **four corners cut away** so the wheel tops show. The lid has **diagonal infill lines**, **nine black Phillips screws** around its edge, a big **Road Runner (Looney Tunes) sticker**, a **square hole** about 12 mm across (with a dark switch or component inside), and in AWS67 a **round hole** about 7 mm across. Across the front is a **purple bumper**: a **vertical plate the full width of the tub** with **angled ends** that wrap back to the side walls, **four black screws** in a row along its face, and **two small purple cone "horns"** at its top corners. In AWS67 the lower ≈ 40% of the front is a separate, slightly recessed **panel covered in purple masking tape**.

---

## 2. Part-by-part description

### 2.1 Blue tub (TB)
- **Shape**: an open-topped rectangular box, **x ∈ [−46, +46] (92 mm)**, **y ∈ [−44, +38] (82 mm)**, **z ∈ [2, 24]** (≈ 22 mm wall height; floor clearance ≈ 2 mm **(guess)**).
- **Walls**: **≈ 2.5 mm** thick (AWS63 shows a thin blue rim around the lid, with the inner face visible in the right-rear corner well). The outer faces are **flat and vertical**, with fine **horizontal layer lines** (AWS63's left wall shows them clearly at px ≈ (850–1300, 280–890)).
- **Corners**: sharp outside corners (radius ≤ 1 mm).
- **Colour**: **bright, saturated mid-blue** with a slight sheen (PLA or PETG).
- **Floor**: not seen. Openings under each wheel let the tyres reach the floor **(guess, high)**.

### 2.2 Side walls / wheel guards (SW-L, SW-R) and rear wall (RW)
- **SW-L / SW-R**: full-length plain walls, **82 mm long × 22 mm tall**, that run **outside the wheels**. They cover the wheels' outer faces completely: only the tyres' **tops** are visible from above (through the lid corner cut-outs).
- **Wheel-to-wall gap**: AWS63's right-rear well (image top centre, px ≈ (520–660, 45–135)) and left-front well (px ≈ (750–970, 560–740)) show **≈ 1.5–2 mm** between the tyre and the blue wall's inner face.
- **RW**: the rear wall is never seen face-on; its top edge is visible in AWS63 (px ≈ (580–1300, 30–270)) and AWS67 (px ≈ (175–1080, 60–75)) as a thin blue strip. Presumed plain **(guess)**.
- **Guard-to-chassis support**: the guards **are** the tub walls, joined to the floor along their whole length and to the front/rear walls at the corners. There are no separate guard struts.

### 2.3 Lid (LD) and corner cut-outs (LC)
- **Material / colour**: **purple** FDM, about **3 mm** thick, with clearly visible **diagonal (±45°) infill/top-skin lines** and **two or three diagonal bands** where the top skin changes direction (AWS67 shows long diagonal streaks).
- **Plan shape**: a **cross** made of:
  - a **central band** spanning nearly the full inner width, **x ∈ [−43, +43]**, **y ∈ [−16, +12]** (≈ 28 mm deep), its ends sitting on the side walls' tops;
  - a **front tongue**, **x ∈ [−30, +30] (60 mm)**, **y ∈ [+12, +37]**;
  - a **rear tongue**, **x ∈ [−30, +30]**, **y ∈ [−43, −16]**.
- **Corner cut-outs LC**: four rectangles **≈ 13 mm wide (X) × 26–27 mm long (Y)**, one over each wheel.
- **Height**: the lid top is at **z ≈ 26–27**, i.e. it **sits on the wall tops** (≈ 0.5 mm proud of the blue rim, AWS63).
- **Re-entrant corners**: sharp (square notches).
- **Edges**: the lid's outer edges are slightly **inside** the blue wall's outer faces (the blue rim shows around the whole lid, ≈ 2.5 mm).

### 2.4 Lid screws (S-LD)
- **Type**: **black Phillips pan/button heads**, head Ø ≈ **4.5 mm**, probably **M2.5 or M3** into the tub walls or internal posts.
- **Positions (robot frame; consistent in both photos)**:
  - Rear tongue edge: **2** at (±7, −40).
  - Central band, right end: **2** at (+40, −10) and (+40, +6).
  - Central band, left end: **2** at (−40, −10) and (−40, +6).
  - Front tongue edge: **3** at (−18, +34), (0, +34), (+18, +34).
  - **Total: 9.**
- AWS63 (mirrored to robot frame): rear-right pair at px (475, 147) and (385, 212) [the right band end], rear pair (860, 128), (950, 163), left band pair (1085, 420), (995, 510), front row (360, 460), (455, 515), (555, 572). AWS67: rear pair (565, 82), (690, 85); right band (215, 220), (210, 300); left band (1060, 235), (1080, 318); front row (500, 490), (655, 483), (805, 490).

### 2.5 Square hole (SQ) and round hole (RH)
- **SQ**: a **square through-hole ≈ 12 × 12 mm** at about **(−12, +5)** (robot left of centre, slightly forward). In AWS63 (px ≈ (785–840, 375–420)) the inside is dark; in AWS67 (px ≈ (790–860, 265–310)) a **black ribbed surface** is visible inside: it looks like a **wheel tread or the knurled top of a component**, or the **switch** body **(guess: the access hole for a slide switch or a link, medium)**.
- **RH (AWS67 only)**: a **round hole Ø ≈ 7 mm** at about **(+0, +18)** on the front tongue (px ≈ (705–765, 380–420)). The inside shows **purple** (a purple part below, perhaps the bumper back or a purple key). It may be a **removable link** socket or a **screwdriver access hole** **(guess, low)**.

### 2.6 Sticker (ST)
- A die-cut **Road Runner** cartoon sticker with a **white border**, about **55 mm wide × 40 mm tall** in the lid plane. The bird is **running to the robot's left** (its head at the robot's left-rear, its legs and tail at the robot's right-front in AWS67; the photos show it rotated relative to each other because the sticker is laid diagonally).
- Colours: **light blue/cyan** body, **dark blue** head crest, **orange** legs and beak, white outline.
- Position: centred at about **(+2, −2)**, covering most of the central band and parts of both tongues.

### 2.7 Front bumper (BP) and ends (BE-L, BE-R)
- **Main plate BP**: a **vertical purple plate**, about **4–5 mm thick (Y)**, spanning **x ∈ [−40, +40]** on its front face, from **z ≈ 0** to **z ≈ 24** (AWS63) — or from **z ≈ 10** to **z ≈ 24** above the taped panel (AWS67). Its front face is at **y ≈ +44**, i.e. ≈ 6 mm ahead of the tub's front wall.
- **Lean**: the face leans back slightly, about **5–10° from vertical** (AWS63 shows a slight top-back lean).
- **Top edge**: a narrow **chamfer** (≈ 1.5 mm) along the top front edge.
- **Ends BE**: the plate's ends turn back at about **45° in plan**, forming **angled end facets ≈ 8 mm long** that run from (±40, +44) back to the tub corners at (±46, +38). In AWS63 the left end (image bottom right, px ≈ (780–860, 780–1000)) and the right end (image left, px ≈ (60–130, 380–600)) are both visible as sloped faces. The bumper's overall outline in plan is therefore a **flat trapezoid** hugging the front of the tub. The spec names these `bumper_end_l/r`.
- **Layer lines**: horizontal, fine.
- **Screws S-BP**: **four black screws** in a horizontal row along the face at **z ≈ 14** (AWS67: px (325, 680), (528, 665), (780, 675), (985, 690), i.e. x ≈ ±12 and ±31). In AWS67 two of them (the outer ones) are **socket cap heads** that look **raised ≈ 3 mm** from the face (longer screws with spacers or simply not fully seated), and the inner two are **Phillips pan heads**. In AWS63 the four are flush **Phillips** heads (px (190, 545), (305, 615), (465, 720), (605, 820)). They fix the bumper into the tub's front wall **(guess, high)**.

### 2.8 Horns (HN-L, HN-R)
- **Shape**: **small purple cones** about **Ø 5 mm at the base × 7–9 mm tall**, with **rough, stringy tips** (they look printed point-up, ending in a stringy tip). They stand on the **top of the bumper** at its **outer corners** (AWS67 px ≈ (155–200, 530–625) and (1110–1160, 545–640); AWS63 px ≈ (60–130, 390–460) and (680–760, 780–880)).
- **Lean**: they lean **forward and slightly outward** about **20–30°** from vertical (AWS63 shows both pointing forward).
- **Interpretation**: decorative "horns", or **spikes to catch** an opponent's edge when the opponent rides up the bumper **(guess)**. The spec names them `horn_l/r`.

### 2.9 Lower front panel (LP) with tape (TP), AWS67 only
- **Shape**: a **rectangular panel** across the lower front, **≈ 84 mm wide × 10 mm tall**, below the bumper's lower edge. It sits **recessed ≈ 2 mm** behind the bumper face, outlined by a **dark shadow line** (px ≈ (115–1225, 700–845)).
- **Surface**: covered with a strip of **purple masking/washi tape** about **70 × 8 mm** (lighter, mottled texture, px ≈ (150–1140, 715–835)).
- **Interpretation (guess, medium)**: the **front of a separate low scoop/wedge plate** (`scoop` in the spec) whose front face is taped. The tape makes it slick and protects it. Alternatively the bumper is split into an upper plate and a lower replaceable skirt.
- **AWS63**: no separate panel. The bumper face appears to run to the floor, so the AWS67 panel is a later modification **(guess)**.

### 2.10 Wheels (WH-FL, WH-FR, WH-RL, WH-RR)
- **Shape**: **Ø ≈ 26 mm × 10–11 mm wide**, black, with a **deep gear-tooth tread** of about **30–34 square teeth** (each ≈ 2 mm deep, ≈ 2 mm wide), like a coarse spur gear (AWS63's left-front wheel px ≈ (790–970, 560–740) shows the teeth clearly).
- **Hub**: a **black inner disc** behind the tread (AWS63 left-front wheel shows a dark hub face inboard).
- **Material**: black **TPU** (printed, typical of gear-tread antweight wheels) **(guess, medium)**.
- **Positions (centres)**: **(±37, ±25, 13)**. Wheelbase **≈ 50 mm** (front-to-rear centres), track **≈ 74 mm** (centre-to-centre).
- **Height**: tyre top at **z ≈ 26**, about **level with the lid top**, so the robot **may be able to drive inverted** on the wheel tops and lid edges, but only just **(guess)**.
- **Running gaps**: tyre to wall ≈ 1.5–2; tyre to lid cut-out edges ≈ 1–2; tyre fore-aft to the front/rear walls ≈ 2–3.

### 2.11 Wiring and switch
- **No wires are visible.** The switch is most likely under the **square hole SQ** **(guess, medium)**.

---

## 3. Per-view sections

### 3.1 AWS63 (front-left, ≈ 40° above)
- **Silhouette**: a flat rhombus (the square box in perspective) with the purple bumper strip along the near-left edge and the blue wall along the near-right edge.
- **Top**: the purple cross with 9 screws, the sticker and the square hole; four black gear wheels in the corner cut-outs (rear-right px (520–660, 45–135), front-right px (190–320, 250–380), rear-left px (1095–1230, 280–380), front-left px (790–970, 560–740)).
- **Front**: the bumper's sloped right end at the image far left, its face with 4 screws, its left end at the bottom right, and the 2 horns.
- **Left side**: the blue wall with layer lines and no features.

### 3.2 AWS67 (front, ≈ 35° above)
- **Silhouette**: a wide rectangle (bumper and taped panel at the bottom, ≈ 1160 px wide) with the lid trapezoid above it (wider at the front, narrower at the back).
- **Top**: the lid with 9 screws, the sticker, the square and round holes; the four wheels in the corner cut-outs (rear pair at px (200–280, 85–190) and (985–1075, 105–200); front pair at (160–255, 360–510) and (1035–1160, 370–520)).
- **Front**: the bumper (px y 520–700) with 2 horns and 4 screws; the taped lower panel (px y 700–845).

### 3.3 Top view (synthesised)
- A **92 × 82** blue rectangle with a 2.5 mm rim, the purple cross inside it (band 86 × 28, tongues 60 wide), four **11 × 26** tyre rectangles in the corners at (±37, ±25), the bumper trapezoid ahead (80 mm front face, 92 mm at the back, 6 mm deep) with horn dots at its corners.

### 3.4 Front view (synthesised)
- A 92 × 26 rectangle. The bumper face (80 wide plus angled ends) covers z 10–24 (AWS67) or z 0–24 (AWS63); the taped panel below; the horns standing up at the top corners to z ≈ 32. The wheels are hidden behind the bumper; their tops show just above the lid line at the corners.

### 3.5 Side view (synthesised)
- An 82 × 22 blue rectangle (z 2–24), the lid edge on top (z 24–27), the bumper ahead (y 38–44), the horn tip leaning forward at the top front. No wheels visible from the side (guards).

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| TB | open box | 92 × 82 × 22, wall 2.5 | 1 × 0.89 × 0.24 | blue FDM | — | 1 |
| LD | cross plate | 86 × 80 × 3 (band 28 deep, tongues 60 wide) | 0.93 × 0.87 | purple FDM | 9 screws | 1 |
| SQ | square hole | 12 × 12 | 0.13 | — | — | 1 |
| RH | round hole | Ø 7 | — | — | — | 1 (AWS67) |
| ST | sticker | 55 × 40 | 0.6 | multicolour vinyl | adhesive | 1 |
| BP | vertical plate | 80 × 4.5 × 24 (or 14) | 0.87 | purple FDM | 4 screws | 1 |
| BE | angled end | 8 × 4.5 × 24 | — | purple | integral with BP | 2 |
| HN | cone | Ø 5 × 8 | — | purple | integral with BP | 2 |
| LP | panel | 84 × 10 × 3 | 0.91 | purple + tape | under BP (guess) | 1 (AWS67) |
| WH | gear-tread wheel | Ø 26 × 10.5 | 0.28 × 0.11 | black TPU | motor shaft / axle | 4 |
| S-LD | Phillips pan | head Ø 4.5 | 0.05 | black | into tub | 9 |
| S-BP | Phillips pan / socket cap | head Ø 4.5 | — | black | bumper to tub | 4 |

---

## 5. Contact / gap matrix (estimated mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD underside ↔ TB wall tops | rests on, screwed | 0 |
| LD outer edge ↔ TB outer face | inset | 2.5 |
| BP back face ↔ TB front wall | screwed | 0 (or a ≈ 1–2 spacer) |
| BE ↔ TB front corners | butted | 0 |
| HN ↔ BP top | integral | 0 |
| LP ↔ BP lower edge | under it, recessed | 2 back |
| LP bottom ↔ floor | near | 0–1 |
| BP bottom ↔ floor (AWS63) | near | 0–2 |
| WH tyre ↔ SW inner face | running gap | 1.5–2 |
| WH tyre ↔ LD cut-out edges | side gap | 1–2 |
| WH tyre ↔ front/rear wall | fore-aft gap | 2–3 |
| WH top ↔ LD top | about level | 0 ± 1 |
| WH bottom ↔ floor | contact | 0 |
| TB floor ↔ floor | clearance | ≈ 2 |
| WH-FL ↔ WH-RL | tyre gap | ≈ 24 |
| ST ↔ LD | stuck | 0 |

---

## 6. Mechanism

1. **Drive**: four wheels, **skid steer**. The spec drives the **front pair** with two motors (`dm_wheel_l0/r0`) and puts the **rear pair on idler axles** (`dt_axle_wheel_l1/r1`). The photos cannot confirm that, but there is no belt or chain visible, so either **4 motors** or **2 motors + 2 free idlers** **(guess: 2 motors front + 2 idlers, medium; 4 motors, medium–low)**.
2. **Weapon**: none active. The bumper is a **pushing face**; the lower taped panel (AWS67) is a **low scoop** that helps get under.
3. **Invertibility**: marginal; the wheel tops are about level with the lid.

---

## 7. Assembly order (suggested rebuild)

1. Print **TB** (floor on the bed), with motor pockets and screw bosses.
2. Install the **motors** in **printed clamps** at the front corners; the **idler axles** at the rear corners (steel pins through the side walls, guess). Fit the **wheels**.
3. Install **battery, ESC, receiver and switch**; route the wires.
4. Screw the **bumper BP** (with ends and horns) to the front wall with **4 screws**. AWS67: fit the **lower panel LP** under it and apply the **tape**.
5. Screw on the **lid LD** with **9 screws**.
6. Apply the **sticker**.

---

## 8. Profiles as math (for rebuilding curves)

**8.1 Lid outline (XY, z 24–27).** Polygon:
(−30, −43) → (+30, −43) → (+30, −16) → (+43, −16) → (+43, +12) → (+30, +12) → (+30, +37) → (−30, +37) → (−30, +12) → (−43, +12) → (−43, −16) → (−30, −16) → close.
Square hole: x ∈ [−18, −6], y ∈ [−1, +11]. Round hole (AWS67): circle centre (0, +18), r = 3.5.

**8.2 Bumper plan (XY, z 0/10 to 24).** Front face line y = +44 for x ∈ [−40, +40]; ends: **y = 44 − (|x| − 40)** for |x| ∈ [40, 46] (45° facets); back face y = +38 against the tub. Thickness of the front plate: 4.5 (so back face at y = 39.5 except at the ends).

**8.3 Bumper side profile (YZ, AWS63 version).** Front face from (y +44, z 0) to (y +42, z 24): a 4.8° back-lean, i.e. **y = 44 − 0.083·z**. Top chamfer 1.5 × 45°.

**8.4 Horn (cone).** Axis from base (±38, +42, 24) to tip (±40, +46, 31.5): base radius 2.5, tip radius 0.3; the axis leans forward 28° and outward 15°.

**8.5 Wheel tread (in the wheel frame).** Root radius 11; N = 32 square teeth, 2 mm tall: **r(φ) = 11 + 2·[sin(32·φ) > 0]**, φ ∈ [0, 2π). Width 10.5.

**8.6 Taped panel (AWS67).** Rectangle x ∈ [−42, +42], z ∈ [0.5, 10.5], face at y = +42 (2 mm behind the bumper face). If it is a scoop, its true section is a ramp from (y +46, z 0) up to (y +40, z 10) (≈ 59°) **(guess)**.

---

## 9. Pixel-based measurements (independent check)

**AWS67 (1280 × 928):**
- Bumper face: px x 70 → 1230 (≈ 1160 px) at y ≈ 520–700; taped panel px x 115 → 1225, y 700–845.
- Blue tub at the lid's rear edge: px x 175 → 1085 (≈ 910 px; farther from the camera).
- Lid front edge: px x 255 → 1135 (880 px) with the tongue; the band px x 160 → 1135.
- Front wheels: right (image left) px (160–255, 360–510), left (image right) px (1035–1160, 370–520).
- Square hole: px (790–860, 265–310). Round hole: px (705–765, 380–420).
- Horns: ≈ 45 px wide × 95 px tall.
- Scale at the bumper face: 1160 px / 92 mm ≈ **12.6 px/mm**.

**AWS63 (1335 × 1116):**
- Bumper face from px (60, 400) to (850, 1000): ≈ 990 px along its length.
- Left blue wall from px (850, 890) to (1300, 280): ≈ 760 px (foreshortened).
- Left-front wheel: ≈ 180 × 180 px.
- Screw heads: ≈ 30 px.

---

## 10. Several independent estimates of key quantities

| Quantity | Method A (limits / spec) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Tub width | cube ≤ 101.6, square body | lid band / bumper ≈ 0.93 | AWS67: 1160 px at 12.6 px/mm (defined) ; rear rim 910 px / ≈ 10 px/mm (farther) = 91 | **92** |
| Tub length | — | AWS63: left wall 760 px vs bumper 990 px; foreshortening of the wall ≈ 0.75 → 760/0.75 = 1013 px ≈ 1.02 × bumper → 94 incl. bumper | AWS67 lid depth ≈ 0.9 × width after correcting for the 35° view (lid px 75 → 520 = 445 px / sin 35° ≈ 776 px / 9.5 px/mm (mid-depth) ≈ 82) | **82 + 6 bumper = 88** |
| Wheel Ø | — | wheel ≈ tub height + 2 → 26 | AWS67 front wheels 150 px tall (seen from 35° above, the tread top visible) / 12 ≈ 12.5 ×… (partly hidden) ; AWS63 left-front wheel ≈ 180 px / 7 px/mm (at that depth) ≈ 26 | **26** |
| Wall height | — | 0.24 W | AWS63 left wall ≈ 150 px tall at ≈ 7 px/mm = 21 | **22** |
| Bumper height | — | — | AWS67: 180 px / 12.6 = 14 (upper part); + panel 145 px → 11.5; total 25.5 | **24–26** |
| Lid screw head | M2.5–M3 pan ≈ 4.5–5.5 | — | AWS67 ≈ 55 px / 12.6 = 4.4 | **4.5** |
| Square hole | — | ≈ 0.13 W | AWS67 70 px / ≈ 10.5 px/mm = 6.7?? (foreshortened in Y only; X 70 px → 6.7) ; AWS63 55 px / 7 = 7.9 | **≈ 9–12** (see §11) |

---

## 11. Consistency check: conflicts and reconciliation

1. **Square hole size.** The two pixel estimates (6.7 and 7.9) are smaller than my first visual impression (12). Both photos agree on ≈ 7–8 mm, which also matches a typical switch-lever access. **Reconciled: 9 mm square.**
2. **Overall length vs the cube.** 82 + 6 = 88 mm (≤ 101.6). The robot is **square-ish (92 × 88)**. **Consistent.**
3. **Wheel tops vs lid.** A 26 mm wheel at z = 13 reaches z = 26, the lid top is z = 26–27. AWS63 shows the tyres' tops slightly **below** the lid surface (the lid edge casts a shadow on them). **Reconciled: wheels Ø 25–26, tops ≈ 1 mm below the lid top → not reliably invertible.**
4. **Bumper bottom (AWS63 floor-length vs AWS67 panel).** Two versions; the AWS67 version adds a separate low panel. **Build AWS67 as current, AWS63 as variant.**
5. **Which wheels are driven.** The spec says front pair; with the bumper at the front the front wheels carry more load when pushing, so driving the front is sensible. **Accepted (medium).**

---

## 12. Why the designer did it (per part, mostly adversarial)

- **Blue tub with walls outside the wheels**
  - Attacks: horizontal spinners and side-on wedges hit the **flat blue wall**, not the tyres. A tyre is the most fragile and the most "grabbable" part of a small robot; hiding it removes both problems.
  - Getting under vs contact: the walls are vertical with ≈ 2 mm floor clearance, so a thin wedge can still get under from the side. The robot is designed to **meet opponents front-on** with its bumper.
  - Construction: the simplest possible print, no supports, and all four corners are the same.
- **Cross-shaped lid**: the cut-outs give the wheels room to stand nearly level with the top (helping invertibility) without making the tub taller, and save weight. The full-width band braces the side walls together between the wheels against side hits. Nine screws make it rigid but quick to remove.
- **Square / round holes**: switch and link access without removing the lid (the AWS safety check requires the robot to be armed and disarmed quickly). Small holes mean a weapon cannot reach the switch.
- **Purple bumper (vertical, full width, with angled ends)**
  - Pushing: a flat full-width face gives a stable push. The angled ends **deflect** an opponent who hits the front corner sideways instead of letting them catch the corner and spin the robot.
  - Attacks: vertical spinners meet a 4.5 mm plate screwed at four points to the tub front wall, which spreads the hit. It is replaceable.
  - Getting under vs contact: a vertical bumper only **makes contact**. That is why the AWS67 version adds a **low taped panel/scoop**, so the front edge sits on the floor and can get under opponents.
- **Tape on the lower panel**: slick tape helps opponents slide up; it also covers print layer edges that could catch and lets a fresh strip be applied after damage.
- **Horns**: likely cosmetic (a nod to the cartoon, or just "spikes"); they could catch an opponent's edge and stop it sliding sideways off the bumper.
- **Gear-tread TPU wheels**: high grip for pushing. Four wheels keep traction when one end is lifted by an opponent's wedge.
- **Sticker**: theme (Road Runner, "meep meep": a fast pusher).

---

## 13. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors DM | 2 × N20 gearmotors (front) | 12 × 10 × 25 + 9 shaft | along X at (±22, +25, 13), shafts outward | medium |
| Rear idler axles AX | steel pins Ø 3 through the side walls into the rear wheel hubs | Ø 3 × 15 | (±40, −25, 13) | medium (spec) |
| Motor mounts MM | printed **U-clamps** on the tub floor with 2 × M2 each | 16 × 14 × 14 | over each motor | medium |
| Battery | 2S LiPo, 180–300 mAh | 40 × 20 × 10 | centre-rear, (0, −20, 8) | medium |
| ESC | dual brushed ESC | 25 × 15 × 5 | (+15, 0, 6) | low |
| Receiver | micro 2.4 GHz | 20 × 12 × 5 | (−15, −5, 6) | low |
| Switch | mini slide switch, lever up under SQ | 12 × 6 × 6 | (−12, +5, 18) | medium |
| Screw bosses | Ø 6 posts under the 9 lid screws and 4 bumper screws | Ø 6 × 20 | at the screw positions | medium |
| Wiring | battery → switch → ESC → 2 motors; RX → ESC | — | — | high (exists) |

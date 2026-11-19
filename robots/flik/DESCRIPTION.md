# Flik: full rebuild description from reference photos

Source photos:
- `robots/flik/reference/flik.aws70.webp` (1200 × 884 px): AWS 70, cut out onto white. **Front-left three-quarter** (`REFERENCE.json`: azimuth 120, elevation 35). The big yellow flipper plate faces the image bottom-left, the robot's **left side panel** is on the image right, and the top lid recedes to the image top. Two black knurled corner bosses with silver socket screws are at the top right (the rear-left corner).
- `robots/flik/reference/flik.aws73.webp` (866 × 784 px): AWS 73, pit photo on a black/pink event towel. **Front-left, high (about 55–60°)**, the camera looking down at the lid. It shows the **"FLIK" marker writing** on the lid, the **exposed black deck with the ON/OFF slide switch and a red/black ON/OFF sticker**, both **clear polycarbonate stop tabs**, a cracked lid corner, both rear corner boss pairs, the left wheel inside the side panel, and a large **clear plastic skirt sheet** under and ahead of the flipper (only in this event). Screwdrivers lie at the bottom right.
- `robots/flik/reference/flik.aws74.webp` (1200 × 858 px): AWS 74, cut out onto white. **Front-right three-quarter** (azimuth 60, elevation 35). The flipper faces the image bottom, the robot's **right side panel** is at the image left, the lid has "FLIK" and "ON ↔ OFF" with arrows written near its rear edge, the right clear stop tab sticks out sideways at the image left, and a **green item** peeks out at the far top-right corner of the flipper (the robot's left hinge end).

Pixel coordinates refer to the jpg copies at the sizes given above, read by eye, ±10 px.

Facts are read from the photos. Inferences are marked **(guess)** with a confidence **H/M/L**. Dimensions are estimates, scaled from the AWS antweight rules (150 g, 101.6 mm cube) and from typical sheet thicknesses (1.5–2 mm) and screw heads (M3 button head ≈ Ø 5.7 mm, M3 socket cap ≈ Ø 5.5 mm). Ratios are given against **W = frame width between the side panels ≈ 80 mm**.

Robot class: **servo wedge-flipper** (`REFERENCE.json`: flipper, 2 wheels, axis x). The whole front wedge is a single plate hinged along its **upper (rear) edge** about a transverse X axis at the top-front of the box. At rest it slopes down to the floor as a wedge. When the servo fires, the plate rotates up about that top hinge, the front edge swings upward and forward, and an opponent sitting on the wedge is flicked up, hence **"Flik"**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the flipper's leading edge), **+Z** = up.
- **Origin O** = the floor point at mid-width, placed so that the black frame spans **y −42 (rear face) … +15 (hinge line)**. The frame's own plan centre is therefore at y −13.5. (O is close to the robot's overall mid-length, which runs −43 … +56.)
- **Flipper angle β** = the plate's slope below horizontal, measured from the hinge. Rest β₀ ≈ 36°. A firing rotation **θ** lifts the plate: β = β₀ − θ.
- Left/right are the robot's own. aws70 shows the **left** side, aws74 the **right** side, and aws73 the left side from high.

| ID | Part |
|---|---|
| FR | black printed frame / tub (box between the side panels) |
| DK | exposed front deck of FR between the lid and the hinge (switch area) |
| SW | slide power switch in DK |
| ST | ON/OFF sticker (red "ON" arrow, black "OFF" arrow) on DK |
| CS-1, CS-2 | two countersunk holes/screws in DK |
| LD | yellow top lid plate, marker "FLIK" and "ON ↔ OFF" |
| S-LD | lid screws (silver button heads, 4) |
| SP-L / SP-R | yellow side panels (also the wheel guards) |
| S-SP | side panel screws (silver button heads) |
| S-FR | frame screws visible at the front corners (silver socket cap) |
| FP | yellow flipper / wedge plate |
| S-FP | 2 flipper screws (silver button, with swirl marks) |
| TP-FP | clear tape band over the lower part of the flipper |
| SK | large clear skirt sheet under the flipper (aws73 only) |
| TB-L / TB-R | clear polycarbonate stop tabs at the flipper's upper corners |
| S-TB | tab screws (silver button) |
| HG | flipper hinge (hidden under the plate's upper edge, guess) |
| RB-L1, RB-L2, RB-R1, RB-R2 | black knurled rear corner bosses with M3 socket cap screws (RS) |
| WH-L / WH-R | black rubber drive wheels, enclosed by the side panels |
| DM-L / DM-R | drive gearmotors (hidden, guess) |
| SV | flipper servo (hidden, guess) |
| LK | servo-to-flipper linkage (hidden, guess) |
| RX, ESC, BAT | receiver, drive ESC, LiPo (hidden, guess) |
| GR | green item at the left hinge end (aws74), probably a green tab or LED |
| WR | wiring (hidden) |

---

## 1. Overall description in one paragraph

Flik is a **compact box-wedge** with a **full-width hinged wedge plate** as its weapon. The core is a **black 3D-printed frame** about 80 mm wide, 57 mm long and 32 mm tall. Two flat **yellow sheet side panels** (about 1.6 mm thick, 90 mm long, 32 mm tall, with the front edge cut on a slant to follow the wedge) are bolted to it with silver button-head screws. They hide the two **black rubber drive wheels** at the rear and act as wheel guards. The top is a **yellow lid** about 64 × 45 mm with four screws and marker writing. Ahead of it, a strip of the black frame's top deck stays exposed. That strip holds a **slide switch** with an ON/OFF sticker and two countersunk screws. The front is one **yellow flipper plate** about 80 mm wide and 55 mm long on the slope. It is hinged along its top edge at the front of that deck and slopes down at about 36° to touch the floor. Its lower ~40 % is covered with **clear tape**. Two small **clear polycarbonate tabs**, screwed to its top corners, stick out sideways over the side panels and act as **rest stops**. At the two rear top corners, **black knurled printed cylinders** with **silver M3 socket cap screws** in their ends sit on a transverse axis. Nothing rotating or electrical is visible apart from the switch and the wheels.

---

## 2. Part-by-part description

### 2.1 Frame (FR)
- **Seen**: matt black print with fine 0.2 mm layer lines, a faint **diagonal hatching texture** on the deck top surface (top-skin infill lines at about 45°), and sharp edges. It is visible in the gaps between the lid, the flipper and the side panels in all three views.
- **Shape**: a rectangular tub. Outer plan **80 (X) × 57 (Y) mm**, y −42 … +15, height to the deck top **z ≈ 31**. The lid sits on its rear part. The flipper hinge is on its top front edge.
- **Front corners**: each front top corner has a **silver M3 socket cap screw** (S-FR) going in along X through the side panel into the frame. One is at aws70 (843, 435), just behind the flipper's upper corner, at about (x ±40, y +12, z 26). In aws73 the matching screw shows at (595, 815).
- **Front face (guess, M)**: under the flipper plate, the frame's front face is sloped parallel to the flipper or stepped, so the plate can rest close to it. A dark band between the flipper and the side panel in aws74 (450–530, 400–690) is the frame's front-lower face behind the flipper, visible on the slope.
- **Inside (guess, M)**: a floor 1.5–2 mm thick at z ≈ 3–5, two motor cradles at the rear, a servo bay at the front centre under the hinge, and a battery/electronics bay in the middle under the lid.

### 2.2 Exposed deck (DK), switch (SW), sticker (ST), countersunk screws (CS)
- **DK** is the top face of the frame between the lid's front edge (y ≈ +3) and the hinge line (y ≈ +15): a strip **≈ 76 × 12 mm** at z 31. A small **raised step** runs along its right half (aws73 crop: a rectangular plinth at about x +5 … +30 rising 2–3 mm, carrying the switch and a countersunk hole). It is also visible in aws70 as a small black rectangular **lug** (the switch slider) at (865–900, 285–320).
- **SW**: a **miniature slide switch**. Its black slider (≈ 4 × 3 × 3 mm) protrudes from a rectangular window **≈ 10 × 4 mm** cut in DK. It slides along X. The sticker says: arrow **left = OFF**, arrow **right = ON** (aws73: a red "ON" label with a white arrow pointing right-forward and a black "OFF" label with an arrow pointing left). In aws74 the lid's rear writing repeats this as "ON ↔ OFF".
- **ST**: a printed label **≈ 18 × 7 mm**, two halves (red/white ON, black/white OFF), stuck on DK just in front of the switch window, at about x −10 … +8, y +9.
- **CS-1, CS-2**: two **countersunk holes** with black (or recessed silver) screws, Ø 6 mm head recess, at about (x −14, y +8) and (x +12, y +11). They probably hold DK to the hinge block or the servo mount inside (M).

### 2.3 Lid (LD) and lid screws (S-LD)
- **Material**: yellow sheet, about **1.6 mm** thick. In aws73 a **crack** runs diagonally across its front-left corner. Near a screw at the front-left the edge is torn into a small notch (crop: the triangular flap at (280–320, 480–540)). A **flake lifts at the crack**, suggesting a laminated or layered material: either FR4/G10 (delaminating glass laminate) or a printed sheet splitting along layers. **Best guess: yellow G10/FR4 1.5–1.6 mm (M).**
- **Plan**: **≈ 64 (X) × 45 (Y) mm**, x −32 … +32, y −42 … +3. It is inset about 8 mm from each side panel, so the frame's top rail shows on both sides. Square corners.
- **Writing**: "FLIK" in purple/black marker, letters ≈ 10 mm tall, read from the left side in aws73 (written along Y) and upside down/sideways in aws74. "ON ↔ OFF" with double arrows near the rear edge (aws74 top: "ON", "↔", "OFF" stacked along the right-rear corner).
- **S-LD**: silver M2.5/M3 **button-head** screws, head Ø 5. Visible at aws70 (535, 120) and (745, 240), and aws73 (415, 130), (548, 270) and one more hidden near the rear. Assume **4**, at about (±27, −37) and (±27, −2).

### 2.4 Side panels (SP-L, SP-R), also the wheel guards
- **Material**: the same yellow sheet as the lid, **≈ 1.6 mm**. The edges show **white chipped spots** (aws70 (830, 490); aws74 along the bottom-left edge (290–420, 430–520) with greenish/dark scuffs). These are typical of FR4/G10 or impact-damaged PC with paint (M).
- **Outline (in the YZ plane)**: a pentagon or hexagon. Vertices (y, z): rear-bottom (−43, 3) → rear-top (−43, 32) → front-top (+13, 32) → front-bottom slant down to (+47, 3), following the flipper slope a few mm behind it → back along the bottom to (−43, 3). The rear-bottom corner may be chamfered about 6 × 6 mm (aws70 (1080–1130, 450–520)).
- **Position**: x = ±41.6 (outer faces), standing 2–3 mm off the floor.
- **Fasteners S-SP**: two visible per side. aws70 left: (958, 505) at the middle, about (y −10, z 18), and (745, 617) lower front, about (y +18, z 10). aws74 right: (350, 520) and (300, 340). The front corner S-FR also passes through the panel. Plus 1–2 more at the rear (hidden). **Assume 4 per side.**
- **Wheel guard role**: the wheels sit fully inboard of these panels. Only the tyre's bottom stands below the panel's lower edge (the panel bottom is z ≈ 3; the tyre reaches z 0).

### 2.5 Flipper plate (FP)
- **Material/finish**: yellow sheet, about **2 mm** thick. The upper part has a glossy, **dimpled "hammered" texture**. This is the pattern a textured PEI print bed leaves, so FP is probably a **printed PETG plate (M)**, though it could also be G10 with a textured film. Two screw heads S-FP have **concentric ripple rings** around them (aws70 (325, 315) and (520, 455)). These are local warping from counterbore heat, or from overtightening a thin printed plate.
- **Plan (in the plate)**: rectangle **≈ 80 (along X) × 55 mm (along the slope)**, square corners. In aws70 the upper-right corner has a slight brown burn/scuff (825, 370).
- **Tape TP-FP**: the lower **≈ 22 mm** (40 %) of the slope, full width, is covered with **clear packing tape**. It reads as a frosted, crazed band with a sharp boundary line (aws70 from (65, 395)/(545, 815) up to the line (80, 260)–(640, 600); aws74 the band (430–1100, 250–690)). The tape is wrapped around the leading edge.
- **Pose**: hinge at (y +15, z 32). Slope β₀ ≈ 36°. The leading edge is on the floor at y ≈ +15 + 55·cos 36° = **+59.5**. Hmm: that overruns the 101.6 box with the rear at −42. See §13.1 for the reconciliation (**plate 52, β₀ 38°, edge at y +56**).
- **S-FP**: 2 silver button heads on the plate's centreline zone, at about 25 mm and 40 mm from the hinge and x −15 / +5 (they are not symmetrical). They likely fix the plate to a **printed hinge arm** underneath that carries the servo linkage (M).

### 2.6 Stop tabs (TB-L, TB-R)
- **Seen**: clear polycarbonate strips about **1 mm thick, 12 mm wide, 28 mm long**, with a **rounded outer end** (r 6) and some scratches. Each one is screwed (S-TB, a silver button head) to the top of the flipper at its upper corner. It runs outward and rearward past the plate edge, over the side panel's top edge.
  - aws73: one tab at (220–340, 40–110) at the plate's far upper corner, and the other (with a blue protective film) at (570–700, 400–530), lying over the left side panel's top edge (in that view the side panel at the image right is the robot's left).TB-R at (570–700, 400–530), lying over the right... (in that view the side panel at the image right is the robot's left; the tab with a blue film is at the plate's left corner).
  - aws74: the right tab at (140–350, 330–400) lies over SP-R's upper-front edge, with a lettered protective film ("+ ¼") partly peeled.
- **Function (guess, H)**: **rest stops**. They land on the side panel top edges when the plate drops, so the flipper rests at a fixed slope with the leading edge just touching the floor, and the servo isn't loaded at rest. They also stop the plate from being driven down below the floor line when an opponent lands on it.

### 2.7 Hinge (HG)
- **Not directly visible**. It is under the plate's upper edge along y +15, z ≈ 31.
- **Guess (M)**: a **printed knuckle hinge** along the frame's top front edge with an M3 pin (or 3 mm rod) along X, ≈ 76 mm long. The flipper plate is screwed through S-FP to a **printed hinge leaf/arm** that wraps the pin. The servo horn pushes on this leaf.
- **Alternative (L)**: the plate is driven directly by the servo output shaft placed at the hinge line (the servo lies along X with its spline on the hinge axis, with an idler pin on the other side). This is common in small ant flippers and would explain the absence of external linkage.

### 2.8 Rear corner bosses (RB) and their screws (RS)
- **Seen**: at **each rear top corner**, a **pair of black printed cylinders** sits end-to-end along X. Each is about **Ø 11 mm × 9 mm long**, with **fine axial knurling** (about 24 ridges) on the circumference. A **silver M3 socket cap screw** head (Ø 5.5) sits in the outer end, flush or 1 mm proud.
  - aws70: the left-rear pair at (790–1020, 90–260), the screw face at (1000, 230) facing the robot's left (+image right).
  - aws73: both pairs, at the top left (540–625, 45–125) and the right (660–760, 160–265).
  - aws74: the right-rear one at (195–260, 120–200), the screw facing image-left = the robot's right.
- **Position**: axis at about (y −40, z 31). The cylinders span x ±(21 … 41), so **two per side, about 20 mm of each corner**. The lid's rear edge sits between the inner ends.
- **Function (guess)**:
  - (a) **Hinge for the lid** (the lid's rear edge clamps between the bosses, which pivot on the M3 screws so the lid can swing up for access) (M).
  - (b) **Clamp nuts** for the side panels (knurled for finger tightening) (M).
  - (c) **Self-righting / anti-wedge rollers**: when the robot is on its back or tipped back after its own flip, it rolls on these instead of digging in (L).
  The knurl suggests they are meant to be turned by hand, so (b) is the most likely answer, or (a)+(b): a knurled nut on each end of a long rear through-bolt that pins both side panels and the lid. **Chosen: a rear through-bolt M3 × 90 with 4 knurled printed cylinders as spacer-nuts (M).**

### 2.9 Wheels (WH-L, WH-R)
- **Seen**: the left wheel through the gap between the frame and SP-L, in aws70 crop (600–770, 590–690) and aws73 (720–810, 315–380): a **black rubber or foam tyre**, rounded edges, matt.
- **Size**: **Ø ≈ 28 mm, width ≈ 12 mm**. Centre at about (x ±33, y −24, z 14).
- **Hub**: not visible (guess: a printed hub on a 3 mm D-shaft).
- **Invertibility**: the tyre top at z 28 is below the lid (z 32.6) and the side panel top (32), so the robot **cannot drive inverted**. It must self-right with the flipper (H).

### 2.10 Drive (DM) and electronics (hidden)
- **DM (guess, M)**: two **N20 gearmotors** (or 12 mm "1000 rpm" micro gearmotors) mounted along X at y −24, z 14, gearboxes outboard into the wheel hubs.
- **SV (guess, M)**: a 9–12 g metal-gear micro servo (e.g. MG90S class, 23 × 12 × 29 mm) under DK at the front centre, output toward the hinge.
- **RX/ESC/BAT (guess, M)**: under the lid. A 2S 180–300 mAh LiPo across the middle, a dual brushed ESC, and a receiver. The servo is powered from the RX's BEC.
- **GR (aws74, top right)**: a **green tab** (≈ 5 × 8 mm) peeking out at the flipper's far top corner. It is probably a green-tinted version of the stop tab on that side, or green tape on TB-L (M).

### 2.11 Clear skirt (SK), aws73 only
- A **large clear flexible sheet** (PET/acetate, ≈ 0.25 mm) about **90 × 70 mm** sits under the flipper and ahead of it. Its front edge lies flat on the towel well ahead of the plate (aws73 (20–470, 300–760)). It is taped to the plate's underside or lower edge.
- **Purpose**: a temporary zero-height **skirt to win the under-game** against other wedges. In the cut-out photos it is absent, or trimmed to just the tape band.

---

## 3. Per-view sections (for silhouette matching)

### 3.1 aws70 (front-left iso, el. 35°)
- The **flipper parallelogram** dominates the left half: corners (310, 45), (830, 370), (545, 815), (65, 395), with the frosted tape band on its lower 40 %.
- **Lid**: a lit yellow quadrilateral (460, 110) / (650, 55) / (940, 215) / (720, 285). Its front edge has screws at (535, 120) and (745, 240).
- The **black deck** strip with the switch lug and two countersunk holes at (790–1000, 250–360).
- **SP-L**: a yellow band from (575, 790) up to (1160, 320), two screws visible.
- **Rear-left bosses** at the top right, (790–1020, 90–260).
- The **wheel** shows inside the panel at about (1000, 330).

### 3.2 aws73 (front-left, high)
- The lid with "FLIK", the crack and the notch. The deck with the **switch and the red/black sticker** fully visible. Both stop tabs. The left wheel. Both rear boss pairs. The clear skirt is huge at the left/bottom.

### 3.3 aws74 (front-right iso, el. 35°)
- The flipper spans (300–1100, 60–690) with its tape band. The lid writing "FLIK" and "ON ↔ OFF".
- **SP-R** at the left (60–530, 215–700), chipped. TB-R sticks out at (140–350, 330–400). One right-rear boss at (195–260, 120–200).
- The **green tab** at (915–945, 115–150).

### 3.4 Top view (synthesised)
- An 83 × 98 rectangle overall: the side panels ±41.6, from y −43 to the flipper edge at +56.
- From rear to front: the boss pairs at the rear corners; the lid (64 × 45, inset 8 mm each side); the deck strip (12 mm) with the switch at the right-centre; then the flipper plate (80 wide × 41 in plan). The stop tabs reach out to x ±46.

### 3.5 Front view
- The flipper is a wide low ramp, 80 wide, rising from the floor to z 32. The side panels stand just outside it. The tabs are at its top corners, sticking out sideways by about 5 mm. The bosses peek above the rear at the corners (z up to 36.5).

### 3.6 Side view (left)
- The panel pentagon: the slanted front edge parallel to the plate, which overhangs it by about 3 mm. The flipper's top-edge hinge is at (y +15, z 32). The boss at the rear-top corner. The tyre bottom shows below the panel's lower edge at y −24.

### 3.7 Rear view (not photographed, inferred)
- The black frame's rear face, 80 × 30 (guess: a charge port hole), flanked by the panel edges. The four knurled bosses on top. The wheels are hidden behind the panels.

---

## 4. Part table

| ID | Shape | Size (mm) | Centre / location | Material |
|---|---|---|---|---|
| FR | tub | 80 × 57 × 28 (z 3–31) | (0, −13.5, 17) | black PLA/PETG |
| DK | top strip | 76 × 12 | y +3 … +15, z 31 | black |
| SW | slide switch | slider 4 × 3 × 3, window 10 × 4 | (+14, +9, 31) | black |
| ST | label | 18 × 7 | (−1, +9, 31) | red/black |
| CS-1/2 | csk screws | head Ø 6 | (−14, +8), (+12, +11) | black/steel |
| LD | plate | 64 × 45 × 1.6 | (0, −19.5, 31.8) | yellow G10 |
| S-LD ×4 | button M2.5 | Ø 5 × 1.5 | (±27, −37), (±27, −2) | steel |
| SP-L/R | pentagon plate | 90 × 29 × 1.6 | x ±40.8 | yellow G10 |
| S-SP ×4/side | button M3 | Ø 5.7 | per §2.4 | steel |
| S-FR ×2 | socket cap M3 | Ø 5.5 | (±41.6, +12, 26) | steel |
| FP | plate | 80 × 52 × 2 | hinge (y 15, z 32), β 38° | yellow PETG (M) |
| TP-FP | tape | 80 × 22 | lower plate | clear |
| S-FP ×2 | button M3 | Ø 5.7 | plate stations 25 and 40 | steel |
| TB-L/R | tab | 28 × 12 × 1, r 6 end | the plate's upper corners | clear PC |
| HG | knuckle hinge + pin | Ø 3 × 76 | (0, +15, 31) | printed + steel |
| RB ×4 | knurled cylinders | Ø 11 × 9 | x ±25.5, ±36.5; y −40, z 31 | black PLA |
| RS ×2 | M3 socket cap | Ø 5.5 | ends at x ±41 | steel |
| WH-L/R | wheels | Ø 28 × 12 | (±33, −24, 14) | black rubber |
| DM-L/R | N20 | 12 × 10 × 24 | along X, y −24, z 14 | (guess) |
| SV | servo | 23 × 12 × 29 | (0, +4, 16) | (guess) |
| BAT | LiPo | 40 × 20 × 8 | (0, −15, 24) | (guess) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WH bottom ↔ floor | drive contact | 0 |
| FP leading edge (tape) ↔ floor | skid contact at rest | 0 |
| FR floor ↔ floor | clearance | 3 |
| SP bottom edge ↔ floor | clearance | 3 |
| SP inner face ↔ FR side | screwed | 0 |
| WH outer face ↔ SP inner face | running gap | 1.5 |
| WH inner face ↔ FR side wall | via the wheel well (FR side is cut away at the wheel) | 2 |
| LD ↔ FR top rim | screwed | 0 |
| LD side edge ↔ SP inner face | inset | 8 |
| LD front edge ↔ HG line | deck exposed | 12 |
| LD rear edge ↔ RB inner ends | adjacent | 1 |
| RB ↔ RS / rear bolt | threaded/clamped | 0 |
| RB outer end ↔ SP outer face | flush | 0 |
| FP upper edge ↔ DK front edge | hinge clearance | 1 |
| FP underside ↔ FR front face | rest gap | 2–4 |
| TB ↔ FP | screwed | 0 |
| TB underside ↔ SP top edge | resting (stop) | 0 |
| FP side edge ↔ SP inner face | the plate (80) sits between the panels | 0.8 per side |
| SP slanted edge ↔ FP underside | below the plate | 3 |
| SW slider ↔ DK window | sliding | 0.3 |
| SK (aws73) ↔ FP underside | taped | 0 |

---

## 6. Mechanism

- **Drive**: two-wheel differential, wheels at the rear third (y −24). The robot's front weight rests on the flipper's leading edge (a sliding contact). This is a classic "wedge on the floor" setup: the plate's tip skids, and the wheels push.
- **Flipper**: the plate rotates about the hinge at (y +15, z 31.5). The leading-edge point P(θ) = (y 15 + L·cos(β₀ − θ), z 31.5 − L·sin(β₀ − θ)), with L = 52 and β₀ = 38°. At θ = 38° the plate is horizontal: P = (67, 31.5). At θ = 90°: P = (y 15 + 52·cos(−52°) = 47, z 31.5 + 41 = 72.5). Servo travel of about 90–120° gives a quick flick of 40–70 mm tip lift. Speed and force are limited by the servo (a "flick", not a launch).
- **Self-righting**: when inverted, the robot lies on the lid, bosses and panel tops. Firing the plate pushes it against the floor, levering the robot about the rear bosses (here the knurled cylinders act as a roll axis) (M).

---

## 7. Assembly order (suggested rebuild)

1. Print the frame FR (black), including the motor cradles, the servo bay, the hinge knuckles at the top front and the switch window.
2. Install the drive motors and the wheels. Install the slide switch, RX, ESC and battery. Wire everything.
3. Install the servo at the front centre and fit the horn/arm.
4. Pin the flipper hinge leaf to the frame (M3 rod). Screw FP to the leaf with the 2 S-FP screws. Add the stop tabs TB with S-TB.
5. Bolt the side panels SP-L/R with 4 screws each, plus the front corner socket screws S-FR.
6. Fit the rear through-bolt with the four knurled cylinders RB.
7. Screw on the lid LD (4 screws). Write "FLIK" and the switch legend.
8. Apply the clear tape band to the flipper's lower part (and the optional clear skirt SK).

---

## 8. Hidden / uncertain list

- Hinge construction, servo position and linkage.
- The exact function of the knurled rear bosses.
- The wheel/motor type and the axle position (only the tyre is seen).
- The underside and rear face: never photographed.
- Plate materials (printed PETG vs G10).

---

## 9. Coordinate frame (restated)

+X right, +Y forward, +Z up. O on the floor at mid-width, with the frame spanning y −42 … +15. Hinge axis: the line (y +15, z 31.5) ∥ X. Rest β₀ = 38°, plate length 52, leading edge at y +56.

---

## 10. Profiles as math

**10.1 Flipper (in world, rest).** The plate's upper surface: the plane through the hinge line, z = 31.5 − tan 38°·(y − 15) = 31.5 − 0.781·(y − 15) for y ∈ [15, 56], x ∈ [−40, 40]. Thickness 2 mm below this plane. Tape band region: y ∈ [43, 56].

**10.2 Side panel outline (YZ).** Polygon: (−43, 3), (−43, 32), (+13, 32), (+47, 5.4) [the line z = 32 − 0.781·(y − 13), offset 3 mm below the plate], (+47, 3), back to (−43, 3). Optional rear-bottom chamfer: replace (−43, 3) with (−43, 9) → (−37, 3).

**10.3 Stop tab (in the plate's plane).** A rectangle 12 × 22 plus a semicircle r 6 at the outer end: the stadium-like outline u ∈ [0, 22], |v| ≤ 6, plus (u − 22)² + v² ≤ 36. Its axis runs at about 30° to the plate's upper edge, outward and rearward.

**10.4 Knurled boss.** A cylinder r 5.5, length 9, about the axis (y −40, z 31). Knurl: r(φ) = 5.5 − 0.4·|sin(12φ)|. Counterbore Ø 5.8 × 3 at the outer end for the socket cap.

**10.5 Wheel.** A torus-capped cylinder: r 14, width 12, edge fillet 3.

**10.6 Lid.** A rectangle [−32, 32] × [−42, 3] at z 31 … 32.6. The crack (aws73) is approximately the line from (−32, −8) to (−5, +3) (cosmetic).

---

## 11. Pixel-based measurements (independent check)

**aws70** (1200 × 884): flipper upper edge 613 px; flipper side edge 528 px (slant, partly foreshortened); lid front edge 308 px, lid side 331 px; the screw head S-LD ≈ 22 px; the knurled boss Ø ≈ 55 px; SP-L top length ≈ 420 px.
**aws74** (1200 × 858): flipper upper edge 607 px, lower edge 724 px; side edges 463 and 413 px; lid width visible ≈ 420 px; screw heads ≈ 20 px; boss Ø ≈ 60 px.
**aws73** (866 × 784): lid ≈ 300 × 260 px; the switch window ≈ 45 × 20 px; sticker ≈ 90 × 35 px; screw head ≈ 22 px; wheel Ø ≈ 120 px.

---

## 12. Several independent estimates of key quantities

| Quantity | Method A (rules/parts) | Method B (screw-head scale, Ø 5.7) | Method C (ratios) | Reconciled |
|---|---|---|---|---|
| Flipper width | ≤ frame width 80 | aws70: 613/22 × 5.7 = 159?? (the screw is farther than the near edge; perspective) → aws74: 607/20 × 5.7 = 173 (same issue) → unusable | lid/flipper width ratio in aws74 ≈ 0.75 → 64/0.8 = 80 | **80** |
| Flipper slant length | box: 101.6 − 57 (frame) = 44 plan → 44/cos 38° = 56 | — | width/length ratio from aws74 ≈ 1.45 → 55 | **52–55** |
| Lid width | 80 − 2 × 8 inset | 308/22 × 5.7 = 80 (near-field) → ×0.8 = 64 | — | **64** |
| Lid depth | frame 57 − 12 deck | 331/22 × 5.7 × 0.55 (foreshortened) ≈ 47 | lid ≈ 0.7 W | **45** |
| Knurled boss Ø | M3 head 5.5 + 2 × 2.5 wall = 10.5 | 55/22 × 5.7 = 14 (nearer) → 11 | — | **11** |
| Wheel Ø | must fit under 32 with 3 mm to spare → ≤ 29 | aws73: 120/22 × 5.7 = 31 | — | **28** |
| Height | lid at 32 | — | side panel ratio height/length ≈ 0.33 → 30 | **32** |
| Mass | 2 × N20 (20) + servo (13) + BAT 2S 180 (12) + RX/ESC (8) + wheels (8) + frame (35) + G10 plates (lid 7, panels 2 × 10, flipper 12) + screws (8) ≈ 143 g | — | — | **≤ 150** OK |

---

## 13. Consistency check: conflicts and reconciliation

1. **Box length.** The frame (57) + the flipper reach (55·cos 36° = 44.5) = 101.5 is right at the limit. Using 52 mm at 38° gives 41 → **98 total**, plus the bosses (which sit at y −40, inside). **Reconciled: L = 52, β₀ = 38°.** The side panels at −43 are 1 mm behind the frame.
2. **Plate width vs side panels.** In aws70/74 the plate looks nearly as wide as the outside of the panels. If the plate were wider than 83 it would hit the panels when lifting (unless it is above them). The stop tabs rest **on** the panel tops, so the plate's edge must be **inside** the panels at the hinge. **Reconciled: plate 80 (between panels, 0.8 mm gap each side)**, and the tabs reach over.
3. **Lid inset.** The lid is visibly narrower than the frame (the frame rail shows on both sides), consistent with 64 vs 80.
4. **Material of the plates.** The flipper's dimpled texture (textured PEI) vs the panels' smooth, chipped finish (G10) suggests **mixed materials**: a printed flipper and G10 panels and lid. The cracked, flaking lid fits G10 delamination. **Reconciled: FP printed PETG 2 mm; LD and SP G10 1.6 mm (M).**
5. **Wheel visibility.** The wheel is seen only through the gap, near the rear. The side panels hide the rest. Consistent with Ø 28 at z 14 behind a 29 mm panel.
6. **Knurled bosses as nuts.** Four cylinders with screws only on the outer ends implies a through-bolt (or two short screws into the inner cylinders). Both fit. Function uncertain (§2.8).

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Full-width hinged wedge plate (FP)**: The plate wins the ground game against other wedges and spinners (a long low ramp). Because it is also the weapon, any opponent that drives up the ramp is already on the flipper. The **top hinge** means the whole wedge lifts, so the opponent's contact point never slides off a smaller flipper tip.
- **Clear tape band**: it covers the leading edge so the plate's printed edge isn't chewed. It gives a thin, low, slick lip, and it is renewable between fights.
- **Clear skirt (aws73)**: a temporary lower lip for a specific opponent (to beat a lower wedge). Cheap, removable.
- **Stop tabs (TB)**: they fix the rest angle mechanically, so the plate can't be pushed through the floor or overload the servo when rammed. Clear PC because it flexes rather than cracks.
- **Side panels as wheel guards**: they protect the wheels from horizontal spinners and from being grabbed. They also make the robot a sealed box with no snag points. G10 is stiff and light, and the screws make the panels replaceable.
- **Inset lid**: a smaller lid saves weight and leaves the frame rails as the structural top. A lid that is not flush with the panels avoids catching on the flipper.
- **Exposed deck with the switch**: the switch must be reachable with the flipper down (AWS rules require easy power-off). Placing it in front of the lid, under the flipper's upper edge, protects it from top hits. The sticker makes the ON direction unambiguous for arena marshals.
- **Knurled rear bosses**: tool-less nuts for quick panel changes, and/or rollers so the robot doesn't stick on its back. They also stiffen the rear corners against side hits.
- **Wheels inboard**: no wheel overhang to be hit. The trade-off is that the robot cannot drive inverted, so the flipper must self-right.
- **Writing "FLIK" and "ON ↔ OFF" on the lid**: for event identification and for marshals to switch it off.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Confidence |
|---|---|---|
| Servo | MG90S-class metal-gear servo at the front centre, horn driving the hinge leaf | M |
| Hinge | printed knuckles + M3 rod across the full width at the top front | M |
| Hinge leaf | printed 2–3 mm arm under the plate, fixed by S-FP | M |
| Drive motors | 2 × N20 (≈ 300–500 rpm at 2S), along X, rear | M |
| Wheels | Ø 28 foam/rubber on printed hubs | M |
| Battery | 2S 180–300 mAh LiPo across the middle under the lid | M |
| ESC/RX | dual brushed ESC + 4-ch receiver | M |
| Rear bolt | M3 × 90 through the bosses, frame and panels | L–M |
| Front face of the frame | sloped 38° behind the plate | M |
| Floor | printed, with holes for the motor clamp screws | M |
| Green item | a green-tinted stop tab or tape on the left hinge end | L |

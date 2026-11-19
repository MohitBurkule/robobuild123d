# Flippant: full rebuild description from reference photos

Source photos (all one Team Termite robot over three events; colours change):
- `robots/flippant/reference/flippant.aws69.webp` (1200 × 1057 px): AWS 69, cut out onto white. **The primary build target** (the only photo listed in `REFERENCE.json`). **Front-right three-quarter**, camera at about 35° elevation and 45° azimuth (json: user pick az 45, el 35). Body: **translucent natural/milky PETG**. **Green** treaded wheels at the two rear corners. A **flat front panel** carries a "FLIPPANT" label and a **blue tape strip**. A **white printed hoop flipper** sits across the middle of the top, with a **steel rod**. A **yellow smiley sticker** is on the rear lid, and a **switch window** shows a black slide switch and red electronics.
- `robots/flippant/reference/flippant.aws68.webp` (487 × 377 px): AWS 68 pit photo. **Almost straight front, about 30–45° elevation.** Body: **white** with a **dark grey/black front panel** carrying a big square "TEAM TERMITE" smiley sticker, a **black cylinder** across the top behind the panel with a "FLIPPANT" label, white hoops over it, **orange** wheels at the rear corners, and a translucent front lip with a clear tape skirt on the table.
- `robots/flippant/reference/flippant.aws65.webp` (294 × 228 px): AWS 65, small and blurred. **Front-right, ≈ 45° elevation.** White body, a white front panel with a "TEAM TERMITE" smiley sticker, a "FLIPPANT" label on the right side wall, **black hoops**, **teal/blue** wheels, and a **black-and-grey grip strip** (rough tape) along the front lip.

Pixel coordinates refer to the jpg copies at these sizes, read by eye, ±10 px (±3 px for the small images).

Facts are read from the photos. Inferences are marked **(guess)** with confidence **H/M/L**. Dimensions are estimates, scaled from the AWS antweight limits (150 g, 101.6 mm cube), the M2 screw heads (black button heads, Ø ≈ 3.8 mm) and the wheel (Ø ≈ 26 mm, typical for this low build). Ratios are given against **W = body width ≈ 92 mm**.

Robot class: `REFERENCE.json` says **flipper**, 2 wheels, axis x. What the photos actually show is a **low, wide wedge box** whose front slope is a **fixed screwed panel**, with a **rotating hoop flipper** on a transverse shaft at the top of that slope. The hoops are C-shaped printed arms. At rest they arch up and back over the robot. Firing rotates the shaft so the hoops sweep forward and down over the wedge face, flicking what is on it. Rotated the other way, they push against the floor for self-righting. See §6 and §13.3 for why I read it this way and the alternative (a hinged front panel).

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the front lip with the blue tape), **+Z** = up.
- **Origin O** = the floor point under the centre of the body plan (mid-width; mid-length between the rear wall face y −40 and the front lip edge y +46). The body is not symmetric fore-aft about O: the wedge face is forward, and the lid and wheels are rearward.
- **Hoop angle ψ**: the rotation of the flipper shaft about X. ψ = 0 is the rest pose of aws69 (hoops arching up and rearward). Positive ψ swings the hoops **forward** (over the wedge).
- In aws69 the robot's **right** side is the long face at the image bottom-left, the rear edge runs along the image top-left, and the front lip runs along the image bottom-right.

| ID | Part |
|---|---|
| BD | main body tub (translucent PETG in aws69) |
| SW-L / SW-R | side walls (thick, with the chamfered front-top corner) |
| RR | rear rail / rear wall top (ribbed by layer lines) |
| WW-L / WW-R | rear-corner wheel wells (notches in the top/rear) |
| LD | rear lid (translucent, with the smiley sticker STK-1) |
| WN | switch window in the lid |
| PS | power slide switch (black), seen through WN |
| FP | front wedge panel (fixed, screwed; label LB-1 "FLIPPANT") |
| BT | blue tape strip along the front panel's lower edge |
| LP | front lip: the printed wedge edge strip below/ahead of FP |
| TS | clear tape skirt on the lip |
| HB | hoop bar: white printed beam on the shaft, along X |
| SH | steel shaft (the visible silver rod), along X |
| HP-1 … HP-4 | hoops: HP-1 left end band, HP-2 inner left crescent, HP-3 inner right spike (seen edge-on), HP-4 right end band |
| BK-L / BK-R | shaft bearing blocks (end supports, translucent) |
| S-FP | black M2 button screws around FP (≈ 10) |
| S-LD | silver M2 screws on the lid and side walls |
| WH-L / WH-R | green TPU lugged wheels |
| DM-L / DM-R | drive motors (hidden, guess N20) |
| SV | flipper servo (hidden, guess) |
| ESC, RX, BAT | electronics (red PCB and red wires visible through WN) |
| STK-1, STK-2 | stickers: the smiley (lid, aws69) and TEAM TERMITE (front panel, aws65/68) |

---

## 1. Overall description in one paragraph

Flippant is a **flat, wide, two-wheeled wedge** about **92 mm wide, 86 mm long and 24 mm tall** (to the top of the body). The front half is a **broad panel sloping down** to a long **printed lip** with a **clear tape skirt**. A **blue tape strip** runs along the panel's lower edge. About **ten black M2 screws** hold the panel on around its perimeter, and a white "FLIPPANT" label sits on it at an angle. The rear half is a **flat lid** with a yellow **smiley sticker**. A rectangular **window** in the lid shows a black **slide switch**, red wires and a red ESC board. Two **green lugged wheels** (Ø ≈ 26 × 10 mm) sit in **notches at the two rear corners** and stick out slightly beyond the rear and the sides. Across the top, where the lid meets the sloped panel, is the weapon. A **steel rod** lies along X between two end supports. A **white printed bar** runs beside it, and four **white C-shaped hoops** rise from the bar and arch up and back over the lid. The two end hoops are wide bands, and the two inner ones are slimmer crescents and a fin. They make the robot's highest points (z ≈ 45). The walls are thick translucent PETG with prominent horizontal layer lines. The side walls carry a chamfer at the front-top corner that follows the panel slope.

---

## 2. Part-by-part description

### 2.1 Body tub (BD), side walls (SW-L/R), rear rail (RR)
- **Material**: aws69: **translucent natural PETG**, milky, with strong horizontal **layer lines** (0.2–0.3 mm) visible on the side wall and rear rail as fine ribbing. It is thick-walled (light passes through as a pale green-white glow). aws68/aws65: opaque white.
- **Plan**: **92 (X) × 86 (Y) mm**, y −40 … +46 including the lip. The rear part (lid area) is y −40 … +2. The slope is y +2 … +40, and the lip is y +40 … +46.
- **Side walls**: **≈ 5 mm thick** (x ±41 … ±46). Height **24 mm** from z 1 to z 25 over y −40 … +5. Then the top edge **drops along a straight chamfer** following the front panel slope from (y +5, z 25) to (y +42, z 4), and a short vertical front end reaches the lip. In aws69 the right wall shows as the long translucent face (70–560, 520–1000) with a **silver M2 screw** near its top front at (355, 685) and the slope chamfer at (330–650, 640–900).
- **Rear rail RR**: the top of the rear wall, **≈ 8 mm deep (Y)**, ribbed, spanning between the wheel wells (x −32 … +32), at z 25. In aws69 it runs along the image top-left (130–480, 80–440). In aws65 the rear is not visible.
- **Floor (guess, M)**: 1.5 mm at z 1–2.5; ground clearance ≈ 1 mm.

### 2.2 Wheel wells (WW-L/R) and wheels (WH-L/R)
- **Wells**: at each rear corner, a **rectangular notch** cut through the top and the rear and side walls, about **14 (X) × 30 (Y) mm**, so the wheel shows from above, from the rear and from the side. In aws69 the rear-left wheel is at (480–640, 60–185) and the rear-right at (85–315, 440–600).
- **Wheels**: **translucent green TPU** (aws69), orange (aws68), teal/blue (aws65). **Ø ≈ 26 mm, width ≈ 10 mm.** The tread has **about 20 square lugs** (≈ 3 mm wide, 1.5 mm deep), like a coarse gear. The inner hub is not visible. The top of the tyre is at z ≈ 26, about **1 mm above the lid** (so the robot can drive inverted on the wheels, just barely), and the tyre stands ~2 mm proud of the side wall.
- **Position**: centre (x ±40, y −25, z 13).
- **Wheel guards**: none apart from the wells. The wall material around the well acts as a partial guard on the front and inner sides.

### 2.3 Rear lid (LD), sticker (STK-1), switch window (WN), switch (PS)
- **LD**: a translucent plate, **≈ 64 (X) × 40 (Y) × 2 mm**, at z 23–25, flush with the side walls between the wheel wells. In aws69 it has small silver screws near its corners (one is visible at (365, 295)). The smiley sticker sits on its left-rear part.
- **STK-1**: a round **yellow smiley** sticker, **Ø ≈ 22 mm**, with its top edge torn or folded (showing grey/silver), at about (x −5, y −20). In aws69 it is at (440–615, 160–330).
- **WN**: a **rectangular window ≈ 22 × 14 mm** in the lid's right-front zone (aws69 (310–520, 370–560), near the hoop bar). Its edges are stepped (2 levels), suggesting a **recessed switch plate**. Through it: the **black slide switch PS** (body ≈ 8 × 4, slider ≈ 3 × 2 × 3 mm, sliding along Y), a small **gold/brass bead** (a solder joint or screw), **red wires** and a **red PCB**.
- **Electronics glimpsed**: red silicone wires (≈ 22–24 AWG) and a red-solder-mask board, most likely a **dual brushed ESC** (e.g. a red "DasMikro"/"Pololu-style" board) (M).

### 2.4 Front panel (FP) and its screws (S-FP)
- **Shape**: a **flat rectangular plate**, **≈ 82 (X) × 42 mm along the slope**, ≈ 2 mm thick. It spans x ±41 between the side walls, from the hoop zone (y +2, z 24) down to the lip (y +40, z 4): a slope of **≈ 28°**.
- **Material/colour**: aws69 milky translucent (the same PETG). aws68 **dark grey/black** (a different panel, perhaps carbon/G10 or black PLA). aws65 white.
- **Fasteners**: **black M2 button screws** (head Ø 3.8) about **8–10 mm apart along the side edges** and the upper edge. aws69 visible: (735, 215), (840, 230), (880, 290), (935, 330) along the right/upper edge, (770, 550) mid, and (487, 663), (545, 733), (605, 790) along the left lower edge. Total **≈ 10–12 screws**. The dense pattern suggests the panel is a **fixed armour face**, not a moving flipper (H).
- **LB-1**: a **white label ≈ 46 × 14 mm** reading "FLIPPANT" in black capitals, stuck **diagonally** across the panel's centre (the long axis about 60° to X). In aws69 it is at (600–760, 380–800), partly hidden by the hoops. aws68 has it on the black cylinder instead, and aws65 on the side wall.
- **STK-2**: aws68/65: a square **"TEAM TERMITE" smiley sticker ≈ 30 × 30 mm** in the panel centre.

### 2.5 Blue tape strip (BT), lip (LP), skirt (TS)
- **BT**: **blue painter's/PVC tape ≈ 8 mm wide**, along the full length of the panel's lower edge (aws69 (650–1020, 380–870)). It probably covers the panel-to-lip seam and stops the lip's printed edge from delaminating (M).
- **LP**: the long **printed wedge lip**: a strip **≈ 92 (X) × 8 (Y)**, a triangular section falling from z 4 to z 0.5, with very visible horizontal **layer ribs**. It is the leading edge of the whole robot (aws69 (1000–1140, 410–1010)).
- **TS**: **clear tape** (or a thin PET sheet) laid over the lip and extending **≈ 6–8 mm** ahead onto the floor (aws69 (1060–1140, 450–1010)). In aws68 the skirt is obvious on the table.
- aws65: instead of BT/TS, the lip carries a **black-and-grey rough grip strip** (sandpaper or gaffer tape) along it.

### 2.6 Hoop flipper (HB, SH, HP-1…4, BK)
- **SH**: a **silver steel rod Ø ≈ 3 mm**, along X, about **80 mm long** (x −40 … +40). It is visible through the gaps under the hoops (aws69 crop: from (480, 640) up to (700, 200) in image). It lies at about **y +4, z 22**, just behind and below the bar HB.
- **HB**: a **white (opaque, PLA/PETG) printed beam ≈ 72 (X) × 7 (Y) × 7 (Z) mm**, its rectangular section rotated about 20° so one face is parallel to the panel slope. It runs parallel to SH and joins the hoop roots. In aws68 the equivalent is a **black cylinder Ø ≈ 12 mm** spanning the width, with the label on it.
- **HP-1 (left end band)**: a wide arch, band **≈ 10 mm wide (X) × 3 mm thick**, about a semicircle of **outer radius ≈ 13 mm**. It rises from HB at x ≈ −32, arches up to z ≈ 40 and comes back down toward the lid at y ≈ −22, where its free end hangs 2–3 mm above the lid. aws69 (430–700, 400–650).
- **HP-2 (inner left crescent)**: a slimmer **crescent** (band 6 mm wide, tapering to a 3 mm tip) of **radius ≈ 14 mm**, at x ≈ −10, rising up and back to z ≈ 42. aws69 (560–860, 250–420).
- **HP-3 (inner right spike/fin)**: seen almost **edge-on**, as a curved **horn** rising to the highest point **z ≈ 46** at x ≈ +8, with a forked/“Y” look where it overlaps HP-2. aws69 (600–700, 120–330).
- **HP-4 (right end band)**: like HP-1 but **wider (≈ 14 mm band)**, at x ≈ +32, arching up and back with its free end over the rear-left wheel well area. aws69 (740–980, 110–250).
- All the hoops are **white, smooth, opaque**, with no visible screws. They are probably printed in one piece with HB (H).
- **BK-L / BK-R (guess, M)**: translucent printed blocks at each end of SH, inside the side walls at x ±38 … ±41, holding the rod. In aws69 a translucent block shows at the right end under HP-4 (720–790, 170–250) and at the left end under HP-1 (330–420, 640–720).
- **aws65**: the hoops are **black** and look thicker. aws68: the hoops are **white** but rise **straighter** (more like inverted-U handles seen from the front, top at about the same height as the wheel tops + 20 mm).

### 2.7 Screws, other
- **S-LD**: silver M2 pan heads on the lid corners and on the side wall top-front (aws69 (365, 295), (355, 685)).
- **S-FP**: black M2 button heads (§2.4).
- Wheels: no visible screws (pressed on, guess).

### 2.8 Hidden: drive, servo, battery, receiver
- **DM (guess, M)**: two **N20 gearmotors** along X at the rear (y −25, z 13), gearboxes outboard into the wheels. Inside, the space between them (x −28 … +28) is available for the battery.
- **SV (guess, M)**: a **micro servo** (e.g. 9 g) mounted under the hinge zone with its output shaft **co-axial with SH** at one end, or driving SH through a horn and link from under the lid. The bar HB is fixed to the servo horn on one side and pivots on SH at the other.
- **BAT (guess, M)**: 2S 180–300 mAh LiPo under the lid.
- **RX (guess)**: under the lid, next to the red ESC.

---

## 3. Per-view sections (for silhouette matching)

### 3.1 aws69 (front-right iso)
- A **wide flat parallelogram body**: the rear edge runs from (70, 450) to (520, 55), the right wall from (70, 520) to (560, 1000), the front lip from (560, 1000) to (1140, 410), and the right end of the rear rail at (980, 270).
- **Green wheels** at the two rear corners. **Hoops** rise from a line through (430, 650)–(980, 230) and arch toward the top-left.
- The **front panel** (with the blue strip, label and black screws) fills the bottom-right half. The **lid** with the smiley and switch window fills the upper-left quarter.
- Highest silhouette points: the tops of HP-3 and HP-4.

### 3.2 aws68 (front view)
- Front: a translucent lip with a clear skirt on the table. A **black panel** rising back at ≈ 28°, with the TEAM TERMITE sticker (square, about 1/3 of the width) and 6 screws at its corners and edges.
- Behind it: a **black cylinder** across almost the full width (100–370, 85–160 px) with the white "FLIPPANT" label. White hoops arching over it: one wide hoop left of centre (100–185, 95–165), one tall slim fin at the centre (195–240, 15–130), one at the right (310–350, 40–90).
- **Orange wheels** at the far corners (25–60, 40–100) and (285–330, 35–60), at about the same height as the cylinder.
- White side walls with chamfered fronts. Overall the width is about 1.4× the visible height including the hoops.

### 3.3 aws65 (front-right, high)
- A white body, white panel with the smiley sticker, **black hoops**, teal wheels at the rear corners, a "FLIPPANT" label on the right side wall's sloped part, and a **black grip strip** on the lip. The proportions match aws69.

### 3.4 Top view (synthesised)
- A 92 × 86 rectangle. Wheel notches at the rear corners (x ±32 … ±46, y −40 … −10), with the wheels showing.
- The lid from y −40 to +2, with the smiley at the left-centre and the window at the right-front.
- The shaft and hoop bar at y +2 … +8. The hoops overhang rearward to y −22.
- The panel from y +8 to +40, with the blue strip at y +37 … +40 and the lip to +46, skirt to +53.

### 3.5 Front view
- Lip line at z 0–4; the panel rising to z 24 at the hinge zone; the hoops above it to z 46. Side walls at x ±41 … ±46. Wheels peek out at the rear corners above the wall line by about 1 mm.

### 3.6 Side view (right)
- A flat profile 24 tall from y −40 to +5, then a 28° slope to the lip at y +46. The wheel circle (Ø 26) at the rear corner, centred at y −25. Hoop arcs above the slope's top, curling back over the lid.

### 3.7 Rear view (not photographed, inferred)
- The rear wall 64 wide × 24 tall between two wheel notches; possibly a charge-port hole (L). The hoops' free ends are visible above.

---

## 4. Part table

| ID | Shape | Size (mm) | Position | Material |
|---|---|---|---|---|
| BD | tub | 92 × 86 × 24 | centre (0, +3, 12.5) | translucent PETG |
| SW-L/R | wall | 5 × 86 × 24 with slope chamfer | x ±43.5 | PETG |
| RR | rail | 64 × 8 × 3 | (0, −36, 23.5) | PETG |
| WW | notch | 14 × 30 | rear corners | — |
| WH-L/R | lugged wheel | Ø 26 × 10, 20 lugs | (±40, −25, 13) | green TPU |
| LD | plate | 64 × 40 × 2 | (0, −19, 24) | PETG |
| WN | window | 22 × 14 | (+14, −4, 25) | — |
| PS | slide switch | 8 × 4 × 5 | under WN | black |
| STK-1 | round sticker | Ø 22 | (−5, −20, 25) | yellow |
| FP | plate | 82 × 42 × 2 | slope y +2 … +40, 28° | PETG (black in aws68) |
| S-FP ×10–12 | M2 button | Ø 3.8 | around FP | black steel |
| LB-1 | label | 46 × 14 | the FP centre, diagonal | white |
| BT | tape | 82 × 8 | FP lower edge | blue |
| LP | lip | 92 × 8 × 4 → 0.5 | y +40 … +46 | PETG |
| TS | tape | 92 × 8 | y +44 … +53 | clear |
| SH | rod | Ø 3 × 80 | (y +4, z 22) | steel |
| HB | beam | 72 × 7 × 7 | (0, +6, 25) | white PLA |
| HP-1 | band arch | 10 wide, R 13 | x −32 | white |
| HP-2 | crescent | 6 wide, R 14 | x −10 | white |
| HP-3 | fin/horn | 4 wide, R 16 | x +8 | white |
| HP-4 | band arch | 14 wide, R 13 | x +32 | white |
| BK-L/R | blocks | 6 × 10 × 10 | x ±39, y +4, z 20 | PETG |
| DM-L/R | N20 | 12 × 10 × 24 | (±22, −25, 13) | (guess) |
| SV | servo | 23 × 12 × 22 | (−18, −5, 13) | (guess) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WH ↔ floor | drive contact | 0 |
| LP/TS ↔ floor | skid contact | 0 |
| BD floor ↔ floor | clearance | 1 |
| WH top ↔ LD top plane | the wheel stands proud | +1 |
| WH outer face ↔ SW outer plane | proud | 2 |
| WH tyre ↔ WW walls | running clearance | 1.5 |
| LD ↔ BD rim | screwed | 0 |
| FP ↔ BD (walls and front rail) | screwed (10–12) | 0 |
| FP side edges ↔ SW inner faces | butt | 0.3 |
| BT ↔ FP/LP seam | taped | 0 |
| LP ↔ BD | integral (H) | 0 |
| TS ↔ LP | taped | 0 |
| SH ↔ BK bores | rotating | 0.1–0.2 |
| HB ↔ SH | fixed or concentric sleeve | 0 |
| HB underside ↔ FP top | rest clearance | 1–2 |
| HP free ends ↔ LD | rest clearance | 2–3 |
| HP-1 / HP-4 outer faces ↔ SW inner faces | inboard | 3–5 |
| HP sweep (ψ 0 → +150°) ↔ FP surface | clears, tips skim | 1–3 |
| PS slider ↔ WN | recessed below the lid | −2 |
| STK-1 ↔ LD | stuck | 0 |

---

## 6. Mechanism

- **Drive**: two-wheel differential, wheels at the rear corners. The front lip is the third contact (a skid). The centre of mass is near y −10 (the battery and motors are at the rear), so the lip is lightly loaded and the wedge stays low.
- **Weapon (the chosen interpretation, M)**: the servo rotates HB and the hoops about SH (axis X, at y +4, z 22).
  - **Attack**: ψ from 0 to about +150°. The hoops swing forward over the top and sweep down onto the wedge panel. An opponent that has driven up the panel is hooked from behind and above and **flipped/flicked** forward and over, or just knocked off balance. Hoop tip radius ≈ 16 mm about the shaft. The swept volume is a half-cylinder of R 16 along X × 72 mm above the panel's upper part.
  - **Self-righting**: when the robot is inverted it rests on the hoop tops (they are the highest points). Rotating the hoops (ψ negative) pushes against the floor and levers the robot upright over its rear edge (M).
  - Rest (ψ = 0): the hoops arch rearward over the lid, protecting the switch window from top hits and acting as **roll bars**.
- **Alternative (L)**: the front panel FP is a rear-hinged flipper about SH, and the hoops are fixed roll bars on its hinge bar. Against: the panel carries ≈ 12 screws into the side walls (a fixed panel) and its edges butt against the walls.

---

## 7. Assembly order (suggested rebuild)

1. Print BD (the tub with the side walls, rear rail, wheel wells, lip and switch-plate recess) in translucent PETG, base down.
2. Install the N20 motors into the rear cradles and press on the green TPU wheels.
3. Install the ESC (red board), receiver, battery and slide switch (switch under WN).
4. Install the servo near the left hinge block, then pass SH through BK-R, HB (with the hoops) and the servo horn adaptor into BK-L.
5. Screw FP onto the walls and front rail with 10–12 black M2 screws. Stick the "FLIPPANT" label on.
6. Screw on LD (silver M2), with the smiley sticker.
7. Tape the blue strip along the panel's bottom edge. Add the clear tape skirt over the lip.

---

## 8. Hidden / uncertain list

- Servo position and coupling to HB/SH.
- Whether HB is fixed to SH or rotates on it.
- The exact hoop count and shapes (HP-2/HP-3 overlap in projection).
- The underside, the rear wall and the left side: never seen in detail.
- The battery/ESC layout.

---

## 9. Coordinate frame (restated)

+X right, +Y forward, +Z up. O on the floor at the body plan centre; the body spans y −40 … +46, x ±46. Shaft axis: (y +4, z 22) ∥ X. Panel plane: z = 24 − tan 28°·(y − 2) for y ∈ [2, 40].

---

## 10. Profiles as math

**10.1 Side wall profile (YZ).** Polygon (y, z): (−40, 1) → (−40, 25) → (+5, 25) → (+42, 5.3) [chamfer line z = 25 − 0.532·(y − 5)] → (+42, 1) → close. Minus the wheel notch [−40, −10] × [3, 25] for |x| > 32.

**10.2 Panel FP.** The plane z = 24 − 0.532·(y − 2), y ∈ [2, 40], |x| ≤ 41, 2 mm thick below. Screw holes Ø 2.2 at a 9 mm pitch along x = ±38 and along the line y = 5.

**10.3 Lip LP.** A triangle section (y, z): (40, 4) → (46, 0.5) → (40, 0.5), extruded |x| ≤ 46.

**10.4 Hoops (in the YZ plane, relative to the shaft centre C = (y 4, z 22)).** HP-n centreline: a circular arc of radius R_n about the centre C_n = C + (−R_n, +3), from the angle 0° (the root, at the bar, pointing forward-up) to 180° (the tip, pointing down toward the lid). R = 13 (HP-1, HP-4), 14 (HP-2), 16 (HP-3). Band cross-section: w_n × 3 mm, with w = 10, 6, 4, 14. The tips taper linearly to 60 % width over the last 30°.

**10.5 Hoop rotation.** A point P on a hoop maps to P(ψ) = C + R_X(ψ)·(P − C), with R_X(ψ) the rotation about X. Forward attack is positive ψ.

**10.6 Wheel.** r(φ) = 11.5 + 1.5·[cos(20φ) > 0] (square lugs, 20 around), width 10, about the axis (y −25, z 13).

---

## 11. Pixel-based measurements (independent check)

**aws69** (1200 × 1057):
- Rear-right wheel: ≈ 225 px wide (oblique) × 160 px. Rear-left wheel: ≈ 160 × 125 px (farther).
- Front lip length: (560, 1000) → (1140, 410) ≈ 830 px. Right side wall: (70, 520) → (560, 1000) ≈ 690 px. Rear rail: (70, 450) → (520, 55) ≈ 600 px.
- Black screw head ≈ 14–16 px. Smiley Ø ≈ 175 px.
- HP-4 width ≈ 70 px across the band; hoop heights above the bar line ≈ 130–180 px.

**aws68** (487 × 377): the overall robot width (wall to wall) ≈ 430 px; the visible front height to the hoop top ≈ 120 px; the sticker ≈ 150 × 140 px; the wheel ≈ 35 px wide.

**aws65** (294 × 228): body width ≈ 250 px; the sticker ≈ 65 px.

---

## 12. Several independent estimates of key quantities

| Quantity | Method A (rules/parts) | Method B (screw scale Ø 3.8) | Method C (ratios) | Reconciled |
|---|---|---|---|---|
| Body width | ≤ 101.6 with the wheels inset | aws69 lip 830/15 × 3.8 = 210 (near-field and oblique; ≈ ×0.45) → 95 | aws68: width/sticker = 430/150 × 30 = 86 | **92** |
| Body length | lid 42 + slope 38 + lip 6 | right wall 690/15 × 3.8 = 175 → ×0.5 (obliquity) = 87 | rear rail/lip length ratio 600/830 = 0.72 (rail between wheel notches) → 66 at width 92 → lid width 64 ✓ | **86** |
| Body height | low wedge, hoops must fit under 101.6 | — | aws68: height to the hoop tops ≈ 120/430 × 92 = 26 above the panel base → hoops ≈ 45 total | **24 body, 46 hoops** |
| Wheel Ø | N20 + small tyre 24–28 | 160/15 × 3.8 = 40 (nearest object, inflated) → 27 | aws68: 35/430 × 92 = 7.5 visible width ≈ tread width | **26** |
| Panel slope | from aws68 front, the panel occupies ≈ 60 % of the visible height | — | the side wall chamfer in aws69 ≈ 28–32° | **28°** |
| Smiley Ø | — | 175/15 × 3.8 = 44 (the sticker is nearer than the screws? no, at similar depth) → oblique 0.5 → 22 | — | **22** |
| Hoop radius | fits between the bar and the lid: ≤ 20 | 130/15 × 3.8 × 0.6 ≈ 20 | — | **13–16** |
| Mass | 2 × N20 (20), servo 9, LiPo 12, ESC/RX 8, wheels 6, tub (thick PETG) ≈ 60, panel 8, lid 6, hoops 8, rod 4, screws 5 ≈ 146 g | — | — | **≈ 145 g** |

---

## 13. Consistency check: conflicts and reconciliation

1. **Width vs the 4-inch box**: 92 body + 2 × 2 proud wheels = 96 ≤ 101.6. ✓ Length 86 + skirt 7 = 93 ✓. Height 46 ✓.
2. **Invertibility**: the wheels stand 1 mm above the lid but the hoops reach 46. Upside down the robot sits on the hoops, not on the wheels, so it **cannot drive inverted** and must self-right with the hoops (or by rotating the hoops flat). This supports the self-righting role (§6).
3. **Fixed panel vs hinged flipper**: the screw pattern (≥ 10 screws along both side edges and the top edge) means the panel is **fixed**. The only moving part must be the hoop assembly on SH. **Reconciled: rotating hoop flipper.** The json's `flipper` with axis x is consistent (the rotation axis is X).
4. **aws68 black cylinder vs aws69 white bar + steel rod**: the older version used a thick black tube (perhaps a carbon tube over the rod) as the hoop hub. The newer one used a printed bar beside a visible rod. Same axis, same function. **Model the aws69 version.**
5. **Hoop count**: aws68 shows 3 clear arches (wide, fin, right), and aws69 shows 4 shapes (wide left, crescent, fin, wide right). **Reconciled: 4 hoops, two wide end bands and two inner slim ones.**
6. **Switch window height**: the switch is seen below the lid level with stepped edges → a **recessed** switch, protected from top hits. ✓

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Very wide, low body with a long lip**: maximises the chance of getting under opponents (the ground game), and makes the robot hard to get under. A 92 mm lip is nearly the full allowed width.
- **Fixed screwed panel**: a strong, rigid wedge that survives spinners. Many small screws spread the load, and the panel is replaceable and swappable (black in aws68, translucent in aws69).
- **Rotating hoops instead of a flipper plate**: they need only a micro servo and a short lever, yet reach above and behind an opponent riding the wedge to **flick** it. At rest they double as **roll bars** and as a **self-righting lever**. The open C-shapes are light and springy (absorbing hits rather than transmitting them to the servo).
- **Hoops of different widths**: the wide end bands take side impacts and protect the bearing blocks. The slim inner ones save weight while still giving a central contact point.
- **Blue tape strip**: it covers the panel-lip joint so opponents' wedges can't catch on the seam, and it protects the printed edge.
- **Clear skirt / grip strip**: a zero-height leading edge (clear tape) or more traction for pushing (grip tape in aws65). These are tuned per event.
- **Rear-corner wheels in notches**: the wheels are protected on two faces but still touch the walls in a pushing match. Being slightly proud on top and at the rear lets the robot climb off walls and bump along when it is pushed backward.
- **Recessed switch window**: AWS requires accessible power isolation. The recess keeps the switch from being bumped off by hits.
- **Translucent PETG**: tough, slightly flexible, inexpensive. The translucent look shows the electronics (a team style).
- **Stickers and labels**: team identity (Team Termite) and the robot name for the judges.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Confidence |
|---|---|---|
| Servo | 9 g metal-gear servo, output along X at the left end of SH, horn screwed to HB | M |
| HB–SH relation | HB clamps SH; SH rotates in BK bores; the servo drives it from one end | M |
| Drive | 2 × N20 at the rear, along X | M |
| Battery | 2S 180–300 mAh under the lid, across the middle | M |
| ESC | red dual brushed ESC under the switch window | M |
| RX | small receiver beside the ESC | M |
| Floor | integral with the tub, 1.5 mm | H |
| BK blocks | integral with the side walls (bosses with Ø 3.1 holes) | M |
| Wheel hubs | TPU tyres moulded around a D-bore, or printed one-piece in TPU | M |
| Charge lead | through the switch window or under the lid | L |

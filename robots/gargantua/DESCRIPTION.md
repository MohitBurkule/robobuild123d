# Gargantua: full rebuild description from reference photos

Source photos:
- `robots/gargantua/reference/gargantua.aws67.webp` (1146 × 1200 px): AWS 67, cut out onto white. **The primary build target** (the only photo in `REFERENCE.json`). **Front view from high and slightly left** (json: az 105, el 35; in practice the camera is about 40–45° up and 10–15° to the robot's left of the nose). The **grey steel ring blade** fills the bottom half of the frame. The **black box chassis** with its rounded **nose lobe** is in the middle. **Teal** treaded wheels are at the top left and right (at the rear).
- `robots/gargantua/reference/gargantua.aws65.webp` (458 × 546 px): AWS 65 pit photo on a wooden table. **Near top view** (json: top), the camera nearly overhead with the robot's front pointing down the image. **Pink/red** wheels with black side blocks (wheel guards/brackets). Raised lettering **"Gargantua"** runs along the right half of the lid. Same ring, same nose lobe with five fasteners.
- `robots/gargantua/reference/gargantua.aws66.webp` (437 × 416 px): AWS 66 pit photo on yellow card. **Front-right three-quarter, ≈ 45° elevation.** Pink/red wheels with black hubs, the same chassis, and the ring with a visible tooth notch at the image bottom-left. Another robot labelled "Ankle" is at the top left.

Pixel coordinates refer to the jpg copies at these sizes, read by eye, ±10 px (±4 px on the small ones).

Facts are read from the photos. Guesses are marked **(guess)** with **H/M/L**. Dimensions are estimates scaled from the AWS 4-inch cube (the ring plus the chassis must fit 101.6 mm in length) and from the screw heads (M3 countersunk ≈ Ø 6 mm). Ratios are given against **B = chassis body width (without the wheels) ≈ 62 mm**.

Robot class: **horizontal ring spinner / "shell-less undercutter ring"** (`REFERENCE.json`: horizontal_spinner, ring, axis z). A **flat steel ring blade** with **three spokes** is bolted below an **inverted outrunner motor** housed in a semicircular **nose lobe** at the front of a two-wheel box. It spins about a **vertical axis just above the floor** in front of (and partly under) the chassis. The ring's outer rim carries **one tooth** (a radial step).

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the nose lobe and the ring's front), **+Z** = up.
- **Origin O** = the floor point under the **weapon axis** (the centre of the nose lobe and the ring). This puts the ring centred on O, the chassis box mostly at negative Y, and the wheels at the rear.
- Ring angle **φ** is measured about +Z from +Y (counter-clockwise seen from above). The tooth position in each photo is given as φ.
- The weapon spin direction is unknown. A single-tooth ring is normally spun so the tooth's step face leads (guess); see §2.7.

| ID | Part |
|---|---|
| CH | black printed chassis box |
| NL | nose lobe: the semicircular front extension that houses the weapon motor |
| SH-L / SH-R | front shoulders of the box on either side of the lobe |
| HT | raised rectangular hatch on the top (battery/electronics cover) |
| S-HT | hatch screws (black, 3–4) |
| SWR | oval recess with the slide power switch (SW) |
| TX | raised "Gargantua" lettering on the top (aws65) |
| WM | weapon brushless outrunner (hidden, inside NL, inverted) |
| WMS | weapon motor fasteners: 4 black countersunk screws on the lobe top |
| AX | weapon axle top: a silver button/socket screw with a washer at the lobe centre |
| RG | steel ring blade (rim RG-R, three spokes RG-S1…3, hub RG-H, tooth RG-T) |
| RGS | ring-to-bell screws (hidden under the hub, guess) |
| WH-L / WH-R | drive wheels (teal in aws67, pink/red in aws65/66), grooved tread |
| HB-L / HB-R | black wheel hubs |
| WG-L / WG-R | black wheel-guard / outboard support blocks in front of each wheel |
| DM-L / DM-R | drive gearmotors (hidden, guess N20) |
| ESC-W, ESC-D, RX, BAT | electronics (hidden, guess) |
| S-CH | small black screws at the chassis top corners |

---

## 1. Overall description in one paragraph

Gargantua is a **compact black printed box** with a **semicircular nose lobe** at the front centre and two **grooved TPU wheels** at the rear corners. Under the lobe, an **inverted brushless outrunner** spins a **large flat steel ring** (Ø ≈ 88 mm, 8–9 mm wide rim, ≈ 3 mm thick) just above the floor. The ring is joined to a small central hub by **three straight spokes**: one points back under the chassis, and two angle forward-left and forward-right at ±60° from the nose, so the visible part looks like a "peace sign" or Mercedes star. The rim has **one tooth**, a radial step of ≈ 4 mm where the outer edge spirals out and then drops back. The box is about **62 mm wide, 60 mm long and 24 mm tall**, with fine diagonal top-skin texture. It carries a **raised rectangular hatch** (≈ 26 × 36 mm) held with small black screws, an **oval recess** with a **slide switch** in front of the hatch, and (in aws65) raised **"Gargantua"** lettering. The lobe top shows **four black countersunk screws** around a **silver centre screw**: the motor mount and the axle retainer. The wheels (Ø ≈ 32 × 13 mm) stick out beyond the box sides and slightly above its top. **Black blocks** in front of each wheel act as small wheel guards and/or outboard motor supports.

---

## 2. Part-by-part description

### 2.1 Chassis box (CH)
- **Material**: black PLA/PETG. The top has **diagonal hatch infill texture** at about 45° (a top-skin print pattern), and the walls have horizontal layer lines. The aws65 surface looks rougher and more matt (perhaps a textured "fuzzy skin" print or simply a lower-resolution photo).
- **Plan**: **≈ 62 (X) × 58 (Y) mm**, y −66 … −8, with the corners rounded to r ≈ 4. The front face at y −8 is split by the lobe into two **shoulders** SH-L / SH-R (x ±13 … ±31). Their front corners are rounded r ≈ 5, and a vertical **concave fillet** (r ≈ 6) blends into the lobe (aws67 (300–350, 520–600) and (640–690, 570–620)).
- **Height**: the top is at **z ≈ 26**. The bottom (guess, M) is at z ≈ 8, so the box is **≈ 18 mm tall**, sitting **above the ring plane** (the ring at z 3–6) with ≈ 2 mm clearance. Box walls ≈ 2 mm.
- **Top corner screws S-CH**: small black screws (M2) at the top corners, e.g. aws67 (800, 118) and (795, 575), aws65 (155, 35) and (290, 35). They fix the top plate to the tub, or the body halves together.
- **TX (aws65 only)**: raised letters **"Gargantua"** (≈ 6 mm tall, ≈ 50 mm long), reading along −Y on the right half of the top (x ≈ +18), lettering height ≈ 0.6 mm.

### 2.2 Hatch (HT) and screws (S-HT)
- **Shape**: a raised flat **rectangle ≈ 26 (X) × 36 (Y) × 3 mm**, with crisp edges and a slight bevel. It sits on the top's centreline toward the rear, y −64 … −28. Its own top skin is printed with a different (finer) hatch direction, which shows it is a separate part.
- **Fasteners**: a black M2 screw at each rear corner (aws67 (545, 70) and (800, 120)) and **one at the front centre** (aws67 (575, 330), in a small round boss in front of the hatch). So it is a **3-screw hatch** (M).
- **Purpose**: the battery/receiver access cover.

### 2.3 Switch recess (SWR) and switch (SW)
- **SWR**: an **oval/lozenge-shaped pocket ≈ 18 × 8 mm**, ≈ 3 mm deep, in front of the hatch at (x 0, y −22). In aws67 (510–665, 355–415) it has a raised rim on its right end.
- **SW**: a black **miniature slide switch** in the pocket, slider ≈ 3 × 2 mm, moving along X. aws65 shows a **white/grey mark** (paint or a label) next to it, probably an "ON" marking.

### 2.4 Nose lobe (NL) and weapon motor mount (WMS, AX)
- **Shape**: a **semicircular extension** of the box, **outer radius ≈ 20 mm** about the weapon axis (x 0, y 0). It is joined to the box front by the concave fillets. Same top height (z 26) as the box. Its sides are vertical down to **z ≈ 7**, just above the ring hub.
- **Top features** (aws67 (380–620, 460–600), aws65 (165–270, 255–335)):
  - **AX**: a **silver M3 button/socket screw** with a **washer Ø 8** at the centre. It sits in a **bearing recess Ø ≈ 12** (a polished steel ring, likely the outer race of a flanged bearing, MR63/683ZZ). This is the axle top, which keeps the weapon shaft or the motor's stator bolt captive.
  - **WMS**: **four black M3 countersunk screws** on a **Ø ≈ 22 mm** bolt circle at 90° spacing (in aws67 rotated about 15° from the axes). They are the motor's stator-mount screws (a 22xx/28xx outrunner commonly has a 16/19 mm bolt pattern; with countersunk printed heads, Ø 22 measured on the outer head edges ≈ Ø 16–19 hole circle).
- **WM (hidden, guess H)**: an **inverted brushless outrunner**, e.g. a **2205/2207 or 2806** class motor, **Ø ≈ 28 × 20 mm**. The stator is screwed to the underside of the lobe roof. The rotating bell faces down and the ring hub is bolted to the bell's bottom face. The lobe interior is a cylindrical pocket Ø 30 × 18.

### 2.5 Ring blade (RG)
- **Material**: **grey steel** (laser-cut, matt, slight blue-grey; the edges look sharp and slightly dark from the laser oxide). Thickness **≈ 3 mm** (aws67 the cut edge at the near rim shows as a thin bright band). In aws66 it looks like painted or anodised grey (it could be **titanium**) (M).
- **Rim RG-R**: an annulus of **outer Ø ≈ 88 mm** (r_o = 44) and **inner Ø ≈ 70 mm** (r_i = 35), so a **9 mm** wide band. aws67: the rim spans from x 45 to 985 across the image and runs down to the image bottom (1070).
- **Spokes RG-S1…3**: **three straight bars ≈ 7 mm wide**, radial, from the hub to the rim at **120° spacing**. S1 points to **−Y** (φ = 180°, straight back under the chassis; hidden). S2 and S3 are at **φ = 60° and φ = 300°**, i.e. **forward-left and forward-right**, forming the visible "V" in front of the lobe. In aws67 the two visible spokes run from the lobe at (350, 740) to the rim at (170, 885), and from (560, 760) to (850, 870). The spokes meet the rim with small fillets (r ≈ 3) and make the three **sector-shaped cut-outs** (circular-segment "triangles") seen in all photos.
- **Hub RG-H**: a disc **Ø ≈ 22** at the centre (hidden under the lobe). It has a centre hole for the shaft and **3–4 bolt holes** to the motor bell (guess, M).
- **Tooth RG-T**: **one** tooth. The outer edge **steps radially by ≈ 4 mm** at a single place: the rim radius increases slowly around the circle (or is constant), then a sharp **radial step face** drops back. In aws67 it is at the bottom right (720–830, 960–1075): the rim's outer edge has a notch where the step face shows, with a small inward **relief notch** cut into the rim behind it. In aws65 it is at the right-front (400–445, 415–450). In aws66 it is at the left-front (180–215, 355–390). **φ in aws67 ≈ 330° (front-right, slightly right of the nose).**
- **Plane**: the ring is **horizontal**, its bottom at **z ≈ 3**, top at z ≈ 6, i.e. just above the arena floor (a low undercutter).

### 2.6 Wheels (WH), hubs (HB), wheel guards (WG)
- **Tyres**: **teal** (aws67) or **pink-red** (aws65/66) TPU, **Ø ≈ 32 mm**, **width ≈ 13 mm**. The tread is **≈ 40 deep axial grooves** (like a coarse spur gear: 1.5 mm deep, 1 mm wide slots), with chamfered edges.
- **Hubs**: black printed, recessed into the tyre, with **3–4 round holes / spokes** (aws66: the left wheel's hub shows 3 openings).
- **Position**: centre (x ±40, y −46, z 16). The tyre inner face is 2 mm from the box side (x ±31 → ±33), so the outer face is at x ±46.5. The **wheel top (z 32)** is above the box top (26) by 6 mm, so the robot can **drive inverted** (with the ring then on top).
- **WG-L / WG-R**: black printed blocks **≈ 8 (X) × 10 (Y) × 14 (Z) mm** on the **front side of each wheel**, extending outboard to about x ±47, low down (z 2–16). In aws65 they are clearly visible as black "brackets" hugging the front of each wheel (15–45, 140–235) and (380–410, 130–235). In aws67 the right one is at (890–930, 440–530). **Function**: a front wheel guard (stops opponents and the ring's own deflected debris from hitting the tyre), and/or an outboard bearing bracket for the axle (M).
- **Rear**: the rear of the wheels is open (no guard). The wheels overhang the box rear by ≈ 4 mm.

### 2.7 Hidden: drive, electronics
- **DM (guess, H)**: 2 × **N20** micro gearmotors along X at y −46, z 16, in cradles under the hatch, gearboxes outboard.
- **ESC-W (guess, M)**: a small brushless ESC (10–20 A, BLHeli) in the lobe-adjacent front space between the shoulders.
- **ESC-D / RX (guess, M)**: a dual brushed ESC + receiver, possibly a combined board.
- **BAT (guess, M)**: a 2S/3S 300 mAh LiPo under the hatch (≈ 40 × 18 × 10).
- **Spin direction**: unknown. With the tooth step at the trailing end of the spiral, the tooth face leads in the rotation direction. **Guess: clockwise seen from above (L).**

---

## 3. Per-view sections (for silhouette matching)

### 3.1 aws67 (front, high)
- **Ring**: a big ellipse spanning (45–985, 470–1075). The near (front) part of the rim is at the bottom with the tooth at the bottom right. The far (rear) part is hidden under the box. The left part of the rim arcs up to (60, 600) and the right part up to (985, 640).
- Visible spokes: the left spoke from the lobe base down-left, the right spoke down-right. The three openings read as a left sector (165–380, 590–880), a bottom sector (220–830, 760–1000) and a right sector (590–900, 590–870).
- **Box** from (185, 50) to (970, 700): the top plane is lit, with the hatch at (460–785, 65–345) and the switch recess below it. The **lobe** protrudes at the bottom centre (320–660, 470–760) with its 5 fasteners.
- **Wheels**: teal at the top left (200–355, 40–340) and the right (930–1055, 185–480).

### 3.2 aws65 (top view)
- The box is a near-rectangle (65–365, 20–335). The lobe semicircle (150–320, 250–390). The ring (15–445, 230–520) with spokes to the lower-left and right and the tooth at the right.
- Pink wheels at the rear corners (15–65, 20–235) and (370–415, 20–235), with the black guard blocks.
- The "Gargantua" lettering along the right of the top.

### 3.3 aws66 (front-right)
- The box with the hatch, switch recess and lobe. The ring visible in front and to the right, with the tooth at the left-front. Pink wheels at the left (front-left in the image) and the top (rear-right).

### 3.4 Top view (synthesised)
- Ring circle r 44 at O. The lobe semicircle r 20 at O (rear half merged with the box). The box from y −8 to −66, x ±31. The wheels at x ±(33 … 46.5), y −62 … −30. The hatch on the centreline, y −64 … −28. The switch at y −22. The tooth at φ ≈ 330° (as in aws67).
- Overall, as first measured: **X 93 (wheels) × Y ≈ 110**. §13.1 reconciles this to ≤ 102 by shortening the box.

### 3.5 Front view
- A low wide ring line at z 3–6 spanning x ±44. Above it, the lobe front (a semicircle seen as a 40-wide rounded face, z 7–26). The box shoulders behind, out to x ±31. The wheels at the sides to x ±46.5, tops at z 32. The front guard blocks WG are in front of the wheels.

### 3.6 Side view (right)
- The ring line from y −44 to +44 at z 3–6. The box (y −66 … −8, z 8–26) sits above the ring's rear half. The lobe nose reaches y +20. The wheel circle Ø 32 at y −46. The wheel bottom (z 0) is below the ring (z 3).

### 3.7 Rear view (not photographed, inferred)
- A flat box rear 62 × 18 with rounded corners. The wheel backs are exposed. The ring rim shows under the box (at the rear, the ring's r 44 reaches y −44, which is inside the box footprint, so it is hidden from behind except at the sides).

---

## 4. Part table

| ID | Shape | Size (mm) | Position | Material |
|---|---|---|---|---|
| CH | rounded box | 62 × 58 × 18 | x ±31, y −66 … −8, z 8–26 | black PLA |
| NL | half-cylinder | r 20, z 7–26 | centre (0, 0) | black PLA |
| HT | raised plate | 26 × 36 × 3 | (0, −46, 27.5) | black PLA |
| S-HT ×3 | M2 | head Ø 3.8 | (±11, −62), (0, −25) | black |
| SWR | oval pocket | 18 × 8 × 3 | (0, −22, 26) | — |
| SW | slide switch | 8 × 4 | in SWR | black |
| AX | M3 button + washer + bearing | Ø 8 washer | (0, 0, 26) | steel |
| WMS ×4 | M3 countersunk | Ø 6 | bolt circle Ø 19, 90° | black |
| WM | outrunner | Ø 28 × 20 | (0, 0, 9–25), bell down | (guess) |
| RG-R | annulus | r 35 … 44, t 3 | z 3–6 | steel |
| RG-S ×3 | bars | 7 wide | φ 60°, 180°, 300° | steel |
| RG-H | disc | Ø 22 | centre | steel |
| RG-T | step | 4 radial | φ ≈ 330° (aws67) | steel |
| WH-L/R | grooved wheels | Ø 32 × 13 | (±40, −46, 16) | teal/pink TPU |
| HB | hubs | Ø 18 | in WH | black PLA |
| WG-L/R | blocks | 8 × 10 × 14 | (±43, −27, 9) | black PLA |
| S-CH ×4 | M2 | Ø 3.8 | box top corners | black |
| TX | raised text | 50 × 6 × 0.6 | (+18, −40, 26) | black (aws65) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WH ↔ floor | drive contact | 0 |
| RG bottom ↔ floor | running clearance | 3 |
| CH bottom ↔ RG top | clearance under the box | 2 |
| NL bottom ↔ RG hub top | clearance (the bell spins between them) | 1 |
| RG-H ↔ WM bell | bolted | 0 |
| WM stator ↔ NL roof | screwed (WMS) | 0 |
| AX ↔ NL roof bearing | retained | 0 |
| RG-R outer ↔ WH tyre | the ring passes inboard of and under the tyre fronts, with no overlap in the occupied volume | ≥ 2 (see §13.2) |
| RG-R ↔ WG blocks | the guard is above/beside the ring | z clearance 1–2 |
| WH inner face ↔ CH side | running clearance | 2 |
| WG ↔ CH side | integral / screwed | 0 |
| HT ↔ CH top | screwed | 0 |
| SW ↔ SWR | sunk | −1 (below the top) |
| CH shoulders ↔ NL | integral, concave fillets r 6 | 0 |
| Ground contacts (static) | 2 wheels + a front skid? | the robot tips forward onto the lobe/ring when stopped (guess: a small skid under the lobe, see §15) |

---

## 6. Mechanism

- **Weapon**: an outrunner direct drive. The ring's moment of inertia, with ρ = 7.85 g/cm³ and t = 3 mm: rim mass = ρ·t·π·(r_o² − r_i²) = 7.85e-3·3·π·(44² − 35²) = **52.5 g**?? This is too heavy for a 150 g ant. See §13.3 → **the ring is probably titanium or thinner steel (2 mm)**: Ti 3 mm → 30 g; steel 2 mm → 35 g. Spokes and hub add ≈ 6–8 g.
  - With the rim at 30 g, I ≈ m·(r_o² + r_i²)/2 = 0.030·(0.044² + 0.035²)/2 = **4.7e-5 kg·m²**. At 15,000 rpm (1571 rad/s): E = ½·I·ω² ≈ **58 J**. A big weapon for an ant, hence the name **Gargantua**.
- **Drive**: two wheels at the rear. The ring sits ahead of them, close to the floor. When the robot stops, its weight rests on the wheels and (guess) a skid under the lobe or the hub (the ring itself must not touch). Gyroscopic effects are mild about Z (the ring's axis is vertical: turning does not tilt the robot; this is a classic reason to choose a horizontal ring).

---

## 7. Assembly order (suggested rebuild)

1. Print the chassis (box + lobe, black) bottom-up. Include the cradles for the N20s, the lobe's motor pocket and the bearing seat.
2. Mount the weapon motor upside down in the lobe with 4 countersunk M3 screws through the roof. Fit the axle bearing and AX screw/washer.
3. Bolt the ring hub to the motor bell from below (3–4 M3 screws).
4. Insert the drive motors, then press on the wheels. Attach the guard blocks WG (if separate).
5. Fit the ESCs, RX and battery. Wire the switch into the SWR recess.
6. Screw on the hatch (3 × M2) and the top-corner screws.

---

## 8. Hidden / uncertain list

- The underside: skids, ground clearance, the ring-to-bell joint.
- The rear spoke (S1) and the hub shape.
- The ring material and thickness (steel vs Ti; see §13.3).
- The wheel-guard block function.
- The rear of the robot.

---

## 9. Coordinate frame (restated)

+X right, +Y forward, +Z up. O = the floor under the weapon axis. Box y −66 … −8; lobe r 20 about O; ring r 44 about O at z 3–6; wheels at (±40, −46, 16).

---

## 10. Profiles as math

**10.1 Ring outline (polar about O, in its plane z ∈ [3, 6]).** Outer: r_o(φ') = 42 + 4·(φ'/360°), where φ' = (φ − φ_T) mod 360° and φ_T is the tooth angle. This gives a **one-tooth spiral** that rises from 42 to 46 around the circle with a radial step of 4 mm at φ_T (the mean r_o is 44). Inner: r_i = 35. Relief notch behind the step: a semicircle r 2 centred at (r 35, φ_T + 6°) cut from the inner edge.

**10.2 Spokes.** Bars with centrelines at φ_k = 60°, 180°, 300°, width 7, from r 11 to r 35, with fillets r 3 at both ends.

**10.3 Hub.** A disc r 11, centre hole Ø 5, 4 holes Ø 3.2 at r 8.

**10.4 Box plan.** A rounded rectangle x ∈ [−31, 31], y ∈ [−66, −8], corner r 4. Lobe: the circle r 20 about (0, 0) united with the box, and concave fillets r 6 where it meets the shoulder line y = −8 at x = ±20.

**10.5 Wheel.** r(φ) = 16 − 1.5·[frac(40φ/2π) < 0.25] (40 grooves, 25 % duty), width 13, chamfer 1.

---

## 11. Pixel-based measurements (independent check)

**aws67** (1146 × 1200): ring width 940 px; box front width (shoulder to shoulder) ≈ 675 px; lobe Ø ≈ 340 px; hatch ≈ 325 × 280 px; countersunk head ≈ 40 px; washer ≈ 45 px; teal wheel height ≈ 300 px (left, farther) and 300 px (right).
**aws65** (458 × 546): body 300 × 315 px; ring Ø ≈ 430 px; lobe Ø ≈ 170 px; wheel height ≈ 215 px (side view of the tread) × 40 px wide; hatch 115 × 135 px; the hub-to-rear distance ≈ 280 px.
**aws66** (437 × 416): box ≈ 260 px wide; ring ≈ 310 px.

---

## 12. Several independent estimates of key quantities

| Quantity | Method A (rule/parts) | Method B (screw head Ø 6) | Method C (ratios) | Reconciled |
|---|---|---|---|---|
| Body width B | 101.6 track limit − 2 × 15 wheel/gap → ≤ 70 | aws67: 675/40 × 6 = 101 (near-field; the lobe screws are at the front) → ×0.65 ≈ 66 | aws65: body/ring = 300/430 → 0.70 × 88 = 61 | **62** |
| Ring Ø | the box rule: ring r + (hub to rear) ≤ 101.6 | aws67: 940/40 × 6 = 141 (nearest object, the ring front near the camera; ×0.62) ≈ 88 | aws65: 430/300 × 62 = 89 | **88** |
| Lobe radius | must hold a 28 mm motor + 2 mm wall → ≥ 16 | aws67: 340/40 × 6 / 2 = 25 → ×0.8 ≈ 20 | aws65: 170/300 × 62/2 = 17.5 | **20** |
| Hub to rear | 101.6 − 44 = 57.6 | — | aws65: 280/430 × 88 = 57 | **57–66** (see §13.1) |
| Wheel Ø | N20 standard 30–34 | — | aws65: 215/300 × 62 = 44?? (the tread seen along Y in a slightly tilted view includes the side) → aws67: 300/675 × 62 = 28 (farther) | **32** |
| Box height | the outrunner Ø 28 × 20 + roof 2 + clearance → top at 26 | — | aws67: the shoulder face ≈ 130 px tall vs the 675 px width → 12 + perspective → 18 | **18 (z 8–26)** |
| Hatch | — | aws67: 325/40 × 6 = 49?? (×0.6) → 29 | aws65: 115/300 × 62 = 24 | **26 × 36** |

---

## 13. Consistency check: conflicts and reconciliation

1. **Length vs the 101.6 cube.** The ring front (y +44, or +46 at the tooth) to the box rear (y −66) gives **110–112 mm**: too long. Options: (a) the box is shorter (rear at y −56), (b) the ring is smaller (Ø 80), or (c) the robot fits diagonally (cube rules allow any orientation; the diagonal of a 101.6 square is 143 mm). AWS checks the cube with the robot in any orientation, so a 110 mm length is **allowed if the width and height are small** (fitting diagonally: L + W ≈ 110 + 93 → no, the diagonal fit needs √(L² + W²)·cos… it needs the robot to fit inside the box footprint; 110 × 93 does **not** fit). **Reconciled: shorten the box to y −56 (box 48 long) and keep ring Ø 88 → length 102 at the tooth tip, 100 at the mean rim.** The wheels move to y −38 (inside the box's rear 18 mm). This also matches aws65's hub-to-rear ratio (57/88 → rear at y −57).
2. **Ring vs wheels.** At the wheel centre y −38 the ring's half-chord is √(44² − 38²) = 22 mm, so the ring passes **inboard** of the wheels (inner face x ±33). At the tyre's front edge (y −22) the half-chord is 37.9 > 33, so in plan the ring reaches under the front of each tyre. Check heights: at y −22 the tyre's lowest point is at z 16 (the tyre front is vertical there), well above the ring top (z 6). At y −30 the tyre bottom is at z 2.1, but there the ring's half-chord is only 29.7 < 33, so the ring is inboard of the tyre. ✓ No collision anywhere. The WG blocks in front of the wheels are **above the ring's path** and guard the tyre's front from the ring's own hits on the opponent (debris) and from opponents.
3. **Ring mass.** Steel 3 mm at Ø 88/70 = 52 g of rim alone: too heavy for a 150 g robot with all its parts (motors 20, weapon motor 25, battery 20, ESCs 12, chassis 30, wheels 8 → 115 g + the ring). The ring must be **≤ 35 g**. **Reconciled: 2 mm hardened steel (rim 35 g) or 3 mm titanium (30 g). Choose 2 mm steel.** The edge looks thin in aws67 (2–3 mm), consistent with this.
4. **Height**: the wheels reach 32, and the box top is 26 (+3 for the hatch = 29). ✓ The robot can drive upside down on its wheels, with the ring on top (useless, but mobile).
5. **Tooth position**: it differs between photos (330°, 300°, 30°), as expected for a spinning ring. ✓

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Huge ring for the robot's size**: maximise the radius → the moment of inertia grows with r². A ring puts almost all its mass at the rim (the best energy per gram). Three thin spokes are the minimum for a stable hub joint, and the open sectors save mass.
- **Ring low and in front**: it hits opponents' wheels and wedge lips (an undercutter), and the ring is hard to wedge under because it sits ≈ 3 mm off the floor.
- **One tooth**: a single deep step gives a large "bite" (time for the opponent to enter the tooth's path between passes), so more of the stored energy transfers in each hit. The cost is balance: a single step leaves the ring slightly out of balance. Spiralling the rim radius over the whole circle spreads the extra mass, which keeps the imbalance small.
- **Inverted outrunner in a nose lobe**: the shortest load path from the ring to the chassis. The lobe's thick printed walls take the reaction torque. The stator screws through the roof make it serviceable from the top.
- **Wheels at the rear, outboard and taller than the box**: invertible drive, and the wheels are kept out of the ring's swept area.
- **Front guard blocks (WG)**: protect the most exposed wheel area (the front) from rebounds after hits. They may also carry an outboard axle support.
- **Raised hatch on 3 screws**: quick battery access. A low-profile raised panel is a separate print, so it can be replaced when hit.
- **Recessed switch**: the rules require an accessible switch. The recess prevents accidental switching by hits.
- **Raised lettering, coloured wheels**: identification and team style.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Confidence |
|---|---|---|
| Weapon motor | 2205–2806 class outrunner, inverted in the lobe | H |
| Ring–bell joint | 3–4 M3 screws into the bell face, with a printed or Al spacer | M |
| Bearing | a flanged 3 mm-bore bearing in the lobe roof, under AX | M |
| Underside skid | a small printed skid/ball under the box front to keep the ring off the floor | M |
| Drive motors | N20 at ≈ 300–600 rpm, along X at y −38 | M |
| Weapon ESC | 10–20 A BLHeli ESC in the front of the box | M |
| Drive ESC + RX | a combined dual brushed ESC/receiver | M |
| Battery | 2S/3S 300 mAh LiPo under the hatch | M |
| Ring thickness | 2 mm steel | M |
| Rear spoke | identical to the front ones, under the box | H |

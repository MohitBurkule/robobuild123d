# Corsac: full rebuild description from reference photos

Source photos (all three cut out onto white by the AWS wiki):
- `robots/corsac/reference/corsac.aws72.webp`: AWS 72. **Front-right three-quarter**, camera about 35° above the floor and roughly 50° right of the nose. The fox-face front panel is on the image right; the **right side** (clear green-edged guard plate, right wheel, right "paw" with claws) is on the image left; the black top cage and a **brass wire** at the rear are at the top.
- `robots/corsac/reference/corsac.aws74.webp`: AWS 74. **Front-left three-quarter**, camera about 25° above the floor, about 35° left of the nose. Shows the fox face almost frontally, the **sawtooth front wedge** below it, and the **left** side with its paw, wheel and green-edged guard plate.
- `robots/corsac/reference/corsac.aws76.webp`: AWS 76. Same pose as AWS74. The fox-face print is **badly torn** (battle damage), revealing the black printed backing panel and showing that the face panel is a printed plate with a paper print glued on.

`REFERENCE.json`: `wedge`, 2 wheels, weapon wedge (no active weapon).

Pixel coordinates refer to copies scaled to 1200 px on the long side (AWS72 → 1200 × 822, AWS74 → 1200 × 822, AWS76 → 1200 × 826), ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit and from the visible **N20 gearmotors** (brass gearbox 12 × 10 mm section) and **Ø 24 mm rubber wheels**. Ratios use **W = body width at the rear (outer faces of the guard plates) ≈ 86 mm**.

A corsac is a steppe fox; the robot is themed as a **fox head** (front panel with ears and narrowed eyes) with **clawed paws** at the front corners.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the fox face), **+Z** = up. **Origin O** = floor point under the centre of the main body footprint (the tub between the wheels, excluding the front wedge teeth).
- The face panel's slope angle **γ** = angle of the panel above the floor; the lower toothed wedge's slope **δ**.

| ID | Part |
|---|---|
| CH | black main body/tub |
| FP | fox-face front panel (black printed backing) |
| FP-P | paper print of the fox face glued on FP |
| FP-S | 4 black screws on FP (at the eyes) |
| EAR-L / EAR-R | ear points of FP |
| TW | lower sawtooth front wedge (black, teeth along the edge) |
| TW-T | individual triangular teeth |
| PW-L / PW-R | black paws at the front corners |
| CL | claws on the paws |
| CG | top cage/frame (black side rails and rear cross-beam) |
| CG-R | rear cross-beam of the cage |
| BW | brass wire link/pin at the rear top |
| WH-L / WH-R | rear wheels (black rubber, ribbed) |
| GM-L / GM-R | N20 gearmotors (brass gearbox, white end caps) |
| MC | white printed motor clamps/caps |
| GP-L / GP-R | clear acrylic/PC side guard plates (green edges) |
| GP-S | screws on GP |
| GPS | guard spacer block (black, between GP and the body) |
| TS | silver screw with washer on the top deck near each wheel |
| RD | small red/white component inside (AWS72) |
| BAT, RX, ESC | hidden electronics (guess) |

---

## 1. Overall description in one paragraph

Corsac is a **two-wheel wedge robot styled as a fox head**. Its black printed body is about 86 mm wide and 80 mm long, very low at the front and rising to a **top cage** about 40 mm high at the back. The front is a **two-stage wedge**: a low **sawtooth plate** whose leading edge is a row of about **nine sharp triangular teeth** on the floor, and above/behind it a **steep fox-face panel** shaped like a fox's head with two **pointed ears**, faced with a **grey paper print** of a scowling fox (narrowed eyes, whisker lines, a black nose). At each front corner, beside the face, a **black rounded paw** sticks out with **four or five claws** pointing forward. The two **drive wheels** sit at the **rear corners**, each shielded on the outside by a **clear plate with green-glowing edges** held by two screws to a black spacer. The top of the body is an open **frame/cage** (two rails and a rear cross-beam) through which the **white N20 motor clamps**, brass gearboxes and some wiring are visible, and a **bent brass wire** sticks out of the rear cross-beam as a removable power link.

---

## 2. Part-by-part description

### 2.1 Main body (CH)
- **Shape**: a black printed tub, about **70 mm wide (X) between the wheel pockets × 72 mm long (Y)**, with a flat floor. The rear half is a box about **22 mm tall** (deck at z ≈ 22) holding the motors; the front half is covered by the face panel and the wedge.
- **Deck**: flat black top surfaces at z ≈ 22 beside the wheels (AWS72: the right deck at (245–500, 330–470) px; AWS74/76: the left deck at (880–1080, 260–420) px), each with a **silver pan-head screw with a washer** (TS, head Ø 5 mm) near the front inner corner of the wheel pocket.
- **Sides**: below the deck, the side walls are vertical (AWS74: the left wall below the deck, black, about 18 mm tall), merging at the front into the paws.
- **Colour/material**: matt black PLA/PETG with fine layer lines; the front surfaces show diagonal infill texture.

### 2.2 Fox-face panel (FP, FP-P, FP-S, EAR)
- **Outline (front view)**: a **fox head**: a **pentagon** with a **V-notch** in the top: the bottom edge straight, about **82 mm** wide; the sides rise vertically (slightly outward) about **35 mm**; then each side goes up and inward to an **ear tip**; between the ears a **V-notch** reaching down about **18 mm**. Ear tips about **50 mm** above the bottom edge (in the panel plane), about **55 mm apart**. In AWS74 the outline is: bottom (120, 525)–(800, 600) px, left ear tip (355, 45), right ear tip (820, 140), notch bottom (575, 285).
- **Slope**: the panel leans back at about **γ ≈ 65–70°** from the floor (steep): in AWS72 (side-ish view) its plane rises from the wedge root at y ≈ +30 to the ear tips at y ≈ +12.
- **Thickness**: backing about **3 mm** black printed plate (AWS72 shows its black edge along the left side, ~3 mm), with the print **(FP-P)**, a ~0.2 mm paper sheet, glued over the front.
- **Print**: a grey fox face: two **pale grey ear interiors** (triangles) inside the ear tips; **narrowed angry eyes** (white with a black upper line) at about 40% height; **white cheek fur tufts** at the lower sides; **whisker strokes**; a **black triangular nose** at the bottom centre. In AWS76 the print is torn away over its lower half, exposing black backing and white paper fibres.
- **Screws (FP-S)**: **4 small black pan-head Phillips screws** (head Ø 3.5 mm, M2): two at each eye (one above the other, about 10 mm apart): AWS74 at (325, 210), (720, 300); AWS72 shows two per eye (at (893, 172), (925, 218) and (612, 320), (643, 378)). They fix the panel to two **vertical posts/brackets** of the body behind it **(guess)**.
- **Behind the panel**: an open space; through the ear notch in AWS72 the cage interior (black) is visible, and in AWS74 white/red internals.

### 2.3 Sawtooth front wedge (TW, TW-T)
- **Shape**: a **black printed plate** about **3 mm thick**, **86 mm wide**, lying at a **low slope δ ≈ 20°**, from the base of the face panel (z ≈ 10) forward and down to the floor. Its **leading edge is a row of triangular teeth** (TW-T): AWS74/76 show **8–9 teeth**, each about **9 mm wide at the base × 9–11 mm long**, pointed (sharp tips), with small **step/sawtooth facets** on their tops (the teeth have a **second smaller step**, like a double tooth or a stepped chisel). Their tips touch the floor.
- **Depth**: from the face panel base to the tooth tips about **22 mm** (plan).
- **Extends sideways**: at the outer ends, the wedge wraps around into the paws (the outermost teeth merge with the claws).
- **Material/finish**: black PLA/PETG; the teeth show layer texture and a few broken tips (AWS76).

### 2.4 Paws (PW-L, PW-R) and claws (CL)
- **Shape**: at each front corner, outboard of the face panel and in front of the wheel pocket, a **rounded black lump** like a curled paw: about **24 mm long (Y) × 18 mm wide (X) × 18 mm tall (Z)**, with a **domed top** (radius about 10 mm) and **concentric layer rings** visible (printed as a dome, AWS72 (280–480, 520–700) px).
- **Claws**: at the front-bottom of each paw, **4–5 pointed claws**, each a narrow triangular spike about **3 mm wide × 10–14 mm long**, pointing **forward and down**, side by side, curving slightly downward, with their tips at or just above the floor. AWS72: claws at (430–600, 640–780) px; AWS74: the left paw's claws at (850–980, 620–700) and the right paw's claws at (50–100, 380–470).
- **Position**: paw centres at about **x ±38, y +25, z 9**, claw tips reaching **y ≈ +45**.

### 2.5 Top cage (CG, CG-R)
- **Shape**: an open frame over the rear half: **two black side rails**, each about **8 mm wide × 12 mm tall**, running from just behind the face panel's ears (y ≈ +10, z ≈ 38) back to the rear (y ≈ −38, z ≈ 40), and a **rear cross-beam** (CG-R) about **60 mm long × 10 mm × 12 mm** joining their rear ends. In AWS72 the rails look like **inverted-L/angle sections** with a sloped outer face. Between the rails the top is **open** (looking into the body).
- **Front**: the rails join the top of the face panel's back (behind the ears) and the body front posts.
- **Rear**: the cross-beam sits at the rear top, roughly above the wheel axle line, with a **small black block** at its middle carrying the brass wire.
- **Function**: a **roll cage** that keeps the robot's top from being crushed and gives a surface to rest on when inverted; also the mount of the power link.

### 2.6 Brass wire (BW)
- **Shape**: a **brass/copper rod Ø 1.5 mm**, about **25 mm** long, sticking **sideways and up** out of the rear cross-beam, with a **U-bend** (hook) at its inner end (AWS74/76 show it entering a hole in the cross-beam's top and bending back down). AWS72 shows it sticking out to the robot's right at the rear.
- **Function**: a **removable power link** (a shorting pin inserted into a socket) **(high-medium confidence)**; it is the standard antweight "link" made from brass rod.

### 2.7 Wheels (WH-L, WH-R) and motors (GM, MC)
- **Wheels**: **black rubber**, **Ø 24 mm × 9 mm**, with **transverse ribs** (about 40), on black hubs (N20 wheels). Visible at the rear corners: AWS72 right wheel at (130–270, 345–460) px and left wheel at the far top (720–840, 55–110).
- **Positions**: centres at **x ±37, y −22, z 12**.
- **Gearmotors**: **N20** with **brass gearboxes** next to the wheels (AWS72 at (270–300, 380–410)) and **white end caps/clamps** (MC): white rectangular blocks about **12 × 14 × 10 mm** inboard of each wheel (AWS72 (235–345, 300–390), AWS74 (880–960, 245–295)). These are white printed **motor clamps** or the motors' white plastic **encoder/back caps** **(guess: printed clamps)**.
- **Wheel top**: z 24, about 2 mm above the deck.

### 2.8 Guard plates (GP-L, GP-R), spacers (GPS) and screws (GP-S)
- **GP shape**: a **clear acrylic or polycarbonate plate**, about **2 mm thick**, standing vertically outside each rear wheel: about **30 mm long (Y) × 22 mm tall (Z)**, rectangular with a **slanted front edge** (the front edge leans back toward the top). Its **edges glow green** (fluorescent-green tinted acrylic/PETG or edge-lit by the green background; most likely **fluorescent green acrylic**).
- **Position**: outer face at **x ±43**, y −38 to −8, z 2 to 24.
- **Screws (GP-S)**: **2 silver pan-head screws** near the front edge (stacked vertically, about 10 mm apart: AWS72 at (40, 430) and (240, 575)… along the plate; AWS74 at (1150, 320) and (1095, 465)), plus 1–2 at the rear.
- **Spacer (GPS)**: a **black block** between the plate and the body side in front of the wheel (AWS72 (230–290, 440–560)), into which the front screws go. The rear of the plate is fixed to the rear cross-beam/rear wall.
- **Function**: **wheel guards** covering the wheels' outer faces; they are the robot's widest points at the rear.

### 2.9 Visible internals
- AWS72: the white motor clamps, a **red-and-white small component** (a connector or the receiver's LED) at (380–440, 290–340), a white rounded component (servo? no weapon — likely the **receiver**). AWS74/76: white and red parts through the ear notch.

---

## 3. Per-view sections

### 3.1 AWS72 (front-right)
- **Right**: the fox panel (490–1175, 45–770) with its ears, eyes and screws; the sawtooth wedge only peeking below its left part.
- **Left**: the right guard plate (25–265, 395–630) with green edges and 2–3 screws; the right wheel behind it (130–270, 345–460); the right deck with the silver screw/washer (300, 425); the right paw (280–480, 520–700) with claws (430–600, 640–780).
- **Top**: the cage rails from (190, 230) to (500, 300) and from (290, 150) to (860, 170); rear cross-beam (540–860, 30–110); the left wheel far top (720–840, 55–110) with a green spot (far guard edge); the brass wire at (190–290, 195–240).

### 3.2 AWS74 (front-left)
- **Centre-left**: the fox face (120–900, 45–690) with the ear notch showing white internals; the sawtooth wedge teeth along the bottom (80–820, 530–790), about 9 teeth.
- **Right**: the left deck (880–1080, 230–420) with a silver screw (1010, 325); the left wheel (1010–1080, 255–320); the left guard plate (1080–1160, 285–510) with screws; the left paw (850–1010, 430–700) with claws.
- **Top**: cage rails and rear beam (390–900, 40–230); the brass wire at (360–560, 25–80).
- **Far left**: the right paw's claws (50–100, 380–470).

### 3.3 AWS76 (front-left, damaged print)
- As AWS74; the print torn, showing the black backing with diagonal infill texture; the teeth at (60–790, 560–770); left paw (850–1060, 450–690).

### 3.4 Top view (synthesised)
- Body 70 wide with wheel pockets at the rear corners and guard plates at ±43; the wedge 86 wide with 9 teeth reaching y ≈ +48; paws at the front corners with claws to y +45; the face panel as a thin line at y ≈ +12 to +28 (sloping); the open cage over the rear half with the brass wire on the rear beam.

### 3.5 Front view
- The fox head silhouette (82 wide, 50 tall to the ear tips), under it the toothed wedge edge (86 wide) on the floor, paws at both sides (to z 18) with claws, the guard plates just visible behind the paws at ±43, the cage rails visible through the ear notch.

### 3.6 Side view (left)
- Floor line with the tooth tips at y +48 and the claws at y +45; the paw dome; the steep face panel rising to the ear at z 48; the cage rail running back at z 38–40 to the rear beam; the wheel (Ø 24) at y −22 behind the clear guard plate.

### 3.7 Rear view (not photographed)
- Rear wall, wheels with guard plates at both sides, the cage cross-beam with the brass link on top **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | tub | 70 × 72 × 22 | 0.81 × 0.84 × 0.26 | black FDM | — | 1 |
| FP | fox-head plate | 82 × 50 × 3 | 0.95 × 0.58 | black FDM + paper | 4 × M2 | 1 |
| FP-P | paper print | 82 × 50 | — | grey/white/black | glue | 1 |
| TW | toothed wedge plate | 86 × 22 × 3, 9 teeth 9 × 10 | 1 × 0.26 | black FDM | integral with CH (guess) | 1 |
| PW | domed paw | 18 × 24 × 18 | 0.21 × 0.28 | black FDM | integral (guess) | 2 |
| CL | claws | 3 × 12 each | — | black | integral | 8–10 |
| CG | rails + beam | 8 × 12 × 50 rails; 60 × 10 × 12 beam | — | black | integral / screws | 1 |
| BW | bent rod | Ø 1.5 × 25 | — | brass | in socket | 1 |
| WH | ribbed wheel | Ø 24 × 9 | 0.28 | black rubber | N20 shaft | 2 |
| GM | N20 gearmotor | 12 × 10 × 25 | — | brass/silver | MC clamp | 2 |
| MC | clamp block | 12 × 14 × 10 | — | white FDM | screws | 2 |
| GP | clear guard plate | 30 × 22 × 2 | 0.35 × 0.26 | fluorescent green acrylic/PC | 3–4 × M2 | 2 |
| GPS | spacer | 6 × 8 × 18 | — | black | screws | 2 |
| TS | pan screw + washer | head Ø 5 | — | silver | into CH | 2 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| FP ↔ CH front posts | screwed (4) | 0 |
| FP bottom edge ↔ TW top | meeting | 0–1 |
| FP-P ↔ FP | glued | 0 |
| TW tooth tips ↔ floor | touching | 0 |
| TW outer ends ↔ PW | joined | 0 |
| PW ↔ CH | integral | 0 |
| CL tips ↔ floor | near | 0–2 |
| CG rails ↔ FP back (at ears) | joined | 0 |
| CG ↔ CH rear | joined | 0 |
| BW ↔ CG-R socket | inserted | 0 |
| WH inner ↔ CH pocket wall | near | 1–2 |
| WH outer ↔ GP | near | 1–2 |
| GP ↔ GPS / CH rear | screwed | 0 |
| GP bottom ↔ floor | above | 2 |
| WH top ↔ deck | above | +2 |
| WH top ↔ cage top | below | −16 |
| CH floor ↔ floor | above | 2 |

---

## 6. Mechanism
- **Drive**: two rear wheels on N20 gearmotors, skid steer. The front rests on the tooth tips (and the claw tips): a sliding front.
- **Weapon**: none active; the robot is a **pusher/wedge**. The sawtooth edge gets under opponents, the steep face panel then stops them at the front while the robot shoves them into hazards or walls.
- **Invertibility (guess)**: upside down the robot would rest on the cage top (z 40) and the ear tips, with the wheels (top z 24) not reaching the floor, so **not invertible**; the steep face and ears make it roll back over onto its wheels in many cases (a "self-righting" shape) **(low confidence)**.

---

## 7. Assembly order (suggested)
1. Print CH with integral toothed wedge, paws, cage (or the cage separately), FP, MC, GPS.
2. Fit the N20 gearmotors with the white clamps MC; press on the wheels.
3. Install the battery, receiver, ESC and the link socket in the rear beam.
4. Screw the guard spacers and the clear guard plates GP.
5. Glue the fox print to FP; screw FP to the front posts (4 screws through the eyes).
6. Insert the brass link BW.

---

## 8. Hidden / uncertain list
- Whether the toothed wedge is a separate plate or part of the tub.
- Whether the cage is part of the tub.
- Motor clamp details; internal layout.
- The rear face and underside.
- Guard plate material (fluorescent acrylic vs PETG).
- All mm ±15–20%.

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the tub centre; +X right, +Y forward, +Z up, mm.
- Tub x ∈ [−35, +35], y ∈ [−38, +26], z ∈ [2, 22]; guards x ±[41, 43]; wedge teeth to y +48; face panel to z 48; cage to z 40.

## 10. Profiles as math

**10.1 Face panel outline (front view; u across, w up the panel from its bottom edge).** Polygon: (−41, 0) → (+41, 0) → (+42, 35) → (+28, 50) → (+8, 32) → (0, 32)… use a symmetric V: (+28, 50) → (0, 32) → (−28, 50) → (−42, 35) → close. Pose: (x = u, y = 28 − w·cos 68°, z = 10 + w·sin 68°).

**10.2 Toothed wedge (YZ).** Plate top line z = 10 − 0.364·(y − 26) for y ∈ [26, 48] (20°). Tooth outline in plan: N = 9 teeth across x ∈ [−43, +43], pitch p = 9.55; each tooth: base from x_k − p/2 to x_k + p/2 at y = 38, tip at (x_k, 48), where x_k = −43 + p·(k + 0.5), k = 0…8. Secondary step: at y = 43 the tooth top drops 1 mm (a stepped chisel).

**10.3 Paw (dome).** Ellipsoid centre (±38, +25, 2), semi-axes a_x 9, a_y 12, a_z 16, cut at z = 0. Claws: 5 cones from points on the dome at z ≈ 6, x = ±(32, 35, 38, 41, 44), aimed along (0, cos 15°, −sin 15°), length 12, base Ø 3.

**10.4 Cage rail (YZ, at x ±27).** Line from (y +12, z 38) to (y −38, z 40), section 8 × 12. Rear beam: box x ∈ [−30, +30], y ∈ [−42, −32], z ∈ [30, 42].

**10.5 Guard plate (YZ at x ±43).** Polygon: (−40, 2) → (−8, 2) → (−12, 24) → (−40, 24) → close. Holes at (−14, 18), (−12, 8), (−36, 14).

**10.6 Wheel.** r 12, width 9; ribs r(φ) = 12 + 0.5·[sin(40φ) > 0].

## 11. Pixel measurements
- **AWS74**: face panel bottom edge ≈ 690 px; ear-tip spacing ≈ 470 px; panel height to the ear tips ≈ 480 px (projected); tooth pitch ≈ 75–80 px; left wheel visible ≈ 70 px wide (oblique) and ≈ 75 px tall; guard plate ≈ 225 px tall.
- **AWS72**: face panel width along its bottom ≈ 520 px (oblique); right wheel ≈ 140 × 115 px; guard plate ≈ 240 × 240 px (oblique, near); paw ≈ 200 × 180 px; brass wire ≈ 105 px.
- **AWS76**: tooth row ≈ 730 px for 9 teeth → ≈ 81 px pitch.

## 12. Several independent estimates

| Quantity | Method A (rule/part) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width | ≤ 101.6 | — | AWS74: face 690 px; teeth 730 px; if teeth = 86 → 8.5 px/mm → face 81 | **86 (wedge), 82 (face)** |
| Wheel Ø | N20 wheel 22–25 | 0.28 W | AWS72: 140 px; guard 240 px tall = 22 mm?? → 13; using the face scale (AWS72 at the wheel ≈ 6 px/mm) → 23 | **24** |
| Face height to ears | 50 | 0.58 W | AWS74: 480 px / 8.5 / sin 68° ≈ 61 (near-camera, ×0.85) ≈ 52 | **50** |
| Tooth pitch | 86/9 = 9.6 | — | 81 px / 8.5 = 9.5 | **9.55** |
| Guard plate height | 22 | 0.26 W | AWS74: 225 px at far scale ~ 8 px/mm (rear, slightly farther) = 28 (incl. perspective) | **22–24** |
| Cage height | 40 | 0.47 W | AWS74: cage top ≈ 0.75 × ear tip height above the floor → 0.75 × 56 = 42 | **40** |
| Length | 101.6 limit; 48 + 42 = 90 | — | AWS72 side span from the guard rear to the face front ≈ 1060 px ≈ (oblique) 90–95 | **90** |

## 13. Consistency check
1. **Box fit**: length 90 (y −42 to +48), width 86, height 52 (ears) — all within 101.6 ✓.
2. **Ear height vs cage**: the ears (z ≈ 56 at their tips with the panel's base at z 10 and 50 mm along a 68° plane: 10 + 50·sin 68° = 56) stick up above the cage (40) — matches AWS74 where the ears are the highest points. Use **z_ear = 56**.
3. **Wheel vs guard**: wheel Ø 24 at z 12 → top z 24; guard plate 22 tall from z 2 → 24: the guard covers the full wheel face ✓ (AWS72: the guard hides most of the wheel).
4. **Teeth count**: 8 in AWS74 (one hidden at the right), 9 in AWS76. **Reconciled 9.**

---

## 14. Why the designer did it (adversarial first)

- **Sawtooth leading edge**: a saw-toothed wedge gets under opponents at many small points; if one tooth lifts on a floor seam, the others still touch. Pointed teeth dig into opponents' wedge lips (forks-like behaviour), winning the "who gets under whom" contest against flat wedges. Being printed, they are sacrificial; broken teeth (AWS76) don't stop the robot. Weak point: printed tips are not as sharp as steel forks.
- **Steep fox-face panel**: once under, the opponent rides up the low teeth and meets a steep face: it can't climb over Corsac and is pushed. Against vertical spinners, a steep high face presents a target, but the plate is just a cover over a solid frame and is cheap to reprint (the torn print in AWS76 shows it takes hits). Ears add height to stop opponents riding over the top.
- **Paws with claws**: protect the front corners (where the wheels/guards are vulnerable to angled attacks), and the claws act as **extra forks** at the corners, catching opponents that come in at an angle. Domed backs deflect hits. Theming.
- **Rear wheels with clear guard plates**: wheels at the back keep the front free for the wedge and put traction behind the pushing face; clear guard plates shield the wheel faces from horizontal spinners and side wedges, while staying light. Their green edges make the robot easy to track in the arena.
- **Open top cage**: rigid, light structure; a crush-resistant rail on top in case of being driven over or flipped; open top saves weight and gives ventilation and access.
- **Brass link**: arms/disarms the robot from outside without opening it; the rule-compliant removable link.
- **No active weapon**: all weight goes to robustness and drive: a wedge/pusher strategy, relying on getting under and controlling opponents.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors (brass gearbox) | 12 × 10 × 25 | (±22, −22, 12) along X | high |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 9 | (0, 0, 8) under the cage centre | medium |
| RX + ESC | combined board | 25 × 20 × 6 | (0, +15, 10) behind the face | medium |
| Link socket | 2 brass tubes / a JST receptacle for the brass pin | — | (0, −37, 38) in the rear beam | medium |
| Face mounting posts | two vertical posts behind the eyes with M2 pilot holes | 6 × 6 × 30 | (±20, +18, 25) | medium |
| Wheel guard rear fixing | screws into the rear wall | — | (±43, −38, 14) | low |
| Wiring | battery → link → ESC → motors; all inside the tub under the cage | — | — | medium |

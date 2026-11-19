# Queen Sarah Denning: full rebuild description from reference photos

Source photos:
- `robots/queen_sarah_denning/reference/queen_sarah_denning.aws71.webp` (AWS 71, 1617 × 1527 px, cut out). The **best photo**. Camera **in front of the robot, high** (about 50–60° above the floor), nearly square-on, so the front scoop is at the bottom of the image and the rear at the top. Bright **red** print; the clear side plates show a **green** tint (the cut-out background through clear plastic). **Green cat/snake-eye stickers** on the two side pods.
- `robots/queen_sarah_denning/reference/queen_sarah_denning.aws69.webp` (AWS 69, 722 × 734 px, not cut out, on an oak desk). An **earlier version**, darker **brick-red/brown** (painted or different filament), with **blue eye stickers**. Camera almost **straight down** (about 70–80°), the robot rotated so its front points to the **lower-right**. Shows the top layout clearly: three longitudinal sections, all the top screws, a black tube, a **clear plastic flap** at the rear of the centre section and **clear skirts** around the front scoop.
- `robots/queen_sarah_denning/reference/queen_sarah_denning.aws70.webp` (AWS 70, 327 × 358 px, small). Camera **in front, about 45–55° high**; red, **green eyes**, the clear side plates with black screws seen at the left, the front scoop with two screws and a clear front edge. A grey round object at the top-left (part of the background or the left wheel, guess low).

Facts are read from the photos; inferences are marked **(guess)**. Dimensions are **estimates**. Scale: the AWS 150 g / 101.6 mm cube; the **black M3 button-head screws** (head Ø ≈ 5.5 mm, hexalobular/hex socket seen in aws71); the kit draft (`kit.json`: flipper; body 110 × 100 × 36, ramp 30; two internal wheels r 12 × 10 at y −30; a 40 × 80 × 8 flipper plate at (0, −8, 40) pivoting at (y −45, z 38); a 90 × 30 × 2 front scoop at (0, +62, 8) tilted −15°). Ratios are against **W = body width ≈ 96 mm** (outer faces of the clear side plates).

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the scoop), **+Z** up. Units mm.
- **Origin O** = floor point under the centre of the footprint (mid-width, mid-length from the scoop's front edge to the rear wall).
- aws71/aws70: +Y points toward the camera (down the image), +X to the image left (the robot faces the camera), +Z up/toward the top of the image.
- aws69: +Y points to the lower-right of the image, +X to the lower-left... (the robot's right pod is the one at the image left with the lower eye; see 3.2).

| ID | Part |
|---|---|
| CH | chassis (hidden; floor and inner walls) |
| FL | central flipper strip (segmented, red) |
| FL-1…FL-4 | the strip's visible segments (rear to front) |
| FFE | flipper front end face (thick, layered) |
| HG | rear hinge of FL (with clear plastic flap/hinge in aws69) |
| CF | clear plastic flap at the rear of FL (aws69) |
| PD-L, PD-R | left and right side pods (red, with eye stickers) |
| PT | pods' rear flat tops |
| PS | pods' front slopes |
| EY-L, EY-R | eye stickers |
| S-PD | black screws on the pods (tops and slopes) |
| S-FL | screws and small holes on FL (aws69) |
| TB | black tube/hole in the right pod top (aws69) |
| SC | front scoop (full-width wedge, red with frosted clear overlay) |
| SCO | clear/frosted polycarbonate overlay on SC |
| S-SC | scoop screws |
| SK | clear skirts at the scoop edges (aws69, aws70) |
| SP-L, SP-R | clear polycarbonate side plates |
| S-SP | black screws along the side plates' edges |
| RC | small red rounded protrusions at the rear corners (aws69) |
| WH-L, WH-R | drive wheels (hidden) |
| SV, M-L, M-R, BAT, ESC, RX, SW | hidden internals |

---

## 1. Overall description in one paragraph

Queen Sarah Denning is a **red, flat, three-lane servo flipper with a full-width front scoop and a pair of angry eyes**. Seen from the front it is a **low trapezoidal block** about **96 mm wide, 100 mm long and 36 mm tall**, built from three longitudinal sections: a **central flipper strip about 34 mm wide**, made of several **printed segments** that slope down toward the front, and two **side pods about 30 mm wide**, each with a **flat rear top** carrying two screws and a **steep front slope** printed with **horizontal layer ridges** and decorated with a tall **almond-shaped "cat/snake eye" sticker** (green iris with a slit pupil and a white highlight in AWS 70/71; blue in AWS 69). The eyes slant inward like a frowning face. Across the whole front lies a **wide scoop**: a red plate, sloping down at about **25–30°** to the floor, covered with a **frosted clear plastic sheet** and held by **two screws**, its edges extended by **clear skirts**. The outer sides are **clear polycarbonate plates** held by a row of **black screws** along their front edges. The central strip is hinged at the rear (a **clear flexible flap** is seen there in AWS 69) and is the **flipper**: driven by a servo, it lifts at the front to tip opponents that have been scooped onto it (guess, high).

---

## 2. Part-by-part description (AWS 71 unless stated)

### 2.1 Central flipper strip (FL)
- **Plan**: a strip about **34 mm wide at the rear** widening slightly to about **38 mm at the front** (aws71: 455 px at the top vs 560 px at the front, with perspective; true widening ≈ 2–4 mm or none, guess) running from the rear (y ≈ −50) to the back edge of the scoop (y ≈ +28).
- **Segments** (aws71, from the rear):
  - **FL-1**: a **flat rear block** about **34 × 14 mm**, top at **z ≈ 36**, standing slightly **proud** of the pods' rear tops (≈ 2 mm), with a smooth top (px (545–990, 60–210)).
  - **FL-2**: a **sloping panel** about **34 × 22 mm** with a **diagonal hatched top texture** and a raised **perimeter rim** (≈ 1 mm), px (550–1035, 210–450).
  - **FL-3**: the longest panel, about **36 × 30 mm**, same hatched texture and rim, px (550–1090, 450–790).
  - **FL-4**: a short panel, about **37 × 8 mm**, px (550–1110, 790–870).
  - **FFE**: the **front end face**, a vertical-ish band about **8–10 mm tall** showing **stacked layer lines** (the flipper's thickness), px (550–1130, 870–965), sitting just behind the scoop.
- **Side profile (guess from the face-on photo)**: the strip slopes **down toward the front** at about **12–15°** from z 36 at the rear to about **z 26** at its front top edge, and its front face drops ~10 mm to z ≈ 16 where the scoop's rear edge begins.
- **Segments' meaning**: the lines between segments are **seams**: the strip is probably **one flipper plate** printed with **panels of different infill/top patterns** (cosmetic) or **several printed plates glued to a flipper arm** (guess). In aws69 the strip shows **three panels separated by thin black seams** and carries **screws (S-FL)**: two black screw heads near the front of the rear panel (aws69 px (285, 295), (395, 237)), one at the front panel (420, 420), plus a **small hole Ø ≈ 2** with a dark insert (385, 355): these fix the **flipper plate to the servo arm** (guess, medium).
- **Colour/material**: red PLA/PETG; aws69 brick red.

### 2.2 Rear hinge (HG) and clear flap (CF)
- In aws69, a **clear plastic flap** about **30 × 14 mm**, 0.5 mm thick, lies over the **rear edge** of FL and bends down over the rear: probably a **flexible polycarbonate/PET living hinge** taped/screwed between the flipper plate and the chassis, or a **rear skirt** (guess, medium). The kit puts the flipper pivot at **(y −45, z 38)**. Reconciled: **FL pivots about an X axis at its rear top (y ≈ −46, z ≈ 34)** via a pin hinge or this plastic flap.

### 2.3 Side pods (PD-L, PD-R)
- **Plan**: each **≈ 30 mm wide**, x ±17…±45, from y ≈ −50 to +28.
- **Rear top (PT)**: a **flat area** about **30 × 18 mm** at **z ≈ 34**, with **two black screws** near its outer/rear corner (aws71 left pod px (245, 100) and (230, 165); right pod (1295, 90) and (1335, 155)); aws69 shows **three screws** on each pod's rear top (one of which may be on the side plate).
- **Front slope (PS)**: from the rear top's front edge (y ≈ −32, z 34) down to (y ≈ +28, z ≈ 14): about **18–20°** in side view?? The face looks steep in aws71 because the camera is high: its **horizontal ridges** (layer lines about 0.3 mm, plus coarser ridges about **4 mm** apart giving a stepped/terraced look) show it was printed upright. Reconciled from the kit and from aws69 (where the slopes look long): slope about **20°** over ≈ 60 mm, the pod front edge at z ≈ 14 above the scoop.
- **Inner edges**: a small vertical gap (about 1 mm) separates each pod from FL (dark lines in all photos), so FL can move.
- **Outer edges**: the pod outer faces are covered by the clear side plates.
- **Screw on the slope**: one **black button-head screw** on each slope near the eye's lower inner corner (aws71 left (330, 690), right (1330, 680)): pod-to-chassis fixing.
- **Small hole/marks**: aws69 shows a small hole at the right pod's slope bottom (px (513, 368)).

### 2.4 Eye stickers (EY-L, EY-R)
- **Shape**: tall **almond / flame-shaped eyes** about **20 mm wide × 40 mm tall** (in the slope plane), with a **black outline** (thick on the inner, upper edge like an eyebrow, thin on the outer edge), a **white border** (die-cut sticker edge), a **green iris** (AWS 70/71) filling the middle with a **dark horizontal slit pupil** (a long spike pointing to the inside) and a small **white oval highlight** at the top; the lower part is pale grey/white (sclera). The eyes are **mirror images**, their pointed lower tips curving **outward** and their pointed tops leaning **inward**, giving a **fierce, slanted look**.
- **AWS 69**: **blue** iris with a round white highlight, different style (a classic cartoon "evil eye" sticker); the left eye lies across the pod's lower slope.
- Position: centred on each pod's slope, about (±31, −2, 24).

### 2.5 Front scoop (SC), overlay (SCO), skirts (SK)
- **Shape**: a **full-width wedge plate** about **92 mm wide (x ±46) × 30 mm deep (Y, plan) × 3 mm thick**, sloping from its rear edge at about **(y +28, z 16)** down to a **thin front edge on the floor** at about **(y +52, z 0.5)**: slope about **33°** in side view (kit: tilt −15° for a box at z 8 — gentler; see 12). Its upper face is **red**, covered by a **frosted, slightly pink translucent sheet** (SCO, polycarbonate ≈ 1 mm, scuffed matt by wear) about **80 × 25 mm**, its left end marked by a **thin black line** (tape edge or the sheet's edge, px (255–270, 1000–1240)).
- **Screws (S-SC)**: **two countersunk/flat screws** (Ø ≈ 4) through the overlay near its ends, at about (±32, +40) (aws71 px (355, 1170), (1340, 1170)); aws70 shows **two silver/grey screws** at the same places; aws69 shows **pairs** of screws at each end (4 in total).
- **Skirts (SK)**: **clear plastic** extends the scoop's front edge by about **3–5 mm** (aws69: a clear sheet projecting beyond the red plate at the front and both ends; aws70: clear front edge band). They make the very leading edge thin and flexible.
- **Scoop ends**: the scoop's ends meet the clear side plates; at the lower corners the side plates' front edges bend to follow the scoop (aws71 left (160, 980) → (210, 1240)).

### 2.6 Clear side plates (SP-L, SP-R)
- **Shape**: **clear polycarbonate**, about **3 mm thick**, at x ±45…±48 (aws71 shows them leaning **outward toward the bottom**: the body is a **trapezoid in front view**, about 88 wide at the top and 96 at the bottom; the plates tilt about **7–8°** from vertical).
- **Side outline (guess)**: rear vertical edge (y −50) full height (z 0–36); top edge following the pods' profile (flat z 34 then sloping to z 14 at y +28); front edge following the scoop down to the floor at y +52.
- **Screws (S-SP)**: a **row of 5 black screws** along each plate's front/top edge, roughly every 15 mm (aws71 left: px (110, 200), (100, 440), (110, 650), (150, 880), (180, 1140); right: (1530, 320), (1530, 430), (1525, 700), (1510, 870), (1515, 1140)). They screw into the pods' outer faces and the scoop's ends.
- **Edges**: slightly chipped/frosted (worn).

### 2.7 Black tube (TB) (aws69)
- A **black hollow cylinder**, outer Ø ≈ 7, inner Ø ≈ 4, flush with the top, on the **right pod's rear top**, next to FL (aws69 px (430, 210)). Likely the **power switch access hole / link socket** or a **LED holder** (guess, medium). In AWS 71 this region shows no tube (perhaps hidden by the raised FL-1).

### 2.8 Rear corner protrusions (RC) (aws69)
- **Small red rounded shapes** stick out at both **rear corners**, beyond the clear side plates (aws69 px (20–45, 250–300) at the left with a bent wire/clip, (480–520, 20–50) at the right). Possibly the **tops of red wheels** set at the rear corners, or **red rear bumpers**, or **antenna/clip parts** (guess, low). The kit says the wheels are **inside**; these may be rear-corner **wheel hubs** showing through notches.

### 2.9 Wheels (WH, hidden)
- **Guess**: two **red or black TPU wheels Ø ≈ 24–26 × 10 mm** inside the pods near the rear, centres at about **(±32, −30, 12.5)**, protruding through floor slots; the side plates hide them.

### 2.10 Hidden internals
- **Flipper servo**: a high-torque micro servo under FL at the rear-centre, output along X near the hinge (guess, medium).
- **Drive**: two N20 gearmotors in the pods (rear).
- **Electronics**: battery, receiver, dual ESC, switch (under TB).

---

## 3. Per-view sections

### 3.1 aws71 (front, high)
- Top-centre: FL-1 rear block; down the middle: the hatched segments FL-2/3/4 and the layered front face FFE.
- Left and right: the two pods with their screws, ridged slopes and **green eyes**; the eyes' slit pupils point toward the centre.
- Bottom: the **wide scoop** with the frosted overlay and two screws; the clear side plates with five screws each, framing everything, leaning outward at the bottom.

### 3.2 aws69 (top-down, older version)
- Robot rotated about 30°, scoop at the lower-right covered with clear plastic and with black marks; the three lanes visible; the blue eyes (one on each pod slope); screws on the pod tops and on the flipper; the black tube; the clear flap at the rear of FL (upper-left); red protrusions at the rear corners.

### 3.3 aws70 (front, small)
- Same as aws71 but darker; the left clear side plate and its screws seen at a grazing angle; the scoop's clear front band and two screws; the trapezoidal front silhouette.

### 3.4 Top view (synthesised)
- 96 × 100 outline; three lanes: pods 30 wide (x ±17…±45) and FL 34 wide; pod rear tops with 2 screws each; slopes with eyes; scoop 92 wide across the front (y +28 to +52); side plates 3 mm along both sides.

### 3.5 Side view (synthesised)
- Clear plate outline: 36 tall at the rear, flat top to y −32, slope down to z 14 at y +28, then the scoop slope to the floor at y +52; FL slightly above the pod line at the rear; wheels near the rear behind the clear plate.

### 3.6 Front view
- A trapezoid: 88 wide at the top, 96 at the bottom; the scoop face at the bottom, the FL front face above its centre, the two eyes on the pod slopes.

### 3.7 Rear and underside (not photographed)
- Rear: flat wall, FL's hinge at the top centre, possibly the wheels at the corners. Underside: flat, wheel slots near the rear, scoop edge at the front.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| FL | segmented sloped strip | 34–37 × 78 × 8–10 | 0.36 × 0.81 | red FDM | hinge + servo screws | 1 |
| CF | clear flap | 30 × 14 × 0.5 | — | PC/PET | tape/screws | 1 |
| PD | pods (flat top + slope) | 30 × 78 × 34 | 0.31 × 0.81 | red FDM, ridged | screws | 2 |
| EY | eye stickers | 20 × 40 | 0.21 | printed vinyl | stuck | 2 |
| SC | wedge plate | 92 × 30 (plan) × 3, ≈ 33° | 0.96 | red FDM | screws | 1 |
| SCO | frosted overlay | 80 × 25 × 1 | — | polycarbonate | 2 screws | 1 |
| SK | clear skirts | 3–5 wide | — | polycarbonate | under SC | 1–3 |
| SP | clear side plates | 100 × 36 × 3, 7° lean | — | polycarbonate | 5 screws each | 2 |
| S-PD/S-SP | button heads | M3, Ø 5.5 | — | black | — | ≈ 16 |
| S-SC | flat heads | Ø 4 | — | black/silver | — | 2–4 |
| TB | tube | Ø 7 / 4 | — | black | in pod | 1 |
| WH | wheels (hidden) | Ø 25 × 10 | 0.26 | TPU | motor shaft | 2 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| FL sides ↔ pod inner faces | running clearance | ≈ 1 |
| FL-1 top ↔ pod rear tops | FL proud | +2 |
| FL front face ↔ SC rear edge | clearance | 1–2 |
| FL ↔ hinge | pivoting | 0 |
| CF ↔ FL / CH | taped/screwed | 0 |
| Pods ↔ CH | screwed | 0 |
| SP ↔ pods/SC ends | screwed | 0 |
| SC ↔ CH | screwed | 0 |
| SCO ↔ SC | screwed flat | 0 |
| SC front edge ↔ floor | touching | 0–0.5 |
| SK ↔ floor | touching | 0 |
| SP bottom ↔ floor | near | 0.5–1 |
| EY ↔ pod slopes | stuck | 0 |
| WH outer face ↔ SP inner face | inside | 3–5 (guess) |
| WH bottom ↔ floor | touching | 0 |

---

## 6. Mechanism
1. **Drive**: two internal rear wheels; front resting on the scoop's edge.
2. **Scoop**: gets under opponents across the full width; they ride up onto the flipper strip's front.
3. **Flipper**: a servo lifts FL about its rear hinge, raising its front end (FFE) by maybe 30–40 mm (rotation ≈ 30–40°), tipping the opponent over backward or sideways (a **rear-hinged lifting flipper / "tipper"**) (guess, high from the kit and the layout).
4. **Invertibility**: the body is a flat box 36 tall; wheels hidden inside likely do not reach the top; inverted, the flipper may self-right it by pushing off the floor (guess, medium).

---

## 7. Assembly order (suggested rebuild)
1. Print CH (floor, inner walls, motor and servo mounts), two pods (with rear tops and ridged slopes), FL (segmented plate), SC (scoop); cut SP ×2, SCO and skirts from polycarbonate.
2. Fit drive motors and wheels; fit servo; fit battery, ESC, receiver, switch (under TB).
3. Screw the pods onto CH.
4. Fit FL on its hinge (pin or clear flap) and screw it to the servo arm.
5. Screw SC with SCO and SK across the front.
6. Screw SP plates to both sides (5 screws each).
7. Stick on the eyes.

---

## 8. Coordinate frame (restated)
- Footprint: x ±48 (bottom), y −50…+52. Top z 36 (FL-1), pods z 34.
- FL: x ±17 (rear) to ±18.5 (front), y −50…+26; hinge at (y −46, z 34).
- Pods: x ±17…±45.
- SC: rear edge (y +28, z 16), front edge (y +52, z 0.5), x ±46.
- SP: x ±45…±48 (leaning 7°), y −50…+52.

## 9. Profiles as math

**9.1 Pod side profile (YZ).** (−50, 0) → (−50, 34) → (−32, 34) → (+28, 14) [z = 34 − (y + 32)/3, 18.4°] → (+28, 0) → close.

**9.2 Flipper strip (YZ, top surface).** z = 36 for y ∈ [−50, −36] (FL-1); then z = 36 − 0.2·(y + 36) to y +26 (11.3°), front face from z 23.6 down to z 15 at y +26. Thickness 8–10.

**9.3 Scoop.** z = 16·(52 − y)/24 for y ∈ [28, 52] (33.7°); thickness 3 normal to the slope.

**9.4 Side plate lean.** Outer face x(z) = ±(48 − 0.125·z) (7.1° from vertical): x ±48 at z 0, ±43.5 at z 36.

**9.5 Eye sticker (in its own u–v plane, u across, v up the slope).** Outline: outer curve v = 20·sin(π·(u + 10)/20)... simpler: an almond formed by two arcs of radius 26 whose centres are at (u = ±16, v = 0), giving a lens 40 tall × 20 wide; rotated 15° so the top leans inward; the lower tip extended by a 6 mm curl outward. Iris: circle r 8 at (0, +3); pupil: a thin lens 12 × 1.5 horizontal, its point toward the centre line; highlight: ellipse 2.5 × 3.5 at (+2, +10).

## 10. Pixel-based measurements (aws71 native 1617 × 1527, ±10 px)
- FL: rear block (545–990, 60–210); front face (550–1130, 870–965).
- Left pod: (130–545, 90–960); right pod (1000–1460, 70–970).
- Eyes: left (190–545, 110–915), right (1100–1450, 95–895).
- Scoop: (230–1500, 990–1250); overlay (275–1385, 1050–1240); screws (355, 1170), (1340, 1170).
- Pod screws: (245, 100), (230, 165), (1295, 90), (1335, 155), slopes (330, 690), (1330, 680).
- Side plates: left outer edge (100, 120) → (210, 1240); right (1460, 120) → (1520, 1240).

## 11. Several independent estimates

| Quantity | Method A (kit / rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Width | kit 100 | — | aws71 bottom width ≈ 1420 px; screw head ≈ 70 px = 5.5 mm → 12.7 px/mm (at the pod tops, far) → 112?? (bottom is nearer: ≈ 15 px/mm) → 95 | **96** |
| FL width | kit 40 | ≈ 0.36 × W | 455 / 12.7 = 36 | **34–37** |
| Pod width | — | (96 − 36 − 6)/2 = 27 | 415 / 12.7 = 33 (incl. side plate) | **30** |
| Eye height | — | ≈ 0.42 × W | 800 px / ≈ 14 → 57 along the steep slope image?? (foreshortened, slope seen at ≈ 45°) → 40 | **40** |
| Scoop depth (slope) | kit 30 | ≈ 0.3 × W | 260 px / 15 → 17 seen, slope foreshortened (cos 55°) → 30 | **30 (along slope ≈ 29)** |
| Length | kit 110 (over 101.6) | ≈ 1.05 × W | — | **100–102 → 100** |
| Height | kit 36 | — | — | **36** |
| Flipper pivot | kit (y −45, z 38) | — | aws69 clear flap at the rear | **(y −46, z 34)** |

## 12. Consistency check
1. **Length**: kit 110 breaks the cube; use 100 (y −50…+52 ≈ 102 → trim scoop to +50: **100**).
2. **Scoop angle**: kit −15° (a near-flat plate at z 8) vs photos showing a moderately steep face in front view with the scoop ending at the FL front face (z ≈ 15): a plate from z 16 to the floor over 24 mm is ≈ 34°. Kept **≈ 33°**; the clear skirts lower the effective angle at the very edge.
3. **Trapezoid front view**: the side plates leaning out at the bottom (aws71, aws70) reconciled as 7° lean.
4. **Eye colour**: green (AWS 70, 71) vs blue (AWS 69): different events; use **green** for the latest build.
5. **Mass**: pods + FL + scoop + CH (red PLA, 2 mm walls) ≈ 60 g; polycarbonate plates 2 × 9 g; servo 15 g; motors 20 g; wheels 6 g; battery 15 g; electronics 8 g; screws 8 g: **≈ 150 g** (tight; the printed parts must be light).

---

## 13. Why the designer did it (per part, adversarial)

- **Full-width scoop with frosted polycarbonate and clear skirts**
  - Getting under: a wide, low scoop meets opponents anywhere across the front; the polycarbonate overlay and skirts make the leading edge thin, tough and replaceable (they wear: the overlay is scuffed white).
  - Against spinners: polycarbonate absorbs hits without shattering; the printed scoop behind it is backed up.
- **Central flipper strip**
  - Fight: once an opponent is on the scoop it slides onto the strip; lifting the strip tips it. The narrow strip (34 mm) is light so a servo can move it fast.
  - The rear hinge keeps the mechanism simple; the clear flap may act as a **living hinge** that needs no pin.
  - Segments: reduce print warping on a long thin part and allow replacing only the damaged front segment (guess).
- **Side pods with sloped fronts**
  - Deflect hits upward; house wheels and electronics; give the robot a low, wedge-like profile from the front corners too.
  - Ridged slopes: printed upright for strength against frontal hits (layers perpendicular to the impact direction would delaminate; here the load goes along the layers' plane... the designer chose upright printing for a clean slope surface, guess).
- **Clear side plates leaning outward**
  - Tough, light side armour; the outward lean deflects horizontal spinners' hits downward and toward the floor rather than flipping the robot (and makes the base wider and more stable).
  - Many screws: spread impact load so the plates don't tear off.
- **Eyes**
  - Character ("Queen" with a fierce cat/snake gaze); zero cost.
- **Black tube**
  - Easy switch/link access from the top without removing parts (guess).

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Flipper servo | metal-gear micro/mini servo (≥ 3 kg·cm) | 23 × 12 × 25 | (0, −35, 18), horn near the hinge | medium |
| Hinge | Ø 2–3 pin through FL-1 and CH, or clear living hinge | 34 long | (y −46, z 34) | medium |
| Drive motors | 2 × N20 | 12 × 10 × 25 | in the pods (±30, −30, 12.5) | medium |
| Wheels | Ø 25 × 10 TPU | — | (±32, −30, 12.5) | medium-low |
| Battery | 2S 180–300 mAh LiPo | 35 × 18 × 10 | under FL front (0, 0, 8) | medium |
| ESC/RX | combined ant board | 25 × 20 × 6 | in a pod (−30, +5, 10) | medium |
| Switch | slide switch under TB | 10 × 6 | (+22, −42, 28) | medium |
| Wiring | battery → switch → board → motors and servo | — | — | medium |

## 15. What the photos cannot show
- True side profile (all photos are from the front or above), the rear, the underside, the wheels and the flipper's range.
- All values are estimates (±15%); the side profile is the least certain.

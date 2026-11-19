# Stagnant: full rebuild description from reference photos

Source photos:
- `robots/stagnant/reference/stagnant.aws67.webp`: AWS 67, 2056 × 1268 px, cut out onto white, sharp, with a **strong green colour cast** over everything (the black plastic looks green-black, the steel looks green-grey with blue/purple heat tint at the left end). **Front view from about 20–25° above**, robot square to the camera and turned about 10° to its left, so the **front steel plate** fills the lower two-thirds and the right side's wheels show at the far right.
- `robots/stagnant/reference/stagnant.aws62.webp`: AWS 62, 649 × 526 px, on a pale wooden table, slightly soft. **Front-left three-quarter from about 50° above**, the front plate facing the lower right. Shows the top of the body, both hinge brackets with their **aluminium leaves**, the left pair of wheels and the right pair.

Stagnant is a **four-wheel, low, wide pusher with a full-width bent steel front plate** (a "wedge/bulldozer") hung from **two bracket-and-leaf mounts** on the front top edge of a **black printed body**. It has no active weapon. Everything stated as fact is read from the photos; anything inferred is marked **(guess)**. All mm values are **estimates** (±15%), scaled from the AWS 101.6 mm (4 in) cube, from the small N20-class wheel size (Ø 20–24 mm), and from screw sizes and pixel ratios. Ratios are given against **W = front plate width ≈ 96 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the steel plate), **+Z** = up; mm. **Origin** = the point on the floor (z = 0) under the centre of the body footprint (mid-width, mid-length of the black body, **not** including the plate). Side-profile angles are measured from the floor.
- **Front** = the steel plate side. In both photos the front faces the camera (AWS67 straight on, AWS62 toward the lower right).

| ID | Part |
|---|---|
| BD | black printed body (tub) |
| TP | body top plate (black, diagonal print texture) |
| FP | front steel plate (main face) |
| FP-L | lower lip band of the front plate (lighter, bevelled/bent) |
| FP-W-L / FP-W-R | wrap-around side returns of the front plate |
| FP-N-L / FP-N-R | notches in the plate's top edge where the leaves pass |
| HB-L / HB-R | hinge/mount brackets (black printed slotted blocks) on the body front-top corners |
| LF-L / LF-R | leaves (flat tabs) linking the plate to the brackets: green FR4/G10 (AWS67), aluminium (AWS62) |
| HB-BT | bracket bolts (2 per bracket) with nyloc nuts and button heads |
| S-FP | two large slotted cheese-head screws on the plate face |
| S-TP | small black screws on the top plate |
| SR-R / SR-L | side rails between the wheels (black, ladder-like) |
| SG-R / SG-L | thin black side guard plates outboard of the wheels |
| WH-FL, WH-RL, WH-FR, WH-RR | four small black treaded wheels |
| M-x, BAT, RX, ESC, SW | drive motors, battery, receiver, ESCs, switch (hidden, guess) |

---

## 1. Overall description in one paragraph

Stagnant is a **wide, low, four-wheeled bulldozer** about **98 mm wide, 72 mm long (including the plate) and 26 mm tall**. Its body is a **matte black printed tub** with a **flat top plate** (fine diagonal print texture, one or two small screws). Hung across the whole front is a **single bent steel plate** about **1.2–1.5 mm thick**: a **flat, steep main face** about 96 mm wide and 25 mm tall, a **lighter lower band** along the bottom that forms a **sharpened lip** at floor level, and **rounded corners that wrap back** a few millimetres around both front corners. The plate is badly **scratched and heat-tinted** (blue/purple at the left end), clearly a working armour plate. Two **large slotted cheese-head screws** on its face fix it to **two flat leaves**. These leaves rise through **notches** in the plate's top edge into **slotted black brackets** on the body's front-top corners, each clamped by **two bolts with nyloc nuts**. The four **small black treaded wheels** (about Ø 22 × 8 mm) sit at the four corners inside the body width, two per side, with thin black side plates outboard of the right pair. The wheels stick slightly above the top plate, so the robot drives either way up.

---

## 2. Part-by-part description

### 2.1 Body (BD)
- **Shape**: a low rectangular tub about **90 mm wide (X) × 58 mm long (Y) × 22 mm tall** (top plate surface at z ≈ 24), with **wheel recesses** at all four corners. The body is narrower than the plate: its front face is hidden behind the plate.
- **Material/colour**: **matte black FDM** (PLA/PETG); in AWS67 it looks dark green-black because of the colour cast. Layer lines are visible on the vertical faces.
- **Side rails (SR)**: between the front and rear wheels on each side, a **black printed rail** about **6 mm wide × 10 mm tall**. On the right side in AWS67 it looks like a **ladder/bridge**: a horizontal bar at about z = 14 linking the bracket area to the **side guard** at the far right, with the wheels above and below it in the view.
- **Side guards (SG)**: on the right side in AWS67, a **thin black plate** (about **2 mm thick, 50 mm long, 22 mm tall**) stands vertically **outboard of the right wheels** at x ≈ +49, with a **small screw** on its outer face near the top front. Its front edge meets the steel plate's right wrap. The left side guard is not visible (the left wheels are seen from the front) **(guess: symmetric)**.
- **Underside**: not seen. Ground clearance about **2–3 mm** **(guess)**.

### 2.2 Top plate (TP)
- **Shape**: a flat plate about **86 × 52 mm**, **2 mm** thick, on top of the tub at z ≈ 22–24. Its surface shows the **diagonal crosshatch of a printed top layer**, with a faint **diagonal seam** (two print regions meeting) running from front-left to rear-right.
- **Screws S-TP**: AWS67 shows **one small black pan-head screw at the rear centre** (about (+5, −20)) and one near the right bracket (about (+30, +5)). AWS62 shows **one silver screw near the front centre** at (−3, +10) and one at the right rear corner (+40, −22), plus one at the left front (−40, +18).
- **Front edge**: at the left and right ends of the front edge, the plate has **recesses** in which the brackets HB sit; between them the front edge is straight and lies just behind the steel plate's top edge.

### 2.3 Front steel plate (FP)
- **Main face**: a flat **steel** sheet about **1.2–1.5 mm thick**, **96 mm wide** (x −48 … +48) and about **24 mm tall** measured along its face. It is **steep**: about **70–75° from the floor** (leaning back slightly at the top), so in AWS67 (viewed from 20–25° above) it looks almost like a vertical wall.
- **Top edge**: straight, at z ≈ 24, slightly **below or level with the top plate's front edge**. It has two **narrow notches FP-N** (about 4 mm wide × 8 mm deep) at about **x = −30** and **x = +24**, through which the leaves pass. The top edge right of the right notch slopes down slightly to the right corner.
- **Lower band FP-L**: the bottom **8–10 mm** of the plate is **lighter and smoother** than the face above, with a crisp horizontal boundary at z ≈ 9. It looks like either a **ground bevel/sharpened lip** or the plate **bent forward to a shallower angle (about 35–45°)** for the last 8–10 mm so the edge meets the floor at a low angle **(guess: bent lip, medium)**. The bottom edge is straight and touches the floor across the full width.
- **Wrap-around ends FP-W**: both ends of the plate **curve back** around the front corners with a **radius of about 5–6 mm**, continuing as short **side returns about 8–12 mm long** toward the rear. The right return in AWS67 ends just in front of the side guard SG-R. The left end shows **blue/purple heat tint**, as if the plate was heated to bend it there (or tempered).
- **Surface**: dull grey steel with many **scratches and gouges** (vertical scrape marks from arena floors and opponents), dark smudges, and the tint at the left.
- **Screws S-FP**: **two large slotted cheese-head (fillister) screws**, head about **Ø 8 mm** (M4), at about **(−36, +y, z 15)** and **(+25, +y, z 8)** in AWS67. The left one sits high and left, the right one low and right of centre, so they are **not symmetric**. In AWS62 the left screw is at the lower left and the right one at the upper right of the face, which is also asymmetric. They pass through the plate into the leaves' lower ends **(guess, medium)**, or into the body's front wall.

### 2.4 Brackets (HB-L, HB-R) and leaves (LF-L, LF-R)
- **Brackets HB**: two **black printed slotted blocks**, each about **14 mm wide (X) × 12 mm long (Y) × 14 mm tall**, set into recesses at the front corners of the top plate. Left bracket centre at about **(−30, +22, 20)**, right at about **(+24, +22, 20)**. Each has a **vertical slot** (about 3 mm wide) running front to back in which a leaf sits, with two **cheeks** either side.
- **Bolts HB-BT**: two **horizontal bolts along X** through each bracket's cheeks and leaf, about **8 mm apart vertically** (upper at z ≈ 22, lower at z ≈ 15). One side shows **silver nyloc nuts** (M3, across flats 5.5 mm, with the blue/white nylon insert visible). The other side shows **silver button heads**: the right bracket has nuts on its left face and button heads on its right face; the left bracket has nuts on its left face.
- **Leaves LF**: flat tabs about **2–3 mm thick**.
  - **AWS67**: **green FR4/G10-looking** sheet (partly the colour cast; the right one has a clear PCB-green tone). **LF-R** is a **rounded rectangle tab** about **12 × 20 mm**, standing almost vertical and slightly tilted, its top rounded, its lower part passing **down through the plate's notch**. **LF-L** is much bigger and different: a **long triangle** about **35 mm long × 15 mm tall**, its point sticking **forward and to the left** past the plate's top edge like a **horn or fin**, with its long edge along the top. It is probably a replacement leaf cut in a hurry, or a deliberate **"wedgelet" prong** to catch opponents riding over the plate **(guess, low)**.
  - **AWS62**: both leaves are **bare aluminium strips** about **5 × 30 mm**, the left one lying **diagonally** from the bracket down-forward to the plate, the right one more upright.
- **Function**: the leaves connect the plate to the body. With two bolts each they are **clamped**, i.e. the plate is held **rigidly** **(guess, medium)**. Alternatively the upper bolt is the pivot and the lower bolt is a **stop**, which would let the plate **float/hinge** a few degrees to follow the floor **(guess, low–medium)**. The changed leaf angles between AWS62 and AWS67 suggest the plate position was adjusted between events.

### 2.5 Wheels (WH)
- **Count/position**: four, at the corners of the body, in recesses: **front** pair axles at about **y = +14**, **rear** pair at about **y = −20**, wheel centre planes at **x = ±42**, axle height z ≈ 11.
- **Size**: about **Ø 22 × 8 mm**.
- **Look**: **black printed TPU tyres with coarse straight ribs** (about 24 ribs; layer lines visible on the ribs in AWS67's zoom), or N20 rubber wheels. The ribs are about 1.5 mm deep.
- **Height**: the rear wheels' tops rise **1–2 mm above the top plate** (seen at the top left in AWS67), so the robot can drive inverted.
- **Visibility**: in AWS67, rear-left at the top left, front-left under the big left leaf, rear-right at the top right, front-right at the lower right behind the plate's right return. In AWS62, the two left wheels at the left end (one above the other in the view) and the two right wheels at the top right.

### 2.6 Hidden electronics, switch and wires
Nothing is visible: no wires, switch or lights in either photo. All electronics are inside the tub under the top plate **(guess)**.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 AWS67 (front, 20–25° down)
- **Outline**: a wide **rounded rectangle** (the steel plate), about **2.1:1** (width:height) in the image. The plate's rounded ends curve back at the left and right edges. Above it, a **thin black strip** (the body top) with two brackets, the **green triangle horn** sticking up-left at the left, and the right leaf. The four wheels peek out at the top corners and the right edge.
- **Plate**: big flat grey-green face, lighter lower band across the bottom third, two large slotted screws, scratches.

### 3.2 AWS62 (front-left, 50° down)
- **Outline**: a **trapezoid** (the body top seen at an angle) above a long **lower-front band** (the plate) that runs from the lower left to the right; the plate's ends curve back. The body top is a dark flat area with three silver screws, the two brackets with aluminium leaves, and wheels at the left end and the top-right corner.

### 3.3 Top view (synthesised)
- A 90 × 58 black rectangle (body) with wheel cut-outs at the corners; the plate as a thin 96-wide line along the front edge (y ≈ +30 … +36 including its lean and lip), its ends curving back 10 mm; the two brackets at the front corners of the top.

### 3.4 Side view (synthesised, right)
- A low rectangle 58 × 24 with two Ø 22 wheel circles, the side guard covering them, and the plate as a nearly vertical line at the front (top leaning back), with its lip kinking forward at the bottom.

### 3.5 Rear view (inferred)
- A plain black rear wall with two rear wheels at the corners; no detail known.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W (96) | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | tub | 90 × 58 × 22 | 0.94 × 0.6 × 0.23 | black FDM | — | 1 |
| TP | plate | 86 × 52 × 2 | 0.9 × 0.54 | black FDM | 2–3 small screws | 1 |
| FP | bent plate | 96 × 24 (face) × 1.3 | 1 × 0.25 | steel, scratched/tinted | 2 × M4 slotted | 1 |
| FP-L | lip band | 96 × 9 | 1 × 0.09 | lighter steel | integral | 1 |
| FP-W | side returns | R 6 + 10 long × 24 | 0.1 | steel | integral | 2 |
| FP-N | notches | 4 × 8 | — | — | — | 2 |
| HB | slotted block | 14 × 12 × 14 | 0.15 | black FDM | integral/screwed to BD | 2 |
| HB-BT | bolt + nyloc | M3 × 16 | — | steel, silver | through HB + LF | 4 |
| LF-R | tab | 12 × 20 × 2.5 | — | green FR4 (67) / Al (62) | 2 bolts + 1 screw | 1 |
| LF-L | triangle tab | 35 × 15 × 2.5 | 0.36 | green FR4 (67) / Al (62) | 2 bolts + 1 screw | 1 |
| S-FP | slotted cheese head | M4, head Ø 8 | 0.08 | zinc steel | into LF / BD | 2 |
| SR | rail | 6 × 30 × 10 | — | black FDM | integral | 2 |
| SG | thin plate | 50 × 22 × 2 | 0.52 × 0.23 | black | 1–2 screws | 2 |
| WH | wheel | Ø 22 × 8 | 0.23 × 0.08 | black ribbed TPU/rubber | motor shaft | 4 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP ↔ BD | screwed | 0 |
| HB ↔ TP/BD | seated in recess / integral | 0 |
| LF ↔ HB | clamped by 2 bolts | 0 |
| LF ↔ FP notch sides | passing through | 0.5–1 |
| LF lower end ↔ FP back | screwed (S-FP) | 0 |
| FP top edge ↔ TP front edge | just in front | 1–3 |
| FP back ↔ BD front wall | in front | 2–5 (guess) |
| FP lip ↔ floor | touching | 0–0.5 |
| FP-W return ↔ WH-F tyre | outside/ahead | 2–4 |
| FP-W-R end ↔ SG-R front edge | near | 1–2 |
| SG ↔ SR / BD | screwed | 0 |
| SG inner face ↔ WH outer face | side by side | 1–2 |
| WH inner face ↔ BD recess wall | side by side | 1 |
| WH-F ↔ WH-R tyres | fore-aft gap | 12 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ TP top | wheel above | +1–2 |
| BD floor ↔ ground | clearance | 2–3 |
| LF-L horn tip ↔ FP top edge | horn ahead and above | +5 ahead, +4 above |

---

## 6. Mechanism

1. **Drive**: four-wheel skid steer, probably **4 × N20 gearmotors** (one per wheel) or **2 motors** each driving a front and rear wheel through a belt/gear **(guess: 4 motors, medium)**.
2. **No weapon**. The steel plate is a **bulldozer blade/wedge**: the low lip gets under opponents' edges, the steep face pushes them, and the body behind is protected by steel.
3. **Plate mount**: two leaves in slotted brackets. Rigid **(medium)** or floating **(low–medium)**. If floating, the plate's weight keeps the lip on the floor while the body pitches.
4. **Invertible**: the wheels stick slightly above the top. Inverted, the plate's lip is then at the top, and the plate presents a steep wall at the front.

---

## 7. Assembly order (suggested rebuild)

1. Print the body tub BD with its wheel recesses, side rails and bracket seats; print the top plate TP and the two brackets HB.
2. Fit the drive motors and wheels.
3. Fit the battery, receiver, ESCs and switch inside; close with the top plate (2–3 screws).
4. Cut and bend the steel plate: a 96 × 33 blank, bend the lower 9 mm forward (lip), roll both ends back around R 6 into 10 mm returns, cut the two top notches. Grind the lip.
5. Cut the leaves (FR4 or aluminium). Screw each leaf's lower end to the back of the plate with the M4 slotted screw (nut behind, guess).
6. Drop the leaves into the bracket slots through the notches and fit the two M3 bolts and nylocs per bracket.
7. Screw on the side guards.

---

## 8. Hidden / uncertain list
- Whether the plate pivots or is rigid.
- The plate's real cross-section (bent lip vs ground bevel).
- Drive motor count and layout.
- The rear and underside.
- Left side guard.
- All mm ±15%; the colour cast in AWS67 makes the leaf colour uncertain.

---

## 9. Coordinate frame (restated)
- Origin on the floor under the centre of the body footprint; +X right, +Y forward, +Z up; mm.
- Body x ∈ [−45, +45], y ∈ [−29, +29], z ∈ [2, 24]. Plate: face plane from (y +31, z 24) down to (y +36, z 9), lip from (y +36, z 9) to (y +42, z 0); x ∈ [−48, +48]. Side returns from y +36 back to y +26 at x = ±48. Side guards at x = ±49. Wheel axles at y = +14 and −20, z = 11, centre planes x = ±42 (outer faces ±46).
- Overall bounding box: **≈ 100 × 72 × 26** (fits the cube).

## 10. Profiles as math (for rebuilding curves)

**10.1 Plate cross-section (YZ, any x in [−42, 42]).** Two straight segments:
- Main face: from A = (y 31, z 24) to B = (y 36, z 9). Slope from the floor: atan(15/5) = **71.6°**.
- Lip: from B to C = (y 42, z 0): slope atan(9/6) = **56°**. (If the lower band is only a ground bevel, use one straight line A → (y 39, z 0), 69°.)
- Fillet at B: R 3 inside bend.

**10.2 Plate plan at the corners (XY plane).** The front line y = y_face(z) runs to x = ±42; then a quarter-circle of radius 6 centred at (±42, y_face − 6) turns the plate back to run along x = ±48 for 10 mm toward −Y.

**10.3 Notches.** Rectangles in the top edge: x ∈ [−32, −28] and [+22, +26], depth 8 (z 16–24).

**10.4 Left horn leaf (AWS67), in its own plane (a vertical plane at x = −30, tilted 15° outward).** Triangle with vertices (y +20, z 26) (bracket top), (y +20, z 12) (lower bolt), (y +50, z 28) (tip, 6 mm ahead of the plate top edge and slightly above it).

**10.5 Wheels.** (y − y0)² + (z − 11)² = 11², y0 ∈ {+14, −20}. Ribs: 24 equal ribs of 1.5 mm depth, i.e. r(φ) = 11 − 0.75 (1 + sign(cos 24φ)) as a square-wave tread.

## 11. Pixel-based measurements (independent check)

AWS67 at 1400 px wide (scale 0.681 of the original):
- Plate width from the left curve (60, 380) to the right curve (1320, 520) ≈ **1270 px** along the face.
- Plate face height from the top edge (≈ 330) to the bottom edge (≈ 770) at x ≈ 400 ≈ **440 px**. At the right end (x ≈ 1200): 400 → 790 ≈ **390 px**. The view is 20–25° down and the plate is nearly vertical, so the vertical extent is almost true size: height/width = 440/1270 ≈ **0.35** → with W = 96, face + lip ≈ **33 mm** along the face (24 + 9). Consistent with the 24 + 9 split (boundary at about 60% down: 330 + 0.6 × 440 ≈ 595, where the lighter band starts at ≈ 540–580 ✓).
- Slotted screw head ≈ **85 px** → 85/1270 × 96 ≈ **6.4 mm** → M3.5/M4 cheese head (Ø 6–7). Revise: **Ø 7**.
- Nyloc nut ≈ **45 px** across flats → **3.4 mm**?? Too small for M3 (5.5 AF). The nuts are farther back (behind the plate top, about 25 mm deeper) and seen foreshortened; still, this suggests **M2.5 nylocs (5 AF)** at most. **Use M2.5–M3.**
- Rear-left wheel visible height ≈ **150 px** (top half only) → full Ø ≈ 22–24 mm by ratio. ✓
- Big left horn leaf: ≈ **280 px long** → **21 mm** projected; it points toward the camera-left, so the true length is about **30–35 mm**. ✓

AWS62 (649 px):
- Plate width (lower-left curve (95, 470) to the right end (600, 300)) ≈ **535 px**; body depth (front edge to rear edge on the left, (120, 330) → (160, 190)) ≈ **145 px**, foreshortened by the 50° view along Y: the body top is seen about 50° down, so its depth projects by about sin 50° = 0.77, giving a true **188 px** → 188/535 × 96 ≈ **34 mm**? Too short. The body's left end is farther from the camera (it is at the far end of a diagonal); scale it up ×1.4 → **47 mm**. With the plate's lean and wrap the body may be **50–58 mm** deep. **Use 58** (the AWS67 top view shows more depth; see §13).

## 12. Several independent estimates of key sizes

| Quantity | Method A (rules / parts) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width | ≤ 101.6 | 1.0 W + guards 2 | AWS67 plate 1270 px = W | **96 plate, 100 overall** |
| Body depth | — | 0.6 W = 58 | AWS62 34–47 (foreshortened) | **58** |
| Body height | wheel Ø + 2 | 0.25 W = 24 | AWS67 black strip above plate ≈ small | **24** |
| Plate height (face + lip) | 30–35 | 0.35 W = 34 | AWS67 33 | **33** |
| Wheel Ø | N20 wheels 22–25 | 0.23 W = 22 | 22–24 | **22** |
| Plate thickness | 1–1.5 spring steel | — | edge glint ≈ 15 px → 1.1 | **1.3** |
| Screw head | M4 cheese Ø 7 | — | 6.4 | **Ø 7** |
| Left horn length | — | — | 30–35 | **33** |

## 13. Consistency check: conflicts and reconciliation
1. **Body depth**: AWS62 pixels give 34–47 mm, ratios give 58. With wheels Ø 22 at two axles, the minimum depth is 2 × 22 + gap 10 = **54** (two wheels per side in tandem). **Reconciled 58** (wheels at y +14 and −20, 34 apart).
2. **Bracket positions**: the brackets are at x ≈ −30 and +24 (asymmetric, matching the asymmetric screws: left screw at x −36, right at +25). The photos show this asymmetry in **both** events, so it is real, not perspective. **Keep the asymmetry.**
3. **Leaf colour/material**: AWS62 silver aluminium; AWS67 green. The colour cast tints everything green, but the right leaf is clearly greener than the steel next to it, so it is probably **green FR4/G10**. Two versions, both described.
4. **Plate lean**: AWS67 looks nearly vertical, AWS62 shows the face lit and slanted. A ~72° face plus a 56° lip fits both.
5. **Nyloc size**: the pixel estimate (3.4 mm) is too small for any nut. The nuts are deeper and partly hidden; **M3** is the usual choice. Keep **M3**.
6. **Spec says wedge**: matches (bulldozer wedge).

---

## 14. Why the designer did it (per part, from several angles)

Common lens: **adversarial**. For each part: what can attack it (spinners, wedges, lifters, flippers, wall slams, inversion), how it survives, and how it helps win. Then construction reasons.

- **Full-width steel front plate**
  - Fight: the only "weapon" and the main armour. Steel survives vertical and horizontal spinner hits that would shred printed plastic (the scratches show it has taken many). The low lip gets under opponents; the steep face then pushes them like a bulldozer without letting them climb over. The wrap-around ends **protect the front wheels and corners** from horizontal spinners and stop wedges from hooking the corners.
  - Weak points: a steep plate is easy for a lower wedge to get under (the lip must be kept sharp); heavy steel takes a large part of the 150 g.
  - Construction: one cut-and-bent sheet; the heat tint shows the bend was done hot.
- **Two-leaf, slotted-bracket mount**
  - Fight: the leaves are the "fuse": a big hit bends a leaf rather than the body, and a bent leaf is quick to replace. If the plate floats, it follows the floor so the lip stays down.
  - Weak points: only two narrow attachment points; a strong uppercut can tear a leaf out.
  - Construction: bolts and nylocs, no glue; plate position adjustable via the leaves (AWS62 vs AWS67 differ).
- **Big left "horn" leaf (AWS67)**
  - Fight: a sharp point above the plate can catch opponents riding up the plate, or stop overhead hits on the top-left; it may also act as a **wedgelet** when inverted (it would then be at floor level at the front) **(guess)**.
- **Notches in the plate**
  - Construction: let the leaves pass through so the plate sits close to the body and the brackets stay hidden behind the plate.
- **Black printed tub and top plate**
  - Fight: low profile (24 mm) is a small target and gives a low centre of gravity, hard to flip.
  - Weak points: plastic sides and rear are unarmoured (only the side guards protect the wheels).
  - Construction: printed, screw-on top for access.
- **Four small wheels, inside the body width**
  - Fight: four-wheel drive gives the best pushing traction; small wheels keep the robot low. Wheels slightly above the top let it drive inverted. Inset wheels are protected by the plate's returns at the front and by the side guards.
  - Weak points: small wheels have little ground clearance over arena seams.
- **Side guards**
  - Fight: protect the right/left wheels from horizontal spinners and from being hooked.
- **Slotted cheese-head screws**
  - Construction: robust heads that survive scraping; a slotted head can be undone with any flat tool even when damaged.
- **Name "Stagnant"**
  - Character: a robot that just **sits and pushes**, with no moving weapon: a joke on being static/stagnant.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors, shafts along X | 12 × 10 × 25 | (±25, +14, 11), (±25, −20, 11) | medium |
| (alt) | 2 motors with belts to the front wheels | — | rear | low |
| Battery | 2S 300 mAh LiPo | 45 × 25 × 8 | (0, −3, 8) centre | medium |
| Receiver / ESC | combined board | 25 × 20 × 5 | (0, +12, 16) | medium |
| Switch | slide switch or link through the rear wall or top | 12 × 6 × 6 | (0, −29, 12) | low |
| Body front wall | printed, 2 mm, with nut traps for the plate screws | 86 × 2 × 20 | y +28 | medium |
| Plate screw nuts | M4 nuts behind the leaves | — | behind the S-FP positions | medium |
| Floor | integral 1.5 mm | — | z 2–3.5 | medium |
| Wiring | short leads to 4 motors | — | inside | high |

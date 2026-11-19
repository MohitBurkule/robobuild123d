# Smart Ant 5!!!: full rebuild description from reference photos

Source photos (AWS fan wiki, `File:Smart Ant 5!!!.awsNN.jpg`, stored as webp in `robots/smart_ant_5/reference/`):
- `smart_ant_5_.aws61.webp` (862 × 940 px), AWS 61. The **best view**. It looks at the front, high and nearly head-on (the user picked a camera at azimuth 90°, elevation 35°; the likeness gate uses 45°). The door is **closed**. Visible: the full grille, the hinge, both rear wheels, the aluminium lip and a clear polycarbonate extension, and the right flank (with a "5" sticker and embossed text). It sits on a light wooden table.
- `smart_ant_5_.aws63.webp` (586 × 476 px), AWS 63. The **front-right three-quarter** view, about 40° down. The door is closed. Visible: the right flank in full ("SmartAnt 5 V2.x" embossed along its bottom edge, a black "5" sticker), the right rear wheel face (white tread, blue five-spoke hub), the left rear wheel tread over the top, the hinge knuckles and the aluminium lip. Blue arena-floor background. Other robots are partly in frame (a red box at the top-left, an orange tub at the left, a red/black robot at the bottom).
- `smart_ant_5_.aws58.webp` (664 × 976 px), AWS 58. The **door is open**, seen from behind and above. This is an earlier version: a **blue** door, orange A-frame flanks, a brass floor plate, blu-tack ballast, a visible servo, battery and wiring. It is used for the inside layout and the hinge/servo mechanism only. Its outer shape differs from AWS 61/63 (open A-frame flanks, not solid flanks).

Everything stated as fact below is read from those photos. Anything inferred is marked **(guess)**, with a confidence tag where it matters. Dimensions in mm are **estimates**. The scale comes from the AWS antweight box (a 150 g robot fits a 101.6 mm cube when the lip is folded; the lip here is fixed, so the body is well under 100 mm) and from the current spec (`spec.json`: body 78 mm wide × 92 mm long × 44 mm tall, wheels Ø 28). Ratios are given against **W = body base width ≈ 78 mm**.

---

## 0. Coordinate system and naming

- **+X** = the robot's right, **+Y** = forward (toward the lip), **+Z** = up. Units are mm.
- **Origin O** = the floor point (z = 0) under the centre of the body footprint (mid-width; mid-length of the printed body, not counting the lip).
- The model in `spec.json` uses the wheel axle as z = 0. Model z = floor z − 14 (wheel radius). Below, **floor z** is used unless "model z" is written.
- **Front** = the lip end. **Rear** = the hinge/wheel end.
- In AWS 61 the robot's left is on the image left. In AWS 63 the camera is front-right, so the robot's right flank faces the camera. In AWS 58 the camera is behind and above the robot, so the robot's left is on the image left and the rear is at the top of the image.

| ID | Part |
|---|---|
| BD | orange printed body (base frame, flanks, rear wall, floor ring) |
| FL-L / FL-R | left and right leaning side flanks (triangular faces) |
| RW | rear wall (vertical, behind the hinge line) |
| DR | the trap door: orange printed grille, hinged at the rear-top |
| DF | door frame (outer border of the grille) |
| LR-1..5 | longitudinal ribs of the grille (fan toward the hinge) |
| TR-1..3 | transverse ribs of the grille |
| TB | small rib tabs that stick out past the door frame at the transverse-rib ends |
| HG | hinge: 5 knuckles (alternating body/door) on a steel pin |
| HP | hinge pin |
| LP | aluminium lip (front strip) |
| PC | clear polycarbonate extension under/ahead of the lip (AWS 61) |
| WH-L / WH-R | rear drive wheels: white ribbed tread, blue five-spoke hub |
| M-L / M-R | drive gearmotors (hidden; micro metal gearmotors, guess) |
| SV | door servo (seen in AWS 58: Turnigy S306x-HV class, metal case) |
| HN | servo horn plus white printed door link (AWS 58) |
| BAT | 2S LiPo (seen in AWS 58: blue/white label, lying diagonally) |
| ESC/RX | receiver + ESC board (hidden; guess Malenki-type combined board) |
| SW | power switch (AWS 58: small black rectangle at the left of the floor, guess) |
| FP | floor plate (AWS 58: brass/gold sheet) |
| BT | ballast (AWS 58: white/blue putty on the floor plate) |
| TX | embossed text "SmartAnt 5 V2.x" on the right flank, black "5" sticker |

---

## 1. Overall description in one paragraph

Smart Ant 5 is a **two-wheel, rear-drive, steep wedge with a trap door**. Seen from the front it is a **trapezoid**, wide at the floor and narrow at the top. Seen from the side it is a **right triangle**: the top face rises from the lip at the front to a hinge at the rear-top, and a short vertical rear wall drops to the floor. Seen from above, the sloped face (which is also the door) is a **trapezoid that narrows toward the rear hinge**. The whole sloped face is a hinged **orange grille door**. It has a thick frame, five longitudinal ribs that **fan in toward the hinge**, and three transverse ribs whose ends poke out past the frame as small tabs. The door swings up about a **five-knuckle hinge** along the narrow rear-top edge. A servo inside opens it, so the robot can trap or release an opponent, or use the door as a flipper-like lid. A full-width **aluminium strip lip** is fixed across the bottom-front edge, and in AWS 61 a **clear polycarbonate sheet** sticks out a further centimetre or so ahead of it. The two side flanks are solid sloped plates that lean inward. The right one carries the embossed name "SmartAnt 5 V2.x" and a sticker "5". Two **white ribbed wheels with blue five-spoke hubs** sit at the rear corners, partly outside the body, so the body hides most of each wheel from the front. The body is printed in **bright orange** filament. The electronics show through the grille: a servo with a red/white label, a LiPo with a warning label, a red JST plug and dark wiring.

---

## 2. Part-by-part description

### 2.1 Body base (BD)
- **Plan footprint**: a rectangle about **78 mm wide (W) × 92 mm long (1.18 W)**, not counting the lip. The rear edge is straight. The front edge is the hinge-less bottom edge of the door, where the lip is fixed.
- **Height**: the hinge axis is about **47–48 mm** above the floor (floor z). The top of the knuckles is about **50 mm**. The body proper (rear wall top) is about **46 mm**.
- **Ground clearance**: the body bottom edge sits about **2 mm** above the floor (wheels Ø 28 against a body bottom at the axle height minus 12) **(guess; the bottom is never seen)**.
- **Material**: bright orange FDM (PLA or PETG, possibly nylon in the spec). Layer lines are visible on the flanks in AWS 63 (horizontal, ~0.2 mm). The "SmartAnt 5 V2.x" text is printed in relief on the flank, so the flank is printed lying on its side or the text is on a vertical surface **(guess)**.

### 2.2 Side flanks (FL-L, FL-R)
- **Shape**: each flank is a **planar triangle-like face that leans inward**. Its bottom edge is a straight line on the body bottom at x ≈ ±39, from y ≈ −46 (rear) to y ≈ +46 (front). Its top edge is the door's side edge, running from the front-bottom corner (y ≈ +46, z ≈ 3.5) to the hinge end (y ≈ −36, z ≈ 46).
- **Lean**: in AWS 61 the flank faces are clearly visible from the front, and the door's top width is about **0.53 ×** its bottom width. So the flank leans in from a half-width of 39 mm at the floor to about 21 mm at the hinge height. That is a lean of (39 − 21)/44 ≈ **0.41 mm per mm**, about **22° from vertical**.
- Near the bottom there is a short **vertical band** (about 6–10 mm tall) before the lean starts. AWS 63 shows the flank meeting the floor with a near-vertical lower lip under the embossed text **(medium confidence)**. The current model uses a knee at floor z ≈ 10 (model z −4).
- **Rear part of the flank**: behind the door, the flank turns into the vertical **rear wall** (RW), and at the rear corner it carries the wheel mount. In AWS 63 the flank face runs back to the wheel and the wheel sits just outside it, with the hub about 3 mm outboard of the flank's lower edge.
- **Thickness**: about **2–3 mm** (printed skin) **(guess)**.
- **Markings (TX)**: on the right flank, embossed raised letters "SmartAnt 5 V2.x" run along the bottom edge from the front corner to under the wheel. The letters are about **5 mm tall**, raised about 0.6 mm. A black vinyl "5" sticker (about 8 × 10 mm) is at mid-height, about 60% of the way back. AWS 61 also shows a vertical stack of characters ("5", "Smart…") on the right flank's front corner.

### 2.3 Rear wall (RW)
- Never seen face-on. It is a vertical wall about **42 × 44 mm** (narrow at the top: it spans the flank width at each height, so it is also a trapezoid, 78 mm wide at the floor and 42 mm wide at the top) **(guess)**.
- It carries the hinge knuckles on its top edge (body knuckles) and probably the power switch **(guess)**.
- In AWS 58 the rear of the body is a horizontal orange bar at the top with the hinge knuckles, with the servo just below it.

### 2.4 Trap door (DR) and frame (DF)
- **Outline in plan**: an **isosceles trapezoid**. The front (bottom) edge is about **74 mm** wide (the body width minus the flanks' outer bevel). The rear (hinge) edge is about **40 mm** wide. The length along the slope is about **92 mm** (horizontal run about 82 mm, rise about 42 mm). The door sits at **27°** to the floor: atan(42.5/82) = 27.4°.
- **The user's note**: "It is not exactly rectangular… it's closer to the hinge." This means the door narrows toward the hinge. The narrowing is what makes the front view a trapezoid.
- **Frame**: a thick orange border about **4–5 mm wide** on the sides and **6 mm** at the front, with rounded inner corners (r ≈ 2 mm). At the hinge end the frame merges with the knuckles.
- **Thickness**: the door skin is about **3 mm**, but the ribs stand proud of the skin plane (see LR/TR), so the door looks about **5 mm thick** in section at the ribs **(guess)**.
- **Openings**: 6 columns × 4 rows of rounded rectangular windows (corner r ≈ 2 mm). The rows, front to back, measured along the slope: about **15 mm** (bottom row, right above the lip), **18 mm**, **18 mm**, and **22 mm** (top row near the hinge, where the servo shows through). The top row in AWS 61 has **extra thin slots** in the two right-of-centre columns: three or four narrow (~2 mm) vertical slits instead of one window, probably a stiffener over the servo horn **(guess)**.
- In AWS 63 the rows look more numerous (5–6) because the near side of the door is foreshortened. Counting the transverse ribs gives **3 inner ribs + front frame + hinge frame**, so 4 rows. This matches AWS 61.

### 2.5 Longitudinal ribs (LR-1..5)
- **Count**: 5 ribs, giving 6 columns.
- **Direction**: they do **not** run parallel. Each rib follows a line from the front edge to the hinge edge, at the same fraction of the local width. So the ribs **fan toward the hinge**. At the front the rib pitch is about 74/6 ≈ 12.3 mm; at the hinge it is about 40/6 ≈ 6.7 mm.
- **Section**: about **1.6–2.0 mm wide** (AWS 61: 10–14 px against a 640 px door width at the bottom row, i.e. 1.3–1.7 mm at the front; up to 2.5 mm where layer blobs show). They stand about **2–3 mm proud** of the frame, and their tops are rounded.
- **Shading**: in AWS 63 the ribs throw shadows and look like fins, so their height above the skin is roughly equal to their width.

### 2.6 Transverse ribs (TR-1..3) and tabs (TB)
- Three cross ribs, each about **2 mm wide**, the same height as the longitudinal ribs.
- **Tabs**: at each end, the transverse rib continues **3–4 mm past the frame's outer edge** as a small rounded nub (AWS 61: nubs on the left at y ≈ 275 px and 470 px, and on the right at y ≈ 340 px and 540 px). These could be print-in-place hooks for rubber bands, or simply the rib ends left long **(guess)**. They give the door's silhouette a **slightly saw-toothed side edge**.

### 2.7 Hinge (HG, HP)
- **Five knuckles** across the narrow top edge, each about **7–8 mm long** with **~1 mm gaps**, about **Ø 7 mm**. They are rounded orange cylinders.
- In AWS 61 the knuckles at the top (y ≈ 15–90 px, x ≈ 350–690 px) look like 5 separate blocks. Some are taller (door knuckles: 1, 3, 5) and some are part of the rear wall (2, 4) **(guess)**.
- **Pin**: a steel rod about **Ø 2–3 mm**. Its end is visible as a silver dot at the left of the hinge in AWS 61 (x ≈ 345 px). In AWS 58 the pin is a bright steel rod at the top right of the open door.
- **Axis**: along X, at floor z ≈ 47.5, y ≈ −42.

### 2.8 Lip (LP) and polycarbonate (PC)
- **LP**: an aluminium strip about **90 mm wide × 14 mm deep (along the slope) × 1.5–2 mm thick**. It is fixed at the bottom-front edge of the door (or of the body floor), angled at about **12°** to the floor. It is wider than the body by about **6 mm** each side. AWS 61: x 50–745 px at the bottom edge, against a body bottom width of about 640 px.
- **Fixing**: no screws are visible on the top surface. It is probably bonded or screwed from below into the body floor ring **(guess)**. AWS 63 shows a single straight edge with no hardware.
- **PC**: in AWS 61 a **clear sheet** about **0.5–1 mm** thick sticks out **8–12 mm** ahead of the aluminium, with reflections. It is probably a skirt to get under opponents that the lip cannot **(guess)**. It is not present in AWS 63 (or not visible).
- **Combat function**: the lip's front edge is the lowest point of the robot, about **0.5–1 mm** off the floor.

### 2.9 Wheels (WH-L, WH-R)
- **Size**: about **Ø 28 mm × 12 mm wide** (AWS 63: the right wheel spans about 120 px against a flank length of about 470 px for ~92 mm, which gives 23–26 mm Ø in projection; AWS 61 gives 26–28 mm from the left wheel's vertical extent of 165 px at about 6.3 px/mm). **Reconciled: Ø 28** (see §12).
- **Tread**: white rubber or TPU with about **24 axial grooves** (ribs about 2 mm wide, grooves about 1 mm deep). It looks like a moulded silicone tyre on a printed hub.
- **Hub**: blue printed, with **five spokes** and a central boss. The outer face is about 2 mm inside the tyre face.
- **Position**: centres at about **x ± 43.5**, **y ≈ −36**, axle z ≈ 14 (floor). The inner faces sit about **1 mm** outside the body flanks at axle height.
- **Visibility**: from the front (AWS 61) only the upper halves show, behind and outside the flanks. From the side (AWS 63) the right wheel is fully visible.

### 2.10 Drive motors (M-L, M-R), hidden
- **Guess**: two **micro metal gearmotors** (Pololu/N20 class, 12 × 10 × 25 mm gearbox plus motor, about 9.5 g each), lying transversely at the rear corners with the shafts straight into the wheel hubs **(medium)**. The spec uses `pololu_hpcb6v_50to1` at (±24, −36, 14 floor z).
- In AWS 58 two small dark cylinders show at the rear behind the servo, with orange motor clamps **(low)**.

### 2.11 Door servo (SV) and link (HN)
- AWS 58 shows a **servo with a silver metal case and a red label band** ("TURNIGY S306G-HV" mirrored) mounted at the rear-left inside the body, output shaft along X, just below the hinge line.
- A **white printed link/horn**, about 25 mm long and 4 mm wide, with two pinned joints, connects the servo output to a lug on the door's underside near the hinge. This forms a four-bar linkage that rotates the door about the hinge by about 90–100°: in AWS 58 the door stands nearly vertical, leaning back.
- In AWS 61 the same red/white label is visible through the top-left windows. So in the V2 body the servo sits at the rear-left (x ≈ −12, y ≈ −30, floor z ≈ 32) **(medium)**.

### 2.12 Battery (BAT), electronics (ESC/RX), switch (SW), wiring
- **Battery**: AWS 58 shows a small LiPo (blue/white printed wrap with a "WARNING READ AND FOLLOW…" label, about 40 × 16 × 10 mm) lying **diagonally at the right side** from the rear-centre to mid-right. Through the grille in AWS 61 the same warning-label pack is visible at the **right-middle** (x ≈ +15, y ≈ −5).
- **ESC/RX**: not identified. It is probably a combined board (Malenki/DasMikro type) under the servo or beside the battery **(low)**.
- **Switch**: AWS 58 has a small black rectangular object at the left-middle of the floor (near the left flank, below the servo). This could be a slide switch or an XT-style link **(low)**.
- **Wiring**: red/black battery leads with a **red JST-style connector** (visible in AWS 58 and AWS 61, centre-front of the bay), plus dark servo and motor leads. No wire is visible outside the body.

### 2.13 Floor plate (FP) and ballast (BT), AWS 58 version
- A **brass or gold-anodised sheet** (about 0.8–1 mm) forms the floor between the A-frame flanks, running the length of the front bay.
- **White/pale-blue putty** (blu-tack or modelling clay) is pressed onto the floor plate as ballast, about 60 × 30 × 6 mm. This moves the centre of mass forward and down and makes up the mass to near 150 g **(guess)**.
- In AWS 61 a grey/blue putty mass is visible through the bottom-row windows. So the ballast is still present in the V2 build.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 Top view (plan; synthesised)
- The outline is a **rectangle 78 × 92** with a 90 × 14 lip strip across the front. Two wheel rectangles (28 × 12) stick out at the rear corners, from x ±37.5 to ±49.5 and y −50 to −22.
- Inside the outline, the **door trapezoid** (front 74 mm, rear 40 mm wide) is in the middle. The two **flank faces** are the long thin triangles between the door's side edges and the outline's long sides. Each is 0 mm wide at the front corner and about 18 mm wide at the rear. The hinge knuckles form a 42 × 7 strip across the rear end of the door.
- The grille pattern: 5 fanning ribs, 3 cross ribs, small tabs on the side edges.

### 3.2 Front view (AWS 61 ≈ front + 35–45° elevation)
- A **trapezoid** body: bottom width 78, top (hinge) width about 42, height 46. The lip is a wide flat strip across the bottom, wider than the body. The clear PC sheet is a lighter band below it. The wheels' upper halves stick out at the top-left and top-right corners, behind the flanks. The hinge knuckles crown the top.
- The grille shows 6 columns × 4 rows of windows. Through them: the servo (red/white label) at the upper-left, the LiPo (white label) at the right-middle, the red connector at the centre, and grey putty at the bottom.

### 3.3 Right side view (AWS 63 ≈ right + 40° elevation)
- A **right triangle**: hypotenuse = the door (27°), height at the rear = 46, base = 92. A vertical rear wall. The lip carries the hypotenuse down to the floor ahead of the body.
- The flank is the near face, solid orange, with the embossed text and the "5". The rear wheel overlaps the rear-bottom corner, centred about 10 mm in front of the rear wall and at axle height 14.
- The grille ribs show as fins along the top.

### 3.4 Rear view (not photographed; inferred)
- A trapezoid rear wall (78 wide at the bottom, 42 at the top) with the five hinge knuckles on top and both wheels at the bottom corners. Probably a switch slot **(guess)**.

### 3.5 Open-door view (AWS 58)
- The door rotates up about 100° about the hinge, so its front edge points up and slightly back. The body then reads as an **A-frame**: two orange flank frames converging toward the hinge, a floor plate, electronics in the open bay. In the V2 (AWS 61/63) the flanks are solid, so the open view would show solid side walls instead **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | wedge body with leaning flanks | 78 × 92 × 46 | 1 × 1.18 × 0.59 | orange FDM | — | 1 |
| FL | leaning triangular flank | 92 long × 44 tall, lean 22° | 1.18 × 0.56 | orange | integral | 2 |
| RW | trapezoid wall | 78→42 × 44 | 1 → 0.54 | orange | integral | 1 |
| DR | trapezoid grille door | 74→40 wide × 92 along slope × 3–5 | 0.95→0.51 × 1.18 | orange | hinge + servo link | 1 |
| LR | fan rib | 1.8 × 2.5 section | 0.02 | orange | integral with DR | 5 |
| TR | cross rib | 2 × 2.5 section | 0.03 | orange | integral with DR | 3 |
| TB | rib tab | 3 × 2 × 2.5 | 0.04 | orange | integral | 6 |
| HG | knuckle | Ø 7 × 7.6 | 0.09 | orange | on HP | 5 |
| HP | pin | Ø 2.5 × 44 | — | steel | pressed (guess) | 1 |
| LP | strip lip | 90 × 14 × 1.5 | 1.15 × 0.18 | aluminium | bonded/screwed from below (guess) | 1 |
| PC | clear skirt | 90 × 10 × 0.75 | 1.15 × 0.13 | polycarbonate | under LP (guess) | 1 |
| WH | ribbed wheel | Ø 28 × 12 | 0.36 × 0.15 | white tyre, blue hub | motor D-shaft | 2 |
| M | gearmotor | 12 × 10 × 35 | — | metal | printed pocket/strap | 2 |
| SV | servo | ~33 × 15 × 30 (S306x) | — | metal case | screwed to the rear bulkhead (guess) | 1 |
| HN | link | 25 × 4 × 3 | 0.32 | white FDM | 2 pins | 1 |
| BAT | 2S LiPo | 40 × 16 × 10 | — | blue/white wrap | velcro/putty (guess) | 1 |
| FP | floor plate | 70 × 60 × 1 | — | brass (AWS 58) | screws (guess) | 1 |
| BT | ballast putty | 60 × 30 × 6 | — | white/blue putty | pressed | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| DR side edge ↔ FL top edge | closed door rests on the flank tops | 0.5–1 (door must swing) |
| DR front edge ↔ LP rear edge | lip under/at the door's front edge | 0–1 |
| DR knuckles ↔ RW knuckles | interleaved on HP | ~1 axial gap each |
| HP ↔ all knuckles | through | 0 (running fit) |
| LP bottom edge ↔ floor | lowest point | 0.5–1 |
| PC front edge ↔ floor | trailing skirt | 0–0.5 |
| BD bottom ↔ floor | clearance | ~2 |
| WH inner face ↔ FL/RW | outside the body | ~1 |
| WH bottom ↔ floor | contact | 0 |
| WH top ↔ door/hinge | well below the hinge (wheel top z 28 vs hinge 47.5) | n/a |
| SV case ↔ RW inner face | screwed | 0 (guess) |
| HN ↔ DR lug | pinned | 0 |
| BAT ↔ FP/floor | on velcro/putty | 0 |
| BT ↔ FP | pressed | 0 |
| M ↔ BD pocket | captured | 0.2–0.5 (guess) |
| TR tab ↔ FL top edge | tabs overhang the flank | ~1 above |

---

## 6. Mechanism
1. **Drive**: two rear wheels on direct-drive gearmotors. The front of the body rests on the lip edge, so the lip and the polycarbonate skirt are the third contact (a "wedge drag"). Skid steering.
2. **Trap door**: a servo at the rear-left drives a short four-bar (servo horn → white link → door lug) that rotates the door up about the rear-top hinge by about 90–100°. With the door open, the body is an open A-frame scoop. The likely uses are:
   - **Self-righting**: when inverted, the door opens against the floor and levers the robot back over **(medium)**.
   - **Flipping/lifting**: an opponent driven up the lip onto the door is lifted when the door opens. The leverage is poor, because the hinge is at the rear and the load at the front.
   - **Trapping/control**: in the earlier blue-door version the door could close on an opponent's edge.
3. The door frame, ribs and hinge take the opponent's weight when it is driven onto the slope. The fan ribs carry load along the slope straight into the hinge.

---

## 7. Assembly order (suggested rebuild)
1. Print the body BD (flanks, rear wall, floor ring, motor pockets, servo mount, body knuckles 2 and 4). The flanks lean in; print the body upright with the rear wall on the bed **(guess)**, or flat on its base with supports under the hinge.
2. Fit the two gearmotors in their pockets. Press the wheels onto the shafts.
3. Fit the servo to the rear bulkhead and the horn to its spline.
4. Fit the battery (velcro), ESC/RX board and switch. Route the wires along the floor.
5. Press in the ballast putty (optional).
6. Print the door DR (grille, knuckles 1, 3 and 5, a link lug underneath), flat on its outer face.
7. Slide the hinge pin through all 5 knuckles. Pin the white link between the horn and the door lug.
8. Fix the aluminium lip (and PC skirt) to the front of the floor ring.

---

## 8. Hidden / uncertain list
- How the lip is fixed (no visible screws).
- Whether the bottom is open (A-frame with a separate floor plate, as in AWS 58) or a printed floor.
- The exact servo model and horn geometry; the link attachment point on the door.
- Motor type and pocket design; whether there is a rear switch slot.
- Whether the side tabs on the transverse ribs are functional.
- All dimensions ±15%.

---

## 9. Coordinate frame (restated)
- O = the floor point under the body centre. +X right, +Y forward, +Z up, mm. Model z = floor z − 14.
- Body extents (floor z): x ∈ [−39, +39] at the floor, narrowing to [−21, +21] at the hinge height; y ∈ [−46, +46]; z ∈ [2, 46]. Hinge axis (x, y −42, z 47.5). Lip from y 47 to 61, z 3 → 1.

## 10. Profiles as math

**10.1 Door / top face, side profile (YZ, any x inside the door).** A straight line from the front bottom F = (y +46, z 3.5) to the hinge-end top H = (y −36, z 46):
z_top(y) = 46 − (y + 36) · 42.5 / 82 = 46 − 0.518 (y + 36), for y ∈ [−36, +46]. Slope angle 27.4°. Behind H, a flat top from y = −36 to −46 at z 46. Rear wall: y = −46, z from 2 to 46.

**10.2 Flank lean (XZ, any y).** Half-width as a function of floor z:
hw(z) = 39 for z ≤ 10 (vertical skirt), and hw(z) = 39 − 18 · (z − 10)/36 for 10 < z ≤ 46.
At the hinge height hw = 21. The flank plane meets the door plane along the door's side edge:
x_edge(y) = ±[hw(z_top(y)) − f], where f = the frame overlap (~1 mm). At the front (z 3.5) x = ±39; at the hinge x = ±21.

**10.3 Door plan outline (projected on XY).** A trapezoid with vertices (±(hw(3.5) − 1), +46) = (±38, +46) and (±(hw(46) − 1), −36) = (±20, −36). Sides: x = ±[38 − 18 · (46 − y)/82].

**10.4 Grille windows.** Let e(y) = hw(z_top(y)) − 4 be the inner edge of the 4 mm side frame, and the rib width b = 1.8. Column c ∈ {0..5} spans the plan coordinates
x ∈ [−e(y) + c·p(y), −e(y) + c·p(y) + p(y) − b], with p(y) = (2 e(y) + b)/6.
Rows (y ranges in plan, front to back): [26, 39.5], [4, 23], [−16, 1], [−33, −19]. The window corners are rounded at r = 2 (in the door plane).

**10.5 Rib tabs.** At each transverse rib y_t ∈ {24.5, 2.5, −17.5}: a 3 × 2 × 2.5 block from x = ±e(y_t) to ±(e(y_t) + 7), so it ends 3 mm outside the frame.

**10.6 Hinge.** Five cylinders r = 3.4, length 7.6, gap 1.0, centred on (y −42, z 47.5): x centres at −17.2, −8.6, 0, +8.6, +17.2. Pin r = 1.25 (the model uses 1.6), length 44.

**10.7 Lip.** A 90 × 14 × 2 box rotated −12° about X, centred at (0, +54, 3). Lowest edge at z ≈ 0.5 at y ≈ 60.8.

**10.8 Wheel.** Tyre outline r(φ) = 14 − 0.8·[sin(24 φ) < 0] (24 grooves, 0.8 mm deep), width 12. Hub: 5 spokes at 72°, each 2.5 mm wide, from r = 3 to r = 10, with a rim ring r 10–11.

## 11. Pixel-based measurements (independent check)
Coordinates are (x px, y px) from the top-left, read by eye, ±10 px.

**AWS 61 (862 × 940, front, high):**
- Lip (aluminium): x 50–745, y 600–805 (its front edge is lower-left in the image because of the slight rotation). Clear PC: y 760–890.
- Body bottom corners (where the flanks meet the lip): left (95, 600), right (740, 690). The body bottom width is about 650 px along the rotated edge.
- Hinge knuckles: x 350–690, y 15–90, so the top width is about 340 px → ratio top/bottom = 340/650 = **0.52**.
- Grille: front frame at y 560–640; transverse ribs at y ≈ 275, 470 and 540 on the left side (rotated); top row windows y 100–270.
- Wheels: left x 190–270, y 40–205 (165 px tall, the upper part only); right x 770–840, y 120–300.
- Scale at the front edge: 650 px / 78 mm = 8.3 px/mm. At the hinge (farther away): about 340 px / 42 mm = 8.1 px/mm (consistent with a mostly orthographic look).

**AWS 63 (586 × 476, front-right three-quarter):**
- Lip: from (40, 175) to (245, 425) along its front edge.
- Door: the front edge runs along the lip, the hinge edge from (400, 30) to (490, 140).
- Right flank: from the bottom front (250, 420) to the bottom rear (500, 270). The rear wall corner is at (540, 190).
- Right wheel: centre (520, 250), Ø ≈ 95 px (in a frame where the flank bottom length is ≈ 290 px for 92 mm → 3.15 px/mm) → **Ø 30 mm** (near the camera, so slightly inflated).
- Text "SmartAnt 5 V2.x": along (270, 405) → (460, 300), letters about 15 px tall → about 5 mm.

**AWS 58 (664 × 976, behind, door open):**
- Door (blue): from y 90 to 470 px, top width at the free end x 115–610 (495 px), hinge width x 160–420 (260 px) → ratio 0.53. This confirms the trapezoid door narrows toward the hinge in the old version too.
- Orange flanks: an A-frame from the floor corners (45, 890)/(480, 930) up to the hinge ends (160, 470)/(420, 470).
- Servo: x 155–265, y 515–620. Battery: from (330, 590) to (410, 770), diagonal.

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec / class) | Method B (ratio from photo) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body base width | 78 (spec) | — | AWS 61: 650 px / 8.3 px/mm | **78** |
| Body length (no lip) | 92 (spec) | 1.18 W from AWS 63 (flank 290 px vs width ~245 px) = 92 | — | **92** |
| Hinge height | 46 (spec 44 + 2 clearance) | AWS 63: rear wall 0.5 of the length → 46 | AWS 61: perspective; n/a | **46 (axis 47.5)** |
| Door top/bottom width | 21/39 half-widths | AWS 61: 0.52; AWS 58: 0.53 | — | **0.53 → 41.5 / 78** |
| Door slope | 27° (spec) | AWS 63: hypotenuse / base 46/92 → 26.6° | — | **27°** |
| Wheel Ø | 28 (spec) | 0.36 W | AWS 63: 30; AWS 61: 26–28 (partly hidden) | **28** |
| Lip width | 90 | 1.15 W | AWS 61: 695 px / 8.3 = 84 (rotated, far end smaller) | **88–90** |
| Rib width | 2.6 (round-5 model) | — | AWS 61: 10–14 px / 8.3 = 1.2–1.7 | **1.8** |
| Frame width | 4–5 | — | AWS 61 side frame 25–35 px = 3–4 | **4** |

## 13. Consistency check: conflicts and reconciliation
1. **Height/length**: the likeness gate reports the model's height/length at 1.11 against the photo's 1.05 (in the front camera's frame). Possible causes:
   - The hinge and knuckles are too tall. The knuckle tops (z ≈ 51 in the model) add about 4 mm.
   - The lip is too short.
   - The photo camera is lower than 45°.

   AWS 63 gives a rear height of 0.5 of the length (46/92). The spec matches that. **Reconciled**: keep the base height. Lower the knuckles so they stand only ~2 mm above the top face (r 3.0 at z 46.5), and lengthen the visible lip/PC by ~6 mm. Both bring the ratio toward 1.05.
2. **Rib count**: AWS 63 seems to show 5–6 rows, but AWS 61 clearly shows 3 inner transverse ribs (4 rows). In AWS 63 the transverse ribs near the hinge are foreshortened, and the extra "rows" are the thin servo slots. **Reconciled: 4 rows**, plus thin slots in the top row.
3. **Flank solid vs A-frame**: AWS 58 (an older event, blue door) shows open A-frame flanks with a brass floor. AWS 61/63 show solid orange flanks with text. **Reconciled: solid flanks (V2)**; the brass floor may still be there.
4. **Wheel position**: AWS 63 shows the wheel centre about 10 mm ahead of the rear wall, and AWS 61 shows the wheels at the very rear. Both are consistent with y ≈ −36 for a body rear at −46.
5. **Lip angle**: the spec has −12°. AWS 63 suggests a flatter lip, about 8–10°. Keep 12° (combat rule R022: entry ≤ 25°, fine either way).

---

## 14. Why the designer did it (per part, mostly adversarial)

Common lens: what attacks reach the part (vertical spinners, horizontal spinners, wedges, flippers, wall slams, inversion), how the part survives, and how it helps win (getting under the opponent, control, pushing). Then construction reasons: printability, weight, repair.

- **Steep 27° wedge body with the hinge at the top rear**
  - Fight: the whole top face is a ramp. Any opponent that reaches the lip rides up a long, gentle slope and loses its wheel traction, and the robot can push it. A vertical spinner hitting the slope is deflected upward instead of biting a vertical face. The tall rear (46 mm) and the low centre of gravity (battery, motors and ballast on the floor) mean it is hard to flip from the front.
  - Weak points: the rear wall is vertical and tall, an easy target for a wedge from behind. The robot cannot drive inverted: its wheels are below the hinge height, so upside down it rests on the door and hinge. It relies on the door to self-right **(guess)**.
- **Leaning flanks (trapezoid front view)**
  - Fight: side hits from horizontal spinners glance off a sloped face rather than land square. A wedge coming from the side meets a slope, not a wall. The narrow top keeps the mass low.
  - Construction: the lean makes the door narrower, so the door is lighter and stiffer, and the servo needs less torque to lift it. The hinge is short (42 mm), so the pin bends less.
  - The user's point: the door gets **narrower toward the hinge**. This is the main recognisable feature in the front view.
- **Grille door (not a solid plate)**
  - Fight: big windows make the door light (a fast servo can snap it open), and the ribs stay stiff along the slope, which is the load direction when an opponent drives onto it. The windows also let the driver and judges see that the robot is working, and let air cool the motors and servo.
  - Weak points: a horizontal spinner can catch the rib tabs or a window edge. Thin ribs can crack, but they are printed in one piece with the frame, so a crack rarely frees a part.
  - Construction: the fan pattern follows the trapezoid, so every column has the same relative width. It prints flat with no supports, because the ribs stand on the skin.
- **Rib tabs past the frame**
  - Possibly a design detail: band hooks or a stop that keeps the door from falling into the body (the tabs rest on the flank tops when the door closes) **(medium)**. Adversarially they are small snag points, but they are short.
- **Five-knuckle hinge on a steel pin**
  - Fight: five knuckles spread the hinge load over the whole edge, so a hit on one corner of the door does not tear it off. A steel pin does not shear.
  - Construction: the knuckles alternate between the body and the door, so the door is removed by pushing out one pin.
- **Servo with a four-bar link**
  - Fight: the link gives the servo leverage near the end of travel, where the door is most loaded when self-righting. A high-voltage metal-gear servo survives shock.
  - Weak points: the servo is the heaviest single part and a hit on the door feeds straight into the servo gears. The link is a deliberate weak point (a cheap printed part that breaks before the servo).
- **Aluminium lip + clear polycarbonate skirt**
  - Fight: this decides the wedge-vs-wedge battle. A thin, hard, straight edge sits lower than a printed nose can, and the PC sheet extends it further and flexes to follow the floor. The lip is wider than the body, so it protects the front corners and the flank bottoms.
  - Weak points: the lip can bend, and the PC can be cut by spinners. Both are cheap to replace.
- **Two rear wheels, partly hidden**
  - Fight: hiding the wheels behind the flanks and lip protects them from the front. Rear drive with the front on the lip gives the lip constant down-force (it does not lift off the floor when pushing). A white soft tread grips smooth arena floors.
  - Weak points: the wheels stick out at the rear sides, exposed to side and rear spinners. Two wheels means one damaged wheel stops the robot from driving straight.
- **Ballast putty**
  - Fight: puts the mass low and forward to load the lip, and brings the robot up to the 150 g limit for pushing power. It is easy to add or remove at weigh-in.
- **Brass floor plate (AWS 58)**
  - Fight/construction: dense, so it adds low mass, and it is a smooth, hard bottom that slides when the robot is pushed.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, floor z) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × micro metal gearmotor 50:1–100:1 | 12 × 10 × 35 | (±24, −36, 14), shafts along ±X | medium |
| Motor pods | printed blocks round each gearbox, with a strap | 9 × 18 × 19 | (±34.5, −37, 11.5) | medium |
| Motor end stop | printed block between the motor tails | 23 × 10 × 8 | (0, −36, 5) | low |
| Servo | Turnigy S306G-HV (or similar 30 × 15 × 30 class) | 33 × 15 × 30 | (−12, −30, 32), output along X | medium |
| Servo horn + link | aluminium horn + white printed link 25 mm | — | horn at (−5, −30, 38) | medium |
| Battery | 2S 180–300 mAh LiPo | 40 × 16 × 10 | (+12, −10, 8), diagonal | medium |
| ESC/RX | combined 2-channel brushed + servo out | 32 × 19 × 3 | flat on the floor (+10, +13, 4) | low |
| Switch | slide switch through the floor or a rear link | 12 × 4 × 4 | (0, −13, 4) or rear wall | low |
| Floor | printed 3 mm floor ring + brass plate | 74 × 88 × 3 | z 2–5 | low |
| Ballast | putty | 60 × 30 × 6 | (0, +25, 7) | medium |
| Lip fixings | 2–3 M2 countersunk from below into the floor ring | — | y +45 | low |
| Wiring | battery → switch → ESC; ESC → motors along the floor; ESC → servo up the rear-left | — | all below z 20 | medium |

**Wiring path summary (guess)**: battery at the right-middle → switch (floor, centre) → ESC (floor, front-right). The motor leads run rearward along the floor to the motor tails at the centre-rear, and the servo lead goes up the left side to the servo. Everything sits under the door, protected by the grille, with the ballast at the front.

---

## 16. Model status vs this description (round 5 of `spec.json`)
- Matches: trapezoid door narrowing toward the hinge; leaning flanks with a vertical skirt; fanned 6 × 4 grille; 5 knuckles; lip; wheel size and position.
- To fix (driven by this description):
  1. **Rib width 2.6 → 1.8 mm** and frame 4 mm (§10.4). Thin servo slots in the top row (optional).
  2. **Height/length**: lower the knuckles to r 3.0 with their tops ~2 mm over the top face; lengthen the lip/PC (§13.1).
  3. Rib tabs past the frame (§10.5) for the slightly toothed side edge.
  4. Optional: flank text and "5" (decal), blue wheel hubs, white ribbed tyres.

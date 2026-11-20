# Whopper BVM: full rebuild description from the reference photo

Source photo (only one):
- `robots/whopper_bvm/reference/whopper.aws76.webp` (2174 × 1252 px): AWS 76, cut out onto white by the AWS wiki. Camera **in front of the robot, slightly to its right**, about 25–30° down. All the forks point toward the camera (image bottom). The robot's **right** is on the image **left**. Everything is printed in **black/dark grey** filament; the cut-out lighting gives the black a **green cast** (not a real colour). The only non-black parts are the two **bright steel fork strips** and the **translucent grey tyres** at the two ends.

Because there is one photo, the rear, underside and the far side of every part are inferred, and all three-way size estimates (§12) lean on ratios and the AWS limits more than on a second view. Facts read from the photo are stated plainly; inferences are marked **(guess)**. Sizes are **estimates in mm**, from the AWS antweight limit (150 g, 101.6 mm cube) and the earlier spec draft (body 60 × 112 × 26, two inboard wheels r 11, a lifter arm, side fins and outer forks; 2 forks 34 mm). Ratios are against **W = body bar width ≈ 98 mm** (X, end to end of the main bar, excluding the side wedges' flare).

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the main body bar (mid-width, mid-depth).
- **+X** = robot right, **+Y** = forward (toward the forks), **+Z** = up. mm. Side-profile angles from the floor.
- Main bar extents (reconciled §12): x ∈ [−49, +49], y ∈ [−20, +20], z ∈ [2, 24]. Side wedges reach forward to y ≈ +62 at x ≈ ±50. Centre forks reach y ≈ +52; steel forks y ≈ +55.

| ID | Part |
|---|---|
| BB | main body bar (wide, shallow black box spanning the robot) |
| TP-L, TP-R | top surfaces of the left/right halves with engraved "X-truss" recess pattern |
| CH | central channel through the bar (where the arm sits) |
| SL-L, SL-R | long slots in the top beside the channel |
| AR | central lifter arm (grey fuzzy-skin block) |
| AP | arm front plate (dark smooth plate with chevron top edge, Phillips screws) |
| CF-L, CF-R | centre forks (grey textured tines hanging from the arm) |
| CW | dark web/skin between the centre forks |
| FN-L, FN-R | black "shark-fin" tabs flanking the arm's rear |
| SW-L, SW-R | side wedges (long tapered wedges at the outer ends, pointing forward to the floor) |
| HB-L, HB-R | hinge/bracket blocks at the top of the side wedges (curved tab + 2 screws) |
| SF-L, SF-R | steel strip forks (hinged, either side of the centre forks) |
| SK-L, SK-R | black link brackets carrying SF (pivots with screws, sharp screw tips) |
| WH-L, WH-R | drive wheels in pockets at the two ends of the bar |
| SV | lifter servo (hidden) |
| SWT | switch/plug (silver clip visible at the top near the right-end wheel) |
| S-x | screws: black Phillips pan heads, black socket heads, self-tapping tips |
| M-L, M-R, BAT, ESC, RX | hidden motors and electronics |

---

## 1. Overall description in one paragraph

Whopper BVM is a **very wide, shallow, black "T-bar" robot**: its main body is a long transverse bar about 98 mm wide, only about 40 mm deep front-to-back and 22 mm tall, with a **drive wheel buried in a pocket at each end** (the translucent grey knurled tyres just show above the top at the far ends). At each end of the bar a **long tapered side wedge** sweeps forward and down to a point on the floor, like the claws of a crab or the arms of a "U", making the whole robot about 100 mm wide and 80 mm deep. In the middle of the bar, a **grey fuzzy-textured lifter arm** sits in a channel; its front is closed by a **dark smooth plate with a bat-wing (chevron) top edge** and two Phillips screws, and below that **two grey textured tines** run forward and down to the floor with a thin dark skin between them. Either side of the centre tines hangs a **bright steel strip fork** on a small **hinged black link bracket**, free to follow the floor. The top of each half of the bar carries an engraved **X-truss pattern**, black screws, a long slot beside the channel, and small **shark-fin tabs** stick up beside the arm. The robot reads as a five-pronged front (two side wedges, two steel forks, one centre fork pair) on a narrow wheeled bar: a **wide wedge/fork lifter**.

---

## 2. Part-by-part description

### 2.1 Main body bar (BB)
- **Shape**: a long rectangular box, **98 mm wide (X) × 40 mm deep (Y) × 22 mm tall (Z)** (z 2 to 24). The front face is vertical and plain except for screws and the brackets. The top edges have a small chamfer (about 1 mm). The front face of each half has a **horizontal ledge/step** about 6 mm below the top (a lid seam: the top 6 mm is a separate lid or a shelf) **(guess: two-part print with a lid)**.
- **Ends**: each end is an open **wheel pocket** (see 2.9): the end wall is cut away at the top so the tyre shows; the side wedge springs from the outer front corner.
- **Colour/material**: black PLA/PETG with visible horizontal layer lines on the faces and white scuff marks.

### 2.2 Top surfaces (TP-L, TP-R)
- **Shape**: two flat rectangles, each about **34 mm wide × 36 mm deep**, either side of the central channel.
- **Engraving**: each carries an **engraved "X-truss" pattern**: a rectangular groove about 1 mm wide and 0.6 mm deep, about 3 mm in from the edges, with two diagonal grooves crossing inside it. On the robot-left half (image right) the pattern is partly a "Z" (diagonal + horizontal); on the robot-right half (image left) a rectangle with an X. These are **lightening/stiffening recesses** printed into the lid, or cosmetic **(guess)**.
- **Screws**: **black Phillips pan heads** (head Ø about 4 mm, M2) at the corners: visible at the robot-left half's front-outer corner (image (1770, 270)), rear-centre (1495, 215), front edge (1350, 300); and on the robot-right half near the front edge (520, 270) and rear (960, 105).
- **Details**: near the robot-right end, behind the wheel, a **silver metal clip / plug** (about 8 × 6 mm) with a black body (image (830, 70)): the **power switch or link** **(guess, medium)**.

### 2.3 Central channel (CH) and slots (SL-L, SL-R)
- **CH**: a gap through the bar, about **24 mm wide** (x ≈ −12 to +12), running the full depth, in which the lifter arm sits.
- **SL**: a **long narrow slot**, about **4 mm wide × 22 mm long (Y)**, in each top surface just outboard of the channel (image (1000, 200) on the robot-right side and (1390, 140) on the left). Probably clearances for the arm's side cheeks or for servo linkage **(guess)**.

### 2.4 Central lifter arm (AR)
- **Shape**: a **grey printed block** with a **fuzzy-skin (textured) surface**, about **24 mm wide × 40 mm long × 14 mm tall**, lying in the channel with its top about **6–8 mm above the bar top** at the rear and sloping slightly down toward the front. A **small round hole** (Ø 2 mm) and a short groove sit on its top centre (image (1085, 160)). The rear of the arm's top shows a **notch**.
- **Side faces**: the right side face (robot-left, image right of the arm) shows **diagonal ribs** (three parallel 45° ribs about 2 mm wide) on a chamfered upper edge (image (1270, 120–220)).
- **Front**: closed by the front plate AP; below AP the two centre forks continue forward and down.
- **Pivot**: hidden; most likely a **transverse hinge at the rear of the channel** (y ≈ −15, z ≈ 12), driven by a servo inside the bar **(guess, medium)**.

### 2.5 Arm front plate (AP)
- **Shape**: a **dark, smooth flat plate** (it is shinier than the textured arm: a different material, perhaps a printed plate on a smooth bed side, or thin G10), about **36 mm wide × 18 mm tall × 2 mm thick**, standing almost vertical (tilted about 10° back) on the arm's front face. Its **top edge is a bat-wing / chevron**: the outer parts rise to points at the top corners and the middle is a lower straight section, with the transitions as 45° slopes (outline in §10.3). The plate is **wider than the arm** by about 6 mm each side.
- **Screws**: two visible **black Phillips pan heads** (Ø 4 mm) at the lower left and lower right (image (890, 410) and (1115, 375)), plus a third at the arm's upper right (1200, 225) holding the arm top **(guess for any hidden 4th)**.
- **Function**: the front face of the lifter that pushes on opponents, and a stiffening plate that ties the centre fork roots together.

### 2.6 Centre forks (CF-L, CF-R) and web (CW)
- **Shape**: two **grey fuzzy-skin printed tines**, each **10 mm wide × 6 mm tall** at the root, tapering to about **8 × 2 mm** at the tip, running **forward and down at about 25°** from the bottom of AP to the floor, about **34 mm long**. Their centres are at x ≈ ±10 (inner gap about 10 mm).
- **Web CW**: between the tines, at the root, a **thin dark smooth skin** (about 1 mm, the same material as AP) spans the gap over the first 18 mm, with a **concave (curved) front edge** (image (850–960, 560–580)). It makes the root area a scoop.
- **Tips**: cut square, flat on the floor; the right tine (image (860–970, 800–850)) and the left (590–700, 720–750).
- **Connection**: integral with the arm (printed in one piece with AR) **(guess)**, so the whole centre (arm + plate + tines) moves together as the lifter.

### 2.7 Shark-fin tabs (FN-L, FN-R)
- **Shape**: two thin black **curved, pointed tabs**, about **2 mm thick × 12 mm long × 10 mm tall**, rising from the channel walls behind the arm's front corners (image (1100, 50) and (1300, 100)), each with a **concave back edge and a pointed tip** leaning backward, like shark fins.
- **Function (guess)**: printed **limit stops / guides** for the arm (the arm's sides slide against them), or the tops of the arm's hinge cheeks. Their rough tips suggest broken or trimmed print features. Confidence low.

### 2.8 Side wedges (SW-L, SW-R)
- **Shape**: each is a long **tapered wedge prism** springing from the end of the bar and running **forward and down** to a point on the floor. Side profile: a **right triangle** with its vertical back about **22 mm tall** at the bar's front (y = +20), the top face sloping down at about **25°** to a floor tip about **42 mm ahead** (y ≈ +62). Plan: about **16 mm wide at the root**, tapering to about **6 mm at the tip**; the inner face is vertical; the outer face continues the bar's end plane.
  - SW-R (robot right, image left) is seen along its length: a long slim tapered blade with a **sharp tip on the floor at image (60, 590)**, a **line of raised print features** (a groove/ridge) along its top, and white scuffs.
  - SW-L (robot left, image right) is seen nearer face-on: a large **trapezoid-faced block** with **engraved diagonal grooves** on its inner face (an "N"/lightning pattern of grooves, image (1600–1900, 450–950)), a vertical back at the bar end, and the floor tip at the bottom (image (1600–1780, 960)).
- **Hinge brackets (HB-L, HB-R)**: at the top of each wedge root, a black **bracket block** with **2 screws** (one Phillips, one socket head) and a **curved tab** rising from it (robot right: a curved hooked tab at image (520–580, 150–270); robot left: a small post at (1525, 375) with two socket screws below at (1580, 520)). These look like **hinges** or **mount clamps** for the wedges: the wedges may be **hinged** at their tops so they can rise over obstacles and fall back to the floor ("floppy wedges") **(guess, medium)**.
- **Material**: black printed, thick.

### 2.9 Wheels (WH-L, WH-R)
- **Shape**: **Ø 22 mm × 10 mm wide**, with **translucent grey knurled TPU tyres** (fine ribs across the tread, about 30 ribs) on black hubs.
- **Position**: in **pockets at the two ends of the bar**, axes along X, at **x = ±41, y ≈ −4, z = 11**. The tyres stick up about **1–2 mm above the top** (they show at the top of each end: image (560–650, 50–150) on the robot right and (1790–1870, 280–420) on the robot left), and down to the floor.
- **Drive**: each driven by a gearmotor lying along X inside the bar, inboard of its wheel **(guess)**.
- **Wheel pocket**: open at the top and the end; the end wall is cut away so the tyre is visible; the side wedge protects the front of the pocket.

### 2.10 Steel strip forks (SF-L, SF-R) and link brackets (SK-L, SK-R)
- **SF shape**: two **bright steel (or aluminium) strips**, each about **8 mm wide × 1.5 mm thick × 45 mm long**, slightly **curved** (concave up), running forward and down from their brackets to the floor. Each tip is a **squared chisel** with a small step (a worn bevel) at about 8 mm from the end (image (440–500, 690–750) and (1000–1060, 840–920)). The strips lie **flat** (wide face up, 8 mm across X), tilted down toward the floor.
- **Positions**: at x ≈ +22 (robot right, image left of the centre forks) and x ≈ −22 (robot left), i.e. in the gaps between the centre forks and the side wedges.
- **SK shape**: each strip is carried by a small **black printed link bracket** (about **8 mm wide × 30 mm long × 6 mm thick**) hanging from the bar's front face. The bracket has **two or three pivot screws** (black socket/Phillips heads, Ø 4 mm), forming a **two-link chain** (a short upper link from the bar to an intermediate pivot, then a lower link carrying the strip) **(image (600–720, 450–620) on the robot right; (1140–1250, 500–760) on the robot left)**. **Self-tapping screw tips** stick out of the brackets' sides (image (520, 580), (1240, 830)), showing screws driven straight into printed plastic.
- **Function**: **free-hanging hinged forks**: gravity keeps them on the floor; the double pivot lets each fork stay flat on the floor whatever the bar's pitch, and fold up when the robot drives over something **(design reading, medium confidence)**.

---

## 3. Per-view descriptions

### 3.1 Top view (plan, inferred)
- A **"U" or crab shape**: a 98 × 40 bar across the back; from its two ends, long tapered wedges run forward 42 mm to points (overall about 100 wide × 82 deep). In the middle of the bar, the 24 mm channel with the grey arm, and the two centre tines running forward to y ≈ +52. Between the tines and the side wedges, the two steel strips running forward to y ≈ +55.
- On the bar top: two X-truss engraved panels, slots beside the channel, black screws, shark-fin tabs beside the arm, and the wheel tyres just showing at both ends.

### 3.2 Front view (the photo is close to this)
- A long black horizontal bar, 98 wide × 22 tall. At both ends, the side wedges come toward the viewer (seen as triangles narrowing to points at the floor). In the middle, the dark chevron plate and the arm above it, the two grey tines coming down to the floor, and the two silver strips on their link brackets either side.
- The wheels are hidden except for their tops at the ends.

### 3.3 Right side view (inferred)
- A short block (40 deep × 22 tall) with the wheel visible in the end pocket; from its front, the side wedge triangle runs forward to the floor (42 long). Above, the arm and fins stick up about 8 mm. The steel fork and centre tines hang ahead behind the wedge.

### 3.4 Rear view (inferred)
- A plain black wall 98 × 22, with the wheel pockets at the ends and the arm's rear hinge in the middle **(guess)**.

### 3.5 Isometric (as the photo)
- A wide flat bar with claws: two big side wedges, a central fork-lifter with a bat-wing face plate, and two shiny hanging forks.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BB | long box | 98 × 40 × 22 | 1 × 0.41 × 0.22 | black PLA | — | 1 |
| TP | lid panel with X-truss | 34 × 36 × ~3 | 0.35 × 0.37 | black | 3–4 × M2 | 2 |
| CH | channel | 24 wide | 0.24 | — | — | 1 |
| SL | slot | 4 × 22 | — | — | — | 2 |
| AR | arm block | 24 × 40 × 14 | 0.24 × 0.41 × 0.14 | grey fuzzy-skin PLA | hinge (guess) | 1 |
| AP | chevron plate | 36 × 18 × 2 | 0.37 × 0.18 | dark smooth | 2–3 × M2 | 1 |
| CF | tapered tine | 34 × 10→8 × 6→2 | 0.35 | grey fuzzy-skin | integral with AR | 2 |
| CW | web skin | 10 × 18 × 1 | — | dark | integral | 1 |
| FN | curved tab | 12 × 10 × 2 | 0.12 | black | integral | 2 |
| SW | tapered wedge | 42 long × 16→6 wide × 22 tall | 0.43 × 0.16 × 0.22 | black | hinge/bracket (guess) | 2 |
| HB | bracket + tab | 12 × 10 × 12 | — | black | 2 screws | 2 |
| SF | steel strip | 45 × 8 × 1.5 | 0.46 × 0.08 | steel/aluminium | on SK | 2 |
| SK | 2-link bracket | 30 × 8 × 6 | 0.31 | black | 2–3 pivot screws | 2 |
| WH | wheel | Ø 22 × 10 | 0.22 | translucent grey TPU | motor shaft | 2 |
| SWT | switch/clip | 8 × 6 × 5 | — | silver/black | in top | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| BB bottom ↔ floor | clearance | 2 |
| WH bottom ↔ floor | contact | 0 |
| WH top ↔ TP plane | above | +1 to +2 |
| WH faces ↔ pocket walls | clearance | 1–2 |
| SW tips ↔ floor | contact | 0 |
| SW back ↔ BB end/front | hinged or screwed | 0 |
| HB ↔ BB top | screwed | 0 |
| AR sides ↔ CH walls | running clearance | 0.5–1 |
| AR top ↔ TP plane | above | +6 to +8 |
| AP ↔ AR front | screwed | 0 |
| AP edges ↔ BB front face (outboard of the channel) | in front | 1–2 |
| CF tips ↔ floor | contact (arm down) | 0 |
| CF outer faces ↔ SF inner edges | side by side | 4–6 |
| SF tips ↔ floor | contact (gravity) | 0 |
| SF outer edges ↔ SW inner faces | side by side | 10–14 |
| SK ↔ BB front face | pinned | 0 |
| SF ↔ SK lower link | screwed | 0 |
| FN ↔ AR sides | beside | 0.5–1 |
| TP ↔ BB | screwed | 0 |

---

## 6. Mechanism

1. **Drive**: two wheels at the ends of the bar, axes along X, both near y ≈ −4; skid steer. Because the wheels are far apart (track ≈ 82 mm) and the robot is short, it turns quickly; the front is carried by the wedges, tines and strips sliding on the floor.
2. **Lifter**: the centre arm (block + plate + two tines) is hinged at the rear of the channel and raised by a servo inside the bar; the tines get under an opponent and the arm lifts it, tipping it backward over the bar or simply taking its wheels off the floor. With the pivot at y ≈ −15 and the tine tips at y ≈ +52, the lever is about 67 mm; a 30° servo stroke lifts the tips by about 33 mm. The spec draft also calls the robot a lifter.
3. **Passive front**: the side wedges (possibly hinged) and the steel forks (definitely hinged on links) follow the floor, so every part of the 100 mm wide front has an edge on the floor.

---

## 7. Assembly order (suggested rebuild)

1. Print the bar BB with the channel, wheel pockets, motor and servo bays; print the two lids TP with X-truss engraving.
2. Install the two drive gearmotors along X, shafts out into the end pockets; fit the wheels.
3. Install the servo in the centre of the bar under the arm's rear, the battery, ESC, receiver and switch (switch clip near the robot-right end).
4. Print the arm (grey fuzzy-skin) with its tines; screw on the dark chevron plate; fit the hinge pin through the channel walls; link the servo horn to the arm.
5. Screw on the lids.
6. Attach the side wedges with their brackets HB (2 screws each).
7. Build each steel fork assembly: link bracket with 2–3 pivot screws, strip screwed to the lower link; screw the upper link to the bar front at x ≈ ±22.

---

## 8. Hidden / uncertain list
- Arm pivot location and servo; whether the arm is powered at all.
- Whether the side wedges are hinged or fixed.
- Internal layout, rear, underside.
- The exact number of screws on the plate and lids.
- Fin tab function.
- All sizes ±15–20% (one photo).

---

## 9. Coordinate frame (restated)
- Origin under the bar's centre, +X right, +Y forward, +Z up; mm.
- BB: x ∈ [−49, 49], y ∈ [−20, 20], z ∈ [2, 24]. Wheels (±41, −4, 11), Ø 22. Arm hinge (guess) (0, −15, 12). Centre tine tips (±10, +52, 0). Steel fork tips (±22, +55, 0). Side wedge tips (±46, +62, 0).

## 10. Profiles as math

**10.1 Side wedge (YZ at x = ±49 → ±33, tapering).** Triangle (y 20, z 0), (20, 22), (62, 0); top face z = 22 − 0.524·(y − 20) (27.6°). Plan width w(y) = 16 − 10·(y − 20)/42 (outer face fixed at x = ±49, inner face moving outward).

**10.2 Centre tine (YZ at x = ±10).** Root at the bottom of AP (y 22, z 10). Top edge z = 10 − 0.333·(y − 22) for y ∈ [22, 52] (18.4°), giving z = 0 at y = 52; thickness t(y) = 6 − 4·(y − 22)/30 below the top edge (clipped at z ≥ 0). Width 10 → 8.

**10.3 Chevron plate AP (XZ in its own plane, x across, z up, origin at the plate's bottom centre).** Polygon: (−18, 0), (18, 0), (18, 16), (15, 18), (8, 11), (−8, 11), (−15, 18), (−18, 16). Screw holes r 1.1 at (±11, 4).

**10.4 Steel fork (YZ).** Curve from the lower link pivot P0 = (y 26, z 10) to the tip P2 = (55, 0), quadratic Bézier with P1 = (44, 2) (concave up). Strip 8 wide, 1.5 thick; tip bevel step at 8 mm from the end.

**10.5 Two-link bracket.** Upper link: from the bar pivot A = (y 20, z 14) to B = (y 24, z 6), length 9; lower link 12 mm long from B forward to C = (y 34, z 3), the strip screwed to it along B–C. Pivots r 1.5 at A and B.

**10.6 Wheel tread.** r(φ) = 10.5 + 0.5·[sin(30φ) > 0], width 10.

**10.7 X-truss engraving (on each lid, local u across, v along).** Rectangle groove inset 3 mm from a 34 × 36 panel; diagonals from (3, 3) to (31, 33) and (31, 3) to (3, 33); groove 1 wide × 0.6 deep.

## 11. Pixel-based measurements (2174 × 1252 original; coordinates below in the 2000-wide display, × 1.09 for the original)

- Bar front edge: from (470, 300) on the robot right to (1950, 300–420) on the robot left; bar height at the centre front ≈ 80 px (y 300–380).
- Robot-right wedge tip: (60, 590). Robot-left wedge block: x 1580–1950, y 300–960, tip near (1620, 960).
- Centre arm: x 860–1240, y 30–420. Chevron plate: x 845–1180, y 230–440; screws (890, 410), (1115, 375).
- Centre tines: left tip (600–700, 720–750); right tip (870–970, 800–850).
- Steel forks: robot right (430–510, 380–750); robot left (990–1240, 510–920).
- Wheels: robot right (560–650, 50–150); robot left (1790–1870, 280–420).
- Switch clip: (800–870, 50–100).

## 12. Several independent estimates of key sizes

| Quantity | Method A (rules/spec) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Bar width | 112 (spec, too wide) | ≤ 101.6 cube | front edge ≈ 1480 px; plate 36 mm ≈ 335 px → 9.3 px/mm → 159?? (perspective: ends recede) | **98** |
| Bar depth | 60 (spec) | wheel Ø 22 + walls → ≥ 30 | wheel pocket length ≈ 0.4 of the wedge length | **40** |
| Bar height | 26 (spec) | 0.22 W | bar front 80 px / 9.3 px/mm ≈ 9?? (front face partly hidden by the step); with the lid 22 | **22** |
| Wheel Ø | 22 (r 11 spec) | 0.22 W | robot-left tyre 140 px tall at the far end (smaller scale ≈ 6.5 px/mm) → 21 | **22** |
| Centre fork length | 34 (spec) | 0.35 W | tine ≈ 330 px along its length at ~9.5 px/mm → 35 | **34** |
| Side wedge length | — | 0.43 W | robot-right wedge 520 px from bar to tip at a receding angle (~11 px/mm near) → 47 | **42** |
| Steel fork length | — | 0.46 W | 380 px at 9 px/mm → 42 | **45** |
| Plate width | — | 0.37 W | 335 px / 9.3 = 36 | **36** |

## 13. Consistency check: conflicts and reconciliation
1. **Width vs cube**: the spec's 112 mm bar exceeds 101.6 mm. The robot must fit; **reconciled 98 mm bar**, with the side wedges inside that width (their outer faces flush with the bar ends).
2. **Depth**: the spec's 60 mm is plausible for the full footprint minus wedges; the photo shows the bar is shallow (the wheel pockets are hardly longer than the wheels). **Reconciled bar 40 deep; total with wedges 82.**
3. **Pixel scale**: the photo is strongly perspective (the robot-left end is much nearer to the camera than the robot-right end), so pixel widths across the bar are unreliable; lengths were measured near the centre (plate scale 9.3 px/mm) and ratios used elsewhere.
4. **Lifter powered**: no servo is visible, but the arm is a separate grey part sitting in a channel with clearances (slots, fins), and the spec says lifter. **Reconciled: powered lifter, medium confidence.**
5. **Side wedges hinged**: the brackets at their roots have curved tabs that look like hinge knuckles; but the wedges could also be fixed. **Reconciled: model a hinge at the top root with a small range (0–20°).**

---

## 14. Why the designer did it (per part, adversarial first)

- **Wide, shallow bar with wheels at the ends**
  - Fight: a wide front means **opponents cannot get round** the forks easily, and a spinner hitting the front meets forks and wedges, not the body. A shallow bar keeps the robot short so it turns quickly and the centre of mass is close to the wheels. Wheels buried in end pockets are protected on three sides; only their tops and outer ends show.
  - Threats: a horizontal spinner can hit the bar ends (wheel pockets); the side wedges sit in front of them. From behind, the bar is a plain wall: being hit from the rear is the weakness, and the robot depends on turning fast to face opponents.
- **Side wedges ("claws")**
  - Fight: they extend the front edge to the full width and protect the wheel pockets. Their sloped tops deflect a vertical spinner's hit upward; their points get under opponents trying to go round the centre. If hinged, they follow the floor and cannot be used as a lever to lift Whopper itself.
  - Being got under: their tips on the floor reach 42 mm ahead, so an enemy wedge meets them first.
- **Centre fork-lifter**
  - Fight: forks beat wedges at getting under; once under, the arm lifts the opponent, removing its traction so Whopper can push it anywhere (toward the pit or walls). The chevron plate gives a broad flat face to push against and stops opponents sliding over the arm into the body.
  - Survival: the fuzzy-skin texture hides scuffs and slightly improves impact toughness of the surface; the tines are thick at the root and thin at the tip.
- **Hinged steel strip forks**
  - Fight: metal tips are thinner and harder than printed ones, so they get lower. The double-pivot link keeps them on the floor even when the robot pitches or the floor is uneven, closing the gaps between the centre fork and the side wedges. They fold up harmlessly if driven over.
  - Threat: links held by self-tapping screws in plastic can pull out; cheap to replace.
- **Shark-fin tabs and slots**
  - Construction: guide the arm and keep debris out of the channel **(guess)**.
- **X-truss engraved lids**
  - Construction: lighter lids with stiffening ribs, plus a visual identity; screws at the corners for quick access.
- **Switch near the end**
  - Rules: the power switch must be accessible; placing it at the top near the end keeps it away from the centre arm.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors along X | 12 × 10 × 25 | x ±24, y −4, z 11, shafts to the end wheels | medium |
| Lifter servo | 9 g micro servo (metal gear) | 23 × 12 × 23 | x 0, y −8, z 13 under the arm's rear; output along X | medium |
| Arm hinge | 2–3 mm steel pin through the channel walls | Ø 2.5 × 26 | (0, −15, 12) | low |
| Battery | 2S 300 mAh LiPo | 45 × 18 × 10 | in one half of the bar, x +28, y 0, z 8 | medium |
| ESC | dual brushed ESC | 25 × 15 × 5 | other half, x −28, y 0, z 7 | medium |
| Receiver | micro receiver | 20 × 12 × 5 | x −28, y −10, z 14 | low |
| Switch | the silver clip at the robot-right end top | 8 × 6 × 5 | (+30, −14, 24) | medium |
| Wedge hinges | screw pivots in HB | M2 | at the wedge roots (±44, +20, 20) | low |
| Wiring | battery → switch → ESC → motors along the bar; servo lead to the centre | — | — | medium |

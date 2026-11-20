# Stack Overflow: full rebuild description from reference photos

Source photos:
- `robots/stack_overflow/reference/stack_overflow.aws67.webp`: AWS 67, 1172 × 972 px, background removed. **Front view from about 25–30° above**, robot square to the camera with a slight turn to its left. The **large faceted aluminium wedge** fills the lower 60% of the frame; the **grey-blue lifter arm** with a **black-wrapped finger** lies across its right half; the **clear polycarbonate box** with visible wiring is behind; two **black treaded wheels** show at the rear corners; **green FR4 side plates** show at the far left and right edges. This is the likeness photo.
- `robots/stack_overflow/reference/stack_overflow.aws66.webp`: AWS 66, 730 × 612 px, on a pale yellow table. **Rear-left three-quarter view from about 50° above**, robot facing the **upper right**. Shows the **aluminium rear plate with engraved text**, both wheels outboard at the rear corners, the inside of the clear box with its **grey printed corner blocks**, the **large grey printed lifter gear** across the middle, the **green receiver/ESC board**, a **white JST plug**, a **black switch** and the wedge with its row of screws. A white numbered event tag "S2" sits at the lower right (not part of the robot).
- `robots/stack_overflow/reference/stack_overflow.aws65.webp`: AWS 65, **150 × 103 px only** (tiny thumbnail). Left side view, robot facing the **image left**, on a wooden table. Gives the side silhouette: long triangular wedge in front, arm lying along the wedge top, box behind, wheels at the rear sticking up above the box. Too small for detail; used only for proportions.

Stack Overflow is a **two-wheel lifter/wedge**: a clear box on two outboard rear wheels, a full-width **folded aluminium wedge** at the front, and a **single narrow printed arm** pivoted on top of the box and driven by a **printed spur-gear train**. The arm lies on the wedge and lifts whatever has slid up it. Everything stated as fact is read from the photos; anything inferred is marked **(guess)**. All mm values are **estimates** (±15%), scaled from the 101.6 mm (4 in) AWS cube, from the Ø 32 mm wheel class (N20 rubber wheels) and from pixel ratios. Ratios are given against **W = box width between the clear side walls ≈ 76 mm**. This file replaces an earlier short description of this robot.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the wedge tip), **+Z** = up. Units mm. **Origin** = the point on the floor (z = 0) under the **centre of the clear box** (mid-width between the side walls, mid-length of the box). Side-profile angles are measured from the floor (slope) unless stated; plan angles from +Y toward +X.
- **Front** = the wedge end. In AWS67 the front faces the camera; in AWS66 the front points to the upper right and the robot's **left side and rear** face the camera; in AWS65 the front points to the image left and the robot's **left side** faces the camera.

| ID | Part |
|---|---|
| BX | clear polycarbonate box (floor, side walls, front wall, upper lids) |
| BX-LD-L / BX-LD-R | clear upper lid plates either side of the gear/arm area |
| BX-CB | grey-blue printed corner blocks inside the box corners |
| RP | aluminium rear plate (engraved text) |
| SP-L / SP-R | green FR4 side plates (AWS67) |
| WG | folded aluminium wedge: centre face WG-C, left facet WG-L, right facet WG-R, top flange WG-F |
| AR | lifter arm: hub plate AR-H, flat finger AR-F, black wrap AR-T |
| GA | large printed arm gear on the arm shaft |
| GP | pinion / intermediate gear |
| SH | arm shaft (along X) |
| GB | printed gearbox brackets/bearing blocks (grey-blue) |
| AM | arm (lifter) motor (gold/brass gearbox can) |
| ST | black ribbed rubber block behind the arm hub (arm stop or bumper, guess) |
| WH-L / WH-R | drive wheels (black treaded rubber on grey hubs) |
| DM-L / DM-R | drive motors (hidden, guess N20) |
| RX | green receiver/ESC board |
| JST | white JST connector |
| SW | black power switch |
| W | wires: red, yellow, blue, green |
| TG | lilac square tag on the wedge flange; white block right of the arm root |
| S-xx | screws (listed per part) |
| BAT | battery (hidden, guess) |

---

## 1. Overall description in one paragraph

Stack Overflow is a **low, see-through, two-wheeled lifter** about **98 mm wide, 100 mm long and 34 mm tall** (38 at the arm hub). Its body is a **clear polycarbonate box** about 76 mm wide, 60 mm long and 28 mm tall, assembled with **grey-blue printed corner blocks** and many **silver Phillips pan-head screws**. The **rear wall is an aluminium plate** with engraved text. Two **black treaded rubber wheels** (about Ø 32) sit **outside the box at the two rear corners**, their tops a little above the box. Bolted to the front is a **brushed aluminium wedge** of about 1 mm sheet, folded into a **blunt chevron**: a **central trapezoid face** that slopes down at about 30–35° to a straight floor edge, and **two triangular side facets** folded back toward the box corners, so the wedge is wider than the box. On top, a **single grey-blue printed arm** about 12 mm wide rises from a **hub on a cross shaft** at the box's top. It runs forward and **bends down to lie on the wedge's centre-right**, with its outer half **wrapped in black tape/heat-shrink**. A **large printed spur gear** on the arm shaft, driven by a **small geared motor** through a pinion, turns the arm up. Inside the box, the wiring (red, yellow, blue, green), a **green receiver/ESC board**, a **white JST plug** and a **black switch** are all visible. In AWS67 **green FR4 plates** cover the sides.

---

## 2. Part-by-part description

### 2.1 Clear box (BX)
- **Shape**: a rectangular box about **76 mm wide (X) × 60 mm long (Y) × 28 mm tall**, floor at z ≈ 3 (ground clearance 3 mm), top at z ≈ 31. Wall sheets about **2 mm** thick, **clear polycarbonate** (scratched, with bright edge reflections). The vertical box edges are sharp; panels butt at the corners.
- **Floor**: clear (AWS66 shows the yellow table through it) **(medium)**.
- **Front wall**: clear, about 76 × 25 mm, behind the wedge's top flange; in AWS67 its top edge is visible above the wedge at the left (with screws) and right.
- **Side walls**: clear, about 60 × 28 mm, with the drive motor shafts passing through near the rear **(guess)**.
- **Upper lid plates (BX-LD)**: the top is **not one flat lid**. AWS67 shows **two raised clear plates** on the left and right rear quarters (about **28 × 24 mm** each, at z ≈ 31, with a step down of about 5 mm toward the centre). Further forward, left and right of the arm root, it shows **lower clear panels** (z ≈ 26), each with a screw at its corners. The centre strip (about 22 mm wide) is open for the gear and arm. AWS66 shows similar clear plates over the left-rear and right-rear corners, each about 22 × 20 mm, carrying a corner screw. **(Read: the top is stepped and partly open.)**
- **Corner blocks (BX-CB)**: grey-blue printed **square posts** about **8 × 8 × 26 mm** in each inside corner, screwed through both adjacent walls (one screw per wall, M2 pan). AWS66 shows **at least six**: four box corners plus two mid-side posts near the gear (holding the gearbox brackets).
- **Screws (S-BX)**: silver **Phillips pan head M2–M2.5**, head Ø about 4–5 mm; roughly **2 per corner per wall**. AWS67 shows about 10: left wall front, three in a vertical line at z ≈ 7, 15, 23; right wall, four; upper lids, four.

### 2.2 Aluminium rear plate (RP)
- **Shape**: a flat **brushed aluminium sheet about 1–1.5 mm thick, about 80 × 26 mm**, forming the rear wall (or covering a clear rear wall), at y = −30. It runs between the inner faces of the two wheels.
- **Detail**: **engraved/scribed text** across its middle (two lines, illegible in AWS66, possibly the robot name or team). **Six screws**: three near each end (top, middle, bottom), into the corner blocks. The left end has a small notch/step at the top.

### 2.3 Green side plates (SP-L, SP-R) (AWS67 only)
- **Shape**: flat **green FR4 sheets** (PCB laminate, glossy dark green with a lighter edge), about **1.6 mm** thick, about **60 mm long × 26 mm tall**, mounted outside the clear side walls. The left one in AWS67 shows a silver screw near its front-middle and a chamfered front-top corner. The right one shows at the far right edge.
- **Position**: x = ±40, y from −28 to +28, z from 3 to 29. The wheels are outboard of them at the rear; their front parts extend alongside the wedge's side facets.
- **Absent in AWS66** (only the clear sides are seen there), so they are a **later addition** (stiffening or armour).

### 2.4 Wedge (WG)
- **Material**: **brushed aluminium sheet about 1 mm thick**, scratched, with a white-grey sheen. **Three facets folded from one sheet**, plus a **top flange**:
  - **Top flange WG-F**: a strip about **8 mm** wide bent up against the box front wall, across the full box width (x −38 … +38), screwed to the box with **4–5 screws** (AWS66 shows a row of about 5 screws along the flange, at x ≈ −28, −14, 0, +14, +28). A **lilac square tag** (about 10 × 10 mm, a paper or plastic label) sits on the left part of the flange in AWS67 at about x = −15.
  - **Centre face WG-C**: a **trapezoid**, about **60 mm wide at the top** (at the box front, z ≈ 26) widening to about **72 mm at the floor edge**. It slopes down at about **30–35°** from the box front (y = +30) to the floor edge at about **y = +68**. Three **silver Phillips pan screws** run in a nearly vertical line down its centre (in AWS67 at about 20%, 50% and 80% of the slope length, x ≈ +4). These hold the face to an inner printed support **(guess)**.
  - **Side facets WG-L, WG-R**: **triangles** folded back from the centre face's side edges toward the box front corners, each about **30 mm** along the floor edge and **40 mm** along the fold, sloping at about **45°** sideways-down. In plan, the floor edge is a **blunt chevron**: a straight centre edge plus two angled edges sweeping back to the box corners. In AWS66 the left facet ends in a **sharp point** at the upper left of the wedge and the right facet in a point at the right. The wedge's floor outline is therefore **wider than the box**: about **96 mm** at the widest point (x ±48) at about y = +40.
  - **Side-facet screws**: AWS67 shows two screws on the left box edge where the left facet meets the box (at z ≈ 10 and 18) and two on the right.
- **Tip**: the floor edge is straight and sharp (sheet edge), touching the floor. AWS67 shows a small **scratch gouge** on the centre face (a light diagonal scar) and an irregular dent at the lower left.

### 2.5 Lifter arm (AR)
- **Hub plate AR-H**: a grey-blue printed flat plate about **12 mm wide × 5 mm thick × 25 mm long**, lying on top of the gear hub at about **z = 33–38**, running forward from the shaft. **Three silver Phillips pan screws (M2)** in a straight row along its centreline, 6 mm apart, fasten it to the gear/hub block.
- **Bend**: at about y = +15 the arm **bends down** by about **34°** with a smooth radius (about R 8) and continues as the finger.
- **Finger AR-F**: a straight flat bar **12 mm wide × 5 mm thick × about 55 mm long**, lying **on (about 0.5–1 mm above) the wedge centre face**, slightly **right of centre**. Its centreline is at x ≈ +4 at the bend and x ≈ +12 at the tip, so the arm runs about 10° to the right in plan. Its **square tip** ends about **6–8 mm short of the wedge floor edge**.
- **Black wrap AR-T**: the outer **60%** (about 35 mm) of the finger is wrapped in **black electrical tape or heat-shrink**, slightly thicker than the plastic (the bare grey tip end shows below the wrap in AWS67). In AWS66 the black part looks like a separate **black rubber/plastic sleeve** extending past the grey part.
- **Material**: grey-blue PLA/PETG (bluish slate grey), print lines along its length.

### 2.6 Gear train (GA, GP), shaft (SH) and gearbox (GB)
- **Arm gear GA**: a **large printed spur gear** in grey-blue, about **Ø 24–26 mm × 10–12 mm wide**, with **coarse teeth** (about 12–14 teeth, module about 1.8–2), on the **arm shaft SH along X** at about **(0, −2, 22)**. The arm hub plate sits on a block on top of this gear's hub. In AWS66 the gear is the most prominent part in the middle of the box: its teeth face upward/backward and mesh with a smaller gear.
- **Pinion/idler GP**: a **smaller printed gear** about **Ø 12 × 10 mm** behind or below GA, partly hidden, driven by the arm motor **(seen partly in AWS66, medium)**.
- **Gearbox brackets GB**: **grey-blue printed bearing blocks** either side of the gear. In AWS67: a **cylindrical boss** (Ø 12 × 12) on the left of the arm hub with a hole along X (the left shaft bearing); a **block with a screw** under it at about (−12, +8, 20); and a **curved bracket** on the right behind the arm (Ø 12 boss). In AWS66: a **grey cylinder** (Ø 12 × 18) on the left of the gear (the motor clamp) and another grey block on the right.
- **Shaft SH**: steel, about **Ø 3 × 40 mm**, through the bosses and gear **(guess)**.
- **Black ribbed block ST**: in AWS67 a **black rubber/foam block with vertical ribs** (about 14 × 10 × 12 mm) sits at the top centre **behind** the arm hub at about (+2, −12, 32). It looks like a piece of tyre or a ribbed rubber bumper. Most likely it is the **arm's rear stop**, which stops the arm rotating too far back **(guess, low)**.

### 2.7 Arm motor (AM)
- **Seen**: a **gold/brass-coloured cylindrical can** inside the left half of the box in AWS67, just inboard of the left wheel at about (−24, −15, 15). This is a **gearmotor's brass gearbox** (an N20 has a brass-coloured gearbox) **(guess, medium: it could also be the left drive motor)**. In AWS66 the left grey cylinder holds a motor along X.
- **Size**: N20 class, **12 × 10 × 25 mm** plus a 9 mm shaft.

### 2.8 Wheels (WH-L, WH-R)
- **Position**: outside the box at the **two rear corners**, axles along X at about **y = −16**, wheel centre planes at **x = ±44**, axle height z ≈ 16.
- **Size**: about **Ø 32 × 10 mm**. **Black rubber tyre with fine straight cross-tread** (about 40 ribs around), on a **grey/black plastic hub** (AWS66 shows a grey hub and a small centre boss on the outer face).
- **Height**: tops at z ≈ 32, about 1–3 mm above the box's top lids; bottoms on the floor. AWS65 confirms the wheels stand above the box at the rear. The arm hub (z ≈ 38) sticks above the wheels, so **inverted running is doubtful** unless the arm is used to self-right **(guess)**.

### 2.9 Electronics, switch and wires
- **RX**: a **green PCB** with components, about **30 × 20 mm**, inside the box at the **right rear**, lying flat or slightly tilted at about (+18, −14, 8) (AWS66, under the right-rear lid; AWS67 shows a green-board edge and red components at the right).
- **JST**: a **white 2–3 pin JST connector** at the **left rear** top of the box at about (−18, −24, 24) in AWS66 (white plug with red/black leads), and a white connector housing at the right in AWS67 (about (+34, +5, 15)).
- **SW**: a **black slide switch or link** at the **left rear corner** at about (−30, −26, 22) in AWS66 (a dark rectangle against the clear wall), reachable from outside **(medium)**.
- **Wires W**: in AWS67, a loom on the left: **two yellow, one blue, one red, one green** wires looping from the left rear to the centre front (to the arm motor and RX). In AWS66: **red** and **yellow/blue** loops at the right rear and red at the left rear.
- **White block TG**: a white rectangular block (about 10 × 8 × 8 mm) to the right of the arm root at about (+14, +22, 28), possibly a **foam pad/arm rest** or a cable-tie mount **(guess)**.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 AWS67 (front, about 25–30° down)
- **Outline**: a wide flat **hexagon**. The wedge's chevron floor edge is at the bottom (centre edge nearly horizontal across the image, side edges angled up to the box corners); the box sides are vertical on the left and right; the box/wheel top is a straight upper edge with the two wheel bumps at the top corners.
- **Wedge**: the lower 60%, bright aluminium, with the centre face (lit from the left) and two side facets; three screws down the middle.
- **Arm**: a dark grey-blue strip from the top centre down to the lower right; outer 60% black.
- **Box**: clear, with wires, gears and lids behind.
- **Green plates** at the far left and right edges.

### 3.2 AWS66 (rear-left, about 50° down)
- The aluminium rear plate runs diagonally across the lower left, a wheel at each end. The clear box looks open, with corner posts. The large grey gear is in the middle, with the arm going up-right to the wedge. The wedge is a large grey sheet at the upper right with pointed side corners and a row of screws.

### 3.3 AWS65 (left side, tiny)
- A long, low silhouette: the wedge triangle on the left (slope about 30°, height about 0.75 of the box height); the arm a dark line along the top of the wedge, rising and flattening over the box; the box rectangle behind; and two wheels at the rear right (the near one lower, the far one higher in the image), wheel tops above the box.

### 3.4 Top view (synthesised)
- Box 76 × 60 in the middle; wheels as 10 × 32 rectangles outside the rear corners; the wedge in front, a chevron reaching y = +68 at the centre and spreading to x = ±48 at y = +40; the arm a 12-wide strip from (0, −5) to (+12, +61).

### 3.5 Rear view (inferred)
- The aluminium rear plate 80 × 26 between two wheel discs Ø 32; the arm hub just visible above.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W (76) | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BX | box | 76 × 60 × 28, 2 wall | 1 × 0.79 × 0.37 | clear PC | corner blocks + M2 | 1 |
| BX-LD | lid plates | 28 × 24 × 2 | 0.37 × 0.32 | clear PC | 2–4 × M2 each | 2–4 |
| BX-CB | post | 8 × 8 × 26 | 0.11 | grey-blue PLA | M2 through walls | 6 |
| RP | plate | 80 × 26 × 1.2 | 1.05 × 0.34 | aluminium, engraved | 6 × M2 | 1 |
| SP | plate | 60 × 26 × 1.6 | 0.79 × 0.34 | green FR4 | 2–3 screws | 2 (AWS67) |
| WG-C | trapezoid | 60→72 wide × 45 slope | 0.8–0.95 | aluminium 1 mm | 3 screws | 1 |
| WG-L/R | triangle facets | 30 × 40 | 0.4 × 0.53 | aluminium | folded, 2 screws | 2 |
| WG-F | flange | 76 × 8 | 1 × 0.1 | aluminium | 4–5 screws | 1 |
| AR-H | flat plate | 25 × 12 × 5 | 0.33 × 0.16 | grey-blue PLA | 3 × M2 | 1 |
| AR-F | flat bar | 55 × 12 × 5 | 0.72 × 0.16 | grey-blue + black wrap | integral | 1 |
| GA | spur gear | Ø 25 × 11, ~13 teeth | 0.33 | grey-blue PLA | on SH | 1 |
| GP | spur gear | Ø 12 × 10 | 0.16 | grey-blue | on AM shaft | 1 |
| SH | rod | Ø 3 × 40 | 0.53 | steel | bosses | 1 |
| GB | bearing blocks | Ø 12 × 12 bosses | — | grey-blue | to box | 2–3 |
| ST | ribbed block | 14 × 10 × 12 | — | black rubber | glued (guess) | 1 |
| AM | gearmotor | 12 × 10 × 25 | — | brass/silver | printed clamp | 1 |
| WH | wheel | Ø 32 × 10 | 0.42 × 0.13 | black rubber, grey hub | motor shaft | 2 |
| RX | PCB | 30 × 20 × 5 | — | green | tape | 1 |
| JST | plug | 8 × 6 × 5 | — | white | — | 1–2 |
| SW | switch | 12 × 6 × 6 | — | black | in wall | 1 |
| S | pan Phillips | M2–M2.5, head Ø 4–5 | — | silver | — | ~30 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| BX walls ↔ BX-CB | screwed | 0 |
| BX-LD ↔ BX-CB tops | screwed | 0 |
| RP ↔ BX rear / BX-CB | screwed | 0 |
| SP ↔ BX side walls | screwed, flat on | 0 |
| WG-F ↔ BX front wall | screwed | 0 |
| WG-C floor edge ↔ floor | touching | 0–0.5 |
| WG-L/R rear edges ↔ BX front corners | screwed/meeting | 0 |
| WG-L/R ↔ WH-L/R | far apart (wheels at the rear) | ~30 in Y |
| AR-F bottom ↔ WG-C top | resting above | 0.5–1 |
| AR-F tip ↔ WG floor edge | short of it | 6–8 |
| AR-H ↔ GA hub | screwed (3 × M2) | 0 |
| GA ↔ SH | fixed | 0 |
| GA ↔ GP | meshing | 0 (backlash ~0.3) |
| GP ↔ AM shaft | fixed | 0 |
| SH ↔ GB bosses | bearing fit | 0.1 |
| ST ↔ AR-H rear | stop face | 0–2 |
| WH inner face ↔ BX side wall / SP | side by side | 1.5–2 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ BX-LD top | wheel above | +1–3 |
| AR-H top ↔ WH top | arm above | +4–6 |
| BX floor ↔ ground | clearance | 2–3 |

---

## 6. Mechanism

1. **Drive**: two-wheel differential drive with the wheels at the rear. The **wedge's floor edge is the front skid**, so the robot rests on the two wheels and the wedge tip. This keeps the wedge edge pressed to the floor, which is good for getting under opponents.
2. **Lifter**: the arm motor turns the pinion GP, which turns the large gear GA and the arm shaft SH. The printed stage gives about **2:1** reduction on top of the gearmotor's own. The arm swings about SH from rest (finger on the wedge, about 13° below the shaft's horizontal) up to about **+60°**. The finger tip, about 64 mm from SH, rises by about **50–70 mm**. This lifts an opponent that has slid up the wedge and pushes it over backward, or **self-rights** the robot if it is inverted (the arm swings past vertical and pushes off the floor) **(guess, medium)**.
3. **Wedge**: passive. The chevron facets steer opponents toward the centre face and the arm.

---

## 7. Assembly order (suggested rebuild)

1. Cut the clear PC panels (floor, front, sides, lids) and the aluminium rear plate.
2. Print the grey-blue corner blocks, gearbox bosses, gears and arm.
3. Screw the floor, sides and front to the corner blocks; screw the rear plate on.
4. Fit the two drive motors at the rear, shafts out through the side walls; fit the wheels.
5. Fit the arm motor in its clamp, then the pinion. Fit the shaft SH through the bosses with GA on it.
6. Screw the arm hub plate to GA's hub with 3 × M2.
7. Fit the electronics (RX/ESC board, battery), the switch and the JST plug; route the wires.
8. Fold the wedge from one sheet. Screw its flange to the box front, its side facets to the box corners, and the centre face (3 screws).
9. Fit the clear lid plates and the green side plates (AWS67 version); wrap the finger with tape.

---

## 8. Hidden / uncertain list
- Gear tooth counts and exact reduction.
- Whether the arm is a self-righter as well as a lifter.
- What the black ribbed block ST is.
- Battery position.
- Underside (wedge support behind the centre face).
- All mm ±15%. AWS65 is too small for anything but proportions.

---

## 9. Coordinate frame (restated)
- Origin on the floor under the centre of the clear box; +X right, +Y forward, +Z up; mm.
- Box x ∈ [−38, +38], y ∈ [−30, +30], z ∈ [3, 31]. Wheels x ∈ [−49, −39] and [+39, +49], axis y = −16, z = 16. Wedge y ∈ [+30, +68], floor edge at the centre y = +68, side points (±48, +40). Arm shaft at (0, −2, 22); arm hub top z ≈ 38.
- Overall bounding box: **98 × 100 × 38** mm (fits the 101.6 cube).

## 10. Profiles as math (for rebuilding curves)

**10.1 Wedge centre face (YZ section at x = 0).** Line from (y +30, z 26) to (y +68, z 0): slope atan(26/38) = **34°**. Equation: z = 26 − 0.684 (y − 30), for 30 ≤ y ≤ 68.

**10.2 Wedge floor edge (XY plane, z = 0).** Polyline: (−48, +40) → (−36, +68) → (+36, +68) → (+48, +40). The side facets' rear edges run from (±48, +40, 0) up to the box front corners (±38, +30, 26). Each side facet is the plane through (±36, +68, 0), (±48, +40, 0) and (±38, +30, 26).

**10.3 Wedge flange.** Vertical strip y = +30.5, x ∈ [−38, +38], z ∈ [18, 26].

**10.4 Arm side profile (YZ plane, arm centreline, top edge).** Piecewise:
- Hub plate: z = 38 for −10 ≤ y ≤ +15.
- Bend: arc of radius 8, turning 34° down, from (y +15, z 38) to about (y +19.5, z 36.8).
- Finger: line of slope −34° parallel to the wedge face, 5.5 mm above it (5 mm thickness + 0.5 gap): z = 31.5 − 0.684 (y − 30), for y from ≈ +20 to +61 (tip).
In plan the finger centreline runs from (+4, +18) to (+12, +61): **10° to the right of +Y**.

**10.5 Arm sweep.** Tip radius from SH: √((61 − (−2))² + (8 − 22)²) ≈ 64 mm. Tip path: y = −2 + 64 cos θ, z = 22 + 64 sin θ, θ from −13° (rest, on the wedge) to about +60°.

**10.6 Gears.** GA pitch circle r = 12.5 at (y −2, z 22). GP pitch circle r = 6, assumed **behind** GA at about (y −20.5, z 22), centre distance 18.5.

**10.7 Wheels.** (y + 16)² + (z − 16)² = 16² at x = ±44.

## 11. Pixel-based measurements (independent check)

- **AWS67** (1172 px): wedge floor-edge span from the lower-left corner (230, 690) to the right (1110, 520) ≈ **900 px**. Arm top face width near the tip ≈ **75 px**; with the shadowed side face ≈ **95 px**. Screw head ≈ **30 px**. Scaling by the arm (12 mm per 75 px) gives 900/75 × 12 ≈ **144 mm**, and by a 4 mm screw head 900/30 × 4 ≈ **120 mm**. Both are impossible for a 101.6 mm robot; see §13.1.
- **AWS66** (730 px): rear plate from the top-left wheel's inner face (110, 235) to the bottom wheel's inner face (330, 520) ≈ **360 px**; near wheel diameter ≈ **125 px** (bottom wheel). 360/125 × 32 = **92 mm**. The bottom wheel is nearest the camera, so the plate is under-scaled by this: **80–92 mm**.
- **AWS66** right side wall from the rear (420, 540) to the front (640, 350) ≈ **290 px** → 290/125 × 32 = **74 mm**. It runs away from the camera and is farther than the reference wheel, so the true length is shorter: **60–75 mm**.
- **AWS66** gear GA ≈ **85 px** across → 85/125 × 32 = **22 mm** (farther than the wheel, so a little larger in reality).
- **AWS65** (150 px): total length ≈ **122 px**, near wheel ≈ **28 px** → 122/28 × 32 = **139 mm**, too long (blur spreads the outline). Ratios are more useful: wedge ≈ 0.42 of the length; box height ≈ 0.22 of the length; wheel ≈ 0.23–0.3 of the length.

## 12. Several independent estimates of key sizes

| Quantity | Method A (rules / parts) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width | ≤ 101.6 | box 76 + 2 × 12 = 100 | AWS67 wedge ≈ 96 at the facet points (ratio to box) | **98** |
| Overall length | ≤ 101.6 | box 60 + wedge 38 | AWS65: wedge 0.42 L → L ≈ 98 if the wedge is 41 | **100** |
| Box width | — | 1 W | AWS66 80–92 (incl. wall/plate) | **76** |
| Box length | — | 0.79 W | AWS66 60–75 | **60** |
| Box height | > wheel radius | 0.37 W | AWS65 0.22 × 98 = 22 + clearance + lids | **28** |
| Wheel Ø | N20 rubber wheels Ø 32/34 | 0.42 W | AWS65 0.23–0.3 × 98 = 23–29 (blurred) | **32** |
| Wedge slope | 30–35° typical | — | AWS65 ≈ 30°; AWS67 face proportions → 34° | **34°** |
| Arm width | printed bar 10–14 | 0.16 W | AWS67 75/900 × 96 = 8 (top face); 95/900 × 96 = 10 | **12** |
| Gear Ø | 20–26 | — | AWS66 22+ | **25** |

## 13. Consistency check: conflicts and reconciliation
1. **AWS67 absolute scale**: screw-head and arm-width scaling give 120–150 mm across the wedge, which is impossible. The 30 px screw heads are probably **5 mm** heads with washers and nearer to the camera than the wedge's far corners; the arm is seen with its side face. **Reconciled**: trust the ratio method. Wedge overall **96**, arm **12**, screws M2–M2.5.
2. **Wheel size**: AWS65's ratio gives 23–29 mm, but the box is 28 tall and the wheels are clearly taller than the box in AWS67/66, so they are at least 30. **Reconciled 32.**
3. **Wheels inside vs outside the box**: AWS66 clearly shows the wheels outside the clear walls at the rear; in AWS67 they appear behind the box top at the rear corners. Consistent: **outside, at the rear**.
4. **Box top**: AWS67 shows stepped lids, AWS66 a mostly open top. The lids may have been added later (like the green plates). Model the AWS67 version.
5. **Arm offset**: the finger lies right of centre in AWS67 and looks more central in AWS66 (perspective). **Reconciled: hub on the centreline, finger angled 10° right**, which fits both.
6. **Overall length**: 60 box + 38 wedge = 98. With the axle at y −20 the wheel rear would be at y −36, 6 mm behind the box, making 104. **Reconciled**: axle at y = −16, wheel rear at −32, overall **100**.

---

## 14. Why the designer did it (per part, from several angles)

Common lens: **adversarial**. For each part: what can attack it (spinners, wedges, lifters, flippers, wall slams, inversion), how it survives, and how it helps win. Then construction reasons.

- **Clear polycarbonate box**
  - Fight: polycarbonate is very impact-tough for its weight and flexes rather than cracking; a box with corner posts is stiff in all directions.
  - Weak points: 2 mm PC walls can be cut by a fast spinner; screws into printed posts can pull out.
  - Construction: laser-cut or hand-cut flat sheets, no large prints. Clear walls let the builder (and judges and audience) see the internals. The name "Stack Overflow" is a programming joke, matching the see-through "stack" of parts.
- **Aluminium rear plate**
  - Fight: the rear is hit when the robot is pushed backward or turned, and metal there resists wedge edges. It is also a strong cross-member between the wheels.
  - Construction: an engraved name plate doubles as structure.
- **Green FR4 side plates**
  - Fight: added after AWS66 to armour the clear sides against horizontal spinners and to stiffen the box at the wheel mounts.
  - Construction: off-cut PCB laminate; light, stiff, easy to cut.
- **Faceted aluminium wedge**
  - Fight: the main tool for getting under opponents. A 1 mm aluminium edge gets lower than a printed one and survives scraping. The **chevron** shape means opponents that arrive at an angle meet a facet and slide toward the centre face, where the arm is. The wedge is wider than the box, so it shields the box's front corners and sides from frontal attack.
  - Weak points: thin sheet can dent or fold back under a vertical spinner hit (see the gouge in AWS67), and the floor edge can catch on arena seams.
  - Construction: one sheet, cut and folded by hand, screwed to the box flange.
- **Rear wheels, wedge tip as skid**
  - Fight: putting weight on the wedge tip keeps it down, and two wheels save weight for the lifter.
  - Weak points: a two-wheeler turns on the spot but can be spun by side hits; the exposed wheels can be hit by horizontal spinners.
- **Single narrow arm lying on the wedge**
  - Fight: a single finger is light and does not cover the wedge, so the wedge works normally. When an opponent rides up, the finger lifts it from underneath and tips it over. If the robot is flipped, swinging the arm past vertical can right it **(guess)**. The black wrap gives grip and protects the printed finger from scraping on the floor and opponents.
  - Weak points: the printed arm can snap at the bend under a hard hit, and the off-centre finger lifts unevenly.
  - Construction: printed in one piece with a screwed hub; easy to replace.
- **Printed spur gears and a small gearmotor**
  - Fight: high torque from a small motor through the gear reduction lifts a 150 g opponent on the long arm. Large-module printed teeth tolerate shock better than fine ones.
  - Weak points: printed teeth can strip, and open gears can jam with debris (the top is partly open).
  - Construction: printed gears are free and quick to iterate. No servo is needed, and a gearmotor tolerates stalling and shock better than a servo.
- **Black ribbed stop**
  - Fight: limits arm travel so the arm does not slam into the rear and break **(guess)**.
- **Corner blocks and many screws**
  - Construction: simple and repairable; any panel can be swapped.
- **Visible switch and JST plug**
  - Rules: an accessible power switch is required; the JST lets the battery be unplugged for charging.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors, shafts along X out through the side walls | 12 × 10 × 25 | (±24, −16, 16) | medium |
| Motor clamps | printed U-clamps screwed to the floor | 14 × 12 × 6 | over each motor | low |
| Arm motor | N20 high-ratio gearmotor (e.g. 100:1–300:1) on the left, along X | 12 × 10 × 25 | (−20, −10, 18) | medium |
| Pinion position | behind GA on the motor shaft | Ø 12 | (≈ −8, −20, 22) | low |
| Battery | 2S 7.4 V LiPo 150–300 mAh | 40 × 18 × 8 | floor, front centre under the gear (0, +12, 8) | medium |
| Receiver / ESC | combined board (green PCB seen) | 30 × 20 × 5 | (+18, −14, 8) | high |
| Wedge backing | printed triangular ribs behind WG-C (screws go into them) | 3 × 38 × 26 | x = 0 and ±20 | low |
| Box floor | clear PC 2 mm | 76 × 60 | z 3–5 | medium |
| Arm shaft retention | e-clips or printed shoulders | — | at the bosses | low |
| Wire routing | along the left wall to the front | — | left | high (seen) |

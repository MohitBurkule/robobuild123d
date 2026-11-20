# Ice Breaker Junior: full rebuild description from reference photos

Source photos (all cut out onto white by the AWS wiki; black surfaces carry a strong **green colour cast** from the cut-out/white balance, so "green" on black parts is not a real colour):
- `robots/ice_breaker_junior/reference/ice_breaker_junior.aws74.webp` (1412 × 1047 px): AWS 74. Camera at the **front-right**, about 35° down. The forks point toward the camera (lower left and lower right). The robot's **right** side is on the image left. Best for the **weapon pod from the front**, the **right-side lid**, the **blue right wheel cover** and the **power jumper**.
- `...aws76.webp` (1554 × 992 px): AWS 76. Camera at the **left side, slightly front**, about 20–25° down. The forks point to the image left. Best for the **side profile of the forks and corner blocks**, the **beak plate**, the **upright servo horns**, the **disc's rim and hub**, and the **black left wheel cover**.
- `...aws77.webp` (1443 × 1091 px): AWS 77. Camera at the **rear-right**, about 40° down, forks pointing to the lower right. Best for the **top layout**: right lid, central hump with its top window, S-shaped horn plate, both horns, and the right wheel cover.

Everything stated as fact is read from those photos; inferences are marked **(guess)**. All sizes are **estimates in mm**, scaled from the AWS antweight limit (150 g, 101.6 mm cube) and the earlier spec draft (body 74 × 88 × 22 mm, wheels r 17, disc r 20, forks 45 mm), cross-checked against pixel ratios. Ratios are given against **W = body width without wheels ≈ 66 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the body footprint (mid-width, mid-length of the printed body, forks excluded).
- **+X** = robot right, **+Y** = forward (toward the forks and the disc), **+Z** = up. mm. Side-profile angles are measured from the floor in the YZ plane.
- Body extents (reconciled §12): x ∈ [−33, +33], y ∈ [−38, +30], z ∈ [3, 25]. Forks reach y ≈ +72. Wheels outboard to x = ±50 with their covers.

| ID | Part |
|---|---|
| BD | black printed body tub |
| LD-R, LD-L | flat top lids, right and left of the hump |
| HP | central raised hump (servo box), running fore-aft |
| HW | rectangular window in the hump top |
| HN-R, HN-L | two upright black servo horns at the front of the hump |
| SP | S-shaped black horn/link plate with 3 screws on the hump's right side face (rear) |
| FB-L, FB-R | front corner blocks (fork roots) |
| FK-L, FK-R | front forks (flat tapered printed bars) |
| GS-L, GS-R | fork gussets (sloped fillets under the fork roots) |
| WP | weapon pod: yokes YK-L, YK-R, outrunner MW, disc DS, axle AX |
| YK-L, YK-R | black printed weapon bearing yokes |
| BK-L, BK-R | pointed "beak" plates on the yokes' outer faces, each with a round hole |
| DS | steel weapon disc |
| MW | brushless outrunner driving DS |
| WH-L, WH-R | rear drive wheels (translucent knurled tyres, blue hubs) |
| WC-L, WC-R | outer wheel covers (D/teardrop plates: right blue, left blue at AWS74/77, black at AWS76) |
| WB-L, WB-R | wheel-cover brackets (blue on the right, black on the left at AWS76) with 2 × 2 holes |
| JP | small blue jumper (power link) |
| LED | small clear rectangular light pipe on the left lid |
| S-LD | silver Phillips lid screws |
| S-YK | silver Phillips yoke screws |
| S-HN | horn screws (silver hex + 2 Phillips below each horn) |
| S-FB | screws on the front corner blocks |
| M-L, M-R | drive gearmotors (hidden) |
| SV-L, SV-R | servos (hidden in the hump) |
| BAT, ESC, WESC, RX | battery, drive ESC, weapon ESC, receiver (hidden) |
| WR | wiring (a single fine white wire visible near the left lid; blue/white braided lead near the left wheel in AWS76) |

---

## 1. Overall description in one paragraph

Ice Breaker Junior is a **small two-wheel vertical-spinner** printed almost entirely in **black PLA**, with **blue** accents (wheel covers, brackets, hubs) and **translucent grey-white knurled tyres**. The body is a low box about 66 mm wide, 68 mm long and 22 mm tall. Two **long flat black forks** run forward and down from blocky front corners to the floor, giving a wide-legged "stag-beetle" stance. Between the forks, at the front, a **compact weapon pod** carries a **thick steel disc** (about Ø 40 mm) spinning in a vertical plane on a transverse axle, directly driven by a **black outrunner** beside it; the pod is held by two **black yokes** whose outer faces carry **pointed beak plates**. Behind the pod, the top of the body is split into **two flat lids** (left and right, each with 4 screws) and a **central raised hump** with a rectangular **window** in its top. Two **tall black servo horns** stand straight up on either side of the hump's front end, and a black **S-shaped plate** with three screws lies on the hump's right flank. At the rear corners, two **drive wheels** sit outboard, each hidden on its outer side by a large **D-shaped cover** on a bracket with four holes.

---

## 2. Part-by-part description

### 2.1 Body tub (BD)
- **Shape**: a rectangular box, **66 mm wide (W) × 68 mm long (1.03 W) × 22 mm tall (0.33 W)** from z = 3 to z = 25. All vertical edges are sharp; the top edges have about 1 mm chamfer/rounding where the lids sit. Walls about **2.5 mm** thick.
- **Front**: the front edge is not a wall but the **two corner blocks FB** with the weapon pod between them; the space between them (x ≈ −20 to +20) is open to let the disc protrude down and forward.
- **Sides**: plain black walls; at the rear, the wheel-cover brackets WB bolt to the side walls with 2 screws each (AWS74: one silver screw at the bracket front at z ≈ 14; AWS76: screws at the bracket and below the lid corner).
- **Rear**: not photographed squarely; the rear wheels sit at the rear corners, so the rear wall is probably short (between the wheels) **(guess)**.
- **Colour/material**: black PLA with fine 0.2 mm layer lines, a lightly textured top (the lids show a diagonal print texture).

### 2.2 Flat lids (LD-R, LD-L)
- **Shape**: two flat rectangular plates, each about **24 mm wide (X) × 62 mm long (Y) × 2 mm thick**, sitting on the body wall tops at z = 23–25. LD-R spans x ≈ +9 to +33, LD-L x ≈ −33 to −9.
- **Fasteners S-LD**: **4 silver Phillips pan screws** per lid (head Ø about 4 mm, M2), at the four corners about 3 mm in from the edges. AWS77 shows all four on LD-R; AWS74 shows four on LD-R and one on LD-L near its front; AWS76 shows LD-L's front-outer and rear-outer screws.
- **Surface**: a crosshatched print texture (top-layer pattern), with white scuffs.
- **Details**: LD-L carries a **small clear rectangular light pipe / LED window** (about **4 × 3 × 6 mm**) near its inner front corner (AWS76, at x ≈ −12, y ≈ +5), sticking up about 4 mm. A thin white wire loops from it toward the rear **(guess: status LED)**.

### 2.3 Central hump (HP) and window (HW)
- **Shape**: a raised rectangular box along the centreline, **18 mm wide (x ≈ −9 to +9) × 50 mm long (y ≈ −30 to +20) × 12 mm higher than the lids** (top at z ≈ 37). Its front top corner is **rounded** (radius about 6 mm, seen in AWS76 and AWS77 as a smooth curve where the top meets the front face).
- **Window HW**: a rectangular opening in the hump top, **8 mm wide × 18 mm long**, centred at y ≈ −2. Through it a **dark cylindrical part** is visible (a servo body or a motor can).
- **Side faces**: the right face carries the **S-plate SP** at its rear half and the **right horn's mounting screws** at its front. The left face mirrors this (left horn's screws visible in AWS76).
- **Function**: houses the two servos (SV-L/R) side by side or stacked, with their output splines coming out of the hump's side faces at the front.

### 2.4 Servo horns (HN-L, HN-R)
- **Shape**: standard **single-arm servo horns**, black plastic, about **22 mm long**, **7 mm wide at the hub tapering to 5 mm** at the rounded tip, **2.5 mm thick**. Each has a **round hub** (Ø about 7 mm) with a **silver hex/Phillips centre screw**, and **two or three small holes** along the arm (one near the tip visible).
- **Pose**: both stand **straight up** (vertical), with the hub at about z ≈ 32 and the tip at z ≈ 52. HN-R sits against the hump's right face (x ≈ +11), HN-L against the left face (x ≈ −11), both at y ≈ +14 (front end of the hump). The horn planes are YZ, so they rotate about **X**.
- **Screws below each horn**: two small silver Phillips screws vertically below the hub (AWS76: at z ≈ 27 and 24 below the near horn), fixing a horn adaptor or the servo flange to the hump wall.
- **Function (guess)**: the most likely function is a **pair of self-righting arms**: each servo swings its horn backward/forward through about 180° to push the robot over when inverted, since the horn tips (z ≈ 52) are taller than everything else. An alternative is that the horns tilt the weapon pod or the forks via a hidden linkage, but no link is attached to the horn holes in any photo. Confidence: **self-righter, low–medium**.

### 2.5 S-plate (SP)
- **Shape**: a flat black plate, about **26 mm long × 9 mm wide × 2 mm thick**, shaped like a **shallow "S" or dog-bone**: three round lobes (Ø 9 mm) joined by narrower waists, the middle lobe offset down by about 3 mm. Three silver Phillips screws (head Ø 4 mm) through the lobes, spaced about **9 mm** apart.
- **Position**: on the hump's **right side face**, rear half (y ≈ −28 to −4, z ≈ 27–33), screwed into the wall (AWS74 and AWS77).
- **Function (guess)**: a **servo retaining strap**: it clamps the servo flange (or a cross-shaft bearing) through the hump wall. Its S shape follows the servo's mounting ears. Alternatively a cut-down servo horn used as a clamp. Confidence low.

### 2.6 Front corner blocks (FB-L, FB-R) and gussets (GS)
- **Shape**: two blocky black parts at the front corners, each about **14 mm wide (X) × 16 mm long (Y) × 20 mm tall**, from z = 3 to z = 23. Their front faces are sloped/faceted: the upper front edge is cut back at about 45°, and a **sloped gusset GS** (a triangular fillet about 12 mm long) flows from the block's lower front into the fork root.
- **Fasteners S-FB**: a silver Phillips screw on each block's outer side face (AWS76: at about z ≈ 12, y ≈ +22) and one on the top front corner of the lid near it.
- **Damage**: both blocks show **white stress-whitening and scraped edges** at the fork roots (AWS74 left fork root: a pale scar; AWS76 near root: cracked layers), meaning they have taken hits.

### 2.7 Forks (FK-L, FK-R)
- **Shape**: flat tapered bars printed in black, **about 46 mm long** from the block face to the tip, **11 mm wide at the root tapering to 8 mm at the tip**, **3 mm thick at the root tapering to about 1 mm** at the chisel tip. The tip edge is cut square across.
- **Side profile**: from the root at z ≈ 10 (y ≈ +30) the fork runs **forward and down at about 12°** to the floor at y ≈ +72. The bottom face of the last 10 mm lies flat on the floor (a skid). The root merges with the gusset GS.
- **Plan**: the forks are **parallel**, pointing straight ahead, at x ≈ ±25 (centres), so the gap between them is about **38 mm** and their outer edges are about 61 mm apart.
- **Surface**: rough, with scuffs and a pale scratched tip (wear from the floor).

### 2.8 Weapon pod (WP): yokes YK, disc DS, outrunner MW, axle AX
- **Yokes YK-L/YK-R**: two black printed **bearing blocks**, each about **9 mm thick (X) × 20 mm long (Y) × 22 mm tall (Z)**, with a rounded front (radius about 10 mm around the axle) and a **top lug** carrying a **silver Phillips screw** (S-YK, AWS76: one on each yoke top at z ≈ 33, one on the outer face). They stand at x ≈ −22 (YK-L) and x ≈ +14 (YK-R) **(positions reconciled §13)**, between the fork blocks, and are screwed down to the body front.
- **Disc DS**: a **steel disc, Ø 40 mm × 5 mm thick**, its plane vertical (YZ), centred at **x ≈ −10, y ≈ +24, z ≈ 22**. The **outer rim is bright ground steel** (about 3 mm band) and the faces are dark/blued. A **silver hub bolt/spacer** (Ø about 8 mm) sits at its centre. No teeth are visible on the rim in any photo; it may have **two small shallow bites** (not seen) **(guess)**, or be a plain round "flywheel" disc relying on friction (unlikely) **(guess: two low teeth)**.
- **Outrunner MW**: a black **brushless outrunner, about Ø 22 × 14 mm**, coaxial with the disc on its **right side** (x ≈ +2), with **orange/copper windings visible** through the can's gap (AWS74). It sits inside the right yoke's ring.
- **Axle AX**: a steel shaft **Ø 3–4 mm** along X at z ≈ 22 through both yokes, the disc and the motor (the motor shaft itself extended, or a dead axle on which the disc+bell spins) **(guess)**.
- **Disc clearance**: the bottom of the disc is at z ≈ 2 (2 mm above the floor) and its front at y ≈ +44, so it reaches **14 mm ahead of the body front**; the top is at z ≈ 42.

### 2.9 Beak plates (BK-L, BK-R)
- **Shape**: flat black plates about **3 mm thick**, outline a **pointed hexagon / arrowhead**: about **24 mm long × 18 mm tall**, with the point toward the rear, and a **round hole Ø 4 mm** near the centre (AWS74, AWS76, AWS77). The front edge is screwed to the yoke's outer face; the rear point lies against the lid edge.
- **Position**: one on each yoke's outer face (AWS74 and AWS77 show the robot-right one; AWS76 shows the robot-left one), sloping back and down onto the lids at about 20°.
- **Function (guess)**: **tie plates** that brace each yoke back onto the body (the hole takes a screw into the lid/body; it is empty in the photos, so it may be a pivot for tilting the pod, or a spare). Confidence low.

### 2.10 Rear wheels (WH-L, WH-R)
- **Shape**: **Ø 34 mm × 10 mm** wheels. The tyre is **translucent grey-white TPU** with a coarse **knurl / gear-tooth tread** (about 40 teeth, each about 1.5 mm tall and 2 mm wide, running across the tyre). The hub is **blue** printed plastic.
- **Positions**: wheel centres at **x = ±40, y = −22, z = 17**. Wheel tops at z = 34 (above the lids by 9 mm, below the hump top by 3 mm); bottoms at z = 0.
- **Drive**: each wheel is on the shaft of an N20-class gearmotor inside the rear of the body **(guess)**.

### 2.11 Wheel covers (WC-L, WC-R) and brackets (WB-L, WB-R)
- **WC shape**: a flat plate about **3 mm thick**, shaped like a **"D" or teardrop**: a **circle of Ø 38 mm** around the wheel axis merged with a straight tangent edge running forward-down to the bracket. The outer face is plain and slightly domed at the edge.
- **WB shape**: a printed **bracket arm**, about **20 mm long × 14 mm tall × 10 mm thick (X)**, bolted to the body side wall ahead of the wheel and running back to the cover. Its outer face shows a **2 × 2 grid of round holes** (Ø about 4 mm, two of which carry screws) and a sloped top.
- **Colours**: right side **blue** (AWS74 and AWS77), left side **blue** in AWS74 (far side, top right) and **black** in AWS76.
- **Position**: the cover's inner face is about **1–2 mm** outside the tyre face, at x ≈ ±46 to ±49. The cover hides the hub and the tyre side completely.
- **Function**: hubcap/side guard, and the far end of a **wheel support**: the cover likely carries an **outer bearing** or stub for the axle, making the wheel supported on both sides **(guess, medium)**.

### 2.12 Small parts
- **JP**: a **blue 2-pin jumper** (about 5 × 3 × 6 mm) between LD-R and the hump at y ≈ +10 (AWS74) **(power link, guess)**.
- **LED**: clear light pipe on LD-L (see 2.2).
- **WR**: a **blue/white braided lead** behind the left horn in AWS76 (near the left wheel), probably the antenna or battery balance lead.

---

## 3. Per-view descriptions

### 3.1 Top view (synthesised from AWS77 and AWS74)
- A 66 × 68 mm black rectangle. Down the middle, the **hump** (18 wide, rounded front) with its window; either side, a flat lid with four screws. At the rear corners, two wheel rectangles (34 × 10) with D-shaped covers outboard (overall width about 100 mm).
- In front: two **corner blocks** and two **parallel forks** running 42 mm ahead; between the blocks the **weapon pod**: disc (a 40 × 5 mm slot shape in plan, left of centre) with the outrunner circle to its right, yokes either side, and the arrowhead **beak plates** pointing back onto the lids.
- Overall: about **100 mm wide (over the covers) × 110 mm long (rear of wheel covers to fork tips)**. The diagonal fits the cube when placed corner-to-corner; the AWS cube check is lenient for forks **(note)**.

### 3.2 Front view (AWS74)
- The floor line with the two fork tips (11 mm wide) at x ≈ ±25. Above them, the sloped gusset fillets rising to the corner blocks.
- In the middle, the **disc** edge-on (5 mm wide, 40 tall) left of centre, with the **outrunner** beside it and the **yokes** framing both.
- Behind and above, the hump's rounded front with the two horns standing up on either side like ears, then the lids, and the wheel tops and covers at the outer corners.

### 3.3 Left side view (AWS76)
- A low black rectangle (68 × 22) with the black D-shaped wheel cover covering the rear third. In front, the corner block with its gusset and the fork running down to the floor (42 mm ahead). Behind the block, the **beak plate** (arrowhead with a hole) on the yoke, the **disc** rim showing as an arc above the yoke, and the **horn** standing up behind it. Above the lid line: the hump with its rounded front.

### 3.4 Rear view (inferred)
- The rear wall between the two wheels; the covers at the outer edges; the hump's rear end in the middle; the horn tips above it. Possibly the switch/jumper access **(guess)**.

### 3.5 Isometric (AWS77-like, rear-right high)
- Reads as a black box with a raised centre spine, two "ears" (horns), blue D-caps on the wheels, and a disc and two long prongs at the front.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | box tub | 66 × 68 × 22 | 1 × 1.03 × 0.33 | black PLA | — | 1 |
| LD | flat plate | 24 × 62 × 2 | 0.36 × 0.94 | black PLA | 4 × M2 | 2 |
| HP | raised box | 18 × 50 × 12 (above lids) | 0.27 × 0.76 | black PLA | screwed/integral | 1 |
| HW | window | 8 × 18 | 0.12 × 0.27 | — | — | 1 |
| HN | servo horn | 22 × 7 × 2.5 | 0.33 | black | spline + screw | 2 |
| SP | S-plate | 26 × 9 × 2 | 0.39 | black | 3 × M2 | 1 (right; left unseen) |
| FB | corner block | 14 × 16 × 20 | 0.21 × 0.24 × 0.30 | black PLA | screws | 2 |
| GS | gusset | 12 × 11 × 10 | — | black PLA | integral | 2 |
| FK | tapered bar | 46 × 11→8 × 3→1 | 0.70 | black PLA | integral with FB | 2 |
| YK | yoke | 9 × 20 × 22 | 0.14 × 0.30 × 0.33 | black PLA | 2 × M2 | 2 |
| BK | arrowhead plate | 24 × 18 × 3 | 0.36 | black PLA | 1–2 screws | 2 |
| DS | disc | Ø 40 × 5 | 0.61 | steel, ground rim | on axle | 1 |
| MW | outrunner | Ø 22 × 14 | 0.33 | black + copper | in YK-R | 1 |
| AX | axle | Ø 3–4 × 40 | — | steel | yokes | 1 |
| WH | wheel | Ø 34 × 10 | 0.52 × 0.15 | clear TPU + blue hub | motor shaft | 2 |
| WC | D-plate | Ø 38 + tail, 3 thick | 0.58 | blue / black | on WB | 2 |
| WB | bracket | 20 × 14 × 10 | 0.30 | blue / black | 2 × M2 to BD | 2 |
| JP | jumper | 5 × 3 × 6 | — | blue | plug | 1 |
| LED | light pipe | 4 × 3 × 6 | — | clear | in LD-L | 1 |
| S-LD | pan screw | head Ø 4 | 0.06 | silver | lids | 8 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| BD bottom ↔ floor | clearance | 3 |
| WH bottom ↔ floor | contact | 0 |
| FK tip ↔ floor | contact (skid) | 0 |
| DS bottom ↔ floor | clearance | 2 |
| DS faces ↔ YK-L inner face / MW | side by side | 1–2 |
| MW ↔ YK-R | clamped | 0 |
| YK ↔ BD front | screwed | 0 |
| BK ↔ YK outer face | screwed | 0 |
| BK rear point ↔ LD | resting / screwed | 0 |
| DS rim ↔ FB inner faces | side clearance | 8–12 |
| DS rear ↔ hump front | clearance | 3–5 |
| HN ↔ HP side face | side by side (rotates) | 1 |
| HN tip ↔ anything | free | — |
| SP ↔ HP right face | screwed | 0 |
| LD ↔ BD wall tops | screwed | 0 |
| LD inner edge ↔ HP side face | butt joint | 0–0.5 |
| WH inner face ↔ BD side | near | 2 |
| WH outer face ↔ WC inner face | near | 1–2 |
| WB ↔ BD side wall | screwed | 0 |
| WC ↔ WB | integral/screwed | 0 |
| WH top ↔ LD plane | wheel above lids | +9 |
| WH top ↔ HP top | hump higher | −3 |
| HN tip ↔ WH top | horns higher | +18 |

---

## 6. Mechanism

1. **Drive**: 2WD at the rear; the forks act as front skids. Two N20 gearmotors, one per wheel **(guess)**. Turning is skid-steer on the two wheels with the forks sliding.
2. **Weapon**: a direct-drive vertical disc. The outrunner bell drives the disc on a common axle; the disc spins so that its front edge moves **upward** (standard vertical spinner) **(guess for direction)**. Tip speed estimate: a 2S 2200 kV outrunner at about 15,000 rpm under load gives v = π·0.040·250 ≈ 31 m/s. Stored energy for a 5 mm steel disc of Ø 40: m = 7.85 g/cm³ · π · (2 cm)² · 0.5 cm ≈ 49 g. That is too heavy for a 150 g robot, so the disc is probably **thinner (3 mm, ~30 g) or has lightening holes**, or the steel is just a rim on an aluminium centre **(see §13)**.
3. **Horns**: two servos turn the horns in the YZ plane (about X). Upright is their parked position. Primary guess: **self-righting** (the horn tips reach 52 mm, enough to lever the 68 mm long robot over when inverted, especially as the robot inverted would rest on the hump and the wheel tops).
4. **Invertibility**: the wheels (top at 34) are below the hump (37) and horns (52), so **the robot cannot drive inverted**; it must self-right. This supports the self-righting reading.

---

## 7. Assembly order (suggested rebuild)

1. Print **BD** (tub with front corner blocks, gussets and forks as one piece, or forks as separate printed parts screwed to FB) and the **hump HP**.
2. Install the two **drive gearmotors** in the rear of the tub, shafts out at z = 17, y = −22.
3. Bolt the **wheel-cover brackets WB** to the side walls; mount the wheels on the shafts; screw the **covers WC** to the brackets (carrying the outer axle stub, if any).
4. Install the two **servos** in the hump with their splines out through the side faces at y ≈ +14, z ≈ 32; fit the **S-plate** retainer on the right side.
5. Install the **battery, drive ESC, weapon ESC and receiver** under the lids; plug in the **jumper JP**; fit the **LED** light pipe in LD-L.
6. Build the **weapon pod**: press the outrunner into YK-R, slide the disc and spacer onto the axle, close with YK-L; screw both yokes to the body front.
7. Screw the **beak plates** onto the yokes' outer faces and down onto the lids.
8. Screw the **lids** on (8 screws). Fit the **horns** upright.

---

## 8. Hidden / uncertain list
- Function of the upright horns (self-righting vs weapon tilt).
- Disc tooth profile and thickness; whether it is solid steel.
- Whether the forks are separate parts.
- Exact x-offset of the disc (left of centre in all three photos, by about 10 mm).
- Drive motor type; whether the wheel covers carry outer bearings.
- The underside and rear.
- All sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin under the body centre, +X right, +Y forward, +Z up, mm.
- BD: x ∈ [−33, 33], y ∈ [−38, 30], z ∈ [3, 25]. HP top z = 37. Horn tips z = 52. Disc centre (−10, +24, 22), Ø 40. Wheels (±40, −22, 17), Ø 34. Fork tips at y = +72, x = ±25.

## 10. Profiles as math

**10.1 Fork FK side profile (YZ, at x = ±25, thickness along X 11 → 8 mm).**
- Top edge: z = 13 − 0.24·(y − 30) for y ∈ [30, 72] (from 13 down to 3, then the tip bevel).
- Bottom edge: z = 10 − 0.24·(y − 30) for y ∈ [30, 62]; z = 0 for y ∈ [62, 72] (flat skid).
- Tip: a vertical cut at y = 72 from z = 0 to z = 1 (chisel).
- Width in X: w(y) = 11 − 3·(y − 30)/42.

**10.2 Gusset GS (YZ).** Triangle with vertices (y 24, z 22), (30, 13), (30, 22) blended into the block's sloped front: front face line z = 22 − 1.5·(y − 24).

**10.3 Hump HP (YZ section at x = 0).** Rectangle y ∈ [−30, +20], z ∈ [25, 37] with the front-top corner rounded by an arc centred at (y +14, z 31), r = 6, from θ = 0° (front) to 90° (top).

**10.4 Wheel cover WC (outline in its YZ plane at x = ±48).** Union of a circle centred (y −22, z 17), r = 19, and the convex hull of that circle with the point (y +2, z 8) (the bracket end): the tangent lines from (2, 8) to the circle form the teardrop tail.

**10.5 Beak plate BK (outline in its plane, local u forward, v up, origin at the yoke centre).** Arrowhead pentagon with vertices (6, 9), (6, −9), (−6, −9), (−18, 0), (−6, 9). Hole r = 2 at (−5, 0).

**10.6 Horn HN (in the YZ plane).** Hub circle r = 3.5 at (y +14, z 32); arm a tapered slot from the hub to a tip circle r = 2.5 at (y +14, z 50) (vertical): outline = convex hull of the two circles. Holes r = 0.8 at z = 40, 44, 48.

**10.7 Disc DS.** Circle r = 20 at (y +24, z 22), extruded along X from −12.5 to −7.5. Optional two teeth: r(φ) = 20 + 2·[φ mod π < 0.25].

**10.8 Tyre tread.** r(φ) = 15.5 + 1.5·[sin(40φ) > 0], width 10.

## 11. Pixel-based measurements

**AWS74 (front-right):**
- Left fork (robot right) root block at (440–600, 540–700); tip at (720–770, 920–955). Right fork (robot left) root (1090–1160, 400–470); tip (1290–1370, 670–715).
- Disc rim: x 900–960, y 260–500 (edge-on ellipse, about 240 px tall). Outrunner: x 780–900, y 300–480.
- Right lid: corners about (240, 270), (480, 210), (650, 400), (440, 545); four screws at (285, 355), (455, 225), (460, 535), (645, 400)?
- Horns: (630–700, 120–330) and (880–930, 150–310).
- Right wheel cover (blue): x 40–200, y 290–580 (about 290 px tall).

**AWS76 (left side):**
- Near fork: root block (700–1000, 540–640), tip (560–700, 890–970). Far fork tip (30–80, 590–615).
- Disc: x 420–560 wide ellipse, y 240–580 (about 340 px tall).
- Near horn: (700–790, 100–360). Far horn: (520–600, 40–190).
- Black left wheel cover: (1270–1520, 360–700), Ø about 330 px.
- Beak plate: (610–870, 370–540), hole at (725, 435).
- Body side from front block to wheel bracket: x 660–1070 (about 410 px), wall height (bottom edge 600 → lid 560?) about 140 px.

**AWS77 (rear-right high):**
- Right wheel cover (blue) at (40–360, 390–770). Right lid: (250–720, 300–700). Hump window: (680–790, 210–250). Horns: (760–820, 230–420) and (900–960, 110–240). Disc: (840–1110, 290–530).

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | 74 (spec) | wheels outboard, total ≤ 101.6 → W ≤ 101.6 − 2·(10 + 3 + 4) = 68 | AWS74: lid 24 of ≈ 2.7 lid widths… ≈ 66 | **66** |
| Body length | 88 (spec) | wheel Ø 34 is 0.5 of length (AWS76) → 68 | AWS76: 410 px body vs 330 px cover (Ø 38) → 47?? (foreshortened, side oblique) | **68** |
| Body height | 22 (spec) | 0.33 W | AWS76: 140 px vs 330 px cover (38 mm) → 16 + lid… ≈ 20 | **22** |
| Wheel Ø | 34 (r 17 spec) | 0.52 W | AWS76: cover 330 px ≈ Ø 38 → wheel 34 | **34** |
| Disc Ø | 40 (r 20 spec) | about the hump's 0.8 length | AWS76: 340 px vs cover 330 px → ≈ 39 | **40** |
| Fork length | 45 (spec) | 0.7 W = 46 | AWS74 (near fork, foreshortened): 260 px / 6 px/mm ≈ 43 | **46** |
| Horn length | std horn 20–25 | 0.33 W | AWS76: 260 px vs disc 340 px × 40 → 31 (incl. hub and perspective) | **22** (std part) |
| Hump height above lids | — | 0.18 W | AWS76: about 100 px vs 330 px cover → 11.5 | **12** |

## 13. Consistency check: conflicts and reconciliation
1. **Body length**: the spec's 88 mm plus 42 mm of forks gives 130 mm, far over the cube. The photos show the forks as long as about two-thirds of the body. **Reconciled body 68 + forks 42 = 110 mm**; the diagonal of the 101.6 cube's face is 143 mm, and forks are commonly angled to fit, so accept.
2. **Disc mass**: a 40 × 5 solid steel disc weighs about 49 g, a third of the robot. That is possible for a "spinner-first" design but tight with 2 servos. **Reconciled: Ø 40 × 4 mm steel (≈ 39 g)**, hub bolt, two low teeth; note "thickness 3–5 mm".
3. **Disc offset**: all three photos put the disc on the robot's **left** of centre with the motor to its right. AWS76 (left side) shows the disc rim nearest the camera of all pod parts after the beak. **Reconciled: disc centre x = −10**, motor x = +2, yokes at x = −20 (inner face −15) and x = +12 to +20.
4. **Beak plates on both sides**: AWS74/77 show one on the robot-right yoke; AWS76 shows one on the robot-left yoke. **Reconciled: two, mirrored.**
5. **Wheel cover colour**: the left cover changed from blue (AWS74, far side) to black (AWS76). **Reconciled: geometry identical, colour per event.**
6. **Hump orientation**: from the rear-right photo the hump appears diagonal; using the rear axle (wheel to wheel) as the X reference, the hump's long edges are parallel to the fork direction. **Reconciled: hump fore-aft on the centreline**, flanked by two lids.
7. **Horns as weapon actuators**: no linkage is attached to the horns in three different events, and they are always upright, so they are not driving anything continuously. **Reconciled: self-righting levers (low–medium confidence).**

---

## 14. Why the designer did it (per part, adversarial first)

- **Low black box (22 mm)**
  - Fight: little face for an enemy vertical spinner to hit, and a low centre of gravity so wedges and lifters have to get fully under to tip it. All-black PLA is cheap; the robot accepts that body parts will crack (visible stress whitening at the fork roots) and relies on screwed-on, replaceable parts.
  - Threats: horizontal spinners hitting the square corners; flippers getting under the flat floor between the forks.
- **Two long forks**
  - Fight: **forks beat wedges** at getting under opponents: two thin chisel tips flat on the floor slide under an opponent's front edge earlier than a broad wedge would, and lift its front so the **disc** can strike the exposed underside. They also define the **engagement range**: an opponent pushed into the fork gap meets the disc at exactly the right height.
  - Being got under: forks leave the body's front edge open between them, but the disc fills that gap, so an enemy wedge entering between the forks gets hit by the spinner first.
  - Survival: forks are long levers; a hit bends them up at the root, so the root has a **thick gusset** and the block is solid; damage there is visible in the photos. They are sacrificial.
  - Construction: printed integral with the corner blocks; reprinted per event.
- **Weapon pod with the disc slightly off-centre**
  - Fight: a **direct-drive** outrunner removes the belt (a common failure point); the motor itself is the hub. The disc is small and thick (energy in the rim) and spins vertically to **launch opponents upward** or flip them. Placing it between the forks means it only contacts what the forks have lifted.
  - Off-centre: the motor and disc together are about 25 mm wide; centring the **pair** (not the disc) on the robot puts the disc slightly left. That is a packaging choice.
  - Survival: the yokes are thick and screwed down; the beak plates triangulate the yokes back onto the lids so a hit on the disc that tries to rotate the pod backward is resisted by a tie in compression/tension. The weapon's own gyroscopic stiffness also resists being knocked aside.
  - Threat: hits on the disc pass into the axle and yokes; a horizontal spinner can strike the exposed outrunner can from the side between the forks.
- **Beak plates**
  - Fight: braces against the recoil of each weapon hit (the reaction pushes the pod back and up). The pointed shape puts the material along the force line.
  - Construction: flat, quick to print, one screw hole as an anchor.
- **Central hump and two servos**
  - Fight: the servos are buried in a box behind the weapon, protected on all sides. The hump also acts as the **roll-over contact** when inverted.
  - Self-righting: a vertical spinner that cannot run inverted must right itself; two horns working together can push from the hump sides on the floor and roll the robot back onto its wheels. Horns are **cheap, replaceable** standard parts (the tips show wear holes).
  - Threats: the horns stick up 15 mm above everything, so an overhead spinner or the opponent's lifter can snap them. Standard horns are cheap to replace.
- **Lids with 4 screws each**
  - Construction: fast access to battery and ESCs; separate left/right lids so one side can be opened without removing the hump or weapon. Fight: a flat top lets a lifter/flipper slide over rather than catch.
- **Rear wheels outboard with D-covers**
  - Fight: the covers shield the tyres' outer faces from horizontal spinners and keep the wheels from snagging on walls. The D-tail running forward to the bracket presents a **sloped face** to anything coming from the side, deflecting it. Translucent knurled TPU tyres give strong grip for pushing.
  - Survival: the covers take the side hits instead of the motor shafts; with a second support at the cover, a side hit does not bend the gearmotor shaft **(guess)**.
  - Construction: separate covers in different colours show they are replaced or swapped often.
- **Jumper and LED**
  - Rules: a removable link is the required power isolator; the LED shows power-on status as required by AWS rules. Both are mounted on top for quick access.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotor, 6 V, 300–600 rpm | 12 × 10 × 25 | x ±22, y −22, z 17, shafts out along ±X | medium |
| Servos | 2 × 9 g micro servos (metal gear) | 23 × 12 × 23 | inside HP, side by side? HP is only 18 wide, so stacked fore-aft: SV-R at y +8, SV-L at y −10, splines out of the side faces at y +14 (via a short shaft on SV-L) | low |
| Weapon ESC | 20–30 A brushless ESC | 30 × 15 × 6 | under LD-L, x −20, y −5, z 10 | medium |
| Drive ESC | dual brushed ESC | 25 × 15 × 5 | under LD-R, x +20, y −10, z 8 | medium |
| Battery | 2S 300–450 mAh LiPo | 45 × 18 × 10 | under LD-R/hump, along Y, x +18, y +0, z 9 | medium |
| Receiver | small 2.4 GHz | 20 × 12 × 5 | under LD-L rear, x −20, y −25, z 8 | low |
| Weapon motor | 22xx outrunner, 1500–2500 kV | Ø 22 × 14 | x +2, y +24, z 22 | high (seen) |
| Axle and bearings | 3–4 mm shaft, small flanged bearings in the yokes | Ø 3–4 | along X at (y 24, z 22) | medium |
| Outer wheel bearings | none or a plain hole in the cover | — | at the cover centre | low |
| Wiring | battery → JP link → both ESCs; weapon ESC phase wires forward to the outrunner along the hump's left side; motor leads back to the wheel motors; servo leads into the hump; LED on LD-L | — | — | medium |

# Slipper: full rebuild description from reference photos

Source photos (all small, uncut, low resolution; every detail below is read at the limit of what the pixels show):
- `robots/slipper/reference/slipper.aws62.webp` (407 × 419 px): AWS 62. The robot sits on a pale wooden/laminate table. The camera looks **down the sloped top face from the front**, about 50–60° down, so the top face fills the image and the left side wall is visible on the image left. The body is **matt silver-grey**. The **perforated top flap** is closed.
- `...aws63.webp` (320 × 279 px): AWS 63. The robot is inside a **clear plastic storage tub** with other robots. The camera is at the **front-left**, about 40° down. The **flap is open** (raised), showing the inside: a **white block**, **red wires**, a **black/white component** and a **perforated aluminium floor**. The handwritten name **"SLIPPER"** is on the left side wall.
- `...aws64.webp` (390 × 294 px): AWS 64. A **rebuilt body in bare aluminium sheet** on a wooden board/lid. The camera is above the **left side**, about 45° down, with the front (thin edge) on the image left and the **rounded rear "heel"** on the image right. A **white hinge strip** separates the top plate from the rolled heel. "Slipper" is written on the left side.

Everything stated as fact is read from those photos; anything inferred is marked **(guess)**. Sizes are **estimates in mm**, scaled from the AWS antweight limit (150 g, fits a 101.6 mm cube) and the earlier spec draft (body 110 × 80 × 48 with a long ramp, 2 inboard wheels r 11, which is too long for the cube; see §13). Ratios are given against **W = body width ≈ 70 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the body footprint.
- **+X** = robot right, **+Y** = forward (toward the thin wedge edge, the "toe"), **+Z** = up. mm. Angles in side profiles are measured from the floor.
- **Front** = the thin edge (toe). **Rear** = the tall rounded end (heel). In AWS62 the toe is at the bottom of the image and the left side is on the image left. In AWS63 the toe points toward the image bottom-centre, the heel to the upper left. In AWS64 the toe is on the image left.
- Body extents (reconciled §12): x ∈ [−35, +35], y ∈ [−45, +50], z ∈ [0, 40].

| ID | Part |
|---|---|
| SW-L, SW-R | side walls (right-trapezoid profile, printed silver-grey in AWS62/63, folded aluminium in AWS64) |
| BF | base / floor plate (perforated aluminium visible inside in AWS63) |
| TO | toe: front wedge edge / front sloping face below the flap |
| FL | perforated top flap (lid / possible flipper) |
| FL-H | flap hinge (at the top rear edge) |
| BB | black rubber/foam-covered bar along the flap's rear edge (hinge barrel) |
| HL | rounded heel (rear end; printed rounded corner in AWS62, rolled aluminium in AWS64) |
| HS | white hinge strip (AWS64) |
| S-FL | front screws on the flap: 2 large slotted round heads + 1 small centre screw + 2 tiny corner screws |
| S-HL | screws on the heel (AWS64: 3) |
| S-TP | screws on the AWS64 top plate (7) |
| WB | white printed block inside (linkage pivot or mount) |
| SV | flap servo (hidden, only if powered) |
| WH-L, WH-R | drive wheels (hidden; guessed inboard under the body) |
| M-L, M-R | drive motors (hidden) |
| BAT, RX, ESC, SW | battery, receiver, ESC, switch (black/white component seen in AWS63) |
| WR | red wires visible inside (AWS63) |
| NM | handwritten name "Slipper" on the left side |

---

## 1. Overall description in one paragraph

Slipper is a **shoe-shaped full-body wedge with a hinged top flap**. In side view it is a **low right-trapezoid**: a flat bottom, a long **top face sloping at about 25–26°** from a knife-thin **toe** at the floor up to a **rounded heel** about 40 mm tall at the rear. In plan it is a plain rectangle about 70 mm wide and 95 mm long. In AWS62/63 the body is printed (or painted) **matt silver-grey**, with thick side walls that stand slightly proud of the top face and form two rails either side of a **recessed, perforated grey flap** that fills most of the top. The flap has a **4-column × 5-row grid of rectangular windows**, two big slotted screws at its low (front) end, and a **black rubber-covered bar** across its high (rear) end. In AWS63 the flap is swung up about its rear edge, showing a white printed block, red wiring and a perforated aluminium floor inside. In AWS64 the robot has been rebuilt from **bare folded aluminium sheet**: a flat top plate with seven screws, a front lip folded down, and a large **rolled heel** joined to the top plate by a **white piano-hinge strip**. No wheels or weapons protrude anywhere; the drive is hidden underneath.

---

## 2. Part-by-part description

### 2.1 Side walls (SW-L, SW-R), AWS62/63 body
- **Shape**: two thick printed walls with a **right-trapezoid profile**: bottom edge 95 mm long, rear edge about 40 mm tall (with a rounded top-rear corner), top edge sloping down to the toe. The wall thickness is about **6 mm** (0.08 W; AWS62 shows a broad flat top rim on each wall). The top of each wall stands **about 2–3 mm above the flap**, so the flap sits in a recess between them.
- **Bottom flare**: in AWS62 the left wall's outer face appears to **flare slightly outward toward the floor** (a draft of about 5°) **(guess: printed with a slight batter)**.
- **Details**: a **small round hole** (Ø about 3 mm) near the top rear of each wall (AWS62, top left and top right of the image): the **hinge pin ends** of FL-H **(guess, medium)**. A short scratch/mark line mid-way down the left wall in AWS62.
- **Name**: **"Slipper"** written by hand in black marker, running diagonally down the left wall (AWS62 and AWS63), letters about 6 mm tall.
- **Colour/material**: matt **silver-grey PLA** (or grey-painted), with soft rounded edges (radius about 2 mm).

### 2.2 Top flap (FL)
- **Shape**: a flat plate, **about 52 mm wide × 78 mm long (down the slope) × 2.5 mm thick**, lying in the recess between the side walls at the wedge angle.
- **Windows**: a grid of **20 rectangular through-holes**, **4 columns × 5 rows**. Each hole is about **5 mm wide × 8 mm long** (long axis along the slope). The columns are arranged as **two pairs**: within a pair the holes are about 4 mm apart; between the pairs there is a **solid centre strip about 10 mm wide**. Rows are spaced about **13 mm** centre to centre. The holes show a raised rim (perimeter walls of the print). A **small round hole** (Ø about 2 mm) sits in the centre strip between rows 4 and 5.
- **Front (low) end**: the last 12 mm of the flap is solid and carries **two large slotted round-head screws** (heads Ø about 7 mm, M4-ish) at x ≈ ±12, **one small screw** (Ø 2.5 mm head) on the centreline between them, and two tiny screws at the far corners (x ≈ ±22). The flap's front edge stops about **8–10 mm above the floor**; the body's toe continues below it.
- **Rear (high) end**: the black bar BB lies across the full width of the recess.
- **AWS63 (open)**: the perforated plate (here looking like **aluminium**, shiny with punched square holes) is lifted, rotated up about the **rear** edge (the black-bar end) by about **60–70°** relative to its closed position, with its free (front) end pointing up and forward. A **white strip** lies along one underside edge (a spacer or printed backing).
- **Material**: **grey PLA** in AWS62 (hole rims look printed), **perforated aluminium** in AWS63. Possibly a printed frame over an aluminium plate **(guess)**.

### 2.3 Black bar (BB) and flap hinge (FL-H)
- **Shape**: a **cylinder-like bar**, about **52 mm long × 10 mm diameter**, covered with **black rubber/foam or black tape**, with white flecks on its surface (AWS63). It lies along the top rear edge of the flap at y ≈ −30, z ≈ 37.
- **Function**: the **hinge barrel** of the flap (the flap pivots about the bar's axis, along X) and a **rubber bumper** on the highest point of the robot **(guess, medium)**. The hinge pin passes through the side walls' small holes.

### 2.4 Heel (HL), AWS62/63
- **Shape**: the rear end of the body: a **rounded top-rear corner** (radius about 12 mm) blending the sloped top into a short vertical rear wall (about 28 mm of straight wall below the arc). Seen in AWS62 at the top of the image as rounded corners at both sides of the black bar, and in AWS63 as the rounded upper end of the side wall.

### 2.5 Toe (TO)
- **Shape**: the front edge of the body, a **knife edge at floor level** across the full 70 mm width. The side walls taper to nothing at the toe (AWS63 shows the left wall coming to a **point**). Below the flap's front end, a short solid sloped face (about 10 mm long along the slope) continues the wedge down to the floor.
- **Material**: printed (AWS62/63); a **folded-down aluminium lip** in AWS64.

### 2.6 Base / floor (BF)
- **Seen**: through the open flap in AWS63, the inside floor is an **aluminium plate with a grid of round holes** (Ø about 4 mm, spaced about 8 mm).
- **Guess**: the structural floor, about **1.5 mm aluminium**, screwed to the bottoms of the side walls; the holes save weight and give mounting points. Slots for the wheels must be cut in it **(guess)**.

### 2.7 White block (WB) and inside parts (AWS63)
- **WB**: a **white printed block**, about **14 × 14 × 10 mm**, with a **round hole** (Ø about 4 mm) in its top and a second hole on its side, sitting on the floor at the front-left of the cavity (x ≈ −8, y ≈ +10). Likely a **pivot block for a linkage or a pillar for the flap screws** **(guess)**.
- **Black/white component**: about **12 × 8 × 10 mm**, at the rear right of the cavity, with **red wires** looping from it toward the front. Possibly the **switch**, a **servo** or a motor end **(guess)**.
- **Dark component**: a black block behind WB under the hinge (servo or battery) **(guess)**.
- **Red wires**: a red pair, about 22 AWG, running from the rear right forward around the white block.

### 2.8 AWS64 rebuilt body (aluminium)
- **Top plate (TP64)**: a flat **aluminium sheet**, about **70 mm wide × 62 mm long × 1 mm thick**. Its **front edge is folded down** as a sloped lip running to the floor (the toe), and its rear edge ends at the white hinge strip. **7 screws S-TP** (small Phillips/countersunk, heads Ø about 3 mm) are scattered over it: two near the front edge, two near the left edge, one at the centre, and two near the rear edge by the hinge.
- **Hinge strip (HS)**: a **white strip**, about **6 mm wide × 50 mm long**, along X, between the top plate's rear edge and the heel. It looks like a **plastic piano hinge** or a white printed knuckle bar. The top plate is therefore the flap, hinged at its rear edge, exactly as in AWS63.
- **Heel (HL64)**: the rear is a sheet **rolled into a large curl**, about **Ø 30 mm**, running the full width (70 mm). It carries **3 screws S-HL** along its top, fixing it to an inner frame. Its end shows the open curl of the sheet ("C" profile).
- **Side**: a folded aluminium side wall with "Slipper" in black marker.
- **Overall**: the AWS64 robot looks **flatter** than the AWS62 wedge; the slope is probably 15–20° **(guess)**.

### 2.9 Drive (hidden)
- **No wheels are visible** in any photo. For a full-body wedge the usual arrangement is **two wheels inboard**, through slots in the floor near the rear, with the toe and floor skidding **(guess, medium)**. The spec draft used two wheels of r 11 inboard.
- **Guess**: two N20 gearmotors with Ø 22 mm wheels at x = ±26, y = −20, protruding 1–2 mm below the floor.

---

## 3. Per-view descriptions

### 3.1 Top view (plan)
- A plain rectangle 70 × 95 mm. Inset in the middle, the flap (52 wide, about 70 long in plan), with its 4 × 5 window grid (two column pairs and a centre strip), two large slotted screws at its front end, and the black bar across its rear. The 6 mm side-wall rims frame it. The toe strip (about 10 mm) is in front of the flap; the rounded heel strip (about 12 mm) is behind the bar.

### 3.2 Front view
- A low trapezoid: knife edge at the floor (70 wide), the sloped top rising away from the viewer; the black bar at the top (z ≈ 32–42); the heel corners just visible. No wheels visible.

### 3.3 Left side view (AWS63 / AWS64)
- A right trapezoid: floor line 95 mm; the top line rising from the toe at about 26° to the heel; a quarter-round of radius 12 at the top rear, then a vertical rear edge. "Slipper" written along the slope. With the flap open (AWS63), a plate sticks up from the top-rear corner at about 40° above horizontal.

### 3.4 Rear view (inferred)
- A 70 × 40 rounded rectangle, the black bar on top. Possibly the switch access **(guess)**.

### 3.5 Isometric
- A silver doorstop with a perforated grey tile inset into its slope and a black roll on top.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| SW | trapezoid wall | 95 × 40 × 6 | 1.36 × 0.57 × 0.09 | silver-grey PLA | screws to BF (guess) | 2 |
| FL | perforated plate | 52 × 78 × 2.5 | 0.74 × 1.11 | grey PLA / aluminium | hinge at rear | 1 |
| windows | rectangles | 5 × 8 | 0.07 × 0.11 | — | — | 20 |
| BB | rubber-covered bar | Ø 10 × 52 | 0.14 × 0.74 | black | hinge pin | 1 |
| HL | rounded heel | R 12 corner, 70 wide | — | silver-grey | integral | 1 |
| TO | knife-edge strip | 70 × 10 | 1 × 0.14 | silver-grey / Al lip | integral | 1 |
| BF | perforated floor | 58 × 90 × 1.5 | 0.83 × 1.29 | aluminium | screws | 1 |
| S-FL | slotted round head | Ø 7 | 0.10 | silver | flap front | 2 (+1 small, +2 tiny) |
| WB | block | 14 × 14 × 10 | 0.2 | white PLA | on BF | 1 |
| TP64 | flat sheet | 70 × 62 × 1 | 1 × 0.89 | aluminium | 7 screws | 1 (AWS64) |
| HS | hinge strip | 6 × 50 | 0.71 | white | — | 1 (AWS64) |
| HL64 | rolled sheet | Ø 30 × 70 | 0.43 × 1 | aluminium | 3 screws | 1 (AWS64) |
| WH | wheel (hidden) | Ø 22 × 8 | 0.31 | — | motor shaft | 2 (guess) |
| SV | servo (hidden) | 23 × 12 × 23 | — | — | inside (guess) | 0–1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| TO edge ↔ floor | touching | 0–0.5 |
| BF bottom ↔ floor | clearance | 1–2 |
| WH bottom ↔ floor (guess) | contact | 0 |
| FL edges ↔ SW inner faces | side clearance | 1 |
| FL top ↔ SW rim top | recessed | −2 to −3 |
| FL front edge ↔ TO face | step | 1–2 |
| FL ↔ BB | joined | 0 |
| BB ↔ SW (hinge pin holes) | pinned | 0 |
| BB top ↔ HL top | about level | 0–2 |
| FL underside ↔ WB / SV | above | 2–5 when closed |
| SW ↔ BF | screwed (guess) | 0 |
| TP64 ↔ HS ↔ HL64 | hinged | 0 |
| S-FL heads ↔ FL top | proud | +2 |

---

## 6. Mechanism

1. **Drive** (hidden): two wheels under the body, skid steer, the toe sliding **(guess)**.
2. **Flap**: hinged at the top rear (about BB, axis along X at y ≈ −30, z ≈ 37). When opened, its **front (low) end lifts**, rotating the plate up about the rear hinge. Two readings:
   - **(a) Servo flipper / lifter**: a servo inside pushes the flap's underside; an opponent that has slid up the toe onto the flap is **tipped upward and backward**. A 78 mm flap rotating 60° lifts its front end by about 78·sin 60° ≈ 68 mm.
   - **(b) Access lid**: the flap opens for maintenance (AWS63 is in a pit tub, where robots are opened) and is screwed shut at the front by the two big slotted screws for fights.
   - The big slotted screws at the front suggest (b) in AWS62: they look like they **fasten the flap's free end to the body**. The spec draft calls the robot a flipper. **Reconciled: hinged lid, possibly servo-powered (low confidence on (a))**; build the hinge either way.
3. **Self-righting**: none visible. The rounded heel lets the robot **rock back onto its base** if tipped onto its rear **(design reading)**.

---

## 7. Assembly order (suggested rebuild)

1. Print the **two side walls** (or one U-shaped tub including toe and heel) in silver-grey.
2. Cut the **perforated aluminium floor BF**, cut wheel slots, and screw it to the walls' bottoms.
3. Mount the two **drive gearmotors** and wheels on the floor in the rear third.
4. Fit the **white block WB**, the **servo** (if used), the **battery, receiver, ESC and switch**, routing the red wires along the floor.
5. Make the **flap** (grey printed plate with 20 windows, or punched aluminium), fix the **rubber-covered bar** along its rear edge, and push the **hinge pin** through the side walls and the bar.
6. Close the flap and fasten its front with the **two slotted screws** (and the small centre screw).
7. Write "Slipper" on the left wall.
8. AWS64 variant: fold the aluminium top plate with the front lip, roll the heel sheet, join them with the white hinge strip, and screw on (7 + 3 screws).

---

## 8. Hidden / uncertain list
- Wheels and motors: entirely hidden.
- Whether the flap is powered.
- Flap material (printed vs aluminium) and the exact window count (AWS62 clearly 4 × 5; AWS63 a similar grid with smaller square holes).
- Function of the white block.
- AWS64 geometry beyond the top and left side.
- All sizes ±20% (low-resolution photos).

---

## 9. Coordinate frame (restated)
- Origin under the body centre; +X right, +Y forward (toe), +Z up; mm.
- Body: x ∈ [−35, +35], y ∈ [−45, +50], z ∈ [0, 40]. Toe at y = +50, z = 0. Heel top at y ≈ −33, z = 40. Flap hinge axis at (y −30, z 37), along X.

## 10. Profiles as math

**10.1 Body side profile (YZ, the side walls).**
- Bottom: z = 0 for y ∈ [−45, +50].
- Rear wall: y = −45 for z ∈ [0, 28].
- Heel arc: centre (y −33, z 28), r = 12, θ from 180° (rear) to 90° (top): (−45, 28) → (−33, 40).
- Top slope: from (−33, 40) to the toe (+50, 0): z = 40 − 0.482·(y + 33), slope atan(40/83) = 25.7°.
- The flap lies parallel to this rim, 2.5 mm lower.

**10.2 Flap FL (own plane: u down the slope from the hinge, v across).**
- Outline: u ∈ [0, 78], v ∈ [−26, +26].
- Windows: column centres v_c ∈ {−17, −8, +8, +17}, row centres u_r ∈ {12, 25, 38, 51, 64}; rectangles |v − v_c| ≤ 2.5, |u − u_r| ≤ 4.
- Screws: (u 72, v ±12) large, (u 72, v 0) small, (u 74, v ±22) tiny.
- Placement: hinge line (y −30, z 37); closed plate direction (cos 25.7°, −sin 25.7°) in (Y, Z). Opened by α about the hinge, the plate direction becomes (cos(25.7° − α), −sin(25.7° − α)); at α = 65° it points 39° above horizontal toward the front.

**10.3 Bar BB.** Cylinder r = 5 centred (y −30, z 37), x ∈ [−26, +26].

**10.4 AWS64 heel.** Rolled sheet: arc centred (y −30, z 15), r = 15, θ from −60° to 200° (open "C" at the bottom front), 1 mm thick, extruded along X over 70 mm.

## 11. Pixel-based measurements

**AWS62 (407 × 419 px):**
- Flap: x ≈ 125–335 at the top (y ≈ 75); x ≈ 160–335 at the bottom (y ≈ 385). Flap top y ≈ 70, bottom y ≈ 390.
- Window column centres about x = 160, 192, 245, 280 (row 1); rows at y ≈ 120, 165, 215, 265, 315.
- Front screws: (195, 360) and (300, 365); small centre (260, 350).
- Black bar: x 85–345, y 25–70.
- Left wall rim: x 20–125; right wall rim x 335–370.

**AWS63 (320 × 279 px):**
- Left side wall from the heel (x 10–80, y 100–140) to the toe point (x 205, y 255).
- Flap: from the black bar (x 50–175, y 30–100) to the free end (x 275, y 60).
- White block: x 125–180, y 145–195. Red wires: x 190–235, y 130–225.

**AWS64 (390 × 294 px):**
- Top plate: x 30–260, y 25–235. Hinge strip: x 260–275, y 50–190. Heel: x 275–360, y 10–270.
- Screws: about (80, 95), (165, 80), (75, 150), (160, 135), (65, 205), (250, 65), (250, 180).
- "Slipper" text: x 185–265, y 240–260.

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | 80 (spec) | flap 52 + 2 × 6 walls + 2 × 1 clearance + 2 × 2 = 70 | AWS62: flap 0.6 of the visible top width at the bar, 0.74 at the toe → 70–87 | **70** |
| Body length | 110 (spec) | cube limit 101.6 | AWS64: length 330 px vs width 260 px → 1.27 W = 89; AWS63 side ≈ 1.35 W = 95 | **95** |
| Rear height | 48 (spec) | 0.57 W = 40 | AWS63: side triangle height/length ≈ 0.4 → 38 | **40** |
| Slope | long ramp (spec) | atan(40/83) = 25.7° | AWS63: 22–28° | **25.7°** |
| Flap length | — | 0.82 of the body length = 78 | AWS62: 320 px long vs 210 px wide (52 mm) → 79 (foreshortening cancels roughly at this view) | **78** |
| Window size | — | — | AWS62: 25 × 40 px at 4 px/mm → 6 × 10 | **5 × 8** |
| Bar Ø | — | 0.14 W | AWS62: 45 px / 4 px/mm → 11 | **10** |
| Heel Ø (AWS64) | — | 0.43 W | AWS64: 85 px of 260 px (70 mm) → 23 (curl partly hidden) | **30** |

## 13. Consistency check: conflicts and reconciliation
1. **Length vs the cube**: the spec's 110 mm body does not fit a 101.6 mm cube. Photos give 1.3–1.4 W. **Reconciled 95 mm.**
2. **Height**: the spec's 48 mm vs ratio 40 mm; 40 also gives the photographed ~26° slope. **Reconciled 40.**
3. **Flap material**: printed grey (AWS62) vs punched aluminium (AWS63): two versions or a printed frame with an aluminium skin. **Reconciled: printed 2.5 mm plate; AWS63 variant aluminium 1 mm.**
4. **Hinge location**: AWS63 shows rotation about the black-bar end, so the hinge is **rear/top**; consistent with AWS64's hinge strip at the rear of the top plate.
5. **Powered or not**: no horn or link is visible. **Reconciled: hinged lid, optionally servo-flipped; model the hinge as a revolute joint 0–65°.**
6. **Wheels**: unseen; two inboard wheels assumed.

---

## 14. Why the designer did it (per part, adversarial first)

- **Full-body wedge (toe to heel)**
  - Fight: a full-body wedge has no exposed vertical faces at the front: an opponent driving at it meets a slope and is **steered upward**. The thin toe gets **under** opponents, lifting their front so they lose traction while Slipper pushes. Against **vertical spinners**, a 26° slope deflects the disc upward rather than taking it squarely; against **horizontal spinners**, there are no corners above the floor to bite.
  - Being got under: the toe must be lower than the opponent's wedge. A printed toe cannot be as sharp as steel; this is the **main weakness**, which the AWS64 rebuild addresses by folding an aluminium lip at the front.
  - Rear: the **rounded heel** lets a robot pushed onto its back rock back onto its base, and a hit on the rear is deflected rather than caught on a square corner.
- **Thick side walls standing proud of the flap**
  - Fight: the walls are the structural rails taking hits; the recessed flap means a spinner sliding over the top meets the wall rims, not the flap edges. The walls taper to a point at the toe so they do not catch on opponents.
  - Construction: thick walls make the body stiff without ribs; the flat rims are easy to screw into.
- **Perforated flap**
  - Fight: 20 windows **save weight** (about 40% of the plate) while keeping a stiff frame, and make the flap light enough for a small servo to move it quickly if powered.
  - Threat: a spinner tooth could catch in a window; the holes are small and the slope makes teeth slide across them.
  - Construction: the windows show the electronics (status LED) without opening the robot.
- **Black rubber bar on the hinge**
  - Fight: the highest point is soft: it hits the wall or floor when the robot is flipped, and protects the hinge from direct hits. Rubber grips when the robot lands on its back, helping it rock over **(guess)**.
  - Construction: the bar doubles as the hinge barrel, so no separate knuckles are needed.
- **Large slotted front screws**
  - Construction: can be undone with a coin or any flat screwdriver in the pits; they lock the flap closed.
  - Fight: round heads low on the slope help opponents slide rather than catch.
- **Perforated aluminium floor**
  - Fight: the stiffest member; it carries the motors and takes floor impacts when the robot is slammed down. Holes save weight.
- **AWS64 aluminium rebuild**
  - Fight: an all-aluminium shell dents rather than shatters under spinner hits; the folded lip gives a **thin, sharp toe** to get under opponents; the **rolled heel** is a strong curved section that resists crushing and acts as a rocker.
  - Construction: sheet bent by hand, screwed to an inner frame; the white hinge strip opens the whole top for access.
- **Hidden wheels**
  - Fight: no wheel can be hit; but small inboard wheels give little clearance and modest pushing grip, and the robot **cannot drive inverted**; the rounded heel and low centre of gravity are the defence against flips.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors, 6 V, 300–500 rpm | 12 × 10 × 25 | along X, x ±14, y −20, z 9 | medium |
| Wheels | Ø 22 × 8 printed hubs with O-ring or TPU tyres | Ø 22 × 8 | x ±26, y −20, z 11, through floor slots | medium |
| Flap servo | 9 g servo (only if powered) | 23 × 12 × 23 | x +10, y −15, z 14, horn under the flap | low |
| Linkage | horn pushing the flap underside, or a link to the white block's hole | 20 mm horn | near WB | low |
| Battery | 2S 180–300 mAh LiPo | 40 × 18 × 9 | x 0, y +5, z 6 on the floor | medium |
| ESC | dual brushed micro ESC | 20 × 15 × 5 | x −10, y −30, z 6 | medium |
| Receiver | micro 2.4 GHz | 18 × 12 × 5 | x +12, y −32, z 8 | low |
| Switch | slide switch (the black/white component) | 12 × 8 × 10 | x +18, y −35, z 10 | low |
| Wall screws | M3 from underneath through BF into the walls | — | 4–6 per side | low |
| Wiring | battery → switch → ESC → motors; red leads around the white block | — | under the flap | medium |

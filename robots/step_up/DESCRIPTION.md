# Step Up: full rebuild description from reference photos

Source photos:
- `robots/step_up/reference/step_up.aws72.webp`: AWS 72, 1294 × 1428 px, cut out onto white, sharp. **Front-left three-quarter view from about 40° above.** The **white front bumper plate** is nearest the camera at the lower left, the body is wrapped in **bright green tape** printed with black **"Step up"** lettering, and a **tall white paddle** covered in torn **silver foil tape** stands up from the far (rear) end. Four black-tyred wheels with **grey/silver hubs**.
- `robots/step_up/reference/step_up.aws64.webp`: AWS 64, 1147 × 1055 px, on a white plastic surface (table/arena), sharp. **Left-rear three-quarter from about 45° above.** Body wrapped in **blue painter's tape** with yellow letters "STEP UP" (reading "UP" then "STEP" upward) and a **crumpled gold/yellow paper** at one end. The paddle is white with a **red translucent card bearing a black "!"**. Wheels have **white three-spoke hubs**. A **white curved channel** (a length of white plastic trunking or a scoop) lies at the right, beside the clear base plate. The underside shows a **clear acrylic base plate**, a brass N20 gearbox, red-painted spots and an orange/red/brown **servo lead**.
- `robots/step_up/reference/step_up.aws65.webp`: AWS 65, 763 × 729 px, on a wooden table, held by a finger at the upper left; a black/orange **hot-glue gun** at the bottom (not part of the robot). **Top view from the paddle end, about 60–70° down.** Body wrapped in **Mondrian-style paper** (black grid lines with red, blue and yellow blocks and the words "STEP UP"). The paddle (white with the pink/red "!" card) stands up in the middle, facing the camera. A white front bumper with a blob of white hot glue is at the bottom.

Step Up is a **simple, home-made four-wheel robot with a servo-driven paddle** (a flipper/self-righting paddle; the spec draft calls it a lifter). It is built from **white plastic sheet**, a **clear acrylic base**, **N20 gearmotors**, **hobby-kit wheels** and lots of **tape**. Everything stated as fact is read from the photos; anything inferred is marked **(guess)**. All mm values are **estimates** (±15%), scaled from the hobby wheel (black ribbed tyre on a 3-spoke hub, normally **Ø 34 × 7 mm**) and from the AWS 101.6 mm (4 in) cube. Ratios are given against **W = body width between the wheels ≈ 62 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the white bumper plate), **+Z** = up; mm. **Origin** = the point on the floor (z = 0) under the centre of the body footprint (mid-width between the wheel rows, mid-way between the front and rear axles). Side-profile angles are measured from the floor; paddle angles are measured from vertical, positive leaning backward (toward −Y).
- **Front** = the end with the **white bumper plate** (AWS72 nearest the camera; AWS65 at the bottom of the image). **Rear** = the end the paddle leans toward.
- **Note**: which end is "front" cannot be proved; the bumper end is chosen because the bumper is a pushing face and the paddle sits nearer the other end.

| ID | Part |
|---|---|
| BP | clear acrylic base plate |
| BD | body box (white plastic sheet walls), tape-wrapped |
| WR | wrap: green tape (AWS72), blue tape + gold paper (AWS64), Mondrian paper (AWS65) |
| FB | front bumper plate (white plastic sheet) |
| SC | white curved channel lying beside the robot (AWS64; a scoop or loose part) |
| PD | paddle plate (white sheet) |
| PD-F | paddle face covering: silver foil tape + green tape (AWS72), red "!" card (AWS64/65) |
| PA | paddle arm/strip (vertical white strip joining the paddle to the servo) |
| PA-S | wood screws through the paddle arm (two tips seen) |
| SV | paddle servo (hidden except the lead) |
| SV-W | servo lead (orange/red/brown) |
| WH-FL, WH-RL, WH-FR, WH-RR | four wheels: black ribbed tyres on 3-spoke hubs |
| DM | drive gearmotors (N20, brass gearbox seen) |
| AX | wheel hub screws (silver, at the hub centres) |
| HG | hot-glue blobs (white) |
| RP | red paint spots on the base (AWS64) |
| BAT, RX, ESC, SW | battery, receiver, ESCs, switch (hidden, guess) |

---

## 1. Overall description in one paragraph

Step Up is a **small, boxy four-wheeler** about **80 mm wide over the wheels, 95 mm long and 24 mm tall at the body**, with a **paddle that stands up to about 85 mm**. The body is a low box of **white plastic sheet** on a **clear acrylic base plate**, completely **wrapped in tape or paper** that carries the name "Step Up". Four **hobby-kit wheels** (black ribbed rubber tyres on three-spoke hubs, about Ø 34 × 7) stand **outboard of the body at the four corners**. Their tops are well above the body, so it can drive upside down. Across the front is a **flat white bumper plate**, nearly vertical and leaning back a little, scratched from use. Near the rear, a **narrow vertical white strip** rises out of a slot in the top, held by **screws** to a hidden **hobby servo**. On top of the strip is a **rectangular white paddle** about **35 × 55 mm**, leaning backward at about **15–25°** from vertical. Its face carries a **red translucent card with a black "!"** or, later, **silver foil tape** with a **strip of green tape**. The servo swings the paddle over to push the robot back onto its wheels after being flipped, and to **"step up"** over or flip an opponent **(guess)**.

---

## 2. Part-by-part description

### 2.1 Base plate (BP)
- **Shape**: a flat **clear acrylic sheet** about **2 mm thick**, roughly **62 × 90 mm**, forming the floor of the body. In AWS64 its edge is seen as a clear rim, about 3–5 mm wider than the body walls at the near corner, with **red paint dots/marks** on it (marker or nail varnish). In AWS65 it shows as a clear edge under the right rear corner.
- **Height**: underside at about **z = 6** (ground clearance about 6 mm, set by the axle height of the N20 motors mounted on it) **(guess)**.

### 2.2 Body box (BD) and wrap (WR)
- **Shape**: a low box about **60 mm wide × 85 mm long × 18 mm tall** (on the base), top at about **z = 26**. The walls are **white plastic sheet** (styrene or PVC foam board, about **2 mm**), visible at the cut edges and through tears in the wrap. The edges are slightly rounded by the wrap.
- **Top**: flat, about 60 × 85, with a **slot about 10 × 6 mm** near the rear centre (at about (0, −20)) where the paddle strip comes out. In AWS72 the green tape is **torn and lifted** around the slot and at the right rear corner.
- **Wrap**:
  - **AWS72**: **bright lime-green tape** (sticky-note green, like frog tape or masking tape), wrapped around the top and sides, with **"Step up"** written in large black lower-case letters across the top (about 12 mm tall letters). It is wrinkled and lifting at the right rear.
  - **AWS64**: **blue painter's tape** across the front half with **yellow capital letters "STEP UP"** (the letters run along the robot), and **crumpled metallic gold/yellow paper** over the rear half; badly torn at the near corner, exposing the motor and the clear base.
  - **AWS65**: **white paper printed in a Mondrian pattern**: black grid lines about 1 mm thick dividing white, **red**, **blue** and **yellow** rectangles, with "STEP UP" in black capitals in one white block at the upper left.
- **Wall gaps**: AWS65 shows a gap between the body's side and the near-side wheels where white plastic posts and the brass N20 gearboxes are visible.

### 2.3 Front bumper (FB)
- **Shape**: a flat **white plastic plate** about **64 mm wide × 22 mm tall × 2 mm thick**, across the front end between the front wheels, at about **y = +46**. It leans **back about 10–15°** from vertical (top toward the body). Its top edge is level with the body top (z ≈ 26) and its bottom edge about 3–4 mm above the floor.
- **Surface**: matte white, **scratched and scuffed** (crossed scratch marks) in AWS72; edges cut square.
- **AWS65**: a white bumper strip at the near (bottom) end, with a **blob of white hot glue** on its top edge and a smear of grey glue.
- **Fixing**: glued (hot glue) to the body's front wall and base **(guess, high)**.

### 2.4 White curved channel (SC) (AWS64)
- **Shape**: a **white plastic channel** about **95 mm long**, with a **U or J cross-section** (about 15 mm wide, 10 mm deep), lying on the table at the right of the robot, roughly parallel to its right side. Near one end it has a **rectangular notch** about 12 × 6 mm cut into one flange.
- **Status**: it is **not clearly attached** to the robot: it lies beside the clear base plate. It could be a **detached front scoop** (a curved ramp that clips to the front), a part of the arena/table, or a spare **(guess, low)**. It is not modelled as part of the robot unless needed.

### 2.5 Paddle (PD), paddle face (PD-F) and paddle arm (PA)
- **Paddle plate PD**: a flat **white plastic rectangle** about **34 mm wide × 55 mm tall × 2 mm thick**, with square corners (one corner slightly bent in AWS72). In AWS65 it shows as a **white rectangular frame** with a **pink/red card** occupying its middle (about 26 × 46 mm), leaving a white border of about 4 mm.
- **Face covering PD-F**:
  - **AWS64/65**: a **red translucent card** (like a red plastic file divider) about **26 × 46 mm** with a large black **exclamation mark "!"** (a long wedge-shaped bar and a round dot, which may be a hole with a screw/rivet), and two lines of tiny dark text at the bottom ("... Do not ...", illegible).
  - **AWS72**: the face is covered with **silver foil tape** (crinkled, torn, with black scuffs and white plastic showing through), and a **strip of green tape** about 10 mm tall across the lower right corner. The paddle back (left edge seen in AWS72) is **white** with green tape traces.
- **Paddle arm PA**: a **narrow vertical white strip** about **8 mm wide × 2–3 mm thick × 30 mm long**, joined to the lower part of the paddle's back (the paddle plate overlaps it by about 10–15 mm). It goes down through the top slot to the servo horn. In AWS72 **two pointed wood-screw tips** stick out of its right face just above the body top (at about z = 30 and 33): screws driven through the servo horn into the strip, too long, so their tips poke through. AWS64 shows the same two screw tips and the white strip; AWS65 shows two screw heads (silver) beside the paddle base at the right, at the body top.
- **Angle at rest**: in AWS72 the paddle leans **back about 20°** from vertical (top toward −Y) and is twisted about 10° about Z. In AWS64 it leans **back about 35°**. In AWS65 it stands nearly upright, facing the camera.
- **Overall height**: paddle top at about **z = 80–85**.

### 2.6 Servo (SV) and lead (SV-W)
- **Seen**: only its lead: an **orange, red and brown three-core servo cable** looping under the torn tape at the right side in AWS64 at about (+20, −10, 12). The servo body is hidden in the body under the paddle slot **(guess)**.
- **Guess**: a **9 g micro servo** (23 × 12 × 23 mm, output spline along X) lying with its output shaft along **X**, so the paddle swings in the YZ plane **(medium)**.

### 2.7 Wheels (WH)
- **Size**: **Ø 34 mm** tyres, **7 mm wide**, black rubber with **fine straight transverse ribs** (about 50 ribs), on **three-spoke hubs**: **white** plastic (AWS64, AWS65) or **light grey/silver** (AWS72; same shape, possibly painted or a different batch). Each hub has a **small silver screw** at the centre (AWS64) fixing it to the motor shaft.
- **Positions**: at the four corners, **outboard** of the body: centre planes at **x = ±38** (inner faces at ±34.5, outer at ±41.5). Front axles at **y = +32**, rear axles at **y = −32** (64 mm wheelbase). Axle height **z = 17**.
- **Height**: wheel tops at **z = 34**, about **8 mm above the body top**, so the robot can drive inverted (the paddle would then be underneath; see §6).

### 2.8 Drive motors (DM)
- **Seen**: a **brass N20 gearbox** inboard of the near front wheel in AWS64 at about (−26, +28, 15) and a **brass gearbox** at the right front in AWS65 at about (+26, +28, 15), with white plastic clamp blocks around them.
- **Guess**: **four N20 gearmotors**, one per wheel, lying along X with their shafts out to the wheels, glued or clamped to the base plate **(medium)**; or two driven wheels and two idlers (low).

### 2.9 Hot glue (HG), paint (RP), wires and switch
- **HG**: white hot-glue blobs on the bumper top (AWS65), along the paddle strip base and body edges **(seen in places)**.
- **RP**: **red paint/marker spots** on the clear base plate near the front right wheel in AWS64.
- **Wires**: the servo lead (orange/red/brown); green and red thin wires are glimpsed near the front motor in AWS64.
- **Switch**: not visible **(guess: under the tape at the rear)**.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 AWS72 (front-left, 40° down)
- **Outline**: a low **green box** with four black wheel discs at the corners and a **white rectangular bumper** across the near end, plus a **tall rectangular paddle** rising from the far end like a sign, leaning away and to the right. The paddle's top is the highest point of the image.
- **Details**: "Step up" in black on the green top, torn green tape at the paddle base and right rear, two screw tips on the paddle strip, grey hubs.

### 3.2 AWS64 (left-rear, 45° down)
- **Outline**: the box with the gold paper end at the upper left and the blue tape band, four wheels with **white three-spoke hubs** (the near two large and clear), the **paddle with its red "!" card** leaning over toward the upper left, and the white channel lying at the right.
- **Details**: torn tape at the near corner exposing the N20 gearbox, servo lead, red spots and the clear base.

### 3.3 AWS65 (top, from the paddle side, 60–70° down)
- **Outline**: a **rectangle** (the Mondrian-wrapped body) with four wheels at the corners (seen edge-on as black ribbed bars), the paddle standing up in front of the camera covering the middle, and a white bumper strip at the bottom.

### 3.4 Top view (synthesised)
- A 60 × 85 rectangle with 7 × 34 wheel rectangles at the corners (overall 83 × 98), a 64 × 2 bumper line across the front, and the paddle seen as a 34 × (55 × sin 20° ≈ 19) rectangle behind the slot at y ≈ −20.

### 3.5 Side view (synthesised, left)
- A 85 × 20 box on a 2 mm base 6 mm off the floor, two Ø 34 wheels whose tops stick 8 mm above the box, the bumper a near-vertical line at the front, and the paddle a 55 mm line from (y −20, z 30) leaning back 20° to (y −39, z 82).

### 3.6 Rear view (inferred)
- The rear wall of the box between the rear wheels; the paddle face above it, facing rearward-up.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W (62) | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BP | flat sheet | 62 × 90 × 2 | 1 × 1.45 | clear acrylic | base | 1 |
| BD | box | 60 × 85 × 18 | 0.97 × 1.37 × 0.29 | white plastic sheet | hot glue | 1 |
| WR | wrap | covers BD | — | green tape / blue tape + gold paper / Mondrian paper | adhesive | 1 |
| FB | flat plate | 64 × 22 × 2 | 1.03 × 0.35 | white plastic | hot glue | 1 |
| SC | U-channel | 95 × 15 × 10 | 1.5 | white plastic | loose (AWS64) | 0–1 |
| PD | flat plate | 34 × 55 × 2 | 0.55 × 0.89 | white plastic | glued to PA | 1 |
| PD-F | card / foil | 26 × 46 | — | red card with "!" / silver foil + green tape | adhesive | 1 |
| PA | strip | 8 × 30 × 2.5 | 0.13 × 0.48 | white plastic | 2 wood screws to the servo horn | 1 |
| PA-S | wood screw | Ø 2 × 10 | — | steel | through horn + PA | 2 |
| SV | micro servo | 23 × 12 × 23 | 0.37 | (hidden) | glued | 1 |
| WH | wheel | Ø 34 × 7 | 0.55 × 0.11 | black rubber, white/grey 3-spoke hub | motor shaft + screw | 4 |
| DM | N20 gearmotor | 12 × 10 × 25 | — | brass/silver | clamp/glue | 4 (guess) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| BD walls ↔ BP | glued | 0 |
| WR ↔ BD | stuck on | 0 |
| FB ↔ BD front wall / BP | glued | 0 |
| FB bottom ↔ floor | above | 3–4 |
| FB ends ↔ WH-F tyres | side by side | 1–3 |
| PA ↔ servo horn | screwed | 0 |
| PA ↔ BD top slot | passing through | 1–2 |
| PD ↔ PA | glued/overlapping | 0 |
| PD bottom edge ↔ BD top | above | 4–8 |
| PD ↔ WH-R tyres | clear (paddle narrower than body) | ~10 sideways |
| WH inner face ↔ BD side / BP edge | near | 1–3 |
| WH ↔ DM shaft | fixed | 0 |
| DM ↔ BP | glued/clamped | 0 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ BD top | wheel above | +8 |
| BP underside ↔ floor | clearance | 6 |
| SC ↔ robot | not attached (AWS64) | — |

---

## 6. Mechanism

1. **Drive**: four-wheel skid steer on N20 gearmotors **(guess: 4 motors)**.
2. **Paddle**: a hobby servo rotates the paddle about an **X axis** at about **(0, −20, 22)**. At rest it leans back 20–35°. Swinging it **forward** (toward +Y) would **slap down onto an opponent over the front** (a hammer-like action) or push it. Swinging it **backward** past horizontal pushes against the floor behind the robot, **lifting the rear and flipping the robot back over** (self-righting). The paddle, 55 mm long on a 30 mm arm, reaches about 80 mm from the pivot, enough to push the robot over if it lands on its back **(guess, medium)**.
3. **Inverted**: the wheels stick out 8 mm above the body, so it can drive inverted, but the paddle would be underneath. Hence a self-righter.
4. **Bumper**: a passive pushing face.

---

## 7. Assembly order (suggested rebuild)

1. Cut the clear acrylic base.
2. Glue four N20 gearmotors to the base at the corners, shafts outward; press on the wheels and screw the hub screws.
3. Glue the servo upright near the rear centre with its output along X.
4. Fit the battery, receiver and dual ESC (or motor driver) in the remaining space; route the wires.
5. Build the body walls and top from white sheet around everything, leaving a slot for the paddle arm; hot-glue.
6. Glue the bumper across the front.
7. Screw the paddle arm to the servo horn (two wood screws), glue the paddle onto it, apply the face card or foil.
8. Wrap the body in tape/paper and write the name.

---

## 8. Hidden / uncertain list
- Which end is the front (the bumper end is assumed).
- Paddle pivot axis and servo orientation.
- Motor count (4 vs 2).
- The white channel in AWS64.
- Battery, electronics and switch.
- All mm ±15% (wheel Ø 34 is the anchor).

---

## 9. Coordinate frame (restated)
- Origin on the floor under the body footprint centre; +X right, +Y forward (bumper), +Z up; mm.
- Body x ∈ [−30, +30], y ∈ [−42.5, +42.5], z ∈ [6, 26]. Wheels: centre planes x = ±38, axles y = ±32, z = 17, Ø 34. Bumper plane y ≈ +46 (bottom) leaning to y ≈ +43 (top), z 4–26. Paddle pivot (0, −20, 22); paddle plate from z ≈ 30 to 82.
- Overall bounding box at rest: **83 × 98 × 82** (fits the 101.6 cube).

## 10. Profiles as math (for rebuilding curves)

**10.1 Paddle line (YZ plane, at rest, AWS72).** The arm runs from the pivot P = (y −20, z 22) at an angle θ = 20° back from vertical. A point at distance s from P along the arm/paddle is (y, z) = (−20 − s sin θ, 22 + s cos θ). The arm is s ∈ [0, 30], the paddle plate s ∈ [15, 64] (overlapping 15 mm). The top edge is at s = 64: (y −41.9, z 82.1).

**10.2 Paddle sweep.** The top edge circle: (y + 20)² + (z − 22)² = 64². Forward position θ = −90° puts the top edge at (y +44, z 22), just ahead of the front axle, i.e. the paddle lies flat over the top and the bumper. Backward θ = +110° reaches (y −80, z 0): **it touches the floor 80 mm behind the pivot**, enough to lever the body over.

**10.3 Bumper.** Plane through (y +46, z 4) and (y +43, z 26): lean atan(3/22) ≈ **8°** back from vertical (10–15° in the photo, perspective).

**10.4 Wheels.** (y ∓ 32)² + (z − 17)² = 17². Hub: three spokes at 120°, each about 6 mm wide, from a Ø 8 boss to the Ø 26 rim.

**10.5 Wrap lettering.** "Step up" baseline along the body's long axis (Y), letters about 12 mm tall, starting at y ≈ +30 and reading toward −Y, so that the letters sit across the body width. (Decorative.)

## 11. Pixel-based measurements (independent check)

- **AWS72** (scaled to 1400 tall, factor 0.98): front-right wheel (nearest) vertical extent ≈ **330 px** at y_px 1000–1330, width ≈ 130 px (seen at an angle). Front bumper width from its left end (110, 880) to its right end (860, 1090) ≈ **780 px**; its height ≈ **190 px**. With the near wheel 330 px = 34 mm: bumper ≈ **80 mm** wide (the bumper is farther from the camera than the wheel only at its left end, so this is a slight overestimate) → **64–75 mm**. Height ≈ **20 mm** ✓.
- **AWS72** paddle: width ≈ **270 px** (at the top, x 750–1040), height ≈ **480 px** (y 30–510). It is farther from the camera than the near wheel (about 1.3×), so the scale is ≈ 330/1.3 = 254 px per 34 mm → paddle ≈ **36 × 64 mm**. Slightly larger than the ratio estimate; the paddle leans toward the camera's upper side, which elongates it a little. **Use 34 × 55–60.**
- **AWS64**: near wheel ≈ **220 px** across. Red card ≈ 300 × 360 px seen obliquely; paddle long edge ≈ 470 px → 470/220 × 34 ≈ **73 mm**, overstated (the paddle is nearer the camera, leaning toward it). Corrected ≈ **55–60**.
- **AWS65**: the top-right wheel, seen edge-on from above, spans about **190 px** along Y. It is foreshortened by the steep top view (about 34 × cos 25° ≈ 31 mm), giving about **6.1 px/mm**. The span between the left and right wheel rows is about **540 px** (x 95 → 635), which gives **88 mm**. That is close to the outer-face width, not the inner one, and the camera is nearer the wheels than the body; see §13.1.

## 12. Several independent estimates of key sizes

| Quantity | Method A (parts / rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Wheel Ø | kit wheel 34 | — | anchor | **34** |
| Body width | ≤ 101.6 − 2 × 7 − gaps | 1 W | AWS72 bumper 64–75; AWS65 ≈ 70–88 | **62** (inner face spacing 69) |
| Body length | wheelbase 64 + wheel radius | 1.37 W = 85 | AWS72 ≈ 2.6 wheel Ø = 88 | **85** |
| Overall length | ≤ 101.6 | — | 64 + 34 = 98 | **98** |
| Body height | — | 0.29 W = 18 + base 8 | AWS72 body top ≈ 0.75 wheel Ø = 26 | **26 (top)** |
| Paddle | — | 0.55 × 0.89 W | AWS72 36 × 64; AWS64 55–60 | **34 × 55** |
| Paddle top height | — | — | AWS72 ≈ 2.4 wheel Ø = 82 | **82** |

## 13. Consistency check: conflicts and reconciliation
1. **Body width**: AWS65 pixels suggest inner tyre spacing up to 88 mm, but with Ø 34 × 7 wheels and the 101.6 limit, the outer faces must be ≤ 101.6 → inner spacing ≤ 87. AWS72 shows the bumper (64–75 wide) fitting between the front tyres with a 1–3 mm gap each side → inner spacing ≈ **70**. AWS65 also includes the wrap bulging and the camera nearer the wheels. **Reconciled: wheel inner faces at ±34.5 (69 apart), body 60–62 wide, overall 83.**
2. **Paddle size**: 64 mm (AWS72 pixels) vs 55 (ratio). The paddle overlaps the arm by 15 mm; total paddle+arm ≈ 64 from the pivot. **Reconciled: plate 55 tall, top at s = 64 from the pivot.**
3. **Paddle angle**: 20° (AWS72), 35° (AWS64), ~0° (AWS65). The servo holds different positions in different photos: **it moves**, which confirms it is actuated.
4. **Wheel hub colour**: white (64/65) vs grey (72): different hubs, same size.
5. **Front/rear**: AWS65's top view puts the bumper at the near end and the paddle in the middle-rear. AWS72 has the bumper near and the paddle far. Consistent: bumper = front.
6. **Spec says lifter**: a paddle that lifts by levering is close enough; the description treats it as a **servo paddle (flipper/self-righter)**.

---

## 14. Why the designer did it (per part, from several angles)

Common lens: **adversarial**. For each part: what can attack it (spinners, wedges, lifters, flippers, wall slams, inversion), how it survives, and how it helps win. Then construction reasons. This is clearly a **beginner/young builder's robot** built from craft materials; many reasons are about cost and ease.

- **Servo paddle**
  - Fight: the robot's only active part. Its main job is probably **self-righting**: a box with 34 mm wheels can still drive inverted, but the paddle makes sure it can get back the right way up and keep the bumper useful. It can also **hit down** on an opponent that drives up the front, or **push** opponents away at the rear. A big flat paddle is easy to aim.
  - Weak points: a tall paddle is the first thing a spinner hits (AWS72's torn foil and bent corner show this); a 9 g servo strips easily under shock.
  - Construction: a servo with a horn and two screws is the simplest actuator; no gears or bearings.
- **"!" card and silver foil on the paddle**
  - Character: a warning sign ("!") as decoration; the foil adds a little toughness and slipperiness.
- **Front bumper**
  - Fight: a flat face to push opponents and to protect the front of the box. Leaning back slightly helps it ride over a little rather than catch.
  - Weak points: not low enough to get under opponents (3–4 mm above the floor): a wedge will get under it.
- **Tape/paper wrap**
  - Fight: holds the box together and keeps debris out; light.
  - Construction: cheap and colourful; easy to redo between events (three different wraps in three events).
- **White plastic sheet body on a clear base**
  - Construction: cuts with a knife, glues with hot glue; the clear base makes it easy to see wiring.
  - Weak points: weak against any real weapon; held together largely by glue and tape.
- **Hobby wheels outboard, larger than the body**
  - Fight: tall wheels let it drive inverted and get over small arena seams; four-wheel drive gives pushing grip.
  - Weak points: exposed wheels are easy to hit and the hubs are brittle plastic.
  - Construction: standard kit wheels that press onto N20 shafts.
- **Screws poking through the paddle arm**
  - Construction: the screws are longer than needed; quick fix rather than a design choice.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors along X | 12 × 10 × 25 | (±22, ±32, 17) | medium |
| Motor mounts | white plastic blocks + hot glue on the base | 14 × 12 × 10 | at each motor | medium (white blocks seen) |
| Servo | 9 g micro servo, output along X | 23 × 12 × 23 | (0, −20, 18) | medium |
| Battery | 2S 150–300 mAh LiPo or 1S | 35 × 20 × 8 | (0, +10, 10) | low |
| Receiver + ESC | combined antweight board or 2 small brushed ESCs | 25 × 15 × 5 | (0, +25, 12) | low |
| Switch | slide switch or link under the wrap at the rear | 10 × 5 × 5 | (0, −42, 15) | low |
| Wiring | servo lead (seen), motor leads | — | inside | high |
| Paddle hinge | none: the servo horn is the only bearing | — | — | medium |

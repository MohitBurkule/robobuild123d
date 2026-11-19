# Duck (Duck-ling): full rebuild description from reference photos

Source photos (all three cut out onto white; the files are named `duck_ling_`):
- `robots/duck/reference/duck_ling_.aws72.webp` (**primary**): AWS 72. **Front-left three-quarter from above**, camera about 40° above the floor. **Black** body; **white flipper panel** with a hand-drawn **blue-and-white duck face** with an orange-red bill; **black C-shaped hinge clips** at the panel's rear corners; a **salmon/coral front wedge plate** with **eight screws** along its top and a **silver metal strip** under its leading edge; **clear/green tape** over the rear top.
- `robots/duck/reference/duck_ling_.aws71.webp`: AWS 71. **Front-right three-quarter from above** (front to the image left). Black body; **orange flipper panel** (a plain printed panel, two shades), black hinge clips, and instead of the wedge plate a **blue printed fork bar** with **three tines** and a row of countersunk holes, held by three silver screws. The curved rear and the rear wheel tread (under clear tape) are visible.
- `robots/duck/reference/duck_ling_.aws67.webp`: AWS 67, earlier. **From the front, high** (≈ 55°). **Orange** body with an **integral front ramp** and a **silver metal strip** under its leading edge; **white flipper panel** with the duck face and the hand-written name **"DUCK LING"** in red; **translucent blue hinge clips** each screwed with **three small screws** onto blue brackets; **pale translucent orange gear-tread wheels** peeking at the rear corners.

`REFERENCE.json`: `flipper`, 2 wheels, weapon flipper, axis x, position **middle**, width_frac **0.53** (the flipper panel is about half the robot's width, mounted in the middle of the top).

Pixel coordinates refer to copies scaled to 1200 px on the long side (AWS72 → 1200 × 947, AWS71 → 1200 × 885, AWS67 → 1200 × 1096), ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit. Ratios use **W = body width ≈ 88 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the wedge/forks), **+Z** = up. **Origin O** = floor point under the centre of the body footprint (excluding the front wedge plate/forks).
- Flipper angle **φ** = angle of the panel above its rest plane, about the hinge axis (along X) at its rear.

| ID | Part |
|---|---|
| CH | body (black in AWS71/72, orange in AWS67): a wedge-shaped shell with a curved rear |
| RC | rounded rear (quarter-cylinder sides) |
| TR | top recess (pocket) in which the flipper panel lies |
| FP | flipper panel (white with duck face; orange in AWS71) |
| FP-D | duck drawing / name on FP |
| HC-L / HC-R | C-shaped hinge clips at FP's rear corners |
| HB-L / HB-R | hinge clip brackets (blue in AWS67) with screws |
| HA | hinge axle (hidden, transverse) |
| WP | front wedge plate (salmon, AWS72) |
| WP-S | screws along WP's top edge (8) |
| ME | metal strip under the leading edge (AWS67/72) |
| FB | blue fork bar with three tines (AWS71) |
| FB-T | fork tines |
| FB-S | screws on FB (3) |
| WH-L / WH-R | rear drive wheels (inside the rear corners) |
| TP | clear/green tape over the rear top |
| SV | flipper servo (hidden; blue/orange parts glimpsed, guess) |
| BAT, RX, ESC, DM | hidden internals (guess) |

---

## 1. Overall description in one paragraph

Duck is a **two-wheel servo flipper shaped like a doorstop with a rounded back**. Its body is a single printed shell about 88 mm wide, 78 mm long and 32 mm tall at the rear, whose top **slopes down to the front** in a long ramp and whose **rear is a quarter-round** (each side wall is a quarter-circle at the back). Set into the middle of the top is a **rectangular recess** holding the **flipper panel**: a flat plate about 46 mm wide × 58 mm long, decorated (in AWS67/72) with a **hand-drawn blue duck face with a red bill** and "DUCK LING". The panel is held at its **rear corners by two C-shaped clips** that wrap a hidden transverse axle near the back; a servo rotates the axle and lifts the panel's front edge. The front edge of the robot is either a **separate salmon wedge plate** with eight screws and a **thin metal strip** at the floor (AWS72), the body's own ramp with a metal strip (AWS67), or a **blue three-tine fork bar** (AWS71). The two **drive wheels** are hidden **inside the rear corners**, only their tread tops showing (under tape).

---

## 2. Part-by-part description

### 2.1 Body (CH) and rounded rear (RC)
- **Side profile**: from the front, the top surface is a **straight ramp** rising at about **18–20°** from z ≈ 6 at the front edge (y +39) to z ≈ 30 at y ≈ −15; then the rear is a **quarter-circle** of radius about **28 mm** (centre at about y −11, z 2… so the curve runs from the top at (y −11, z 30) down to the floor at (y −39, z 2)). AWS72 shows the left side wall clearly: a long black slab with the curved rear (45–440, 220–700 px); AWS71 shows the right side with its curve at the far right (1000–1180, 280–700 px).
- **Plan**: a rectangle about **88 mm wide × 78 mm long**, square front corners (where the wedge plate/forks attach), rounded rear in side view only.
- **Side walls**: flat, about **3 mm** thick, with horizontal layer lines; a **small hole** (Ø 2) low on the right side wall near the rear (AWS71 at (710, 625) px) — probably a screw or axle hole.
- **Colour/material**: black PLA/PETG (AWS71/72); orange PLA (AWS67).
- **Top surface**: flat ramp faces either side of the recess, about **20 mm** wide each, with visible layer lines; a **small hole** in the top near the recess front-right (AWS71 at (685, 480) px).

### 2.2 Top recess (TR)
- **Shape**: a **rectangular pocket** in the ramp, about **48 mm wide × 60 mm long**, about **3 mm deep**, centred on X, from y ≈ −25 to y ≈ +35. The flipper panel sits in it flush with (or slightly proud of, ≈ 1 mm) the ramp surface. At the recess's front edge there are small **notches** (AWS72 shows a pair of tiny rectangular notches at the panel's front-right corner at (680, 435) px — finger/lever slots or alignment tabs).
- **Behind the recess** (at the top rear), a **transverse gap** about 10 mm long exposes the hinge region and the wheels' tread tops, covered by tape TP in AWS71/72.

### 2.3 Flipper panel (FP, FP-D)
- **Shape**: a **flat rectangular plate**, about **46 mm wide × 58 mm long × 4 mm thick**, with sharp corners (AWS72 shows a thick white plate with visible vertical layer lines on its edge, about 4 mm). AWS71's orange panel has **two shades**: the front 2/3 bright orange (smooth) and the rear 1/3 lighter salmon with fine ribs — it may be **two stacked plates** or a step **(uncertain)**.
- **Drawing (FP-D)**: AWS67/72: a **circle about 38 mm across** drawn in thick black marker, filled **turquoise blue**, with a **white duck head** (an oval) inside, **two black dot eyes**, and an **orange-red trapezoidal bill** pointing down/forward; AWS67 adds "**DUCK LING**" hand-lettered in red below.
- **Width check**: 46 / 88 = 0.52 ≈ json width_frac 0.53 ✓.
- **Hinge end**: the rear edge of the panel at y ≈ −25.

### 2.4 Hinge clips (HC-L, HC-R), brackets (HB) and axle (HA)
- **Clips**: two **C-shaped hooks**, each about **10 mm wide (X) × 14 mm long × 12 mm tall**, made of a **3 mm thick curved strip** forming about **270° of a circle** of inner radius ≈ 5 mm, open toward the rear-bottom, mounted at the **rear corners of the panel** (x ±20), projecting **behind** the panel's rear edge. AWS72: black clips at (190–360, 210–290) and (600–760, 60–150) px; AWS71: black clips at (465–600, 45–135) and (780–940, 225–310); AWS67: **translucent blue** clips at (420–580, 95–200) and (875–1030, 300–380), each on a **dark blue bracket plate** (about 14 × 14 mm) with **three small silver screws** (two stacked + one beside).
- **Function**: they **wrap around a transverse axle/hinge bar** (HA, Ø ≈ 8–10 mm, at about **(y −30, z 26)**) near the back of the robot. Either the axle is the **servo-driven shaft** and the clips are clamped to it (driving the panel), or the clips are hinge knuckles and the servo pushes the panel from below **(guess: clips = hinge on a servo-driven axle)**.
- **Damage**: AWS71 shows the left clip with a **broken/torn tip** (ragged edge at (465–540, 45–80) px).

### 2.5 Front wedge plate (WP, WP-S, ME), AWS72
- **Shape**: a **flat salmon/coral printed plate**, about **88 mm wide × 30 mm long (along the slope) × 4 mm thick**, laid on the front of the ramp at about **18°**, its top edge at y ≈ +12, z ≈ 13 and its lower edge at y ≈ +40, z ≈ 3. Its **side edges** are flush with the body sides.
- **Screws (WP-S)**: **8 silver pan-head Phillips** (head Ø 3.5 mm, M2) in a **straight row** along its top edge, about **10 mm apart**, about 4 mm in from the edge.
- **Metal strip (ME)**: under the leading edge, a **thin silver strip** (aluminium or steel, about **0.8 mm thick**) protrudes about **3–4 mm** ahead of the printed plate along the full width, forming the true floor-contact edge.

### 2.6 Front ramp with metal strip, AWS67
- The orange body's ramp continues to the front without a separate plate; a **silver strip** (about 1 mm thick, aluminium) lies **under** the leading edge, protruding about 3 mm all along (AWS67 bottom edge (45–740, 650–1030) px). Its top is smooth orange.

### 2.7 Blue fork bar (FB, FB-T, FB-S), AWS71
- **Bar**: a **blue printed bar** about **88 mm long (X) × 10 mm wide × 4 mm thick** fixed across the front edge with **three silver screws** (at the left end, the middle and the right end — (215, 355), (375, 495), (570, 680) px), with a **row of 6 countersunk/recessed holes** between them (spare screw positions or lightening).
- **Tines (FB-T)**: **three flat prongs** projecting forward from the bar: at the two ends and the middle, each about **8 mm wide × 3 mm thick × 32 mm long**, each with a **small downward step/barb** near the tip (a notch underneath at about 8 mm from the tip) and a **chamfered point**. They lie flat on the floor.
- **Colour**: royal blue PLA.

### 2.8 Wheels (WH-L, WH-R)
- **Hidden in the rear corners**: only the **tread tops** show through the rear gap, at x ≈ ±32, y ≈ −25: AWS67 shows **pale translucent orange gear-tread wheels** (about 10 mm wide with ~2 mm teeth) at (535–620, 40–100) and (1020–1110, 230–330) px; AWS72/71 show dark wheels under **green/clear tape**.
- **Size (guess)**: **Ø 34 mm × 10 mm**, centres at **(±32, −22, 17)**, tops at z 34 (just above the body's highest point, so the robot can drive inverted on the wheels and the rounded rear) **(medium)**.
- **Guarding**: the wheels are **inside** the body's side walls (the side walls cover their outer faces entirely) — **fully guarded**.

### 2.9 Tape (TP)
- AWS72: a strip of **clear tape with a green tinge** (probably green-tinted packing tape, or clear tape over green) running across the rear top, over the hinge gap and the wheels, about **12 mm wide**, extending beyond the body at both sides. AWS71: clear tape over the rear wheels. Purpose: **keep debris out** of the hinge/wheel gap, or secure the hinge/axle **(guess)**.
- Under it in AWS72: **blue and orange** parts (the servo body, wires) visible at (150–230, 185–230) px.

---

## 3. Per-view sections

### 3.1 AWS72 (front-left, above)
- **Bottom right**: the salmon wedge plate (440–1170, 400–890) with 8 screws along its top edge and the silver strip below it.
- **Centre**: the white duck panel (215–770, 140–530) in its recess, with the two black clips at its rear.
- **Left**: the left side wall with its curved rear (45–440, 220–700).
- **Top**: the tape across the rear (75–760, 10–235), wheels underneath.

### 3.2 AWS71 (front-right, above; front to the left)
- **Left**: the blue fork bar and three tines (30–610, 340–845).
- **Centre**: the orange panel (370–1000, 90–530) with two shades; the two black clips (one broken).
- **Right**: the right side wall with its curved rear (600–1180, 280–720); the tape and wheel at the rear top (620–1100, 80–290).

### 3.3 AWS67 (front, high)
- The orange body (45–1150, 30–1030) as a ramp toward the camera; the white panel with the duck and "DUCK LING" (400–990, 80–640); the blue clips on blue brackets with screws; the orange translucent wheels at the rear corners; the silver strip at the bottom edge.

### 3.4 Top view (synthesised)
- An 88 × 78 rectangle with a 46 × 58 recess/panel in the middle; clips behind the panel at x ±20; the rear gap with wheel tops at x ±32; in front, the wedge plate (88 × 28 in plan) or the fork bar with tines to y +72.

### 3.5 Side view (left)
- A doorstop with a quarter-round back: the floor line from y −39 to +40; the top ramp from (+40, 3) up to (−11, 30), then the quarter-circle down to (−39, 2). The panel lies on the ramp; the clip and axle at the rear top.

### 3.6 Rear view (not photographed)
- The rounded rear, wheels hidden behind the side walls, the tape over the top gap **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | doorstop shell, rounded rear | 88 × 78 × 32 | 1 × 0.89 × 0.36 | black / orange FDM | — | 1 |
| TR | recess | 48 × 60 × 3 | 0.55 × 0.68 | — | — | 1 |
| FP | flat panel | 46 × 58 × 4 | 0.52 × 0.66 | white (drawn) / orange | clips | 1 |
| HC | C-clip | 10 × 14 × 12, r_in 5 | — | black / translucent blue | on axle; 3 screws via HB (AWS67) | 2 |
| HB | bracket plate | 14 × 14 × 3 | — | dark blue | 3 × M1.6–M2 | 2 (AWS67) |
| WP | wedge plate | 88 × 30 × 4 | 1 × 0.34 | salmon FDM | 8 × M2 | 1 (AWS72) |
| ME | metal strip | 88 × ~15 × 0.8 | — | aluminium | under WP | 1 |
| FB | fork bar | 88 × 10 × 4 | 1 × 0.11 | blue FDM | 3 × M2 | 1 (AWS71) |
| FB-T | flat tine | 8 × 32 × 3 | 0.09 × 0.36 | blue | integral | 3 |
| WH | gear-tread wheel | Ø 34 × 10 (guess) | 0.39 | translucent orange TPU / black | motor shaft | 2 |
| TP | tape | 12 wide | — | clear/green | adhesive | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| FP ↔ TR floor | resting | 0 |
| FP edges ↔ TR walls | clearance | 1 |
| HC ↔ FP | joined (printed/glued) | 0 |
| HC ↔ HA | wrapped | 0 |
| WP ↔ CH ramp | screwed (8) | 0 |
| ME ↔ floor | touching | 0 |
| ME ↔ WP | clamped under | 0 |
| FB ↔ CH front | screwed (3) | 0 |
| FB-T tips ↔ floor | touching | 0 |
| WH outer ↔ CH side wall | inside | 1–2 |
| WH top ↔ rear gap | through | +2 above the body |
| TP ↔ CH rear top | stuck | 0 |
| CH rear curve ↔ floor | tangent near the rear | 0–2 |

---

## 6. Mechanism
- **Drive**: two hidden rear wheels; the front rests on the metal strip / fork tips.
- **Flipper**: a servo turns the transverse axle HA at the rear (y −30, z 26); the clips transmit the rotation to the panel, which pivots about its rear and raises its **front edge** (from y +35). An opponent that has driven up the ramp onto the panel is tipped **backward over Duck**. The panel's 58 mm length gives about 10 mm of lift per 10° of rotation.
- **Rounded rear**: if Duck is flipped onto its back, the curve lets it roll, and the wheels (top above the body) can still drive; firing the panel against the floor helps self-right.

---

## 7. Assembly order (suggested)
1. Print CH (shell with recess, rear gap, wheel bays), FP, clips, wedge plate/fork bar.
2. Fit the two drive gearmotors in the rear bays; mount the wheels through the rear gap.
3. Fit the servo and axle HA across the rear; battery, receiver, ESC.
4. Snap the clips onto the axle; attach the panel (glue or screws via brackets HB).
5. Front: screw the wedge plate with the metal strip under it (8 screws), or the fork bar (3 screws).
6. Tape over the rear gap.

---

## 8. Hidden / uncertain list
- Exact hinge/actuation (clips on a driven axle assumed).
- Wheel size and motors.
- Underside (open or closed), rear face.
- Whether AWS71's two-shade panel is one part.
- All mm ±15–20%.

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the body centre; +X right, +Y forward, +Z up, mm.
- Body x ∈ [−44, +44], y ∈ [−39, +39], z ∈ [0, 32]; recess x ∈ [−24, +24], y ∈ [−25, +35]; axle at (y −30, z 26); fork tips (AWS71) to y +72; metal strip to y +43.

## 10. Profiles as math

**10.1 Body side profile (YZ).** Ramp: z = 3 + 0.54·(39 − y) for y ∈ [−11, 39] (28.4°?) — measured 18–20° in the photos → use z = 3 + 0.36·(39 − y) giving z = 21 at y −11; then a quarter-circle: (y + 11)² + (z − 2)² = 28²... combining: top of the arc at (−11, 30) requires z_ramp(−11) = 30 → slope 0.54 (28°). Reconciled in 13.2: **ramp 22°, top z 26 at y −11, rear arc r 24 centred (−15, 2)**.

**10.2 Panel pose.** Rest: lies on the ramp. Rotation about HA = (y −30, z 26): front edge E₀ = (+33, 6)… for a rotation θ, E(θ) = HA + R·(cos(β₀ − θ)…) with R = |E₀ − HA| = √(63² + 20²) = 66.1, β₀ = −17.6° (below horizontal): z_E(θ) = 26 + 66.1·sin(θ − 17.6°). θ = 40° → z_E = 51.

**10.3 Clip.** Arc of inner radius 5, thickness 3, from 45° to 315° around HA, extruded 10 mm in X at x ±[15, 25].

**10.4 Fork tine (AWS71).** Plan: rectangle 8 × 32 with a 45° point chamfer of 4 mm at the tip; side profile: thickness 3 with a 1 mm step under it at 8 mm from the tip.

**10.5 Wedge plate (AWS72).** Plane z = 3 + 0.36·(40 − y) for y ∈ [12, 40], thickness 4; screw holes at y ≈ 14, x = −35 + 10k (k = 0…7).

## 11. Pixel measurements
- **AWS72**: wedge plate top edge ≈ 560 px (oblique, 8 screws at ≈ 60–70 px pitch → 10 mm pitch → ≈ 6.5 px/mm there); panel width ≈ 330 px at its front; body side length ≈ 420 px.
- **AWS71**: fork tine length ≈ 200–230 px; bar ≈ 470 px; panel ≈ 330 × 420 px.
- **AWS67**: body front width ≈ 700 px (front edge), rear ≈ 650 px; panel ≈ 440 × 560 px; clips ≈ 150 px wide.

## 12. Several independent estimates

| Quantity | Method A (rule) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | ≤ 101.6 | — | AWS72: 8 screws at 10 mm pitch span 70 mm ≈ 0.8 of the plate → plate 88 | **88** |
| Panel width | 0.53 × 88 = 47 (json) | — | AWS67: 440/700 × 88 = 55 (panel farther than the front edge → ×0.85 = 47) | **46** |
| Panel length | 58 | 0.66 W | AWS67: 560 px / 6.4 px/mm ≈ 87 projected?? (top-down foreshortening reversed) → AWS72 330 px wide : 420 long → 46 × 1.3 = 58 | **58** |
| Body length | ≤ 101.6 − strip 4 | 0.89 W | AWS72 side ≈ 420 px / 6.5 ≈ 65 (foreshortened ×1.2) ≈ 78 | **78** |
| Fork tine length | 101.6 − 78 = 23 + bar | — | AWS71: 220 px / 7 px/mm ≈ 31 | **30** (see 13.1) |
| Body height | 30 | 0.36 W | AWS72 side wall rear ≈ 180 px / 6 ≈ 30 | **30–32** |

## 13. Consistency check
1. **Cube fit with forks (AWS71)**: 78 + 3 (bar) + 30 = 111 > 101.6. Either the body is shorter (≈ 68) or the tines ≈ 20. The fork bar may replace the front ~10 mm of the body ramp. **Reconciled: body 70 + forks 30 = 100 for AWS71; AWS72 body 78 + strip 4 = 82.**
2. **Ramp angle vs height**: a 22° ramp over 50 mm rises 20 mm (from z 6 to z 26), then the rear arc (r 24) to the floor — overall height 26–30 ✓ with the wheels (Ø 34) topping out at 34 through the gap ✓.
3. **Hinge at rear**: clips at the rear corners in all three photos → the hinge is at the rear; position "middle" in the json refers to the panel's place on the body.

---

## 14. Why the designer did it (adversarial first)

- **Doorstop body with a full-width front edge**: the whole robot is a wedge; opponents meet a thin metal strip (AWS67/72) that sits on the floor — metal gets under printed wedges — and then ride up the ramp **onto the flipper panel**. The forks (AWS71) do the same with less surface and better under-ability.
- **Flipper in the middle of the top**: the panel only acts on opponents that are already on top of Duck; tilting its front up throws them backward and over, using the opponent's own approach. Its smaller size (half width) keeps the servo load low. Weak point: the opponent must climb the ramp first; a servo flipper is slow compared with pneumatic ones.
- **Rear hinge clips on an axle**: easy to unclip and change the panel between fights (three panels/colours seen); the clips also act as **fuses** — one broke (AWS71) instead of the servo. Translucent blue/black clips are cheap prints.
- **Wheels hidden inside the rear corners**: completely protected from horizontal spinners and from side wedges; only the tread tops show, sealed with tape against debris. The rounded rear and wheel tops above the body allow driving inverted and rolling back upright.
- **Rounded rear**: an opponent pushing from behind meets a curve and slides up/over rather than catching an edge; the curve also helps self-righting.
- **Hand-drawn duck panel**: personality (a family/junior team robot, "Duck-ling") and identity.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Flipper servo | metal-gear micro servo driving HA via the horn | 23 × 12 × 25 | (0, −28, 14), output at HA (y −30, z 26) | medium |
| Axle HA | Ø 8–10 printed/steel rod across the rear between the clips | Ø 9 × 50 | (0, −30, 26) | medium |
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | (±20, −22, 17) | medium |
| Battery | 2S LiPo 200–300 mAh | 40 × 18 × 9 | (0, +10, 8) under the panel | medium |
| ESC + RX | combined board | 25 × 20 × 6 | (0, −5, 8) | low |
| Power switch | on the side wall or under the tape | — | (+44, −20, 12) | low |
| Wiring | servo lead and motors at the rear; battery under the ramp | — | — | medium |

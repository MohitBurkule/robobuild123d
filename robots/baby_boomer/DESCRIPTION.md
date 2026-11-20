# Baby Boomer: full rebuild description from reference photos

Source photos:
- `robots/baby_boomer/reference/baby_boomer.aws69.webp` (483 × 456 px): AWS 69. Uncut, low resolution, on a white table under warm light. Camera at the **front-right**, high (about 50° down). Shows the whole top: the green U-shaped top plate, the **yellow centre flap** with a **black leaping-deer sticker**, the **steel butt hinge**, two **dark tapered spikes** at the front and a **clear tape tip** on the yellow ramp.
- `...aws72.webp` (1340 × 1083 px): AWS 72. Cut out onto white. Camera at the **front, slightly right of centre**, about 40° down; the front faces the camera, so the robot's **right** side is on the image **left**. Best for the **barbed steel forks**, the **front corner blocks**, the **yellow ramp with its translucent tip**, the **hinge** and the **right-side dark-green block**.
- `...aws73.webp` (1171 × 685 px): AWS 73. Uncut, on a grey arena/pit floor. Camera **above the robot's right side**, about 45° down; the front is on the **image right**. Best for the **right side profile**: both right wheels (3-spoke hubs), the **dark-green side block**, the **broken right front corner block**, the yellow ramp projecting forward, and a **spare front block** (green wedge) lying beside the robot.

Facts come from the photos; inferences are marked **(guess)**. Sizes are **estimates in mm** from the AWS limit (150 g, 101.6 mm cube) and the spec draft (body 72 × 84 × 24, four outboard wheels r 11, flipper, two forks 40 mm), checked against pixel ratios. Ratios are against **W = body width without wheels ≈ 64 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the body footprint (front blocks and forks excluded).
- **+X** = robot right, **+Y** = forward (toward the forks and ramp), **+Z** = up. mm. Side-profile angles from the floor.
- Body extents (reconciled §12): x ∈ [−32, +32], y ∈ [−38, +30], z ∈ [3, 25]. Front blocks to y = +40. Ramp tip y ≈ +58. Fork tips y ≈ +72. Wheels to x = ±42.

| ID | Part |
|---|---|
| BD | neon-green translucent body tub |
| TP | green U-shaped top plate (two side strips + rear cross-bar) |
| FP | yellow centre flap / lifting ramp |
| FT | translucent tape/plastic tip on the ramp |
| HG | steel butt hinge (two leaves, 4 screws) |
| DS | black leaping-deer sticker on FP (AWS69) |
| FB-L, FB-R | green front corner blocks (rounded outer corners, fork roots) |
| FK-L, FK-R | steel forks (barbed knife blades at AWS72; plain dark spikes at AWS69) |
| SB-R | dark-green block on the right side between the wheels |
| WH-FL, WH-FR, WH-RL, WH-RR | four wheels: black knurled tyres on yellow-green 3-spoke hubs |
| S-TP | 4 black Phillips/Torx pan screws on TP corners |
| S-FP | 1 black screw in the middle of FP |
| S-HG | 4 black countersunk screws in the hinge leaves |
| SV | flap servo (hidden) |
| M-x, BAT, ESC, RX, SW | hidden motors and electronics |
| SP | spare green wedge block (AWS73, beside the robot) |

---

## 1. Overall description in one paragraph

Baby Boomer is a **small four-wheel servo flipper/lifter** printed in **translucent neon green** with a **yellow** centre. The body is a plain box about 64 mm wide, 68 mm long and 22 mm tall, with **four black knurled wheels** on **3-spoke yellow-green hubs** mounted **outboard** at the four corners (overall width about 84 mm). The top is a **green U-shaped plate** held by four black screws, framing a **yellow flap** that runs down the centre: the flap is **hinged at the rear on a small steel butt hinge** and continues past the front of the body as a **ramp sloping down to the floor**, ending in a **translucent taped tip**. Either side of the ramp, the front corners are **chunky green blocks with rounded outer corners**, and from the bottom of each block a **steel fork** runs forward and down to the floor: at AWS72 these are **barbed knife blades**, at AWS69 **plain dark tapered spikes**. A **dark-green block** sits on the right side between the wheels. AWS69 shows a black **leaping-deer sticker** on the flap. The look is a bright green "toy tractor" with a yellow tongue and two fangs.

---

## 2. Part-by-part description

### 2.1 Body tub (BD)
- **Shape**: a rectangular box, **64 mm wide × 68 mm long × 22 mm tall** (z 3 to 25). Vertical walls about 2.5 mm thick; sharp vertical edges; the top edge carries the top plate.
- **Wheel mounting**: the side walls carry the motors' gearboxes; the wheels sit outboard of the walls with a 2 mm gap.
- **Colour/material**: **translucent neon green PLA/PETG**, with visible layer lines and a glowing edge look. The interior is not visible.

### 2.2 Top plate (TP)
- **Shape**: a flat plate about **2.5 mm thick**, outline **64 × 68 mm** with a **centre cut-out about 22 mm wide** running from y ≈ −22 to the front edge, so it is a **"U"**: two **side strips** (each about 21 mm wide) and a **rear cross-bar** (about 16 mm deep, y −38 to −22).
- **Screws S-TP**: **4 black pan screws** (head Ø about 5 mm, M2.5–M3, Phillips or Torx) at about 6 mm in from the corners: (±24, −30) and (±24, +22). AWS72 and AWS73 show all four clearly.
- **Surface**: diagonal top-layer infill pattern, slightly scuffed.
- **Fit**: the top plate's outer edges are flush with the tub walls; a thin horizontal seam is visible between the plate and the tub (AWS73).

### 2.3 Yellow flap / ramp (FP)
- **Shape**: a **yellow printed plate**, **20 mm wide**, consisting of two sections:
  1. A **flat top section** lying in the top plate's cut-out, **about 50 mm long** (y −22 to +28), **4 mm thick**, flush with the top plate (its top at z ≈ 25). It carries **one black screw** (S-FP) on its centreline at about y +8 (AWS72: (700, 400); AWS73: (615, 268)).
  2. A **ramp section** bending down at the front: from y +28 the flap angles down at about **35–40°** to the floor, about **28 mm** long, its tip at y ≈ +52. The ramp is slightly **wider (22 mm)** and its surface shows **print lines and translucent infill**.
- **Tip (FT)**: the last 8–10 mm of the ramp is a **translucent whitish strip** (clear packing tape folded over the tip, or a thin clear plastic plate); AWS69 shows a **clear tape flap** extending a further 6 mm beyond the yellow onto the floor (y ≈ +58).
- **Hinge**: at the rear end (y ≈ −22) the flap joins the steel hinge HG; the rear cross-bar of the top plate carries the other leaf.
- **Sticker (DS, AWS69)**: a **black silhouette of a leaping deer/antelope** (about 12 × 12 mm) on the ramp near its top bend (a John Deere-style tractor joke, given the green-and-yellow colours) **(identity, reading)**.
- **Function**: the **lifting element**. With the hinge at the rear and a servo inside pushing up under the flap, the ramp's tip rises in an arc about the hinge: the flipper/lifter.

### 2.4 Steel hinge (HG)
- **Shape**: a small **steel butt hinge**, **about 20 mm wide (X) × 16 mm long (Y) open**, leaves about 1 mm thick with a **knuckle barrel Ø 3 mm** along X. Each leaf has **2 countersunk holes** with **black screws** (S-HG, 4 total). Brass/steel colour with tarnish (AWS73 shows it brownish).
- **Position**: centred on X, the knuckle at **y ≈ −22, z ≈ 25.5**, the rear leaf screwed to the top plate's rear cross-bar, the front leaf to the flap's rear end.
- **Gap**: a small dark gap (about 2 mm) under the knuckle (AWS73, a black slot at the hinge's front edge) where the flap meets the plate.

### 2.5 Front corner blocks (FB-L, FB-R)
- **Shape**: two green translucent blocks at the front corners, each about **21 mm wide (X) × 12 mm long (Y) × 24 mm tall**, from z ≈ 1 to 25, standing ahead of the tub's front wall at y +30 to +42. The **outer front vertical edge is rounded** (radius about 8 mm in plan); the inner face borders the ramp with about 1 mm clearance. Their tops are flush with the top plate.
- **Fork slot**: each block has a slot in its lower front face (about 1.5 mm wide × 8 mm tall) at x ≈ ±22, z ≈ 4, from which the fork projects.
- **Damage**: the right block in AWS73 is **broken**: its lower front is chipped and cracked (rough exposed infill at the front bottom), showing it takes the impacts.
- **Spare (SP)**: AWS73 shows a loose **green wedge-shaped part** (about 25 × 15 × 10 mm, a prism with a sloped top) beside the robot and another under the blue folder: spare **front blocks or fork holders** **(guess)**.

### 2.6 Forks (FK-L, FK-R)
- **AWS72**: **steel blades**, about **1 mm thick**, **5 mm tall at the root tapering to a point**, **38 mm long** from the block face, laid **on edge** (the blade plane vertical, YZ), sloping down at about 20° from z ≈ 6 at the block to the floor. Each tip has **two backward barbs** (sawtooth notches about 3 mm deep, 6 mm apart) near the end, like a **snap-off utility-knife blade** or a cut hacksaw blade. Scratched dark steel.
- **AWS69**: **plain dark tapered spikes** (brown/dark grey, round or square section about 4 mm at the root tapering to a point), similar length, sloping to the floor.
- **AWS73**: the right fork lies flat on the floor under the broken block, protruding about 20 mm beyond it (partly hidden).
- **Positions**: x = ±22, tips at y ≈ +72 on the floor.

### 2.7 Right side block (SB-R)
- **Shape**: a **dark-green (opaque) rectangular block**, about **24 mm long × 12 mm tall × 6 mm thick**, on the **right side wall** between the front and rear wheels, low (z ≈ 2 to 14), standing out about 6 mm from the wall (as far as the tyres' inner faces). Its edges are slightly rounded; AWS73 shows a chip in its lower edge.
- **Function (guess)**: a **removable power link / switch cover** or a **side skid/bumper** that stops the robot resting on its side. A different, opaque material suggests it is an **add-on**. Confidence low. Only the right side is photographed; the left side may have a matching block **(guess)**.

### 2.8 Wheels (WH-x)
- **Shape**: **Ø 26 mm × 8 mm**: **black rubber/TPU tyres** with fine **knurled ribs** (about 40 ribs across the tread), on **translucent yellow-green printed hubs** with **3 curved spokes** (three kidney-shaped openings) and a central boss (AWS73 clearly; AWS72 shows a 3-hole hub).
- **Positions**: centres at **x = ±38, y = +18 (front) and y = −26 (rear), z = 13**. Tops at z = 26 (about level with the top plate), bottoms at z = 0.
- **Drive**: 4WD, each wheel on its own N20 gearmotor, or two motors with front/rear coupled **(guess)**.

---

## 3. Per-view descriptions

### 3.1 Top view (plan; AWS69 is nearly this)
- A green 64 × 68 rectangle with a yellow 20 mm strip down the centre from the hinge at y −22 to the front, continuing as the ramp to y ≈ +52 (tip at +58). Four black screws at the plate corners, one on the flap, four on the hinge.
- The four wheels (26 × 8) stick out at the corners, 2 mm off the walls.
- At the front, the two rounded green blocks either side of the ramp and the two forks (thin lines) at x ±22 out to y +72.

### 3.2 Front view (AWS72)
- The two green blocks (21 wide each) with rounded outer edges, the yellow ramp coming down between them to the floor, the two fork blades running forward from the block bottoms. Behind and above, the flat top with the hinge; the four wheels at the outer edges, their tops level with the top plate.

### 3.3 Right side view (AWS73)
- A green rectangle 68 × 22, the two wheels (Ø 26) at the ends with 3-spoke hubs, the dark-green block between them at the bottom. At the front, the tall green block with the fork at the floor and the yellow ramp sloping down ahead of it. On top, a flat line.

### 3.4 Rear view (inferred)
- A plain green wall 64 × 22 with the rear wheels at the corners; the hinge barrel just visible on top.

### 3.5 Isometric (AWS72)
- A bright green box on four black wheels with a yellow tongue running down to the floor and two steel fangs.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | box | 64 × 68 × 22 | 1 × 1.06 × 0.34 | neon green translucent PLA | — | 1 |
| TP | U-plate | 64 × 68 × 2.5, cut-out 22 wide | 1 × 1.06 | neon green | 4 × M2.5 black | 1 |
| FP | bent plate | 20–22 wide, 50 flat + 28 ramp, 4 thick | 0.31 | yellow PLA | hinge + servo | 1 |
| FT | tape tip | 22 × 8–14 | — | clear | adhesive | 1 |
| HG | butt hinge | 20 × 16 × 3 | 0.31 × 0.25 | steel/brass | 4 × M2 countersunk | 1 |
| DS | sticker | 12 × 12 | — | black | adhesive | 1 (AWS69) |
| FB | block | 21 × 12 × 24, R 8 outer corner | 0.33 × 0.19 × 0.38 | neon green | screws/glue (guess) | 2 |
| FK | barbed blade / spike | 38 × 5 × 1 | 0.59 | steel / dark | slot in FB | 2 |
| SB-R | block | 24 × 12 × 6 | 0.38 × 0.19 | dark green | screws (guess) | 1 |
| WH | wheel | Ø 26 × 8 | 0.41 × 0.13 | black tyre, green hub | motor shaft | 4 |
| S-TP | pan screw | Ø 5 head | 0.08 | black | TP | 4 |
| S-FP | pan screw | Ø 4 head | — | black | FP | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| BD bottom ↔ floor | clearance | 3 |
| WH bottom ↔ floor | contact | 0 |
| WH top ↔ TP top | about level | 0 to +1 |
| WH inner face ↔ BD wall | clearance | 2 |
| WH-FL ↔ FB-L (Y) | wheel behind block | 2–4 |
| TP ↔ BD walls | screwed | 0 |
| FP edges ↔ TP cut-out edges | running clearance | 1 |
| FP top ↔ TP top | flush | 0 |
| FP ↔ HG front leaf | screwed | 0 |
| HG rear leaf ↔ TP cross-bar | screwed | 0 |
| FP ramp edges ↔ FB inner faces | clearance | 1 |
| FT ↔ floor | touching / 0.5 above | 0–0.5 |
| FB ↔ BD front | joined | 0 |
| FK ↔ FB slot | clamped | 0 |
| FK tip ↔ floor | contact | 0 |
| SB-R ↔ BD right wall | screwed/glued | 0 |
| SB-R outer face ↔ WH inner-face plane | about level | 0 |

---

## 6. Mechanism

1. **Drive**: four wheels, skid steer, outboard; tops level with the top plate, so when inverted the robot rests on the wheel tops and can drive (the flap face is flush and the hinge is low).
2. **Flipper/lifter**: a servo under the flap pushes it up about the rear hinge. The ramp tip is about 75 mm ahead of the hinge (y −22 → +52), so a 30° rotation raises the tip by 75·sin 30° ≈ 38 mm. Because the ramp is bent down, when the flap rotates up the ramp swings from pointing down-forward to pointing forward, scooping and tipping an opponent backward over the robot. A fast high-torque servo gives a "flip" rather than a slow lift (hence "Boomer").
3. **Forks**: passive, fixed in the blocks.

---

## 7. Assembly order (suggested rebuild)

1. Print the tub with motor pockets, the front corner blocks (integral or separate), the U top plate and the yellow flap (bent shape printed on its side, or flat + ramp joined).
2. Install the four gearmotors; fit the wheels.
3. Install the servo under the flap position (horn pushing the flap's underside or a short link), plus battery, ESC, receiver and switch.
4. Screw on the top plate (4 screws).
5. Screw the hinge to the top plate's rear cross-bar and to the flap's rear end (4 screws); fix the flap to the servo horn (the centre screw S-FP).
6. Push the forks into the block slots (glue or clamp).
7. Tape the ramp tip; fit the right side block; stick on the deer.

---

## 8. Hidden / uncertain list
- Servo type, position and linkage (the single flap screw may be the horn attachment).
- Whether the front blocks are separate parts (AWS73's spares suggest yes).
- Function of the dark-green side block, and whether there is one on the left.
- Drive motor count.
- All sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin under the body centre, +X right, +Y forward, +Z up, mm.
- BD x ∈ [−32, 32], y ∈ [−38, 30], z ∈ [3, 25]. Hinge axis (y −22, z 25.5) along X. Ramp bend at y +28; tip y +52 (tape to +58). Forks x ±22, tips y +72. Wheels (±38, +18 / −26, 13).

## 10. Profiles as math

**10.1 Flap FP side profile (YZ, closed).** Flat top: z ∈ [21, 25] for y ∈ [−22, +28]. Bend: an arc with inner radius 3 about (y +28, z 18) from θ = 90° to θ = 52°. Ramp: top line from (28, 19) to the tip (52, 0): z = 19 − 0.79·(y − 28) (38.4°). Thickness 4 normal to the line.
- Opened by α about the hinge H = (−22, 25.5): every point p maps to H + R(α)·(p − H), R rotating in the YZ plane, front edge up.

**10.2 Front block FB (plan, XY).** Rectangle x ∈ [11, 32], y ∈ [30, 42], with the outer front corner (32, 42) replaced by a quarter circle of r 8 centred (24, 34). Mirrored for FB-L. Height z ∈ [1, 25]; fork slot at z ∈ [3, 11], x = ±22.

**10.3 Barbed fork blade (YZ, x = ±22).** Upper edge from (42, 9) to the tip (72, 0): z = 9 − 0.3·(y − 42). Lower edge from (42, 4) to (72, 0): z = 4 − 0.133·(y − 42). Barbs: notches on the upper edge at y = 60 and y = 66, each a right triangle 3 mm deep with its vertical face toward the rear.

**10.4 Wheel hub (in the wheel plane).** Rim r ∈ [9, 10]; hub r ≤ 3.5; three curved spokes, each the band between the spirals φ = φ_k + 0.08·r and φ = φ_k + 0.08·r + 0.35 (radians), φ_k = 0, 2π/3, 4π/3. Tyre r ∈ [10, 13] with 40 ribs: r(φ) = 12.6 + 0.4·[sin(40φ) > 0].

**10.5 Top plate cut-out.** The U: outline rectangle minus x ∈ [−11, 11], y ∈ [−22, 30].

## 11. Pixel-based measurements

**AWS72 (1340 × 1083):**
- Front blocks: robot right (image left) x 350–700, y 580–830; robot left (image right) x 880–1160, y 400–580.
- Ramp: from (690, 420) at its top to the tip (760–960, 640–790); tape tip (780–960, 680–790).
- Forks: robot right from (520, 770) to the tip (690, 1010); robot left from (1060, 550) to (1280, 790).
- Hinge: (400–590, 175–265). Top-plate screws: (680, 125), (240, 260), (530, 525), (940, 375). Flap screw (700, 400).
- Wheels: front-right (270–410, 490–700); rear-right (40–170, 230–410); rear-left (690–800, 30–150); front-left (950–1090, 250–370).
- Side block: (170–290, 400–640).

**AWS73 (1171 × 685):**
- Body side from x 60 to 760 (rear to front), top plate edge at y 330–480 near side, top line y 70–90 far side.
- Wheels: rear-right (45–240, 480–650) Ø ≈ 190 px; front-right (520–715, 460–630) Ø ≈ 190 px.
- Side block: (290–520, 530–640). Ramp projects to x ≈ 920. Fork tip near (940, 545).
- Screws: (200, 140), (680, 135), (200, 440), (690, 390); flap (615, 268); hinge (205–350, 225–335).

**AWS69 (483 × 456):**
- Body: x 40–440; flap x 130–220 at the front; spikes from (70, 260) to (20, 360) and (260, 320) to (205, 430); tape tip (80–160, 390–430).

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | 72 (spec) | overall ≤ 101.6 with wheels: 64 + 2 × (2 + 8) = 84 | AWS69: body 400 px wide vs wheel 75 px (Ø) → if wheel Ø 26, body ≈ 90?? (wheels foreshortened) | **64** |
| Body length | 84 (spec) | 1.06 W = 68 | AWS73: wheel centres 480 px apart vs wheel Ø 190 px = 26 → 66 between axles + 2 × 13 → body ≈ 70–76 incl. blocks | **68 + 12 blocks** |
| Height | 24 (spec) | 0.34 W = 22 | AWS73: side wall height ≈ 160 px vs wheel 190 px → 22 | **22** |
| Wheel Ø | 22 (r 11 spec) | 0.41 W = 26 | AWS73: wheel top level with the top plate → Ø ≈ height + 3 = 25–26 | **26** |
| Flap width | — | 0.31 W | AWS72: 175 px vs top plate 600 px → 0.29 × 64 = 19 | **20** |
| Fork length | 40 (spec) | 0.59 W = 38 | AWS72: 260 px / 7 px/mm → 37 | **38** |
| Ramp reach beyond the blocks | — | — | AWS73: ramp 140 px past the block, wheel scale 7.3 px/mm → 19 | **10–16** |

## 13. Consistency check: conflicts and reconciliation
1. **Wheel size**: spec r 11 (Ø 22) vs photos showing the wheel tops level with the 25 mm top plate. A Ø 22 wheel at z 11 would sit 3 mm below. **Reconciled Ø 26** (z 13).
2. **Width**: the spec's 72 mm may include the side block or be over the tub plus clearances; ratios to the flap (20 mm, 0.31 W) give 64. Overall with wheels 84 fits the cube. **Reconciled 64.**
3. **Length**: spec 84 includes the front blocks (68 + 12 = 80); consistent.
4. **Ramp tip**: AWS72 shows the ramp tip ahead of the blocks by about the blocks' length; AWS73 similar. **Reconciled tip y +52, tape to +58.**
5. **Forks**: steel barbed blades (AWS72) vs dark spikes (AWS69): event variants; same position and length.
6. **Hinge position**: both AWS72 and AWS73 put it at about one third of the length from the rear, on the centreline. Consistent with a rear-hinged flipper.

---

## 14. Why the designer did it (per part, adversarial first)

- **Rear-hinged yellow flap that becomes a ramp**
  - Fight: the flap's front is a **ramp to the floor**, so opponents that drive at Baby Boomer **ride up the ramp onto the flap**, and the servo then flips them back over the robot. A long lever (hinge to tip 75 mm) gives a big tip movement for a small servo rotation. The taped tip makes the leading edge thinner and slicker so it gets **under** opponents' front edges.
  - Being got under: the ramp tip and the two forks are the lowest points at the front; an enemy wedge meets them first.
  - Threats: a vertical spinner hitting the ramp loads the hinge and the servo; the hinge is a stock steel part (strong), and the servo is protected inside. The flap is a separate yellow part, easy to reprint.
- **Steel butt hinge**
  - Construction: an off-the-shelf hinge is strong, cheap and low-profile, sitting flush with the top so nothing sticks up to be hit.
- **Front corner blocks**
  - Fight: they protect the front wheels and the ramp's sides from frontal hits and give the forks a solid root. Rounded outer corners let opponents and walls slide off rather than catching. They are sacrificial (AWS73 shows one broken, and spares were brought).
- **Forks (barbed blades or spikes)**
  - Fight: two points spread to the corners get under opponents arriving at angles; barbs hold the opponent's edge so it cannot back off before the flip. Blades on edge are stiff vertically (resist bending up) while thin.
- **Four outboard wheels level with the top**
  - Fight: invertible driving: if flipped, the robot still drives on its wheel tops, and the flap (flush) can still work as a self-righter by pushing the floor. 4WD keeps traction when the front is lifted by an opponent's wedge.
  - Threats: outboard wheels are exposed to horizontal spinners; the front blocks shield the front pair from the front.
- **Dark-green side block**
  - Fight/construction (guess): either a side bumper protecting the wall between the wheels, or the power link/switch housing, which the rules require to be accessible; an opaque add-on part.
- **Translucent neon green + yellow and the deer sticker**
  - Identity: tractor colours (and the deer) make the robot recognisable; translucent filament also lets LEDs show through **(guess)**.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors (or 2 with coupled pairs) | 12 × 10 × 25 | x ±18, y +18 / −26, z 13, shafts along X | medium |
| Flap servo | 9–20 g servo, metal gear, high speed | 23 × 12 × 28 | x 0, y −5, z 12, horn under the flap with the flap screw on it | medium |
| Battery | 2S 300 mAh LiPo | 45 × 18 × 10 | along Y beside the servo, x +18, y −5, z 9 | medium |
| ESC | dual brushed ESC (or 2) | 25 × 15 × 5 | x −18, y −5, z 7 | medium |
| Receiver | micro receiver | 20 × 12 × 5 | x −18, y −28, z 10 | low |
| Switch | removable link in the dark-green side block | 10 × 6 × 6 | (+33, −4, 8) | low |
| Wiring | battery → switch → ESC → 4 motors; servo lead from RX | — | — | medium |
| Block fixing | M2 screws from inside the tub into the front blocks | — | — | low |

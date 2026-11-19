# Trappist-1: full rebuild description from reference photo

**Photo coverage note**: there is **only one photo**, a 679 × 675 px pit shot taken from almost directly above the robot (slightly from the rear). The top deck, wheels, wedge and arm are clear. The sides, front face, underside and interior are not seen, so this description is **shorter than usual (about 3700 words)** and leans on inference, marked **(guess)**.

Source photo:
- `robots/trappist_1/reference/trappist_1.aws63.webp` (679 × 675 px). AWS 63. The robot lies on a pale grey speckled table. The camera looks down at about **70–75°**, from slightly **behind** the robot, so the **rear edge is at the bottom of the image** and the **steel front wedge at the top**. A tall **two-strip arm** stands up from the middle and projects toward the top of the image (it is standing nearly **upright**, foreshortened, see §13).

The draft spec labels it a lifter on an X axis. From the arm geometry and the name ("Trappist" → **trap**), it reads best as a **servo-driven clamp / grabber**: the tall arm swings forward and down onto an opponent that has driven onto the wedge, trapping it. A lifter reading is also possible (see §6).

Scale anchors: AWS 150 g / 101.6 mm cube; the **micro servo** (9 g class, about 23 × 12 mm in plan); the silver **button/countersunk screws** (M2–M2.5, head Ø ≈ 4.5 mm); the carbon-fibre weave (a 3 mm twill pattern is typical). Reference width **W = width across the red side walls ≈ 90 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the centre of the chassis footprint.
- **+X** = robot's right (image right), **+Y** = forward (image up, toward the steel wedge), **+Z** = up; mm.
- Envelope (arm up): x ∈ [−48, +48], y ∈ [−38, +42], z ∈ [0, ~100].

| ID | Part |
|---|---|
| TP | carbon-fibre top plate (stepped outline with a central cut-out) |
| FB | black printed front block / servo bay (in the cut-out) |
| SV | micro servo (black) |
| HN | white servo horn (left side of the servo) |
| IP | idler pivot (right side of the servo) |
| AR-L / AR-R | left / right arm strips |
| AX | arm cross-bar (bent black strip) |
| NT | black nylon nuts/spacers at the cross-bar joints |
| TIP | arm tips (bent hooks with clear blobs) |
| WG | stainless steel front wedge strip |
| S-WG | 3 screws along the wedge's top edge |
| SW-L / SW-R | red printed side walls (wheel guards) |
| WH-FL, WH-FR, WH-RL, WH-RR | four small black wheels |
| RB | carbon rear bar (rear edge strip) |
| S-RB | 2 silver screws at the rear centre |
| PN | brass pin at the rear-left (switch / link, guess) |
| S-TP | 8 silver screws on the top plate wings |
| WR | wires: white JST connector, red lead, servo lead (orange/red/brown) |
| M-x | drive motors (hidden, guess N20) |
| MM | plastic motor mounts (hidden) |
| BAT, ESC, RX | hidden electronics |

---

## 1. Overall description in one paragraph

Trappist-1 is a **flat, four-wheel box** about **90 mm wide and 76 mm long**, topped by a **glossy carbon-fibre plate** and walled on both sides by **red printed side plates**. Across the whole front runs a **bright stainless-steel wedge strip**, slightly wider than the robot, screwed on with three screws, with its ends folded back round the front corners. The **four small black wheels**, wrapped in lumpy black rubber or tape, sit in the **corners** inside the red walls. The carbon top plate has a **trapezoidal cut-out** in the middle, where a **black printed bay** holds a **micro servo**. From the servo's sides rise **two thin black strips** forming a **tall, narrow U-shaped arm**, about 95 mm long, braced by a **bent cross-bar** about halfway up with black nylon nuts. The tips are bent into small hooks with **clear blobs** on them. The arm is shown **standing upright**; it swings forward over the wedge to **clamp down** on an opponent. At the rear there is a carbon edge strip with two screws and a **brass pin**, probably the power link.

---

## 2. Part-by-part description

### 2.1 Top plate (TP)
- **Material**: **carbon-fibre sheet**, about **1.5 mm** thick, **twill weave** (diagonal pattern of glossy dots, period about 3 mm), glossy.
- **Outline (plan)**: a rectangle about **82 × 64 mm** (inside the red walls), y ∈ [−34, +30], with:
  - **Corner notches** at all four corners for the wheels, each about **16 × 18 mm** (X × Y).
  - A **central cut-out** open to the front: about **44 mm wide at the front edge** (x ±22), narrowing with **45° chamfered sides** to about **30 mm wide** (x ±15) at y ≈ +16, then straight sides back to y ≈ −14 (the servo bay). So the plate is a **"U" with two wings** (left and right), joined at the rear by a **solid band** about **20 mm deep** (y −34 to −14).
- **Screws S-TP**: **8 silver pan/button Phillips screws**, head Ø ≈ **4.5 mm** (M2.5):
  - Left wing: **3** along the outer edge (y ≈ +18, +4, −10 at x ≈ −36), plus **1** near the chamfer (x −24, y +18).
  - Right wing: **4**: (x +24, y +18), (+38, +10), (+38, −4), (+38, −18) approximately.
  - They fasten the plate to the red side walls and to internal posts **(guess)**.

### 2.2 Front block / servo bay (FB)
- **Shape**: a **black printed part** filling the top plate's cut-out, with its top surface about **1 mm below** the carbon plate. Its front part is a **flat black deck** behind the wedge (y +16 to +30, x ±22). Inside the bay is a **raised black cradle** around the servo, about **28 × 30 mm**, with a **rounded rectangular boss** on top of the servo (a cover or the servo's own top).
- **Function**: servo mount and front structural member carrying the wedge screws.

### 2.3 Servo (SV), horn (HN), idler (IP)
- **SV**: a **black micro servo** (9 g class), seen from above inside the cradle. Its body is about **23 × 12 mm** in plan (the dark rectangle at the centre), lying with its **output shaft along X** (pointing left) at about **z ≈ 14, y ≈ −2** **(guess)**.
- **HN**: a **white plastic horn** visible at the servo's left side, where the **left arm strip** meets it. The arm strip is screwed to the horn.
- **IP**: on the servo's right side the **right arm strip** ends at a pivot (a screw through the cradle wall, coaxial with the servo output) **(guess)**.
- **Wires**: a **white 2-pin JST connector** with a **red wire** just in front of the servo (battery or ESC lead), and the **servo lead** (orange/red/brown) leaving its right-rear corner.

### 2.4 Arm strips (AR-L, AR-R)
- **Shape**: two **thin flat black strips** (spring steel painted/blued, or carbon strip), about **3–4 mm wide × 1 mm thick**, each about **95 mm long** from the pivot to the tip.
- **Spacing**: about **28 mm apart** (x ≈ ±14) at the pivot, staying **parallel** (they look slightly convergent in the photo through perspective).
- **Pivot**: at the servo's sides, **y ≈ −2, z ≈ 14**.
- **Pose in the photo**: **upright** (pointing up, maybe leaning a little forward). Seen from above and behind, they project toward the top of the image, crossing over the front wedge line.
- **Tips (TIP)**: each strip's top end is **bent into a small hook or loop** (about 5 mm), coated with a **clear blob** (hot glue or a clear rubber cap), Ø ≈ 4–5 mm. They are the **contact points** when the arm comes down on an opponent (soft tips to grip, or to stop the steel tip skating) **(guess)**.

### 2.5 Cross-bar (AX) and nuts (NT)
- **AX**: a **bent black steel strip**, about **4 mm wide**, forming a **flat-bottomed U**: a straight middle about **30 mm** long with ends bent at 90° to meet the arms. It ties the two strips together about **45–50 mm from the pivot**.
- **NT**: at each joint, a **black nylon nut or spacer** (about Ø 5 × 5 mm) on the **outside** of each arm strip, with an M2 nylon bolt through the strip and the bar's bent end.
- **Function**: makes the two strips act as one stiff frame against twisting.

### 2.6 Front wedge (WG) and screws (S-WG)
- **Shape**: a **stainless-steel strip**, about **0.8–1 mm** thick, **96 mm wide** (wider than the red walls by about 3 mm each side) and about **14 mm** deep (Y) along the slope. It slopes down from the top plate's front edge at about **30–35°** to the floor. Its **ends are folded back** round the front corners at about 45° (forming small corner cheeks about 6 mm long).
- **Screws S-WG**: **3 countersunk/pan screws** (head Ø ≈ 4 mm) along its **top edge**, at x ≈ −30, 0, +28, into the front block FB.
- **Finish**: bright, polished, with scratches.

### 2.7 Red side walls (SW-L, SW-R): wheel guards
- **Shape**: two **vertical red printed plates**, about **3 mm thick**, running the **full length** (y −36 to +30) at the outer edges (x ≈ ±45), about **20 mm tall** (guess). Their front ends reach just behind the wedge's folded corners; their rear ends wrap slightly round the rear corners (AWS63 shows red at the rear-left corner beside the wheel).
- **Function**: **wheel guards**: the wheels sit **inside** them, so the walls cover the wheels' outer faces completely.
- **Support (guard-to-chassis)**: the walls carry the top plate's outer screws along their tops, and are joined to the internal floor **(guess: printed integral with the floor tub)**.

### 2.8 Wheels (WH-FL, WH-FR, WH-RL, WH-RR)
- **Shape**: **small drums, Ø ≈ 18 mm × 14 mm wide**, black, with a **lumpy, glossy surface** (wrapped in black electrical tape, or coated with liquid rubber / silicone for grip).
- **Positions**: in the top plate's corner notches, centres at about **x = ±34, y = +22 (front)** and **y = −28 (rear)**, z = 9. Wheelbase about **50 mm**. Outer faces 2 mm inside the red walls.
- **Height**: tops at z ≈ 18, about level with the top plate (z ≈ 19) **(guess)**. If the wheels are just below the top plate, the robot is **not invertible** (and the arm would be underneath anyway).
- The front wheels are directly behind the wedge's corners.

### 2.9 Rear bar (RB), screws (S-RB), pin (PN)
- **RB**: a **carbon-fibre strip**, about **8 mm** tall (it reads as the top plate's rear edge plus a vertical rear plate), across the rear between the rear wheels, x ±26.
- **S-RB**: **2 silver countersunk Phillips screws** (head Ø ≈ 4.5) side by side at the rear centre (x ≈ −4 and +6).
- **PN**: a **brass/gold pin** about **Ø 1.5 × 12 mm**, lying along X on the rear face at the left (x ≈ −20). It is probably a **removable link pin** (a brass pin pushed between two contacts) or a **plug switch** **(guess, medium)**. A **small silver dot** on the right (x ≈ +22) is a screw head or LED.
- Several **small holes** along the rear strip (about Ø 2) are fixing holes or vents.

### 2.10 Motors and plastic motor mounts (hidden)
- **Guess**: **4 × N20 gearmotors**, one per wheel, lying along X at each corner (front pair at y +22, rear pair at y −28), with **printed cradles** in the floor tub, clamped by the top plate **(medium)**. An alternative is **2 motors with the front and rear wheels linked by belts** **(low)**.

---

## 3. Per-view descriptions

### 3.1 Top view (the photo is close to this)
- A 90 × 76 mm rectangle: red strips down both sides; a glossy carbon plate shaped like a U with a trapezoidal front cut-out; 4 black wheel blobs in the corners; a stainless strip across the front; a black servo bay in the middle; 8 + 2 silver screws; a brass pin at the rear left.
- The arm (when lying forward in its clamped pose) would appear as two thin parallel lines from the servo forward, about 28 mm apart, with a U-shaped cross-bar.

### 3.2 Front view (inferred)
- A low steel wedge across the full width, red side walls at the ends, the black front block above. The arm stands up from the middle like a tall narrow "H" (two strips + cross-bar), about 100 mm tall.

### 3.3 Side view (inferred)
- A red wall, 76 × 20 mm, hiding the wheels. The steel wedge slopes to the floor at the front. The arm rises from about the middle of the robot's length.

### 3.4 Rear view (inferred)
- The carbon rear strip with 2 screws, the brass pin and the rear wheels' backs inside the red walls.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 90 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| TP | U plate | 82 × 64 × 1.5 | 0.91 × 0.71 | carbon fibre | 8 × M2.5 | 1 |
| FB | printed bay | 44 × 46 × 16 | 0.49 × 0.51 | black FDM | to floor | 1 |
| SV | micro servo | 23 × 12 × 23 | — | black | in FB | 1 |
| HN | horn | 15 × 5 | — | white nylon | servo spline | 1 |
| AR | flat strip | 95 × 3.5 × 1 | 1.06 | black steel/CF | horn screw / idler | 2 |
| AX | U strip | 30 + 2 × 6, 4 wide | 0.33 | black steel | 2 nylon bolts | 1 |
| NT | nylon nut | Ø 5 × 5 | — | black nylon | — | 2 |
| TIP | hook + blob | Ø 5 | — | steel + clear glue | — | 2 |
| WG | bent strip | 96 × 14 × 0.9 | 1.07 × 0.16 | stainless | 3 screws | 1 |
| SW | side wall | 66 × 20 × 3 | 0.73 × 0.22 | red FDM | integral (guess) | 2 |
| WH | drum wheel | Ø 18 × 14 | 0.20 × 0.16 | black, taped | motor shaft | 4 |
| RB | rear strip | 52 × 8 × 1.5 | — | carbon | 2 × M2.5 | 1 |
| PN | brass pin | Ø 1.5 × 12 | — | brass | push-in | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP ↔ side wall tops | screwed | 0 |
| TP cut-out edge ↔ FB | side by side | 1 |
| SV ↔ FB cradle | clamped | 0 |
| AR-L ↔ HN | screwed | 0 |
| AR-R ↔ IP | pinned | 0 |
| AR inner faces ↔ FB cradle walls | outside the cradle | 1–2 |
| AX ↔ AR | bolted (NT) | 0 |
| WG ↔ FB front | 3 screws | 0 |
| WG front edge ↔ floor | touching | 0 |
| WG folded ends ↔ SW front ends | wraps round | 0–1 |
| WH outer face ↔ SW inner face | guarded | ~2 |
| WH ↔ TP notch edges | clear | 1–2 |
| WH bottom ↔ floor | touching | 0 |
| WH-F front ↔ WG rear | close | 2–3 |
| TIP ↔ floor (arm forward/down) | touching or above the wedge | 0 to +10 |
| PN ↔ RB | inserted | 0 |

---

## 6. Mechanism
1. **Drive**: 4WD skid steer (4 × N20 guessed), wheels in the corners behind the red walls.
2. **Arm (clamp)**: the servo turns the arm about the X axis through the servo output (y ≈ −2, z ≈ 14). From upright (the photo), rotating forward by about **100–110°** brings the tips down to about the wedge's front edge level: tip reach = pivot + 95 mm. At the forward-down pose the tips land at about y = −2 + 95·cos(θ) with θ measured below horizontal. For the tips to come down onto the wedge (y ≈ +36, z ≈ 6): cos θ ≈ 0.4 → θ ≈ 66° below… that would put the tips under the floor. So in practice the arm **comes down onto the top of an opponent** sitting on or in front of the wedge, at a height of 15–40 mm, and pins it. A 9 g servo at about 1.5 kg·cm gives only about 160 g force at 9.5 cm, enough to **hold** a 150 g opponent's front against the wedge while pushing, not to crush.
3. **Lifter reading (alternative)**: if the arm instead swings backward and is used to self-right, the robot can flip itself back over. This is plausible since the robot is not invertible on its wheels **(low-medium)**.

---

## 7. Assembly order (suggested rebuild)
1. Print the **floor tub** with the **red side walls** and the **motor cradles** at the corners.
2. Fit **4 N20 motors** and their wheels (tape-wrapped).
3. Print and fit the **black front block / servo bay**; mount the **servo** with its output to the left.
4. Install the electronics (battery, dual ESC, receiver) and the **brass link pin** contacts at the rear.
5. Screw the **carbon top plate** on (8 screws) and the **rear strip** (2 screws).
6. Screw the **steel wedge** to the front block (3 screws); fold its ends round the corners.
7. Fit the **left arm strip** to the servo horn and the **right strip** to the idler pivot; bolt the **cross-bar** between them with nylon bolts and nuts; add the **clear tips**.

---

## 8. Hidden / uncertain list
- Arm function (clamp vs self-righter) and its rotation range.
- Side wall height, whether the robot is invertible.
- Motor count/layout.
- What the brass pin is.
- Everything below the top plate.
- All dims ±20 % (single photo, near top-down).

## 9. Coordinate frame (restated)
Origin on the floor under the chassis centre; +X right; +Y forward; +Z up; mm. Top plate at z ≈ 19–20.5. Servo/arm pivot at (x ±14, y −2, z 14). Wheels at (±34, +22, 9) and (±34, −28, 9).

## 10. Profiles as math

**10.1 Top plate outline (plan).** Start from the rectangle |x| ≤ 41, y ∈ [−34, 30]. Remove: the 4 corner notches (|x| ≥ 26 and y ≥ 14) ∪ (|x| ≥ 26 and y ≤ −20); the central cut-out C = {|x| ≤ 22 − max(0, 16 − y)·(7/14)… simplified: |x| ≤ 15 for y ∈ [−14, 16]} ∪ {|x| ≤ 15 + (y − 16) for y ∈ [16, 23]} ∪ {|x| ≤ 22 for y ∈ [23, 30]} (45° chamfers).

**10.2 Arm (side view, upright).** Line from the pivot P = (y −2, z 14) to the tip T = (y +4, z 108) (leaning 3–4° forward). Rotation by θ about P (forward positive): T(θ) = P + 95·(sin(θ + 3.6°), cos(θ + 3.6°)).

**10.3 Cross-bar.** In the XZ plane at the arm's mid-length (s = 48 mm along the arm): segment from (−14, s) to (+14, s) offset 4 mm behind the strips; bent legs 6 mm long at each end.

**10.4 Wedge (YZ section).** Line from (y 30, z 9) to (y 39, z 1) … slope atan(8/9) ≈ 42°? The photo foreshortening suggests 30–35°; rebuild: from (30, 8) to (42, 0), 34°, thickness 0.9. Corner folds: the strip's ends rotate 45° about vertical lines at x = ±45.

**10.5 Wheel.** Cylinder r = 9 about the X axis, |x| ∈ [27, 41], with a lumpy surface r(φ) = 9 + 0.3·sin(7φ)·sin(3x) (cosmetic).

## 11. Pixel-based measurements (native 679 × 675; ±5 px)
- Red wall outer edges: x ≈ 50 and ≈ 610 → 560 px across (at the rear); at the front x ≈ 60–600.
- Steel wedge: x ≈ 40–620 (580 px), y ≈ 280–325.
- Rear strip bottom edge: y ≈ 600; top plate front edge: y ≈ 320 → body length ≈ 280 px.
- Wheel blobs: ≈ 65 × 85 px (front-left), ≈ 70 × 80 (rear-left).
- Servo dark body: ≈ 115 × 60 px.
- Screw heads: ≈ 25 px.
- Arm strips: x ≈ 210 and ≈ 395 at the cross-bar (185 px apart); tips at y ≈ 25–60.
- Cross-bar: x ≈ 230–395 at y ≈ 245.

## 12. Several independent estimates

| Quantity | Method A (W = 90 → 6.2 px/mm) | Method B (servo 23 mm long) | Method C (screw head 4.5 mm) | Reconciled |
|---|---|---|---|---|
| px/mm | 560 / 90 = 6.2 | 115 / 23 = 5.0 (servo is lower than the plate, but the camera is above; small effect) | 25 / 4.5 = 5.6 | **5.6** |
| Overall width | 90 (assumed) | 560 / 5.0 = 112 (too big for the cube) | 560 / 5.6 = 100 | **94** |
| Body length | 280 / 6.2 / sin 72° = 47?? (see §13) | — | — | **76** |
| Wheel Ø | 85 / 6.2 = 14 (top-down: wheel length along Y = Ø) | 85 / 5 = 17 | 85 / 5.6 = 15 | **16–18** |
| Arm strip spacing | 185 / 6.2 = 30 (at the cross-bar, nearer the camera → inflated) | — | — | **28** |

## 13. Consistency check
1. **Overall width**: the servo-based scale gives 112 mm, over the cube; the screw-based gives 100. A 9 g servo in plan is 23 × 12, but the visible dark rectangle could include the cradle rim, so its length is overestimated. **Reconciled: 94 mm across the wedge, 90 across the red walls.**
2. **Body length**: the camera looks down at 70–75° from behind, so Y lengths are foreshortened only by about 5 % (sin 72°). 280 px / 5.6 / 0.95 = **53 mm** from the wedge root to the rear strip. With the wedge (12 mm) that is **65 mm**; the earlier 76 mm figure is too long. **Reconciled: chassis 60 mm long (y −32 to +28), wedge to y +40.** The coordinates in §2 (y ∈ [−34, +30]) are within 4 mm of this, which is inside the error.
3. **Arm length**: the strips appear about 300 px long from the pivot to the tips in the image. If they were lying flat they would be 300 / 5.6 = 54 mm long and reach only to the wedge. Since the tips appear **beyond** the wedge (at the top of the image, 270 px ahead of the pivot), and an upright arm seen from 72° elevation projects as L·cos 72°… = 0.31 L forward, a 95 mm upright arm would project to only about 30 mm, i.e. about 165 px. A **forward-leaning arm at about 45°** projects 95·sin(45°)… ≈ 67 mm ≈ 375 px. The observed 270–300 px fits an arm **leaning forward about 30° from vertical**, about **90–95 mm long**. **Consistent with a tall arm in a half-raised pose.**
4. **Arm vs cube**: a 95 mm arm upright on a pivot at z = 14 reaches z = 109, over 101.6 mm. Either the arm is about 85 mm long or the start pose is leaning. **Reconciled: arm 88 mm long**, which still matches the photo within error.
5. **Mass**: CF plate 8 g, tub/walls 25 g, front block 6 g, steel wedge 10 g, servo 9 g, arm + bar 8 g, 4 N20 + wheels 44 g, battery 12 g, ESC/RX 8 g, screws 5 g; total ≈ 135 g. **Consistent** with 150 g.

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Steel wedge across the full width**
  - Getting under: a thin metal edge (≤ 1 mm) gets under printed wedges in a wedge-vs-wedge meeting. Being wider than the body, it also covers the front wheels.
  - Adversarial: spinners hit steel, not plastic; the folded ends deflect hits from the front corners away from the side walls.
- **Clamp arm (two thin strips + cross-bar)**
  - Attack: once the opponent is on the wedge, the arm comes down on top of it and **traps** it ("Trappist"), adding downforce on the opponent's front so it cannot drive off, and letting Trappist push it to the arena edge or pit.
  - Adversarial: the arm is the most exposed part (tall, thin). It is made of **flexible thin strips** that bend rather than break, and the two-strip frame with a cross-bar has little area for a spinner to hit. Soft tips stop it skating off the opponent.
  - Alternative use: self-righting (pushing off the floor when the robot is inverted).
- **Micro servo**: light and simple. The arm's job is holding, not lifting heavy weights, so a small servo is enough.
- **Carbon top plate**: very stiff and light; good protection against an overhead weapon or an opponent climbing over. Its central cut-out saves weight and makes room for the servo and arm.
- **Red side walls (wheel guards)**: cover the wheels' outer faces against horizontal spinners and side pushes. They also stiffen the chassis.
- **Wheels in the corners**: a short, wide wheelbase for agility; four driven wheels for pushing traction. Tape or rubber coating improves grip on the arena floor.
- **Rear brass pin (link)**: a removable link at the back is safe to reach (away from the arm and wedge) and cannot be switched off by an impact.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 along X | 12 × 10 × 25 | (±20, +22, 9), (±20, −28, 9) | medium |
| Motor cradles | printed pockets in the floor tub | 14 × 12 × 12 | at the motors | medium |
| Battery | 2S LiPo 180–250 mAh | 40 × 18 × 10 | across the rear band, (0, −24, 9) | medium |
| ESC | 2 × dual brushed or one 4-ch ESC | 20 × 15 × 4 | under the left wing | low |
| Receiver | 2.4 GHz micro rx | 18 × 12 × 4 | under the right wing | low |
| Link contacts | two brass sockets for the pin | — | (−20, −34, 10) | low |
| Floor tub | printed 1.5 mm floor joined to the side walls | 84 × 60 | z 2–3.5 | medium |
| Servo screws | 2 × M2 through the servo tabs into FB | — | (0, ±14, 14) | medium |
| Idler pivot | M2 screw through the cradle wall with a nylon washer | — | (+14, −2, 14) | medium |
| Wiring | battery → pin link → ESCs → 4 motors; RX → servo; JST visible in front of the servo | — | — | medium |

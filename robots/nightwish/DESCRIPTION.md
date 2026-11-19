# Nightwish: full rebuild description from reference photos

Source photos:
- `robots/nightwish/reference/nightwish_aws62.webp` (AWS 62, 680 × 510 px). The **best photo**. Taken in **low blue/violet light** on a black leather surface, camera **low (about 10–15° above the floor)** at the robot's **right-front-ish side**: the robot's **right side** faces the camera, the **front (forks) points to the right** of the image and slightly toward the camera. Visible: the right wheel, the right side of the glittered body, both aluminium-faced fork wedges, the crescent arm, the near (right) bat wing and the far (left) bat wing's claw tips, and the root of a tall spike. Not visible: left side, rear, underside.
- `robots/nightwish/reference/nightwish.aws63.webp` (AWS 63, 424 × 380 px, **motion-blurred**). Camera **high (about 50–60°)** from the robot's **right-rear/right side**; the forks point to the **left** of the image. Shows the top: the crescent arm reaching forward over the forks, the bat wings/spikes at the top-right, the right wheel at the bottom-right, both fork wedges at the left with aluminium faces.
- `robots/nightwish/reference/nightwish_bestboi.webp` (2880 × 1800 px, an arena video frame; the robot is only about **240 × 200 px**). Robot in the near corner of a clear-walled arena, seen through scratched polycarbonate from high front-left. Shows an **earlier or alternative configuration**: a **flat aluminium plate** on the front, a **swirl ("hypno spiral") sticker disc**, a **Y-shaped double spike** on top, and black wheels at the corners. Little detail is usable (see 3.3).

Everything stated as fact is read from the photos. Anything inferred is marked **(guess)**. Dimensions in mm are **estimates**. Absolute scale comes from: the AWS 150 g / 101.6 mm cube, the **pan-head screws** on the fork plates (read as M2.5–M3, head Ø ≈ 5 mm), the tyre (read as a ~Ø 26 mm treaded micro-crawler tyre), and the kit draft (`kit.json`: lifter, body 78 × 62 × 28, ramp 26, two wheels r 12 × 10 at y −25, two forks length 40, width 18, spread 46, tilt 24°, thickness 2). Ratios are given against **W = body width ≈ 60 mm**. **The photos are few, dark and blurry, so confidence is generally lower than for other robots; the description is still complete but many sizes are ±20%.**

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the fork tips), **+Z** = up. Units mm.
- **Origin O** = floor point (z = 0) under the centre of the main body box (mid-width, mid-length of the black box, not counting forks or wheels).
- In aws62: +Y points to the right of the image (and a little toward the camera), +X toward the camera, +Z up.
- In aws63: +Y points to the left of the image, +X toward the bottom of the image (camera on the right side), +Z up/out of the image.

| ID | Part |
|---|---|
| BX | main body box (black, glitter-painted) |
| TP | flat black top plate / lid |
| S-TP | brass/silver pan screws on the lid |
| NS | sloped lower nose / side skirt under the forks (glittered) |
| FK-L, FK-R | two fork wedges (black printed blocks) |
| AP-L, AP-R | aluminium sheet facings on the fork wedges |
| S-AP | pan-head screws holding the aluminium facings (2 per fork) |
| CA | crescent arm (black, glittered, with round lightening holes) |
| CH | crescent hook tip |
| LH | round lightening holes in CA |
| SP | tall spike(s) on top at the crescent root (Y-shaped pair in bestboi) |
| BW-L, BW-R | bat wings (flat scalloped plates over the wheels) |
| WC | claw points on the bat wings' trailing edges |
| WH-L, WH-R | rear drive wheels with treaded tyres |
| ACT | crescent arm actuator (servo, hidden, guess) |
| M-L, M-R | drive motors (hidden) |
| BAT, ESC, RX, SW | electronics (hidden) |
| SPR (bestboi) | spiral-printed round sticker/disc |
| AFP (bestboi) | flat aluminium front/top plate |

---

## 1. Overall description in one paragraph

Nightwish is a **gothic-themed two-wheel fork/wedge robot with an overhead crescent "clamp" arm**, finished in **gloss black paint dusted with silver and holographic glitter** (a night sky). A compact **black box body about 60 mm wide, 50 mm long and 28 mm tall** sits on two **chunky treaded black tyres (Ø ≈ 26 mm)** at the rear. In front, two **separate fork wedges about 18 mm wide**, spaced about 28 mm apart, slope from the body top down to the floor; each is faced with a **bent aluminium sheet** held by two pan screws, with a **steep upper face** and a **shallower lower ramp** (about 25°) ending in a thin edge. From the top of the body a **black crescent arm about 10 mm thick** rises and arcs forward like a scorpion tail or a scythe, pierced by **five or six round holes**, its **hooked tip** hanging over the forks. Each side carries a **flat "bat wing"** plate with a scalloped trailing edge and three or four claw points, sweeping back over the wheel, and a **tall spike** (a Y-shaped pair in one photo) stands on top at the arm root. The kit calls it a lifter; the photos show no lift mechanism in the forks, and the crescent arm is the only plausible moving part: it most likely **swings down to clamp/stab an opponent sitting on the forks (guess, medium)**.

---

## 2. Part-by-part description

### 2.1 Main body box (BX)
- **Shape**: a rectangular box about **60 mm wide (x ±30) × 50 mm long (y −35 to +15) × 28 mm tall (z 0–28)**. Vertical side walls at the rear; at the front-lower part the sides **slope inward and downward** (NS, 2.3), so the side silhouette is a box at the rear and a wedge-shaped nose at the front.
- **Finish**: **gloss black** with heavy **silver and multicolour glitter** (flakes 0.5–2 mm) on the side walls, nose, wings and arm. The lid TP is **less glittered, matt-black**, suggesting a separate part (printed or carbon/G10) left plain.
- **Material**: printed PLA/PETG (layer texture faintly visible on the lid and fork blocks) (guess, medium).

### 2.2 Top plate (TP) and screws (S-TP)
- **Shape**: a **flat black plate** about **1.5–2 mm thick**, covering the top of BX from the arm root back to the rear, about **50 × 45 mm**, its top at **z ≈ 28–30**. Its front edge forms a **step** (about 4 mm high) down to the front block where the forks attach (aws62 crop px (300–620, 280–420)).
- **Screws**: at least **one bright brass/zinc pan-head screw** (head Ø ≈ 4.5 mm) at its front-right corner, about **(+26, +10, 30)** (aws62 crop px (530, 385)). Probably **4 corner screws** in total (guess, medium).

### 2.3 Nose / side skirts (NS)
- **Shape**: below the forks and lid, the lower front of each side wall is **sloped**: from the lid edge at z ≈ 22 down to the floor, running forward at about **35°**, glittered. In aws62 the near side shows this as a **broad glittered surface** from the wheel forward to the fork tips, narrowing to the front (crop px (280–700, 380–620)). It behaves as an inner **wedge skirt** that fills the area under the forks' outer edges.
- **Extent**: from y ≈ −10 (just in front of the wheel) to y ≈ +45, outer face at x ≈ ±30.

### 2.4 Fork wedges (FK-L, FK-R) and aluminium facings (AP-L, AP-R)
- **Blocks**: two **black printed wedge blocks**, each about **18 mm wide (X)**, centred at **x ≈ ±23** (spread 46 centre to centre, kit), so they occupy x ±14 to ±32, leaving a **28 mm wide open channel** between them in which the floor is visible (aws62, the gap between the two aluminium faces).
- **Side profile** (each, in YZ): a **two-slope wedge**:
  - **Upper face**: from the body top at about (y +12, z 28) steeply down and forward at about **60–65°** to a crease at about (y +22, z 12).
  - **Lower ramp**: from the crease at (y +22, z 12) at about **24°** down to a **thin tip** on the floor at about (y +52, z 0).
  - **Rear**: attached to the front of BX; the inner faces (toward the channel) are **vertical black walls** (visible on the far fork in aws62).
- **Aluminium facings (AP)**: each wedge's top surfaces are covered by a **single bent aluminium sheet**, about **0.5–0.8 mm thick**, **18 mm wide**, following the crease (bent about 35°), from the top of the upper face to about **1–2 mm beyond** the plastic at the tip (the sheet forms the actual leading edge). The far end of the near sheet has a **slightly ragged, angled corner** (cut at about 10° off square). Colour: bright satin aluminium (blue-tinted in aws62's light).
- **Screws (S-AP)**: **two pan-head screws per fork**, head Ø ≈ 4.5–5 mm, silver/brass: one in the **upper face** about 5 mm below its top, one in the **lower ramp** about 2/3 of the way to the tip. Near fork (FK-R): at about (+23, +16, 21) and (+23, +40, 5). Far fork (FK-L): mirrored. All 4 screws are on the fork centre lines.
- **Overall**: fork length (plan) **about 40 mm** in front of BX (y +12 to +52), matching kit `length 40`.

### 2.5 Crescent arm (CA), hook (CH) and holes (LH)
- **Shape**: a **flat crescent / scythe plate** about **8–10 mm thick (X)** lying in the **YZ plane at x ≈ 0** (centre line). Its spine is an **arc of about 150°**:
  - **Root**: a **thicker block** (about 14 × 14 mm in section) standing on the body top at about **(0, −2, 28)**, rising vertically.
  - **Arc**: from the root it rises to a **crest at about z 62** above y ≈ +10, and curves forward and down to the **hook tip CH** at about **(0, +42, 38)**, the tip pointing **down and slightly back** (like a talon).
  - **Section width (radial)**: about **12 mm** at the root, tapering to **8 mm** in the middle and **4 mm** at the tip; the inner (concave) edge is smooth, the outer (convex) edge carries **a few small scallops/notches** near the tip (aws62 shows a bumpy outer edge).
- **Holes (LH)**: **5–6 round holes** along the arc's mid-line, each about **Ø 6–7 mm** near the root, decreasing to about **Ø 4 mm** toward the tip, spaced about **9–10 mm** along the arc. The holes are lightening and decorative (they glow blue in aws62 as the light shines through).
- **Finish**: gloss black with silver glitter.
- **Pivot**: the root block is where it meets the body; a **horizontal pivot along X** at about (0, −2, 26) is assumed (guess, medium) so the arm can swing forward/down until the hook meets the forks' channel.

### 2.6 Spike(s) on top (SP)
- **aws62**: a **tall thin black glittered spike** (about 6 mm wide, tapering) rises from the arm root, going **up and slightly back**, cut off by the top of the frame; visible length at least **25 mm**, top at z ≥ 70 (guess: z ≈ 85).
- **bestboi**: a **Y- or V-shaped double spike** (two prongs diverging at about 60°, each about 15 mm long) standing on top at the centre.
- **aws63**: dark spiky shapes at the top centre/right, consistent with the spike(s) plus the wing claws.
- Reconciled: a **V/Y pair of horns** (devil horns / bat ears) about **15–20 mm** tall above the arm root, each about 5 mm wide at the base, tapering to points, splayed ±30° from vertical in the XZ plane. In aws62 one prong is seen nearly edge-on as the single tall spike (medium).

### 2.7 Bat wings (BW-L, BW-R) and claws (WC)
- **Shape**: flat **plates about 1.5–2 mm thick**, glittered black, mounted near **z ≈ 30–32** at each side of the body top, **extending outward and backward** over the wheels like folded bat wings. Each wing is about **55 mm long (Y)** and **18–22 mm wide (X)**, its outer edge reaching about **x ±42**.
- **Outline**: a **straight leading edge** (outer edge) running from the arm root area (y ≈ +5) back to a **sharp rear point** at about y −50 (beyond the wheel rear), and a **scalloped trailing edge** (inner/lower edge) with **3–4 concave arcs** between **pointed claws** (WC). The far wing in aws62 shows **3–4 finger-like claw points** sticking forward/up (crop px (370–420, 50–130)), so the far wing may be angled up (about 20–30°) rather than flat.
- **Mount**: screwed or glued to the lid sides; a small **slot or hole** is visible in the near wing at its root (aws62 crop px (440, 270)), likely a screw (guess, medium).
- **Function**: decoration (bat theme), and **top cover over the wheels** (partial wheel guards) (guess).

### 2.8 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 26 mm × 10 mm** tyres with **chunky block tread** (alternating lugs about 2 mm tall and 3 mm wide, like an RC crawler tyre), black rubber. The hub is a **black plastic rim** with a **recessed face** about 4 mm deep and a **central hub boss** Ø ≈ 8 mm.
- **Position**: rear, **outside the body**: centres at about **(±36, −25, 13)** (kit y −25). Outer faces at x ±41.
- **Height**: wheel top at z 26, slightly below the lid (z 28–30); the wings sit over the wheels.

### 2.9 Bestboi-only features
- **AFP**: a **flat aluminium rectangle**, about **60 × 40 mm**, covering the front/top, tilted (a wedge plate), with a darker square near its middle (a hole or sticker).
- **SPR**: a **round disc about Ø 30 mm** on the left-front with a **black-on-white spiral** (two-turn spiral) printed on it, like a hypnotic eye.
- A **silver curved plate** at the right side (one fork facing seen edge-on), and **four dark round shapes** at the corners (two wheels plus two rear posts or the other configuration's four wheels, guess low).
- A red glow under the robot (an underglow LED or the receiver light, guess low).
- Reconciled: bestboi is an **earlier/alternative top configuration** (flat aluminium wedge-lid and spiral); the AWS photos (62, 63) are the reference for the build.

### 2.10 Hidden internals
- **ACT**: micro servo under the arm root (guess, medium).
- **Drive**: two N20 gearmotors at the rear driving the wheels directly.
- **Electronics**: 2S LiPo, receiver, dual brushed ESC, switch.

---

## 3. Per-view sections

### 3.1 aws62 (low right side, front to the right)
- Left: the **right wheel** (big, treaded), above it the **near bat wing** sweeping back to a point at the far left.
- Middle: the glittered right side of the body, the **matt black lid** with a brass screw at its front corner, the **glittered sloping nose** below.
- Right: the **two aluminium-faced forks** (near one large at the lower right with 2 screws, far one higher and smaller with 2 screws), the open channel between them; above, the **crescent arm** arcing from the body top to the upper right, holes glowing blue, the hook tip at the far upper right; at the top-left of the arm, the **spike** rising out of frame; behind the arm, the far wing's **claw tips**.

### 3.2 aws63 (high, right side, front to the left, blurred)
- The **two forks** at the left (aluminium tops, upper one is the left fork, lower one the right fork), separated by a dark gap; the **crescent arm** seen from above as a curved black band from the body centre reaching left with its hook at the top-left; the **body** as a dark rectangle with glitter; the **right wheel** at the bottom-right corner; spiky wing/horn silhouettes at the top-right.

### 3.3 bestboi (arena, high, front-left, small)
- As described in 2.9: a flat aluminium plate on the front, spiral disc, Y-shaped horn pair on top, wheels at the corners, aluminium fork side plate at the right.

### 3.4 Top view (synthesised)
- Rear: BX 60 × 50 with the lid; wheels 10 mm wide sticking out at the rear corners (overall width ≈ 82); wings above the wheels out to ±42.
- Front: the **two 18 mm fork strips** at x ±14…±32, from y +12 to +52, with the 28 mm channel; the **crescent** a 10 mm band along x = 0 from y −2 to +42.
- Overall length: wheel rear y −38 / wing tips y −50 to fork tips y +52: about **90–102 mm** (see section 12).

### 3.5 Right side view
- Wheel Ø 26 at the rear; box 28 tall; two-slope fork profile in front; crescent arc above, crest z ≈ 62, hook down to z ≈ 38 at y +42; spike to z ≈ 85; wing as a thin line at z 30–32 over the wheel.

### 3.6 Front view
- Two aluminium fork faces at the bottom, 18 wide each with a 28 mm gap; behind, the body 60 wide and the two wheels; the crescent edge-on (10 mm) in the middle with the hook in front; horns at the top; wings as thin lines out to ±42.

### 3.7 Rear and underside (not photographed)
- Rear: flat black wall between the wheels with the wings' pointed ends sticking out (guess). Underside: flat floor, wheels at the rear, fork tips at the front: three/four-point stance.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BX | box with sloped nose | 60 × 50 × 28 | 1 × 0.83 × 0.47 | black + glitter, FDM | — | 1 |
| TP | flat plate | 50 × 45 × 2 | 0.83 × 0.75 | matt black | 4 screws (guess) | 1 |
| S-TP | pan head | Ø 4.5 | — | brass/zinc | — | 4 (1 seen) |
| NS | sloped skirts | 55 long, 35° | — | black + glitter | integral | 2 |
| FK | two-slope wedge block | 18 × 40 × 28 | 0.3 × 0.67 | black FDM | to BX | 2 |
| AP | bent Al sheet | 18 × ≈ 50 (developed) × 0.6 | 0.3 | aluminium | 2 screws each | 2 |
| S-AP | pan head | Ø 4.5–5 | — | silver | — | 4 |
| CA | crescent plate with holes | arc r ≈ 28, band 12→4, 9 thick | — | black + glitter | pivot (guess) | 1 |
| LH | round holes | Ø 7 → 4 | — | — | — | 5–6 |
| SP | V/Y horn pair | 15–20 tall, 5 base | — | black + glitter | on CA root | 1 pair |
| BW | scalloped flat wing | 55 × 20 × 1.5 | 0.92 × 0.33 | black + glitter | screw/glue | 2 |
| WH | treaded tyre on rim | Ø 26 × 10 | 0.43 × 0.17 | black rubber | motor shaft | 2 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP ↔ BX | screwed on | 0 |
| FK ↔ BX front | bolted/glued | 0 |
| AP ↔ FK | screwed flat | 0 |
| AP tip ↔ floor | touching | 0–0.5 |
| AP tip ↔ FK tip | sheet overhangs | 1–2 |
| FK-L inner face ↔ FK-R inner face | channel | 28 |
| CA root ↔ TP | on pivot/mount | 0–1 |
| CA hook tip ↔ fork channel floor (rest) | above | ≈ 35 |
| CA hook tip ↔ fork ramp (arm lowered, guess) | closes on | 0–5 |
| CA ↔ FK (X) | in the channel centre, clear | 9–10 each side |
| SP ↔ CA root | integral | 0 |
| BW ↔ TP side | mounted | 0 |
| BW underside ↔ WH top | wing above wheel | 4–6 |
| BW outer edge ↔ WH outer face | wing slightly beyond | ≈ 1 |
| WH inner face ↔ BX side | near | 1–2 |
| WH bottom ↔ floor | touching | 0 |
| NS ↔ floor | skims at front | 0.5–1 |

---

## 6. Mechanism
1. **Drive**: two rear wheels, differential steering; the fork tips carry the front.
2. **Forks**: two fixed aluminium-edged wedges get under opponents; the two-slope profile lifts an opponent's edge steeply onto the body front once it is past the shallow ramp, and the channel between the forks catches corners and wheels.
3. **Crescent arm** (guess, medium): a servo rotates the arm about an X axis at its root, bringing the hook **down onto the opponent** held on the forks (a clamp/"crusher" or a stab), or lifting it. The kit's "lifter" label may come from this arm being used to lift/hook opponents. The arm's thin section and holes make it too weak for a heavy hit; a **controller/clamp** role is most consistent.
4. **Invertibility**: wheels (Ø 26) do not reach above the lid (z 28–30) and the arm/horns stick up 30–55 mm, so the robot **cannot drive inverted**; the arm may help self-right (guess, low).

---

## 7. Assembly order (suggested rebuild)
1. Print BX (with motor cradles and a servo pocket at the top-centre), two FK blocks, TP, CA (with horns), two BW wings; paint gloss black and sprinkle glitter on the wet paint (all except TP).
2. Fit drive motors and wheels.
3. Fit the servo; mount CA on its horn through the lid opening.
4. Fit battery, ESC, receiver, switch.
5. Bolt FK blocks to the front; bend AP sheets over them and screw (2 each).
6. Screw on TP; glue/screw BW wings at the lid sides.

---

## 8. Coordinate frame (restated)
- BX: x ±30, y −35…+15, z 0…28 (lid to 30).
- FK: x ±14…±32, y +12…+52; crease at (y +22, z 12).
- CA: plane x 0 (±4.5 thick); root (0, −2, 28); crest (0, +12, 62); hook tip (0, +42, 38).
- Wheels: (±36, −25, 13), Ø 26, w 10. Wings at z 30–32, x ±22…±42, y +5…−50.

## 9. Profiles as math

**9.1 Fork side profile (YZ), each fork.**
- Upper face: line (12, 28) → (22, 12): z = 28 − 1.6·(y − 12) (58°).
- Lower ramp: line (22, 12) → (52, 0): z = 12 − 0.4·(y − 22) (21.8°, kit 24°).
- Bottom z = 0 from y 12 to 52; inner/outer faces vertical planes x = ±14, ±32.

**9.2 Crescent arm (YZ plane).**
- Spine: circle arc, centre C = (y +14, z 34), radius R = 28, from angle θ = 180° + 10° (root side, point (−13.6, 29); joined to the root block by a vertical segment from (−2, 28) → (−2, 45) blended) through θ = 90° (crest (14, 62)) to θ = −20° (tip region (40, 24.4)), then hooking back: the last 8 mm curl to θ = −45° with the radius shrinking to 22.
- Simpler: spine as a cubic Bézier P0 = (y −2, z 30), P1 = (y −2, z 70), P2 = (y 44, z 72), P3 = (y 42, z 38).
- Band width w(s) = 12 − 8·s for s ∈ [0, 1] along the spine; thickness 9 in X.
- Holes: centres at s = 0.18, 0.32, 0.46, 0.6, 0.74 (and 0.86 optional) on the spine, radius r(s) = 3.5 − 1.5·s.

**9.3 Bat wing (plan, XY, right wing; left mirrored).**
- Leading/outer edge: line from (22, +5) to (42, −10) then to (30, −50) (rear point).
- Trailing/inner edge: three circular scallops between claw points at (26, −14), (28, −26), (30, −38): each scallop is an arc of radius 7 bulging toward +X between consecutive claws, starting from (22, +5) and ending at (30, −50).

**9.4 Tyre.**
- r(φ) = 13 + 1·[cos(18φ) > 0] (18 lug pairs), width 10, rim recess 4 deep, hub boss r 4.

**9.5 Horns.**
- Each a cone-like tapered prism from base 5 × 5 at (±3, −2, 45) along direction (±sin 30°, 0, cos 30°) for 18 mm to a point.

## 10. Pixel-based measurements (aws62 native 680 × 510, ±5 px)
- Right wheel: x 35–185, y 255–375 (tyre ≈ 120–150 px tall). Wheel centre ≈ (110, 315).
- Near fork aluminium: top crease (300, 260), tip corner (505, 460); screws (390, 345), (455, 395).
- Far fork aluminium: (340, 175)–(505, 290); screws (425, 213), (470, 255).
- Crescent: root (330, 110), crest (470, 40), hook tip (570, 190); holes at about (370, 160), (410, 115), (450, 100), (490, 110), (525, 125)...
- Lid screw: (315, 290). Near wing: (15, 230)–(310, 205)–(250, 255). Spike: (395–430, 0–80).

## 11. Several independent estimates of key quantities

| Quantity | Method A (kit / rules) | Method B (ratios in photo) | Method C (pixels + screw scale) | Reconciled |
|---|---|---|---|---|
| Scale at near fork | — | — | screw head ≈ 22 px = 5 mm → 4.4 px/mm | **4.4 px/mm (near fork)** |
| Wheel Ø | kit 24 | ≈ 0.9 × body height 28 → 25 | 130 px at ≈ 5 px/mm (wheel nearer camera) → 26 | **26** |
| Fork width | kit 18 | ≈ 0.3 × body width | AP width ≈ 80 px / 4.4 → 18 | **18** |
| Fork length (plan) | kit 40 | ≈ 1.5 × wheel Ø → 39 | — | **40** |
| Fork ramp angle | kit 24° | lower ramp looks ≈ 20–25° in side view | — | **22–24°** |
| Body width | kit 62 | 2 forks 18 + gap 28 = 64 outer span | — | **60–64** |
| Body height | kit 28 | ≈ wheel Ø + 2 | — | **28** |
| Crescent crest height | — | ≈ 2.2 × body height → 62 | crest 270 px above floor at ≈ 4 px/mm → 67 | **62–65** |
| Crescent hole Ø | — | ≈ 0.25 × wheel Ø → 6.5 | 28 px / 4.2 → 6.7 | **6.5 (largest)** |
| Overall length | ≤ 101.6 | wheel rear −38 to fork tip +52 = 90 | — | **90 (wings to −50 → 102, see 12)** |

## 12. Consistency check: conflicts and reconciliation
1. **Cube limit with wings**: wing rear points at y −50 plus fork tips at +52 give 102 mm, just over 101.6. Reconciled: shorten wings to end at **y −46** (total 98).
2. **Height with horns**: crescent crest ≈ 62–65, horns to 85 if the single spike in aws62 is as tall as it looks; under 101.6, fine.
3. **"Lifter" vs photos**: the kit label says lifter but the forks are visibly fixed (screwed sheet over printed blocks rigidly attached). The only candidate moving part is the crescent. Kept as **servo crescent clamp/hook (medium)**.
4. **Bestboi config**: shows a flat aluminium plate and spiral not present in AWS 62/63; treated as a different event's configuration (low weight in the reconciliation).
5. **Wheel outside vs wings**: wheels outboard at ±36 with wings above to ±42: wing covers the wheel top, consistent with aws62 (wing directly over the wheel).
6. **Mass**: printed body + forks ≈ 40 g, aluminium 6 g, crescent + horns + wings ≈ 15 g, motors 20 g, wheels 10 g, servo 9 g, battery 15 g, electronics 8 g, paint/glitter 3 g: ≈ 126 g < 150. Consistent.

---

## 13. Why the designer did it (per part, adversarial)

- **Two separate forks with aluminium faces (FK, AP)**
  - Getting under: the thin aluminium edge, overhanging the printed tip, gets under opponents better than plastic; two narrow forks touch the floor at only two places, so they stay flat on uneven arena floors (a single wide wedge rocks on high spots).
  - The **channel** between them catches an opponent's corner or wheel, and gives the crescent hook room to come down without hitting the forks.
  - The **two-slope profile**: the shallow 24° ramp gets under; the steep upper face stops an opponent from riding all the way over the robot, keeping it in front where the hook can reach.
  - Against spinners: the metal faces spread hits and stop the printed blocks from being gouged; screws allow quick replacement.
- **Sloped nose skirts (NS)**
  - Close the area beside and under the forks so opponents do not get under the body edges; deflect side hits upward.
- **Crescent arm (CA)**
  - Fight (guess): hooks down on an opponent lifted onto the forks, holding it while the robot pushes (a "clamp" in the AWS sense) or pierces thin lids. The hook geometry concentrates force at the tip.
  - Lightening holes keep the arm light (servo torque limited) and the moment of inertia low for fast swings.
  - Against attacks: a high, thin arm is exposed to vertical spinners; cheap to reprint.
- **Horns and bat wings (SP, BW)**
  - Theme (Nightwish: night, bat, gothic). The wings also act as **partial wheel guards** from above (blocking overhead hits and opponents riding over the wheels), and their pointed ends make the robot harder to push from the rear corners.
  - Weakness: thin plates break easily; they are cosmetic.
- **Treaded tyres**
  - Grip for pushing; the tall lugs bite on dusty arena floors.
- **Glitter paint**
  - Cosmetic; zero performance cost (a few grams).
- **Matt lid with screws**
  - Easy access; plain so the screws can be found.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Arm servo | micro metal-gear servo, output along X | 23 × 12 × 23 | (0, −5, 15) under the arm root | medium |
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | (±18, −25, 13) | medium |
| Battery | 2S LiPo 180–300 mAh | 35 × 18 × 10 | front of BX under the lid (0, +5, 8) | medium |
| ESC + receiver | dual brushed ESC + micro RX | 25 × 15 × 6 | rear-centre | medium |
| Switch | slide switch or link at the rear wall | 10 × 6 | rear | low |
| Fork mounting | 2 screws per fork into BX front | M2.5 | (±23, +14, 10) | medium |
| Wing mounting | 1–2 screws each into lid sides | M2 | (±26, −5, 30) | low |
| Underglow LED | red LED (bestboi glow) | — | underside | low |

## 15. What the photos cannot show
- Whether the crescent moves, and how; the left side, rear, underside.
- Exact wing outlines and horn shape (blurry/dark photos).
- All dimensions are scaled estimates (±20%); the photos are dark (aws62), blurry (aws63) and tiny (bestboi).

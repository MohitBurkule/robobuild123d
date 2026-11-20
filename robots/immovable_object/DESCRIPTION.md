# Immovable Object: full rebuild description from reference photos

Source photos (all cut out onto white by the AWS wiki):
- `robots/immovable_object/reference/immovable_object.aws69.webp`: AWS 69, 1419 × 1132 px. **Front-right, high** three-quarter (camera about 35–40° above the floor, about 30° to the robot's right of straight-on). Fitted with **three** steel forks. Orange-red front plough with a polygonal (flat-topped) top edge, two holes in its face, and a black-taped switch on the lid.
- `robots/immovable_object/reference/immovable_object.aws71.webp`: AWS 71, 2184 × 1463 px. **Front-right, lower** three-quarter (camera about 25° above the floor, about 35–40° to the right). Fitted with **four** steel forks. Red plough with a rounded "D" top edge.
- `robots/immovable_object/reference/immovable_object.aws72.webp`: AWS 72, 1292 × 956 px. **Front-left, high** three-quarter (camera about 35° up, about 45° to the robot's left). Four forks. A **pinker red**, rougher plough, rounded "D" top, **chewed and torn at its left end** (fight damage), a **long countersunk screw backed out** of its top, and a **slide switch in a metal frame** on the lid.

The three photos show the same chassis and wheels with **three versions of the front plough**. The main description uses the **AWS 71 four-fork version** as the base, and notes the AWS 69 and AWS 72 differences. Everything stated as fact is read from the photos; inferences are marked **(guess)**. Dimensions are estimates scaled from the 150 g / 101.6 mm cube limit and the project kit draft (`kit.json`: body 85 × 64 × 26 mm, clearance 3, four wheels r 15 × 8 at y −28 and +20, four forks 38 mm long, 5 mm wide, spread 84). Ratios are given against **W = black body width ≈ 64 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the forks), **+Z** = up. mm.
- **Origin O** = the point on the floor under the centre of the black body's footprint.
- **Front** = the red plough with the forks.

| ID | Part |
|---|---|
| BD | black body box (tub) |
| TL | black top lid plate (textured top) |
| S-TL | 4 small black screws at the lid corners |
| PD-L, PD-R | side pods/motor housings between the wheels (black) |
| PL | red front plough/shield |
| PL-LIP | lower lip/skirt of the plough carrying the fork holes |
| PL-H | fork holes/notches in the lip |
| S-PL-F | 2 horizontal screws through the plough face (AWS 69 holes) |
| S-PL-T | vertical screws through the plough top-rear flange (one backed out in AWS 72; a black socket head in AWS 71) |
| FK-1…FK-4 | steel forks (bar + tip blade); FK-1 is the leftmost |
| FB | fork bars (square steel) |
| FT | fork tip blades (on-edge triangular steel blades) |
| RV | rivets/pins joining FT to FB (2 per fork) |
| WH-FL, WH-FR | front wheels (smaller) |
| WH-RL, WH-RR | rear wheels (larger) |
| HB | black six-spoke hub insert in each wheel |
| SW | slide power switch (on the lid, front-centre-right) |
| SWP | switch mounting plate (silver, 2 screws), AWS 72 |
| TP | black tape patch over the switch area (AWS 69) |
| M-x | drive gearmotors (hidden, guess) |
| BAT, ESC, RX | battery, ESC, receiver (hidden, guess) |

---

## 1. Overall description in one paragraph

Immovable Object is a **four-wheel pusher/fork-wedge** with a **black rectangular body** about 64 mm wide, 70 mm long and 26 mm tall, a **finely textured black top plate** with a small screw in each corner, and **four red wheels** with black six-spoked hubs mounted outboard, the **rear pair noticeably larger** (about Ø 36) than the **front pair** (about Ø 26). The whole front is covered by a **thick red printed plough**: a shield as wide as the body plus a little, standing **slightly taller than the body**, its front face **leaning back about 15–20°** and **gently convex in plan**, with a **rounded "D"/arched top edge** (AWS 71/72) or a flat top with chamfered shoulders (AWS 69). A thin **lip** along the bottom of the plough is pierced by **three or four holes** from which **steel forks** project about 35–40 mm forward. Each fork is a **square steel bar** angled slightly down, ending in a **flat triangular steel blade standing on edge**, pinned to the bar with two small rivets, whose sharp point rests on the floor. The robot has no active weapon: it gets the forks under the opponent and pushes.

---

## 2. Part-by-part description

### 2.1 Body box (BD)
- **Shape**: a rectangular box, about **64 mm wide (x ±32) × 70 mm long (y −38 to +32) × 23 mm tall** (z 3 to 26, the lid included). Corners are square with about 1 mm radii.
- **Colour/material**: **matt black FDM**, with horizontal layer lines on the walls.
- **Side walls**: in AWS 71 and AWS 69 the right wall shows **two levels**: an upper band (about 8 mm tall) directly under the lid, and below it, between the wheels, a **protruding block** (the side pod PD-R, section 2.3). The wall is plain elsewhere, with no visible screws.
- **Front**: hidden behind the plough. **Rear**: not photographed.
- **Ground clearance**: about **3 mm** (kit) under the body floor.

### 2.2 Top lid (TL)
- **Shape**: a flat plate about **64 × 70 × 2 mm**, flush with the walls, top at z ≈ 26. Its surface has a fine **woven/diamond texture** (the "textured PEI" print-bed finish), reading as a dull fabric-like grey-black in AWS 69/72.
- **Screws S-TL**: **4 small black Phillips pan heads**, head Ø ≈ 4 mm (M2), about **4 mm in from each corner**. Seen: rear-left (AWS 69 at (850, 112); AWS 72 at (515, 100)), rear-right (AWS 69 (1240, 295); AWS 71 (1110, 120)), front-right (AWS 71 (1690, 270); AWS 69 (830, 470) just behind the plough), front-left (AWS 72 (185, 245)).
- **Switch area**: at about **x +8, y +22** (just behind the plough, slightly right of centre):
  - AWS 72: a **black slide switch** (body about 12 × 6 mm, slider 3 × 3 mm) mounted under a **silver rectangular plate** about 16 × 7 mm with **two Phillips screws**, one each end; the plate has a rectangular cut-out for the slider.
  - AWS 69: a **black tape patch** about 18 × 16 mm covering the same area, with the switch slider and a silver edge peeking through.
  - AWS 71: hidden behind the plough's taller top; a silver glint and a black socket screw are visible just behind the plough's top-right.

### 2.3 Side pods (PD-L, PD-R)
- **Shape**: on each side, between the front and rear wheels, a **black box section** about **20 mm long (Y) × 10 mm tall (Z) × 4–6 mm proud** of the body side, at about z 5–15, y −15 to +5. Its top face is flat and its front and rear faces sit 1–2 mm from the wheel tyres. It is visible on the right in AWS 71 and AWS 69 and on the left in AWS 72.
- **Function (guess)**: houses the **gearmotor gearboxes** (motors lying along Y, with their output shafts poking out sideways at each end via a gear or the motor body itself), or is a printed **motor clamp/axle bearing block**. It also spaces the wheels away from the body.

### 2.4 Front plough (PL), base version AWS 71
- **Overall**: a **thick, solid-looking red printed shield**, about **70 mm wide (x ±35)** at the bottom, **32 mm tall** at the centre (z 0 to 32, i.e. **about 6 mm above the lid**), about **14–16 mm deep (Y)** at the bottom, with its rear face against the body front.
- **Front face**: leans back about **15–20° from vertical** (it is a steep wedge, not a ramp), and is **convex in plan**, a shallow arc of about **R ≈ 120 mm**, so the centre stands about 5 mm ahead of the ends. Fine horizontal print layer lines; light scuffs.
- **Top edge**: **rounded arch ("D")**: flat-ish in the middle and dropping in a large-radius curve (R ≈ 25 mm) at each shoulder to the vertical side faces. The top surface is a **narrow flat band about 6–8 mm deep**, sloping slightly back, with a **thin raised rim** at its front edge (a tiny overhang of the top layers).
- **Sides**: at each end the plough has a **side face** about **14 mm deep**, angled back about 30° (a chamfer between the front face and the body side) and about 22 mm tall. In AWS 71 the right side face shows a **vertical crease** where the chamfer meets a short flat face.
- **Bottom lip (PL-LIP)**: along the bottom of the front face, a **step**: the lowest **6–8 mm** of the plough projects about **2–3 mm further forward** than the face above, forming a lip. The fork holes are in this lip.
- **Fork holes (PL-H)**: four **round-topped holes/notches** (arch-shaped, about **6 mm wide × 6 mm tall**), evenly spaced, through the lip, at **x ≈ −30, −10, +10, +30**, centres at z ≈ 5. The bars exit from them.
- **Fasteners**:
  - AWS 71: a **black socket cap screw** (head Ø 5 mm) on the top-right just behind the arch top, and probably another on the left (hidden). These go **vertically** through a rear flange of the plough into the body (or into the body's front wall bosses) **(guess)**.
  - AWS 72: a **long silver countersunk Phillips screw** (head Ø 6–7 mm, M3 × ~25 or a 3.5 mm wood screw) has **backed out about 12–15 mm** above the plough's top-rear at about x −5; its threads are visible. Evidence that the plough is held by **vertical self-tapping screws from the top** into the body, and that fight impacts work them loose.
  - AWS 69: **two small round holes** (Ø ≈ 3.5 mm, counterbored) in the plough face, one above the other at the centre (x ≈ 0, z ≈ 20 and z ≈ 13): **horizontal screws** into the body front wall **(guess)**.

### 2.5 Plough variants
- **AWS 69**: orange-red PLA. The top is **flat in the middle with two 45° chamfered shoulders** and short vertical sides (a polygonal arch). A **horizontal ridge/step** runs across the face at about z ≈ 16, dividing it into an upper band set back by about 2 mm and a lower band. The plough top is at about the **same height as the lid** (z ≈ 27). The bottom lip is curved in plan (convex arc) and carries **3 forks** at about **x ≈ −28, −4, +20** (unevenly spaced; possibly evenly spaced at −26, 0, +26 with perspective error). Upper edge has a fine raised rim (top layers). Two face screw holes.
- **AWS 71**: red, rounded D top, 4 forks evenly spaced, one black socket screw on top. The cleanest version.
- **AWS 72**: **pink-red** (a different, pinker filament), coarser layer lines, rounded D top that rises well above the lid (about 8 mm), **badly chewed at its left end** (a ragged bite about 15 mm wide × 20 mm tall missing from the left shoulder/side face, with stringy torn plastic: the mark of a spinner hit). Four forks. One long countersunk screw backed out of the top.

### 2.6 Forks (FK-1…FK-4): bars (FB), tip blades (FT), rivets (RV)
- **Bar FB**: a **square steel bar about 3 × 3 mm** (dark, slightly oily grey), leaving the plough hole at z ≈ 5 and running **forward and slightly down** (about 5–8° below horizontal), about **18–20 mm** visible beyond the lip.
- **Tip blade FT**: a **flat steel blade standing on edge** (plane vertical, parallel to YZ), about **2 mm thick**, fixed to the **outer side face of the bar's end** with **two small rivets/pins** (dots about 1 mm, seen on the blade face). Side profile: a **long right triangle** about **22–24 mm long × 6–7 mm tall at its rear**: the **rear edge is vertical** (a step/shoulder, which also acts as a barb), the **bottom edge is flat on the floor**, and the **top edge slopes from the rear-top corner down to the point** at the floor. The point is sharp. The blade's faces are **bright, ground steel**, lighter than the bar; one blade in AWS 71 shows faint stamped text, suggesting it was cut from a **commercial blade (planer knife, scraper blade or hacksaw)** **(guess)**.
- **Overall fork length** from the plough lip to the tip: about **38–40 mm** (kit 38). Tips at about **y ≈ +86**? This conflicts with the cube (see section 12; reconciled tip at y +62 with a shorter body).
- **Spacing**: tips parallel, at the same x as their holes (x −30, −10, +10, +30 for four; three in AWS 69).
- **Bottom**: blade bottoms flat on the floor, so the **forks are the robot's lowest front contact**.

### 2.7 Wheels (WH-FL, WH-FR, WH-RL, WH-RR)
- **Shape**: solid **red discs** with a **black six-spoke hub insert (HB)** on the outer face: six radial arms (each about 3–4 mm wide, widening at the ends into rounded "petals"), meeting at a central hub (Ø ≈ 6 mm) with the axle/shaft, set flush with the red face, so the face reads as a **red disc with a black six-armed flower/star**. In AWS 69/71/72 the black of the spokes is smudged into the red, suggesting a **two-material print** (black PLA hub + red TPU tyre) or a **red TPU tyre cast/printed around a black hub**. The tread is **smooth or finely knurled** red TPU with a grainy, worn look (scuffed white on the edges).
- **Sizes**:
  - **Rear wheels**: about **Ø 36 mm × 9 mm wide**.
  - **Front wheels**: about **Ø 26 mm × 8 mm wide**.
  - The size difference is seen in all three photos, including AWS 72 where the rear wheel is **nearer** the camera yet still clearly larger than the front, and AWS 69/71 where the rear wheel is **farther** away and still larger. So it is real, not perspective.
- **Positions (centres)**: rear wheels at **(±37, −24, 18)**, front wheels at **(±37, +18, 13)**, i.e. the front axle about **5 mm lower** than the rear so all four tyres touch the floor and the body stays level **(guess; the alternative is a nose-down body with the forks taking the load)**. Wheel inner faces about 1 mm from the side pods' ends, outer faces at x ≈ ±41.5.
- **Heights**: the rear wheel top at z ≈ 36, about **10 mm above the lid**; the front wheel top at z ≈ 26, level with the lid and hidden behind the plough shoulders from the front. When inverted, the robot rides on the **rear wheels and the plough top/lid**, not on the front wheels (section 6).
- **No wheel guards**: all four outer faces are exposed.

### 2.8 Drive motors (hidden, guess)
- Probably **two or four N20-class gearmotors**. The side pods between the wheels suggest each side has either one motor driving both wheels through a gear or chain hidden in the pod, or **two motors back-to-back along Y** in the pod/body, one per wheel. Given the **different wheel sizes** (which only make sense if the wheels are driven independently or geared), the most likely is **four motors**, each with its own shaft (medium).

---

## 3. Per-view sections

### 3.1 AWS 71 (front-right, low)
- The red plough fills the left two thirds, its D-shaped top above the body; four forks fan out to the lower-left. The black lid with corner screws is at the top-right; the right side shows the small front wheel, the pod and the large rear wheel; the rear-left wheel's top shows behind the lid at the top-left.

### 3.2 AWS 69 (front-right, high)
- The orange plough with the flat top and shoulders, a horizontal ridge and two face holes; three forks at the lower-left; the lid with its taped switch; the right side with small front and large rear wheels; the left wheels' tops show at the rear-left and front-left (a small red arc peeks out behind the plough's left shoulder: the front-left wheel).

### 3.3 AWS 72 (front-left, high)
- The pink plough on the right of the image with its chewed left end and the backed-out screw on top; four forks pointing to the lower-right; the switch with its silver plate on the lid behind the plough; the left side with the small front wheel and large rear wheel; the right wheels' tops behind.

### 3.4 Top view (plan, synthesised)
- A 64 × 70 mm black rectangle with four corner screws and the switch at the front-centre-right; the 70 mm wide red plough across the front, convex in plan, about 15 mm deep; forks as thin lines 3 mm wide reaching about 38 mm ahead of the plough lip; four wheels outboard: rear ones Ø 36 (long rectangles 36 × 9 in plan), front ones Ø 26 (26 × 8).

### 3.5 Front view
- The red plough as a 70 mm wide, 32 mm tall arched shield, with four holes along its bottom lip and four fork blades in front of them; the large rear wheels show beyond the plough at both sides above shoulder height (their top 4 mm above the plough top at the sides); the small front wheels are hidden behind the plough sides.

### 3.6 Right side view
- From the rear: the large rear wheel (Ø 36), the black body (23 mm tall) with the pod between the wheels, the small front wheel (Ø 26), the red plough's side (14 mm deep, 32 mm tall, the front leaning back 15–20°), and the fork bar + triangular blade reaching out to the floor point.

### 3.7 Rear view and underside (not photographed; inferred)
- Rear: a plain black wall between the two large wheels. Underside: a flat floor at z 3, four tyre contacts, the fork blade bottoms on the floor.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | box | 64 × 70 × 21 | 1 × 1.09 × 0.33 | black FDM | — | 1 |
| TL | textured plate | 64 × 70 × 2 | 1 × 1.09 | black FDM (textured bed side up) | 4 × M2 pan | 1 |
| PD | side pod | 20 × 5 × 10 | 0.31 × 0.08 × 0.16 | black | integral (guess) | 2 |
| PL | arched convex shield | 70 × 15 × 32 | 1.09 × 0.23 × 0.5 | red / orange / pink FDM | vertical top screws (+2 face screws AWS 69) | 1 |
| PL-H | arched holes | 6 × 6 | 0.09 | — | — | 3–4 |
| FB | square bar | 3 × 3 × ≈ 35 (incl. inside the plough) | 0.05 | steel | pressed in the plough | 3–4 |
| FT | on-edge triangle blade | 23 × 6.5 × 2 | 0.36 × 0.10 | ground steel | 2 rivets | 3–4 |
| WH-R | disc wheel | Ø 36 × 9 | 0.56 × 0.14 | red TPU + black hub | shaft | 2 |
| WH-F | disc wheel | Ø 26 × 8 | 0.41 × 0.13 | red TPU + black hub | shaft | 2 |
| SW | slide switch | 12 × 6 × 6 | 0.19 | black + silver plate | 2 screws / tape | 1 |
| S-PL-T | countersunk/socket | M3 × 25 | — | steel | into the body | 2 (guess) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| TL ↔ BD walls | rests on, screwed | 0 |
| PL rear face ↔ BD front wall | bolted | 0 |
| PL bottom ↔ floor | above | 1–2 |
| PL top ↔ TL top | plough above the lid | +6 (AWS 71), +8 (AWS 72), ≈ 0 (AWS 69) |
| PL sides ↔ front wheels (inner face) | near | 2–3 |
| FB ↔ PL-H | pressed/glued in | 0 |
| FT ↔ FB | riveted | 0 |
| FT bottom ↔ floor | touching | 0 |
| FT rear edge ↔ PL lip | ahead | 16–18 |
| FT ↔ adjacent FT | side by side | 18 (4 forks) |
| WH-F inner face ↔ BD/PD | near | 1–2 |
| WH-F tyre ↔ PD front face | near | 1–2 |
| WH-R tyre ↔ PD rear face | near | 1–2 |
| WH-R top ↔ TL | wheel above | +10 |
| WH-F top ↔ TL | about level | 0 |
| All tyres ↔ floor | touching | 0 (front axle lower, guess) |
| BD floor ↔ floor | above | 3 |
| SW ↔ TL | screwed / taped | 0 |

---

## 6. Mechanism
1. **Drive**: four-wheel skid steer. The large rear wheels carry the weight and the pushing torque; the small front wheels sit tucked behind the plough.
2. **Forks + plough**: the forks get under; the steep plough then acts as a **wall** that pushes the opponent rather than a ramp that lifts it. The robot "is immovable": weight forward on the forks, a solid front, and big rear wheels for traction.
3. **Inverted**: the rear wheels (top at z 36) stand 10 mm above the lid and 4 mm above the plough top, so inverted it can still drive on the rear wheels while sliding on the plough top; the forks are then useless (pointing up), and the front wheels do not touch. So inverted driving is possible but clumsy **(design observation)**.

---

## 7. Assembly order (suggested rebuild)
1. Print BD (with motor cradles and side pods), TL (textured side up), PL (with fork holes and screw bosses/flange), the wheels (black hubs + red TPU tyres).
2. Fit the motors into the pods/body; press on the wheels (large at the rear, small at the front).
3. Fit the battery, ESC, receiver, switch; route the wires.
4. Screw on the lid (4 × M2); fix the switch (plate and screws, or tape).
5. Rivet the tip blades onto the square bars; press/glue the bars into the plough holes.
6. Fix the plough to the body front with vertical screws from the top (and two horizontal face screws on the AWS 69 version).

---

## 8. Coordinate frame (restated)
- Origin O on the floor under the centre of BD. +X right, +Y forward, +Z up. mm.
- BD x ∈ [−32, 32], y ∈ [−38, +32], z ∈ [3, 26]. PL x ∈ [−35, +35], y ∈ [+32, +47], z ∈ [1, 32]. Wheels: rear (±37, −24, 18) Ø 36; front (±37, +18, 13) Ø 26.

## 9. Profiles as math

**9.1 Plough front face (in plan, XY plane at the bottom of the upper face, z = 8).**
- Arc of radius R = 120 centred at (0, 47 − 120) = (0, −73): y(x) = −73 + √(120² − x²), x ∈ [−30, +30] (y = 47 at x = 0, 43.2 at x = ±30). Then 30° chamfers from (±30, 43.2) back to (±35, 34).
- Lip: the same arc offset +2.5 mm in y for z ∈ [1, 8].
- Face lean: at height z the face is set back by (z − 8)·tan 18°, i.e. y(x, z) = y(x) − 0.325·(z − 8).

**9.2 Plough front elevation (XZ plane).**
- AWS 71/72 "D" arch: top z(x) = 32 for |x| ≤ 10; for 10 < |x| ≤ 35, z(x) = 7 + 25·√(1 − ((|x| − 10)/25)²) (a quarter-ellipse falling from 32 to 7 at the ends). Sides vertical from z 7 to 1.
- AWS 69 polygon: top z = 27 for |x| ≤ 22; 45° chamfers to (±35, 14); vertical to z 1. Horizontal ridge at z 16.
- Fork holes: arches of width 6, sides vertical from z 2 to 5, semicircle r 3 on top, centres at x ∈ {−30, −10, +10, +30}.

**9.3 Fork (YZ plane at the fork's x).**
- Bar centre line from (y 47, z 5) to (y 65, z 3): slope −6.3°. Square 3 × 3.
- Blade outline: rear edge vertical at y = 62 from z 0 to z 6.5; top edge from (62, 6.5) to tip (85, 0): z = 6.5 − 0.283·(y − 62); bottom edge z = 0 from y 62 to 85. Thickness 2, on the bar's outer side. Rivets r 0.6 at (65, 3.5) and (69, 3).
- (Use the reconciled tip y = +62 from section 12 by shifting everything forward of the plough by −23 mm if building inside the cube.)

**9.4 Wheels.**
- Rear: disc r = 18, width 9. Front: r = 13, width 8.
- Hub star on the outer face: six arms at φ_k = 60°k; each arm: width w(r) = 3 + 0.25·r (widening outward), from r = 3 to r = 0.8·R; rounded petal ends of radius w/2.

## 10. Pixel-based measurements (independent check)
Native coordinates (x, y) from the top-left, ±10 px.
- **AWS 71** (2184 × 1463): plough bottom-left corner (360, 760); bottom-right (1240, 1135); top centre of the arch (870, 220). Fork holes: (425, 750), (690, 845), (960, 960), (1220, 1110). Fork tips: (40, 990), (270, 1100), (555, 1235), (810, 1355). Rear-right wheel x 1880–2140, y 270–790 (≈ 520 px tall); front-right wheel x 1590–1840, y 590–1010 (≈ 420 px tall). Lid front-right screw (1845, 295); rear-right (1210, 130).
- **AWS 69** (1419 × 1132): plough bottom from (230, 590) to (985, 960); top band at y ≈ 290–330; face holes (605, 515) and (585, 600). Rear-right wheel x 1150–1395, y 300–610 (≈ 310 px); front-right wheel x 985–1165, y 540–765 (≈ 225 px). Fork tips (85, 735), (290, 860), (520, 1030).
- **AWS 72** (1292 × 956): plough from (470, 300) to (1180, 700); bitten left end (540–590, 520–620). Rear-left wheel x 40–260, y 250–545 (≈ 295 px); front-left wheel x 290–450, y 445–665 (≈ 220 px). Backed-out screw: head (780, 185), shank to (775, 270). Switch plate (540–700, 300–345).

## 11. Several independent estimates of key quantities

| Quantity | Method A (kit / rules) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | kit 64 | plough ≈ 1.1 × body | AWS 69 plough bottom ≈ 830 px; plough 70 → 11.9 px/mm; lid width ≈ 760 px → 64 | **64** |
| Body height (to lid top) | kit 26 | ≈ 0.4 × width → 26 | AWS 71 body right side ≈ 250 px at ≈ 10 px/mm (near the front wheel) → 25 | **26** |
| Rear wheel Ø | kit r 15 → 30 | rear / front ≈ 1.38 (AWS 69: 310 / 225; AWS 71: 520 / 420 = 1.24 but rear is farther; AWS 72: 295 / 220 = 1.34 with rear nearer) → mean 1.32 | AWS 69: 310 px / 9.5 px/mm (rear depth) ≈ 33; AWS 71: 520 / 14 ≈ 37 | **36** |
| Front wheel Ø | kit 30 | 36 / 1.35 = 26.7 | AWS 69: 225 / 9.5 (nearer → use 10.5) ≈ 21–24; AWS 71: 420 / 16 ≈ 26 | **26** |
| Plough height | — | ≈ 1.2 × body | AWS 71: arch top (870, 220) to bottom (870, 870) = 650 px at ≈ 20 px/mm (near) → 32 | **32 (AWS 71)** |
| Fork length beyond the lip | kit 38 | ≈ 0.55 × plough width | AWS 71: hole (425, 750) to tip (40, 990) = 454 px at ≈ 13 px/mm (perspective, near) → 35; AWS 69: hole (315, 575) to tip (85, 735) = 280 px at 11.9 → 23.5 (foreshortened, the fork points toward the camera) | **38** |
| Fork spacing (4) | kit spread 84 (tip-to-tip span?) | 3 gaps across ≈ 60 → 20 | AWS 71 holes ≈ 280 px apart at ≈ 14 px/mm → 20 | **20** |
| Blade length | — | ≈ 0.6 × fork length | AWS 71 blade ≈ 300 px / 13 → 23 | **23** |

## 12. Consistency check: conflicts and reconciliation
1. **Overall length vs the cube**: rear wheel rear edge (−24 − 18 = −42) to fork tips (+85) = 127 mm, far beyond 101.6. The kit's 85 mm body + 38 mm forks has the same problem. The AWS 101.6 mm rule applies to the robot's starting configuration; forks cannot fold here. So **lengths must shrink**: body length 60 (y −30 to +30), plough to y +42 (12 deep), forks 30 beyond the lip to y +72, rear wheel centre at −14 (rear edge −32): **total 104** — still slightly over. Final: body 58 (−29 to +29), plough to +40, forks to +68, rear wheel centre −12 with r 18 → rear edge −30: **total 98 mm**. Use these numbers for a cube-legal build; the photo ratios (fork length ≈ 0.55 × plough width) are kept.
2. **Rear vs front wheel size**: kit used equal r 15. All three photos show the rear larger from both near and far viewpoints. **Reconciled: rear Ø 36, front Ø 26.**
3. **Front wheel contact**: with axles at the same height the front wheels would hang 5 mm above the floor. The photos don't show the floor line under the front wheels clearly. A builder trying to be "immovable" would want all four on the floor, so **front axle 5 mm lower** (centre z 13 vs 18). Medium confidence.
4. **Plough height variants**: AWS 69 ≈ lid height, AWS 71 +6, AWS 72 +8. These are three different prints. Not a conflict.
5. **Fork count**: 3 (AWS 69) vs 4 (AWS 71/72). Different events. Not a conflict.
6. **Width**: rear wheels at x ±37 with 9 mm width → outer at ±41.5 → overall 83 mm; plough 70; fits.

---

## 13. Why the designer did it (per part, mostly adversarial)

- **Forks with on-edge steel blades (FT, FB)**
  - Getting under vs contact: on-edge triangular blades have a **sharp, hard point at floor level** and present only 2 mm of width, so they slip under an opponent's wedge edge or chassis lip more easily than a full-width plate (fork beats wedge in most first contacts). The flat blade bottom keeps them riding level on the floor instead of digging in. Several forks spread across the width make sure at least one finds a gap under the opponent.
  - The **vertical rear edge** of each blade acts as a **barb/stop**: once an opponent's edge passes over the slope it drops behind the step and is hooked, so it cannot simply slide off the forks while being pushed.
  - Against spinners: thin forks offer little for a horizontal spinner to hit; when hit, a fork bends rather than passing the full impact into the body. Square steel bars resist bending in both directions better than a flat strip. The bars are separate from the tips so a damaged tip can be replaced by drilling out two rivets.
  - Construction: cut from cheap steel blade stock; riveting avoids heat (welding would soften hardened steel).

- **Steep, convex, thick red plough (PL)**
  - Fight: once the forks are under, the **steep face** acts as a pushing wall that holds the opponent against the forks instead of letting it ride up and over the robot. The **convex plan** shape centres an opponent on the plough and **deflects glancing hits** from horizontal spinners outward instead of letting them bite square. Thick printed plastic is **sacrificial armour**: AWS 72 shows it took a big bite at the left end and the robot survived. Standing taller than the lid, it protects the lid edge and the switch from front attacks and stops opponents climbing onto the lid.
  - Against vertical spinners: the rounded/chamfered top edge gives a tooth little square edge to catch.
  - Weak points: the top screws back out under impacts (AWS 72); the plough is the heaviest single printed part.
  - Construction: printed as one block; easy to reprint in a new colour or shape per event (three versions seen); fork holes moulded in.

- **Black box body and textured lid**
  - Fight: low and compact, so most of the robot sits behind the plough and between the wheels; the lid is not a primary target.
  - Construction: the lid printed face-down on a textured bed gives a tough, nice surface with no top-layer weakness; four corner screws give quick access.

- **Side pods (PD)**
  - Fight: they fill the gap between the wheels, so an opponent's fork or wedge cannot get in between the tyres and the body; they also shield the motors from side hits.
  - Construction: house the gearboxes outboard to leave the middle of the body free for electronics (guess).

- **Large rear wheels, small front wheels**
  - Fight: big rear wheels give **traction and pushing power** where the weight is (the plough and forks put weight forward, but the battery is likely at the rear) and keep the robot drivable inverted. Small front wheels **tuck behind the plough's shoulders**, so a frontal attacker cannot hit them; they also keep the nose low so the forks are loaded onto the floor.
  - Weak points: no wheel guards, so side spinners can hit the exposed red tyres; the large rear wheels are the most exposed parts.
  - Construction: TPU tyres for grip on the arena floor; black hub stars for stiffness and grip on the motor shaft.

- **Switch at the front-centre of the lid behind the plough**
  - Fight: shielded from frontal attacks by the plough (taller than the lid); covered by tape (AWS 69) or a metal plate (AWS 72) so it cannot be knocked off during a fight.
  - Construction: reachable from the top without removing anything.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors (or 2 with geared pairs) | 12 × 10 × 25 | in or behind the pods along Y; shafts at (±32, −24, 18) and (±32, +18, 13) | medium |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 10 | rear-centre, (0, −20, 10) | medium |
| ESC | dual brushed ESC / combined receiver-ESC board | 30 × 20 × 6 | front-centre under the lid, (−5, +10, 10) | medium |
| Switch | slide switch | 12 × 6 × 6 | (+8, +22, 23) | high (seen) |
| Plough fixings | 2 vertical M3 or 3.5 mm screws into front corner bosses; 2 horizontal M3 in AWS 69 | — | (±20, +30, 26) | medium |
| Fork bar sockets | blind holes 20 mm deep in the plough lip; bars glued | 3.2 × 3.2 × 20 | behind each hole | medium |
| Wires | battery → switch → ESC → motors, low along the walls | — | — | medium |

## 15. What the photos cannot show (uncertain list)
- The rear wall, underside and inner layout.
- Whether the front axle is lower or the body sits nose-down.
- The motor count and the pod internals.
- Exact plough fixing scheme.
- All mm values are scaled estimates (±10–15%); overall length must be shrunk to fit the cube (section 12).

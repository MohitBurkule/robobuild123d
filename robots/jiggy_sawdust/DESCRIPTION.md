# Jiggy Sawdust: full rebuild description from reference photos

Source photos (all **low-resolution and not cut out**):
- `robots/jiggy_sawdust/reference/jiggy_sawdust.aws62.webp`: AWS 62, 615 × 550 px, on a light wooden table, **front-left, about 30–35° above the floor**, close. The **best photo**. This version shows **no saw blades fitted**; it shows the clear box, the front V nose, both front side plates, both wheels, the top beam with a short **steel chain**, and the wiring inside.
- `robots/jiggy_sawdust/reference/jiggy_sawdust.aws63.webp`: AWS 63, 344 × 295 px, on a grey carpet/table, **front-right, about 25° up**, blurry. Shows the robot **with two black toothed jigsaw blades** fitted, running fore-aft along the top-left and the right side. Another robot's wheel is in the foreground (background object, not part of Jiggy Sawdust).
- `robots/jiggy_sawdust/reference/jiggy_sawdust.aws60.webp`: AWS 60, 150 × 130 px, a tiny pit-table shot, front-left, with other robots around it. It only confirms the general layout and **two dark blades** sticking out of the top of the box.

**The photos show little fine detail**: they are small, blurry and the robot is made of **clear polycarbonate**, so edges are faint. This description is therefore shorter than the 4000-word target and gives wider error bars (±20%). Facts are read from the photos; inferences are marked **(guess)**. Dimensions are scaled from the 150 g / 101.6 mm cube limit and the project kit draft (`kit.json`: "other" type, body 70 × 70 × 55, two wheels r 14 × 8 at y −18, a front plate 80 wide at 35°, a 2 × 80 × 9 saw blade at z 38 with a pivot, and a saw body block 14 × 30 × 16). Ratios are against **W = box width ≈ 70 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the aluminium V nose), **+Z** = up. mm.
- **Origin O** = the floor point under the centre of the clear box footprint.

| ID | Part |
|---|---|
| BX | clear polycarbonate box (side walls, front wall, rear wall, floor) |
| SW-L, SW-R | clear side walls (with rounded top corners) |
| FN | clear tall fin/tab at the rear-right top (AWS 62) |
| TB | top cross-beam (clear bar across the front top) |
| CH | short steel chain on the top-left of TB (AWS 62) |
| NV | aluminium V nose (centre, folded triangular plate) |
| FS-R | aluminium front-right side plate (wedge) |
| FS-L | clear polycarbonate front-left side plate (wedge) |
| S-NV, S-FS | black screws on the nose and side plates |
| BL-L, BL-R | black toothed jigsaw blades (AWS 60/63) |
| SM | saw mechanism (crank/slider, hidden, guess) |
| WH-L, WH-R | two black treaded wheels |
| PCB | green circuit board (receiver/ESC) |
| RP | red component at the top-left inside (motor can or capacitor, guess) |
| WR | wires (red, orange/yellow, black, brown) |
| SWT | black switch on the top-right (AWS 62, guess) |
| M-x | drive motors (hidden) |
| BAT | battery (hidden, guess) |

---

## 1. Overall description in one paragraph

Jiggy Sawdust is a **tall, see-through box robot with a jigsaw weapon**. Its body is a **clear polycarbonate box** about 70 mm wide, 65 mm long and 50–55 mm tall, built from flat clear plates screwed together, with **rounded top corners on the side walls** and a **clear cross-beam** across the front top. You can see straight in: **red, orange and yellow wires**, a **green circuit board**, a **red component** and other electronics fill it. Two **black treaded rubber wheels** (about Ø 30 mm) sit outside the side walls toward the rear. The front is a **pointed plough**: a **folded aluminium V nose** in the middle (two triangular faces meeting at a ridge, its point on the floor) flanked by two **sloped side plates**, **aluminium on the right** and **clear polycarbonate on the left**, all held with black screws, with the team's name scratched into the plates. In the later version (AWS 63) two **black toothed jigsaw blades** run **fore-aft** along the top-left and the right side of the box, sticking out ahead of the front: the weapon is a **reciprocating saw** ("jig" = jigsaw) driven by a mechanism inside the box **(mechanism guessed)**.

---

## 2. Part-by-part description

### 2.1 Clear box (BX)
- **Shape**: a box of flat **clear polycarbonate sheets**, about **2 mm thick**, about **70 mm wide (x ±35) × 65 mm long (y −35 to +30) × 50 mm tall** (z 3 to 53). The sheets are joined at the corners, probably with **small screws into printed or aluminium corner angles** or with tabs **(guess)**; small silver/black screw heads are visible along the vertical edges in AWS 62 (left front edge at native (125, 140) and (130, 205)).
- **Side walls (SW-L, SW-R)**: clear rectangles about **65 × 50 mm**, with the **top-front and top-rear corners rounded** (radius about 10 mm) — seen clearly on the left wall in AWS 63 and the right wall in AWS 62. The right wall in AWS 62 also has a **tall clear tab/fin FN** rising about **15 mm** above the rest at its rear-top corner (native (370–410, 10–55)); its purpose is unclear: a **handle**, an **antenna mount** or a **blade guide** **(guess)**.
- **Front wall**: clear, behind the nose plates; the lower part is covered by the plough plates.
- **Rear wall / floor**: not visible; assumed clear sheet **(guess)**.
- **Scratched text**: "100%" is scratched into the left front clear plate (AWS 62).

### 2.2 Top beam (TB) and chain (CH)
- **TB**: a **clear bar** about **70 mm long × 8 mm tall × 6 mm deep** across the **front top** of the box at z ≈ 45–53, joining the side walls, with **metal fittings** (silver screws/brackets) at both ends.
- **CH**: a short **steel chain** (about 6–8 links, each about 4 mm long) hangs from a **metal fitting at the top-left** of TB in AWS 62 (native (175–235, 70–105)). Possibly part of the **saw drive** (a link from the crank) or a **lanyard for the arming link** **(guess, low)**.
- **SWT**: a **black rectangular component** about 12 × 4 mm on the top at the rear-right (AWS 62, native (290–370, 80–95)): probably the **power switch** or a removable link **(guess)**.

### 2.3 Front V nose (NV)
- **Shape**: an **aluminium sheet (≈ 1.5 mm) folded along a centre line** into a **V**, forming a **pointed wedge nose**: two triangular faces meet at a **sloping ridge** that runs from the **point on the floor** (front) **up and back** to the top edge at about mid-height of the box. In plan the V's apex angle is about **90°**; the slope of the ridge is about **35–40°** from the floor.
- **Size**: about **30 mm wide** at its top edge (x ±15), **35 mm long** along the ridge, top edge at z ≈ 20 and y ≈ +30, point at about **(0, +55, 0)**.
- **Screws S-NV**: **six black pan screws** (head Ø ≈ 3.5 mm): two at the top corners and four in two rows of two on the faces (AWS 62 native (300, 380), (355, 375), (300, 420), (340, 415), (295, 470), (335, 455), approximately). They fix the nose to a **bracket behind it** or to the front wall **(guess)**.

### 2.4 Front side plates (FS-R, FS-L)
- **FS-R**: an **aluminium plate**, about **32 mm wide × 28 mm long**, **sloped about 35°** like a wedge, on the **right** of the nose, its lower edge on/near the floor and set back about 10 mm from the nose point; its outer front corner is **cut at 45°**. **Two black screws** (native (410, 380), (465, 365) in AWS 62). Scratched text, roughly "Sawdust … ALL LAMI…", on its face.
- **FS-L**: the same shape in **clear polycarbonate** on the **left** (AWS 62 native (105–250, 270–460)), standing more steeply (about 60°) in AWS 62 and hanging slightly forward; in AWS 63 it is the clear plate at the lower-left.
- Together NV, FS-L and FS-R give the front a **three-faceted arrowhead** plan: the nose point in the middle, and the side plates sloping back to the box corners.

### 2.5 Wheels (WH-L, WH-R)
- **Shape**: **black rubber tyres with block tread** (RC-car type), about **Ø 30 mm × 12 mm**, on black hubs.
- **Position**: outside the side walls, centres about **(±42, −15, 15)**: AWS 62 left wheel native (75–120, 270–390), right wheel (455–500, 200–310); AWS 63 right wheel (530–630, 310–450).
- **Height**: tyre tops at z ≈ 30, about halfway up the box; the robot **cannot drive inverted** (the box is 50 mm tall).
- **No guards**.

### 2.6 Jigsaw blades (BL-L, BL-R), AWS 60/63 only
- **Shape**: standard **black jigsaw blades** (T-shank), about **7 mm deep × 1.2 mm thick**, toothed along one edge (teeth pointing down/outward, pitch about 2.5 mm = 10 TPI wood blades), visible length about **50–60 mm**.
- **Position (AWS 63)**: **BL-L** runs **fore-aft along the top-left edge** of the box at z ≈ 45, from inside the box near the top beam forward and slightly down, its tip about **25–35 mm ahead** of the front top edge (native from (210, 130) to (40, 215)). **BL-R** runs parallel to it along the **right side** at mid-height (z ≈ 30), from inside the box forward to about the front face (native (500, 210) to (350, 280)), teeth down.
- **AWS 60**: two dark blades similarly placed, one at each side, angled down toward the front.
- **Mechanism (guess)**: a **gearmotor with a crank** (eccentric pin) inside the box drives a **slider** to which both blades are clamped (or two slides, 180° out of phase), so the blades **reciprocate fore-aft** with a stroke of about **15–20 mm**, sawing at whatever sits in front/on top of the nose. The chain in AWS 62 may be a connecting rod substitute or unrelated.
- **Alternative reading (low)**: the blades run along X and stick out sideways; rejected because both blades in AWS 63 are parallel to the box's side-wall edges (the Y direction in that view).

### 2.7 Electronics and wires (seen through the box)
- **Green PCB** (about 25 × 15 mm) standing vertically at the right-centre (AWS 62 native (345–400, 190–260); AWS 63 (450–500, 250–300)): likely a **receiver/ESC** or a **brushed ESC** board.
- **Red component** (about 12 × 10 mm) at the top-left inside (AWS 62 (130–160, 140–175)): possibly a **motor can**, a **capacitor** or a red **XT/JST plug** **(guess)**.
- **Wires**: **red** (several, about 1 mm), **orange/yellow** and **brown** (servo-type three-core) looping across the inside and over the top; one **yellow/orange** loop at the top-left corner exits and re-enters the box (AWS 62 (95–115, 120–160)). A **black wire bundle** runs down the middle.
- **Battery**: not identifiable; perhaps the dark object at the bottom-centre behind the nose **(guess)**.

---

## 3. Per-view sections

### 3.1 AWS 62 (front-left, no blades)
- A clear cube on a wooden table: wires and boards visible through it; a clear beam on top with a chain; the aluminium V nose at the bottom-centre pointing at the camera, the aluminium right plate and the clear left plate; black wheels at both sides.

### 3.2 AWS 63 (front-right, blades fitted)
- The clear box with two black blades running diagonally (fore-aft in the robot), the left one sticking out ahead at the top-left; the nose and right plate at the bottom; the right wheel at the right.

### 3.3 Top view (plan, synthesised)
- A 70 × 65 rectangle (clear), the wheels (30 × 12) outside its rear half, the arrowhead front (nose point at y +55, side plates to the box corners), two blade lines along x ≈ −33 and x ≈ +30 reaching to y ≈ +60 (left) and +35 (right).

### 3.4 Front view
- A tall clear rectangle (70 × 50) above a low aluminium/clear plough (20 mm tall); the wheels at both sides; the blades end-on as thin dark vertical slivers at the top-left and the right.

### 3.5 Side view (right)
- A clear rectangle 65 × 50 with rounded top corners, a tall tab at the rear-top, the wheel (Ø 30) at the rear half, the sloped plough at the front reaching the floor about 25 mm ahead of the box, and the blade along the side.

### 3.6 Rear and underside (not photographed)
- Assumed plain clear sheets; flat floor.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BX | sheet box | 70 × 65 × 50, sheet 2 | 1 × 0.93 × 0.71 | clear PC | screws/angles (guess) | 1 |
| FN | tab | 12 × 15 × 2 | — | clear PC | part of SW-R | 1 |
| TB | bar | 70 × 6 × 8 | 1 | clear PC | screws at the ends | 1 |
| CH | chain | 6–8 links × 4 | — | steel | on a fitting | 1 |
| NV | folded V plate | 30 wide × 35 ridge, 1.5 thick | 0.43 | aluminium | 6 black screws | 1 |
| FS-R | sloped plate | 32 × 28 × 1.5 | 0.46 | aluminium | 2 screws | 1 |
| FS-L | sloped plate | 32 × 28 × 1.5 | 0.46 | clear PC | 2 screws (guess) | 1 |
| BL | jigsaw blade | ≈ 75 × 7 × 1.2 | 1.07 | black steel | clamped to a slider | 2 (AWS 63) |
| WH | treaded tyre | Ø 30 × 12 | 0.43 × 0.17 | black rubber | motor shaft | 2 |
| PCB | board | 25 × 15 | — | green | in the box | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| BX sheets ↔ each other | screwed/joined | 0 |
| TB ↔ SW-L/R | screwed | 0 |
| NV ↔ BX front | screwed (via bracket) | 0 |
| NV point ↔ floor | touching | 0 |
| FS-R/L lower edge ↔ floor | near | 0–2 |
| FS ↔ NV | side by side | 1–3 |
| WH inner face ↔ SW | near | 2 |
| WH ↔ floor | touching | 0 |
| BX floor ↔ floor | above | 3 |
| BL ↔ slider (inside) | clamped (guess) | 0 |
| BL-L ↔ SW-L top edge | running along, clearance | 1–2 |
| BL tips ↔ NV ridge | above | ≥ 20 |

---

## 6. Mechanism
1. **Drive**: two wheels, skid steer, with the plough edges taking the front weight.
2. **Weapon (guess)**: a jigsaw-style **reciprocating blade pair** driven by a crank inside the box; the blades saw at an opponent pushed against the nose or sitting on it.
3. **Plough**: the V nose splits/deflects opponents to the side plates, and the plates lift their edges.

---

## 7. Assembly order (suggested rebuild)
1. Cut the clear sheets (sides with rounded tops and the right tab, front, rear, floor, top beam).
2. Fit the drive motors and wheels to the side walls; fit the saw motor, crank and slider inside.
3. Fit the electronics (board, battery, switch) and wire up.
4. Close the box (screws/angles).
5. Fold and drill the aluminium V nose; screw it and the two side plates to the front.
6. Clamp the jigsaw blades into the slider.

---

## 8. Coordinate frame (restated)
- Origin O on the floor under the box centre; +X right, +Y forward, +Z up; mm.
- Box x ∈ [−35, 35], y ∈ [−35, +30], z ∈ [3, 53]. Wheels (±42, −15, 15). Nose point (0, +55, 0).

## 9. Profiles as math
- **Side wall outline (YZ)**: rectangle y ∈ [−35, 30], z ∈ [3, 53] with top corners rounded r 10 (arc centres (−25, 43) and (20, 43)); right wall adds the tab: rectangle y ∈ [−35, −23], z ∈ [53, 68] with a rounded top.
- **V nose**: two triangles sharing the ridge from A = (0, +55, 0) to B = (0, +30, 20): left face A, B, C_L = (−15, +30, 0)… with the top edge B–(±15, +30, 20); i.e. each face is the triangle {A, (0, 30, 20), (±15, 30, 20)} plus the lower triangle {A, (±15, 30, 20), (±15, 38, 0)}. Ridge slope atan(20/25) = 38.7°.
- **Side plates**: planes through (±15…±35, 38, 0) and (±15…±35, 25, 18): slope atan(18/13) = 54°… use 40° for FS-R (lower), 60° for FS-L (AWS 62 hangs steeper).
- **Blade motion (guess)**: blade position y(t) = y₀ + (s/2)·sin(ωt), stroke s ≈ 18 mm.

## 10. Pixel-based measurements
- **AWS 62** (615 × 550): box front-left top corner (85, 115), front-right top (400, 95) (behind the right side), box bottom-left (115, 320). Nose: top edge (255–385, 360–390), point (330, 520). FS-R: (330–520, 300–410). FS-L: (105–250, 270–460). Wheels: left (75–120, 270–390), right (455–500, 200–310). Chain (175–235, 70–105). Tab (370–410, 10–55).
- **AWS 63** (344 × 295): box (80–320, 20–250); blade L (20–105, 60–110); blade R (175–250, 105–140); right wheel (265–315, 155–225); nose (120–185, 190–275).

## 11. Several independent estimates

| Quantity | Method A (kit / rules) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Box width | kit 70 | wheel Ø ≈ 0.43 W | AWS 62 front ≈ 315 px; wheel 120 px tall → if Ø 30, 4 px/mm → 79 (perspective at the nearer front) | **70** |
| Box height | kit 55 | ≈ 0.7 W | AWS 62 left front edge 115 → 320 = 205 px / 4 → 51 | **50** |
| Wheel Ø | kit 28 | ≈ 0.6 × box height | AWS 63 right wheel 70 px vs box height ≈ 115 px (at similar depth) → 0.61 × 50 = 30 | **30** |
| Nose length (point ahead of box) | kit plate at 35° | ≈ 0.35 W | AWS 62 ≈ 130 px vertical at 30° view → ≈ 25 | **25** |
| Blade overhang ahead | — | ≈ 0.4 W | AWS 63 ≈ 85 px along the foreshortened Y; scale ≈ 3.4 px/mm → 25–35 | **30** |

## 12. Consistency check
1. **Length vs cube**: box 65 + nose 25 = 90 in Y, plus the left blade overhang 30 beyond the box top front (y +60) — fits within 101.6 overall only if the blades are near their **retracted** position at the start (the box rear at −35 to blade tip +60 = 95). Consistent.
2. **Height**: 53 + tab 15 = 68. Fits.
3. **Blade direction**: AWS 63 shows both blades parallel to the side-wall edges; AWS 60 agrees. **Fore-aft.**
4. **Wheel position**: AWS 62 suggests the wheels are in the rear half; AWS 63 shows the right wheel at the rear-right. Consistent.

---

## 13. Why the designer did it (per part, mostly adversarial)

- **Clear polycarbonate box**
  - Fight: polycarbonate is **very tough** for its weight; it flexes and absorbs hits from spinners and wedges instead of shattering. A plain box has no small parts to snap off.
  - Weak points: tall (50 mm) and flat-sided, so it is easy for wedges to get under and for flippers to tip; it cannot run inverted.
  - Construction: easy to cut by hand from sheet; transparent, so the builder (and judges) can see inside; cheap; quick to repair.
- **V nose + sloped side plates (plough)**
  - Getting under vs contact: the **point on the floor** meets an opponent first and slides under its edge; the V faces spread the load and lift the opponent's corner; the side plates catch opponents that slide off the nose. Aluminium on the nose and right plate resists cuts; clear PC on the left is a lighter replacement (perhaps after damage).
  - Against spinners: a pointed nose deflects horizontal spinners sideways instead of taking a square hit.
- **Jigsaw blades**
  - Fight: a cheap, legal **cutting weapon**: the reciprocating teeth scrape and cut into plastic armour, wires and tyres of an opponent pinned on the nose. Two blades at different positions increase the chance of contact.
  - Weak points: low energy; a fast opponent will not stay in contact; blades can snap or bend; the mechanism adds weight.
  - Construction: standard jigsaw blades are cheap and easy to replace.
- **Top beam and tab**
  - Construction: the beam stiffens the box top; the tab gives a handle or guide.
- **Exposed wheels**
  - Fight: big treaded tyres give good grip; they are unguarded, a weak point against side attacks.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 or micro gearmotors | 12 × 10 × 25 | low in the rear half, shafts at z 15 | medium |
| Saw motor | N20 or 130-size gearmotor with a crank disc | 12 × 10 × 30 | upper middle | low |
| Slider | printed or aluminium carriage on rails along the top edges | 60 × 10 × 6 | z 40–50 | low |
| Battery | 2S LiPo 200–300 mAh | 40 × 18 × 10 | floor, centre-front | low |
| ESC/receiver | green board seen | 25 × 15 | right-centre | medium |
| Switch | black part on the top-right | 12 × 4 | top rear-right | low |
| Box joints | small aluminium angles with M2 screws | — | edges | low |

## 15. What the photos cannot show
- The saw mechanism, exact blade mounting and stroke.
- The rear, underside and box joints.
- Fine detail of everything (small, blurry photos).
- All mm values ±20%.

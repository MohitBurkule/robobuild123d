# Brisk: full rebuild description from reference photos

Source photos:
- `robots/brisk/reference/brisk.aws76.webp` (**primary**, cut out onto white, sharp): AWS 76. **Front-right three-quarter**, camera about 30–35° above the floor and about 40° to the right of the nose. The big orange flipper plate fills the right two-thirds of the image; the robot's **right** side (with a wheel inside an open side pocket) is on the image left; the grey top lid and the lime-green actuator link are at the top.
- `robots/brisk/reference/brisk.aws78.webp`: AWS 78. A **tiny** image (247 × 205 px), dark, **front-left** (`REFERENCE.json`), cut out onto black. It shows the same orange plate, slot, lime link and grey lid, and a small notch at the front edge. It adds almost no detail; it confirms that the design was unchanged.

**Limitation**: effectively one useful photo. The left side, rear and underside are not seen and are mirrored or inferred **(guess)**.

`REFERENCE.json`: `flipper`, 2 wheels, weapon flipper, axis x.

Pixel coordinates refer to AWS76 scaled to 1200 × 740, ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit and from the visible wheel (a common **Ø 26–28 mm foam/rubber-tyre wheel with a grey hub**). Ratios use **W = flipper plate width ≈ 92 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the plate's floor edge), **+Z** = up. **Origin O** = floor point under the centre of the chassis footprint (the box under the plate and lid, excluding the plate's forward overhang).
- **Flipper angle φ** = angle of the plate surface above the floor, YZ plane. At rest φ ≈ 30°.

| ID | Part |
|---|---|
| CH | orange chassis tub |
| LD | grey top lid at the rear |
| LD-S | silver screws on the lid |
| FP | orange flipper plate (front, full width) |
| FP-SL | central slot in FP |
| FP-S | 4 silver countersunk/pan screws on FP |
| FP-N | small notch/hole at the front edge (right of centre) |
| HG | flipper hinge (hidden, at the plate's rear edge; guess) |
| CK | grey clevis knuckles on the lid (pivot block) |
| CK-B | black screw/bolt through CK |
| LV | lime-green actuator lever/link |
| SV | servo (hidden; blue/black parts seen through the slot) |
| SP-R / SP-L | open side pockets for the wheels |
| GW-R / GW-L | orange outer side walls of the pockets (wheel guards) |
| GW-H | holes in the guard walls (Ø 4 and Ø 2.5) |
| GW-S | silver screw at the guard's top rear |
| WH-R / WH-L | drive wheels (grey hub, black knurled tyre) |
| DM-R / DM-L | drive motors (dark part behind the wheel, partly seen) |
| BAT, RX, ESC | hidden electronics (guess) |

---

## 1. Overall description in one paragraph

Brisk is a **compact two-wheel servo flipper** dominated by **one big orange plate**. Seen from the front it is almost all plate: an **orange printed sheet about 92 mm wide and 66 mm long**, with a **pebbled/textured top surface**, sloping at about 30° from a **bevelled edge on the floor** up to the top of the robot. Its rear corners are **cut off at 45°**, and a **long central slot** at its rear lets a **lime-green lever** pass through. Behind the plate, the top of the robot is a **grey printed lid** with silver screws and a **grey clevis block** on the centreline, from which the lime lever runs forward and down through the slot to the plate's underside. On each side, behind the plate, an **open pocket** holds a **wheel with a black knurled tyre and a grey hub**, enclosed on the outside by an **orange guard wall** with two holes and a screw. The chassis tub under everything is orange, about 70 mm wide at the floor, with chamfered lower front corners.

---

## 2. Part-by-part description

### 2.1 Chassis tub (CH)
- **Shape**: an orange box, about **70 mm wide (X) between the pockets × 76 mm long (Y) × 30 mm tall**, hidden mostly under the plate and lid. In AWS76 its **right lower front** is visible below the plate's right rear edge: a **vertical side face** (about 18 mm tall) with a **45° chamfered lower front corner** where the side meets the front (the face at (240–300, 430–560) px), so in plan the tub's front corners are chamfered.
- **Floor**: flat at z ≈ 2 **(guess)**.
- **Colour/material**: **orange PLA/PETG**, textured surfaces where printed against a textured bed (the plate shows strong pebble texture; the sides show layer lines).

### 2.2 Grey top lid (LD) and screws (LD-S)
- **Shape**: a flat **grey (blue-grey) printed plate**, about **62 mm wide × 34 mm long × 3 mm thick**, at **z ≈ 30–33**, covering the rear part of the tub behind the flipper plate. Its edges are straight with small chamfers. The plate's rear edge overlaps the lid's front part.
- **Screws**: **silver pan-head Phillips**, head Ø 4 mm (M2): one at the front-right corner (x +28, y −2) and one at the rear-right corner (x +22, y −30) visible; a third at the rear-left (x −22, y −30) in AWS76 at (660, 50) px. Likely **4** in total.
- **Colour**: matt blue-grey PLA.

### 2.3 Clevis knuckles (CK, CK-B)
- **Shape**: on top of the lid, on the centreline at about y −20, a **grey clevis**: two **grey cylinders (Ø 9 mm × 5 mm)** standing on small pedestals, about **14 mm apart** (inner faces), with a **black screw/threaded rod** (Ø 2.5–3 mm) passing **transversely (X)** through both and the lever between them. Black nut/screw heads show on both outer ends (AWS76 at (430, 100) px and (540, 75) px).
- **Height**: axis at about **z 40**.
- **Function**: a **pivot** for the top end of the lime lever.

### 2.4 Lime-green lever (LV)
- **Shape**: a **flat bar**, about **8 mm wide × 5 mm thick × 45 mm long**, bright **lime/chartreuse** printed plastic, with a rounded end around the clevis pin.
- **Pose**: from the clevis (y −20, z 40) it runs **forward and down at about 50–55°** below horizontal, passing through the plate slot FP-SL at about (y 0, z 22), and disappears under the plate. Its lower end is presumably pinned to the **underside of the plate** or to a **servo horn** inside **(guess)**.
- **Interpretation (preferred)**: the clevis is a **fixed pivot** and LV is the **servo output lever**: the servo's output shaft (along X) is the clevis pin (the black screw is the horn screw into the spline, and the grey cylinders are bearing bosses printed on the servo mount). Rotating LV **forward/down** drives its lower end against the plate's underside, lifting the plate front **(medium confidence)**. Alternative: LV is a **passive link** between the plate and a servo horn inside the tub, with the clevis being the joint on the plate side **(low confidence)**.

### 2.5 Flipper plate (FP, FP-SL, FP-S, FP-N)
- **Shape**: a **flat orange plate**, about **3 mm thick**, outline (in its own plane):
  - **Front edge**: straight, **92 mm wide**, with a **bevel** along its underside (a sharp leading edge on the floor; in AWS76 the front edge looks very thin, ~1 mm).
  - **Sides**: straight, parallel, about **52 mm** long up the slope.
  - **Rear corners**: **cut at 45°**, each chamfer about **14 mm** in X and Y, so the rear edge is about **64 mm** wide.
  - **Slot (FP-SL)**: a **rectangular slot**, about **14 mm wide × 22 mm long** (along the slope), on the centreline, open to the **rear edge** (a notch), with square corners. AWS76: slot edges at x ≈ (490–660, 145–275) px.
- **Pose**: at rest the plate slopes at **φ ≈ 30°**: front edge at (y +62, z 0), rear edge at (y +4, z 33). It sits just above the side pockets' front edges and the lid's front edge.
- **Surface**: **pebbled texture** (printed face-down on a textured PEI sheet), with many tiny bright flecks.
- **Screws (FP-S)**: **4 silver countersunk or low pan screws** (head Ø 4.5 mm): two on the left of the slot at (x −22, 18 mm and 30 mm down-slope from the rear edge) and (x −30, …), two on the right at (x +20, 8 mm) and (x +28, 20 mm). In AWS76 at (400, 235), (455, 330), (780, 135) and (840, 220) px. They fix the plate to the **hidden hinge arms/brackets** under it **(guess)**.
- **Notch (FP-N)**: a **small dark notch or hole** at the front edge, right of centre (x ≈ +40 in AWS76 at (1120, 410); AWS78 shows a notch near the right front corner) — possibly a **chip** or a **pin hole** **(uncertain)**.
- **Colour**: orange, the same filament as the tub.

### 2.6 Hinge (HG), hidden
- The plate must pivot somewhere for a flipper. Candidates:
  1. **Rear hinge (preferred)**: two knuckles under the plate's rear edge on the tub at (x ±28, y +2, z 30), with a pin along X. The plate then rotates up about its rear edge, the front edge rising — a "front-hinged flipper plate" in reverse, i.e. a classic **lifting wedge**.
  2. **Front-low hinge**: a hinge near the front of the tub, with the plate as a lever — less likely, as the plate's lowest part is its leading edge.
- The 4 plate screws likely fix the plate to **two printed hinge arms** that run along its underside to the rear hinge **(guess)**.

### 2.7 Side pockets (SP-R, SP-L) and guard walls (GW-R, GW-L)
- **Pocket**: on each side, between the tub's side wall (x ±35) and an **outer guard wall** (x ±47), an **open-topped, open-front-and-back slot** about **12 mm wide** and **50 mm long**, holding the wheel.
- **Guard wall shape**: an **orange vertical plate**, about **3 mm thick**, **52 mm long (Y) × 30 mm tall (Z)**, with a **bottom flange/rail** (the pocket floor) about 10 mm wide joining it to the tub at the bottom, and a **rear end** that is **angled**: in AWS76 the wall's rear upper corner is **chamfered at about 45°** (the wall top edge runs forward from a sloped rear edge). Its front end meets the plate's side.
- **Holes (GW-H)**: two round holes on the outer face: a **larger hole Ø 4–5 mm** at (y −10, z 10) and a **smaller hole Ø 2.5–3 mm** at (y +8, z 8). In AWS76 at (150, 405) and (210, 460) px. The larger hole is on the wheel axle line: it is the **access hole to the wheel's set screw / axle end** or a bearing hole for an outer axle; the smaller hole may be a motor-clamp screw hole or a pin **(guess)**.
- **Screw (GW-S)**: a **silver pan-head screw** at the **top rear** of the guard wall (x +47, y −28, z 30) in AWS76 at (175, 175) px, fixing the wall's top to the lid/tub via a **top bridge** **(guess)**.
- **Supports**: the guard wall is joined to the tub by the **pocket floor flange** (bottom) and the **top-rear bridge with GW-S** (top). It is probably printed **as one piece with the tub** (the pocket being a U-channel), with the screw securing the lid. **(medium)**
- **Coverage**: the wall covers the wheel's outer face fully below z 30; the wheel top (z 28) is below the wall top, so from the side the wheel is **fully hidden**. From the front it is hidden behind the plate; from the rear it is open.

### 2.8 Wheels (WH-R, WH-L) and drive motors (DM)
- **Wheels**: **Ø 28 mm × 10 mm**, **black tyre with a fine knurled/diamond tread** (looks like foam-rubber "sticky" tyres or knurled rubber), on a **grey plastic hub** (Ø 18) with a recessed centre. Only the right wheel is seen (AWS76 at (105–240, 255–370) px).
- **Position**: centres at **x ±41, y −14, z 14**.
- **Motor**: a **dark cylindrical part** behind/inboard of the wheel (AWS76 at (215–265, 350–400) px), probably the **N20 gearmotor** or its **gearbox**, lying along X.
- **Track**: outer faces of the wheels at x ±46, just inside the guard walls (x ±47 inner face → 1 mm gap).

### 2.9 Visible internals through the slot
- Through FP-SL: **blue** and **black** parts and a bit of **green** (AWS76 at (510–640, 150–270) px) — a **blue servo case** (e.g. an Emax/Corona blue micro servo), black wires and the green lever's lower part **(guess)**.

---

## 3. Per-view sections

### 3.1 AWS76 (front-right)
- **Right two-thirds**: the plate as a large parallelogram: front edge from (410, 690) to (1165, 420); right-side edge (in image the far side) from (1165, 420) up to (950, 140); rear chamfers to (650, 75) and the slot at (490–660, 145–275); left side edge from (410, 690) up to (240, 400); near rear chamfer from (240, 400) up to (300, 190).
- **Upper left**: the grey lid (230–740, 35–190) with screws at (290, 130), (660, 50), (720, 90); the grey clevis knuckles at (415–565, 65–120) with the black pin ends; the lime lever from (510, 85) to (600, 290).
- **Left**: the right pocket with the wheel (105–240, 255–370), the orange guard wall (45–300, 135–520) with its two holes and the top screw; the chamfered lower front of the tub at (240–300, 430–560).

### 3.2 AWS78 (front-left, tiny)
- Plate in front with the slot and lime lever, grey lid at the rear, the left pocket at the image left, a notch at the plate's front right. Proportions match AWS76.

### 3.3 Top view (synthesised)
- Overall about **94 × 96 mm**: a 92-wide plate from y +4 to +62, with 45° rear corners and a 14 × 22 slot open to its rear edge; behind it the grey lid (62 × 34) with the clevis; on each side the pocket (12 wide) and guard wall (3 wide) from y −40 to +12, with the wheels at y −14.

### 3.4 Front view
- A wide trapezoid: the plate from the floor (92 wide) up to z 33 (rear edge 64 wide), the lime lever and clevis above it on the centreline (to z 45), the grey lid line, and the two guard walls at x ±47 rising to z 30.

### 3.5 Right side view
- The guard wall rectangle (52 × 30, rear upper corner chamfered) with two holes; the plate as a 30° line from (62, 0) to (4, 33); the lid at z 33 to the rear; the clevis knuckle at (−20, 40) with the lever running down-forward to the slot.

### 3.6 Rear view (not photographed)
- Tub rear wall 70 × 30 with the wheels visible in their open pockets on each side; probably a switch here **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | tub | 70 × 76 × 30 | 0.76 × 0.83 × 0.33 | orange FDM | — | 1 |
| LD | flat lid | 62 × 34 × 3 | 0.67 × 0.37 | blue-grey FDM | 4 × M2 | 1 |
| CK | 2-knuckle clevis | Ø 9 × 5 each, 14 apart | — | grey FDM | pin + nut | 1 |
| LV | flat lever | 8 × 5 × 45 | 0.49 | lime FDM | clevis pin; lower end hidden | 1 |
| FP | chamfered plate | 92 × 66 × 3 | 1 × 0.72 | orange FDM, textured | 4 × M2 | 1 |
| FP-SL | slot | 14 × 22 | 0.15 × 0.24 | — | — | 1 |
| GW | guard wall | 3 × 52 × 30 | 0.03 × 0.57 × 0.33 | orange | integral + 1 screw | 2 |
| WH | knurled wheel | Ø 28 × 10 | 0.30 × 0.11 | black tyre, grey hub | motor shaft | 2 |
| FP-S | screw | head Ø 4.5 | — | silver | into hinge arms | 4 |
| LD-S / GW-S | pan screw | head Ø 4 | — | silver | into CH | 4 + 2 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| FP front edge ↔ floor | touching | 0 |
| FP rear edge ↔ LD front edge | overlap/above | 1–2 above |
| FP underside ↔ GW top front corner | above | 2–4 |
| FP slot sides ↔ LV | clearance | 3 each side |
| LV ↔ CK pin | pivot | 0 |
| CK ↔ LD | integral / screwed | 0 |
| LD ↔ CH | screwed | 0 |
| WH outer face ↔ GW inner face | near | 1 |
| WH inner face ↔ CH side wall | near | 1–2 |
| WH tread ↔ pocket floor | clearance | 2 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ GW top | below | −2 |
| GW ↔ CH | integral (bottom), screw (top) | 0 |
| CH floor ↔ floor | above | 2 |

---

## 6. Mechanism
- **Drive**: two wheels, skid steer, behind the plate's centre of pressure; the plate's front edge is the third contact.
- **Flipper**: a servo inside (axis along X at the clevis, z ≈ 40 — or lower inside the tub) swings LV; LV pushes the plate's underside; the plate rotates about the rear hinge HG (y +2, z 30) and its front edge rises. For a 58 mm lever (hinge to front edge), each 10° of rotation raises the edge by ~10 mm; a fast servo makes this a **flipper** rather than a slow lifter. Its full-width plate tips the opponent backward.

---

## 7. Assembly order (suggested)
1. Print CH (with integral side pockets and guard walls), LD (with clevis bosses), FP, LV, hinge arms.
2. Install the drive motors in the pockets' inner walls; fit the wheels through the open pocket tops; fix through the guard-wall access holes.
3. Install the servo under the lid at the clevis; electronics in the tub.
4. Screw LD to CH (4 screws) and the guard tops (GW-S).
5. Attach LV to the servo output at the clevis with the black screw.
6. Fit the hinge arms to the plate (4 screws), mount the plate on the rear hinge, pass LV through the slot.

---

## 8. Hidden / uncertain list
- Hinge location and the exact role of LV.
- Servo type, location and output axis height.
- The left side, rear, switch and underside.
- The notch at the plate front.
- All mm ±15–20% (essentially one photo).

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the tub centre; +X right, +Y forward, +Z up, mm.
- Tub x ∈ [−35, +35], y ∈ [−40, +36], z ∈ [2, 30]; guard walls x ±[44, 47]; plate y ∈ [+4, +62], z ∈ [0, 33]; clevis to z 45.

## 10. Profiles as math

**10.1 Plate outline (in plane: u across, v up the slope from the front edge).** Polygon: (−46, 0) → (+46, 0) → (+46, 52) → (+32, 66) → (+7, 66) → (+7, 44) → (−7, 44) → (−7, 66) → (−32, 66) → (−46, 52) → close. Pose: (x = u, y = 62 − v·cos 30°, z = v·sin 30°). Front bevel: the underside chamfered 3 mm → a 1 mm edge.

**10.2 Plate rotation.** Hinge H = (y +4, z 33)… i.e. the plate's rear edge. Front edge E(θ) = H + 66·(cos(−30° + θ)… in YZ: E = (4 + 66·cos(30° − θ)·1, 33 − 66·sin(30° − θ)) for the plate rotating up by θ about H. At θ = 0: (61.2, 0); θ = 30°: (70, 33); θ = 45°: (67.7, 50).

**10.3 Lever LV.** Line from C = (y −20, z 40) at angle −52° (down-forward): P(s) = C + s·(cos 52°, −sin 52°), s ∈ [0, 45] → lower end (7.7, 4.5)?? — too low; so LV is ~30 mm long to reach the plate underside at (y −1.5, z 16)… use s ∈ [0, 30]. See 13.3.

**10.4 Guard wall (YZ, at x ±44…±47).** Polygon (−40, 2) → (+12, 2) → (+12, 30) → (−28, 30) → (−40, 18) → close. Holes: Ø 4.5 at (−14, 14) [axle line], Ø 2.8 at (+6, 8).

**10.5 Wheel.** r 14, width 10, knurl ±45° grooves 0.4 deep, pitch 1.2. Hub r 9, recess 1.5.

**10.6 Clevis.** Two cylinders r 4.5, axis along X at (y −20, z 40), x ∈ [−12, −7] and [+7, +12]; pin r 1.5 from x −14 to +14.

## 11. Pixel measurements (AWS76, 1200 × 740)
- Plate front edge length ≈ 805 px (oblique); right (near) side edge ≈ 340 px; far side ≈ 330 px.
- Wheel ≈ 135 px tall × 115 px wide.
- Guard wall length ≈ 255 px (oblique), height ≈ 200 px.
- Lid width (visible) ≈ 510 px.
- Slot width ≈ 90 px near its mouth; lever width ≈ 45 px.
- Clevis knuckle Ø ≈ 45 px.

## 12. Several independent estimates

| Quantity | Method A (rule / typical) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Plate width | ≤ 101.6, flush with guards → 94 | — | 805 px oblique; wheel 135 px = 28 mm → 4.8 px/mm → 805/4.8 = 168 × cos(~55° obliquity) = 96 | **92** |
| Plate length (slope) | (101.6 − 40 rear) / cos 30 = 71 | 0.72 W = 66 | 340 px / 4.8 = 71 (near side, slightly enlarged) | **66** |
| Wheel Ø | 26–30 | 0.30 W | reference | **28** |
| Body height | plate rear 33 | 0.36 W | guard wall 200 px / 4.8 ≈ 42 × (foreshortening ~0.75) ≈ 31 | **30–33** |
| Lid width | 62 | 0.67 W | 510 px / 4.8 ≈ 106 × cos(55°) ≈ 61 | **62** |
| Lever width | 8 | — | 45 / 4.8 ≈ 9 | **8** |

## 13. Consistency check
1. **Box fit**: depth from the lid rear (y −40) to the plate edge (y +62) = 102: **1 mm over**. Shift: tub y ∈ [−38, +36] and plate edge at +62 → 100 ✓.
2. **Width**: plate 92 vs guard walls ±47 = 94 — the plate is slightly narrower than the guard-to-guard width, matching AWS76 where the guard wall sticks out at the plate's left rear.
3. **Lever length**: 45 mm (pixel impression) would put its end below the floor; the lever must end at the plate's underside, ~30 mm from the clevis. The extra visible length in the photo is the part seen through the slot plus perspective. **Reconciled 30–32 mm.**
4. **Hinge**: if the plate hinged at the rear, its rear edge could not rise; the slot open to the rear edge lets the lever pass whatever the plate angle — consistent with a rear hinge.

---

## 14. Why the designer did it (adversarial first)

- **One huge full-width plate**: the robot's whole front is a ramp, so no matter how an opponent approaches from the front, it meets the plate's thin leading edge and is scooped up; a flipper plate this wide gives a stable launch. At 30° the plate also **deflects vertical spinners** upward and sends horizontal spinner hits over the top. The textured face gives no grip to opponents' wheels if they climb on. Weak points: a 3 mm printed plate can flex and its thin edge chips; spinners can bite at the leading edge.
- **45° rear corners**: remove material where no opponent will ever be, saving weight, and stop the corners snagging on the guard walls when the plate rises.
- **Slot open to the rear**: lets the actuator lever stay central (no twisting load) and pass through the plate at any angle; the plate shields it from the front.
- **Lever on a top clevis**: places the actuator above the plate's hinge so the servo pushes with good leverage at the start of the stroke; replaceable cheap lever acts as a fuse (it breaks before the servo gears strip).
- **Wheels in side pockets with guard walls**: the wheels are completely shielded from side hits and from horizontal spinners; the walls' holes give tool access to the axle without disassembly. The pockets are open at the top, so the robot can still drive on the wheels if flipped? — no: the wheel tops are below the wall tops, so **Brisk is not invertible** on its wheels; the flipper must self-right (a flipper pushing on the floor rights the robot) **(guess)**.
- **Grey lid**: a separate, quick-access hatch for the electronics; the colour contrast helps the driver see orientation.
- **Chamfered tub corners**: deflect hits and reduce snagging.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Flipper servo | blue metal-gear micro/mini servo (fast type) | 23 × 12 × 27 | (0, −20, 22), output along X at z ≈ 40 via the clevis | medium |
| Plate hinge arms | two printed arms under the plate, 4 screws, hinge pin Ø 3 at (y +4, z 30) | 8 × 50 × 6 | x ±22 | low |
| Drive motors | 2 × N20 gearmotors along X | 12 × 10 × 25 | (±28, −14, 14) | medium |
| Battery | 2S LiPo 200–300 mAh | 40 × 18 × 9 | (0, +12, 8) under the plate | medium |
| RX/ESC | combined brushed ESC/RX | 25 × 20 × 6 | (0, −32, 10) | low |
| Power switch | rear wall slide switch / link | 10 × 5 | (+15, −38, 15) | low |
| Wiring | servo lead to RX at the rear; motor leads short | — | — | medium |

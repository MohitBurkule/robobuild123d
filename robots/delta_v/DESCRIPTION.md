# Delta V: full rebuild description from reference photos

Source photos (cut out by the AWS wiki):
- `robots/delta_v/reference/delta_v.aws72.webp`: front-left three-quarter, about 35° down. **4 short forks.**
- `delta_v.aws74.webp`: front-left, about 30° down, with a strong green colour cast (the body is really black). **2 long outer forks.**
- `delta_v.aws76.webp`: front-right three-quarter, about 25° down. **Full-width flat wedge blade.**

Facts come from the photos; inferences are marked **(guess)**. Sizes are estimated against the AWS 150 g / 101.6 mm cube limit. **W = body width over the side plates ≈ 72 mm.**

---

## 0. Coordinate frame
- **Origin O** = the floor point under the centre of the body footprint (side plate to side plate; rear wall to the front face of the pods, excluding forks/blade).
- **+X** = robot right, **+Y** = forward, **+Z** = up. Units are mm.
- Body: x ∈ [−36, +36], y ∈ [−34, +34], z ∈ [0, 24].

## 1. Part IDs

| ID | Part |
|---|---|
| BD | black main body (tub, rear 2/3) |
| LD-L / LD-R | inset top lid panels |
| SPL-L / SPL-R | black stadium side plates |
| WH-L / WH-R | yellow drive wheels (rear) |
| PD-L / PD-R | front wedge pods |
| EY-L / EY-R | "sleepy eye" stickers |
| SLT | weapon slot between the pods |
| TW | right weapon tower (motor mount) |
| BH | left bearing housing (outboard support) |
| OR | outrunner motor (black bell) |
| DS | yellow single-tooth weapon disc |
| SH | weapon shaft/bolt plus nut |
| FK72 | 4 short forks (AWS72) |
| FK74 | 2 long forks (AWS74) |
| BLD | full-width wedge blade (AWS76) |
| SW | white switch/connector (rear right) |
| S-* | screws |

## 2. Overview
Delta V is a **compact black vertical spinner**. A **yellow, single-tooth, hook-shaped disc** spins on a transverse axle in a **slot between two front wedge pods**. The disc is carried on a **black outrunner** bolted to a **D-shaped right-hand tower**, with an **outboard bearing housing** on the left. There are two **yellow drive wheels** at the rear corners, inside **stadium-shaped black side plates**. Each pod has a cartoon **"sleepy eye" sticker**, so the front looks like a face. The forks/wedge changed at each event.

---

## 3. Part-by-part

### 3.1 Body BD
- **Shape**: a black box, **64 mm wide (between the side plates) × 40 mm long (rear block, y −34 to +6) × 24 mm tall**. The top is flat at z = 24. The front of the rear block meets the pods at y ≈ +6. Wall thickness is about 2.5 mm **(guess)**.
- **Colour/material**: matt black PLA or PETG with a fine layer texture.
- **Top**: two **inset lid panels LD** (each about 26 × 34 × 2 mm, recessed 0.5 mm), separated by the weapon tower area. Each is fixed with **2–4 small black pan screws** (Ø 3 mm heads). AWS72 shows 2 screws near the rear corners of the left lid, and AWS74 shows 2 at the rear left.
- **Rear-right**: a **white switch/connector SW** (about 8 × 5 mm) in a rectangular cut-out on the top surface near the right wheel (AWS76).

### 3.2 Side plates SPL
- **Shape**: **stadium**, **L 60 × H 24 × T 3 mm**, end radius 12. Math (plate YZ frame): union of rectangle y ∈ [−18, +18], z ∈ [0, 24] and circles of centre (±18, 12), r = 12.
- **Position**: outer faces at x = ±36, spanning y ∈ [−34, +26].
- **Screws**: **3–4 small black Phillips/socket screws**: one top-front (y +15, z 20), one mid (y 0, z 12), one bottom-rear (y −20, z 5), and sometimes one top-rear. They fix the plates to the body side walls or standoffs.
- **Function**: wheel guards. The wheel's outer face sits about 1 mm inside.

### 3.3 Wheels WH
- **Shape**: **Ø 28 × 8 mm**. A **yellow/cream speckled tyre** (foam-like or yellow TPU with a granular surface) on a hub with **3 round holes** (Ø about 5, at r 7).
- **Position**: centres (±29, −20, 14). The tops (z 28) stick out **4 mm above the body top** and show through **notches in the body's rear top corners** (each about 10 × 20 mm). The bottoms are at z 0.
- **Drive**: one wheel per side (2WD). The motors are inside the rear block **(guess)**.

### 3.4 Front pods PD
- **Shape**: a **prism with a sloped top**. Each pod is **24 mm wide (X) × 28 mm long (Y)**. The back height is 24 (flush with the body top). The top face slopes in **two facets**: an upper facet (y +6 → +14, about 20° down, carrying the eye) and a lower, steeper facet (y +14 → +34, about 35°, with oval recesses) down to the front at z ≈ 6. Math, YZ polygon: (6, 0) → (6, 24) → (14, 21) → (34, 7) → (34, 0).
- **Position**: PD-L x ∈ [−36, −12], PD-R x ∈ [+12, +36].
- **Recesses**: each lower facet has **3 oval pockets** (about 7 × 5 mm, 2 mm deep). Two upper pockets hold **black Phillips screws** (fixing the forks/blade from above). The lower pocket is empty or a fork-slot access hole.
- **AWS74 variant**: the pods are **tapered in plan to a chisel nose** at the outer front corner, each pointing at its single fork.

### 3.5 Eye stickers EY
- A **round sticker, Ø 11 mm**: white disc, black outline, a **black half-moon pupil** in the lower half and a **thick black "eyelid" line** across the middle, giving a sleepy look. One on each pod's upper facet, centred at x ±24. In AWS76 the stickers are shiny (laminated with clear tape).

### 3.6 Weapon slot SLT
- A gap **24 mm wide** between the pods (x ∈ [−12, +12]), open from the pod fronts back to y ≈ +6, and continuing upward. The disc's lower part rotates in it. The slot floor is open or the floor plate is cut, so the disc tip clears the floor by about **3–5 mm** **(guess)**.

### 3.7 Right tower TW
- **Shape**: a **D-shaped upright**: a rectangle 18 (Y) × 20 (Z) with a semicircle of r = 9 on top. Thickness (X) **14 mm**. It stands on the body top at **x ∈ [+12, +26]**, y ∈ [−6, +12], rising from z 24 to z 53.
- **Face**: on its outer (+X) face there is a **4-hole bolt circle** (PCD about 12 mm, black socket screws M2) plus a **centre hole**. That is the **outrunner stator mount** (stator bolted to the tower, shaft pointing −X).
- **Colour**: matt black, scuffed.

### 3.8 Outrunner OR
- **Shape**: a black **cylindrical bell Ø 28 × 12 mm**, coaxial with the axle at (y +3, z 40), x ∈ [0, +12], between the disc and the tower. The rotor bell carries the disc.

### 3.9 Disc DS
- **Shape**: a **flat plate, 3 mm thick**, outline: a **hub circle** of r = 15 centred on the axle, plus a **single large hooked tooth**. Polar description (angle measured in the disc frame): r(θ) = 15 for θ ∈ [60°, 360°]; for θ ∈ [0°, 60°] the outline sweeps out along a curve from r 15 to a tip at r 30 (a logarithmic-spiral-like back edge, r = 15·e^(0.0115·θ°)), then the **hook front edge** returns sharply to r 15 at θ = 0 with a concave curve (an arc of r 12). There is a **triangular lightening hole** near the tip: a triangle with vertices at r 19, 25 and 25, spanning 15° and 35°. The overall diameter across the tooth is about 45 mm.
- **Colour**: **yellow** (painted or anodised; the AWS74 colour cast makes it lime green), with dark edges where the paint is chipped.
- **Mounting**: **4 black hex nuts / socket screws** on a PCD of about 16 mm to the outrunner bell, plus a hub boss.
- **Plane**: vertical, at x ≈ −1 to +2 (just left of the robot centreline, in the slot).

### 3.10 Left bearing housing BH and shaft SH
- **Shape**: a **black cylinder Ø 18 × 10 mm** with a **steel ball bearing** (Ø 10, silver race visible) in its outer face. A **threaded shaft end with a nut** (M4 **guess**) protrudes about 4 mm.
- **Position**: x ∈ [−14, −4], at the axle (y +3, z 40). It is carried by a **small black pillar** (about 10 wide) rising from the left body top behind PD-L **(guess; mostly hidden by the disc)**.

### 3.11 Front variants
- **FK72 (AWS72)**: 4 **steel strips 4 mm wide × 1.5 mm thick**, flat, protruding **22 mm** from slots at the pods' lower front edge, at x = −30, −16, +16 and +30. Each tip has a **barb**: a step to 7 mm wide at 6 mm from the end, then a chisel point.
- **FK74 (AWS74)**: 2 strips at x = ±32, protruding **40 mm**, with the same barb tips.
- **BLD (AWS76)**: a **flat plate 72 × 18 × 1.5 mm** (clear polycarbonate or thin steel, scratched; green-tinted edges), lying at about 15° below horizontal under both pods and across the slot. The front edge is at y +46, z 0. The front corners are chamfered 10 × 45°. It is held by the pod pocket screws (4 screws).

## 4. Per-view
- **Top**: a 72 × 68 rectangle. Two yellow wheel arcs show at the rear corners. Two lid panels sit at the rear. The tower is a 14 × 18 block right of centre, with the 4 mm-thick disc line plus the 12 mm-thick motor between the tower and the slot. The bearing housing is left of the disc. At the front: two pods with eyes and a 24 mm slot. Forks or blade ahead.
- **Front**: two pods (24 wide) at the left and right, with eyes. The slot in the middle shows the disc edge-on (3 mm) rising to z ≈ 70 at the tooth tip. The tower is behind on the right, and the bearing housing (silver bearing) on the left. The side plates are at the outer edges. Forks/blade at floor level.
- **Side (right, AWS76)**: the stadium side plate with 2–3 screws, the wheel top above it at the rear, the tower D-shape above the body, and the disc profile with the tooth up (tip about z 70). The pods slope down to the front.
- **Rear**: not photographed. Presumably a flat black wall with the wheels at the corners.

## 5. Part table

| ID | Size (mm) | Ratio W | Colour | Fixing | Qty |
|---|---|---|---|---|---|
| BD | 64 × 40 × 24 | 0.89 × 0.56 × 0.33 | black | — | 1 |
| LD | 26 × 34 × 2 | 0.36 | black | 2–4 × M2 | 2 |
| SPL | 60 × 24 × 3, R12 | 0.83 × 0.33 | black | 3–4 screws | 2 |
| WH | Ø 28 × 8 | 0.39 | yellow tyre | motor shaft | 2 |
| PD | 24 × 28 × 24 (sloped) | 0.33 × 0.39 | black | integral (guess) | 2 |
| EY | Ø 11 | 0.15 | white/black | sticker | 2 |
| TW | 14 × 18 × 29 | 0.19 × 0.25 × 0.4 | black | integral/screws | 1 |
| OR | Ø 28 × 12 | 0.39 | black | 4 × M2 to TW | 1 |
| DS | Ø 45 (tooth), hub r 15, 3 thick | 0.62 | yellow | 4 nuts to OR | 1 |
| BH | Ø 18 × 10 | 0.25 | black plus steel bearing | pillar | 1 |
| FK72 | 22 × 4 × 1.5 | 0.3 | steel | in pod slots | 4 |
| FK74 | 40 × 4 × 1.5 | 0.56 | steel | in pod slots | 2 |
| BLD | 72 × 18 × 1.5 | 1 × 0.25 | clear/steel | 4 screws | 1 |

## 6. Contact / gap matrix

| A ↔ B | Relation | Gap (mm) |
|---|---|---|
| LD ↔ BD | inset, screwed | 0 |
| SPL ↔ BD sides | screwed | 0 |
| SPL inner ↔ WH outer | clearance | 1 |
| WH top ↔ body top | above | +4 |
| PD back ↔ BD front | joined | 0 |
| PD inner faces ↔ DS | slot clearance | ~10 each side |
| DS ↔ OR bell | bolted | 0 |
| OR stator ↔ TW | bolted | 0 |
| OR ↔ DS ↔ BH | axle chain | 0.5 between rotating and fixed parts |
| DS tip (lowest) ↔ floor | clearance | 3–5 |
| DS tip ↔ PD front face (Y) | disc tooth sweeps ahead of the pods | tooth reaches y ≈ +26 vs pod front +34 (tooth inside the slot when level) |
| FK/BLD ↔ PD underside | clamped | 0 |
| FK/BLD ↔ floor | touching | 0 |
| TW base ↔ BD top | joined | 0 |

## 7. Mechanism
- The outrunner spins the disc (vertical, transverse axis). The likely rotation is **top-forward** (the tooth comes over the top toward the front, then down), or **bottom-forward up** (uppercut). The hook shape suggests the tooth's leading edge is the concave hook side, **guess: uppercut** (the tooth rising at the front to throw opponents up).
- Drive: 2 rear wheels; the front rests on the forks/blade (skids).
- Forks/blade: get under the opponent and feed it into the disc.

## 8. Assembly
1. Print BD with the pods, tower and bearing pillar. Install the drive motors, ESC, battery, receiver and switch.
2. Bolt the outrunner stator to TW (4 screws). Bolt the disc to the bell (4 nuts). Pass the shaft through the bearing housing BH; nut.
3. Fit the wheels; screw on the side plates.
4. Screw on the lids.
5. Fit the forks/blade with the pod screws. Stick on the eyes.

## 9. Pixel measurements
- **AWS72** (about 1280 × 1050): disc x 505–770, y 60–495 (the tooth tip at (720, 60)); bearing (520, 340); left pod eye centre (510, 545), right pod eye (900, 380); fork tips (690, 990), (880, 850), (1050, 780), (1230, 700). Left side plate x 55–420, y 330–750. Wheel at (140, 330).
- **AWS76** (about 1600 × 1310): disc x 640–1000, y 60–790; tower x 750–1120, y 280–760 with the 4 screws at about (990, 470); blade x 100–1110, y 780–1200; eyes at (535, 615) and (1040, 810); right wheel (1470, 580); side plate x 1110–1590, y 520–1080.

## 10. Independent estimates and consistency check

| Quantity | Limit/scale | Ratio | Pixels | Reconciled |
|---|---|---|---|---|
| Body width | 72 | — | AWS76: blade 1010 px wide = 72 mm → 14 px/mm | 72 |
| Disc overall | 45 | 0.62 W | AWS76: 360 px wide / 14 = 26?; 730 px tall / 14 = 52 | **disc Ø ≈ 50 including the tooth** (the width of 26 is a foreshortened edge view) |
| Disc tip height | 70 | — | AWS76: tip y 60 vs floor about 1200 → 1140 px / 14 ≈ 81 (perspective: the top is farther away) | **72** |
| Tower height above the body | 29 | 0.4 W | AWS76: 480 px / 14 = 34 | **31** |
| Eye Ø | 11 | 0.15 W | AWS76: 130 px / 14 = 9 | **10** |
| Side plate length | 60 | 0.83 W | AWS76: 480 px / 14 = 34 (foreshortened) | 60 |
| AWS74 fork length | 40 | 0.56 W | AWS74: ~330 px at ~8 px/mm = 41 | 40 |

Conflicts:
1. **Disc size**: the ratio (45) and pixel (50) estimates differ by 10%. **Reconciled: Ø 50 tooth envelope, hub r 15.** It must fit under the 101.6 mm cube height with its axle at z 40: 40 + 25 = 65 < 101. OK.
2. **Disc vs slot floor**: with the axle at z 40 and tooth r 25, the lowest point is z 15, so the **tooth does not reach the floor**. Earlier estimate (3–5 mm clearance) **corrected**: the disc's lowest point is about **z 15**; the pods' sloped faces and forks feed opponents up into it. If the axle is lower (z 30), clearance would be 5. **Reconciled: axle z = 34, lowest tooth point z ≈ 9.**
3. **Front configuration**: three different versions; the model should use AWS76 (the latest, full-width blade) as default.

## 11. Why the designer did it
- **Vertical single-tooth disc**: a single tooth gives the deepest bite per rotation (more "bite" against a spinning gap) and the energy is concentrated in one impact. The vertical axis throws opponents upward, and the gyroscopic effect is in the pitch plane (less turning disruption). The weak points are the exposed top of the disc and the tower (an overhead hammer could hit them), and asymmetric imbalance means vibration.
- **Outrunner direct drive**: no belts (a fragile part removed), compact and light. The motor bell is shielded between the disc and the tower. Risk: a hit transmits directly into the motor bearings, which is why the **outboard bearing housing** on the left shares the load.
- **Tower on the right only (D shape)**: one strong printed upright carries the motor, and the round top deflects hits. The outboard bearing on a small pillar gives a two-point support so the shaft does not bend.
- **Pods with sloped faces**: they guide opponents up into the disc and **protect the disc sides** from wedges and horizontal spinners. The eyes are personality.
- **Forks/blade evolution**: 4 short forks (AWS72) → 2 long forks (AWS74) → a full-width blade (AWS76). Each change gets **lower and wider** under opponents. The blade covers the slot as well, so opponents' wedges cannot sneak in under the disc. Thin steel or polycarbonate gets lower than printed plastic.
- **Stadium side plates**: shield the wheels from side hits. Round ends roll off walls.
- **Rear wheels sticking up 4 mm**: allow some driving inverted. The vertical spinner disc works inverted only if spun in reverse **(guess)**.
- **Black colour**: hides scuffs. Yellow disc for visibility/identity.

## 12. Unseen / inner parts

| Part | Guess | Size | Position | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | rear block, shafts to the wheels at (±22, −20, 14) | medium |
| Weapon ESC | 10–20 A brushless ESC | 25 × 12 × 5 | under LD-R | medium |
| Drive ESC | dual brushed ESC | 25 × 15 × 5 | under LD-L | low |
| Battery | 3S or 2S LiPo 250–350 mAh | 45 × 18 × 12 | across the rear block, x 0, y −22, z 9 | medium |
| Receiver | micro receiver | 20 × 12 × 5 | front of the rear block, x −10, y 0 | low |
| Switch | the white connector at the rear right is the switch/link | 8 × 5 | (+20, −28, 24) | medium |
| Weapon wires | three motor phase wires from OR through TW (hollow) into the body | — | x +18 | medium |
| Bearings | 1 ball bearing in BH (visible); the outrunner's own bearings on the right | Ø 10 | as stated | high |
| Shaft | M4 bolt or a 4 mm steel shaft through the bell and BH | Ø 4 × 35 | axle line | medium |
| Ribs | internal walls separating the battery and electronics; screw posts for the lids | 2 mm | — | low |

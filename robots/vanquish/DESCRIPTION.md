# Vanquish: full rebuild description from the reference photo

Source photo (only one):
- `robots/vanquish/reference/vanquish.aws76.webp` (1535 × 1299 px): AWS 76. Cut out onto white by the AWS wiki; black parts and the thin metal edges carry a **green cast** from the cut-out (the forks and the blade's edge look pale green but are really bright metal). Camera at the **front-left**, about **30° down**: the two forks point toward the lower left (the robot's front faces the lower left), so the robot's **right** half is on the image **left** and its **left** half, with the visible wheel, runs toward the image **lower right**.

Vanquish is a **wide, short vertical spinner**: a transverse black body with a wheel at each end, a **large asymmetric steel bar** spinning on an outrunner between **two black uprights** in the middle, and **two long thin forks** at the front corners. Facts are read from the photo; inferences are marked **(guess)**. Sizes are **estimates in mm**, from the AWS limit (150 g, 101.6 mm cube), the spec draft (body 90 × 62 × 24, two inboard wheels r 11, a bar weapon r 52 with 2 teeth on an X axis, a motor, uprights and forks) and pixel ratios using the **outrunner (about Ø 28)** and the **M4 nyloc nut (7 mm AF)** as scales. Ratios are against **W = body width (X) ≈ 90 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the body (mid-width, mid-depth).
- **+X** = robot right, **+Y** = forward (toward the fork tips), **+Z** = up. mm.
- Extents (reconciled §12): body x ∈ [−45, +45], y ∈ [−20, +12], z ∈ [2, 24]; uprights to z ≈ 42; weapon axle (y −2, z 38); blade swept radius 36 (top z 74, lowest z 2), see §13; forks to y ≈ +50.

| ID | Part |
|---|---|
| BH-L, BH-R | black body halves (left and right of the weapon gap) |
| GP | central gap / weapon slot between the halves |
| TP-L, TP-R | top plates of the halves (screwed, with a centre seam line) |
| UP-L, UP-R | black uprights (weapon supports) rising from the inner ends of the halves |
| MW | brushless outrunner (silver bell with copper windings visible) |
| BL | asymmetric steel bar blade ("S" shape, 2 teeth) |
| AX | axle: threaded M4 shaft with a **silver nyloc nut** on the left upright |
| BH | bearing housing on the right upright (black round boss) |
| LG | lower lugs/gussets at the bottom of the uprights (black, with screws) |
| FK-L, FK-R | long thin metal forks at the front outer corners |
| S-FK | 2 silver Phillips screws per fork |
| WH-L, WH-R | drive wheels at the outer ends (white hub, black tyre) |
| S-x | other screws: silver Phillips on top plates; socket head on the left top plate |
| M-L, M-R, BAT, ESC, WESC, RX | hidden motors and electronics |

---

## 1. Overall description in one paragraph

Vanquish is a **black vertical spinner with a huge blade**. Its body is a **wide, low transverse bar** about 90 mm across, 32 mm deep and 22 mm tall, split in the middle into **two halves** by the weapon slot. Each half is a black printed box tapering slightly toward its outer end, closed by a **top plate** with silver screws, and ending in a **drive wheel** (white hub, black tyre) at the outer end. At the inner ends, two **black uprights** rise in curved, swept shapes to about 42 mm, carrying a transverse axle: the right upright holds a round **bearing boss**, the left upright the **threaded axle end with a silver nyloc nut**. Between them a **brushless outrunner** (silver bell, copper windings visible through its spokes) spins a **large flat steel bar blade** about 88 mm long: an **asymmetric "S"** with a long upper arm ending in a rounded tooth and a shorter lower arm curving into a hooked tooth, its edges ground bright. At the front of each outer end, a **long thin metal fork** (about 45 mm) is screwed on with two screws and runs forward and down to a point on the floor.

---

## 2. Part-by-part description

### 2.1 Body halves (BH-L, BH-R)
- **Shape**: each half is a black printed box about **36 mm wide (X) × 32 mm deep (Y) × 22 mm tall** (z 2 to 24), from x = ±9 (inner face at the slot) to x = ±45 (outer end). The outer end is **rounded/chamfered** around the wheel (the left half's outer end in the photo has a curved wall following the wheel). The front faces are vertical; the inner front corners carry the uprights' lower lugs.
- **Material**: matt black PLA/PETG with fine layer lines, a lighter grey seam line along the top plates.

### 2.2 Top plates (TP-L, TP-R)
- **Shape**: flat black plates, about **30 × 28 × 2 mm**, on each half, with a **diagonal top infill pattern** and a **dashed seam line** down the middle of the left plate (image (1010–1040, 660–760)): a print seam or an embossed parting line.
- **Screws**: the left plate shows a **socket-head** screw at its front inner corner (image (1075, 825)) and a **silver Phillips** screw at its rear outer corner (1205, 685); the right half shows a silver screw near the upright (image (390, 605)). Another silver screw sits at the left half's rear near the upright (1005, 585).

### 2.3 Weapon slot (GP)
- A gap about **18 mm wide** (x ∈ [−9, +9]) between the halves, open at the front and top, through which the lower part of the blade passes. The bottom of the slot is open (the blade's lower tooth passes about 4 mm above the floor) **(guess)**.

### 2.4 Uprights (UP-L, UP-R) and lugs (LG)
- **Shape**: black printed **swept arms**, each about **8 mm thick (X)**, rising from the inner front corner of each half: a wide base (about 30 mm long) curving up and forward into a **rounded head** (radius about 9 mm) around the axle at **(y −2, z 34)**. The left upright's profile has a **concave front edge** and a straight rear edge sloping back to the half's top (image (700–960, 420–850)). The right upright is partly hidden behind the blade and motor (image (470–580, 330–560)).
- **Lugs LG**: at the base of each upright, **two stacked black lugs** with **round holes** (image (500–600, 790–860) and (760–860, 830–900)), screwed into the half's front face: the uprights are **separate parts** bolted to the halves **(medium)**.
- **Bearing boss BH (right upright)**: a **black cylinder**, about **Ø 18 × 8 mm**, with a glossy face (a flanged bearing or a printed cap) at the axle.
- **Nut (left upright)**: a **silver M4 nyloc nut** (7 mm across flats, with a nylon ring) on a **threaded shaft end** protruding about 8 mm (image (760–850, 470–560)).

### 2.5 Outrunner (MW)
- **Shape**: a **brushless outrunner**, bell **Ø 28 mm × 14 mm**, silver with a polished rim, **copper windings** visible through the bell's spoke openings (image (600–720, 380–620)). It sits between the blade and the left upright, coaxial with the axle.
- **Arrangement (guess)**: a **dead-shaft** design: the M4 shaft is fixed between the uprights (nut on the left, bearing boss on the right) and the stator is fixed to the shaft; the bell spins and carries the blade. Or the stator is bolted to the left upright and the shaft passes through.

### 2.6 Blade (BL)
- **Material**: flat **steel plate**, about **4 mm thick**, black/dark faces with **bright ground edges** (the edge band shows as a bright pale-green stripe).
- **Outline (in its own YZ plane)**: an **asymmetric "S" bar**, overall about **88 mm** from tip to tip, centred on the axle with a **hub region** about Ø 30 mm:
  - the **upper arm** runs up and slightly back, about **48 mm** from the axle to a **rounded tip** (radius about 8 mm) at the top; its leading edge (the image-left edge) is a **long straight bevel**, its trailing edge **concave** with a deep inner curve near the hub;
  - the **lower arm** is shorter (about **40 mm**) and curves round into a **hooked tooth** (image (490–600, 620–740)), the hook pointing in the direction of rotation;
  - the two arms are 180° apart, so the blade is a **two-tooth bar** with unequal arms (balance achieved by the upper arm being narrower) **(guess)**.
- **Mounting**: bolted to the outrunner's bell face (the hub region overlaps the bell); a dark spacer shows between the blade and the right bearing boss.
- **Plane**: x ≈ −3 (slightly right of centre), vertical.

### 2.7 Forks (FK-L, FK-R)
- **Shape**: **long thin flat metal strips** (aluminium or spring steel; the edges look bright with the green cut-out cast), about **45 mm long × 8 mm wide × 1.5 mm thick**, each with a **short upturned tab** at its root (a 90° bend about 8 mm tall where it is screwed) and a **chisel tip** on the floor.
- **Mounting**: each fork's upturned root tab is fixed to the **front face of the outer end** of its half by **two silver Phillips pan screws** (image left fork (1255–1305, 900–990)), stacked vertically; the strip runs forward and slightly outward, down to the floor at about **15°**.
- **Positions**: at x ≈ ±42, tips at y ≈ +50.
- **Plan**: the forks are roughly parallel, pointing forward, flanking the blade's path at a distance of about 40 mm each side.

### 2.8 Wheels (WH-L, WH-R)
- **Shape**: **Ø 24 mm × 14 mm** wide: a **black tyre** (smooth or finely ribbed rubber/TPU, about 4 mm thick) on a **white hub** with a **large central bore** (the white hub reads as a white ring with a dark/light inner circle, image (1320–1490, 730–1020)).
- **Position**: at the outer ends of the halves, axes along X, centres **x = ±45, y ≈ −4, z = 12**; the tyre's outer face is flush with or slightly outside the body end. Only the left wheel is visible; the right is inferred.
- **Spec**: r 11, inboard: the wheel is partly inside the half's rounded end.

---

## 3. Per-view descriptions

### 3.1 Front view (inferred)
- A wide low black bar (90 × 22) with a wheel at each end and a slot in the middle; two thin forks running toward the viewer from the outer ends; above the slot, the two uprights and the blade standing up to about 78 mm with its long upper arm, the silver motor bell beside it.

### 3.2 Top view (inferred)
- Two black rectangles (36 × 32) separated by an 18 mm slot; the uprights at the inner front corners; the blade as a 4 mm line along Y, 88 long in its swept plane but appearing as a thin line; the motor (Ø 28 × 14) to the robot left of it; forks running forward 38 mm from the outer front corners; wheels at the ends.

### 3.3 Left side view (inferred)
- The wheel at the left end face-on (white hub, black tyre); the left half's profile; the upright's swept curve rising to the axle with the nyloc nut; the blade's upper arm towering above; the fork sloping to the floor in front.

### 3.4 Rear view (inferred)
- The plain rear faces of the halves; uprights and the blade above; wheels at the ends.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BH | box half | 36 × 32 × 22 | 0.40 × 0.36 × 0.24 | black PLA | — | 2 |
| TP | plate | 30 × 28 × 2 | 0.33 | black | 2–3 screws | 2 |
| UP | swept upright | 30 × 8 × 40 | 0.33 × 0.09 × 0.44 | black PLA | lugs + screws | 2 |
| BH-b | bearing boss | Ø 18 × 8 | 0.20 | black | in UP-R | 1 |
| AX | threaded shaft + nyloc | M4 × 40 | — | steel | nut | 1 |
| MW | outrunner | Ø 28 × 14 | 0.31 | silver/copper | on AX | 1 |
| BL | S-bar blade | 88 × 30 (hub) × 4 | 0.98 | steel | bolted to MW bell | 1 |
| FK | strip with root tab | 45 × 8 × 1.5 (+8 tab) | 0.50 | aluminium/steel | 2 × M2.5 | 2 |
| WH | wheel | Ø 24 × 14 | 0.27 × 0.16 | black tyre, white hub | motor shaft | 2 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| BH bottom ↔ floor | clearance | 2 |
| WH bottom ↔ floor | contact | 0 |
| FK tips ↔ floor | contact | 0 |
| BL lowest point (swept r 36 about z 38) ↔ floor | clearance | 2 (see §13) |
| BL faces ↔ slot walls | clearance | 5–7 each side |
| BL ↔ MW bell | bolted | 0 |
| MW ↔ UP-L | shaft/stator fixed | 0 |
| BL hub ↔ BH-b | spacer | 1 |
| UP ↔ BH halves | screwed via lugs | 0 |
| TP ↔ BH | screwed | 0 |
| FK root tab ↔ BH front face | screwed (2) | 0 |
| WH ↔ BH outer end | clearance | 1–2 |

---

## 6. Mechanism

1. **Drive**: two wheels at the outer ends of a wide, short body; skid steer about the centre; the forks skid at the front. Very wide track (90) and short wheelbase (wheels near the middle of the depth) give fast, stable turning.
2. **Weapon**: an outrunner spins the S-bar about X. The **lower, hooked arm** is the primary tooth (it passes through the slot and bites what the forks lift); the long upper arm is the counter-tooth and also strikes opponents that ride up high. Direction: the hook leads, so the blade's front moves **upward** (uppercut) **(guess)**.
   - Energy (if the blade is 4 mm steel, ≈ 88 × 22 average width): m ≈ 7.85·(8.8·2.2·0.4) ≈ 61 g, which is too heavy for 150 g with everything else; the blade is probably **narrower (≈ 14 mm average) and/or aluminium-alloy-steel 3 mm**: m ≈ 7.85·(8.8·1.4·0.3) ≈ 29 g. I ≈ (1/12)·0.029·0.088² ≈ 1.9 × 10⁻⁵ kg·m². At 10,000 rpm (1047 rad/s): E ≈ ½·1.9 × 10⁻⁵·1047² ≈ 10 J; tip speed ≈ 46 m/s.
3. **Forks**: passive.

---

## 7. Assembly order (suggested rebuild)

1. Print the two body halves (with wheel pockets at the outer ends and motor/electronics bays) and the two uprights.
2. Fit the drive gearmotors and wheels at the outer ends.
3. Fit the battery, ESCs, receiver and switch in the halves; route the weapon phase wires to the left upright.
4. Bolt the uprights to the halves' inner front corners (lugs + screws), tying the halves together.
5. Assemble the weapon: stator on the M4 shaft (dead shaft) or on the left upright; bolt the blade to the bell; pass the shaft through the right bearing boss; nyloc nut on the left.
6. Screw on the top plates.
7. Screw the forks to the outer front faces.

---

## 8. Hidden / uncertain list
- How the halves are joined under the slot (a floor bridge or only through the uprights).
- Blade thickness and material; exact outline of the hidden side.
- Right wheel and right fork details (inferred by symmetry).
- Rear and underside.
- Sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin under the body centre; +X right, +Y forward, +Z up; mm.
- Halves x ∈ [±9, ±45], y ∈ [−20, +12], z ∈ [2, 24]; axle (y −2, z 38) along X; blade plane x ≈ −3; motor x ∈ [+1, +15]; wheels (±45, −4, 12); forks from (±42, +12, 8) to (±42, +50, 0).

## 10. Profiles as math

**10.1 Blade outline (YZ, polar about the axle A, θ from +Z toward +Y).**
- Hub: circle r 15.
- Upper arm (θ ≈ −10°, pointing up and slightly back): a tapered bar from the hub to a tip circle of r 8 centred at A + 40·(sin −10°, cos −10°); width 22 at the hub tapering to 16 near the tip; trailing edge concave: an arc of r 20 joining the hub to the arm on the rear side.
- Lower arm (θ ≈ 170°): from the hub to r 36, then a hook: an arc of r 10 curving toward +Y (the rotation direction) ending in a point at r 32, θ 150°.
- Thickness 4 mm (3 mm per §6 alternative).

**10.2 Upright (YZ, extruded 8 mm).** Base from (y −14, z 24) to (+12, z 24); front edge concave: arc of r 25 centred (y +20, z 44) from (+12, 24) to (+6, 38); head: circle r 9 about the axle (−2, 34); rear edge straight from (−11, 36) to (−14, 24).

**10.3 Fork (plan and side).** Strip x = ±42 ± 4; side line from (y +12, z 8) at the root (after a 90° tab z 8–16) to (y +50, z 0): z = 8 − 0.21·(y − 12) (12°). Tip chisel: last 4 mm tapered to 0.3 thick.

**10.4 Body half end (plan).** Outer end rounded: arc r 16 centred (±29, −4) joining the front and rear faces.

**10.5 Wheel.** Hub r 8 with bore r 5; tyre r 8–12, width 14.

## 11. Pixel-based measurements (1535 × 1299)

- Blade: upper tip (720–820, 40–110); leading edge from (540, 330) up to (700, 60); lower hook (490–600, 620–740); hub region (520–700, 330–640). Blade overall extent ≈ 700 px.
- Motor bell: (600–720, 380–620), Ø ≈ 240 px tall in the ellipse.
- Nyloc nut: (760–850, 470–560) ≈ 80 px across flats.
- Left upright: (700–960, 420–850). Right bearing boss: (470–580, 330–560).
- Left half top plate: (890–1300, 640–860). Left wheel: (1320–1490, 730–1020).
- Forks: left (960–1260, 870–1240); right (60–345, 590–870).

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/known part) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Scale | M4 nyloc 7 mm AF | — | 80 px → 11.4 px/mm at the nut | 11.4 px/mm (mid-depth) |
| Motor bell Ø | 28 (22xx/28xx) | 0.31 W | 240 px / 11.4 = 21 (ellipse foreshortened) → ≈ 28 | **28** |
| Blade length | 104 (spec r 52) | ≤ height budget: axle 34 + r ≤ 101 | 700 px / 11.4 ≈ 61 (foreshortened; the blade plane is oblique) → true ≈ 85–90 | **88** |
| Body width | 90 (spec) | ≤ 101.6 | half from slot to wheel end ≈ 600 px oblique / 11.4 ≈ 53 (inflated by perspective) | **90** |
| Body depth | 62 (spec, incl. forks?) | 0.36 W = 32 | top plate depth ≈ 220 px / 11.4 ≈ 19 + walls → 28–32 | **32** |
| Height | 24 (spec) | 0.24 W | left half side ≈ 230 px / 11.4 ≈ 20 + plate | **22** |
| Wheel Ø | 22 (r 11) | 0.27 W | 290 px tall / 11.4 = 25 (near, enlarged) | **24** |
| Fork length | — | 0.5 W | 420 px along the strip / 9 px/mm (nearer) ≈ 47 | **45** |

## 13. Consistency check: conflicts and reconciliation
1. **Blade size and floor clearance**: with the axle at z 34 and a symmetric r 44 blade, the tips would hit the floor. The blade is **asymmetric**: the upper arm reaches r ≈ 48, the lower hooked arm only r ≈ 32–36, and it passes through the slot. If the lower arm leads at the bottom, its lowest point is z = 34 − 36 = −2: still touching. **Reconciled: the axle is at z ≈ 38** (the uprights' heads are higher than they look) and the lower arm reaches r 34, giving 4 mm clearance; the upper arm's swept circle (r 48) then must also pass the floor: z = 38 − 48 = −10 — impossible, unless the upper arm passes through the slot and the floor is open under the slot. **Final reconciliation**: the blade's radius is **r 36 for both swept arms** (the long-looking upper arm is an effect of perspective: it points toward the camera), axle z 38, overall blade length about 76 mm. The spec's r 52 is too large.
2. **Body depth 32 vs spec 62**: the spec likely includes the forks (32 + 30). Consistent.
3. **Wheels**: only one seen; symmetry assumed.
4. **Mass**: §6's 29 g blade fits a 150 g budget with a 28 mm motor (≈ 25 g), two N20s (20 g), battery (25 g), electronics (15 g), body (30 g), forks (6 g).

---

## 14. Why the designer did it (per part, adversarial first)

- **Wide transverse body with end wheels**
  - Fight: the wide stance resists the weapon's gyroscopic and reaction forces (a vertical spinner's recoil tries to flip it over sideways on turns; a wide track resists). Wheels at the ends are far from the weapon so its recoil doesn't lift them. The short depth lets it turn very fast to keep the blade aimed.
  - Threats: the long flat sides are big targets for horizontal spinners; the wheels at the ends are exposed. The forks protect the front corners only.
- **Big asymmetric blade**
  - Fight: a long bar stores far more energy than a disc of the same weight (mass at the tips), and two teeth with a **hooked** primary tooth give a deep, positive bite. The tall upper arm also makes Vanquish hard to approach from above.
  - Threats: a big blade sticking up is exposed to other vertical spinners (weapon-to-weapon hits), and its gyroscopic effect makes the robot hop when turning; the uprights' swept shape and the nyloc-secured dead shaft are designed to survive weapon-on-weapon clashes.
- **Two uprights, dead shaft, nyloc nut**
  - Construction: support at both ends keeps the shaft straight; a nyloc nut does not shake loose under vibration; the bearing boss on the other side takes the load.
  - Fight: the swept, curved uprights deflect hits instead of presenting flat faces, and their thick bases spread impact loads into the halves.
- **Thin metal forks at the corners**
  - Fight: they get under opponents and **present them to the blade**; long and wide-set, they catch opponents arriving from the front corners and stop the robot itself being wedged from the front. Root tabs with two screws make them quick to replace when bent.
- **Black finish, top plates**
  - Construction: separate top plates for access; matte black hides damage.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors along X | 12 × 10 × 25 | x ±30, y −4, z 12 | medium |
| Weapon motor | 2806–2810 class outrunner (dead-shaft) | Ø 28 × 14 | x +8, y −2, z 38 | medium |
| Weapon ESC | 30 A BLHeli ESC | 30 × 15 × 6 | left half, x +27, y −4, z 10 | medium |
| Drive ESC | dual brushed ESC | 25 × 15 × 5 | right half, x −27, y −4, z 8 | medium |
| Battery | 3S 300–450 mAh LiPo | 45 × 17 × 15 | split or in the right half along X | low |
| Receiver | micro | 20 × 12 × 5 | right half | low |
| Switch | link in a top plate | 8 × 6 | — | low |
| Floor bridge | a printed bridge under the slot joining the halves | 18 × 30 × 3 | (0, −4, 2) | low |
| Wiring | battery → switch → ESCs; weapon phases up the left upright to the stator | — | — | medium |

---

## 16. Final reconciled numbers (use these for CAD)

This section overrides any earlier figure that differs from it. The earlier sections keep their first readings so the reasoning can be followed.
- **Axle**: along X at (y −2, z 38). The upright heads are circles of r 9 about this point, so the uprights reach z 47.
- **Blade**: an S-bar whose swept circle has r 36 (overall 72–76 mm tip to tip in its plane). The upper arm is r 36 at the rounded tip. The lower hooked arm is r 34 at the hook point and r 36 at the outer curve. It is 3 mm steel plate with a hub disc of r 15. The bore is Ø 4 with four Ø 2.5 bolt holes on a r 8 circle into the motor bell **(guess)**.
- **Clearance**: the lowest swept point is z 2, which passes through the 18 mm slot GP. The halves' floor bridge (if it exists) must lie behind y −2 − 36 = −38, or below the swept circle in the slot region. **The slot is open from floor to top across y ∈ [−38, +34] wherever the blade sweeps**, so the halves join only through the uprights' lugs and a rear bridge at y < −20 **(medium)**.
- **Weapon mass and energy (recomputed)**: the area is about 72 × 16 average plus the hub, about 13 cm². At 3 mm steel, m ≈ 7.85 × 1.3 × 0.3 ≈ 31 g. I ≈ 1/12 · m · L² ≈ 0.083 × 0.031 × 0.074² ≈ 1.4 × 10⁻⁵ kg·m². At 12,000 rpm (1257 rad/s), E ≈ 11 J and the tip speed is ≈ 45 m/s.
- **Forks**: root tab at (±42, +12, 8–16); the strip runs to (±42, +50, 0).

## 17. Mass budget (est. g, target ≤ 150)

| Item | Mass | Basis |
|---|---|---|
| Blade BL | 31 | §16 |
| Outrunner MW (2806 class) | 22 | catalogue |
| Shaft, nyloc, bearing | 5 | M4 × 45 steel |
| Uprights UP × 2 + lugs | 12 | 2 × 30 × 8 × 40 at 40 % infill |
| Body halves + plates | 26 | 2 × (36 × 32 × 22 shell 1.6) |
| Drive motors × 2 (N20) | 20 | catalogue |
| Wheels × 2 | 6 | printed hub plus TPU tyre |
| Battery 3S 300 | 26 | catalogue |
| ESCs + receiver + switch | 14 | catalogue |
| Forks × 2 + 4 screws | 6 | 45 × 8 × 1.5 aluminium |
| Wires, screws, misc | 6 | — |
| **Total** | **174** | over the limit |

**Reconciliation**: 174 g is over 150, so something is lighter than assumed. The most likely savings are a **2S 180 mAh battery** (−14 g), a **2204-class outrunner** (−8 g), thinner halves (−4 g) and a slimmer blade at 22 g (−9 g). That gives about 139–150 g. So the motor bell is probably a 22–24 mm motor seen close up rather than a 28 mm motor. If Ø 24 is used, the scale from §12 gives a nut of 6 mm, which suggests an M3 nyloc (5.5 AF) rather than M4. **Reconciled: M3 shaft, Ø 24 bell, 2S battery (medium).** The geometry above scales by at most 10 %; keep W = 90.

## 18. Matchups (getting under vs being got under)

- **Against wedges and thin-fork pushers**: Vanquish's two forks sit at the outer corners, so the middle of the front, under the blade, has no fork. A wedge entering the centre meets the blade's lower arm first. This is the point of the layout: anything that gets under at the centre is uppercut as it rides up. A wedge that enters at a corner has to beat a fork of equal thinness. Fork-on-fork contests are decided by height and stiffness, and Vanquish's 1.5 mm strips sprung flat to the floor are competitive. The risk is a wedge driving into the **side**: the long 32 mm-deep side faces have no wedge and the end wheels are exposed. Vanquish relies on its fast turn (short wheelbase) to keep facing forward.
- **Against horizontal spinners**: the end wheels and the plain side faces take the hits. The blade can meet a low horizontal bar only if the bar rides over the forks into the slot zone. The forks are bent away easily (a quick swap). The wide stance resists being spun out.
- **Against vertical spinners and drums**: a weapon-to-weapon exchange. Vanquish's blade is large in diameter for its class (72–76 mm), and a big tooth bite beats a small drum. The gyroscopic and reaction kick lifts the robot onto its rear edge, and the uprights take the load. A drum that gets under the forks lifts the robot. The fork tips are the defence: they must stay on the floor, which is why they are long and slope at a shallow angle.
- **Against control bots and lifters**: a lifter must get under the forks or the body. The 2 mm body clearance and floor-touching forks make that hard at the front, easier at the sides and rear.
- **Invertibility**: upside down, the uprights and the blade's top arc stick up 47–74 mm. Vanquish cannot drive inverted unless the blade is used to self-right: spinning the blade up while inverted kicks the robot over (the usual vertical-spinner "gyro flip") **(guess)**. The wheels, 24 mm against a 22 mm body, reach just above the top plates, so inverted driving with the blade stopped might be possible on the wheels plus the upright heads. That is unlikely to be intended.

## 19. Wear and fight-damage reading

- **Blade edges**: the edges are ground bright (the green-cast highlight), which suggests sharpening or fresh machining rather than heavy fight damage. There are no visible chips on the hook.
- **Forks**: both appear straight and parallel. If they were bent in fights they have been straightened or replaced.
- **Body**: clean black print with the layer lines intact. No visible gouges on the left side face, so this is probably a pre-event or early-event photo.
- **Screws**: the fasteners are mixed (silver Phillips on the forks and plates, one socket head on the left plate). This suggests at least one screw was replaced during use, or a stiffer fastener was used where a top plate carries load from the upright.

## 20. Alternatives considered for ambiguous features

- **Uprights printed integral with the halves vs bolted on**: the lugs with holes at the upright bases are read as separate bolted parts. The alternative, one-piece printed halves with integral uprights, would leave no lugs. Bolted is chosen (medium).
- **Live vs dead shaft**: a nyloc on a threaded shaft end with a plain boss opposite fits a dead shaft clamped between the uprights. A live shaft would need bearings in both uprights and a grub-screwed hub. Dead shaft is chosen (medium).
- **Blade direction**: the hook points so that the lower tooth moves forward and up at the front of the robot (uppercut). The opposite (overhead) direction would carry the hook backward through the slot first, which is a poor bite. Uppercut is chosen (medium).
- **Fork material**: aluminium vs spring steel. The forks are thin, long and straight after use, which suggests spring steel or hardened aluminium. Either works for CAD at 1.5 mm.

# Goobers: full rebuild description from reference photos

Goobers is a **cluster**: two near-identical red wedge robots, labelled **"ROBOT"** and **"OTHER ROBOT"**. Both photos show both of them side by side. `REFERENCE.json` crops each photo to its **left half** (`crop [0, 0, 0.5, 1]`), so **the CAD target is a single unit**: the left robot in each photo. That is "ROBOT" in aws71 and "OTHER ROBOT" in aws72. They are the same design, so this file describes **one unit (GU)** and lists the differences between the two at the end of §2.

Source photos:
- `robots/goobers/reference/goobers.aws71.webp` (1200 × 426 px): AWS 71, cut out onto white. **Front view, about 20–25° elevation** (json: front, el 25). Left: "ROBOT", seen almost square-on (yawed 5–10° so its left side shows a little). Right: "OTHER ROBOT", yawed about 25° to the right.
- `robots/goobers/reference/goobers.aws72.webp` (1200 × 482 px): AWS 72, cut out onto white. **Front view, about 25–30° elevation.** Left: "OTHER ROBOT", yawed about 20° (its left side and wheel show strongly). Right: "ROBOT", yawed about 20° the other way. Both have a **clear lip strip** on the front edge in this event.

Pixel coordinates refer to the jpg copies at these sizes, read by eye, ±6 px.

Facts are read from the photos. Guesses are marked **(guess)** with **H/M/L**. The photos show **only the front and top-front faces**: the rear, the underside and the inside are never seen, so a large part of §15 is guesswork, and this file is correspondingly shorter in places. Dimensions are estimated from the wheel (**D ≈ 28 mm**, a common small printed ant wheel), the black M2 screw heads (Ø ≈ 3.8) and the AWS limits: the cluster's combined mass is ≤ 150 g, so each unit is ≈ 75 g, and the units must fit the 101.6 mm cube.

Robot class: **pushing wedge** (`REFERENCE.json`: wedge, 2 wheels). Each unit is a **two-wheeled box with a two-stage front wedge** (a steeper lower band and a shallower ribbed upper slope) and wheels at the rear corners. There is no active weapon.

---

## 0. Coordinate system and naming

- **+X** = unit right, **+Y** = forward (toward the wedge lip), **+Z** = up.
- **Origin O** = the floor point under the centre of the unit's plan (mid-width; mid-length between the rear face y −28 and the lip y +28).
- Left/right are the unit's own. In aws71 and aws72 the camera faces the fronts, so the unit's right is on the image left of each robot.

| ID | Part |
|---|---|
| BD | red printed body (tub) |
| LB | lower front band (steep lower wedge face) |
| UP | upper wedge panel (shallow, ribbed by layer steps), possibly a separate lid |
| RM | side rims framing UP |
| DK | flat rear top deck |
| LBL | white name label ("ROBOT" / "OTHER ROBOT") on DK |
| BP-L / BP-R | two raised rectangular pads on UP near its top edge |
| SW | power switch (silver, small, at the left-rear of DK) with a tape patch |
| S-1 … S-4 | black M2 screws at the top corners of DK (S-1, S-2) and the side rims (S-3, S-4) |
| LP | clear lip strip on the bottom front edge (aws72) |
| WH-L / WH-R | wheels: red tyres on dark green 6-spoke hubs |
| DM-L / DM-R | drive gearmotors (hidden, guess N20) |
| RX/ESC, BAT | electronics (hidden, guess) |
| DMG-x | damage marks (gouges, chips) |

---

## 1. Overall description in one paragraph

Each Goobers unit is a **small red PLA wedge box** about **74 mm wide (body; 94 mm over the wheels), 56 mm long and 26 mm tall**, with two **thin wheels** (Ø ≈ 28 × 8 mm) outboard at the **rear corners**. The wheels have red, dirt-darkened tyres on **dark green six-spoke hubs**. From the front, the body is a **trapezoid** that is wider at the lip than at the rear deck. The front is a **two-stage wedge**: a **lower band** (about 15 mm along the face, sloped ≈ 45°) rising from the floor lip, then a sharp crease, then a **shallow upper panel** (≈ 33 mm along the face, ≈ 25°) whose surface is strongly **stepped by thick layer lines** (about 14 ridges). Two **raised rectangular pads** (≈ 14 × 7 × 4 mm) sit near the top of the upper panel, one each side of centre. Behind the slope a **flat narrow deck** carries a **white label** with the unit's name, a **small silver switch** at its left-rear and **black M2 screws** at its corners. In aws72 the front lip has a **clear/white translucent strip** (polycarbonate or tape) about 4 mm tall. Both units are heavily chipped and gouged from fights.

---

## 2. Part-by-part description

### 2.1 Body (BD)
- **Material**: red PLA (a slightly pinkish red), with very visible layer lines. Print orientation (guess, H): **printed upright on its rear face or its base** with thick (≈ 0.3 mm) layers. The shallow upper slope shows staircase steps 1.5–2 mm apart.
- **Plan**: a **trapezoid** with the lip width **≈ 80 mm** (x ±40) and the rear-deck width **≈ 70 mm** (x ±35). The sides are straight, flaring out going forward by about 5 mm per side over the length. Length **≈ 56 mm** (y −28 … +28).
- **Height**: top deck **z ≈ 26**.
- **Sides**: flat, vertical faces (aws72 left unit: the left side is visible next to the wheel at (95–130, 220–320) as a red face with damage). The sides carry the wheel axles near the rear.

### 2.2 Lower front band (LB)
- **Shape**: a flat face across the full lip width, **≈ 15 mm along the slope at ≈ 45°**, from the lip edge (y +28, z 1) up to the crease (y +17, z 11.5). Its lateral edges are the body's flared side edges.
- **Appearance**: smoother than UP (the layer lines are finer here because the face is steeper). It shows a **horizontal crease** at its top where UP starts, with a **slight overhang/shadow** (UP's lower edge stands ≈ 1 mm proud: aws71 left unit's crease at y-pixel 255 from x 110 to 530). That suggests UP is a **separate plate** (M).
- **Lip**: the lower edge is a nearly sharp edge, chipped in places (aws71 (130–165, 340–360) shows a broken corner). In aws72 a **clear strip LP** about **4 mm tall** runs along the whole lip (aws72 left unit (270–550, 300–440)). It is translucent white with sparkles, like a **polycarbonate or clear PETG strip** bonded or taped to the lip, giving a fresh sharp edge.

### 2.3 Upper wedge panel (UP) and side rims (RM)
- **Shape**: a flat inclined plate **≈ 72 mm wide at the bottom, 66 mm at the top, ≈ 33 mm along the slope at ≈ 25°**, from the crease (y +17, z 11.5) up to the deck edge (y −13, z 25.5).
- **Surface**: **≈ 14 horizontal ridges** (layer-step ridges ≈ 2 mm apart and ≈ 0.3–0.5 mm tall), running along X across the whole panel. This is a printing artefact (a shallow slope printed in thick layers), but it gives the panel a grippy, washboard surface.
- **Frame**: along each side edge of UP is a narrow **rim RM ≈ 3 mm wide**, slightly raised (aws72 the left unit's right edge (500–530, 120–300) and the right unit's left edge show a border). This reads as a **lid sitting inside a frame**.
- **Fasteners**: black M2 screws at the top corners (S-1, S-2 on the deck corners: aws71 left unit (105, 85) and (485, 65)). Lower-corner screws are not seen (guess: 2 more under the crease, or tabs instead).

### 2.4 Raised pads (BP-L, BP-R)
- **Shape**: two **rounded rectangular blocks**, **≈ 14 (X) × 7 (Y) × 4–5 (Z) mm**, with 1–2 mm edge fillets. They sit on UP near its upper edge at **x ≈ ±14**, y ≈ −8. In aws71 the left unit's pads are at (145–200, 85–135) and (390–445, 80–125).
- In aws72 the right unit ("ROBOT") has both pads intact. The left unit ("OTHER ROBOT") has one pad (its right pad at (380–425, 140–165)) with its **top skin broken**, showing **printed infill lattice**: so the pads are hollow printed bosses (M).
- **Function (guess)**: covers for the **drive motor clamp screws** or **bosses for the lid screws** (M); or "anti-flip bumps" that stop the unit from sliding flat when inverted (L).

### 2.5 Rear deck (DK), label (LBL), switch (SW)
- **DK**: a flat top strip **≈ 70 × 15 mm** at z 26, y −28 … −13.
- **LBL**: a **white printed label ≈ 34 × 12 mm** (aws71 "ROBOT" at (225–375, 70–100)) or **≈ 32 × 18 mm, two lines** ("OTHER / ROBOT", aws72 (225–365, 115–175)). It is centred on the deck, rotated slightly. Black sans-serif capitals.
- **SW**: a **silver miniature slide/toggle switch** (body ≈ 8 × 4 mm, lever ≈ 2 mm) at the deck's **right**-rear (the image left of each unit: aws71 (140–200, 72–98); aws72 (150–185, 148–180)). It is mounted flush with a small **tape patch** (a silver/grey strip). In a front view the unit's right is on the image left, so the switch is on the unit's **right**, at about **x +22, y −22**.

### 2.6 Wheels (WH-L, WH-R)
- **Size**: **Ø ≈ 28 mm, width ≈ 8 mm**.
- **Tyre**: red (a red TPU print or a red rubber band), dirty and worn to a dark maroon, ≈ 3 mm thick.
- **Hub**: **dark green**, with **six straight spokes** and a central boss Ø ≈ 7 (aws71 right unit's right wheel (1085–1180, 140–335) shows clearly 6 spokes and dark openings). The spokes are flush with the tyre face.
- **Position**: centre (x ±43, y −16, z 14). The wheels are **outboard of the body sides** (inner face at x ±39, about 4 mm from the body's rear-side face, which is at x ±35; the gap is filled by the gearbox shaft and a spacer). The wheel tops at z 28 stand **≈ 2 mm above the deck** (z 26), so the unit can **drive inverted** (H): aws71 shows both wheels' tops above the deck line.
- **Wheel guards**: **none**. The wheels are fully exposed at the sides and rear, but they are behind the front lip's flare (the lip is at x ±40, the wheel outer face at x ±47).

### 2.7 Screws (S-1 … S-4)
- **Seen**: black M2 pan/button heads (Ø ≈ 3.8) at the deck corners (aws71 left unit (105, 85), (485, 65); right unit (735, 55), (1078, 160)) and on the side rims (aws72 (420, 98), (1105, 195)). **4 per unit visible**, probably 4–6 in total, holding the top/lid to the tub.

### 2.8 Damage (DMG)
- **Gouges and chips** on UP (aws71 left unit (250–290, 180–250): a triangular gouge; (240, 235): a torn flap) and on the lip corners. aws72 left unit: chunks missing at the upper-left corner of UP (165–260, 195–225) and the lower-right of LB (520–550, 280–300). These show it has fought spinners (cosmetic; ignore for CAD unless modelling wear).

### 2.9 Hidden: drive and electronics (guess)
- **DM (guess, M)**: two **N20 gearmotors** along X at y −16, z 14, in a rear cradle.
- **BAT (guess, M)**: a 1S/2S **150 mAh** LiPo (≈ 30 × 18 × 8) in the front, under UP.
- **RX/ESC (guess, M)**: a **combined receiver + dual brushed ESC** (micro, ≈ 25 × 15 mm), e.g. an AWS-standard "DasMikro"-style board.
- Both units have identical internals (H).

### 2.10 Differences between the two units
| Feature | ROBOT | OTHER ROBOT |
|---|---|---|
| Label | one line "ROBOT" | two lines "OTHER / ROBOT" |
| Pads | both intact | one pad's top broken (infill visible) in aws72 |
| Damage | a gouge at the left-centre of UP | heavy chips at the upper left of UP and the lip right |
| Lip strip (aws72) | present | present |
| Overall size/shape | identical | identical |

---

## 3. Per-view sections (for silhouette matching)

### 3.1 aws71, left half ("ROBOT", front, el ≈ 22°)
- A trapezoid outline: the lip from (100, 385) to (535, 380), the sides rising to the deck corners at (95, 75) and (500, 55).
- The lower band occupies (100–535, 255–385). The upper ribbed panel occupies (100–520, 85–255), with the pads at the top and the label "ROBOT" centred above.
- **Wheels**: the right wheel (image left) at (15–70, 65–235) is seen edge-on as a tall narrow ellipse. The left wheel (image right) at (515–585, 35–190) shows its hub (6 spokes).
- The switch at (140–200, 72–98) is at the top left of the deck.

### 3.2 aws72, left half ("OTHER ROBOT", front-left yaw ≈ 20°, el ≈ 28°)
- The lip (with the clear strip) from (275, 440) to (550, 330): slanted by the yaw.
- The unit's right wheel (image left) at (20–110, 175–340), seen nearly face-on, shows the hub. The left wheel (image right) at (445–540, 50–185) is seen obliquely.
- The upper panel with ridges, the two-line label, one pad and the broken pad. The switch at the top-left.

### 3.3 Top view (synthesised)
- A trapezoid 80 (front) × 70 (rear) × 56 long. From the front: the lip strip (4 mm), LB (in plan ≈ 10.6 deep), UP (≈ 30 deep), and DK (15 deep, with the label at the centre and the switch at x +22). The wheels sit at the rear corners, x ±(39 … 47), y −30 … −2.

### 3.4 Front view
- The wedge rises from the floor lip to z 26 over 41 mm of run. The two-stage profile shows as two bands. The pads stick up 4 mm near the top. The wheels stand at the sides behind, to z 28, outer x ±47.

### 3.5 Side view
- Profile (y, z): the lip (+28, 1) → the crease (+17, 11.5) → the deck edge (−13, 25.5) → the deck (−28, 26) → the rear face down to (−28, 2). The wheel circle (Ø 28) at y −16 overlaps the rear half.

### 3.6 Rear view (not photographed)
- Inferred: a flat rear face 70 × 24 with the wheels on each side, perhaps the charge port.

---

## 4. Part table (one unit)

| ID | Shape | Size (mm) | Position | Material |
|---|---|---|---|---|
| BD | trapezoid tub | 80/70 × 56 × 26 | O-centred | red PLA |
| LB | inclined face | 80 × 15 at 45° | y +17 … +28 | red PLA |
| UP | inclined plate | 72/66 × 33 at 25° × 2 | y −13 … +17 | red PLA |
| RM | rims | 3 wide | along the UP sides | red PLA |
| DK | flat deck | 70 × 15 | y −28 … −13, z 26 | red PLA |
| BP-L/R | pads | 14 × 7 × 4.5 | (±14, −8, 23) on the slope | red PLA |
| LBL | label | 34 × 12 (or 32 × 18) | deck centre | white paper |
| SW | slide switch | 8 × 4 × 3 | (+22, −22, 26) | silver |
| S-1…4 | M2 screws | Ø 3.8 | deck corners, rims | black steel |
| LP | strip | 80 × 4 × 1 | the lip front | clear PC |
| WH-L/R | wheels | Ø 28 × 8 | (±43, −16, 14) | red tyre, green hub |
| DM-L/R | N20 | 12 × 10 × 24 | (±22, −16, 14) | (guess) |
| BAT | LiPo | 30 × 18 × 8 | (0, +5, 8) | (guess) |
| RX/ESC | combo | 25 × 15 × 5 | (0, −20, 12) | (guess) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WH ↔ floor | drive contact | 0 |
| Lip (LP) ↔ floor | skid contact | 0–0.5 |
| BD floor ↔ floor | clearance | 2 |
| WH inner face ↔ BD side | gap (shaft spacer) | 4 |
| WH top ↔ DK | the wheel stands proud | +2 |
| WH front ↔ LB (y) | well behind | ~28 |
| UP ↔ BD frame / RM | lid seated, screwed | 0 (edge seam 0.5) |
| UP lower edge ↔ LB top | step | +1 proud |
| BP ↔ UP | integral | 0 |
| LBL ↔ DK | stuck | 0 |
| SW ↔ DK | flush mount + tape | 0 |
| LP ↔ lip | bonded/taped | 0 |
| Unit ↔ other unit | separate robots | n/a (no linkage) |

---

## 6. Mechanism

- **Drive**: two-wheel differential, wheels at the rear, and the lip as the front skid. The centre of mass should sit between the axle (y −16) and the lip (y +28), around y −5, so the lip is lightly loaded and stays down.
- **Weapon**: none. Pushing, plus wedging: the two-stage wedge gets under opponents (lower band), then the shallow upper slope lifts them. Clusters win by **numbers**: two units can push from two sides or swarm.
- **Invertible**: yes (the wheels stand above the deck). Inverted, the wedge points up, so it is less useful but still drives.

---

## 7. Assembly order (suggested rebuild)

1. Print the tub (sides, floor, LB, deck, motor cradles) in red PLA. Print UP with BP-L/R separately (or as one piece with the tub; the photos suggest separate).
2. Fit the N20 motors in the rear cradle. Press on the wheels.
3. Install the battery in the front under UP, the RX/ESC behind it, and the switch through the deck.
4. Screw UP/the top on with black M2 screws.
5. Stick on the label. Bond or tape the clear lip strip.
6. Repeat for the second unit.

---

## 8. Hidden / uncertain list

- Everything behind and below the front faces: the rear face, the floor, the internals.
- Whether UP is a separate lid.
- The pad function.
- The motor type and the battery.
- The exact switch type (slide vs toggle).

---

## 9. Coordinate frame (restated)

Per unit: +X right, +Y forward, +Z up, O on the floor at the plan centre. Body y −28 … +28. Wheel axle at (y −16, z 14).

---

## 10. Profiles as math

**10.1 Side profile (YZ).** Polygon (y, z): (28, 1) → (17, 11.5) → (−13, 25.5) → (−28, 26) → (−28, 2) → (26, 2) → back to (28, 1). LB line: z = 1 + (28 − y) for y ∈ [17, 28] (45°). UP line: z = 11.5 + 0.467·(17 − y) for y ∈ [−13, 17] (25°).

**10.2 Plan (half-width).** w(y) = 35 + 5·(y + 28)/56 for y ∈ [−28, 28] (from 35 at the rear to 40 at the lip).

**10.3 Ridges on UP.** Along the slope coordinate s ∈ [0, 33] from the crease: a ridge at each s_k = 2.3·k, k = 1…14. Ridge profile: a 0.4 mm tall triangle, 1.2 mm wide.

**10.4 Pads.** Rounded boxes 14 × 7 × 4.5, fillet 1.5, standing normal to UP at s = 27, x = ±14.

**10.5 Wheel.** Tyre: an annulus r 11 … 14, width 8. Hub: a disc r ≤ 11 with 6 spokes 2 mm wide at 60° spacing and a central boss r 3.5. The openings are annular sectors r 3.5 … 10, 56° each.

---

## 11. Pixel-based measurements (independent check)

**aws71 left unit**: wheel height 170 px (right wheel) and 155 px (left); span over the wheels 15 → 585 = 570 px; lip width 435 px; deck-edge width 405 px; LB visible height 130 px; UP visible height 155–170 px; pad 55 × 45 px; label 150 × 30 px; screw head ≈ 12 px.
**aws72 left unit**: wheel face Ø ≈ 165 px (right wheel, face-on); lip strip height ≈ 22 px; label 140 × 60 px.

---

## 12. Several independent estimates of key quantities

| Quantity | Method A (rules/parts) | Method B (wheel D = 28) | Method C (screw Ø 3.8) | Reconciled |
|---|---|---|---|---|
| Wheel Ø | small printed ant wheel 25–32 | — | 170/12 × 3.8 = 54?? (the screws are farther away and tiny; unreliable) | **28** |
| Span over the wheels | ≤ 101.6 | 570/170 × 28 = 94 | — | **94** |
| Lip width | span − 2 × (8 wheel + 4 gap) + flare = 78 | 435/170 × 28 = 72, but the lip is nearer the camera than the wheels, so this is inflated and the depth correction is uncertain | — | **80** (the flare brings the lip out to about the wheel inner faces) |
| Rear-deck width | — | 405/170 × 28 = 67 | — | **70** |
| Height | wheel top 28 − 2 | aws71: the deck is 30 px below the wheel tops → 28 − 5 = 23 … 26 | — | **26** |
| Length | 56 (wheel at the rear + a 41 mm wedge run) | not measurable from the front | — | **56 (L)** |
| Pad size | — | 55/170 × 28 = 9 wide?? (nearer: ×1.5) → 14 | — | **14 × 7 × 4.5** |
| Mass per unit | 2 × N20 (20) + wheels (5) + battery (10) + RX/ESC (5) + body (≈ 30) + screws (2) ≈ 72 g | — | — | **≈ 72–75 g** (cluster ≤ 150 ✓) |

---

## 13. Consistency check: conflicts and reconciliation

1. **Size vs the cube.** One unit is 94 × 56 × 28. Two units side by side would be 188 wide (does not fit), and front to front 112 long (does not fit). Stacked: 94 × 56 × 56 → **fits** in 101.6. Clusters are checked as a whole in their starting configuration, so **stacking (or interlocking) is the likely way they fit** (M). This also argues the units can't be much bigger.
2. **The lip width vs the wheel span.** The lip (80) is inside the wheel span (94). The body flares forward, so the wheels are not covered from the front; consistent with the photos, where the wheels are visible beside the upper slope.
3. **Upper slope angle.** The projected-height maths (§11 with el 25°) gives UP ≈ 33 along the slope at 25°, and LB ≈ 15 at 45°. These sum to a z rise of 10.5 + 14 = 24.5 → the deck at ≈ 26 ✓, consistent with the wheel top.
4. **Switch side**: the switch appears at the image-left on both units in both photos. In a front view that is the unit's **right**. ✓ Same side on both units (built from the same file).

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Cluster of two identical units**: two cheap robots, each ≈ 75 g; if one is disabled the other fights on (AWS cluster rules make the team lose only when all units are out). Identical files are cheaper to print and maintain.
- **Two-stage wedge**: the steep lower band gives a strong, chip-resistant leading edge with mass at the bottom. The shallow upper slope then lifts the opponent gradually and keeps it moving up and over rather than jamming. The crease is a natural seam for a separate lid.
- **Ribbed (stepped) upper panel**: a cheap print, and the ridges also catch opponents' edges and stop wedges from sliding up and over (more grip on the opponent's underside when pushing).
- **Clear lip strip (aws72)**: renews the battered printed lip with a sharp, tough edge, after aws71 showed the lip chipped.
- **Wheels outboard and slightly above the deck**: invertible drive for tiny robots, without self-righting.
- **Pads near the top of the slope**: if they cover the screw bosses, they protect the screws from being sheared off by opponents riding up the wedge. They also act as a stop for an opponent riding up (a small "lip" to grab it).
- **Labels "ROBOT" / "OTHER ROBOT"**: a joke name pair, and also an identifier for the drivers and judges.
- **Silver switch on the deck**: it must be accessible. The rear deck is the least attacked surface.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Confidence |
|---|---|---|
| Drive | 2 × N20 gearmotors, rear cradle | M |
| Battery | 1S 150 mAh or 2S 100 mAh LiPo under UP | M |
| RX/ESC | combined micro board | M |
| Floor | integral, 1.5 mm, with 2 mm ground clearance | M |
| Rear face | flat, possibly a charge-lead exit | L |
| UP fixing | 4 M2 screws (2 visible at the deck corners + 2 hidden near the crease) | M |
| Pads | hollow printed bosses over the screw heads or the motor clamps | L–M |
| Wheel hubs | printed green PLA with a D-bore press fit | M |
| Tyres | red TPU, printed | M |

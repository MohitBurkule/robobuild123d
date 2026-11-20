# Mini E: full rebuild description from reference photos

Source photos:
- `robots/mini_e/reference/mini_e.aws76.webp`: AWS 76, 1560 × 1042 px, cut out. **Front-right, about 30° up**, close. **Orange-red** wedge with heavy paint chipping showing bare aluminium; "MINI E" written in black on the bumper.
- `robots/mini_e/reference/mini_e.aws72.webp`: AWS 72, 1254 × 891 px, cut out. **Front-left, about 35° up**. **Fresh bright red** paint, same layout. The clearest view of the lid and the left side.
- `robots/mini_e/reference/mini_e.aws43.webp`: AWS 43, 717 × 531 px, an **old, watermarked (Photobucket) photo** of an earlier version: **front, high (about 50° up)**, orange bumper with **four** slotted screws and a small yellow "MINI E" label, the wedge's ends cut to **sharp points**, treaded tyres. The kit draft skipped it, but it confirms the layout.

Facts are read from these photos; inferences are marked **(guess)**. Dimensions are scaled from the 150 g / 101.6 mm cube limit and the project kit draft (`kit.json`: body 72 long × 100 wide × 22 tall; two inboard wheels r 14 × 10 at x ±36, y −12, in notches; an aluminium bumper 104 × 3 × 14 at y 37.5, z 15; a wedge skirt from (y 36, z 9) to (y 52, z 0.5) across x ±52). Ratios are against **W = body width ≈ 98 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the red wedge), **+Z** = up. mm.
- **Origin O** = the floor point under the centre of the black box footprint.

| ID | Part |
|---|---|
| BX | black printed box (tub) |
| RM | raised rim around the top (part of BX) |
| LD | black textured top lid (inset in the rim) |
| S-LD | 4 silver Phillips pan screws on the lid |
| WW-L, WW-R | rectangular wheel windows through the top |
| MB-L, MB-R | black blocks at the inner/rear end of each window (motor clamps, guess) |
| WH-L, WH-R | two inboard wheels (black rubber/foam tyres) |
| FW | front wedge: one bent painted aluminium plate |
| FW-V | vertical upper part (bumper) |
| FW-S | sloped lower part (skirt/plough) |
| TX | "MINI E" lettering |
| S-FW | slotted cheese-head screws through FW-V (2 in AWS 72/76, 4 in AWS 43) |
| S-SD | slotted screws on the side walls (2 per side) |
| M-L, M-R | drive gearmotors (hidden) |
| BAT, ESC, RX, SW | electronics (hidden, guess) |

---

## 1. Overall description in one paragraph

Mini E is a **very flat, wide, two-wheel wedge**: a **black printed box** about **98 mm wide, 70 mm long and 20 mm tall**, with a **rounded rear top edge**, closed by a **black, finely textured lid** set inside a raised rim and held by **four silver Phillips screws**. Two **inboard wheels** sit in **rectangular windows cut through the top** near each side, slightly behind mid-length, their black tyres just peeking above the lid so it can drive either way up. The whole front is a **single bent aluminium plate painted red/orange**: an upper **vertical bumper** across the box front, with **"MINI E"** written on it and **two slotted screws**, bending at its bottom into a **lower sloped skirt** that runs forward and down to the floor at about 35°, with its two ends **cut back at an angle**. The paint is heavily **chipped** in AWS 76, revealing bare aluminium. No weapon; it is a pusher/wedge.

---

## 2. Part-by-part description

### 2.1 Box (BX) and rim (RM)
- **Shape**: a rectangular tub, about **98 mm wide (x ±49) × 70 mm long (y −36 to +34) × 20 mm tall** (z 2 to 22), black FDM with fine layer lines on the sides.
- **Top edges**: the **rear top edge is rounded** with a large radius (about **10–12 mm**), so from the side the top curves down at the back (clearly seen at the rear-right in AWS 76 and the rear-left in AWS 72). The front top edge is square, hidden behind the bumper. The side top edges have small (≈ 2 mm) chamfers.
- **Rim RM**: a raised border about **3–4 mm wide** around the top, standing about **1 mm proud** of the lid, with **steps/notches** where it wraps round the wheel windows (the lid outline steps in and out around the windows).
- **Side walls**: plain black, about 20 mm tall, each with **two slotted cheese-head screws** (head Ø ≈ 5 mm, silver with a green tint in the photos): AWS 76 right side at native (1205, 640) (front, low) and (1490, 450) (rear, mid-height); AWS 72 left side at (65, 320) and (215, 535). These screws likely fix the **side flanges of the wedge plate** (front screw) and the **motor clamps or floor** (rear screw) **(guess)**.
- **Rear wall**: not visible; presumably plain **(guess)**.

### 2.2 Lid (LD) and screws (S-LD)
- **Shape**: a flat black plate about **1.5–2 mm thick**, about **70 mm wide × 62 mm long**, with **stepped notches** at its sides around the wheel windows. Its surface has a **fine woven/diamond texture** (printed on a textured bed).
- **Screws S-LD**: **four silver Phillips pan heads**, Ø ≈ 4 mm (M2), placed **at the corners of the wheel windows**: in AWS 72 at native (220, 180) (left-rear), (380, 405) (left-front), (700, 70) (right-rear), (950, 260) (right-front); in AWS 76 at (780, 105), (420, 230), (1310, 265), (1020, 455).

### 2.3 Wheel windows (WW) and motor blocks (MB)
- **WW**: a **rectangular opening** through the top on each side, about **30 mm long (Y) × 16 mm wide (X)**, at x ≈ ±(28…44), y ≈ −24 to +6. The tyre's top shows through it.
- **MB**: at the **rear end** of each window (AWS 76) or at the inner end (AWS 72), a **small black block** about **12 × 6 × 6 mm**, a little below the rim: a **motor clamp bridge** or the **end of the gearmotor** **(guess)**.

### 2.4 Wheels (WH-L, WH-R)
- **Shape**: black **rubber or dense foam tyres**, about **Ø 28 × 12 mm**, smooth and worn (AWS 72/76); the AWS 43 version had **block-tread tyres**. Hubs are hidden.
- **Position**: centres at about **(±36, −9, 13.5)**, fully inside the box footprint (inboard). Tyre tops at z ≈ **27**? — see section 12: the tyres show above the lid only slightly, so reconciled Ø 24 with centre z 12 and top z 24 (≈ 1.5 mm above the lid).
- **Fit**: tyre sides about 2 mm from the window walls; tyre ends about 2 mm from the window ends.

### 2.5 Front wedge (FW = FW-V + FW-S), lettering (TX), screws (S-FW)
- **Material**: **aluminium sheet about 1.5 mm thick**, **painted** red (AWS 72) / orange-red (AWS 76); in AWS 76 large irregular **chips** of paint are missing, showing silver metal underneath, especially on the skirt and bumper face.
- **FW-V (bumper)**: a **vertical band** across the full front of the box, about **100 mm wide × 12 mm tall** (z ≈ 10 to 22), screwed flat to the box front with **two slotted cheese-head screws** (Ø ≈ 5 mm) at about **x ≈ −22 and +22**, z ≈ 16 (AWS 72 at native (515, 515) and (965, 390)). AWS 43 shows **four** screws across.
- **TX**: "MINI E" in **black hand lettering** (marker, about 7 mm tall capitals), centred on FW-V between the screws. AWS 43 instead has a small **yellow printed label** "MINI E".
- **Bend**: at the bottom of FW-V (z ≈ 10) the plate bends **forward** by about **55°**.
- **FW-S (skirt)**: a sloped band about **100 mm wide** at its top edge, running forward and down at about **35°** for about **17 mm**, to a **leading edge on the floor** at about **y ≈ +48**. Its **two ends are cut back** so the skirt is narrower at the floor: each end edge runs from the bend at x ≈ ±50 inward to the floor edge at about x ≈ ±42 (a **trapezoid** in plan, about 84 mm wide at the floor). In AWS 43 the ends are cut more sharply and the skirt is **wider at the bend than the box** (the left end sticks out as a point).
- **Gap**: the skirt's underside to the box front lower corner: a small triangular void (the skirt passes in front of the box's lower front).

---

## 3. Per-view sections

### 3.1 AWS 76 (front-right)
- The chipped orange wedge along the bottom-left, "MINI E" on its upper band with two screws; the black box top with its textured lid, rim and four screws; the two wheel windows with tyres and black blocks; the rounded rear-right top edge; two slotted screws on the right side.

### 3.2 AWS 72 (front-left)
- The bright red wedge along the bottom-right; the lid with four screws; the left wheel window (front-left in the image) and right window (rear-right); the left side with two slotted screws.

### 3.3 AWS 43 (front, high, old version)
- The wide box with its textured lid and four screws; two treaded tyres in windows; an orange bumper with four slotted screws and a yellow "MINI E" label; the skirt with pointed ends.

### 3.4 Top view (plan, synthesised)
- A 98 × 70 black rectangle (rounded rear edge), the lid inset with four screws, two 30 × 16 windows with tyres near the sides slightly behind the middle; the red bumper line across the front and the trapezoidal red skirt (100 → 84 wide) reaching y +48.

### 3.5 Front view
- A 100 × 12 red band (bumper) over a 100 → 84 trapezoid skirt sloping to the floor; the black box behind (20 mm tall); tyres barely visible above the top.

### 3.6 Side view
- A low black rectangle 70 × 20 with a rounded rear-top corner, two screws, the tyre top peeking above the top in the window; in front, the red plate: a vertical bit (12 mm) then a 35° slope to the floor 14 mm ahead.

### 3.7 Rear and underside (not photographed)
- Rear: plain black wall with the rounded top edge; switch probably there or underneath. Underside: flat floor with two wheel slots **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BX | tub, rounded rear top | 98 × 70 × 20 | 1 × 0.71 × 0.20 | black FDM | — | 1 |
| LD | textured plate with notches | 70 × 62 × 2 | 0.71 × 0.63 | black FDM | 4 × M2 pan | 1 |
| WW | window | 30 × 16 | 0.31 × 0.16 | — | — | 2 |
| MB | block | 12 × 6 × 6 | — | black | in BX | 2 |
| WH | tyre | Ø 24–28 × 12 | 0.27 × 0.12 | black rubber/foam | motor shaft | 2 |
| FW-V | vertical band | 100 × 12 × 1.5 | 1.02 × 0.12 | painted aluminium | 2 slotted M3 (4 in AWS 43) | 1 |
| FW-S | sloped trapezoid | 100/84 × 17 × 1.5 | 1.02 | painted aluminium | bent from FW-V | 1 |
| S-SD | slotted cheese head | Ø 5 | — | steel | into BX sides | 4 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD ↔ BX rim | inset, screwed | 0 (lid 1 mm below the rim) |
| FW-V ↔ BX front | screwed flat | 0 |
| FW-V top ↔ BX top | level | 0 |
| FW-S leading edge ↔ floor | touching | 0 |
| FW-S underside ↔ BX lower front | small void | 2–4 |
| FW-V ends ↔ BX sides | flush / 1 mm proud | 0–1 |
| WH ↔ window walls | clearance | 2 |
| WH top ↔ LD | wheel above | +1 to +2 |
| WH bottom ↔ floor | touching | 0 |
| BX floor ↔ floor | above | 2 |
| MB ↔ WH | near | 2 |

---

## 6. Mechanism
1. **Drive**: two inboard wheels near mid-length; the wedge leading edge carries the front, the rear floor edge (or a skid) carries the back. Pivot-turns on the spot.
2. **Wedge**: the skirt's floor edge gets under; the 35° slope then the vertical bumper push the opponent. The bumper height (22) stops opponents climbing straight over.
3. **Inverted**: the tyres poke 1–2 mm above the lid through the windows, so it can drive upside down; the wedge then points up and is useless.

---

## 7. Assembly order (suggested rebuild)
1. Print the box (with motor pockets, wheel windows, rounded rear top edge) and the lid.
2. Fit two gearmotors (clamped by the black blocks) and the wheels through the windows.
3. Fit the battery, ESC/receiver and switch.
4. Screw the lid on (4 × M2).
5. Cut and bend the aluminium wedge (vertical band 12 mm, 55° bend, 17 mm skirt with angled ends), paint it, letter "MINI E".
6. Screw it to the box front (2 slotted screws) and through the side screws (guess).

---

## 8. Coordinate frame (restated)
- Origin O on the floor under the box centre; +X right, +Y forward, +Z up; mm.
- BX x ∈ [−49, 49], y ∈ [−36, 34], z ∈ [2, 22]. FW-V at y 34–35.5, z 10–22. FW-S from (y 35.5, z 10) to (y 48, z 0). Wheels (±36, −9, 12).

## 9. Profiles as math
- **Box side profile (YZ)**: bottom z = 2; front y = 34; top z = 22 for y ∈ [−24, 34]; rear-top arc centre (−24, 10), r 12, from θ = 90° to 180° (reaching (−36, 10)); rear wall y = −36 from z 10 down to 2.
- **Wedge (YZ, outer surface)**: vertical line y = 35.5 from z 22 to z 10; bend r 1.5; skirt line from (35.5, 10) to (48, 0.5): z = 10 − 0.76·(y − 35.5) (37°).
- **Skirt plan (XY at the floor)**: trapezoid with the top edge x ∈ [−50, 50] at y 35.5 and the floor edge x ∈ [−42, 42] at y 48; end edges are lines from (±50, 35.5) to (±42, 48).
- **Wheel**: circle r 12 centred (y −9, z 12), width 12.
- **Window**: rectangle x ∈ ±[28, 44], y ∈ [−24, 6], through the lid and box top.

## 10. Pixel-based measurements
- **AWS 72** (1254 × 891): bumper top edge (270, 560)–(1160, 330); skirt floor edge (205, 700)–(1200, 545) approximately; box rear edge (100, 215)–(850, 55); left window (130–300, 210–420); right window (750–960, 80–230); left side height ≈ 300 px at the front-left corner (40, 230)–(270, 640) diagonal.
- **AWS 76** (1560 × 1042): bumper top edge (180, 265)–(1100, 680); skirt floor edge (75, 470)–(1185, 975); windows (450–700, 90–260) and (1100–1350, 280–470); right side screws (1205, 640), (1490, 450).

## 11. Several independent estimates

| Quantity | Method A (kit / rules) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | kit 100 | ≈ 1.4 × length | AWS 72 bumper 950 px; box depth edge ≈ 690 px oblique → width/length ≈ 1.38 | **98** |
| Body length | kit 72 | 98 / 1.38 = 71 | — | **70** |
| Body height | kit 22 | ≈ 0.2 W | AWS 76 right side at the front ≈ 130 px vertical vs bumper width 1010 px (≈ 100 mm) → ≈ 13 px... at the near end ≈ 10 px/mm → 18–20 (vertical edge 1100,680 to 1100,? ) | **20** |
| Bumper band height | kit 14 | ≈ 0.6 × body height | AWS 72 band ≈ 75 px at ≈ 9 px/mm → 8; AWS 76 ≈ 110 px at 10 → 11 | **12** |
| Skirt depth (Y) | kit 16 | — | AWS 72 skirt ≈ 150 px slant at ≈ 9 px/mm, seen at 35° camera → 12–14 | **12.5** |
| Wheel Ø | kit 28 | window 30 long → tyre ≤ 26 | AWS 76 tyre ≈ 170 px tall incl. the part above the window at ≈ 7 px/mm → visible ≈ 24 | **24** |

## 12. Consistency check
1. **Wheel size vs body height**: a Ø 28 tyre centred low would stick out 6 mm above a 22 mm body, but the photos show only a sliver above the lid. **Reconciled Ø 24 at z 12 → top 24 vs lid 22–23: about 1–2 mm proud.**
2. **Overall length**: rear −36 to skirt edge +48 = 84 mm; width 100 (skirt top edge) — both fit the cube.
3. **Screws on the bumper**: 2 (AWS 72/76) vs 4 (AWS 43): different versions.
4. **Skirt end shape**: AWS 76/72 angled back to 84 at the floor; AWS 43 pointed ends sticking out wider. Use the AWS 72/76 shape.

---

## 13. Why the designer did it (per part, mostly adversarial)

- **Wide, very flat box with a rounded rear edge**
  - Fight: at 20 mm tall there is almost nothing for a vertical spinner or a wedge to bite, and a wide body (≈ 100 mm) is hard to flip sideways and pushes across a lot of arena. The **rounded rear edge** means an opponent attacking from behind meets a ramp rather than a corner, and a flipped Mini E rolls rather than catching.
  - Construction: one simple print; textured lid looks good and resists scuffing.
- **Inboard wheels in top windows**
  - Fight: the wheels are **fully inside the box footprint**, so side attacks cannot reach them; only a sliver of tyre shows above and below, enough to **drive inverted**. Placing the axle near mid-length lets it spin on the spot.
  - Weak point: anything dropping through the window (a spinner tooth from above) can hit the tyre.
- **Single bent aluminium wedge (bumper + skirt)**
  - Getting under vs contact: the **skirt edge** lies on the floor and gets under opponents; the **35° slope** lifts their edge; the **vertical bumper** takes the push. One continuous bent plate has no joints to fail; screwed to the box front it transfers push loads directly.
  - Against spinners: aluminium takes hits and dents rather than shattering; paint chips (AWS 76) show it has been hit hard and kept working. The **angled ends** stop the skirt corners snagging on walls and deflect side-on hits.
  - Construction: cut and bent by hand from sheet, painted for identity ("MINI E").
- **Slotted screws on the sides**
  - Construction: tie the wedge and internal parts to the box sides, spreading front impacts into the side walls.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors lying along X inside, shafts out to the wheels | 12 × 10 × 25 | (±18, −9, 12) | medium |
| Motor clamps | the black blocks MB + screws | 12 × 6 × 6 | ends of the windows | medium |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 10 | front-centre, (0, +18, 8) | medium |
| ESC + receiver | combined board | 30 × 18 × 5 | rear-centre, (0, −22, 8) | medium |
| Switch | slide switch on the rear wall or underside | 10 × 5 × 5 | (0, −36, 10) | low |
| Rear skid | printed skid or the box floor edge | — | rear floor | low |

## 15. What the photos cannot show
- The rear, underside and switch.
- The tyre hubs and motor layout.
- All mm values ±10–15%.

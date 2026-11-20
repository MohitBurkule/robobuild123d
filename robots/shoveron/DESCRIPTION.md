# Shoveron: full rebuild description from reference photos

Source photos (in `robots/shoveron/reference/`), both cut out onto white with a green backdrop fringe:
- `shoveron.aws71.webp` (1789 × 1340 px): **orange version**. A **three-quarter view from the front-left, about 40° above horizontal**. The front points to the image lower left. It shows two **orange pods**, a long **aluminium "shovel"** between them that rises from the floor at the front to a **black hinge/actuator** at the rear, and two **steel blade forks**.
- `shoveron.aws72.webp` (1003 × 861 px): **red version**, quite different. A **front view, about 40° above horizontal**. A **black central box** with an **aluminium lid** and a **slide switch**, four **black wheels**, and two **red outer pods** that run forward into **tape-wrapped steel blade forks**. **No shovel** is visible in this version.

Everything stated as fact is read from the photos. Anything inferred is marked **(guess)** with a confidence. Dimensions are **estimates in mm**, scaled from the AWS antweight limits (150 g, fits a 101.6 mm cube) and the photo proportions, and checked against the project spec draft (`spec.json`, which models the **AWS71 orange version**: two pods, a bridge, two wheels with axles and nuts, two forks with mounts and bolts, six screws and a `shovel`; robot type "lifter"). **W = overall width over the pods ≈ 96 mm** is the ratio base.

**Evidence limits**: two photos, two different builds; one view each. The rear, underside and right sides are not seen. This description is therefore shorter than the 4000-word target in places and relies on inference for hidden parts, which is marked.

Shoveron (AWS71) is a **lifter / shovel robot**: a long sheet-aluminium **shovel** pivoted at the rear between two orange pods, lying on the floor at the front, flanked by two **steel blade forks**. AWS72 is a **fork-and-box** rebuild with outer pods and four wheels.

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) under the centre of the robot (mid-width between the pods, mid-length of the pods; forks excluded).
- **+X** = robot's right, **+Y** = forward (toward the forks), **+Z** = up. Units mm.
- AWS71: camera at the **front-left**; the robot's **left pod** is at the image lower left, the **right pod** at the image right. AWS72: camera at the **front**; the robot's right is on the image left.

Part IDs (AWS71 unless noted):

| ID | Part |
|---|---|
| PD-L / PD-R | orange printed side pods |
| PB-L / PB-R | front blocks of the pods (carry the fork slots) |
| PH | oval lightening holes in the pods |
| PI-L / PI-R | white printed inner liners / motor carriers in the pods |
| BR | bridge joining the pods (hidden, spec) |
| SH | aluminium shovel (long curved sheet) |
| SH-E | crimped/serrated edges of the shovel |
| SA | black rear hinge / actuator block for the shovel |
| FK-L / FK-R | steel blade forks (AWS71) |
| WH-L / WH-R | large black rear wheels |
| FR-L / FR-R | small black front rollers / motor ends with copper windings |
| S-PD | black pod screws with washers |
| WR | black wires |
| — AWS72 — | |
| CB | black central box |
| AL | aluminium lid with 4 screws |
| SW | slide switch on the lid's left |
| BI | brass inserts / screw heads on the box front and rear |
| RP-L / RP-R | red outer pods (wheel guards) |
| RT | red tabs on the pods |
| RF-L / RF-R | steel blade forks with red tape |
| W4 | four black wheels |

---

## 1. Overall description in one paragraph

**AWS71**: Shoveron is a **low two-pod lifter** about **96 mm wide** and **≈ 95 mm long** (with forks). Each side is an **orange printed pod** about **30 mm wide**, sculpted with **curved recesses and large oval holes**, holding a **big black rear wheel (Ø ≈ 28)** at its rear and a **small black roller with exposed copper windings** (a coreless motor) at its front, with a **white printed liner** inside. Between the pods lies the **shovel**: a **≈ 36 mm wide strip of thin aluminium sheet**, its edges **crimped/serrated** from cutting, that **lies on the floor at the front**, rises in a **smooth convex curve** over the middle of the robot to **≈ 35 mm** high, and ends at the rear on a **black hinge/actuator block**. Ahead of each pod a **steel blade fork** (like a utility-knife blade, ≈ 10 mm wide) comes out of a **slot in the pod's front block** and slopes down to the floor. **Black wires** loop near the front of each pod. **AWS72**: a **black box chassis** (≈ 55 mm wide) with an **aluminium lid** held by 4 screws and a **slide switch**, four **black wheels** at its corners, and two **red curved outer pods** that guard the wheels and extend forward into **tape-wrapped steel forks**.

---

## 2. Part-by-part description (AWS71, orange version)

### 2.1 Side pods (PD-L, PD-R)
- **Overall**: each pod spans **x ∈ ±[18, 48]**, **y ∈ [−40, +38]**, **z ∈ [2, 30]**. Matt **orange** FDM with rough, stringy surfaces in places and visible layer lines.
- **Shape**: not a simple box. From the front:
  1. **Front block PB**: a **rectangular block ≈ 22 mm wide × 14 mm long × 18 mm tall**, at the front of the pod (AWS71 left pod px ≈ (150–440, 580–880); right pod px ≈ (830–1180, 820–1180)). Its **front face carries a vertical slot** (≈ 2 × 12 mm) for the fork, and a **split line** (the right pod's block shows a vertical seam at px (1130–1140, 1000–1180)), suggesting the block is **two halves clamping the fork** **(guess, medium)**.
  2. **Front well**: behind the block, an open pocket **≈ 18 × 18 mm** containing the **front roller FR** (left px (200–330, 500–620); right px (1100–1310, 800–1000)).
  3. **Mid section**: an **outer wall** that **curves inward** in plan (a concave "waist", AWS71 right pod px (1260–1600, 560–1050): the outer face sweeps in a large S-curve). The wall has **two big oval through-holes PH**, each ≈ **10 × 7 mm** (right pod px (1120–1190, 420–500), (1430–1500, 570–660), (1260–1330, 1050–1130), (1380–1440, 960–1040)). Its **top** carries **three small raised ribs** (a grip or a label, right pod px (1190–1300, 290–370)).
  4. **Rear well**: an open-topped pocket holding the **rear wheel WH** (left px (660–770, 110–260); right px (1490–1690, 320–510)), with the pod's outer wall **wrapping around the wheel's outside and rear** as a curved guard (right pod rear px (1500–1730, 410–700)).
- **Screws S-PD**: **black button screws with black washers**, one near the inner top edge at mid-length on each pod (left px (575, 350); right px (1405, 355)) and one near the inner front (right px (1215, 550)). **≈ 3–4 per pod**.

### 2.2 White inner liners (PI-L, PI-R)
- **White printed parts** visible along the **inner side** of each pod, between the pod and the shovel (right px (1150–1500, 300–800); left px (430–560, 360–640)). Each is an elongated **trough or motor carrier ≈ 10 mm wide × 50 mm long**, with a curved channel. **Interpretation**: the **motor and wire carriers** that clip into the orange pods, or the **shovel's side guides** **(guess, medium)**.

### 2.3 Rear wheels (WH-L, WH-R)
- **Black rubber or TPU tyres**, **Ø ≈ 28 × 12 mm**, smooth, with a dark hub. Positions: **(±42, −28, 14)**. Their tops (z ≈ 28) are **about level with the pod tops**. Only the tops and fronts are visible; the outer faces are partly **guarded** by the pods' curved rear walls.
- **Axle**: the spec has a **steel axle and nut** per wheel (`dt_axle_wheel`, `dt_nut_wheel`), i.e. the wheel runs on an axle through the pod **(guess, medium)**.

### 2.4 Front rollers / motors (FR-L, FR-R)
- In each front well: a **small black cylinder ≈ Ø 12 × 10 mm**, with a **white collar** and **exposed copper windings** (a reddish copper ring) next to it (right px (1130–1210, 830–990): black cylinder with white ring and copper; left px (240–300, 520–600)).
- **Interpretation (guess, low–medium)**: a **coreless micro motor** (the copper is its exposed rotor winding or a commutator) with a **rubber sleeve** on its shaft acting as a **small front drive roller** or as a **friction drive** pressing on a front wheel. With the big rear wheels (spec: two wheels only), the most consistent reading is that these are the **drive motors**, located at the front, driving the **rear wheels** through a **belt or long shaft** hidden in the white liners. A simpler alternative is that the front rollers are **small powered front wheels** (making it 4-wheel) **(low)**.

### 2.5 Shovel (SH)
- **Material**: **thin aluminium sheet**, ≈ **0.3–0.5 mm** thick (it is visibly flexible: the surface is wavy and dented), dull silver with dot-pattern marks (like an embossed or perforated sheet: rows of tiny dimples at px (800–960, 450–600)).
- **Edges SH-E**: both long edges are **crimped / serrated** (a fine zigzag), as if cut with **pinking shears** or folded over (px along (290–440, 100–1020) and (770–1170, 120–1000)). A fold-over hem would **stiffen** the edges **(guess)**.
- **Width**: **≈ 36 mm** (x ∈ [−18, +18]).
- **Side profile**: a **long convex curve**:
  1. **Front lip** on the floor at **y ≈ +45** (px (290–630, 950–1030): the lower end, slightly upturned at its very tip).
  2. **Rising section**: from the floor up and back at ≈ 30–40°, curving.
  3. **Crest**: at about **y ≈ −5, z ≈ 35** (px (800–1050, 150–260)).
  4. **Rear section**: flattens and runs back to the **black block SA** at **y ≈ −35, z ≈ 35** (px (850–1230, 40–220)), where its end is **folded or clamped**.
- **Length** (along the curve): **≈ 105 mm**.

### 2.6 Rear hinge / actuator (SA)
- A **black block** at the rear centre, about **24 × 12 × 14 mm**, with a **black lever** projecting from its right side (px (1010–1280, 40–230): a dark block with a short arm and a round pin end at (1265, 180)).
- **Interpretation (guess, medium)**: a **servo** (black case) whose **horn/arm** is attached to the rear end of the shovel; rotating the servo **lifts the rear** of the shovel or **rotates the whole shovel** about a rear pivot, raising its front lip. Since the shovel is a thin sheet, the more likely mode is that the servo **pulls the shovel's rear end up and back**, so the sheet's front lip **lifts** while the convex middle bends **(a flexible "shovel" lifter)**. The spec names the robot a **lifter**.

### 2.7 Forks (FK-L, FK-R)
- **Shape**: **flat steel blades ≈ 10 mm wide × 0.6 mm thick**, protruding **≈ 35 mm** from the pods' front blocks, with an **angled (knife) tip**: the end is cut at ≈ 30° (like a snapped utility-knife segment). Bright steel, scratched.
- **Position**: centred at **x ≈ ±32** (in front of each pod's block), from the slot at **(y +38, z 12)** sloping down at **≈ 20°** to the floor at **y ≈ +72**.
- **Mount**: through the slot, clamped in the split front block (spec: `dt_mount_fork` + `dt_bolt_fork`) **(guess, high)**.

### 2.8 Wires (WR)
- **Black thin wires** loop in the front wells and along the white liners (left px (380–460, 470–600); right px (960–1060, 740–820) and (1340–1380, 540–760)). They are the **motor leads**.

### 2.9 Bridge (BR), hidden
- The two pods must be joined; the spec has a `bridge`. It is hidden under the shovel, probably a **plate across the floor** from pod to pod under the shovel's middle and a **rear cross-member** carrying SA **(guess, high)**.

---

## 3. Part-by-part description (AWS72, red version)

- **CB black central box**: **≈ 55 mm wide × 60 mm long × 22 mm tall**, matt black print. Its front face (px (400–610, 380–560)) is recessed behind the pods' fronts.
- **AL aluminium lid**: a **rectangle ≈ 45 × 40 mm**, brushed aluminium (green-tinted in the photo), with **4 screws** at its corners (black button heads at px (265, 135), (665, 128), (270, 265), (710, 265)) and a **cut-out on its left** around the switch.
- **SW slide switch**: a **black miniature slide switch** in a slot at the **robot's right side** of the lid (image left, px (240–275, 165–220)), with two small screws.
- **BI brass**: two **brass screw heads / inserts** on the box's top front and rear edges (px (450, 78) and (495, 345)).
- **W4 wheels**: four **black smooth wheels, Ø ≈ 22 × 10 mm**, at the box's four corners (px (130–210, 55–175), (695–790, 65–175), (130–215, 300–410), (770–860, 300–410)).
- **RP red pods**: two **curved red printed shells** outside the wheels: each starts at the rear wheel with a **hooked rear guard** (px (60–200, 90–260)), runs along the side, and **sweeps forward and outward** into a **rounded front lobe** (px (40–400, 380–720)). The front lobes have **sloped tops** and **curved outer faces**; the inner faces are vertical and leave a **≈ 45 mm channel** in front of the box.
- **RT red tabs**: one small **rectangular tab** on top of each pod at its inner front corner (px (220–300, 370–460) and (670–810, 375–440)).
- **RF forks**: from the bottom front of each lobe, a **flat steel blade ≈ 14 mm wide** protrudes ≈ 15 mm, its root wrapped in **red tape** (px (125–275, 580–800) and (770–920, 600–810)).

---

## 4. Per-view sections

### 4.1 AWS71 (front-left, ≈ 40° above)
- **Silhouette**: a wide, low, three-lobed shape: the left pod (lower left), the central aluminium shovel arching up from the front lip to the rear, and the right pod (right); two blade forks stick out at the front.
- **Detail**: oval holes, pod screws, white liners, black wheels at the rear corners, front rollers with copper, black wires, the rear black block.

### 4.2 AWS72 (front, ≈ 40° above)
- **Silhouette**: a black box with an aluminium lid between two red curved pods, four black wheels, two taped blade forks at the bottom.

### 4.3 Top view (AWS71, synthesised)
- Two 30 × 78 pods at x ±[18, 48], each with a front block, front well, waisted middle and rear wheel well; the 36 mm shovel down the centre from y +45 to −35; forks ahead of the pods to y +72.

### 4.4 Side view (AWS71, synthesised)
- The pod profile (≈ 28 tall) with the rear wheel; the shovel's convex arc above the centreline, peaking at z 35 near the middle; the fork sloping to the floor ahead.

---

## 5. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| PD | sculpted pod | 30 × 78 × 28 | 0.31 × 0.81 | orange FDM | bridge + screws | 2 |
| PB | split front block | 22 × 14 × 18 | — | orange | integral / bolted | 2 |
| PH | oval hole | 10 × 7 | — | — | — | 2 per pod (each side) |
| PI | white liner | 10 × 50 × 15 | — | white FDM | clipped (guess) | 2 |
| SH | curved strip | 36 × 105 (developed) × 0.4 | 0.38 | aluminium | SA at the rear | 1 |
| SA | servo block + lever | 24 × 12 × 14 | — | black | bridge | 1 |
| FK | blade fork | 10 × 35 × 0.6 | 0.1 | steel | clamped in PB | 2 |
| WH | wheel | Ø 28 × 12 | 0.29 | black rubber | axle + nut | 2 |
| FR | motor/roller | Ø 12 × 10 | — | black + copper | in front well | 2 |
| S-PD | button + washer | M2, Ø 5 washer | — | black | into pods | 6 (spec) |
| CB (72) | box | 55 × 60 × 22 | 0.57 | black FDM | — | 1 |
| AL (72) | plate | 45 × 40 × 1 | — | aluminium | 4 screws | 1 |
| RP (72) | curved shell | 25 × 85 × 25 | — | red FDM | to CB | 2 |
| RF (72) | blade | 14 × 15 × 0.6 | — | steel + red tape | in RP | 2 |
| W4 (72) | wheel | Ø 22 × 10 | — | black | motor shaft | 4 |

---

## 6. Contact / gap matrix (AWS71; estimated mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| PD ↔ BR | screwed | 0 |
| SH front lip ↔ floor | rests on | 0 |
| SH edges ↔ PI / PD inner faces | side gap | 2–4 |
| SH rear ↔ SA | clamped | 0 |
| SA ↔ BR rear | mounted | 0 |
| FK ↔ PB slot | clamped | 0 |
| FK tip ↔ floor | touches | 0 |
| FK ↔ SH front lip | side gap | ≈ 6 |
| WH ↔ PD rear wall | running gap | 1–2 |
| WH bottom ↔ floor | contact | 0 |
| FR ↔ front well walls | gap | 2 |
| PD bottom ↔ floor | clearance | ≈ 2 |

---

## 7. Mechanism

1. **Shovel lifter (AWS71)**: the opponent is driven onto the thin, flexible aluminium lip (which lies flat on the floor), then the servo at the rear lifts / pulls the shovel, raising the opponent's front and taking its wheels' traction **(guess, medium)**.
2. **Forks**: fixed steel blades on both sides of the shovel get under opponents arriving at an angle.
3. **Drive (AWS71)**: two large rear wheels; the front rests on the forks, the shovel lip and possibly the front rollers. **(guess: coreless motors at the front with a transmission to the rear wheels, low; or the black "rollers" are the drive wheels and the large rear wheels are idlers, low)**.
4. **AWS72**: four-wheel drive box robot; the red pods guard the wheels and carry the forks; no lifter seen.

---

## 8. Assembly order (AWS71, suggested)

1. Print the **pods**, **liners**, and **bridge**.
2. Fit the **motors** into the liners and pods; fit the **rear wheels** on axles with nuts.
3. Join the pods with the **bridge** (screws).
4. Mount the **servo SA** at the rear of the bridge.
5. Cut the **aluminium shovel**, crimp its edges, bend its curve; fix its rear to the servo horn.
6. Slide the **blade forks** into the front blocks and clamp them.
7. Fit the **electronics** (in the pods / under the shovel) and route the wires.

---

## 9. Profiles as math

**9.1 Shovel centreline (YZ).** A cubic Bézier from P0 = (y +45, z 0.5) [front lip] with control points P1 = (+20, 0), P2 = (+5, 38), to P3 = (−15, 35), then a straight segment to (−35, 35). Width 36 (x ∈ [−18, +18]), thickness 0.4. Edge serration: a zigzag of 1.5 mm pitch, 0.8 mm amplitude along both edges.

**9.2 Pod plan outline (left pod; mirror for the right), XY.** (−48, +38) → (−26, +38) → (−26, +24) [front block] → (−18, +24) → (−18, −40) → (−40, −40) → curve: outer wall from (−48, −20) inward to (−40, 0) and back out to (−48, +20), i.e. **x(y) = −48 + 8·cos(π·y/40)** for y ∈ [−20, +20] → (−48, +38).

**9.3 Fork.** Strip 10 wide, from (y +38, z 12) to (y +72, z 0): **z = 12 − 0.353·(y − 38)** (≈ 19.4°), tip cut at 30° across its width.

**9.4 Oval holes.** Ellipses with semi-axes 5 × 3.5 in the pod's outer wall plane.

**9.5 Rear wheel.** Cylinder r = 14, width 12, edge fillet 2.

---

## 10. Pixel-based measurements

**AWS71 (1789 × 1340):** overall px x 90 → 1730; shovel width ≈ 330–380 px; forks: left px (95–330, 710–980), right (790–1000, 1080–1290); rear wheels ≈ 190 px tall; pod front blocks ≈ 300 px wide.
**AWS72 (1003 × 861):** overall px x 40 → 970 (≈ 930 px); box px x 205–770 (≈ 565 px); lid px x 230–750; wheels ≈ 90 × 120 px; forks ≈ 150 px wide.

---

## 11. Several independent estimates

| Quantity | Method A (limits/spec) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width | ≤ 101.6 | — | — | **96** |
| Shovel width | — | ≈ 0.38 W | AWS71: 360 px / (1640 px / 96 mm, front plane) ≈ 21 (the shovel is behind the front plane and foreshortened); against the pod front blocks (300 px ≈ 22 mm) → ≈ 26 at mid-length | **30–36 → 34** |
| Rear wheel Ø | spec ≈ 28 | ≈ pod height | AWS71 190 px at the rear (smaller scale ≈ 8 px/mm) → 24 | **26** |
| Fork width | — | — | AWS71 fork ≈ 65 px at ≈ 11 px/mm → 6; AWS72 150 px / (930/96) = 15 | **10 (AWS71), 14 (AWS72)** |
| AWS72 box width | — | 565/930 × 96 = 58 | lid 520/930 × 96 = 54 | **55** |
| Shovel crest height | ≤ cube | ≈ 1.2 × pod height | AWS71 crest at px y 150 vs floor at the shovel front px 1020 vs pod top ≈ 300 → (perspective) ≈ 35 | **35** |

---

## 12. Consistency check

1. **Shovel width (21–36).** Perspective makes the shovel look narrow where it recedes; it must fit between the white liners (≈ 36 mm apart). **Reconciled: 34.**
2. **Rear wheel size.** 24–28; the wheel tops are about level with the pod tops (28): **Ø 26**, axle at z 13.
3. **Drive layout.** The spec's two wheels with axles and nuts suggests **idler or axle-driven** wheels; the front motors are visible. This is the least certain part. **Recorded as uncertain.**
4. **Two versions.** AWS71 and AWS72 share only the concept of two side pods with blade forks. **Build AWS71** (matches the spec); AWS72 is a variant with a separate description in §3.

---

## 13. Why the designer did it (mostly adversarial)

- **Thin aluminium shovel lying on the floor**: the thinnest possible leading edge (≈ 0.4 mm) gets under almost anything, including other wedges. The flexibility lets the lip **conform to the floor** (no gap), and when hit it bends rather than transferring the hit. **Weakness**: it dents and can fold; the crimped edges suggest the builder stiffened it.
- **Convex shovel shape**: opponents driven onto it ride up the curve, lifting their front wheels off the floor; the curve also deflects vertical spinners upward.
- **Rear servo**: as far as possible from the front, protected between the pods.
- **Blade forks beside the shovel**: cover the pods' fronts, so an opponent meeting the robot at an angle still meets a floor-level edge. Steel blades are thin, sharp and cheap to replace (snap-off knife segments).
- **Sculpted pods with oval holes**: weight saving; the curved outer walls **deflect** side hits; the rear walls **guard the wheels**.
- **AWS72 red pods**: full outer guards for all four wheels, forming deflecting curved shells; the forks at their fronts get under; the box between them holds everything, with a top-accessible switch for safety checks. Tape on the fork roots stops the blades sliding out and protects the joint.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × coreless micro motors (Ø 7–8) with gearing, or N20 gearmotors | Ø 8 × 20 | front wells, (±32, +28, 10) | low–medium |
| Transmission | belt or long shaft in the white liners to the rear wheels | — | along x ±25 | low |
| Shovel servo | micro servo, horn clamped to the shovel's rear | 23 × 12 × 25 | (0, −35, 20) | medium |
| Battery | 1S/2S LiPo, 150–250 mAh | 30 × 18 × 8 | under the shovel's crest, (0, −5, 8) | medium |
| ESC/RX | combined micro board | 20 × 15 × 5 | under the shovel, (0, +10, 6) | low |
| Switch | slide switch on a pod's rear | — | (−30, −40, 15) | low |
| Bridge | printed floor plate pod-to-pod plus rear cross bar | 36 × 70 × 2 | z 2–4 | medium |
| Wiring | motor leads (black) along the liners; servo lead to the rear | — | — | high (exists) |

# Infernal: full rebuild description from reference photos

Source photos:
- `robots/infernal/reference/infernal.aws71.webp`: AWS 71, 1719 × 1209 px, cut out onto white. **Front-left, high** three-quarter: camera about 35° above the floor and about 40° to the robot's left of straight-on. The lifter is **down** (resting). Visible: the aluminium front wedge with the "flame eyes", the aluminium top plate, the clear lifter fins with green-tinted rear horns, the black printed cross-beam, the metal servo horn on the left fin, the servo, the left side of the black body with a **clear side wedge plate**, the left wheel and the top of the right wheel.
- `robots/infernal/reference/infernal.aws69.webp`: AWS 69, 916 × 985 px, **not cut out** (on a wooden table in front of a cardboard box). **Front-right, high** three-quarter: camera about 45° up, about 25° to the robot's right. The lifter is **raised**, and this is an **older lifter design** (bent "Γ" fins). Visible: the front wedge with eyes and a **clear plastic skirt** below it, the top plate with a big cut-out, the servo with its label and orange wires, the white servo horn, the right side with an **aluminium rear side plate**, the right wheel and the top of the left wheel. The kit draft skipped this photo as cluttered, but it carries a lot of information.

Everything stated as fact is read from these photos; inferences are marked **(guess)**. Dimensions are estimates, scaled from the 150 g / 101.6 mm cube limit and the project kit draft (`kit.json`: body 100 × 100 × 36 mm with a 42° ramp, two inboard wheels r 13 × 14 at y −22, a front plate 84 × 3 × 40 tilted 48°, a top plate 70 × 45 × 2 at z 39, lifter horn pivot at (y −25, z 38)). Ratios are given against **W = body width at the floor ≈ 96 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the eyes wedge), **+Z** = up. mm.
- **Origin O** = the point on the floor under the centre of the black body footprint.
- **Front** = the aluminium wedge with the painted eyes.

| ID | Part |
|---|---|
| BD | black printed body (faceted tub) |
| SF-L, SF-R | sloped side facets of BD |
| CF-L, CF-R | front corner chamfer facets of BD |
| FP | aluminium front wedge plate |
| EY | "flame eyes" graphic patch on FP |
| SK | clear polycarbonate front skirt (under FP, reaching the floor) |
| S-FP | 4 pan screws on FP (+1 small hole at the top centre) |
| TP | aluminium top plate (with the servo cut-out) |
| S-TP | pan screws on TP |
| SW-L | clear (green-tinted) polycarbonate side wedge plate, rear-left (AWS 71) |
| SW-R | aluminium side wedge plate, rear-right (AWS 69) |
| S-SW | pan screws on the side plates |
| WH-L, WH-R | two inboard drive wheels (black, fine tread) |
| WW | wheel wells (openings in the side facets) |
| SV | lifter servo (black, standard/mini size) |
| SH | servo horn: white plastic (AWS 69) / aluminium bar with holes (AWS 71) |
| LF-L, LF-R | clear polycarbonate lifter fins |
| HN-L, HN-R | green-tinted rear horns (tips of the fins, AWS 71) |
| CB | black printed cross-beam joining the fins |
| PV | lifter pivot (servo output axis, along X) |
| S-AR | bolts/nuts on the arm |
| WR | servo wires (orange/red/brown) |
| M-L, M-R | drive gearmotors (hidden) |
| BAT, ESC, RX, SWT | battery, ESC, receiver, power switch (hidden, guess) |

---

## 1. Overall description in one paragraph

Infernal is a **wide, faceted, low servo lifter/wedge** that fills nearly the whole 4 in square. Its **black printed body** has an elongated-hexagon section: a flat top about 70 mm wide, **sloped side facets** that flare out to about 96 mm at the floor, and **chamfered front corners**. The front is a **broad aluminium wedge plate** (about 76 × 44 mm) at about 42–45°, bolted at its four corners, carrying a **black patch painted with angry red-and-yellow "flame eyes"**, with a **thin clear plastic skirt** sticking out below its lower edge to meet the floor. Behind it, a **shaped aluminium top plate** covers the body, with a **large cut-out at the rear-centre** where a **black servo** sits. The servo drives a **lifter made of two clear polycarbonate fins** joined by a **black printed cross-beam**; in the AWS 71 version the fins lie flat along the top plate and down the wedge face, standing on edge, and end at the rear in two **green-tinted pointed horns** that stick up like ears. Two **black, finely treaded wheels** sit **inside wells** in the sloped side facets toward the rear. The rear corners carry **small add-on wedge plates** (clear polycarbonate on the left in AWS 71, aluminium on the right in AWS 69).

---

## 2. Part-by-part description

### 2.1 Body (BD)
- **Overall**: a printed black tub, about **96 mm wide at the floor × 92 mm long × 30 mm tall** (z 2 to 30, where TP sits). Matt black, horizontal layer lines on all faces.
- **Section across X (looking from the front)**: an **elongated hexagon cut flat at the bottom**: flat top about **70 mm wide** (x ±35) at z 30; **side facets** sloping outward and down at about **55–60° from horizontal** to about x ±48 at z ≈ 10; then a short near-vertical band to the floor (z 2–10). So the sides are **wedges too**.
- **Plan**: rectangular rear part; the front corners are **chamfered** in plan at about 30–35° (CF-L, CF-R), each chamfer about 15 mm long, so the front edge is about **76 mm wide** (matching FP) and the full width (96) is reached about 15 mm behind the front.
- **Front**: a sloped face at about 42–45° from the floor, from about (y +46, z 2) up to (y +18, z 30), covered by FP. The front-corner chamfers are themselves sloped (they are the meeting of the side and front slopes), giving a faceted "gem" look.
- **Wheel wells (WW)**: openings in the side facets toward the rear, about **34 mm long × 18 mm tall**, centred at about **y −22, z 14**, through which the inboard wheels' outer treads show.
- **Rear**: not photographed; probably a sloped or vertical rear face with the switch **(guess)**.

### 2.2 Front plate (FP) and eyes (EY)
- **Shape**: a flat **aluminium plate**, about **76 mm wide × 44 mm long (down the slope) × 1.5 mm thick**, with **rounded corners** (radius about 5 mm), lying on the sloped front face at about **42–45°**. Brushed/scratched finish with many fine score marks (from fights).
- **Position**: top edge at about (y +18, z 30), meeting the front edge of TP with a slight overlap; bottom edge at about (y +49, z 1).
- **Screws S-FP**: four **silver Phillips pan heads with washers** (head Ø ≈ 5.5 mm, M3), about 6 mm in from each corner: AWS 71 px (1545, 485) top-right, (840, 840) bottom-left; AWS 69 px (70, 615) top-left, (530, 765) bottom-right; the other two are hidden by the fins/graphics. A **small round hole** (Ø ≈ 2.5 mm) at the **top centre** (AWS 71 (1205, 580); AWS 69 (310, 650)), maybe a spare/alignment hole or an LED window **(guess)**.
- **Eyes EY**: a **black rectangular patch** about **50 mm wide × 24 mm tall**, slightly left of centre in the lower half of FP (from about 10 mm above the bottom edge), painted with two **angry flame-shaped eyes**: each eye is a red "J"/flame stroke with yellow highlights below, slanting inward. The patch has visible straight edges and slight relief: it is **black tape/vinyl with paint marker** stuck on the plate **(medium)**, or a **window cut in FP** revealing the black body painted with the eyes **(low)**.

### 2.3 Front skirt (SK)
- **Seen in AWS 69**: a **clear, thin (about 0.5–1 mm) polycarbonate sheet** sticking out about **6–8 mm below/ahead of FP's bottom edge** along its whole width, lying almost flat on the table: a flexible **floor-hugging lip**.
- **Function**: lets the wedge get a true zero-height edge (the 1.5 mm aluminium edge can't reach the floor at 45° without lifting the robot). In AWS 71 it is not visible (cut out by the mask or removed).

### 2.4 Top plate (TP)
- **Shape**: a flat **aluminium sheet** about **1 mm thick**, outline about **70 mm wide × 70 mm long**, covering the flat top of BD from the front plate back to near the rear. It has a **large cut-out** at the rear-centre for the servo and arm: about **36 mm wide × 30 mm deep**, opening to the rear (AWS 69 shows it as a U-notch with rounded inner corners and angled sides). In AWS 71 the plate also has a **stepped/notched outline** at the left: its left edge is cut back around the left wheel well and steps in at the front-left (a jog of about 6 mm).
- **Screws S-TP**: silver Phillips pans with washers, Ø ≈ 5.5: front-left (AWS 71 (390, 575)), rear-right (AWS 71 (1285, 215); AWS 69 (715, 545) front-right?), rear-left (AWS 69 (155, 385)). Probably 4–5 in all.
- **Rear corners**: TP's rear corners stop at the rear wheel wells; the plate's rear edge has a **small upward kink/tab** on the right in AWS 71 near the right wheel (a light-reflecting tab).

### 2.5 Side wedge plates (SW-L, SW-R)
- **SW-L (AWS 71)**: a **clear polycarbonate plate with a green tint** (thickness ≈ 1.5 mm), roughly a **trapezoid about 30 mm long × 22 mm tall**, screwed onto the **rear-left sloped side facet** behind the left wheel with **three small Phillips screws** (px (50, 575), (295, 700), (300, 790)). Its front edge stands proud and is slightly bent outward. A couple of **orange paint marks** on it.
- **SW-R (AWS 69)**: a matching **aluminium plate**, about 30 × 22, on the **rear-right facet** behind the right wheel, with **two screws** (px (870, 470), (780, 600)).
- **Function**: cover the facet behind the wheel and present a hard ramp at the rear corners.

### 2.6 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 28 mm × 12 mm wide**, black rubber/TPU tyres with a **fine knurled tread** (about 50–60 small blocks/ribs around), black hubs. Kit: r 13 × 14.
- **Position**: centres at about **(±40, −22, 14)**, inside the wells: their outer tread surfaces sit flush with or about 1 mm inside the side facet envelope, so they are **protected by the body** (inboard mounting). Tops at z ≈ 28, i.e. **just below the top plate**: so the robot can **not** drive inverted on its wheels alone; it relies on the lifter to self-right **(guess)**.
- **AWS 69**: the right wheel shows inside its well behind a **white plastic part** (a motor mount or gearbox, white) at (700, 470).

### 2.7 Servo (SV)
- **AWS 69**: a **black servo** (standard-mini size, about **23 × 12 × 28 mm**, with mounting ears), standing **upright** in the cut-out with its output toward **+X (right)**, a **red/silver label** on its side, and **orange/red/brown wires** coming out of its lower side. Its top stands about **12 mm above TP**.
- **AWS 71**: the servo is seen **lying down** in the cut-out (body along X), black, under the cross-beam, with its output on the **left (−X)** side where the aluminium horn is.
- **Mount**: in a printed cradle in BD (the cradle's black walls show around it) **(guess)**.

### 2.8 Servo horn (SH)
- **AWS 69**: a **white plastic servo horn** (cross or bar type) on the servo output at about (600, 400), with the right fin bolted to it by **two small bolts with nuts**.
- **AWS 71**: an **aluminium flat bar**, about **28 mm long × 7 mm wide × 1.5 mm thick**, bolted on the left fin's outer face: it has **two Phillips bolts** (at its ends, px (515, 360) and (710, 350)), **two small holes/rivets** between them, and an **oval slot** (about 4 × 2 mm) near its front end. It is the metal servo arm that connects the servo output to the fins.

### 2.9 Lifter fins (LF-L, LF-R) and horns (HN)
- **AWS 71 version (lowered)**:
  - Each fin is a **clear polycarbonate plate standing on edge** (in a YZ plane), about **1.5–2 mm thick**, about **12–14 mm tall**. LF-L at x ≈ −14, LF-R at x ≈ +20 (asymmetric: the right fin sits at the right edge of the eyes patch, the left fin near the left of it; both are within the eyes patch width) **(guess on exact x)**.
  - **Side profile** (follows the robot): from the rear horn (up and behind the pivot), **forward along the top plate** about 10–14 mm above it, then **bending down at the front edge of TP** to run **down the front wedge face**, standing **8–12 mm proud** of FP, to a front end about 5 mm above the floor near the wedge's bottom edge. The bend at the wedge top is a smooth curve (radius about 10 mm) — the plate was **heat-bent** or cut to shape **(cut to shape: the fin is a flat profile)**.
  - **Horns HN**: at the rear, each fin rises into a **pointed tip** about **20 mm above TP**, raked backward, with a **green tint** (the plate edge seen end-on; polycarbonate looks green at its edges/thickness) — a **sharp triangular "ear"**.
  - **Cross-beam CB**: a **black printed beam**, about **50 mm long × 10 mm × 8 mm**, with a **tapered right end**, joining the two fins just ahead of the horns at about z ≈ 38, y ≈ −14. It holds the fins parallel and stiff.
- **AWS 69 version (raised)**: each fin is a **flat clear sheet, about 45 mm tall × 25 mm wide**, with its free end **bent 90° into a horizontal flange** about 15 mm wide (a "Γ"), forming two tall paddles. A **black printed bar** joins them near their top. The right fin is bolted to the white servo horn with two bolts and nuts; a third bolt lower down. In the raised position the fins stand about **55 mm above TP**, leaning forward.

### 2.10 Pivot (PV)
- The fins rotate with the **servo output** about an **X axis** at about **(y −14, z 34)** (just above TP, at the front of the servo cut-out). In the AWS 71 version the rotation **lifts the fin fronts off the wedge face**, scooping the opponent that has climbed the wedge upward; in the AWS 69 version the paddles swing forward/down onto the wedge.

### 2.11 Wires (WR)
- AWS 69: **orange, red and brown servo wires** loop from the servo's underside down into the body on the right. No other wires visible.

---

## 3. Per-view sections

### 3.1 AWS 71 (front-left, high, lifter down)
- Bottom-right: the **wide aluminium front plate** with screws and the **flame-eyes** patch; two clear fins lying down its face.
- Centre: the aluminium top plate with the servo hole, the black beam, the **metal servo arm** on the left fin, the two **green horns** sticking up at the rear.
- Left: the sloped black left side with the wheel in its well and the **clear side plate** at the rear-left.

### 3.2 AWS 69 (front-right, high, lifter up)
- Bottom: the front plate with eyes, two screws, centre hole, and the **clear skirt** under it.
- Middle: the top plate with its U cut-out; the **upright servo** with its label, wires and **white horn**; the two **Γ-shaped clear paddles** raised high with the black bar between them.
- Right: the right side facets with the **aluminium rear-corner plate**, the right wheel inside its well behind a white motor mount.

### 3.3 Top view (plan, synthesised)
- An elongated hexagon: 96 mm wide, 92 mm long, with the front corners chamfered; the front plate (76 × 32 in plan) across the front; the top plate (70 × 70) in the middle with the rear-centre cut-out holding the servo; the two fins as thin lines over the top plate and front plate; the cross-beam across them; two wheel treads showing in the side wells at the rear.

### 3.4 Front view
- A wide, low trapezoid: 96 mm at the floor, 70 mm at the top (30 mm tall), the aluminium plate filling the middle with the eyes; two clear fins standing out from the plate; the horns and the servo top behind; the side facets slanting away.

### 3.5 Left side view
- A long low profile: the front slope (45°), the flat top at z 30, the rear; the **wheel** in a well toward the rear; the fins' rear horns sticking up about 20 mm above the top behind the servo; the clear plate at the rear.

### 3.6 Rear view and underside (not photographed; inferred)
- Rear: sloped or vertical black face 70–96 mm wide; servo back visible in the cut-out; possibly the switch. Underside: flat, with two wheel slots.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | faceted tub | 96 × 92 × 28 | 1 × 0.96 × 0.29 | black FDM | — | 1 |
| FP | rounded-corner plate | 76 × 44 × 1.5 | 0.79 × 0.46 | aluminium | 4 × M3 pan + washer | 1 |
| EY | patch | 50 × 24 | 0.52 × 0.25 | black tape + red/yellow paint | adhesive | 1 |
| SK | thin lip | 76 × 10 × 0.7 | 0.79 | clear PC | under FP (clamped) | 1 (AWS 69) |
| TP | shaped plate with U cut-out | 70 × 70 × 1 (cut-out 36 × 30) | 0.73 | aluminium | 4–5 × M3 pan + washer | 1 |
| SW-L/R | trapezoid plate | 30 × 22 × 1.5 | 0.31 | clear green PC / aluminium | 2–3 screws | 1 + 1 |
| WH | treaded tyre | Ø 28 × 12 | 0.29 × 0.13 | black rubber/TPU | motor shaft | 2 |
| SV | servo | 23 × 12 × 28 | — | black | printed cradle | 1 |
| SH | horn | white plastic / Al bar 28 × 7 × 1.5 | — | white / aluminium | 2 bolts + nuts | 1 |
| LF | profiled on-edge plate | ≈ 80 along the profile × 13 × 1.8 | 0.83 | clear PC | bolted to SH and CB | 2 |
| HN | pointed tip | 20 tall | 0.21 | (tip of LF) | — | 2 |
| CB | printed beam | 50 × 10 × 8 | 0.52 | black FDM | screws into fins | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| FP ↔ BD front slope | screwed flat | 0 |
| FP top edge ↔ TP front edge | butt/overlap | 0 |
| FP bottom edge ↔ floor | above | 1 |
| SK ↔ floor | touching (AWS 69) | 0 |
| SK ↔ FP | clamped under | 0 |
| TP ↔ BD top | screwed | 0 |
| TP cut-out edge ↔ SV | around | 2–4 |
| SW-L/R ↔ BD rear facets | screwed | 0 |
| WH outer tread ↔ side facet envelope | flush/inside | 0 to −1 |
| WH ↔ well edges | clearance | 2 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ TP | below | −2 |
| LF lower edge ↔ TP (lowered, AWS 71) | above | 0–2 |
| LF front edge ↔ FP (lowered) | resting on / just above | 0–1 |
| LF front end ↔ floor (lowered) | above | 5 |
| LF ↔ CB | screwed | 0 |
| LF-L ↔ SH | bolted | 0 |
| SH ↔ SV spline | on spline | 0 |
| HN tip ↔ TP | above | 20 |
| BD floor ↔ floor | above | 2 |

---

## 6. Mechanism
1. **Drive**: two inboard wheels toward the rear, skid steer; the front plate edge (and the skirt) carry the front.
2. **Lifter**: the servo rotates the fin assembly about the X axis near the front of the servo. AWS 71: when the opponent rides up the wedge onto the fins, rotating the fins lifts their fronts, raising the opponent further and tipping it; a large rotation could **flip** light opponents. AWS 69: the tall paddles swing down/forward onto an opponent on the wedge.
3. **Self-righting** (guess): with the wheels below the top plate, an inverted Infernal rests on its top plate and fins; rotating the fins pushes the horns/fin tips against the floor and rolls the robot back over. The horns' rearward rake suits this.

---

## 7. Assembly order (suggested rebuild)
1. Print BD with the wheel wells, motor cradles, servo cradle and screw bosses for FP, TP and the side plates.
2. Fit the two drive motors and the wheels (with the white mounts in AWS 69).
3. Fit the servo in its cradle, output to the side (left in AWS 71), and route its wires.
4. Fit the battery, receiver/ESC and switch.
5. Screw on the top plate TP.
6. Clamp the clear skirt under the front plate and screw FP on (4 × M3). Apply the eyes patch.
7. Screw on the side plates SW.
8. Assemble the lifter: screw CB between the two clear fins; bolt the metal arm (or white horn) to the left fin; fit the horn onto the servo spline; set the lowered position so the fins rest on the wedge.

---

## 8. Coordinate frame (restated)
- Origin O on the floor under the centre of BD. +X right, +Y forward, +Z up. mm.
- BD: x ∈ [−48, +48] at the floor, [−35, +35] at the top (z 30); y ∈ [−46, +46]. FP from (y +18, z 30) to (y +49, z 1). Wheels at (±40, −22, 14). Pivot at (y −14, z 34).

## 9. Profiles as math

**9.1 Body cross-section (XZ plane, valid for y ∈ [−46, +18]).** Polygon: (−48, 2), (−48, 10), (−35, 30), (35, 30), (48, 10), (48, 2). Side facet slope: atan(20/13) = 57°.

**9.2 Front slope (YZ plane).** Line from (y 18, z 30) to (y 48, z 2): z = 30 − 0.933·(y − 18) → 43°. FP lies 1.5 mm proud of it; its flat length √(30² + 28²) ≈ 41 mm (+3 mm overhang at the bottom = 44).

**9.3 Front corner chamfers (plan, at z = 2).** From (±48, +31) to (±38, +46): 34° from Y.

**9.4 FP outline (in its own plane, u across, v down the slope).** Rectangle u ∈ [−38, 38], v ∈ [0, 44], corner fillets r 5. Screws at (±32, 6) and (±32, 38). Hole Ø 2.5 at (0, 7). Eyes patch u ∈ [−30, +20], v ∈ [18, 42].

**9.5 Lifter fin (AWS 71) side profile (YZ plane at the fin's x), lowered.**
- Lower edge: from the pivot P = (−14, 34) forward horizontally to (16, 32) (2 mm above TP), arc centre (16, 22), r = 10, turning down to follow the front slope; then a line parallel to the front slope offset 0 mm: from (24, 25) to (44, 6).
- Upper edge: the same path offset 12 mm outward (up/forward).
- Rear horn: from (−10, 44) a line up-back to the tip (−24, 56), back down to (−20, 34).
- Thickness 1.8 along X. Hole Ø 3 at P; two holes Ø 2 for CB at (−14, 40) and (−6, 40).

**9.6 Lifter rotation.** Fin points rotate about P by angle θ (0 lowered, up to ≈ 60°): (y, z) → P + R(θ)·((y, z) − P), with R(θ) = [[cos θ, −sin θ], [sin θ, cos θ]] taking +Y toward +Z. The front tip (44, 6) goes to (−14 + 58 cos θ + 28 sin θ, 34 + 58 sin θ − 28 cos θ): at θ = 30°, (+50, 39); at 60°, (+39, 70).

**9.7 Wheels.** r(φ) = 13.4 + 0.6·[sin(56φ) > 0], width 12.

## 10. Pixel-based measurements (independent check)
- **AWS 71** (1719 × 1209): FP corners about (735, 640) top-left, (1480, 340) top-right, (980, 1100) bottom-left, (1700, 720) bottom-right. Eyes patch (950–1600, 560–940). Left wheel (150–310, 470–660). Clear side plate (40–325, 520–860). Horns tips (500, 160) and (880, 30). Cross-beam (720–1160, 180–330). Servo horn bar (500–790, 330–420).
- **AWS 69** (916 × 985): FP from (55, 520) top-left to (590, 690) top-right and (40, 880) bottom-left to (490, 925) bottom-right; eyes (100–480, 620–860). Servo (380–580, 300–490). Paddles: left (75–330, 30–200), right (370–670, 85–420). Right wheel (735–820, 445–545). Right rear plate (760–880, 450–640).

## 11. Several independent estimates of key quantities

| Quantity | Method A (kit / rules) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width (floor) | kit 100 (cube max 101.6) | FP ≈ 0.8 × body width | AWS 69: FP 535 px wide; body visible width ≈ 870 px incl. facets → ratio 0.61 at FP depth (body behind is farther) → FP 76 gives ≈ 100 (upper bound) | **96** |
| Front plate width | kit 84 | ≈ 0.8 W → 77 | AWS 71 top edge 805 px; servo width (23) ≈ 230 px nearby → 10 px/mm → 80 | **76** |
| Front plate length | kit 40 | ≈ 0.55 × FP width → 42 | AWS 69 left edge 360 px vs width 535 → 0.67 × 76 = 51 (foreshortened slope seen from high is actually lengthened) | **44** |
| Wedge angle | kit 42–48° | — | AWS 69 FP looks about as tall as wide-ish at 45° camera → 40–50° | **43°** |
| Body height | kit 36 (incl. plates) | ≈ 0.31 W | AWS 71: left side height at the front ≈ 300 px at ≈ 10 px/mm → 30 | **30 to TP** |
| Wheel Ø | kit 26 | ≈ 0.95 × body height | AWS 71 left wheel 190 px at ≈ 7 px/mm (rear, farther) → 27 | **28** |
| Servo size | 9 g (23 × 12 × 23) vs mini (23 × 12 × 28) | — | AWS 69 servo 200 × 190 px; FP 535 px = 76 mm → 7 px/mm → 28 × 27 (upright view) | **mini servo, 23 × 12 × 28** |
| Horn height above TP | kit pivot z 38 | — | AWS 71 horn tip 160 px above TP at ≈ 8 px/mm → 20 | **20** |

## 12. Consistency check: conflicts and reconciliation
1. **Body size vs cube**: kit 100 × 100 is at the limit; side facets and front chamfers give little bulk beyond the 96 × 92 box. **Reconciled 96 × 92**, leaving clearance.
2. **Fin x positions**: AWS 71 shows the fins not symmetric about the centre of FP (the right fin on the right edge of the eye patch, the left fin near the left third). The camera angle distorts the right side less. **Reconciled: LF-L at x −14, LF-R at +20** (spacing 34 = servo-horn + beam length); flagged as uncertain.
3. **Two lifter designs**: AWS 69 paddles vs AWS 71 profiled fins. Different events; the base model uses AWS 71.
4. **Wheel top vs TP**: Ø 28 at z 14 gives top 28 < TP 30. Inverted driving is not possible, consistent with the horns' role in self-righting.
5. **Skirt visibility**: seen in AWS 69 only; AWS 71's cut-out mask may have removed a clear sheet. Keep it as optional.

---

## 13. Why the designer did it (per part, mostly adversarial)

- **Broad aluminium front wedge at about 43° (FP) + clear skirt (SK)**
  - Getting under vs contact: the clear flexible skirt makes the first contact at **floor level**, sliding under the opponent's edge; the 43° aluminium face then carries the opponent up onto the fins. Aluminium resists spinner bites and scraping far better than printed plastic. The wide plate (76 mm) covers most of the front, so a head-on opponent always meets metal.
  - Against horizontal spinners: the slope deflects hits upward; the rounded corners avoid a catchable corner; four screws at the corners leave no edge to peel.
  - Construction: a flat cut plate is easy to replace; painted eyes give the robot its identity ("Infernal" flames).
- **Faceted body with sloped sides and chamfered front corners (BD)**
  - Fight: **every face is a ramp**. An opponent hitting the side or a front corner tends to ride up and over rather than getting a square push; horizontal spinners glance off the slopes. The wide footprint (96 mm) resists being flipped sideways.
  - Construction: printed as one piece; slopes print without supports when printed upside-down or with the slopes at ≤ 60°.
- **Inboard wheels in wells**
  - Fight: the wheels are hidden inside the sloped silhouette, so spinners and wedges cannot reach the tyres or shafts from the side; only a sliver of tread shows.
  - Weak point: the robot cannot drive upside down (wheels below the top). Accepted because the lifter self-rights.
- **Rear corner side plates (SW)**
  - Fight: the rear facets are where an opponent coming from behind or the side hits; a hard plate stops chewing of the printed facet next to the wheel well. Clear polycarbonate is tough and takes impacts without cracking; aluminium is harder.
- **Aluminium top plate with a cut-out (TP)**
  - Fight: overhead hits and opponents riding over meet aluminium. The cut-out exists only where the servo and arm must pass; everything else is covered.
  - Construction: easy access by removing a few screws.
- **Clear polycarbonate lifter fins with a printed cross-beam (LF, CB)**
  - Fight: on-edge fins standing proud of the wedge **concentrate the contact** onto two thin edges under the opponent, and when lifted they raise the opponent's front clear of the floor so it loses traction and can be pushed or flipped. Polycarbonate bends and springs back instead of snapping under spinner hits. The cross-beam keeps the fins together so one cannot fold sideways.
  - **Horns**: sharp rear tips that stick up give a self-righting lever and a pointy profile that discourages overhead attacks (and look like devil horns, matching "Infernal").
  - Weak points: a servo gearbox can strip under shock loads; the metal arm (AWS 71) spreads the load to the fin better than a plastic horn (AWS 69), which explains the change.
- **Mini servo**
  - Construction: cheap, self-contained actuator with position control; mounted in the middle of the robot, protected on all sides by the body and plates.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors with white printed mounts | 12 × 10 × 25 | transverse at y −22, z 14; x ±22 | medium |
| Battery | 2S LiPo 300–450 mAh | 45 × 20 × 12 | front, under TP behind FP, (0, +12, 12) | medium |
| ESC + receiver | combined board | 30 × 20 × 6 | middle, (0, −2, 10) | low |
| Power switch / link | at the rear face or under TP's rear edge | 10 × 5 × 5 | (0, −45, 15) | low |
| Servo cradle | printed pocket with 2 screws through the servo ears | 34 × 14 × 20 | (0, −24, 20) | medium |
| Wires | servo wires to the receiver; motor leads; battery → switch → ESC | — | inside | high (servo wires seen) |
| FP / TP bosses | M3 screw bosses in the tub corners | Ø 7 | under each screw | medium |

## 15. What the photos cannot show (uncertain list)
- The rear, underside and switch position.
- Exact fin x positions and the lifter's full travel.
- Whether the eyes patch is tape or a window.
- All mm values are scaled estimates (±10–15%).

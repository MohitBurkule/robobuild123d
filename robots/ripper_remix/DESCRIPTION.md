# Ripper Remix: full rebuild description from reference photos

Source photos (in `robots/ripper_remix/reference/`):
- `ripper_remix.aws70.webp` (304 × 343 px): a small pit snapshot on a grey table. **Straight-on front view, about 20–25° above horizontal**. A white object (another robot or a box) is at the left edge; ignore it.
- `ripper_remix.aws72.webp` (1239 × 1100 px): cut out onto white. The **best photo**. **Front-left three-quarter, about 30° above horizontal**, so the scoop's left end, the left pod's vents and the flipper's right edge (with its gap) are visible.
- `ripper_remix.aws77.webp` (552 × 539 px): cut out. **Straight-on front view, about 20° above horizontal**, very like AWS70.

**Limits of the evidence.** All three photos show the **front**. The rear, the underside, the sides in profile and the wheels are **never seen**. **No screws, wires, switch or wheels are visible in any photo.** The robot is printed entirely in **one yellow filament**, with smooth faceted surfaces. Because the photos show only one side of a deliberately closed, featureless shell, this description is somewhat shorter than the target length, and a large share of it is reasoned inference (marked **(guess)**). The project spec draft (`spec.json`) is used as an independent source for the hidden geometry: chassis 92 × 85 mm, 42 mm tall; a front scoop; a rear-hinged flipper with a flat top and sloped front; two Ø 22 TPU wheels on Pololu 50:1 micro gearmotors at y = −25.

Dimensions are **estimates in mm**, scaled from the AWS antweight limits (150 g, fits a 101.6 mm cube) and the photo proportions. **W = pod-to-pod body width ≈ 92 mm** is the ratio base.

Ripper Remix is a **servo flipper / lifter**: a yellow faceted body with two **armoured side pods**, a **full-width front scoop**, and a **central flipper plate** embossed "RIPPER REMIX", hinged at its **rear top edge** on an exposed pin.

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) under the centre of the body (mid-width, mid-length of the chassis, **excluding** the scoop).
- **+X** = robot's right, **+Y** = forward (toward the scoop), **+Z** = up. Units mm.
- All photos face the front, so the **robot's right is on the image left**. In AWS72 the camera is to the **image-left of centre**, i.e. at the **robot's right-front**: the scoop's image-left end (the robot's right end) is nearest and largest. The pod at the image right is the **robot's left pod**. Its vent slots are still visible because the upper chamfer faces upward toward the high camera. All positions below are in robot coordinates.

Part IDs:

| ID | Part |
|---|---|
| CH | central chassis tub (hidden behind the flipper and pods) |
| PD-L / PD-R | side pods (faceted armour boxes that enclose the wheels) |
| VT-L / VT-R | vent slots in the pods' upper outer chamfers (3 each) |
| SC | front scoop (trapezoid wedge block across the full width) |
| SC-F | scoop front lip facet (the lighter lower strip) |
| SC-T | scoop top ramp facet |
| SC-E | scoop end facets (angled) |
| FL | flipper plate |
| FL-U | flipper upper (rear) flat section, with a slot at the top |
| FL-L | flipper lower (front) sloped section, with the embossed name |
| TX | embossed "RIPPER" / "REMIX" lettering |
| HP | hinge pin across the top-rear |
| HE-L / HE-R | hinge ears (knuckles) at each end of the pin |
| WH-L / WH-R | drive wheels (hidden, guess) |
| DM-L / DM-R | drive gearmotors (hidden, guess) |
| MM-x | motor mounts (hidden, guess) |
| SV | flipper servo (hidden, guess) |
| LK | servo-to-flipper link (hidden, guess) |
| BAT, ESC, RX, SWT | electronics (hidden, guess) |
| S-x | screws (none visible; hidden underneath, guess) |

---

## 1. Overall description in one paragraph

Ripper Remix is a **bright lemon-yellow, fully printed** flipper about **≈ 100 mm wide** (at the scoop), **≈ 92 mm wide** at the pods, **≈ 42 mm tall** at the hinge, and **≈ 100 mm long** including the scoop **(length is a guess; never seen from the side)**. In front view it reads as **three columns plus a bumper**: a **central flipper panel** (about 44 mm wide) standing between two **chunky faceted side pods** (each about 24 mm wide), with a **wide trapezoid scoop** across the bottom front. The pods have a **flat top**, a **45° upper outer chamfer pierced by three parallel angled slots**, a **vertical outer face**, and a **lower outer chamfer** that tucks inward toward the floor, so each pod's cross-section is a **lopsided hexagon**. The flipper panel is **two flat facets**: a near-horizontal upper (rear) facet ending at a **hinge pin** with **two small knuckles** that stand above the pods at the rear, and a steeper lower (front) facet carrying **raised block lettering "RIPPER" with smaller "REMIX"** below it. The flipper's lower front edge tucks in just behind the **scoop**, which is a wide **trapezoid ramp**: a lighter, steep **front lip strip** at the bottom, a sloped **top facet**, and **angled end facets**. No fasteners, wheels or electronics are visible.

---

## 2. Part-by-part description

### 2.1 Side pods (PD-L, PD-R)
- **Cross-section (XZ, front view)**: a **six-sided shape**, symmetric pods mirrored about X = 0. For the right pod (x > 0):
  - inner vertical face at **x = +22** (against the flipper gap), from z ≈ 4 to z ≈ 36;
  - flat top at **z ≈ 36**, from x = +22 to x = +33;
  - **upper outer chamfer** at about **45°**, from (+33, 36) to (+44, 25);
  - **outer vertical face** at **x = +46**, from z = 25 to z = 15 (a short vertical band, slightly wider than the chamfer ends);
  - **lower outer chamfer** at about **55–60° from horizontal**, tucking in from (+46, 15) to (+36, 2);
  - bottom at **z ≈ 2** from x = +36 to the inner face.
- **Length (Y)**: from about **y = −40 to y = +30** **(guess; consistent with the spec chassis length 85)**. The pod front faces are **vertical** and flat (AWS72 shows the left pod's front face as a lit flat area at px ≈ (870–1000, 400–520) behind the scoop's end).
- **Front-top corner**: a **chamfer** joins the top and the front face (AWS72 px ≈ (830–960, 300–400): a lighter sloping facet).
- **Surface**: smooth, with fine horizontal **layer lines** on the vertical faces; the chamfer faces show stair-stepping. Printed upright **(guess)**.
- **Vent slots (VT)**: **three parallel slots**, each about **2 mm wide × 10 mm long**, cut through the **upper outer chamfer** near its **front end**, running **down the slope** (perpendicular to the chamfer edge), about **4 mm apart**. AWS72 shows them clearly on the left pod (px ≈ (1150–1230, 250–370)); AWS77 shows them on both pods (px (75–110, 70–130) and (440–480, 70–130)); AWS70 too.
- **Function of the slots (guess)**: weight saving and cooling of the drive motors inside, and a styling detail.

### 2.2 Wheels (WH-L, WH-R), not visible
- No wheel is visible in any photo. The pods reach almost to the floor (z ≈ 2), and their lower chamfers would hide a wheel inside. The spec puts **Ø 22 × 8 TPU wheels** at **x = ±41.5, y = −25**, i.e. **inside the pods** in a cut-out in the pod wall.
- **Reconciled guess (medium)**: two **Ø 22–24** wheels, one in each pod, toward the rear (y ≈ −25), protruding **≈ 2 mm below** the pod bottoms through openings in the pod floors. Their outer faces are covered by the pod walls, so the wheels are **fully guarded**. The robot is therefore **two-wheel drive** with the scoop or a rear skid as the third and fourth contact points.

### 2.3 Central chassis (CH), mostly hidden
- Between the pods and under the flipper is a tub about **44 mm wide (x ±22)**. Its front is closed by the scoop; its top is the flipper. A **dark gap** between the flipper's right edge and the left pod in AWS72 (px ≈ (790–840, 160–500)) shows the inside is dark (shadow, or a dark component) **(guess: the flipper servo or wires)**. In AWS77 a small **reddish-brown glint** at the top of the gap left of the flipper (px ≈ (175–185, 70–110)) may be a **wire** or the servo case **(guess, low)**.

### 2.4 Front scoop (SC)
- **Plan**: a **trapezoid**, widest at the front. Front edge **≈ 102 mm** wide (x ±51), rear edge **≈ 80 mm** wide (x ±40). The ends are **angled facets SC-E** at about **45–50°** in plan (AWS72's right end at the image left is a large angled facet, px ≈ (110–240, 430–700)).
- **Depth (Y)**: **≈ 26 mm**, from y ≈ +34 (rear, against the pods' fronts) to y ≈ +60 (front edge).
- **Side profile (YZ)**: two facets:
  - **SC-F front lip**: a **steep facet** about **6–8 mm** tall, from the floor up and slightly back. In AWS72 it is the **lighter, translucent-looking strip** (px y ≈ 715–920 at the bottom of the scoop), whose different shade is due to its steeper angle facing the light.
  - **SC-T top ramp**: a **sloped facet** at about **30–35°** from horizontal, rising from the top of the lip (z ≈ 7) to the back edge at **z ≈ 22**. Its surface shows horizontal layer lines (parallel to X), so it was printed with the ramp as a stair-stepped slope.
- **Bottom**: presumably flat, at the floor or ≈ 0.5–1 mm above it.
- **Front edge**: straight across the full width, **blunt** (the lip is a few mm thick). It is not a knife edge, so the scoop relies on its low height and its corners **(see §11)**.
- **Joining**: printed **integral with the chassis floor** or screwed from below **(guess)**. The spec models it as a separate nylon part.

### 2.5 Flipper plate (FL)
- **Width**: **≈ 44 mm** (x ±22), fitting between the pods with a **gap of ≈ 1.5–2 mm** each side (AWS72 shows a clear dark gap on one side).
- **Thickness**: the plate's exposed edge in AWS72 (px ≈ (800–840, 150–520)) shows a **≈ 6–8 mm** thick rim. The plate may be a **hollow shell** or a solid 3 mm plate with a down-turned **edge flange** **(guess)**.
- **Facets**:
  - **FL-U (upper/rear)**: a flat, **almost horizontal** facet (sloping slightly up toward the rear, ≈ 5–10°), from the hinge at **y ≈ −40, z ≈ 40** forward to **y ≈ −2, z ≈ 36**. Near the hinge it carries a **rectangular slot or step** about **20 × 3 mm** (AWS72 px ≈ (780–905, 85–105); AWS77 px ≈ (270–310, 40–50)). The slot may be a **finger grip** or the **access slot for a link/switch** **(guess)**.
  - **Bend**: a straight transverse crease at about **y ≈ −2** (AWS72 px y ≈ 190–200).
  - **FL-L (lower/front)**: a **steeper facet** at about **35–40°**, from the bend down to the front edge at about **y ≈ +32, z ≈ 12**, just behind and above the scoop's rear edge. It carries the lettering.
- **Lettering TX**: **raised** (embossed) block capitals, **≈ 1 mm** high. **"RIPPER"** about **34 mm long × 6 mm tall**, centred on the lower facet; **"REMIX"** about **18 mm long × 3.5 mm tall**, right-aligned below it (in robot frame: under the "PER" end of RIPPER). The letters are in a stylised, squared typeface with notched corners.
- **Seam / step**: in AWS72 and AWS77 the lower facet's left edge (robot right, image left) shows a **vertical step** about **2 mm** where the plate's side flange begins (px ≈ (555–570, 180–480) in AWS72).

### 2.6 Hinge pin (HP) and knuckles (HE-L, HE-R)
- **HP**: a **round pin about Ø 3 mm** spanning the full flipper width plus the knuckles, about **58 mm** long, along X at **(y −40, z 41)**. In AWS72 its two ends are visible as short **yellow stubs** (printed pin, or filament-wrapped steel rod **(guess)**) sticking out beyond each knuckle by ≈ 2 mm (px ≈ (645, 50) and (1075, 175)).
- **Knuckles**: two **upright tabs** about **4 mm thick × 8 mm tall**, one at each end of the flipper's rear edge (x ≈ ±25), standing **≈ 4–6 mm above the pod tops** (AWS70 px ≈ (100–115, 10–30) and (215–230, 10–30); AWS77 (150–165, 25–45) and (385–400, 25–45)). They are **part of the chassis** (the fixed half of the hinge), and the flipper has a matching **barrel along its rear edge** between them **(guess, medium)**.
- AWS72 shows a **thin vertical rib** running down from each knuckle along the flipper's side edge (px ≈ (650–690, 60–450) left and (1000–1050, 140–520) right). These are the flipper's **side flanges**, which are hinged at their top ends.

### 2.7 Hidden actuator (SV, LK), guess
- A flipper of this size in an antweight is almost always driven by a **high-torque micro/mini servo** (e.g. 9–20 g digital, metal gear) **(guess, high)**. It would sit **in the central tub under the flipper**, its output horn pushing the underside of the flipper through a short **link LK**, or the horn itself acting as a cam on the flipper's underside.

### 2.8 Screws and fasteners
- **None are visible.** The yellow surfaces are uninterrupted. The pods, scoop and chassis are probably **one print** or are screwed **from underneath** **(guess, medium)**. The flipper is held only by the hinge pin.

### 2.9 Wires and switch
- **None visible.** The switch is probably on the **rear wall** or **underside** **(guess)**; the slot in FL-U could be a switch access **(low)**.

---

## 3. Per-view sections

### 3.1 AWS77 (straight front, ≈ 20° above)
- **Bottom band**: the scoop as a wide trapezoid (px x 35–525 at the front edge, y 290–480), the lighter lower lip barely distinct.
- **Middle**: the two pods (left pod px x 60–180, right pod px x 380–500 in the image) as **hexagonal shields**, with their vents on the upper chamfers. The pods' lower chamfers tuck in toward the scoop.
- **Centre**: the flipper panel (px x 175–385), the lettering at y ≈ 190–250, and the bend at y ≈ 120.
- **Top**: the hinge pin across px y ≈ 30–45 with knuckle stubs at the ends.
- **Silhouette**: a **broad "bulldozer" shape**: a wide low bumper, two shoulders, and a raised centre with a horizontal top line.

### 3.2 AWS70 (front, ≈ 25° above)
- The same arrangement. The vents show as **three slanted slots** in each pod (px (45–70, 50–100) and (240–265, 50–100)). The flipper's lettering is crisp at px y ≈ 120–150.

### 3.3 AWS72 (front three-quarter, ≈ 30° above, from the robot's right)
- The scoop's right end facet is large on the image left. The **left pod** (image right) shows its **front face**, **front-top chamfer**, **upper chamfer with three vents**, **outer vertical face** and **lower chamfer**. The flipper's **left edge** with a dark gap to the left pod is clear. The pin end stubs and both knuckles show at the top.

### 3.4 Top view (synthesised)
- A **92 × 80** rectangle (pods + flipper) with the hinge pin across the rear (y = −40), the flipper's two facets in the centre band (44 wide), the pods' top strips (x ±22 to ±33) and chamfer strips (±33 to ±46), and the scoop trapezoid ahead (102 front edge, 80 rear edge, 26 deep).

### 3.5 Side view (synthesised, never photographed)
- Pod profile: a box ≈ 70 long × 34 tall, with a chamfered front-top corner. The scoop ramp ahead of it (z 0 → 22 over 26 mm). The flipper's upper facet rising from the pod top at the front to the hinge at the rear (z ≈ 41), with the knuckle stubs above. The wheel (Ø 22) hidden inside the pod near the rear.

### 3.6 Rear view (never photographed; inferred)
- The two pods and the chassis rear wall, the knuckles and pin at the top centre. Possibly a switch.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| PD | hexagonal-section pod | 24 × 70 × 34 | 0.26 × 0.76 × 0.37 | yellow FDM | integral with CH (guess) | 2 |
| VT | slot | 2 × 10 | — | — | — | 3 per pod |
| CH | central tub | 44 × 75 × 30 | 0.48 | yellow FDM | — | 1 |
| SC | trapezoid scoop | 102 (front) / 80 (rear) × 26 × 22 | 1.11 × 0.28 × 0.24 | yellow FDM | integral or screws below (guess) | 1 |
| FL | two-facet plate with flanges | 44 × 75 (unfolded) × 6–8 edge | 0.48 × 0.82 | yellow FDM | hinge pin | 1 |
| TX | embossed text | 34 × 6 and 18 × 3.5, 1 high | — | yellow (integral) | — | 2 lines |
| HP | pin | Ø 3 × 58 | 0.63 | yellow (printed) or steel | through knuckles | 1 |
| HE | knuckle tab | 4 × 8 × 8 | — | yellow | integral with CH | 2 |
| WH | wheel (hidden) | Ø 22 × 8 | 0.24 | TPU (spec) | on the motor shaft | 2 |
| DM | micro gearmotor (hidden) | 10 × 12 × 26 | — | metal | in pod | 2 |
| SV | servo (hidden) | 23 × 12 × 25 | — | — | in CH | 1 |

---

## 5. Contact / gap matrix (estimated mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| PD inner face ↔ CH side | integral | 0 |
| FL side edge ↔ PD inner face | running gap | 1.5–2 |
| FL rear barrel ↔ HP | rotates on | 0 |
| HP ↔ HE knuckles | fixed or rotating | 0 |
| HE ↔ CH rear top | integral | 0 |
| FL-L front edge ↔ SC rear top edge | rests just behind/above | 0–2 |
| FL-U underside ↔ CH top / servo | rests on (down stop) | 0 |
| SC rear face ↔ PD front faces | integral or butted | 0 |
| SC front lip bottom ↔ floor | near | 0–1 |
| SC ends ↔ PD outer faces | scoop sticks out | +5 each side |
| PD bottom ↔ floor | clearance | ≈ 2 |
| WH bottom ↔ floor (hidden) | contact | 0 |
| WH outer face ↔ PD outer wall (hidden) | running gap | 1–2 |
| HE top ↔ PD top | stands proud | +4 to +6 |

---

## 6. Mechanism

1. **Flipper**: hinged at the **rear top** (HP at y −40, z 41). The servo lifts the **front edge** of the flipper, rotating it **up and back** about the pin. An opponent driven onto the scoop is pushed up the scoop's ramp onto the front facet; firing then raises the front facet and **lifts / tips the opponent upward and backward**. With a servo the action is a **lift and tip**, not a high-energy flip **(guess, high)**.
2. **Drive**: two wheels inside the pods, skid steer. Spec: Pololu HPCB 6 V 50:1 micro metal gearmotors. 50:1 on Ø 22 wheels gives ≈ 600 rpm × π × 22 mm ≈ **0.7 m/s**.
3. **Self-righting**: the hinge is at the top rear, and the flipper swings up and back, so if the robot lands upside down, firing the flipper pushes against the floor and could **roll it back over** **(guess, medium)**. The faceted pods also make the robot unstable when upside down, which helps self-righting.

---

## 7. Assembly order (suggested rebuild)

1. Print **CH + PD + HE** as one body (floor on the bed), with motor pockets in the pods and a servo bay in the centre. Print the **scoop** integral or separately.
2. Fit the **drive motors** into **plastic clamps / pockets** in the pods (shafts pointing outboard into the wheel cut-outs). Fit the **wheels**.
3. Fit the **servo** in the centre bay, horn pointing up under the flipper.
4. Install **battery, ESC, receiver, switch**. Route the wires.
5. Close the underside with a **floor plate** (screws from below, guess), or close the top through the flipper opening.
6. Place the **flipper**, thread the **hinge pin** through the knuckles and the flipper barrel, and cap the pin ends.
7. Attach the **scoop** if separate (screws from below).

---

## 8. Profiles as math (for rebuilding curves)

**8.1 Pod cross-section (XZ, right pod; mirror for the left), extruded along Y from −40 to +30.**
Polygon: (+22, 2) → (+36, 2) → (+46, 15) → (+46, 25) → (+33, 36) → (+22, 36) → close.
Upper chamfer: **z = 36 − (x − 33)·(11/13)** for x ∈ [33, 46] (≈ 40°). Lower chamfer: **z = 2 + (x − 36)·1.3** for x ∈ [36, 46] (≈ 52°).
Front-top chamfer: cut the pod by the plane through (y +30, z 28) and (y +22, z 36), i.e. **z + y = 58** for y ∈ [22, 30].
Vent slots: three slots 2 × 10 mm on the upper chamfer face, slot centres at y = +24, +20, +16; each slot runs down the chamfer from 2 mm below the top edge.

**8.2 Scoop SC.**
Side profile (YZ): (y +34, 0) → (+60, 0) → (+58, 7) → (+34, 22) → close. Lip facet from (60, 0) to (58, 7): **≈ 74°**. Ramp facet from (58, 7) to (34, 22): **z = 7 + (58 − y)·0.625**, slope **≈ 32°**.
Plan (XY): trapezoid (−40, +34), (+40, +34), (+51, +50), (+51, +60), (−51, +60), (−51, +50): end facets angled 55° from X between y = 34 and 50, then straight ends to the front.

**8.3 Flipper FL (YZ profile of the top surface, constant along X for x ∈ [−22, +22]).**
Upper facet: from the hinge (y −40, z 41) to (y −2, z 36): **z = 41 − 0.1316·(y + 40)** (≈ 7.5° down to the front).
Lower facet: from (−2, 36) to (+32, 12): **z = 36 − 0.706·(y + 2)** (≈ 35°).
Plate thickness 3 mm, with side flanges 6 mm deep along both edges.
Hinge barrel: circle centre (−40, 41), r = 4, with a Ø 3.2 bore.

**8.4 Lettering.** Raised 1 mm on the lower facet, "RIPPER" cap height 6, "REMIX" cap height 3.5.

---

## 9. Pixel-based measurements (independent check)

**AWS77 (552 × 539):**
- Scoop front edge: px x 35–525 = **490 px**. Scoop rear edge (top): px x 95–470 = 375 px.
- Pod pair outer extent: px x 60–500 = **440 px**. Flipper: px x 175–385 = **210 px**.
- Hinge pin: px y ≈ 35; scoop bottom: px y ≈ 480.
- Knuckles: px (150–165, 25–45) and (385–400, 25–45).

**AWS70 (304 × 343):**
- Scoop front: px x 15–285 = 270. Pods: px x 40–282 = 242. Flipper: px x 95–210 = 115.
- Hinge pin y ≈ 15; scoop bottom y ≈ 305.

**AWS72 (1239 × 1100):**
- Scoop: px x 110–860 front edge (oblique). Lip strip height ≈ 150–200 px at the image left (near), ≈ 70 px at the right.
- Flipper visible width at the lettering: px x 450–840.
- Hinge pin: from px (645, 50) to (1075, 175).

---

## 10. Several independent estimates of key quantities

| Quantity | Method A (spec / limits) | Method B (photo ratio) | Method C (second photo) | Reconciled |
|---|---|---|---|---|
| Pod-to-pod width | spec 92 | — | — | **92** |
| Scoop front width | spec 112 (too wide for the cube unless diagonal) | AWS77: 490/440 × 92 = **102** | AWS70: 270/242 × 92 = **103** | **102** |
| Flipper width | spec 44 | AWS77: 210/440 × 92 = **44** | AWS70: 115/242 × 92 = **44** | **44** |
| Pod width (each) | (92 − 44)/2 = 24 | AWS77: (440 − 210)/2 = 115 px → 24 | — | **24** |
| Overall height (hinge top) | spec 42 above its datum | AWS77: px 35 → 480 = 445 px, but includes ≈ 40% depth projection at 20° view → height ≈ 0.6 × 445 / 440 × 92 ≈ 56 (over-estimate; scoop front is nearer) | knuckle tops ≈ +5 above the pod tops; pods ≈ 36 → ≈ 41 | **42–45** |
| Scoop height | spec 24 | AWS77: scoop px 290–480 → 190 px, mostly the ramp seen from above at 20° | AWS72 lip 6–8 + ramp | **22** |
| Hinge pin length | — | AWS77: knuckle to knuckle 250 px → 52 | AWS72: ≈ 58 incl. stubs | **58** |

---

## 11. Consistency check: conflicts and reconciliation

1. **Scoop wider than the cube?** Spec 112 mm would not fit a 101.6 mm cube square-on. The photo ratio gives 102 mm. With a body length of ≈ 100 mm, a 102 × 100 footprint just fits the cube **diagonally in plan**, or the scoop is 101 and my ratio is 1% high. **Reconciled: 101 mm.**
2. **Overall length.** The spec scoop sits at y = +36…+72 with a chassis ±42.5, i.e. 114 mm overall, which exceeds the cube. The photos cannot measure length. With the cube limit, **body 72 mm + scoop 26 mm ≈ 98–100 mm**. **Reconciled: pods y ∈ [−40, +32], scoop y ∈ [+32, +58].**
3. **Blunt scoop lip.** A 6–8 mm steep lip is a poor wedge. In the photos the lighter lower strip could be a very steep facet or **a vertical bumper face**. Either way, the scoop is a **ramp for guiding opponents onto the flipper** rather than a razor wedge. **Accepted as photographed.**
4. **Wheels unseen.** The pods' lower chamfers come within ≈ 2 mm of the floor, which agrees with wheels hidden inside them and protruding 2 mm below. **Consistent with the spec.**
5. **Hinge at the top rear.** The pin is clearly at the top of all three images and above the pods, which with the camera elevated means it is at the **rear**. The spec's flipper profile (flat top running back, sloped front) matches. **Consistent.**

---

## 12. Why the designer did it (per part, mostly adversarial)

- **Faceted side pods**
  - Attacks: the angled upper and lower chamfers **deflect** hits from horizontal spinners and from opponents' wedges up or down rather than taking them square. A horizontal spinner hitting the lower chamfer is deflected downward into the floor; one hitting the upper chamfer is deflected over the top. They also protect the wheels completely, so a spinner cannot hit a tyre.
  - Getting under vs contact: the **lower chamfer tucks in**, so an opponent's wedge arriving from the side meets a slope that starts only 2 mm above the floor and has nothing vertical to hook. The wedge can lift the pod somewhat, but it cannot get under a wheel directly.
  - Weakness: the pods are wide and tall, a big target for vertical spinners; 3D-printed shells can crack.
  - Construction: one print, no supports (the chamfers are ≤ 45° overhangs at most), and smooth for a clean look.
- **Vent slots**: cooling for the drive motors, weight saving, and styling (they look like grilles on a car).
- **Full-width trapezoid scoop**
  - Getting under: the scoop is wider than the body, so the robot meets opponents with the scoop's corners even when slightly turned. The angled ends **deflect** opponents toward the centre, i.e. onto the flipper.
  - Attacks: the scoop is the first thing a vertical spinner meets; its sloped top deflects the spinner up and over. Its lip is thick enough to survive hits.
  - Weakness: a blunt lip loses wedge-vs-wedge contests against thin metal edges.
- **Rear-hinged flipper with two facets**
  - Weapon: a lifter/flipper that **rotates opponents up and back** over the robot.
  - The steep front facet is a **ramp continuation** of the scoop. An opponent pushed up the scoop rides onto it, putting their weight forward of the hinge, where the servo can tip them.
  - Attacks: the flipper is the centre of the top surface and can be hit by overhead weapons. It is not thick, but its sloped face deflects.
  - The exposed **hinge knuckles at the top rear** are a weakness: a hit there can bend the pin. They are, however, at the back, away from most attacks.
- **Embossed name**: branding, integral to the print (no stickers to peel off).
- **No visible screws**: a clean shell with fasteners **from below** means nothing on the exposed surfaces for opponents to catch on or strip.

---

## 13. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors DM | 2 × Pololu-style micro metal gearmotors (50:1, 6 V) | 10 × 12 × 26 + 9 shaft | in the pods along X, (±30, −25, 11) | medium (spec) |
| Motor mounts MM | printed **plastic clamps**: a pocket in the pod with a strap and 2 × M2 screws from below | 14 × 14 × 14 | over each motor | medium |
| Wheels WH | Ø 22 × 8 TPU tyres on printed hubs | Ø 22 | (±40, −25, 11) | medium |
| Flipper servo SV | high-torque micro servo (9–20 g, metal gears) | 23 × 12 × 25 | centre bay, output along X, (0, −10, 14) | high (type), low (position) |
| Link LK | servo horn acting directly on the flipper underside, or a short pushrod | 15 × 4 × 2 | (0, 0, 28) | low |
| Battery | 2S LiPo, 180–300 mAh | 35 × 18 × 10 | rear centre, (0, −28, 8) | medium |
| ESC | dual brushed ESC | 25 × 15 × 5 | front centre, (0, +18, 6) | low |
| Receiver | micro 2.4 GHz | 20 × 12 × 5 | (0, +8, 6) | low |
| Switch | slide switch on the rear wall or underside | 10 × 5 × 5 | (0, −40, 10) | low |
| Floor plate | printed or 1 mm polycarbonate floor screwed on from below with 4–6 × M2 | 92 × 70 × 1.5 | z 0.5–2 | low |
| Wires | battery → switch → ESC → motors; RX → ESC and servo | — | inside | high (exists) |

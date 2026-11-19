# Th'UNDER'er: full rebuild description from the reference photos

Source photos (three):
- `robots/th_under_er/reference/th_under_er.aws71.webp` (2047 × 1489 px): AWS 71. Cut out onto white with a **green cast** on dark parts. The camera is at the **front-right, high** (about 40° down). The straight front edge and the blade face the lower middle; the pointed rear rises to the top right.
- `robots/th_under_er/reference/th_under_er.aws72.webp` (1405 × 958 px): AWS 72. The same robot from the **front-left, high**. The blade is at the lower right and the pointed rear at the top left. The pods are a more **purple** shade of blue.
- `robots/th_under_er/reference/th_under_er.aws73.webp` (528 × 351 px): AWS 73. A small pit photo, taken from above in a clear plastic box. This is an **earlier/alternative build**: a **brushed aluminium top plate** over a black body, **purple pods**, **grey wheels**, and an **orange (plastic) test blade** under the front.

**Th'UNDER'er is a flat undercutter.** It is a horizontal spinner whose **hooked steel blade spins under the body**, just above the floor. The blade reaches out beyond the straight front edge, "under" the opponent (the name puns THUNDER / UNDER).
- The body is a **flat black printed pentagon**: a straight front bar 100 mm wide with **wheel pods** at both ends, and a pointed rear.
- A **white motor cap** with four socket screws sits on top at the middle of the front bar.
- The robot's name is painted in **orange capitals** across the top.

Facts are read from the photos; inferences are marked **(guess)**. Sizes are **estimates in mm**, from:
- the AWS limits (150 g, 101.6 mm cube);
- the spec draft (pods 24 × 40 × 18, wheels r 11 × 8, a hub disc r 16, a J-hook weapon about 62 × 110 in plan, wheels at y −24 of a hexagonal body);
- the **M2.5/M3 Phillips pan heads (≈ 5 mm)**, the **M3 socket heads (≈ 5.5 mm)** and the **M3 nut (5.5 AF)** as scales.

Ratios are against **W = overall width across the pods ≈ 100 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the **weapon axis**.
- **+X** = robot right, **+Y** = forward (the straight edge, where the blade reaches out), **+Z** = up. mm.
- In photo 71, robot right is the **image right pod** (lower right), because the camera is at the front-right. In 72, robot right is the image upper-right pod.
- Extents (reconciled §12):
  - front bar x ∈ [−50, +50], y ∈ [−12, +8];
  - pentagon body x ∈ [−34, +34], y ∈ [−12, −78], rear apex at (0, −78);
  - top z = 16 (plate top), body bottom z = 6;
  - pods z ∈ [0, 20];
  - blade plane z 2–5, swept radius 48 about (0, 0).

| ID | Part |
|---|---|
| TP | top plate (black printed, 2–3 mm, painted lettering, scratches) |
| BD | body walls / lower shell (black printed, layered sides) |
| FB | front bar section (narrow front of the plan, carrying the pods) |
| MB | motor bulge: rounded protrusion of the front edge around the weapon motor |
| MC | white motor cap: Ø 34 disc with 3 lugs, 4 central socket screws, 3 lug screws |
| PD-L, PD-R | blue printed wheel pods at the ends of the front bar |
| WH-L, WH-R | drive wheels: translucent ribbed TPU tyres on blue hubs |
| BL | weapon: a hooked steel undercutter bar with a balance hole |
| BP | bottom plate / blade guard disc under the motor (silver ring visible) |
| ST | threaded stud with nut and washer at the rear apex |
| SW | power switch slot with ON / OFF painted labels |
| S-TP | silver Phillips screws holding TP and the pods (10+) |
| S-PD | 2 silver Phillips screws with washers on each pod's front face |
| M-L, M-R, WM, BAT, ESC, WESC, RX | hidden motors and electronics |

---

## 1. Overall description in one paragraph

Th'UNDER'er is a **flat, wide, low undercutter**. Seen from above, it is shaped like a **house or shield pointing backward**:
- a **straight front bar** about 100 wide and 20 deep, ending in two **blue boxy wheel pods**;
- behind the bar, a **black pentagon** about 68 wide that tapers to a **pointed rear apex** about 78 mm behind the front edge.

The whole body is about **14 mm tall** (z 2 to 16). Its top is a scratched **black printed plate** with the robot's name painted in **orange stencil capitals** in an arc, "ON / OFF" labels by a **switch slot** at the front left, and a **threaded stud with a nut** at the rear apex.

At the **middle of the front edge**, the outline bulges forward around the **weapon motor**, which is capped on top by a **white disc** with three screw lugs and four socket screws.

Under the body, a **hooked steel blade** about 3 mm thick spins horizontally just above the floor. It reaches about 48 mm from the axis, so its **J-shaped hooked tip** sweeps **40 mm out in front** of the front edge, under any opponent that comes close.

The **wheel pods** are open-topped boxes. Each holds a **translucent ribbed tyre** that shows through a slot at the top, and has a **sloped front face** with two screws.

---

## 2. Part-by-part description

### 2.1 Top plate (TP) and body (BD)
- **Plan outline (TP)**, in robot coordinates:
  - front edge y = +8 from x −38 to +38;
  - the **motor bulge** MB, a semicircle of r 20 about (0, 0), protrudes to y = +20 between x ±18 (photo 71: the rounded black housing under the white cap at the front edge);
  - the bar runs back to y −12 at x ±38;
  - the pentagon flanks step out to x ±34, run back to y −40 and then converge in **two straight edges** to the rear apex (0, −78), with small **chamfers** at the shoulders (x ±34, y −40) (71: (1530–1640, 230–620));
  - the rear apex is **truncated** about 20 mm wide (71 top right (1220–1520, 90–170)), with a short raised **step** (the plate there is slightly higher).
- **Thickness**: TP is **2.5 mm**. Under it, the **body walls** are about **10 mm tall**, black printed with visible layer lines, giving a total height **≈ 14** (z 2 to 16).
- **Surface**: matt black PLA, **heavily scratched** in circular swirls (fight wear and arena dust). The name is painted in **orange** (paint pen) in an **arc** around the motor cap.
- **Lid seams**: in 71 the plate shows a **step/seam** along the front bar's rear edge and at the pods (a separate front-bar top piece screwed at its ends, with 2 screws each side).

### 2.2 Motor bulge (MB) and motor cap (MC)
- **MB**: a **cylindrical black housing**, Ø ≈ 40, 14 tall, centred on the weapon axis at (0, 0). It projects forward of the straight front edge as a half-cylinder (71: (700–1110, 520–820)). Its lower edge shows a **silver ring** (BP, the blade's bearing plate or a steel guard disc) about Ø 36.
- **MC**: a **white printed disc**, about **Ø 34 × 3**, with **three lugs**:
  - one at the image upper right (≈ 60° from +Y);
  - one at the front-left (≈ 160°);
  - one at the lower centre (≈ 280°).
- Each lug is about 8 wide, ends in a semicircle of r 4, and carries a **silver Phillips pan screw** into the body.
- **Four small socket (hex) screws**, M2.5, sit on a **Ø 18 square/rhombus pattern** in the centre. These fix the **weapon motor's stator** (an outrunner mounted upside down, its can spinning below) (guess, high).
- Next to the cap there is a **rectangular slot** about 10 × 4 (71: (1120–1180, 470–520)): a vent or wire pass.

### 2.3 Pods (PD-L, PD-R)
- **Shape**: blue printed **open boxes**, each about **24 (X) × 40 (Y) × 20 (Z)**, at the two ends of the front bar (x ±38 to ±62, but see §13 for the cube width). Features:
  - an **outer wall** 3 mm thick;
  - a **front face** that is **sloped** (about 20° back from vertical) with a **lip** at its top;
  - a **rear curved fender** over the wheel's rear;
  - a **top slot** through which the tyre shows.
- **Fastening**:
  - **two silver Phillips screws with washers** on each pod's **front face**, stacked vertically (71: left pod (255–300, 455–560), right pod (1280–1320, 1010–1130));
  - **two screws** on top at the joint with the body (71: (380, 350), (575, 235)).
- **Wear**: the left pod's front face has chewed edges in 72 ((300–330, 690–720)).

### 2.4 Wheels (WH-L, WH-R)
- **Shape**: **Ø 26 × 10**. The tyres are **translucent white-blue TPU** with **transverse ribs** (about 24 ribs around, 1.5 mm deep) on **blue printed hubs** with a raised rim.
- **Axes**: along X, inside the pods. Centres at **(±50, −2, 13)**, with the tyre bottom on the floor. The tyre tops show through the pod slots and stand **about 6 mm above** the pod rim.
- **73 variant**: grey rubber wheels, the same size.

### 2.5 Weapon blade (BL)
- **Material**: **steel**, about **3 mm thick**, satin-ground surface with machining marks. 73 shows an orange plastic blade (a practice blade or a pit placeholder).
- **Outline (plan, about the axis)**: a **single-tooth hooked bar**:
  - a **straight arm**, about **22 wide**, from the hub out to r ≈ 40;
  - then a **J-hook**: the arm curves round so that its tip points **back against** the arm, leaving a **concave throat** of r ≈ 14 (71 (960–1260, 1050–1250); 72 (930–1080, 640–850));
  - the leading face of the hook is a **straight chisel** about 25 long, with a **sharpened point** at r 48.
- Opposite the hook, a **short counter-arm** (r ≈ 25, hidden under the body) balances it.
- A **round hole Ø 7**, about 14 from the axis on the hook side (71: (1050–1110, 950–1000)), trims the balance (guess).
- **Plane**: z ≈ 2–5, about **2 mm above the floor**. It spins under the bottom of the body (z 6), which sits **4 mm** above the blade.
- **Direction**: the hook's point leads. In plan from above, the hook curls **clockwise** in 72, so the blade spins **clockwise seen from above** (guess, medium).

### 2.6 Bottom plate (BP)
- A **silver disc/ring**, about Ø 36, under the motor bulge (71: (720–1000, 770–830)). It is either the bottom of the outrunner's steel can, to which the blade is bolted, or a separate steel spacer.
- Read as: the outrunner can (or a steel hub) spins with the blade and is exposed under the bulge (medium).

### 2.7 Rear stud (ST)
- An **M3 threaded stud**, about 12 mm long, standing up from the **rear apex** with an **M3 hex nut** and a **washer** at its base (71: (1430–1500, 60–170); 72: (420–470, 30–100)).
- **Role (guess)**:
  - most likely a **body-clamp screw** reversed: the rear screw passes up through the bottom shell, the nut clamps the lid, and the excess length is left (low);
  - or a **lifting point / weapon-lock pin anchor** (low);
  - or an **aerial post** (low).

### 2.8 Switch (SW)
- A **rectangular slot** about 10 × 4 at the front left of the plate, near the left pod (71: (700–760, 240–300); 72: (330–360, 380–420)). It is the slide switch's actuator, labelled **"ON"** and **"OFF"** in orange paint on either side.

### 2.9 Screws (S-TP, S-PD)
- **Top plate**: silver Phillips pans at: pod joints (2 each side), the front bar's ends (2 each side), the white cap lugs (3), the rear corners (hidden in the photos but implied by the seam).
- **Count**: about **14 Phillips** plus **4 socket** screws visible.

---

## 3. Per-view descriptions

### 3.1 Top view (inferred from 71/72)
- A shield shape pointing backward. A 100 mm wide front bar with blue pods at the ends showing tyre slots. The white three-lug cap centred on the front edge's bulge. The orange name arching over the cap. The switch slot at the front left. The stud at the rear apex.
- The blade's hook projecting **in front** of the bulge when it is at the front, or hidden under the body otherwise.

### 3.2 Front view (inferred)
- A long low bar 14 tall. At the ends, the blue pods 20 tall with their sloped faces and two screws each. In the middle, the cylindrical bulge 14 tall with the white cap on top. Under everything, the thin blade line at z 2–5 reaching **96 mm** across when side-on.

### 3.3 Side view (inferred)
- A wedge-less flat profile: the pod (40 long, 20 tall) at the front, then the 14 tall body running back 66 mm to the apex. The blade a thin line under the front. The stud sticking up 12 mm at the rear.

### 3.4 Underside (inferred)
- A flat black bottom with a circular opening for the motor can. The blade below it. The wheels in the pods. **Rear skid** at the apex (a printed bump or a screw head; see §15).

### 3.5 Photo 73 (alternative build)
- The same plan with an **aluminium top plate**. The name is cut through or engraved ("TH'UNDER'ER" at the top). The motor cap is aluminium with 3 lugs, the pods purple, the wheels grey. An orange printed blade sticks out at the front left. The rear apex has a **white printed stud mount**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| TP | pentagon plate | 100 × 86 (incl. bar) × 2.5 | 1.0 × 0.86 | black PLA / Al (73) | ≈ 10 screws | 1 |
| BD | shell walls | 68 × 78 × 10 | 0.68 × 0.78 | black PLA | — | 1 |
| MB | half-cylinder | Ø 40 × 14 | 0.40 | black | integral | 1 |
| MC | lugged disc | Ø 34 × 3 (+3 lugs r 21) | 0.34 | white PLA | 3 Phillips + 4 socket | 1 |
| PD | open box | 24 × 40 × 20 | 0.24 × 0.40 × 0.20 | blue PLA | 2 front + 2 top | 2 |
| WH | ribbed wheel | Ø 26 × 10 | 0.26 | translucent TPU / blue hub | motor shaft | 2 |
| BL | J-hook bar | 48 r × 22 wide × 3 | 0.48 | steel | to motor can | 1 |
| BP | disc | Ø 36 × 2 | 0.36 | steel | — | 1 |
| ST | stud + nut | M3 × 12 | — | steel | nut | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| WH ↔ floor | contact | 0 |
| rear skid ↔ floor | contact (light) | 0 |
| BD bottom ↔ floor | clearance | 6 |
| BL bottom ↔ floor | clearance | 2 |
| BL top ↔ BD bottom | clearance | 1–2 |
| BL tip sweep r 48 ↔ PD inner walls (x ±38) | clearance in plan: the blade passes **under** the pods? | see §13 |
| PD bottom ↔ floor | clearance | 1 |
| WH ↔ PD walls | clearance | 1.5 |
| MC ↔ TP | screwed | 0 |
| BP/can ↔ BL | bolted | 0 |
| ST ↔ TP | nut-clamped | 0 |

---

## 6. Mechanism

1. **Drive**: two wheels at the **front corners**, skid steer. The rear apex drags on a skid or a small low-friction point. With the wheels at the front and the weapon axis between them, the robot turns about the weapon, which keeps the blade's sweep centred on the target while turning.
2. **Weapon**: an **inverted outrunner** with its stator screwed under the white cap. The can spins below the body carrying the blade, so the **blade is the lowest part of the robot** apart from the wheels and skid.
   - A **single hook** stores energy at r 40–48 and hits once per turn with full bite.
   - Mass ≈ 7.85 × (area ≈ 14 cm²) × 0.3 ≈ 33 g.
   - I ≈ (counting the hook as a point at r 40 with about 18 g, and the arm) ≈ 0.018·0.04² + (1/3)·0.015·0.04² ≈ 3.7 × 10⁻⁵ kg·m².
   - At 9000 rpm (942 rad/s): E ≈ 16 J, tip speed ≈ 45 m/s. This is large for an antweight. A 22–28 mm outrunner on 3S can reach it.
3. **Undercutting**: the blade hits opponents **below their armour**, at their wheels, wedge edges and undersides, and flips or lifts them because the hook digs in from under.

---

## 7. Assembly order (suggested rebuild)

1. Print the bottom shell with pockets: battery at the rear pentagon, ESCs beside it, drive motors in the front bar, and the weapon motor pocket at the front centre.
2. Fit the N20 drive motors along X in the front bar, with shafts out to the pods. Fit the wheels.
3. Screw on the pods (2 top + 2 front screws each).
4. Fit the electronics and the switch (slider up through the slot).
5. Mount the weapon motor upside down: stator to the white cap with 4 socket screws, the cap to the body with 3 lug screws. The can comes out through the bottom opening.
6. Bolt the blade (and BP) to the can from below.
7. Screw on the top plate. Fit the rear stud/nut.
8. Paint the name and the ON/OFF labels.

---

## 8. Hidden / uncertain list
- The underside layout, the rear skid and the bottom opening.
- The blade's counter-arm and its full outline (only the hook side is seen).
- The blade spin direction.
- The rear stud's purpose.
- Whether the pods are part of the bottom shell or separate (they are read as separate because of their colour and screws).
- Sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin under the weapon axis. +X right, +Y forward, +Z up. mm.
- Front edge y +8 (bulge to +20). Pods x ±[38, 62] (see §13 for the reconciled ±[26, 50]), y [−22, +12], z [0, 20]. Wheels (±38, −4, 13).
- Pentagon to the apex (0, −78). Blade z 2–5, r 48 about (0, 0). Stud at (0, −72, 16–28).

## 10. Profiles as math

**10.1 Plan outline (TP), reconciled (§13).**
- Front edge y = +8, |x| ≤ 50 (pods to the ends).
- Bulge: x² + y² = 20², y ≥ 8.
- Pods' rear edge y = −22 for 26 ≤ |x| ≤ 50.
- Body flank x = ±34 for −40 ≤ y ≤ −22.
- Rear edges: |x| = 34·(y + 78)/38 for −78 ≤ y ≤ −40, truncated at |x| ≤ 8 near y −78.

**10.2 Blade (plan, polar about the axis).**
- Hub circle r 14.
- Arm: a band of half-width 11 along θ = 0 from r 14 to r 38.
- Hook: the outer edge continues as an arc of r 48 (about the axis) for θ ∈ [0°, 25°]. Then the inner throat is an arc of r 14 centred at r 36 on θ 15°, giving the J. The tip is a 30° point.
- Counter-arm: a band of half-width 10 along θ = 180° to r 26, with a round end.
- Hole: Ø 7 at r 14, θ 0°.
- Thickness 3.

**10.3 Motor cap.** Disc r 17. Lugs: three circles of r 4 centred at r 21, θ ∈ {60°, 160°, 280°}, joined to the disc by tangent lines. Central screws at (±6, 0) and (0, ±6) (a rhombus).

**10.4 Pod.** Box 24 × 34 × 20. Front face plane: y = 12 − 0.36·(20 − z) (20° slope). Fender: arc of r 16 about the wheel axis over the rear half.

**10.5 Wheel tyre.** r(φ) = 13 − 0.75·(1 − cos(24φ)), giving 24 ribs 1.5 mm deep.

## 11. Pixel-based measurements

- **71 (2047 × 1489)**:
  - overall pod-to-pod extent: left pod outer (45, 330) to right pod outer (1960, 900); about 1950 px diagonal;
  - motor cap Ø: (680–1140, 380–660), 460 px wide;
  - Phillips head: about 40 px;
  - blade: (930–1270, 860–1250);
  - stud: (1430–1500, 60–170).
- **72 (1405 × 958)**: cap (570–870, 285–490), 300 px. Pods: left (35–430, 400–860), right (960–1360, 195–590). Blade (780–1080, 600–860). Phillips head about 28 px.
- **73 (528 × 351)**: plate (100–480, 20–300).

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/known) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Scale (72) | Phillips M3 pan 5.5 | — | 28 px → 5.1 px/mm | 5.1 px/mm (mid-depth) |
| Cap Ø | hub disc r 16 → 32 | 0.34 W | 72: 300 px / 5.1 = 59 (incl. lugs, oblique) → disc alone ≈ 200 px → 39 | **34 disc, 42 over lugs** |
| Overall width | ≤ 101.6 | 1.0 W | 72: pods outer 35 → 1360 = 1325 px / (5.1 × 2.5 for perspective) | **100** |
| Wheel Ø | 22 (r 11) | 0.26 W | 72: tyre about 130 px / 5.1 ≈ 25 | **26** |
| Body height | 14–18 | 0.14 W | 72: front face below the plate about 70 px / 5.1 ≈ 14 | **14** |
| Pod height | 18 | 0.20 W | 72: 110 px / 5.5 ≈ 20 | **20** |
| Blade reach beyond edge | — | — | 72: hook tip about 230 px from the bulge ≈ 40 (oblique) | **≈ 28–40** |
| Length (front to apex) | — | ≤ 101.6 | 71 diagonal ≈ 85 | **86 incl. bulge** |

## 13. Consistency check: conflicts and reconciliation
1. **Width vs pods**: if the front bar is 76 wide plus two 24 mm pods, the total is 124, which is over the cube. **Reconciled**: the pods are **at** the ends of a 100 mm bar, so x ∈ ±[26, 50], and the wheels are centred at x ±38. The pentagon flanks at x ±34 lie **inside** the pods' outer edges, which matches photo 72 where the body's side is roughly level with the pod's inner wall.
2. **Blade vs pods**: a blade of r 48 about (0, 0) sweeps out to x ±48, which crosses the pods' footprint (x 26–50, y −22 to +12). The blade must pass **under the pods** (pod bottom z ≥ 6) or be shorter than 26 where it passes them.
   - **Reconciled**: the pods' **bottom faces are open/raised** under their inner halves (z 6). The wheels sit in the outer halves and only touch the floor at x ±38. The blade at z 2–5 passes under the pods' inner halves.
   - The hook tip (r 48) would still meet the **wheels** at x ±38, y −4: the distance from the axis is √(38² + 4²) ≈ 38, which is less than 48. **Conflict.**
   - **Final**: the blade radius is **r 34** (hook tip), and the blade reaches 14–20 mm beyond the bulge. Or the axis is further forward than the wheels.
   - Photo 72 shows the hook tip about 30 mm in front of the bulge. With the bulge at y +20, that gives tip y ≈ +50, so r ≈ 50 in the forward direction. That only works if the wheels are **behind** the blade disc: wheels at y −40 (clearance √(38² + 40²) = 55 > 50).
   - **Final reconciliation**: the **wheels and pods sit further back** than they look, at y ≈ −30 (pods y [−48, −12]), and the weapon axis is at the front centre with r 46. Photo 71's perspective (pods at the image ends, "level with" the cap) is consistent with this, because the cap lies closer to the camera.
   - **Use**: pods y ∈ [−48, −12]; wheels (±38, −30, 13); blade r 46 about (0, 0); front edge y +8; apex y −78 becomes y −70, keeping the length under 101.6 with the blade inside the box at rest (the blade does not count once it spins, but the rest pose must fit).
3. **Mass** (§17): within 150 g.
4. The spec's wheels at y −24 match this reconciliation (behind the weapon axis).

---

## 14. Why the designer did it (per part, adversarial first)

- **Under-body blade (undercutter)**
  - Fight: the blade sits **2 mm off the floor**, below every opponent's armour. It hits wedge lips, wheel bottoms and fork tips from underneath. Wedges are the natural enemy of horizontal spinners, but against an undercutter **"getting under" is impossible**: the lowest thing in the arena is the spinning steel. A wedge that drives in has its lip cut or is thrown upward.
  - The flat body above the blade is a roof that the opponent hits after being lifted.
  - Threats: the blade is exposed on the arena floor, so seams and screw heads can catch it. Inverted, the blade is on top and useless. Vertical spinners can hit the flat top plate (which is scratched all over).
- **Single J-hook tooth**
  - Fight: one tooth gives the longest bite time per revolution (the opponent can move deep into the sweep before the tooth comes round). The hook drags rather than glances, pulling the target's edge down and outward. The balance hole and counter-arm keep it smooth.
- **Flat, low body (14 mm)**
  - Fight: a vertical spinner or drum needs to get under an edge. With 6 mm clearance and a spinning blade in front, there is no edge to reach from the front. From the sides and rear, the body's low height leaves little for a vertical spinner to bite.
- **Pentagon with a pointed rear**
  - Fight: the angled rear faces deflect rear attacks sideways rather than taking them square. The point also drags lightly on the floor as a third contact without a castor.
- **Wheel pods**
  - Fight: the pods' **sloped front faces** deflect hits upward and away from the tyres. The two screws on each face make them quick to replace. The open tops let the tyres reach above the pods so the robot **drives inverted** (the tyres stand about 6 mm above the pod rims).
  - Threats: the pods are the widest points and the first thing horizontal spinners hit. They are separate and replaceable for that reason.
- **White motor cap with 7 screws**
  - Fight: the motor is clamped from above by a wide plate that spreads the blade's reaction impulse into the body over three lugs. The socket screws into the stator are short and accessible from the top, so the weapon can be changed without opening the robot.
- **Rear stud**
  - Construction/fight (guess): a long screw left proud at the rear could be a handle for safe lifting (pick-up point away from the blade), which is useful for an undercutter whose blade is hard to avoid when lifting from the front.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Weapon motor | 2205–2806 outrunner, upside down, can below | Ø 28 × 16 | (0, 0, 8) | high |
| Weapon ESC | 20–30 A | 25 × 13 × 5 | (−14, −40, 9) | medium |
| Drive motors | 2 × N20 along X | 12 × 10 × 25 | (±18, −30, 11) | medium |
| Drive ESC | dual brushed | 20 × 15 × 4 | (+14, −40, 9) | medium |
| Battery | 3S 300 mAh | 45 × 17 × 9 | (0, −55, 9) along X | medium |
| Receiver | micro | 18 × 12 × 4 | (0, −66, 10) | low |
| Switch | slide switch | 12 × 6 × 6 | (−22, −8, 10) | high |
| Rear skid | printed bump or screw head | Ø 6 × 2 | (0, −70, 1) | medium |
| Wiring | battery → switch → ESCs → motors | — | — | high |

## 16. Variant notes (71 / 72 / 73)
- **73 (earliest?)**: aluminium top plate, a purple pod colour, grey rubber wheels, an orange printed blade. This is a lighter, possibly testing configuration. The aluminium plate makes the top stiffer against vertical spinners.
- **71/72**: an all-printed black top with painted lettering (cheaper to replace), blue/purple pods with translucent TPU ribbed tyres (more grip for pushing), and a steel hook blade.
- The pod colour changes between 71 (blue) and 72 (purple), which suggests the pods were reprinted between events after damage.

## 17. Mass budget (est. g)

| Item | Mass |
|---|---|
| Blade (3 mm steel) | 30 |
| Weapon motor | 22 |
| Body shell + top plate + cap | 32 |
| Pods × 2 | 10 |
| Drive motors × 2 + wheels | 26 |
| Battery 3S 300 | 25 |
| Electronics + switch | 12 |
| Screws, stud, wires | 8 |
| **Total** | **≈ 165** |

This is over 150 g, so savings are likely: a 2S pack (−10 g), a thinner blade (2.5 mm, −5 g) or thinner walls. The result is about 148 g.

## 18. Matchups
- **Vs wedges**: the undercutter's best matchup. The wedge's lip meets the blade first. The weak spot is the **rear**: if a wedge reaches the side or rear, the 6 mm clearance under the flat body lets it under. The pointed rear and quick skid steer about the weapon axis help it face forward.
- **Vs horizontal spinners**: blade-on-blade at different heights. The undercutter is lower and hits the opponent's base, but the pods take the opponent's blade.
- **Vs vertical spinners/drums**: the opponent wants to get under the front. It meets the blade, which hits the drum's lower edge. A tall vertical blade can reach over and hit the top plate (the scratches are probably from this).
- **Vs pushers**: a fast pusher with a strong front can absorb the hit and push. The low weapon has no lifting action except through the hook.

## 19. Wear reading
- Circular scratches all over the top plate (71): hits from vertical spinners, and dragging upside down.
- Chewed front edges of the pods (72): blade impacts.
- The blade's chisel edge is bright and slightly rounded (71), showing use.
- Paint lettering intact: the top plate may have been replaced between events.

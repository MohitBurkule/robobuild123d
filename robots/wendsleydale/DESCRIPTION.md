# Wendsleydale: full rebuild description from reference photos

Source photos (all small, soft pit photos; only `aws65` and `aws68` have masks):
- `robots/wendsleydale/reference/wendsleydale.aws63.webp` (373 × 424 px). AWS 63. The robot is **held in two hands** on a white table, someone working on it with a **screwdriver**. Seen from the **left side, slightly front and above (≈ 25–30° down)**, front to the **left**. The **flipper is raised** (about 70–80° up): a **blue arm with a channel-shaped curved spine** rising from the rear and ending in a **T-shaped front plate** at the upper left. Shows the **clear polycarbonate left side plate** (a wedge-profiled quadrilateral with black screws), the **left rear wheel** (black tyre, grey/blue hub), **orange brackets** by the wheel, a **white wire loop** behind the side plate, **red** parts inside the body.
- `robots/wendsleydale/reference/wendsleydale.aws65.webp` (545 × 421 px, wooden table). AWS 65. Seen from the **rear-left, high (≈ 40–45° down)**, rear at the **lower left**, front at the **upper right**. The flipper is **down**. Best view of the **rear**: the **rear centre housing** (servo box) with a **rectangular opening**, both **rear wheels** with **orange fenders** above them, the **two top pods** with black screws, the **curved spine** of the flipper lying along the centre, the **right clear side plate** with the wheel hub seen through it and an orange bracket, and **silver strips** at the far (front) edges of the pods.
- `robots/wendsleydale/reference/wendsleydale.aws68.webp` (605 × 576 px, cream table, plastic box behind). AWS 68. Seen from **above and in front (≈ 60–70° down)**, front at the **bottom**, rear at the **top**. Best view of the **top layout**: the two pods with screws and **orange front pads**, the **flipper spine** down the centre and the **full-width front plate** with **two small tabs**, the **clear side plates** on both sides projecting forward, and the **orange fenders** at the rear corners.

Everything stated as fact is read from these photos; the images are small and soft, so small features (screw counts, exact edges) are approximate. Inferences are marked **(guess)** with a confidence. Dimensions are **estimates**. Scale anchors: (1) the AWS 101.6 mm cube (the robot fills it in width: side plate to side plate ≈ 96 mm); (2) the **rear wheels** (black treaded tyres, Ø ≈ 26–28 mm, a common N20 wheel); (3) the black **M2 / M2.5 pan / button screws** (head Ø ≈ 4 mm). Reference **W = width over the side plates ≈ 96 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the centre of the robot's plan footprint (side-plate front tips to the rear face; between the side plates).
- **+X** = robot's right, **+Y** = forward (toward the flipper's front plate), **+Z** = up; mm. Flipper angle α = rotation of the flipper about its hinge axis (X), 0 = lying down (rest), positive = front lifting.
- Envelope (flipper down): x ∈ [−48, +48], y ∈ [−48, +52], z ∈ [0, 32].

| ID | Part |
|---|---|
| CH | blue printed chassis (floor, inner walls, rear housing) |
| RH | rear centre housing (servo box) with rectangular opening (RHO) |
| POD-L / POD-R | blue top pods (fixed lids) either side of the flipper, each with a flat rear and a sloped front |
| OP-L / OP-R | orange pads on the pods' sloped fronts |
| ST-L / ST-R | silver strips at the pods' front edges (AWS65) |
| SP-L / SP-R | clear polycarbonate side plates (wedge profile) |
| S-SP | black screws along the side plates |
| S-P | black screws in the pods and pads |
| FL | flipper: spine arm (FLS) + front plate (FLP) + tabs (FLT) |
| FH | flipper hinge (at the rear, on the servo output) |
| SV | flipper servo (hidden; silver horn/gear glimpsed in RHO) |
| WH-L / WH-R | rear drive wheels |
| FD-L / FD-R | orange fenders (wheel guards) over the rear wheels |
| OB | orange brackets on the side plates by the wheels (motor clamps) |
| DM-L / DM-R | drive gearmotors (hidden) |
| WR | white wire loop (AWS63), red parts (AWS63) |
| BAT, ESC, RX, SW | electronics (hidden) |

---

## 1. Overall description in one paragraph

Wendsleydale is a **two-wheel, rear-drive, servo-powered front-hinged-at-the-rear flipper ("lifter lid")** antweight. It is a **low wedge about 96 mm wide, 100 mm long and 30 mm tall**, printed in **blue** with **orange** accent parts and **clear polycarbonate side plates**. The top is split lengthwise into **three strips**: a **left pod** and a **right pod** (fixed blue lids, each about 30 mm wide, with black screws, a **flat rear half** and a **front half sloping down** to the front, finished with an **orange pad**) and, between them, the **flipper**: a **blue arm with a curved, channel-shaped spine** about 32 mm wide that runs from a **hinge at the rear centre** forward over the body and ends in a **full-width front plate** that lies at the bottom of the wedge between the side plates, with **two small tabs** on its front edge. The two **clear side plates** have a **wedge profile**: sharp floor tips at the front, a sloping front edge, a flat top and black screws along their edges. **Two rear wheels** (Ø ≈ 27 mm, black treaded tyres, grey/blue hubs) sit just inside the side plates at the rear corners, roofed by **orange fenders**, and a **blue box at the rear centre** houses the **servo** whose output drives the flipper. When fired (AWS63) the arm swings up about the rear hinge to ≈ 75°, lifting the front plate to well above the robot.

---

## 2. Part-by-part description

### 2.1 Chassis (CH) and rear housing (RH)
- **Chassis**: a blue printed **tray** between the side plates, **≈ 92 mm wide (x −46…+46) × 96 mm long (y −48…+48)**, floor ≈ 2 mm at z 2–4 (ground clearance ≈ 2 mm). Internal walls form two side bays (under the pods) for the electronics and drive motors, and a central channel for the flipper.
- **Rear face**: flat and vertical at y −48, from z 2 to z ≈ 26 at the centre, with the wheel openings at the corners.
- **Rear housing RH**: a **blue box at the rear centre**, between the wheels, **≈ 34 mm wide (x −17…+17) × 22 mm long (y −48…−26) × 26 mm tall**, with **rounded top-rear edges (r ≈ 6)** and **layer lines running across**. Its rear face has a **rectangular opening RHO ≈ 20 × 9 mm** at mid-height (z 10–19), through which a **silver metal part** shows (a metal servo horn / output gear or the hinge pin) and a dark cavity (AWS65). On top it merges into the flipper's spine root (the spine sits on/over it).
- **Colour / material**: matt **blue PLA** (two shades: a light sky blue in AWS65, a deeper royal blue in AWS63/68 — lighting/white balance or reprints).

### 2.2 Pods (POD-L, POD-R), pads (OP), strips (ST), screws (S-P)
- **Shape**: two **flat blue lids** forming the top either side of the flipper, each **≈ 30 mm wide** (POD-L x −46…−16, POD-R x +16…+46), from the rear (y −46) to the front lip of the wedge.
  - **Rear half**: flat, horizontal, at **z ≈ 26**, from y −46 to y ≈ +2.
  - **Front half**: a **plane sloping down to the front at ≈ 28–32°**, from the **crease** at y ≈ +2 (visible as a straight line across each pod in AWS68 at about 55 % of the pod's length from the rear) down to the front edge at **y ≈ +40, z ≈ 6**.
  - The crease line is slightly further forward on the right pod than on the left in AWS68 (perspective) → treat as symmetric.
- **OP (orange pads)**: on the lower part of each sloped front, a **rectangular orange block ≈ 28 × 16 mm, ≈ 3 mm thick**, its front edge at the pod's front edge, fixed with **2–3 black screws** (AWS68 left pad: 2 screws at the left and right of its lower half; right pad: 2 screws plus one at the upper left). Probably **TPU or PETG** wear pads / **rest stops for the flipper plate** **(guess: rest stops and wear pads, medium)**.
- **ST (silver strips)**: in AWS65, along the pods' **front edges** (far end of the pods from that camera), **silver/grey strips ≈ 3–4 mm wide** glint: either **aluminium angle / steel strip** lips on the pod fronts or the **edges of the clear side plates / polycarbonate seen edge-on** **(guess: the pads' front edges are capped with a metal strip in the AWS65 build, low)**.
- **S-P**: each pod has **4 black screws** in its flat rear half: two near the rear (y ≈ −36, at x ±22 and ±36) and two at mid-length (y ≈ −10 at x ±24 and ±38, AWS68 shows one pair near the crease at the outer edge) plus the 2–3 in its pad. In AWS65 the left pod shows screws at (rear-outer), (rear-inner), (mid-inner); the right pod at (mid-inner, mid-outer, front-outer, front-inner). **Total ≈ 8 + 5 = 13 black pan screws, head Ø ≈ 4.**
- **Fixing**: the screws go into the chassis walls / bay walls below, so the pods are **removable lids** for access.

### 2.3 Side plates (SP-L, SP-R) and screws (S-SP)
- **Material**: **clear polycarbonate**, ≈ **2 mm thick**, scratched, with bright cut edges.
- **Profile (YZ, the same on both sides)**: a quadrilateral:
  - **front tip** on the floor at **(y +52, z 0)**: a **sharp point** (AWS63 left plate: a needle-sharp tip at the lower left);
  - **front edge** rising **back and up at ≈ 35°** to the **top-front corner** at (y +12, z 28);
  - **top edge** horizontal at **z ≈ 28** (2 mm above the pods) back to (y −36, z 28);
  - **rear edge** down to (y −36, z 6), rounded corner r ≈ 4;
  - **bottom edge** horizontal at z ≈ 2 from (y −36) forward to the tip.
  The plate ends **≈ 2 mm in front of the wheel centre** at the rear → the rear half of each wheel is **not covered by the plate** (AWS63/65: the tyre sticks out behind the plate's rear edge).
- **Position**: outer faces at **x ±48**, inner faces at ±46: they are the outermost parts, outside the wheels.
- **S-SP**: **black pan screws (M2/M2.5)** along the plate's **top edge**, ≈ 6 at 13–15 mm spacing (AWS63 shows 5–6 along the top edge, AWS68 shows 4–5 along each plate's edge) and **2 near the bottom edge** at the front, screwing into the chassis' side walls / the pods' edges.
- **Projection**: in AWS68 the plates **project forward of the flipper plate's front edge by ≈ 10–12 mm** (their tips are the frontmost points), forming **wedgelets/ forks** either side of the flipper plate.

### 2.4 Flipper (FL: spine FLS, front plate FLP, tabs FLT) and hinge (FH)
- **Spine FLS**: a **blue channel-shaped arm ≈ 32 mm wide (x −16…+16)**, **≈ 3 mm thick**, with a **convex curved top** (its top surface is a smooth curve seen in AWS68 by the curving layer lines and in AWS65 as a raised hump). In side view (AWS63, raised), the spine is **curved like a shallow "S"/banana**: from the hinge it rises, bends, then runs straight to the front plate; total length from hinge to front plate ≈ **85 mm**. The spine's **sides** (channel walls) are ≈ 10 mm tall at the rear, tapering to ≈ 4 mm at the front, so the spine is stiff in bending.
  - At rest it lies in the **central channel** between the pods, its top **level with or ≈ 4 mm above** the pods (AWS65: a slight hump above the pods at the rear-mid, the flat pods either side), following the same **flat-rear / sloped-front** profile as the pods.
  - In AWS65, near the rear, the spine has a **step / notch** (a rectangular cut ≈ 14 × 4 mm across its top at y ≈ −8, AWS68 at about 1/3 from the rear: a short slot/ridge) **(guess: a clearance slot for a screw head or the servo linkage)**.
- **Front plate FLP**: a **flat blue plate** across the front, **≈ 88 mm wide (spanning between the side plates' inner faces with ≈ 2 mm clearance each side), ≈ 12–14 mm long (along the slope), ≈ 3 mm thick**, joined to the spine's front end in a **T**. At rest it lies **at the bottom of the wedge** in front of the pods' orange pads, sloping down at the same ≈ 30° to its **front edge on the floor** at y ≈ +44. In AWS63 (raised) the T's crossbar is seen nearly end-on at the upper left: the crossbar shows a **step** at its left end.
- **Tabs FLT**: **two small rectangular tabs ≈ 6 mm wide × 4 mm long** project forward from the front plate's front edge at **x ≈ ±32** (AWS68: at about 15 % in from each end), probably **thin lips that slide under opponents** **(guess, medium)** or **hinge leaves** for a separate lip **(low)**.
- **Hinge FH**: at the **rear centre**, at about **(y −38, z 22)**, axis along X, inside/at the top of the rear housing RH: the spine's rear end is fixed to the **servo output horn / a hinge pin**. When fired (AWS63) the spine's rear end rotates about this point and the front plate goes up and over.
- **Travel**: from 0° (rest) to **≈ 75–90°** (AWS63 shows ≈ 75°, front plate high above the body at z ≈ 85–90).

### 2.5 Servo (SV), hidden
- **Guess (medium-high)**: a **standard-size or mini metal-gear servo** (e.g. 23 × 12 × 29 mm micro, or a 40 × 20 × 38 standard is too big; so a **micro/mini high-torque servo** such as MG90S / DS929MG / a 25 g digital servo), lying with its output shaft along X at the hinge, in the rear housing, its body forward of it inside the central channel under the spine. The **silver part seen through RHO** is the servo's **aluminium horn** or a metal-gear clamp **(medium)**.
- Torque: 2–3 kg·cm at 6 V → force at the front plate (85 mm) ≈ 0.25–0.35 kg: a **lifter / self-righting flipper** rather than a high-energy flipper.

### 2.6 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 27 mm × 10 mm**. **Tyre**: black rubber with **circumferential grooves / tread blocks** (AWS65 shows a grooved tread), ≈ 4 mm thick, rounded shoulders. **Hub**: **grey plastic** disc with a **blue centre** (AWS63: a grey hub ≈ Ø 18 with a small blue/orange centre boss; the blue may be the printed coupler).
- **Position**: centres at **(x ±40, y −34, z 13.5)**; outer face x ±45 (just inside the side plate, 1 mm gap), inner face x ±35. Top at z 27 (under the fender). Bottom on the floor.
- **Exposure**: covered on the outside front half by the clear plate, on top by the orange fender; exposed at the rear and under.

### 2.7 Orange fenders (FD-L, FD-R)
- **Shape**: **orange curved shells** over the top-rear of each wheel, about **24 mm long (X, across the wheel width + margin) × 16 mm (Y) × 3 mm thick**, curved to follow the tyre (a **quarter-cylinder** of inner radius ≈ 15 about the wheel axle) and spanning **from the pod's rear-outer corner to the side plate**. Their top surface shows **ribs** (layer lines across) and in AWS65 they look like **orange rollers**. AWS68 shows them at the rear corners above the wheels, their outer ends touching the side plates.
- **Material**: **orange PLA/PETG or TPU** **(guess: TPU, low)**.
- **Purpose**: wheel guards (stop the tyre from being hit from above/behind and keep debris out) and **rear bumpers**.

### 2.8 Orange brackets (OB) and drive motors (DM)
- **OB**: on each side plate, just **ahead of and above the wheel hub**, an **orange vertical bar ≈ 4 × 6 × 20 mm** (AWS63: at the left plate, a vertical orange strip with **two black screws** at its top and bottom, plus a second orange part above the wheel; AWS65: the same on the right plate). It is **inside the clear plate** (seen through it) **(guess: the printed motor clamp that holds the N20 gearbox, screwed through the plate, medium)**.
- **DM (hidden)**: **2 × N20 gearmotors**, along X, at y −34, z 13.5, shafts outward into the hubs; motors pointing inward, side by side either side of the rear housing / servo body **(high)**.

### 2.9 Wires and other visible items
- **WR (AWS63)**: a **white wire loop** (thin, ≈ 1 mm) visible **behind the left side plate** near the front-bottom (between the plate and the chassis), and a short **orange/red** wire near it: probably the **receiver antenna** or a **switch lead** **(guess)**.
- **Red parts (AWS63)**: in the gap under the raised flipper, **red components** inside the body: **red battery leads / connector / red-cased servo** **(guess)**.
- **Switch**: not seen. **Guess (low)**: a slide switch under a pod lid, reached through a hole in the side plate.

---

## 3. Per-view descriptions

### 3.1 Top view (AWS68)
- A near-square outline. Left and right: thin clear side plates (edges catch the light), projecting forward past the front plate to sharp tips. Inside them: the two blue pods, each with a flat rear half (with screws) and a front half beyond a crease line, finished with an orange pad (2–3 screws) at the front. Centre: the flipper spine (32 wide) from the rear to the front, its layer lines curving; at the bottom (front) the full-width front plate with two small tabs. At the top (rear) corners: the orange fenders over the wheels; the rear housing hidden under the spine's root.

### 3.2 Rear-left view (AWS65)
- Lower left: the rear housing (blue box with rounded top and a dark rectangular opening with a silver part inside), the left wheel to its left with an orange fender above, the right wheel to its right. Above: the two pods and the central spine hump; the right clear side plate on the right with the wheel hub seen through it and an orange bracket; silver strips at the far edges.

### 3.3 Left side view, flipper raised (AWS63)
- The clear left plate: a wedge-profile quadrilateral from a sharp tip at the left to the wheel at the right, black screws along its top edge, an orange bracket and the grey hub of the left wheel at the rear, the black tyre behind the plate's rear end, a white wire loop inside. Above: the raised blue flipper arm going from the rear (by the hands) up-forward to the T plate at the upper left; red items inside the body under it.

### 3.4 Front view (inferred)
- A low wedge: the full-width front plate on the floor between the two sharp side-plate tips, the pods' sloped fronts with orange pads above it, the spine's front curve in the centre, the flat pod tops at z 26 behind; the side plates' top edges at z 28 at the sides. Wheels hidden behind.

### 3.5 Rear view (AWS65 closest)
- Rear housing in the centre (34 × 26) with its opening; wheels either side (Ø 27) with orange fenders above them; the pods' rear edges and the clear plates at the extremes.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 96 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | tray | 92 × 96 × 24 | 0.96 × 1.0 | blue PLA | — | 1 |
| RH | rounded box | 34 × 22 × 26 | 0.35 | blue | integral | 1 |
| POD | flat + sloped lid | 30 × 86 × 2.5 | 0.31 | blue | 4 screws each | 2 |
| OP | pad | 28 × 16 × 3 | 0.29 | orange | 2–3 screws | 2 |
| SP | wedge quadrilateral plate | 88 long × 28 tall × 2 | 0.92 | clear PC | ≈ 8 screws each | 2 |
| FLS | curved channel spine | 32 × 85 × 3 (walls 10→4) | 0.33 × 0.89 | blue | servo horn | 1 |
| FLP | flat plate | 88 × 13 × 3 | 0.92 | blue | integral with FLS | 1 |
| FLT | tab | 6 × 4 × 1.5 | — | blue | integral | 2 |
| WH | treaded wheel | Ø 27 × 10 | 0.28 | black / grey hub | N20 shaft | 2 |
| FD | quarter-cylinder fender | 24 × 16 × 3 | 0.25 | orange | screws / clip | 2 |
| OB | bracket bar | 4 × 6 × 20 | — | orange | 2 screws | 2 |
| S-P, S-SP | pan screws | M2/M2.5, head Ø 4 | — | black | into blue walls | ≈ 30 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| SP tips ↔ floor | contact | 0 |
| SP bottom edge ↔ floor | above (rear) | 2 |
| FLP front edge ↔ floor (rest) | contact / near | 0–1 |
| FLP ends ↔ SP inner faces | clearance | 2 |
| FLS sides ↔ POD inner edges | clearance (channel) | 1–2 |
| FLS top ↔ POD tops (rest) | spine proud at the rear | +2…+4 |
| FLP back edge ↔ OP front edges | rest stop | 0–1 |
| POD ↔ CH | screwed | 0 |
| SP ↔ CH / POD edges | screwed | 0 |
| SP top edge ↔ POD tops | plate proud | +2 |
| WH outer face ↔ SP inner face | running clearance | 1 |
| WH top ↔ FD underside | clearance | 1–2 |
| WH bottom ↔ floor | contact | 0 |
| WH rear ↔ rear face plane | about flush | 0 |
| FD ↔ SP / POD | fastened | 0 |
| RH ↔ CH | integral | 0 |
| FLS rear end ↔ servo horn (FH) | screwed | 0 |
| OB ↔ SP | screwed through | 0 |

---

## 6. Mechanism

1. **Wedge**: the low front (side-plate tips at the floor, the flipper plate lying at the floor between them, pods sloping at ≈ 30°) gets under opponents; the sharp clear tips act as **forks** that slide under first.
2. **Flipper / lifter**: the servo at the rear rotates the spine about the rear hinge (y −38, z 22). The front plate, 85 mm from the hinge, rises along an arc: height z(α) ≈ 22 + 85 sin(α − 12°) (the plate starts ≈ 12° below the hinge line), lifting an opponent sitting on it by **≈ 60 mm at 75°**. Servo speed (≈ 0.1 s/60°) gives a **lift, not a throw**: the purpose is to **tip opponents over and to self-right**.
3. **Self-righting**: upside down, the robot rests on its pod tops (z 26 → flat). Swinging the flipper fully (beyond 90°) pushes the front plate against the floor and rolls the robot over backwards onto its wheels **(guess, high: this is why rear-hinged servo lifters are built)**.
4. **Drive**: 2WD rear-wheel skid steer; the front plate and the side-plate tips are the front skids. Not designed to drive inverted (the side plates' top edges at z 28 stand above the wheel tops at 27 → upside down the wheels barely touch); relies on self-righting.

---

## 7. Assembly order (suggested rebuild)
1. Print the **blue chassis tray** (with rear housing and bay walls), the **two pod lids**, the **flipper** (spine + front plate in one print), and the **orange** pads, fenders and brackets. Cut the two **clear PC side plates** and drill them.
2. Fit the **servo** in the rear housing / central channel, its output shaft along X at the hinge.
3. Fit the **two N20 gearmotors** in the rear bays, clamped by the **orange brackets** (screwed through the side plates later), and push the **wheels** on.
4. Fit the **battery, ESC/receiver** (with antenna) and **switch** in the side bays under the pods.
5. Screw the **side plates** onto the chassis sides (and through the orange brackets).
6. Fit the **flipper**: screw the spine's rear end to the servo horn; check that at rest the front plate lies on the floor between the side-plate tips and against the orange pads.
7. Screw the **pod lids** on (4 screws each), add the **orange pads** (2–3 screws each) and the **orange fenders** over the wheels.

---

## 8. Hidden / uncertain list
- The flipper's exact side profile and hinge point (only seen raised and blurred in AWS63).
- Servo type and how the spine fixes to it.
- What the silver strips (AWS65) and the tabs (AWS68) are.
- Whether the orange brackets are motor clamps.
- Electronics layout, switch.
- All dims ±15–20 % (small photos).

## 9. Coordinate frame (restated)
Origin on the floor under the plan centre; +X right; +Y forward; +Z up; mm. Flipper hinge axis: line (y −38, z 22) along X. Wheels at (±40, −34, 13.5), Ø 27 × 10. Side plates at |x| = 46…48, tips at (y +52, z 0). Pod tops z 26, crease at y +2, front edge (y +40, z 6).

## 10. Profiles as math

**10.1 Side plate (YZ).** Polygon: T = (52, 0) → (12, 28) → (−36, 28) → (−36, 6) [fillet r 4 at (−36, 28) and (−36, 6)] → (−36, 2) → (40, 2) → T. Front edge: z = 28 · (52 − y)/40 for y ∈ [12, 52] (slope 35°).

**10.2 Pod top profile (YZ, for |x| ∈ [16, 46]).** z(y) = 26 for y ∈ [−46, 2]; z(y) = 26 − (y − 2)·tan 28° for y ∈ [2, 40] → z(40) = 5.8. Orange pad: on the slope from y 26 to 40 (16 mm along the slope projected), thickness 3 normal to the slope.

**10.3 Flipper spine (in the flipper frame at α = 0, i.e. rest).** Centre-line from the hinge H = (−38, 22): straight to (−20, 28) (rising 18°), then along z = 28 (top surface 30) to y = +2, then down the slope parallel to the pods (28°) to the front plate at y ≈ +34, z ≈ 13; front plate continues the slope to its front edge at (y +44, z 0). Section: a channel 32 wide, web 3, side walls of height h(s) = 10 − 6 s/85 (s along the spine). Top surface convex across: z_top = z_c + 2 · (1 − (x/16)²).

**10.4 Flipper arc.** For a point P at polar coordinates (ρ, β) about H in the YZ plane (β from +Y), its position at flipper angle α is H + ρ (cos(β + α), sin(β + α)). Front plate's front edge: ρ = √(82² + 22²) ≈ 85, β = −15°; at α = 75° → (y −38 + 85 cos 60°, z 22 + 85 sin 60°) = (y +4.5, z 95.6).

**10.5 Fender.** Quarter-cylinder shell, inner radius 15, thickness 3, about the wheel axle (y −34, z 13.5), spanning angles 60°–150° from +Y, width (X) 24, centred over the wheel.

**10.6 Wheel.** Tyre annulus r ∈ [9.5, 13.5], width 10, with 3 circumferential grooves 1 mm wide.

## 11. Pixel-based measurements
- **AWS68 (605 × 576)**: side plate to side plate ≈ 495 px at the front (x 60 → 555); pods ≈ 175 px (left x 65–240) and ≈ 160 px (right x 390–550); spine ≈ 150 px at mid-length (x 245–395); front plate y 395–455; tabs at x ≈ 95–110 and 485–500; crease lines at y ≈ 255 (left) and 270 (right); orange pads ≈ 160 × 85 px (left) and 165 × 85 (right); screw heads ≈ 12–14 px.
- **AWS65 (545 × 421)**: rear housing ≈ 110 px wide (x 130–240); left wheel ≈ 70 × 100 px; right wheel ≈ 60 × 110 px; fenders ≈ 85 × 40 px; overall robot ≈ 490 px across the diagonal.
- **AWS63 (373 × 424)**: side plate from tip (5, 345) to rear (≈ 235, 330) ≈ 230 px; plate top-front corner ≈ (45, 290); wheel tyre ≈ 70 px tall, hub ≈ 45 px; raised arm from (270, 210) to the T at (40–130, 20–160): ≈ 280 px.

## 12. Several independent estimates

| Quantity | Method A (W = 96 over plates, AWS68 495 px → 5.15 px/mm at the front) | Method B (wheel Ø 27, AWS63 70 px → 2.6 px/mm) | Method C (screws Ø 4, AWS68 13 px → 3.3 px/mm) | Reconciled |
|---|---|---|---|---|
| Pod width | 175/5.15 = 34 (near the front) | — | 175/3.3 = 53 (inconsistent → screws are smaller: M2 head 3.8 → 3.4 px/mm…) | **30** |
| Spine width | 150/5.15 = 29 | — | — | **32** (top at rear wider in perspective) |
| Side plate length | — | 230/2.6 = 88 | — | **88** |
| Overall length | — | plate 88 + wheel rear beyond plate (−36 → −48) = 100 | — | **100** |
| Rear housing width | AWS65: 110 px / (490 px diag ≈ 135 mm → 3.6 px/mm) = 30 | — | — | **34** |
| Arm length (hinge → front plate) | — | 280/2.6 ≈ 108 (the arm is closer to the camera, held up → inflated) | — | **85** |
| Height (pod top) | — | AWS63: plate top 28 ≈ 1.0 × wheel Ø | — | **26–28** |
| Front plate width | ≈ 470 px / 5.15 = 91 | — | — | **88** |

## 13. Consistency check
1. **Screw scale**: method C gives pods 53 mm, impossible inside 96 mm with a 30 mm spine. The screws must be **M2 pan heads Ø 3.5–3.8**, still giving ≈ 46: the screw heads in a soft 600 px photo are ±3 px (±25 %). **Discard method C**; use W.
2. **Arm length vs body**: hinge at y −38 and front plate edge at y +44 → 82–85 mm, consistent with the spine spanning ≈ 90 % of the body length in AWS68. **Consistent.**
3. **Flipper raised height**: at 75° the front edge reaches z ≈ 96 — AWS63 shows the T plate far above the body (≈ 3 body heights). **Consistent.**
4. **Width budget**: plates 2 × 2 + pods 2 × 30 + spine 32 → 96; wheels 10 wide inside the pods' footprint (x ±35…±45). **Consistent.**
5. **Length vs cube**: tips y +52 to rear y −48 → 100 mm < 101.6. **Consistent.**
6. **Mass**: chassis + pods + flipper 50 g (PLA), PC plates 2 × 6 g, orange parts 6 g, servo 14–25 g, 2 N20 + wheels 24 g, battery 2S 300 mAh 18 g, dual ESC 5 g, RX 4 g, screws 8 g, wires 4 g → **≈ 145–150 g. Consistent (tight → micro servo ≈ 14 g).**

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Rear-hinged full-length servo flipper with a full-width front plate**
  - Getting under: the front plate lies **on the floor at the front**, so the whole front is a wedge that also is the flipper: anything that drives onto it is directly over the lifting surface. Full width means opponents cannot slip past the plate's ends.
  - Attack: a long lever from a rear hinge gives a large lift height (≈ 60–70 mm) from a small servo rotation, enough to **tip opponents onto their backs**, and the robot can then push them.
  - Adversarial: a servo is light and simple (no gas, no spring), and doubles as the **self-righting** mechanism. A rear hinge keeps the arm's pivot away from front impacts.
  - Channel-section spine: stiff in bending for a 3 mm print; the convex top deflects hits.
- **Fixed pods either side**: removable lids for easy access to electronics in each side bay; the sloped fronts continue the wedge so the whole front works as a ramp, even when the flipper is up.
- **Orange pads**: protect the pods' front edges where opponents hit, and give the flipper plate a hard stop at rest so it stays at the floor.
- **Clear polycarbonate side plates with sharp tips**: PC is tough (it bends rather than shatters) and lets the builder see the drivetrain; the sharp forward tips act as **forks** that get under opponents' side skirts before the plate; the plates also take side hits from horizontal spinners and protect the wheels' outer faces.
- **Rear wheels inside the plates with orange fenders**: shielded from the side and above; at the rear they push the wedge in, and with the hinge and servo also at the rear the weight sits on the drive wheels, which gives traction for pushing.
- **Rear housing for the servo**: protects the servo's output and hinge from hits from behind; the opening gives access to the horn screw.
- **Colours** (blue, orange, clear): team styling; the clear plates show off the internals.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Flipper servo | micro/mini metal-gear servo (e.g. MG90S-class, 13–25 g), output along X | 23 × 12 × 29 (+ ears) | body at (0, −20, 12), output at (0, −38, 22) | medium |
| Servo horn | aluminium or plastic horn screwed to the spine's rear end | Ø 20 | (±6, −38, 22) | medium |
| Hinge pin | an M3 pin through the spine and RH's side walls on the side opposite the servo output | M3 × 40 | axis (y −38, z 22) | low |
| Drive motors | 2 × N20 (50:1–100:1) along X | 12 × 10 × 25 | (±24, −34, 13.5) | high |
| Motor clamps | orange printed straps (OB) | 4 × 6 × 20 | at the plates | medium |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 10 | left bay (−30, +4, 10) | medium |
| ESC + receiver | combined AIO board (e.g. Malenki / DasMikro) with servo output | 25 × 20 × 6 | right bay (+30, +4, 10) | medium |
| Switch | slide switch in a bay wall, reached through the side plate | 12 × 4 × 6 | (+44, −10, 10) | low |
| Antenna | white wire looped inside the left side plate (AWS63) | — | (−45, +20, 8) | medium |
| Wiring | battery → switch → AIO → motors + servo (red leads seen) | — | inside | high |

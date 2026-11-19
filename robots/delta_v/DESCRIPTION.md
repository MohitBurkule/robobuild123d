# Delta V: full rebuild description from reference photos

Source photos (all cut out onto white by the AWS wiki; black parts carry a **green colour cast**, strongest in AWS74, which is not a real colour):
- `robots/delta_v/reference/delta_v.aws72.webp` (1287 × 1061 px): AWS 72. Camera at the **front-left**, about 35° down; the robot's **left** side and side plate face the camera (image left). Front fitted with **four short barbed steel forks** (two per pod). Best for the **left bearing hub** (silver ball bearing, threaded shaft end and nut), the **black four-lug clamp flange** on the disc and the **pods with eyes and pockets**.
- `...aws74.webp` (1366 × 962 px): AWS 74. Camera at the **front-left**, about 30° down. Front fitted with **two long barbed steel forks** at the outer corners on **narrow tapered pods**. Best for the **left side plate** and the **wheel**.
- `...aws76.webp` (1609 × 1367 px): AWS 76. Camera at the **front-right**, about 25° down; the robot's **right** side faces the camera (image right). Front fitted with a **full-width flat clear/green wedge blade**. Best for the **right weapon tower** (D-shape, four socket screws), the **outrunner bell**, the **hex nuts** clamping the disc, the **white switch** and the **right side plate**.

Facts come from the photos; inferences are marked **(guess)**. Sizes are **estimates in mm**, from the AWS 150 g / 101.6 mm cube limit and pixel ratios (the AWS76 blade width is the main scale). Ratios are against **W = body width over the side plates ≈ 72 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the body footprint (side plate to side plate; rear wall to the front faces of the pods, forks/blade excluded).
- **+X** = robot right, **+Y** = forward, **+Z** = up. mm. Side-profile angles measured from the floor.
- Body extents: x ∈ [−36, +36], y ∈ [−34, +34], z ∈ [2, 24]. Weapon axle at (y +3, z 41). Tooth tip radius 31 mm. Forks/blade to y ≈ +46 (AWS76 blade), +56 (AWS72 forks), +74 (AWS74 forks).

| ID | Part |
|---|---|
| BD | black main body (rear block) |
| LD-L, LD-R | inset top lid panels on the rear block |
| SPL-L, SPL-R | black stadium-shaped side plates (wheel guards) |
| WH-L, WH-R | rear drive wheels (yellow sponge tyres) |
| PD-L, PD-R | front wedge pods (wide in AWS72/76, narrow tapered in AWS74) |
| PK | oval pockets on the pods' lower facets (screw access) |
| EY-L, EY-R | "sleepy eye" stickers on the pods' upper facets |
| SLT | weapon slot between the pods, continuing back into the body |
| TW | right weapon tower (D-shaped motor mount) |
| OR | outrunner motor (black bell) |
| DS | yellow single-tooth hooked weapon disc |
| CF | black four-lug clamp flange on the disc's left face |
| HB | left hub boss with ball bearing (rotates with the disc, guess) |
| SH | dead shaft / bolt, threaded end and nut on the left |
| S-DS | 4 bolts + hex nuts through CF, DS and the bell |
| S-TW | 4 black socket screws + centre hole on TW's outer face |
| FK72 | 4 short barbed forks (AWS72) |
| FK74 | 2 long barbed forks (AWS74) |
| BLD | full-width flat wedge blade (AWS76) |
| SW | white switch / connector, rear right top |
| BL | blue part under the left lid edge (AWS76; battery wrap or receiver, guess) |
| S-LD, S-SPL, S-PD | small black screws: lids, side plates, pods |
| M-L, M-R, BAT, ESC, WESC, RX | hidden drive motors and electronics |

---

## 1. Overall description in one paragraph

Delta V is a **compact black vertical spinner with a cartoon face**. The body is a low, flat black box about 72 mm wide, 68 mm long and 22 mm tall, in two parts: a **rear block** carrying the electronics under two inset lids, and two **front wedge pods** whose sloped faces carry round **"sleepy eye" stickers**, so that the front looks like a drowsy face. Between the pods a **slot** runs back into the body. Above the slot, a **yellow single-tooth disc** with one big **hooked tooth** (with a triangular window) spins on a transverse axle about 41 mm above the floor. The disc is bolted to a **black outrunner bell** whose stator is fixed to a **D-shaped black tower** standing on the right of the body; on the disc's left face a **black four-lug clamp flange** ends in a **hub boss with a silver ball bearing** riding on the shaft's threaded end. Two **yellow sponge-tyred wheels** sit at the rear corners behind **stadium-shaped black side plates**. The front edge is interchangeable: **four short barbed steel forks** (AWS72), **two long barbed forks on narrow pods** (AWS74), or a **full-width clear/green wedge blade** (AWS76).

---

## 2. Part-by-part description

### 2.1 Rear block (BD)
- **Shape**: a black box, **64 mm wide (between the side plates) × 40 mm long (y −34 to +6) × 22 mm tall (z 2 to 24)**. The top is flat. Wall thickness about **2.5 mm (guess)**. The front of the block meets the pods at y ≈ +6.
- **Wheel notches**: at the rear top corners, **notches about 10 mm wide × 20 mm long** let the wheel tops show above the body (AWS72, AWS74: the yellow wheel visible above the side plate at the rear left).
- **Slot continuation**: the weapon slot (24 mm wide) continues into the block's front as a pocket about 14 mm long (y −8 to +6), open at the top, so the hub's lower part and the tooth can pass **(AWS76 shows the slot's dark floor behind the pods)**.
- **Colour/material**: matt black PLA/PETG with fine layer lines; scuffs on the tower and top.

### 2.2 Lids (LD-L, LD-R)
- **Shape**: two **inset flat panels**, each about **24 × 34 × 2 mm**, recessed about 0.5 mm into the block top either side of the tower/slot area. A thin seam separates each from the block top (AWS72 shows the left lid as a slightly raised rectangle with a seam all round).
- **Fasteners**: **2–4 small black pan/Phillips screws** (head Ø about 3 mm, M2): AWS72 shows two at the left lid's rear corners and two along its outer edge; AWS74 shows two at the rear left; AWS76 shows one at the right lid's front outer corner and one behind the switch.
- **Details**: on the right lid's rear part, a **white rectangular switch/connector SW** (about **8 × 5 × 4 mm**) in a cut-out (AWS76). Under the left lid's front edge a **blue** part shows (AWS76: a blue edge at (470, 520) px), probably **battery wrap or a receiver case** **(guess)**.

### 2.3 Side plates (SPL-L, SPL-R)
- **Shape**: **stadium** plates (a rectangle with two semicircular ends), **60 mm long × 24 mm tall × 3 mm thick**, end radius 12. In plate coordinates (Y, Z): the union of the rectangle y ∈ [−18, +18], z ∈ [0, 24] and circles centred (±18, 12), r = 12.
- **Position**: outer faces at x = ±36; spanning y ∈ [−34, +26] (the front end overlaps the pods' rear by about 20 mm); bottom at z ≈ 1.
- **Screws S-SPL**: **3–4 small black screws** per plate: top-front (y +15, z 20), middle (y 0, z 12), bottom-rear (y −20, z 5), and sometimes top-rear (AWS74 shows 3 on the left; AWS76 shows 2–3 on the right, one at the upper front at (1395, 690) px and one low at (1210, 995)).
- **Function**: wheel guards covering the wheels' outer faces. The wheel's outer face sits about **1 mm** inside the plate.

### 2.4 Wheels (WH-L, WH-R)
- **Shape**: **Ø 28 × 8 mm**. The tyre is a **yellow/cream sponge** (open-cell foam look, granular surface) or speckled yellow TPU. The hub has **3 round holes** (Ø about 5, on a radius of 7) and a central boss.
- **Position**: centres (±29, −20, 14). Tops at z = 28 (4 mm above the body top, through the notches); bottoms at z = 0.
- **Drive**: one N20-class gearmotor per wheel inside the rear block **(guess)**.

### 2.5 Front pods (PD-L, PD-R), AWS72/76 (wide)
- **Shape**: a prism with a two-facet sloped top. Each pod is **24 mm wide (X) × 28 mm long (Y)**. Back height 24 (flush with the block top). Upper facet from y +6 to +14 sloping about **20°** (it carries the eye); lower, steeper facet from y +14 to +34 sloping about **35°** down to the front face at z ≈ 6. YZ polygon: (6, 2) → (6, 24) → (14, 21) → (34, 7) → (34, 2).
- **Position**: PD-L x ∈ [−36, −12], PD-R x ∈ [+12, +36]. The inner faces bound the slot.
- **Pockets PK**: each lower facet has **3 oval pockets** (about **7 × 5 mm**, 2 mm deep): two in the upper row, each with a **black Phillips screw** at its bottom (fixing the forks/blade from above), and one lower pocket, empty (a fork-slot access hole, or a screw removed). AWS76 shows the same pattern: two screws plus an empty pocket on the left pod, two screws plus one empty on the right pod.
- **Pod/blocks joint**: a horizontal seam at about z = 17 crosses each pod's front (AWS72 and AWS76), which suggests the pod is made of **two printed layers** (an upper cap with the eye, and a lower wedge) or is a separate part screwed on **(guess)**.

### 2.6 Front pods, AWS74 (narrow tapered)
- **Shape**: each pod is tapered in plan toward a **chisel nose at the outer front corner**, pointing at its single long fork. Plan: back width 24, front tip width about 8 at x ≈ ±32. The sloped top continues down to the fork root at z ≈ 6, y ≈ +38.
- **Screws**: two small screws on each pod's sloped face (AWS74 at (580, 580) and (700, 570) px on the left pod).

### 2.7 Eye stickers (EY-L, EY-R)
- **Shape**: round stickers **Ø 10–11 mm**: a white disc with a black outline, a **black half-moon pupil** in the lower half, and a thick **black horizontal "eyelid" line** across the middle, giving a sleepy look. One on each pod's upper facet at x ±24. AWS76 shows them shiny (laminated with clear tape); AWS74's left eye is partly torn.

### 2.8 Weapon slot (SLT)
- A **24 mm wide** gap (x ∈ [−12, +12]) between the pods, from y +34 back to y −8 inside the block; open at the top. The floor of the slot is open or cut, so the tooth can pass at its lowest point (z ≈ 10).

### 2.9 Right tower (TW)
- **Shape**: a **D-shaped upright**: a rectangle 18 mm (Y) × 20 mm (Z) with a semicircle of r 9 on top, **14 mm thick (X)**. It stands on the block top at x ∈ [+12, +26], y ∈ [−6, +12], rising from z 24 to z 53.
- **Outer face**: a **4-hole bolt circle** (PCD about 12 mm) of **black socket-head screws** (M2–M2.5) around a **centre hole** (Ø about 5 mm), centred at (y +3, z 41): the **outrunner stator mount** (the stator is bolted to the tower's inner face; the screws come in from outside). Scratches and white scuffs on the tower face (AWS76) show it is hit often.
- **Function**: the only fixed support of the weapon (a cantilever).

### 2.10 Outrunner (OR)
- **Shape**: a black **cylindrical bell Ø 28 × 12 mm** (a 22xx-size outrunner), coaxial with the axle, x ∈ [0, +12], between the disc and the tower. It is visible in AWS76 as a black drum ring between the yellow disc and the tower.

### 2.11 Weapon disc (DS)
- **Shape**: a **flat plate, 3 mm thick**, made of a **hub circle of r 18** centred on the axle plus **one large hooked tooth**. Polar outline (angle θ in the disc frame, measured in the direction of rotation backward from the hook face):
  - r(θ) = 18 for θ ∈ [70°, 360°];
  - for θ ∈ [0°, 70°] the back edge rises along r(θ) = 18·e^(0.0078·θ) (a log-spiral from r 18 at θ = 70° back to r 31 at θ = 0);
  - at θ = 0 the **hook face** returns from the tip (r 31) to the hub circle with a **concave arc of radius 12**, so the tip leans forward (a raked hook).
  - A **triangular lightening window** near the tip, vertices at (r 22, θ 8°), (r 27, θ 4°), (r 26, θ 22°), with rounded corners (AWS72, AWS76).
- **Colour**: **yellow** (painted/powder-coated steel or anodised aluminium; lime-green in AWS74's cast), with dark chipped edges and a black ink mark on its rim (AWS76).
- **Clamping**: 4 bolts on a PCD of about 16 mm pass through the black clamp flange CF, the disc and the bell; **hex nuts** on the bell side (AWS76 shows 4 hex nuts at the disc's right face, at roughly 90° spacing).
- **Plane**: vertical, at x ≈ −2 to +1 (just left of centre, in the slot).

### 2.12 Clamp flange (CF) and hub boss (HB)
- **CF**: a **black printed (or aluminium) four-lug flange** on the disc's left face, **outer size about 26 × 26 mm** with four rounded lugs carrying the bolt heads, and a raised **ring** in the middle.
- **HB**: a **black cylinder, Ø 18 × 10 mm**, projecting from CF's centre toward −X, with a **steel ball bearing** (Ø about 10 mm, silver race and seals visible) pressed into its outer face; the **threaded end of the shaft** (M4 **guess**) protrudes about 4 mm from the bearing, with a **nut**.
- **Reading**: the motor is a **dead-shaft** outrunner: the shaft bolt is fixed in the tower; the bell, disc, flange and hub boss rotate together on the shaft, supported by the motor's own bearings on the right and by **HB's bearing on the left**, with the nut clamping the bearing's inner race **(guess, medium)**. No fixed left pillar is visible in any photo.

### 2.13 Front variants
- **FK72 (AWS72)**: four **steel strips, 4 mm wide × 1.5 mm thick**, flat, protruding about **22 mm** from slots at the bottom of the pods' front faces, at x = −30, −16, +16 and +30 (two per pod, one at each pod corner). Each tip has a **barb**: the strip widens to about 7 mm with a step about 6 mm from the end, then ends in a **chisel point** (a sawtooth-shaped tip, bevelled on top). The strips lie flat on the floor, sloping about 5° down from the pod.
- **FK74 (AWS74)**: two strips at x = ±32, protruding about **40 mm**, with the same barbed chisel tips; they emerge from the noses of the tapered pods.
- **BLD (AWS76)**: a **flat plate about 72 × 18 × 1.5–2 mm**, **clear with green-tinted edges** (polycarbonate or glass-fibre sheet), heavily scratched along its front third. It lies at about **15° below horizontal** under both pods and across the slot, front edge at y ≈ +46 on the floor. The **front corners are chamfered** about 10 × 45° (AWS76: the right end angles back). It is held by the pod pocket screws (4 screws).

---

## 3. Per-view descriptions

### 3.1 Top view (plan)
- A 72 × 68 rectangle: the rear block (40 long) with two lid panels and the wheel tops showing at the rear corners; the two pods (24 wide each) with eyes; the 24 mm slot between them running back to y −8.
- The tower: a 14 × 18 block at x +12 to +26, y −6 to +12; between it and the slot, the bell (12 thick) and the disc (3 thick line, 49 mm long including the tooth); the hub boss (Ø 18, 10 thick) left of the disc.
- In front: four short fork lines (AWS72), two long ones at the outer corners (AWS74) or a 72 × 12 blade strip (AWS76).

### 3.2 Front view
- Two pods (24 wide) at the sides with eyes; the slot in the middle showing the disc edge-on (3 mm) rising to z ≈ 72 at the tooth tip; behind, the tower on the right and the hub boss with its silver bearing on the left. The side plates at the outer edges. Forks or blade at floor level.

### 3.3 Right side view (AWS76)
- The stadium side plate (60 × 24) with 2–3 screws, the wheel top above it at the rear, the D-tower above the body with its 4 screws, and the disc behind with the hooked tooth up (tip about z 72). The pods slope down to the front; the blade sticks out below.

### 3.4 Left side view (AWS72/74)
- The left side plate with the wheel at the rear; above the body, the hub boss with its silver bearing and nut in front of the black clamp flange on the yellow disc; the tower behind the disc.

### 3.5 Rear view (inferred)
- A flat black wall 64 × 22 with the side plates and wheels at the corners; the tower's round top and the disc above. The switch is reached from the top.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | box | 64 × 40 × 22 | 0.89 × 0.56 × 0.31 | black PLA | — | 1 |
| LD | inset plate | 24 × 34 × 2 | 0.33 × 0.47 | black | 2–4 × M2 | 2 |
| SPL | stadium plate | 60 × 24 × 3, R 12 | 0.83 × 0.33 | black | 3–4 screws | 2 |
| WH | wheel | Ø 28 × 8 | 0.39 | yellow sponge, black hub | motor shaft | 2 |
| PD | 2-facet wedge | 24 × 28 × 22 | 0.33 × 0.39 | black | integral/screwed | 2 |
| PK | oval pocket | 7 × 5 × 2 | — | — | — | 6 |
| EY | sticker | Ø 10.5 | 0.15 | white/black | adhesive | 2 |
| TW | D-upright | 14 × 18 × 29 | 0.19 × 0.25 × 0.40 | black | integral | 1 |
| OR | bell | Ø 28 × 12 | 0.39 | black | 4 × M2 to TW | 1 |
| DS | hooked disc | hub r 18, tip r 31, 3 thick | 0.68 (envelope Ø 49) | yellow | 4 bolts + nuts | 1 |
| CF | 4-lug flange | 26 × 26 × 3 | 0.36 | black | bolts | 1 |
| HB | boss with bearing | Ø 18 × 10 | 0.25 | black + steel | on CF | 1 |
| SH | shaft / bolt | Ø 4 × 40 | — | steel | nut | 1 |
| FK72 | barbed strip | 22 × 4 × 1.5 | 0.31 | steel | pod slots + screws | 4 |
| FK74 | barbed strip | 40 × 4 × 1.5 | 0.56 | steel | pod slots + screws | 2 |
| BLD | flat plate | 72 × 18 × 1.5 | 1 × 0.25 | clear/green sheet | 4 screws | 1 |
| SW | switch | 8 × 5 × 4 | — | white | in a lid cut-out | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| BD bottom ↔ floor | clearance | 2 |
| WH bottom ↔ floor | contact | 0 |
| FK/BLD tips ↔ floor | contact | 0 |
| LD ↔ BD | inset, screwed | 0 |
| SPL ↔ BD side | screwed | 0 |
| SPL inner ↔ WH outer | clearance | 1 |
| WH inner ↔ BD side wall | clearance | 2 |
| WH top ↔ BD top | wheel above | +4 |
| PD back ↔ BD front | joined | 0 |
| PD inner faces ↔ DS faces | slot clearance | ≈ 10 each side |
| DS ↔ OR bell | bolted | 0 |
| DS ↔ CF | clamped | 0 |
| OR stator ↔ TW | bolted | 0 |
| OR bell ↔ TW inner face | running clearance | 0.5–1 |
| HB ↔ SH (via bearing) | concentric | 0 |
| DS hub (lowest, z 23) ↔ BD top / slot | just above / inside the slot pocket | 0–1 |
| DS tooth (lowest, z 10) ↔ slot floor | clearance | 5–8 |
| DS tooth tip (forward reach y +34) ↔ pod front plane | level | 0 |
| FK/BLD ↔ PD underside | clamped | 0 |
| TW base ↔ BD top | joined | 0 |
| SW ↔ LD-R | in cut-out | 0 |

---

## 6. Mechanism

1. **Drive**: 2WD, two rear wheels; skid steer; the front rests on the forks/blade (skids).
2. **Weapon**: the outrunner spins the bell, disc, flange and hub boss together on a fixed shaft. The disc is vertical with a transverse axle and the **hook face leads**. In AWS72 the tooth is at the top with its hook face toward the **rear**, so at the top the tip moves rearward and at the front it moves upward: an **uppercut** that launches opponents. **Reconciled: uppercut (front edge moving up)**.
   - Energy: hub disc r 18 (3 mm steel) ≈ 7.85·π·1.8²·0.3 ≈ 24 g plus tooth ≈ 6 g ≈ 30 g (if aluminium, 10 g). Moment of inertia ≈ ½·0.024·0.018² + 0.006·0.026² ≈ 8.0 × 10⁻⁶ kg·m². At 15,000 rpm (1571 rad/s), E ≈ ½·8 × 10⁻⁶·1571² ≈ 10 J.
3. **Front**: forks/blade get under opponents and the pods' slopes lift them into the tooth's path at the front of the slot.

---

## 7. Assembly order (suggested rebuild)

1. Print the body (rear block with pods and tower, or pods separately) with the slot, wheel notches and lid recesses.
2. Install the two drive gearmotors in the rear block; fit the wheels; screw on the side plates.
3. Install battery, drive ESC, weapon ESC, receiver and switch; route the weapon phase wires up through the hollow tower to the stator.
4. Bolt the outrunner stator to the tower's inner face (4 socket screws from outside); fix the shaft.
5. Bolt the yellow disc between the clamp flange and the bell (4 bolts, hex nuts on the bell side); press the bearing into the hub boss; slide on and nut the shaft end.
6. Screw on the lids.
7. Fit the chosen front: forks into the pod slots (screws through the pockets), or the blade under the pods (4 screws).
8. Stick on the eyes.

---

## 8. Hidden / uncertain list
- Dead shaft vs live shaft; whether the hub boss rotates.
- Disc material (steel vs aluminium) and thickness.
- Rotation direction.
- Whether the pods are separate parts.
- Blade material (polycarbonate vs G10).
- Electronics layout, underside.
- All sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin under the body centre; +X right, +Y forward, +Z up; mm.
- Rear block y ∈ [−34, +6]; pods y ∈ [+6, +34]; body z ∈ [2, 24]; tower x ∈ [12, 26], y ∈ [−6, 12], z to 53; axle (y +3, z 41); disc plane x ≈ −0.5; hub boss x ∈ [−12, −2]; wheels (±29, −20, 14).

## 10. Profiles as math

**10.1 Pod side profile (YZ).** Polygon (6, 2), (6, 24), (14, 21), (34, 7), (34, 2). Upper facet z = 24 − 0.375·(y − 6); lower facet z = 21 − 0.7·(y − 14).

**10.2 Side plate (YZ).** Stadium: |y − y_c| ≤ 18 with z ∈ [1, 25] ∪ circles r 12 at (y_c ± 18, 13), y_c = −4.

**10.3 Tower (YZ, extruded x 12 → 26).** Rectangle y ∈ [−6, 12], z ∈ [24, 44] ∪ semicircle centre (3, 44), r 9 (top half). Bolt circle: 4 holes r 1.2 at (3 ± 6·cos(45° + k·90°), 41 ± 6·sin(…)), centre hole r 2.5 at (3, 41). (The bolt circle is slightly below the arc centre.)

**10.4 Disc.** Hub r = 18 about (y 3, z 41). Tooth: back edge r(θ) = 18·e^(0.0078·θ°) for θ from 70° to 0°; hook face: arc r 12 centred at (r 24, θ −20°) in polar disc coordinates, joining the tip (r 31, θ 0) to the hub (r 18, θ −12°). Window: triangle (22, 8°), (27, 4°), (26, 22°), fillet 1.5.

**10.5 Barbed fork tip (plan, strip axis along Y, tip at y = t).** Width w(y) = 4 for y < t − 6; w = 7 for t − 6 ≤ y < t − 4 (barb step); then tapering linearly from 7 to 0.5 at y = t, with the taper on one side only (sawtooth). Thickness 1.5, top bevel over the last 3 mm.

**10.6 Blade BLD (YZ).** Line from (y +26, z 6) to (+46, 0.5): z = 6 − 0.275·(y − 26) (15.4°), 1.5 thick above. Plan: x ∈ [−36, +36] with corner chamfers removing triangles of legs 10 at the front corners.

**10.7 Eye sticker.** Circle r 5.25 (white) with a 0.6 mm black ring; pupil: the lower half-disc of r 3.0 centred 0.5 below the sticker centre; eyelid: a black bar 9 × 1.2 through the centre.

## 11. Pixel-based measurements

**AWS72 (1287 × 1061):** disc x 505–770, y 60–495 (tooth tip at (720, 60)); bearing (520, 340); clamp flange lugs at about (575, 125), (700, 205), (650, 470), (520, 410); left eye (510, 545); right eye (900, 380); fork tips (690, 990), (880, 850), (1050, 780), (1230, 700); left side plate x 55–420, y 330–750; wheel (140, 330); tower x 720–830, y 120–470.

**AWS74 (1366 × 962):** disc x 480–830, y 50–480; bearing (535, 245); left eye (590, 470); right eye (870, 320); fork tips (880, 890) and (1290, 590); left side plate x 60–480, y 330–640; wheel (110, 330).

**AWS76 (1609 × 1367):** disc x 640–1000, y 60–790; tower x 750–1120, y 280–760, 4 screws around (990, 470); blade x 100–1110, y 780–1200; eyes (535, 615) and (1040, 810); right wheel (1470, 580); side plate x 1110–1590, y 520–1080; switch (1255, 560).

## 12. Several independent estimates of key sizes

| Quantity | Method A (rules/scale) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | 72 (cube minus nothing) | — | AWS76: blade 1010 px = 72 mm → 14 px/mm at the front | **72** |
| Body length | 68 | 0.94 W | AWS72: side plate 60 mm ≈ 0.88 of the side → 68 | **68** |
| Body height | 24 | 0.33 W | AWS76: side plate 24 tall = 0.33 W | **22–24** |
| Disc envelope | 45 (earlier) | 0.68 W = 49 | AWS76: tooth tip 410 px above the axle at ~16.5 px/mm (tower scale) → 25 + perspective → 31 tip radius; hub 320 px below → 19 | **hub r 18, tip r 31** |
| Axle height | — | 0.57 W = 41 | AWS76: tower 480 px for 29 mm; the bolt-circle centre 40% down → z 41 | **41** |
| Tower height above body | 29 | 0.40 W | AWS76: 480 / 16.5 = 29 | **29** |
| Eye Ø | 11 | 0.15 W | AWS76: 130 px / 14 = 9.3 | **10.5** |
| AWS74 fork length | 40 | 0.56 W | AWS74: 330 px at 8 px/mm = 41 | **40** |
| AWS72 fork length | 22 | 0.31 W | AWS72: 170 px at 8 px/mm = 21 | **22** |

## 13. Consistency check: conflicts and reconciliation
1. **Disc size**: the earlier description gave hub r 15 / tip r 30 / axle z 34–40. Pixel ratios against the tower give hub r 18–19 and tip r 30–31 with the axle at z 41. **Reconciled: hub r 18, tip r 31, axle z 41.** Then the hub's lowest point is z 23 (just inside the slot pocket at the block's top) and the tooth's lowest point is z 10, inside the slot between the pods: the **tooth only reaches down into the slot**, never the floor, so the forks/blade must lift opponents into it. The tooth's forward reach is y = 3 + 31 = +34, exactly the pods' front plane, so it strikes whatever sits on the pods' lower facets. Consistent.
2. **Height vs cube**: tooth top z = 41 + 31 = 72 < 101.6. OK.
3. **Left support**: the earlier description guessed a fixed left pillar; no pillar is visible below the hub boss in AWS72/74 (the lid surface is visible under it). **Reconciled: rotating hub boss with an outboard bearing on a dead shaft.**
4. **Front configurations**: three versions; the latest (AWS76 blade) is the default; pods are wide in AWS72/76 and narrow in AWS74.
5. **Rotation direction**: hook orientation in AWS72 (tooth at the top, hook face toward the rear) implies the tip moves rearward at the top, i.e. forward-and-up at the bottom/front: an **uppercut**. Consistent with standard practice.

---

## 14. Why the designer did it (per part, adversarial first)

- **Single hooked tooth**
  - Fight: one tooth gives the **deepest bite** per revolution: between impacts the opponent moves further into the disc's path, so the tooth catches a solid edge instead of skimming it. The hook rakes forward into the opponent, so on contact it grips rather than glancing off. The uppercut rotation throws opponents up and over, using the slot pods as a fulcrum.
  - Threats: a single tooth is unbalanced; the hub mass and the window in the tooth reduce the imbalance. The disc's top half is exposed above the body, so an overhead hammer or another vertical spinner can hit it; a 3 mm plate and the stiff bell absorb this.
- **Cantilever on a D-tower + outboard bearing hub**
  - Fight: a weapon hit pushes the disc sideways and back; a pure cantilever bends the shaft. The hub boss bearing on the shaft's far end keeps the shaft from bending without needing a second fixed upright, which would have narrowed the slot. The tower's round top deflects hits rather than catching them, and its thick 14 mm section survives being hit directly (the scratches show it has been).
  - Construction: one upright, one bolt circle, one shaft; the weapon comes off by removing one nut and four bolts.
- **Pods with sloped faces, eyes and pockets**
  - Fight: the pods are the **ramp** that guides an opponent up into the tooth; they also shield the disc's sides from wedges and horizontal spinners. Recessing the screws in pockets keeps the heads below the slope surface, so opponents slide over them and spinner teeth do not snag them.
  - Personality: the eyes make the robot recognisable (the "sleepy face" of Delta V).
- **Front evolution: 4 short forks → 2 long forks → full blade**
  - **AWS72 four short forks**: four points spread across the front so at least one finds a gap under an opponent at any angle; barbs hold the opponent's edge for the tooth.
  - **AWS74 two long forks**: reach far ahead (40 mm), so the opponent is lifted before it reaches the pods; they also keep spinners at arm's length. Narrow pods save weight for longer forks.
  - **AWS76 blade**: closes the slot underneath and covers the whole width: no gap for an enemy wedge to sneak under the disc, and a flat thin edge gets lower than barbed forks against flat-fronted wedges. Clear sheet flexes and springs back.
  - Being got under: every version puts a thin metal/plastic edge on the floor ahead of the printed pods, so Delta V is not the one being got under.
- **Stadium side plates**
  - Fight: protect the wheels from side hits; the round ends roll off walls and opponents rather than catching; screws in from the outside so a damaged plate is swapped in a minute.
- **Wheels showing above the body**
  - Fight: 4 mm above the top lets the robot drive inverted (the tower and disc stick up further, so it would rest on them; inverted driving is limited) **(guess)**.
- **Lids inset with small screws**
  - Construction: quick access; flush lids give an overhead weapon nothing to catch.
- **Yellow disc, black body**
  - Construction/identity: black hides scuffs; the yellow disc is easy to see spinning (safety and showmanship).

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | rear block, shafts to the wheels at (±22, −20, 14) | medium |
| Weapon motor | 2204–2206 outrunner, 1800–2600 kV | Ø 28 × 12 bell | (x +6, y 3, z 41) | high (seen) |
| Weapon ESC | 10–20 A brushless ESC | 25 × 12 × 5 | under LD-R | medium |
| Drive ESC | dual brushed ESC | 25 × 15 × 5 | under LD-L | low |
| Battery | 2S or 3S LiPo 250–350 mAh (blue wrap seen) | 45 × 18 × 12 | across the rear block, x 0, y −22, z 9 | medium |
| Receiver | micro receiver | 20 × 12 × 5 | front of the rear block, x −10, y 0 | low |
| Switch | the white connector at the rear right | 8 × 5 | (+20, −28, 24) | medium |
| Weapon wires | three phase wires from the stator through the hollow tower into the body | — | x +18 | medium |
| Bearings | 1 ball bearing in HB (visible; 4 × 10 × 4, MR104 or 624-size); motor's own bearings | Ø 10 | axle line | high |
| Shaft | M4 bolt / 4 mm steel shaft through the tower, stator, bell and HB | Ø 4 × 40 | axle line | medium |
| Internal walls | ribs separating battery and electronics; lid screw posts | 2 mm | — | low |

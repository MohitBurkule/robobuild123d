# Orion: full rebuild description from reference photos

Source photos:
- `robots/orion/reference/orion.aws69.webp` (AWS 69, 664 × 751 px, not cut out). The robot sits on a **blue silicone work mat** with a box and a servo (white, top of image) behind it. Camera **high and straight in front** (about 50–55° above the floor), looking at the **front/top**. This build is printed mostly in **grey** with **white** upper side pods. Clear plastic film/skirt pieces are visible under the front edges.
- `robots/orion/reference/orion.aws70.webp` (AWS 70, 473 × 611 px). Camera **straight in front, about 45–50° high**, robot all **white**, with a **black chequered tape strip** on the flipper and a **brass hinge pin** visible at the top of the flipper.
- `robots/orion/reference/orion.aws72.webp` (AWS 72, 1337 × 1162 px, cut out). Camera **front-left/front, high (about 35–40°)**, slightly from the robot's left so the **right side** (image right) is seen at a grazing angle and the **left side** wraps away; white body, **grey ribbed cones**, **dark grey treaded wheel** visible in the right side cut-out. The green areas at the far left and right are the **cut-out background seen through clear plastic skirts**.

Everything stated as fact is read from the photos. Anything inferred is marked **(guess)**. Dimensions in mm are **estimates**. Scale comes from the AWS 150 g / 101.6 mm cube, the **brass hinge pin** (aws70; read as a Ø 2–3 mm brass rod, about 20 mm long), the flipper width, and the kit draft (`kit.json`: flipper type, trapezoid plan, body 110 × 92 × 46, front width 60, ramp 85, two internal wheels r 11 × 8 at y −35, a 34 × 95 × 3 flipper plate pivoting at (y −40, z 48) tilted −28°, and "spring" cylinders r 7 × 6 at (±50, −30, 26)). Ratios are against **W = rear width ≈ 90 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward, **+Z** up. Units mm.
- **Origin O** = floor point under the centre of the footprint (mid-width at mid-length, length measured from the front edge to the rear wall).
- **Front** = the low end where the central plate meets the floor; **rear** = the tall end with the hinge.
- aws69/aws70: +Y points toward the camera and down the image, +X to the image left (robot faces the camera), +Z up. aws72: +Y toward the lower-left of the image, +X toward the right.

| ID | Part |
|---|---|
| CH | chassis / tub (hidden core, rear wall, floor) |
| FL | central flipper/lifter plate (long ramp strip on top) |
| FL-U, FL-L | upper and lower sections of FL (aws72 shows a crease) |
| HG | hinge at the top-rear of FL with brass pin |
| LG | ORION logo disc on FL |
| FH | two small round holes on FL (aws69) |
| CQ | black chequered tape (aws70) |
| CR-L, CR-R | channel rails / raised edges either side of FL |
| SP-L, SP-R | sloped side panels (front-side wedges) |
| WC-L, WC-R | circular wheel cut-outs in the side panels |
| PD-L, PD-R | upper rear side pods (white, with 3 vent slots) |
| VS | vent slots on the pods |
| CN-L, CN-R | grey ribbed conical "thruster" bumpers |
| RT | rear top rim with corner lugs |
| SK | clear plastic skirts under the lower edges |
| WH-L, WH-R | drive wheels (dark grey, treaded) |
| SV | flipper servo (hidden; a white servo is seen on the bench in aws69) |
| M-L, M-R, BAT, ESC, RX, SW | hidden internals |

---

## 1. Overall description in one paragraph

Orion is a **two-wheel, servo-driven ramp-lifter/flipper shaped like a space capsule or a tent**. Seen from the front it is a **wedge-roofed trapezoid**: a long **flat central plate about 34 mm wide** runs from a **thin edge on the floor at the front** up at about **25°** to a **hinge at the top-rear** about **45 mm** high, carrying a round **"ORION" logo disc** (stencil-cut letters plus a crescent like a planet's orbit). On each side of this plate a **flat trapezoidal panel** slopes **down and outward** at about 55–60° to the floor, so the whole front and both front-sides are ramps; the plan is a **trapezoid**, about **60 mm wide at the front and 90 mm at the rear**, about **100 mm long**. Near the rear, each side panel has a **big circular cut-out** through which a **dark grey treaded wheel (Ø ≈ 28 mm)** is seen; above each cut-out a **white pod with three vent slots** carries a **grey ribbed cone** pointing out and up like a **rocket thruster nozzle**. Clear plastic **skirts** extend the lower edges to the floor. The central plate is hinged at its top (brass pin) and is the weapon: lifted by a servo it raises its front edge to tip opponents over (guess, high: kit says flipper).

---

## 2. Part-by-part description

### 2.1 Central plate (FL) and hinge (HG)
- **Shape**: a **flat rectangular plate** about **34 mm wide × 98 mm long × 3 mm thick**, lying on a **25–28° slope**: its front edge on the floor at about **(y +48, z 0.5)**, its rear edge at the hinge at about **(y −40, z 44)** (kit: pivot (y −40, z 48), tilt −28°).
- **Front edge**: straight and thin (bevelled underneath to about 0.5 mm), the same width as the plate (34 mm). In aws72 the lower front of the plate has a **frosted/scuffed** texture (sanded or roughened, with white marks from wear); in aws69 the front of the plate shows a slight lip.
- **Crease (aws72)**: a faint **transverse line** about 25 mm below the hinge and a **step** about 1 mm high just below the logo (y ≈ −5) suggest the plate is **two printed parts**: an **upper hinge leaf FL-U** (about 34 × 35 mm) and a **lower ramp FL-L** (about 34 × 63 mm), glued/screwed with an overlap (guess, medium). aws69/aws70 show a single continuous plate.
- **Hinge (HG)**: at the top rear, a **brass pin** about **Ø 2.5 × 20 mm** lies across the top of the plate along X (aws70, px (175–235, 52–58)), held in printed knuckles in the rear top rim. In aws69 a short **rectangular hinge tab** (about 20 × 5 mm) is visible at the plate top (px 190–275, 70–85).
- **Rails (CR)**: the plate sits **in a shallow channel** between two **thin raised rails** (about 2 mm wide, 2 mm proud) that form the inner top edges of the side panels; a gap of about **1 mm** separates plate and rails (visible as dark lines in aws69).

### 2.2 Logo disc (LG), holes (FH), chequer tape (CQ)
- **LG**: a **round disc Ø ≈ 34–36 mm** centred on the plate about **35 mm below the hinge** (at about (0, −8, 30)), carrying the word **"ORION"** in stencil capitals about **5 mm tall** and a **crescent arc** curving around the left of the "O" (aws69/70: a C-shaped thin arc of radius ≈ 13 mm, open to the right, like a planet's orbit). In aws69 the letters and crescent are **cut through** the plate (we see darkness through them). In aws70 the disc is a **separate raised disc** about 1.5 mm proud, slightly wider than the plate, with the letters cut through (brown/gold interior visible, the servo or a sticker behind). In aws72 the logo is **embossed** (raised letters) on a raised disc.
- **FH (aws69)**: two **round holes Ø ≈ 4 mm** on the centre line, one above the logo (about 12 mm from the hinge) and one below it: probably **screw holes** for the plate-to-servo-horn link (guess, medium).
- **CQ (aws70)**: a strip of **black electrical tape squares** about **8 × 8 mm**, arranged as a **two-column chequer** from just below the logo to the front edge, on the plate's left half (image left = robot's right). Pure decoration.

### 2.3 Side panels (SP-L, SP-R)
- **Shape**: flat **trapezoidal plates**, about **2.5 mm thick**, each running from the plate rail (inner top edge, along the slope of FL at x ±18) **down and outward** to a **bottom edge** on the floor. The bottom edge runs from the front corner at about **(±30, +48, 0)** back to the rear corner at about **(±46, −35, 0)**: the side panels flare out toward the rear, giving the **trapezoid plan** (60 front, 92 rear).
- **Slope**: near the rear (where the inner edge is at z ≈ 44) the panel goes from x ±18 at z 44 down to x ±46 at z 0: about **57°** from the floor. Near the front the inner edge is low, so the panel is a narrow strip. The panels are therefore **not quite planar** (a ruled/twisted surface), or they are planar with the bottom edge a little higher toward the front (guess: build as planar triangles/trapezoids between the four corner points; the photos show flat faces with straight edges).
- **Front ends**: each side panel's front end meets the front corner of FL in a **sharp point** (aws69 lower corners at px (330, 700) and (600, 610)); the front outline is therefore a shallow **V/trapezoid**: FL's 34 mm edge in the middle and the two side panels' short front edges angled back.
- **Colour**: aws69 grey PLA (with fine diagonal infill pattern on the top surface); aws70/72 white.

### 2.4 Wheel cut-outs (WC)
- **Shape**: a **circular opening about Ø 30 mm** cut through each side panel at the rear-upper part, its centre at about **(±40, −30, 16)** in the slope plane; the upper part of the circle is broken into by the pod (PD) above. The wheel's tread is seen through it, set back about 3–5 mm inside the panel surface.

### 2.5 Side pods (PD) and vent slots (VS)
- **Shape**: on each side, at the top-rear corner, a **white printed block** (about **28 × 22 × 18 mm**) forming the upper-rear part of the side, between the rear top rim, the plate rail and the wheel cut-out; its lower edge is **concave**, following the wheel cut-out. In aws69 these pods are **white** while the panels are **grey**, confirming they are separate parts.
- **Vents (VS)**: **three parallel slots** about **8 × 2 mm**, 3.5 mm pitch, on the pod's upper face near the plate rail (aws72 right pod), oriented across the slope. Function: cooling / lightening, or **zip-tie slots** (guess).
- **Small marks**: aws69 shows **embossed text/marks** on the left pod (small raised shapes) and aws70 a **small raised rib/tab** on each pod at mid-height (px (100, 180) and (330, 155)): likely **screw bosses or print seams** (guess).

### 2.6 Grey ribbed cones (CN)
- **Shape**: **stepped/ribbed cones**, printed grey: base (outer, wide end) **Ø ≈ 16 mm**, narrow end (attached to the pod) **Ø ≈ 8 mm**, length about **20 mm**, with **4 circumferential ribs** (rings about 1.5 mm proud) at about 4 mm pitch, like a coil spring or a **rocket engine nozzle with cooling rings**. The wide end is a flat disc with a slightly rounded rim.
- **Position and axis**: one on each pod, root at about **(±38, −30, 32)**, axis pointing **outward and up** (about 30–40° above horizontal, perpendicular-ish to the side panel), wide end at about **(±54, −32, 40)**. In aws69 each cone sticks out sideways beyond the side panels and is the **widest point** of the robot.
- **Function (guess)**: (1) decorative **thrusters** (the robot is named after the Orion space capsule, and the body shape resembles a capsule/lander); (2) **side bumpers**: if the robot ends up on its side, the cones keep it from resting flat and make it roll back onto its wheels; (3) protect the wheel tops. The kit draft calls them "spring". Medium confidence on (1)+(2).

### 2.7 Rear top rim (RT)
- A **narrow rim** (about 3 mm thick) along the top rear edge, the **highest part** at z ≈ 46, with small **square lugs** at both ends (aws72 px (720, 90) and (870, 190)) that hold the hinge pin ends. Behind it, the rear wall (not photographed), presumed vertical.

### 2.8 Clear skirts (SK)
- **Thin clear polycarbonate/PET sheet** (about 0.5 mm) strips taped/glued under the lower edges: under the front corners (aws69, transparent rectangles extending about **5–10 mm** beyond the front edges) and along the side bottom edges (aws72, the green-tinted areas, extending the side panels by about **5–8 mm**). Function: lower the edges to the floor and close gaps so opponents can't get under; cheap replaceable wedgelets.

### 2.9 Wheels (WH)
- **Shape**: **Ø ≈ 28 mm × 10 mm**, **dark grey printed TPU** with a **knurled/ribbed tread** (fine axial ribs about 1 mm) and a **flat face** with a small **hex/square hub feature** (a small light square at px (1125, 545) in aws72: the end of a set screw or the motor shaft flat).
- **Position**: inside the side panels, centres at about **(±36, −30, 14)**, bottom touching the floor through the floor slots. Kit gave r 11 (Ø 22); the cut-out photo suggests closer to Ø 28 (see section 11).

### 2.10 Hidden internals
- **Flipper servo** (a white servo seen on the bench in aws69 is a spare or the same type, guess): a standard/mini servo inside the rear, horn linked to FL near the upper hole FH.
- **Drive**: two N20 gearmotors at the rear driving the wheels.
- **Electronics**: 2S LiPo, receiver, dual ESC, switch.

---

## 3. Per-view sections

### 3.1 aws69 (front, high, grey build)
- Centre: the long grey plate FL from the hinge tab at the top (px 190–275, 75) to its front edge at the bottom (px 330–600, 690), the stencilled **ORION** logo at px (250–360, 200–285), two round holes at px (260, 145) and (330, 300).
- Sides: the grey side panels sloping away, the **white pods** at the top-left and top-right, and the **grey ribbed cones** sticking out sideways (left px 0–95, 170–310; right px 410–505, 70–190).
- Through the side panel cut-outs: shadows of the wheels (px (60–100, 330–400) and (520–560, 240–290)).
- Bottom: clear film patches under the front edges.

### 3.2 aws70 (front, high, white build)
- The plate with the raised **ORION** disc at px (160–300, 160–285), **brass pin** at the top (px 175–235, 55), **black chequer tape** down the lower plate.
- Both side panels in white; wheel cut-outs at px (25–70, 200–290) and (380–420, 190–240) with **black wheels** visible in them; small tabs on the pods.

### 3.3 aws72 (front-left, high)
- The plate from the lower-left (front edge at px (200–590, 820–880)) up to the rear rim at px (700–880, 90–200); the **embossed logo disc** at px (535–800, 300–500); the frosted lower plate; the crease line.
- Right: the right side panel with the **wheel cut-out** and dark wheel, the **pod with three vents**, the **grey cone** (px 1090–1250, 320–430).
- Left: the left side panel receding to the left, its **cone** at px (500–650, 135–255) behind the left pod.
- Green/clear skirt edges at the far left and far right.

### 3.4 Top view (synthesised)
- A **trapezoid** 60 wide at the front (y +48) and 92 at the rear (y −35 to −50); the central 34 mm strip (FL) down the middle; the side panels as two long triangles/trapezoids; circular wheel cut-outs near the rear; cones sticking out at x ±54 near y −32.

### 3.5 Side view
- A **right triangle-like** profile: floor from y −50 to +48, the plate's slope from z 0 at the front to z 44–46 at the rear, a vertical rear wall; the side panel seen at a slant with the round cut-out and wheel; the cone sticking up and out near the top rear.

### 3.6 Front view
- A **trapezoid/pentagon**: 34 mm flat strip at the top centre (the plate seen end-on at its rear height 46) sloping side panels to the floor 92 wide; cones at the upper corners as the widest points (≈ 108 wide over the cones; see 12).

### 3.7 Rear and underside (not photographed)
- Rear: vertical wall, about 60–70 wide × 46 tall, with the hinge knuckles at the top (guess). Underside: flat floor, wheel slots at the rear, front edge of the plate and skirts at the front.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| FL | flat sloped plate | 34 × 98 × 3, 26° | 0.38 × 1.09 | white / grey FDM | hinge pin + servo link | 1 (2 parts in aws72) |
| HG | brass pin + knuckles | Ø 2.5 × 20 | — | brass | in rim lugs | 1 |
| LG | disc with cut/embossed letters | Ø 35 × 1.5 | 0.39 | white/grey | integral or glued | 1 |
| FH | holes | Ø 4 | — | — | — | 2 |
| CQ | tape squares | 8 × 8 | — | black tape | stuck | ≈ 10 |
| CR | rails | 2 × 2 × 98 | — | FDM | integral with SP | 2 |
| SP | trapezoid side panels | ≈ 85 × 50 (slant) × 2.5 | — | FDM | to CH | 2 |
| WC | circular cut-outs | Ø 30 | 0.33 | — | — | 2 |
| PD | pods with 3 vents | 28 × 22 × 18 | 0.31 | white FDM | to CH | 2 |
| CN | ribbed cones | Ø 16 → 8 × 20, 4 ribs | 0.18 | grey FDM | on PD | 2 |
| RT | rear rim with lugs | 62 × 3 × 4 | — | FDM | integral | 1 |
| SK | clear skirts | 5–10 wide × 0.5 | — | polycarbonate | tape/glue | 3–4 |
| WH | treaded wheels | Ø 28 × 10 | 0.31 × 0.11 | dark grey TPU | motor shaft | 2 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| FL front edge ↔ floor | rests on | 0–0.5 |
| FL sides ↔ CR rails | clearance | ≈ 1 |
| FL ↔ HG pin | pivots | 0 |
| HG ↔ RT lugs | pin in knuckles | 0 |
| LG ↔ FL | integral/glued | 0 |
| SP inner top edge ↔ CR | integral | 0 |
| SP bottom edge ↔ floor | skims | 1–2 (closed by SK) |
| SK ↔ floor | touching | 0 |
| WH tread ↔ WC edge | inside cut-out | 3–5 radial |
| WH outer face ↔ SP inner surface | inside | 1–3 |
| WH bottom ↔ floor | touching | 0 |
| PD ↔ SP / CH | fixed | 0 |
| CN root ↔ PD | glued/screwed | 0 |
| CN wide end ↔ floor | above | ≈ 35 |
| CN outer tip ↔ SP bottom edge (X) | sticks out beyond | ≈ 8 |
| FL underside ↔ servo horn/link | linked | 0 |

---

## 6. Mechanism
1. **Drive**: two internal rear wheels; front rests on the plate edge and skirts.
2. **Lift/flip**: the servo rotates FL about the hinge at the top-rear (X axis at (y −40, z 44)). Rotating the plate upward raises its **front edge**; an opponent that has driven onto the ramp is lifted and tipped backward/sideways. Range maybe 30–50° (guess). This makes it a **"dustpan" lifter / reverse-hinged flipper**: the whole top is the weapon.
3. **Self-righting**: on its back, the plate swinging out can push off the floor to roll the robot back (guess, medium). The cones help roll it from its side.
4. **Defence**: every outer surface except the rear is a ramp; spinners and wedges meet sloped faces.

---

## 7. Assembly order (suggested rebuild)
1. Print CH (floor + rear wall + motor and servo mounts), two SP side panels (with rails and wheel cut-outs), two PD pods, FL (one or two parts), the logo disc, two cones, wheels.
2. Fit motors and wheels; fit the servo at the rear-centre.
3. Fit battery, ESC, receiver, switch.
4. Fix SP panels and PD pods to CH; glue the cones onto the pods.
5. Mount FL with the brass pin through the rim lugs; link to the servo horn (screw through FH).
6. Stick the logo disc (if separate), chequer tape, and clear skirts.

---

## 8. Coordinate frame (restated)
- Footprint trapezoid: front edge y +48 (x ±30), rear y −50 (x ±46). Rear rim top z 46.
- FL: x ±17, from (y +48, z 0.5) to (y −40, z 44); hinge axis X at (y −40, z 44).
- WC centres (±40, −30, 16) on the panel, WH centres (±36, −30, 14) Ø 28.
- CN: root (±38, −30, 32), tip (±54, −32, 40).

## 9. Profiles as math

**9.1 Plate (in YZ).** z_FL(y) = 44·(48 − y)/88 for y ∈ [−40, +48] (slope atan(44/88) = 26.6°).

**9.2 Side panel surface (right panel).** Plane through three points: A = (17, −40, 44) (rear top inner), B = (30, 48, 0) (front bottom), C = (46, −40, 0) (rear bottom). Normal n = (B − A) × (C − A) = (13, 88, −44) × (29, 0, −44) = (−3872, −704, −2552) → normalised ≈ (−0.82, −0.15, −0.54) (flip sign to point outward: (0.82, 0.15, 0.54)). The panel is the triangle/trapezoid A–(17, +48, 0.5)–B–C clipped by the floor; the front point (17, 48, 0.5) nearly coincides with the plate front corner.
- Side panel slope at the rear (XZ section): atan(44 / (46 − 17)) = 56.6°.

**9.3 Logo.** Disc r 17.5 centred at y −8 on the plate. Crescent: arc of radius 13 from 100° to 260° (opening to +X in the plate frame), width 1.5. Letters "ORION" cap height 5, total width 26, centred.

**9.4 Cone.** Radius along its axis s ∈ [0, 20]: r(s) = 4 + 4·s/20 + 0.75·[frac(s/4.5) > 0.66] (base cone plus 4 ribs).

**9.5 Wheel cut-out.** Circle r 15 in the panel plane centred at the point of the panel above (±40, −30, 16).

**9.6 Wheel.** r(φ) = 14 + 0.5·[sin(48φ) > 0], width 10.

## 10. Pixel-based measurements
- aws70 (473 × 611): plate width at the logo ≈ 160 px (x 125–285); plate width at the front ≈ 210 px (perspective); disc Ø ≈ 140 px; brass pin 60 px long; overall front width at the bottom px 30–445 = 415 px; chequer squares ≈ 30 px.
- aws69 (664 × 751): plate width at the logo ≈ 230 px (x 125–355... inner plate ≈ 200 px); cones ≈ 85–95 px long; front edge px (330–600) ≈ 280 px.
- aws72 (1337 × 1162): logo disc ≈ 265 px; plate width there ≈ 300 px; right wheel visible arc ≈ 260 px tall (≈ Ø when completed); right cone ≈ 175 px long, Ø base ≈ 110 px.

## 11. Several independent estimates of key quantities

| Quantity | Method A (kit / rules) | Method B (ratios in photos) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Plate width | kit 34 | ≈ 0.37 × rear width (aws70) | brass pin 20 mm = 60 px → 3 px/mm; plate 160 px / 3 → 53?? (pin nearer & foreshortened; disc 140 px ≈ plate) → disc ≈ plate | **34–36** |
| Logo disc Ø | — | ≈ plate width | aws72: 265 / 300 × 34 = 30 | **33** |
| Rear width | kit 92 | ≈ 2.6 × plate (aws70: 415/160) → 88 | — | **90–92** |
| Front width | kit 60 | ≈ 1.75 × plate (aws69 front 280/160) → 60 | — | **60** |
| Length | kit 110 (too long) | ≤ 101.6 cube | — | **98 (y −50 to +48)** |
| Height | kit 46 | ≈ 1.3 × plate width → 45 | — | **46** |
| Plate slope | kit 28° | from 46 height over ≈ 90 run → 27° | — | **26–28°** |
| Wheel Ø | kit 22 | cut-out ≈ 0.85 × disc → 28–30 for the cut-out, wheel slightly smaller | aws72: wheel arc 260 px vs disc 265 px (similar depth) → ≈ 33 | **28** |
| Cone length | kit "spring" r 7 × 6 | ≈ 0.6 × disc → 20 | aws72 175 / 265 × 33 → 22 | **20** |
| Cone base Ø | kit 14 | ≈ 0.45 × disc → 15 | 110 / 265 × 33 → 14 | **15–16** |

## 12. Consistency check
1. **Length**: kit 110 breaks the cube; the side views are not available, but a 98 mm length gives plate slope 26.6° with height 44: consistent with the photos' look. **98 kept.**
2. **Width over the cones**: rear width 92 + cones sticking out ≈ 8 mm each side = **108**, over the 101.6 cube if the cones are at the full rear width. Reconciled: the cones sit **higher and further in** (root at x ±38, where the side panel is at z ≈ 25–35), tip at x ±50 → overall **100**, fits (medium).
3. **Wheel size**: kit Ø 22 vs photo ≈ 28; with the axle at z 14 the wheel top is z 28, under the side panel (which at x ±36 is at z ≈ 18 at the rear: the wheel pokes through the cut-out). Consistent with the photo (wheel visible through the hole). **Ø 28.**
4. **Two plate builds**: aws69/70 continuous plate with cut-through logo; aws72 two-piece plate with embossed logo. Use aws72 as the final (latest) version.
5. **Mass**: printed shell ≈ 55 g (thin 2.5 mm panels), servo 9–15 g, motors 20 g, wheels 8 g, battery 15 g, electronics 8 g, pin/screws 3 g: ≈ 120–125 g < 150.

---

## 13. Why the designer did it (per part, adversarial)

- **Whole-top hinged plate (FL)**
  - Fight: the plate is the ramp **and** the weapon. Opponents that drive at the robot ride up the 26° slope; lifting the plate then raises their front higher and tips them. A long plate gives a big lever arc at its front edge.
  - Against attacks: a vertical spinner hitting the plate is deflected upward along the slope; the plate is easily reprinted (and was: three builds show three versions).
  - Weakness: hinged at the top, the servo has a long lever to drive; a heavy opponent at the tip loads the servo heavily, so the weapon is more a **tipper** than a launcher.
- **Sloped side panels with trapezoid plan**
  - Fight: no vertical faces at the front or front-sides; pushers and wedges approaching from the side meet a ramp too, so the robot is hard to get under from any front-side angle. The narrow front lets it slip under opponents' corners.
  - Against horizontal spinners: hits glance off sloped faces.
- **Internal wheels in cut-outs**
  - Protected from spinners; the round cut-outs keep a little tread exposed near the top so the robot can still drive off walls or when partly tipped (guess).
- **Ribbed cones**
  - Theme (rocket thrusters for a robot named after the Orion capsule/constellation); bumpers to stop it settling on its side and to roll it back (guess). Ribs add stiffness and give a grip edge.
- **Vent slots on the pods**
  - Cooling for motors/servo; lightening; zip-tie points (guess).
- **Clear skirts**
  - Make the edges meet the floor exactly, cheaply and replaceably; polycarbonate flexes instead of chipping.
- **Brass pin hinge**
  - Strong and smooth; easy to replace; printed knuckles alone would wear.
- **Logo and chequer tape**
  - Identity and judges' memory; zero cost.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Flipper servo | 9–17 g metal-gear servo, output along X | 23 × 12 × 25 | rear-centre (0, −32, 20), horn linked to FL via a short link to FH upper hole | medium |
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | (±22, −30, 14) | medium |
| Battery | 2S LiPo 180–300 mAh | 35 × 18 × 10 | under the plate centre (0, +5, 6) | medium |
| ESC/receiver | combined board | 25 × 20 × 6 | under the plate (0, −12, 8) | medium |
| Switch | at the rear wall | 10 × 6 | rear | low |
| Floor | printed floor with wheel slots | 2 thick | — | medium |
| Panel fastening | M2 screws or snap tabs into CH | — | along edges | low |

## 15. What the photos cannot show
- The rear wall, the underside, the true wheel size and exact position, the servo linkage and plate range, and whether the side panels are exactly planar.
- All mm values are estimates (±15%).

# Relativity: full rebuild description from reference photos

Source photos (in `robots/relativity/reference/`), all cut out onto white. All three have a strong **green colour cast at the edges** (green-screen spill): the body is **black** printed plastic, and the green fringe on the blade edges and the green tint on the stickers are photo artefacts, not paint.
- `relativity.aws72.webp` (1447 × 980 px): a **three-quarter view from the front-left, about 35° above horizontal**. The weapon nose is at the lower right and the rear wheels at the upper left. The blade is stopped across the nose, sticking out to the right (toward the robot's right-front) and to the left under the body.
- `relativity.aws74.webp` (1225 × 1007 px): almost the same viewpoint, slightly higher and more from the left. The blade is stopped pointing **toward the camera** (forward-left), showing one fishtail end clearly.
- `relativity.aws76.webp` (1687 × 1069 px): a **three-quarter view from the front-right, about 25° above horizontal**. The nose is at the left, the rear at the right. The right side wall and the right rear wheel guard are seen almost square. The blade sticks out to the left, showing a **crescent end with a large hole**.

Everything stated as fact is read from those photos. Anything inferred is marked **(guess)** with a confidence. Dimensions are **estimates in mm**, scaled from the AWS antweight limits (150 g, fits a 101.6 mm cube) and cross-checked against the project spec draft (`spec.json`: a kite-shaped plan from y = −48 to +52, max half-width 50 at y = −10, wheels Ø 22, an 1806 outrunner hanging under the nose, a 3 mm steel blade). Ratios use **L = body length ≈ 98 mm**.

Relativity is an **undercutter / low horizontal bar spinner**: a kite- or arrowhead-shaped black printed body, with a **steel bar spinning just above the floor under its pointed nose**, two **guarded rear wheels**, a lid with **googly eyes**, and a **U-shaped printed handle/roll bar** on top.

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) under the body's plan centroid, about mid-length (the midpoint between nose tip and rear edge) and on the centreline.
- **+X** = robot's right, **+Y** = forward (toward the nose and blade), **+Z** = up. Units mm.
- In AWS72/74 the camera is at the **front-left**: the robot's left side faces the camera, the nose is at the image right. In AWS76 the camera is at the **front-right**: the robot's right side faces the camera, the nose is at the image left.

Part IDs:

| ID | Part |
|---|---|
| BD | main body shell (black printed tub) |
| NS | nose plate (the thick pointed front of the body that carries the weapon motor) |
| SW-L / SW-R | side walls (the long sloped flanks) |
| GD-L / GD-R | rear wheel guards (outer walls around the rear wheels) |
| WL-L / WL-R | rear wheel wells (open-topped pockets) |
| LD | front lid (flat plate with eyes and switch) |
| RC | rear cover (raised textured panel behind the lid) |
| HB | U-shaped handle / roll bar on the lid |
| EY-L / EY-R | googly-eye stickers |
| SWT | power slide switch on the lid |
| MS | weapon motor mount screws (4, in a diamond on the nose) |
| WM | weapon motor (1806-class outrunner, hanging under the nose, hidden) |
| HUB | blade hub / pulley disc under the nose |
| BL | steel spinner blade (bar) |
| WH-L / WH-R | rear drive wheels |
| AX-L / AX-R | wheel axle screws through the guards (silver socket heads) |
| S-LD | lid screws (black Phillips) |
| WR | visible wiring (red, black, white heat-shrink) |
| DM-x, BAT, ESC, WESC, RX | hidden internals (guess) |

---

## 1. Overall description in one paragraph

Relativity is a **low, wedge-nosed undercutter**. In plan its body is an **arrowhead / kite**: about **96 mm wide** across the rear wheel guards and **≈ 98 mm long**, tapering from the guards to a **rounded nose about 20 mm wide**. The body is **black FDM** with clear layer lines. The rear half is a **tub about 24 mm tall** whose rear corners are **open-topped wells holding two black drive wheels (Ø ≈ 22)**, enclosed on the outside by **tall printed guard walls**, each with a **silver socket screw** acting as the wheel axle. The front half narrows to a **thick (≈ 12 mm) nose plate**. On top of the nose, **four socket screws in a diamond** hold an **outrunner motor hanging underneath**, which drives a **black hub disc** and a **3 mm steel bar blade** spinning **≈ 2–5 mm above the floor**. The blade sticks out well beyond the body outline at the front and sides. The top of the body carries a **flat lid** with two **googly-eye stickers** (white ovals with black pupils) and a tiny **white slide switch**, plus a raised **U-shaped handle bar** (5 mm round section) running along the lid's front and right edges. Behind the lid is a **raised rear cover** with a fine ribbed texture. **Wires with white heat-shrink** show through a gap behind the lid on the robot's right.

---

## 2. Part-by-part description

### 2.1 Body shell (BD)
- **Plan outline (best estimate, z = mid-height)**: a ten-sided kite, symmetric about X = 0. Vertices (x, y): rear corners (±42, −48), widest points (±48, −10), shoulders (±38, +14), front flanks (±22, +36), nose shoulders (±9, +48), and a **round nose cap** of radius ≈ 10 centred at (0, +43) that closes the front (tip at y ≈ +53). See §8.1.
- **Height**: rear tub walls to the top edge **≈ 24 mm** (z ≈ 3 to 27 at the guards); the mid-flanks **≈ 18 mm** (z 5 to 23), dropping toward the nose; the nose plate **≈ 12 mm thick** (z ≈ 10 to 22).
- **Side profile**: the side walls' **lower edge is not straight**. It is lowest at the rear guards (z ≈ 1–2, nearly touching the floor) and **rises toward the nose** (z ≈ 9–10 under the nose), leaving room for the hub and blade underneath. In AWS76 there is a clear **step** in the lower edge at the front of the right guard (px ≈ (1220–1290, 780–830)): the guard drops ≈ 4 mm lower than the flank in front of it.
- **Wall slope**: the flanks lean **outward toward the bottom** by about **10–15°** (the walls are slightly **sloped / curved**, wider at the base). In AWS76 the right guard face is visibly **convex** in plan.
- **Colour / material**: matt black FDM with **horizontal layer lines** (printed upright). Many **chips and gouges** at the top edges near the nose (AWS72 px ≈ (1000–1080, 480–620): bitten, ragged edge on the nose's top-right), which are battle damage.

### 2.2 Nose plate (NS)
- **Shape**: the front ≈ 30 mm of the body is a **solid-looking thick plate**, **≈ 12 mm thick**, with a flat top at z ≈ 22 and a **flat underside at z ≈ 10**. In plan it is the tapered tip of the kite with a **round nose** (r ≈ 10).
- **Top**: the **4 motor mount screws MS** sit in a **diamond / cross pattern** around a **central hole** (a small red/brown glint is visible through it in AWS72, probably the motor's shaft end or a wire **(guess)**).
- **Edge**: the nose's front and side faces are vertical (12 mm), with layer lines. In AWS74 a few small chips are visible on the nose edge.

### 2.3 Side walls (SW-L, SW-R)
- Long sloped flanks from the guards forward to the nose. Each is about **55 mm long** (in plan, along the edge) and **18 → 12 mm** tall from rear to front. Wall thickness **≈ 2.5–3 mm** **(guess)**.
- AWS74 (left flank) shows **several scars**: a crack line, two small rectangular dents and a vertical notch at px ≈ (110–150, 470–520), plus small light tabs that look like **support remnants or patched cracks**.

### 2.4 Rear wheel guards (GD-L, GD-R) and wells (WL)
- **Shape**: the rear outer corners are **tall printed walls** that enclose the wheels on the outside. Each guard face is about **36–40 mm long (Y)**, **24–26 mm tall**, **≈ 3 mm thick**, slightly **convex** in plan and leaning outward at the bottom.
- **Top edge**: in AWS72/74 the left guard top is **flat**, at z ≈ 27, and ends at the rear in a **chamfered corner**. In AWS76 the right guard's top edge is **slightly sloped**, higher at the rear.
- **Axle screws AX**: each guard carries **one silver socket-head cap screw**, head Ø ≈ **5.5 mm (M3)**, at about **(±48, −28, 12)**. It is the **wheel axle**: it passes through the guard into the wheel hub and probably into an inner bearing boss **(guess, medium)**. Below the AWS76 screw, a small **"V" mark** (px ≈ (1455, 520)) is moulded or scratched into the guard.
- **Wells**: between the guard and the tub's inner walls, each wheel sits in a **pocket open at the top** (AWS72 px ≈ (160–430, 240–400) shows the left wheel's top through it; AWS76 px ≈ (1260–1440, 280–400) shows the right). So the wheels' **tops are visible from above** but they are **shielded on the outside and front**.
- **Guard-to-chassis support**: the guard is **printed as one piece with the tub** **(guess, high)**. It is joined to the tub floor along its bottom and to the rear wall at its rear end, and braced at the front by the flank. There are no separate struts.

### 2.5 Rear drive wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 22 mm × 8–10 mm wide**, black. The tread has **2–3 deep circumferential ribs or a coarse block tread**: AWS72 shows **three black rounded rings side by side** (px ≈ (200–330, 290–380)), as if the wheel is a stack of three narrow discs or has two deep grooves.
- **Material**: black printed TPU or moulded rubber **(guess)**.
- **Position (centres)**: **(±40, −28, 11)**. The tyre tops (z ≈ 22) are **below the guard tops (z ≈ 27)**, so **from the side the wheels are fully hidden**. The tyres touch the floor through openings in the tub floor.
- **AWS76 right well**: two rounded black shapes (px ≈ (1280–1430, 270–360)): the wheel top and **a second rounded part** that may be the **motor gearbox end** or a hub flange.

### 2.6 Lid (LD)
- **Shape**: a **flat black plate ≈ 2 mm thick**, roughly a **pentagon** in plan: about **48 mm wide**, extending from **y ≈ −12 (rear edge)** to **y ≈ +28 (front edge)**. Its front edge is **parallel to X**; its front corners are cut to follow the flanks; its rear edge has a **step notch** on the robot's left (AWS72 px ≈ (350–440, 260–400): the lid's rear-left corner is cut away in an inverted "L" where it meets the rear cover).
- **Height**: top at z ≈ 25, i.e. **≈ 3 mm above the nose plate top**.
- **Screws S-LD**: small black **Phillips pan screws**, head Ø ≈ 3.5 mm: one at the lid's **rear-left corner** (AWS72 px (355, 430); AWS74 (425, 385)), one at the **rear-right corner** (AWS72 (870, 190); AWS74 (830, 155)), one at the **right** (AWS76 (1190, 440)) and one at the **left front** (AWS76 (630, 180)). So **4 screws**, one near each corner.
- **Front lip**: in AWS76 the lid's front edge sits on a **thin, sloped skirt** (a separate chamfered plate, px ≈ (930–1250, 290–440)) that runs down to the flank's top edge. This looks like a **ramp** that fills the gap between the lid and the lower nose **(guess)**.

### 2.7 Rear cover (RC)
- **Shape**: a **raised rectangular panel** behind the lid, about **40 mm wide × 18 mm deep × 2 mm thick**, sitting at z ≈ 27–29 (≈ 2–3 mm above the lid) on the rear part of the tub between the wells. Its front edge slopes down to the lid. In AWS72/74 it is the textured panel at px ≈ (210–440, 120–270).
- **Surface**: a fine **ribbed/knurled texture** (like a textured PEI print bed finish, or a separate **TPU** panel) that is different from the lid's smooth top.
- **Function (guess)**: the battery/electronics hatch, or a tough top over the rear electronics.

### 2.8 Handle / roll bar (HB)
- **Shape**: a **rectangular "U" loop** of **round-section printed bar, Ø ≈ 5 mm**, standing **≈ 6–8 mm** above the lid on short legs.
  - **Front crossbar**: parallel to X, along the **front edge of the lid**, from about x = −24 to x = +18, at y ≈ +26, top at z ≈ 33.
  - **Right side arm**: from the right end of the crossbar **back along the robot's right side** of the lid to the rear-right, ending at about (+20, −16).
  - **Rear crossbar**: from (+20, −16) inboard to about (−2, −20) (AWS72 px ≈ (600–760, 60–110)). The loop is **open on the left side**.
  - **Legs**: the crossbar's free left end turns **down onto the lid** as a leg (AWS72 px ≈ (700–760, 500–560); AWS76 px ≈ (450–490, 310–360)). The right-front corner is supported by the lid edge. The rear end stands on the rear cover.
- **Surface**: a **matt, slightly rough black** (a different finish from the body; possibly printed in TPU or with a fuzzy-skin setting).
- **Function**: see §12. A **carry handle**, and a **roll hoop** that keeps the robot from sitting flat on its lid when inverted.

### 2.9 Googly eyes (EY-L, EY-R)
- Two **oval white stickers**, each about **10 × 12 mm**, with a **black D-shaped pupil** looking down/forward (the pupil is at the lower front edge of each oval). On the lid at about **(−9, +12)** and **(+6, +18)**: not side by side, but **offset diagonally**, the right eye further forward. They give the robot a cartoon face.

### 2.10 Power switch (SWT)
- A **miniature slide switch**, **≈ 7 × 4 mm** visible, with a white body (AWS74/76) or silver metal shell (AWS72), mounted **flush in a rectangular hole** in the lid at about **(0, +8)**, between and behind the eyes. AWS76 shows a small **arrow or "ON" mark** printed beside it.

### 2.11 Weapon motor screws (MS)
- **4 black socket button-head screws** with **silver washers**, head Ø ≈ 4 mm, washer Ø ≈ 6 mm, at the corners of a diamond of **≈ 16 mm** across (screw centres at r ≈ 8 mm from the motor axis). The diamond is rotated 45° to the body axes. Centre of the pattern: **(0, +40)**. This matches the **M2 mounting pattern of an 1806-class outrunner** (16 mm / 19 mm holes) **(guess, high)**.

### 2.12 Weapon motor (WM), hidden
- An **outrunner** (spec: 1806, 2300 kV) mounted **upside down** under the nose plate: the stator base is screwed to the nose underside by the 4 MS screws, and the **rotating bell faces down**. The bell carries the hub and blade. Size **Ø 23 × 18 mm** **(guess, high from the screw pattern)**.

### 2.13 Hub (HUB)
- A **black printed (or aluminium, black) disc**, about **Ø 26–30 mm × 6–8 mm**, under the nose plate and above the blade, concentric with the motor. Visible in AWS72 (px ≈ (830–1080, 760–930)) and AWS74 (px ≈ (830–1090, 650–760)) and AWS76 (px ≈ (400–680, 590–700)). It has a **flat bottom face** and a **small chamfer**. The blade is clamped between the hub and the motor bell or bolted to the hub **(guess)**.

### 2.14 Spinner blade (BL)
- **Material**: **hardened steel plate, ≈ 3 mm thick**, dark grey with blued/heat-tinted patches and bright, scratched edges.
- **Plane**: horizontal, at **z ≈ 2–5** (the bottom of the blade ≈ 2 mm above the floor).
- **AWS72 / AWS74 version (straight fishtail bar)**:
  - A **straight bar** about **12 mm wide** with **parallel edges**, total length **≈ 70 mm** tip to tip.
  - **Ends**: each end **flares to ≈ 24 mm** across, ending in a **concave "fishtail"** cut. That gives each end **two sharp corner tips** (impact points), at r ≈ 35 mm.
  - **Holes**: one **Ø 4 mm** hole in each arm at r ≈ 18 mm (AWS72 px (1185, 715)), plus a centre bore. AWS74 shows two small holes along the visible arm.
- **AWS76 version (crescent)**:
  - A shorter, wider shape: each end is a **crescent (hook)** about **26 mm across**, with a **large Ø ≈ 10 mm hole** at r ≈ 18 mm. The crescent's concave edge faces **forward in the direction of rotation** and its two points are sharp. This matches the spec blade (a 60 mm prism with hooked ends and r = 4.5 holes at x = ±18.6).
- **Direction of rotation (guess)**: the concave/hook faces lead, so the blade's leading face is the hook. In AWS76 the visible crescent's hook points toward the image bottom-left; in plan that suggests **clockwise from above** **(low)**.
- **Reach**: the tips sweep a circle of **r ≈ 35 mm** around the motor axis at (0, +40), so the blade reaches **y ≈ +75 at the front (≈ 22 mm ahead of the nose)** and **x ≈ ±35 at the sides**, inside the guards' width.

### 2.15 Wiring (WR)
- In the gap between the lid's rear-right corner and the right guard (AWS72 px ≈ (570–700, 80–240); AWS74 px ≈ (530–690, 80–200)):
  - a **white heat-shrink sleeve** about **Ø 5 × 12 mm** (a joint or a connector),
  - a **red silicone wire** (~ 22 AWG), with a red loop at the bottom,
  - a **black wire** with a white label band or printed lettering (AWS72 shows "MFO..." lettering on a black sleeve).
- These are probably the **battery leads** going to the switch or the weapon ESC **(guess, medium)**.

---

## 3. Per-view sections

### 3.1 AWS72 (front-left, ≈ 35° above)
- **Silhouette**: an arrowhead pointing at the image lower right, with the blade protruding as a long bar to the right (px x 1080–1430) and a crescent to the lower left under the body (px x 590–760, y 820–930).
- **Left side**: the left guard (px x 40–330, y 230–720) with its silver axle screw at (165, 380); the left flank sloping down to the nose; the nose edge (px ≈ (900–1080, 640–700)).
- **Top**: the rear cover, the lid with eyes and switch, the U-handle, the wires in the right-rear gap, the right guard's top at (560–890, 40–230), and the 4 nose screws.
- **Under the nose**: the black hub and the blade.

### 3.2 AWS74 (front-left, slightly higher)
- The same layout. The blade points toward the camera (px (880–1150, 690–940)), its fishtail end at the bottom. The left flank shows the damage marks and the guard axle screw at (215, 355).

### 3.3 AWS76 (front-right, ≈ 25° above)
- **Silhouette**: the arrowhead pointing left. The **right guard** is large and square to the camera (px x 1220–1640, y 250–870), with its axle screw at (1460, 435). The right flank runs from the nose (px x 270) to the guard (px x 1220), its bottom edge rising toward the nose.
- **Top**: the lid with eyes, the switch, the handle crossbar running diagonally across the image, the rear cover beyond, and the black wheel tops showing in the open wells (right well px ≈ (1250–1440, 270–400); left well px ≈ (760–880, 90–150)).
- **Under the nose**: the hub disc (px (400–680, 590–700)) and the crescent blade end (px (60–470, 720–1000)).

### 3.4 Top view (synthesised)
- An arrowhead 96 wide × 98 long. Two open wells at the rear corners with the wheel tops. A pentagonal lid in the middle with the U-handle along its front and right edges and the eyes and switch. The rear cover between the wells. The nose with the 4-screw diamond. The blade's swept circle (r 35) centred at (0, +40), extending 22 mm beyond the nose.

### 3.5 Side view (synthesised, right)
- A low profile: the guard rectangle at the rear (24–26 tall, reaching the floor); the flank sloping down toward the nose (top 23 → 22, bottom 2 → 10); the nose plate (z 10–22); the hub (z 5–10) and blade (z 2–5) under the nose, the blade sticking out ahead. Above: the handle loop (top z ≈ 33) and the rear cover.

### 3.6 Front view (synthesised)
- The nose (20 wide, z 10–22) in the centre, with the blade spanning up to ±35 at z 2–5 below it. Behind, the flanks spread out to the guards (±48). The handle crossbar shows above the lid at z ≈ 33.

### 3.7 Rear view (not photographed; inferred)
- The rear wall between the two guards, ≈ 84 mm wide × 24 tall; the rear cover on top; perhaps a charging connector **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to L | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | kite tub | 96 × 98 × 24 (rear) | 0.98 × 1 × 0.24 | black FDM (nylon/PETG) | — | 1 |
| NS | thick nose plate | 20–44 wide × 30 × 12 | 0.31 long | black | integral | 1 |
| GD | outer guard wall | 38 × 3 × 25 | 0.39 | black | integral | 2 |
| WH | wheel | Ø 22 × 9 | 0.22 | black TPU/rubber | axle screw | 2 |
| AX | socket cap screw | M3, head Ø 5.5 | — | silver | through the guard | 2 |
| LD | pentagon plate | 48 × 40 × 2 | 0.49 | black FDM | 4 × M2 Phillips | 1 |
| RC | textured panel | 40 × 18 × 2 | 0.41 | black textured / TPU | clipped or screwed (guess) | 1 |
| HB | U loop, round bar | Ø 5, 42 × 46 loop, 6–8 high | 0.47 | black rough FDM | legs into the lid (guess) | 1 |
| EY | oval sticker | 10 × 12 | — | white + black | adhesive | 2 |
| SWT | slide switch | 7 × 4 visible | — | white/silver | in the lid | 1 |
| MS | button head + washer | M2, head Ø 4 | — | black + silver | into the motor | 4 |
| WM | outrunner | Ø 23 × 18 | — | metal | 4 × MS | 1 |
| HUB | disc | Ø 28 × 7 | 0.29 | black | on the motor bell | 1 |
| BL | bar blade | 70 × 12 (ends 24) × 3 (AWS72/74) or 60 × 26 crescents (AWS76) | 0.71 | hardened steel | hub bolts | 1 |
| S-LD | Phillips pan | head Ø 3.5 | — | black | lid to body | 4 |

---

## 5. Contact / gap matrix (estimated mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD ↔ BD wall tops | rests on, screwed | 0 |
| RC ↔ BD rear top | rests on | 0 |
| RC top ↔ LD top | step | +2 to +3 |
| HB legs ↔ LD | fixed | 0 |
| HB bar underside ↔ LD top | clearance under the bar | 4–6 |
| SWT ↔ LD | flush in a hole | 0 |
| GD ↔ BD | integral | 0 |
| WH outer face ↔ GD inner face | running gap | 1–2 |
| WH inner face ↔ tub inner wall / motor | near | 1–2 |
| WH top ↔ GD top | below | −5 |
| WH bottom ↔ floor | contact | 0 |
| GD bottom ↔ floor | clearance | 1–2 |
| AX ↔ GD | screwed through | 0 |
| AX ↔ WH hub | axle (bearing or bore) | 0 |
| MS ↔ NS top | seated with washers | 0 |
| WM base ↔ NS underside | screwed | 0 |
| HUB top ↔ NS underside | running gap | 1–2 |
| BL ↔ HUB | clamped | 0 |
| BL bottom ↔ floor | clearance | ≈ 2 |
| BL tip circle ↔ nose tip | blade reaches past | +22 |
| BL tip circle ↔ flanks | running clearance in plan | ≥ 5 (flanks diverge behind the blade circle) |
| BD flank bottom ↔ floor (mid) | clearance | ≈ 5 |
| WR ↔ gap behind LD | loose in the gap | — |

---

## 6. Mechanism

1. **Weapon**: an **outrunner bell-driven bar** under the nose (direct drive, no belt). The blade spins in a horizontal plane ≈ 2–5 mm above the floor and hits opponents **at their lowest edges** (wedge lips, wheels, the bottoms of side walls). Tip speed at a plausible 15 000 rpm (1806 at 2300 kV on 2S ≈ 17 000 rpm no-load) and r = 35 mm: v = 2π·0.035·250 ≈ **55 m/s** **(guess)**.
2. **Drive**: two rear wheels, **skid steer**. The front rests on the **hub/blade** region or on the nose underside; the robot is effectively **three-point** (two wheels plus the nose) **(guess: a small skid under the nose or the hub bottom carries the front load; with the blade stopped, the blade itself may touch the floor)**.
3. **Invertibility**: the wheels are **below the guard tops**, so upside down the wheels do **not** reach the floor. The robot is **not invertible**; the **handle loop** would make it rest at an angle on the bar and guard tops. The designer probably relies on a low centre of mass and the wide guards to avoid being flipped **(guess, medium)**.

---

## 7. Assembly order (suggested rebuild)

1. Print **BD** (tub, guards, flanks and nose in one piece, floor on the bed).
2. Fit the **drive motors** (two N20-class gearmotors, guess) inside the tub at the rear, shafts outward. Push the **wheels** onto the shafts or hubs, then insert the **axle screws AX** through the guards into the wheel hubs/bosses for outer support.
3. Screw the **weapon motor WM** to the nose underside with the **4 MS screws and washers** from the top.
4. Fit the **hub** and **blade** to the motor bell and secure them (2–3 small screws or a central nut, **guess**).
5. Install **battery, ESCs, receiver**, route the wires; the weapon leads run forward under the lid to the nose.
6. Fit the **switch** into the lid, fit the **lid** (4 screws), the **rear cover**, and the **handle** loop.
7. Apply the **googly-eye stickers**.

---

## 8. Profiles as math (for rebuilding curves)

**8.1 Body plan outline (XY).** Polygon, then a nose arc:
(−42, −48) → (+42, −48) → (+48, −10) → (+38, +14) → (+22, +36) → (+9, +48) → arc → (−9, +48) → (−22, +36) → (−38, +14) → (−48, −10) → close.
Nose arc: centre (0, +44), r = 9.8, from θ = −24° to θ = 204° (measured from +X), i.e. tip at (0, +53.8).
Flank lines in slope-intercept form (right side; mirror for the left): **x = 48 − 0.4167·(y + 10)** for y ∈ [−10, +14]; **x = 38 − 0.727·(y − 14)** for y ∈ [+14, +36]; **x = 22 − 1.083·(y − 36)** for y ∈ [+36, +48].

**8.2 Side wall lower edge (YZ projection).** z_bottom(y) = 1.5 for y ∈ [−48, −10] (guard), then **z_bottom = 5 + 0.13·(y + 10)** for y ∈ [−6, +38] (rising to ≈ 10.7), then flat at 10 for the nose. The step at y ≈ −8: a vertical edge from z 1.5 to z 5.
**Top edge**: z_top = 27 for y ∈ [−48, −12] (guard), then **z_top = 25 − 0.05·(y + 12)** to the nose (z ≈ 22 at y ≈ +48).

**8.3 Blade (AWS72/74 fishtail bar, XY in the blade frame, origin at the motor axis).**
- Centre bar: |y'| ≤ 6, |x'| ≤ 28.
- Flare: for x' ∈ [28, 33], half-width grows linearly: **|y'| ≤ 6 + 1.2·(x' − 28)** (to 12 at x' = 33).
- Fishtail end: the end edge is a **concave arc**, centre (x' = 42, y' = 0), r = 9.5, cut from the end of the flared region. The two tips are at about (35, ±12).
- Holes: Ø 4 at (±18, 0); centre bore Ø 5 (or the motor's 4-hole pattern).
- Extrude 3 mm.

**8.4 Blade (AWS76 crescent, as the spec).** Polygon in the blade frame: (−30, −1), (−24, −7), (−10.5, −7), (10.5, −9), (24, −7), (30, −1), (27, 8), (21, 13), (16.5, 0), (9, 7), (−9, 7), (−16.5, 0), (−21, 13), (−27, 8). Holes Ø 9 at (±18.6, 0). The concave notch between (21, 13), (16.5, 0) and (27, 8) is the **hook**.

**8.5 Handle HB (centreline path, in world coordinates, round section r = 2.5).**
P1 (−24, +26, 25) up to P2 (−24, +26, 32.5) [leg], then a straight bar to P3 (+18, +26, 32.5), a corner arc (r = 4) to P4 (+22, +22, 32.5), a straight bar to P5 (+22, −14, 32.5), a corner arc (r = 4) to P6 (+18, −18, 32.5), then to P7 (−2, −18, 30) where it meets the rear cover.

**8.6 Wheel tread.** Three ribs: r(x_w) = 11 for |x_w| within each 2.5 mm rib, r = 9.5 in the two 1 mm grooves between ribs (x_w along the axle).

**8.7 Hub.** A cylinder r = 14, z ∈ [5, 10], with a 1 mm × 45° chamfer at the bottom edge.

---

## 9. Pixel-based measurements (independent check)

**AWS72 (1447 × 980):**
- Body extent along its axis: rear-left corner px (40, 240) to nose tip px (1085, 640): ≈ 1120 px (foreshortened).
- Left guard: px x 40–330, top y ≈ 230, bottom y ≈ 720 (≈ 490 px tall including the slope and perspective).
- Nose screw diamond: px (870–1010, 500–620) → ≈ 140 px across for 16 mm → ≈ 8.8 px/mm at the nose.
- Hub: px (830–1080, 760–930), ≈ 250 px wide → 250/8.8 ≈ 28 mm.
- Blade, right arm: from the hub centre px ≈ (950, 840) to the tip px (1430, 700): ≈ 500 px.
- Eyes: ≈ 90 × 110 px each.

**AWS74 (1225 × 1007):**
- Nose screws: px (900–1050, 420–520), ≈ 150 px.
- Blade arm visible: from px (1000, 700) to (1140, 1000).
- Fishtail end: px (885–1145, 905–945) → ≈ 260 px wide (near the camera).

**AWS76 (1687 × 1069):**
- Body extent: nose px x ≈ 270 → rear px x ≈ 1640 = **1370 px**.
- Right guard face: px x 1220–1640 = 420 px long, y 250–870 (≈ 620 px tall, including the slope).
- Hub: px x 400–680 = 280 px.
- Crescent end: px (60–470, 720–1000); big hole px (165–310, 840–905) → ≈ 145 px.
- Motor screw diamond: px (345–600, 480–580), ≈ 255 px across.

---

## 10. Several independent estimates of key quantities

| Quantity | Method A (spec / limits) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body length | spec 100 (y −48..+52) | fits the cube; arrowhead looks about as long as wide | AWS76: 1370 px; screw diamond 255 px = 16 mm → 16 px/mm (nose depth) → 86 (rear is farther, smaller) → ≈ 98 corrected | **98** |
| Body width | spec 100 (±50) | ≈ 1.0 L | AWS72 guard-to-guard not visible together | **96** (must fit the cube with margin) |
| Hub Ø | spec 26 | 0.29 L | AWS72 250/8.8 = 28; AWS76 280/16 = 17.5 (the hub is seen edge-on, so its visible width is its diameter only if fully seen: partial) | **28** |
| Blade length (fishtail) | spec 60 (crescent version) | AWS72: one arm ≈ 0.45 × the body's visible length → 2 × 0.45 × 98 ≈ 88 (near the camera, inflated) | AWS74 fishtail width 260 px / ≈ 11 px/mm (near) = 24 | **70 tip to tip** |
| Crescent hole Ø | spec 9 | — | AWS76 145 px / 14 px/mm = 10 | **9.5** |
| Guard height | spec walls 24 | 0.25 L | AWS76 620 px includes ≈ 30% slope → 430 px / 16 = 27 | **25** |
| Wheel Ø | spec 22 | below the guard top (27) with clearance → ≤ 24 | AWS72 ribs ≈ 130 px across at ≈ 7 px/mm (far corner) ≈ 19 | **22** |
| Handle bar Ø | spec 5 × 6 box | — | AWS76 crossbar ≈ 70 px thick / 14 = 5 | **5** |

---

## 11. Consistency check: conflicts and reconciliation

1. **Blade length (88 vs 70 vs 60).** AWS72's arm is near the camera and stretched by perspective; the spec's 60 mm matches the AWS76 crescent version. The fishtail bar looks longer than the crescent in all views. **Reconciled: fishtail 70, crescent 60**; both are about 3 mm thick, with a swept circle of r 30–35.
2. **Blade reach vs flanks.** With the motor axis at y = +40 and r = 35, the blade sweeps to x = ±35 at y = +40. The flanks at y = +40 are at x = ±17.7, so the blade sticks out **≈ 17 mm** each side of the body there. At y = +14 (shoulders, x = ±38) the blade circle reaches only to x = ±√(35² − 26²) = ±23.4, well inside. **So the blade never hits the body. Consistent.**
3. **Wheels hidden vs drive.** The wheels are inside guards whose tops are above them and whose bottoms are only 1–2 mm off the floor. If the floor clearance under the guards were larger than the wheel's reach, the robot would sit on the guards. With Ø 22 wheels at z = 11 the tyres reach z = 0 and the guards at z = 1.5: **consistent**, with only 1.5 mm margin (so on uneven floors the guards may drag).
4. **Front support.** If the wheels are at y = −28 and the CG is near y = 0, the front must rest on something. The hub bottom (z ≈ 5) and blade (z ≈ 2) are above the floor; the nose underside (z ≈ 10) is too high. **Reconciled (guess)**: either a small **skid/standoff under the hub** (the hub bottom has a dome) or the robot leans forward until the **blade tips touch the floor** (which would be a bad design for a spinner). More likely the **hub's lower face** is the front bearing surface, i.e. the hub is a **low-friction skid** at z = 0 on the motor axis: the "hub" visible under the nose then reaches the floor, and the blade sits **above** the hub's bottom by 2–3 mm. **Adopted: hub bottom at z = 0.5, blade at z = 3–6, hub top at z = 9.**
5. **Lid height vs guard tops.** Lid at z ≈ 25, guard tops at 27, rear cover 27–29, handle top 33. In AWS76 the handle is clearly the highest point and the guard tops are about level with the rear cover. **Consistent.**
6. **Two blade versions.** Different events; build the AWS72 fishtail bar as the default and record the AWS76 crescent as the alternative.

---

## 12. Why the designer did it (per part, mostly adversarial)

- **Undercutter blade under the nose**
  - Getting under vs contact: an undercutter does not need to get under; it **hits the bottom edges** of opponents. Most antweight wedges have their thinnest, most fragile part at the floor, and the blade hits exactly there. It also strikes **wheels** of robots without guards.
  - Attacks on it: opponents' wedges can ride up onto the nose, but they meet the spinning blade first (it reaches 22 mm ahead of the nose). A vertical spinner hitting the nose hits the blade or hub. The hub absorbs ground contact.
  - Why steel and why a bar: a bar concentrates mass at the tips (high energy for little weight). Hardened steel resists chipping. The fishtail/crescent ends give **two sharp tips per end**, so the tooth "bites" rather than glancing off.
- **Direct-drive outrunner hanging under the nose**: no belt or pulleys to fail; simple and light. The motor is protected from above by the 12 mm nose plate, and the 4 screws go through the full thickness. **Weakness**: hits on the blade go straight into the motor bearings; the motor can be knocked loose.
- **Arrowhead body**
  - Attacks: the angled flanks **deflect** horizontal spinners' hits and opponents' pushes sideways. The narrow nose keeps the front of the body inside the blade's swept circle, so opponents reach the blade before the body.
  - Getting under: the rising lower edge of the flanks keeps the body clear of the floor near the blade so debris and opponents' wedges hit the blade, not the body.
- **Thick nose plate**: the most-hit area of the body. 12 mm of solid print spreads the motor's reaction torque and impact loads into the flanks. The chewed edges in AWS72/74 show it gets hit hard.
- **Rear wheel guards (tall, enclosing)**
  - Attacks: they hide the tyres completely from the side and front, so a horizontal spinner cannot hit the wheels, and an opponent's wedge cannot climb the tyres. The axle screw through the guard gives the wheel **double support** (motor + guard), which resists being knocked sideways.
  - Weakness: the guards make the robot **non-invertible**; the open-topped wells let debris fall in and let overhead attacks reach the wheels.
  - Construction: printed with the tub (no separate guard supports). The axle screw is a cheap, replaceable outer bearing.
- **Lid and rear cover**: removable access to the electronics. The lid is 3 mm above the nose plate, so an opponent sliding over the nose climbs a step. The rear cover's texture may be a TPU panel that **absorbs hits** from above **(guess)**.
- **U-shaped handle / roll bar**
  - Practical: a **carry handle** for removing the robot from the arena safely (the spinner is under the body, so picking it up by the body is risky).
  - Adversarial: if flipped, the robot lands on the handle and guard tops instead of on its lid; the handle keeps the switch and eyes from being scraped. The open side lets wires and the switch be reached.
- **Switch on the lid**: easy to reach without lifting the robot (important for a spinner: arm and disarm without putting hands near the blade). It is flush, so it is hard to knock.
- **Googly eyes**: character; no fight function.
- **Wires in the gap**: a sign of a tight interior; the leads are exposed to overhead hits **(weakness)**.

---

## 13. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors DM-L/R | 2 × N20 gearmotors (6 V, about 300–600 rpm) | 12 × 10 × 25, + 9 shaft | along X at (±24, −28, 11), shafts outward | medium |
| Motor mounts | printed **plastic saddles** with a clamp strap and 2 × M2 screws each, or a pocket in the tub floor | 16 × 14 × 14 | over each motor | medium |
| Wheel hub / bearing | printed hub with a D-bore; the AX screw runs into a brass bushing in the hub's outer face | Ø 10 | in each wheel | low |
| Battery | 2S LiPo, 300–450 mAh | 45 × 20 × 12 | centre-rear, (0, −20, 12) under the rear cover | medium |
| Drive ESC | dual brushed ESC | 25 × 15 × 5 | (−12, 0, 8) | low |
| Weapon ESC | 20–30 A brushless ESC | 30 × 15 × 6 | (+10, +8, 8), close to the motor leads | medium |
| Receiver | micro 2.4 GHz | 20 × 12 × 5 | (0, −5, 18) | low |
| Weapon motor leads | 3 phase wires through the nose plate into the tub | 30 mm | from (0, +40, 10) back to the WESC | high |
| Lid supports | 4 screw bosses with M2 inserts at the lid corners | Ø 6 | under each S-LD | medium |
| Handle mounting | 2–3 pegs or M2 screws from below the lid into the handle legs | — | at the handle legs | low |
| Hub fixing | 2–3 M2 screws from the hub into the motor bell, blade clamped between | — | r ≈ 6 | medium |

**Wiring path summary (guess)**: battery under the rear cover → switch in the lid → both ESCs; drive leads short to the rear motors; weapon phase leads forward under the lid to the nose and down through the plate to the motor. The red/black leads seen in the right-rear gap are the battery leads.

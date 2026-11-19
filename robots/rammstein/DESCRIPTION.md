# Rammstein: full rebuild description from reference photos

Source photos (in `robots/rammstein/reference/`):
- `rammstein.aws70.png` (855 × 681 px): a **pit-table snapshot**, not cut out. The robot is the **black version**, seen from the **front-left, about 35–40° above horizontal**, with the front pointing to the image left/bottom-left. A greyish-tan sheet-metal wedge fills the lower left. The photo is slightly soft. **Other robots also appear in this photo**: the black curved shell with a silver screw and a slot at the bottom right, and the black parts with stickers at the top right, are neighbouring robots, **not** Rammstein **(high confidence: the shell's curvature and slot match nothing on the other two photos)**. The robot sits on a clear plastic box with a green and red card under its wedge.
- `rammstein.aws71.png` (1114 × 1296 px): **black version**, cut out onto white. A **high view from the front, about 50° above horizontal**. The front wedge is nearest the camera (image bottom) and the rear notch is at the image top. This is the best plan-view photo.
- `rammstein.aws72.png` (1545 × 1041 px): **green version**, cut out onto white. A **high three-quarter view from the rear-left, about 30–35° above horizontal**. The rear (with two sloped lobes and a notch) is at the image lower left and the aluminium front wedge is at the upper right.

Everything stated as fact below is read from those photos. Anything inferred is marked **(guess)** with a confidence where useful. All dimensions are **estimates in mm**. They are scaled from the AWS antweight limits (150 g, must fit a 101.6 mm cube) and cross-checked against the project spec draft (`spec.json` uses a chassis about 70 mm wide and 84 mm long, wheels at x = ±34.4, y = ±24, and a carbon plate at z ≈ 6 above its own datum). Ratios are given against **W = chassis tub width ≈ 72 mm**.

Rammstein is a **four-wheel box wedge / pusher**. It has no active weapon. Its "weapon" is a full-width sheet-metal front wedge, plus (green version) a hinged FR4 wedgelet at the front corner.

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) directly under the centre of the chassis tub footprint (mid-width, mid-length of the tub, **not** including the wedge).
- **+X** = robot's right, **+Y** = forward (toward the metal wedge), **+Z** = up. Units are mm. Profile angles are measured from the floor (XY plane) unless stated otherwise.
- **Front** = the metal-wedge end. **Rear** = the notched end with the two lobes.
- In AWS71 the robot's left is on the image left (the camera is in front, looking back and down, so the image is left–right mirrored relative to a top view from behind; I correct for that in all positions below). In AWS72 the robot's left side and rear face the camera. In AWS70 the robot's left side and front face the camera.

Part IDs:

| ID | Part |
|---|---|
| CH | printed chassis tub (black in AWS70/71, dark green in AWS72) |
| WG-FL / WG-FR | front wheel guards / front pods (integral side walls outboard of the front wheels) |
| WG-RL / WG-RR | rear wheel guards / rear lobes (outboard of the rear wheels, forming the rear prongs) |
| SW-L / SW-R | mid side walls (between the front and rear wheel wells) |
| RN | rear notch (trapezoid cut in the rear of the tub, between the rear lobes) |
| BT | black bumper/trim strip on top of the rear lobes (AWS72) |
| TP | carbon-fibre top plate (cross-shaped) |
| TPN | trapezoid notch in the rear tongue of TP |
| WC-1…4 | four wheel cut-outs in TP (the corners of the cross) |
| LG | Rammstein logo sticker (square) |
| TX | "RAMMSTEIN" text sticker |
| SS | power switch slot in TP (oval, AWS70/71) |
| SWT | power switch (black toggle/slide, under SS) |
| LNK | red removable link / switch key (AWS72) |
| WD | sheet-metal front wedge (stainless/titanium-look in AWS70/71, aluminium in AWS72) |
| WD-FL | wedge side flanges (folded up, AWS71) |
| WD-B | wedge bend line (flat top tab to sloped face) |
| FX | green FR4 hinged wedgelet / flap on the front-right corner (AWS72) |
| WH-FL, WH-FR, WH-RL, WH-RR | four wheels, grey/black treaded tyres |
| HB-x | wheel hubs (dark, visible inside the tyres in AWS71) |
| M-x | drive gearmotors (hidden, guess) |
| MM-x | plastic motor mounts / clamps (hidden, guess) |
| S-TP | top-plate fasteners (button-head sockets and nyloc nuts) |
| S-WD | wedge fasteners (flange screws and front-tab screws) |
| S-FX | FR4 flap hinge screw |
| BAT, ESC, RX | battery, ESCs, receiver (hidden, guess) |
| WR | wiring (hidden, guess) |

---

## 1. Overall description in one paragraph

Rammstein is a **low, flat, four-wheel box wedge**. Its body is a **printed tub** (black or dark green), about **72 mm wide, 78 mm long and 21 mm tall**. The tub encloses all four wheels: each wheel runs in its own **well**, with a solid printed **wall outboard of the tyre** acting as a wheel guard. The tub is closed on top by a **cross-shaped carbon-fibre plate** about 1.5 mm thick. The plate is full width only in a central band between the front and rear wheel pairs. In front of and behind that band it narrows to a tongue about 44 mm wide, so the **tops of all four tyres show through four rectangular corner cut-outs**. The plate carries a square **Rammstein cross logo** sticker and a **"RAMMSTEIN" text** sticker and is held by **12–14 small socket screws and nyloc nuts**. At the **front**, a **full-width sheet-metal wedge** (about 74 mm wide) is clamped under the front edge of the plate and slopes down to the floor at about **35°**, reaching about **24 mm** ahead of the tub. In AWS71 its sides are **folded up as flanges** screwed to the tub. At the **rear**, the tub ends in **two lobes with a trapezoid notch** between them. In the green version the lobes have **sloped rear faces** and a **black trim strip** on top. The wheels are about **Ø 24 mm**, slightly taller than the tub, so their tops stand **about 2–3 mm proud of the top plate**, and the robot can drive inverted. The green version adds a **hinged green FR4 flap** on the front-right corner and a **red link/key** poking up through the aluminium wedge.

---

## 2. Part-by-part description

### 2.1 Chassis tub (CH)
- **Overall shape**: a rectangular tub. In plan it is about **72 mm wide (x ∈ [−36, +36]) × 78 mm long (y ∈ [−40, +38])**. Wall-top height is about **21 mm** (z from ≈ 2 to ≈ 21; ground clearance ≈ 2 mm **(guess)**). Plan corners are sharp at the front, with a small radius (≈ 2 mm) at the outer rear corners (AWS71 top-right corner looks slightly rounded).
- **Colour / material**: AWS70/71 **matt black** printed plastic with a slightly sparkly, rough finish (likely black PETG or nylon; the spec says nylon). AWS72 **dark bottle-green** printed plastic with very clear **horizontal layer lines** (≈ 0.2 mm) on all vertical walls, so it was printed upright (floor on the bed).
- **Floor**: never seen. Presumed flat, **≈ 2 mm thick**, with the wheel wells open through it so the tyres touch the floor **(guess, high confidence: the tyres must reach the floor)**.
- **Wheel wells**: four rectangular pockets, one per wheel, open at the top (under the plate cut-outs) and at the bottom. Each is about **10–11 mm wide (X) × 27–28 mm long (Y)**, i.e. tyre width + about 1–1.5 mm each side and tyre Ø + about 1.5–2 mm each end. Centres at x ≈ ±27.5, y ≈ ±21.
- **Internal bay**: the central space between the four wells, roughly **x ∈ [−22, +22], y ∈ [−36, +34], z ∈ [4, 20]**, holds the motors, battery and electronics **(guess)**.

### 2.2 Front wheel guards / front pods (WG-FL, WG-FR)
- **Shape**: solid printed blocks forming the outer wall of each front wheel well and the front corners of the tub. Each is about **4–5 mm wide (X, x ∈ ±[31.5, 36])**, **≈ 30 mm long** (y from ≈ +8 to ≈ +38) and full tub height (**≈ 19–21 mm**).
- **AWS72** (green version, front-right pod clearly seen at the image upper right and lower right): the pod top carries a **raised embossed text strip** along its length (a row of small raised letters/characters about 2 mm tall, illegible; perhaps the robot's name or a builder's mark). The pod's front face is **chamfered** (sloped back from the bottom) and meets the wedge flank. The **green FR4 flap FX** is screwed to the outer face of the front-right pod.
- **AWS71** (black): the front pods are hidden behind the wedge flanges WD-FL, which overlap their outer faces.
- **Function**: they are both the wheel guards and the anchor points for the wedge flanges.

### 2.3 Rear wheel guards / rear lobes (WG-RL, WG-RR)
- **Shape (AWS71, black)**: two rectangular blocks forming the rear corners. Each lobe spans from the side wall inwards to the edge of the rear notch, i.e. **x from ±14 to ±36 (≈ 22 mm wide)**, and from **y ≈ +2 back to y = −40**. The rear face is vertical and flat; the top is flat at z ≈ 21. The rear wheel wells are cut into the inboard-front part of each lobe.
- **Shape (AWS72, green)**: the lobes are **much more pronounced**. Each has a **flat top** (z ≈ 21) that runs back to about y ≈ −28, then a **sloped rear face at about 40–45°** down to a short vertical face (≈ 6–8 mm tall) at the rear edge y ≈ −42. Seen from the rear-left, the lobes look like two **ramps**. The inner faces of the lobes (facing the notch) are vertical, with layer lines, and are angled slightly in plan (the notch widens toward the rear).
- **Black trim strip BT (AWS72 only)**: along the top outer edges of both rear lobes, and down the edge of the notch, there is a **dark, slightly irregular band about 2–3 mm wide**. It looks like a **black TPU or rubber edge strip**, or black tape folded over the edge. Its edges are wavy, which suggests it is hand-applied tape or a soft printed overlay rather than a crisp print **(guess)**.

### 2.4 Mid side walls (SW-L, SW-R)
- Between the front and rear wheel wells, each side of the tub is a plain vertical wall at **x = ±36**, about **18 mm long** (y ≈ −9 to +9) and full height. Wall thickness is about **3 mm** **(guess)**. In AWS72 the left mid-wall is visible below the plate's full-width band, plain green with layer lines and no screws.

### 2.5 Rear notch (RN)
- **Shape**: a trapezoid cut through the full height of the tub at the rear centre. **Mouth (at y = −40) ≈ 30 mm wide (x ±15)**, **floor (at y ≈ −30) ≈ 20 mm wide (x ±10)**, **depth ≈ 10 mm**. The sides are angled about **26°** from the Y axis in plan. The notch floor is a vertical wall (the rear wall of the internal bay).
- **AWS71**: seen at the top centre of the image as a dip in the far tub edge (px x ≈ 545–720 at the edge, floor at px y ≈ 180).
- **AWS72**: the notch between the two green ramps is very clear, and its floor wall rises higher than the ramp ends.
- **Spec cross-check**: the spec notch is 39 mm wide at the mouth and 29 mm at an 11 mm depth. My photo estimate is about 25% narrower. See §13.

### 2.6 Carbon-fibre top plate (TP)
- **Material / colour**: **carbon-fibre sheet**, about **1.5 mm thick** (AWS71: black with a visible **twill weave**; AWS72: **green-tinted carbon** (green-dyed fibre or green resin) with a strong twill weave that gives a chevron pattern). The edges are slightly lighter where cut.
- **Plan shape (best in AWS71)**: a **cross / plus shape** made of three rectangles:
  1. **Central band**: full width, **x ∈ [−36, +36] (72 mm)**, **y ∈ [−9.5, +9.5] (19 mm)**. Its ends overhang the mid side walls flush (AWS71 shows the band reaching the tub sides).
  2. **Front tongue**: **x ∈ [−22, +22] (44 mm)**, **y ∈ [+9.5, +36]**. Its front edge sits just behind the wedge bend line.
  3. **Rear tongue**: **x ∈ [−22, +22]**, **y ∈ [−37, −9.5]**, with the **notch TPN** cut in its rear edge.
  - The re-entrant corners between band and tongues are sharp (radius ≤ 1 mm). The outer corners have about a **1 mm** radius.
- **Wheel cut-outs WC**: the four "missing corners" of the cross, each about **14 × 27 mm**, expose the tyre tops and the guard tops.
- **Notch TPN**: a trapezoid in the rear edge. **Mouth ≈ 16 mm wide (x ±8)**, **floor ≈ 8 mm wide (x ±4)**, **depth ≈ 6 mm**. It mirrors the tub notch RN at a smaller scale.
- **AWS72 differences**: the plate looks like the same cross, but its **front tongue is wider** (it reaches the inner faces of the front pods) and the plate front edge overlaps the **aluminium wedge tab**. One plate-edge corner near the left rear wheel shows a step.
- **Scuffs**: AWS71 shows a **grey abraded patch** at about (x +8, y −5) on the plate (px ≈ 700–770, 405–440) next to the logo, and a few **white scratch lines** at the rear right. These are hit marks from opponents riding over the top.

### 2.7 Stickers (LG, TX)
- **LG**: a square sticker about **18 × 16 mm**, centred at about **(x 0, y −4)** (AWS71) or slightly right of centre (AWS72). It shows the **Rammstein cross logo**: an outlined plus sign with an "R" inside, **white on black** (AWS71) or **red outline on dark green** (AWS72).
- **TX**: a narrow strip about **34 × 5 mm**, reading **"RAMMSTEIN"** in the band's blocky typeface. AWS71: **white letters on black**, laid along X at about **y +12** (front of the band, just behind the front tongue). AWS70: the same text at the front-left, white. AWS72: **red letters on white**, laid **along Y** at about **x −10, y 0 to −30**, i.e. rotated 90°.

### 2.8 Power switch slot (SS) and switch (SWT)
- **AWS71**: an **oval / slotted hole** about **4 × 9 mm** (long axis along Y), at about **(x 0, y +27)** on the front tongue, between two screws. Inside it a small **black slide or toggle lever** is visible.
- **AWS70**: a dark oval hole at the plate front-left, px ≈ (350, 345). It is the same slot seen obliquely.
- **Interpretation**: a **miniature slide switch** mounted under the plate, operated through the slot with a small screwdriver or finger **(high confidence)**.
- **AWS72**: no slot is visible on the plate. Instead a **red block LNK** about **7 × 5 × 5 mm** sticks up through the aluminium wedge tab at about **(x −14, y +34)**. It is likely a **removable link / red switch key**, or a red slide-switch knob **(guess, medium)**.

### 2.9 Front wedge (WD)
- **Material / colour**:
  - **AWS70**: a **matt greyish-tan metal**, slightly brown. It looks like **titanium or brushed stainless steel**, about **0.8–1.0 mm** thick.
  - **AWS71**: **matt dark grey metal** with scratches and scuffs, the same part as AWS70 (same photo era).
  - **AWS72**: **bright, matt aluminium**, scuffed, about **1.2–1.5 mm** thick (aluminium needs to be thicker for the same stiffness).
- **Shape (side profile, YZ)**: a sheet bent once along a transverse line WD-B.
  1. **Top tab**: a flat strip, **y ∈ [+30, +38]**, lying horizontally **under the front edge of TP** at z ≈ 19.5–20.5 (or on top of the tub front wall). It is clamped by the front plate screws S-TP and by its own screws S-WD.
  2. **Bend WD-B**: at y ≈ +38 (the tub front edge), inner radius about **1.5–2 mm**.
  3. **Sloped face**: from (y +38, z 20) down to the **leading edge at (y +62, z 0)**. The slope is about **35–40° to the floor** and the face is **≈ 31 mm long**. The leading edge is straight and sharp, running the full width.
- **Plan**: the wedge is about **74 mm wide** (x ∈ [−37, +37]), 1 mm wider each side than the tub. AWS71 shows the corners of the leading edge **slightly rounded** (≈ 3 mm radius) and the left edge at the bend has a small **notch**.
- **Side flanges WD-FL (AWS71)**: both side edges of the sloped face are **folded up 90°**, forming triangular cheeks about **6–8 mm tall** that run back to the tub and lie **flat against the outer faces of the front pods**. The left flange shows **three black button-head screws** (px ≈ (75, 870), (70, 1055), (80, 1150)) and the right flange **two** (px ≈ (962, 905), (962, 1100)). The flanges therefore bolt the wedge sideways into the pods.
- **AWS72**: the aluminium wedge has no visible flanges. Its sloped face spans between the two green front pods, whose inner faces bracket it; the screws at the pod tops (px ≈ (930, 140)) probably clamp the wedge tab **(guess)**.
- **AWS70**: the sheet's upper edge is tucked **under** the carbon plate. A row of **silver screws** runs along the front edge of the plate above it.

### 2.10 Green FR4 flap (FX), AWS72 only
- **Shape**: a flat **green FR4 / G10 plate**, about **1.5 mm thick**, roughly a **trapezoid about 22 mm long × 12 mm tall**. Its edges are sharp and pale (cut fibreglass), and it has a slightly translucent green look with a light circuit-board sheen.
- **Mount**: attached to the **outer face of the front-right pod** by **one socket screw S-FX** (px ≈ (1460, 515)) acting as a hinge. A second small screw or rivet is at the lower front of the plate.
- **Position**: x ≈ +37.5 (just outboard of the pod), from y ≈ +18 to y ≈ +40, with its lower edge reaching **the floor at its front tip**. In the photo it hangs **angled down and forward** by about 25–30°.
- **Interpretation**: a **free-hanging wedgelet / side skirt**. It drops to the floor under its own weight and gets under opponents that approach the front-right corner, covering the gap at the corner where the wedge leading edge ends **(guess, medium)**. A mirror flap on the left is probable but not seen **(guess, low–medium: the left front corner is hidden behind the plate in AWS72)**.

### 2.11 Wheels (WH-FL, WH-FR, WH-RL, WH-RR) and hubs (HB)
- **Tyre shape**: a cylinder about **Ø 24 mm × 8–9 mm wide**. The tread has **fine transverse ribs** about **1 mm** pitch across the full width (like a knurl or fine spur-gear teeth). The edges are slightly rounded.
- **Colour / material**: **grey-black rubber or foam** (AWS71: dusty grey, worn; AWS72: dark grey with a fine rib tread, look like moulded rubber or printed TPU). In AWS71 the tyres look **soft and slightly squashed** **(foam/rubber, guess)**.
- **Hubs HB**: dark **black/grey discs** about **Ø 16 mm** visible inboard of the tread in AWS71 (the dark part next to each tyre). They are possibly printed hubs with a tyre stretched over them.
- **Positions (centres)**: **x = ±27.5**, **y = ±21**, **z = 12**. So the **wheelbase is ≈ 42 mm** and the **track (tyre centres) ≈ 55 mm**.
- **Height**: Ø 24 with the centre at z = 12, so the tyre top is at z = 24. That is about **2.5 mm above the top of the carbon plate** (z ≈ 21.5), so the robot can drive inverted on its wheel tops. AWS70 and AWS72 both show the tyre tops standing slightly proud of the plate.
- **Running gaps**: tyre to guard inner face ≈ 1 mm, tyre to well ends ≈ 1–2 mm, tyre to plate cut-out edges ≈ 1–2 mm (AWS71 shows clear gaps around each tyre in the cut-outs).

### 2.12 Top-plate fasteners (S-TP)
- **Type**: **small socket button-head screws** (black in AWS71, silver/zinc in AWS72) with head Ø ≈ **4 mm**, and in AWS72 **silver nyloc nuts** standing ≈ **3–4 mm** proud of the plate with the screw tips poking through. That means at least some screws are fitted **from below with the nut on top**.
- **Count and positions (AWS71, black, plan positions after mirroring)**:
  - Rear tongue: 2 at (±15, −27); 2 at (±16, −15).
  - Band: 2 at the far ends (±33, −2), 2 near the front edge of the band (±30, +6).
  - Front tongue: 2 nyloc nuts at (±9, +13); 1 screw at (0, +16) behind the switch slot; 2 screws at (±12, +34) and 1 silver nut at (+3, +34) along the front edge (these also clamp the wedge tab).
  - Total ≈ **14**.
- **AWS72**: about **12** visible silver nuts/heads: near the rear notch (2), at the band ends (2), the band inner corners (2), the front tongue (4), and near the left rear wheel cut-out (2).
- **Size**: M2 or M2.5 **(guess)**, into heat-set inserts or nuts in the tub (the spec places inserts at the tub corners, (±26.9, +33.9) and (±24.9, −38.9)).

### 2.13 Wedge fasteners (S-WD) and flap screw (S-FX)
- **S-WD**: 5 black button heads on the AWS71 flanges (3 left, 2 right visible). In AWS72 one socket screw is visible on each front pod top near the wedge.
- **S-FX**: one socket button head, M2–M2.5, acting as the flap hinge.

### 2.14 Wiring and switch path
- **No external wires are visible** in any photo. A **small blue patch** at the front-right wheel well in AWS72 (px ≈ 1110, 515) may be **wire insulation or the blue end cap of a motor** seen through the gap between tyre and well **(guess, low)**.
- The switch SWT is under the slot SS. Battery leads presumably go from the battery to the switch, then to the ESCs, with motor leads to the four motors, all under the plate **(guess, high)**.

---

## 3. Per-view sections

### 3.1 AWS71: front view from high (≈ 50° down), black version
- **Bottom third**: the **metal wedge**, seen nearly face-on as a large dark-grey rectangle (px x ≈ 70–960, y ≈ 790–1250). Its leading edge is the bottom silhouette. The **left flange** stands up as a narrow strip at the left edge with three black screw heads; the **right flange** is at the right edge with two.
- **The bend line** shows as a thin lighter strip across the wedge at px y ≈ 840–870, where the top tab meets the slope. The carbon plate's front edge overlaps it in the middle.
- **Middle**: the carbon cross. Its band reaches the full width at px y ≈ 515–700. The **front-left and front-right tyres** show in the near corner cut-outs (px (150–270, 680–890) and (820–900, 700–880)). The **rear tyres** show in the far corner cut-outs (px (245–345, 335–510) and (865–940, 350–510)).
- **Logo** (px x 490–690, y 395–590) and **text** (px x 345–755, y 640–690).
- **Switch slot**: px (505–530, 780–830).
- **Top**: the black tub's rear edge with the **trapezoid notch** (px x 545–720), the plate's smaller notch (px x 540–725 at the edge, floor at y ≈ 270), and the rear lobes' flat tops.

### 3.2 AWS72: rear-left three-quarter, green version
- **Near (lower left)**: the two **rear ramps** with their sloped faces and black edge trim, and the **notch** between them. The left ramp's sloped face is the largest flat area in the photo (px ≈ 160–600, 330–900).
- **Left side** (lower middle): the left wall, with the **rear-left tyre** (px ≈ 690–860, 560–660) in its well and the **front-left guard** beyond. The near mid wall below the band shows plain green layer lines.
- **Top**: the green carbon cross with the red-on-white text sticker along Y and the red logo, about **12 silver nuts/screws** standing proud, and the tyre tops showing in the four cut-outs.
- **Far (upper right)**: the **aluminium wedge** tab extending past the plate front edge (px ≈ 1000–1500, 30–470), with the **red link** (px ≈ 1120–1170, 230–285), and the **front-right pod** with the hinged **FR4 flap** (px ≈ 1205–1470, 430–730).

### 3.3 AWS70: front-left close-up, black version
- **Left**: the wedge as a large tan-grey plate, sloping down to the left, its top edge tucked under the carbon plate.
- **Centre**: the carbon plate with the logo and text, the oval switch slot, silver screws along the plate front edge, and black screws at the corners.
- **Wheels**: three of the four tyre tops show through cut-outs: rear-left (px ≈ 300–410, 125–190), front-left (px ≈ 160–250, 240–290), front-right (px ≈ 485–580, 370–420), and rear-right (px ≈ 625–700, 245–300). The pods/guards around them look **black, with layer lines and chamfered tops**.
- **Bottom right**: another robot's black shell (ignore).

### 3.4 Top view (synthesised)
- A **72 × 78 rectangle** (the tub) with a **30 mm trapezoid notch** at the rear centre, a **74 × 24 mm wedge trapezoid** ahead of it, and a **carbon cross** on top. Four **tyre rectangles (9 × 24 mm)** show in the cross's corner cut-outs, centred at (±27.5, ±21). Overall plan length ≈ **102 mm**, width ≈ **74 mm**.

### 3.5 Left side view (synthesised)
- From the rear: the rear lobe (vertical rear face in AWS71; ramp in AWS72), then the left wall (full height 21 mm) with **no wheel visible from the side** (the guards cover the tyres; only the top and bottom few mm of the tyres stand above the plate and below the floor). Then the front pod, then the wedge flank (AWS71: the triangular flange; AWS72: the FR4 flap hanging to the floor). The silhouette is a **low rectangle with a 35° ramp at the front**.

### 3.6 Front view (synthesised)
- The wedge face fills almost the whole width (74 mm) from the floor up to z ≈ 20. Above it only the plate edge (z 20–21.5) and the four tyre tops (z up to 24) peek over. The red link (AWS72) pokes up at x ≈ −14.

### 3.7 Rear view (synthesised)
- Two lobes, each ≈ 22 mm wide and 21 mm tall (AWS71) or with a vertical face only 6–8 mm tall below a ramp (AWS72), with the notch (30 mm mouth) between them. The floor of the notch is the rear wall of the bay. The plate notch is visible above it.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | tub with 4 wheel wells | 72 × 78 × 21 | 1 × 1.08 × 0.29 | black / dark-green FDM (nylon or PETG) | — | 1 |
| WG-F | front pod/guard | 4.5 × 30 × 20 | 0.06 × 0.42 × 0.28 | as CH | integral | 2 |
| WG-R | rear lobe/guard | 22 × 42 × 21 | 0.31 × 0.58 × 0.29 | as CH | integral | 2 |
| SW | mid side wall | 3 × 18 × 21 | — | as CH | integral | 2 |
| RN | trapezoid notch | mouth 30, floor 20, depth 10 | 0.42 | — | — | 1 |
| BT | edge trim | 2.5 wide strip | — | black TPU/tape | stuck (guess) | 1 (AWS72) |
| TP | cross plate | 72 × 73 × 1.5 (band 19 deep, tongues 44 wide) | 1 × 1.01 | carbon fibre (black / green) | 12–14 screws | 1 |
| TPN | plate notch | mouth 16, floor 8, depth 6 | 0.22 | — | — | 1 |
| LG | sticker | 18 × 16 | 0.25 | white/black or red/green | adhesive | 1 |
| TX | sticker | 34 × 5 | 0.47 | white/black or red/white | adhesive | 1 |
| SS | oval slot | 4 × 9 | — | — | — | 1 (AWS70/71) |
| SWT | slide switch | 12 × 6 × 6 (guess) | — | black | under TP | 1 |
| LNK | red key | 7 × 5 × 5 | — | red plastic | push-in | 1 (AWS72) |
| WD | bent sheet wedge | 74 wide, 8 tab + 31 slope, t 1.0 (Ti/SS) or 1.5 (Al) | 1.03 | Ti/SS (black version) / Al (green) | under TP + flange screws | 1 |
| WD-FL | side flange | triangle 24 × 7 | — | as WD | 2–3 screws each | 2 (AWS71) |
| FX | hinged flap | 22 × 12 × 1.5 | 0.31 | green FR4 | 1 hinge screw | 1 seen |
| WH | tyre | Ø 24 × 8.5 | 0.33 × 0.12 | grey rubber/foam | on hub | 4 |
| HB | hub | Ø 16 × 8 | 0.22 | black | on motor shaft | 4 |
| S-TP | button head + nyloc | head Ø 4, M2–M2.5 | 0.06 | black / silver | into tub | 12–14 |
| S-WD | button head | head Ø 4 | 0.06 | black | flange to pod | 5 seen |
| S-FX | button head | head Ø 4 | 0.06 | silver | flap hinge | 1 |

---

## 5. Contact / gap matrix (estimated mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP underside ↔ CH wall tops | rests on, screwed | 0 |
| TP band ends ↔ SW outer faces | flush | 0 (±0.5) |
| TP front edge ↔ WD top tab | TP clamps the tab | 0 |
| WD top tab ↔ CH front wall top | clamped between | 0 |
| WD flange inner face ↔ WG-F outer face | screwed | 0 (AWS71) |
| WD leading edge ↔ floor | touching | 0 |
| WD slope underside ↔ WH-FL/FR tyre fronts | in front of | 3–5 |
| WD sides ↔ WG-F inner faces | bracketed | 0–1 (AWS72) |
| FX ↔ WG-FR outer face | hinged | 0–0.5 |
| FX front tip ↔ floor | rests on | 0 |
| WH tyre ↔ WG outer guard inner face | running gap | ≈ 1 |
| WH tyre ↔ well ends (fore/aft) | running gap | 1–2 |
| WH tyre top ↔ TP top plane | stands proud | +2.5 |
| WH tyre ↔ TP cut-out edges | side gap | 1–2 |
| WH tyre bottom ↔ floor | contact | 0 |
| CH floor ↔ floor | clearance | ≈ 2 |
| WH-FL tyre ↔ WH-RL tyre | fore-aft gap | ≈ 18 |
| LNK ↔ WD tab | passes through a slot | 0–0.5 |
| SWT ↔ TP underside | mounted under the slot | 0 |
| BT ↔ rear lobe tops | stuck on | 0 |
| S-TP nuts ↔ TP top | seated | 0 |

---

## 6. Mechanism

1. **Drive**: four wheels, **4WD skid steer**. Each wheel is probably driven by its own **N20-class gearmotor** (the spec places one motor per side at y = −24 with front wheels possibly driven separately; the photos show four independent wells with no belts, so four motors is the most likely build **(guess, medium)**).
2. **Wedge**: fixed. It gets under opponents and lets the robot push them. There is no lifter or spinner.
3. **FX flap (AWS72)**: passive, gravity-hinged.
4. **Invertibility**: the tyres stand ≈ 2.5 mm above the plate and ≈ 2 mm below the floor, so the robot drives either way up. Inverted, the wedge leading edge is at the top, so it no longer works as a wedge. The **green version's rear ramps** give some wedge function on the other end **(guess on intent)**.

---

## 7. Assembly order (suggested rebuild)

1. Print **CH** (floor, walls, pods, lobes, wells and notch in one piece), floor on the bed. Fit **heat-set inserts** (M2) at the plate screw positions.
2. Fit the four **gearmotors** into their printed **motor mounts MM** (cradles in the floor between the wells, with the shafts pointing outboard into the wells). Press the **hubs HB** onto the D-shafts and fit the **tyres**.
3. Place the **battery** in the centre-rear of the bay, the **ESC(s)** at the sides, the **receiver** at the front, and the **switch** under the switch-slot position. Route the wires.
4. Lay the **wedge WD** on the tub front wall with its tab on the wall top. AWS71: screw the **flanges** to the front pods (5 screws).
5. Lay the **carbon plate TP** on top, covering the wedge tab, and fit the **12–14 screws/nuts**.
6. Apply the **stickers** LG and TX.
7. AWS72: screw the **FR4 flap FX** to the front-right pod. Fit the **red link LNK**. Apply the **black trim BT** to the rear lobes.

---

## 8. Profiles as math (for rebuilding curves)

**8.1 Top plate TP outline (XY plane, z from 20 to 21.5).** A closed polygon, listed clockwise from the rear-left tongue corner:
(−22, −37) → (−8, −37) → (−4, −31) → (+4, −31) → (+8, −37) → (+22, −37) → (+22, −9.5) → (+36, −9.5) → (+36, +9.5) → (+22, +9.5) → (+22, +36) → (−22, +36) → (−22, +9.5) → (−36, +9.5) → (−36, −9.5) → (−22, −9.5) → back to start.
The notch sides are the lines x = ±(4 + (y + 31)·(4/−6)) for y ∈ [−37, −31], i.e. **|x| = 4 − 0.667·(y + 31)**. Fillet the outer convex corners with r = 1.

**8.2 Tub rear notch RN (XY plane, full height).** Trapezoid with vertices (−15, −40), (−10, −30), (+10, −30), (+15, −40). The sides are **|x| = 10 − 0.5·(y + 30)** for y ∈ [−40, −30].

**8.3 Green-version rear lobe side profile (YZ plane, x from ±14 to ±36).** Top z = 21 for y ∈ [−28, +2]. Ramp: **z = 21 − (−28 − y)·tan 42°** for y ∈ [−42, −28] (from z = 21 down to z ≈ 8.4). Then a vertical rear face at y = −42 from z = 8 down to z = 2. Black version: a plain rectangle, z ∈ [2, 21], y ∈ [−40, +2].

**8.4 Wedge WD side profile (YZ plane, the sheet mid-surface).**
- Tab: z = 20.5, y ∈ [+30, +36.5].
- Bend: arc, centre (y +36.5, z 18.5), r = 2, from θ = 90° to θ = 54° (measured from +Y), i.e. turning down by 36°.
- Slope: **z = 19.7 − (y − 37.7)·tan 36°** for y ∈ [37.7, 62.8], reaching z ≈ 1.4; then a sharp leading edge ground (or naturally thin) to z = 0 at **y ≈ 62.8**. Rounded leading-edge corners in plan: r = 3.
- Sheet thickness: 1.0 (Ti/SS) or 1.5 (Al), offset below the mid-surface by half.

**8.5 Wedge flange WD-FL (AWS71, YZ plane at x = ±37).** Because the flange lies flat against the pod outer face (that is where its screws go), it must extend **back** past the tub front at y = +38. Use a **trapezoid** with vertices **(+22, 20), (+22, 13), (+60, 1.5), (+38, 20)**, which overlaps the pod outer face for y ∈ [22, 38] and carries 2–3 screws there.

**8.6 Tyre tread (in the wheel's own frame, XZ disc).** Root radius r₀ = 11.5. Ribs: N = 72 rounded ribs, height h = 0.6, so **r(φ) = 11.5 + 0.3·(1 + cos(72·φ))**, φ ∈ [0, 2π). Width 8.5, with edge fillets r = 1.

**8.7 FX flap (YZ plane at x = +37.5, as hanging in AWS72).** Trapezoid with vertices (y +18, z 14), (+28, 16), (+42, 3), (+40, 0) **(guess)**. Hinge hole Ø 2.5 at (+21, 12).

---

## 9. Pixel-based measurements (independent check)

Coordinates are (x px, y px) from the top-left, read by eye, ±10 px.

**AWS71 (1114 × 1296):**
- Tub width at the band: px x ≈ 170 → 1030 = **860 px**. Plate band: 150 → 1000.
- Plate length, rear tongue edge to front tongue edge: px y ≈ 190 → 870 = **680 px** (foreshortened).
- Wheel centres: rear y ≈ 420, front y ≈ 790 → **370 px** fore-aft. Left x ≈ 295 (rear) and 210 (front), right x ≈ 905 and 860.
- Tyre visible width (X): rear-left 245–345 = 100 px, front-left 150–270 = 120 px (nearer).
- Wedge: x 70 → 960 = **890 px** wide; y 790 → 1250 = **460 px** tall.
- Tongue width (rear): x 375 → 895 = **520 px**. Notch in plate: mouth 540–725 = 185 px, floor 595–690 = 95 px.
- Logo: 200 × 195 px. Text: 410 × 50 px.
- Scale at the band (mid-depth): 860 px / 72 mm ≈ **11.9 px/mm** across X.

**AWS72 (1545 × 1041):**
- Left rear ramp: from the top edge at px (300, 330) to the bottom edge at (300, 900).
- Rear-left tyre: px x 690–860 (an ellipse 170 px wide). Front-left tyre top: px (360–520, 245–320).
- Aluminium wedge exposed beyond the plate: px x ≈ 1260–1500.
- FR4 flap: px (1205, 730) to (1470, 430).
- Nut heights: each nut ≈ 25 px tall against a plate thickness edge ≈ 10 px, so nut ≈ 2.5 × plate thickness ≈ 3.5–4 mm.

**AWS70 (855 × 681):**
- Plate front edge: from px (110, 270) to (560, 420).
- Wedge visible: px x 25 → 540, y 260 → 640.

---

## 10. Several independent estimates of key quantities

| Quantity | Method A (spec / limits) | Method B (ratio in photo) | Method C (pixels + scale) | Reconciled |
|---|---|---|---|---|
| Tub width W | spec ≈ 70 | must leave room for the wedge in a 101.6 cube: ≤ 80 | AWS71 860 px / 11.9 px/mm (scale from the 44 mm tongue: 520 px → 11.8 px/mm) = 73 | **72** |
| Tub length | spec 84 (y −45..+39) | AWS71 plate length / band width: 680/0.77 (foreshortening at 50°) / 860 = 1.03 W ≈ 74 tub ≈ +4 | AWS72: length along the left side ≈ 1.1 × the width seen at the rear | **78** |
| Wheel Ø | spec hub ≈ 25 | AWS71 tyre length in the cut-out ≈ 175 px / 0.77 / 11.9 = 19 (the cut-out hides the ends) | AWS72 rear-left tyre ellipse 170 px wide (seen along its axis at ≈ 55°) vs the 21 mm wall ≈ 160 px → ≈ 24 | **24** |
| Wheelbase | spec 48 | AWS71: 370 px / 0.77 / 11.9 = 40 | AWS72: rear-left to front-left tyre centres ≈ 1.8 × tyre Ø ≈ 43 | **42** |
| Wedge slope length | — | AWS71: 460 px seen almost face-on → 460/11.9 ≈ 39 (includes the tab and the flanges) | AWS70: the sheet looks about 0.45 × the plate length ≈ 33 | **31 slope + 8 tab** |
| Wedge angle | typical 25–40° | AWS70 the sheet edge rises at ≈ 35° in a near-side view | 20 mm rise over a ≈ 24–26 mm run → 37–40° | **36°** |
| Tub height | spec carbon at z ≈ 6 above a datum at mid-height → about 20 | AWS72 left wall ≈ 0.29 × width | AWS71 flange height ≈ tub height ≈ 21 | **21 (+1.5 plate)** |
| Overall length | must fit the cube | — | 78 + 24 = 102 | **≈ 102** (see §11) |

---

## 11. Consistency check: conflicts and reconciliation

1. **Overall length vs the 101.6 mm cube.** 78 (tub) + 24 (wedge run) = 102 mm, which is about 0.4 mm over a 4" cube if measured straight. Either my tub length is a few % high, or the robot fits the cube **diagonally** (allowed in practice by measuring in the box). The tub could also be 76 mm. **Reconciled: tub 78, wedge run 24, with ±3 mm uncertainty; keep the build ≤ 101.6 by trimming the tub to 77.**
2. **Wheelbase 48 (spec) vs 40–43 (photos).** The spec wheels at y = ±24 with Ø 25 would leave the plate band only ≈ 22 mm deep, but in AWS71 the band is almost as deep as the tyre gap. **Reconciled: wheelbase 42 (y = ±21), band 19 mm deep.**
3. **Rear-notch width (spec 39 vs photo 30).** AWS72 makes the notch look large (each ramp is about 1/3 of the width, so the notch is ≈ 1/3 ≈ 24–30 mm at the mouth). **Reconciled: 30 mm mouth, 20 mm floor.**
4. **Wheel height vs plate.** If the tyres are Ø 24 at z = 12, the tyre tops are at 24, i.e. 2.5 mm above the plate top at 21.5. AWS70 shows the tyres clearly proud of the plate, AWS71 shows them roughly level (seen from above, a small protrusion is invisible). **Consistent.**
5. **Two versions.** The black (AWS70/71) and green (AWS72) robots share the cross plate, the logo, the four guarded wheels and the metal wedge. They differ in **rear-lobe shape** (flat vs ramp), **wedge metal** (Ti/SS with flanges vs Al without), the **switch access** (slot vs red link), the **FR4 flap** and **trim**. The descriptions above flag each one. Build the **AWS71 black version as the base**, with the AWS72 features as variants.
6. **Wedge flanges overlapping the pods.** If the flanges sit outside the pods, the wedge is 2 × 1 mm wider than the tub (74 vs 72). AWS71 does show the wedge slightly wider than the tub. **Consistent.**
7. **Screw count.** AWS71 ≈ 14 vs AWS72 ≈ 12. Some AWS72 screws are hidden by the viewing angle (the far-right side). **Reconciled: 14.**

---

## 12. Why the designer did it (per part, mostly adversarial)

Common lens: for each part, what attacks can reach it (vertical spinners, horizontal spinners, opposing wedges, flippers, wall slams, inversion), whether it helps Rammstein **get under** the opponent or merely **make contact**, and then construction reasons.

- **CH, a low 21 mm tub that encloses the wheels**
  - Attacks: a horizontal spinner hitting the side meets a **solid printed wall**, not a tyre, so the tyre cannot be torn off or used to spin the robot. A vertical spinner has only 21 mm of frontal height to bite, and most of the front is covered by the wedge.
  - Getting under vs contact: the tub's own edges are vertical and blunt. They only make contact, so all "getting under" is left to the wedge.
  - Construction: one print, floor on the bed, no supports. The wheel wells are simple pockets. Nylon/PETG absorbs hits without shattering.
- **WG-F / WG-R wheel guards (integral)**
  - Attacks: they protect the tyres from side hits and stop an opposing wedge from riding up the tyre (a tyre is a ramp an enemy can climb). With the guards, the side profile is a wall.
  - Weakness: they add width (each 4–5 mm) and weight, and a guard that cracks may rub on the tyre.
  - Construction: integral with the tub, so there is no separate guard-to-chassis support to fail. That answers the "guard supports" question for this robot: **there are none, because the guards are part of the tub walls**.
- **RN rear notch and rear lobes**
  - Attacks: the notch removes material where the robot is least likely to be attacked head-on, saving weight. Behind the notch the rear wall of the bay protects the electronics.
  - Getting under: in the green version the **ramps** make the rear a second, blunter wedge. If Rammstein is turned around, an attacker hitting the rear meets a slope that deflects it upward instead of a vertical wall it can push. The lobes also act as **two rear prongs** that can push an opponent with two contact points.
  - Construction: the notch might also give access to a charge plug or link at the rear wall **(guess)**.
- **BT black trim (AWS72)**
  - Attacks: a soft strip on the edges that opponents hit most when they ride over the rear. It absorbs scraping and keeps the printed edges from chipping **(guess)**. It may also simply be gaffer tape repairing a crack.
- **TP carbon cross plate**
  - Attacks: the top is reachable by overhead hammers, by vertical spinners after a flip, and by opponents riding up the wedge. Carbon fibre is **stiff and light**, and it spreads a point hit across the walls.
  - Why a cross: the cut-outs let the tyres stand **proud of the top** for inverted driving without making the tub taller. The full-width band ties the two side walls together between the wheels, where a side hit would otherwise flex the tub.
  - The plate clamps the wedge tab, so the plate is also part of the wedge mount.
- **Stickers**: purely cosmetic (a robot named after the band), but the plate gives a flat surface for them.
- **SS / SWT switch through the plate**: the switch can be turned on and off without removing anything, and the slot is small, so a weapon cannot hit the switch. The slot is in the front tongue, behind the wedge, which shields it from the front.
- **LNK red link (AWS72)**: a removable link is the AWS-recommended failsafe. It is bright red so marshals can see it. It pokes through the wedge tab, so a hit there could knock it out **(a risk)**.
- **WD sheet-metal wedge**
  - Getting under: this is the robot's whole offensive. A **thin metal leading edge (≈ 1 mm)** on the floor gets under printed wedges, which cannot be made as thin. A **35–40° slope** is steep enough to make opponents climb high (often flipping lighter ones onto their backs) yet shallow enough that the robot does not have to push them uphill too hard.
  - Attacks: a vertical spinner hitting the wedge face is deflected upward and over the robot. Titanium or stainless (black version) resists denting and cutting by spinner teeth. Aluminium (green version) is lighter but dents; to compensate it is thicker.
  - Full width: there are no gaps at the corners for an opponent's wedge to get in under the tyres.
  - Flanges (AWS71): they stiffen the sheet against twisting and give the side screws something to hold. They also close off the front-wheel area from the side.
  - Construction: one cut-and-bent sheet. It is easy to replace, and the bend line is the only forming operation.
- **FX FR4 flap (AWS72)**
  - Getting under: a hinged flap rests on the floor under its own weight even when the robot rocks, so the **front corner never leaves a gap** for an opponent's wedge. When the robot turns into an opponent at an angle, the flap meets it first and gets under.
  - Attacks: FR4 is tough and flexible. If hit by a spinner it flexes or swings out of the way rather than transferring the hit. It is a cheap sacrificial part.
- **WH tyres (Ø 24, ribbed rubber/foam)**
  - Attacks: the tyres are shielded on the outside by the guards and from above by the plate, so only the top 2.5 mm and the bottom contact patch are exposed. A vertical spinner coming over the top can still reach the tyre tops.
  - Pushing: 4WD with soft ribbed tyres gives maximum traction, which matters most for a pusher/wedge. With all four wheels driven, the robot still pushes when an opponent's wedge lifts its front or rear.
  - Invertibility: the tyre tops are above the plate, so a flip does not end the match.
- **Fasteners S-TP with nyloc nuts**: nyloc nuts do not vibrate loose under impacts. Screws fitted from below with nuts on top make the top plate removable without disturbing the inserts in the tub **(guess)**. The nuts stand proud, which slightly raises the effective top height (by ≈ 3.5 mm), so inverted the robot may rest on its nuts rather than its tyres if a tyre is worn. That is a **design weakness**: the tyre tops (+2.5 mm) are **lower** than the nut tops (+3.5 mm) in the green version **(possible issue, medium confidence)**.

---

## 13. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors M-x | 4 × N20 micro gearmotors (6 V, about 300–500 rpm) | 12 × 10 × 25, + 9 mm D-shaft | lying along X, shafts out into the wells: (±14, ±21, 12) | medium (2 motors with front and rear wheels each driven separately is the spec's version: low–medium) |
| Motor mounts MM-x | printed **plastic cradles** in the tub floor: U-shaped saddles with a strap or a printed clamp over each motor, 2 × M2 screws each | 16 × 14 × 14 | over each motor | medium |
| Wheel hubs HB | printed hubs, D-bore press fit on the N20 shaft, tyre stretched or glued on | Ø 16 × 8 | in each well | medium |
| Battery BAT | 2S 7.4 V LiPo, 150–300 mAh | 35 × 18 × 10 | centre-rear of the bay, (0, −14, 8) | medium |
| ESC | one dual brushed ESC per side, or one 4-channel board | 25 × 15 × 5 | (±12, +6, 6) | low |
| Receiver RX | small 2.4 GHz receiver | 20 × 12 × 5 | front centre, (0, +20, 8) | low |
| Switch SWT | mini slide switch, lever up | 12 × 6 × 6 | under SS, (0, +27, 17) (AWS71) | medium–high |
| Inserts | M2 heat-set inserts in the wall tops and corner posts | Ø 3.2 × 4 | under each S-TP position | medium |
| Corner posts | printed posts Ø 6 from floor to plate, carrying inserts | Ø 6 × 19 | near (±22, ±34) and (±30, 0) | medium |
| Wedge tab bolts | 2–4 × M2 from the plate through the tab into the front wall | — | (±12, +34) | medium |
| Wiring WR | battery → switch → ESC(s) → four motors, about 30–60 mm leads each, kept below z ≈ 18 so the plate clears them | — | — | high (that it exists), low (exact routing) |

**Wiring path summary (guess)**: the battery sits at the rear, its leads run forward along the centreline to the switch under the front tongue, then back to the ESCs at the sides. Motor leads run sideways a short distance to the four motors next to their wells. The receiver at the front connects to the ESC signal leads. Nothing is outside the tub or the plate, so the whole system is shielded by the guards, plate and wedge.

---

## 14. Hidden / uncertain list

- Whether there are four motors or two.
- Floor shape and ground clearance.
- The rear-wall details (a charge port or a link in the notch?).
- Whether the left front corner of the green version also carries an FR4 flap.
- Exact wedge metal (Ti vs stainless) in the black version.
- Whether the black version's rear lobes are ramps too (the AWS71 view from the front cannot show the rear faces).
- All mm values are scaled estimates (±10–15%).

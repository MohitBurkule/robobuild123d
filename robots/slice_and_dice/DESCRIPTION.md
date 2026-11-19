# Slice and Dice: full rebuild description from reference photos

Source photos (both cut out onto white by the AWS wiki):
- `robots/slice_and_dice/reference/slice_and_dice.aws64.webp`: AWS 64, 795 × 408 px, low resolution and slightly soft. Shows **two robots side by side**: on the left a **dark navy/purple rectangular-ish robot with a small vertical spinner and a front scoop**, and on the right a **light-blue (sky/cyan) triangular robot with a horizontal bar spinner at its front apex**. Both are seen from the front, high (about 45–55° down), the navy one turned about 30° to its right and the blue one about 40° to its left.
- `robots/slice_and_dice/reference/slice_and_dice.aws72.webp`: AWS 72, 1994 × 961 px, sharp. Shows the **later versions of the same pair**, both printed in **black**: on the left the **triangular horizontal spinner** (blue wheel hubs, blue fuzzy-textured motor cap, curved steel bar under it) and on the right the **wide rectangular vertical spinner** (cyan brushless outrunner in a central slot, a curved hook-shaped steel bar, two front forks tipped with knife-blade inserts, yellow fuzzy wheels). Seen from the front-right, about 35–40° down.

**Slice and Dice is a two-robot cluster** (AWS clusters share the 150 g limit, so each robot is probably around 70–80 g **(guess)**). The name fits the pair: one horizontal spinner that "slices" and one vertical spinner that "dices". This description calls them:
- **TB** = the **triangular horizontal-spinner robot** (light blue at AWS64, black at AWS72).
- **RB** = the **rectangular vertical-spinner robot** (navy at AWS64, black at AWS72).

The existing `spec.json`/`kit.json` drafts model the robot as a single trapezoid "lifter" (70 × 84 × 22 mm). That is wrong for the weapon: **neither robot is a lifter**. The trapezoid footprint does roughly match TB. Everything stated as fact below is read directly from the photos. Anything inferred is marked **(guess)**. All mm values are **estimates** (±15%), scaled from the 101.6 mm (4 in) cube that each cluster member must fit in, from typical part sizes (Ø 22–30 mm antweight wheels, 1104–1806 class outrunners, M2/M3 screws), and from pixel ratios. The reference length for ratios is **W = RB lid length across the robot (wheel-to-wheel body length) ≈ 84 mm**.

---

## 0. Coordinate system and naming

- **One frame convention**, used for both robots: **+X** = the robot's own right, **+Y** = forward (toward the weapon), **+Z** = up, units mm. Each robot has its **own origin** on the floor (z = 0) under the centre of its body footprint (TB: centre of the triangle's bounding box; RB: centre of the box). For a combined scene, place **TB's origin at global (−75, 0, 0)** and **RB's origin at global (+75, 0, 0)**, both facing +Y, which matches the side-by-side arrangement of AWS72 (TB on the left of the picture, RB on the right). Every coordinate given in a part section is in that robot's own frame.
- **Front** of TB = the apex with the horizontal spinner. **Front** of RB = the long face carrying the forks/scoop and the exposed spinner. In both photos the fronts face roughly toward the camera.
- Angles in side profiles are measured from +Y in the YZ plane; angles in plan are measured from +Y toward +X.

| ID | Part | Robot |
|---|---|---|
| TB-CH | triangular chassis (tub at the rear, open truss toward the apex) | TB |
| TB-TP | triangular top plate (cut-corner triangle, with eye window) | TB |
| TB-BP | lower/bottom plate (apex tongue under the motor) | TB |
| TB-ST-L / TB-ST-R | diagonal side struts (apex to rear corners) | TB |
| TB-WN | front window/ramp recess in the top plate | TB |
| TB-SW | switch slot with a removable link/pin | TB |
| TB-MC | weapon motor cap (blue fuzzy cylinder, AWS72) / bare motor (AWS64) | TB |
| TB-WM | weapon motor (outrunner, hanging bell-down) | TB |
| TB-BL | horizontal spinner bar (S-curved steel bar, AWS72; steel + brass bar, AWS64) | TB |
| TB-WH-L / TB-WH-R | drive wheels at the rear corners | TB |
| TB-EY-L / TB-EY-R | googly-eye stickers | TB |
| RB-CH | rectangular chassis box with a central weapon slot | RB |
| RB-LD-L / RB-LD-R | lid halves either side of the slot | RB |
| RB-SL | central weapon slot (front to back) | RB |
| RB-MM | weapon motor mount (black printed block with two silver cap screws) | RB |
| RB-WM | weapon motor (cyan outrunner, AWS72) | RB |
| RB-BL | vertical spinner bar (curved hook bar, AWS72; small toothed disc, AWS64) | RB |
| RB-BB | bearing/axle block beside the AWS64 blade | RB |
| RB-FK-L / RB-FK-R | front forks with knife-blade tips (AWS72) | RB |
| RB-KB-L / RB-KB-R | knife-blade inserts in the fork tips (AWS72) | RB |
| RB-SC | front scoop/wedge with a square window (AWS64) | RB |
| RB-WH-L / RB-WH-R | drive wheels at the ends of the box | RB |
| RB-EY-L / RB-EY-R | googly-eye stickers | RB |
| S-xx | screws (listed per part) | both |
| W-xx | wires (red/green visible inside RB) | both |
| M-x, BAT, RX, ESC | drive motors, battery, receiver, ESCs (hidden, guess) | both |

---

## 1. Overall description in one paragraph

Slice and Dice is a **pair of small spinner robots with cartoon googly eyes**. **TB** is a **flat triangle** about 84 mm across the rear edge and 80 mm from the rear edge to the tip, about 20 mm tall. It drives on **two wheels at the two rear corners**, and its **front apex carries a horizontal bar spinner** hung under the top plate, with the bar sweeping a circle just above the floor in front of the robot. Behind the apex, the sides of the triangle are **open truss**, not walls: a top plate, a bottom tongue and diagonal struts. **RB** is a **wide, low box** about 84 mm across, 40 mm deep and 22 mm tall, with a **wheel on each end** (the wheels are on the short ends, so the robot is wider than it is long). A **slot runs front to back through the middle** of the box. In that slot sits a **vertical spinner**: at AWS72 a **cyan outrunner** turning a **curved, hook-shaped steel bar** that sticks up about 20 mm above the lid; at AWS64 a **small toothed disc** on an axle block. RB's front has **two forks with steel knife tips** (AWS72) or **one central scoop** with a square window (AWS64). Both robots have their top plates held by small black pan-head screws and carry **two large googly-eye stickers** on top.

---

## 2. Part-by-part description

### 2.1 TB chassis (TB-CH)
- **Plan shape**: an isosceles triangle with its **apex forward**. The rear edge is straight and long (about **84 mm**). The two side edges converge toward the front. The **rear corners are cut off** (chamfered about 8–10 mm) where the wheels sit, so the outline is really a pentagon/hexagon: rear edge, two short rear chamfers (the wheel faces), two long side edges, and a **rounded apex** where the motor sits.
- **Height**: about **20 mm** at the rear (TB-TP top at z ≈ 20), body floor about 1.5–2 mm above the ground **(guess)**.
- **Rear half**: a **solid tub**. In AWS72 the left side below the top plate is a full vertical wall from the left wheel forward for about 30 mm; it is about 2 mm thick, black PLA/PETG, with visible layer lines. The rear wall is not seen but is assumed full **(guess, high)**.
- **Front half**: **open**. From about y = +5 forward, the side "walls" are replaced by a **diagonal strut** on each side (TB-ST) running from the bottom of the apex back and up toward the rear tub, leaving triangular openings through which the floor and background are visible (white background seen through the side in both photos). This makes the front of the robot a **two-plate sandwich** (top plate plus bottom tongue) joined by struts.
- **Material/colour**: AWS64 light sky-blue FDM; AWS72 matte black FDM with a slight sheen.

### 2.2 TB top plate (TB-TP)
- **Shape**: a flat plate, **2–2.5 mm thick**, the same triangle outline as the chassis, slightly overhanging (0.5–1 mm). In AWS72 its outline is: rear edge straight (y = −36, x −42 … +42), rear corners chamfered toward the wheels, side edges converging toward the apex, apex rounded around the motor at radius about **12 mm** centred at (0, +34).
- **Screws (S-TP)**: small **black pan-head Phillips M2**, head Ø about 3.5–4 mm. AWS64: about 6 visible (both rear corners, one mid-left edge, one mid-right edge, two near the centre front of the eyes). AWS72: about 7 (rear-left corner (−38, −32), rear-right corner (+38, −32), left edge (−30, −12), right edge (+30, −10), two near the centre (−4, +2) and (+8, +2), and one at the right of the window).
- **Window/ramp (TB-WN)**: in front of the eyes, slightly right of centre, the plate has a **rectangular-trapezoid cut-out** about **28 × 9 mm**, angled about 15° to the X axis, through which a **sloped surface** is visible. In AWS72 there is a **step**: the right end of the window carries a small raised block (about 8 × 6 × 4 mm) with a slot. In AWS64 the window is **triangular** (a wedge-shaped hole with its point toward the apex) and the lower tongue and struts are visible through it. Its purpose is probably **access to the motor wires or ESC**, or simply a weight-saving pocket **(guess)**.
- **Switch slot (TB-SW)**: left of the eyes, a small **slot about 12 × 3 mm** with a dark pin inside it (AWS72 at about (−22, −4)). AWS64 shows a similar short slot at about (−14, −2). This is very probably the **power switch or a removable link** **(guess, high)**.
- **Eyes (TB-EY)**: two round **white googly-eye stickers** with black pupils, each about **Ø 13–15 mm**, set side by side at about (−8, +2) and (+10, +6) on the AWS72 plate (they follow the plate's slight rotation). At AWS64 the pupils look up and to the right, giving a "side-eye" face.

### 2.3 TB bottom plate / apex tongue (TB-BP)
- **Shape**: a flat plate about **2–3 mm** thick at floor level (z ≈ 1.5–4) running forward under the apex. At the apex it forms a round tongue under the motor (outer radius about 13 mm), so the weapon motor is **held between the top plate above and this tongue below**. In AWS64 a **lower front tip** is visible under the blade, sticking out about 3–4 mm past the top plate apex.
- **Connection**: integral with the diagonal struts and the rear tub (one print), or a separate plate screwed on **(guess: one print, medium)**.

### 2.4 TB diagonal side struts (TB-ST-L, TB-ST-R)
- **Shape**: flat bars about **5–6 mm wide × 3 mm thick**, running from the apex tongue at the bottom (y ≈ +28, z ≈ 3) **back and up** to the rear tub at the side (y ≈ −5, z ≈ 15). Angle about **20–25° from horizontal** in side view. In AWS72 the left strut is clearly seen under the blue motor cap running toward the left wheel; a second, nearly parallel member (the plate edge) lies above it.
- **AWS64**: the struts are the same blue colour; one carries a **wrap of black electrical tape** about 8 mm long near the apex, probably holding the weapon wires to the strut **(guess)**.
- **Why**: see §14.

### 2.5 TB weapon motor (TB-WM) and motor cap (TB-MC)
- **Position**: at the apex, axis **vertical**, centre at about **(0, +34)** in TB's frame.
- **AWS72**: the motor is hidden under a **blue cylindrical cap**, about **Ø 22 × 14 mm**, printed with a **fuzzy/rough skin texture**, flat top at z ≈ 20 (level with the top plate). The cap's **top face carries four black socket-head screws (M2) in a square** of about **8 × 8 mm**, rotated 45°, around a central hole (the motor shaft or its retaining screw). That square pattern matches a **brushless stator mounting pattern** (e.g. 1104/1306 class, M2 on Ø 9–12 mm), so the motor is mounted **upside down**: stator bolted to the top, **bell spinning downward**. The cap has a flat cut on its right/front side **(guess, from a straight edge seen)**.
- **AWS64**: no cap; the top plate itself extends over the apex as a rounded lobe with the **same four black screws in a square**. Under it the motor body is visible: black with a **red band** (red tape or the motor's red bell ring).
- **Motor class**: about **Ø 14–18 mm × 10–12 mm** outrunner (1306/1407 class) **(guess, medium)**.

### 2.6 TB horizontal spinner bar (TB-BL)
- **AWS72**: a **steel bar**, about **2 mm thick**, about **10 mm wide** and about **48–52 mm tip to tip**, with an **S-curved plan** (each half sweeps back like a sickle, so the leading edges are concave). One visible tip shows a **hole about Ø 3 mm** (a mounting hole or a weight-relief hole) and the trailing tip is cut square. A thin **green stripe** runs along the bottom edge (green tape, paint, or a heat-shrink edge protector **(guess)**). The bar sits at about **z = 3–5**, just above the floor and directly below the motor bell, centred on (0, +34). It overhangs the apex by about 12 mm in front and to each side.
- **AWS64**: a straight bar about **45 mm long**, one half **bare steel** with a pointed cutting edge toward the left, the other half a **brass/gold coloured block** (a counterweight or a hardened brass impactor), about 12 mm wide. It is mounted under the motor (red band) with a small washer stack.
- **Rotation**: unknown direction; the S-curve in AWS72 implies the concave edges lead, so it turns **clockwise from above** if the curve is read as trailing **(guess, low)**.

### 2.7 TB wheels (TB-WH-L, TB-WH-R)
- **Position**: on the two rear chamfered corners, axles along X at about **y = −22**, x = ±44 (outer face at ±48). They stick out beyond the side of the triangle.
- **AWS72**: **blue printed hubs** with **black rubber O-ring/tyres**, about **Ø 24 × 7 mm**. The hub face is flat, blue, with a dark ring; the left wheel shows a **silver axle end/grub screw** at the centre. The tyre is about 3 mm thick.
- **AWS64**: off-the-shelf **black rubber treaded wheels** (fine straight knurl), about **Ø 22 × 9 mm**, with a small hub boss.
- **Ground**: the wheels are the tallest thing at the rear (top at z ≈ 24, about 4 mm above the top plate), so TB can drive inverted **(guess, medium)**.

### 2.8 RB chassis (RB-CH)
- **Shape**: a box about **84 mm wide (X) × 40 mm deep (Y) × 20 mm tall** (to the lid underside). AWS72 edges are sharp; AWS64 has the **two front corners chamfered** at about 45° (about 12 mm legs), so the AWS64 plan is a hexagon: wide rear, narrower front.
- **End walls**: carry the wheel axles. In AWS72 the right end wall shows a **round hole about Ø 6 mm** near the bottom front (a motor shaft hole, cable hole or switch hole **(guess)**).
- **Front wall**: full height either side of the slot. AWS72: each half of the front wall carries a **small rectangular boss** (about 8 × 6 mm) with a recessed screw, above each fork, at about x = ±20, z = 12.
- **Material**: AWS64 dark navy/purple FDM (the lid looks violet in the light), AWS72 black FDM.

### 2.9 RB lid halves (RB-LD-L, RB-LD-R)
- **Shape**: two flat plates about **2 mm thick**, each about **36 × 40 mm**, either side of the central slot. In AWS72 the lids are slightly inset inside a 1 mm lip of the walls. The lid surface has the faint diagonal "ironing" pattern of a print bed side.
- **Screws (S-LD)**: black pan-head M2 at the corners: about 4 per half (AWS72 visible: right lid front-right, right lid rear-right, right lid front-left near the slot, left lid rear-left). AWS64: a single lid with about 6 silver/grey screws (rear-left, rear-centre, front-left, two either side of the blade, right).
- **Eyes (RB-EY)**: AWS72: one **googly-eye sticker Ø 14–16 mm on each half**, the left one partly hidden behind the blade at (−12, +4), the right one at (+18, −2), pupils as crescents (looking sideways). AWS64: two eyes either side of the blade slot, pupils looking right.
- **Switch (RB-SW)**: AWS64 shows a **small rectangular slot** near the rear centre (about 6 × 3 mm, at (+5, −10)) with a **purple tab** sticking up at the rear edge behind it: the power switch or a link **(guess, high)**. AWS72: hidden **(guess: in the end wall hole)**.

### 2.10 RB central slot (RB-SL)
- AWS72: a **slot about 24–26 mm wide** (X) through the full depth of the box and through the lid, centred on x ≈ −2. The weapon motor and its mount fill the right half of the slot; the blade spins in the left half.
- AWS64: a narrower **slot about 8–9 mm wide** in the lid, from the front edge back about **18 mm**, with the small blade disc protruding through it.
- Inside the AWS72 slot, behind the motor, **a red wire and a green part** (wire or PCB) are visible.

### 2.11 RB weapon motor mount (RB-MM)
- **Shape (AWS72)**: a black printed **upright plate/block** about **20 × 8 × 22 mm** standing on the right side of the slot, with the motor's stator bolted to its left face. On its outer (right) face, two **silver socket-head cap screws** (M3, head Ø 5.5 mm) are visible: one upper at about z = 17 and one lower at about z = 8, plus a smaller black screw near the bottom. The block's top is rounded (a half-round of radius about 10 mm around the motor axis) **(guess from the curved outline)**.
- **Fastening**: the two cap screws probably go **through the mount into the right lid half or the slot's side wall**, or they are the stator screws **(guess)**.

### 2.12 RB weapon motor (RB-WM)
- **AWS72**: a **cyan/turquoise anodised outrunner**, about **Ø 18 × 12 mm** (bell), with text printed on the bell, axis **along X** at about **(0, 0, 14)**. Copper windings are visible through the bell's end slots. The bell faces **left (−X)**, toward the blade.

### 2.13 RB vertical spinner bar (RB-BL)
- **AWS72**: a **steel bar** about **2–3 mm thick**, about **10–12 mm wide**, about **60 mm tip to tip**, with a **crescent/hook plan** (it curves like a banana, the concave side facing forward-down at the moment of the photo). It is fixed to the bell's left face by **three silver screws** (one at the centre over the shaft, one on each arm about 12 mm out), with a black printed **spacer/hub** between the bar and the bell. The top tip sticks about **20 mm above the lid**; the bottom tip reaches down to about z = 3. The bar's leading/lower edge has a **green stripe** (like TB's bar). The tips are cut square with slight rounding.
- **Plane**: the bar spins in the **YZ plane** at x ≈ −8, so it hits upward at the front.
- **AWS64**: a small **saw-toothed disc** (silver, about **Ø 26 × 3 mm**, 6–8 coarse teeth), spinning in the YZ plane in the narrow lid slot, with its axle carried by a **black bearing block RB-BB** on the right side (about 10 × 10 × 18 mm) showing **three silver screw heads in a vertical row**. The blade's lower half drops into the scoop's square window.

### 2.14 RB front forks (RB-FK-L, RB-FK-R) and knife tips (RB-KB) (AWS72)
- **Shape**: each fork is a black printed **tapered arm**, triangular in side view: about **12 mm wide**, **20 mm tall at the front wall**, running **forward and down** about **30 mm** to a tip at floor level. The top face is a ramp at about **35°**. The sides are flat and parallel. The fork has a horizontal slot at its tip.
- **Position**: x ≈ **−28** and **+20** (inboard of the wheels, outboard of the slot), from y = +20 to y ≈ +50.
- **Knife tips (RB-KB)**: each fork tip holds a **steel utility-knife blade segment** about **12 mm wide × 15 mm long × 0.6 mm**, protruding about **10 mm** ahead of the printed tip, with its sharp bevelled edge facing forward and lying almost flat on the floor (a "wedgelet"). Each is held in the fork's slot, probably with glue or a screw across it **(guess)**.
- **Mount**: each fork attaches to the front wall below the small boss described in §2.8, probably by one screw into the wall **(guess)**.

### 2.15 RB front scoop (RB-SC) (AWS64)
- **Shape**: a black printed **ramp/scoop** about **32 mm wide × 38 mm long**, from the lid level at the front wall sloping down to the floor at about **25–30°**, with a vertical lip (about 5 mm) at the front edge. A **square window about 9 × 9 mm** is cut through the ramp about 10 mm from its front edge, under the blade. Its side walls are vertical.
- **Position**: centred on the blade, x ≈ −6, y from +20 to +58.
- **Why the window**: the blade's lower edge passes through it, so the scoop does not have to be cut away and the blade can hit things on the scoop **(guess, medium)**.

### 2.16 RB wheels (RB-WH-L, RB-WH-R)
- **AWS72**: **yellow** wheels about **Ø 28–30 × 10 mm**, with a soft, **fuzzy/foam-like** surface (TPU printed with fuzzy skin, or real foam). The face shows **six round holes on a ring** (Ø 4 mm on a pitch circle of about Ø 16) around a hub. Axle along X at about (±47, 0, 14). The wheel tops stick out above the lid by about 4 mm and the bottom below the floor plane, so RB can drive inverted.
- **AWS64**: black **treaded rubber** wheels about **Ø 22 × 9 mm** (same type as TB's at AWS64), set **toward the rear** of the end walls at about y = −5.

### 2.17 Wires (W) and electronics
- RB AWS72: a **red wire** and a **green item** visible behind the motor mount in the slot: the weapon ESC leads or the battery lead **(guess)**. Nothing else is visible; all electronics are inside the boxes.
- TB: the black tape on the AWS64 strut suggests the weapon motor wires run back along a strut into the tub **(guess, medium)**.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 AWS64 view (front, high, both robots)
- **Left of picture (RB, navy)**: the lid is seen almost face-on, a wide hexagon with its long side at the back. The wheels show at the upper-left and right edges. The **scoop** hangs forward and down toward the camera like a tongue, with its **white square window** clearly visible. The small silver toothed blade stands up through the lid slot, tilted. The black bearing block with three silver screws is just right of the blade.
- **Right of picture (TB, light blue)**: the triangle points toward the lower right. The top plate with two eyes fills most of the outline. The underside shows open truss (white background between members). At the apex, the four black screws, the black/red motor, and the **steel-and-brass bar** sticking out to the lower right.

### 3.2 AWS72 view (front-right, about 35–40° down, both robots)
- **Left of picture (TB, black)**: the top plate as a large dark triangle with the apex toward the lower right. Blue wheels at both ends of the rear edge (left one large and near, right one smaller and farther). The **blue fuzzy cap with four black screws** at the apex, the **curved steel bar** below it, and the **diagonal strut** running back to the left.
- **Right of picture (RB, black)**: the box runs from upper left (yellow wheel) to lower right (yellow wheel). The **cyan motor and hook bar** in the central slot, the bar standing up above the lid. **Two forks with silver knife tips** pointing toward the lower left.

### 3.3 Top views (synthesised)
- TB: a triangle, rear edge 84 mm, depth 80 mm to the cap's front, wheels sticking out at the rear corners, cap circle at the apex, bar extending to about Ø 50 beyond.
- RB: a rectangle 84 × 40 with wheels at both ends (overall width about 104 mm), a central slot, forks (or scoop) sticking out 30–38 mm in front.

### 3.4 Side views (inferred)
- TB from the left: a wedge-like profile, 20 mm tall at the rear, thinning toward the apex only in the open truss, with the motor cap at full height at the front and the bar at floor level. The wheel circle at the rear.
- RB from the left: a 40 × 20 rectangle hidden mostly behind the Ø 30 yellow wheel, forks sloping down in front, and the blade arc above.

### 3.5 Rear views
Not photographed. Both robots are assumed to have plain rear walls **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W (84) | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| TB-CH | triangle tub + truss | 84 × 80 × 20 | 1 × 0.95 × 0.24 | black (72) / sky blue (64) FDM | — | 1 |
| TB-TP | flat cut triangle | 84 × 80 × 2 | — | same | ~7 × M2 black pan | 1 |
| TB-BP | apex tongue | Ø 26 round end, 2.5 thick | 0.31 | same | integral (guess) | 1 |
| TB-ST | flat bar | 40 × 6 × 3 | 0.48 | same | integral (guess) | 2 |
| TB-WN | window | 28 × 9 | 0.33 | — | — | 1 |
| TB-SW | slot | 12 × 3 | — | — | — | 1 |
| TB-MC | fuzzy cylinder | Ø 22 × 14 | 0.26 | blue TPU/PLA | 4 × M2 into stator | 1 (72) |
| TB-WM | outrunner | Ø 16 × 12 | 0.19 | black/red | 4 × M2 | 1 |
| TB-BL | S-bar | 50 × 10 × 2 | 0.60 | steel (+brass at 64), green edge | on bell, 1–2 screws | 1 |
| TB-WH | wheel | Ø 24 × 7 | 0.29 | blue hub + black O-ring (72) | drive shaft + grub | 2 |
| TB-EY | sticker | Ø 14 | 0.17 | white/black | adhesive | 2 |
| RB-CH | box | 84 × 40 × 20 | 1 × 0.48 × 0.24 | black (72) / navy (64) | — | 1 |
| RB-LD | plate | 36 × 40 × 2 | — | same | 4 × M2 black pan each | 2 |
| RB-SL | slot | 25 wide (72) / 9 wide (64) | 0.30 | — | — | 1 |
| RB-MM | upright block | 20 × 8 × 22 | — | black | 2 × M3 silver cap + 1 black | 1 |
| RB-WM | outrunner | Ø 18 × 12 | 0.21 | cyan | 4 × M2 into MM | 1 |
| RB-BL | hook bar | 60 × 11 × 2.5 | 0.71 | steel, green edge | 3 silver screws | 1 |
| RB-BB | bearing block | 10 × 10 × 18 | — | black | 3 silver screws | 1 (64) |
| RB-FK | tapered arm | 12 × 30 × 20 | 0.14 × 0.36 | black | 1 screw (guess) | 2 (72) |
| RB-KB | knife blade | 12 × 15 × 0.6 | — | steel | slot + glue (guess) | 2 (72) |
| RB-SC | ramp | 32 × 38 × 20 | 0.38 × 0.45 | black | screws (guess) | 1 (64) |
| RB-WH | wheel | Ø 29 × 10 | 0.35 | yellow fuzzy (72) / black tread (64) | drive shaft | 2 |
| RB-EY | sticker | Ø 15 | 0.18 | white/black | adhesive | 2 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| TB-TP ↔ TB-CH wall tops | screwed | 0 |
| TB-MC top ↔ TB-TP top plane | flush | 0 |
| TB-WM stator ↔ TB-TP / TB-MC | bolted (4 × M2) | 0 |
| TB-WM bell ↔ TB-BP tongue | above | 1–2 |
| TB-BL ↔ TB-WM bell | bolted | 0 |
| TB-BL bottom ↔ floor | above | 2–4 |
| TB-BL tip circle ↔ TB-WH tyre | well clear | ~25 |
| TB-BL tip circle ↔ TB-ST struts | clear (below/in front) | 3–5 |
| TB-ST ↔ TB-BP / TB-CH | integral | 0 |
| TB-WH inner face ↔ TB-CH chamfer | near | 1–2 |
| TB-WH top ↔ TB-TP top plane | wheel above | +3–4 |
| TB-CH floor ↔ ground | clearance | 1.5–2 |
| RB-LD ↔ RB-CH wall tops | screwed | 0 |
| RB-LD inner edge ↔ RB-SL | edge of slot | 0 |
| RB-MM ↔ RB-CH slot wall | bolted (2 × M3) | 0 |
| RB-WM ↔ RB-MM | bolted | 0 |
| RB-BL ↔ RB-WM bell | bolted (3 screws) | 0 |
| RB-BL face ↔ slot left wall | side by side | 3–5 |
| RB-BL tip circle ↔ floor | above | 2–4 |
| RB-BL tip circle ↔ RB-FK | between, clear | 6–10 sideways |
| RB-FK ↔ RB-CH front wall | screwed | 0 |
| RB-KB ↔ RB-FK | inserted | 0 |
| RB-KB edge ↔ floor | touching | 0–0.5 |
| RB-SC ↔ RB-CH front | screwed (guess) | 0 |
| RB-SC window ↔ RB-BL (64) | blade passes through | 1–2 |
| RB-WH inner face ↔ RB-CH end wall | near | 1–2 |
| RB-WH top ↔ RB-LD top | wheel above | +4–5 |
| TB ↔ RB | separate robots | — |

---

## 6. Mechanism

1. **Drive (both)**: two-wheel differential drive with the wheels outboard of the body. TB's wheels are at the rear, so its apex rests on the bottom tongue (a skid). RB's wheels are on the X-axis centreline, so the box rocks onto the forks/scoop at the front and onto the rear edge at the back **(guess)**.
2. **TB weapon**: an inverted brushless outrunner directly drives a horizontal bar just above the floor. **Direct drive, no belt.**
3. **RB weapon**: a brushless outrunner with its axis along X directly drives a vertical bar (AWS72), or a disc on a separate axle (AWS64; possibly belt- or direct-driven from a motor inside, **unknown**). The bar spins in the YZ plane between the forks so that the forks feed the opponent into the bar.
4. **Cluster tactic**: one robot attacks low and sideways (TB), the other upward (RB). If one is knocked out the other continues.

---

## 7. Assembly order (suggested rebuild)

**TB**
1. Print TB-CH as one piece (rear tub, struts, apex tongue).
2. Fit two drive gearmotors in the rear tub, shafts out through the chamfered corners; press the wheels on.
3. Fit the battery, receiver and two ESC channels plus the weapon ESC in the tub; route the weapon wires forward along a strut (tape).
4. Bolt the weapon motor upside down to the top plate (or the blue cap) with 4 × M2; bolt the bar to the bell.
5. Screw TB-TP onto the chassis with about 7 × M2. Fit the switch link in TB-SW. Stick on the eyes.

**RB**
1. Print RB-CH (box with central slot, front bosses).
2. Fit the drive gearmotors in each end, shafts out of the end walls; fit the wheels.
3. Bolt the motor to RB-MM; bolt RB-MM into the slot with 2 × M3; bolt the bar and hub to the bell with 3 screws.
4. Fit the electronics either side of the slot; route the weapon leads through the slot wall.
5. Screw on the forks (AWS72) or the scoop (AWS64); insert the knife blades.
6. Screw on both lid halves (4 × M2 each). Stick on the eyes.

---

## 8. Hidden / uncertain list
- Whether TB's apex tongue is a separate plate.
- TB's rear wall, underside and wheel axle arrangement.
- RB's AWS64 blade drive (direct motor vs belt).
- RB fork mounting (screw vs integral) and blade retention.
- Exact motor sizes.
- Robot masses (cluster split).
- All mm values ±15%.

---

## 9. Coordinate frame (restated)
- Per robot: origin on the floor under the body footprint centre; +X right, +Y forward (weapon), +Z up, mm.
- TB extents: x ∈ [−48, +48] incl. wheels (body [−42, +42]), y ∈ [−36, +46] (body to cap front; bar reaches +59), z ∈ [0, 24] (wheels), body top z = 20.
- RB extents (AWS72): x ∈ [−52, +52] incl. wheels (body [−42, +42]), y ∈ [−20, +50] incl. forks/knives (body [−20, +20]), z ∈ [0, 42] including the bar's top tip at the moment of the photo (body top z = 22, bar circle radius 30 about (−8, 0, 14), so top of circle z = 44, bottom z = −16 clipped by the floor: **the bar cannot be 60 mm long if its axis is at z 14**; see §13).
- Global scene: TB at X −75, RB at X +75.

## 10. Profiles as math (for rebuilding curves)

**10.1 TB top plate outline (XY plane, TB frame).** Polygon, then a fillet:
- P1 (−42, −36) → P2 (+42, −36): rear edge.
- P2 → P3 (+46, −28): rear-right chamfer (wheel face is outside this).
- P3 → P4 (+11, +38): right side edge. Line: x = 46 − 0.53 (y + 28).
- Arc about C = (0, +34), r = 12, from P4 around the front to P5 (−11, +38).
- P5 → P6 (−46, −28): left side edge, mirror of P3–P4.
- P6 → P1: rear-left chamfer.
- Apex half-angle: atan(35/66) ≈ **28°**, so the included angle at the apex is about **56°** (a fairly sharp triangle).

**10.2 TB bar plan (AWS72).** Centre at the motor axis, half-length L = 25, width 10. Centreline of each arm: a circular arc of radius R ≈ 30 starting tangent to the radial direction at the hub, i.e. the centreline is the arc through (0, 0), (12, 2.5), (24, 10) (a gentle sickle). The other arm is the 180° rotation of the first (point symmetry, an S shape).

**10.3 RB bar plan (AWS72, in the YZ plane).** A crescent: outer edge an arc of radius ≈ 34 mm, inner edge an arc of radius ≈ 26 mm, centres offset by 3 mm, tips cut square, total chord ≈ 50 mm. Mounted with the hub at the arc's middle, so the tips sweep a circle of radius ≈ 25–27 mm.

**10.4 RB fork side profile.** Triangle in the YZ plane: (y +20, z 20) → (y +50, z 0) → (y +20, z 0). Ramp slope = 20/30 → **34°**. Knife: rectangle from y +44 to +56 at z 0–0.6, i.e. extending 6–10 mm past the printed tip.

**10.5 RB AWS64 scoop side profile.** (y +20, z 20) → (y +52, z 5) → (y +58, z 5) → (y +58, z 0) → (y +20, z 0), i.e. ramp slope 15/32 → **25°** plus a 5 mm vertical lip. Window: square 9 × 9 at y +40 … +49.

**10.6 Wheel circles.** TB, in the YZ plane at x = ±44: (y + 22)² + (z − 12)² = 12². RB: y² + (z − 14.5)² = 14.5².

## 11. Pixel-based measurements (independent check)

Measured on the AWS72 image scaled to 1400 px wide (scale factor 0.702 of the original).
- RB, near-edge lid length (front-left lid corner to front-right lid corner, excluding wheels): about **600 px** along an oblique. Right yellow wheel face height: about **125 px**. Ratio wheel Ø / lid length = 0.21 in projection; the end wheels are seen at an angle, which shortens the length less than it shortens the face. Corrected ratio ≈ 0.33–0.36 → **Ø 28–30 mm** if W = 84.
- RB, cyan bell: about **50 px** across in the scaled view, against **125 px** for the near wheel face → 0.40 × 29 ≈ **Ø 12–18 mm** (perspective: the bell is farther than the wheel) → **Ø 16–18 mm**.
- RB bar: from the top tip (x ≈ 1050, y ≈ 70) to the lower tip (x ≈ 880, y ≈ 300) ≈ **285 px**, against a near wheel of 125 px → 2.3 × 29 ≈ **66 mm** chord. With the bar tilted toward the camera, this overstates it slightly → **55–60 mm**.
- RB forks: from the front wall to the knife tip, about **150 px** on the near (right) fork, foreshortened (pointing toward the camera-left) → **30–45 mm**; reconciled **30 mm arm + 10 mm knife**.
- TB rear edge: from the left wheel (x ≈ 70) to the right wheel (x ≈ 600) along the far edge ≈ **530 px**. Near left wheel face ≈ **130 px** tall → 530/130 × 24 ≈ **98 mm** wheel-to-wheel → body rear edge ≈ **84–88 mm**. Consistent.
- TB cap: about **150 px** across at the near apex (nearer to the camera than the wheels) against the near wheel 130 px → **Ø 24 mm**, corrected for nearness → **Ø 22 mm**.
- TB bar: visible arm from the cap edge to the tip ≈ **110 px** → about **18–20 mm** past a cap radius of 11 → half-length about **25 mm**. Consistent with 50 mm.

AWS64 (795 px wide):
- RB lid rear edge ≈ **300 px**; wheel ≈ **75 px** → ratio 0.25 → with Ø 22 wheels, lid ≈ **88 mm**. Consistent with W = 84.
- RB scoop width ≈ **110 px** → 110/300 × 88 ≈ **32 mm**. Window ≈ **30 px** → **9 mm**.
- TB triangle rear edge ≈ **290 px**, wheel ≈ **70 px** → 4.1 × 22 = **91 mm** including the chamfers. Consistent.

## 12. Several independent estimates of key sizes

| Quantity | Method A (rule/size class) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| RB body width (X) | ≤ 101.6 incl. wheels → body ≤ 82 | — | AWS64: 88; AWS72: 84 | **84** |
| RB body depth (Y) | — | 0.45–0.50 W | AWS72 end-wall to wheel ≈ 1.4 wheel Ø = 41 | **40** |
| RB height | > wheel radius + clearance | 0.24 W | 0.7 × wheel Ø ≈ 20 | **20 + 2 lid = 22** |
| RB wheel Ø | 28–30 (typical foam) | 0.35 W = 29 | 28–30 | **29** |
| RB bar length | must clear the floor and the forks | ~0.7 W = 59 | 55–66 | **58** (see §13.1) |
| RB motor bell Ø | 1806 bell ≈ 23; 1306 bell ≈ 17 | 0.2 W = 17 | 16–18 | **18** |
| TB rear edge | ≤ 101.6 with wheels | 1.0 W | 84–91 | **84** |
| TB depth | ≤ 101.6 | 0.95 W | AWS64: 260 px / 290 × 88 = 79 | **80** |
| TB wheel Ø | 22–24 typical | 0.28 W | 24 | **24** |
| TB bar length | fits inside 101.6 with body | — | 50 | **50** |
| TB cap Ø | stator 1306 + walls | 0.26 W | 22–24 | **22** |

## 13. Consistency check: conflicts and reconciliation
1. **RB bar vs floor**: a 60 mm bar spinning about an axis at z = 14 would hit the floor (bottom of circle at z = −16). Either the axis is higher or the bar is shorter. The motor bell centre appears at about lid height minus 6 mm, i.e. z ≈ 16; the bar's lower tip is seen at about z ≈ 3, which means its **effective radius below the axis is ≈ 13 mm**. That fits a **crescent bar whose hub is offset from its middle** (one long arm up, short arm down) — but a spinner must be balanced. **Reconciled**: the bar is about **40 mm tip to tip, radius 20 mm about an axis at z ≈ 22–24** (the axle sits high, above lid level, carried by the upright mount RB-MM), the crescent shape making it look longer. The upper tip at the photo instant is at z ≈ 42, which matches the pixel impression of "about 20 mm above the lid". Update: **bar length 40–45 mm, axis at (−8, 0, 22)**, clearing the floor by 2 mm. This overrides §9's provisional numbers.
2. **TB depth**: the kit draft uses 84 mm long trapezoid; the photos show a triangle of 80 mm plus the bar. With the bar at full radius in front (y up to +59) and the wheels at the rear corners, the bounding box is ≈ 96 × 95 mm, just inside the 101.6 cube. Consistent.
3. **RB width with wheels**: 84 + 2 × (10 + 2) = 108 mm would **exceed 101.6 mm**. So either the body is about 78 mm or the wheels are partly recessed. The AWS72 end walls look flush with the wheel inner faces, so **reconciled: body 78 mm, wheels 10 mm thick with 1 mm gap → 102 mm**; or measure diagonally (the cube rule allows any orientation). **Use body 80, overall 100.**
4. **RB weapon type**: AWS64 vertical toothed disc vs AWS72 bar. These are two versions; both described.
5. **Spec says "lifter"**: rejected; both are spinners.
6. **Fork x positions**: the forks look asymmetric in the photo (left at −28, right at +20). With the slot centred at x ≈ −2 and 25 wide, symmetric forks about the **slot** centre at ±24 from it give −26 and +22. **Reconciled: x = −26 and +22.**

---

## 14. Why the designer did it (per part, from several angles)

Common lens: **adversarial**. For each part: what can attack it (enemy spinners, wedges, lifters, flippers, wall slams, inversion), how it survives, and how it helps win. Then construction reasons: print, weight, repair, cost.

- **Cluster of two**
  - Fight: in AWS a cluster wins only when both are out, and it can attack from two sides. One wedge can only handle one robot at a time; while it deals with RB, TB can hit it from behind or the side.
  - Weak points: each robot is half weight, so each is easily pushed or thrown; weapons are small.
  - Construction: two small identical-electronics robots share spares.
- **TB triangle shape**
  - Fight: the narrow apex puts the weapon at the front and the long side edges deflect pushers sideways. A triangle has no flat front face for an enemy wedge to push square.
  - Weak points: the open truss sides leave the inside reachable by thin forks and spinner teeth; the rear edge is wide and flat, a target for wedges from behind.
  - Construction: a triangle is the minimum shape that holds two wheels and one weapon; it uses little plastic.
- **TB open truss front**
  - Fight: the front half has to be narrow and light so the weapon motor can be far forward (longer reach). Struts are stiff in bending but weigh little.
  - Weak points: a strut can snap from a heavy hit, leaving the apex hanging.
  - Construction: printable without supports if printed upside down on the top plate **(guess)**; lets air reach the weapon motor.
- **TB inverted weapon motor at the apex, bar low**
  - Fight: a low bar hits the opponent's wheels and wedge edges below their armour. The apex position means the bar reaches ahead of everything else, so it hits first. The cap protects the stator and bolts from hits on top.
  - Weak points: the bar is exposed and the motor bearings take the full shock. A wedge can lift the apex and stop the bar on the floor.
  - Construction: direct drive (no belts or bearings), 4 bolts, easy to change.
- **TB blue fuzzy cap**
  - Fight: a soft cap absorbs light hits; the colour makes the weapon obvious to drivers and judges.
  - Construction: fuzzy-skin printing hides layer lines and adds grip for picking the robot up.
- **TB wheels outboard at the rear corners**
  - Fight: wide track for turning quickly; the wheels taller than the body let it run inverted (the inverted bar would then be on top, unusable, but the robot can still drive and push).
  - Weak points: exposed to horizontal spinners and side hits.
  - Construction: standard N20 wheels.
- **TB window and switch slot**
  - Fight: the window is a small weakness; the switch is recessed to avoid being knocked off.
  - Construction: the window gives access to the weapon wires without removing the plate. A link in a slot is a simple rule-compliant "removable link" power switch.
- **RB wide box with end wheels**
  - Fight: the wheels are at the ends, so the box is short front to back and **the weapon is close to the centre of mass**, which reduces gyroscopic tipping effects and keeps the robot stable after hits. The wheels shield the ends.
  - Weak points: a short depth means the robot is easy to flip end-over-end by a lifter; the flat lid is a target for overheads.
  - Construction: two lid halves let the slot run through; each half is a small print.
- **RB central slot and vertical bar**
  - Fight: a vertical spinner throws opponents upward and damages wedges; in the middle of the robot it is protected on both sides by the body halves and wheels. The crescent shape gives a hooked leading edge that bites better.
  - Weak points: the bar is exposed at the top (overhead hits) and the motor bearings take shock; the mount's two screws carry all the load.
  - Construction: direct drive from an off-the-shelf outrunner; the bar is a simple laser- or waterjet-cut plate.
- **RB forks with knife tips**
  - Fight: the thin steel tips get under opponents' edges, raising them into the bar (the forks "feed" the weapon). Two forks either side of the slot let the bar reach between them. Forks beat blunt wedges.
  - Weak points: knife blades are brittle and chip; the printed fork bodies can snap off.
  - Construction: utility-knife blades are cheap and pre-sharpened; easy to replace.
- **RB AWS64 scoop with window**
  - Fight: a single central ramp feeds opponents into the small disc; the window keeps the disc low.
  - Weak points: the disc was small, so energy was low; replaced by the larger bar later.
- **Googly eyes**
  - Fight: none.
  - Construction/branding: a recognisable character face on both robots (judges' and crowd appeal); the eyes are light stickers.
- **Black screws on the plates**
  - Construction: small M2 into plastic, light and quick to remove for battery changes.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| TB drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | (±28, −22, 10), shafts out at ±40 | medium |
| TB battery | 2S 150–180 mAh LiPo | 30 × 15 × 8 | (0, −20, 7) | medium |
| TB receiver + dual ESC | combined micro board (e.g. a "DasMikro"/Malenki-class combined RX/ESC) | 25 × 15 × 5 | (0, −5, 6) | medium |
| TB weapon ESC | 6–12 A brushless ESC | 20 × 10 × 4 | (+15, −8, 8) | medium |
| TB weapon wires | three thin leads along the left strut | — | strut | medium |
| TB stator bolts | 4 × M2 × 6 into the stator | — | square 8 × 8 at the apex | high |
| RB drive motors | 2 × N20 along X, one in each end | 12 × 10 × 25 | (±30, 0, 12) | medium |
| RB battery | 2S 150–200 mAh LiPo | 30 × 15 × 8 | left half (−25, 0, 8) | low |
| RB receiver + ESCs | combined board | 25 × 15 × 5 | right half (+25, 0, 8) | low |
| RB weapon ESC | brushless 6–12 A | 20 × 10 × 4 | right half under MM | low |
| RB motor shaft support | none (direct mounted on bell) | — | — | medium |
| RB AWS64 disc drive | small outrunner inside the bearing block side, shaft along X | Ø 14 | (+8, +10, 12) | low |
| RB switch | link plug through the end-wall hole | Ø 6 | (+42, +12, 6) | low |
| Floor plates | 1.5–2 mm integral floors | — | z 0–2 | medium |
| Fork screws | 1 × M2/M3 per fork through the front boss | — | (±24, +20, 12) | medium |

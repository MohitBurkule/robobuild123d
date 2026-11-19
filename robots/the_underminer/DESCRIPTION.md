# The Underminer: full rebuild description from reference photos

Source photos:
- `robots/the_underminer/reference/the_underminer.aws67.webp` (1352 × 1228 px, the best photo, cut out onto white). AWS 67. Seen from **above and in front**, at about **60–65° down**, front toward the bottom of the image. It shows the whole top deck, all four wheels, the KST servo, the central lifter arm and the **orange three-piece front** (a centre scoop flanked by two side wedges, all faced with fibre tape).
- `robots/the_underminer/reference/the_underminer.aws64.webp` (603 × 531 px, pit table photo on a wooden bench). AWS 64. Seen from the **rear-left, about 45° down**, front toward the lower right. It shows the **left side wall**, the white servo horn/bracket, the arm with its slot, raised **"UnderMiner" lettering** on the right lid, and a **brass/gold hexagonal front plate**. Wheels: grey tyres at the rear, blue at the front.
- `robots/the_underminer/reference/the_underminer.aws66.webp` (473 × 459 px, pit photo on a yellow table). AWS 66. Seen from the **front-left, about 50° down**. It shows a **silver-taped full-width front wedge block**, white painted "Under miner" lettering, a green LED by the servo and blue wheels.

Everything stated as fact is read from these photos. Anything inferred is marked **(guess)**. Dimensions in mm are **estimates**. Scale anchors: the **KST DS215MG** servo (a real part: case about **23.5 × 9 × 25 mm** without mounting tabs, **about 32 mm long including tabs**), the AWS antweight limit (150 g, 101.6 mm cube), and the wheels (Ø ≈ 22 mm). The reference width is **W = chassis body width (side wall to side wall) ≈ 80 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the centre of the black chassis footprint.
- **+X** = robot's right, **+Y** = forward (toward the scoop), **+Z** = up; mm.
- Chassis extents: x ∈ [−40, +40], y ∈ [−36, +36], z ∈ [2, 20].
- **Left/right** are the robot's own. In AWS67 the robot's left is on the image left. In AWS64 the robot's left side faces the camera (lower left).

| ID | Part |
|---|---|
| CH | black printed chassis tub |
| TD | top deck (the chassis top skin, with pockets) |
| LD-LR | left-rear small lid (recessed panel) |
| SV | KST DS215MG servo (lifter) |
| SVW | servo window (pocket in TD showing the servo) |
| SVB | white servo bracket / horn hub (AWS64) |
| HN | white servo horn (AWS64) |
| AR | central lifter arm (long black printed bar) |
| ARS | slot in the arm (AWS64) |
| CHN | central channel in which the arm lies |
| PVB | rear pivot blocks (two small raised blocks at the rear of the channel) |
| LD-R | right raised lid (electronics/battery cover, AWS67) / right lettering lid (AWS64) |
| LD-RR | right-rear recessed panel |
| HL-1 / HL-2 | two round holes in the front-left deck (switch / LED access) |
| TXT | "Under miner" lettering |
| SC-O | orange centre scoop (AWS67) |
| WG-L / WG-R | orange fixed side wedges (AWS67) |
| FP-B | brass hexagonal front plate (AWS64) |
| FW-S | silver-taped front wedge block (AWS66) |
| FT | fibre-reinforced tape on the front faces |
| WH-FL, WH-FR, WH-RL, WH-RR | four wheels |
| M-x | four N20 drive motors (hidden, guess) |
| S-TD | small black countersunk screws round the deck and lids |
| S-SC | 3 black countersunk screws on the centre scoop |
| S-FP | screw pairs on the brass plate |
| LED | small green LED (AWS66) |
| BAT, RX, ESC | hidden electronics |

---

## 1. Overall description in one paragraph

The Underminer is a **flat, rectangular, four-wheel servo lifter**. The body is a **black FDM box**, about **80 mm wide, 72 mm long and 18 mm tall**, with **four wheels at the corners** sticking out about 10 mm at each side. Its top deck is a patchwork of **screwed-on lids**: a raised **right-hand cover** over the electronics, a **recessed left-rear lid**, a **window on the left** through which a flat-lying **red-and-silver KST DS215MG servo** is visible, and a **front-left panel with two round holes** and the painted name. Down the middle runs a **channel holding a long, flat black lifter arm**. The arm is driven at its rear by the servo and carries the **front attachment**, which reaches past the chassis front. The front attachment changes between events: at AWS67 it is an **orange printed scoop in the middle flanked by two fixed orange wedges** covering the front wheels, all faced with fibre tape; at AWS64 it is a **single brass sheet cut as an elongated hexagon**; at AWS66 a **silver-taped full-width wedge block**. The wheels are **small (Ø 22 mm), white-hubbed, with ribbed blue or grey tyres**. They stand slightly taller than the body, so it can drive inverted.

---

## 2. Part-by-part description

### 2.1 Chassis (CH)
- **Shape**: a rectangular tub, **80 mm wide × 72 mm long × 18 mm tall** (z 2–20). The corners are **square with a small outer radius (about 1–2 mm)**. The side walls are vertical and plain. AWS64 shows the **left wall as a smooth black face** with horizontal layer lines, about 18 mm tall, with **two small black screw heads** near its top front and top rear corners (the lid screws seen from the side, or side fixing screws).
- **Wheel cut-outs**: the wheels are **outboard** of the side walls. The chassis does not wrap round them. Each wheel's inner face is about **1–2 mm** from the side wall.
- **Wall thickness**: about **2–2.5 mm** (seen at the servo window edges).
- **Floor**: not seen. Presumably a 1.5 mm floor at z ≈ 2 **(guess)**.
- **Colour/material**: matt black PLA or PETG. Top surfaces show **diagonal 45° infill lines** (AWS67).

### 2.2 Top deck (TD) and lids
The deck (z ≈ 20) is divided into five zones (left half, channel, right half). Every lid edge is ringed by small black countersunk screws.

- **LD-LR, left-rear lid**: a flat rectangular panel about **30 × 20 mm**, recessed about **1 mm** into the deck, at x ∈ [−36, −8], y ∈ [−34, −14], at the **left-rear corner** (image top-left in AWS67). Two screws: rear-left corner and front-left corner.
- **SVW, servo window**: an open rectangular pocket about **32 × 18 mm** (X × Y), at x ∈ [−32, −4], y ∈ [−14, +2] (the left-middle). The servo lies in it with its **label face up**, flush with or 1 mm below the deck. A **white sliver** on the window's left edge (AWS67) is part of the servo case or a white spacer.
- **Front-left panel**: a flat panel about **32 × 26 mm** at the left front, x ∈ [−36, −4], y ∈ [+8, +34]. It carries:
  - **HL-1 and HL-2**: two **round holes Ø ≈ 6 mm**, side by side about **14 mm apart**, near the panel's rear edge (just in front of the servo). Through the left one a dark interior is seen; through the right one something **red** (a red switch actuator, red wire, or LED) **(guess: switch access hole and LED hole)**.
  - **TXT**: **"Under" / "miner"** in two lines of **white bold rounded letters** about **7 mm tall**, painted or filled into engraved letters (AWS67, AWS66).
  - Screws at its front-left and rear-left corners.
- **LD-R, right raised cover (AWS67)**: a **raised rounded-rectangle lid**, about **36 × 42 mm** (X × Y), standing about **3–4 mm above the deck** (z ≈ 23–24), with **corner radii about 3 mm** and a **notch** at its rear-left corner (the outline steps in by about 5 mm at the rear-left). It is held by **4–5 screws** (one at each corner, plus one at the left-rear step). It sits at x ∈ [+6, +40], y ∈ [−16, +26].
  - **AWS64 version**: the right half of the deck is a **single long panel with raised lettering "UnderMiner"** (about 8 mm tall, silver/grey painted letters) running **along Y**, reading from the right side. This panel spans the whole right half (about 36 × 70 mm).
- **LD-RR, right-rear recessed panel**: behind LD-R, about **34 × 20 mm**, recessed 1 mm, held by **2 screws** at its corners.
- **Screws S-TD**: **small black countersunk/flat Phillips screws**, head Ø about **3.5 mm** (M2). AWS67 count: about **18** round the deck (front-left panel 3, left rear lid 2, servo window frame 2, centre channel 2, right cover 5, right rear panel 2, corners 2).

### 2.3 Central channel (CHN) and rear pivot blocks (PVB)
- **CHN**: a slot through the deck along the centreline, **about 14 mm wide (X)**, running the **full chassis length** from y = −36 to y = +34. Its floor is at about z ≈ 8 **(guess)**. The arm lies in it.
- **PVB**: at the rear end of the channel there are **two small raised black blocks**, about **8 × 8 × 6 mm**, one each side of the channel (x ≈ ±10, y ≈ −32), standing about **4 mm above the deck**. The left one in AWS67 has a **vertical slot/notch** and a small hole. These are the **pivot bearing blocks** for the arm's rear axle or the servo's far-side bearing **(guess)**.

### 2.4 Servo (SV), bracket (SVB) and horn (HN)
- **SV**: **KST DS215MG V3.0**, a **slim metal-cased "wing" servo**. The case has a **red anodised aluminium cover with white text "KST" and "DS215MG V3.0"**, and **silver aluminium side frames**, with a **slot-shaped cooling vent/label line** across it.
  - It lies **flat**, label up, in the servo window, its long side along X. The output spline is on its **right-hand end**, which faces the channel, so the **output axis is along X**, at about **y ≈ −8, z ≈ 12** **(guess, consistent with AWS64 where the white horn emerges at the servo's channel-side end)**.
- **SVB/HN (AWS64)**: a **white plastic part** at the channel-side end of the servo, about **10 × 6 × 6 mm**. A second **white rectangular block** is at the rear end of the servo window. These are the **servo horn (white nylon)** and a **white spacer/bracket** that clamps the servo. The horn connects to the arm.
- **Mount**: the servo is clamped in the window by the surrounding deck lips and screwed through its tabs (2 screws visible on the window frame at its corners) **(guess)**.

### 2.5 Lifter arm (AR) and slot (ARS)
- **Shape**: a **flat black printed bar**, about **12 mm wide (X) × 6 mm thick (Z)**, running from the **rear pivot (y ≈ −30)** to the front attachment, about **72 mm long** within the chassis, plus about **10 mm** beyond the front edge where it turns down into the scoop mount.
- **Top**: at deck level or **1–2 mm proud** of the deck (z ≈ 20–22) when lowered. AWS67 shows the arm top **flush with the deck** and its outline as a dark bar with layer-line sides.
- **Slot ARS (AWS64)**: a **through slot about 4 × 22 mm** along the arm near its rear third, with **raised edges** and a broken/rough rim. It is probably a **guide slot for the servo horn pin** (a slot-and-pin drive: the horn's pin runs in the slot and lifts the arm) **(guess, medium)**.
- **Front end**: the arm passes over the chassis front edge and **bends down** to the front attachment (hidden under the orange scoop in AWS67).

### 2.6 Front attachment, AWS67: centre scoop (SC-O) and side wedges (WG-L, WG-R)
- **SC-O (centre scoop)**:
  - **Shape**: a **block with a sloped front face**, about **46 mm wide (X) × 26 mm deep (Y) × 14 mm tall (Z)**. The top/front face is a **flat slope at about 35–40°** to the floor, with **rounded upper corners (r ≈ 4 mm)** in plan (the outline is a rounded rectangle). Its front edge reaches the floor.
  - **Fasteners S-SC**: **3 black countersunk hex (or Phillips) screws** in a **vertical line along the centreline** (along Y), about **8 mm apart**, head Ø ≈ 4 mm. They fix the scoop to the **arm's front end** underneath.
  - **FT**: **two rectangles of fibre-reinforced (filament) tape**, each about **18 × 28 mm**, either side of the screw line, showing the **white grid of glass fibres**. A thin clear tape also covers the upper part.
  - **Colour**: **bright orange** printed PLA/PETG.
- **WG-L / WG-R (side wedges)**:
  - **Shape**: each is a **sloped block**, about **24 mm wide (X) × 24 mm deep (Y) × 12 mm tall**, with its top surface a slope of about **35°** down to a floor edge. The outer upper corner is **chamfered/rounded** (r ≈ 3 mm). Each has a **rectangle of fibre tape** (about 16 × 22 mm) on its sloped face.
  - **Position**: directly **in front of the front wheels**, x ∈ [±26, ±50]. They are **fixed to the chassis**, not to the arm (they sit below the arm's line and their rear tucks under the wheel fronts). Gap between each side wedge and the centre scoop: about **2–3 mm**, which allows the scoop to rise.
  - **Height**: their tops are about **4 mm lower** than the scoop top.
  - **Mount (guess)**: bolted to the chassis front corners from underneath, or printed as one bracket that clips over the front wall corners. No screws visible on top.
- **Overall front width** at AWS67: about **96 mm** (two wedges + scoop + gaps), slightly wider than the chassis and nearly flush with the wheel outer faces.

### 2.7 Front attachment, AWS64: brass hexagon plate (FP-B)
- **Shape**: a single **thin sheet (about 0.5–0.8 mm)** of **brass or gold-coloured aluminium**, cut to an **elongated hexagon**: about **96 mm wide**, with a straight front edge about 60 mm long, two **45° chamfered front corners**, straight sides, and **two 45° chamfered rear corners** toward the chassis. Depth about **40 mm**.
- **Mounting**: two pairs of **black screws** (Ø ≈ 3) sit in the plate's middle, one pair forward and one pair at the rear-left, so the plate is screwed to the arm's front block. It covers the front wheels from above when lowered.
- **Surface**: covered by **clear/silver tape** with darker grey (dirty) patches; edges scuffed.

### 2.8 Front attachment, AWS66: silver taped wedge block (FW-S)
- **Shape**: a **full-width block (about 96 × 26 × 14 mm)** with a sloped front face, wrapped completely in **shiny silver tape** (aluminium-look or holographic) with a fibre tape panel in the middle. The outer ends cover the front wheels' tops. Same envelope as the orange set in AWS67.

### 2.9 Wheels (WH-FL, WH-FR, WH-RL, WH-RR)
- **Shape**: **Ø ≈ 22 mm × 10 mm wide**. **White hub** (Ø about 14 mm, with a small central hole) and a **ribbed tyre**: about **24–28 transverse ribs**, each about 1.2 mm tall. The ribs are wavy and soft, like printed TPU.
- **Colour**: AWS67 **blue tyres** on white hubs (the white shows as a ring on the inner side). AWS64 **grey tyres at the rear, blue at the front**. AWS66 blue.
- **Positions (centres)**: **WH-FL/FR at (±46, +24, 11)** and **WH-RL/RR at (±46, −24, 11)**. In AWS67 the front wheels sit **just behind the side wedges** and the rear wheels about 12 mm in from the rear corners. Wheelbase 48 mm. Track (centres) 92 mm; outer faces at ±51.
- **Height**: top at z = 22, about **2 mm above the deck** (z 20) and about level with the raised right cover (z 23–24). Bottom at z = 0, the chassis floor at z ≈ 2. So the robot can **drive inverted**, but only just: inverted, it rides on the wheels with the raised cover nearly touching the floor.
- **Guards**: **none**. The wheels are fully exposed at the sides. Only the side wedges (AWS67) or the hex plate (AWS64) shield the front wheels from the front.

### 2.10 Motors and plastic motor mounts (hidden)
- No motor is visible. With four wheels and a low 18 mm body, the drive is almost certainly **4 × N20 gearmotors** **(guess, medium)**, lying along X at each corner (two at the front, two at the rear), with shafts out through the side walls, held in **printed cradles** in the chassis floor and clamped down by the lids above them (the left-rear lid and the right-rear panel sit over the rear motors; the front-left panel and the right cover over the front motors).
- An alternative is **2 motors with the front and rear wheels on each side linked by a belt**. There is no belt visible outside, so this is less likely **(low)**.

### 2.11 Switch, LED, wires
- **HL-1** (front-left hole, left of the pair) is most likely a **switch access hole** for a screw-type or slide switch operated by a hex key **(guess)**.
- **HL-2** (right of the pair) shows red: a **red LED** or the switch body **(guess)**.
- **LED (AWS66)**: a **small green glow** to the right of the servo's front end (near HL-2), so HL-2 is probably an **LED window** **(medium)**.
- **Wires**: AWS67 shows a **yellow wire** visible beside the arm in the channel's front part (between the front-left panel and the arm). Others are hidden.

---

## 3. Per-view descriptions

### 3.1 Top view (plan, AWS67 is close)
- A black rectangle 80 × 72 mm with a full-length central slot holding a dark bar (the arm). Four blue wheel rectangles (10 × 22) stick out at the corners. Left of the arm, from rear to front: a small lid, the **red/silver servo**, then a panel with **two holes and "Under miner"**. Right of the arm: a **big raised rounded lid** and a small rear panel. About 18 screw dots.
- In front: an orange centre scoop (46 wide) and two orange side wedges (24 wide each), each with a white grid of fibre tape. Total length about **100 mm**, total width about **102 mm** over the wheels.

### 3.2 Front view
- At the floor: the three orange sloped faces (AWS67) or one hexagonal brass plate (AWS64). Behind them, the black front wall (80 × 18) and the four wheels' fronts sticking out to ±51. The arm's front end is in the middle, under/behind the scoop.

### 3.3 Left side view (AWS64 is closest)
- A plain black rectangle (72 × 18 mm) with two wheels (Ø 22) outboard, centred 48 mm apart, their tops 2 mm above the deck. The front plate/scoop sticks out ahead at floor level. The rear pivot blocks and the servo bracket peek above the deck line.

### 3.4 Rear view (not photographed; inferred)
- A plain black rear wall with two rear wheels at the corners. The arm's rear end and the pivot blocks stick up 4 mm above the deck at the centre.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 80 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | tub | 80 × 72 × 18 | 1 × 0.9 × 0.23 | black FDM | — | 1 |
| LD-LR | recessed lid | 30 × 20 × 2 | — | black | 2 × M2 | 1 |
| Front-left panel | flat lid | 32 × 26 × 2 | — | black + white letters | 3 × M2 | 1 |
| HL | round hole | Ø 6 | — | — | — | 2 |
| SVW | window | 32 × 18 | — | — | — | 1 |
| SV | wing servo | 23.5 × 9 × 25 (32 with tabs) | — | red/silver metal | 2 × M2 (guess) | 1 |
| SVB/HN | horn + spacer | 10 × 6 × 6 | — | white nylon | servo spline | 1–2 |
| CHN | slot | 14 × 70 | — | — | — | 1 |
| PVB | block | 8 × 8 × 6 | — | black | integral (guess) | 2 |
| AR | flat bar | 12 × 6 × ~82 | 0.15 × 0.08 × 1.0 | black FDM | pivot pin + horn | 1 |
| ARS | slot in arm | 4 × 22 | — | — | — | 1 |
| LD-R | raised lid | 36 × 42 × 4 | 0.45 × 0.53 | black | 5 × M2 | 1 |
| LD-RR | recessed panel | 34 × 20 × 2 | — | black | 2 × M2 | 1 |
| SC-O | sloped block | 46 × 26 × 14 | 0.58 × 0.33 × 0.18 | orange + fibre tape | 3 × M2 CSK into the arm | 1 (AWS67) |
| WG-L/R | sloped block | 24 × 24 × 12 | 0.30 × 0.30 × 0.15 | orange + fibre tape | to chassis (hidden) | 2 (AWS67) |
| FP-B | hexagon sheet | 96 × 40 × 0.6 | 1.2 × 0.5 | brass | 4 screws | 1 (AWS64) |
| FW-S | taped block | 96 × 26 × 14 | — | silver tape | — | 1 (AWS66) |
| WH | ribbed wheel | Ø 22 × 10 | 0.28 × 0.13 | white hub, blue/grey TPU | motor shaft | 4 |
| S-TD | CSK Phillips | M2, head Ø 3.5 | — | black | into chassis | ~18 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| Lids ↔ deck | screwed | 0 |
| LD-R top ↔ deck | raised | +3 to +4 |
| SV ↔ SVW | clamped | 0 |
| SV label face ↔ deck top | flush / below | 0 to −1 |
| HN ↔ SV spline | splined | 0 |
| HN pin ↔ ARS | sliding in the slot (guess) | 0.2 |
| AR ↔ CHN walls | side by side | 1 each side |
| AR rear ↔ PVB | pinned (guess) | 0 |
| AR top ↔ deck (lowered) | flush/proud | 0 to +2 |
| SC-O ↔ AR front end | 3 screws | 0 |
| SC-O front edge ↔ floor (lowered) | touching | 0 |
| SC-O side ↔ WG side | side by side | 2–3 |
| WG ↔ chassis front corners | fixed | 0 |
| WG front edge ↔ floor | touching | 0 |
| WG rear ↔ WH-FL/FR tread | close | 1–3 |
| WH inner face ↔ CH side wall | near | 1–2 |
| WH top ↔ deck | wheel proud | +2 |
| WH bottom ↔ floor | touching | 0 |
| CH floor ↔ floor | above | ~2 |
| FP-B (AWS64) ↔ front wheels top | over the wheels | 2–3 above |

---

## 6. Mechanism
1. **Drive**: 4WD skid steer (4 × N20 guessed), wheels at the corners.
2. **Lifter**: the KST servo lies flat with its output along X. Its white horn engages the arm. The arm pivots near the rear of the chassis (PVB) and its front carries the scoop. When the servo turns, the arm rotates up about the rear pivot and the scoop's front edge rises. With a lever about 70–75 mm long from pivot to scoop tip, a 30° arm rotation gives about **35 mm of tip rise**. The pin-in-slot drive (ARS) means the horn can push the arm up while the servo's rotation is converted into a near-linear lift **(guess)**.
3. **Side wedges** (AWS67) are fixed, so even when the scoop is raised the robot still presents low wedges at the front corners.

---

## 7. Assembly order (suggested rebuild)
1. Print **CH** (tub with floor, motor cradles, servo pocket, central channel, pivot blocks).
2. Fit **4 N20 motors** in the corner cradles, shafts out through the side walls at z ≈ 11.
3. Press on the **4 wheels**.
4. Fit the **servo** flat in its window with its spline toward the channel. Fit the **white horn**.
5. Fit the battery, ESCs and receiver under the right raised cover; the switch and LED under the front-left panel.
6. Lay the **arm** in the channel, pin its rear end in the pivot blocks, and engage the horn pin in the arm slot.
7. Screw on all lids (about 18 × M2): left-rear lid, front-left panel (with lettering), right raised cover, right-rear panel.
8. Screw the **centre scoop** to the arm's front end (3 screws). Fix the **side wedges** to the chassis front corners.
9. Apply **fibre tape** to all three front faces.

---

## 8. Hidden / uncertain list
- Exact pivot location and the horn-to-arm coupling (pin-in-slot is a guess).
- Motor count and layout.
- How the side wedges are fixed.
- Switch type, LED.
- All dims ±15 %.

## 9. Coordinate frame (restated)
Origin on the floor at the centre of the chassis footprint; +X right, +Y forward, +Z up; mm. Chassis x ∈ [−40, 40], y ∈ [−36, 36], z ∈ [2, 20]. Wheels at (±46, ±24, 11). Front attachment from y = +36 to y ≈ +62.

## 10. Profiles as math

**10.1 Arm side profile (YZ at x = 0, lowered).** Rear pivot P = (y −30, z 14). Top line z = 21 for y ∈ [−34, +34]. Front bend: arc centre (y 34, z 15), r = 6, from θ = 90° to θ = 0°, then a vertical drop on y = 40 down to z = 8, where it meets the scoop block. Raised position: rotate the whole arm about P by θ_lift ∈ [0°, 30°]: (y′, z′) = P + R(θ)·((y, z) − P).

**10.2 Centre scoop SC-O (YZ section, constant over |x| ≤ 23).** Polygon (36, 14), (40, 14), (62, 0), (36, 0). The front face is the line z = 14 − 0.636·(y − 40), slope atan(0.636) = 32.5°… (photos read 35–40°; use 35°: z = 14 − 0.70·(y − 40), meeting the floor at y = 60). Plan corners rounded r = 4 at the two front corners.

**10.3 Side wedges WG (YZ section, 26 ≤ |x| ≤ 50).** Polygon (34, 12), (36, 12), (54, 0), (34, 0); slope atan(12/18) = 33.7°. The outer top-front corner is rounded r = 3 in plan.

**10.4 Brass plate FP-B (plan).** Hexagon with vertices (±30, 64), (±48, 46), (±48, 34), (±36, 24)… straight front edge y = 64 for |x| ≤ 30, 45° chamfers to the sides, sides at |x| = 48 from y 46 to 34, rear chamfers to (±36, 24).

**10.5 Raised cover LD-R (plan).** Rounded rectangle x ∈ [6, 40], y ∈ [−16, 26], r = 3, minus the rear-left notch x ∈ [6, 11], y ∈ [−16, −10]; top at z = 24.

**10.6 Wheel tread.** r(φ) = 10.0 + 1.2·[sin(26φ) > 0], extruded 10 mm.

## 11. Pixel-based measurements (AWS67 native 1352 × 1228, ±10 px)
- Wheels' outer faces: x ≈ 100 (left) to ≈ 1125 (right) → 1025 px.
- Chassis body: x ≈ 215–1005 → 790 px.
- Servo visible case (silver-red): x ≈ 150–440 of the crop + 150 offset → about 290 px wide, 150 px tall.
- Rear-left wheel along Y: y ≈ 90–300 → 210 px. Front-left: y ≈ 520–680 (partly hidden behind the wedge).
- Orange centre scoop: x ≈ 350–860 (510 px) × y ≈ 550–1040.
- Side wedges: left x ≈ 95–335, right x ≈ 880–1150.
- Lettering "Under" ≈ 300 px wide, 60 px tall.

## 12. Several independent estimates

| Quantity | Method A (servo case 30 mm incl. part of tabs) | Method B (cube limit) | Method C (wheel Ø 22 → px/mm) | Reconciled |
|---|---|---|---|---|
| px/mm at deck level | 290 / 30 = 9.7 | — | 210 / 22 = 9.5 | **9.6** |
| Chassis width | 790 / 9.7 = 81 | ≤ 101.6 − 2 × 11 (wheels) = 80 | 790 / 9.5 = 83 | **80** |
| Overall width over wheels | 1025 / 9.7 = 106 | ≤ 101.6 | 1025 / 9.5 = 108 | **102** (wheels are lower than the deck so they appear larger; see §13) |
| Scoop width | 510 / 9.7 = 53 (nearer the camera → inflated) | — | — | **46** |
| Lettering height | 60 / 9.6 = 6.3 | — | — | **6–7** |
| Chassis length | (650 − 75) / 9.6 / sin 62° = 68 | — | wheelbase 405 px / 9.6 / 0.88 ≈ 48 + 2 × 12 | **72** |

## 13. Consistency check
1. **Overall width** comes out at 106–108 by pixels, over the 101.6 mm cube. The front-facing camera is closer to the front wheels and wedges than to the servo, which inflates them. Rescaling by about 0.94 gives about **100–102**. The robot may also be measured diagonally in the cube. **Reconciled: 102 over the wheels**, chassis 80.
2. **Wheel diameter**: 22 mm from the pixel ratio, and the AWS64 view where the wheel top stands just above the 18 mm chassis wall. **Consistent.**
3. **Arm length vs pivot**: the arm starts at the rear pivot blocks (y ≈ −32, the top of the AWS67 image) and reaches the scoop. Lever ≈ 70 mm. **Consistent** with a strong-enough servo for 150 g (the DS215MG gives about 5 kg·cm; at 7 cm that is about 0.7 kg at the tip, so it can lift the front of a 150 g robot comfortably).
4. **Servo orientation**: a flat-lying wing servo has its spline on a narrow face. AWS64 shows the white horn at the channel side of the servo, consistent with a spline axis along X. **Consistent.**
5. **Side wedges fixed vs moving**: in AWS67 their tops are lower than the scoop's, and there is a gap between them and the scoop. If they moved with the arm they would need a cross-bar, which is not seen. **Reconciled: fixed.**

---

## 14. Why the designer did it (per part; adversarial lens first)

- **CH: flat 18 mm box, 4 wheels outside**
  - Fight: a low body leaves little for vertical spinners to hit and gives a low centre of gravity against flips. The wheels outboard give a wide track, so the robot is hard to tip sideways.
  - Weak points: the wheels are completely unguarded at the sides. A horizontal spinner or an enemy wedge from the side reaches them directly. The designer traded protection for weight and simplicity.
  - Construction: one print with pockets; lids give access to each zone separately.
- **Multiple screwed lids**: each subsystem (servo, electronics, motors) can be reached without taking the whole robot apart, which speeds up repairs between fights. Small lids are stiffer than one big lid.
- **Raised right cover**: makes room for a taller part (the battery or a stacked ESC/receiver) without making the whole chassis taller.
- **Flat-lying wing servo (DS215MG)**: a slim servo lying flat fits in an 18 mm body; metal gears ("MG") survive shock loads; the metal case acts as a heat sink. Showing it through a window saves a lid and lets the team check it.
  - Adversarial: the servo window is on top, protected from frontal and side attacks by the chassis walls. A hit on the scoop is taken by the arm and the pivot first.
- **Long arm with rear pivot**: the longest possible lever in the body length gives the biggest tip rise for a small servo rotation. The pivot at the rear means the scoop arcs up and back, tipping opponents backward toward the robot (then they can be pushed) or onto their backs.
- **Pin-in-slot drive (guess)**: limits the load on the servo when the scoop is hit: the force goes through the arm into the pivot and the horn pin, not straight into the spline.
- **Centre scoop + fixed side wedges (AWS67)**
  - Getting under: three low edges across the whole front. If the opponent comes at a corner, a fixed wedge gets under it. If straight on, the scoop gets under and lifts.
  - Adversarial: the side wedges cover the **front wheels** from frontal attacks (spinners hit the wedge, not the tyre). Fibre tape stops the printed faces splitting and makes them slick.
  - The gaps let the scoop move freely.
- **Brass plate (AWS64)**: a thin metal edge gets under printed wedges, and the metal survives spinner hits better than plastic. The hexagonal cut keeps the corners clear of the wheels when the plate is raised.
- **Silver taped block (AWS66)**: a cheap full-width replacement; tape makes it slick.
- **Wheels Ø 22, proud of the deck**: just enough to keep driving when inverted. Soft TPU ribs grip the floor for pushing.
- **Holes for switch/LED**: the rules need the switch reachable and the robot's on state visible. A recessed switch in a hole cannot be knocked off by an opponent.
- **Black countersunk screws**: flush heads give nothing for an opponent to catch on.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 (300–500 rpm) | 12 × 10 × 25 each | at the corners: (±30, ±24, 11), axes along X | medium |
| Motor cradles | printed U-pockets in the floor, clamped by the lids | 14 × 12 × 12 | under the lids | medium |
| Battery | 2S 7.4 V LiPo 150–180 mAh | 35 × 20 × 12 | under LD-R: (+22, −4, 10) | medium |
| ESCs | 2 dual brushed ESCs or one 4-ch board | 20 × 15 × 4 each | under LD-R / LD-RR | low |
| Receiver | micro 2.4 GHz | 18 × 12 × 4 | under the front-left panel | low |
| Switch | slide or screw switch behind HL-1 | 10 × 5 × 5 | (−24, −14, 14) | low |
| LED | 3 mm green LED behind HL-2 | Ø 3 | (−10, −14, 16) | medium |
| Arm pivot pin | steel M2/M3 pin or screw through the PVB blocks | Ø 2.5 × 24 | (0, −30, 14) | medium |
| Side wedge mounts | 2 × M2 screws from below into the chassis front corners, or a printed tab | — | (±38, +34, 4) | low |
| Wiring | battery → switch → ESCs → motors; servo lead to the receiver; all below z 18 | — | — | medium |

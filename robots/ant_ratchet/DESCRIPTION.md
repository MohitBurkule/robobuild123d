# Ant Ratchet: full rebuild description from reference photos

Source photos (three versions of the same concept; the two newest are cut out onto white):
- `robots/ant_ratchet/reference/ant_ratchet.aws76.webp`: AWS 76 (**primary**). **Front-right three-quarter**, camera about 25–30° above the floor, about 40° right of the nose. Bright **red** printed body, **clear polycarbonate (PC) front plate over a "Ratchet & Clank" print**, **black front corner skids**, a **pale pink translucent TPU gear-tread wheel** at the rear right, and a **clear PC side guard plate** in front of/outside that wheel.
- `robots/ant_ratchet/reference/ant_ratchet.aws72.webp`: AWS 72. **Front-left three-quarter**, camera about 35° above the floor. **Darker red** body heavily covered by clear PC panels over printed red/black marble art; a **clear rear top lid**, an **open gap** between lid and front plate showing wires and a red ribbed part, a **green-tinted clear left side wedge plate** reading "ANT RATCH…", a **white JST connector** on the left side, and a **beige/grey TPU wheel** at the rear left.
- `robots/ant_ratchet/reference/ant_ratchetaws63.webp`: AWS 63, an older version labelled **"ANT RATCHET VI"**. **Straight front view** on an arena-like patterned floor (not cut out). **Olive-brown** printed body, clear PC panels over **flame** prints, **black treaded wheels** at the rear corners, angled side wedges, a grey printed hinge block above the front plate.

The CAD target is the **AWS76** version. The other two are used to confirm hidden structure (top layout, the gap/servo, the side wedges), and their differences are listed.

Pixel coordinates refer to copies scaled to **1200 px on the long side** (AWS76 → 1200 × 776, AWS72 → 1200 × 958, AWS63 → 829 × 753 native size), ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit and from the parts. Ratios use **W = red body width (side wall to side wall, excluding wheels and guards) ≈ 74 mm**.

`REFERENCE.json`: `lifter`, 2 wheels, weapon lifter, axis x, position front, `width_frac` 0.62 (the lifter plate is 62% of the overall robot width).

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the art-covered plate), **+Z** = up. **Origin O** = floor point under the centre of the red body footprint.
- In AWS76 the robot's **right** side faces the camera; in AWS72 the **left** side; AWS63 is head-on.
- Lifter plate angle **β** = slope of the plate face above the floor (YZ plane).

| ID | Part |
|---|---|
| CH | red printed body (tub + integral top) |
| TS | top surface with the long lifter slot |
| SLT | long transverse/longitudinal slot in the top (AWS76) |
| SWH | small rectangular hole in the top (switch / link) |
| LED | small round hole in the top (indicator or link pin) |
| LP | front lifter plate (printed backing) |
| LPC | clear PC face plate over the art on LP |
| ART | Ratchet & Clank print sheet |
| LIP | clear PC lip strip at LP's bottom edge |
| LP-S | screws on LP (6 in AWS76) |
| PV | lifter pivot bolt with washer/nut on the side wall |
| SK-L / SK-R | black front corner skids |
| SK-S | screws in the skids |
| WH-L / WH-R | rear drive wheels (pink TPU gear tread in AWS76) |
| GP-L / GP-R | clear PC side guard plates in front of/outside the wheels |
| GB-L / GB-R | red guard brackets (printed blocks between the body and GP) |
| GP-S | screws through GP into GB |
| AXS | wheel outer axle screw in GP (AWS76) |
| S-TS | screws on the top |
| SV | lifter servo (hidden; red ribbed part in AWS72 may be it) |
| DM-L / DM-R | drive gearmotors (hidden, guess) |
| BAT, RX, ESC | electronics (wires visible in AWS72) |
| JST | white connector on the left side (AWS72) |
| SWG-L | left side wedge plate "ANT RATCH…" (AWS72) |
| RL | rear clear lid over flame/marble art (AWS72, AWS63) |

---

## 1. Overall description in one paragraph

Ant Ratchet is a **two-wheel servo lifter** built as a **squat, wedge-fronted red box**. The body is about 74 mm wide, 84 mm long and 32 mm tall, with a flat top and a **front slope** that is almost entirely the **lifter plate**: a printed panel about 46 mm wide × 50 mm long, faced with **clear 1 mm polycarbonate** sandwiching a **printed picture of Ratchet and Clank** in front of red flames, held with six silver Torx/Phillips screws, and ending in a **clear PC lip** that touches the floor. At each front corner a **black printed skid**, a long low sloped block, rides on the floor beside the plate. The two **drive wheels** are at the **rear corners**, outboard of the body: in AWS76 they are **pale pink translucent TPU** with **coarse gear-like teeth**, about Ø 34 × 12 mm. In front of and outside each wheel, a **clear PC guard plate** (an elongated hexagon) is bolted to a **red printed bracket**, shielding the lower front of the wheel and carrying its outer axle screw. The top is flat red with a long slot, six or more silver screws, a small rectangular hole and a small round hole. A **silver bolt with a washer** on each side wall, just behind the top of the plate, is the **lifter pivot**.

---

## 2. Part-by-part description

### 2.1 Body (CH)
- **Shape**: a box with a **flat top** at z ≈ 32, **vertical side walls**, and a **front that slopes down** to the floor. Plan **74 mm wide × 84 mm long** (y −42 to +42). The top flat runs from the rear (y −42) to about y +8; the front slope (the lifter plate region) runs from y +8, z 32 to the floor at about y +42. The side walls follow that slope: their front edge is the sloped line, so the body in side view is a **trapezoid** (a rectangle with the front-top corner cut off).
- **Rear**: the rear wall is vertical (seen in AWS72 as a short red face behind the wheel) **(mostly guess)**.
- **Side walls**: flat, red, with **strong horizontal layer lines** (the sides were printed as vertical walls). Wall thickness about **2.5 mm** (seen in the top slot edges). In AWS76, behind the lifter plate on the right side, there is a **ribbed band** (fine vertical ribs, like a knurled strip) running along the top edge of the side wall and down the slope edge — the edge of the **lifter plate's side cheek**, printed with vertical ridges **(guess)**; AWS72 shows the same ridged red edge on both sides of the plate.
- **Colour/material**: **bright red PLA/PETG** (AWS76), darker red (AWS72), olive-brown (AWS63).
- **Lower front corners**: the black skids SK attach here.
- **Underside**: not seen. A ground clearance of about **1–2 mm** is suggested by the plate lip and skids touching the floor while the body's lower edges are just above it.

### 2.2 Top surface (TS), slot (SLT), holes (SWH, LED), screws (S-TS)
- **Top**: flat, about **74 × 50 mm** (y −42 to +8). In AWS76 the front half is a **separate raised lid**: a step about **1 mm** runs across at y ≈ +5, and a **long transverse slot** (SLT) about **50 mm wide (X) × 7 mm deep (Y)** opens just behind the lifter plate's top edge, at y ≈ +2, x −25 to +25. Through it, dark interior and a red part (the lifter's top bar / servo horn, **guess**) are visible. A second, parallel **raised bar** (about 6 mm wide, 2 mm tall) runs across in front of the slot: the **top edge of the lifter plate frame** (its hinge knuckle) **(guess)**.
- **SWH**: a small **rectangular hole about 8 × 3.5 mm**, long axis along X, on the right rear of the top at x ≈ +12, y −20. It is a **slot for a removable power link or a slide-switch actuator** **(guess)**.
- **LED**: a small **round hole Ø 2.5 mm** at x ≈ +20, y −28 (AWS76), possibly an LED window or a link pin hole.
- **S-TS**: **silver pan-head Torx/Phillips screws**, head Ø **4.5 mm** (M2.5–M3), with a small **green-ish tinge** in places (thread-lock or a reflection). AWS76 shows them at: rear-left corner (x −32, y −38), rear-mid (x −5, y −40), rear-right corner (x +32, y −36), right edge front (x +32, y +2), front-left (x −20, y +5) and in the middle (x +15, y −10). About **6–7** in total.
- **AWS72**: the top is instead covered by a **clear PC rear lid** (RL) over **red/black marble-print paper**, about **74 × 40 mm**, held with **4 silver screws** at its corners; between its front edge and the lifter plate there is an **open gap about 12 mm** showing **red and black wires**, a **red ribbed block** about 15 × 8 × 6 mm (the servo, or a printed servo-saver/horn hub) and the inside of the body.
- **AWS63**: similar layout: a clear rear lid over flames with 4 screws, a gap, and a **grey printed hinge block** (about 40 × 8 × 8 mm) along the top of the lifter plate, with a raised tab in its centre.

### 2.3 Lifter plate (LP, LPC, ART, LIP, LP-S)
- **Shape**: a **flat rectangular panel** about **46 mm wide (X) × 50 mm along the slope × 3 mm thick** (printed backing 2 mm + PC 1 mm), lying at **β ≈ 40°** (AWS76; AWS72 looks closer to 35°). Its top edge is at (y +8, z 32); its lower edge at about (y +46, z 1).
- **Printed backing**: red, with a raised **frame border about 3 mm wide** at its sides (the ribbed cheeks) that wrap around the side edges to the side walls.
- **Clear PC face (LPC)**: a **1 mm clear polycarbonate sheet**, the same size as the plate, which protects the **art print** (ART) underneath — a glossy paper print of **Ratchet (yellow Lombax) and Clank**, with the black-and-white striped outfit, a blue gun/gauntlet, and a red flame background. In AWS72 the PC sheet is scratched and fogged with white abrasion marks; its corners are slightly lifted.
- **Lip (LIP)**: along the bottom, the PC sheet **extends about 8–10 mm beyond** the printed backing, as a **clear strip** (AWS76 shows a band of **frosted/scuffed clear PC** across the full width at the bottom, about 10 mm tall), forming a **thin flexible leading edge** that touches the floor. In AWS72 the clear lip is bent slightly downward. In AWS63 the bottom clear strip is about 10 mm and sits just above a heart-patterned floor.
- **Screws (LP-S)**: AWS76 shows **6 silver Torx pan-head screws** (head Ø 4.5 mm): two near the top corners (about 5 mm in from the top and side edges), two at mid-height near the edges, and two lower (about 12 mm above the bottom edge). AWS72 shows **4** (top-right, two mid, bottom-left) plus a few hidden; AWS63 shows **6** in two columns of three.
- **Width check**: the plate occupies the centre **46 mm** of the 74 mm body; the corner skids take the outer 14 mm each side.

### 2.4 Lifter pivot (PV)
- On the **right side wall** (AWS76) at about **(x +37, y −2, z 26)** — i.e. on the side wall, just behind the top of the plate and 6 mm below the top surface — there is a **silver hex/button bolt head with a large flat washer** (washer Ø about 8 mm, bolt head Ø 5 mm). A matching bolt head is presumed on the left **(guess)**.
- This bolt is the **pivot of the lifter frame**: the lifter plate is part of a **U-frame** whose side cheeks run back inside the side walls to this bolt. When the servo lifts, the frame rotates about PV and the plate's lower edge swings up and back.
- AWS72 shows two **silver screws** on the left side wedge plate near the top (x −40, y +5 and y −2): one of them probably the left pivot.

### 2.5 Front corner skids (SK-L, SK-R)
- **Shape (AWS76)**: a **black printed block** at each front corner, about **12 mm wide (X) × 45 mm long (Y) × 14 mm tall** at its rear, with a **sloped top face** running down to a **toe** on the floor ahead of the body. Seen from the side it is a long low **wedge/ramp** with a **flat bottom**, a **rounded rear top** (radius about 4 mm), and a front tip that is a **chamfered toe about 3 mm tall** (not a knife edge). It has a **vertical inner face** beside the lifter plate and a flat outer face flush with the body side wall.
- **Position**: x ±31 to ±43 (i.e. its outer face is **slightly proud** of the body side wall, by about 5 mm), y +5 to +50, z 0 to 14. The toe reaches about **4–8 mm ahead** of the lifter plate's lower edge.
- **Fixings**: on its outer face a **black screw head** in a recess (about Ø 4) at mid-length, and a **round hole** (Ø 3) low near the front; one more black screw at the rear-top end. They screw into the body's front corners.
- **Colour/material**: **matt black**; probably TPU or PETG (a slightly rubbery look) **(guess)**.
- **AWS72/AWS63 equivalent**: instead of skids, AWS72 has a **sloped side wedge plate** at the left front corner: a **green-tinted clear PC plate** with a mirrored silver/green marbled print and the text **"ANT RATCH(ET)"** in silver letters, shaped as a **trapezoid** about **35 mm long × 30 mm tall**, sloping like the lifter plate but angled outward, held with **4–5 silver screws** along its edges onto a **red printed triangular cheek** behind it. AWS63 has two such **side wedges** (olive printed, with a triangular-pattern texture) flanking the plate, each about 20 mm wide, angled to deflect outward.

### 2.6 Drive wheels (WH-L, WH-R)
- **AWS76 shape**: a **thick pale pink translucent TPU wheel**, about **Ø 34 mm × 12 mm wide**, with **coarse gear-like teeth** on the rim: about **36–40 teeth**, each about **2 mm tall × 2 mm wide**, square-ish, running straight across the width. The outer face has a recessed hub with a **silver screw** at the centre (the outer axle support through the guard, see AXS).
- **AWS72**: **beige/grey TPU** wheels of the same size and tooth form (the left wheel shows ~10 teeth across its visible arc).
- **AWS63**: **black rubber-treaded wheels** (fine ribs), about Ø 32 × 12.
- **Position**: centres at **x ±44, y −24, z 17**. The inner face is about 1 mm from the body side wall (x ±37); the outer face at x ±50. The wheel top (z 34) stands **2 mm above** the top surface (z 32), so the robot can just about **drive inverted** on the wheels and the rear top edge **(guess)**.
- **Mount**: wheel on the drive motor shaft from inside, and **supported on the outside** by the guard plate GP via the axle screw AXS (a double-supported wheel).

### 2.7 Wheel guards (GP-L, GP-R) and their supports (GB-L, GB-R)
- **GP shape**: a **clear polycarbonate plate**, about **1.5–2 mm thick**, standing vertically in the **XZ… actually YZ plane** (parallel to the side wall), outline an **elongated hexagon**: about **38 mm long (Y) × 22 mm tall (Z)**, with its front and rear ends cut at 45° chamfers (each about 7 mm) and a straight top and bottom. It spans from about y −36 (behind the wheel axle) to y +2 (in front of the wheel), at **z 4 to 26**, **outside** the wheel's outer face at x ≈ +52.
- **What it covers**: the **lower half of the wheel's outer face** and the gap in front of the wheel. The wheel's top half and tread are exposed above it.
- **GB shape**: a **red printed bracket block** about **14 mm long × 14 mm tall × 15 mm wide (X)**, sticking straight out from the body side wall **in front of the wheel** at y −5 to +9 (centre y +2), z 6 to 20, out to x ≈ +52. It bridges between the body and the front part of GP.
- **Fasteners**:
  - **GP-S**: **3 silver pan-head screws** (head Ø 4.5) on the front part of the plate into GB: one at the front-upper corner (y −1, z 20) and **two stacked** (y +6, z 18 and y +6, z 10) — AWS76 shows them as a column of two plus one, with **nuts/washers** on some.
  - **AXS**: a single screw at the wheel centre (y −24, z 17) through GP into the wheel hub or an axle — so GP is also the **outer bearing plate** of the wheel.
- **Colour**: clear, slightly scratched, edges whitish.
- **AWS72**: the left guard is a **vertical clear plate tinted green** in front of the left wheel with **4 silver screws** in a vertical column — the same idea, taller (about 30 mm), extending down to the floor.

### 2.8 Electronics, wires, switch
- **AWS72**: through the gap: **red and black silicone wires** (about 22–26 AWG) in loose loops, the **red ribbed block** (servo case or a printed servo mount with cooling slots), and a **white 2-pin JST** connector mounted in a hole on the **left side wall** at about (x −37, y −5, z 22), facing out: a **charge/balance port or power link** **(guess)**.
- **AWS76**: closed top; the rectangular hole SWH is the probable power link/switch.
- No external wiring on AWS76.

---

## 3. Per-view sections

### 3.1 AWS76 (front-right iso)
- **Left**: the black left skid seen end-on as a sloped black bar at (25–240, 205–465).
- **Centre-left**: the lifter plate at (75–735, 145–665) px with the art and **6 screws** at about (360, 180), (275, 285), (665, 315), (200, 380), (580, 435), (500, 545); the frosted clear lip band at (75–560, 415–660).
- **Centre**: the right black skid at (505–810, 425–745), its screw at (775, 480).
- **Top**: flat red top (330–1095, 30–260) with the slot (545–860, 100–135), the small rectangular hole at (850–880, 160), the round hole at (935, 195), and screws at (585, 40), (518, 65), (860, 120), (1040, 185), (965, 220).
- **Right**: the pivot bolt with washer at (915, 300); the pink wheel at (950–1175, 255–520); the guard plate GP at (810–1100, 340–605) with screws at (885, 525), (990, 490), (985, 545); the red bracket GB behind GP's front half.

### 3.2 AWS72 (front-left iso)
- Lifter plate at (390–1130, 225–860) with the PC lip at the bottom right; the left side wedge plate "ANT RATCH…" at (180–470, 425–870); the green clear guard at (55–185, 285–625) with 4 screws; the beige wheel at (75–205, 255–420); the rear clear lid at (160–880, 45–310) with screws at (240, 220), (265, 265), (820, 125), (775, 90); the white JST at (255–300, 360–410); wires and the red ribbed block through the gap at (330–780, 200–330).

### 3.3 AWS63 (front)
- A symmetric front view: plate 440 px wide at (200–640, 250–630) with 6 screws; side wedges (120–200 and 640–800) with triangle texture; rear lid (165–690, 30–190) with 4 screws; black wheels at the far left and right top corners; clear side guards at the extreme edges (40–100 and 760–820) with silver bolt heads at z mid-height; grey hinge block at (330–480, 205–250).

### 3.4 Top view (AWS76, synthesised)
- A 74 × 84 rectangle; the front 34 mm is the sloped plate (46 wide) flanked by the 12 mm skids, whose toes stick 6 mm further forward; the slot just behind the plate top; the wheels at the rear corners (12 mm outboard each side, total width ≈ 100 mm); the guard plates outside the front halves of the wheels with the red brackets ahead of the wheels.

### 3.5 Side view (right)
- Trapezoid body: rear vertical 32 tall, top flat to y +8, slope down to y +42. The black skid along the bottom front, the pivot bolt near the top at y −2, the wheel Ø 34 at the rear with the hexagonal clear guard over its lower front quarter, the red bracket ahead of the wheel.

### 3.6 Rear view (not photographed)
- Vertical red rear wall 74 × 32; wheels at both sides sticking 2 mm above the top. Possibly the servo body or a switch **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | trapezoid-profile box | 74 × 84 × 32 | 1 × 1.14 × 0.43 | red FDM | — | 1 |
| SLT | slot | 50 × 7 | 0.68 | — | — | 1 |
| SWH | rect hole | 8 × 3.5 | — | — | — | 1 |
| LP | sloped panel | 46 × 50 × 2 | 0.62 × 0.68 | red FDM | pivot frame | 1 |
| LPC | clear sheet | 46 × 58 × 1 | 0.62 × 0.78 | polycarbonate | 6 × M2.5 | 1 |
| ART | paper print | 44 × 48 | — | photo paper | under LPC | 1 |
| LIP | extension of LPC | 46 × 9 × 1 | — | PC | — | 1 |
| PV | bolt + washer | M3, washer Ø 8 | — | steel | through side walls | 2 |
| SK | ramp block | 12 × 45 × 14 | 0.16 × 0.61 × 0.19 | black TPU/PETG | 2 × M2.5 | 2 |
| WH | gear-tread wheel | Ø 34 × 12, ~38 teeth | 0.46 × 0.16 | pink TPU (76) | motor shaft + AXS | 2 |
| GP | hexagonal plate | 38 × 22 × 1.5 | 0.51 × 0.30 | clear PC | 3 + 1 screws | 2 |
| GB | bracket block | 14 × 14 × 15 | 0.19 | red FDM | integral with CH (guess) | 2 |
| S-TS | pan Torx | head Ø 4.5 | — | silver | into CH | 6–7 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| LPC ↔ LP | screwed (6) | 0 |
| LIP ↔ floor | touching | 0 |
| LP side cheeks ↔ CH side walls (inside) | sliding | 0.5–1 |
| LP side edge ↔ SK inner face | side by side | 1–2 |
| LP top edge ↔ top surface front edge | slot clearance | 2–7 |
| PV ↔ CH side wall | bolted | 0 |
| SK ↔ CH front corners | screwed | 0 |
| SK bottom ↔ floor | touching | 0 |
| SK toe ↔ LIP edge (y) | toe ahead | 4–8 |
| WH inner face ↔ CH side wall | near | 1 |
| WH outer face ↔ GP inner face | near | 1–2 |
| GP ↔ GB | screwed (3) | 0 |
| GP ↔ WH axle | AXS screw | 0 |
| GB ↔ CH side | integral/bolted | 0 |
| GB rear face ↔ WH tread | near | 1–3 |
| GP bottom ↔ floor | above | 4 |
| WH top ↔ top surface | above | +2 |
| CH bottom ↔ floor | above | 1–2 |

---

## 6. Mechanism

- **Drive**: two rear wheels, skid steer; the front rests on the plate lip and the skids.
- **Lifter**: a servo inside the body drives the lifter frame, which pivots at PV (y −2, z 26). The plate's lower edge is about **50 mm** from PV (√(48² + 25²) ≈ 54 mm). Rotating the frame up by 45° lifts the lip by about **35–40 mm**, tilting an opponent backward. Driven either by the servo horn directly on the pivot axis, or via a short link **(guess)**.
- The slot SLT gives clearance for the frame's top edge as it rotates back.

---

## 7. Assembly order (suggested)

1. Print CH (with integral guard brackets GB), LP frame, skids SK.
2. Fit the two drive gearmotors at the rear corners; push on the wheels.
3. Install the servo, battery, receiver, ESC; set the power link in SWH.
4. Insert the lifter frame, align with the side-wall holes, fit the **pivot bolts PV** with washers.
5. Couple the servo to the frame.
6. Lay **ART** on LP, cover with **LPC**, screw with 6 screws; check LIP touches the floor.
7. Screw the **skids SK** to the front corners.
8. Bolt **GP** to **GB** (3 screws) and fit **AXS** through GP into the wheel hub.

---

## 8. Hidden / uncertain list
- Lifter drive (direct servo on the pivot vs linkage); whether the pivot is on both sides.
- Exact servo location; contents.
- Rear wall, underside.
- Whether GB is integral or a separate printed part.
- Wheel motor type and whether the AXS is a real axle or a dummy screw.
- AWS72/63 versions differ in side panels and colours; the rebuild uses AWS76.
- All mm ±15%.

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the body centre. +X right, +Y forward, +Z up, mm.
- Body x ∈ [−37, +37], y ∈ [−42, +42], z ∈ [1.5, 32].
- Wheels to x ±50; guards to x ±52; skids to y +50.

## 10. Profiles as math

**10.1 Body side profile (YZ).** Polygon: (−42, 1.5) → (−42, 32) → (+8, 32) → (+42, 1.5)... front slope line z = 32 − 0.897·(y − 8) for y ∈ [8, 42], angle atan(30.5/34) = 41.9°.

**10.2 Lifter plate.** In-plane outline (u along X, v up the slope from the PC lip edge): PC sheet u ∈ [−23, 23], v ∈ [0, 58]; printed backing v ∈ [9, 58]. Pose: (x = u, y = 48 − v·cos 40°, z = 0.5 + v·sin 40°).

**10.3 Skid side profile (YZ at x = ±37).** Polygon: (+5, 0) → (+50, 0) → (+50, 3) → (+12, 14) → arc r 4 centred (+8, 10) back to (+5, 10) → close. Top line: z = 3 + 0.289·(50 − y) for y ∈ [12, 50] (16° ramp).

**10.4 Guard plate GP (YZ, at x = ±52).** Hexagon: (−36, 11) → (−29, 4) → (−5, 4) → (+2, 11) → (+2, 19) → (−5, 26) → (−29, 26) → (−36, 19) → close. Holes Ø 2.7 at (−24, 17) [AXS], (−1, 20), (+6… clipped to −1), (−1, 10)… use (−2, 20), (−2, 10), (−8, 22).

**10.5 Wheel.** Root r 15, tip r 17, 38 square teeth: r(φ) = 15 + 2·[sin(38φ) > 0]; width 12; hub recess r 6, depth 2.

**10.6 Lifter rotation.** Pivot P = (y −2, z 26). Lip edge E₀ = (48, 0.5). R = √(50² + 25.5²) = 56.1. Edge height z_E(θ) = 26 − R·sin(27° − θ) for rotation θ upward; at θ = 45°, z_E = 26 + 56.1·sin 18° = 43.

## 11. Pixel measurements

- **AWS76**: wheel 225 px wide × 265 tall (Ø ≈ 265 px at the near rear corner); plate width along its top edge from (335, 150) to (735, 320) ≈ 435 px; body top from front-left (330, 90) to rear-right (1095, 185) ≈ 770 px diagonal; skid length ≈ 330 px (near skid) and 300 px (far).
- **AWS72**: wheel ≈ 130 × 170 px; plate width along its bottom edge ≈ 560 px; rear lid width ≈ 720 px.
- **AWS63**: plate 440 px; total body width (side wedge outer edges) 680 px; total incl. guards 780 px; wheel visible height 150 px.

## 12. Several independent estimates

| Quantity | Method A (rule/typical) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width (incl. wheels/guards) | ≤ 101.6 → ~100 | — | AWS63: 780 px; plate 440 px → plate = 0.56 of overall | **100** |
| Plate width | 0.62 × 100 (json width_frac) = 62?? | 0.62 W(body) = 46 | AWS63: 0.56 × 100 = 56 | **46 printed + PC; 56–62 incl. side cheeks** (see 13.1) |
| Body width | 100 − 2 × 13 = 74 | — | AWS63: side-wedge outer edges 680/780 × 100 = 87 (includes cheeks) | **74** |
| Wheel Ø | 30–35 | 0.46 W = 34 | AWS76: 265 px vs plate 435 px / 46 mm → 9.5 px/mm → 28 (rear is farther: ×1.2) = 34 | **34** |
| Body height | 30–35 | 0.43 W = 32 | AWS63: plate height (front) 380 px projected… n/a | **32** |
| Skid length | 40–45 | 0.6 W | AWS76: 330 px / 9.5 = 35 (oblique foreshortening ×1.3 → 45) | **45** |
| Guard length | 35–40 | — | AWS76: 290 px / 9.5 / cos(40°)… ≈ 38 | **38** |

## 13. Consistency check

1. **width_frac 0.62**: the json fraction most likely compares the **lifter plate including its frame cheeks (≈ 58–62 mm)** to the robot width with wheels (≈ 100). The visible art area is 46 mm; with 6–8 mm ribbed cheeks each side the lifter frame is 58–62. **Reconciled: art plate 46, frame 60, body 74.**
2. **Plate/skids vs body**: frame 60 + 2 × 12 skid = 84 > 74; the skids are slightly **outboard** of the walls (AWS76 shows them stepping out), and the cheeks overlap the skids' inner region. **Reconciled: skids x ±31…±43.**
3. **Box limit**: length 84 + skid overhang 8 = 92 < 101.6; width 100–104 incl. guards: borderline; **guard outer face at x ±51** → 102. Take wheels 11 mm wide, guards at ±50.5 → 101. OK.
4. **Invertibility**: wheel top only 2 mm above the top; inverted driving is marginal — the lifter (pushing on the floor) or rolling onto the sloped front is the self-righting plan **(guess)**.

---

## 14. Why the designer did it (adversarial first)

- **Front plate as the lifter, with a PC lip**: the clear PC lip is a thin, flexible edge that **hugs the floor** better than any printed edge, so Ant Ratchet **gets under** opponents first; once under, the servo lifts the front of the opponent, taking its wheels off the floor. PC is tough (it does not shatter like acrylic) so it survives spinner hits, and it is **sacrificial and cheap to replace**. The steep 40° slope also deflects vertical spinner hits upward.
- **Art under PC**: theme (Ratchet & Clank pun on "Ant"), and the PC face protects the print.
- **Pivot at the side walls, near the top**: a high, rear pivot makes the plate's edge rise and come back toward the robot, pulling the opponent on; mounting the pivot through both side walls spreads the load into the strongest parts of the body.
- **Black corner skids**: they fill the corners beside the narrower lifter, so an opponent arriving at an angle meets a ramp rather than a vertical corner; their toes are ahead of the plate so they meet opponents first at the corners and guide them toward the centre. A softer black material (TPU-like) absorbs hits and does not chip. Weak point: their 3 mm blunt toes are worse at getting under than the PC lip.
- **Rear wheels with clear guards**: wheels at the rear keep the front free for the lifter and put traction where the weight is when the front is loaded by an opponent. The **clear guard plates** protect the wheels' lower front quarter from **horizontal spinners and wedges sweeping along the side**, and double-support the wheel (axle screw), so a side hit does not bend the motor shaft. They are clear so they are light and do not hide the wheel. The red bracket in front of each wheel takes direct frontal hits that would otherwise land on the tread.
- **Coarse TPU gear tread**: grips well on the AWS arena floor and is printable in any colour; translucent pink matches the theme.
- **Flat top with flush screws**: gives opponents' wedges nothing to catch if they ride over; the slot is narrow.
- **Rectangular link hole on top**: the driver can arm the robot without lifting it; recessed so it cannot be knocked out.
- **AWS72/AWS63 differences**: earlier versions used clear PC side wedges and lids everywhere (good impact resistance, but heavier and more screws). AWS76 simplified to a solid printed top and black skids.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Lifter servo | 9–12 g metal-gear micro servo, output along X | 23 × 12 × 25 | x −10, y −5, z 18, output shaft at the pivot axis (y −2, z 26) | medium |
| Lifter frame | U-frame: plate + two side cheeks 2 mm thick running back inside the walls to PV | 60 × 40 × 26 | — | medium |
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | x ±22, y −24, z 17 | high |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 9 | x +5, y −28, z 8 (rear centre) | medium |
| RX + ESC | combined board | 25 × 20 × 6 | under the top, y +5, z 10 | low |
| Power link | plug in SWH | 8 × 3.5 | (+12, −20, 30) | medium |
| Axle screws AXS | M3 screw into a hub boss on the wheel | — | wheel centre | medium |
| Wiring | battery → link → ESC → motors at the rear; servo lead forward | — | — | medium |

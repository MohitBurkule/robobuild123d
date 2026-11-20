# Smashie Tip: full rebuild description from reference photos (two-robot cluster)

Smashie Tip is a **cluster of two small robots** that fight together inside the 150 g antweight limit: a **wide, shallow vertical-spinner** with an orange top ("Smashie", here called **bot S**) and a **sloped-top wedge with long front prongs** ("Tip", here called **bot T**). Every photo shows both side by side. The project spec draft models only bot S (one of two). Both are described here; **bot S first, then bot T**.

Source photos:
- `robots/smashie_tip/reference/smashie_1.aws73.webp` (896 × 433 px): AWS 73. Uncut, on a grey pit table between storage tubs, about 40° down. Bot S on the left seen from its **front-left**, with a **dark two-tooth disc** and a **white bearing block**; it rests on a loose **dark-blue plate** (a spare part / the cluster's base). Bot T on the right seen from its **front-right**, **purple** with a **black sloped top plate**, pink/peach wheels at the rear; a loose purple **fork part** lies in front of it.
- `...aws74.webp` (2149 × 913 px): AWS 74. Cut out onto white. Bot S (left) from the **front-left**, about 35° down (dark disc with a hook tooth, white bearing block, pink-anodised motor collar, "ON" sticker). Bot T (right) from the **front-left**, **blue/purple** with a **black top plate** tilted up at the rear.
- `...aws76.webp` (2421 × 998 px): AWS 76. Cut out. Bot T (left) now **painted in "Gulf" racing livery**: light blue with an orange stripe and a **"Gulf" roundel**, seen from the front, about 40° down. Bot S (right) from its **front**, about 25° down, with a **bright plain steel disc**, the white bearing block and an **"ON OFF" label**.

Facts come from the photos; inferences are marked **(guess)**. Sizes are **estimates in mm**. Scale anchors: AWS cluster rules (the robots together ≤ 150 g; each ≈ 70–80 g), the spec draft for bot S (body 55 × 42 × 18 with a ramp, wheels r 8 outboard, disc r 12 with 2 teeth, 1 fork 22 mm), and the photo ratios between the two bots (they are photographed at about the same distance in each image). Ratios are against **W_S = bot S body width (X) ≈ 62 mm** and **W_T = bot T body width ≈ 52 mm**.

---

## 0. Coordinate system and naming

- **One frame convention for both bots**: for each bot, **origin O** = floor point (z = 0) under the centre of that bot's main body footprint. **+X** = that bot's right, **+Y** = its forward, **+Z** = up. mm.
- **Bot S front** = the long side carrying the disc and the floor feet (the robot is **wider than it is long**: wheels at the two X-ends, axes along X). **Bot T front** = the end with the two long prongs.
- Bot S extents: body x ∈ [−31, +31], y ∈ [−17, +17], z ∈ [2, 20]; wheels to x = ±38; disc to y ≈ +19, z ≈ 31.
- Bot T extents: body x ∈ [−26, +26], y ∈ [−30, +20], z ∈ [0, 24 at the rear]; prongs to y ≈ +52.

| ID | Part |
|---|---|
| **Bot S** | |
| S-BD | blue/purple body tub (wide, shallow) |
| S-TP | orange top plate (with a notch for the disc and motor) |
| S-SLT | disc slot through the body's front centre |
| S-UG | blue U-shaped guard under the disc |
| S-FT-L, S-FT-R | blue floor feet / skid wedgelets at the front corners |
| S-RF | rear feet (inferred, matching pair) |
| S-DS | weapon disc (dark two-tooth at AWS73/74; plain bright steel at AWS76) |
| S-MT | brushless motor (black can with **pink-anodised collar**) |
| S-MB | blue motor bracket / housing (U-shape around the motor) |
| S-BB | white/translucent bearing block (triangular gusset with a hub insert) |
| S-HI | black hub insert in S-BB (two holes) |
| S-WH-L, S-WH-R | lavender/purple-grey treaded wheels at the X-ends |
| S-LBL | "ON OFF" label and switch slot on the top plate (right half) |
| S-SCR | silver Phillips screws on the top plate (7–8) |
| **Bot T** | |
| T-BD | body frame (purple at AWS73, blue at AWS74, light blue "Gulf" at AWS76) |
| T-SC-L, T-SC-R | side cheeks (low at the front, rising to rounded rear wheel housings) |
| T-TP | sloped top plate (black at AWS73/74, painted Gulf livery at AWS76) |
| T-XB | front cross-bar of the frame |
| T-PR-L, T-PR-R | two long front prongs |
| T-HK-L, T-HK-R | small curved hook tabs at the rear top |
| T-WH-L, T-WH-R | rear wheels (peach/pink foam or TPU tyres) |
| T-LBL | "ON" label at the rear (AWS74) |
| T-INT | visible internals under the plate (red connector/servo, wires) |

---

## 1. Overall description in one paragraph

**Bot S** is a **flat, wide brick** about 62 mm wide, 34 mm deep and 18 mm tall: a **purple-blue printed tub** under an **orange top plate** held by small silver screws, with a **lavender treaded wheel** poking out of each end. In the middle of its long front side, a **slot** cuts through the body, and a **small vertical disc** (about Ø 26) spins in it on an axle along X, driven directly by a tiny **black outrunner with a pink anodised collar** that sits in a **blue U-bracket** on the right of the slot; on the left of the slot a **white translucent bearing block** shaped like a triangular gusset carries the axle's other end. Below the slot, a **blue U-shaped guard** loops around the bottom of the disc, and two **little blue feet** at the front corners skid on the floor. A label "ON OFF" marks the switch. **Bot T** is a **sloped wedge**: two side cheeks, low at the front and rising to rounded wheel housings at the rear, joined by a **front cross-bar** from which **two long flat prongs** run forward to the floor; a **rectangular top plate** sits in the frame sloping up from the front cross-bar to the rear; two small **hook tabs** stick up at the rear top; the **rear wheels** have peach-coloured tyres. At AWS76 bot T is painted in the **Gulf** racing colours (light blue, orange stripe, "Gulf" roundel).

---

## 2. Bot S: part-by-part description

### 2.1 Body tub (S-BD)
- **Shape**: a rectangular box, **62 mm wide (X) × 34 mm deep (Y) × 16 mm tall** (z 2 to 18), open on top (closed by S-TP). Its long front face (y = +17) carries the slot and the feet. The bottom front edge has small **notches** where the feet attach.
- **End pockets**: at each X-end the body is notched at the top front/back so the wheel can sit **partly inside** the end: the top plate's outline steps in around the wheel (AWS74, AWS76: the orange plate has a rectangular notch at each end where the tyre shows).
- **Colour/material**: **purple-blue PLA** (AWS73 more violet, AWS74/76 deep blue), rough layer lines, white scuffs and a dark scorched/scraped area at the right end (AWS76).

### 2.2 Top plate (S-TP)
- **Shape**: a flat **orange plate, 2 mm thick**, covering the whole top, about **62 × 34 mm**, with:
  - a **notch at each end** (about 8 × 14 mm) around the wheel's top;
  - a **central notch** at the front, about **24 mm wide × 18 mm deep**, around the disc, motor and bearing block;
  - a step in its front edge on the right half (AWS76: the right half's front edge is set back about 3 mm, following the motor bracket).
- **Screws S-SCR**: **7–8 small silver Phillips pan screws** (head Ø 3.5 mm, M2): at the four outer corners, two near the centre notch, one on the bearing block foot, one on the motor bracket (AWS74 shows eight).
- **Label S-LBL**: a white sticker **"ON OFF"** (about 12 × 6 mm) on the right half near the rear edge, with a **slot** below it (about 6 × 2 mm) for the slide switch (AWS76). AWS74 shows only "ON" visible.
- **Material**: orange PLA with visible diagonal infill on top.

### 2.3 Disc slot (S-SLT) and U-guard (S-UG)
- **Slot**: a gap **about 5 mm wide** (X) through the front of the body at x ≈ −2, from the front face back about 18 mm, the full body height, so the disc's lower half passes down through the body.
- **U-guard**: a **blue printed U-loop** below the front of the slot: two short legs (about 5 × 5 mm) either side of the slot's bottom and a bottom bar about **14 mm long (Y) × 4 mm**, forming a rectangular hoop around the bottom of the disc at floor level (AWS76: the white gap inside the U shows the floor; AWS74: same). The disc's bottom edge passes about **2 mm above** the U's bottom bar.
- **Function**: protects the disc from the floor and from being pushed down, and acts as a **centre skid** ahead of the disc **(design reading)**.

### 2.4 Weapon disc (S-DS)
- **AWS73/74**: a **dark (brown/black oxide) steel disc**, **Ø 26 mm, 3 mm thick**, with **two teeth** (spec: 2 teeth): AWS74 shows a **hooked tooth** at the bottom (a step in the rim about 3 mm deep). A dark hub boss.
- **AWS76**: a **bright plain steel disc**, about **Ø 26 × 3 mm**, round with no visible teeth (the rim catches light all round).
- **Position**: centred at **x ≈ −2, y ≈ +6, z ≈ 18** (the axle at the top-plate level), so its top reaches about **z 31** above the plate and its bottom **z 5** inside the U-guard; its front reaches **y ≈ +19**, about 2 mm proud of the front face.

### 2.5 Motor (S-MT) and motor bracket (S-MB)
- **S-MT**: a tiny **brushless outrunner**, **black can Ø 12 × 10 mm** with a **pink/magenta anodised shaft collar / prop adapter** (Ø 8 × 6 mm) between it and the disc (AWS74, AWS76). A 1104–1105 class motor **(guess)**.
- **S-MB**: a **blue printed U-bracket** around the motor, about **16 mm wide (X) × 14 mm deep × 14 mm tall above the plate**, open at the top and toward the disc, screwed down through the top plate (one silver screw at its outer front corner, AWS76). It holds the motor stator; its outer wall is on the right (x ≈ +16).
- **Arrangement**: from the slot outward on the right: disc → pink collar → black can → bracket wall.

### 2.6 Bearing block (S-BB) and hub insert (S-HI)
- **Shape**: a **white/translucent printed (or nylon) part** on the left of the disc: a **right-triangle gusset** in side view (YZ): a foot on the top plate about **14 mm long**, a vertical edge about **14 mm tall** against the disc, and a sloped hypotenuse; about **5 mm thick (X)**. Its foot is screwed to the top plate (one silver screw, AWS74/76). At its top, against the disc, a round **boss** (Ø 10) holds the **black hub insert S-HI** with **two small holes** (AWS74: a black disc with two holes, about Ø 8), a bearing or a bushing for the axle **(guess)**.
- **Function**: the **outboard axle support**: the motor shaft passes through the disc into this block, so the disc is supported on both sides.

### 2.7 Feet (S-FT, S-RF)
- **Front feet S-FT-L/R**: **small blue sloped feet** at the front corners, each about **6 mm wide × 8 mm long × 5 mm tall**, sloping down and forward from the body's bottom front edge to the floor (like tiny wedges/skids). AWS74 shows them at both front corners; AWS76 shows them at the front left and front right.
- **Rear feet S-RF**: AWS74 shows a matching foot at the far rear-right corner **(so probably four feet, guess)**.
- **Function**: the robot rests on its two wheels and these skids; the feet keep the body's flat bottom (and the disc) off the floor and act as tiny wedges against opponents.

### 2.8 Wheels (S-WH)
- **Shape**: **Ø 18 × 8 mm**, **lavender/grey-purple treaded tyres** (coarse transverse ribs, about 24 ribs) on matching hubs; AWS73 shows a lighter hub with a small round cap.
- **Position**: at the X-ends, centres **x = ±33, y ≈ −2, z = 9**, partly inside the end notches; the tops stick about 1–2 mm above the top plate (z 18–20).
- **Drive**: each on an N10/N20-class micro gearmotor along X inside the body **(guess)**.

---

## 3. Bot T: part-by-part description

### 3.1 Frame (T-BD), side cheeks (T-SC) and cross-bar (T-XB)
- **Side cheeks**: two printed side plates about **5 mm thick**, each a **long tapered profile**: at the front (y ≈ +20) about 4 mm tall, rising along a straight top edge at about **20–25°** to the rear, where the cheek ends in a **rounded wheel housing** (a semicircle of radius about 12 around the wheel axle) about **24 mm tall** at y ≈ −22. The cheek has a **circular hole** at the wheel axle (AWS76, AWS74: an open round hole in the rounded rear end) and **one silver screw** near its front (AWS74: (1280, 510)).
- **Cross-bar T-XB**: a **flat bar about 52 mm wide × 8 mm deep × 3 mm thick** joining the cheeks at the front (y ≈ +16), lying almost on the floor; the top plate's front edge rests on or just behind it.
- **Rear**: the cheeks are joined at the rear by the wheel axle and a rear bar under the plate **(guess)**.
- **Colours**: purple (AWS73), blue/violet (AWS74), **light blue painted with an orange stripe** (AWS76, the paint chipped along all edges showing the base colour).

### 3.2 Prongs (T-PR)
- **Shape**: two flat **prongs**, each about **12 mm wide × 3 mm thick × 36 mm long**, continuing the cheeks' lower front forward from the cross-bar to the floor, angled slightly down (about 5°), at x ≈ ±20. The tips are cut **square** (AWS74) or **chamfered** on the outer corner (AWS76). In plan the inner edges are straight and parallel, with the cross-bar forming a "U" between them.
- **Spare**: AWS73 shows a loose purple **prong/fork part** lying in front of bot T (a replacement prong or a different nose part).

### 3.3 Top plate (T-TP)
- **Shape**: a **flat rectangular plate**, about **36 mm wide × 58 mm long × 3 mm thick**, sitting between the cheeks, with its **front edge low** at the cross-bar (y ≈ +14, z ≈ 4) and its **rear edge high** (y ≈ −30, z ≈ 34), i.e. sloping at about **40°**, steeper than the cheeks' top edges, so its rear end stands **above** the cheeks and the wheels. Its edge has a raised border (the print's perimeter, AWS74/76).
- **Colours**: **matt black** (AWS73/74); at AWS76 **painted Gulf livery**: light blue with a **vertical orange stripe** (about 8 mm wide, black-outlined) running its full length and a **round orange/white "Gulf" roundel** (Ø about 22 mm) with the word "Gulf" hand-painted in dark blue.
- **Function (two readings)**: (a) a **fixed sloped lid** making the robot a wedge with a ramp that lifts opponents who climb the prongs; (b) a **servo flipper/"tipper"** hinged at its front edge, shown raised **(guess)**: it is raised in all three photos, which favours (a) a fixed rest angle, or a lid simply resting on the internals. **Reconciled: fixed sloped top (medium-low confidence)**.

### 3.4 Hook tabs (T-HK)
- **Shape**: two small **curved hook-shaped tabs**, about **3 mm thick × 12 mm long × 8 mm tall**, rising at the rear top of each cheek beside the plate's rear corners and curling backward (AWS76: orange-tipped curls at the left rear and right rear; AWS74: one at the right rear).
- **Function (guess)**: **self-righting / anti-turtle hooks** or simply guides that stop the plate sliding back; they also make the robot rest tilted if flipped.

### 3.5 Rear wheels (T-WH)
- **Shape**: **Ø 22 × 8 mm**, **peach/pink foam or soft TPU tyres** (AWS73 shows pink tyres with purple hubs; AWS74 a peach tyre with a pale hub; AWS76 a tan tyre).
- **Position**: at the rear, inside the rounded cheek ends, centres **x = ±21, y = −22, z = 11**. AWS74 shows the tyre **between** the cheek and the plate (inboard of the cheek), with the cheek's round end covering it on the outside. **Reconciled: inboard of the cheeks**, tops at z 22.
- **Drive**: 2WD rear; the prongs/cross-bar skid at the front.

### 3.6 Internals (T-INT) and labels
- Under the raised plate: a **red part** (a servo body or a red connector, about 10 × 6 mm) and wiring (AWS74, AWS76), a green PCB edge (AWS73).
- AWS74 shows a white **"ON"** label on the rear top near the left wheel.

---

## 4. Per-view descriptions

### 4.1 Bot S, front view (AWS76)
- A long low rectangle (62 × 18): blue tub with the orange plate on top, a wheel at each end. In the middle, the disc edge-on in its slot, rising about 13 mm above the plate; to its right the pink collar, black can and blue bracket; to its left the white gusset block. Below the slot, the blue U-hoop on the floor; at the corners, the two little feet.

### 4.2 Bot S, top view (AWS74 approx.)
- A 62 × 34 orange rectangle with end notches (tyres showing) and a front-centre notch holding the 3 mm disc line, the motor (Ø 12) and bracket on the right, and the white block on the left. Screws at the corners; "ON OFF" at the rear right.

### 4.3 Bot S, side view (inferred)
- A 34 × 18 rectangle with the wheel (Ø 18) at the centre, the disc's top arc peeking above the plate at the front, the feet sloping down at the front bottom.

### 4.4 Bot T, front view (AWS76)
- Two prongs on the floor leading back to a low cross-bar; behind it, the top plate rising steeply away (the Gulf roundel facing the camera); the side cheeks rising to rounded rear ends with the wheels; the hook tabs at the top rear corners.

### 4.5 Bot T, side view (AWS73/74)
- A long wedge: a cheek profile rising from the prong tip at the floor to a rounded rear end 24 mm tall, with the plate's rear edge sticking up to about 34 mm.

### 4.6 Rear views (inferred)
- Bot S: the plain rear long side, 62 × 18, wheels at the ends, the switch slot on top.
- Bot T: the two rounded cheek ends with the wheels between them and the plate's rear edge above.

---

## 5. Part tables

### 5.1 Bot S

| ID | Shape | Size (mm, est.) | Ratio to W_S | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| S-BD | box | 62 × 34 × 16 | 1 × 0.55 × 0.26 | purple-blue PLA | — | 1 |
| S-TP | notched plate | 62 × 34 × 2 | 1 × 0.55 | orange PLA | 7–8 × M2 | 1 |
| S-SLT | slot | 5 × 18 | — | — | — | 1 |
| S-UG | U-hoop | 14 × 5 × 8 | 0.23 | blue PLA | integral | 1 |
| S-DS | disc | Ø 26 × 3 | 0.42 | dark steel (AWS73/74), bright steel (AWS76) | on motor shaft | 1 |
| S-MT | outrunner | Ø 12 × 10 (+ collar Ø 8 × 6) | 0.19 | black + pink | in S-MB | 1 |
| S-MB | U-bracket | 16 × 14 × 14 | 0.26 | blue PLA | 1–2 screws | 1 |
| S-BB | gusset block | 14 × 14 × 5 | 0.23 | white translucent | 1 screw | 1 |
| S-HI | hub insert | Ø 8 | — | black | press | 1 |
| S-FT | foot | 6 × 8 × 5 | 0.1 | blue PLA | integral | 2–4 |
| S-WH | wheel | Ø 18 × 8 | 0.29 | lavender TPU | motor shaft | 2 |

### 5.2 Bot T

| ID | Shape | Size (mm, est.) | Ratio to W_T | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| T-SC | tapered cheek | 50 × 24 × 5 | 0.96 × 0.46 | purple/blue/Gulf blue | screws to bars | 2 |
| T-XB | flat bar | 52 × 8 × 3 | 1 × 0.15 | same | integral | 1 |
| T-PR | flat prong | 36 × 12 × 3 | 0.69 × 0.23 | same | integral | 2 |
| T-TP | rectangle plate | 36 × 58 × 3 | 0.69 × 1.12 | black / painted Gulf | resting/hinged | 1 |
| T-HK | hook tab | 12 × 8 × 3 | 0.23 | same (orange tips at AWS76) | integral | 2 |
| T-WH | wheel | Ø 22 × 8 | 0.42 | peach/pink tyre | motor shaft | 2 |

---

## 6. Contact / gap matrices (est. mm)

### 6.1 Bot S

| A ↔ B | Relation | Gap |
|---|---|---|
| S-BD bottom ↔ floor | clearance | 2 |
| S-WH bottom ↔ floor | contact | 0 |
| S-FT tips ↔ floor | contact (skid) | 0 |
| S-UG bottom ↔ floor | touching / 0.5 | 0–0.5 |
| S-DS bottom ↔ S-UG bar | clearance | 2 |
| S-DS faces ↔ slot walls | clearance | 1 each side |
| S-DS ↔ pink collar | fixed | 0 |
| S-MT ↔ S-MB | clamped | 0 |
| S-DS ↔ S-BB hub | running | 0.5 |
| S-BB foot ↔ S-TP | screwed | 0 |
| S-TP ↔ S-BD | screwed | 0 |
| S-WH ↔ end notch walls | clearance | 1–2 |
| S-WH top ↔ S-TP | above | +1 |

### 6.2 Bot T

| A ↔ B | Relation | Gap |
|---|---|---|
| T-PR tips ↔ floor | contact | 0 |
| T-XB bottom ↔ floor | clearance | 1 |
| T-WH bottom ↔ floor | contact | 0 |
| T-WH outer face ↔ T-SC inner face | clearance | 1–2 |
| T-TP front edge ↔ T-XB | resting / hinged | 0 |
| T-TP side edges ↔ T-SC inner faces | clearance | 1–2 |
| T-TP rear edge ↔ T-WH top | above | +12 |
| T-HK ↔ T-SC | integral | 0 |

---

## 7. Mechanism

1. **Bot S drive**: two wheels at the X-ends, skid steer about the robot's centre; the feet and U-guard skid. The robot is short in Y, so it spins on the spot very quickly.
2. **Bot S weapon**: direct-drive micro outrunner; the disc is mounted on the motor shaft (via the pink adapter) and supported at its far side by the white block. With a 1104-class motor at about 20,000 rpm and a Ø 26 disc, the tip speed is π·0.026·333 ≈ 27 m/s. Disc mass ≈ 7.85·π·1.3²·0.3 ≈ 12.5 g; I ≈ ½·0.0125·0.013² ≈ 1.06 × 10⁻⁶ kg·m²; E ≈ ½·I·(2094)² ≈ 2.3 J. It spins with the front edge moving **up** (uppercut) **(guess)**.
3. **Bot T**: a pusher/wedge: prongs get under opponents, the sloped plate ramps them up; possibly a servo raises the plate (not confirmed).
4. **Cluster tactics**: one bot pins/lifts (T), the other hits (S) **(design reading)**.

---

## 8. Assembly order (suggested rebuild)

**Bot S**: 1) print the tub with slot, U-guard and feet; 2) fit the two drive micro-motors and wheels at the ends; 3) fit battery, ESCs, receiver and switch (switch under the "ON OFF" slot); 4) screw on the orange top plate; 5) screw the blue motor bracket and fit the outrunner; 6) fit the disc on the pink adapter; 7) screw down the white bearing block with the hub insert on the shaft end.

**Bot T**: 1) print the frame (cheeks, cross-bar, prongs, hooks) in one piece; 2) fit the rear motors and wheels inside the cheeks' round ends; 3) fit electronics (and the servo if any) under the plate; 4) fit the top plate (hinge or rest on the cross-bar); 5) paint (Gulf livery, AWS76).

---

## 9. Hidden / uncertain list
- Bot S: disc teeth (two at AWS73/74; none visible at AWS76), motor size, bearing type, drive motors, rear feet.
- Bot T: whether the plate moves, internals, wheel drive.
- Cluster weight split.
- All sizes ±20% (small robots, no direct scale).

---

## 10. Coordinate frames (restated)
- Each bot: origin under its body centre, +X right, +Y forward, +Z up, mm.
- Bot S: body x ∈ [−31, 31], y ∈ [−17, 17], z ∈ [2, 18]; disc centre (−2, +6, 18), r 13; wheels (±33, −2, 9).
- Bot T: cheeks x ∈ [±21, ±26], y ∈ [−34, +20]; prongs to y = +52; plate from (y +14, z 4) to (y −30, z 34); wheels (±21, −22, 11).

## 11. Profiles as math

**11.1 Bot S top plate outline (XY).** Rectangle x ∈ [−31, 31], y ∈ [−17, 17] minus the end notches x ∈ [±23, ±31], y ∈ [−9, +5] and minus the centre notch x ∈ [−10, +14], y ∈ [−1, 17].

**11.2 Bot S U-guard (YZ at x = −2).** Outer rectangle y ∈ [+6, +20], z ∈ [0, 8] minus the inner rectangle y ∈ [+9, +17], z ∈ [3, 8]; extruded X ∈ [−6, +2].

**11.3 Bot S disc (AWS73/74, two teeth).** r(φ) = 13 − 3·frac(φ/π) (a ramp from r 13 down to 10 over each half-turn, then a radial step back to 13: two hook teeth 180° apart); AWS76: r = 13.

**11.4 Bot S bearing gusset (YZ, extruded X ∈ [−9, −4]).** Triangle (y −6, z 18), (y +8, z 18), (y +8, z 32) plus a boss circle r 5 centred on the axle at (y +6, z 18).

**11.5 Bot T cheek (YZ, extruded 5 mm).** Bottom z = 0 from y −22 to +20; top line from (+20, 4) to (−22, 22): z = 4 + 0.43·(20 − y) (23°); rear end: semicircle r 12 centred (−22, 12) from θ = 90° to 270°; axle hole r 4 at (−22, 11).

**11.6 Bot T plate (YZ).** Line from (y +14, z 4) to (y −30, z 34): z = 4 + 0.682·(14 − y) (34°), 3 mm thick below.

**11.7 Bot T prong (plan).** Rectangle x ∈ [±14, ±26], y ∈ [+16, +52], z 0–3, tip chamfer: cut the outer front corner by a 6 × 6 triangle.

## 12. Pixel-based measurements

**AWS76 (2421 × 998, coordinates in the 2000-wide display, × 1.21):**
- Bot S: body x 1115–1950, y 160–560; disc x 1500–1560, y 125–520; motor can (1555–1650, 190–310); pink collar (1630–1680, 220–290); bracket (1560–1690, 210–360); white block (1370–1470, 180–330); U-guard (1430–1570, 440–530); feet (1140–1200, 410–470) and (1840–1890, 500–560); wheels (1190–1260, 140–280) and (1870–1930, 200–330); label (1700–1810, 225–265).
- Bot T: plate x 240–720, y 50–540; prong tips (430–550, 690–760) and (930–1020, 520–560); hooks (180–310, 240–310) and (600–700, 150–190); wheel (100–200, 250–330).

**AWS74 (2149 × 913, display 2000 wide):** Bot S body x 50–930, y 250–800; disc (480–600, 300–800); bearing block (420–520, 400–580). Bot T plate (1260–1590, 40–500); prong tips (1440–1520, 640–710) and (1880–1950, 560–600); wheel (1080–1190, 190–300).

**AWS73 (896 × 433):** Bot S (20–400, 40–370) with disc (205–305, 115–230); bot T (430–870, 60–390), plate (570–800, 85–295).

## 13. Several independent estimates of key sizes

| Quantity | Method A (spec/rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Bot S width | 55 (spec) | wheels outboard: 55 + 2 × 8 = 71 overall | AWS76: body 835 px; disc 395 px tall (Ø 26 + exposure) → 26/395 × 835 ≈ 55 for the visible body, + end wheels | **62 body (wheel notches inside), 76 overall** |
| Bot S depth | 42 (spec) | 0.55 W_S = 34 | AWS74: depth ≈ 0.6 of the width in the oblique view | **34** |
| Bot S height | 18 (spec) | 0.29 W_S | AWS76: tub 220 px + plate 20 px vs width 835 → 0.29 × 62 = 18 | **18** |
| Disc Ø | 24 (r 12) | 0.42 W_S = 26 | AWS76: 395 px vs 835 px body → 0.47 × 55 = 26 | **26** |
| Wheel Ø (S) | 16 (r 8) | 0.29 W_S | AWS76: 140 px tall / (835/62) → 10?? (partly hidden in notches) | **18** |
| Bot T width | — | ≈ 0.85 of bot S's width in AWS74 | AWS76: frame 52 mm if prong spread ≈ 590 px at bot S's scale ~13 px/mm → 45 | **52** |
| Bot T length | — | — | AWS74: frame ≈ 1.2 × width | **54 frame + 32 prongs** |
| Fork length (spec) | 22 | — | — | spec "1 fork 22 mm" refers to bot S's U-guard/skid; bot T prongs **36** |

## 14. Consistency check: conflicts and reconciliation
1. **Bot S orientation**: the disc and feet are on a **long side**, so bot S is wider than long. The spec's 55 × 42 matches X × Y. **Reconciled: wheels at the X-ends, axes along X.**
2. **Disc teeth**: AWS74 shows a hook step (two teeth per the spec); AWS76 shows a round bright disc. Event variants. **Reconciled: model the 2-tooth version (11.3).**
3. **Wheel diameter**: spec Ø 16; the photos show the tyres reaching just above the 18 mm top. With the wheel centre at z 9, Ø 18 is the minimum. **Reconciled Ø 18.**
4. **Bot T plate**: raised at the rear in all photos, so it is the rest position. **Reconciled: fixed sloped top**, hinge optional.
5. **Weight**: two robots at 75 g each: bot S's steel disc (12.5 g) + motor (8 g) + 2 drive motors (2 × 10 g) + battery (15 g) + ESCs/receiver (10 g) + plastic (15 g) ≈ 80 g; plausible.

---

## 15. Why the designer did it (per part, adversarial first)

- **Cluster of two**
  - Fight: two robots split the opponent's attention: while the opponent deals with one, the other attacks from the side or rear. To win, the opponent must disable **both** (AWS cluster rules count each), so losing one does not end the fight. Each is small and light, so each is easily thrown, which is the cost.
- **Bot S: wide, short, wheels at the ends**
  - Fight: a short wheelbase in Y and a wide track gives a **very fast turn**, keeping the disc pointed at the opponent. The low height (18 mm) offers little to hit; the disc is the only thing that sticks up.
  - Threats: the long flat sides are easy targets for wedges; the feet and U-guard keep the front low so wedges must get under 1–2 mm skids.
- **Disc in a slot with a U-guard**
  - Fight: the slot shields the disc's sides; the U-guard stops the disc digging into the floor or being jammed down by a wedge, and gives a contact point exactly where the disc strikes upward.
  - Survival: the disc is small (low energy, about 2 J), so it relies on chipping/flicking light opponents; it cannot destroy big robots but can catch wheels and edges.
- **White bearing block + blue motor bracket**
  - Fight: supporting the disc on both sides stops it being bent sideways by impacts; the white (nylon/PETG) block flexes rather than cracking.
  - Construction: both are separate screwed parts, replaceable between fights.
- **Orange top plate**
  - Construction: a single screwed plate gives access to all internals; the notches let the wheels and weapon sit low.
- **Bot T: sloped wedge with long prongs**
  - Fight: the prongs are the first thing to touch an opponent, getting under it; the sloped plate then ramps it up, taking its wheels off the floor so bot S can hit its underside, or so bot T can push it into a hazard. The rounded rear cheeks let it roll back onto its wheels if tipped backward.
  - Threats: the prongs are printed and can snap (AWS73 shows a spare prong part); the open frame between the cheeks exposes the internals under the plate edges.
- **Hook tabs**
  - Fight (guess): they hold the plate in place and give bot T a point to rest on so it can rock back over when flipped.
- **Gulf livery**
  - Identity: a racing-car paint job (Gulf blue/orange); cosmetic.

## 16. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| S drive motors | 2 × N10/N20 micro gearmotors along X | 10 × 12 × 24 | x ±20, y −2, z 9 | medium |
| S weapon motor | 1104–1105 outrunner, 4000–7000 kV | Ø 12 × 10 | x +8, y +6, z 18 | high (seen) |
| S weapon ESC | 6–12 A micro ESC | 20 × 10 × 4 | left half, x −18, y −8, z 8 | medium |
| S drive ESC | dual brushed micro ESC | 18 × 12 × 4 | right half, x +18, y −8, z 6 | medium |
| S battery | 2S 150–200 mAh LiPo | 35 × 15 × 9 | across the rear, x 0, y −10, z 8 | medium |
| S receiver | micro receiver | 15 × 10 × 4 | x −18, y +6, z 8 | low |
| S switch | slide switch under the "ON OFF" slot | 8 × 4 × 4 | (+16, −12, 16) | high |
| T drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | x ±10, y −22, z 11 | medium |
| T electronics | 2S battery, dual ESC, receiver (red connector seen) | — | under the plate | medium |
| T servo (if plate moves) | 5–9 g servo | 20 × 10 × 20 | under the plate front | low |

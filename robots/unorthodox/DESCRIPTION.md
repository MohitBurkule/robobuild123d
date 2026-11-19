# Unorthodox: full rebuild description from reference photos

Source photos:
- `robots/unorthodox/reference/unorthodox.aws74.webp` (1786 × 1178 px, cut out onto white). AWS 74. Seen from the **front-left three-quarter, about 30° down**. Dark green body, **wide green-tinted wedge**, a **Savox SB-2272MG brushless servo** lying in a raised central housing, a **"SAVOX" logo** on the front wall, and **two orange/tan mottled rear top plates**, the left one with a **switch slot** and on/off marks, plus a tan **rear-left corner plate**.
- `robots/unorthodox/reference/unorthodox.aws76.webp` (1831 × 1152 px, cut out onto white). AWS 76. Seen from the **front-right three-quarter, about 30° down**. All dark green. It shows the servo's **right side with a purple anodised aluminium horn/arm** (2 socket screws at the spline and a Phillips screw at its end), a **"RobotMad" yellow sticker**, the right rear top plate, the **right rear corner skid**, and an open pocket left of the servo with a **blue part** inside.
- `robots/unorthodox/reference/unorthodox.aws61.webp` (751 × 1050 px, pit photo, older version). AWS 61. An **orange** tub with **foil/brass-tape panels**, two **silver wheels/motors** visible inside, and a **tall black servo-driven arm** carrying a **long steel angle blade** (an axe/hammer head), held up near vertical. This is an earlier form of the same robot.

Everything stated as fact is read from these photos. Inferences are **(guess)**. Dimensions are **estimates**. Scale anchors: AWS 150 g / 101.6 mm cube; the **Savox SB-2272MG** (a real standard-size brushless servo: **40.3 × 20.2 × 37.2 mm** plus mounting tabs to 54 mm, about 62 g); the purple **aluminium servo arm** (25T spline). Reference width **W = wedge width ≈ 100 mm**.

**Note on the weapon**: in AWS74 and AWS76 the servo carries only a short purple arm; no long weapon is fitted. AWS61 shows the earlier long **axe/hammer arm**. The AWS74/76 machine is therefore described as a **servo-weapon wedge** whose arm is either removed for the photo or is the short purple arm itself (a **servo "flipper/grabber" stub**) **(uncertain)**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the centre of the body footprint (excluding the wedge).
- **+X** = robot's right, **+Y** = forward (toward the wedge), **+Z** = up; mm.
- Envelope (AWS74/76): x ∈ [−50, +50], y ∈ [−40, +58], z ∈ [0, 36].

| ID | Part |
|---|---|
| BD | dark green printed body (tub) |
| FW | body front wall (with "SAVOX" logo) |
| WG | front wedge plate (green-tinted, wide) |
| WGE | wedge leading-edge strip |
| SH | raised central servo housing |
| SV | Savox SB-2272MG brushless servo |
| SVC | servo clamp bridge(s) |
| HA | purple aluminium servo arm |
| S-HA | 2 socket screws (spline clamp) + 1 Phillips (arm end) |
| PK-L / PK-R | open pockets left/right of the servo (wheel wells, guess) |
| WH-L / WH-R | internal drive wheels (blue, seen in the pockets) |
| M-L / M-R | drive motors (hidden) |
| MM | plastic motor mounts (hidden) |
| RP-L / RP-R | rear top plates (tan mottled AWS74, green AWS76) |
| RC-L / RC-R | rear corner skids / plates |
| SW | switch slot in RP-L |
| S-RP | screws on the rear plates |
| STK | "RobotMad" sticker |
| AX61 | AWS61 axe arm + steel angle blade |
| BAT, ESC, RX | hidden electronics |

---

## 1. Overall description in one paragraph

Unorthodox (AWS74/76) is a **low, wide, wheel-less-looking wedge** built round a **big brushless servo**. The **dark green printed body** is about **88 mm wide and 70 mm long**, and only about **22 mm tall**, with a **raised central housing** in which a **Savox SB-2272MG servo** lies on its side, its gold label facing up, its output spline pointing to the robot's right. The whole front is a **wide, shallow wedge plate**, about **100 mm wide**, sloping from the front wall down to a **thin green leading edge** on the floor, scuffed white along its length. The front wall carries an embossed **"SAVOX" logo** with an orange "S". Behind, the body steps down to **two flat rear top plates** at the corners (tan/orange mottled at AWS74, with a switch slot and on/off marks), and **angled corner skids** fold down at the rear corners. **No wheels are visible from outside**: two **blue drive wheels** are glimpsed inside **pockets either side of the servo**, so the wheels run **inside the body** and the robot looks like a sled. On the servo's right side is a short **purple aluminium servo arm**, the mounting point of the weapon. At AWS61 the robot (orange) carried a tall **servo-driven axe** with a long steel angle blade.

---

## 2. Part-by-part description

### 2.1 Body (BD) and front wall (FW)
- **Shape**: a low tub, **88 mm wide × 70 mm long × 22 mm tall** (z 2–24), y ∈ [−40, +30], with **vertical side walls** and a **chamfered rear** (the rear corners are cut at 45° by the corner skids, see 2.7).
- **Front wall FW**: a vertical face about **60 mm wide × 22 mm tall** at y ≈ +30 in the centre (behind the wedge's upper edge), stepping out to full width at the wedge root. The **"SAVOX" logo** is embossed on it (about 45 mm long × 9 mm tall letters; "S" filled orange in AWS74, plain in AWS76).
- **Side walls**: plain dark green, about **22 mm** tall, with vertical layer lines. The right wall (AWS76) has a **vertical step** at y ≈ −8 where a **rear corner plate** (RC-R) begins.
- **Material/colour**: dark green PLA/PETG, matt.

### 2.2 Servo housing (SH) and clamps (SVC)
- **Shape**: a **raised rectangular collar** on the body centreline, about **46 mm wide (X) × 52 mm long (Y)**, standing about **12 mm above the body top** (top at z ≈ 36). It is open on top over the servo, with **walls about 3 mm thick**.
- **Open pocket in front of the servo** (AWS76): the housing's **front-left part is an empty rectangular pocket** about **20 × 16 mm** (the area ahead of the servo body), with a **blue** object visible at its bottom (a wheel or motor) **(guess: wheel)**.
- **SVC**: **printed bridges** across the servo: a **front bridge** at the servo's front end (AWS74: a dark block across the servo's left-front, with a **notch/slot**) and **two socket-head screws** (M3, silver, head Ø ≈ 5.5) on the right-front corner of the housing (AWS74 at (640, 160)), which clamp the servo's tabs.

### 2.3 Servo (SV)
- **Savox SB-2272MG "Brushless"**, **black case with a gold label** reading "SAVÖX", "Brushless", "SB-2272MG". Lying on its **broad side** (label up): **40 mm long (Y) × 37 mm across (X) × 20 mm tall (Z)**, its top at z ≈ 36 (flush with the housing walls). Its **output spline is on the right**, axis along **+X** at about **(y +6, z 26)** **(guess from the arm position)**.
- **Mass**: about **62 g**, over 40 % of the robot's weight.

### 2.4 Purple servo arm (HA) and screws (S-HA)
- **Shape**: a **flat aluminium servo arm**, **purple anodised**, about **38 mm long × 9 mm wide × 3 mm thick**, with **rounded ends**. It sits on the servo's right side (outside the housing's right wall, which is cut down there), clamped on the spline by **2 small silver socket screws** (a clamp-type horn, at its inner end) and carries a **Phillips screw** with a nut at its outer end and a **spare hole** midway.
- **Pose (AWS76)**: it points **rearward, roughly horizontal**, lying along the top of the right rear plate. The Phillips screw at its end is where a **weapon arm or link** attaches **(guess)**.

### 2.5 Wedge (WG) and leading edge (WGE)
- **Shape**: a **wide flat plate**, **100 mm wide (X) × 34 mm long along the slope × 2 mm thick**, from the front wall bottom (y +30, z ≈ 12) down to the floor at **y ≈ +58**, a slope of about **20°**. It is wider than the body by about 6 mm each side; its side edges are straight and square.
- **Surface**: diagonal top-surface lines and **horizontal ridges** near the top (a stepped fillet where it meets the front wall, about 8 mm tall, with horizontal layer lines). The lower 60 % is **heavily scuffed white**, suggesting a harder or slicker material on the face.
- **WGE**: the **front 6–8 mm** is a slightly **lighter green, translucent strip**, separated by a fine line; it reads as a **thin FR4/G10 or polycarbonate insert** forming the sharp edge **(guess)**.
- **Fixing**: integral with the body front, or clamped by the edge insert. No screws visible on the wedge face.

### 2.6 Rear top plates (RP-L, RP-R), switch (SW), screws (S-RP)
- **Shape**: flat plates about **28 × 30 mm × 2 mm**, at the rear-left and rear-right, either side of the servo housing, on the body top at z ≈ 24.
- **AWS74**: both are **tan/orange with a mottled, marbled texture** (wood-fill PLA or a printed TPU look). The **left plate** has a **rectangular switch slot** (about 8 × 4 mm) with the slider visible, and hand-marked **"O"** and **"|"** symbols beside it (off/on). One **silver pan screw** (head Ø 4) at its rear-left corner and one at the front-right corner. The right plate has a screw at its rear-right corner.
- **AWS76**: the right plate is **dark green**, with the **"RobotMad" sticker** (yellow, with a pointed bottom, about 26 × 14 mm) and **2 screws** (front-left corner, rear-right corner).

### 2.7 Rear corner skids (RC-L, RC-R)
- **Shape**: at each rear corner, a **plate angled at about 45°** in plan and **sloping down and back** in side view: it starts at the rear plate's outer edge and descends to the floor behind and outside the body corner, about **28 mm wide × 30 mm long**. AWS74 shows the left one in the same **tan mottled** colour, a **separate plate** whose lower edge reaches the floor; AWS76 shows the right one in green, forming a **trapezoidal fin** at the rear-right corner.
- **Function**: rear skids/wedges that keep the rear corners low (so the robot always presents a slope) and act as **rear supports** in place of visible wheels.

### 2.8 Wheels (WH-L, WH-R) and pockets (PK), hidden
- **Seen**: blue parts inside the gaps next to the servo (AWS74 right of the servo front under the housing; AWS76 in the left pocket).
- **Guess**: **two blue TPU wheels, Ø ≈ 22 × 8 mm**, inside **slots in the floor** either side of the servo housing at **x ≈ ±28, y ≈ +8**, their bottoms 1–2 mm below the body floor. The robot rests on the wheels plus the wedge edge plus the rear skids. Being inside the body, the wheels are fully protected but the robot **cannot drive inverted** (and has no self-righting other than the weapon).
- **AWS61** shows **two silver drums** inside the orange tub, at the front-left and rear-right, possibly the wheels (aluminium hubs) **(low)**.

### 2.9 Drive motors and plastic motor mounts (hidden)
- **Guess**: **2 × N20 gearmotors** under the rear plates, along X, driving the internal wheels directly; held by **printed cradles** under the rear plates **(medium)**.

### 2.10 AWS61 version: axe (AX61)
- An **orange printed tub** about 60 × 110 mm with **foil (silver) and brass-coloured tape panels** on its top.
- A **black printed arm**, a tall A-frame/strut about 70 mm high, driven by a servo (an **orange horn** visible), carrying a **long steel angle blade**: an L-section strip about **100 mm long × 20 mm × 20 mm**, with a **ground, sharp edge** running along its length. The arm holds it raised in the photo; it would swing forward and down onto opponents (an **axe/hammer**).
- A **tail skid** sticks out at the rear-right; **red/black wires** lead off the robot (charging/testing).

---

## 3. Per-view descriptions

### 3.1 Top view
- A wide trapezoid (wedge 100 wide at the front), the body 88 wide behind it. In the middle, the raised servo housing (46 × 52) with the black servo and gold label. Two small rear plates at the corners with screws and the switch, and 45° skids at the rear corners. Purple arm on the servo's right side. Overall about **100 × 98 mm**.

### 3.2 Front view
- A wide thin wedge across the whole front, the front wall with "SAVOX" above it, the servo housing rising in the middle to z ≈ 36. No wheels visible.

### 3.3 Side views
- Left (AWS74): the wedge slope at the front, the 22 mm tall side wall, the housing above it, the tan rear plate and the down-sloping rear skid.
- Right (AWS76): the same with the purple arm on the servo side and the green rear fin.

### 3.4 Rear view (inferred)
- The two angled rear skids, the rear wall between them, the servo housing's rear wall above.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 100 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | low tub | 88 × 70 × 22 | 0.88 × 0.70 × 0.22 | dark green FDM | — | 1 |
| SH | collar | 46 × 52 × 12 | 0.46 × 0.52 | dark green | integral | 1 |
| SV | servo | 40 × 37 × 20 (54 with tabs) | 0.40 × 0.37 | black/gold | clamps + 2 × M3 | 1 |
| HA | servo arm | 38 × 9 × 3 | 0.38 | purple aluminium | spline clamp (2 screws) | 1 |
| WG | sloped plate | 100 × 34 × 2 | 1 × 0.34 | green | integral (guess) | 1 |
| WGE | edge strip | 100 × 7 × 1 | — | translucent green FR4/PC | bonded (guess) | 1 |
| RP | flat plate | 28 × 30 × 2 | 0.28 × 0.30 | tan mottled / green | 2 × M2.5 | 2 |
| RC | sloped corner plate | 28 × 30 × 2 | — | tan / green | to body (guess) | 2 |
| SW | slide switch | 8 × 4 slot | — | — | in RP-L | 1 |
| WH | internal wheel | Ø 22 × 8 | 0.22 | blue TPU | motor shaft | 2 (hidden) |
| STK | sticker | 26 × 14 | — | yellow/black | adhesive | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WG edge ↔ floor | touching | 0 |
| WG ↔ FW | joined (fillet) | 0 |
| SV ↔ SH walls | clamped | 0–0.5 |
| SV top ↔ SH top | flush | 0 |
| HA ↔ SV spline | clamped | 0 |
| HA inner face ↔ SH right wall | outside, close | 1–2 |
| HA ↔ RP-R top | above, lying along | 1–3 |
| RP ↔ BD top | screwed | 0 |
| RC lower edge ↔ floor | touching | 0 |
| RC ↔ RP outer edges | joined | 0 |
| WH bottom ↔ floor | touching | 0 |
| BD floor ↔ floor | above | 1–2 |
| WH ↔ pocket walls | clearance | 1–2 |

---

## 6. Mechanism
1. **Drive**: 2WD skid steer on **internal wheels**. The robot slides on its wedge edge and rear skids; the low floor clearance keeps the wedge edge in contact.
2. **Weapon**: the brushless servo turns the arm about X at the right side. With a long arm fitted (as at AWS61), it is an **overhead axe/hammer** or a **grabber** that swings forward over the wedge onto opponents. The SB-2272MG gives about **25 kg·cm**; at 7 cm that is about **3.5 kg** of force at the tip, enough to pin or lift a 150 g opponent, and fast (about 0.08 s/60°).
3. **Self-righting**: the arm can push the robot back over if it is flipped (the robot cannot drive inverted).

---

## 7. Assembly order (suggested rebuild)
1. Print **BD** with the servo housing, wedge, front wall logo, wheel pockets and motor cradles.
2. Fit the **drive motors** and the **internal wheels** in their pockets.
3. Install the battery, ESC, receiver and the **switch** (under RP-L).
4. Drop the **servo** into the housing, spline to the right; fit the **clamp bridge** and the 2 M3 screws.
5. Screw the **rear plates** and fit the **rear corner skids**.
6. Bond the **edge strip** to the wedge.
7. Clamp the **purple arm** onto the spline and attach the weapon arm/link to its end screw.
8. Apply the "RobotMad" sticker.

---

## 8. Hidden / uncertain list
- The weapon fitted at AWS74/76 (none visible beyond the purple arm).
- Wheel count, size, position (only glimpses of blue).
- Wedge edge material.
- Rear skid geometry and fixing.
- All dims ±15 %.

## 9. Coordinate frame (restated)
Origin on the floor under the body centre; +X right; +Y forward; +Z up; mm. Body x ∈ [−44, 44], y ∈ [−40, 30], z ∈ [2, 24]. Servo box x ∈ [−18.5, 18.5], y ∈ [−14, 26], z ∈ [16, 36]. Servo axis (y +6, z 26) along X. Wedge from y +30 to +58.

## 10. Profiles as math

**10.1 Wedge (YZ, constant over |x| ≤ 50).** Fillet at the front wall: arc centre (y 22, z 20), r = 8, from θ = −90°+20° … simplified: the face z = 12 − tan(20°)·(y − 30) for y ∈ [30, 58] → z(58) ≈ 1.8; edge strip from y = 51 to 58 thinned to a 0.5 mm edge: underside chamfer from (58, 0) to (51, 1).

**10.2 Servo housing (plan).** Rectangle |x| ≤ 23, y ∈ [−18, 34], wall 3, top z = 36. Front-left pocket: x ∈ [−20, 0], y ∈ [18, 34] open down to the floor slot.

**10.3 Rear corner skid.** A plane through the points (±44, −22, 24), (±30, −40, 24) (the top edge, at 45° in plan) and (±50, −46, 0) (the floor edge, offset 8 mm outward and back). Thickness 2.

**10.4 Purple arm.** Stadium of length 38 (centres 30 apart), width 9, thickness 3, in the YZ plane at x = +22, centred along the line from the spline (y 6, z 26) toward the rear (θ = 180° in the YZ plane).

## 11. Pixel-based measurements (AWS74 thumbnail 1200 px = native × 0.672; ±8 px)
- Wedge front edge: (250, 690) to (1100, 355) → ≈ 915 px.
- Servo label top face: ≈ 255 × 70 px; servo housing top: x ≈ 255–615.
- "SAVOX" logo: ≈ 210 px long.
- Rear-left plate: ≈ 330 px across its rear edge.
- Screw heads: ≈ 16 px.

## 12. Several independent estimates

| Quantity | Method A (servo 40 mm long → px/mm) | Method B (W = 100) | Method C (screw head 4 mm) | Reconciled |
|---|---|---|---|---|
| px/mm | label 255 px / 40 → 6.4 (label face is at the top and farther) | 915 / 100 = 9.2 (wedge edge is nearest) | 16 / 4 = 4 (far rear) | front ≈ 9, mid ≈ 7, rear ≈ 5 |
| Wedge width | 915 / 7 (mid scale) = 130?? | 100 | — | **100** (front-plane scale used) |
| Servo housing width | 360 / 6.4 = 56 (incl. walls, oblique) | 0.46 W | — | **46** |
| Logo length | 210 / 8 = 26 | — | — | **45**? → see §13 |
| Body height | front wall ≈ 160 px tall / 8 ≈ 20 | 0.22 W | — | **22** |

## 13. Consistency check
1. **Scale varies strongly** with depth in a 30° close-up; using the front-plane scale for front parts and the mid scale for the servo gives a consistent model: wedge 100, servo 40 × 37, body 88.
2. **Logo**: 210 px at about 8 px/mm is 26 mm; the "SAVOX" lettering on the front wall is therefore **about 30 mm** long × 7 mm tall, not 45. **Reconciled: 30 × 7.**
3. **Mass**: servo 62 g, body 30 g, rear plates/skids 6 g, 2 N20 + wheels 24 g, battery 12 g, ESC/RX 6 g, screws 3 g, arm 4 g: ≈ 147 g with no weapon head. A long axe arm (AWS61) would push it over 150 g unless the body is lightened. **Consistent with the photos showing no long arm** (or a very light one).
4. **Height**: 36 mm at the servo top; with a weapon arm upright the robot must still fit the 101.6 mm cube. **Consistent.**

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Huge brushless servo**: maximum torque and speed for a servo weapon; brushless servos survive repeated stalls and shocks better than brushed ones. It is the robot's main investment (over 40 % of the mass).
- **Raised housing around the servo**: shields the servo's sides from hits; the servo top is exposed but faces up, away from most attacks.
- **Wide, low wedge**: getting under is the robot's first job: a 100 mm wedge with a thin edge gets under most opponents, and then the servo weapon acts on them while they are on the wedge.
- **Edge strip**: a harder, thinner leading edge than printed plastic; replaceable.
- **Internal wheels**: nothing for a horizontal spinner or a wedge to hit at the sides. The body walls take every side hit. This is the "unorthodox" part: it trades invertibility for complete wheel protection.
- **Rear corner skids**: keep the rear low and sloped so opponents coming from behind meet a ramp; also stop the robot rocking back onto its rear edge when the weapon fires.
- **Rear plates with the switch**: the switch is at the back, away from the wedge and weapon, recessed in a plate.
- **Purple aluminium arm**: a metal clamp horn does not strip under shock the way plastic horns do.
- **AWS61 axe**: a long steel angle blade gives a heavy, rigid striking edge.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Drive wheels | 2 × blue TPU Ø 22 × 8 in floor slots | Ø 22 × 8 | (±28, +8, 11) | low-medium |
| Drive motors | 2 × N20 along X | 12 × 10 × 25 | (±28, −2, 11) behind the wheels? or coaxial | low |
| Battery | 2S LiPo 300 mAh (the servo needs current) | 45 × 18 × 10 | under the servo, (0, −20, 8) | medium |
| Drive ESC | dual brushed ESC | 20 × 15 × 4 | under RP-R | low |
| Receiver | micro rx | 18 × 12 × 4 | under RP-L | low |
| Switch | slide switch | 10 × 5 × 5 | under the RP-L slot (−30, −30, 20) | medium |
| Wedge edge | FR4 strip bonded into a slot | 100 × 7 × 1 | y 51–58 | low |
| Weapon arm | removed for the photos; mounts to the purple arm's end screw | — | — | low |
| Wiring | battery → switch → ESC & servo; servo lead direct to rx | — | — | medium |

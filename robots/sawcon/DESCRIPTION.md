# Sawcon: full rebuild description from reference photos

Source photos (in `robots/sawcon/reference/`):
- `sawcon.aws66.webp` (420 × 384 px): a small pit snapshot on a cream table. **Front view, about 35° above horizontal**, square to the front. **Steel plough** fitted, **steel hoop blade** on the arm. Another orange robot at the left edge; ignore it.
- `sawcon.aws67.webp` (1484 × 1244 px): cut out onto white. **Front-left three-quarter, about 30° above horizontal**. The best photo: plough, arm, gear, wires, red link, hoop blade, wheels.
- `sawcon.aws70.webp` (519 × 525 px): a pit snapshot on a grey floor. **Front view, about 55° above horizontal** (nearly top-down). A different front: an **orange printed bumper with two wedge feet**, and a **round disc** blade in an **orange motor housing**. An orange object at the top right belongs to something else.

Everything stated as fact is read from those photos. Anything inferred is marked **(guess)** with a confidence. Dimensions are **estimates in mm**, scaled from the AWS antweight limits (150 g, fits a 101.6 mm cube) and the photo proportions, and checked against the project spec draft (`spec.json`: two pods joined by a bridge, a weapon on an arm with an arm mount, four wheels each with its own motor, a plough with a face plate, battery, RX/ESC, weapon ESC, switch, lock pin). **W = overall width over the wheels ≈ 98 mm** is the ratio base.

Sawcon is a **"saw on a stick"**: a four-wheeled, two-pod chassis with a **front plough**, carrying a **powered arm** that is pivoted low at the front centre and holds a **small spinning blade** at its upper end. The arm swings the spinning blade **down onto** an opponent held on the plough.

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) under the centre of the chassis (mid-width between the pods, mid-length of the pods; plough excluded).
- **+X** = robot's right, **+Y** = forward (toward the plough), **+Z** = up. Units mm.
- All photos face the front, so the **robot's right is on the image left**. In AWS67 the camera is at the **front-left** of the robot (image right = robot left, nearer the camera).

Part IDs:

| ID | Part |
|---|---|
| PD-L / PD-R | orange printed side pods (motor housings) |
| BR | bridge joining the pods (rear and/or under the arm) |
| TP-L / TP-R | frosted white top plates on the pods |
| S-TP | top-plate button screws |
| LS | link slot in TP-L with the red plug |
| LK | red removable link (JST/BEC plug) |
| AB-L / AB-R | orange arm pivot bosses (on the pods' inner faces) |
| PV | arm pivot bolt with hex nut |
| AR | white translucent weapon arm |
| AG | white gear (sector) on the arm's base |
| MH | motor housing at the arm's tip (white/blue ring in AWS66/67; orange cylinder in AWS70) |
| WM | weapon motor (small, at the arm tip) |
| BH | blade hub (black, 4 holes) |
| BL-H | steel hoop blade (AWS66/67) |
| BL-D | steel disc blade (AWS70) |
| WW | weapon motor wires (black pair, plus red in AWS70) running along the arm |
| PL | steel plough (AWS66/67) |
| PL-N | notch in the plough's top edge |
| S-PL | plough Torx countersunk screws |
| OB | orange printed front bumper (AWS70) |
| OB-F | orange wedge feet of OB |
| S-OB | bumper screws |
| WH-FL/FR/RL/RR | four wheels: orange spoked hubs, black gear-tread tyres |
| DM-x | drive motors (hidden, guess) |
| AM | arm actuator (hidden, guess: servo with pinion) |
| BAT, RX/ESC, WESC | electronics (hidden, guess) |

---

## 1. Overall description in one paragraph

Sawcon is a **low four-wheeled robot** about **98 mm wide over the wheels** and **≈ 95 mm long** with its plough. The chassis is **two separate orange printed pods**, each about **34 mm wide × 70 mm long × 18 mm tall**, carrying **two wheels on its outer side** and closed on top by a **frosted, translucent white printed plate** held by **4–6 small silver button screws**. The pods are joined, with a **≈ 24 mm gap** between them that forms a **central channel**. At the front of that channel, between two **orange round bosses**, a **white translucent printed arm** is pivoted on a **through-bolt**. Its base is a **white spur-gear sector**, so the arm is **gear-driven** from below. The arm rises **up and back at ≈ 50°** for about **60 mm** to an upper end that carries a **small motor** and a **thin steel blade**: in AWS66/67 a **rounded-diamond steel hoop** about **45 × 38 mm**, in AWS70 a **round steel disc** in an **orange housing**. A **black wire pair** runs from the channel up the arm to the motor. On the **robot's left pod plate**, a **red link plug** sticks up through a slot. Across the front, the AWS66/67 robot has a **dark steel plough** with **pointed, swept-back ends**, a **rectangular notch** in its top edge where the arm swings down, and **two Torx countersunk screws**. The AWS70 robot has instead an **orange printed bumper bar** with **three screws** and **two hexagonal wedge feet** at its ends. The **four wheels (Ø ≈ 24)** are exposed, with **orange 5-spoke hubs** and **black gear-tooth tyres**.

---

## 2. Part-by-part description

### 2.1 Side pods (PD-L, PD-R)
- **Shape**: two rectangular boxes, each **x ∈ ±[12, 46]** (34 mm wide), **y ∈ [−35, +35]** (70 mm long), **z ∈ [4, 22]** (≈ 18 mm tall; ground clearance ≈ 4 mm **(guess)**).
- **Colour / material**: **bright orange** FDM (PLA or PETG) with fine horizontal layer lines (AWS67 px ≈ (1150–1290, 680–870) on the robot-left pod's front-right side).
- **Wheel axles**: each pod carries two wheels on its **outer side** at the front and rear corners. The pod's outer wall lies **just inboard** of the wheels (gap ≈ 1–2 mm).
- **Inner faces**: facing the central channel. At the front, each inner face carries an **orange round boss AB** for the arm pivot.
- **Front faces**: in AWS67 the robot-left pod's front face shows a **white sticker or label** (px ≈ (1270–1300, 720–810), a white rectangle on the pod's outer front corner) **(guess: a label or a white printed tab)**.

### 2.2 Bridge (BR)
- The pods must be joined. Visible evidence: in AWS67 an **orange horizontal bar** lies across the channel **at the bottom front**, under the arm pivot (px ≈ (430–620, 840–960): an orange rectangular frame seen through the plough's notch, enclosing a dark opening). In AWS70 a **dark opening** in the channel floor (px ≈ (225–295, 330–360)).
- **Reconciled**: the pods are joined by an **orange U-shaped floor frame** at the front (under the arm) and a **rear bridge** (not seen) **(guess, medium)**. The spec has a single `bridge` part.

### 2.3 Top plates (TP-L, TP-R)
- **Material**: **frosted, translucent white/natural** printed plastic (natural PETG or PLA, printed with visible infill/top-skin lines that show as a diamond texture). About **2–3 mm** thick.
- **Plan**: each plate covers its pod: **≈ 34 × 68 mm**, with the outer edges **between** the wheels (the plates do not overhang the wheels), and a **stepped outline**: the outer corners are notched around the wheel tops (AWS67 robot-left plate px ≈ (690–1290, 400–900) shows notches at both outer corners).
- **Link slot LS**: the **robot-left plate** has a **rectangular slot ≈ 6 × 10 mm** near its front inner corner (AWS67 px ≈ (840–880, 650–700); AWS66 px ≈ (290–310, 190–215); AWS70 px ≈ (335–360, 260–300)). A **red plug LK** sticks up ≈ 8 mm through it.
- **Robot-right plate**: has a **small square hole** near its middle-inner edge (AWS67 px ≈ (420–460, 440–480)) **(guess: a screw access or a vent)**.
- **Screws S-TP**: **silver button-head hex screws**, head Ø ≈ 4 mm. In AWS70 each plate shows **6**: two at the outer corners front and rear, two at the inner corners, and two at mid-length (left plate px (140, 135), (228, 143), (105, 217), (222, 224), (95, 350), (190, 352); right plate px (355, 152), (440, 157), (330, 233), (448, 240), (315, 368), (420, 372)). AWS67 shows 5 on the robot-left plate. **Reconciled: 6 per plate, 12 total.**

### 2.4 Wheels (WH)
- **Tyre**: **black gear-tooth tread**, ≈ 40 teeth of ≈ 1.5 mm, **Ø ≈ 24 mm × 9 mm wide**.
- **Hub**: **bright orange**, **5 spokes** with **round/pear-shaped holes** between them, and a small centre boss (AWS67 robot-left wheels px (1010–1150, 860–1060) and (1300–1430, 490–710)).
- **Positions (centres)**: **(±44.5, ±27, 12)**. Wheelbase ≈ 54 (centres), track ≈ 89 (centres), outer faces at **x = ±49**.
- **Height**: tyre top z ≈ 24, ≈ **2 mm above the top plates** (z ≈ 22–24). Marginal invertibility.
- **Guards**: **none**. The wheels' outer faces and treads are fully exposed.

### 2.5 Arm pivot bosses (AB-L, AB-R) and pivot bolt (PV)
- **AB**: two **orange round bosses** (discs), about **Ø 18 × 6 mm**, on the inner faces of the pods at the **front of the channel**, centred at **(±10, +22, 20)**. Their outer rims are **toothed/knurled** on the robot-right boss in AWS67 (px ≈ (500–560, 560–700)), which suggests the right boss is **a gear** too (see §2.7).
- **PV**: a **steel bolt** along X through both bosses and the arm base. A **silver hex nut** (M3, ≈ 5.5 mm across flats) is on the robot-left boss's outer side (AWS67 px ≈ (760–795, 670–700)); AWS70 shows a **steel bolt end** at the robot-right side (px ≈ (190–205, 285–305)) and the nut at the left (px ≈ (320–335, 300–310)).

### 2.6 Weapon arm (AR)
- **Material**: **white translucent printed** plastic (natural PETG/nylon), with a frosted look and visible layer lines.
- **Shape**: a **straight beam** with a **rectangular section ≈ 12 mm wide (X) × 9 mm thick**, about **60 mm** from the pivot to the blade axis.
- **Base**: wraps the pivot bolt between the bosses. On its lower front it carries the **white gear sector AG**.
- **Body**: from the base it rises **up and back** at **≈ 50° from horizontal** (AWS67: from px (560, 650) to (950, 330); AWS66: from (225, 240) to (205, 60), which is nearly vertical in that frontal view, confirming that the arm leans straight back along the centreline).
- **Cut-outs**: in AWS67 a **window ≈ 10 × 20 mm** at mid-length (px ≈ (880–930, 330–400)) and a step on the near face (px ≈ (820–880, 360–460)) **(lightening or a wire channel)**.
- **Tip**: carries the **motor housing MH**. In AWS66 there are **three black screws** on the arm's front face near the tip (px ≈ (160–170, 65–100)): they hold the motor **(guess, medium)**.

### 2.7 Arm gear (AG) and actuator (AM, hidden)
- **AG**: a **white spur-gear sector**, about **Ø 18–20 mm** pitch circle, ≈ **12–16 coarse teeth** visible, integral with the arm base, on its **robot-right side** next to the right boss (AWS67 px ≈ (520–610, 580–720)).
- **AM (guess, medium)**: a **servo or geared motor** inside the robot-right pod or the bridge, driving a **pinion** that meshes with AG. The toothed rim seen on the right orange boss may be that **pinion or an idler**. A gear drive lets a small servo with a pinion swing the arm through a large angle (≈ 120°) quickly.

### 2.8 Weapon motor housing (MH), motor (WM) and hub (BH)
- **AWS66/67**: at the arm tip, a **round motor seat** (white, part of the arm) with a **blue anodised ring** (px ≈ (960–1000, 300–420)) that looks like the **bell or the mounting ring of a small motor**, and a **black hub BH** with **4 small holes** (≈ Ø 10, px (990–1050, 300–380)) clamping the blade with a **silver screw** at its centre.
- **AWS70**: an **orange cylindrical housing** about **Ø 20 × 15 mm** at the arm tip (px ≈ (238–300, 40–100)), with the **disc** on its robot-left side.
- **WM (guess, medium)**: a **small brushed or brushless motor**, Ø ≈ 16–20 mm. The **two-wire black pair WW** (AWS67) running up the arm suggests a **brushed** motor (a brushless would need three wires); AWS70 shows **red and black** wires. **Brushed, two-wire, ≈ Ø 16 × 20** is the best guess.
- **Axis**: along **X** (the blade is in a **YZ** plane, i.e. a **vertical** blade that spins in the plane of the arm's swing).

### 2.9 Blades (BL-H AWS66/67, BL-D AWS70)
- **BL-H hoop**: a **steel loop** cut from plate ≈ **2 mm** thick, with a **rounded-diamond outline ≈ 45 × 38 mm** and a **frame width ≈ 4 mm**, i.e. mostly **empty**. Dark, oxidised steel with scratches. The hub sits **off-centre**, near the lower front corner of the loop (AWS67), so the loop is **an eccentric single-tooth hoop**: most of its mass is on one side, and the far corner is the striking point **(guess, medium; the perspective makes the hub position uncertain)**. AWS66 shows the same hoop from the front (px ≈ (200–245, 15–130)).
- **BL-D disc**: a **round steel disc** ≈ **Ø 40 × 1.5 mm** with a plain edge (AWS70 px ≈ (295–325, 30–180), seen almost edge-on) and a hub screw at its centre.

### 2.10 Weapon wires (WW)
- **AWS67**: a **pair of thin black wires** loops from the channel (px ≈ (650, 640)) up along the **front face** of the arm to about mid-height (px (700, 520)), then into the arm. AWS66 shows the pair running from the channel up the arm's robot-left side.
- **AWS70**: **red and black** wires loop at the arm base (px ≈ (255–300, 255–285)).
- They are exposed between the chassis and the arm.

### 2.11 Steel plough (PL), AWS66/67
- **Material**: **dark grey steel plate**, ≈ **1.5 mm** thick, with bluish highlights (blued or painted) and many scratches.
- **Shape (front elevation)**: a **wide hexagon / chevron**: the lower edge is straight and long, the ends are **pointed** (the outer corners sweep back and up at ≈ 45°), and the top edge has a **rectangular notch PL-N** in the centre, about **24 mm wide × 12 mm deep**, matching the channel (so the arm and blade can swing down into it).
- **Size**: ≈ **96 mm wide** at its widest (the lower edge, nearly the full robot width), ≈ **26 mm** tall along its slope.
- **Slope**: ≈ **30–35°** from the floor, leading edge on the floor at **y ≈ +52**, top edge at about **(y +36, z 16)**.
- **Edge wrap**: the notch edges and the upper edges have **black rubber/tape strips** wrapped over them (AWS67 px ≈ (430–480, 600–790) and (680–740, 690–760)) **(guess: edge protection or anti-slip)**.
- **Screws S-PL**: **2 countersunk Torx (star) screws** with silver heads, one on each half (AWS67 px (290, 830) and (685, 1020); AWS66 px (175, 335) and (320, 335)), into the pods' fronts.

### 2.12 Orange bumper (OB), AWS70
- **Bar**: an **orange printed bar** across the front, ≈ **84 mm wide × 10 mm tall × 8 mm deep**, at y ≈ +36…+44, with **3 silver button screws** (px (180, 405), (250, 408), (325, 413)).
- **Feet OB-F**: at each end, a **hexagonal wedge block** ≈ **24 mm wide × 22 mm deep**, with a **sloped top** running from the bar's top down to the floor at the front and **chamfered outer corners** (px (30–160, 380–480) and (330–475, 385–500)). Fine horizontal layer lines.
- **Gap**: between the feet, under the bar, a **≈ 30 mm opening** at the floor where the blade can reach down **(guess)**.

---

## 3. Per-view sections

### 3.1 AWS67 (front-left, ≈ 30° above)
- **Silhouette**: a flat 4-wheeled base with a tall diagonal arm rising from the front centre to a hoop at the top right; the plough fills the front.
- **Detail**: the plough with its notch, Torx screws and edge tape; the orange bosses with the white gear; the nut; the black wires up the arm; the red link; both frosted plates with their screws; the orange spoked wheels.

### 3.2 AWS66 (front, ≈ 35° above)
- The plough across the bottom (px x 60–410), two plates left and right, the arm standing up at the centre to the hoop at the top, the red link, wires, orange wheels at the four corners.

### 3.3 AWS70 (front, nearly top-down)
- The plan view: two frosted plates (each with 6 screws) on orange pods, wheels at the corners, the arm in the channel leaning back, the orange motor housing and disc at the top, the orange bumper with feet across the bottom.

### 3.4 Top view (synthesised)
- Two 34 × 70 plates at x ±[12, 46], a 24 mm channel between them, the arm along the channel from the pivot at y +22 back to the blade at about y −15 (when raised), wheels at the four outer corners, the plough (96 wide) at the front.

### 3.5 Side view (synthesised)
- An 18 mm tall pod with two Ø 24 wheels; the plough sloping down ahead; the arm from the pivot at (y +22, z 20) back and up to (y −17, z 66); the blade in the YZ plane around it (top at z ≈ 85 for the hoop).

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| PD | box | 34 × 70 × 18 | 0.35 × 0.71 | orange FDM | bridge | 2 |
| BR | U frame / bar | 24 × 20 × 6 | — | orange FDM | integral or screwed | 1–2 |
| TP | stepped plate | 34 × 68 × 2.5 | 0.35 × 0.69 | frosted white FDM | 6 button screws | 2 |
| LK | red plug | 6 × 5 × 12 | — | red plastic | in LS | 1 |
| AB | boss / gear | Ø 18 × 6 | 0.18 | orange | integral with pods (guess) | 2 |
| PV | bolt + nut | M3 × 40 | — | steel | through AB and AR | 1 |
| AR | beam | 12 × 9 × 60 | 0.61 long | white translucent FDM | on PV | 1 |
| AG | gear sector | Ø 19, ≈ 14 teeth | — | white | integral with AR | 1 |
| MH | motor seat / housing | Ø 20 × 15 | — | white/blue (66/67), orange (70) | 3 screws | 1 |
| BL-H | eccentric hoop | 45 × 38 × 2, frame 4 | 0.46 | steel | hub screw | 1 (66/67) |
| BL-D | disc | Ø 40 × 1.5 | 0.41 | steel | hub screw | 1 (70) |
| PL | notched chevron plate | 96 × 26 × 1.5 | 0.98 | steel | 2 Torx CSK | 1 (66/67) |
| OB | bar + 2 wedge feet | 84 × 10 × 8 + 24 × 22 feet | 0.86 | orange FDM | 3 screws | 1 (70) |
| WH | gear-tread wheel | Ø 24 × 9 | 0.24 | black tread + orange hub | motor shaft | 4 |
| S-TP | button head | M2.5, head Ø 4 | — | silver | into pods | 12 |

---

## 5. Contact / gap matrix (estimated mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP ↔ PD tops | screwed | 0 |
| PD inner faces ↔ channel | gap between pods | 24 |
| AR base ↔ AB faces | side clearance | 0.5–1 |
| AR ↔ PV | rotates on | 0 |
| AG ↔ pinion (hidden) | meshing | 0 |
| AR (down) ↔ PL notch | swings into | 2–5 |
| BL ↔ TP edges (arm down) | clearance | ≥ 3 (guess) |
| WW ↔ AR | loose, taped/clipped (guess) | 0–5 |
| LK ↔ LS | plugged through | 0 |
| PL ↔ PD fronts | screwed | 0 |
| PL lower edge ↔ floor | touching | 0 |
| PL ↔ front wheels | clearance | 3–5 |
| OB ↔ PD fronts | screwed | 0 |
| OB-F bottom ↔ floor | near | 0–1 |
| WH inner face ↔ PD outer wall | running gap | 1–2 |
| WH top ↔ TP top | stands proud | +2 |
| WH bottom ↔ floor | contact | 0 |
| PD floor ↔ floor | clearance | ≈ 4 |

---

## 6. Mechanism

1. **Weapon**: a small, fast **vertical blade** at the end of a **swinging arm**. The arm rests leaning **back** (≈ 50°). To attack, the actuator drives the gear and swings the arm **forward and down**, through ≈ 90–120°, so the spinning blade comes down onto an opponent in front of the robot, ideally one held on the plough. The blade spins with its lower edge moving **toward the robot** or **away** (unknown); a saw on an arm typically cuts with the lower edge moving **forward** to throw debris away **(guess)**.
2. **Drive**: four wheels, **4WD skid steer**, one motor per wheel (spec) **(guess: N20 gearmotors, two per pod)**.
3. **Plough**: passive; gets under or holds opponents in the arm's reach.
4. **Self-righting**: with the arm swinging through a large arc, it can likely **push the robot back over** if flipped **(guess, medium)**.

---

## 7. Assembly order (suggested rebuild)

1. Print the **pods** and the **bridge**; join them (screws or integral print).
2. Fit **4 drive motors** in **plastic clamps** in the pods (shafts out through the outer walls); fit the **orange hubs** and **tyres**.
3. Fit the **arm actuator** (servo with pinion) in the right pod / bridge.
4. Install **battery, RX/ESC, weapon ESC** in the pods; route the **link** to the left plate slot.
5. Fit the **weapon motor** into the arm tip (3 screws), clamp the **blade** with the hub. Run the **wires** along the arm.
6. Place the arm between the bosses, insert the **pivot bolt**, fit the nut; check the gear mesh.
7. Screw on the **top plates** (12 screws).
8. Screw on the **plough** (2 Torx) or the **orange bumper** (3 screws).

---

## 8. Profiles as math (for rebuilding curves)

**8.1 Plough (front elevation in its own plane; u = across, v = up the slope, origin at the lower edge centre).**
Outline: (−48, 0) → (+48, 0) → (+40, 12) → (+30, 26) → (+12, 26) → (+12, 14) → (−12, 14) → (−12, 26) → (−30, 26) → (−40, 12) → close. The plate plane passes through the lower edge (y +52, z 0) and the top edge (y +30, z 13): **slope ≈ 31°**. Rotate (u, v) into world by x = u, y = 52 − v·cos 31°, z = v·sin 31°.

**8.2 Arm centreline (YZ, x = 0, at rest).** From the pivot P = (y +22, z 20) to the blade axis A = (y −17, z 66): length √(39² + 46²) ≈ 60.3, angle **≈ 50° above the −Y direction**. Arm section 12 × 9 about this line. Swing about P around X: A(θ) = P + 60.3·(−cos θ, sin θ) in (y, z), with θ from 130° (raised, i.e. leaning back: θ measured from +Y) down to ≈ 10° (forward, blade at z ≈ 30 over the plough).

**8.3 Gear sector AG.** Pitch radius 9.5 about P, module ≈ 1.25, 24-tooth full-circle equivalent, sector of ≈ 150° on the arm's lower front.

**8.4 Hoop blade (in its plane, origin at the hub).** A rounded rhombus with vertices (−6, −4), (+30, −8), (+36, +26), (+4, +30), each corner filleted r = 6; offset inward by 4 mm for the window, i.e. a 4 mm frame. A hub web from the origin to the nearest frame side.

**8.5 Disc blade.** Circle r = 20, hub hole r = 1.5.

**8.6 Wheel.** Root r 11, 40 teeth 1.5 mm tall: **r(φ) = 11 + 1.5·[sin(40·φ) > 0]**; hub with 5 spoke holes on a 6.5 mm radius, each Ø 4.

---

## 9. Pixel-based measurements (independent check)

**AWS67 (1484 × 1244):**
- Plough: lower edge from px (70, 670) to (1060, 1160) (oblique). Notch px ≈ (430–690, 590–720).
- Arm: from the base px (560, 650) to the hub px (1010, 330): ≈ 550 px.
- Hoop: px x 975–1215, y 35–400.
- Wheels: robot-left front px (1010–1150, 860–1060) ≈ 200 px tall; robot-left rear (1300–1430, 490–710).
- Plates: robot-left px (690–1290, 400–900).

**AWS66 (420 × 384):**
- Overall wheel-to-wheel width: px x 30 → 410 = 380 px. Plough: px 60 → 410 = 350 px.
- Arm from px (225, 245) to (200, 60): 185 px (foreshortened, mostly vertical in the image).
- Hoop: px (200–245, 15–130).

**AWS70 (519 × 525):**
- Wheel outer faces: px x 40 → 495 = 455 px. Plates: left 75–245, right 310–470.
- Channel: px 245–310 = 65 px. Bumper: px 30–475.
- Disc: px (295–325, 30–180) → 150 px tall.

---

## 10. Several independent estimates of key quantities

| Quantity | Method A (limits) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Width over wheels | ≤ 101.6 | — | — | **98** |
| Scale | — | — | AWS70: 455 px / 98 = 4.64 px/mm | 4.64 |
| Pod/plate width | — | (98 − 24 − 2 × 9)/2 = 28 | AWS70: 170 px / 4.64 = 37 (left), 160 / 4.64 = 34 | **34** |
| Channel width | — | — | AWS70: 65 / 4.64 = 14 (at the plate level, the plates overhang the pods); AWS66: 2 × 20 px gap → ≈ 20 | **24 between pods, 14–18 between plate edges** |
| Wheel Ø | — | 0.24 W = 24 | AWS67: 200 px vs plough 990 px for 96 → 19 (foreshortened); AWS70 wheel length 85 px / 4.64 = 18 (top view, chord of the visible top) | **24** |
| Arm length | — | ≈ 0.6 W | AWS67: 550 px vs plough 990 px → 53; corrected for perspective (the arm runs away from the camera) → ≈ 60 | **60** |
| Disc Ø (AWS70) | — | ≈ 0.4 W | 150 px / 4.64 = 32 (foreshortened in Y since seen from above) → ≈ 40 | **40** |
| Plough width | ≤ 101.6 | AWS66: 350/380 × 98 = 90 | AWS67 (oblique) 990 px vs wheel span ≈ 1050 px → 92 | **92–96 → 94** |

---

## 11. Consistency check: conflicts and reconciliation

1. **Channel width (14 vs 24).** The plates' inner edges overhang the pods' inner walls (to cover the pivot bosses), so the gap at the plate level is smaller than the gap between pod walls. The arm (12 wide) must fit between the bosses: bosses 6 mm each, so the pod gap ≈ 12 + 2 × 6 + clearance = **25**. **Reconciled: pods 24–25 apart, plates 16 apart.**
2. **Arm leaning back vs height limit.** A 60 mm arm at 50° puts the blade axis at z ≈ 66; plus the hoop's 38 mm → **top ≈ 85–90 mm**: within the 101.6 cube height. **Consistent.**
3. **Blade on the arm vs robot length.** The blade axis at y ≈ −17 with the hoop extending to −40 keeps the robot inside its own footprint at rest. **Consistent.**
4. **Brushed vs brushless weapon motor.** Two wires (AWS67) → brushed. **Adopted.**
5. **Plough width.** 94 mm, slightly narrower than the wheel span (98); the plough's pointed ends sit just ahead of the front wheels. **Consistent with AWS66 (wheels visible beyond the plough's ends).**

---

## 12. Why the designer did it (per part, mostly adversarial)

- **Saw on an arm**
  - Attack mode: the plough or bumper holds the opponent at the front; the arm brings the blade down onto its **top surface**, the least armoured part of most antweights. It is a **contact / cutting** weapon, not a getting-under weapon.
  - Attacks on it: the arm sticks up and is the tallest feature, so it is exposed to vertical spinners and to opponents pushing it. The translucent white print (likely PETG/nylon) **flexes** rather than snapping. The exposed wires are a weakness.
  - A small blade on a long lever: the blade's own energy is small, but the arm adds a hammer-like impact when it swings down.
- **Gear drive at the arm base**: a gear lets the actuator sit low and protected in the pod, and gives a large swing angle with a servo; it also isolates the actuator from some shock (gear teeth can skip instead of the servo stripping).
- **Two pods with a central channel**: the arm swings down through the chassis line; the channel gives it room to rest low and to reach the floor area in front. Separate pods also keep the drive and electronics apart and are smaller, simpler prints.
- **Frosted top plates with many screws**: removable access; stiff tops for the pods.
- **Red link on the top**: AWS rules require a removable link or switch accessible on the outside. Red and on top is easy for marshals to see. **Weakness**: it can be knocked out by an overhead hit.
- **Steel notched plough (AWS66/67)**
  - Getting under: a thin steel leading edge at 31° gets under opponents and lifts their front, presenting their top to the descending blade.
  - Attacks: the pointed ends **cover the front wheels** from a frontal approach; spinners hitting the plough are deflected up (into the arm's zone, which is a risk).
  - Notch: lets the blade reach down to the opponent's edge on the plough.
  - Edge tape: protects the notch edges or adds grip so opponents don't slide off.
- **Orange printed bumper with feet (AWS70)**: a lighter, cheaper front for pushing; the feet act as two **forks** that can get under opponents' corners, and the gap between them lets the disc reach the floor.
- **Exposed wheels**: maximum grip and width-in-cube for stability; **weakness**: horizontal spinners can hit them directly. The robot accepts this to save weight for the arm and blade.

---

## 13. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors DM | 4 × N20 gearmotors | 12 × 10 × 25 + shaft | two per pod along X, shafts out at (±46, ±27, 12) | medium (spec has 4) |
| Motor mounts | printed **plastic clamps/saddles** in the pods, each with 2 × M2 | 14 × 14 × 14 | at each motor | medium |
| Arm actuator AM | high-torque micro servo with a printed pinion on its horn | 23 × 12 × 25 | in the right pod's front, output along X at (+20, +22, 14) | medium |
| Weapon motor WM | brushed micro motor (e.g. 1306-class coreless / 180-size) | Ø 16 × 20 | arm tip | medium |
| Weapon ESC WESC | brushed ESC or a relay/MOSFET switch | 20 × 12 × 5 | left pod | low |
| Battery | 2S LiPo, 200–300 mAh | 40 × 18 × 10 | left pod | medium |
| RX/ESC | combined RX + dual brushed ESC | 25 × 15 × 5 | right pod rear | low |
| Link socket | JST/BEC plug socket under LS | — | (−25, +20, 18) | high |
| Bridge | U-frame floor joining the pods under the pivot, plus a rear cross bar | 25 × 20 × 6 | (0, +25, 4) and (0, −33, 10) | medium |
| Wiring | link → battery → ESCs; drive leads within each pod; arm actuator lead; weapon pair up the arm (exposed) | — | — | high (exists) |

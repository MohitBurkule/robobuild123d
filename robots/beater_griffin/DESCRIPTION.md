# Beater Griffin: full rebuild description from reference photos

Source photos:
- `robots/beater_griffin/reference/beater_griffin.aws67.webp` (1260 × 1152 px): AWS 67. Cut out onto white (a green fringe under the weapon is cut-out halo). Camera at the **front-right**, high (about 45° down); the front faces the lower right, so the robot's **right** side is on the image **left**. Best for the **weapon** (rectangular steel beater frame and the **purple "Quantum BE1806" brushless motor**), the **white body and top plate**, the **red power link**, the **orange side pods** with their **front skid legs**, and the **wheels**.
- `...aws70.webp` (444 × 377 px): AWS 70. Uncut, on a grey surface, low resolution. Camera **straight in front**, about 30° down. Best for the **front layout**: white front cheeks either side of the weapon bay, the beater bar spanning the bay, the motor on the robot's right, the orange pods and their legs, and the red link on the top.

Facts come from the photos; inferences are marked **(guess)**. Sizes are **estimates in mm**, scaled from the AWS limit (150 g, 101.6 mm cube), from the **BE1806 motor** (a known part: stator 18 mm, can about Ø 23 × 18 mm, which is the best scale in the photos), and from the spec draft (body 72 × 84 × 32, two inboard wheels r 14, drum r 9 with 2 teeth, a bumper). Ratios are against **W = overall width across the orange pods ≈ 84 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the white body footprint.
- **+X** = robot right, **+Y** = forward (toward the weapon), **+Z** = up. mm.
- Extents (reconciled §12): white body x ∈ [−30, +30], y ∈ [−36, +24], z ∈ [3, 30]; orange pods to x = ±42; weapon bay y ∈ [+10, +38]; skid legs to y ≈ +44 on the floor.

| ID | Part |
|---|---|
| BD | white (natural) body box |
| TP | white top plate (translucent) |
| S-TP | 4 black socket-head screws on TP |
| LK | red power link / JST plug on the top front-right |
| FC-L, FC-R | white front cheeks either side of the weapon bay |
| WB | weapon bay (open front between the cheeks) |
| BT | beater: rectangular steel frame spinning about X |
| MW | purple-anodised brushless motor ("Quantum BE1806 KV2…") |
| BRG | outboard bearing on the left cheek |
| PD-L, PD-R | orange side pods / wheel guards (C-shaped in plan) |
| LG-L, LG-R | orange front skid legs at the bottom of the pods' fronts |
| WH-L, WH-R | drive wheels: orange hubs, black treaded tyres |
| M-L, M-R, BAT, ESC, WESC, RX | hidden motors and electronics |

---

## 1. Overall description in one paragraph

Beater Griffin is a **compact "beater bar" spinner**: a horizontal spinning weapon across the front, between two side pods. The body is a **white/natural translucent printed box** about 60 mm wide, 60 mm long and 27 mm tall with a **white top plate** held by **four black socket screws** and a **red power link** plugged in at its front right. Along each side, a **bright orange pod** wraps around the outside of a **drive wheel** (orange hub, black chunky-tread tyre) like a mudguard, with rounded corners, and at the front each pod ends in a **short orange leg** that runs down to the floor as a skid. The front of the body is cut away into a **weapon bay** framed by two **white cheeks**; spanning the bay on a transverse axis is the weapon: a **rectangular steel frame** (two parallel steel bars joined by end plates, with a large open window between them), driven directly by a **purple-anodised Quantum BE1806 brushless motor** on the robot's right and supported by a **bearing** in the left cheek. The look is orange-and-white with a purple and steel "rolling pin" across the front.

---

## 2. Part-by-part description

### 2.1 Body box (BD)
- **Shape**: a box **60 mm wide × 60 mm long × 27 mm tall** (z 3 to 30) behind the weapon bay, with its front corners extended forward as the cheeks. Wall thickness about **2.5 mm**; the material is **natural/white translucent** (nylon, PETG or natural PLA), with layer lines and dirt in the corners.
- **Top front edge**: a **chamfered/rounded transition** from the top plate down to the weapon bay's back wall (AWS67: the white face below the top plate's front edge, sloping down toward the beater).

### 2.2 Top plate (TP) and screws (S-TP)
- **Shape**: a **flat white translucent plate**, about **56 × 56 × 2 mm**, sitting on the body rim; diagonal top-layer lines and scratches.
- **Screws**: **4 black socket-head cap screws** (M2.5–M3, head Ø 5 mm) at the corners, about 4 mm in (AWS67: (190, 210), (700, 45), (920, 265), (375, 465); AWS70: (130, 25), (95, 125), (325, 140), (355, 40)).
- **Power link LK**: a **red 2-pin JST-style plug** (about 8 × 6 × 12 mm) standing up from a **rectangular hole** (about 8 × 6 mm) in the plate's front-right corner (AWS67: (370–420, 300–440); AWS70: (90–120, 80–130)). It is the **removable power link** required by the rules.

### 2.3 Front cheeks (FC-L, FC-R) and weapon bay (WB)
- **Cheeks**: two **white blocks** at the body's front corners, each about **10 mm wide (X) × 20 mm long (Y) × 25 mm tall**, from z ≈ 4 to 29, with rounded front edges. They extend forward to y ≈ +38. Each carries one end of the weapon axle: the right cheek holds the **motor's mount**, the left cheek the **bearing BRG** (AWS67: a black ring/bearing at (1040–1080, 520–600)).
- **Bay**: the open space between the cheeks, **40 mm wide (X) × 28 mm deep (Y) × 25 mm tall**, open at the front, top front and bottom; its back wall is the body's front wall (white).

### 2.4 Beater (BT)
- **Shape**: a **rectangular steel frame**: two **parallel steel bars** about **34 mm long (X) × 6 mm × 5 mm** section, joined at each end by a **flat end plate** about **26 mm tall × 6 mm wide × 3 mm thick**, forming a closed rectangle **34 × 26 mm** with a large **window (about 22 × 14 mm)** in the middle (AWS67 shows the window clearly from the oblique view; AWS70 shows the top and bottom bars and the right end plate head-on). The frame is a **cut section of rectangular steel tube** or **welded/bolted bars** **(guess)**; its surfaces are ground bright with grey scale and dents on the edges (impact marks).
- **Axis**: the frame spins about **X**, through the centre of its end plates, at **(y ≈ +24, z ≈ 16)**. The two long bars are the **two "teeth"**, at a radius of about **10–13 mm** from the axis (spec: drum r 9, 2 teeth).
- **Mounting**: the right end plate is bolted to the motor's can (AWS67: two small black screw heads on the end plate at (775, 650) and (780, 690)); the left end plate carries a stub axle into the bearing.

### 2.5 Weapon motor (MW)
- **Shape**: a **brushless outrunner** with a **purple anodised can** and a black band with a white logo: "**Q**uantum" and "**BE1806 KV2…**" (AWS67: the text "BE1806 KV2" is legible on the can). Can about **Ø 23 × 18 mm**, with **slots** in the purple end for cooling.
- **Arrangement**: the motor's stator is fixed to the right cheek; the **can spins with the beater** (the beater's right end plate is screwed to the can's face). So the motor is **inside the weapon** on the right: from the right cheek inward: stator mount → spinning can → beater frame → bearing in the left cheek.
- **Position**: x ≈ +4 to +22, axis (y +24, z 16).

### 2.6 Orange side pods (PD-L, PD-R) and legs (LG-L, LG-R)
- **Shape**: each pod is an **orange printed "C"** in plan, about **12 mm wide (X) × 74 mm long (Y) × 28 mm tall**, wrapping the outside of its wheel: an outer wall with **rounded front and rear corners** (radius about 10 mm), and short returns at the front and rear that join the body. The top edge is rounded. The pods are **thicker and taller at the front** where they protect the weapon bay's sides.
- **Legs LG**: at the bottom of each pod's front, a **short orange leg/skid** about **6 mm wide × 10 mm long**, angled down and forward to the floor (AWS67: at (480–540, 950–1030) and (1110–1150, 680–770); AWS70: at (55–75, 300–350) and (325–345, 310–355)). They are the robot's **front skids** and stop the weapon touching the floor.
- **Wear**: the pods are scuffed and dirty, with the front of the right pod showing chipped layers.

### 2.7 Wheels (WH)
- **Shape**: **Ø 30 mm × 10 mm**: **black rubber/TPU tyres** with a **chunky tank-track-like tread** (rectangular lugs about 3 mm long, about 24 lugs) on **orange hubs** (the hub's flat face visible inside the tyre).
- **Position**: in the space between the body sides and the pods, centres **x = ±36, y ≈ −10, z = 15**. Tops at z ≈ 30, level with the top plate; bottoms at z = 0. They are **inboard of the pods** (spec: inboard).

---

## 3. Per-view descriptions

### 3.1 Front view (AWS70)
- Two orange pods at the sides (12 wide, 28 tall) with legs at the floor; inside them, the white cheeks; between the cheeks, the beater frame (34 wide, 26 tall) with the purple/black motor can on the robot's right (image left). Above, the white top with the red link sticking up at the front right; the wheel tops show between the pods and the top plate.

### 3.2 Top view (inferred from AWS67)
- A white 60 × 60 square with four screws and the red link at the front right; orange C-shaped pods along both sides (overall 84 wide) with the black tyres visible in the gaps; at the front, the weapon bay with the beater (34 × 6 bars) and the motor (Ø 23).

### 3.3 Right side view (inferred)
- The orange pod's outer wall (74 × 28) with rounded corners, the leg at the front bottom, nothing of the wheel visible (covered); the motor can's end just visible in front.

### 3.4 Rear view (inferred)
- The white rear wall between the two orange pods; the wheel tyres partly visible.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | box | 60 × 60 × 27 | 0.71 × 0.71 × 0.32 | natural/white | — | 1 |
| TP | plate | 56 × 56 × 2 | 0.67 | white translucent | 4 × M3 socket | 1 |
| LK | JST link | 8 × 6 × 12 | — | red | plug | 1 |
| FC | cheek block | 10 × 20 × 25 | 0.12 × 0.24 × 0.30 | white | integral | 2 |
| BT | rectangular steel frame | 34 × 26 × 6 (bars 6 × 5) | 0.40 × 0.31 | steel | bolted to MW can; stub in BRG | 1 |
| MW | outrunner | Ø 23 × 18 | 0.27 | purple/black | stator to FC-R | 1 |
| BRG | bearing | Ø 8 × 3 | — | black/steel | in FC-L | 1 |
| PD | C-shaped pod | 12 × 74 × 28 | 0.14 × 0.88 × 0.33 | orange | screws to BD (guess) | 2 |
| LG | skid leg | 6 × 10 × 6 | — | orange | integral | 2 |
| WH | wheel | Ø 30 × 10 | 0.36 × 0.12 | black tyre, orange hub | motor shaft | 2 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| BD bottom ↔ floor | clearance | 3 |
| WH bottom ↔ floor | contact | 0 |
| LG tips ↔ floor | contact (skids) | 0 |
| WH top ↔ TP | level | 0 |
| WH outer face ↔ PD inner wall | clearance | 1–2 |
| WH inner face ↔ BD side | clearance | 1–2 |
| PD ↔ BD | screwed/joined at front and rear returns | 0 |
| BT bars (swept circle r 13) ↔ floor | clearance | 3 |
| BT swept circle ↔ bay back wall | clearance | 3–5 |
| BT end plates ↔ FC inner faces | clearance | 1 (left), 0 to the can (right) |
| MW stator ↔ FC-R | bolted | 0 |
| BT ↔ MW can | bolted | 0 |
| BT stub ↔ BRG | running fit | 0 |
| LK ↔ TP hole | plugged | 0 |

---

## 6. Mechanism

1. **Drive**: two wheels slightly behind the centre, skid steer; the front rests on the two orange legs.
2. **Weapon**: the BE1806 outrunner (an 1806 multirotor motor, typically 2300 kV) spins the beater directly. On 3S (11.1 V) at about 70% efficiency: ≈ 18,000 rpm. Swept radius 13 mm → tip speed ≈ 2π·0.013·300 ≈ 24.5 m/s. Mass of the frame (2 bars 34 × 6 × 5 + 2 end plates 26 × 6 × 3) ≈ 7.85·(2·1.02 + 2·0.47) ≈ 23 g; I ≈ 0.016·0.0115² + small ≈ 2.4 × 10⁻⁶ kg·m²; E ≈ ½·I·(1885)² ≈ 4.3 J. The beater spins with its front moving **up** (an uppercutting drum) **(guess)**.
3. **Bars as teeth**: the two bars are 180° apart, giving two impacts per revolution; the window between them saves weight while keeping the mass at the rim.

---

## 7. Assembly order (suggested rebuild)

1. Print the white body with the cheeks, motor and bearing seats, and the battery/ESC bays; print the white top plate.
2. Fit the two drive motors and wheels.
3. Print the orange pods (with legs) and screw them to the body's sides over the wheels.
4. Fit the battery, drive ESC, weapon ESC, receiver; wire the red JST power link through the top-plate hole.
5. Bolt the BE1806 stator into the right cheek; bolt the steel beater frame to the motor can; slide its left stub into the bearing in the left cheek.
6. Screw on the top plate (4 socket screws); plug in the link.

---

## 8. Hidden / uncertain list
- Beater construction (cut rectangular tube vs welded bars) and exact attachment to the can.
- Drive motor type, wheel exact position.
- Battery cell count.
- The rear and underside.
- Sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin under the white body centre; +X right, +Y forward, +Z up; mm.
- Body x ∈ [−30, 30], y ∈ [−36, 24], z ∈ [3, 30]; cheeks to y +38; beater axis (y +24, z 16) along X, x ∈ [−18, +16] for the frame plus the motor to +22; pods x ∈ [±30, ±42], y ∈ [−36, +38]; wheels (±36, −10, 15).

## 10. Profiles as math

**10.1 Beater frame (cross-section in the YZ plane, about its axis A = (24, 16)).** Two bar sections: rectangles 6 (radial) × 5 (tangential), centred at A ± (0, 10) (rotating with angle θ: centres A + 10·(sin θ, cos θ) and its opposite). Swept envelope: circle r = 13 about A. End plates: rectangles 26 × 6 × 3 in the YZ plane at x = −18 and x = +16 (the frame's ends), with a bore r 1.5 (left stub) and 2 screw holes (right).

**10.2 Pod plan outline (XY, right pod).** Outer wall: x = +42 for y ∈ [−26, +28], with quarter circles of r 10 at the corners: centres (+32, +28) and (+32, −26). Front return from (+32, +38) to (+30, +38); rear return from (+32, −36) to (+30, −36). Wall thickness 3; total pod height 28; leg at the front bottom: a wedge from (y +38, z 6) to (y +44, z 0), 6 wide.

**10.3 Wheel tread.** r(φ) = 13.5 + 1.5·[sin(24φ) > 0.3], width 10.

**10.4 Top plate.** Square 56 × 56 at z 28–30, screws at (±24, ±24), link hole 8 × 6 at (+18, +20).

## 11. Pixel-based measurements

**AWS67 (1260 × 1152):** top plate corners (185, 210), (700, 40), (935, 260), (370, 470); beater frame from (530, 380) to (1030, 830); motor can (520–700, 560–900), "BE1806" text at (640–680, 680–800); orange right pod (50–550, 220–1030), left pod (950–1180, 40–770); right wheel (110–320, 260–520); left wheel (790–990, 40–280); link (370–420, 300–440); legs (480–540, 950–1030) and (1110–1150, 680–770).

**AWS70 (444 × 377):** pods x 20–110 and 300–410; cheeks (55–110, 155–300) and (290–335, 160–300); beater bars from x 95 to 300 (top bar y ≈ 205–215; bottom bar y ≈ 260–285); motor can (75–140, 195–290); top plate (85–360, 20–160).

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/known part) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Motor can Ø | BE1806: ≈ 23 | — | AWS67: 180 px | scale ≈ 7.8 px/mm |
| Beater length | — | 0.40 W | AWS70: weapon 205 px incl. the can vs top plate 275 px (56 mm) → 42; frame alone ≈ 0.75 of that → 31 | **34 frame + 18 can = 52 total weapon width** (the bay is 40 + can inside the right cheek) |
| Overall width | 72 (spec) | ≤ 101.6 | AWS70: 390 px vs top plate 275 px (56 mm) → 79 (the pods are nearer the camera than the plate's rear edge) | **84** |
| Body length | 84 (spec) | 0.88 W = 74 (pods) | AWS67: pod length 900 px oblique | **74 overall, body 60** |
| Height | 32 (spec) | 0.33 W = 28 | AWS70: pod 280 px tall incl. the leg vs plate 275 px → ≈ 0.5 of the plate width + leg → 28 + 6 | **28–30** |
| Wheel Ø | 28 (r 14) | 0.36 W | AWS67: 260 px / 7.8 → 33 (near) | **30** |
| Beater swept r | 9 (spec) | — | AWS67: frame height 26 mm → r 13 | **13** |

## 13. Consistency check: conflicts and reconciliation
1. **Scale**: the BE1806 can (Ø 23) is the one known dimension. In AWS67 it is 180 px, and the top plate's front edge is about 530 px, which would give 68 mm; but the plate is farther from the camera than the can (perspective), so 56–60 is consistent. **Body 60, plate 56.**
2. **Weapon width**: AWS70 shows the weapon (can + frame) spanning nearly the whole bay between the cheeks: bay 40 + can partly inside the right cheek. **Reconciled frame 34 + can 18.**
3. **Drum radius**: spec r 9 is the bar centre radius; the outer swept radius is 13. Consistent.
4. **Overall width**: 84 with pods; within the cube.
5. **Wheel position**: AWS67 shows the wheels near mid-length, slightly behind; the legs carry the front. **Reconciled y −10.**

---

## 14. Why the designer did it (per part, adversarial first)

- **Beater bar weapon (rectangular frame)**
  - Fight: a beater/drum sits low across the front and hits whatever drives into it, at **floor level**; the two bars bite on wedges' edges and wheels. Its short radius gives a high spin-up and high rpm, so it gets back to speed quickly after each hit. The open window halves the mass while keeping it at the rim (efficient energy storage).
  - Survival: a compact steel frame is almost indestructible; recoil goes into the cheeks and the robot's whole width.
  - Threats: wedges try to get under the beater; the orange legs keep the front at a set height so the beater meets the wedge's edge rather than being lifted.
- **Motor inside the weapon (can spins with the frame)**
  - Construction: no belt, no pulleys; the stator is bolted to the cheek, the can is the hub. The purple can is protected inside the bay between the cheeks.
  - Threat: impacts load the motor's bearings; the **outboard bearing** in the left cheek supports the other end, so the shaft is held at both ends.
- **Orange C-pods around the wheels**
  - Fight: they protect the wheels from horizontal spinners and from being caught by forks; rounded corners deflect hits and help the robot slide off walls. They extend forward past the weapon bay so the beater's ends are shielded from side hits.
  - Legs: they are skids and also small **wedgelets** at the outer front corners that feed opponents into the beater.
- **Wheels level with the top**
  - Fight: invertible: if flipped it still drives; the beater works either way up (it just spins the other way relative to the opponent unless reversed).
- **White translucent body and top**
  - Construction: nylon/PETG is tougher than PLA and flexes under impact; four socket screws give quick access; the red link is on top for safe arming/disarming.
- **Colours**: orange and white for visibility; the purple motor stands out.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | x ±20, y −10, z 15, along X | medium |
| Weapon motor | Quantum BE1806 2300 kV (seen) | Ø 23 × 18 | x +13, y +24, z 16 | high |
| Weapon ESC | 12–20 A BLHeli ESC | 25 × 12 × 5 | x −15, y −20, z 10 | medium |
| Drive ESC | dual brushed ESC | 25 × 15 × 5 | x +15, y −20, z 10 | medium |
| Battery | 3S 300 mAh LiPo | 45 × 17 × 15 | across the middle, x 0, y −2, z 12 | medium |
| Receiver | micro receiver | 20 × 12 × 5 | x 0, y −28, z 20 | low |
| Link | red JST plug bridging the battery lead (seen) | 8 × 6 × 12 | (+18, +20, 32) | high |
| Bearing | small flanged bearing (e.g. MR63) in the left cheek | Ø 6–8 | (−22, +24, 16) | medium |
| Wiring | battery → link → both ESCs; weapon phase wires through the right cheek to the stator | — | — | medium |

## 16. Mass budget (independent check)

| Item | Estimate (g) | Basis |
|---|---|---|
| BE1806 outrunner | 18 | catalogue weight of an 1806 motor |
| Steel beater frame | 23 | §6 volume × 7.85 g/cm³ |
| 2 × N20 gearmotors | 20 | 10 g each |
| 2 × wheels Ø 30 × 10 | 8 | 4 g each |
| Battery 3S 300 mAh | 26 | typical |
| Weapon ESC + drive ESC + receiver + link + wiring | 18 | — |
| White body + top plate | 22 | ≈ 18 cm³ PETG/nylon |
| Two orange pods | 10 | ≈ 8 cm³ |
| Screws, bearing, axle stub | 5 | — |
| **Total** | **150** | |

The budget closes at 150 g, with the weapon system (motor + beater + ESC) at about 50 g, a third of the robot: typical for a spinner that relies on its weapon. A heavier (solid) drum would not fit, which is why the beater has a window.

## 17. Matchups (adversarial summary)

| Attacker | First contact | Outcome sought |
|---|---|---|
| Wedge / forks | the orange legs and the beater bars at 3–29 mm height | the beater hits the wedge's leading edge and bounces it up; the legs stop Beater Griffin being lifted from the corners |
| Vertical spinner | beater vs disc, weapon-to-weapon | the stiff steel frame and both-end support survive; recoil is shared by the cheeks and pods |
| Horizontal spinner | the orange pods | the pods' rounded walls take the hit and protect the wheels; the robot turns to face with the beater |
| Flipper / lifter | under the legs or the rear | when flipped it keeps driving (wheels level with the top) and the beater still works inverted |
| Pusher | the beater | a running beater shreds a pusher's front; if the weapon is stopped, the robot is a weak pusher (only 2WD) |

## 18. Surface and wear reading
- **Beater**: the bars' leading edges are dented and greyed with scale, and the frame's top bar shows long scratches: it has made many impacts. The end plates are bright where the edges have been ground.
- **Orange pods**: the right pod's front is chipped and dirty, the left pod's top edge scuffed: side hits and wall contacts.
- **White body**: dark grime in the corners of the weapon bay (dust thrown by the beater) and around the link hole.
- **Wheels**: tread lugs intact; orange hubs clean.

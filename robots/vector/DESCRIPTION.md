# Vector: full rebuild description from the reference photo

Source photo (only one):
- `robots/vector/reference/vector.aws71.webp` (1200 × 846 px in the PNG conversion, cut out onto white, with a mask). AWS 71. Seen from the **front-left three-quarter, about 35–40° down**. The robot's **front** (the weapon between two forks) is at the **lower right**, the **rear** (two wheels) at the **upper left**. Visible: the **amber/gold translucent printed chassis**, the **white printed fork plates and front-bay liner**, the **black single-row "beater" rotor** with **three square hammered-steel teeth**, the **belt pulley and black belt** on the rotor's left end, the **two aluminium "horn" plates** standing up from the fork plates, the **flat top lid** with the raised black name **"VECTOR"** and a **black textured inlay**, silver button screws, the **left rear wheel** (black ribbed tyre, gold spoked hub) and the top of the right rear wheel, an **amber ribbed cylinder** ahead of the left wheel, and inside the open front bay **copper windings of the weapon motor**, a **red wire** and the belt.

Because there is **only one photo**, everything on the robot's **right side, rear and underside** is inferred by symmetry and by how such robots are built; such statements are marked **(guess)** with a confidence. This description is somewhat shorter on per-view material for that reason, but every part visible is covered. Dimensions are **estimates**. Scale anchors: (1) the **M3 countersunk Torx screws** in the steel teeth (head Ø ≈ 6 mm); (2) the **silver M3 button heads** on the lid (Ø 5.7); (3) the steel teeth (square, ≈ 12 mm, typical 12 × 12 tool-steel blocks); (4) the AWS cube 101.6 mm / 150 g. Reference **W = chassis width over the side walls ≈ 74 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the centre of the **chassis** (amber box between the wheels and the front bay, excluding the forks).
- **+X** = robot's right, **+Y** = forward (toward the weapon), **+Z** = up; mm. Rotor angle φ about the X axis measured from +Y toward +Z.
- Envelope: x ∈ [−50, +50], y ∈ [−48, +54], z ∈ [0, 56] (the horn tips are the highest points; the body top is z ≈ 32).

| ID | Part |
|---|---|
| CH | amber translucent printed chassis (tub) |
| LID | amber top lid with diamond texture |
| NM | raised black lettering "VECTOR" on the lid |
| INL | black textured rectangular inlay on the lid |
| S-L | silver M3 button screws on the lid (4) |
| PIN | tall silver pin / long screw sticking up at the rear-left |
| FB | front bay (weapon-motor pocket) with white liner (FBL) |
| FK-L / FK-R | amber fork legs (side wedges) reaching forward to floor tips |
| FP-L / FP-R | white fork plates on the forks (rotor side supports) |
| HN-L / HN-R | aluminium horn plates (axle carriers with upward spikes) |
| AXB | rotor axle bolts (socket caps) + bearings |
| HS | horn fixing screws (2 per horn) |
| RT | black rotor ("beater"): pulley end (RP), hub (RH), tooth lobe (RL) |
| TT-1..3 | three square hammered-steel teeth |
| TS | three M3 countersunk Torx screws in the teeth |
| BLT | black rubber belt (round O-ring or flat) |
| WM | weapon outrunner in the front bay |
| WH-L / WH-R | drive wheels (black ribbed tyres, gold printed spoked hubs) |
| RC | amber ribbed cylinder ahead of the left wheel (motor pod / wheel guard) |
| DM-L / DM-R | drive gearmotors (hidden) |
| MM | motor mounts (hidden, inside RC) |
| BAT, ESC, RX, SW, WR | electronics (hidden; red wire seen in FB) |

---

## 1. Overall description in one paragraph

Vector is a **two-wheel, rear-drive, belt-driven vertical "beater" spinner** with **forks**. The chassis is a **glossy amber/gold translucent printed box** about **74 mm wide, 60 mm long and 32 mm tall**, with a **flat textured lid** carrying the robot's name **"VECTOR" in raised black letters** and a **black textured inlay**. Two **Ø ≈ 32 mm wheels** (black ribbed tyres on **gold printed spoked hubs**) sit **outside the chassis at the rear corners**. At the front, the chassis opens into a **white-lined bay** holding the **weapon outrunner**, and from the chassis' front corners **two amber fork legs** slope **down and forward to pointed floor tips** about 25 mm ahead of the rotor axle. On each fork sits a **thick white plate**, and bolted to each white plate's outside is an **aluminium "horn" plate**: a rounded foot carrying the **rotor axle bolt** and **two screws**, with a **tall narrow spike with a long slot** rising up and back. Between the forks spins a **black printed rotor** about **64 mm wide**: a **pulley on its left end** driven by a **black rubber belt** from the motor, and a **single raised lobe** carrying **three square hammered-steel teeth (≈ 12 × 12 × 6 mm)** side by side along the axle, each held by a **countersunk Torx screw**. It is a single-tooth-row vertical spinner (an "eggbeater-like beater with one impact face"), spinning about X.

---

## 2. Part-by-part description

### 2.1 Chassis tub (CH)
- **Shape**: a box **74 mm wide (X, x −37…+37) × ≈ 60 mm long (y −42 … +18) × 32 mm tall** (z 2–34 incl. lid). The **sides are vertical** toward the rear and **slope inward-down** toward the front (the large amber left side face in the photo at the lower left runs from the top edge down and forward into the left fork, i.e. the side wall flows into the fork leg as one inclined plane).
- **Material / colour**: **translucent amber / gold** filament (PETG or "silk gold" PLA), glossy, with visible horizontal layer lines on the sides and a fine **diamond/knurled texture** on the top (textured build plate, so the lid is printed top-face-down).
- **Rear corners**: notched for the wheels (2.9): the wheels are **outside** the side walls at the rear, and the chassis' rear corners carry the drive motor pods (RC).
- **Rear face**: hidden; assumed flat and vertical at y −42 **(guess, high)**.
- **Floor**: hidden; ground clearance ≈ 3 mm **(guess)**.

### 2.2 Lid (LID), lettering (NM), inlay (INL), screws (S-L), pin (PIN)
- **LID**: a flat amber plate on top of the chassis, **≈ 70 × 56 mm, 2 mm thick**, at z 32–34, set slightly inside the chassis' top edge (a **1 mm step** around its edge is visible on the left and front). Its top has the **diamond texture**. The front edge of the lid is straight across at y ≈ +14, just behind the front bay; a white strip of the bay's liner shows between them.
- **NM**: the word **"VECTOR"** in **raised black block capitals** (≈ 1 mm proud, multi-material print or painted), each letter about **8 mm tall, 6 mm wide**, the word ≈ **45 mm long**, running **along Y** on the **right half** of the lid (from y ≈ −30 to +12, centred at x ≈ +22), with the letters' tops toward the lid's centre line (so the word reads correctly from the robot's left side, upside-down from the right). In the photo it reads rotated, top-right of the lid.
- **INL**: a **black rectangle ≈ 28 × 22 mm** with a fine **diamond / carbon texture**, flush with or 0.5 mm proud of the lid, on the **left-front** quarter of the lid (x −30 … −4, y −14 … +10) **(guess: a carbon-fibre or black-printed hatch over the receiver/switch, medium)**. It is a separate piece (its edges show a gap line).
- **S-L**: **silver M3 button-head screws** at the lid's corners: seen at the rear-right corner (x +30, y −40), front-left (x −30, y +12) and front-right (x +30, y +12); the rear-left is hidden behind PIN (assumed (−30, −40)). They fix the lid into the chassis walls (heat-set inserts or self-tapping).
- **PIN**: a **tall silver pin or long screw** standing **≈ 8 mm above the lid** at the rear-left corner, near the left wheel (x −34, y −44, z 34 → 42). With a domed head. **(guess: a removable link / arming pin, or an over-long lid screw; medium-low)**.

### 2.3 Front bay (FB) and white liner (FBL)
- **Shape**: an **open-topped pocket** at the front of the chassis between the forks, **≈ 34 mm wide (X) × 18 mm long (Y) × 22 mm deep**, its rear wall at y ≈ +14, front open toward the rotor. Lined with **white printed walls** (FBL) about 2.5 mm thick: a back wall and two side walls, the white side walls flowing forward into the **white fork plates** (2.5). The left white wall carries a short sloped top edge.
- **Contents (seen)**: the **copper windings** of a small **outrunner (WM)** low on the left of the bay, a **red wire** curl, and the **black belt** loop running from the rotor's left pulley back into the bay over the motor.

### 2.4 Fork legs (FK-L, FK-R)
- **Shape**: two **amber triangular legs** (in side view a long thin triangle), each about **8 mm wide (X)**, at the outer front corners, x ±(30…38). Each leg's **upper edge** runs from the chassis top front corner (y +10, z 30) **down and forward in a straight line** to the **tip** at about **(y +54, z 0)** (slope ≈ 34° from horizontal). Its **lower edge** runs from the tip back along the floor (z 0–1) to about y +36, then rises to the chassis bottom (y +18, z 3). The tip is **pointed** (1–2 mm flat), slightly chisel-shaped (the inner face chamfered).
- **Front faces**: in the photo the left leg's front-lower part shows a **flat chisel face** (the leg is cut back at the bottom so the tip is a wedge point); the right leg (lower right of the photo) shows the same, **tip at the floor** about 10 mm further right because of perspective.
- **Layer lines** along the length: printed lying on the side.
- **Function**: floor-touching **forks/wedgelets** ahead of the rotor.

### 2.5 White fork plates (FP-L, FP-R)
- **Shape**: **white printed plates ≈ 5 mm thick (X)**, lying on the **inner upper surface of each fork leg**, with a profile that follows the fork's top edge (sloping down-forward) and a **rounded front-top corner around the axle**. Each is about **36 mm long (Y) × 26 mm tall** at the axle. Left plate at x −34…−29, right at x +29…+34. The white plate is visibly a separate print (different colour) and is **sandwiched between the amber leg and the aluminium horn** **(guess)**.
- **Front edge**: below the axle the white plate is cut off with a **straight edge sloping back** at ~70°, leaving the amber leg tip in front.

### 2.6 Aluminium horn plates (HN-L, HN-R), axle bolts (AXB), screws (HS)
- **Material**: **aluminium sheet ≈ 3 mm thick**, satin silver, sawn/milled edges, slightly hammered texture.
- **Shape (left horn, seen clearly)**: a vertical plate on the **outer face of the white fork plate** made of
  - a **foot**: a rounded quadrilateral ≈ **22 × 18 mm** around the rotor axle, its lower front corner rounded r ≈ 6;
  - a **spike**: from the foot's top the plate narrows into a **long thin triangle** pointing **up and slightly back**, about **40 mm tall**, tapering from **≈ 12 mm wide** at its base to a **rounded tip ≈ 3 mm wide**, with a **long slot** (≈ 3 × 26 mm) along its centre, so the spike is a **slender "V" of two 4 mm wide legs** joined at the tip.
  - **Holes / screws**: the **rotor axle bolt (AXB)**: a **black/silver M3 socket cap with a washer and a flanged bearing** at the foot's centre, at **(x −38, y +28, z 26)**; **two small silver M3 button/pan screws (HS)** at the foot's rear (one above-behind the axle at (y +22, z 32), one below-behind at (y +22, z 20)), fixing the horn through the white plate into the amber leg.
- **Right horn (HN-R)**: seen only above the rotor at the upper right of the photo: the **same spike shape**, rising higher in the image (closer to the camera), with its slot, tip at about z 56. Mirror of the left **(high)**.
- **Spike angle**: the spikes lean back about **10–15°** from vertical (tip at y ≈ +20).

### 2.7 Rotor (RT: RP, RH, RL)
- **Axis**: along X at **(y +28, z 26)**, between the white fork plates' inner faces (x −29 … +29 → rotor length ≈ **56–58 mm**, with ≈ 1 mm end gaps).
- **RP (left end pulley)**: a **black disc Ø ≈ 36 mm × 8 mm** at x −28…−20, with a **groove** on its rim carrying the **belt BLT** (a thick black rubber ring around it in the photo, ≈ 3 mm section). The disc's face toward the camera is flat, with a central boss.
- **RH (hub)**: a **black cylinder Ø ≈ 28** from x −20 to −8, joining the pulley to the lobe.
- **RL (tooth lobe)**: from x −8 to +29 (≈ **37–40 mm wide**) the rotor is a **cam-shaped black block**: in side view, a circle Ø 28 about the axis plus a **lobe** extending on one side to a **flat mounting face** at a radius of ≈ 18 mm from the axis, on which the teeth sit. The lobe's back (trailing) side is a **smooth curve** from the flat face back down to the hub radius (the black curved underside visible under the teeth in the photo). In the photo the lobe points **up and forward (φ ≈ 50°)**, the teeth facing up-forward.
- **Material**: black printed (PETG/nylon/TPU?) with a matte, slightly rubbery look **(guess: nylon or PETG, medium)**.

### 2.8 Teeth (TT-1..3) and screws (TS)
- **Shape**: three **square blocks ≈ 12 × 12 mm face × 6 mm thick**, **hammered / shot-peened steel** (silver with a dimpled texture), with slightly rounded edges, **side by side along X** on the lobe's flat face with **≈ 1 mm gaps**: TT-1 at x −8…+4, TT-2 at x +5…+17, TT-3 at x +18…+30 (the third slightly overhangs the lobe's end, or the lobe is that wide). Their outer faces are at radius ≈ **24 mm** (18 + 6) → tooth tip circle Ø ≈ **48–52 mm** (corners at r ≈ √(24² + 6²) ≈ 25).
- **TS**: each tooth has a **countersunk M3 Torx (T10/T15) screw**, black, head Ø 6, flush, in its centre, threading into the lobe (heat-set insert or a nut trapped inside).
- **Leading edge**: the teeth's edge on the rotation side is the impact edge (square).

### 2.9 Belt (BLT) and weapon motor (WM)
- **BLT**: a **black rubber belt** ≈ **3 mm round section** (O-ring belt) or ≈ 5 mm flat, running from RP's groove **back and up into the front bay** to the motor pulley. It is visible as a thick black curve going over the white liner's left wall (top of the bay) and down to the motor.
- **WM**: an **outrunner with exposed copper windings** (seen through a gap: a **brushless motor whose bell has windows** or an **inrunner-less outrunner of ≈ Ø 20–24**), **axis along X**, in the bay at about **(x −14, y +8, z 14)**, its pulley (Ø ≈ 8–10) on the left end aligned with RP at x ≈ −24. Belt ratio ≈ 36/9 = **4:1** reduction **(guess, medium)**.

### 2.10 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 32 mm × 10 mm**. **Tyre**: black rubber with **fine axial ribs** (≈ 1.5 mm pitch) all round, ≈ 4 mm thick. **Hub**: **gold/amber printed** (same filament as the chassis) with **four spokes** in an **X/cross pattern** and four windows, a raised rim ring, and a central boss with a **small silver screw/shaft end**.
- **Position**: centres at **(x ±45, y −32, z 16)**; inner face x ±40 (≈ 3 mm off the chassis side), outer face x ±50. Wheel tops at z 32 — **level with the chassis top**, so the wheels are about level with the lid; inverted, the robot would rest on the wheels and the lid **(guess: drivable inverted, medium)**, and the horns stick up 20 mm above the lid, so it would rest on the horns: **not drivable inverted** unless the horns act as a self-righting kickstand (see §6).
- **Right wheel**: only its top quarter is seen above the chassis at the rear right; same shape **(high)**.

### 2.11 Ribbed cylinder (RC) and motor mounts
- **RC**: an **amber vertical-axis? — no: X-axis cylinder** standing ahead of and inboard of the left wheel at about (x −40, y −18, z 16): about **Ø 18 × 14 mm** with **strong horizontal ridges** (layer lines or a deliberate rib texture). Above it a small **amber tab** with a notch. It is most likely the **drive motor pod**: the printed tube clamping the **N20 gearmotor**, sticking out of the chassis side ahead of the wheel, **or** the **front wheel guard**: a stub that protects the tyre's front **(guess: motor pod / guard, medium)**. The left wheel's front edge is just behind it (gap ≈ 2 mm).
- **Drive motors**: **2 × N20 gearmotors** along X, centred at (±26, −32, 16), shafts out through the chassis rear-side walls into the hubs **(guess, high)**.

---

## 3. Per-view descriptions

### 3.1 The photo (front-left three-quarter, 35–40° down)
- Upper left: the left rear wheel, big and close to the camera, black ribbed tyre and gold cross-spoked hub, with the ribbed amber cylinder in front of it and the tall pin above.
- Centre-top: the amber lid with the black inlay (left-front) and "VECTOR" (right), three silver screws; the right rear wheel's top beyond the lid.
- Centre: the white-lined front bay with copper windings, red wire and the belt.
- Lower centre: the left fork leg's sloping amber face, the white plate on top of it and the aluminium horn with its axle bolt, two screws and tall slotted spike.
- Right: the black rotor with its pulley and belt on the left end and the three steel teeth in a row on its top-front, the right horn's spike rising behind them; the right fork leg's tip on the floor at the lower right.

### 3.2 Top view (inferred)
- An amber rectangle 74 × 60 (lid with name and inlay), wheels outside at the rear corners (x ±40…±50), the front bay as a white-walled notch in the front centre, two fork legs extending forward to y +54 at x ±30…±38, the rotor between them at y +28 (a black bar 58 wide, with the pulley at the left end and teeth across the right two-thirds), the horn plates outside the fork plates at x ±38…±41.

### 3.3 Front view (inferred)
- Two fork tips on the floor at x ±34; between them the rotor (Ø ≈ 50 tooth circle centred at z 26), its pulley at the left; the horn spikes rising above the fork plates to z 56; behind, the chassis front and lid at z 34; the wheels outside at the rear, their tops at z 32.

### 3.4 Left side view (inferred)
- Wheel at the rear (centre y −32), the motor pod ahead of it, the chassis side running forward and down into the fork leg (a long sloping edge from (y +10, z 30) to the tip at (y +54, z 0)); the white plate and the aluminium horn at y +20…+36 with the axle bolt at (y +28, z 26) and the spike rising to z 56; the rotor's tooth circle reaching from z 2 to z 50 around the axle.

### 3.5 Rear view (inferred)
- Flat amber rear face 74 × 32 with the two wheels outside it; the horns' tips just visible above the lid.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 74 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | box with sloping front sides | 74 × 60 × 30 | 1 × 0.81 × 0.41 | amber translucent PETG | — | 1 |
| LID | textured plate | 70 × 56 × 2 | 0.95 × 0.76 | amber | 4 × M3 button | 1 |
| NM | raised letters "VECTOR" | 45 × 8 × 1 | 0.61 | black | printed/painted | 1 |
| INL | textured rectangle | 28 × 22 × 1 | 0.38 | black (CF?) | inset | 1 |
| FBL | U-shaped liner | 34 × 18 × 22, wall 2.5 | 0.46 | white | inside FB | 1 |
| FK | triangular leg | 8 wide × 44 long × 30 tall | — | amber | integral with CH | 2 |
| FP | profiled plate | 36 × 26 × 5 | — | white | screws | 2 |
| HN | foot + slotted spike | 22 × 18 foot, spike 40 × 12, 3 thick | 0.54 tall | aluminium | 2 screws + axle bolt | 2 |
| RT | pulley + hub + cam lobe | Ø 36 pulley; lobe to r 18; 58 long | 0.78 long | black printed | on axle bolts / bearings | 1 |
| TT | square block | 12 × 12 × 6 | 0.16 | hammered steel | 1 × M3 CSK Torx each | 3 |
| BLT | O-ring belt | 3 section, ≈ 120 long | — | black rubber | stretched | 1 |
| WM | outrunner | Ø 22 × 20 | 0.30 | black / copper | in FB | 1 |
| WH | ribbed tyre, X-spoke hub | Ø 32 × 10 | 0.43 | black tyre, gold hub | N20 shaft | 2 |
| RC | ribbed cylinder | Ø 18 × 14 | — | amber | integral | 2 (guess) |
| S-L | button screw | M3, Ø 5.7 | — | silver | inserts | 4 |
| PIN | pin / long screw | Ø 3 × 8 proud | — | silver | — | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| FK tips ↔ floor | sliding contact | 0 |
| WH bottoms ↔ floor | contact | 0 |
| CH floor ↔ floor | above | 3 |
| WH inner face ↔ CH side | running clearance | 3 |
| WH front ↔ RC | clearance | 2 |
| WH top ↔ LID plane | level | 0 (both z ≈ 32) |
| LID ↔ CH top | seated in a 1 mm step | 0 |
| FP ↔ FK | fastened | 0 |
| HN ↔ FP outer face | fastened | 0 |
| AXB ↔ RT | axle (bolt into the rotor's insert / through a shaft) | 0 |
| RT ends ↔ FP inner faces | end clearance | 1 |
| TT tips (r 25) ↔ floor (axis z 26) | lowest pass | 1 |
| TT tips ↔ FB front edge / CH front (y +14) | swept clearance | 28 − 25 − 14 … ≈ 3 at the lid front edge |
| TT ↔ HN spikes | the spikes are outside the rotor's ends | ≥ 3 axially |
| RP ↔ BLT | in groove | 0 |
| BLT ↔ FBL left wall top | passes over / rubbing | 0–1 |
| WM ↔ FBL | mounted | 0 |
| FK tip ↔ rotor tip circle (ahead) | fork ahead of rotor | the tip y +54 vs rotor front y +28 + 25 = +53: tips ≈ 1 ahead |

---

## 6. Mechanism

1. **Weapon**: a **belt-driven single-row vertical spinner**. The rotor spins about X, normally **top moving forward/up** at the front (the teeth come up from below the opponent's front edge and lift it). With a Ø 22 outrunner at ≈ 25 000 rpm and a 4:1 belt, the rotor turns ≈ 6 000 rpm; tip radius 25 → **tip speed ≈ 16 m/s**. The single tooth row and the cam lobe make it a **one-bite-per-turn** weapon: an opponent can get deep before the teeth arrive, so each hit lands fully. The rotor is unbalanced by design unless the hub side is weighted **(guess: the pulley end and the lobe's back are shaped to partially balance, medium)**.
2. **Forks**: two floor-touching legs ahead of and outside the rotor; they get under opponents and lift them slightly into the teeth' path and stop the rotor's reaction from slamming the robot's nose into the floor.
3. **Horns**: carry the axle bolts high enough and give the axle bearings big, stiff aluminium supports. The tall slotted spikes protect the rotor's top from overhead hits and **act as self-righting / anti-flip posts**: when the rotor's reaction flips the robot onto its back, the robot lands on the horns and the wheels, which together with the gyroscopic kick may let it roll back over **(guess, medium)**.
4. **Drive**: 2WD rear-wheel skid steer, wheels outside the chassis at the rear corners; the fork tips are the front skids.

---

## 7. Assembly order (suggested rebuild)
1. Print the **chassis** with the fork legs and motor pods (amber), the **lid** (textured face down) with the raised name (multi-material or paint), the **white liner + fork plates**, the **rotor** (black), the **wheel hubs** (amber).
2. Fit the **drive gearmotors** into the pods, wheels onto the shafts.
3. Fit the **weapon outrunner** with its pulley into the white-lined bay; loop the **belt** on its pulley.
4. Fit electronics (ESCs, receiver, battery, switch) inside the chassis; route wires (red wire visible near the bay).
5. Screw the **teeth** to the rotor's lobe with **3 countersunk Torx screws** (thread-lock).
6. Put the belt round the rotor's **pulley**, place the rotor between the fork plates, slide the **bearings** into the **aluminium horns**, and bolt the horns to the fork plates and legs with **2 screws each**; insert the **axle bolts + washers** through the bearings into the rotor.
7. Fit the **lid** with **4 button screws**, insert the **black inlay** and the **pin**.

---

## 8. Hidden / uncertain list
- The right side, rear and underside (only one photo).
- Weapon motor size and position, belt ratio and type.
- Whether the rotor is a through-axle on bearings or stub bolts into inserts.
- Whether RC is a motor pod or a wheel guard.
- What the black inlay and the tall pin are.
- Spin direction.
- All dims ±15 %.

## 9. Coordinate frame (restated)
Origin on the floor under the chassis centre (between wheels and bay); +X right; +Y forward; +Z up; mm. Rotor axis: line (y +28, z 26) along X, x ∈ [−29, +29]. Wheels at (±45, −32, 16), Ø 32 × 10. Fork tips at (±34, +54, 0). Horn tips at (±39, +20, 56). Lid top z 34.

## 10. Profiles as math

**10.1 Fork leg (YZ outline, x ±30…±38).** Polygon: (y +10, z 30) → (y +54, z 0) → (y +36, z 0) → (y +18, z 3) → (y +10, z 3) → close. Top edge: z = 30 − (30/44)(y − 10) for y ∈ [10, 54] (slope 34.3°). Tip chamfer: inner face cut by the plane x = ±30 + 0.5 (54 − y) for y > 44.

**10.2 Horn (YZ outline, at x ±38…±41).** Foot: rounded rectangle centred at (y +28, z 26), 22 (Y) × 18 (Z), corner radius 6 at the front-lower corner, 3 elsewhere. Spike: triangle with base from (y +21, z 35) to (y +33, z 35) and apex (y +20, z 56), apex rounded r 1.5; slot: stadium width 3 from (y +25, z 38) to (y +21.5, z 52).

**10.3 Rotor cross-section (in the rotor frame, angle φ).** Hub: circle r 14. Lobe (for x ∈ [−8, 29]): the convex hull of the hub circle and the segment from (r 18, φ −20°… ) — i.e. a flat face at distance 18 from the axis, perpendicular to φ = φ0, spanning ±13 tangentially; the trailing side a circular arc of radius 30 joining the face's trailing end to the hub tangentially. Teeth: rectangles 12 (tangential) × 6 (radial) on the flat face, outer face at 24.
Pulley (x ∈ [−28, −20]): circle r 18 with a V/round groove r 1.6 at radius 16.5.

**10.4 Tooth tip circle.** r_tip = √(24² + 6²) = 24.7; with the axis at z 26, the lowest pass is z = 1.3.

**10.5 Chassis side flow into the fork.** The chassis side face is planar from the top edge at (y +10, z 30) down to the fork leg; behind y +10 it is vertical from z 3 to z 32.

**10.6 Wheel hub.** Rim ring r 11–12; 4 spokes 3 wide at 45°, 135°, 225°, 315° from r 3 to r 11; boss r 3.

## 11. Pixel-based measurements (PNG 1200 × 846; ±8 px)
- Steel tooth faces: three squares from x 840 to 1170 (≈ 110 px each, face-on, nearest the camera). Torx screw heads ≈ 55 px.
- Left horn: foot at x 530–650, y 450–560; axle bolt at (575, 515); spike tip at (515, 225) → spike ≈ 300 px tall.
- Right horn spike: x 970–1065, y 65–250 (≈ 190 px visible).
- Left wheel: x 40–200, y 150–420 (≈ 270 px tall, the near side).
- Lid: front-left screw (285, 312), front-right screw (722, 290), rear-right screw (462, 70).
- "VECTOR": from (455, 90) to (760, 215), ≈ 330 px long.
- Inlay: corners ≈ (225, 215), (440, 160), (505, 260), (300, 310).
- Left fork tip (640, 690); right fork tip (1100, 595).
- Pulley disc: x 600–700, y 330–620 (seen nearly edge-on, ellipse).

## 12. Several independent estimates

| Quantity | Method A (Torx head Ø 6: 55 px → 9.2 px/mm at the teeth) | Method B (lid screw Ø 5.7: ≈ 20 px → 3.5 px/mm at the lid) | Method C (cube / typical parts) | Reconciled |
|---|---|---|---|---|
| Tooth face | 110/9.2 = 12.0 | — | common 12 × 12 blocks | **12** |
| Rotor width (3 teeth + hub + pulley) | teeth 330 px → 36; + hub/pulley ≈ 22 → 58 | — | fits between the forks | **58** |
| Horn spike height | ≈ 300 px / (≈ 6 px/mm at that depth) ≈ 50?? | — | — | **40** above the foot (§13) |
| Lid length (front-left → rear-right screws, diagonal) | — | ≈ 380 px /3.5 ≈ 108 (oblique, includes perspective scaling) | — | **≈ 56 × 70 lid** |
| Name length | — | 330 px /3.5 ≈ 94 (too big) | letters ≈ 8 mm tall, 6 letters → 45 | **45** |
| Wheel Ø | — | 270 px; wheel nearer → ≈ 6–8 px/mm → 34–45 | N20 wheel 32–34 | **32** |
| Overall width | — | — | ≤ 101.6 | **100** (wheels 2 × 10 + gaps 2 × 3 + chassis 74) |
| Overall length | — | — | ≤ 101.6 | **102** (y −48 → +54): marginal (§13) |

## 13. Consistency check
1. **Lid scale (method B)** gives oversized values because the lid is farther from the camera than the reference screws and the screw heads are tiny (±3 px → ±15 %). Using the teeth (12 mm) and the rotor width (58 mm) as the yardstick, the chassis width ≈ 74. **Reconciled: chassis 74 wide.**
2. **Overall length vs cube**: wheel rear y −32 − 16 = −48; fork tips y +54 → 102 mm, 0.4 mm over. Shorten: fork tips at y +53 (tips just level with the tooth circle) → **101 mm. Reconciled: tips at y +53.**
3. **Rotor floor clearance**: tooth tip r 24.7 at axis z 26 → 1.3 mm. The fork legs' bottom surface is at z 0 ahead of the rotor, so the teeth pass ≈ 1 mm above the floor between the forks. **Consistent.**
4. **Horn height**: the horn tip at z 56 against a lid at z 34 → 22 mm above the lid; in the photo the left spike tip is level with the lid's front-left screw height in the image but nearer the camera, so ≈ 20 mm above the lid. **Consistent.** Overall height 56 < 101.6.
5. **Wheel top vs lid**: wheel Ø 32 on centre z 16 → top z 32, lid z 34: the photo shows the wheel tops just above the lid line (perspective: wheels nearer). Wheels at most level with the lid. **Consistent within 2 mm.**
6. **Mass**: chassis + lid + forks 40 g (PETG), white plates/liner 8 g, aluminium horns 2 × 4 g, rotor 10 g, 3 steel teeth 3 × 6.8 g = 20 g, screws 4 g, belt 1 g, outrunner 18 g, 2 N20 + wheels 26 g, battery 2S 300 mAh 18 g, ESCs 8 g, RX 3 g → **≈ 164 g: too heavy**. So: chassis lighter (≈ 30 g, 2 mm walls), teeth smaller (12 × 12 × 4 = 4.5 g each → 13.5 g), outrunner 14 g → **≈ 144 g.** **Reconciled: teeth 12 × 12 × 4.5 mm** (the face-on photo cannot show their thickness; earlier 6 mm overridden).

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Single-row toothed beater rotor**
  - Attack: a **one-lobe rotor** gives the deepest bite: between tooth passes the opponent moves further into the swept circle, so the tooth hits a solid edge instead of skimming. **Three replaceable steel teeth** put hard steel where the impacts land while the rotor body stays light printed plastic; hammered/peened steel resists chipping. Countersunk Torx screws sit flush so they are not sheared on impact.
  - Getting under vs contact: the teeth pass 1 mm above the floor, so they meet wedges and low edges at their very bottom and lift opponents upward.
  - Adversarial: a printed rotor absorbs return impacts; if a tooth is lost, only that tooth and its screw are replaced.
- **Belt drive with the motor in the front bay**: the belt **slips on shock**, protecting the motor bearings; it keeps the motor inside the chassis, out of the line of fire, while the rotor is outside. A large pulley on the rotor gives a speed reduction so a small, light outrunner can drive a heavier rotor.
- **White fork plates + aluminium horns**: the white plates set the rotor's end clearances and give a flat seat; aluminium horns put the bearings in metal (printed bearing seats crack under rotor impacts) and spread the load into the forks with 3 fasteners each. The tall slotted spikes: shield the rotor's top, prevent opponents from riding over the rotor onto the lid, and give a fulcrum to roll the robot upright after being flipped; the slot saves weight while keeping two stiff legs.
- **Fork legs reaching the floor ahead of the rotor**: get under opponents first and present them to the teeth; carry the reaction when the rotor bites so the nose is not driven into the floor; protect the rotor from below.
- **Wheels outside at the rear corners with a guard/pod ahead**: big wheels for traction and inverted driving; the pod in front of each wheel stops opponents' spinners from catching the tyre's front. The wheels are exposed at the sides, which is the weak point.
- **Translucent amber chassis**: looks good and lets the builder see LEDs and wiring; PETG is tough and less brittle than PLA under impacts.
- **Raised name and black inlay**: identification; the inlay is probably a **hatch** over the switch/receiver so they can be reached without removing the lid.
- **Tall pin at the rear-left**: probably the **removable link / arming pin** required by the rules (visible, easy to pull) **(guess)**.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Weapon motor | brushless outrunner 1806–2204 class, axis along X | Ø 22 × 20 | (−12, +8, 14) | medium |
| Weapon pulley | grooved Ø 9 on the motor shaft | Ø 9 × 5 | (−24, +8, 14) | medium |
| Rotor bearings | 2 × MR63/683 flanged (3 × 7/8 × 3) in the horns | Ø 8 × 3 | (±38, +28, 26) | medium |
| Rotor axle | 2 × M3 bolts into heat-set inserts in the rotor ends, or one M3 through-rod | — | rotor axis | medium |
| Drive motors | 2 × N20 50:1–100:1 along X | 12 × 10 × 25 | (±26, −32, 16) | high |
| Weapon ESC | 12–20 A brushless | 25 × 13 × 5 | (+14, −6, 12) | medium |
| Drive ESC | dual brushed | 20 × 15 × 5 | (0, −20, 22) | medium |
| Battery | 2S LiPo 300 mAh | 45 × 18 × 12 | (0, −30, 9) | medium |
| Receiver | micro rx under the black inlay | 15 × 11 × 4 | (−18, −2, 28) | low |
| Switch / link | removable link at the tall pin, or switch under the inlay | — | (−34, −44, 30) | low |
| Wiring | battery → link → ESCs → motors; red wire into FB | — | inside | high |

# Alpha: full rebuild description from reference photo

Source photo (one only, cut out onto white by the AWS wiki):
- `robots/alpha/reference/alpha.aws72.webp`: AWS 72. Seen **from the front and above**, camera on the robot's centreline (or a few degrees left of it; `REFERENCE.json` says front-left iso, azimuth 105°, elevation 45°), looking down at about **45–50°**. The front lifter plate, decorated with a **"Night Fury" dragon face** print (two green eyes, blue nostril marks), fills the lower two-thirds of the image. The top of the robot, the two lifter arms, the central link and the open electronics bay are visible above it. Both drive wheels are visible at the rear corners.

**Limitation**: there is only one photo, and it shows the front and top. The sides are seen only as thin slivers, the rear and underside are not seen at all. Everything below about those faces is inferred and marked **(guess)**. The description is still kept complete (every visible part plus guessed hidden parts), but it is shorter than the multi-photo descriptions for that reason.

Pixel coordinates refer to a copy scaled to **1200 px on the long side** (≈ 1086 × 1200), read by eye, ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit and from the visible part proportions. Ratios use **W = overall robot width (outer faces of the green side walls) ≈ 96 mm**.

`REFERENCE.json`: `lifter`, 2 wheels, weapon `lifter`, axis x.

---

## 0. Coordinate system and naming

- **+X** = robot right (image right), **+Y** = forward (toward the camera / the dragon face), **+Z** = up. **Origin O** = the floor point under the centre of the chassis footprint (mid-width, mid-length, excluding the lifter plate's forward overhang).
- **Lifter angle β**: the angle of the front plate's face above the floor, measured in the YZ plane. In the photo β ≈ 35–40° (resting, lower edge on the floor).

| ID | Part |
|---|---|
| CH | black inner chassis (central tub + top) |
| SW-L / SW-R | bright green outer side walls (wheel guards) |
| SK-L / SK-R | black angled side skirts/blocks low on each side, in front of the wheels |
| TP-L / TP-R | black top lid plates either side of the central bay |
| BAY | open central electronics bay |
| EAR-L / EAR-R | black raised "ear" pivot towers at the rear corners |
| LA-L / LA-R | black lifter arms (side beams) |
| LP | front lifter plate (scoop) |
| DEC | dragon-face print on LP |
| LP-S | 2 black screws at the top corners of LP |
| LK | central black link bar (servo pushrod / arm) |
| HB | rear-centre hinge block with silver bolt and nut |
| PV | lifter pivot axle (rear, transverse) |
| WH-L / WH-R | two black treaded drive wheels |
| AX | silver axle/screw ends next to the wheels |
| S-TP | black screws on top lids |
| SV | lifter servo (hidden, guess) |
| DM-L / DM-R | drive gearmotors (hidden, guess) |
| BAT, RX, ESC | battery, receiver, ESC (partly visible) |
| CN-R, CN-W | red JST/BEC connector, white connector (visible in BAY) |
| WR | red, black, blue wires (visible in BAY) |

---

## 1. Overall description in one paragraph

Alpha is a **compact two-wheel servo lifter** with a **wide front lifting plate**. Its body is a **black printed chassis** about 70 mm wide between two **bright green outer side walls** that enclose the wheels, giving an overall width of about 96 mm. The front is dominated by a **flat, nearly square lifter plate** about 76 mm wide and 62 mm long, sloped at about 35–40° from a floor-touching front edge up to the top of the chassis. It is covered with a **glossy printed sticker of a black dragon face** (the "Toothless" Night Fury from How to Train Your Dragon) with two large green eyes. The plate is carried by **two black side arms** that run back over the top to **pivots in raised "ear" towers** at the rear corners. A **thin black central link** runs from a **hinge block with a silver bolt** at the rear-centre top down to the top edge of the plate; this is the servo drive. Between the arms there is an **open bay** showing the electronics (red connectors and wires, a white plug, a green PCB). Two **black wheels with fine moulded tread** sit in pockets at the rear left and right corners, inside the green walls.

---

## 2. Part-by-part description

### 2.1 Inner chassis (CH)
- **Shape**: a black printed body, roughly a box **70 mm wide (X) × 80 mm long (Y) × 30 mm tall** at the rear (the ears rise higher), stepping down toward the front where the lifter plate sits over it. The visible top surfaces are flat with crisp, chamfered edges (about 1 mm chamfers).
- **Colour/material**: matt black FDM (PLA/PETG), fine layer texture.
- **Front**: hidden under LP. Between the plate's upper corners and the side skirts there is a vertical black face about **12 mm tall** visible at the left and right of the plate (x ±38, z 20–32) — the chassis front corners **(guess)**.
- **Rear**: not seen. The rear edge carries the ear towers and the hinge block.

### 2.2 Green side walls (SW-L, SW-R): wheel guards
- **Shape**: a **flat vertical plate** each side, about **3 mm thick × 85 mm long × 32 mm tall**, with its top edge level with or slightly below the black top lids. Seen edge-on as a bright green strip about 3 mm wide down each side of the image, widening at the rear where the top is visible as a green ledge.
- **Position**: outer faces at **x ±48**. They run from the rear (y −42) to about y +40, past the wheels, and their front parts are partly hidden behind the black side skirts SK.
- **Function**: they **cover the outer faces of the wheels completely** (the wheels sit in the slot between the black inner chassis and the green wall). They are therefore the **wheel guards**. They also carry the outer ends of the wheel axles **(guess)**: the small silver screw heads AX at x ≈ ±42 next to each wheel look like axle or axle-bracket screws.
- **Supports to the chassis**: the green walls are tied to the black chassis by **cross bridges at the rear** (a green/black ledge behind each wheel, visible at the top-left and top-right of the image as a horizontal green face at y ≈ −40) and at the front by the black side skirts **(guess)**. Screws through the walls into the chassis are likely but not visible.
- **Colour/material**: **glossy bright green**, likely a different filament (PETG or TPU) or a printed part in green PLA. A TPU wall would make a good flexible guard **(guess)**.

### 2.3 Side skirts (SK-L, SK-R)
- **Shape**: on each side, low and forward, a **black block with a sloped outer face**: a prism about **12 mm wide (X) × 45 mm long (Y) × 28 mm tall**, its outer face sloping inward at about 15° from vertical toward the top. Its lower outer edge is just inside the green wall plane (x ±46), its top inner edge at about x ±38.
- **Position**: y ≈ −5 to +40, i.e. in front of the wheels, flanking the lifter plate. The plate's side edges sit about **4–6 mm inboard** of the skirts.
- **Function**: they enclose the front of the wheel slots and present angled side faces to attacks from the front corners. They may also house the drive gearmotors **(guess)**.

### 2.4 Top lids (TP-L, TP-R)
- **Shape**: two black **flat plates** at z ≈ 32, each about **22 mm wide × 50 mm long × 2 mm thick**, either side of the central bay, from y ≈ −30 to +20. Their inner edges are cut at an angle at the front (they splay outward, giving the bay a **pentagonal/coffin shape** that is wider at the rear).
- **Screws S-TP**: black pan-head Phillips, head Ø 4 mm. Visible: TP-L at its rear-inner corner (x −22, y −27) and front-outer corner region (x −30, y +12, near the wheel); TP-R at its rear corner (x +22, y −27) and front-outer (x +32, y +10). Total about **4 visible**, probably 6 in all.
- **Raised rails**: on top of each lid, along its inner edge, a **narrower raised strip** about 10 mm wide × 3 mm tall (a second plate or a boss) — these are the **lifter arm rest pads** or the arms themselves lying on the lids (see LA).

### 2.5 Central bay (BAY) and visible electronics
- **Shape**: an opening in the top between the arms, about **26 mm wide at the rear, narrowing to 18 mm at the front**, and **40 mm long** (y −25 to +15). Its rear end is a pointed (chevron) shape following the arm inner edges.
- **Contents seen**:
  - A **red JST/Deans-style connector** (CN-R), about **10 × 6 × 6 mm**, at x −4, y −5, standing up with **red wires** looping forward.
  - A **white plastic connector** (CN-W), about **6 × 4 mm**, at x +4, y −15, behind it.
  - **Blue and black thin wires** curling at x +6, y 0.
  - At the front of the bay, low, a **green PCB** (probably the receiver/ESC) with a **silver component** (a crystal or a heatsink pad) at x +6, y +12.
  - A **dark red/orange part** at x −6, y +12 (possibly the battery wrap or the servo body).
- The bay is **open to the top**, with no lid (or the lid was removed for the photo).

### 2.6 Ear towers (EAR-L, EAR-R)
- **Shape**: at the rear corners, the top of the chassis rises into two **curved horn-like humps**. Each is a black block about **14 mm wide × 18 mm long**, rising to **z ≈ 42**, with a **rounded rear top edge (radius about 7 mm)** and a sloped face running down toward the centre. Between them the rear edge dips into a **shallow V** to the hinge block.
- **Position**: centres at x ±30, y −38.
- **Function**: these carry the **lifter arm pivots PV** at their tops **(guess, strongly suggested by the arm geometry)**. A round boss end (Ø 8 mm) is visible at the top of each ear facing outboard.

### 2.7 Lifter arms (LA-L, LA-R)
- **Shape**: two black **straight beams**, each about **10 mm wide × 8 mm tall** in section, running from the ear tops at the rear (y −38, z 42) forward and down to the top corners of the lifter plate (y +22, z 32). In plan they are parallel at **x ±25 (centres)**, with their inner edges forming the bay sides.
- **Front ends**: they widen slightly and join the plate top corners via a **block/clevis** about 14 mm wide, with **one black screw** each (LP-S).
- **Rear ends**: rounded around the pivot (radius 6–7 mm).
- **Pose**: in the photo they slope down to the front at about **10°** (rest position).

### 2.8 Lifter plate (LP) and decal (DEC)
- **Shape**: a **flat rectangular plate**, about **76 mm wide (X) × 62 mm long along its slope × 1.5–2 mm thick**, with a **short downward-curled lip** along its bottom edge (a bent or thicker strip about 4 mm deep, giving a rounded front edge that touches the floor). Its upper corners are **chamfered at about 45° × 8 mm**, and its upper edge is straight between them.
- **Pose**: sloped at **β ≈ 38°**: lower edge at (y +58, z 0), upper edge at (y +9, z 38)… in the photo the upper edge sits **just under the arm front ends**, at the front of the bay.
- **Material (guess)**: thin **aluminium or polycarbonate sheet** under the sticker; the sticker is wrinkled and dimpled (pebbled texture with bumps), suggesting it is a **vinyl print stuck over a slightly uneven (printed or hammered) surface**. The bottom curl suggests a **bent sheet metal** (aluminium 1 mm) edge.
- **Decal**: a full-coverage print of a **black dragon face**: two large **green almond eyes** with vertical black slit pupils and white specular dots, at about (x ±22, y on-plate 30 mm from the bottom edge), each about **22 × 18 mm**; two **small curved blue marks** (nostrils) at (x ±8, 15 mm from the bottom edge). The rest is dark grey-black scaly texture. The decal wraps around the bottom curl.
- **Screws LP-S**: two black pan-head screws at the **top corners** (x ±32, 5 mm below the top edge), clamping the plate to the arm ends. The sticker is puckered around them.

### 2.9 Central link (LK) and hinge block (HB)
- **LK shape**: a **thin black flat bar**, about **6 mm wide × 3 mm thick × 60 mm long**, running from the hinge block at the rear-centre (y −40, z 46) **forward and down** to the top edge of the lifter plate (y +12, z 34) on the centreline. It is straight, with a slight widening at the front.
- **HB**: at the top-rear centre, a **clevis/hinge** made of **two black side cheeks** (each 5 mm wide × 12 mm tall) on either side of LK's rear end, with a **silver bolt** (Ø 3 mm, about 20 mm long, protruding about 8 mm to the right with a **silver hex nut/washer** on its end) passing horizontally (X) through all three. A small black spacer (Ø 6) sits on the bolt on the right.
- **Function (guess)**: HB is the **servo horn assembly** — the servo is mounted at the rear centre, its output axis along X at about z 40, and LK is a **long servo arm** (or a link from the horn) that pushes the plate up. Alternatively LK is a **prop/stop** that keeps the plate from falling. The first is far more likely: it is the only visible connection between the rear mechanism and the plate apart from the side arms.

### 2.10 Wheels (WH-L, WH-R)
- **Shape**: two **black wheels** about **Ø 26 mm × 10 mm wide**, with **fine transverse grooves** (about 20 grooves visible over half the circumference, i.e. about 40–50 ribs in total, each about 1 mm tall), like moulded rubber tyres of the N20 "Pololu-style" kind or printed TPU with ribs.
- **Position**: centres at **x ±40, y −28, z 13**, in the slot between the black inner chassis (inner face at x ±35) and the green wall (inner face at x ±45). The wheel tops are at z 26, below the top lids (z 32), so from the top they are seen **sunk in pockets**.
- **Hubs**: a darker grey hub insert with a small central boss (visible on the left wheel).
- **Clearance**: about **0–1 mm** to the green wall and the inner chassis side faces.
- **Invertibility**: wheel bottom at z 0 and top at z 26 vs chassis top z 32 → if flipped, the robot would rest on its lids/ears, **not on the wheels**. So the robot is **not invertible** and relies on the lifter to self-right **(guess)**.

### 2.11 Axle ends (AX)
- Small **silver** screw heads or pin ends, Ø 2–3 mm, visible at x ±42 just outboard of each wheel's top (in the green wall's inner slot). They are likely **M2/M3 screws** acting as the outer axle support or holding a motor clamp **(guess)**.

---

## 3. Per-view sections

### 3.1 The photo (front, high)
- **Lower half**: the plate, almost filling the robot width, as a rectangle about **815 px wide at the bottom** (x 110–925) and **670 px wide at its top edge** (x 210–880), from y ≈ 1000 (bottom curl) to y ≈ 430 (top edge). Two black screws at (265, 440) and (840, 505). Green eyes at (270, 650) and (780, 680).
- **Sides of the plate**: the black side skirts as sloped dark faces, x 70–200 and 900–1020, from y 300 to 900; the green walls as thin green edges at the far left (x 70–110) and right (x 1000–1030).
- **Upper half**: top lids, arms and bay. Bay outline from (430, 140) to (690, 140) at the rear to (470, 430) and (650, 430) at the front. Red connector at (520, 290–370). White connector at (600, 240). Green PCB at (600–640, 420).
- **Top**: the ears at (330, 65) and (840, 100); the hinge block at (540–640, 45–100) with the silver bolt end at (690, 75).
- **Wheels**: left at (175–245, 145–255), right at (900–980, 220–330), each showing ~8 tread ribs.

### 3.2 Top view (inferred)
- A rectangle 96 × 85 mm: green strips 3 mm at each side, wheel pockets in the rear half, black lids with the coffin-shaped bay between the arms, ears at the rear corners, hinge block on the rear centreline, and the plate extending from y ≈ +9 to +58 in front.

### 3.3 Side view (inferred)
- The green wall (85 × 32) hiding the wheel; the ear rising at the rear to z 42; the arm sloping forward from the ear to the plate's top; the plate as a 38° line from (y +9, z 38) down to the floor at y +58; the central link parallel and slightly above the arm on the centreline.

### 3.4 Rear view (not photographed)
- Green walls at both sides, the ears and hinge block on top, probably a power switch and the servo body visible on the rear face **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | stepped box | 70 × 80 × 30 | 0.73 × 0.83 × 0.31 | black FDM | — | 1 |
| SW | flat wall | 3 × 85 × 32 | 0.03 × 0.89 × 0.33 | bright green (PETG/TPU?) | bridges + screws (guess) | 2 |
| SK | sloped block | 12 × 45 × 28 | 0.13 × 0.47 × 0.29 | black | integral (guess) | 2 |
| TP | flat plate | 22 × 50 × 2 | 0.23 × 0.52 | black | 2–3 × M2 | 2 |
| BAY | opening | 18–26 × 40 | 0.19–0.27 × 0.42 | — | — | 1 |
| EAR | rounded tower | 14 × 18 × 42 (top z) | 0.15 × 0.19 | black | integral | 2 |
| LA | beam | 10 × 8 × 62 | 0.10 × 0.65 | black | pivot + 1 screw | 2 |
| LP | sloped plate | 76 × 62 × 1.5 | 0.79 × 0.65 | aluminium/PC + vinyl | 2 × M2 | 1 |
| DEC | vinyl print | 76 × 66 | — | black/green/blue | adhesive | 1 |
| LK | flat bar | 6 × 3 × 60 | 0.06 × 0.63 | black | bolt at HB, pin at LP | 1 |
| HB | clevis | 16 × 10 × 14 | 0.17 | black + silver bolt/nut | M3 bolt | 1 |
| WH | treaded wheel | Ø 26 × 10 | 0.27 × 0.10 | black rubber/TPU | motor shaft | 2 |
| AX | screw end | Ø 2.5 | — | silver | into SW/clamp | 2+ |
| S-TP | pan Phillips | head Ø 4 | — | black | into chassis | ~6 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| SW inner face ↔ WH outer face | side by side | 0–1 |
| WH inner face ↔ CH side | side by side | 0–1 |
| SW ↔ CH | bridged at the rear and front | 0 |
| SK ↔ CH | integral/joined | 0 |
| LP side edge ↔ SK inner face | side by side | 4–6 |
| LP bottom edge ↔ floor | touching (rest) | 0 |
| LP top edge ↔ LA front ends | screwed | 0 |
| LP top edge ↔ LK front end | pinned (guess) | 0 |
| LA bottom ↔ TP top | resting/near | 0–2 |
| LA rear ↔ EAR | pivoting | 0 |
| LK ↔ HB | bolted pivot | 0 |
| TP ↔ CH | screwed | 0 |
| WH top ↔ TP plane | below | −6 |
| WH bottom ↔ floor | touching | 0 |
| CH floor ↔ floor | above | 2–3 (guess) |

---

## 6. Mechanism

- **Drive**: two wheels at the rear, skid steer. The front of the robot is supported by the **lifter plate's lower edge** resting on the floor (a "wedge-skid"). The centre of mass must be between the wheel axle (y −28) and the plate edge (y +58).
- **Lifter**: a servo at the rear-centre turns the hinge-block axis (X). Two possible layouts:
  1. **(Preferred guess)** The side arms LA pivot on the ears at PV (y −38, z 42); the servo drives LK, which is pinned to the plate top; the plate + arms rotate about PV, the front edge rises in an arc of radius ≈ 100 mm (PV to plate edge) — a classic **"lifting wedge"**.
  2. The servo horn is the HB bolt and LK is a rigid servo arm; the side arms are passive guides (a parallel 4-bar). Then the plate translates and tilts.
- With a 100 mm radius, 30° of rotation raises the plate edge by about **50 mm**, enough to lift the opponent's front off the floor and push it over (and to **self-right** Alpha when inverted, by pushing the plate against the floor).

---

## 7. Assembly order (suggested)

1. Print CH (with skirts and ears) and the two green walls SW.
2. Install the two drive gearmotors in the rear sides, shafts out at x ±35, z 13, y −28; press on the wheels.
3. Fit the green walls, capturing the wheels; screw the axle/outer supports AX.
4. Install the servo at the rear centre (output axis along X at z ≈ 40), battery, receiver and ESC in the bay; route wires.
5. Screw the top lids TP-L and TP-R.
6. Put the side arms LA on the ear pivots (PV pins).
7. Fit LK on the servo/hinge with the silver bolt and nut.
8. Screw the plate LP to the arm ends with the two black screws; pin LK to the plate.
9. Apply the dragon decal over the plate, wrapping the bottom curl.

---

## 8. Hidden / uncertain list
- Exact pivot of the side arms (ears assumed) and whether LK is the driving link.
- Servo location (rear centre assumed) and type.
- Whether the bay has a lid.
- Rear face, underside, switch location.
- Plate material.
- All mm values ±15–20% (single photo, strong perspective).

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the chassis centre. +X right, +Y forward, +Z up, mm.
- Overall envelope: x ∈ [−48, +48], y ∈ [−42, +58], z ∈ [0, 46].
- Chassis top z 32; ears to z 42; hinge to z 46.

## 10. Profiles as math

**10.1 Lifter plate (in its own plane, u across X, v up the slope from the bottom edge).** Outline: (u, v) from (−38, 0) → (+38, 0) → (+38, 54) → (+30, 62) → (−30, 62) → (−38, 54) → close. Pose: a point (u, v) maps to (x = u, y = 58 − v·cos 38°, z = v·sin 38°). Bottom curl: a half-cylinder of r = 2 along the bottom edge, centre (y 58, z 2).

**10.2 Lifter arm LA (side profile).** Line from PV (y −38, z 42) to the plate top (y +9, z 38): z = 42 − 0.085·(y + 38). Section 10 × 8, rear end a semicircle r = 6 around PV.

**10.3 Link LK.** Line from HB (y −40, z 46) to (y +12, z 34): z = 46 − 0.23·(y + 40), 6 × 3 section.

**10.4 Ear (side profile at x = ±30).** From (y −45, z 30) up to (y −45, z 35), arc of r = 7 centred at (y −38, z 35) from 180° to 60°, then a straight line down to (y −24, z 32).

**10.5 Bay outline (plan).** Polygon: (−13, −25) → (+13, −25) → (+9, +15) → (−9, +15). Its rear has a chevron point toward the hinge: add (0, −32).

**10.6 Plate rotation.** With pivot P = (y −38, z 42) and plate edge E₀ = (y +58, z 0): radius R = √(96² + 42²) = 104.8 mm. Edge height after rotating by θ: z_E(θ) = 42 + R·sin(θ − 23.6°) where 23.6° = atan(42/96). Edge lifts 51 mm at θ = 30°.

**10.7 Wheel tread.** r(φ) = 13 + 0.8·[sin(48·φ) > 0], width 10.

## 11. Pixel measurements (one image, 1086 × 1200 scaled)
- Robot width at the plate bottom (nearest): green wall to green wall ≈ x 70–1030 = 960 px.
- Plate bottom edge: 815 px; plate top edge: 670 px; plate slope length (projected) ≈ 570 px.
- Wheel visible width: left ≈ 70 px, right ≈ 80 px; wheel visible length ≈ 110 px.
- Arm width ≈ 65–75 px at mid-length.
- Bay rear width ≈ 260 px, front ≈ 180 px.
- Hinge block width ≈ 100 px; bolt length beyond the block ≈ 60 px.

## 12. Several independent estimates

| Quantity | Method A (rule) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width W | ≤ 101.6, typical 90–100 | — | 960 px; plate 815 px = 0.85 W | **96** |
| Plate width | W − 2 skirts − gaps ≈ 96 − 20 = 76 | 0.79 W | 815/960 × 96 = 82 (nearest edge, perspective) | **76–80** |
| Plate length | box ≤ 101.6 → 100 − 42 (chassis rear half) ≈ 58 | 0.65 W = 62 | 570 px projected at ~45° viewing → ×1.2 = 680 px → 68 | **62** |
| Wheel Ø | 25–28 typical N20 wheel | 0.27 W = 26 | length 110 px foreshortened by sin 45 → 155 px ≈ 15?? (top half only visible) | **26** |
| Wheel width | 10 | 0.10 W | 70–80 px at the rear (smaller scale ~9 px/mm) = 8–9 | **10** |
| Arm width | 10 | 0.10 W | 70 px / 9.5 ≈ 7 | **8–10** |
| Height | 32 + ears 10 | — | not measurable (top view) | **42–46** |

## 13. Consistency check
1. **Wheel Ø**: pixel method only sees the top half of the wheel in its pocket; discard. A wheel below the lids (top z 26 < 32) with Ø 26 is consistent with "sunk in pockets" seen in the photo.
2. **Plate width vs side skirts**: 76 + 2 × 5 gaps + 2 × 12 skirts ≈ 110 > 96. The skirts must overlap the green walls in X (the skirts' lower outer edge is at the wall). Taking skirt width 8 at the plate's level: 76 + 10 + ... Reconciled: **plate 76, gaps 4, skirts 6–8 at the bottom, walls 3** → 96–100. OK within tolerance.
3. **Length**: chassis rear y −42, plate front y +58 → 100 mm, fits the 101.6 mm cube.
4. **Pivot location**: if the arms pivoted at the front of the lids, the plate would not rise as a whole; the ears are the only raised structure at the rear, so they must host the pivots. Consistent with the arms running all the way back.

---

## 14. Why the designer did it (adversarial first)

- **Wide sloped front plate (LP)**: the robot's whole front is a wedge, so any opponent coming straight in meets the plate; its floor-touching bent lip gets **under** flat opponents and wedges with thicker printed edges. Covering ~80% of the width means opponents cannot slip past onto the side skirts. When lifted, the wide plate lifts the opponent level (stable lift), making it easy to push them out or over. Against vertical spinners, a metal plate at 38° deflects hits upward; the sticker absorbs nothing but is cosmetic. Weak point: a single flat plate bending under a spinner tooth; the two top screws are the only fixings.
- **Arms pivoting at the rear ears**: the longest possible lever (≈ 105 mm) gives big lift height with modest servo angle and lets the plate rise as one rigid piece. Having the pivots high (z 42) means the plate edge rises **and moves back slightly**, pulling the opponent onto the robot. Weak point: the ears and arms are the tallest parts, the first thing an overhead weapon reaches.
- **Central link LK**: drives the plate at its centre, avoiding twisting the plate on one arm; thin and light. Weak point: thin printed bar can snap if the plate is hit while the servo resists — but the servo then backdrives first.
- **Green side walls (wheel guards)**: fully covering the wheels protects them from **horizontal spinners** and from being grabbed or tread-cut by enemy forks/wedges sliding along the sides. They also stop the wheels touching the arena wall (no friction when scraping along walls). A flexible green material would absorb side hits. Bright colour aids driver orientation.
- **Side skirts SK**: their sloped faces deflect hits at the front corners and stop opponents climbing onto the wheels; they also close the gap between the plate and the walls.
- **Sunk wheels, below the lid line**: protected from overhead hits and from opponents driving over. Cost: no invertible driving; the lifter is used to self-right.
- **Open bay**: allows fast access and cooling; it is shielded by the arms and plate from the front. Weak point: exposed electronics to overhead weapons and to debris.
- **Rear-mounted servo and hinge**: puts the servo mass at the rear, behind the wheel axle, so that the weight balances the plate on the front skid and keeps traction on the wheels.
- **Dragon decal**: showmanship; it also identifies the front for the driver.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Lifter servo | standard micro (9–17 g, metal gear) | 23 × 12 × 23 | x 0, y −36, z 30, output axis along X at z ≈ 40 | medium |
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | x ±22, y −28, z 13, shafts out along X | high (2-wheel json) |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 10 | x 0, y +5, z 10, under the bay | medium |
| ESC/RX | combined brushed ESC/RX board (green PCB seen) | 25 × 20 × 5 | front of bay, y +12, z 18 | medium |
| Arm pivot pins | M3 screws through the ears | Ø 3 × 16 | (±30, −38, 42) | medium |
| Front skids | none: the plate lip is the front support | — | — | medium |
| Power switch | on the rear face | 10 × 5 | x +15, y −42, z 18 | low |
| Wall–chassis screws | 2 × M2 per side through the green walls | — | y −40 and y +30 | low |
| Wiring | battery → switch → ESC → motors (short leads along the floor), servo lead from RX up to the rear | — | — | medium |

# Tritongue: full rebuild description from reference photos

Source photos:
- `robots/tritongue/reference/tritongue.aws71.webp` (2069 × 1462 px, cut out onto white, the main photo). AWS 71. Seen from the **front-left three-quarter, about 30° down**. Red body and side plates, **green 3-spoke wheels**, **cream/white three-lobed drum**, **green O-ring belts** at the drum's right end, the **left side plate** with its switch, screws, bearing bolt and **down-curved front fang**.
- `robots/tritongue/reference/tritongue.aws73.webp` (609 × 533 px, pit photo on a grey table). AWS 73. Seen from the **left side / above, about 45° down**, front to the right. Red body, **black wheels**, a **pink/peach drum** (lobes peach-orange), **two black belts** running back over the top of the body from the drum's right end, the left side plate with its bearing and a damaged edge near the switch.

Everything stated as fact is read from these photos. Inferences are marked **(guess)**. Dimensions are **estimates**. Scale anchors: AWS 150 g / 101.6 mm cube; the **flanged bearing + M3 socket bolt + washer** on the drum axle (washer Ø ≈ 7 mm, bearing flange Ø ≈ 9–10 mm); the wheels (3-spoke hubs, Ø ≈ 42 mm). Reference width **W = body width between the side plates ≈ 66 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the centre of the body footprint (the red box between the side plates, excluding the front extensions).
- **+X** = robot's right, **+Y** = forward (toward the drum), **+Z** = up; mm.
- Envelope: x ∈ [−48, +48], y ∈ [−42, +58], z ∈ [0, 42].

| ID | Part |
|---|---|
| BD | red printed body box (between the side plates) |
| TP | curved top skin of the body |
| SP-L / SP-R | left / right side plates (with the front extensions) |
| FG-L / FG-R | front fangs (down-curved tips of the side plates) |
| DR | drum (white/cream or peach) |
| LB-1..3 | three lobes ("tongues") on the drum |
| DP | drum pulley end (belt grooves) on the right |
| DS | red ribbed spacer / end ring on the drum's left end |
| BRG-L / BRG-R | flanged bearings in the side plates |
| AXB | axle bolts (M3 socket cap) + washers |
| BT | two drive belts (green O-rings in AWS71, black in AWS73) |
| WM | weapon motor (hidden, guess) |
| WP | weapon motor pulley (hidden) |
| WH-L / WH-R | two large wheels with 3-spoke hubs |
| M-L / M-R | drive gearmotors (hidden) |
| MM | plastic motor mounts (hidden) |
| SW | slide switch on the left side plate |
| S-SP | screws in the side plates |
| HL | blind holes / bosses in the side plates |
| BAT, ESC, RX | hidden electronics |

---

## 1. Overall description in one paragraph

Tritongue is a **two-wheel drum spinner**. A **red printed body box**, about **66 mm wide, 60 mm long and 32 mm tall**, with a gently **curved top**, sits between **two thick red side plates**. At the rear, **two large wheels** (Ø ≈ 42 mm, 3-spoke hubs) are mounted outside the side plates and stand taller than the body. At the front, each side plate extends **forward** past the body into a **rounded boss** that carries a **flanged bearing and bolt** for the drum axle, and then **curves down and forward into a pointed fang** that touches the floor ahead of the drum. Between the two plates spins a **printed drum**: a **round core (Ø ≈ 24 mm)** with **three thick rounded paddle-shaped lobes** ("tongues") standing out about **14 mm**, staggered along the drum's length and spaced 120° apart. The drum is **belt-driven**: two O-ring belts run from a grooved pulley at its **right** end back over the top of the body to a motor inside. The left side plate carries a small **slide switch**.

---

## 2. Part-by-part description

### 2.1 Body (BD) and top (TP)
- **Shape**: a box, **66 mm wide (X, between the side plates' inner faces) × 60 mm long (Y) × 32 mm tall** (z 4–36), y ∈ [−36, +24].
- **Top TP**: the top surface is **gently curved** (convex, falling toward the front): it is about z = 36 at the rear and z = 32 at the front edge, where it turns down into a **rounded front edge (r ≈ 6 mm)** just behind the drum. The top shows **heavy print layer lines running across (X)** and a **step/ridge** about 1/3 back from the front (AWS71: a line across the top where the surface changes slope; AWS73: horizontal ribbing).
- **Front wall**: below the rounded edge, a **vertical wall** facing the drum, with **a slot or recess** where the belts pass in (AWS73: the belts enter the body over the top-right).
- **Rear**: plain wall (not seen).
- **Colour**: bright red, slightly glossy PLA/PETG (AWS71 has a pinkish sheen).

### 2.2 Side plates (SP-L, SP-R)
- **Shape**: two **thick flat plates**, about **5 mm thick (X)**, at x = ±33 to ±38. Each side plate outline (side view):
  - **Rear part**: a rectangle from **y = −40 to +24**, **z = 4 to 38**, with **rounded rear corners** (r ≈ 6). It is about **2 mm taller than the body** (stands proud of the top).
  - **Front extension**: from the body front (y = +24) the plate continues forward as a **neck about 30 mm tall**, with its **top edge dipping** in a concave curve (r ≈ 10) then rising into a **round boss** (r ≈ 13) centred on the drum axle at **(y +40, z 24)**.
  - **Fang (FG)**: below the boss, the plate's **front lower edge sweeps down and forward** in a convex arc into a **pointed tip** on the floor at about **y = +58**. The fang's front face is a concave curve (like a claw); its lower edge is nearly straight along the floor. The fang is about **18 mm long** from the boss and tapers from about 14 mm tall to a point. **The fangs are offset inward/outward?**: in AWS71 the right fang is visible beyond the drum with its tip curled up slightly at the end (a small upturned point), and the left fang has a **step** on its upper edge about 10 mm behind the tip (a **notch / barb**).
  - The bottom edge of the rear part sits about 2–4 mm above the floor.
- **Features on SP-L** (AWS71):
  - **SW**: a **small slide switch** with a **silver metal body and bracket**, about **8 × 4 mm**, mounted through a rectangular hole at about **(y −6, z 30)**, near the top of the plate, a little behind mid-length. A **small black screw** sits just right of it (switch fixing).
  - **S-SP**: **two black socket screws** (head Ø ≈ 4 mm), one at **(y +4, z 28)** (top, ahead of the switch) and one at **(y +4, z 10)** (bottom). They hold the plate to the body or internal posts.
  - **HL**: **three round blind holes / countersinks** (Ø ≈ 4 mm) in a **triangle** around the bearing area: at (y +22, z 30), (y +18, z 18) and (y +24, z 8). Each is surrounded by a faint circular boss outline (printed "screw head" recesses). These are probably the **weapon motor mounting screws' recesses** on the inside, or **countersinks for screws not fitted** **(guess)**.
  - **AXB / BRG-L**: at the boss centre, a **stainless M3 socket cap bolt** with a **flat washer (Ø 7)** over a **flanged ball bearing** (flange Ø ≈ 10) pressed into the plate. AWS73 shows the bearing's black seal ring clearly.
- **Damage**: AWS73 shows the **left plate's top edge broken/chipped** near the switch (a ragged edge about 8 mm long).

### 2.3 Drum (DR), lobes (LB), pulley (DP), spacer (DS)
- **Core**: a **cylinder Ø ≈ 24 mm × 56 mm long** (between the side plates, minus about 4 mm of end parts), axis along X at **(y +40, z 24)**. Colour: **cream-white** (AWS71), **pink** (AWS73), matt, with a slightly rough, stringy surface (printed **TPU or PETG**; the lobes look slightly soft and chipped **(guess: TPU core with lobes)**).
- **Lobes (LB-1..3)**: three **thick rounded paddles**, each about **26 mm long (X, along the axis) × 10 mm thick (tangential) × 14 mm tall (radial, beyond the core)**, with **fully rounded outer ends** (a stadium/"tongue" shape: the outer edge is a semicircle of radius ≈ 13 seen along the radial direction). The lobe tip radius from the axis is about **26 mm** (Ø 52 tip circle).
  - **Placement**: AWS71 shows **LB-1** on top of the drum over the **left half** (x ≈ −18 to +6) and **LB-2** pointing **forward-down over the right half** (x ≈ +2 to +26). The third (**LB-3**) is hidden behind (pointing rear-down). The lobes are **120° apart** and **staggered along the axis**, so that every part of the drum's length is swept by at least one lobe and the drum stays balanced. A likely pattern: LB-1 at x −14 (0°), LB-2 at x +14 (120°), LB-3 at x 0 (240°) **(guess, medium)**.
  - AWS73 shows two **peach-orange** lobes against a pinker core, with a similar staggered arrangement.
- **DS (left end)**: a **red printed ring** about **Ø 26 × 6 mm**, with **two raised ridges** (grooves between), between the drum core and the left side plate. It is a **spacer** or a second (unused) pulley **(guess)**.
- **DP (right end)**: the drum's right end has **two grooves** carrying the belts, Ø ≈ 24 mm, next to the right side plate.
- **Belts (BT)**: **two round-section O-ring belts**, about **2 mm** cross-section: **green** in AWS71, **black** in AWS73. They run from DP **back and up over the body's top-right**, entering the body through a slot near the right side plate. Belt length about **130 mm** each **(guess)**.

### 2.4 Weapon motor (WM) and pulley (WP), hidden
- **Guess**: a **brushless outrunner (about Ø 18–22 × 20 mm)** inside the body near the front-right, its shaft along X, with a small grooved pulley (Ø ≈ 8 mm) driving the belts. The **3 holes (HL)** on the left plate suggest the motor is screwed to a side plate through a triangular pattern, but they are on the **left** side while the belts are on the **right**: so either the motor shaft runs across the whole body (the motor is mounted on the left plate and its shaft reaches the right-hand pulley), or the holes are something else **(low)**.
- Belt ratio: Ø 24 drum / Ø 8 pulley ≈ **3 : 1 reduction**.

### 2.5 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 42 mm × 10 mm**. **Tyre**: smooth or finely textured **green** (AWS71) or **black** (AWS73) rubber/TPU, about 5 mm thick. **Hub**: a **3-spoke wheel** (spokes 4 mm wide at 120°, with large open windows between) and a **small central hub Ø ≈ 8** with a **green/silver centre** (a screw or the shaft end).
- **Position**: centres at **x = ±44, y = −24, z = 21**. Inner faces about **1–2 mm** from the side plates' outer faces. Outer faces at x = ±49.
- **Height**: top at z ≈ 42, about **4 mm above the side plates' top** and about 6 mm above the body. Bottom on the floor. So the robot **can drive inverted** (the drum then spins in the other direction relative to the floor).
- **Guards**: **none**: the wheels are outside the side plates and fully exposed.

### 2.6 Drive motors (M-L, M-R) and plastic motor mounts (MM), hidden
- **Guess**: **2 × N20 gearmotors** (or 2 × 12 mm micro gearmotors) at the rear, along X, shafts through the side plates into the wheel hubs at z = 21, in **printed cradles** in the body **(medium)**.

### 2.7 Switch (SW) and wires
- **SW**: described in 2.2. The slider is accessible from the robot's left side.
- **Wires**: none visible.

---

## 3. Per-view descriptions

### 3.1 Top view
- A red rectangle (66 × 60) with layer lines across it, flanked by two 5 mm side plates that run from y −40 forward to the drum bosses and fangs (to y +58). Two big wheel rectangles (10 × 42) outside the side plates at the rear. Between the plates at the front, the drum (Ø 24 core) with its lobes, two belts running from its right end back over the body's right edge.
- Overall: **98 mm wide** (wheels), **98 mm long** (wheel rear y −45 to fang tips y +58… ≈ 100).

### 3.2 Front view
- The drum fills the space between the plates (66 wide), its lobes sticking out to Ø 52. The plates' bosses (with bolts) frame it at drum height. Below, the two fangs come down to the floor at the outer edges. Behind and above, the body's rounded front edge and the wheel tops sticking out at the sides.

### 3.3 Left side view (AWS71/73 closest)
- The side plate silhouette: a rounded rectangle at the rear, a neck with a dip, a round boss with a bolt and bearing, and a claw-like fang down to the floor. A big wheel at the rear covers most of the rear part. The switch and screws on the plate. The drum's lobes stick out above and in front of the boss.

### 3.4 Rear view (not photographed; inferred)
- The body's rear wall between the side plates; the two wheels outside; the curved top.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 66 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | box, curved top | 66 × 60 × 32 | 1 × 0.91 × 0.48 | red FDM | between plates | 1 |
| SP | profiled plate | 98 × 38 × 5 | 1.48 × 0.58 | red FDM | 2 screws + bearings | 2 |
| FG | claw tip | 18 long, 14 → 0 tall | — | red | integral | 2 |
| DR | cylinder core | Ø 24 × 56 | 0.36 × 0.85 | cream / pink TPU-PETG | axle bolts | 1 |
| LB | rounded paddle | 26 × 10 × 14 | 0.39 | cream / peach | integral | 3 |
| DS | ribbed ring | Ø 26 × 6 | — | red | on axle | 1 |
| DP | grooved end | Ø 24, 2 grooves | — | drum colour | integral | 1 |
| BT | O-ring belt | 2 mm section, ~130 long | — | green / black rubber | stretched | 2 |
| BRG | flanged bearing | 3 × 8 × 3, flange Ø 10 | — | steel | pressed in SP | 2 |
| AXB | socket bolt + washer | M3 × ~8, washer Ø 7 | — | stainless | into the drum's insert/axle | 2 |
| WH | 3-spoke wheel | Ø 42 × 10 | 0.64 × 0.15 | green / black | motor shaft | 2 |
| SW | slide switch | 8 × 4 × 4 + bracket | — | silver | 1 screw | 1 |
| S-SP | socket screw | M2.5, head Ø 4 | — | black | into body | 2 per side |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| SP inner faces ↔ BD sides | screwed | 0 |
| SP top ↔ BD top | plate proud | +2 |
| DR ends ↔ SP inner faces | small end gap (with DS on the left) | 1 |
| LB tips ↔ BD front edge | swept clearance | 3–4 |
| LB tips ↔ floor | above (lowest pass) | ~2 (axle z 24 − tip r 26 = −2 → see §13) |
| LB tips ↔ FG | lobes pass between the fangs (fangs outside x ±33) | ≥ 2 axially |
| BRG ↔ SP | pressed | 0 |
| AXB ↔ DR | threaded into the drum axle (guess) | 0 |
| BT ↔ DP | in grooves | 0 |
| BT ↔ BD top edge | rubbing/close | 0–2 |
| FG tips ↔ floor | touching | 0 |
| WH inner face ↔ SP outer face | near | 1–2 |
| WH top ↔ SP top | wheel proud | +4 |
| WH bottom ↔ floor | touching | 0 |
| BD bottom ↔ floor | above | ~4 |

---

## 6. Mechanism
1. **Weapon**: a belt-driven **three-lobe drum** spinning about X, probably **forward over the top** (the top of the drum moving toward the opponent and down… the usual drum direction is **top moving forward**, so the lobes come down onto opponents and throw them up and back? Standard drums spin so that the front surface moves **upward**, flicking the opponent up). Lobe tip Ø ≈ 52, so at 10 000 rpm the tip speed is about 27 m/s.
2. **Fangs**: fixed floor-touching tips each side of the drum. They get under the opponent and feed it into the drum, and they stop the drum's reaction from tipping the robot's nose down onto the floor.
3. **Drive**: 2WD rear-wheel skid steer; the fangs are the front skids.

---

## 7. Assembly order (suggested rebuild)
1. Print the **body** (box with motor cradles, curved top, belt slot) and the **two side plates**.
2. Fit the **drive motors** in the body; fit the **weapon motor** and its pulley; fit battery, ESCs, receiver.
3. Screw the **side plates** to the body (2 screws each). Mount the **switch** in the left plate.
4. Press the **flanged bearings** into the plate bosses.
5. Fit the two **belts** onto the motor pulley. Place the **drum** between the plates with the **red spacer** on the left, loop the belts into the drum grooves on the right.
6. Insert the **axle bolts + washers** from both sides through the bearings into the drum.
7. Press the **wheels** onto the drive shafts.

---

## 8. Hidden / uncertain list
- The weapon motor type/location and how the 3 left-plate holes relate to it.
- Exact lobe arrangement (staggering) and drum material.
- Spin direction.
- How the drum is held (through-axle vs two stub bolts into inserts).
- All dims ±15 %.

## 9. Coordinate frame (restated)
Origin on the floor under the body centre; +X right; +Y forward; +Z up; mm. Drum axis: the line (y +40, z 24) along X. Wheels at (±44, −24, 21). Side plates at |x| ∈ [33, 38].

## 10. Profiles as math

**10.1 Side plate (YZ outline, x = ±33…±38).** Points in order:
- Rear-bottom (−40, 6) → rear-top (−40, 32) with a fillet r = 6 to (−34, 38) → top edge along z = 38 to (+20, 38).
- Neck dip: arc centre (+26, 44), r = 10, from (+20, 38)… through its lowest point (+26, 34) to (+32, 36) (concave).
- Boss: arc centre A = (+40, 24), r = 13, from θ = 140° (upper rear) clockwise over the top and front down to θ = −30° (front lower): (40 + 13 cos θ, 24 + 13 sin θ).
- Fang front edge (concave claw): from (51, 17.5) curve down to the tip T = (58, 0): quadratic Bézier with control (50, 6).
- Fang lower edge: from T back along z = 0 to (+44, 0), then rising to the plate bottom edge at (+20, 6), then along z = 6 back to (−40, 6).
- Barb (left fang only): a 2 mm step down in the fang's upper edge at y ≈ +48.

**10.2 Drum.** Core: y′² + z′² ≤ 12² (in the drum frame, centred on the axis), for x ∈ [−28, 28]. Lobe k (k = 0, 1, 2) at angle α_k = 120°·k and axial centre c_k ∈ {−14, +14, 0}: the set of points with |x − c_k| ≤ 13 and, in the plane through the axis at angle α_k, a "tongue": radial r ∈ [12, 26 − (13 − √(13² − (x − c_k)²))] (rounded end in X), tangential thickness |t| ≤ 5.

**10.3 Body top.** z_top(y) = 36 − 4·((y + 36)/60)² for y ∈ [−36, +18], then a fillet r = 6 down into the front wall at y = +24.

**10.4 Wheel.** Rim: annulus r ∈ [15, 21], width 10; 3 spokes 4 mm wide at 0°, 120°, 240° from r 4 to r 15; hub r 4.

## 11. Pixel-based measurements (AWS71 native 2069 × 1462; thumbnail ×0.58; ±10 native px)
- Left wheel: x ≈ 40–405, y ≈ 320–845 (≈ 525 px tall). Rear-right wheel: x ≈ 850–1160, y ≈ 40–230 (partly hidden).
- Left side plate: rear corner (330, 370), boss bolt (1050, 800), left fang tip (1410, 1415).
- Bolt washer: ≈ 105 px across (the thumbnail's 60 px).
- Drum core visible length: ≈ 1000 → 1790 native (790 px) at an oblique angle.
- Lobe (front-right): ≈ 420 × 300 native.
- Switch: ≈ 70 × 110 native.

## 12. Several independent estimates

| Quantity | Method A (washer 7 mm) | Method B (W = 66 body) | Method C (wheel 42 mm) | Reconciled |
|---|---|---|---|---|
| px/mm near the boss | 105 / 7 = 15 | — | — | 15 (front plane) |
| Wheel Ø | 525 / 15 = 35 (wheel is nearer the camera → would be larger; so Ø ≤ 35?) | — | assumed 42 | **40** (see §13) |
| Drum core Ø | 24 (core ≈ 360 px / 15) | — | — | **24** |
| Lobe tip radius | core 12 + lobe ≈ 210 px / 15 = 14 → 26 | — | — | **26** |
| Body width | — | 66 | drum length 790 px / cos(45°)/15 ≈ 74 (incl. the end rings) | **66** body, drum + rings 64 |
| Fang reach ahead of the axle | (1410 − 1050) / 15 / cos(30°) ≈ 28?? | — | — | **18–20** (§13) |

## 13. Consistency check
1. **Wheel diameter**: the washer scale gives 35 mm for the near wheel; the wheel sits farther back but closer to the camera laterally. AWS73 shows the wheel slightly taller than the side plate (38) → ≥ 40. **Reconciled: Ø 40**, centre z = 20, top z = 40. Overall height 40 mm.
2. **Lobe vs floor**: with the axle at z = 24 and the tip radius 26, the lobes would hit the floor (−2). Either the axle is higher or the tip radius smaller. The fangs touch the floor ahead, and the drum must clear it. **Reconciled: axle at z = 27, tip radius 25** → 2 mm floor clearance. Boss centre moved to (y +40, z 27).
3. **Fang reach**: the pixel estimate (28 mm ahead of the axle) is inflated because the fang tip is lower and nearer the camera. The cube limit gives: wheels at y −44 (rear edge) to fang tip ≤ y +57. **Reconciled: fang tip at y +58 − 1 = +57**, about 17 mm ahead of the axle. Overall length 101 mm, at the cube limit.
4. **Width**: wheels outer faces ±49 → 98 mm. **Consistent.**
5. **Mass**: body 25 g, side plates 2 × 9 g, drum 18 g (TPU), weapon motor 15 g, ESC 5 g, belts 1 g, bearings/bolts 4 g, 2 drive motors + wheels 30 g, battery 15 g, RX/ESC 7 g, screws 3 g; total ≈ 141 g. **Consistent.**

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Three-lobe drum ("tri-tongue")**
  - Attack: three thick lobes give bigger "bites" than a smooth drum or many small teeth: each hit transfers more energy. Rounded lobe ends are strong (no thin points to snap) and print well. Staggered lobes cover the full width while keeping the drum balanced.
  - Getting under vs contact: the drum is low (2 mm clearance), so it meets the opponent's front edge or wedge lip and flicks it up. Against wedges, the lobes hit the wedge face and the reaction lifts Tritongue's front; the fangs resist that.
  - Adversarial: a TPU drum absorbs return impacts that would crack a PLA drum; chipped lobes (AWS71) show it doing that.
- **Belt drive**: the belt **slips under shock**, protecting the motor and its bearings from impact loads. It also lets the motor sit inside the body, protected, rather than inside the drum. O-ring belts are cheap and quick to replace (green vs black between events).
- **Side plates with bosses**: carry the drum's bearings at both ends, so the drum is supported on both sides: very stiff against impacts. Thick 5 mm plates take the reaction of every hit.
- **Fangs (FG)**
  - Getting under: two floor-touching claws ahead of the drum get under opponents' edges first and steer them into the drum.
  - Adversarial: they protect the drum from being hit from below by an opponent's wedge and stop the drum hitting the floor when the robot rocks forward after a hit. The barb/step on the left fang may catch opponents.
- **Body with curved top**: deflects hits and opponents riding over the drum; keeps the belts running smoothly over the rounded front edge.
- **Large exposed wheels**: invertible driving (the drum still works the other way up if the drum is spun in reverse). The exposed wheels are the weak point to horizontal spinners. The side plates shield the wheels' inner faces only.
- **Switch on the side plate**: easy access without removing anything; mounted high so it is away from floor-level attacks.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Weapon motor | brushless outrunner 1806/2204 class, shaft along X | Ø 22 × 20 | (+14, +12, 22) | medium |
| Weapon pulley | 2-groove pulley Ø 8 | Ø 8 × 6 | on the motor shaft at x +28 | medium |
| Weapon ESC | 12–20 A brushless | 25 × 13 × 5 | (−10, +6, 12) | medium |
| Drive motors | 2 × N20 along X | 12 × 10 × 25 | (±18, −24, 20) | medium |
| Motor cradles | printed pockets + the side plates clamp the gearbox | — | rear of the body | medium |
| Battery | 2S LiPo 300 mAh | 45 × 18 × 12 | across the rear-bottom, (0, −28, 10) | medium |
| Drive ESC / RX | dual brushed ESC + micro rx | 20 × 15 × 4 each | (0, −8, 30) | low |
| Drum axle | two M3 bolts threaded into heat-set inserts at the drum ends, or one through-rod | — | drum axis | medium |
| Wiring | battery → switch (left plate) → ESCs → motors | — | inside | medium |

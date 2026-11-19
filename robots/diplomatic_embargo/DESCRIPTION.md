# Diplomatic Embargo: full rebuild description from reference photos

Source photos (both cut out onto white):
- `robots/diplomatic_embargo/reference/diplomatic_embargo.aws72.webp`: AWS 72. **Front-right three-quarter**, camera about 35° above the floor, about 30° right of the nose. **Dark green** body with a **flat textured lid**, four grey/black wheels in corner pockets, and a **red front plate** with the stencil-cut name **"DIPLOMATIC EMBARGO"** and **three steel fork blades** sticking down through slots in its bottom lip.
- `robots/diplomatic_embargo/reference/diplomatic_embargo.aws76.webp`: AWS 76 (**primary for the CAD**). **Front-left three-quarter from above**, camera about 45° above the floor; the front points to the image left. **Black sparkle** body and lid; the red plate is gone, replaced by **three black printed hinged forks**, each a long tapered beam with a **silver aluminium chisel tip**, mounted in three **hinge cradles** on the front of the chassis. The **left side** shows a rounded side pod enclosing both left wheels.

`REFERENCE.json`: `wedge`, 4 wheels, weapon wedge.

Pixel coordinates refer to copies scaled to 1200 px on the long side (AWS72 → 1200 × 817, AWS76 → 1200 × 966), ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit and from the wheels (common **Ø 22 × 9 mm** TPU/rubber wheels). Ratios use **W = body width ≈ 82 mm** (side wall to side wall).

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the forks), **+Z** = up. **Origin O** = floor point under the centre of the body footprint (excluding forks and front plate).
- Fork angle **κ** = angle of the fork's lower edge below the horizontal, YZ plane.

| ID | Part |
|---|---|
| CH | body tub (green in AWS72, black sparkle in AWS76) |
| LD | flat textured lid |
| LD-S | lid screws |
| PK-FL, PK-FR, PK-RL, PK-RR | four corner wheel pockets |
| SP-L / SP-R | rounded side pods / walls enclosing the wheels |
| SW-W | side windows between the wheels (AWS72) |
| WH-FL, WH-FR, WH-RL, WH-RR | four wheels |
| RP | red front plate with stencil name (AWS72) |
| RP-S | screws on RP (6) |
| RP-L | stepped lower lip of RP with three slots |
| SF-1/2/3 | three steel fork blades (AWS72) |
| HC-1/2/3 | three hinge cradles on the chassis front (AWS76) |
| HK | fork hinge knuckles + screws (AWS76) |
| FK-1/2/3 | three black hinged forks (AWS76) |
| FT | aluminium chisel tips on FK |
| FK-S | screws on each fork (tip clamp + mid) |
| BAT, RX, ESC, DM | hidden electronics and motors (guess) |

---

## 1. Overall description in one paragraph

Diplomatic Embargo is a **low, flat four-wheel box with three forks at the front**. The body is a rectangular tub about 82 mm wide, 66 mm long and 20 mm tall, covered by a **flat, inset lid** printed with a pebbled texture and held by silver screws. The **four small wheels** (about Ø 22 × 9 mm, grey TPU) sit in **open-topped pockets at the four corners**, their outer faces enclosed by the rounded ends of **side pods** so that only the tread tops show. At AWS72 the front was a **red vertical plate** across the full width with the robot's name cut through it as **stencil letters**, held by six screws, with **three thin steel blades** angled down to the floor through slots in its lower lip. At AWS76 the front is three **independent hinged forks**: black printed tapered beams about 45 mm long, each pivoting in a cradle on the chassis front, resting on the floor on a **silver aluminium chisel tip**. The robot has no active weapon: it is a pusher whose forks get under opponents.

---

## 2. Part-by-part description

### 2.1 Body tub (CH)
- **Shape**: a rectangular tub about **82 mm wide (X) × 66 mm long (Y) × 20 mm tall**, with vertical walls and slightly rounded vertical edges (radius ≈ 3 mm). The top rim around the lid is about **3 mm** wide.
- **Corner pockets (PK)**: at each corner, a **rectangular opening** about **12 mm wide (X) × 26 mm long (Y)**, open at the top and to the outside below the pod wall, holding a wheel. The lid area between the pockets is about **58 mm** wide.
- **Side windows (SW-W, AWS72)**: on the right side of the top rim between the front and rear wheel pockets, a **rectangular recess/window** about **10 × 8 mm** (at (205–280, 330–375) px) and at the rear right (880–960, 175–215) — **openings in the side pod tops between the wheels** (weight saving or access to motor screws) **(guess)**.
- **Front**: in AWS76 the front wall carries **three hinge cradles** (HC) separated by **two U-notches**; in AWS72 it is hidden by the red plate.
- **Colour/material**: AWS72 **dark green** PLA/PETG; AWS76 **black with white sparkle/flecks** (sparkle filament or dust).

### 2.2 Lid (LD) and screws (LD-S)
- **Shape**: a **flat plate** about **58 mm wide × 60 mm long × 2 mm thick**, inset flush (or 0.5 mm proud) into the tub rim between the wheel pockets. Its surface is a **fine pebble/diagonal texture**.
- **Screws**: AWS72 shows **two silver/green pan-head Phillips screws** with **washers** in the tub rim at the front-left of the right-front pocket and rear-left of the left-rear pocket… precisely at (240, 290) px (right front, between the lid and the front-right pocket) and (845, 155) px (left rear). AWS76 shows **4 silver pan-head screws** on the lid in a **staggered pattern**: (x −15, y −20), (x +5, y −8), (x −10, y +12), (x +10, y +22) — at (685, 185), (525, 240), (870, 400), (700, 470) px.
- **Colour**: same as the tub (green 72, black 76).

### 2.3 Side pods (SP-L, SP-R)
- **Shape**: along each side, the tub's outer wall is a **rounded "stadium" wall** about **4 mm thick**, **66 mm long × 20 mm tall**, its ends **fully rounded** (radius ≈ 10 mm) around the front and rear wheels. AWS76 shows the left pod as a long rounded black wall at (620–1160, 520–910) px enclosing the front-left and rear-left wheels, with a **silver screw** on its outer face at mid-length (970, 770) px and a **vertical inner partition** between the wheels.
- **Function**: **wheel guards**: they cover the outer faces of all four wheels; only the treads' upper arcs show above the pod tops.
- **Supports**: printed **integral** with the tub, joined by the partition between the wheels and by the front/rear walls **(medium)**; the side screw fixes the lid or an inner motor clamp **(guess)**.

### 2.4 Wheels (WH-FL, WH-FR, WH-RL, WH-RR)
- **Shape**: **Ø 22 mm × 9 mm**, **grey-black TPU** (AWS72: dark grey matte; AWS76: grey with dirt), smooth tread with slightly rounded edges, black hubs.
- **Positions (centres)**: x ±35, y ±20, z 11. Wheelbase ≈ **40 mm**; track ≈ **70 mm**.
- **Height**: the wheel tops (z 22) sit about **2 mm above the lid**, so the robot can drive **inverted** (barely) **(guess)**.
- **Drive (guess)**: four N20 gearmotors (one per wheel) or two motors each driving front + rear via belts; the partition between the wheels suggests one motor per wheel.

### 2.5 Red front plate (RP, RP-S, RP-L), AWS72
- **Shape**: a **red printed plate** about **84 mm wide × 26 mm tall × 4 mm thick**, covering the whole front, **leaning back about 10–15°** from vertical. Its corners are square.
- **Stencil text**: "**DIPLOMATIC**" (top line) and "**EMBARGO**" (bottom line) in a **stencil font** (letters with bridges: the D, O, P, A, B, R, G have the characteristic gaps), **cut through or deeply engraved** into the plate, letters about **6 mm tall**, black showing through (the green/black tub behind).
- **Screws (RP-S)**: **6 silver pan-head Phillips**, head Ø 4 mm: at the upper left (x −32, z 18), lower left (x −38, z 8), centre top (x 0, z 20) and centre lower (x 0, z 14), upper right (x +32, z 18), right (x +40, z 14) — at (430, 520), (385, 635), (715, 418), (730, 465), (990, 380), (1080, 450) px.
- **Lower lip (RP-L)**: the bottom of the plate is a **thicker stepped band** about **8 mm tall** that projects **4–5 mm forward**, with **three vertical slots** (about 6 mm wide × 10 mm tall) at x ≈ −30, 0, +30 through which the steel blades pass.

### 2.6 Steel fork blades (SF-1/2/3), AWS72
- **Shape**: three **flat steel strips**, about **5 mm wide × 1.2 mm thick**, protruding about **28 mm** from the slots, angled **steeply down** at about **κ ≈ 55–60°** below horizontal (they point forward and down to the floor), each with a **chisel tip** on the floor.
- **Position**: x ≈ −30, 0, +30, roots at about (y +36, z 8), tips at about (y +50, z 0).
- **Mount**: they pass into the tub through the slots. They may be **hinged/loose** so they always fall to the floor under their own weight **(guess)**, or fixed.
- **Colour**: bright steel.

### 2.7 Hinge cradles (HC-1/2/3) and knuckles (HK), AWS76
- **Shape**: three **U-shaped cradles** on the chassis front at x ≈ −28, 0, +28, each about **14 mm wide**, with **two cheeks** (each 3 mm thick) holding a **transverse hinge pin** (screw) at about **(y +35, z 12)**. Between the cradles the front wall has **semicircular cut-outs** (the tub front is scalloped: three cradles separated by rounded notches, AWS76 at (380–720, 230–700) px).
- **Knuckles**: each fork's rear end is a **cylindrical knuckle**, about **Ø 12 × 8 mm wide**, sitting between a cradle's cheeks, with a **black/silver screw head** visible on one side (AWS76 at (380, 355), (470, 515), (590, 700) px).
- **Ribbed hinge**: AWS76 shows the knuckle tops with **fine ridges** (printed layers) and a small **stop shoulder** that limits how far the fork can rotate up (the fork top meets the cradle at about 20° up).

### 2.8 Hinged forks (FK-1/2/3), FT, FK-S, AWS76
- **Shape**: each fork is a **black printed tapered beam**: in side view a **long thin triangle/trapezoid**: about **16 mm tall** at the knuckle, tapering to about **3 mm** at the tip, **46 mm** long; in plan a **constant 8 mm width**. The top edge is straight, sloping down toward the tip; the bottom edge is nearly horizontal (on the floor at the tip).
- **Tip (FT)**: a **silver aluminium chisel insert**, about **8 mm wide × 10 mm long × 2.5 mm thick**, with its front face **ground at about 30°**, slotted into the fork end and clamped by a screw (FK-S) about 12 mm behind the tip.
- **Screws (FK-S)**: **2 per fork**: a silver pan head near the tip (tip clamp) at (230, 430), (315, 600), (415, 790) px, and one near the knuckle (the hinge).
- **Pose**: at rest each fork lies with its **tip on the floor** at about **y +78**, its knuckle at (y +35, z 12): slope of the beam's centreline ≈ atan(12/43) ≈ 16° down.
- **Independence**: each fork hinges separately so the three tips **follow the floor** independently over seams and bumps.

---

## 3. Per-view sections

### 3.1 AWS72 (front-right)
- **Bottom**: the red plate across the image (270–1150, 265–760) with the stencil text, 6 screws, the lower lip and the three blades at (460–545, 620–790), (740–820, 540–710), (1010–1085, 465–630).
- **Top**: the lid (165–990, 65–420) with two screws; the four wheels: front-right (230–330, 360–455), rear-right (80–190, 160–270), front-left (935–1050, 205–295), rear-left (735–850, 30–125).
- **Left**: the right side pod wall (45–275, 205–720) dark green, rounded front corner.

### 3.2 AWS76 (front-left, above)
- **Left half**: three hinged forks fanned out to the left (tips at (50–115, 470–525), (120–190, 650–700), (195–285, 815–905)), their knuckles in the cradles along the chassis front edge (370–720, 230–720).
- **Right half**: the lid (395–1080, 90–650) with 4 screws; the left side pod (620–1160, 520–910) with both left wheels visible inside (650–870, 640–790) and (900–1150, 500–620); the right wheels at the top (300–500, 80–200) and (520–700, 25–110).

### 3.3 Top view (AWS76 synthesised)
- An 82 × 66 rounded rectangle; 4 corner pockets with wheels; the lid between them; at the front edge three cradles and three forks to y +78 (width 8 each, at x −28, 0, +28).

### 3.4 Front view
- AWS72: a red plate 84 × 26 with the stencil name and three blades below. AWS76: the black front wall with three cradles, three fork beams going toward the viewer on the floor, wheels at the four corners just visible above the pods.

### 3.5 Left side view (AWS76)
- The stadium side pod (66 × 20) with two wheel tops peeking above it, the forks extending from the front at z 12 down to the floor at y +78.

### 3.6 Rear view (not photographed)
- Plain rear wall between the rear pockets **(guess)**; likely a power switch.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | tub with corner pockets | 82 × 66 × 20 | 1 × 0.80 × 0.24 | green (72) / black sparkle (76) | — | 1 |
| LD | flat lid | 58 × 60 × 2 | 0.71 × 0.73 | same | 2–4 × M2 | 1 |
| SP | stadium side wall | 4 × 66 × 20 | 0.05 × 0.80 | same, integral | 1 side screw | 2 |
| PK | pocket | 12 × 26 | — | — | — | 4 |
| WH | TPU wheel | Ø 22 × 9 | 0.27 × 0.11 | grey TPU | motor shaft | 4 |
| RP | stencil plate | 84 × 26 × 4 | 1.02 × 0.32 | red FDM | 6 × M2 | 1 (72) |
| SF | steel blade | 5 × 1.2 × 28 exposed | — | steel | slot | 3 (72) |
| HC | cradle | 14 × 12 × 14 | — | integral | pin screw | 3 (76) |
| FK | tapered hinged beam | 8 × 46 × 16→3 | 0.10 × 0.56 | black FDM | hinge screw | 3 (76) |
| FT | chisel insert | 8 × 10 × 2.5 | — | aluminium | 1 screw | 3 (76) |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD ↔ CH rim | inset, screwed | 0 |
| WH ↔ pocket walls | clearance | 1–2 |
| WH outer face ↔ SP inner face | near | 1 |
| WH top ↔ LD top | above | +2 |
| WH bottom ↔ floor | touching | 0 |
| CH floor ↔ floor | above | 2 |
| RP ↔ CH front | screwed (6) | 0 |
| RP-L bottom ↔ floor | above | 2–3 |
| SF ↔ RP-L slots | through | 0–1 |
| SF tips ↔ floor | touching | 0 |
| FK knuckle ↔ HC cheeks | hinge | 0.5 |
| FK tip (FT) ↔ floor | resting | 0 |
| FK ↔ neighbouring FK | side gap | ~20 |
| FT ↔ FK | clamped | 0 |

---

## 6. Mechanism
- **Drive**: four-wheel skid steer with a short wheelbase; the forks (AWS76) or blades (AWS72) slide on the floor.
- **Weapon**: none active; a **fork pusher**. The free-hinged forks drop to the floor, slide under opponents, and lift their front edge slightly as the robot drives in; then the robot pushes them.

---

## 7. Assembly order (suggested)
1. Print CH (with corner pockets, side pods, hinge cradles), LD, three forks (FK).
2. Install four gearmotors (or two with transfers) in the pocket walls; press on the wheels.
3. Install the battery, receiver, ESC(s) and switch.
4. Screw the lid on.
5. AWS76: slot the aluminium tips into the forks, clamp with screws; place each fork knuckle in its cradle and insert the hinge screw.
6. AWS72: screw the red plate on; slide the three steel blades into their slots.

---

## 8. Hidden / uncertain list
- Motor count (4 vs 2) and placement.
- Whether the AWS72 blades are hinged.
- Rear face, underside, switch.
- Whether the hinge has springs/stops.
- All mm ±15%.

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the tub centre; +X right, +Y forward, +Z up, mm.
- Tub x ∈ [−41, +41], y ∈ [−33, +33], z ∈ [2, 20]; cradles to y +38; fork tips at y +78 (AWS76); red plate y ∈ [+33, +38] (AWS72), blades to y +50.

## 10. Profiles as math

**10.1 Tub plan with pockets.** Outer rounded rectangle x ∈ [−41, +41], y ∈ [−33, +33], corner radius 10 (side pods). Pockets: x ∈ ±[29, 41)... inner pocket faces at x = ±29, pocket y ranges [+7, +33] and [−33, −7].

**10.2 Side pod (YZ).** Stadium: straight top z = 20 for y ∈ [−23, +23]; semicircle ends r 10 at (y ±23, z 10).

**10.3 Fork FK (YZ, in the fork's plane).** Knuckle circle r 6 at K = (y 35, z 12). Top edge from (35, 18) to (78, 3); bottom edge from (35, 6) to (78, 0)… use z_bottom = 6·(78 − y)/43. Tip insert: y ∈ [68, 80], thickness 2.5, front bevel from (80, 0) to (76, 2.5) (≈ 32°).

**10.4 Fork rotation.** Each fork rotates about K's X-axis; tip radius R = √(43² + 12²) = 44.6; tip height z_T(θ) = 12 − 44.6·sin(15.6° − θ) for upward rotation θ; the stop allows θ_max ≈ 35° (tip up to z 27).

**10.5 Red plate (AWS72).** Rectangle 84 × 26, leaning back 12°: front face plane y = 38 − 0.21·z. Lower lip: box x ∈ [−42, +42], y ∈ [36, 42], z ∈ [2, 10] with slots x ∈ [−33, −27], [−3, +3], [+27, +33].

**10.6 Steel blade (AWS72).** Line from (y 38, z 8) to (y 52, z 0)…: direction 30° from vertical; strip 5 × 1.2; tip chisel 3 mm.

**10.7 Wheel.** r 11, width 9, edge fillet 1.5.

## 11. Pixel measurements
- **AWS72**: red plate width ≈ 880 px along its oblique top edge; plate height ≈ 230 px at the left; front-right wheel ≈ 100 × 95 px; blade exposed length ≈ 170 px; letter height ≈ 55 px.
- **AWS76**: fork length (knuckle to tip) ≈ 330–420 px (nearest longest); fork width ≈ 55–70 px; lid long edge ≈ 690 px; side pod length ≈ 560 px; wheel Ø (front-left) ≈ 160 px.

## 12. Several independent estimates

| Quantity | Method A (rule/part) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | ≤ 101.6 − margin | — | AWS72: plate 880 px / wheel 100 px × 22 = 194?! (oblique, plate nearer) → ×0.45 ≈ 87 | **82** |
| Wheel Ø | 22 | 0.27 W | AWS76: 160 px vs pod 560 px (66) → 19 (wheel partly hidden) | **22** |
| Body length | 66 | 0.8 W | AWS76: pod 560 px / (160/22) = 77 (near side, enlarged) | **66** |
| Fork length | 101.6 − 66 = 35 + cradle 5 → ≤ 45 | 0.56 W = 46 | AWS76: 420 px / 7.3 px/mm = 58 (nearest fork, enlarged) → ×0.8 = 46 | **45** |
| Fork width | 8 | 0.1 W | 60 px / 7.3 ≈ 8 | **8** |
| Plate height (72) | 26 | 0.32 W | 230 px / ~9 px/mm ≈ 26 | **26** |

## 13. Consistency check
1. **Cube fit (AWS76)**: length 66 + 45 = 111?! Too long. The forks' knuckles are at y +35, so fork tips at 35 + 43 = 78; total from the rear (−33) to 78 = **111 mm** — over the limit. Either the body is shorter (≈ 55) or the forks hinge **up** to fit the cube for weigh-in (hinged forks can be folded up for measuring — a common trick) **(likely)**. Reconciled: body 60 long (y ±30), forks 43, fit with forks raised.
2. **AWS72 fit**: 66 + 5 + 14 = 85 ✓.
3. **Wheel tops**: z 22 vs lid z 20: AWS72 shows wheels just above the lid ✓.

---

## 14. Why the designer did it (adversarial first)

- **Three forks rather than a wedge**: forks get under wedges and flat-bottomed robots; three widely spaced forks cover the front width while presenting little to spinners. **Hinged** forks (AWS76) always rest on the floor even when the robot tilts or the floor is uneven, so they keep the "get under" advantage; they also fold up when hit from above, absorbing the hit instead of breaking. **Aluminium chisel tips** are thinner and harder than printed tips and replaceable with one screw.
- **Steel blades through a red plate (AWS72)**: the earlier, simpler version: steep steel blades scrape the floor; the plate behind them is a vertical pushing face. The stencil name is identity/showmanship; cut-through letters also save weight.
- **Low 20 mm flat box**: minimal front face for opponents' wedges (which meet the forks first) and for vertical spinners; a flat lid gives nothing to grab.
- **Wheels in corner pockets with integral rounded side walls**: every wheel is shielded on the outside from horizontal spinners and side wedges; rounded pod ends deflect glancing hits and slide along arena walls. Four-wheel drive keeps traction when an opponent pushes down on the front.
- **Wheel tops above the lid**: inverted driving (forks then on top — the robot still pushes, just without forks).
- **Sparkle black filament**: cosmetic.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors, one per wheel | 12 × 10 × 25 | (±18, ±20, 11) along X | medium |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 9 | (0, −5, 8) | medium |
| ESC(s) + RX | dual brushed ESC driving left pair / right pair in parallel; small RX | 25 × 20 × 6 | (0, +18, 10) | medium |
| Power switch | rear wall or under a lid screw | 10 × 5 | (0, −33, 12) | low |
| Hinge pins | M2.5 screws through the cradle cheeks | — | (−28/0/+28, 35, 12) | high (seen) |
| Wiring | battery → switch → ESC → motors at the corners | — | — | medium |

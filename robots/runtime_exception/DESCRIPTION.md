# Runtime Exception: full rebuild description from reference photos

Source photos (in `robots/runtime_exception/reference/`):
- `runtime_exception.aws70.webp` (761 × 612 px): a pit snapshot on a grey table, not cut out. A **three-quarter view from the front-right, about 40° above horizontal**. The robot wears a **bent sheet-metal plough wedge** and a **metal top sheet**. Other objects (a clear box at the top left, another robot at the right edge) are not part of it.
- `runtime_exception.aws72.webp` (1193 × 827 px): cut out (strong green fringe from the backdrop). A **three-quarter view from the front-right, about 35° above horizontal**, front toward the lower left. The robot is **stripped**: no wedge, no top sheet. It shows the **clear polycarbonate top plate**, the **two black printed rails ("spine")**, two **clear polycarbonate forks** at the front, and the electronics through the clear plate.
- `runtime_exception.aws74.webp` (1381 × 946 px): cut out. A **three-quarter view from the front-left, about 30° above horizontal**. The plough wedge and top sheet are fitted, as in AWS70. The green cast makes the metal top sheet look green; it is **bare metal** (compare AWS70, where the same sheet is grey).

Everything stated as fact is read from those photos. Anything inferred is marked **(guess)** with a confidence. Dimensions are **estimates in mm**, scaled from the AWS antweight limits (150 g, fits a 101.6 mm cube) and photo proportions, and checked against the project spec draft (`spec.json`: chassis, top plate, two wheels with two drive motors, a "spine", a scoop with a strut, battery, a combined RX/ESC and a switch). **W = chassis tub width ≈ 80 mm** is the ratio base.

Runtime Exception is a **two-wheel wedge / pusher** with **interchangeable front attachments** on a pair of top rails: a **wide bent-metal plough wedge** (AWS70/74) or **two clear polycarbonate forks** (AWS72).

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) under the centre of the black chassis tub (mid-width, mid-length, attachments excluded).
- **+X** = robot's right, **+Y** = forward (toward the wedge/forks), **+Z** = up. Units mm.
- AWS70 and AWS72: camera at the **front-right**, front toward the image lower left / lower centre. The robot's right side is the near long side. AWS74: camera at the **front-left**; the robot's left wheel and clear guard are at the image left.

Part IDs:

| ID | Part |
|---|---|
| CH | black printed chassis tub (lower body) |
| CH-C | chassis front corner chamfers |
| TP | clear polycarbonate top plate |
| TP-N | notches in TP for the wheels |
| GD-L / GD-R | clear polycarbonate wheel guards (outboard of the wheels) |
| GT | black tape joining the guards to the chassis |
| RL-L / RL-R | black printed top rails ("spine") with hole rows |
| RL-T | raised rear tails of the rails |
| VC-L / VC-R | black hook-and-loop (Velcro) pads on TP |
| FK-L / FK-R | clear polycarbonate forks (AWS72) |
| S-FK | fork screws (2 per fork) |
| WD | bent sheet-metal plough wedge (AWS70/74) |
| WD-C | wedge centre facet |
| WD-S | wedge side facets |
| S-WD | wedge screws (4, socket heads) |
| TS | metal top sheet (AWS70/74) |
| S-TS | top-sheet screws (5, dome/button heads) |
| WH-L / WH-R | foam-tyred drive wheels |
| HB-L / HB-R | wheel hubs (black ring hubs) |
| DS-x | drive actuators: coreless servos or gearmotors (labelled part visible) |
| BAT | battery (red-wrapped, visible) |
| WR | visible wiring (red, servo-colour leads, yellow) |
| CN | white/pink connector plugs (visible) |
| RX/ESC, SWT | receiver/ESC and switch (partly visible / hidden) |
| SC-S | scoop strut (hidden, spec) |

---

## 1. Overall description in one paragraph

Runtime Exception is a **low, flat two-wheeled wedge** about **80 mm wide** in the body, **≈ 100 mm wide** at the plough, and **≈ 95 mm long**. Its body is a **black printed tub** about **20 mm tall**, rectangular at the rear with **45° chamfered front corners** (a hexagonal plan). The tub is closed by a **clear polycarbonate top plate** through which the **wiring, a red-wrapped battery and a servo-style drive unit labelled "coreless 2S8 multivoltage (6.0V–8.4V)"** can be seen. Two large **foam-tyred wheels (Ø ≈ 32 mm)** stand at the sides at about mid-length, taller than the body, each sheltered by a **bent clear-polycarbonate guard**. On top of the clear plate run **two parallel black printed rails** with rows of small holes; their **rear ends rise into short tails**. The rails are the mounting points for the front weapon: either a **wide three-facet bent-metal plough** fixed by four socket screws, plus a **dented metal top sheet** screwed onto the rails (AWS70/74), or **two clear polycarbonate forks** sloping from the rails' front ends to the floor (AWS72).

---

## 2. Part-by-part description

### 2.1 Chassis tub (CH)
- **Plan**: a hexagon: rear rectangle **x ∈ [−40, +40]**, **y ∈ [−45, +20]**, then **45° chamfers CH-C** from (±40, +20) to (±25, +35), and a straight front wall at **y = +35** for x ∈ [−25, +25].
- **Height**: **≈ 18–20 mm** (z ≈ 2 to 21). AWS72 shows the right side and the chamfer as matt black faces about **0.25 of the width** tall.
- **Colour / material**: matt black FDM with fine layer lines. The front-right chamfer in AWS72 (px ≈ (560–910, 560–700)) is a large plain face; the front wall (px ≈ (300–560, 560–700)) is partly hidden by the forks.
- **Side detail**: at the rear-right corner in AWS72 (px ≈ (900–960, 560–700)) the side has a **black strap or taped joint** (GT) where the clear guard meets the tub.
- **Front wall hardware (AWS72)**: under the forks there are **two black horizontal rods/bolts** (px ≈ (160–360, 390–440) and (320–440, 520–690)), plus a **silver screw end** (px ≈ (540–560, 680–700)). They look like **long M3 bolts or threaded rods** running across the front, sticking out on the left (px (160, 405)). Possibly the **scoop strut / hinge rod** for the front attachment **(guess, medium)**.

### 2.2 Clear top plate (TP)
- **Material**: **clear polycarbonate**, about **1.5–2 mm** thick, with slightly frosted, scuffed edges.
- **Plan**: matches the tub's hexagon (front chamfers), extending **≈ 2 mm** beyond the tub walls, with **rectangular notches TP-N** around each wheel (AWS72 left notch px ≈ (420–560, 110–190); right notch px ≈ (880–960, 380–460)).
- **Fasteners**: small **black screws** at the corners (AWS72 px (285, 185), (555, 110), (880, 440), (885, 550)); about **6** in total **(guess)**.
- **Printed/label area**: at the right rear (AWS72 px ≈ (600–760, 450–560)) a **rectangle with white printing** reads **"coreless", "2S8", "multivoltage", "(6.0V~8.4V)"** next to a striped logo. This is a **label on a component directly under the clear plate** (the plate is clear, so we read the component's own label). The style matches a **micro servo** case label **(guess, medium)**.

### 2.3 Wheel guards (GD-L, GD-R) and tape (GT)
- **Shape**: each wheel has a **clear polycarbonate guard**: a **bent strip** forming the **outer wall** of the wheel well, about **2 mm thick**, **≈ 36 mm long (Y) × 22 mm tall**, with a **top flange** that folds inward and overlaps the top plate (AWS72's right guard px ≈ (1000–1150, 420–580); AWS74's left guard px ≈ (60–240, 250–470)).
- **Coverage**: the guard covers the **lower ≈ 2/3 of the wheel's outer face**; the top of the tyre stands above it.
- **Guard-to-chassis supports**: (1) the top flange is **screwed to the top plate** (a screw at the guard's front corner in AWS72 px (885, 550)); (2) **black tape GT** (gaffer or electrical tape, ≈ 10 mm wide) wraps the guard's lower front corner onto the tub side (AWS72 px (980–1020, 520–600); AWS74 px (150–200, 400–470)). So the guards are **separate parts, held by screws plus tape**.

### 2.4 Top rails (RL-L, RL-R) and tails (RL-T)
- **Shape**: two **black printed bars** running fore-aft, parallel, at **x ≈ ±14** (centres), each about **12 mm wide × 8 mm tall × 70 mm long** (y ≈ −40 to +30). Their tops are flat.
- **Holes**: each rail has **two rows of small holes** (Ø ≈ 2 mm) along its top, about **6 per row** at **≈ 10 mm** pitch (AWS72 px: left rail holes from (440, 175) to (640, 200), right rail (650, 320) to (830, 300)). They are **screw holes for the top sheet** and the front attachments **(guess, high)**.
- **Tails RL-T**: at the rear, each rail **rises into a raised tail** about **10 mm tall above the rail top**, with a **sloped front face** and a flat top (AWS72 px (650–740, 100–190) and (820–930, 205–290); AWS74 px (370–500, 110–180) and (620–750, 60–110); AWS70 px (330–420, 20–70)). They stick up **above the top sheet** when it is fitted.
- **Front ends**: the rails end in a **square face** at the front, at y ≈ +30, just behind the tub's front wall. The fork plates (AWS72) and the plough (AWS70/74) are bolted there.
- **Gap between rails**: ≈ 16 mm, through which the clear plate and wires show.

### 2.5 Velcro pads (VC-L, VC-R)
- Two **black rectangles with a fuzzy texture**, about **14 × 10 mm**, stuck on the clear plate **just inboard of each wheel notch** (AWS72 px (440–560, 140–190) and (800–920, 340–400)). They are **hook-and-loop pads**: probably the battery or ESC is velcroed under the plate, or the pads stop the top sheet rattling **(guess, low–medium)**.

### 2.6 Forks (FK-L, FK-R), AWS72 only
- **Shape**: two **flat clear polycarbonate strips**, each about **18 mm wide × 50 mm long × 2.5 mm thick**, with **square ends**.
- **Mount**: each is bolted to the **front end/underside of a rail** by **two black socket screws S-FK** (head Ø ≈ 4 mm) about **8 mm apart along the strip** (AWS72 px (275, 395)/(310, 420) and (425, 500)/(475, 540)). The upper part of each fork, around the screws, is **purple-tinted and dimpled** (a **purple vinyl wrap or melted/textured patch**).
- **Angle**: the forks slope **down and forward at ≈ 30°** from their mount (z ≈ 20, y ≈ +30) to the floor at **y ≈ +72**.
- **Tips**: the lower ≈ 15 mm of each fork is **scratched white**, with **fine longitudinal scratches** from scraping on arena floors (px ≈ (120–260, 470–600) and (270–420, 560–740)).
- **Spacing**: centres at x ≈ ±14, inner gap ≈ 10 mm, outer edges at x ≈ ±23.

### 2.7 Plough wedge (WD), AWS70/74
- **Material**: **bare sheet metal**, about **0.8–1.0 mm** thick, bright and heavily scratched. Most likely **stainless steel** or **hard aluminium** **(guess)**. The edges are slightly ragged and the lower edges show small dents.
- **Shape**: a sheet folded into **three facets**:
  - **WD-C (centre facet)**: a trapezoid, **≈ 56 mm wide at the top** and **≈ 64 mm at the bottom**, sloping down at **≈ 35–40°** from the top edge (z ≈ 22, y ≈ +30) to the floor (y ≈ +58).
  - **WD-S (side facets)**: on each side, a facet folded back at about **35–45°** in plan, running from the centre facet's edge out and back to the tub's side, also sloping to the floor. In AWS74 the near (left) side facet is large and seen almost square (px ≈ (290–650, 440–930)); in AWS70 the right side facet is seen (px ≈ (640–750, 210–460)).
  - Overall: a **plough / snowplough shape** that covers the front and both front corners, **≈ 100 mm wide** at the floor.
- **Fixing**: **4 small socket button screws S-WD** (silver, head Ø ≈ 4 mm), in **two pairs**, one pair under each rail's front end, along the wedge's top region (AWS74 px (720, 520)/(795, 500) and (990, 437)/(1050, 428); AWS70 px (350, 405)/(385, 393) and (520, 347)/(556, 336)). So the wedge hangs from the rails.
- **Gap**: between the wedge's top edge and the top sheet's front edge, a **dark gap of ≈ 5–8 mm** shows the black rails and tub (AWS70 px (300–560, 260–340); AWS74 px (620–1000, 340–430)).

### 2.8 Metal top sheet (TS), AWS70/74
- **Material**: **bare thin metal sheet**, about **0.5–0.8 mm** thick (aluminium or thin titanium), **heavily dented** and scratched, with a **wavy, buckled** surface from hits.
- **Plan**: roughly **80 × 70 mm**, a rectangle with **chamfered front corners** (matching the tub) and a **notch at one rear corner** where it clears the wheel (AWS74 px ≈ (380, 300)).
- **Fixing**: **5 dome/button-head screws S-TS** (silver), arranged as two pairs along the rails plus one (AWS74 px (465, 205), (520, 262), (590, 322), (765, 128), (828, 182), (900, 238): ≈ 6 heads; AWS70 px (250, 210), (285, 265), (445, 150), (485, 202), plus two small holes at (215, 160) and (420, 95)). Reconciled: **6 screws, 3 per rail**, plus **2 spare holes**.
- **Position**: sits **on top of the rails** (z ≈ 30), so it is ≈ 9 mm above the clear plate. The rail tails stick up through/behind it.

### 2.9 Wheels (WH-L, WH-R) and hubs (HB)
- **Tyre**: a **grey-brown foam** (sponge) tyre with a fuzzy, dusty surface, **Ø ≈ 32 mm × 10 mm wide**, with slightly rounded edges.
- **Hub**: a **black printed ring hub** with a **large central opening** (≈ Ø 14), so the tyre looks like a thick ring (AWS72 right wheel px ≈ (890–1110, 380–550); AWS74 left wheel px ≈ (140–260, 230–400)). Through the hub opening, a **lighter part** (the output horn or a shaft coupler) is visible.
- **Position (centres)**: **(±46, −10, 16)**. Track ≈ 92 (centres), outer faces at x ≈ ±51. The tyre tops (z ≈ 32) stand **≈ 2 mm above the top sheet** and **≈ 10 mm above the clear plate**, so the robot **drives inverted** on its wheel tops and rail tails.
- **Drive**: see §13.

### 2.10 Visible electronics and wiring
- **Battery BAT**: a **red-wrapped pack** with red silicone leads at the left-front under the clear plate (AWS72 px (270–420, 230–290)) **(guess: 2S LiPo)**.
- **Servo-style leads**: **brown/red/orange** three-wire leads loop at the left rear and right side (AWS72 px (570–680, 140–230) and (740–790, 380–560)); a **yellow** wire loop near the centre-rear (px (690–760, 260–300)).
- **Connectors CN**: a **white/pink plug pair** (servo connectors or a JST link) near the centre (px (560–640, 290–340)).
- **Blue part**: a **blue heat-shrunk component** (an ESC or receiver) under the left rail (px (410–450, 360–400)).
- **Switch**: not identified. The white plug pair could be a **link** **(guess, low)**.

---

## 3. Per-view sections

### 3.1 AWS72 (front-right, stripped, ≈ 35° above)
- **Silhouette**: a flat hexagonal slab with two tall foam wheels at the sides and two forks sticking out at the front-left.
- **Top**: the clear plate, two black rails with holes and raised tails, velcro pads, wiring, the labelled component, the red battery.
- **Front**: the forks with purple-tinted bolted ends and scratched tips; the two black bars/bolts across the front under them.
- **Right side**: the black chamfer and side face, the clear guard, the tape.

### 3.2 AWS70 (front-right, armoured, ≈ 40° above)
- **Silhouette**: a sheet-metal box: the plough wedge across the bottom (px x 100–750, y 200–590) and the top sheet above it (px x 60–670, y 30–350), both bright and scratched. Two wheels at the left and right edges, the rail tails at the top.

### 3.3 AWS74 (front-left, armoured, ≈ 30° above)
- The same as AWS70 from the other side: the plough's near (left) facet is large, the 4 wedge screws in two pairs, the dented top sheet with 6 screws, the left wheel in its clear guard with tape, the right wheel at the top right, two rail tails at the top.

### 3.4 Top view (synthesised)
- The hexagonal tub 80 × 80 with the clear plate, two rails at x ±14, wheels (10 × 32) at x ±46, y −10 in notches, guards outside them. Front attachment ahead: a 100 mm plough trapezoid (y +30 to +58) or two 18 × 42 forks (to y +72).

### 3.5 Side view (synthesised)
- A 20 mm tall black slab; the Ø 32 wheel at mid-rear standing above it; the clear guard over the lower part of the wheel; the rails and tails on top; the plough or fork sloping down at the front.

### 3.6 Rear view (not photographed)
- The tub rear wall, the wheels at both sides, the two rail tails standing up. Probably the switch or link **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | hexagonal tub | 80 × 80 × 19 | 1 × 1 × 0.24 | black FDM | — | 1 |
| TP | clear plate | 84 × 82 × 1.8 | 1.05 | clear PC | ≈ 6 black screws | 1 |
| GD | bent clear guard | 36 × 22 × 2 + flange | 0.45 | clear PC | screw + tape | 2 |
| GT | tape | 10 wide | — | black gaffer | wrapped | 2 |
| RL | rail with tail | 12 × 70 × 8 (+10 tail) | 0.15 × 0.88 | black FDM | to TP/CH (guess, screws from below) | 2 |
| VC | pad | 14 × 10 | — | black velcro | adhesive | 2 |
| FK | flat strip | 18 × 50 × 2.5 | 0.23 × 0.63 | clear PC + purple patch | 2 socket screws each | 2 (AWS72) |
| WD | 3-facet plough | 100 wide × 32 slope × 0.9 | 1.25 | stainless/aluminium | 4 socket screws | 1 (AWS70/74) |
| TS | dented sheet | 80 × 70 × 0.6 | 1 × 0.88 | aluminium/thin metal | 6 dome screws | 1 (AWS70/74) |
| WH | foam tyre on ring hub | Ø 32 × 10 | 0.4 | grey foam + black hub | on the drive output | 2 |
| BAT | pack | 35 × 18 × 10 (guess) | — | red wrap | under TP | 1 |

---

## 5. Contact / gap matrix (estimated mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP ↔ CH wall tops | screwed | 0 |
| RL bottom ↔ TP top | screwed (guess) | 0 |
| TS ↔ RL tops | screwed | 0 |
| TS front edge ↔ WD top edge | gap | 5–8 |
| WD top ↔ RL front ends | screwed (4) | 0 |
| WD lower edge ↔ floor | touching | 0 |
| WD side facets ↔ WH front | clearance | ≈ 5 |
| FK upper end ↔ RL front | screwed (2 each) | 0 |
| FK tip ↔ floor | touching | 0 |
| FK-L ↔ FK-R | gap | ≈ 10 |
| GD flange ↔ TP | screwed | 0 |
| GD ↔ CH side | taped | 0 |
| WH outer face ↔ GD inner face | running gap | 1–2 |
| WH inner face ↔ CH side / notch edge | running gap | 1–3 |
| WH top ↔ TS top | stands proud | +2 |
| WH top ↔ RL-T top | about level | 0 ± 2 |
| WH bottom ↔ floor | contact | 0 |
| CH floor ↔ floor | clearance | ≈ 2 |

---

## 6. Mechanism

1. **Drive**: two wheels at mid-rear, **skid steer**. With the wheels slightly behind the middle, the front attachment (plough or forks) carries the front of the robot on the floor, giving a three- or four-point stance.
2. **Weapon**: none active. The **plough** gets under and deflects opponents; the **forks** get under robots with gaps at their front edges.
3. **Invertibility**: yes. The wheels (Ø 32) are ≈ 12 mm taller than the tub, and the rail tails and top sheet are below the wheel tops. Inverted, the plough's lower edge is at the top and does nothing, but the robot can still push and drive.

---

## 7. Assembly order (suggested rebuild)

1. Print **CH** (hexagonal tub, floor on the bed).
2. Fit the two **drive units** (coreless servos converted to continuous rotation, or gearmotors) in **printed pockets** at the sides, outputs pointing out. Fit the **ring hubs** and **foam tyres**.
3. Install the **battery, RX/ESC, switch**; route the wires; velcro the battery.
4. Screw on the **clear top plate TP**. Fit the **clear guards GD** (screws through the flanges) and tape their lower corners.
5. Screw the **rails RL** onto TP (from below into the rails, guess).
6. Either bolt the **forks FK** to the rail fronts (2 screws each), or bolt the **plough WD** (4 screws) and the **top sheet TS** (6 screws).

---

## 8. Profiles as math (for rebuilding curves)

**8.1 Tub plan (XY).** Polygon (−40, −45) → (+40, −45) → (+40, +20) → (+25, +35) → (−25, +35) → (−40, +20) → close. Chamfer lines: **y = 20 + (40 − |x|)** for |x| ∈ [25, 40].

**8.2 Rail side profile (YZ, x ∈ [±8, ±20]).** Bottom z = 21 (on TP). Top z = 29 for y ∈ [−28, +30]. Tail: from (y −28, z 29) rising along **z = 29 + 0.9·(−28 − y)** to (−39, 39), flat top to (−45, 39), vertical rear face down to z = 21.

**8.3 Plough WD (developed as three planes).**
- Centre facet plane through (x ±28, y +30, z 22) and (x ±32, y +58, z 0): normal tilted forward; slope **atan(22/28) ≈ 38°**.
- Side facet (right; mirror for left): quadrilateral (+28, +30, 22) → (+40, +20, 22) → (+50, +40, 0) → (+32, +58, 0). Its fold line with the centre facet is the line from (+28, +30, 22) to (+32, +58, 0).
- Sheet thickness 0.9. Bottom edge in plan: (−32, +58) → (+32, +58) → (+50, +40) and mirror, i.e. **a flat-fronted trapezoid with 45° corners**.

**8.4 Fork (YZ, x ∈ [±5, ±23]).** Strip from (y +26, z 22) to (y +72, z 0): **z = 22 − 0.478·(y − 26)** (≈ 25.6°), thickness 2.5. Bolt holes Ø 2.5 at 4 mm and 12 mm from the upper end.

**8.5 Wheel.** Tyre: annulus r_out = 16, r_in = 11, width 10, edge fillet 2. Hub: ring r_out = 11, r_in = 7, width 8, with 3 spokes or a central boss **(guess)**.

**8.6 Guard (clear, right).** A plate in the plane x = +53 (YZ), y ∈ [−28, +8], z ∈ [3, 23], with a top flange folded 90° inward: x ∈ [+44, +53] at z = 23, y ∈ [−28, +8], minus the wheel slot x ∈ [+45, +52], y ∈ [−26, +6] **(the flange must leave the tyre top free)**.

---

## 9. Pixel-based measurements (independent check)

**AWS72 (1193 × 827):**
- Right wheel ellipse: px x 890–1110, y 380–550 (≈ 220 × 170 px). Left wheel: px x 350–545, y 60–200.
- Rails: left rail from px (310, 300) to (740, 120) (≈ 470 px), width ≈ 60 px. Right rail from px (480, 430) to (930, 250).
- Forks: left fork px (110–380, 330–610), ≈ 75 px wide; right fork (270–560, 420–760), ≈ 85 px wide.
- Right chamfer face: px (560–910, 560–700), ≈ 140 px tall.
- Label text height ≈ 12 px per line.

**AWS74 (1381 × 946):**
- Plough near facet: px (290–650, 440–930). Plough front edge: px (290, 600) to (1330, 590).
- Top sheet: px (230–1170, 60–440).
- Left wheel: px (140–265, 225–400). Right wheel: px (890–1070, 80–230).
- Wedge screws: ≈ 30 px heads.

**AWS70 (761 × 612):**
- Plough: px (100–750, 210–590). Top sheet: px (60–670, 30–350).
- Wheels: left px (45–135, 175–295), right px (545–640, 30–115).

---

## 10. Several independent estimates of key quantities

| Quantity | Method A (limits / spec) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Wheel Ø | — | wheel ≈ 1.6 × tub height (AWS72 right side) → 1.6 × 19 = 30 | AWS72 ellipse major 220 px vs rail length 470 px for 70 mm → 32.8 | **32** |
| Tub width | cube; wheels outside → tub ≤ 101.6 − 2 × 12 = 78 | track ≈ 1.15 W | AWS70: top sheet ≈ 0.8 × plough width → 80 if plough 100 | **80** |
| Rail length | — | 0.88 W | 470 px ≈ rail; reference = itself | **70** |
| Fork length | — | ≈ 0.7 × rail length | AWS72: left fork 360 px long vs rail 470 px → 54 | **50** (projected 54 includes perspective toward the camera) |
| Fork width | — | 1.5 × rail width (12) = 18 | 75–85 px / 6.7 px/mm (rail scale) = 11–13 (the far fork) to 18 (near) | **18** |
| Plough width | ≤ 101.6 | 1.25 W = 100 | AWS74: 1040 px front edge vs top sheet 940 px (80) → 88 (the near facet is foreshortened) | **100** |
| Plough slope | 30–40° typical | AWS70 face looks steep (≈ 40°) | rise 22 over run 28 → 38° | **38°** |
| Tub height | spec ≈ 20 | 0.24 W = 19 | AWS72 chamfer face 140 px / 6.7 = 21 | **19** |

---

## 11. Consistency check: conflicts and reconciliation

1. **Wheel position.** In AWS72 the left wheel appears near the rear and the right wheel near mid-length because of the oblique view. On a two-wheel robot they share an axle line. **Reconciled: both at y = −10.**
2. **Plough width vs cube.** 100 mm plough plus 80 mm tub length plus 23 mm plough reach ≈ 103 mm long overall: **borderline**. With the plough reaching y = +58 and the tub rear at −45, the length is **103 mm**; shorten the tub rear to −42 → **100 mm**. **Reconciled: tub y ∈ [−42, +35].**
3. **Wheel tops vs top sheet.** Wheels Ø 32 at z = 16 reach z = 32; the top sheet on the rails at z = 29–30. AWS74 shows the wheels slightly above the sheet. **Consistent.**
4. **Drive units: servos or gearmotors?** The "coreless 2S8 multivoltage 6.0–8.4 V" label and the three-wire servo-coloured leads point to **converted coreless servos**; the spec uses `dm_wheel` motors. **Reconciled: converted coreless micro servos (medium).**
5. **Top sheet material.** AWS74's green tint is the backdrop's colour cast (the clear guard is also green-tinted there). AWS70 shows the same sheet grey. **Bare aluminium/thin metal.**

---

## 12. Why the designer did it (per part, mostly adversarial)

- **Interchangeable front (plough vs forks) on rails**
  - The designer can choose per opponent: **forks** against wedges and robots with gaps at the front (forks get under a wedge's lip more easily because they are narrow and thin, and they win "wedge vs wedge" fights when they reach lower), and the **plough** against spinners and pushers (full-width coverage, deflects horizontal spinners' hits sideways and upward).
  - The rails make this swap quick: 2–4 screws.
- **Plough shape (three facets)**
  - Attacks: the angled side facets **cover the front corners and the front of the wheels**, so a horizontal spinner hitting the corner meets a sloped steel face and is deflected. A vertical spinner meets the centre facet and is deflected up.
  - Getting under: a thin metal lower edge (0.9 mm) gets under printed wedges.
  - Weakness: hung from only 4 screws at its top edge, the plough can bend back under a big hit (the dents in AWS70/74 show that it takes hits). The gap above it exposes the rails' front ends.
- **Forks (clear polycarbonate)**
  - Getting under: narrow, thin, sloping tips that scrape the floor (the scratched tips prove they are in floor contact) get under opponents' edges.
  - Weakness: a horizontal spinner can snap a fork; polycarbonate flexes rather than shattering, which is why it is used.
- **Metal top sheet**: armour against overhead hits and opponents riding up; it is thin and dents (sacrificial) but protects the clear plate and electronics. It sits on the rails, leaving an air gap that absorbs dents without crushing the wires.
- **Clear top plate**: light and tough; lets the builder see the electronics; doubles as the base for the rails and guards.
- **Raised rail tails**: when the robot is **inverted**, the tails (z ≈ 39) and the wheel tops (z ≈ 32) are the highest points: the tails act as **skids / a rear support** so the robot rests on its wheels and tails, not on its top sheet. They also stop an opponent riding over the top from catching the sheet's rear edge.
- **Big foam wheels (Ø 32)**: grip, invertibility (much taller than the body), and shock absorption. **Weakness**: the tyre tops are exposed above the guards, and foam tears.
- **Clear guards, screwed and taped**: they shield the wheel's outer face from side hits and stop opponents from climbing the tyres. Clear polycarbonate is used because it is light and survives impacts by flexing. The tape shows the guards have been repaired or are deliberately easy to remove.
- **Hexagonal tub with front chamfers**: the chamfers give the plough's side facets room and deflect hits at the corners. The tub is low (19 mm), presenting little to spinners.
- **Velcro pads**: battery retention or a quick way to attach the electronics under the plate without screws.

---

## 13. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive units DS | 2 × coreless micro servos converted to continuous rotation ("coreless 2S8 multivoltage") | 23 × 12 × 25 | along X, outputs outward, (±28, −10, 12) | medium |
| Drive mounts | printed **pockets** in the tub floor with the servo ears screwed down (2 × M2 each) | 32 × 12 × 4 ears | at each servo | medium |
| Hub coupling | the ring hub is screwed to a servo horn (the light part seen through the hub) | Ø 14 | at each output | medium |
| Battery | 2S LiPo, 300 mAh, red wrap | 40 × 18 × 10 | front-left, (−20, +15, 8) | medium |
| RX/ESC | combined receiver + dual ESC (spec `el_rx_esc`), blue heat-shrink | 25 × 15 × 6 | under the left rail, (−12, 0, 10) | low–medium |
| Switch / link | white plug pair as a removable link, or a slide switch on the rear wall | — | (0, −5, 18) or (0, −42, 10) | low |
| Front cross bolts | 2 × M3 threaded rods across the front, as the plough/scoop strut (`dt_strut_scoop`) and as stiffeners for the tub's front | Ø 3 × 80 | (0, +30, 12) and (0, +33, 6) | low |
| Rail fixings | 3–4 × M2 screws from under TP into each rail | — | along x ±14 | medium |
| Wiring | battery → link → RX/ESC → 2 drive servos; servo leads loop above the plate level under the clear top | — | — | high (exists) |

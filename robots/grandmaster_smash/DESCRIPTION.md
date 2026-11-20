# Grandmaster Smash: full rebuild description from reference photos

Source photos:
- `robots/grandmaster_smash/reference/grandmaster_smash.aws72.webp` (1131 × 860 px): AWS 72, cut out onto white. **The primary build target.** **Front-left three-quarter** (json: az 45, el 35): the camera is above and to the robot's front-left. The long green body bar runs from the image bottom-left (the robot's left end, with its wheel) to the top right (the right end). The **green drum** with its **five-hole end face** is in the centre. A **brass ring** is behind it. Two **steel fork blades** with barbed tips point to the image bottom-right, and two **clear polycarbonate uprights** stand at the drum's ends.
- `robots/grandmaster_smash/reference/grandmaster_smash.aws73.webp` (522 × 405 px): AWS 73 pit photo. Front-left view at about 45° elevation, on a **green "SOS"-lettered printed stand** over a yellow/black box. It shows the same robot, with a loose green part (a spare guard or fork cover) at the bottom and a black triangular piece at the right.
- `robots/grandmaster_smash/reference/grandmaster_smash.aws69.webp` (378 × 222 px): AWS 69, a small, slightly blurred **front view** at about 15° elevation. It shows the drum, the **brass ring**, an exposed **silver coil-like part** (the motor stator windings, or a spring), several clear plates and both wheels.

Pixel coordinates refer to the jpg copies at these sizes, read by eye, ±8 px (±4 px on the small ones).

Facts are read from the photos. Guesses are marked **(guess)** with **H/M/L**. Scale comes from the M3 socket cap screws in the drum face (head Ø 5.5 mm), the wheel (Ø ≈ 28 mm), and the AWS cube limit (101.6 mm). Ratios are given against **D = wheel diameter ≈ 28 mm**.

Robot class: **drum spinner with forks** (`REFERENCE.json`: drum, axis x, 2 teeth). A **short, fat green drum** on a **transverse (X) axis** sits in front of a long, narrow body bar. It is driven directly by a brushless motor coaxial with it. Two **steel forks** project forward and down beneath the drum to feed opponents up into it. The drum spins so its front surface moves **upward** (the normal sense for a drum: it throws opponents up and back) (guess, H).

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the drum and the fork tips), **+Z** = up.
- **Origin O** = the floor point below the centre of the body bar (mid-width, mid-depth of the bar).
- The **drum axis** is the line (y +32, z 19), parallel to X.
- In aws72 the robot's **left end** (−X) is at the image bottom-left, the **right end** (+X) at the top right, and the **front** (+Y) toward the image right/bottom-right.

| ID | Part |
|---|---|
| BB | green printed body bar (the main chassis) |
| EG-L / EG-R | end frames: the wheel enclosures and guards at each end of BB |
| TP | top plate of BB (with the inlay and screws) |
| INL | black silhouette inlay/sticker on TP |
| WN | small window in TP near the drum, showing a brass/orange part |
| S-TP | silver M3 button screws on TP (≈ 6) |
| WH-L / WH-R | wheels: dark grey knurled TPU tyres on translucent yellow-green hubs |
| DR | green printed drum shell |
| DR-S | 4 silver M3 socket screws in the drum's end face, plus the keyed centre bore DR-B |
| BR | brass ring (a thin disc at the drum's right end) |
| WM | weapon brushless outrunner (bell inside DR; the stator partly visible as the silver coil in aws69) |
| PC-L / PC-R | clear polycarbonate uprights (drum/motor end supports) |
| PC-S | screws/nuts through the PC uprights |
| FK-L / FK-R | steel fork blades with barbed chisel tips |
| BLK | clear/translucent block at the motor end (motor mount or bearing housing) |
| DM-L / DM-R | drive motors (hidden, guess N20) |
| ESC-W, ESC-D, RX, BAT, SW | electronics (hidden, guess) |

---

## 1. Overall description in one paragraph

Grandmaster Smash is a **wide, shallow, bright-green PLA robot**. It is built around a **long rectangular body bar** (≈ 98 mm across X, ≈ 34 mm deep in Y, ≈ 18 mm tall) with **a wheel at each end**. Each wheel (Ø ≈ 28 × 10 mm, dark grey knurled TPU tyre on a translucent yellow-green printed hub) sits inside a **rectangular end frame** that guards it on the front, rear and outer side. The bar's top is flat. It carries a **black inlaid silhouette** of a leaping creature, six silver button screws, and a small window by the drum. In front of the bar, on a transverse axis about 19 mm up, is the weapon. A **fat green drum** (Ø ≈ 34 × 30 mm) has a flat end face with **four socket screws** and a **keyed centre bore**. Next to it is a **thin brass ring** (Ø ≈ 42 × 1.5 mm), and then the **exposed motor stator** and a clear mount block. The drum assembly is carried between two **clear polycarbonate uprights** bolted to the bar's front face. From the bottom of each upright, a **steel fork blade** (≈ 4 × 1.5 mm in section, ≈ 50 mm long) slopes forward and down to the floor and ends in a **barbed, arrow-like chisel tip**.

---

## 2. Part-by-part description

### 2.1 Body bar (BB)
- **Material**: fluorescent/neon green PLA, matt, fine layer lines (0.2 mm), crisp edges with ≈ 1 mm bevels.
- **Shape**: a rectangular bar **≈ 98 (X) × 34 (Y) × 18 (Z) mm**, bottom at z ≈ 3, top at **z ≈ 21**. In aws72 the top face runs from (100, 495) to (930, 100), and the front face is partly hidden behind the drum.
- **Front face**: flat, vertical, at y +17, with the PC uprights bolted to it. A shallow **recess** (≈ 2 mm) for the drum's rear clearance is likely (guess, M).
- **Rear face (not seen)**: flat at y −17 (guess, H).

### 2.2 End frames / wheel guards (EG-L, EG-R)
- Each end of BB is a **rectangular "picture frame"** around its wheel. It has a **front rail** and a **rear rail** (≈ 4 mm thick each, running along X), joined at the outer end by an **end bar** (≈ 6 mm thick across X, full depth ≈ 38 mm, ≈ 16 mm tall). The wheel turns inside the opening (≈ 12 × 32 mm in plan).
- **EG-L** (aws72 (50–470, 500–690)): the outer end face is a flat green rectangle **≈ 38 (Y) × 16 (Z) mm** at x −49, z 3–19, with layer lines along it. Its top shows the frame around the wheel's top. The wheel's tread top stands **above** the frame (z 28 vs 19–21).
- **EG-R** (aws72 (840–935, 95–245)): the end block beyond the right wheel is visible as a cube-like green block **≈ 8 × 20 × 16 mm** at the bar's right-front corner. Its front part sticks forward of the bar line by ≈ 6 mm, like a bumper.
- **Function**: they protect the wheels on three sides (front, rear, outer end) while leaving the top and bottom open for invertible driving.

### 2.3 Top plate (TP), inlay (INL), window (WN), screws (S-TP)
- **TP**: the bar's top, possibly a separate lid **≈ 70 × 30 × 2 mm** between the wheel openings, flush with the frames (M).
- **INL**: a **black silhouette** of a leaping animal (a hare/greyhound/dragon-like shape, with a long tail to the left and the head up and to the right), **≈ 32 × 10 mm**, at the top's centre-left (aws72 (335–480, 270–320)). Its edges are crisp and the surface is flush, so it is a **multi-material inlay or a vinyl cut sticker** (M).
- **WN**: a **small rectangular window ≈ 10 × 6 mm** near the top's front edge just behind the drum (aws72 (495–560, 280–335)). It shows **gold/brass and orange** parts: likely the **power switch/link** or a JST connector (M). A silver screw sits beside it (520, 325).
- **S-TP**: silver M3 **button-head** screws (Ø 5.7) at: (548, 145) near the rear right, (715, 160) the right-front corner, (380, 460) left-front, (125, 495) left-rear (aws72). Plus 2 more hidden → **≈ 6**. They hold the TP lid to the bar, or the bar halves together.

### 2.4 Wheels (WH-L, WH-R)
- **Tyre**: dark grey (charcoal) TPU with a fine **knurled/serrated tread** (≈ 60 small diagonal ridges), **Ø ≈ 28 mm, width ≈ 10 mm**.
- **Hub**: **translucent yellow-green** PETG/TPU, with concentric ring texture (printed spiral visible through it), recessed about 2 mm. In aws73 a dark centre with spokes shows.
- **Position**: centre (x ±42, y 0, z 14). The wheel spins in the end frame opening. The **tyre top at z 28** stands ≈ 7 mm above the bar top (21), and the **tyre bottom at z 0** is below the bar bottom (3).
- **Wheel guards**: the end frames EG on the front, rear and outer sides (§2.2).

### 2.5 Drum (DR), screws (DR-S), bore (DR-B)
- **Shape**: a **solid-looking green cylinder Ø ≈ 34 mm, length ≈ 30 mm along X**, with ≈ 2 mm chamfered edges. It spans x ≈ −24 … +6, on the axis (y +32, z 19), so its bottom is at z 2 and its top at z 36.
- **End face** (the left face, x −24; aws72 (470–690, 400–580)): flat, with **four silver M3 socket cap screws** on a square pattern of **≈ 13 mm side** (bolt-circle Ø ≈ 18.5), rotated about 15°. A **centre bore Ø ≈ 5 mm** has a small **keyway notch** (keyhole shape) at the top, (577, 492). Through it the motor shaft's end or a D-shaft is visible.
- **Material**: green PLA (like the body) printed as a **shell around the motor bell** (H): the screws clamp the drum to the bell's face (outrunner bells have a threaded M3 face pattern of 12–19 mm).
- **Teeth**: **none visible** on the drum's surface (it reads as a smooth cylinder in aws72/73/69). The json says 2 teeth. The brass ring (§2.6) may carry two raised impact lobes outside the drum surface, or the teeth are on the far (hidden) side (L). **Model: a smooth drum plus two optional 2 mm teeth at 180° on the hidden side (L).**

### 2.6 Brass ring (BR)
- **Shape**: a **thin flat annulus**, **outer Ø ≈ 42 mm**, inner Ø ≈ 28 mm, **≈ 1.5–2 mm thick**, coaxial with the drum, at its right end (x ≈ +7). Its colour is brass/bronze with dark tarnish and a black edge band (aws72 (585–860, 225–520)). In aws69 it is the gold ring between the drum and the coil.
- **Function (guess)**: it is **larger than the drum**, so it is the **first contact**: an impact ring/disc that bites before the drum's surface. It acts as a thin "disc weapon" at the drum's end (M). It may have **two raised lobes** (the json's 2 teeth) that the photos don't resolve (L). It may also be a **brass shim/washer** clamping the drum to the bell (L).

### 2.7 Weapon motor (WM) and mount (BLK)
- aws69 shows a **silver, coil-textured cylinder** (≈ Ø 22 × 12 mm) between the brass ring and the right clear plates. It looks like the **copper/silver windings of an open stator** or a coil spring around the shaft. aws72 shows the motor area at (790–890, 280–420) as a **translucent block** BLK with a nut (a clear printed or PC bearing/motor mount).
- **Reading (M)**: the drum is the **outrunner's bell** with a printed green sleeve. The stator is fixed to the **right PC upright** through the clear block BLK, and the bell (drum) turns around it. The drum's left end runs on a **bearing** on a stub axle supported by the **left PC upright**.
- **Size (guess, M)**: a 2204–2208 class outrunner (stator Ø 22).

### 2.8 Polycarbonate uprights (PC-L, PC-R) and screws (PC-S)
- **Shape**: clear PC plates **≈ 2–3 mm thick**, standing in the YZ plane, **≈ 30 (Y) × 34 (Z) mm**, with rounded tops. PC-L is at x ≈ −28 (aws72 (380–470, 340–560); its top edge sticks up as a clear tab to z ≈ 40). PC-R is at x ≈ +32 (aws72 (730–800, 50–260); its tall clear tab rises to z ≈ 44 above the right wheel area). aws69 shows **three or four** clear plates (two near each end).
- **Fixing**: bolted to BB's front face and to each other through the drum axle. Visible: a **silver nut/socket** at aws72 (745, 215) on PC-R and (495, 545) at PC-L's bottom.
- **Function**: they **carry the drum axle and the motor**, and they are the **fork mounts** (§2.9). Their tall upper tabs stick up above the drum. They are probably **self-righting/anti-tip posts** or **drum guards** that keep the drum off the floor when the robot is upside down (M).

### 2.9 Forks (FK-L, FK-R)
- **Shape**: **flat steel strips** (spring steel / hacksaw blade / mild steel), **≈ 4 mm wide × 1.5 mm thick, ≈ 52 mm long** from the root to the tip. Each one is clamped at the bottom of its PC upright (FK-L at (480–520, 520–580); FK-R at (860–890, 360–400) in aws72). They slope **forward and down** to touch the floor at **y ≈ +68**.
- **Tips**: each ends in a **barbed arrowhead/chisel**: the strip widens to ≈ 8 mm in a **triangular barb** about 10 mm long with its point on the floor. In aws72 the FK-L tip is at (760–830, 735–830) and the FK-R tip at (1000–1100, 400–485).
- **Spacing**: FK-L at x ≈ −30, FK-R at x ≈ +34 (just outside the drum's ends), so the drum sits between and above them.
- **Function**: they get under an opponent and lift its edge into the drum's upward-moving face.

### 2.10 Hidden electronics
- **ESC-W (guess, M)**: a 12–20 A brushless ESC inside BB.
- **ESC-D + RX (guess, M)**: a dual brushed ESC with receiver.
- **BAT (guess, M)**: a 3S 180–300 mAh LiPo along X inside the bar (≈ 45 × 17 × 12).
- **SW (guess, M)**: the power link/switch under WN.
- **DM (guess, M)**: two N20 motors along X, one at each end, gearboxes outboard to the wheels.

---

## 3. Per-view sections (for silhouette matching)

### 3.1 aws72 (front-left iso)
- The body bar is a long diagonal green slab from (50, 690) to (935, 95). The left wheel is at (130–420, 430–590) inside EG-L, the right wheel at (615–850, 60–280).
- The **drum**'s end face is a large green rounded rectangle/circle at (460–700, 380–620). The drum's body extends up-right to (810, 270). The **brass ring** is an ellipse (585–860, 225–520) behind it.
- The **forks** run to the bottom right. The **PC tabs** stick up at (380–470, 340–560) and (730–800, 50–260).
- The inlay is in the middle of the top. The window and its gold part are just above the drum.

### 3.2 aws73 (front-left, high, on a stand)
- The same layout. The robot sits on a green stand with raised "SOS" letters. The drum face with 5 holes is clearly visible. The brass ring and an aluminium/silver motor bell part are behind it. Clear tabs stand at both drum ends. Fork tips are at (180–240, 250–330) and (420–500, 140–200).
- A **separate green bar piece** (≈ 30 × 8 × 8 mm) lies loose at (240–320, 290–385): a spare part or a dropped wheel-guard rail.

### 3.3 aws69 (front, low)
- Left to right: the left wheel, clear plates, the green drum (Ø about 1.3 × the wheel height), the **brass ring**, the **silver coil/stator**, two clear plates, and the right wheel. The body bar is behind with its end blocks. The drum is on the left of centre and the motor on the right of centre.

### 3.4 Top view (synthesised)
- The bar: x ±49, y ±17. The wheels in their end openings at x ±(37 … 47). In front: the drum at x −24 … +6, y +15 … +49; the ring at x +7, Ø 42; the motor/BLK at x +9 … +28. PC-L at x −28 and PC-R at x +32, each y +17 … +47. The forks from (x −30 / +34, y +40) to (y +68).

### 3.5 Front view
- The wide bar (98 × 18) at the back. The drum circle (Ø 34) left of centre, standing above the bar top by 15 mm. The ring Ø 42 just right of the drum. The PC tabs rise to z 40–44. The forks show as two thin lines going down to the floor. The wheels at the outer ends, tops at z 28.

### 3.6 Left side view
- EG-L's end face (38 × 16). The wheel peeks above it to z 28 and below to z 0. The drum (Ø 34) at y +32, z 19 in front. The fork slopes from (y +40, z 6) to (y +68, z 0). PC-L's outline is behind the drum face.

### 3.7 Rear view (not photographed, inferred)
- The bar's flat rear face, 98 × 18, with the end frames. The wheels are visible through the open tops.

---

## 4. Part table

| ID | Shape | Size (mm) | Position | Material |
|---|---|---|---|---|
| BB | bar | 98 × 34 × 18 | (0, 0, 12) | green PLA |
| EG-L/R | end frames | 6 end bar + 4 rails, 38 deep, 16 tall | x ±(37 … 49) | green PLA |
| TP | lid | 70 × 30 × 2 | z 19–21 | green PLA |
| INL | silhouette | 32 × 10 | (−12, −2, 21) | black |
| WN | window | 10 × 6 | (+2, +12, 21) | — |
| S-TP ×6 | M3 button | Ø 5.7 | top corners and the middle | steel |
| WH-L/R | wheels | Ø 28 × 10 | (±42, 0, 14) | grey TPU + yellow-green hub |
| DR | cylinder | Ø 34 × 30, chamfer 2 | axis (y 32, z 20 after §13.2), x −24 … +6 | green PLA |
| DR-S ×4 | M3 socket cap | Ø 5.5 | square 13 on the left face | steel |
| DR-B | keyed bore | Ø 5 + 1.5 notch | the left face centre | — |
| BR | annulus | Ø 38/28 × 1.5 (photo reading 42; reconciled in §13.2) | x +7 | brass |
| WM | outrunner stator | Ø 22 × 12 | x +9 … +21 | copper/steel |
| BLK | mount block | 12 × 16 × 16 | x +22 … +30 | clear PC/PETG |
| PC-L/R | plates | 30 × 34 (+ tab to 40–44) × 2.5 | x −28, +32 | clear PC |
| FK-L/R | strips | 52 × 4 × 1.5, barb 8 × 10 | x −30, +34, y +40 → +68 | steel |
| DM-L/R | N20 | 12 × 10 × 24 | (±25, 0, 14) | (guess) |
| BAT | LiPo | 45 × 17 × 12 | (0, 0, 11) | (guess) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WH ↔ floor | drive contact | 0 |
| FK tips ↔ floor | skid contact | 0 |
| BB bottom ↔ floor | clearance | 3 |
| DR bottom ↔ floor | clearance | 2 |
| DR rear ↔ BB front face | spinning clearance | 2 |
| DR end faces ↔ PC-L / BR | bearing/shim | 0.5 |
| BR ↔ DR right end | clamped (or integral) | 0 |
| BR rim ↔ floor | clearance (after the §13.2 reconciliation: ring Ø 38, axis z 20) | 1 |
| WM stator ↔ BLK ↔ PC-R | bolted | 0 |
| PC-L/R ↔ BB front face | bolted | 0 |
| FK root ↔ PC bottom | clamped | 0 |
| FK ↔ DR underside | the fork passes below the drum's ends | 3–5 |
| WH ↔ EG rails | running gap | 1.5 |
| WH top ↔ TP | the wheel stands proud | +7 |
| PC tab top ↔ DR top | the tab stands proud | +4 … +8 |
| INL ↔ TP | flush | 0 |

---

## 6. Mechanism

- **Weapon**: a direct-drive outrunner drum. With DR as a printed PLA shell (≈ 15 g) around a steel bell (≈ 15 g) and the brass ring (≈ 10 g: 8.5 g/cm³ × π·(2.1² − 1.4²)·0.15 cm³ = 8.5 × 1.15 ≈ 9.8 g), the moment of inertia is I ≈ ½·0.030·0.017² + ½·0.010·(0.021² + 0.014²) ≈ **7.0e-6 kg·m²**. At 20,000 rpm (2094 rad/s): E ≈ **15 J**.
- **Spin direction (guess, H)**: the front surface moves **up** (the drum's top moves backward): hits throw opponents up and over, and the forks feed them in.
- **Drive**: wheels at the extreme ends give a **very wide track (84 mm)** on a short wheelbase: stable against the drum's gyroscopic tilt when turning. (A drum on an X axis makes turning cause a roll moment, which the wide track resists.)
- **Inverted**: the wheels stand 7 mm above the top, so the robot drives upside down. The drum then sits high, so the forks point up: the robot is less effective but mobile. However, the PC tabs (up to z 44) stand above the wheel tops (z 28), so **inverted, the robot would sit on the PC tabs, not its wheels**. See §13.3.

---

## 7. Assembly order (suggested rebuild)

1. Print BB with the end frames, the motor cradles and the internal bay (green PLA). Print the drum shell (green), the wheels' hubs (translucent) and the tyres (TPU).
2. Install the drive N20s at both ends. Press on the wheels inside the end frames.
3. Install the battery, ESCs, RX and the switch under WN. Fit TP with 6 S-TP and apply the inlay sticker.
4. Mount the outrunner stator to BLK and PC-R. Fit the drum shell to the bell (4 × M3 from the left face) with the brass ring between the drum and the stator side.
5. Fit PC-L with the bearing on the stub axle at the drum's left end.
6. Bolt PC-L and PC-R to BB's front face. Clamp the forks to the PC bottoms.
7. Route the weapon motor wires through the bar's front face into the ESC.

---

## 8. Hidden / uncertain list

- The drum teeth (none seen; the json says 2).
- The brass ring's role.
- The exact motor arrangement (the stator on the right, a bearing on the left).
- Everything inside the bar.
- The rear face and the underside.
- The function of the tall PC tabs.

---

## 9. Coordinate frame (restated)

+X right, +Y forward, +Z up. O on the floor below the bar centre. Drum axis (y 32, z 19) ∥ X. Wheels on the axis (y 0, z 14) at x ±42. Fork tips at y +68.

---

## 10. Profiles as math

**10.1 Drum.** A cylinder r 17 about the axis, x ∈ [−24, 6], with 2 mm × 45° chamfers. Bolt holes at the square corners (±6.5, ±6.5) in the drum-face coordinates (rotated 15°). Bore: a circle r 2.5 plus a slot 1.5 wide to r 3.5 at the top.

**10.2 Optional teeth (L).** Two raised blocks 6 (circumference) × 2 (radial) × 30 (X) at θ = 0° and 180° on the drum surface. Leading face radial, trailing face sloped: r(θ) = 17 + 2·(1 − θ/30°) for θ ∈ [0, 30°].

**10.3 Brass ring.** Annulus r 14 … 21, thickness 1.5, at x ∈ [6.5, 8].

**10.4 Fork centreline (YZ).** From the root R = (y 40, z 6) to the tip T = (y 68, z 0): z = 6 − (6/28)·(y − 40), a 12° slope. Barb: the strip widens linearly from 4 to 8 over y ∈ [58, 64], then tapers to a point at y 68 (a triangle). Its inner side is barbed back: the notch from (y 64, half-width 4) to (y 62, half-width 2).

**10.5 PC upright outline (YZ).** A rectangle y ∈ [17, 47], z ∈ [2, 34] plus a tab y ∈ [30, 36], z ∈ [34, 42] with a rounded top (r 3). Axle hole Ø 5 at (32, 19).

**10.6 End frame (XY at any z in [3, 19]).** Outer rectangle x ∈ [37, 49], y ∈ [−19, 19] minus the inner opening x ∈ [37, 43], y ∈ [−15, 15]; the wheel spins in the opening. Mirrored for −X.

---

## 11. Pixel-based measurements (independent check)

**aws72** (1131 × 860): drum face Ø ≈ 215 px; drum screw head ≈ 22 px; bolt square side ≈ 70 px; brass ring long axis ≈ 330 px; left wheel ≈ 290 × 170 px (oblique); right wheel ≈ 235 × 220; bar top length ≈ 1000 px diagonal; fork visible length ≈ 380 px (FK-L); EG-L end face ≈ 420 × 130 px.
**aws69** (378 × 222): total width ≈ 330 px; wheel height ≈ 105 px; drum ≈ 85 wide × 135 tall; ring ≈ 20 wide × 130 tall.
**aws73** (522 × 405): drum face Ø ≈ 95 px; screw ≈ 10 px.

---

## 12. Several independent estimates of key quantities

| Quantity | Method A (rules/parts) | Method B (screw Ø 5.5) | Method C (ratio to D = 28) | Reconciled |
|---|---|---|---|---|
| Drum Ø | outrunner bell 28 + 3 mm shell | aws72: 215/22 × 5.5 = 54?? (the face is the nearest thing to the camera; the screw is on the same face → same depth) → 54 | aws69: 135/105 × 28 = 36 | **34** (see §13.1) |
| Drum length | bell 22 + 8 | — | aws69: 85/105 × 28 = 23 | **30** |
| Ring Ø | > drum by 8 | aws72: 330/22 × 5.5 = 82?? | aws69: 130/105 × 28 = 35 | **42** |
| Bolt square | 12–16 (motor pattern) | 70/22 × 5.5 = 17.5 | — | **13–16** |
| Overall width | ≤ 101.6 | — | aws69: 330/105 × 28 = 88 | **98** |
| Bar depth | — | — | aws72 end face 420/290 × 28 = 40 (near-field) | **34–38** |
| Fork length | box: 101.6 − (bar 34 + drum offset) | aws72: 380/22 × 5.5 = 95?? (strong foreshortening and near-field) | — | **52** |
| Mass | 2 × N20 (20) + weapon motor (25) + BAT (25) + ESCs (12) + RX (3) + wheels (8) + bar (30) + drum (15) + ring (13) + PC (6) + forks (6) + screws (6) ≈ 169 g | — | — | **too heavy → see §13.4** |

---

## 13. Consistency check: conflicts and reconciliation

1. **The drum Ø from screws is too large.** In aws72 the drum face screws give 54 mm, but that face is turned obliquely and the screw heads look smaller than true when foreshortened (and are counterbored, so only the socket rim shows). aws69's front ratio gives 36. A 54 mm drum would not fit with 28 mm wheels and a 21 mm bar (the drum's top would be at z 46). **Reconciled: Ø 34.** The bolt square then measures ≈ 13 mm, the usual M3 pattern for 22xx motors. ✓
2. **The brass ring vs the floor.** At Ø 42 on an axis at z 19, the ring's bottom is at z −2: **below the floor**. Either the ring is smaller (Ø 36, bottom at z 1) or the axis is higher (z 22). aws69 shows the ring ≈ the drum's height (130 vs 135 px). **Reconciled: ring Ø 38, axis z 20 → ring bottom z 1, drum bottom z 3.**
3. **The PC tabs vs invertibility.** The tabs reach z 40–44, above the wheel top (28). Inverted, the robot would rest on the tabs and the wheels would not touch. That only makes sense if the tabs are **self-righting posts**: the drum's gyro reaction or a quick drive manoeuvre tips the robot over onto its wheels (M). Alternatively the tabs are lower (z 30) and only look tall because they are near the camera (M). **Model the tabs to z 36** as a compromise and flag it.
4. **Mass.** The rough budget is 169 g, over the 150 g limit. Trim: BAT 3S 180 (16), weapon motor 2204 (20), bar shell walls 1.2 mm (22) → ≈ 147 g. ✓ The design must use small components.
5. **Box**: the width is 98 ✓. The length: bar rear y −17 → fork tips y +68 = **85** ✓. The height: the tabs at 36–44 ✓.

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Wide body with wheels at the ends**: the widest possible track for stability with an X-axis drum (gyro roll when turning). The narrow depth keeps the robot short so the forks and drum fit in the 4-inch box.
- **End frames as wheel guards**: protect the tyres from spinners and the opponent's wedges, while leaving them proud on the top and bottom for invertible driving.
- **Short, fat drum offset to one side with the motor beside it**: direct drive is simple and light. Putting the drum on the bell saves a belt or bearing. The offset is the price of a single motor. The motor's stator sits beside the drum (not inside).
- **Brass ring**: a dense, thin, larger-diameter element puts mass at the largest radius cheaply (brass is ≈ 8.5 g/cm³) and may give a bite edge, raising the stored energy without a steel drum.
- **Forks with barbed tips**: they get under wedges and opponents' skirts. The barb catches on edges to lift them into the drum. Thin steel strips are light and replaceable.
- **Clear PC uprights**: PC is tough and flexible, absorbing the drum's impact reactions without cracking (better than printed PLA). It is cheap to cut. The tall tabs guard the drum's top and work as self-righting posts.
- **Black inlay, neon green**: identity and visibility on camera.
- **Window over the switch**: AWS requires an accessible isolation switch or link. A recessed window keeps it from being knocked.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Confidence |
|---|---|---|
| Weapon motor | 2204–2208 outrunner; the bell inside the drum shell; the stator on the right PC upright | M |
| Left drum support | a bearing on a stub axle in PC-L | M |
| Drive motors | 2 × N20 (or 1000 rpm micro gearmotors) at the bar ends | M |
| Weapon ESC | 12–20 A BLHeli in the bar | M |
| Drive ESC/RX | a combined board | M |
| Battery | 3S 180 mAh in the bar's centre | M |
| Switch | a link or slide switch under WN | M |
| Drum teeth | 2 small raised teeth on the hidden side, or none (the ring is the impactor) | L |
| Bar interior | 1.2–1.6 mm walls, a floor with screw bosses | M |
| Wire route | the weapon motor leads through a hole in the bar's front face behind the motor | M |

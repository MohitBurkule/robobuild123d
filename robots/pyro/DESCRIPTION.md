# Pyro: full rebuild description from reference photos

Source photo (cut out onto white by the AWS wiki):
- `robots/pyro/reference/pyro.aws71.webp`: AWS 71, 1683 × 1242 px. Camera at the robot's **front-left, high**: about **35–40° above the floor**, about **35–40° round from the front toward the robot's left side**. The front (two pods with flame stickers and black straps) points to the **lower-right**, the left side faces the **lower-left**, the rear is at the **upper-left**. A strong **green colour cast** over the right half (cut-out/lighting artefact; real colours: black body, blue name block, silver disc). Visible: the front and top of both pods, the left pod's outer side, the disc face (left face), the hub, the motor can, the right end of the axle, the rear body lid with screws and switch hole, the blue block, the left wheel's top and the left wheel guard. Not visible: right side, rear wall, underside, right wheel.

Only one photo exists, so the right side, rear and underside are inferred by symmetry and function. Facts are read from the photo; inferences are marked **(guess)**. Dimensions are **estimates**. Scale: the AWS 150 g / 101.6 mm cube, the **M2/M2.5 pan screws** (head Ø ≈ 4 mm), the **brushless outrunner** (read as a 28-class can, Ø ≈ 28 mm), the **5 mm axle**, and the kit draft (`kit.json`: vertical spinner, twin pods, body 90 × 112 × 36, ramp 35, slot 14; two wheels r 13 × 8 at y −32; disc r 40 × 4 at y +2, z 44, axis X, 2 teeth; forks n 2 length 24 width 10 spread 80 tilt 8°; motor cylinder r 10 × 34; uprights 8 × 30 × 40 at x ±14). Ratios are against **W = overall width ≈ 96 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward, **+Z** = up. Units mm.
- **Origin O** = floor point under the centre of the robot's footprint (mid-width on the disc slot centre line, mid-length from the pod tips to the rear wall).
- In the photo +Y points to the lower-right (about 30° below horizontal), +X to the upper-right (about 25° above horizontal, receding), +Z up.

| ID | Part |
|---|---|
| RB | rear body box (black printed, electronics) |
| RL | rear lid (black, screwed) with switch hole SWH |
| S-RL | lid screws |
| BB | blue printed block with embossed text (on the lid, beside the disc) |
| PD-L, PD-R | left and right front pods (black printed wedges) |
| PF | faceted textured top/front faces of the pods |
| ST-L, ST-R | flame/arrow paper stickers on the pods |
| FS-L, FS-R | black textured TPU straps (front flaps/"forks") over the pod fronts |
| WS | small black strap/flap over the left wheel front |
| GP-L, GP-R | wheel guard side plates (black, with V-notch at the rear top) |
| S-GP | screws in the guard plates |
| UL | left upright (black, holds the axle's left end) |
| UR | right upright (translucent/clear, holds the axle's right end) |
| AX | dead axle (steel, Ø 5) |
| NT | axle-end nut/bearing in UL |
| SPC | black printed spacer between UL and the hub |
| HB | silver aluminium hub/clamp on the disc's left face |
| DS | silver disc (ring with 3 windows, 2 teeth) |
| TH | the two teeth on the disc rim |
| WM | brushless outrunner weapon motor (black can) on the disc's right face |
| WH-L, WH-R | drive wheels (cream TPU studded tread, black hub) |
| M-L, M-R, BAT, ESC, WESC, RX | hidden internals |

---

## 1. Overall description in one paragraph

Pyro is a **compact twin-pod vertical disc spinner**. At the rear sits a **black printed box** (about 56 mm wide, 35 mm long, 30 mm tall) with a **screwed lid** and a **rectangular switch hole**, plus a **blue printed block with embossed lettering** standing on its front-right corner. Two **black wedge pods** extend forward on either side of a central slot; their tops are **faceted** (a flat top, a chamfer, then a front slope), printed with a **diagonal hatched texture**, and each carries a **hand-drawn flame/arrow sticker** (red-orange-yellow on black paper). Over each pod's front a **black textured TPU strap** hangs down to the floor like a flexible wedgelet. In the slot between the pods a **silver disc (Ø ≈ 76 mm)**, a flat ring with **three large windows**, a thick rim and **two small step teeth**, spins on a **dead axle** between a **black left upright** and a **translucent right upright**; it is clamped between a **silver aluminium hub** on its left face and a **black brushless outrunner can (Ø ≈ 28)** on its right face, the motor itself being the disc's hub (a "hub-motor" layout). Two drive wheels with **cream studded TPU tyres (Ø ≈ 26)** sit at the rear corners, protected outside by **black guard plates** with a V-notch at their rear tops.

---

## 2. Part-by-part description

### 2.1 Rear body (RB) and lid (RL)
- **Shape**: a **black printed box** about **56 mm wide (x ±28) × 35 mm long (y −48 to −13) × 28 mm tall** to the lid top (z 2–30). Rounded vertical corners (r ≈ 2). Print texture on the lid shows fine diagonal lines.
- **Lid (RL)**: flat, about **2 mm** thick, inset slightly at its front-left where it meets the left pod (a **notch/step** about 3 mm). Its front edge has a **broken/chipped corner** at the right next to the blue block (px (640, 380)).
- **Screws (S-RL)**: **silver pan/button heads** (Ø ≈ 4 mm, M2): at about px (275, 340), (350, 300), (520, 265) and probably a 4th hidden behind BB: i.e. at about (−22, −40), (−10, −42), (+10, −46) and (+22, −20) (guess).
- **Switch hole (SWH)**: a **rectangular slot about 10 × 4 mm** in the lid at about (−2, −42), px (420–455, 285–300), giving access to a **slide switch** or **link** (guess, high).

### 2.2 Blue block (BB)
- **Shape**: a **blue printed rectangular block** about **12 mm wide (X) × 35 mm long (Y) × 14 mm tall**, standing on the lid at its front-right, beside the disc, at about **x +6…+18, y −35…0, z 30–44**. Its top/left face carries **raised embossed text** running along its length (illegible in the photo; likely the robot's name **"PYRO"** or a team name, guess).
- **Function (guess)**: (1) a **name plate**; (2) a **cover/mount for the right upright** or a **wire guard** over the weapon motor wires coming from the right upright into the body; (3) a **brace** for the right upright. Its front end butts against the translucent upright region (medium).

### 2.3 Front pods (PD-L, PD-R) and faceted faces (PF)
- **Shape**: two **wedge-shaped black printed pods**, each about **34 mm wide**, flanking the central slot:
  - **PD-L**: x ≈ −48 to −14; **PD-R**: x ≈ +20 to +48 (the slot is offset slightly toward −X because the disc and its motor stack are asymmetric; see 2.11).
  - **Length**: from the rear body front (y −13) to the pod tips at about **y +44**.
  - **Side profile** (each pod): a flat top at **z ≈ 28** from y −13 to y ≈ −2, then a **chamfer facet** (about 45°, 8 mm) down to z ≈ 22 at y ≈ +5, then the **front slope** at about **25°** from (y +5, z 22) to the tip edge at about (y +44, z 3). The facets have **visible horizontal crease lines** and a **hatched diagonal texture** (printed on a textured PEI sheet or with ironing pattern).
  - **Outer side**: the outer walls slope (the left pod's outer side, seen at the left, is a long **sloped wedge face** with a **cut corner**, pentagon-like in section: an outer chamfer about 8 mm wide along the top outer edge).
  - **Tips**: the pod fronts end in a **thin floor edge** (z ≈ 3) across their width, with the outer corners extended into **pointed fork-like ends** (left pod's outer tip at px (480, 1090); right pod's outer tip at px (1630, 820)), about 5 mm ahead of the main edge.
- **Screws**: a **silver pan head** (Ø ≈ 4.5) on the left pod's outer chamfer at about (−46, +20, 14) (px (410, 935)), another on the right pod's outer top at about (+46, +20, 16) (px (1475, 625)): they fix the pods to the base/body or the guards.

### 2.4 Flame stickers (ST-L, ST-R)
- **Shape**: **black paper/card rectangles** about **30 × 28 mm**, stuck on each pod's front slope and top, each with a **hand-painted curved arrow/flame**: a thick **U-shaped swoosh** going up (red at the top, orange in the middle, **yellow** at the lower right with an **arrowhead** pointing right), like a fire trail or a "flip" arrow. The left sticker's arrowhead points to the lower-right (forward); the right sticker shows the same motif, partly hidden by the disc.
- Purely decorative (Pyro = fire).

### 2.5 Front straps (FS-L, FS-R) and wheel strap (WS)
- **Shape**: **flat black flexible strips** about **12 mm wide × 1.5 mm thick**, surface **diamond-knurled** (printed TPU with a textured top, or rubber grip tape). Each runs from under a **black cover tab** on the pod's top/sticker (left: a black square piece about 12 × 12 at px (700–790, 710–790)) **down over the front slope** and **past the pod tip** by about **8–10 mm**, ending at the floor with a **square cut end**. FS-L is centred at about x −30, FS-R at about x +33.
- **Function**: flexible **wedgelets/"forks"** (kit forks n 2, width 10, length 24): they lie on the floor ahead of the pods so the robot's leading edge is always flush with the floor; they bend rather than break when hit (guess, high).
- **WS**: a similar **black strap** (about 12 mm wide) lies over the gap in front of the **left wheel**, between the guard plate and the body (px (140–210, 340–500)): a **flap guarding the wheel's front** (guess, medium).

### 2.6 Wheel guards (GP-L, GP-R)
- **GP-L**: a **flat black plate** about **3 mm thick**, outside the left wheel at **x ≈ −48…−45**, running from the rear (y ≈ −50) forward along the left pod's outer side to about y +20, its **top edge** sloping down toward the front (from z ≈ 34 at the rear to z ≈ 12 at y +20). At the **rear top** it ends in a **V-shaped notch**: two pointed prongs about 8 mm tall with a V gap between them (px (20–100, 370–470)): this gives the robot **pointed rear corners** (rear "forks" for driving backward / when inverted, guess) and saves weight.
- **Screws (S-GP)**: two **black pan screws** (Ø ≈ 4) at about (−48, −30, 18) (px (115, 630)) and (−48, −5, 10) (px (295, 895)).
- **GP-R**: mirror (hidden).

### 2.7 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 26 mm × 9 mm**; **cream/off-white TPU tyre** with **round studs** (a honeycomb/knob tread, studs Ø ≈ 2 mm, about 3 rows across); **black hub** (face recessed).
- **Position**: centres at about **(±40, −34, 13)** (kit y −32), between the body and the guard plate. Wheel top at z 26, below the guard top (z ≈ 34 at the rear).

### 2.8 Uprights (UL, UR) and axle (AX)
- **UL**: a **black printed post** on the inner side of the left pod (part of PD-L or a separate block), about **10 mm wide (X) × 20 mm long (Y) × 44 mm tall**, its top at z ≈ 50, holding the axle's left end at **(x −22, y +4, z 38)**. A **black printed cylindrical boss/spacer (SPC)** about **Ø 16 × 8 mm** sticks out of it toward the disc, with a **silver nut or bearing** (Ø ≈ 6) visible in its end (NT).
- **UR**: a **translucent/clear printed (or polycarbonate) block** on the inner side of the right pod, about **10 × 20 × 44 mm**, holding the axle's right end at **(x +24, y +4, z 38)**; the axle **protrudes about 6 mm** beyond its outer face as a **plain steel stub Ø ≈ 5 mm** with a chamfered end (px (1380–1420, 385–420)).
- **AX**: a **steel dead axle** about **Ø 5 × 52 mm**, along X, fixed (non-rotating) in both uprights (guess, medium; the visible stub does not appear to have a bearing).

### 2.9 Hub (HB)
- A **silver aluminium cylinder** about **Ø 20 × 6 mm** with a **chamfered outer edge** and **two small holes** (set screws or clamp screws, Ø ≈ 2) in its face, on the disc's left face, concentric with the axle. Between HB and SPC a **dark gap** about 2 mm (a washer or the bearing).

### 2.10 Disc (DS) and teeth (TH)
- **Shape**: a **flat silver metal disc**, outer **Ø ≈ 76 mm**, thickness about **3 mm** (kit 4), with:
  - An **outer rim ring** about **9–10 mm** wide (radial).
  - **Three large windows** (120° apart), each a **curved trapezoid** bounded by the rim's inner circle (r ≈ 28.5), a hub circle (r ≈ 15) and two straight **spokes** about **6 mm** wide, the window corners rounded (r ≈ 3).
  - A **central hub ring** about Ø 30 with **4 small holes** (bolt circle Ø ≈ 19, for the motor bell screws) and a centre hole Ø ≈ 8.
  - **Two teeth (TH)**: small **radial steps** on the rim, about **4 mm** tall, 180° apart (seen at the bottom px (1145–1180, 800–860) and at the upper-left px (850, 70)): the rim radius rises from 36 to 38 over 170° and drops abruptly at the tooth (a two-step **"snail" or stepped-tooth profile**), giving two impact faces (guess, medium).
  - Material: **steel** (hardened, e.g. Hardox or tool steel) or **titanium/aluminium**; the bright satin finish with darker edge scratches suggests **steel or Ti** (guess). Edges show a green glow from the photo's colour cast.
- **Position**: disc plane at **x ≈ −8 (thickness −9.5…−6.5)**, centre **(−8, +4, 38)**: bottom at z ≈ 0 (r 38 → z 0; reconciled to **centre z 40, bottom z 2**, see 12), front edge at about y +42 (close to the pod tips), rear edge at y −34 (cleared by the rear body's front, which is at y −13: the body must have a **slot/notch** for the disc's rear arc, or the disc's rear clears over the lid top (top of disc z 78)). The disc's rear-lower arc passes **inside a notch** in the rear body front between the pods (guess, high).
- **Direction**: spins **forward at the top** (top moving toward +Y? For a vertical spinner hitting upward, the front edge moves **up**: the disc rotates so that the front point moves upward, i.e. top moving backward) (guess, high: standard vertical spinner).

### 2.11 Weapon motor (WM)
- **Shape**: a **black brushless outrunner** can about **Ø 28 × 20 mm**, on the disc's **right face** at x ≈ −6…+14, with a **narrow silver ring and a translucent green-tinted collar** near its right end (the stator mount plate or a clear spacer), then UR. Through the disc's windows, **silver bell spokes** and **copper/brass windings** are visible: the **bell is on the disc side**, i.e. the **bell spins with the disc** and the **stator is fixed to the dead axle** at the right (a classic **"hub motor" vertical spinner**) (medium-high).
- **Wires**: 3 phase wires (hidden) from the stator through UR or along the axle into the body (perhaps under the blue block BB).

---

## 3. Per-view sections

### 3.1 The photo view (front-left, high)
- Upper-left: the **rear body** with lid screws, switch hole, the **left wheel** (cream studded tyre) and the **left guard plate** with its V-notch; the black wheel flap.
- Centre-left: the **left pod** (faceted, hatched texture), its **flame sticker** and **black strap** hanging over the front edge; the **blue block** above-right of the lid.
- Centre-right: the **disc face** with three windows, the **silver hub**, the **black spacer** with a nut in the left upright; the **motor can** on the far side of the disc; the **axle stub** protruding at the right.
- Lower-right: the **right pod** with its sticker and strap; its pointed outer tip.

### 3.2 Top view (synthesised)
- Rear body 56 × 35 at the back; wheels at the rear corners between the body and guards (overall width ≈ 96); two pods 34 wide flanking a slot about 30 wide in which the disc (3 thick, as a line at x −8 from y −34 to +42) and motor (28 dia × 20 at x −6…+14) sit; straps 12 wide sticking out ahead of the pods.

### 3.3 Left side view
- Guard plate in front of the wheel; pod side profile (flat top, chamfer, 25° slope); disc circle Ø 76 centred at z 40 rising above everything to z 78; left upright under the axle.

### 3.4 Front view
- Two pods with straps, the disc edge-on in the middle (3 mm line, 76 tall from z 2 to 78), the motor bulge right of it, the uprights either side, the wheels behind.

### 3.5 Rear and underside (not photographed)
- Rear wall of the body with the guard plates' V-notches at the corners; underside: flat floor, wheel slots, pod tips/straps.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| RB | box | 56 × 35 × 28 | 0.58 × 0.36 | black FDM | — | 1 |
| RL | lid | 56 × 35 × 2 | — | black | 4 × M2 | 1 |
| BB | embossed block | 12 × 35 × 14 | — | blue FDM | glued/screwed | 1 |
| PD | faceted wedge pods | 34 × 57 × 28 | 0.35 × 0.59 | black FDM, hatched | to RB/base | 2 |
| ST | paper stickers | 30 × 28 | — | black card, painted | glued | 2 |
| FS | knurled straps | 12 × ≈ 45 × 1.5 | 0.13 | black TPU | under tabs | 2 |
| WS | wheel flap | 12 × 25 × 1.5 | — | black TPU | — | 1–2 |
| GP | guard plates with V-notch | 70 × 34 × 3 | 0.73 × 0.35 | black FDM | 2 screws | 2 |
| WH | studded tyre wheels | Ø 26 × 9 | 0.27 | cream TPU / black hub | motor shaft | 2 |
| UL | upright + spacer | 10 × 20 × 44; spacer Ø 16 × 8 | — | black FDM | integral with PD-L | 1 |
| UR | upright | 10 × 20 × 44 | — | translucent | integral with PD-R / screwed | 1 |
| AX | dead axle | Ø 5 × 52 | — | steel | clamped | 1 |
| HB | hub | Ø 20 × 6 | 0.21 | aluminium | screws to bell | 1 |
| DS | windowed disc, 2 teeth | Ø 76 × 3 | 0.79 | steel/Ti | 4 screws to bell | 1 |
| WM | outrunner | Ø 28 × 20 | 0.29 | black | stator on AX | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| RL ↔ RB | screwed | 0 |
| BB ↔ RL | fixed | 0 |
| BB ↔ disc right face | beside (motor in between) | ≈ 15 |
| PD ↔ RB front | joined | 0 |
| PD-L inner face ↔ disc left face | clearance | ≈ 8 (hub + spacer) |
| PD-R inner face ↔ motor can | clearance | ≈ 4 |
| Disc rim ↔ floor | above | ≈ 2 |
| Disc rear arc ↔ RB front notch | clearance | 2–3 |
| Disc rim ↔ pod tops (side) | disc is in the slot | — |
| Disc front edge ↔ pod tips (Y) | slightly behind | ≈ 2 |
| HB ↔ DS ↔ WM bell | clamped | 0 |
| HB ↔ SPC | running gap | ≈ 1–2 |
| SPC ↔ UL | integral | 0 |
| AX ↔ UL, UR | fixed | 0 |
| AX stub ↔ UR outer face | protrudes | +6 |
| FS ↔ pod front | lies on | 0 |
| FS end ↔ floor | resting | 0 |
| FS end ↔ pod tip (Y) | ahead | 8–10 |
| WH outer face ↔ GP inner face | clearance | 2–3 |
| WH inner face ↔ RB side | clearance | 2 |
| WH bottom ↔ floor | touching | 0 |
| GP bottom ↔ floor | above | 1–2 |

---

## 6. Mechanism
1. **Drive**: two rear wheels (differential), front resting on the pod tips and straps.
2. **Weapon**: the outrunner's bell, the disc and the hub spin together on the fixed axle; the stator is clamped to the axle at the right. The disc's front arc comes up through the slot between the pods and hits opponents **upward** as the straps/pods get under them. Disc speed maybe 10 000–20 000 rpm (guess). Two teeth give two big bites per revolution.
3. **Gyro/handling**: a heavy vertical disc resists turning; the wheels at the rear give a long lever to steer.
4. **Invertibility**: the disc (top z 78) stands well above the body, so the robot cannot run inverted on its lid; when flipped it would rest on the disc and the guard prongs. The V-notched rear guards and the disc could help it **self-right** by spinning the weapon (guess, low). Not designed to run inverted.

---

## 7. Assembly order (suggested rebuild)
1. Print RB (with base plate, wheel motor mounts, the rear notch for the disc), the two pods (PD-L with UL and SPC; PD-R), UR (clear PETG), RL, BB, the guard plates and wheels (TPU tyres), straps (TPU).
2. Fit drive motors and wheels; fit battery, drive ESC, weapon ESC, receiver and switch.
3. Screw the pods to RB/base; fit UR to PD-R.
4. Assemble the weapon: bolt the disc to the motor bell with the aluminium hub on the other face (4 screws); slide the axle through UL/SPC, hub, disc, motor (stator fixed with grub screw or clamp to the axle), into UR; route phase wires into the body.
5. Screw on the guard plates; fit the straps under their tabs; stick on the flame stickers.
6. Screw on the lid and the blue block.

---

## 8. Coordinate frame (restated)
- RB: x ±28, y −48…−13, z 2…30.
- PD-L: x −48…−14; PD-R: x +20…+48; y −13…+44; profile in 9.1.
- Disc centre (−8, +4, 40), r 38, plane x −8 (3 thick). Axle along X at (y +4, z 40) from x −27 to +31 (stub to +31).
- Motor x −6…+14, Ø 28. Hub x −13…−9.5, Ø 20.
- Wheels (±40, −34, 13), Ø 26. Guards x ±45…±48.

## 9. Profiles as math

**9.1 Pod side profile (YZ).**
- (y −13, z 28) → (−2, 28) flat; → (+5, 21) chamfer 45°; → (+44, 3) slope: z = 21 − 0.4615·(y − 5) (24.8°); → (+44, 0) → (−13, 0) close.

**9.2 Disc outline (polar, in the disc plane, angle θ from the front, rotating).**
- Rim: r_out(θ) = 36 + 2·frac(θ/180°) (two teeth: the radius rises linearly from 36 to 38 over each 180° and drops back at θ = 0° and 180°).
- Windows: for k = 0, 1, 2, the region 15 ≤ r ≤ 28.5 and |θ − (60° + 120°k)| ≤ 60° − δ(r), where δ(r) = asin(3/r) (spoke half-width 3 mm), corners filleted r 3.
- Bolt holes: 4 × Ø 2.2 on r 9.5 at 45° + 90°k; centre hole Ø 8.

**9.3 Guard plate with V-notch (YZ).**
- Polygon: (−52, 2) → (+20, 2) → (+20, 10) → (−42, 30) → (−44, 36) (front prong tip) → (−47, 28) (V bottom) → (−50, 36) (rear prong tip) → (−52, 30) → close.

**9.4 Strap.** A thin strip of width 12, thickness 1.5, following the pod front profile from (y −2, z 28) down to (y +44, z 3) then a short flat on the floor to y +53; diamond knurl pitch 1.5.

**9.5 Wheel.** r(φ) = 13 with studs: hemispheres r 1 on a grid (3 rows × 30) on the tread.

## 10. Pixel-based measurements (native 1683 × 1242, ±8 px)
- Disc: outer extremes px (835, 60) top-left to (1220, 865) bottom; across its minor axis ≈ 360 px (x 840–1220 at mid-height); centre ≈ (1030, 460).
- Hub HB: (900–1030, 340–480), Ø ≈ 130 px across. Spacer SPC: (760–900, 370–520). Nut in SPC: (800, 455).
- Motor can: (1130–1300, 200–620); axle stub end (1405, 400).
- Blue block: (545–790, 70–430).
- Left pod: tip edge from (330, 1000) to (960, 980); left strap tip (790–890, 990–1060); right strap tip (1350–1440, 900–960).
- Left wheel: (75–200, 260–430); lid screws (275, 340), (350, 300), (520, 265); switch slot (420–455, 285–300).

## 11. Several independent estimates

| Quantity | Method A (kit / rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Disc Ø | kit 80 | ≈ 2.7 × motor Ø (28) → 76 | major axis ≈ 830 px; motor Ø ≈ 300 px (similar depth) → 830/300 × 28 = 77 | **76** |
| Motor Ø | kit 20 (r 10) | ≈ 0.37 × disc | 300/830 × 76 = 27 | **28** |
| Hub Ø | — | ≈ 0.26 × disc | 130/830 × 76... (nearer) ≈ 18–20 | **20** |
| Disc centre z | kit 44 | r + 2 = 40 | — | **40 (top 78)** |
| Overall width | kit 112 (over 101.6) | pods 2 × 34 + slot 30 → 98 | — | **96** |
| Length | kit 90 | body 35 + pods 57 + strap 9 → 101 | — | **≈ 100 (y −52 to +53 with straps; −52 to +44 plastic)** |
| Wheel Ø | kit 26 | ≈ 0.95 × body height | — | **26** |
| Strap width | kit 10 | ≈ 0.35 × pod width → 12 | — | **12** |
| Height | kit 36 (body), 84 (disc top) | — | — | **30 body, 78 disc top** |

## 12. Consistency check
1. **Width**: the kit's 112 breaks the cube; 96 (pods to ±48) fits.
2. **Length**: −52 (guard rear) to +53 (strap tips) = 105 if straps lie flat beyond the pods. Reconciled: straps stick out **only ~4–5 mm** horizontally beyond the pod tip (the rest bends down), total ≈ 101; or the guard rear at −50. Use guard −50, strap tips +50 → **100**.
3. **Disc vs body**: disc rear arc reaches y −34, inside the rear body (front at y −13). Needs a **notch** in RB's front-centre about 6 mm wide, down to z ≈ 15 (the disc arc at y −13 is at z ≈ 40 − √(38² − 17²) = 40 − 34 = 6 → the notch must reach almost the floor). Reconciled: the **slot between the pods continues into the rear body as a narrow pocket** (wall thickness kept around it). Kept (medium).
4. **Slot asymmetry**: disc at x −8, motor x −6…+14: the stack centre is near x +3; pods placed to clear both: PD-L inner face at x −14 (6 mm from the disc's left face, room for hub and spacer), PD-R inner face at x +20 (6 mm from the motor). Consistent with the photo (the hub/spacer stack on the left looks about as long as the motor on the right).
5. **Mass**: steel disc Ø 76 × 3 with 3 windows ≈ 70 cm³ × (1 − 0.45) × 7.85 ≈ 75 g?? Too heavy (75 g disc + 22 g motor). Reconciled: a **2 mm Ti or 3 mm aluminium** disc: Ti 2 mm ≈ 7.6 cm³ × 0.55 × 4.5 = 19 g; aluminium 3 mm ≈ 17 g; steel 1.5 mm ≈ 25 g. **Use 2 mm titanium/steel ≈ 20–25 g.** Total ≈ disc 22 + motor 20 + axle/hub 8 + body/pods 45 + wheels/motors 22 + battery 15 + ESCs 10 + misc 5 = **147 g** (tight but under 150).

---

## 13. Why the designer did it (per part, adversarial)

- **Vertical disc between two pods**
  - Fight: the disc hits upward, launching opponents or flipping them; between the pods it is protected from side hits and from being stopped by opponents' wedges; the pods guide opponents into the disc's path.
  - Hub-motor layout: no belt or gears (saves weight and failure points); the motor's bell is the hub, so the disc gets the motor's full torque instantly.
  - Windows: lower mass while keeping most of the inertia at the rim; two teeth give **bite** (more of the energy delivered in one hit) compared with a round disc.
- **Twin faceted pods with straps**
  - Getting under: the TPU straps lie flat on the floor ahead of the pods, getting under wedges and box robots; they are flexible, so a spinner's hit only bends them. The pods' 25° slopes then lift the opponent into the disc.
  - Facets: the chamfer and slopes deflect hits; the flat top gives room for internals.
- **Wheel guards with V-notch**
  - Protect the wheels from horizontal spinners and pushers; the notched rear prongs give pointed rear corners for pushing backward or getting under opponents with the rear (guess).
  - Wheel flaps (WS) stop opponents' forks entering the wheel gap.
- **Translucent right upright**
  - Probably PETG/polycarbonate for toughness at the motor side (it takes the stator torque and impacts) (guess).
- **Blue embossed block**
  - Identity and protection for the weapon wires; braces the right upright.
- **Flame stickers**
  - Theme: Pyro = fire.
- **Switch on top**
  - Easy to reach; the lid is behind the disc, out of the weapon arc.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Weapon motor | 2204–2806 class outrunner, KV 1400–2300, used as hub motor | Ø 28 × 20 | on AX x −6…+14 | medium-high |
| Weapon ESC | 12–20 A BLHeli ESC | 25 × 12 × 5 | in RB right half | medium |
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | in RB rear, shafts at (±28, −34, 13) | medium |
| Drive ESC + RX | combined board | 25 × 20 × 6 | RB left | medium |
| Battery | 3S 180–300 mAh LiPo | 40 × 18 × 12 | RB centre or inside a pod | medium |
| Switch | slide switch under the lid slot | 12 × 6 | (−2, −42, 24) | medium-high |
| Disc notch | narrow pocket in RB front | 8 wide | x −12…−4 | medium |
| Phase wires | 3 wires from the stator through UR into RB under BB | — | — | medium |

## 15. What the photo cannot show
- Right side, rear, underside, the right wheel and guard, the exact disc profile and material, the internal layout.
- All mm values are estimates (±10–15%).

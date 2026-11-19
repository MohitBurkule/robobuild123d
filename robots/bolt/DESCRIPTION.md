# Bolt: full rebuild description from reference photos

Source photos (all three are pit/table snapshots on a grey speckled surface, not cut out; quality is moderate):
- `robots/bolt/reference/bolt.aws63.webp` (**primary**, sharpest): AWS 63. **Front-right three-quarter from high above** (about 55–60° elevation). The clear front scoop is at the image bottom-right, the black rear frame at the top-left. The right side (with a white JST plug and the right rear wheel) faces the camera.
- `robots/bolt/reference/bolt.aws60.webp`: AWS 60. **From the rear, high above** (about 55°), robot centred. The black rear cross-member and pivot knuckles are nearest the camera (bottom); the clear scoop with a "Bristol Bot Builders" sticker (seen upside down) is at the far top. Both rear wheels with their brass gearboxes are visible, and the open central channel shows the servo horn, red wires and a purple LiPo warning label.
- `robots/bolt/reference/bolt.aws57.webp`: AWS 57. **Low resolution and blurred**, from above-left-rear; the front points to the image right. It confirms the same layout (two black arms, central link, clear scoop with the red "B" logo, cyan body, two rear wheels on the left side of the image, a yellow part near the scoop).

`REFERENCE.json`: `lifter`, wheels 4, weapon `wedge`, view aws57 "right", aws63 "front_right_iso". **Only two wheels are visible in all three photos** (at the rear); see §13.

Pixel coordinates refer to copies scaled to 1200 px long side for AWS63 (1200 × 970) and native size for AWS60 (704 × 672) and AWS57 (452 × 380), ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube and from the **N20 gearmotor + 22 mm rubber wheel** set clearly seen (a standard N20 gearbox is 12 × 10 mm in section, the wheels are the common Ø 22 × 9 mm type with a ribbed tread). Ratios use **W = body width at the rear ≈ 80 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the clear scoop), **+Z** = up. **Origin O** = floor point under the centre of the cyan body footprint (excluding the scoop's forward overhang).
- Lifter rotation **θ**: rotation of the black arm frame about the rear pivot axis (along X), positive = scoop up.

| ID | Part |
|---|---|
| CH | cyan printed chassis (floor + walls) |
| TP-L / TP-R | cyan top panels left/right of the central channel |
| CC | open central channel |
| SC-L / SC-R | cyan front side cheeks/prongs (pointed, floor-level) |
| AR-L / AR-R | black lifter arms (long square beams) |
| RX-F | black rear frame/cross-member joining the arm rear ends |
| KN | black pivot knuckles at the rear (with screws) |
| PV | rear pivot axle/screws |
| LK | central black link from the servo horn to the frame |
| SV | lifter servo (white horn visible) |
| HN | white servo horn |
| SP | clear polycarbonate scoop/plate (front) |
| SP-C | scoop side cheeks (bent-up sides of SP) |
| SP-S | screws joining SP to the arms |
| STK | white "Bristol Bot Builders" sticker on SP |
| WH-L / WH-R | rear wheels (black ribbed rubber, Ø 22) |
| GM-L / GM-R | N20 gearmotors (brass gearbox visible) |
| GD-L / GD-R | clear PC side plates (wheel guards) at the rear corners |
| GD-S | screws holding GD |
| JST | white 3-pin JST connector on the right side |
| BAT | LiPo battery (purple warning label visible) |
| WR | red/black wires in the channel |
| S-TP | screws on the top panels |
| YL | yellow part near the scoop base (AWS57) |

---

## 1. Overall description in one paragraph

Bolt is a **cyan, four-sided wedge-shaped servo lifter**. Its printed body is a low box about 80 mm wide at the rear and 80 mm long, about 22 mm tall, whose **sides sweep down into two pointed floor-level prongs** at the front corners. In the middle, between those prongs, a **clear polycarbonate scoop** with bent-up side cheeks sits on the floor; it is carried by **two long black square arms** that run back over the top of the body to a **black rear frame** with **pivot knuckles** at the rear corners. A **thinner black central link** in the open central channel connects the frame to the **white horn of a servo** in the middle of the body, so the servo lifts the whole black frame and the scoop about the rear pivot. Two **small black ribbed rubber wheels** on **brass-geared N20 motors** sit at the rear corners, partly shielded on the outside by **clear PC side plates** held by two screws each. The top of the body is two cyan panels with silver screws; the channel shows red wires, a purple-labelled LiPo and the servo. A **white JST plug** pokes out of the right side, and the scoop carries a **white sticker with a red "B" logo** ("Bristol Bot Builders").

---

## 2. Part-by-part description

### 2.1 Chassis (CH)
- **Shape**: a cyan printed tub with a flat floor. In plan, the rear half is **rectangular, about 80 mm wide**, from y −40 to y 0; the front half **tapers**: the side walls angle inward slightly (about 8°) and then sweep down and forward into the **front prongs** SC. Overall length from the rear face (y −40) to the prong tips (y +44) about **84 mm**.
- **Height**: about **22 mm** to the top panels at the rear; the side walls' top edges slope down toward the front from about y +5, reaching the floor at the prong tips.
- **Side walls**: about **2.5 mm** thick; their outer faces are **flat with a fine textured (fuzzy-skin) finish** (all cyan surfaces show a matt stippled texture — a printer "fuzzy skin" setting or textured PEI side).
- **Rear**: the rear face is hidden behind the black rear frame and the clear guard plates; it is vertical **(guess)**, with notches at the corners for the wheels.
- **Colour/material**: **turquoise/cyan PLA or PETG**, matt fuzzy texture.

### 2.2 Top panels (TP-L, TP-R) and channel (CC)
- **Shape**: two **flat cyan panels**, each about **26 mm wide × 60 mm long × 2 mm thick**, from y −35 to y +25, either side of the channel. Their **inner edges are stepped**: at the rear they are close to the centre (channel width about **14 mm**), then at y ≈ −5 each inner edge **steps outward** by about 6 mm with a 45° chamfer, so the channel widens to about **26 mm** in the front half (AWS60 shows this clearly: a pentagon-ended "notch" shape on each panel's inner edge).
- **Outer edges**: they overhang the side walls slightly and have a **45° chamfer** on the front outer corner.
- **Screws S-TP**: **silver pan-head Phillips screws**, head Ø 4.5 mm (M2.5). AWS60 shows **2 per panel**: one near the rear outer corner (x ±30, y −22) and one near the front, inner (x ±16, y +2); AWS63 shows three on the right panel: rear (x +18, y −30), middle (x +22, y −5) and front (x +28, y +12). Plus one silver screw at each rear-outer corner of the panels near the wheel (AWS60 at x ±35, y −30). Total **6–8**.
- **Channel CC**: open to the top, about **14–26 mm wide** and **60 mm long**, with the battery, servo and wires inside (see 2.10).

### 2.3 Front side prongs (SC-L, SC-R)
- **Shape**: the front ends of the side walls are shaped into **pointed, sloped prongs**: each is a **triangular-section wedge** about **14 mm wide** at its base, running forward **from y +5 to y +44**, with its **top face sloping down** from z 22 to z 0 (about **30°**) and its **outer face** angled inward toward the tip. The tip is a **sharp point** on the floor (AWS63: the right prong's tip at the bottom of the image, a cyan point ahead of the scoop corner).
- **Position**: x ≈ ±30 to ±44 at the base, the tip at x ≈ ±36. They **flank the scoop**: their inner faces are about **2–3 mm** from the scoop's side cheeks.
- **Function**: fixed side wedges.

### 2.4 Lifter arms (AR-L, AR-R)
- **Shape**: two **black square-section beams**, about **8 mm × 8 mm**, about **72 mm long**, straight, running **fore-aft** on top of the body at **x ≈ ±22** (AWS60: the arms run along the outer parts of the top panels, just inboard of the panel screws). Their top surfaces have fine layer texture; ends are square.
- **Front ends**: they come down to the scoop's top rear edge, where each is joined to the clear plate with **two screws** (SP-S, silver pan heads Ø 4, visible on the right arm end in AWS63 at (705, 290) and (750, 320) px, and one on the left arm with a small clear washer/tab).
- **Rear ends**: joined to the rear frame RX-F at the rear corners (y −40, z ≈ 26), where the knuckles KN are.
- **Pose**: at rest the arms slope down to the front by about **5–8°** (rear end at z ≈ 30, front at z ≈ 22).

### 2.5 Rear frame (RX-F), knuckles (KN), pivot (PV)
- **Shape**: a **black printed cross-member** across the rear at y ≈ −42, about **70 mm wide × 8 mm deep × 10 mm tall**, with its **lower edge bent into a shallow U** (AWS60: the black part at the bottom of the photo is a **trapezoidal frame**: a horizontal bar whose ends drop down at 30° into **feet** at the rear corners, each with **two silver screws** (one above the other), so it is a **bridge** over the rear of the body).
- **Knuckles KN**: at the top of the frame, where the central link and the arms meet it, there are **two black round knuckles** (Ø 10 mm, about 6 mm wide) side by side at x ≈ ±6 with a **silver pin/screw** through them (AWS60 at (360, 505) and (440, 505) px; AWS63 the black hinge at (185–235, 160–215)).
- **Pivot PV (interpretation)**: the **arms + rear bar + scoop** form one rigid **U-frame**; the frame pivots on **screws through the frame feet** at the rear corners (x ±38, y −42, z ≈ 12) **into the body's rear corners** (AWS60 shows two screws per foot: one is the pivot, one a stop or a second fixing). The central knuckles are the **joint between the frame and the servo link LK**.
- **Alternative**: the rear frame is **fixed** to the body and the knuckles are the arm pivots. In that case the two arms pivot at the rear centre on a common pin. AWS63 shows the arms' rear ends meeting a **vertical black side post** at each rear corner (the frame foot), with a screw at each arm-foot joint — consistent with the first interpretation. **Preferred: frame pivots at the feet (medium confidence).**

### 2.6 Central link (LK), servo horn (HN)
- **LK**: a **black flat bar**, about **5 mm wide × 6 mm tall × 50 mm long**, lying **in the channel**, from the rear knuckles (y −40, z 26) forward to about y +5, where it **bends down** (AWS63: the link drops at its front end into the channel at about (560, 420) px; AWS60: the link runs up the channel from the knuckles to the servo horn).
- **HN**: a **white plastic servo horn** (single-arm), about **15 mm long**, visible in AWS60 at the left of the channel at (270–310, 250–335) px, standing vertically (so the servo output axis is **horizontal, along X**). The link's front end is pinned to the horn tip.
- **Mechanism**: the servo turns the horn; the horn pulls/pushes LK; LK pulls the rear frame's centre, rotating the frame about the rear-corner pivots; the arms lift the scoop. (With the knuckles above the pivot, pulling LK forward rotates the frame so the front rises.)

### 2.7 Scoop (SP, SP-C, STK, SP-S)
- **Shape**: a **clear polycarbonate sheet** about **1–1.5 mm thick**, bent into a **shallow tray**: a flat **front plate** about **48 mm wide × 42 mm long**, sloping at about **20–25°** from its floor edge up to the arm ends, with **two side cheeks** (SP-C) bent up at about 90° along its long edges, each about **8–10 mm tall** at the rear, tapering to 0 at the front. The rear edge has a short **upward flange** where the arms are screwed (AWS60 shows a clear vertical flange with the arm ends screwed to it, and the sticker on the flat).
- **Front edge**: straight, flush on the floor, extending to about **y +46** (the same as, or 2 mm beyond, the prong tips).
- **STK**: a white paper/vinyl sticker about **40 × 25 mm** with a **red "B" logo** and "BRISTOL BOT BUILDERS" in red letters, scuffed and partly torn (AWS63 shows it worn to bare clear PC in places).
- **Wear**: the clear plate is scratched and frosted, with chewed edges and a small crack near the right rear corner (AWS63).
- **Width check**: scoop 48 + 2 × 2.5 gaps + 2 × 14 prongs ≈ 81 ≈ W.

### 2.8 Wheels (WH-L, WH-R) and gearmotors (GM)
- **Wheels**: **black rubber**, **Ø 22 mm × 9 mm**, with **fine transverse ribs** (about 40 ribs) and a **slight central groove**; standard **N20 wheels** on D-shafts. AWS60 shows a black plastic hub with a dark centre.
- **Gearmotors**: **N20 gearmotors** with **brass/gold spur gearboxes** clearly visible inboard of each wheel (AWS60: gold gearbox ~10 × 12 × 9 mm at (140–180, 470–520) and (550–590, 375–425) px). They lie **transversely (along X)** at the rear corners, the gearbox outward, the motor can inward.
- **Positions**: wheel centres at **x ±36, y −30, z 11**. The tyre outer faces at x ±40.5, i.e. **flush with the body sides**; the wheels sit in **corner notches** of the body.
- **Only two wheels** are visible in all three photos.

### 2.9 Rear corner guard plates (GD-L, GD-R)
- **Shape**: a **clear polycarbonate plate**, about **1.5 mm thick**, standing vertically on the **outside of each rear wheel** (in the YZ plane), about **30 mm long × 20 mm tall**, roughly rectangular with its **front lower corner cut at 45°** to follow the body line. AWS63 shows the right one from (20, 485) to (320, 690) px with **two silver pan screws stacked vertically** at its rear (at (40, 495) and (45, 530)) and **two more stacked** at its front (at (250, 605) and (255, 635)). AWS60 shows the left and right ones as clear vertical strips at the far left and right with two screws each at the rear.
- **Function**: **wheel guards** that cover the outer faces of the rear wheels. They are screwed to the body side wall (front pair of screws) and to the rear frame foot or a rear post (rear pair) — so they also act as the **outer support** joining the rear frame to the body **(guess)**.
- **Clearance**: about **1 mm** from the tyre outer faces.

### 2.10 Channel contents (BAT, SV, WR) and side connector (JST)
- **Battery**: a small **LiPo** with a **purple label** printed "READ … NEVER … UNATTENDED … DISCHARGE … BECOME…" (standard Turnigy/Zippy-style warning), about **30 × 15 × 8 mm**, lying lengthwise in the channel's right half at y −5 to +25 (AWS60 at (345–395, 240–305) px).
- **Servo**: under the left side of the channel at mid-length; only the white horn and part of a black case are seen.
- **Wires**: short **red and black** silicone wires coiled in the channel (AWS60 at (340–395, 320–380) px, AWS63 at (400–470, 360–390) px), plus a **blue** wire in AWS63.
- **JST**: a **white 3-pin JST-XH** (balance/charge) plug with **red wire**, sticking out of a slot in the **right side wall** at about (x +41, y +5, z 14) (AWS63 at (455–525, 640–710) px). It is the **charge lead or power link** **(guess)**.
- **Yellow part (AWS57)**: a small yellow item near the scoop's right rear corner — possibly a yellow zip tie or a part of a link plug **(uncertain)**.

---

## 3. Per-view sections

### 3.1 AWS63 (front-right, high)
- **Bottom right**: the clear scoop (520–965, 310–800) with the worn sticker; its right cheek and rear flange with two screws at the right arm end.
- **Bottom centre-left**: the right side of the body: right prong tip at (690, 800), the side wall with the white JST at (455–525, 640–710), the right top panel with screws at (300, 515) and (555, 160), the right rear guard plate (20–320, 485–690) with four screws, the right rear wheel (95–265, 455–560) with its brass gearbox.
- **Top**: the far (left) side: the left rear wheel (395–550, 50–155), the left arm along the top edge from (300, 80) to (750, 320), the rear frame with knuckles (90–235, 150–390), the right arm from (100, 345) to (530, 560), the central link from the knuckles (175, 205) to (580, 450).

### 3.2 AWS60 (rear, high)
- **Bottom**: the black rear frame (210–575, 490–600) with four screws at its feet and the two central knuckles; the rear wheels at (90–175, 430–550) and (565–640, 335–455) with gold gearboxes; the clear guard strips at the extreme left (50–105, 380–630) and right.
- **Middle**: the two black arms running up the image from the frame to the scoop flange at (130–175, 185–215) and (440–490, 160–200); the two top panels with stepped inner edges; the channel with the horn, wires and LiPo.
- **Top**: the clear scoop (75–520, 40–230), the upside-down sticker reading "BRISTOL … BOT BUILDERS" with the red B.

### 3.3 AWS57 (blurred, above-left)
- Same elements; front to the right. Both wheels on the left side of the image (rear), the clear scoop on the right with the red "B" sticker, the black arms horizontal across the image, the central link, a yellow tag near the scoop.

### 3.4 Top view (synthesised)
- An 80-wide rectangle at the rear (y −40 to 0) tapering into two pointed prongs at y +44; the 48 × 42 clear scoop between them; two black arms at x ±22 from the rear frame to the scoop flange; the channel 14–26 mm wide in the middle; wheels in rear-corner notches at x ±36, y −30.

### 3.5 Front view
- Floor line with the two prong tips (x ±36) and the scoop edge (x −24 to +24, z 0). The scoop rises to the arm ends at z ≈ 20; cheeks visible as thin lines. Behind: the body top at z 22, the arm tops at z 30 at the rear, the rear frame bar at z ≈ 30–36. Wheels hidden behind the body width (flush sides).

### 3.6 Right side view
- Body side profile: rear vertical face 22 tall, top line flat to y +5, then sloping down at 30° to the prong tip at y +44. The rear wheel Ø 22 in the rear notch behind the clear guard; the arm line from the rear (z 30) to the scoop top (z 22); the white JST plug near mid-length.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | tapered tub | 80 × 84 × 22 | 1 × 1.05 × 0.28 | cyan FDM, fuzzy skin | — | 1 |
| TP | stepped panel | 26 × 60 × 2 | 0.33 × 0.75 | cyan | 3–4 × M2.5 | 2 |
| SC | pointed wedge prong | 14 × 39 × 22 | 0.18 × 0.49 | cyan, integral | — | 2 |
| AR | square beam | 8 × 8 × 72 | 0.10 × 0.90 | black FDM | 2 screws front, frame rear | 2 |
| RX-F | U-bridge frame | 70 × 8 × 10 (+ feet) | 0.88 | black FDM | 4 screws (feet) | 1 |
| KN | knuckles | Ø 10 × 6 | — | black | pin | 2 |
| LK | flat bar | 5 × 6 × 50 | 0.63 | black | pins | 1 |
| HN | servo horn | 15 long | — | white | spline | 1 |
| SP | bent tray | 48 × 42 × 1.5, cheeks 10 | 0.60 × 0.53 | clear PC | 4 screws to arms | 1 |
| STK | sticker | 40 × 25 | — | white + red | adhesive | 1 |
| WH | ribbed wheel | Ø 22 × 9 | 0.28 | black rubber | N20 D-shaft | 2 |
| GM | N20 gearmotor | 12 × 10 × 25 | — | brass gearbox | clamp | 2 |
| GD | clear side plate | 30 × 20 × 1.5 | 0.38 | clear PC | 4 × M2 | 2 |
| JST | 3-pin plug | 8 × 6 × 5 | — | white | in side slot | 1 |
| S-TP | pan Phillips | head Ø 4.5 | — | silver | into CH | 6–8 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP ↔ CH walls | screwed | 0 |
| TP inner edges | channel | 14–26 |
| AR bottom ↔ TP top | resting (at rest) | 0–2 |
| AR rear ↔ RX-F | joined | 0 |
| RX-F feet ↔ CH rear corners | pivot screws | 0 |
| KN ↔ LK | pinned | 0 |
| LK ↔ HN | pinned | 0 |
| AR front ↔ SP rear flange | screwed | 0 |
| SP front edge ↔ floor | touching | 0 |
| SP-C outer ↔ SC inner face | side by side | 2–3 |
| SC tip ↔ floor | touching | 0 |
| SC tip y ↔ SP edge y | about level | 0–2 |
| WH outer ↔ GD inner | near | 1 |
| GD ↔ CH side / RX-F foot | screwed | 0 |
| WH ↔ notch walls | clearance | 1–2 |
| WH top ↔ TP top | below | −0 (z 22 both) |
| JST ↔ side wall slot | through | 0 |
| CH floor ↔ floor | above | 1–2 |

---

## 6. Mechanism
- **Drive**: two rear wheels on N20 gearmotors, skid steer; the front rests on the scoop edge and the prong tips (three-point sliding contact at the front).
- **Lifter**: the servo horn (axis along X, z ≈ 14, y ≈ +5) pulls the central link; the link pulls the knuckles at the top of the rear frame; the U-frame (rear bar, arms, scoop) rotates about the rear-corner pivots (y −42, z 12); the scoop edge, about 88 mm in front of the pivot, rises on an arc. A 20° rotation raises the edge by about **30 mm**. The scoop's bent cheeks keep the opponent centred on it while lifted.

---

## 7. Assembly order (suggested)
1. Print CH (with prongs and corner notches), TP-L/R, the black frame (arms + rear bar may be printed as one U or as 3 parts), LK.
2. Fit the two N20 gearmotors in the rear corners; press on the wheels.
3. Fit the servo under the channel, horn vertical; battery and electronics in the channel; JST lead out of the right side slot.
4. Screw the top panels on.
5. Mount the rear frame on its corner pivots; screw the clear guard plates GD over the wheels into the frame feet and side walls.
6. Pin LK between the knuckles and the horn.
7. Bend the PC scoop (front plate + side cheeks + rear flange), apply the sticker, screw it to the arm ends.

---

## 8. Hidden / uncertain list
- Pivot location (rear-corner feet preferred vs central knuckles).
- Wheel count: json says 4, photos show 2.
- Servo position and size; link geometry.
- Rear face, underside.
- Whether the arms and rear bar are one print.
- All mm ±15–20% (moderate photo quality, no cut-out).

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the body centre. +X right, +Y forward, +Z up, mm.
- Body x ∈ [−40, +40], y ∈ [−40, +44] (prong tips), z ∈ [1.5, 22]; arms to z 30; rear frame to y −44.

## 10. Profiles as math

**10.1 Body side profile (YZ).** z_top(y) = 22 for y ∈ [−40, 5]; z_top(y) = 22 − 0.564·(y − 5) for y ∈ [5, 44] (a 29.4° slope to the prong tip).

**10.2 Body plan outline.** Half-width h(y) = 40 for y ∈ [−40, 5]; h(y) = 40 − 0.10·(y − 5) for y ∈ [5, 44] (to 36 at the tip). Prong inner edge: x = ±(26.5 + 0.08·(y − 5)) for y ∈ [5, 44]; prong tip point at (±36, 44).

**10.3 Top panel inner edge (plan).** x_in(y) = ±7 for y ∈ [−35, −8]; a 45° chamfer from (±7, −8) to (±13, −2); x_in = ±13 for y ∈ [−2, 25].

**10.4 Scoop (YZ section of the front plate).** Line from (y +46, z 0) to (y +8, z 17): z = 0.447·(46 − y) (24°). Rear flange: vertical from (8, 17) to (8, 24). Cheeks: in the planes x = ±24, top edge from (46, 0) to (8, 27).

**10.5 Arm.** Line from (y −40, z 30) to (y +6, z 24): z = 30 − 0.13·(y + 40), section 8 × 8 at x ±22.

**10.6 Lift kinematics.** Pivot P = (y −42, z 12). Scoop edge E₀ = (46, 0). R = √(88² + 12²) = 88.8; φ₀ = −7.8°. Edge height z_E(θ) = 12 + 88.8·sin(θ − 7.8°). θ = 20° → z_E = 30.8.

**10.7 Wheel.** r 11, width 9, tread r(φ) = 11 + 0.4·[sin(40φ) > 0].

**10.8 Guard plate (YZ at x = ±42).** Polygon (−45, 2) → (−20, 2) → (−15, 7) → (−15, 22) → (−45, 22) → close; holes Ø 2.2 at (−42, 18), (−42, 12), (−18, 15), (−18, 9).

## 11. Pixel measurements
- **AWS63**: right wheel Ø ≈ 170 px; scoop width along its front edge ≈ 330 px (it is seen at an angle) and its length ≈ 350 px; body right side length from the guard rear (20, 490) to the prong tip (690, 800) ≈ 740 px; arm length ≈ 490 px (right arm).
- **AWS60**: wheel Ø ≈ 105 px (left), 110 px (right); body width between the outer faces of the guards ≈ 610 px (at the rear); arm spacing (centre to centre) ≈ 310 px; channel width at the rear ≈ 70 px, front ≈ 120 px; scoop width ≈ 400 px (far, smaller scale).
- **AWS57**: too blurred for measurement beyond proportions: arms ≈ 0.6 × body length.

## 12. Several independent estimates

| Quantity | Method A (known part / rule) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Wheel Ø | N20 wheel 22 | — | — | **22** |
| Body width (rear) | ≤ 101.6 | — | AWS60: 610 px / 108 px × 22 = 124?! (guards nearer than wheels? no — the wheels are at the same depth) → see 13.1 | **80** |
| Arm spacing | — | 0.55 W = 44 | AWS60: 310/108 × 22 = 63 | **44–50** |
| Body length | 101.6 − scoop overhang 2 | 1.05 W | AWS63: 740 px / 170 px × 22 = 96 (side seen at an angle → less) | **84** |
| Scoop width | W − prongs − gaps = 48 | 0.6 W | AWS60: 400 px (far end) × (far scale 0.75 of near) / (108/22) = 61 | **48–55** |
| Arm length | 72 | 0.9 W | AWS63: 490/170 × 22 = 63 | **70** |

## 13. Consistency check
1. **Width from AWS60 pixels (124 mm)** is impossible (limit 101.6). The wheels in AWS60 are partly hidden and their visible "diameter" is foreshortened (seen from above, the ellipse's short axis is the visible extent). Using the wheel's **long** axis (≈ 130 px): 610/130 × 22 = 103 → still slightly large; the guards bulge outward with perspective at the near (rear) end. **Reconciled 80–90; use 84 overall incl. guards (body 80).**
2. **Wheel count**: no front wheels are visible in AWS63's right side (the right side between the rear wheel and the prong is solid cyan wall with the JST plug). The front is supported by the scoop and prongs. **Reconciled: 2 wheels** (json "4" likely wrong).
3. **Arm spacing**: 44 (ratio) vs 63 (pixels): with arms at x ±22 they sit over the panels' outer halves as seen. **Reconciled ±23 (spacing 46).**
4. **Box fit**: 84 long + rear frame 4 = 88 ✓; width 84 ✓; height 30–36 ✓.

---

## 14. Why the designer did it (adversarial first)

- **Clear PC scoop on the floor**: thin flexible PC gets **under** opponents (closer to the floor than a printed edge) and survives hits without shattering; scratches show it has been the main contact surface. Bent cheeks stop a lifted opponent sliding off the side. Being a cheap bent sheet, it is a quick replacement.
- **Pointed side prongs**: they extend the wedge to the full width at the front corners, so opponents that miss the scoop still meet a ramp; their pointed shape lets the robot slide past walls and dig under opponents at an angle. Being part of the body, they need no extra fasteners. Weak point: printed tips blunt and chip.
- **Rear-pivot U-frame with long arms**: the long lever (≈ 89 mm) gives a big lift for a small servo angle, and the pivot at the rear corners spreads loads into the strongest part of the chassis. Square black beams are stiff and print quickly. They sit on top of the body, so when an opponent drives onto Bolt, the arms carry the load into the frame rather than into the servo.
- **Central link to a mid-body servo**: keeps the servo deep inside the body, protected; only a thin link and horn are exposed in the channel.
- **Rear wheels in corner notches + clear side guards**: wheels at the back so the scoop can sit on the floor; the clear PC plates shield the wheels' outer faces against horizontal spinners and side wedges, and tie the rear frame's feet to the body. Flush sides avoid snagging on walls.
- **Fuzzy-skin cyan body**: cosmetic, but the textured surface hides scratches; cyan is the builder's colour.
- **Open channel**: easy maintenance; protected by the arms on both sides. Weak point: overhead weapons can reach the battery.
- **JST on the side**: charging without opening the robot.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Lifter servo | 9 g micro servo, output axis along X | 23 × 12 × 23 | (−8, +5, 12), horn at (−12, +5, 14) | medium |
| Battery | 2S 180–300 mAh LiPo (purple label) | 30 × 15 × 8 | (+6, +10, 8) in the channel | high (seen) |
| RX + ESC | small combined board (e.g. Malenki-style) | 25 × 20 × 6 | (0, −20, 8) under the rear | medium |
| Motor clamps | printed cradles in the rear corners | — | (±25, −30, 6) | medium |
| Pivot screws | M3 through the frame feet into rear corner bosses | — | (±38, −42, 12) | medium |
| Power switch | the JST lead is the power link or a separate switch under a panel | — | — | low |
| Wiring | battery → (link) → ESC → motors at the rear; servo lead forward | — | — | medium |

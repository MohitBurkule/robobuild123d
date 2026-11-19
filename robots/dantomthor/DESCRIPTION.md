# Dantomthor: full rebuild description from reference photos

Source photos:
- `robots/dantomthor/reference/dantomthor.aws72.webp` (**primary**, cut out onto white): AWS 72. **Front-left three-quarter from above**, camera about 40° above the floor and about 35° left of the nose. The **front scoop** with a pale taped edge is at the bottom-left; the faceted red shell fills the middle; the **grey hammer arm** rises from a slot in the shell toward the upper right (rearward), carrying a **green plate head**.
- `robots/dantomthor/reference/dantomthor.aws70.webp`: AWS 70. A small (324 × 474) **front view**, slightly from above, on a table in front of a transmitter. Same red shell and front scoop; the arm stands nearly **vertical**, with a dark head plate.
- `robots/dantomthor/reference/dantomthor.aws65.webp`: AWS 65, an earlier version on a wooden table, **front-left from above**. **Orange-red** shell, **no separate scoop**: the shell's front is a **U** with two **pointed front horns** whose tips carry **clear tape/plastic strips**, and a clear plastic flap across the opening; the hammer head is an **aluminium** plate. Through the slot: grey hub, **purple/blue and orange** internals (battery wrap, servo). A **black chassis base** with a lightning-bolt logo shows under the rear right of the shell.

`REFERENCE.json`: `other`, 2 wheels, weapon `axe`, axis x. (No wheels are visible: they are inside the shell.)

Pixel coordinates refer to AWS72 scaled to 1162 × 1200 (copy at 1200 long side), AWS70 native 324 × 474, AWS65 native 672 × 731; ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit. Ratios use **W = shell width at the base ≈ 92 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the scoop), **+Z** = up. **Origin O** = floor point under the centre of the shell footprint (excluding the scoop).
- Arm angle **α** in the YZ plane, measured from the **−Y (rear) horizontal**, positive upward. Rest: α ≈ 55–60° (arm up and back). α = 90° vertical (AWS70). Strike: α ≈ 180°+ (down at the front).

| ID | Part |
|---|---|
| SH | faceted red shell (main body cover) |
| SH-F | shell facets (flat planar faces) |
| TW-L / TW-R | raised towers either side of the slot |
| SL | arm slot through the shell top |
| BS | black chassis base under the shell (AWS65) |
| SC | separate front scoop (AWS70/72) |
| SC-T | pale tape/clear strip along the scoop edge |
| SC-N | V-notch at the top centre of the scoop |
| HR-L / HR-R | front horns of the U-front shell (AWS65) |
| FL | clear flap/strips at the front (AWS65) |
| HB | grey pivot hub (two cylinders + shaft) |
| AR | grey printed arm |
| HD | hammer head plate (green FR4 in AWS72, aluminium in AWS65) |
| HP | brass/steel pin through the head |
| SV | servo/actuator driving the hub (hidden; partly seen) |
| WH-L / WH-R | hidden drive wheels (guess) |
| DM | hidden drive motors (guess) |
| BAT, RX, ESC | electronics (battery wrap seen in AWS65) |

---

## 1. Overall description in one paragraph

Dantomthor is a **shell-bodied hammer robot**. Almost everything is hidden under a **faceted, low-poly red printed shell** about 92 mm wide, 85 mm long and 45 mm tall, shaped like a cut gemstone or a helmet: many flat triangular and trapezoidal facets slope down from a raised central ridge to the floor all round. Down the centre of the ridge runs a **slot** between two **block-like towers**; inside it, a **grey pivot hub** carries a **grey printed arm** about 70 mm long that, at rest, points **up and backward**. At the arm's end a **flat plate** (green fibreglass in AWS72, aluminium in AWS65) is pinned **crosswise**, forming a hammer/axe head. In AWS70/72 a **separate wide scoop** wraps around the front: a red trapezoidal ramp with **45° chamfered side wings**, a **pale taped leading edge** and a small V-notch at its top. No wheels are visible: they run under the shell. When the servo fires, the arm swings over the top and slams the head down in front of the robot onto whatever the scoop has caught.

---

## 2. Part-by-part description

### 2.1 Shell (SH, SH-F)
- **Overall form**: a **faceted dome**: in plan a rounded octagon about **92 mm wide × 85 mm long**; in side view a low trapezoid rising from the floor edge to a flat ridge at **z ≈ 42–45**. Every surface is a flat facet (no curves): the photos show at least **5–6 facets per side** — a steep lower band (≈ 60° from horizontal, 10–15 mm tall), a mid band (≈ 40°), and an upper band (≈ 25°) reaching the ridge, with diagonal facets at the corners.
- **Ridge and towers (TW-L, TW-R)**: the top centre is a **raised rectangular block** about **50 mm wide × 40 mm long** at z 40–45, split down the middle by the slot SL into two **towers**, each about **18 mm wide**. Each tower's **front face** is a vertical rectangle (about 18 × 12 mm), its **rear** slopes down to the rear facets; its outer top edge is chamfered at 45°. AWS72 shows the left tower (530–780, 280–600) px and right tower (770–1000, 355–560) px; AWS65 shows both with chamfered tops.
- **Front face of the ridge block**: between the towers' fronts, below the slot, a **flat vertical front face** about 30 × 12 mm, then the shell steps down to the scoop root. AWS72 shows a **small notch/step** where the scoop's V-notch meets it.
- **Colour/material**: **red PLA** (AWS70/72; dark crimson), **orange-red** (AWS65), with clear horizontal layer lines on the steep faces and diagonal lines on the shallow ones.
- **Thickness**: about **2 mm** walls **(guess)**.
- **Lower edge**: the shell's skirt sits at **z ≈ 2–3** all round, hiding the wheels (AWS72's right side shows a darker band low on the rear-right where the black base BS is).

### 2.2 Slot (SL)
- A **rectangular slot**, about **16 mm wide (X)** and **40 mm long (Y)**, through the ridge from the front face back over the top, letting the arm swing from the rear rest to the front. Its side walls are the towers' inner faces. At its front end, the slot opens through the ridge's front face (so the arm can swing down to the front).

### 2.3 Black base (BS), AWS65
- A **black printed chassis plate/tub** under the shell, visible at the **rear right** as a dark band about **8–10 mm tall** below the shell skirt, with a **white lightning-bolt** logo on its side (AWS65 at (560–600, 500–530) px). In AWS72 a similar dark band with a small brass screw head shows at the rear right (1000–1095, 640–840) px. The shell sits **on** this base and is probably screwed to it from the sides **(guess)**.

### 2.4 Front scoop (SC, SC-T, SC-N), AWS70/72
- **Shape**: a **trapezoidal ramp** wrapping the front: a **central flat sloped face** about **62 mm wide × 34 mm long** (along the slope), at about **25–30°** from the floor, flanked by **two side wings** chamfered at **45°** in plan (each about 18 mm), so the scoop's top edge is about **62 mm** wide and its front (floor) edge is about **95 mm** wide... In AWS72 the front edge runs from (105, 820) to (720, 1120) px and the chamfered left wing from (105, 820) to (245, 610). In AWS70 the front view shows the scoop as a **wide trapezoid**: top edge with a small central V-notch, side edges sloping outward and down.
- **Top edge**: horizontal, at z ≈ 16, with a **small V-notch** (≈ 6 mm wide × 3 mm deep) on the centreline (SC-N), at (500–580, 650–690) px in AWS72.
- **Leading edge (SC-T)**: a **pale pink/white band** about **12 mm** wide along the full front edge — **clear packing tape** wrapped around the edge, scuffed white, or a **clear PC strip** glued under the printed edge.
- **Side**: the scoop's **vertical side walls** are triangles (seen at the right in AWS72 at (720–880, 900–1120) px) about 16 mm tall at the rear.
- **Attachment**: it sits in front of the shell's lower front band; probably screwed to the black base **(guess)**.

### 2.5 Front horns and flap (HR-L, HR-R, FL), AWS65 only
- Without the scoop, the shell's front is a **U** in plan: two **pointed horns** at the front corners (each a faceted wedge tapering to a sharp point on the floor, about 15 mm wide at the base, 25 mm long), with **clear tape strips** stuck to their tips extending ~5 mm, and between them a **recessed front opening** about **50 mm wide**, closed at floor level by a **clear plastic flap/strip** (a 12 mm wide clear PC/tape skirt at (150–280, 500–610) px) hinged or taped to the base.

### 2.6 Pivot hub (HB)
- **Shape**: at the front of the slot, at about **(y +8, z 34)**, a **grey printed hub**: a **horizontal shaft** along X with **two grey cylinders** (Ø about **10 mm** × 8 mm) at the slot's sides and the **arm root** between them (a larger rounded boss, about Ø 12). AWS72 shows the hub at (640–770, 420–495) px with the arm root clamped between two grey bosses; AWS65 shows two more small grey knobs on the hub sides, plus a dark grey/black part below (the servo).
- **Interpretation**: the hub is on the **output of a servo** (or a geared motor) lying in the shell's front, output axis along X **(guess)**.

### 2.7 Arm (AR)
- **Shape**: a **straight grey printed bar**, about **8 mm wide × 6 mm thick × 72 mm long** from the hub axis to the head pin. Its face shows a **recessed panel / raised logo**: AWS72 shows a sunken rectangle with a moulded **bird/eagle or lightning emblem** about two-thirds along (at (860–920, 190–260) px).
- **Pose**: AWS72 α ≈ 58° (pointing up-back); AWS65 α ≈ 50°; AWS70 α ≈ 90° (vertical).
- **Tip**: the arm end is a squared block with a **transverse hole** carrying the head pin HP.

### 2.8 Hammer head (HD, HP)
- **Shape**: a **flat rectangular plate**, about **24 mm long × 12 mm wide × 2 mm thick**, pinned **across** the arm tip so that it sticks out **both sides** of the arm in the arm's plane of motion: in AWS72 the green plate shows one part above the arm (950–1010, 25–95) px and one part below (975–1030, 195–260) px with the arm passing between — so it is a **T-head** whose long axis is **perpendicular to the arm** in the YZ plane, i.e. the plate's face points **along the arm's direction of swing** (it lands flat).
- **Material**: **green FR4/G10 fibreglass** (AWS72, with a lighter edge) and **aluminium** (AWS65, bright grey, slightly bent).
- **Pin HP**: a **brass/steel pin** (Ø 1.5–2 mm) through the arm tip and the plate (AWS72 shows a small brass pin end at (1000, 150) px on the right of the arm tip; AWS65 at (590, 105) px).

### 2.9 Wheels and drive (hidden)
- Not visible in any photo. The shell skirt sits 2–3 mm above the floor; the wheels must be **entirely under the shell**, likely **Ø 25–30 mm** wheels in slots of the black base, at x ≈ ±30, y ≈ −10 **(guess)**. The robot drives on these plus the scoop edge sliding.

### 2.10 Visible internals (AWS65)
- Through the slot: a **purple/blue** wrapped block (LiPo or servo label) and an **orange** wire/part, the grey hub, and a dark grey part (servo top).

---

## 3. Per-view sections

### 3.1 AWS72 (front-left, above)
- **Bottom-left**: the scoop (105–880, 575–1125) with the pale tape band along its front edge (105–720, 740–1125) and its V-notch.
- **Centre**: the shell's left side facets (380–560, 340–800) and front ridge (490–870, 280–700), the two towers, the slot with the hub (640–770, 420–495).
- **Right**: right-side facets (860–1100, 360–900), dark base band low at the right.
- **Top right**: the arm from the hub up to (1030, 100), the green head (945–1035, 25–260) with the brass pin.

### 3.2 AWS70 (front)
- Symmetric front view: scoop as a wide trapezoid at the bottom (30–315, 330–445) with the notch at the top centre; shell above (20–300, 170–340) with the two towers and slot; the arm standing vertically from the hub (≈ 160, 230) to the head at (150–170, 15–60).

### 3.3 AWS65 (front-left, above, older)
- U-front shell with horns at (60–100, 460–515) and (265–305, 610–680); the clear flap and tape strips; the faceted sides; towers with chamfers; slot with the grey hub, purple and orange internals; arm to the upper right; aluminium head at (530–600, 20–160).

### 3.4 Top view (synthesised, AWS72)
- Rounded octagon shell 92 × 85 with the ridge block (50 × 40) and slot (16 × 40) on the centreline; scoop in front from y +40 to +62, 95 wide at the floor, 62 wide at the top; arm along the centreline toward the rear, head over the rear facets at rest (y ≈ −30, z ≈ 95 when raised… see §10).

### 3.5 Side view (left)
- Floor line; scoop triangle at the front (y +40 to +62, up to z 16); the shell's facets rising to the ridge at z 44; the arm from the hub (y +8, z 34) up and back; the head T at its end.

### 3.6 Rear view (not photographed)
- Faceted shell rear, black base band at the bottom, the arm and head above **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| SH | faceted dome | 92 × 85 × 44 | 1 × 0.92 × 0.48 | red PLA | screws to BS (guess) | 1 |
| TW | tower block | 18 × 40 × 12 | 0.20 × 0.43 | red, integral | — | 2 |
| SL | slot | 16 × 40 | 0.17 × 0.43 | — | — | 1 |
| BS | base plate/tub | 88 × 80 × 10 | 0.96 × 0.87 | black | — | 1 |
| SC | trapezoid scoop | 95 (floor) / 62 (top) × 22 deep × 16 tall | 1.03 / 0.67 | red + tape edge | screws (guess) | 1 (AWS70/72) |
| HB | hub | Ø 10–12 × 16 | — | grey FDM | servo spline | 1 |
| AR | bar | 8 × 6 × 72 | 0.78 | grey FDM | hub + pin | 1 |
| HD | flat plate | 24 × 12 × 2 | 0.26 | green FR4 / aluminium | pin | 1 |
| HP | pin | Ø 1.8 × 12 | — | brass | press fit | 1 |
| HR | horn wedge | 15 × 25 × 12 | — | orange-red | integral | 2 (AWS65) |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| SH skirt ↔ floor | above | 2–3 |
| SH ↔ BS | sitting on, screwed | 0 |
| TW inner faces ↔ AR sides | clearance | 4 each side |
| HB ↔ TW inner faces | near | 1–2 |
| AR ↔ HB | clamped | 0 |
| HD ↔ AR tip | pinned | 0 |
| SC rear ↔ SH lower front band | touching | 0 |
| SC edge (tape) ↔ floor | touching | 0 |
| SC top edge ↔ ridge front face | below | ~20 (z 16 vs 36) |
| HD ↔ SC top (strike) | lands on/above | 0–10 |
| WH (hidden) ↔ floor | touching | 0 |

---

## 6. Mechanism
- **Drive**: two hidden wheels under the shell; skid steer.
- **Weapon**: the hub actuator (servo or geared motor) swings the arm from the rest pose (α ≈ 58°) over the top to the front (α ≈ 190°), so the head comes down in front of the shell over the scoop: an **axe/hammer**. The head strikes **flat-faced** (the plate's broad face leads), so it is a **blunt hammer** rather than a cutting axe; FR4/aluminium keeps it light so the swing is fast.
- **Self-righting**: if inverted, the shell's ridge and the arm swinging against the floor could push the robot back over **(guess)**.

---

## 7. Assembly order (suggested)
1. Print BS (with wheel slots and actuator cradle), SH, SC, AR, HB.
2. Fit the drive motors and wheels into BS.
3. Install the weapon actuator at the front centre with its output along X at z 34; battery, receiver, ESC.
4. Lower SH over BS; screw it down.
5. Fit HB and AR on the actuator output through the slot.
6. Pin HD to the arm tip with HP.
7. Screw SC to the front of BS; tape its leading edge.

---

## 8. Hidden / uncertain list
- Actuator type (servo vs high-ratio gearmotor), and drive layout.
- Wheel size and position (completely hidden).
- Whether the scoop is attached to the base or the shell.
- The head's exact orientation (T across the arm assumed).
- All mm ±15–20%.

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the shell centre; +X right, +Y forward, +Z up, mm. α from the rear horizontal, upward positive, in YZ.
- Shell x ∈ [−46, +46], y ∈ [−42, +42], z ∈ [2.5, 44]; scoop y ∈ [+40, +62]; hub axis at (y +8, z 34).

## 10. Profiles as math

**10.1 Shell side profile (YZ at x = 0, outside the slot).** Polyline: (−42, 2.5) → (−38, 15) [steep band, 72°] → (−28, 28) [mid band, 52°] → (−20, 36) → (−20, 44) [tower rear] → (+12, 44) [ridge top] → (+12, 32) [ridge front face, vertical] → (+24, 28) → (+36, 18) → (+42, 2.5).

**10.2 Shell plan outline (z = 2.5).** Octagon: (±46, ±25), (±30, ±42). Upper band (z 28): octagon (±36, ±18), (±22, ±32). Ridge block (z 44): rectangle x ∈ [−25, +25], y ∈ [−20, +12], minus the slot x ∈ [−8, +8].

**10.3 Scoop.** Central face: plane through (y 62, z 0) and (y 40, z 16): z = 16 − 0.727·(y − 40) (36°… measured 25–30° → use top at (y 38, z 13): z = 0.542·(62 − y), 28.5°). Plan outline at the floor: x ∈ [−47.5, +47.5] at y 62; top edge x ∈ [−31, +31] at y 38; wings: the 45° lines joining (±31, 38) to (±47.5, 54.5) then straight to (±47.5, 62). Notch: V of half-width 3, depth 3 at x 0 on the top edge.

**10.4 Arm and head.** Hub H = (0, 8, 34). Arm direction d(α) = (0, −cos α, sin α). Tip T(α) = H + 72·d(α). Rest α = 58°: T = (0, −30.2, 95.1). Head plate: centred on T, in the YZ plane, long axis ⟂ d: extent ±12 along n(α) = (0, sin α, cos α), thickness 2 along X?? — the plate is thin in the direction of d (it lands face-first): thickness 2 along d, 12 mm across X, 24 mm along n. At strike α = 190°: T = (0, 8 + 70.9, 34 − 12.5) = (0, 78.9, 21.5) → the head lands **just in front of the scoop edge** (y 62–79), about 20 mm above the floor — i.e. on top of an opponent sitting on the scoop.

**10.5 Hub.** Cylinders r 5 along X at (y 8, z 34), x ∈ [−8, −4] and [+4, +8]; arm root boss r 6, x ∈ [−4, +4].

## 11. Pixel measurements
- **AWS72**: scoop front edge ≈ 690 px; arm length (hub to pin) ≈ 610 px; head plate ≈ 240 px long × 60 px wide; shell width across the ridge-block front ≈ 380 px; tower width ≈ 180 px.
- **AWS70**: scoop floor width ≈ 285 px; shell max width ≈ 280 px; arm visible ≈ 200 px (foreshortened); head ≈ 25 × 45 px.
- **AWS65**: arm ≈ 360 px; head ≈ 75 × 130 px; slot width ≈ 85 px; horn-to-horn ≈ 270 px.

## 12. Several independent estimates

| Quantity | Method A (rule) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Shell width | ≤ 101.6, scoop wider → 92 | — | AWS70: shell 280 px vs scoop 285 px → ≈ equal → if scoop 95 → shell 93 | **92** |
| Shell height | ≈ 0.5 W | 46 | AWS70: shell height ≈ 140 px / 2.95 px/mm ≈ 47 | **44** |
| Arm length | cube limit: hub z 34 + arm + head 6 ≤ 101.6 → ≤ 62 when vertical?! | 0.78 W = 72 | AWS72: 610 px vs scoop 690 px (95 mm, nearer) → 84 × 0.85 (farther) ≈ 71 | **62–72** (see 13.1) |
| Head plate length | 24 | — | AWS65: 130 px vs slot 85 px (16 mm) → 24 | **24** |
| Slot width | 16 | — | AWS65 85 px vs horn spacing 270 px (≈ 50) → 16 | **16** |
| Scoop depth | 22 | — | AWS72 side ≈ 0.3 × scoop width → 28 (oblique) | **22–25** |

## 13. Consistency check
1. **Cube fit with the arm up**: hub z 34 + arm 72 = 106 > 101.6 when vertical (AWS70). Either the arm is shorter (~60 mm) or the robot is measured with the arm folded back. AWS70 shows the head above the transmitter screen — tall. **Reconciled: arm 62 mm** hub-to-pin (head top at 34 + 62 + 6 = 102 ≈ limit), shell 44 tall.
2. **Strike point**: with 62 mm, the head lands at y ≈ 8 + 61 = 69 (α 190°): ahead of the scoop edge (62) by 7 mm — the opponent caught on the scoop is hit ✓.
3. **Wheels hidden**: shell skirt at z 2.5 everywhere; the base visible only at the rear; no wheel openings seen in the left/front/right facets. Wheels must protrude only below — fine for a shell-bot.

---

## 14. Why the designer did it (adversarial first)

- **Faceted full shell**: covers the wheels and all internals, so horizontal spinners only meet sloped facets that **deflect** hits upward instead of taking them square; there are no exposed wheels to rip off. Flat facets are easy to print without supports and look like armour (theme: a Norse "thunder" hammer robot — Thor). Weak point: a printed shell is heavy relative to its strength; the slot is a gap overhead weapons can reach.
- **Separate front scoop (AWS70/72)**: added after AWS65's U-front; a wide sloped wedge with a taped edge gets under opponents and **positions them right where the hammer lands**. The 45° wings deflect angled opponents into the centre. Tape gives a thin, slippery edge.
- **U-front with horns and clear flap (AWS65)**: an earlier attempt to catch opponents in a pocket in front of the hammer; replaced by the scoop, presumably because the horns were weak and opponents escaped.
- **Overhead hammer with a light flat head**: a hammer attacks the **top** of opponents, where armour is usually thin and electronics live; a flat FR4/alu head is light so the servo swings it fast; landing flat spreads the impact (bludgeoning). The arm resting backward keeps the head out of harm's way and the centre of mass central; swinging over also helps self-right.
- **Central slot between towers**: the towers shield the hub from side hits and guide the arm.
- **Hidden wheels**: no wheel damage possible, at the cost of less clearance (the robot can be high-centred on debris).

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Weapon actuator | high-torque metal-gear servo, output along X | 23 × 12 × 28 | (0, +8, 22), output at (0, 8, 34) | medium |
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | (±22, −10, 12) along X | medium |
| Wheels | Ø 26 × 8 rubber in slots of BS | — | (±36, −10, 13) | low |
| Battery | 2S LiPo (purple/blue wrap seen) 200–300 mAh | 40 × 18 × 10 | (0, −15, 10) | medium |
| RX + ESC | combined board | 25 × 20 × 6 | (0, −30, 10) | low |
| Shell fixings | 4 × M2 screws through the lower band into BS | — | corners | low |
| Power switch | under the rear shell / base side | — | (+30, −35, 6) | low |

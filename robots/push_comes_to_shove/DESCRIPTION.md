# Push Comes to Shove: full rebuild description from reference photos

Source photos (phone photos on wooden surfaces, not cut out; both 4160 × 3120 px):
- `robots/push_comes_to_shove/reference/push_mk_1.webp` ("Mk 1"): on a light oak desk. Camera at the robot's **front-left, about 30–35° above the floor**, about **35° round from the front toward the robot's left side**. The **aluminium front wedge** faces the lower-left; the **left side plate** runs from the lower-middle to the upper-right. A clear **top plate** with a black name label is fitted.
- `robots/push_comes_to_shove/reference/push_mk_2.webp` ("Mk 2"): on pine floorboards. Camera at the robot's **front-right, about 30° high**, about **50–60° round toward the robot's right side**. The front wedge faces the **left** of the image; the **right side plate** faces the camera (lower right). The internal parts (white motor blocks numbered 1–3, wires, receiver board) are seen through the clear plastic. Mk 2 has a **darker, scuffed aluminium wedge** and a slightly different top arrangement.

Both photos show **the same basic design**: a clear **polycarbonate box** (two side plates, floor, top), an **aluminium front wedge**, an **aluminium rear plate**, and **four internal black wheels** driven by four N20-class gearmotors in **white printed motor blocks**. Everything stated as fact is read from the photos; inferences are marked **(guess)**. Dimensions are **estimates**. Scale: the AWS 150 g / 101.6 mm cube, the **M2.5/M3 pan screws** (head Ø ≈ 5 mm) at the side plate corners, the wheels (Ø ≈ 24, standard 24 mm N20 wheels), the motor blocks (an N20 is 12 × 10 × 24 mm), and the kit draft (`kit.json`: wedge, 4 internal wheels r 12 × 8 at y −24 / +16, x ±29; side plates polygon (y, z) = (−40, 1), (46, 1), (34, 25), (−52, 25) at x ±38…±40 in polycarbonate; top plate 80 × 86 × 2 at (0, −9, 26); aluminium front plate from (46, 0.5)/(48.5, 0.5) to (36, 27)/(33.5, 27) across x ±44; aluminium rear plate from (−40, 0.5)/(−42.5, 0.5) to (−55, 27)/(−52.5, 27); motors 22 × 12 × 10 at (±14, −24, 9) and (±14, +16, 9); battery 34 × 17 × 9; receiver 18 × 12 × 5; 4 standoffs r 2.2 × 22 at (±34, −34) and (±34, +30)). Ratios are against **W = width ≈ 80 mm** (side plate outer faces).

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the aluminium wedge), **+Z** = up. Units mm.
- **Origin O** = floor point under the centre of the base plate.
- Mk 1: +Y points to the lower-left of the image, +X to the upper-left (away from camera), the left side faces the camera at the right.
- Mk 2: +Y points to the left, +X toward the camera (lower right), +Z up.

| ID | Part |
|---|---|
| BP | clear base (floor) plate |
| SP-L, SP-R | clear polycarbonate side plates (parallelogram profile) |
| TP | clear top plate (with wheel notches) |
| LB | black name label with yellow writing on TP (Mk 1) |
| FWG | aluminium front wedge plate |
| RP | aluminium (or clear) rear plate, sloped |
| SO | 4 corner standoffs (hidden behind screws) |
| S-SP | pan screws through the side plates (pairs) |
| CT | small clear tab/bracket at mid-side (Mk 2, Mk 1) |
| MB1–MB4 | white printed motor blocks numbered "1"–"4" |
| M1–M4 | N20 gearmotors (inside MB) |
| WH-FL, WH-FR, WH-RL, WH-RR | four black ribbed wheels |
| BAT | LiPo battery |
| RX | receiver/ESC board (green PCB at the rear in Mk 2) |
| WR | wires (red, blue, black) |
| RT | red tape bundle (Mk 2; switch/link or fuse wrap) |
| CB | small clear cover/strap with a screw at the rear-left (Mk 2) |

---

## 1. Overall description in one paragraph

Push Comes to Shove is a **four-wheel-drive pusher/wedge built like a clear box**. Two **laser-cut clear polycarbonate side plates** about **2 mm thick**, **25 mm tall** and about **95 mm long**, each with a **parallelogram profile** (front and rear edges both leaning back by about 25° from vertical), are joined by a clear floor, a clear top plate and four **standoffs** held with **pairs of small pan screws** at each corner. Across the front, a **bent aluminium sheet wedge** (about **88 mm wide**, about 1 mm thick) slopes from the floor up and back to the top plate at about **60°**; across the rear, a similar plate slopes the **other way**, so that upside-down, driving backward, the rear plate becomes a wedge (guess, medium). Inside, **four black ribbed wheels (Ø ≈ 24 mm, 8–10 mm wide)** sit just inside the side plates at the four corners, each driven by an **N20 gearmotor in a white printed block** marked with a number (1–4) in black marker. A tangle of **red, blue and black wires**, a battery and a receiver fill the middle. In Mk 1 a **black label with yellow handwriting** ("Push comes to shove") is stuck on the clear top.

---

## 2. Part-by-part description

### 2.1 Side plates (SP-L, SP-R)
- **Shape**: flat **clear polycarbonate** (slightly blue-tinted where seen edge-on), about **2 mm thick**, at x ±38…±40. **Parallelogram side profile**:
  - **Bottom edge**: z ≈ 1 from y −40 to +46.
  - **Top edge**: z ≈ 25 from y −52 to +34.
  - **Front edge**: from (y +46, z 1) up and back to (y +34, z 25): **leaning back about 27°** from vertical (63° from the floor), parallel to the aluminium wedge.
  - **Rear edge**: from (y −40, z 1) up and back to (y −52, z 25): the **same lean**, so the top overhangs the rear.
  - All corners **slightly rounded** (r ≈ 1), edges clean (laser cut).
- **Mid-side tab (CT)**: at about y −2 to +6, a small **clear rectangular tab/plate** (about 12 × 15 mm) is fixed on the inside of each side plate with **two screws** (vertical pair): an **internal clear bracket** joining the side plate to the base plate or holding a motor block (guess, medium). In Mk 2 its outline is clearly seen as a stepped clear shape at px (620–710, 380–470) of the downscaled image.
- **Screws (S-SP)**: **silver pan-head screws**, head Ø ≈ 4.5–5 mm (M2.5 or M3), in **vertical pairs** about **8–10 mm** apart:
  - **Front pair**: near the front-bottom, at about (±40, +38, 6) and (±40, +38, 13), into the front standoff.
  - **Middle pair**: at the CT tab, about (±40, +2, 9) and (±40, +2, 17).
  - **Rear pair**: near the rear-top, at about (±40, −44, 16) and (±40, −44, 22), into the rear standoff.
  - Mk 1 also shows **single screws** at the top-rear corner of the top plate (at about (−36, −46, 27)).

### 2.2 Base plate (BP)
- **Shape**: a **clear polycarbonate plate** about **78 × 72 × 2–3 mm** (kit 78 × 72 × 3) between the side plates at z ≈ 1–3, extending from about y −38 to +40. Visible through the side plates as a thin bright line at the bottom. Probably has **four rectangular wheel cut-outs** (about 26 × 11 mm) at the corners for the wheels (guess, medium) or ends short of the wheels.

### 2.3 Top plate (TP) and label (LB)
- **Shape**: a **clear polycarbonate plate** about **80 × 86 × 2 mm**, on top of the side plates at **z ≈ 25–27**, from about y −52 to +34 (following the side plates' top edges). It has **four rectangular corner notches** (about 28 × 12 mm) where the **wheel tops** come through (Mk 1: the rear-left wheel's tread is seen above the plate surface at px (450–520, 130–165) in the downscaled image; the front-right/rear-right wheels through notches at the right). The middle region of the top therefore forms a **cross/plus-shaped plate** between the wheel notches (medium).
- **Mk 1** also shows a **second, smaller clear plate** (about 50 × 30 mm) on top of the main one near the front, with a **step** (its edges at px (270–620, 230–340)), maybe a battery hold-down or a reinforcing doubler (guess).
- **LB (Mk 1)**: a **black tape/sticker strip** about **55 × 10 mm** on the top plate, at about (0, −10), angled about 15° to X, with **yellow handwriting** reading **"Push comes to shove"** (written upside down relative to the camera), plus some white marker smudges.
- **Mk 2**: the top is clear with a bright **light reflection** at the rear-right; a small **clear strap plate** with a screw at the rear-left (CB) holds something down (battery or receiver). A metallic-grey strip runs across under the top at the rear (a **steel/aluminium plate** or a battery wrapper, px (330–560, 200–240)).

### 2.4 Front wedge (FWG)
- **Shape**: a **flat aluminium sheet** about **88 mm wide (x ±44)**, **1 mm thick**, sloping from the **floor at y ≈ +48** up and back to about **(y +35, z 27)**: slope about **62–65°** from the floor (kit: 46/48.5 → 33.5/36 at z 27). Length along slope about **30 mm**. Its **bottom edge** is straight, very slightly lifted (z ≈ 0.5), with **small dents/scratches** (the Mk 1 plate is bright, brushed, with a few scuffs; the Mk 2 plate is **dark grey, heavily scratched and stained**, with a dent near the lower right corner).
- The sheet is **folded at its top** into a short **horizontal flange** (about 4–6 mm) that lies under/over the front edge of the top plate (Mk 1 shows a slight bend line near the top).
- **Width vs side plates**: the sheet is **wider** than the side plates' outer faces by about **2–4 mm** each side, so its side edges overhang (Mk 1: the left edge of the sheet stands slightly outside the left side plate).
- **Fastening**: screwed through the side plates' front edges with the **front screw pairs** (into folded tabs or the front standoffs) (guess, medium); in Mk 2 one **screw** is seen through the sheet face near its top-left (px (230, 365)).

### 2.5 Rear plate (RP)
- **Shape**: a plate about **88 mm wide**, sloping from the floor at **y ≈ −41** up and **back** to about **(y −54, z 27)** (kit: aluminium "armor", 2.5 thick in Y projection). In Mk 1 the far end at the top-right shows a **sloped aluminium/clear face** behind the rear wheels, consistent with this.
- **Purpose**: closes the rear; inverted and driving backward it becomes a **second wedge** (guess, medium).

### 2.6 Standoffs (SO)
- **Four metal/nylon hex standoffs** about **Ø 4.4 × 22 mm** (M2.5 female-female), vertical, at about **(±34, +30)** and **(±34, −34)**, z 2–24 (kit). They are hidden behind the screws but the screw pairs line up with them. (In this design the screws may actually go into **horizontal** standoffs or blocks; the pairs of screws suggest two screws into one vertical block per corner, guess.)

### 2.7 Wheels (WH ×4)
- **Shape**: **Ø ≈ 24 mm × 9 mm**, black rubber tyres with **fine axial ribs** (about 40 ribs) on **black plastic rims**; outer face has a **raised rim lip** and a **recessed hub** (standard N20 34 mm/24 mm hobby wheels, here the small version). In Mk 2 the near wheels show a **flat dark face** (a dark disc, maybe a cover or the wheel's back face; px (440–540, 380–520)).
- **Positions (centres)**: about **(±29, +16, 12)** front and **(±29, −24, 12)** rear (kit). Wheel outer faces at x ≈ ±33.5, inside the side plates (inner faces ±38) with **≈ 4 mm** clearance. Wheel tops at **z ≈ 24**, just reaching the top plate notches.
- **Wheelbase** 40 mm, track 58 mm.

### 2.8 Motor blocks (MB1–MB4) and motors (M1–M4)
- **Shape**: **white printed blocks** about **22 × 12 × 11 mm** (long axis along X), each wrapped around an **N20 gearmotor** whose shaft points outward (toward the wheel). Top face has **two small holes** (Ø ≈ 1.5–2: screw holes for the motor's face screws, or clamp screws) and a hand-written **number in black marker**: "1", "2", "3", (and "4" hidden). A short **white tab** with a **nut/screw** extends from the block near the wheel (Mk 2 block "3" at px (590–700, 240–340) shows a rounded clamp tab with a screw). The blocks sit on the base plate.
- **Positions**: inboard of each wheel, centres about **(±14, +16, 9)** and **(±14, −24, 9)**.
- **Numbering (Mk 2)**: "1" front-right, "2" rear-left?? (The two photos show "1" and "2" side by side at the front in Mk 1 and "1" near the camera-front, "2" at the left-rear, "3" at the right-rear in Mk 2.) Numbers are likely just **motor/ESC channel IDs**; not geometrically important.

### 2.9 Electronics and wiring
- **Battery (BAT)**: a dark rectangular pack about **34 × 17 × 9 mm** in the centre (kit), wrapped in blue/black (Mk 2: blue items in the middle may be the battery wrap or connectors).
- **Receiver/ESC (RX)**: a **green/blue-green PCB** with silver components near the rear centre (Mk 2 px (330–470, 200–260)), about **25 × 15 mm**; red receiver box in the kit.
- **Wires (WR)**: **red and blue/black silicone wires** in loops between the motors and the board (Mk 1: lots of red wire in the middle; Mk 2: red/white/blue bundle).
- **RT (Mk 2)**: a **bundle wrapped in red tape**, about 15 × 10 mm, at the front-right inside (px (490–600, 350–390)): perhaps the **power link/switch** or a fuse/connector.
- **Small red/orange item** near the top-left in Mk 2 (px (600, 185)): possibly a LED or connector.

---

## 3. Per-view sections

### 3.1 Mk 1 (front-left, 30–35° high)
- Lower-left: the **bright aluminium wedge** filling the front; through the clear top behind it, the two **front motor blocks "1" and "2"** and red wiring.
- Right: the **left side plate** with its sloped front edge, three screw pairs (front-bottom px (590–610, 560–600), middle (750–770, 370–430), rear (870–890, 240–270)); the **front-left and rear-left wheels** inside it.
- Top: the **clear top plate** with the black/yellow **name label**, the smaller clear plate, the rear-right wheel tread visible at the top-left (px (450–520, 130–165)), and the rear-right wheel at (760–820, 210–290).
- Bottom: the oak desk.

### 3.2 Mk 2 (front-right, 30° high)
- Left: the **dark scratched aluminium wedge** (px (65–420, 220–690)), seen nearly face-on but sloping.
- Centre: through the clear top, **motor blocks "2" (rear-left), "1" (front-right), "3" (rear-right)**, red/blue wires, the receiver board at the rear-left, a clear strap with a screw.
- Right: the **right side plate** with front-bottom screw pair (px (390–410, 590–625)), the middle clear tab with two screws (px (660–690, 410–455)), rear screw pair (px (880–890, 275–305)); the **front-right and rear-right wheels** inside.
- Floorboards.

### 3.3 Top view (synthesised)
- An **80 × 96** outline (side plates' top edges y −52…+34; floor y −40…+48 front tip at +48); four wheels at the corners inside; top plate with corner notches; the black label in the middle; aluminium wedge across the front (y +35…+48), rear plate across the back.

### 3.4 Right side view
- A **parallelogram 25 tall**, leaning back, clear; four screws in pairs; the two right wheels (Ø 24) inside it, centres at y −24 and +16; the wedge in front following the front edge, the rear plate behind following the rear edge.

### 3.5 Front view
- The aluminium wedge 88 wide × 27 tall (slanted), the clear side plate edges at its ends, the wheel tops at the top corners just behind.

### 3.6 Rear and underside (not photographed)
- Rear: sloped rear plate. Underside: clear floor with wheel cut-outs, four contact patches, the wedge edge at the front.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| SP | parallelogram plate | 98 (diag) × 25 × 2 | 1.2 × 0.31 | clear PC, laser | screws to SO/CT | 2 |
| BP | flat plate | 78 × 72 × 2.5 | 0.98 × 0.9 | clear PC | screws | 1 |
| TP | plate with 4 notches | 80 × 86 × 2 | 1 × 1.08 | clear PC | screws | 1 |
| LB | label strip | 55 × 10 | 0.69 | black tape, yellow pen | stuck | 1 |
| FWG | bent Al sheet | 88 × 30 (slope) × 1, 63°, flange 5 | 1.1 | aluminium | screws | 1 |
| RP | sloped plate | 88 × 30 × 1 | 1.1 | aluminium | screws | 1 |
| SO | hex standoffs | Ø 4.4 × 22 | — | metal/nylon | M2.5 | 4 |
| S-SP | pan screws | head Ø 4.5–5 | — | steel | — | 12+ |
| CT | clear tab | 12 × 15 × 2 | — | clear PC | 2 screws | 2 |
| MB | white motor blocks | 22 × 12 × 11 | 0.28 | white FDM | screws | 4 |
| WH | ribbed rubber wheels | Ø 24 × 9 | 0.3 | black | N20 D-shaft | 4 |
| BAT | LiPo | 34 × 17 × 9 | — | — | strap | 1 |
| RX | PCB | 25 × 15 × 5 | — | green | — | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| SP ↔ SO | screwed | 0 |
| SP ↔ TP / BP | edge contact, screwed | 0 |
| FWG ↔ SP front edges | screwed/abutting | 0 |
| FWG side edges ↔ SP outer face (X) | overhang | 2–4 |
| FWG bottom edge ↔ floor | near/touching | 0–0.5 |
| RP bottom ↔ floor | near | 0.5 |
| WH outer face ↔ SP inner face | inside | ≈ 4 |
| WH tread ↔ TP notch edges | clearance | 1–2 |
| WH top ↔ TP top | flush/just below | −1…+1 |
| WH bottom ↔ floor | touching | 0 |
| WH front (front wheels) ↔ FWG inside | clearance | ≈ 4 |
| MB ↔ WH inner face | shaft gap | 1–2 |
| MB ↔ BP | screwed/glued | 0 |
| MB front ↔ MB rear (same side) | gap | ≈ 28 |
| BAT ↔ MBs | between | 2–3 |
| BP bottom ↔ floor | above | 1 |

---

## 6. Mechanism
1. **Drive**: four motors, four wheels, **skid steering**; all wheels inside the side plates. Pure **pusher**: the robot wins by shoving with the wedge and four-wheel traction ("push comes to shove").
2. **Wedge**: steep (≈ 63°) aluminium front; it does not get under low wedges well but presents a hard flat face for pushing and deflects spinners' hits; its bottom edge on the floor gets under robots with high front edges.
3. **Invertibility (guess, medium)**: with the parallelogram profile, flipped over the rear plate becomes a front wedge when driving in reverse, and the wheels touch the floor through the top plate notches if they protrude (wheel top ≈ top plate). Marginal; the designer may rely on not being flipped.

---

## 7. Assembly order (suggested rebuild)
1. Laser-cut **BP, SP ×2, TP, CT ×2** from 2 mm polycarbonate; cut and fold the **aluminium front wedge** (with top flange and side tabs) and **rear plate**.
2. Print **4 motor blocks**; fit N20 motors; screw blocks to BP.
3. Press **wheels** onto the motor shafts.
4. Fit **battery, receiver/ESC, switch/link**, solder and route wires.
5. Fit **standoffs** and **CT** tabs; screw on the **side plates** (pairs of screws).
6. Screw the **front wedge** and **rear plate** between the side plates.
7. Screw on the **top plate**; stick the **label**.

---

## 8. Coordinate frame (restated)
- SP at x ±38…±40; profile (y, z): (−40, 1), (46, 1), (34, 25), (−52, 25).
- TP z 25–27, y −52…+34. BP z 1–3.
- FWG: bottom (y +48, z 0.5), top (y +35, z 27), x ±44.
- RP: bottom (y −41, z 0.5), top (y −54, z 27).
- Wheels (±29, +16, 12), (±29, −24, 12). Motor blocks (±14, +16, 9), (±14, −24, 9).

## 9. Profiles as math

**9.1 Side plate.** z ∈ [1, 25]; front edge y_f(z) = 46 − 0.5·(z − 1); rear edge y_r(z) = −40 − 0.5·(z − 1) (lean atan 0.5 = 26.6° from vertical). Plate occupies y_r(z) ≤ y ≤ y_f(z).

**9.2 Front wedge.** Plane through (y 48, z 0.5) and (y 35, z 27): y = 48 − 0.49·(z − 0.5) (63.9° from the floor); flange: horizontal from (35, 27) back to (30, 27).

**9.3 Rear plate.** y = −41 − 0.49·(z − 0.5).

**9.4 Top plate with notches.** Rectangle x ±40, y −52…+34 minus four rectangles x ∈ ±[24, 38], y ∈ [+3, +29] and [−37, −11] (wheel notches 14 × 26).

**9.5 Wheel.** r(φ) = 12 + 0.4·[sin(40φ) > 0], width 9; rim lip 1.5, hub recess 2.

## 10. Pixel-based measurements (downscaled 1040 × 780 = native / 4)
- Mk 1 wedge: bottom edge (125, 400) → (525, 665); top edge (180, 255) → (600, 345).
- Mk 1 left side plate top edge: (600, 345) → (900, 205); bottom (525, 665) → (890, 420).
- Mk 1 screw pairs (heads ≈ 12–14 px): (590, 565)/(580, 595); (765, 375)/(750, 430); (880, 245)/(875, 265).
- Mk 1 front-left wheel visible (560–650, 375–470): Ø ≈ 95 px.
- Mk 2 wedge: (65, 220)–(420, 690); right side plate bottom (330, 690) → (900, 380); screws (400, 600)/(395, 620), (670, 410)/(680, 450), (885, 280)/(880, 300); front-right wheel (400–560, 380–540).

## 11. Several independent estimates

| Quantity | Method A (kit / rules) | Method B (ratios) | Method C (pixels + screws) | Reconciled |
|---|---|---|---|---|
| Scale near the front-left wheel (Mk 1) | — | — | screw head 13 px / 4.8 mm → 2.7 px/mm (downscaled) | 2.7 px/mm |
| Wheel Ø | kit 24 | ≈ 0.95 × side plate height (25) | 95 px / 2.7 → 35?? (wheel nearer the camera and partly the tyre side) → 24–28 | **24** |
| Side plate height | kit 24 | ≈ wheel Ø | — | **25** |
| Width | kit 80 (top plate) | wedge ≈ 3.5 × wheel Ø → 84; side plates ±40 | — | **80 (plates), 88 (wedge)** |
| Length (floor) | kit 86 (−40 → +46) | ≈ 1.1 × width | Mk 2 side bottom ≈ 1.15 × wedge width | **88 floor (−40 → +48), 102 overall top (−54 → +48)** |
| Wedge slope | kit 64° | Mk 2 face looks ≈ 60° | — | **63°** |
| Motor block | kit 22 × 12 × 10 | ≈ N20 + 2 mm walls | — | **22 × 12 × 11** |

## 12. Consistency check
1. **Overall length**: rear plate top at y −54 to wedge tip y +48 = **102 mm**, a hair over 101.6. Reconciled: the cube test is diagonal-tolerant only if the robot fits in any orientation; trim the rear plate lean to reach **y −53** (total 101) or accept a 1 mm shorter wedge. Use **wedge tip +47.5, rear top −53.5** (101).
2. **Wheels inside**: confirmed by both photos (wheels visible through clear plates, no tyre outside the plane of the plates). Kit agrees (`outside: false`).
3. **Two versions**: Mk 1 and Mk 2 differ only in wear (wedge colour), the label, and the top add-ons. Geometry identical (medium-high).
4. **Mass**: polycarbonate (≈ 1.2 g/cm³): SP 2 × 4.5 g, TP 10 g, BP 10 g → 29 g; aluminium 2 × 7 g = 14 g; 4 N20 = 40 g; 4 wheels 12 g; blocks 8 g; battery 15 g; RX/ESC 6 g; screws/standoffs 10 g: **≈ 134 g < 150**.

---

## 13. Why the designer did it (per part, adversarial)

- **Clear polycarbonate box**
  - Construction: laser-cut flat parts are quick, cheap, accurate; polycarbonate is **very tough** (does not shatter), ideal against spinners at this weight; clear lets the team (and judges) see inside.
  - Weakness: thin side plates (2 mm) dent and crack at screw holes after big hits.
- **Aluminium front wedge**
  - Pushing: a hard, smooth face to push opponents; the floor edge gets under robots with high fronts. Aluminium resists spinner gouging better than polycarbonate and protects the front motors.
  - Steep angle (≈ 63°) keeps the body short (more room inside for 4WD) and gives a strong pushing face rather than a long ramp; it **deflects** vertical spinner blows upward.
- **Rear plate sloped the other way**
  - Rear protection and an invertible "reverse wedge" (guess).
- **Four-wheel drive, internal wheels**
  - Maximum traction for pushing; wheels protected by the side plates from horizontal spinners and wedges.
- **Numbered white motor blocks**
  - Construction: easy motor swaps; numbers match wires to ESC channels for quick repairs.
- **Paired screws**
  - Two screws per joint stop the plates from rotating around a single screw after hits.
- **Notched top plate**
  - Lets the wheels sit high (for inverted driving or simply to fit Ø 24 wheels in a 25 mm tall box).
- **Label**
  - Identity.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Motors | 4 × N20 gearmotors (e.g. 100–300 rpm, 6 V) | 12 × 10 × 24 | in MB | high |
| ESC | dual brushed ESC driving left pair and right pair in parallel | 25 × 15 × 5 | centre | medium |
| Receiver | 2.4 GHz micro RX (green PCB seen) | 20 × 12 × 4 | rear-left | medium |
| Battery | 2S LiPo 180–300 mAh | 34 × 17 × 9 | centre (0, −4, 9) | medium |
| Switch/link | in the red-taped bundle | — | front-right inside | low |
| Standoff fastening | M2.5 screws into standoffs; CT tabs screwed into BP edges | — | — | medium |
| Wedge mounting | folded side tabs screwed through SP front screws | — | front | medium |

## 15. What the photos cannot show
- Underside, rear plate details, exact top plate outline, whether the wheels protrude above the top.
- Dimensions are estimates (±10–15%).

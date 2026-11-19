# Kharuul: full rebuild description from reference photos

Source photo (cut out onto white by the AWS wiki):
- `robots/kharuul/reference/kharuul.aws67.webp`: AWS 67, native 1892 × 1600 px. **Front, slightly right, high**: the camera is about 40° above the floor and about 15–20° to the robot's right of straight-on, fairly close. Visible: the whole front wedge (metal plate + green strip), the carbon-fibre shell's front slope and top with the team sticker, the right side with both right wheels and the side flap between them, the tops/outer faces of both left wheels. Not visible: the rear, the underside, the left side flap.

One photo only, but it is sharp and close. Facts are read from it; inferences are marked **(guess)**. Dimensions are estimates scaled from the 150 g / 101.6 mm cube limit and the project kit draft (`kit.json`: wedge type; body 80 long × 84 wide × 26 tall with a rounded side profile and chamfered plan corners; four inboard wheels r 12 × 8 at x ±36, y −26 and +24, in notches; an aluminium scoop from (y 40, z 25.6) to (y 80, z 0.4) across x ±52; a G10 strip 104 × 6 × 1.2 at the front; two scoop screws at x ±26; a 34 × 24 label on top). Ratios are against **W = shell width ≈ 84 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the metal wedge), **+Z** = up. mm.
- **Origin O** = the floor point under the centre of the carbon shell's top panel.
- In the photo the front faces the camera (lower part of the image), the right side is on the image right.

| ID | Part |
|---|---|
| SH | carbon-fibre composite shell (one moulded/laid-up skin) |
| SH-T | flat top panel |
| SH-F | front flap (curves down into the wedge) |
| SH-SR, SH-SL | side flaps (curve down between the wheels: wheel guards / side armour) |
| SH-B | rear flap (hidden, guess) |
| NT-x | wheel notches cut in the shell corners |
| FR | frayed blue fibre fringe along the cut edges |
| LB | "TEAM SIBERIAN WARLORDS" sticker |
| S-SH | 2 silver Torx button screws on the top |
| WP | metal wedge plate (purple/heat-tinted steel or titanium) |
| TP | clear packing tape over WP |
| MT | white fibreglass mesh tape strip across WP |
| S-WP | 2 Torx countersunk screws on WP (one silver, one rusty brass) |
| GS | green G10/FR4 leading-edge strip |
| WH-FL, WH-FR, WH-RL, WH-RR | four black ribbed tyres on 5-spoke hubs |
| CP | brass couplers/hubs on the motor shafts (gold colour seen inside the wheel notches) |
| M-x | drive gearmotors (hidden; brass shafts seen) |
| BAT, ESC, RX, SW | electronics (hidden, guess) |

---

## 1. Overall description in one paragraph

Kharuul is a **low, compact four-wheel wedge** whose whole body is a **single dark carbon-fibre composite shell**, like an upturned tray: a **flat top** about 84 mm wide and 70 mm long, a **front flap that curves smoothly down** into the wedge, and **side flaps that curl down between the wheels** like mudguards. The shell's corners are **cut away into notches** where four **small black ribbed wheels** (about Ø 24 mm) with five-spoke hubs poke out, front and rear on each side, mounted on **brass couplers**. The shell is battered: its cut edges are **frayed into a blue fuzz** (the inner glass/aramid layer), the top is scuffed white, and it carries a **"TEAM SIBERIAN WARLORDS" sticker** with a gear logo and two **silver Torx screws**. Across the bottom of the front slope is a **metal wedge plate** (a purple, heat-tinted look), about 62 mm wide, held with **two Torx countersunk screws**, wrapped in **clear packing tape** with a band of **white fibreglass mesh tape**, and in front of and under it a **green G10 strip** that forms the actual leading edge on the floor. No weapon: it gets under and pushes.

---

## 2. Part-by-part description

### 2.1 Carbon shell (SH)
- **Material**: **2×2 twill carbon fibre** (the weave is clearly visible, about 2.5 mm tow width), dark black-green in this light, with a **blue fibre layer** under it that shows as a **frayed blue fringe** along every cut edge (likely **blue fibreglass or aramid/Dyneema** inner plies, or a blue epoxy/peel-ply layer) **(guess)**. Thickness about **1.5–2 mm** at the edges. It looks **wet-laid over a mould** (smooth, continuous curves, no joints).
- **Top panel SH-T**: flat, about **84 mm wide × 66 mm long** (x ±42, y −36 to +30) at z ≈ 26. White scuffs and torn fibres across its front half (fight damage), a **small hole/dent** at about (−4, +8).
- **Front flap SH-F**: from the top panel's front edge (y ≈ +30), the shell **curves down** with a **large radius (R ≈ 25 mm)** into a **straight slope** at about **35–40°**, ending at about z ≈ 10 where the metal plate WP begins (the plate overlaps the shell's lower front). Width about **62–66 mm** (between the front wheel notches). Its left top corner is torn (a ragged tear at about (−34, +28)).
- **Side flaps SH-SR, SH-SL**: in the middle of each side, between the front and rear wheel notches (y ≈ −14 to +12), the shell **curls down** over the side with a **tight radius (R ≈ 8 mm)** and continues as a **near-vertical tongue** to about **z ≈ 4** (about 3–4 mm above the floor), about **26 mm long** (Y). The right flap's lower edge is **ragged and frayed blue**. These flaps **close the side between the wheels** and act as **side armour/wheel guards** for the inner sides of the wheels.
- **Wheel notches NT**: at each corner the shell is **cut away** in a rectangle about **20 mm long × 12 mm wide** (inward from the side), so the top of each wheel is open to the sky. On the right side the front notch runs from about y +12 to +32 and the rear from y −36 to −14; the top panel's edge between them is the side flap's root.
- **Rear flap SH-B**: not visible; probably curves down like the front, maybe more steeply **(guess)**.
- **Label LB**: a **blue-and-green sticker** about **34 × 24 mm** on the top centre-right (x ≈ +6, y ≈ −8), with a **black gear/sprocket logo** (12 teeth, white centre) and white/blue text "TEAM SIBERIAN WARLORDS", a **red stripe** between the blue upper half and the green lower half; edges peeling.
- **Screws S-SH**: two **silver Torx (six-lobe) button heads**, Ø ≈ 5 mm (M3), at about **(−22, −22)** (rear-left of the label, native (860, 240)) and **(+36, −2)** (right edge near the side flap, native (1580, 420)). They fix the shell to an internal frame or posts **(guess)**.

### 2.2 Metal wedge plate (WP), tape (TP), mesh (MT), screws (S-WP)
- **Shape**: a flat **rectangular plate** about **62 mm wide × 30 mm long (down the slope) × 0.8–1 mm thick**, lying on the front slope at about **31–35°**, its top edge at about (y +36, z 15) over the lower end of the shell's front flap, its bottom edge at about (y +60, z 1). The left end edge is straight; the **right lower corner is torn/bent** (a ragged notch about 5 × 5 mm).
- **Colour/material**: grey metal with a **purple/blue sheen** (heat tint): **spring steel** or **titanium** **(guess: hardened steel)**, with many scratches.
- **TP**: **clear packing tape** wrapped over most of the plate, with yellowed patches around the screws.
- **MT**: a band of **white fibreglass mesh tape** (≈ 2 mm square grid) about **12 mm wide** running across the full width about one third up from the bottom edge, under the clear tape, probably reinforcing the tape against tearing **(guess)**.
- **Screws S-WP**: two **countersunk Torx** screws (head Ø ≈ 6 mm): **left** one silver, near the top-left corner at about (x −24, 6 mm down the slope); **right** one **rusty/brass-coloured**, lower, at about (x +24, 18 mm down the slope). Not mirror-placed: the right screw is a **replacement or re-drilled hole** **(guess)**. Native positions (355, 755) and (1265, 1015).

### 2.3 Green leading-edge strip (GS)
- **Shape**: a **flat green strip** about **66 mm wide × 10–12 mm deep (Y) × 1.2 mm thick**, lying **on the floor** under/in front of WP's bottom edge, sticking out about **8–10 mm ahead** of it and about 3 mm further left than the plate. It reads speckled green: **FR4/G10 glass-epoxy** sheet **(medium)**; an alternative is green felt under the robot that the cut-out kept **(low)**. The kit draft treats it as a 104 × 6 × 1.2 G10 strip.
- **Function**: a **thin, flexible, hard leading edge** that touches the floor and gets under opponents before the metal plate.

### 2.4 Wheels (WH-x) and couplers (CP)
- **Shape**: **black plastic hubs with five curved spokes** (each about 3 mm wide) and a **ribbed black rubber tyre** (about 60 fine axial ribs). Size about **Ø 24 mm × 8 mm wide**.
- **Positions (centres)**: WH-FR (+38, +22, 12), WH-RR (+38, −25, 12), WH-FL (−38, +22, 12), WH-RL (−38, −25, 12). The outer faces at x ±42, flush with the shell's outer edge (the shell does not overhang them; the side flaps sit just inboard of the tyres' inner faces).
- **Couplers CP**: inside each wheel, a **brass/gold-coloured part** (hex coupler, collet or set-screw hub) on the motor shaft is visible (front-right at native (1490, 700); rear-right at (1680, 380)), about Ø 6 × 8 mm.
- **Heights**: tyre tops at z ≈ 24, about 2 mm below the shell top; the shell is the highest part. Inverted, the robot would rest on its shell top and could **not drive** unless the tyres are taller than they look **(guess)**.

### 2.5 Drive (hidden, guess)
- **Four N20-type gearmotors** (one per wheel) inside the shell, shafts out sideways with brass couplers. The brass parts fit common **N20 shaft-to-wheel couplers**.

---

## 3. Per-view sections

### 3.1 The photo (front-right, high)
- Bottom: the **green strip** on the floor and the **taped metal plate** above it with two screws and a mesh band.
- Middle: the **carbon front slope** curving up to the **flat top** with the sticker and two Torx screws.
- Right: the **side flap curling down** between the two right wheels, frayed blue; the wheels in their corner notches with brass couplers inside.
- Top/left: the two left wheels' tops at the rear-left and front-left.

### 3.2 Top view (plan, synthesised)
- An 84 × 66 carbon rectangle with **four rectangular corner notches** (20 × 12) holding the tyre tops; a front band (the curved flap) running to y +36; the metal plate (62 wide) to y +60; the green strip to y +68. Sticker and two screws on top.

### 3.3 Front view
- The green strip and metal plate across the bottom (66 and 62 wide), the carbon slope above, the four wheels at the sides (front ones in front of the rear ones), the top edge at z 26.

### 3.4 Right side view
- A flat top (z 26) with a smooth curve at the front down the 35° slope to the plate and strip; the **side flap** hanging between the wheels to z ≈ 4; two Ø 24 wheels at y −25 and +22 under the corner notches.

### 3.5 Rear and underside (not photographed)
- Rear: probably a curved-down flap and the rear wheels at the corners; switch likely at the rear or underside. Underside: a flat floor or the open shell with an internal chassis plate **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| SH-T | flat panel | 84 × 66 × 1.8 | 1 × 0.79 | carbon twill + blue inner ply | 2 × M3 Torx | 1 |
| SH-F | curved flap | 64 wide, R 25 + 35° slope | 0.76 | carbon | integral | 1 |
| SH-S | side flap | 26 × 22 drop | 0.31 | carbon | integral | 2 |
| NT | corner notch | 20 × 12 | 0.24 | — | — | 4 |
| LB | sticker | 34 × 24 | 0.40 | vinyl | adhesive | 1 |
| WP | flat plate | 62 × 30 × 0.9 | 0.74 × 0.36 | heat-tinted steel/Ti | 2 Torx countersunk | 1 |
| TP / MT | tape | 62 × 28 / 62 × 12 | — | clear / white mesh | adhesive | 1 + 1 |
| GS | strip | 66 × 11 × 1.2 | 0.79 | green G10 | under WP (glued/screwed) | 1 |
| WH | ribbed wheel, 5 spokes | Ø 24 × 8 | 0.29 × 0.10 | black | brass coupler | 4 |
| CP | coupler | Ø 6 × 8 | — | brass | set screw | 4 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| SH ↔ internal chassis | screwed (2 seen) | 0 |
| WP top edge ↔ SH-F | overlapping, screwed | 0 |
| WP bottom edge ↔ GS | resting on / glued | 0 |
| GS ↔ floor | touching | 0 |
| GS front edge ↔ WP bottom edge | ahead | 8–10 |
| SH-S lower edge ↔ floor | above | 3–4 |
| SH-S outer face ↔ tyre inner faces (fore-aft) | between the wheels | 2–4 to each tyre |
| NT edges ↔ tyre tread | clearance | 2–3 |
| Tyre top ↔ SH top | below | −2 |
| Tyre ↔ floor | touching | 0 |
| Front tyre ↔ rear tyre | gap | 23 |
| CP ↔ WH hub | inside | 0 |
| LB ↔ SH-T | stuck | 0 |

---

## 6. Mechanism
1. **Drive**: four-wheel skid steer, wheels at the corners.
2. **Wedge**: the green strip on the floor slips under; the 31–35° steel plate lifts the opponent's edge; the carbon slope continues the ramp; the robot pushes.
3. **Inverted**: the tyres sit below the shell top, so inverted the robot is likely stuck unless the arena floor contacts the tyres through the corner notches (the notches do expose the tyre tops; with tyres at 24 vs shell 26 it would be marginal) **(guess)**.

---

## 7. Assembly order (suggested rebuild)
1. Lay up the carbon shell on a mould (top, front flap, side flaps, rear flap); cut the four corner notches; drill the two top holes.
2. Build an internal chassis/floor with four motor clamps, the battery, ESC/receiver and switch.
3. Fit the motors, brass couplers and wheels.
4. Screw the shell onto the chassis (2 × M3 Torx at least).
5. Glue/screw the green G10 strip under the front; screw the metal wedge plate onto the front slope (2 countersunk Torx); tape it (mesh band, then clear tape).
6. Apply the team sticker.

---

## 8. Coordinate frame (restated)
- Origin O on the floor under the centre of SH-T; +X right, +Y forward, +Z up; mm.
- SH-T x ∈ [−42, 42], y ∈ [−36, 30], z 26. Front flap to (y 36, z 15). WP to (y 60, z 1). GS to y 68. Wheels (±38, +22 / −25, 12) Ø 24.

## 9. Profiles as math
- **Shell side profile (YZ, front)**: top z = 26 for y ≤ 30; arc centre (30, 1), R 25, from θ = 90° down to θ = 55° (reaching (44.3, 21.5)); then a straight slope at 35°: z = 21.5 − 0.70·(y − 44.3)… The plate overlap moves the effective slope onto WP: WP line from (36, 15) to (60, 1): z = 15 − 0.583·(y − 36) (30.3°).
- **Side flap (XZ section at y = 0)**: from the top edge (42, 26) an arc centre (34, 26), r 8, from θ = 90° to 0°, then a vertical line x = 42, z from 26 to 4. (Outer surface.)
- **Corner notches (plan)**: rectangles x ∈ ±[30, 42], y ∈ [12, 32] (front) and [−36, −14] (rear).
- **Wheel**: r(φ) = 11.5 + 0.5·[sin(60φ) > 0]; five curved spokes: φ(r) = φ_k + 0.06·(r − 3), φ_k = 72°k, r from 3 to 9.

## 10. Pixel-based measurements
Native 1892 × 1600; (x, y) from the top-left, ±10 px.
- WP corners: top-left (230, 660), top-right (1310, 690)… bottom-left (230, 1170), bottom-right (1380, 1250).
- GS: (100–1340, 1140–1360).
- Shell top: front edge ≈ y 600 at the centre; rear edge ≈ (900, 60)–(1700, 260); right edge at x ≈ 1760.
- Sticker (820–1420, 200–520). Top screws (860, 240), (1580, 420).
- Wheels: WH-FR (1450–1640, 620–1010); WH-RR (1740–1860, 250–560); WH-FL (460–610, 340–590); WH-RL (820–940, 40–200).
- Right side flap: from the top edge (1700, 500) curving down to its ragged bottom (1720–1800, 900–1000).

## 11. Several independent estimates

| Quantity | Method A (kit / rules) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Shell width | kit 84 | WP ≈ 0.74 of shell width | WP 1080–1150 px; shell at the same depth ≈ 1500 px → ratio 0.74; if WP 62 → 84 | **84** |
| WP width | kit 104 (scoop x ±52) | ≈ 0.74 W → 62 | 1150 px at ≈ 18 px/mm (near) → 64 | **62** |
| WP length (slope) | kit √(40² + 25²) = 47 | ≈ 0.48 × WP width → 30 | 510 px vertical at the front; the slope seen almost face-on from 40° → 510 / 18 ≈ 28 | **30** |
| Wheel Ø | kit 24 | ≈ 0.9 × body height | WH-FR 390 px tall at ≈ 16 px/mm → 24 | **24** |
| Body height | kit 26–28 | wheels just below the top → 26 | right flap drop ≈ 400 px at ≈ 16 → 25 | **26** |
| Shell length | kit 80 | ≈ 0.8 W | rear edge to front curve in the foreshortened view ≈ 550 px vertical / (16 × sin 40° ≈ 10.3) → 53 + front curve → ≈ 66 | **66 + front flap to 72** |
| Wheelbase | kit 50 | gap 23 + Ø 24 = 47 | WH-FR to WH-RR centres ≈ (1545, 815) to (1800, 405): 480 px oblique → ≈ 47 | **47** |

## 12. Consistency check
1. **Wedge size**: the kit's scoop (104 wide, 47 long) is much bigger than the photo's plate (62 × 30) and would break the cube. **Reconciled: WP 62 × 30 at 30–35°, GS 66 × 11.**
2. **Overall length**: shell rear −36 (−38 incl. a rear flap) to GS tip +68 = 106 mm: slightly over. Shorten the shell top to y ∈ [−33, +27] and WP/GS accordingly (GS tip +63): **total 96–98 mm.**
3. **Screw asymmetry**: right WP screw lower than the left; kept as seen.
4. **Wheel height vs shell top**: 24 vs 26; inverted drive marginal. Kept.

---

## 13. Why the designer did it (per part, mostly adversarial)

- **One-piece carbon shell**
  - Fight: carbon composite is **stiff and very light**, so most of the 150 g can go into motors and the steel wedge. The shell spreads a hit over its whole surface. The **blue inner ply (glass/aramid)** stops cracks from running through and keeps the shell together even when the carbon is chewed — the frayed edges show it held together after damage.
  - Getting under vs contact: the **curved front flap** continues the wedge ramp so an opponent lifted by the plate slides up onto the top instead of hitting a corner.
  - Weak points: cut edges fray and delaminate under spinner hits (seen all round).
  - Construction: one moulded part = no joints to fail; screws only at two points.
- **Side flaps between the wheels**
  - Fight: they **close the side** so a wedge or fork cannot get between the front and rear wheels and under the body; they also shield the motors and the inner faces of the wheels from side hits. Hanging 3–4 mm above the floor, they never take weight off the wheels.
- **Corner wheel notches**
  - Fight: the wheels are at the extreme corners, giving the widest stance (hard to tip) and good traction; the shell edge stays just above and inside the tyre, so the tyre top is the only exposed part.
- **Heat-tinted steel/titanium plate with tape and mesh**
  - Getting under vs contact: a thin hard metal plate is **far harder** than carbon or plastic, so its edge stays sharp and it does not chip when it meets an opponent's wedge or a spinner tooth. The **tape** makes the surface slick (opponents slide up) and keeps chips and fragments together; the **mesh tape** stops the clear tape from tearing.
  - Weak points: two screws only; the bottom-right corner is already torn.
- **Green G10 leading-edge strip**
  - Getting under vs contact: G10 is thin, stiff, hard and slightly flexible, so it can lie **flat on the floor** and follow small floor bumps, getting under opponents' edges before anything else. It is sacrificial and cheap to replace.
- **Small ribbed wheels on brass couplers**
  - Construction: off-the-shelf wheels; brass couplers convert N20 D-shafts to the wheel bore and survive impacts.
  - Fight: small wheels keep the robot low (26 mm), making it hard to get under.
- **Team sticker**
  - Identity; also a quick visual check that the top panel hasn't cracked.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors | 12 × 10 × 25 | transverse at y +22 and −25, x ±22, z 12 | medium |
| Chassis | printed or aluminium floor plate with motor clamps and two posts for the shell screws | 80 × 60 × 2 | z 2–4 | medium |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 10 | centre, (0, 0, 10) | medium |
| ESC + receiver | combined dual brushed ESC/receiver | 30 × 18 × 5 | front-centre | medium |
| Switch | on the rear or underside | 10 × 5 × 5 | (0, −36, 10) | low |
| WP backing | the shell's lower front or a printed nose block behind WP | — | behind WP | medium |
| Wires | short runs inside the shell | — | — | medium |

## 15. What the photo cannot show
- The rear, underside, left side flap and the inner chassis.
- Whether GS is G10 or felt.
- Exact shell curves (±3 mm).
- All mm values ±10–15%.

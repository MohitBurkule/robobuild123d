# Counterinsurgency: full rebuild description from reference photo

Source photo (one only, cut out onto white):
- `robots/counterinsurgency/reference/counterinsurgency.aws76.webp`: AWS 76. **Front three-quarter from above** (`REFERENCE.json`: front-right iso, azimuth 60°, elevation 35°). The five black prongs point toward the camera (bottom of the image). The robot's **right** end (with one wheel) is at the image left, the **left** end at the image upper right.

**Limitation**: one photo; the rear, underside and the left end's outer face are not seen. The robot is visually simple (an all-black wide box with five prongs and two end wheels), so the description is shorter than the multi-photo ones but still covers every visible part and guesses the hidden ones.

`REFERENCE.json`: `wedge`, 2 wheels, weapon wedge.

Pixel coordinates refer to a copy scaled to 1200 × 900, ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit (the robot's long axis is clearly near the 100 mm limit) and from the wheel. Ratios use **W = overall width (end cap to end cap) ≈ 100 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the prong tips), **+Z** = up. **Origin O** = floor point under the centre of the body box footprint (excluding prongs).
- The robot is **much wider than it is deep**: the body runs across X; the prongs project along +Y.

| ID | Part |
|---|---|
| CH | black body box (tub) |
| LD | textured black top lid |
| LD-S | silver screws on LD (4) |
| SL | rectangular slot in LD (link/switch) |
| FW | body front wall (between prongs) |
| FW-R | recessed front section (under the lid overhang) |
| EC-L / EC-R | end caps (outer walls beside the wheels) |
| WH-L / WH-R | drive wheels at the ends |
| PR-OR / PR-OL | outer right / outer left prongs (long tapered blades) |
| PR-CR / PR-CM / PR-CL | three central prongs (right, middle, left) |
| PT | clear/white tip insert on PR-CM |
| BAT, RX, ESC, DM-L/R | hidden internals (guess) |

---

## 1. Overall description in one paragraph

Counterinsurgency is a **wide, flat, all-black wedge/fork robot**. Its body is a **long low box** about 100 mm wide, 36 mm deep and 20 mm tall, with a **flat lid** whose top is printed with a **sparkly pebbled texture**, held by four silver screws and pierced by a **small rectangular slot** just right of centre. Two **wheels** sit at the far ends of the box, partly enclosed by **end caps**, so the robot drives "sideways" relative to its long axis like a wide bulldozer blade. From the front of the box, **five black prongs** reach forward and down to the floor: a **long tapered blade at each end** (about 60 mm long) and a **tight group of three narrower prongs** at the centre (about 50 mm long), the middle one tipped with a **clear/white insert**. The prongs are thick at the root (about the full body height) and taper to thin flat tips on the floor, so in side view each is a long triangle (a ramp).

---

## 2. Part-by-part description

### 2.1 Body box (CH)
- **Shape**: a **rectangular box**, about **100 mm wide (X) × 36 mm deep (Y) × 20 mm tall (Z)** (to the lid top), with sharp edges. The front face is vertical. The rear face is vertical **(guess, unseen)**.
- **Front wall (FW)**: between the outer prongs, the front face is a plain vertical black wall about **16 mm tall**. Between the right outer prong and the centre group (x ≈ −35 to −5, image x 230–560) the wall is **recessed about 6 mm** behind the lid's front edge, so the lid **overhangs** there (FW-R; a shadowed undercut is visible under the lid edge). Between the centre group and the left outer prong (image x 640–940) the wall is flush/near flush.
- **Material/colour**: **black PLA/PETG**; vertical faces show layer lines, the lid shows texture.

### 2.2 Lid (LD), screws (LD-S), slot (SL)
- **Shape**: a flat plate, **about 88 mm wide × 34 mm deep × 2 mm thick**, sitting in a shallow rim on top of the box at z 18–20. Its edges show a **fine knurled/ribbed border** (a 1.5 mm raised lip of the box around the lid, printed with diagonal hatching).
- **Surface**: **black with silver-white glitter speckles / pebbled texture** (a textured PEI print surface or a sparkle filament).
- **Screws**: **4 silver pan-head Phillips screws**, head Ø 4 mm (M2–M2.5): at the right front corner (x −40, y +14), at the rear middle (x 0, y −14), at the front just left of the slot (x +8, y +14), and at the left rear corner (x +40, y −12). In the photo at (205, 425), (570, 157), (665, 268) and (905, 182) px.
- **Slot (SL)**: a **rectangular opening about 7 mm wide (X) × 12 mm long (Y)**, at x ≈ −2, y ≈ +8, i.e. just behind the central prongs. Inside it, a dark part with **horizontal ridges** (a slide switch's actuator, or the socket for a removable link) is visible. **(guess: power switch/link access)**.

### 2.3 End caps (EC-L, EC-R)
- **Shape**: at each end of the box, an **outer wall** that wraps around the wheel: a black printed block whose outer face is a **rounded rectangle** in side view, about **36 mm long (Y) × 26 mm tall**, about **4 mm thick**, standing just outboard of the wheel. On the right end (photo left), its top front corner is **rounded** (radius about 8 mm) and its outer face is textured.
- **Wheel enclosure**: the wheel sits between the box end wall and this cap; the cap covers the wheel's lower outer face. The wheel's **upper part sticks out above** the cap and the lid (see WH).
- **Supports**: the cap is joined to the box at its bottom and front (continuous black, likely printed as one piece with the box) **(medium)**.

### 2.4 Wheels (WH-L, WH-R)
- **Shape**: black wheels, about **Ø 30 mm × 8 mm wide**, with a **rough textured tyre** (TPU with a pebbled/knurled surface) and a recessed hub. The right wheel (photo left) is seen edge-on at (50–160, 235–410) px; the left wheel (photo top-right) at (765–900, 45–150) px shows its outer face with a dark hub ring.
- **Position**: centres at **x ±46, y −2, z 15**. The wheel tops at z 30 stand about **10 mm above the lid** (z 20), so the robot **can drive inverted** on its wheels (the prongs would then point up).
- **Clearance**: about 1 mm to the box end walls and end caps.

### 2.5 Outer prongs (PR-OR, PR-OL)
- **Shape**: each a **long tapered black blade**: in side view a **right triangle** (ramp): root height about **18 mm** at the body front (y +18), tapering to a **flat tip about 1.5 mm thick** on the floor at **y ≈ +78** (length ≈ **60 mm**). In plan it is a **constant-width bar about 11 mm wide**. Its top face is flat, sloping at **atan(18/60) ≈ 17°**. The tip end is square-cut.
- **Position**: PR-OR at x ≈ −44 to −33 (right end, aligned under the end cap/wheel's inner side), PR-OL at x ≈ +33 to +44.
- **Surface**: the top face is **glossy-smooth with layer lines along the length**; the side faces matt. The tips are slightly worn/whitened.
- **Attachment**: printed **integral** with the box front (continuous material and layer lines at the root) **(medium)**; or slotted into the front wall **(low)**.

### 2.6 Central prong group (PR-CR, PR-CM, PR-CL, PT)
- Three prongs side by side at the centre, just in front of the slot, filling x ≈ −14 to +12:
  - **PR-CR** (right): about **8 mm wide**, tapered ramp like the outer prongs, root height 18 mm, length about **48 mm** (tip at y ≈ +66). Its side face shows a **fine ribbed (sawtooth) texture** — printed vertical serrations.
  - **PR-CM** (middle): about **9 mm wide**, slightly **shorter** at the root (its top is lower, ≈ 14 mm), length about **52 mm** (tip at y ≈ +70), ending in a **clear/white translucent tip insert (PT)** about **9 × 12 mm**, about 1.5 mm thick — a **polycarbonate or nylon sheet tip** glued or pressed into a slot in the prong's end. Its top face is smooth/glossy.
  - **PR-CL** (left): about **8 mm wide**, with a **strongly serrated side face** (a zig-zag/ribbed profile), length about **46 mm**, tip at y ≈ +64, slightly higher than the others at the root.
- **Gaps** between them about **1–2 mm** (they nearly touch, like a split blade).
- **Root**: they rise from the front wall at the slot's front edge; the box front has a **notch/step** behind them (the lid edge steps there).
- **Function**: a central "spearhead" of three blades; the clear middle tip is the thinnest edge (PC can be ~0.5 mm at its edge), so it reaches under opponents first.

---

## 3. Per-view sections

### 3.1 The photo (front-right, from above)
- **Top**: the lid (150–935, 85–445) with the 4 screws and slot (535–605, 240–300) px.
- **Left**: the right end cap (40–175, 300–520) and right wheel (50–160, 235–410); the right outer prong running from (150, 470) down to its tip at (325–385, 810–900).
- **Centre**: the three central prongs from (545–720, 300–330) down to their tips at (740–775, 650–665) (PR-CR), (775–840, 590–640) (PR-CM with the clear tip), and (850–890, 560–600) (PR-CL).
- **Right**: the left outer prong from (935, 200) to its tip (1110–1170, 410–445); the left wheel at (765–900, 45–150).
- **Front wall**: the black band under the lid, recessed region (230–560, 355–520).

### 3.2 Top view (synthesised)
- A 100 × 36 rectangle (body), with two 30 × 8 wheels at the ends inside end caps; in front five bars: 11 wide at x ±38.5 to y +78; three 8–9 wide at x −10, 0, +9 to y +64…70. The overall depth ≈ 18 + 60 + 18 = **96 mm** (y −18 to +78).

### 3.3 Front view
- A 100 × 20 box with wheel tops sticking 10 mm up at both ends; five prongs on the floor in front — two at the outer ends, three clustered at the centre; the clear tip in the middle.

### 3.4 Side view (right)
- The end cap (36 × 26) with the wheel (Ø 30) above it, the body behind it, and the outer prong as a long thin triangle from z 18 at y +18 down to the floor at y +78.

### 3.5 Rear view (not photographed)
- The 100 × 20 rear wall with the wheels at the ends; probably no features (switch in the top slot) **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | box | 100 × 36 × 18 | 1 × 0.36 × 0.18 | black FDM | — | 1 |
| LD | flat lid | 88 × 34 × 2 | 0.88 × 0.34 | black textured | 4 × M2 | 1 |
| SL | slot | 7 × 12 | — | — | — | 1 |
| EC | rounded wall | 4 × 36 × 26 | — | black | integral | 2 |
| WH | textured wheel | Ø 30 × 8 | 0.30 × 0.08 | black TPU | motor shaft | 2 |
| PR-O | ramp blade | 11 × 60 × 18→1.5 | 0.11 × 0.60 | black | integral | 2 |
| PR-CR / PR-CL | serrated ramp blade | 8 × 46–48 × 18→1.5 | 0.08 × 0.47 | black | integral | 2 |
| PR-CM | ramp blade + tip | 9 × 52 × 14→1.5 | 0.09 × 0.52 | black + clear PT | integral / glued tip | 1 |
| PT | sheet tip | 9 × 12 × 1.5 | — | clear PC/nylon | glued | 1 |
| LD-S | pan screw | head Ø 4 | — | silver | into CH | 4 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD ↔ CH rim | inset, screwed | 0 |
| LD front edge ↔ FW-R | overhang | 6 |
| PR roots ↔ FW | integral | 0 |
| PR tips ↔ floor | touching | 0 |
| PR-CR ↔ PR-CM ↔ PR-CL | side by side | 1–2 |
| PR-O inner ↔ PR-C group | clear gap | ~19–21 |
| WH ↔ CH end wall | near | 1 |
| WH ↔ EC | near | 1 |
| WH top ↔ LD top | above | +10 |
| WH bottom ↔ floor | touching | 0 |
| CH floor ↔ floor | above | 2–3 |
| PT ↔ PR-CM | glued in slot | 0 |

---

## 6. Mechanism
- **Drive**: two wheels at the ends of the long axis, skid steer, with a very wide track (≈ 92 mm) and almost no wheelbase; the front is supported by the five prong tips sliding on the floor. The rear edge of the box may touch the floor too.
- **Weapon**: none active. The prongs get under opponents; the robot then pushes them (into walls, out of the arena, onto hazards). The name suggests a **counter-robot** to "insurgent" wedges: forks beat wedges at getting under.

---

## 7. Assembly order (suggested)
1. Print CH with integral end caps and prongs (prongs printed lying down for strength along their length, or the whole robot printed upright on its rear face).
2. Install two drive gearmotors at the ends, shafts out along X; press on the wheels.
3. Fit battery, receiver/ESC and the switch/link under the slot.
4. Glue the clear tip PT into the middle prong.
5. Screw the lid on (4 screws).

---

## 8. Hidden / uncertain list
- Whether the prongs are integral or separate (fixed into front sockets).
- The exact slot content.
- Rear face, underside, internal layout.
- Wheel motor type.
- All mm ±15–20% (one photo).

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the box centre; +X right, +Y forward, +Z up, mm.
- Box x ∈ [−50, +50], y ∈ [−18, +18], z ∈ [2, 20]; wheels x ±[42, 50] to z 30; prongs to y +78.

## 10. Profiles as math

**10.1 Outer prong (YZ section, constant across its 11 mm width).** Triangle-ish polygon: (18, 0) → (78, 0) → (78, 1.5) → (18, 18) → close. Top line: z = 18 − 0.275·(y − 18) for y ∈ [18, 78] (15.4°); tip flat 1.5.

**10.2 Central prongs.** Same form with lengths: PR-CR z = 18 − 0.344·(y − 18) to y 66; PR-CM z = 14 − 0.240·(y − 18) to y 70 with PT from y 58 to 70 (thickness 1.5); PR-CL z = 18 − 0.364·(y − 18) to y 64. Serrated side faces: a sawtooth of pitch 1.5 mm and depth 0.5 mm along the length.

**10.3 Prong plan positions (x ranges).** PR-OR [−44, −33]; PR-CR [−14, −6]; PR-CM [−5, +4]; PR-CL [+5, +13]; PR-OL [+33, +44].

**10.4 End cap (YZ at x ±48…±50).** Rounded rectangle y ∈ [−18, +18], z ∈ [0, 26], corner radius 8 on the top corners.

**10.5 Wheel.** r 15, width 8, tread texture amplitude 0.4.

**10.6 Lid slot.** Rectangle x ∈ [−5.5, +1.5], y ∈ [+2, +14].

## 11. Pixel measurements (1200 × 900)
- Lid long edge (front) from (150, 445) to (935, 205): ≈ 820 px.
- Right outer prong: length ≈ 420 px from root to tip; width ≈ 70 px near the tip (nearer the camera).
- Central prongs: length ≈ 330–380 px; widths ≈ 45–65 px.
- Right wheel: ≈ 175 px tall (edge-on) × 110 px; left wheel ≈ 105 × 135 px (far).
- Slot ≈ 70 × 60 px.

## 12. Several independent estimates

| Quantity | Method A (rule) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width | ≤ 101.6 → 100 | — | — | **100** |
| Box depth | 101.6 − prongs 60 − margin ≈ 36 | — | lid short edge ≈ 270 px vs long 820 px → 0.33 → 33 (foreshortened ×1.1) → 36 | **36** |
| Prong length (outer) | 100 − 36 = 64 max | 0.6 W | 420 px vs lid 820 px = 0.51 × 100 = 51 → ×1.2 (near-camera, foreshortened along the view) ≈ 60 | **60** |
| Wheel Ø | 28–32 | 0.3 W | 175 px / 8.2 px/mm (lid scale) ≈ 21 → near-end enlarges, but edge-on height = Ø → **≈ 25–30** | **30** |
| Body height | 18–20 | — | front wall ≈ 140 px at near end / ~8.5 px/mm ≈ 16 + lid 2 | **20** |
| Prong width (outer) | 10–12 | — | 70 px at ~6.5 px/mm near the tip ≈ 11 | **11** |

## 13. Consistency check
1. **Box fit**: width 100 ✓, depth 36 + 60 = 96 ✓, height 30 (wheels) ✓.
2. **Inverted driving**: wheels 10 mm above the lid → invertible; the prongs would then be in the air, pointing up: so the robot is "fork-side up" when flipped and **has no weapon** in that state unless the prongs are symmetric — they are not. This suggests the designer accepted it (or relies on the wheels and ramp shape to roll back).
3. **Central prongs differing lengths**: seen as staggered tips (66, 70, 64) — consistent with the photo where PR-CM's clear tip is lowest/nearest.

---

## 14. Why the designer did it (adversarial first)

- **Five floor-touching prongs instead of a solid wedge**: forks beat wedges because their thin tips get under a wedge's edge; five prongs spread across the 100 mm width mean an opponent anywhere in front meets a fork. Gaps between prongs reduce the area that spinners can hit and let debris/floor seams pass. The long ramp profile (thick root, thin tip) makes each prong stiff where the bending moment is highest.
- **Clear sheet tip on the middle prong**: a sheet of PC/nylon can be ground much thinner than a printed tip, giving the very first contact point; sacrificial and replaceable.
- **Serrated sides on the central prongs**: they grip an opponent's edge sideways, stopping it from sliding off; also a printing artefact of strength-oriented infill walls **(guess)**.
- **Very wide body, wheels at the ends**: maximises frontal coverage (a 100 mm wide "blade") within the cube, and puts the wheels at the extreme ends where they also act as **side bumpers**. End caps protect the wheels' lower faces from horizontal spinners and wedges at the sides; the wheel tops stick out for invertible driving.
- **Low 20 mm box**: hard to get under (opponents meet prongs first), hard to hit with vertical spinners (small front face, protected by prongs in front).
- **Recessed front wall under the lid**: possibly to clear a motor or battery, or to save weight; the lid overhang stiffens the edge.
- **Slot switch on top**: arming without opening; recessed to resist impacts.
- **Textured lid**: printed face-down on a textured sheet — no supports needed; scratches don't show.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors along X | 12 × 10 × 25 | (±30, −2, 15) | medium |
| Battery | 2S LiPo 180–300 mAh, lying along X | 45 × 17 × 9 | (+20, 0, 9) | medium |
| RX/ESC | combined brushed ESC/RX | 25 × 20 × 6 | (−20, 0, 9) | medium |
| Switch / link | slide switch or link under SL | 10 × 6 × 6 | (−2, +8, 14) | medium |
| Prong bases | integral roots 18 tall | — | at the front wall | medium |
| Wiring | battery → switch → ESC → motors along the box | — | — | medium |

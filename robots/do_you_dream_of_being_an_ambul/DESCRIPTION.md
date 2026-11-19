# Do You Dream of Being an Ambulance: full rebuild description from reference photo

Source photo (one only, cut out onto white):
- `robots/do_you_dream_of_being_an_ambul/reference/do_you_dream_of_being_an_ambulance.aws71.webp`: AWS 71. **Front-left three-quarter from above**, camera about 40° above the floor and about 45° to the robot's left of the nose (`REFERENCE.json`: front-left iso). The two-pronged purple front is at the image left; the robot's **left** side with two wheels runs along the image bottom-right; the dark lid with a **red link** is in the middle.

**Limitations**: one photo, and it has a **strong blue-green colour cast** (the white balance is off): the wheels and lid look dark green/teal, the chassis purple. True colours are probably **black wheels, black (or very dark) lid, purple chassis/wedge** and a **red/orange link**. The right side, rear and underside are not seen and are inferred **(guess)**.

`REFERENCE.json`: `wedge`, 4 wheels, weapon wedge.

Pixel coordinates refer to a copy scaled to 1200 × 822, ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit and from the wheels (about **Ø 32 mm** gear-tread wheels with three spoke holes — a common printed or hobby wheel). Ratios use **W = body width (between the wheels) ≈ 70 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the prong tips), **+Z** = up. **Origin O** = floor point under the centre of the body tub footprint.

| ID | Part |
|---|---|
| CH | purple body tub |
| LD | dark top lid |
| LD-S | lid screws |
| LK | red removable power link in a lid window |
| LW | lid window around LK |
| TP | tape patches on the lid (right rear) |
| FW | front wedge module (purple) |
| PR-L / PR-R | the two wedge prongs (front corners) |
| RW | recessed front wall between the prongs |
| RW-S | 3 black screws on RW |
| WH-FL, WH-RL, WH-FR, WH-RR | four wheels |
| BAT, RX, ESC, DM | hidden electronics and motors (guess) |

---

## 1. Overall description in one paragraph

This robot is a **simple four-wheel box with a two-pronged wedge front**. The body is a **purple printed tub** about 70 mm wide, 72 mm long and 22 mm tall, closed by a **dark flat lid** held by small black/silver screws, with a **rectangular window** near the middle through which a **red removable link** is plugged. Four **large gear-tread wheels** (about Ø 32 × 10 mm) with **three oval cut-outs** in their faces sit outboard, two per side, and stick up well above the lid, so the robot drives either way up. The front is a **purple wedge module** the full width of the body, shaped like a **U in plan**: two **sloped prongs** at the front corners, each about 18 mm wide and 30 mm long, flanking a **deep rectangular recess** whose back is a vertical wall fixed with three black screws. The prongs' sloped faces carry a **fine grid/waffle texture**. There is no active weapon: the prongs get under opponents and the robot shoves them.

---

## 2. Part-by-part description

### 2.1 Body tub (CH)
- **Shape**: a **rectangular purple box**, about **70 mm wide (X) × 72 mm long (Y) × 20 mm tall** (to the lid underside), visible along the left side between and around the wheels (photo (500–1000, 400–580) px) as a purple band about 14 mm tall below the lid edge. The walls are flat with fine layer lines; edges sharp.
- **Rear**: not seen; vertical rear wall **(guess)**.
- **Colour/material**: **purple PLA** (strong colour, slightly translucent sheen).

### 2.2 Lid (LD, LD-S, LW, TP)
- **Shape**: a **flat dark plate** about **72 mm wide × 74 mm long × 2.5 mm thick**, slightly overhanging the tub (≈ 1 mm), its corners square. Its top edge has a **thin chamfer**.
- **Screws (LD-S)**: **6 pan-head Phillips** screws, head Ø 4 mm (M2–M2.5), silver with dark heads in the cast: at each corner (photo (315, 200), (660, 120), (920, 375)?, (520, 490)) and at mid-edges ((460, 165), (870, 210), (690, 440)). Pattern: **corners + mid-front + mid-rear** **(approximate)**.
- **Window (LW)**: a **rectangular opening** about **24 mm long (X) × 8 mm wide (Y)**, at about **x −4, y +6** (photo (520–650, 215–285) px), with a dark interior.
- **Link (LK)**: a **red/orange plastic key**, about **20 × 5 × 5 mm**, lying **in the window**, long axis along X, with a **step** near one end (a smaller tab, the plug's handle). It is a **removable power link** (e.g. a red XT30/printed shorting key) **(high)**.
- **Tape (TP)**: two **strips of clear/white tape**, torn, at the **right rear** of the lid (photo (775–940, 175–270) px), about 15 × 6 mm each — covering a hole/crack or holding something **(guess)**.

### 2.3 Front wedge module (FW, PR-L, PR-R, RW, RW-S)
- **Shape (plan)**: a **U** spanning the body width (about **74 mm**) and projecting **about 30 mm** ahead of the tub front:
  - **Prongs PR-L / PR-R**: at the two front corners, each about **18 mm wide (X)**. Each is a **ramp**: its top face slopes from the lid height (z ≈ 22) at the rear down to a **blunt tip** about **3–4 mm thick** at the floor, at about **35°**. The tip end is a **small vertical face** (photo: the right prong's tip at (25–90, 345–425) px; the left prong's tip at (185–290, 700–800) px). The prong's **outer side wall** is vertical, flush with the tub side; its **inner side wall** is vertical too.
  - **Recess**: between the prongs, a **rectangular pocket** about **38 mm wide × 25 mm deep**, open at the front and top; its floor is the ground (or a thin 2 mm floor plate) **(guess)**.
  - **Recessed front wall (RW)**: the back of the recess, a **vertical purple wall** about **38 mm wide × 18 mm tall**, carrying **3 black screw heads** in a row along it (photo (250–380, 300–500) px) — fixing the wedge module to the tub front (or holding an internal part).
- **Surface texture**: the prongs' sloped faces and the module's top show a **fine grid/waffle pattern** (printed with a textured top-surface setting or ironed pattern), clearly visible as small squares.
- **Fixing**: the module is likely a **separate print** screwed to the tub front through RW (3 screws) **(medium)**; the lid's front edge overlaps it.
- **Relation to wheels**: the front wheels sit just **behind and outboard of** the prongs; the left prong's rear outer corner nearly touches the front-left wheel's tread (gap ≈ 2–3 mm).

### 2.4 Wheels (WH-x)
- **Shape**: **Ø 32 mm × 10 mm**, **gear-tooth tread** (about 40 square teeth, 1.5 mm tall), flat outer face with **three oval/kidney cut-outs** arranged at 120° around a central hub (visible on the rear-right wheel at the top and the rear-left at the right), and a **central hub boss** Ø 8. The rear-left wheel shows a **small round centre mark** (screw).
- **Colour**: dark green/teal in the cast → probably **black** (TPU or PLA).
- **Positions**: centres at **x ±44, y +18 (front) and y −22 (rear), z 16**. Wheelbase ≈ **40 mm**; tyre gap fore-aft ≈ 8 mm; track (outer faces) ≈ **98 mm**.
- **Height**: wheel tops at z 32, about **8 mm above** the lid (z 24) → **invertible**; bottoms 2 mm below the tub floor.
- **No guards**: the outer faces are fully exposed.

---

## 3. Per-view sections

### 3.1 The photo (front-left, above)
- **Left**: the U-shaped purple wedge: right prong (20–330, 170–430), left prong (180–520, 500–800), the recess between them with the 3-screw front wall.
- **Centre**: the lid (290–1040, 85–520) with the red link in its window and the screws; tape at the right rear.
- **Wheels**: front-right (250–460, 95–190, partly hidden), rear-right (600–790, 15–120), front-left (515–790, 440–770), rear-left (930–1185, 320–580).
- **Bottom right**: the purple tub side between the left wheels.

### 3.2 Top view (synthesised)
- A 72 × 74 lid on a 70 × 72 tub, four wheels outboard (track 98, wheelbase 40), in front a 74-wide U-wedge 30 deep with a 38 × 25 recess.

### 3.3 Front view
- Two prong ramps at the outer front (18 wide each), the recess wall between them with 3 screws, the lid edge above, the wheels outboard and 8 mm higher than the lid.

### 3.4 Left side view
- The tub band (72 × 20) with two Ø 32 wheels; the prong's triangular side profile at the front from z 22 down to the floor at y +66.

### 3.5 Rear view (not photographed)
- Plain tub rear and wheels **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | tub | 70 × 72 × 20 | 1 × 1.03 × 0.29 | purple PLA | — | 1 |
| LD | flat lid | 72 × 74 × 2.5 | 1.03 × 1.06 | dark (black?) | 6 × M2 | 1 |
| LW | window | 24 × 8 | 0.34 × 0.11 | — | — | 1 |
| LK | link key | 20 × 5 × 5 | — | red | plug | 1 |
| FW | U-wedge module | 74 × 30 × 22 | 1.06 × 0.43 | purple, textured | 3 screws | 1 |
| PR | ramp prong | 18 × 30 × 22→3 | 0.26 × 0.43 | purple | integral to FW | 2 |
| RW | recess wall | 38 × 18 | 0.54 | purple | 3 × M2 | 1 |
| WH | gear-tread wheel | Ø 32 × 10, 3 holes | 0.46 | black (cast green) | motor shaft | 4 |
| TP | tape patches | 15 × 6 | — | clear/white | adhesive | 2 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD ↔ CH | screwed | 0 |
| LK ↔ LW | plugged in | 0–1 |
| FW ↔ CH front | screwed (3) | 0 |
| LD front edge ↔ FW top | overlapping/flush | 0 |
| PR tips ↔ floor | touching / ~1 above | 0–1 |
| PR-L ↔ PR-R | recess between | 38 |
| PR rear outer corner ↔ WH-F tread | near | 2–3 |
| WH inner ↔ CH side | near | 2–4 |
| WH-F ↔ WH-R | fore-aft gap | ~8 |
| WH top ↔ LD | above | +8 |
| CH floor ↔ floor | above | 2 |

---

## 6. Mechanism
- **Drive**: 4WD skid steer (four motors or two with coupled wheels), invertible.
- **Weapon**: none; the two prongs get under opponents; the recess between them can **cradle** an opponent's corner or a narrow robot, keeping it centred while pushing.

---

## 7. Assembly order (suggested)
1. Print CH, LD, FW.
2. Fit four drive gearmotors; mount the wheels.
3. Install battery, receiver, ESC; fit the link socket under LW.
4. Screw FW to the tub front (3 screws through RW).
5. Screw LD on (6 screws); insert the red link.

---

## 8. Hidden / uncertain list
- True colours (heavy cast).
- Whether the prongs' tips have metal/plastic sheet edges (they look printed and blunt).
- Motor count; internal layout; rear.
- Whether the recess has a floor.
- All mm ±15–20% (one photo).

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the tub centre; +X right, +Y forward, +Z up, mm.
- Tub x ∈ [−35, +35], y ∈ [−36, +36], z ∈ [2, 22]; lid to z 24.5; wedge y ∈ [+36, +66]; wheels x ±[39, 49].

## 10. Profiles as math

**10.1 Prong (YZ section, x ∈ ±[19, 37]).** Polygon (36, 0) → (66, 0) → (66, 3.5) → (36, 22) → close; top line z = 22 − 0.617·(y − 36) (31.7°).

**10.2 Wedge module plan.** Outer rectangle x ∈ [−37, +37], y ∈ [36, 66] minus the recess x ∈ [−19, +19], y ∈ [41, 66] (recess wall at y 41, 5 mm thick).

**10.3 Lid window.** Rectangle x ∈ [−16, +8], y ∈ [+2, +10].

**10.4 Wheel.** Root r 14.5, tip r 16, 40 teeth: r(φ) = 14.5 + 1.5·[sin(40φ) > 0], width 10. Cut-outs: 3 ellipses centred at r 8, φ = 90°, 210°, 330°, semi-axes 4.5 (tangential) × 3 (radial).

## 11. Pixel measurements (1200 × 822)
- Front-left wheel ≈ 275 × 330 px (Ø ≈ 330, near); rear-left ≈ 255 × 260 px; rear-right ≈ 190 × 105 px (far, partly hidden).
- Lid edges: front ≈ 590 px (oblique, (290, 190)–(520, 500)… ), left ≈ 560 px.
- Prong width ≈ 130–150 px; prong length ≈ 270–330 px.
- Link ≈ 110 × 35 px; window ≈ 130 × 70 px.

## 12. Several independent estimates

| Quantity | Method A (rule/typical) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Wheel Ø | 30–34 | 0.46 W | rear-left 260 px vs lid left edge 560 px (74 mm) → 34 | **32** |
| Body width | track 98 − 2 × 14 = 70 | — | lid front edge 590 px ≈ same scale as left edge → ≈ 78 (oblique) | **70–72** |
| Wedge depth | 101.6 − 72 = 30 | 0.43 W | prong length 300 px / 7.6 px/mm ≈ 39 (near, enlarged) → ×0.8 = 31 | **30** |
| Prong width | 18 | 0.26 W | 140 px / 7.6 ≈ 18 | **18** |
| Link length | 20 | — | 110 px / 7.6 × (farther ×1.1) ≈ 16 | **18–20** |

## 13. Consistency check
1. **Cube fit**: length 72 + 30 = 102 — at the limit; take tub 70 long → 100 ✓. Width 98 ✓. Height 32 ✓.
2. **Invertibility**: wheel tops 8 mm above the lid; the prongs become ramps pointing up when inverted (no front wedge in that orientation) — typical for simple wedges.
3. **Colour**: the lid's dark teal and the wheels' green in the photo both come from the cast; the purple is real (strong saturated purple survives the cast).

---

## 14. Why the designer did it (adversarial first)

- **Two corner prongs + recess**: putting wedge material at the corners gets under opponents arriving at an angle, and the recess **traps** an opponent's corner so it can't slip sideways off the front while being pushed. The prongs are cheap printed ramps; they can be reprinted as a module (3 screws). Weak points: blunt printed tips lose the under-game to metal-edged wedges/forks; the recess wall is a vertical face a vertical spinner can bite.
- **Big outboard wheels, taller than the body**: invertible driving, so flips do not end the fight; good traction for pushing. Unguarded wheels are vulnerable to horizontal spinners but save weight.
- **Low flat lid with a top link**: easy to arm; nothing to grab.
- **Textured prong faces**: printed top-surface texture; may help opponents slide **less** (holding them), or simply cosmetic.
- **Tape on the lid**: field repair over a crack or a loose part.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors, one per wheel | 12 × 10 × 25 | (±22, +18/−22, 16) | medium |
| Battery | 2S LiPo 200–300 mAh | 40 × 18 × 10 | (0, −15, 8) | medium |
| ESC + RX | combined brushed ESC/RX | 25 × 20 × 6 | (0, +15, 10) | medium |
| Link socket | 2-pin socket under LW | 20 × 8 × 8 | (−4, +6, 18) | high |
| Wedge fixing | 3 × M2 through RW into tub front bosses | — | (−12/0/+12, 41, 10) | medium |

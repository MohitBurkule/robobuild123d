# Divebomb: full rebuild description from reference photo

Source photo (one only, cut out onto white; a green background tint remains at the wedge tips):
- `robots/divebomb/reference/divebomb.aws67.webp`: AWS 67. **Front-left three-quarter from above**, camera about 40° above the floor and about 35–40° to the robot's left of the nose (`REFERENCE.json`: front-left iso). The three front prongs point to the image bottom-left; the robot's **left** side with two wheels is at the image right; the **swan-neck arm** with its spinning disc rises from the front of the robot to the top of the image.

**Limitation**: one photo; the right side, rear and underside are only partly seen or inferred **(guess)**.

`REFERENCE.json`: `other`, 4 wheels, weapon `axe`, axis x. The weapon is a **hammer-saw**: a pivoting arm (axis along X) carrying a **spinning hooked disc** on a brushless motor.

Pixel coordinates refer to a copy scaled to 1200 × 1100, ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit and from the visible **brushless outrunner** (about **Ø 28 mm**, a 2204/2206 class can) and the wheels. Ratios use **W = chassis width between the wheels ≈ 72 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the prong tips), **+Z** = up. **Origin O** = floor point under the centre of the chassis box footprint.
- Arm angle **α** in the YZ plane, measured from the **+Y (forward) horizontal**, upward positive. In the photo the arm root rises at α ≈ 100–110° (slightly back from vertical) and the neck curves further back so the head is above the chassis centre. Strike: α → ≈ 10–20° (head down in front).

| ID | Part |
|---|---|
| CH | black printed chassis box |
| TP | aluminium top plate |
| TP-S | black screws on TP |
| LK | black power link/switch tab on TP (rear left of image) |
| PR-L / PR-C / PR-R | three front prongs (left, centre, right) |
| PF | grey felt/grip sheet on the prong faces |
| PT | thin sheet tips extending beyond the prongs |
| PR-S | black screws on the prongs (2 each) |
| HB | arm pivot hub at the front edge |
| PB-1 / PB-2 | pivot bearing blocks (black) |
| PN | steel pivot pin (ends protrude) |
| GW | grey spacer/washer (bushing) on the pin |
| AR | black printed swan-neck arm |
| WT | black tape / cable ties on the arm |
| MM | black printed motor cup at the arm head |
| WM | black brushless outrunner |
| DS | dark grey hooked disc with triangular cut-out |
| DS-S | black screws on the motor cup |
| WR | black weapon wires looping to the top plate |
| WH-FL, WH-RL, WH-FR, WH-RR | four black gear-tread wheels |
| HBS | silver hub screw on the wheel |
| AA | hidden arm actuator (servo/gearmotor, guess) |
| BAT, RX, ESC | hidden electronics (guess) |

---

## 1. Overall description in one paragraph

Divebomb is a **four-wheel hammer-saw**. The chassis is a **low black printed box** about 72 mm wide, 70 mm long and 20 mm tall, closed on top by a **flat brushed-aluminium plate** held by black screws. Four **black printed wheels** with **coarse gear-tooth treads** (about Ø 30 × 10 mm) sit fully outboard, two per side. The front carries **three printed prongs**: a narrow centre prong and two wider outer ones, each a sloped ramp covered with a **grey felt/grip sheet** that continues past the printed tip as a **thin flat lip** on the floor. Between the centre and left prongs, at the front edge of the top plate, a **pivot hub** carries a **curved black "swan-neck" arm**: it rises almost vertically, then curls back, ending in a **black motor cup** that holds a **black brushless outrunner** whose bell carries a **dark grey hooked disc** with a triangular cut-out. The motor wires loop down from the arm to the top plate. In use, the arm swings forward and down, "dive-bombing" the spinning disc onto an opponent held by the prongs.

---

## 2. Part-by-part description

### 2.1 Chassis box (CH)
- **Shape**: a **rectangular black box**, about **72 mm wide (X) × 70 mm long (Y) × 18 mm tall** to the underside of the top plate. The walls are vertical with layer lines; corners are sharp. Visible on the left side (photo right) between the wheels, and at the front between the prongs (the front wall is visible in the gaps between prongs at (300–420, 560–700) and (530–600, 600–700) px).
- **Wheel mounts**: on each side, the axles come out of the side wall at about z 15. Between the front and rear wheels on the left side, a **black block with ridges** (the motor housing or a rib) is visible at (1040–1080, 495–540) px.
- **Colour/material**: matt black PLA/PETG; the prong tops show a **diagonal knurled texture** (printed with a textured top surface).

### 2.2 Top plate (TP), screws (TP-S), link (LK)
- **Shape**: a **flat aluminium sheet**, about **1.5 mm thick**, **74 mm wide × 66 mm long**, covering the whole box top (slightly overhanging at the sides), with **notches**: a **rectangular notch** at the front edge where the arm hub sits (about 20 × 12 mm), a **small notch at the rear left** (photo top-left) for the link LK, and **corner cut-outs** around the wheel positions (at the left side, two shallow notches between the wheels: (930–990, 560–585) px).
- **Finish**: brushed/scuffed bare aluminium, with scratch marks.
- **Screws**: **black pan-head Phillips**, head Ø 4 mm (M2–M2.5): front-right corner (x −30, y +30) at (325, 465) px; front-left corner (x +32, y +26) at (830, 680) px; rear-left (x +34, y −28) at (1000, 550) px; rear-right (x −28, y −30) at (535, 320) px; plus one at the rear left near LK. About **5**.
- **Link (LK)**: a **black rectangular tab**, about **6 × 3 mm** in section, standing **8 mm** up through a slot in the plate near the rear-right corner (x −22, y −20) at (375–390, 405–440) px — a **removable power link** (a printed handle on a shorting plug) **(medium)**.

### 2.3 Prongs (PR-L, PR-C, PR-R), felt (PF), tips (PT), screws (PR-S)
- **Shape**: each prong is a **sloped printed ramp**, triangular in side view, with **vertical side walls** and a **flat sloped top** at about **30°**, rising from the floor at the front to the top of the box (z ≈ 18) at the front wall. Their top faces are covered by a **grey felt-like sheet** (PF), and the sheet continues beyond the printed toe as a **thin flat lip** (PT) lying on the floor, about **10–12 mm** long.
- **Sizes and positions**:
  - **PR-R** (right, photo left): about **20 mm wide**, **38 mm long** (toe at y +73 incl. the lip), at x −34 to −14. Its outer side wall is flush with the chassis right side. **Two black screws** on its upper part (at (265, 525) and (250, 580) px).
  - **PR-C** (centre): about **14 mm wide**, **36 mm long**, at x −8 to +6. Two black screws (at (490, 650) and (470, 685) px). A **small light/LED or reflective spot** near its upper left (a blue-white glint at (485, 625)).
  - **PR-L** (left, photo bottom right): about **22 mm wide**, **42 mm long**, at x +14 to +36. It has an **extra outer side cheek** that **slopes outward** and a **wider base** that wraps forward around the front-left wheel (a triangular side wing at (730–935, 680–970) px). Two black screws (at (770, 780) and (790, 820) px).
- **Gaps**: between PR-R and PR-C about **6 mm**, between PR-C and PR-L about **8 mm** (where the arm hub's lower part sits).
- **Felt sheet (PF)**: a grey **non-woven felt / fibre sheet** (possibly **fibreglass-reinforced tape**, **grip tape** or **carbon-fibre veil**), about **0.5–1 mm** thick, with a **central fold/seam line** down each prong. It probably wraps a **thin metal/plastic sheet** that forms the floor lip **(guess)**.
- **Function**: wedges that get under opponents and hold them in the arm's strike zone.

### 2.4 Pivot hub (HB, PB-1, PB-2, PN, GW)
- **Shape**: at the front edge of the top plate, at **x ≈ +4 to +26** (left of centre), a **transverse steel pin** (PN, Ø 3 mm) about **36 mm long** runs along X, supported by **two black printed bearing blocks** (PB-1 at x ≈ −2, PB-2 at x ≈ +26), each about **10 × 10 × 14 mm** with a rounded top. The pin ends **protrude** about 5 mm beyond each block (silver ends at (495, 520) and (735, 625) px).
- **Arm root**: between the blocks, the arm's root is a **cylindrical boss** about **Ø 14 × 10 mm**, with a **grey spacer/washer GW** (Ø 14, 3 mm thick, light grey — possibly a **flanged bearing** or a nylon washer) on its right side.
- **Axis**: at about **(y +34, z 24)**.
- **Drive**: hidden; the arm root likely has a gear or lever inside the box via the front notch **(guess)**.

### 2.5 Swan-neck arm (AR) and ties (WT)
- **Shape**: a **black printed curved beam**, about **10 mm wide × 8 mm thick**, about **95 mm** along its curve: from the hub it rises **straight up** for about 40 mm, then **curves backward** (concave toward the rear) through a bend of radius about 25 mm, ending at the motor cup, which faces sideways. Its upper part widens into a **triangular gusset** with a **lightening slot** where it meets the motor cup (at (760–830, 220–300) px).
- **Head height**: the motor axis is at about **z ≈ 80**, **y ≈ +10** (above the front half of the chassis).
- **Ties (WT)**: **black electrical tape** wraps at two places along the neck (at (700–760, 300–330) and (690–730, 425–445)), and a **black cable tie** holds the wires at mid-height.

### 2.6 Weapon head (MM, WM, DS, DS-S)
- **MM**: a **black printed cup/plate**, about **Ø 30 mm × 8 mm**, at the top of the arm, axis along **X**, with **4–5 black screws** in a cross/circle (DS-S) on its outer face (at (785–830, 145–230) px).
- **WM**: a **black brushless outrunner**, about **Ø 28 × 16 mm** (bell + stator), with **copper windings** visible between the can and the mount, and a **white printed label** on its can; its bell faces the **robot's right** (photo left), carrying the disc.
- **DS**: a **dark grey (rough, sandblasted or mill-scale) steel disc**, about **3 mm thick**, outline: a circle of about **Ø 36** around the motor axis with a **large hooked tooth** extending up and forward to about **r ≈ 30 mm**, the hook outlined by a **triangular cut-out** (about 16 × 10 mm) inside the tooth root — a "beak" shape (at (565–700, 40–290) px). Its edges show grinding marks.
- **Plane**: YZ (vertical, fore-aft); spin axis along X.

### 2.7 Weapon wires (WR)
- Three **black silicone wires** from the motor run down along the back of the neck (taped), then leave the arm at about z 40 and form a **loose loop** (about 25 mm Ø) down to the top plate at about (x +18, y +10), where they enter the box through the hub notch or a slot (photo at (700–830, 490–610)).

### 2.8 Wheels (WH-x) and hub screws (HBS)
- **Shape**: **black printed wheels**, **Ø 30 × 10 mm**, with **coarse gear-tooth treads**: about **30 square teeth**, each about **2 mm tall × 2 mm wide**, across the full width. The outer face is flat with a raised **hub boss** about Ø 12; the front-left wheel shows a **silver set screw / hub screw** (HBS) at its centre.
- **Positions**: centres at **x ±44, y +16 (front) and y −20 (rear), z 15**. Wheelbase ≈ **36 mm**; fore-aft tyre gap ≈ 6 mm. Track (outer faces) ≈ **98 mm**.
- **Height**: wheel tops at z 30, about **10 mm above** the top plate → **invertible driving** (but the arm is on top).
- **No wheel guards**: the outer faces are exposed. The left prong's side wing partly shields the front-left wheel from the front.

---

## 3. Per-view sections

### 3.1 The photo (front-left, above)
- **Bottom-left**: three prongs with felt faces and floor lips: PR-R (25–360, 485–810), PR-C (320–520, 545–860), PR-L (500–935, 640–1080).
- **Centre**: the aluminium plate (275–1080, 310–700) with screws and the link; the hub with pin and grey washer (490–740, 505–645).
- **Top centre**: the arm from the hub up and curling back to the head (565–840, 40–600), the disc at (565–700, 40–290), the motor (650–790, 80–240), the cup (760–840, 120–240).
- **Right**: the left wheels: front-left (930–1060, 640–830) with hub screw; rear-left (1050–1170, 510–700).
- **Upper left**: the right wheels: front-right (230–330, 370–490), rear-right (400–520, 280–380).

### 3.2 Top view (synthesised)
- A 72 × 70 box (aluminium top), four Ø 30 × 10 wheels outboard (track 98); three prongs in front to y ≈ +73; the hub at the front edge left of centre; the arm rising there, head above y ≈ +10.

### 3.3 Front view
- Three prongs on the floor (widths 20, 14, 22) with the box behind (72 × 20), wheels to the sides; the hub at z 24 left of centre; the neck rising to the head at z 80 with the disc (Ø ~60 incl. tooth) seen edge-on.

### 3.4 Left side view
- Two gear-tread wheels Ø 30; the box behind; the left prong's triangular wing at the front; the arm rising from the front edge and curving back; the disc circle with its hook at the top.

### 3.5 Rear view (not photographed)
- The box rear, wheels at the sides, the link tab on top, the head above **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | box | 72 × 70 × 18 | 1 × 0.97 × 0.25 | black FDM | — | 1 |
| TP | notched plate | 74 × 66 × 1.5 | 1.03 × 0.92 | aluminium | 5 × M2.5 | 1 |
| LK | link tab | 6 × 3 × 8 | — | black | in socket | 1 |
| PR-R | ramp prong | 20 × 38 × 18 | 0.28 × 0.53 | black + grey felt | 2 screws | 1 |
| PR-C | ramp prong | 14 × 36 × 18 | 0.19 × 0.50 | black + felt | 2 screws | 1 |
| PR-L | ramp prong + wing | 22 × 42 × 18 | 0.31 × 0.58 | black + felt | 2 screws | 1 |
| PT | floor lip | prong width × 11 × 0.8 | — | felt-covered sheet | under PF | 3 |
| PB | bearing block | 10 × 10 × 14 | — | black | screws (guess) | 2 |
| PN | pin | Ø 3 × 36 | — | steel | — | 1 |
| GW | washer/bushing | Ø 14 × 3 | — | light grey | on PN | 1 |
| AR | swan-neck beam | 10 × 8 × 95 (curve) | 1.3 | black FDM | on PN | 1 |
| MM | motor cup | Ø 30 × 8 | 0.42 | black | 4–5 × M2 | 1 |
| WM | outrunner | Ø 28 × 16 | 0.39 | black/copper | MM | 1 |
| DS | hooked disc | Ø 36 (r 30 tooth) × 3 | 0.5 | grey steel | bell screws | 1 |
| WH | gear-tread wheel | Ø 30 × 10, 30 teeth | 0.42 | black FDM/TPU | shaft + screw | 4 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP ↔ CH | screwed | 0 |
| PR ↔ CH front wall | screwed / integral | 0 |
| PT ↔ floor | touching | 0 |
| PR-R ↔ PR-C | side gap | ~6 |
| PR-C ↔ PR-L | side gap (hub region) | ~8 |
| PB ↔ TP/CH | fixed | 0 |
| PN ↔ PB | supported | 0 |
| AR root ↔ PN | rotates/fixed to drive | 0 |
| GW ↔ AR root / PB-1 | between | 0 |
| AR ↔ MM | joined | 0 |
| WM ↔ MM | screwed | 0 |
| DS ↔ WM bell | screwed | 0 |
| WR loop ↔ TP | resting | 0 |
| WH inner ↔ CH side | near | 2–4 |
| WH-F ↔ WH-R tyres | fore-aft | ~6 |
| WH top ↔ TP | above | +10 |
| PR-L wing ↔ WH-FL tread | near | 2–3 |
| CH floor ↔ floor | above | 2 |

---

## 6. Mechanism
- **Drive**: 4WD skid steer on gear-tread wheels.
- **Weapon spin**: the outrunner spins the hooked disc directly.
- **Weapon swing**: a hidden actuator rotates the arm about PN (X axis) from its rest (head above the chassis centre, α ≈ 105° at the root) forward through ≈ 90°, so the head **dives** forward and down; the disc lands about **y ≈ +34 + 60 = +90?** → see §13: the head lands over the prongs at y ≈ +55–70.

---

## 7. Assembly order (suggested)
1. Print CH, the prongs, PB blocks, the arm and motor cup.
2. Fit 4 drive motors; mount the wheels (hub screws).
3. Install the arm actuator inside the front, battery, receiver, ESCs; fit the link socket.
4. Screw on the aluminium top plate (5 screws).
5. Mount the bearing blocks, slide the pin through PB-1, washer, arm root, PB-2.
6. Screw the motor to the cup, the disc to the bell; tape the wires along the arm, leave a slack loop into the box.
7. Screw the prongs on; apply the felt sheets with floor lips.

---

## 8. Hidden / uncertain list
- Arm actuator and coupling.
- Disc side (robot's right assumed) and tooth count (one hook seen).
- The right side and rear.
- Felt sheet material and what is under it.
- All mm ±15–20%.

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the box centre; +X right, +Y forward, +Z up, mm. α from the +Y horizontal, upward positive.
- Box x ∈ [−36, +36], y ∈ [−35, +35], z ∈ [2, 20]; wheels x ±[39, 49]; prongs y ∈ [+35, +73]; pivot (y +34, z 24) at x ∈ [−2, +26]; head axis ≈ (x +12, y +10, z 80).

## 10. Profiles as math

**10.1 Prong (YZ section).** Polygon (35, 0) → (62, 0) → (62, 1) → (35, 18) → close; top line z = 18 − 0.667·(y − 35) (33.7°). Floor lip from y 62 to 73, thickness 0.8. PR-L wing: in plan a triangle (36, 35) → (44, 35) → (36, 60) at z 0–12.

**10.2 Swan-neck centreline (YZ, at x ≈ +12).** Straight from P0 = (34, 24) up to P1 = (34, 64); arc of r = 25 centred (9, 64) from θ = 0° to θ = 70° (from +Y toward +Z): P2 = (9 + 25·cos 70°, 64 + 25·sin 70°) = (17.6, 87.5)… head axis H ≈ (14, 82). Section 10 × 8.

**10.3 Disc outline (polar about H, in the YZ plane).** r(φ) = 18 for the base circle; hook tooth for φ ∈ [60°, 120°]: r = 18 + 12·sin²((φ − 60°)·1.5); back face radial at φ = 120°. Triangular cut-out: vertices (r 14, φ 70°), (r 24, φ 90°), (r 14, φ 105°).

**10.4 Strike kinematics.** Head radius from the pivot: |H − P| = √((14 − 34)² + (82 − 24)²) = 61.4 mm at α_H = 109°. Rotating forward by Δ = 95° → α_H = 14°: H' = (34 + 61.4·cos 14°, 24 + 61.4·sin 14°) = (93.6, 38.9); the disc's lower edge at z ≈ 39 − 18 = 21 — **above** the prong lips (z 0) and **ahead** of them; Δ = 105° → H' = (94.9, 28.2)… The disc thus strikes the top of an opponent standing on/ahead of the prongs.

**10.5 Wheel.** Root r 13, tip r 15, 30 teeth: r(φ) = 13 + 2·[sin(30φ) > 0], width 10.

**10.6 Top plate.** Rectangle x ∈ [−37, +37], y ∈ [−33, +33] minus the front notch x ∈ [−2, +26], y ∈ [+24, +33] and the link slot x ∈ [−25, −19], y ∈ [−22, −18].

## 11. Pixel measurements (1200 × 1100)
- Front-left wheel ≈ 130 × 190 px (Ø ≈ 190 px, near); rear-right wheel ≈ 100 px (far).
- Motor can Ø ≈ 140 px; disc span ≈ 250 px.
- Top plate front edge ≈ 650 px (oblique); left side ≈ 520 px.
- Prong widths at their toes ≈ 150 (PR-R), 120 (PR-C), 190 (PR-L) px; lengths ≈ 330–430 px.
- Arm overall height from hub to head ≈ 520 px.

## 12. Several independent estimates

| Quantity | Method A (rule/part) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Wheel Ø | 28–32 | 0.42 W | 190 px vs motor 140 px (28 mm, farther ×0.85) → 45?? (near wheel enlarged ~1.4×) → 32 | **30** |
| Chassis width | 101.6 − 2 × 13 = 75 | — | plate front 650 px / ~8 px/mm ≈ 80 (oblique ~×0.9) = 72 | **72** |
| Arm height (hub to head) | head z ≤ 101.6 − disc r 30 = 72 | — | 520 px / ~8.5 px/mm ≈ 61 vertical | **58–62** |
| Prong length | 101.6 − 70 + 0 = ~38 incl. lip | 0.53 W | PR-R 330 px / 8.5 = 39 | **38–42** |
| Disc size | Ø 36 + hook to r 30 | — | 250 px / 6.5 (far, high) ≈ 38 across | **Ø 36, r_max 30** |

## 13. Consistency check
1. **Cube fit**: length 70 + 38 = 108 > 101.6. Reconcile: body 64 long (y ±32) and prongs 37 → 101; or the wheels define the body length. **Use body 64, prongs to y +69**.
2. **Height**: head axis z 80 + tooth r 30 = 110 > 101.6 in the photographed pose. The disc may rest lower when stored, or the arm is at an angle for measurement. **Reconciled: head axis z 72, arm straight part 32 mm.**
3. **Strike reach**: with the pivot at y +32 and head radius ≈ 55, the disc centre at the strike is at y ≈ 85: past the prong lips (69). The opponent is caught at the prongs' front (y 55–75) and the disc's lower edge sweeps through y 60–85 ✓.

---

## 14. Why the designer did it (adversarial first)

- **Hammer-saw on a front pivot**: the disc attacks the opponent's **top**, usually its weakest armour; spinning while striking turns a soft hit into cutting. Pivoting at the front edge means the full arm swing happens **in front** of the robot, right over the prongs. At rest, the head sits over the robot, so the robot's mass is central and the head is not exposed at the front. Weak points: the tall neck and head are exposed to vertical spinners and horizontal hits; the single pin hub is a stress point.
- **Swan-neck curve**: lets the head rest **over the chassis** (compact, inside the cube) while the pivot is at the front edge; when swung, the curve wraps over the opponent's front edge so the disc meets the top surface rather than the front face.
- **Three felt-covered prongs with floor lips**: the thin lips get under opponents; prongs (instead of a full wedge) leave gaps for the hub and reduce weight; felt/grip sheet on the faces may be for **traction on the opponent** (stopping them sliding off) or to cover thin metal sheet edges. The wider left prong with a wing protects the front-left wheel.
- **Aluminium top plate**: stiff and tough against overhead hits (including the robot's own disc if it overswings), light, and a good mounting base for the hub.
- **Large gear-tread wheels outboard**: traction for pushing, invertible drive; unguarded to save weight.
- **Link tab on top**: easy arming.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Arm actuator | metal-gear servo coupled to the arm root (or a high-ratio gearmotor with a spur pair) | 23 × 12 × 28 | (+12, +22, 12), output at (12, 34, 24) | medium |
| Drive motors | 4 × N20 | 12 × 10 × 25 | (±24, +16/−20, 15) | medium |
| Weapon ESC | 12–20 A | 25 × 12 × 5 | (−18, 0, 8) | medium |
| Drive ESC + RX | dual ESC + RX | 25 × 20 × 6 | (+10, −10, 8) | low |
| Battery | 2S/3S LiPo 300 mAh | 45 × 18 × 10 | (0, −15, 8) | medium |
| Link socket | 2-pin socket under LK | — | (−22, −20, 18) | medium |
| Wiring | weapon wires in through the hub notch to the ESC | — | — | medium |

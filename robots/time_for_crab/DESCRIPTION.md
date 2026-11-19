# Time For Crab: full rebuild description from reference photos

Source photos (files are named `time_for_crab_.*`):
- `robots/time_for_crab/reference/time_for_crab_.aws71.webp` (1981 × 1325 px, cut out onto white). AWS 71. Seen from the **front, slightly right of centre, about 35–40° down**. All red. It shows the body lid, both wheels, both **claws hanging down to the floor**, the **steel cross-tube**, the **yellow gear housing**, a **black gear**, a **coil spring / threaded section**, and **two googly eyes on red stalks**.
- `robots/time_for_crab/reference/time_for_crab_.aws67.webp` (1706 × 1170 px, cut out onto white). AWS 67. Nearly the same view. **Red body, orange side rails and claws, white gear housing**, black wheels with fine tread, **clear packing tape** over the lid, and **green/clear edge strips** on the claws' inner edges.
- `robots/time_for_crab/reference/time_for_crab_.aws73.webp` (639 × 517 px, on a grey table). AWS 73. Seen from the **rear-right, about 45° down**. All red. It shows the **rear face with the switch**, both wheels from behind, the lid, and the **claws raised** (tips up), with the tube, the black gear and both eye stalks between the rails.

Everything stated as fact is read from these photos. Inferences are **(guess)**. Dimensions are **estimates**. Scale anchors: AWS 150 g / 101.6 mm cube; the **steel tube** (looks like an 8 mm tube); slotted cheese-head M3 screws (head Ø 5.5 mm); the googly eyes (common 8–10 mm craft eyes); the wheels (Ø ≈ 32 mm). Reference width **W = body (lid) width ≈ 72 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the centre of the red body's footprint.
- **+X** = robot's right, **+Y** = forward (toward the claws), **+Z** = up; mm.
- Envelope (claws down): x ∈ [−50, +50], y ∈ [−30, +68], z ∈ [0, 32].

| ID | Part |
|---|---|
| BD | red printed body box |
| LD | lid (top plate) |
| LDP | textured insert panel in the lid |
| S-LD | 2 slotted cheese-head screws on the lid (+ 2 empty holes) |
| S-LDP | 1 small black screw at the panel's front edge |
| FO | open front of the body (window above the gear) |
| RL-L / RL-R | left / right side rails (fixed front arms) |
| S-RL | 1 button-head screw on top of each rail |
| TB | steel cross-tube (the claw axle) |
| CL-L / CL-R | left / right claws (rotating) |
| CLE | green/clear edge strips on the claws (AWS67) |
| GH | gear housing (yellow AWS71 / white AWS67 / black AWS73) |
| GD | driven gear on the tube (in GH) |
| GP | black gear / pinion beside GH |
| SPR | coil spring / threaded section on the tube |
| CO | steel collar on the tube |
| EY-L / EY-R | googly eyes on red stalks |
| WH-L / WH-R | two wheels |
| M-L / M-R | drive motors (hidden) |
| MW | weapon (claw) motor (hidden) |
| SW | switch on the rear face |
| S-SW | 2 screws at the switch |
| WR | wires (visible in the front opening) |

---

## 1. Overall description in one paragraph

Time For Crab is a **two-wheel robot shaped like a crab**: a **rectangular red box body** with a big wheel on each side at the back, and **two large curved claws** at the front. The claws hang from a **steel tube** that runs across the front between **two fixed side rails** projecting forward from the body's front corners. Each claw is a thick printed **hook**, curved like a crab's pincer tip. It comes down from the tube and curls **forward and then back** at the bottom, so its tip points rearward along the floor. The two claws face each other across a 40 mm gap, like a pair of pincers. The tube is turned by a **gear** in a small housing hanging under the body's front edge, so the claws can **swing up** (AWS73 shows them raised, tips up) **and down** onto the opponent. Two **googly eyes on short stalks** sit on the tube between the claws. The robot is a **front-hinged lifter / grabber**: the claws hook under or over an opponent and lift or drag it. The lid has a sparkly insert panel and two slotted screws; the switch is on the rear face.

---

## 2. Part-by-part description

### 2.1 Body (BD)
- **Shape**: a rectangular box **72 mm wide × 56 mm long × 26 mm tall** (z 4–30), with **rounded vertical corners (r ≈ 5 mm)** in plan. The walls are about **2.5 mm** thick. Strong **horizontal layer lines** on all vertical faces (AWS71: the lid edge shows about 6–8 visible layer bands over its 4 mm).
- **Underside**: about **4 mm** above the floor at the front **(guess; the wheels hold it up and the claws/rails reach the floor at the front)**.
- **Front (FO)**: the lower front of the body is **open**: a rectangular window about **60 × 14 mm** under the lid's front edge, through which the inner **wires (red and black bundle at the left)**, the **gear housing top** and a **green circuit board edge** (AWS71 and AWS67, a green line low behind the tube) are visible.
- **Rear**: a flat rear wall (AWS73) carrying the **switch SW** at the bottom centre.
- **Sides**: the wheels are mounted on the side walls near the rear; the side walls are plain.
- **Colour/material**: bright red printed PLA/PETG (glossy in AWS73, matt with scuffs in AWS71).

### 2.2 Lid (LD) and panel (LDP)
- **LD**: a flat plate **72 × 56 × 4 mm** forming the body top (z 26–30), with the same rounded corners. Its top edge has a small chamfer.
- **LDP**: a **recessed rectangular insert**, about **48 × 26 mm** with **corner radii ≈ 3 mm**, set in the middle of the lid, slightly offset to the rear. Its surface is a **rough, sparkly/grainy texture** (a textured build-plate or glitter filament print). AWS67: **covered with clear packing tape**.
- **S-LD**: **2 slotted cheese-head (pan) screws**, head Ø ≈ **5.5 mm** (M3, silver), at **two diagonal corners**: front-left (x −30, y +18) and rear-right (x +30, y −18) in AWS71 / AWS67. The **other two corners have empty round holes Ø ≈ 5 mm** (counterbored screw holes, screws missing or not needed). AWS73 shows screws at **front-left and rear-right**, and holes at **front-right and rear-left**, consistent.
- **S-LDP**: **one small black socket screw** (M2, head Ø 3.5) at the **front centre edge of the insert** (x 0, y +12). It probably holds the insert or the lid's front to an internal post.

### 2.3 Side rails (RL-L, RL-R)
- **Shape**: two thick **printed beams** projecting **forward from the body's front corners**. Each is about **14 mm wide (X) × 20 mm tall (Z)**, running from y ≈ +22 (inside the body corner) to y ≈ +44. Their **top faces are flat**, at about z ≈ 26, a little below the lid. Their **front ends** are rounded around the tube.
- **Inner faces** at x ≈ ±32, **outer faces** at x ≈ ±46. So the rails are **wider than the body** by about 10 mm each side and sit **just in front of the wheels**.
- **S-RL**: **one stainless button-head hex screw** (head Ø ≈ 5.5 mm, M3) on the top of each rail at about y ≈ +36 (AWS71: left rail at (150, 410) thumbnail px, right rail at (990, 325)). This screw probably clamps the **tube bearing** or is the rail's fixing to the body floor **(guess)**.
- **Colour**: red (AWS71/73), **orange** (AWS67).

### 2.4 Steel tube (TB)
- **Shape**: a **polished steel tube or rod, Ø ≈ 8 mm**, along X, spanning between the rails (x from −32 to +32) and **through the rails into the claws** at each end. Its axis is at **y ≈ +40, z ≈ 16**.
- **Visible features along it** (AWS71, left to right): the left eye stalk; a plain section; the **gear housing GH** around the tube at the centre-left (x ≈ −8); the **black gear GP** (x ≈ +2); the **spring/threaded section SPR** (x ≈ +8 to +14, brass-coloured coils, Ø ≈ 6); a **steel collar CO** (x ≈ +16, Ø ≈ 10 × 6 long); the right eye stalk (x ≈ +24); then the right rail.
- **Function**: the claw axle. It rotates with the claws (the claws are keyed or pinned to it) and is turned by the gear.

### 2.5 Claws (CL-L, CL-R)
- **Shape**: each claw is a **thick curved hook** (a crab's pincer tip), about **14 mm thick (X)**, printed solid. In side view:
  - The **root** is a round boss around the tube (r ≈ 10 mm about the tube axis), lying just outboard of each rail... Correction from AWS71: the root lies **on the rail's inner side in plan only partly**; the visible claw face spans x from about ±18 to ±46, i.e. the claw is **wider than the rail**: about **28 mm wide (X) at the tip**, tapering to about 14 mm at the root. The claw's outer face is flush with the rail's outer face.
  - From the root it runs **forward and down** as a curved blade, its **front (outer) face convex** (an arc of radius ≈ 30 mm), reaching the floor about **26 mm ahead of the tube** (y ≈ +66).
  - At the floor the claw **curls back**: the **tip** is a **pointed hook** facing **rearward/inward**, about 8 mm long.
  - The **rear (inner) face** is **concave** (radius ≈ 22 mm), forming the hook's throat. The **inner edges** of the two claws (facing each other) are **cut concave in front view** too: each claw's inner edge is a smooth arc, so the gap between the claws is **wider at mid-height (about 46 mm)** than at the tips (about 36 mm) and at the top (about 40 mm). Together the two claws frame a **rounded "mouth"**.
- **Edge strips CLE (AWS67)**: the claws' **inner/lower edges carry thin green-and-clear strips**, about **3 mm wide**, glued or taped along the concave edge: likely **thin polycarbonate or a strip of green FR4 / fibre tape** to give a harder, sharper biting edge **(guess)**.
- **Damage**: AWS71 shows scuffs and **chipped edges** on both claw fronts (white scratches); AWS67 shows a **chip** on the right claw.
- **Raised position** (AWS73): the claws are rotated about **100–120°** up and back: their tips point **up and slightly back** above the rails, standing about **30 mm above the rail tops**.

### 2.6 Gear housing (GH), gears (GD, GP), spring (SPR), collar (CO)
- **GH**: a printed **U-shaped block**, about **18 mm wide (X) × 16 mm deep (Y) × 20 mm tall**, hanging from the body's front underside and **straddling the tube**. In AWS71 (yellow) it has a **slot open at the top-front** and the **gear teeth of GD visible at its bottom**: a spur gear of about **Ø 18 mm, 30–36 teeth**, concentric with the tube. AWS67: **white**, same shape, with a flared lower part. AWS73: the black gear is the visible part, the housing hidden.
- **GP**: a **black gear/plate**, about **Ø 20 × 5 mm**, right next to GH on the tube (AWS71: black disc with fine teeth at x ≈ +2). In AWS73 it is a **black cylinder Ø ≈ 14 × 10 mm** at the tube centre.
  - **Interpretation (guess)**: GD + GP are the **final reduction**: a motor/gearbox inside the body drives a pinion (hidden in GH) that meshes with GD fixed on the tube. GP may be a second gear (the tube gear's twin), or the **clutch plate** of a slip clutch pressed by the spring SPR.
- **SPR**: a short **brass-coloured coil spring** (or exposed thread), **Ø ≈ 6 × 8 mm long**, between GP and CO. With CO it **preloads GP against GD**, forming a **friction slip clutch** that protects the motor when the claws are hit **(guess, medium)**.
- **CO**: a **steel shaft collar** (Ø 10 × 6) with a grub screw (not visible) holding the spring preload.

### 2.7 Googly eyes (EY-L, EY-R)
- **Shape**: each is a **craft googly eye Ø ≈ 9 mm** (white with a black pupil, clear dome), glued to the top of a **red printed stalk**: a **ring clipped round the tube** (Ø 12, 5 mm wide) with a **short upward post** (5 × 4 × 10 mm) holding the eye at **z ≈ 30**, facing forward.
- **Positions**: x ≈ −22 (left) and x ≈ +22 (right) on the tube.
- **Function**: decoration ("crab eyes"). They rotate with the tube (in AWS73 they still point up with the claws raised, so they are probably **free on the tube** or on the fixed part) **(uncertain)**.

### 2.8 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 32 mm × 9 mm** wide. AWS67: **black tyres with fine knurled / transverse-ribbed tread** (about 60 fine ribs) on a **white hub**. AWS71: **dark green** tyres, smooth. AWS73: **black** tyres on **black 5-spoke hubs** with a visible inner rim, so the tyre is a separate rubber O-ring/band.
- **Position**: centres at **x = ±41, y = −14, z = 16**. Outer faces at x = ±46 (flush with the rails' outer faces). Inner faces about 1–2 mm from the body side walls.
- **Height**: tops at z = 32, about **2 mm above the lid**. Bottoms on the floor. So the robot **can drive inverted**, just.
- **Guards**: **none**; the outer faces and treads are exposed. The rails in front partly shield the wheels' front arcs.

### 2.9 Motors (hidden) and plastic motor mounts
- **Drive (guess)**: **2 × N20 gearmotors** along X at the rear of the body, shafts out to the wheels at z = 16, in **printed cradles** in the body floor **(medium)**.
- **Weapon (guess)**: a **geared motor** (N20 high-ratio, e.g. 1000:1, or a servo with its case removed) mounted **along X** in the body's front, driving a pinion inside GH that meshes with GD. A servo is less likely because the claws travel more than 100° and the clutch spring suggests continuous rotation **(medium-low)**.

### 2.10 Switch (SW) and wires
- **SW** (AWS73): at the **bottom centre of the rear face**, a small **slide/toggle switch** between **2 silver pan screws (S-SW)** about **8 mm apart**, plus a dark slot. It is a mini switch screwed through the rear wall.
- **Wires**: a **red-and-black twisted pair** and a **thin orange/brown lead** visible at the left of the front opening (AWS71, AWS67), running down toward the weapon motor area. A **green PCB edge** is visible low behind the tube.

---

## 3. Per-view descriptions

### 3.1 Top view
- A red rounded rectangle (72 × 56) with a sparkly inset panel, 2 slotted screws on diagonal corners and 2 holes on the others. Wheels as dark rectangles (9 × 32) on both sides at the rear half. In front, two rails (14 wide) stick forward from the corners to y ≈ +44, joined by the steel tube with a gear block and two eye stalks. The claws curve ahead of the rails to y ≈ +68, their inner edges forming a rounded mouth about 40 mm wide.

### 3.2 Front view (AWS71, AWS67)
- Two big curved claws dominate, hanging from the tube to the floor, framing a rounded gap. Between them, at mid-height, the tube with the gear housing, black gear, spring, collar and two googly eyes. Above, the body front opening and the lid edge. Wheels peek out at both sides, behind and above the rails.

### 3.3 Side view (inferred)
- A rectangular body (56 × 26) on a wheel (Ø 32) at the rear. A rail sticking forward at mid-height, ending at the tube. The claw drops from the tube in a convex arc to the floor and curls back into a rearward-pointing tip. Overall length about 98 mm.

### 3.4 Rear view (AWS73)
- The plain rear wall with the switch and its 2 screws at the bottom. Wheels at the corners, about 2 mm taller than the lid. Over the lid: the raised claws, two red hooks curving up.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 72 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | rounded box | 72 × 56 × 26 | 1 × 0.78 × 0.36 | red FDM | — | 1 |
| LD | plate | 72 × 56 × 4 | — | red | 2 × M3 slotted | 1 |
| LDP | inset panel | 48 × 26 | 0.67 × 0.36 | sparkly red (tape AWS67) | 1 × M2 | 1 |
| RL | beam | 14 × 22 × 20 | 0.19 × 0.31 × 0.28 | red / orange | 1 × M3 button + body | 2 |
| TB | tube | Ø 8 × ~92 | 0.11 × 1.28 | steel | through the rails | 1 |
| CL | curved hook | 28 × 30 × 32 (tip ⟂) | 0.39 × 0.42 × 0.44 | red / orange (+ green edge) | keyed to TB | 2 |
| GH | U-block | 18 × 16 × 20 | 0.25 | yellow / white / black | to body front | 1 |
| GD | spur gear | Ø 18, ~32 teeth | — | printed | on TB | 1 |
| GP | gear/plate | Ø 20 × 5 | — | black | on TB | 1 |
| SPR | coil spring | Ø 6 × 8 | — | brass/steel | on TB | 1 |
| CO | collar | Ø 10 × 6 | — | steel | grub screw | 1 |
| EY | googly eye + stalk | Ø 9 eye, 12 ring | — | white/black + red | glued / clipped | 2 |
| WH | wheel | Ø 32 × 9 | 0.44 × 0.13 | black/green tyre | motor shaft | 2 |
| SW | mini switch | 10 × 6 × 6 | — | — | 2 × M2 | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD ↔ BD walls | screwed (2) | 0 |
| LDP ↔ LD | inset, flush | 0 |
| RL ↔ BD front corners | joined (integral or screwed) | 0 |
| TB ↔ RL | journalled through | 0.1–0.2 radial |
| CL root ↔ TB | keyed/pinned | 0 |
| CL root inner face ↔ RL outer/inner face | side by side | ~1 |
| CL tip ↔ floor (down position) | touching | 0 |
| CL-L inner edge ↔ CL-R inner edge | mouth gap | 36–46 |
| CL front ↔ RL front end | ahead of | ~24 |
| GH ↔ BD underside | fixed | 0 |
| GD ↔ TB | fixed | 0 |
| GP ↔ GD | pressed (clutch, guess) | 0 |
| SPR ↔ GP / CO | compressed between | 0 |
| EY stalk ↔ TB | ring round the tube | 0 |
| EY top ↔ LD front edge | below the lid | ~0–2 |
| WH inner face ↔ BD side | near | 1–2 |
| WH front ↔ RL rear | near | 2–4 |
| WH top ↔ LD top | wheel proud | +2 |
| WH bottom ↔ floor | touching | 0 |
| BD underside ↔ floor | above | ~4 |

---

## 6. Mechanism
1. **Drive**: 2WD skid steer on the rear-mid wheels. In the down position the claws' tips rest on the floor and act as the front skids.
2. **Claw action**: the weapon motor turns GD, which turns the tube, swinging both claws together about the tube axis (X). From the down position (tips on the floor ahead, pointing back), rotating the claws **up and back** lifts anything hooked by the tips. Rotating them **down from the raised position** brings the hooks **down onto the top or rear edge of an opponent** in front, then dragging back pulls the opponent toward the body or lifts its front. The slip clutch (spring + plate) limits the torque so a jammed claw does not strip the gearbox.
3. Total claw travel: at least **110°** (AWS71 vs AWS73).

---

## 7. Assembly order (suggested rebuild)
1. Print **BD** with the side rails (or print the rails separately and screw them to the front corners).
2. Fit the **drive motors** in the rear cradles and press on the **wheels**.
3. Fit the **weapon gearmotor** in the front, with its pinion entering GH.
4. Fit the electronics and the **switch** (rear wall, 2 screws).
5. Slide the **tube** through the left rail, the left claw, the left eye stalk, **GD** (in GH), **GP**, the **spring**, the **collar**, the right eye stalk, the right claw and the right rail. Set the clutch preload with the collar's grub screw.
6. Pin/key the claws to the tube. Fix the rail screws S-RL.
7. Screw on the **lid** (2 slotted M3 screws) and the panel screw.
8. Glue the **googly eyes** onto their stalks. Apply the edge strips to the claws (AWS67).

---

## 8. Hidden / uncertain list
- Weapon motor type (gearmotor vs servo) and where it sits.
- Whether GP is a gear or a clutch plate.
- How the claws are keyed to the tube.
- Whether the rails are part of the body or separate.
- All dims ±15 %.

## 9. Coordinate frame (restated)
Origin on the floor at the body footprint centre; +X right, +Y forward, +Z up; mm. Body x ∈ [−36, 36], y ∈ [−28, 28], z ∈ [4, 30]. Tube axis: y = 40, z = 16. Wheels (±41, −14, 16).

## 10. Profiles as math

**10.1 Claw side profile (YZ, in the down position).** Tube axis T = (40, 16).
- Root boss: circle centre T, r = 10.
- Front (convex) edge: arc centre (36, −4), r = 32, from the top of the boss (40, 26) round to the floor at (64, 0)… parametrically (36 + 32 sin θ, −4 + 32 cos θ) for θ ∈ [8°, 82°].
- Tip: the floor point (66, 0) to the tip (58, 2): a short straight chisel pointing rearward.
- Rear (concave) edge: arc centre (64, 20), r = 18, from the tip (58, 2.5) up and back to the boss underside (40, 7)… i.e. (64 − 18 sin θ, 20 − 18 cos θ) for θ ∈ [20°, 90°] meeting the boss.
- Extrude in X over 28 mm at the tip tapering to 14 mm at the root (draft the inner face).

**10.2 Claw front-view inner edge.** Each claw's inner edge: x(z) = ±[18 + 5·sin(π·z/30)] for z ∈ [0, 30] (gap 36 at the floor and top, 46 at mid-height).

**10.3 Claw rotation.** Raised position: rotate the profile about T by θ = −110° (up and back): (y′, z′) = T + R(θ)·((y, z) − T).

**10.4 Body plan.** Rounded rectangle |x| ≤ 36, |y| ≤ 28, r = 5. Lid insert: rounded rectangle |x| ≤ 24, y ∈ [−16, +10], r = 3.

**10.5 Rail (plan).** Rectangles 32 ≤ |x| ≤ 46, y ∈ [22, 44], with a semicircular front end r = 10 about the tube: (y − 40)² + (z − 16)² ≤ 10² for y > 40 in side view.

**10.6 Wheel tread (AWS67).** r(φ) = 15.5 + 0.5·[sin(60φ) > 0], width 9.

## 11. Pixel-based measurements (AWS71 thumbnail 1200 px = native × 0.606; ±8 px)
- Lid: x ≈ 100–910 (810 px) at its front edge; top face y ≈ 50–275.
- Left wheel: x ≈ 25–100, y ≈ 85–370 (285 px tall). Right wheel: x ≈ 810–920, y ≈ 30–275.
- Claws: left x ≈ 75–440, right x ≈ 860–1185. Bottom tips at y ≈ 700 (left) and 690 (right).
- Tube: Ø ≈ 45 px (y ≈ 400–445) at x ≈ 240–930.
- Gear housing (yellow): x ≈ 405–565 (160 px), y ≈ 300–500.
- Googly eyes: ≈ 60–70 px across.
- Lid screws: ≈ 50 px heads.

## 12. Several independent estimates

| Quantity | Method A (lid W = 72 → 11.2 px/mm) | Method B (tube Ø 8 → px/mm) | Method C (googly eye 9 mm) | Reconciled |
|---|---|---|---|---|
| px/mm (front plane) | 810 / 72 = 11.2 | 45 / 8 = 5.6?? | 65 / 9 = 7.2 | see §13 |
| Claw width (each) | 365 / 11.2 = 33 | — | 365 / 7.2 = 51 | **28–30** |
| Overall front width | 1110 / 11.2 = 99 | — | — | **≈ 100** |
| Screw head Ø | 50 / 11.2 = 4.5 | — | 50 / 7.2 = 6.9 | **5.5 (M3)** |
| Wheel Ø | 285 / 11.2 / (vertical foreshortening ≈ 0.8) = 32 | — | — | **32** |

## 13. Consistency check
1. **Tube diameter**: with the lid scale, the tube is 45 / 11.2 = 4 mm, not 8. The tube is closer to the camera than the lid's front edge only slightly, so the lid scale holds. **Reconciled: tube Ø ≈ 5–6 mm** (a 6 mm steel tube is the closest standard size; the 8 mm assumption is dropped).
2. **Googly eyes**: the lid scale gives 65 / 11.2 = 5.8 mm, a small (6 mm) googly eye. **Reconciled: eyes Ø 6 mm**. The C column above (based on 9 mm) is therefore inflated and discarded.
3. **Claw width**: 33 mm (lid scale, claws nearer the camera → inflated ~10 %) → **30 mm**. The two claws (2 × 30) plus the mouth (40) = 100, equal to the overall front width. **Consistent.**
4. **Overall length**: body 56 + tube offset 12 + claw reach 26 = about 96 + 2 = **98 mm** ≤ 101.6. **Consistent.**
5. **Raised claws**: at 110° the claw tips reach z ≈ 16 + 30 = 46 mm, above the 101.6 mm cube only if measured in that pose. In the down pose the robot fits. **Consistent with the rules (the start pose fits).**
6. **Mass**: body + lid 30 g, rails 6 g, claws 2 × 10 g, tube 6 g, gears/clutch 4 g, eyes 1 g, 2 drive N20 + wheels 26 g, weapon motor 12 g, battery 12 g, electronics 8 g, screws 5 g, total ≈ 130 g. **Under 150 g; consistent.**

With the reconciled tube Ø 6: the rail ends' semicircle radius stays 10, and GD stays Ø 18.

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Claws (CL)**
  - Getting under vs contact: in the down position the claw tips sit on the floor ahead of the robot. An opponent driving in meets two hooked points on the floor, **under** its front edge. Lifting the claws then raises the opponent's front, or traps it in the mouth. If the opponent is lower (a wedge), the claws can be swung **down onto its top** and drag it back.
  - Adversarial: the claws are the front armour: a spinner or wedge hitting the front meets the thick curved claws first. The convex front faces deflect hits upward. The two separate claws, rather than a full-width scoop, mean less mass and a mouth that can trap an opponent's wheel or a protruding weapon.
  - Weak points: the tips chip (both AWS71 and AWS67 show chips); hence the **edge strips** (AWS67) to harden the biting edges.
  - Theme: a crab's pincers ("Time For Crab").
- **Rails (RL)**: they carry the tube bearings far forward so the claws can swing without hitting the body. They also shield the wheels' front arcs from frontal attacks.
- **Steel tube**: stiff and strong for its weight, and acts as the common axle so both claws move together.
- **Gear + slip clutch (GD, GP, SPR, CO)**: the gear gives a large reduction for lifting torque. The friction clutch slips when an opponent hits or jams the claws, saving the motor's gearbox. The collar sets the slip torque.
- **Gear housing (GH)**: keeps debris and opponents' parts out of the mesh and holds the pinion's bearing.
- **Body box with wheels outboard**: simple and robust. Wheels taller than the lid allow inverted driving. The open front lets the tube gear connect to the motor inside.
- **Lid with 2 diagonal screws**: two diagonal screws are the minimum that locate a lid without rocking, and speed up access. The empty holes allow the other diagonal to be used.
- **Switch at the rear**: the farthest point from the claws and the opponent's attacks.
- **Googly eyes**: personality, crowd appeal.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Weapon motor | N20 high-ratio (e.g. 298:1–1000:1) along X | 12 × 10 × 30 | (−10, +20, 14) | medium |
| Weapon pinion | small spur gear, 10–12 teeth | Ø 8 | inside GH, above GD | medium |
| Drive motors | 2 × N20 along X | 12 × 10 × 25 | (±22, −14, 16) | medium |
| Motor mounts | printed cradles + lid clamp | — | body floor | medium |
| Battery | 2S LiPo 180–300 mAh | 35 × 20 × 10 | under the lid insert, (0, −4, 14) | medium |
| ESC | dual brushed ESC + third channel for the claw (or a 3-ch board) | 25 × 15 × 4 | front of the body (green PCB seen), (0, +18, 8) | medium |
| Receiver | micro 2.4 GHz | 18 × 12 × 4 | (+20, 0, 20) | low |
| Claw keying | M2 grub screw or cross pin through each claw root into the tube | — | (±30, 40, 16) | low |
| Rail bearings | plain printed bores (no ball bearings) | Ø 6 | in the rail front ends | medium |
| Wiring | battery → rear switch → ESC → 3 motors; red/black pair visible to the claw motor | — | inside | medium |

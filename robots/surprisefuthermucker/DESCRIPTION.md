# Surprisefuthermucker: full rebuild description from the reference photo

Source photo:
- `robots/surprisefuthermucker/reference/surprisefuthermucker.aws63.webp`: AWS 63, 1398 × 1003 px, sharp in the centre with a shallow depth of field (the front and rear edges are slightly soft). The robot sits on the **lid of a clear plastic storage box** (moulded ribs and wavy lines below it are the box, not the robot). There is a dark background at the top left and a **silver bullet-shaped object** at the lower right that is **not part of the robot**. View: **from the robot's left-front-top**, about **45° down**, with the robot's **left side** facing the lower left of the image and its **front** pointing to the lower right.

**Only one photo exists**, so the right side, the rear and the underside are not seen. The description is therefore somewhat shorter than for robots with several photos, and more is marked as a guess. Surprisefuthermucker is a **four-wheel vertical spinner**: an **orange printed H-shaped chassis** with two **wheel pods** under **clear printed lids**, joined by a **central spine**. In a notch at the front centre, a **blue brushless outrunner** carries a **dark grey, laminated, D-shaped ring weapon** spinning about the left–right axis. Everything stated as fact is read from the photo; anything inferred is marked **(guess)**. All mm values are **estimates** (±15–20%), scaled from the wheel (black ribbed tyre on a 3-hole orange hub, taken as **Ø 30 × 10 mm**), from the M2 black socket screws (head Ø ≈ 3.8 mm) and from the AWS 101.6 mm (4 in) cube. Ratios are given against **W = overall width over the wheels ≈ 98 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the weapon), **+Z** = up; mm. **Origin** = the point on the floor (z = 0) under the centre of the chassis footprint (mid-way between the left and right wheel planes, mid-way between the front and rear axles). Side-profile angles are measured from the floor; plan angles from +Y toward +X.
- **Image to robot mapping**: the robot's **left** side faces the lower-left of the image (both left wheels show their faces). The **front** (weapon) points to the lower right. The left-rear wheel is at the image's far left, the left-front at the bottom centre, the right-rear at the top centre-right, and the right-front at the far right.

| ID | Part |
|---|---|
| CH | orange printed chassis (H shape) |
| PD-L / PD-R | left and right wheel pods (parts of CH) |
| LD-L / LD-R | clear printed lids on the pods |
| SN | central spine (raised orange bridge between the pods, three round holes) |
| SN-H | three round lightening holes in the spine |
| SN-T | triangular pocket in the spine, in front of the holes |
| MA | motor mount arm (orange bracket on the left of the weapon notch) |
| MA-S | four black screws in the mount face (stator screws) |
| NT | weapon notch (gap at the front centre) |
| CK-R | right cheek of the notch (orange, chamfered) |
| WM | weapon motor (blue anodised outrunner) |
| WP | weapon: D-shaped laminated ring |
| WP-H | weapon hub / inner curved web |
| SW | red switch/link visible through the left lid |
| BL | blue label/part ("25°C" / "25C") at the left lid edge |
| WH-FL, WH-RL, WH-FR, WH-RR | four wheels (orange 3-hole hubs, black ribbed tyres) |
| S-LD | black socket screws on the lids |
| DM, BAT, RX, ESC | drive motors, battery, receiver, ESCs (hidden, guess) |

---

## 1. Overall description in one paragraph

Surprisefuthermucker is a **small, bright orange, four-wheeled vertical spinner** about **98 mm wide over the wheels, 88 mm long and 30 mm tall**, with the weapon ring reaching about **38 mm** high. Seen from above, the chassis is an **"H"**: two long **side pods**, each about 30 mm wide and 70 mm long, carry a wheel at each end, outboard. A **raised central spine** joins them across the middle and runs forward on the left of a **front-centre notch**. Each pod is covered by a **frosted clear printed lid**, held by **black socket screws**, through which the internals (battery, wires) show as a blur of colour. A **red switch** pokes up through a cut-out in the left lid. In the front notch, a **blue anodised outrunner** is bolted by **four black screws** to the inside of an **orange mount arm**. On its bell hangs the weapon: a **D-shaped ring** about 36 mm across, made of **four stacked dark grey plates** (laminated steel or carbon fibre), spinning about the left–right axis so its outer rim strikes upward at the front. The four wheels have **orange printed hubs with three round holes** and **black finely ribbed tyres** about Ø 30. They stick out a little above and below the body so it can drive either way up.

---

## 2. Part-by-part description

### 2.1 Chassis (CH) and pods (PD-L, PD-R)
- **Overall plan**: an **H** about **78 mm wide (between the wheel inner faces) × 80 mm long**, printed in **opaque bright orange** FDM (PLA/PETG) with fine layer lines.
- **Pods**: two long boxes, one per side, each about **30 mm wide (X) × 80 mm long (Y) × 24 mm tall**, outer walls at x = ±39, inner walls at x = ±9 (the spine and notch sit between them). The pod's outer wall is a plain vertical face with the wheel axle bosses at each end. The **top edges are lipped**: the clear lid sits **inside a 1–2 mm orange rim** (seen around the left lid).
- **Pod ends**: the front and rear end walls are vertical; at the left-front end, the pod wall stops just behind the left-front wheel.
- **Floor**: not seen. Ground clearance is estimated at **3 mm** **(guess)**.

### 2.2 Lids (LD-L, LD-R)
- **Shape**: flat **frosted clear (translucent) printed plates** about **2 mm thick**, about **28 mm wide × 70 mm long**, inset into the pods' top rims, top surface at z ≈ 26.
- **Screws S-LD**: **black socket-head M2 screws** (head Ø 3.8): on the left lid, one at the **rear-outer corner** (about (−36, −30)), one at the **front-inner** corner (about (−12, +28)) and one at the mid-outer edge (about (−36, +5)). On the right lid, two are seen: front-outer (about (+36, +28)) and rear-inner (about (+12, −30)). There are probably 3–4 per lid in total **(guess)**.
- **Cut-out**: the left lid has a **rectangular hole about 10 × 7 mm** near its rear-inner part at about (−22, −12), through which a **red slide switch/DIP-style link** sticks up about 4 mm (red, with two small white marks/ribs on top).
- **Edge damage**: the left lid's front edge near the motor mount is cracked/chipped, and a **blue part with white text "25°C"/"25C"** pokes out at its front-inner corner at about (−12, +30, 22): probably the **label of a LiPo battery (25C rating)** inside the left pod **(guess, medium)**.
- **Visible through the lids**: red and orange blurs (wires/battery), more visible in the right lid (a pale yellow-white rectangle, possibly the receiver).

### 2.3 Central spine (SN), holes (SN-H) and pocket (SN-T)
- **Shape**: a raised orange bridge about **18 mm wide (X) at the rear widening forward**, running from the rear of the chassis forward between the pods, its top at about **z = 30** (about 4 mm above the lids). In plan its outline flares: narrow (18 mm) at the rear centre, widening toward the front into a **V/Y-shape** that joins the left mount arm and the right cheek.
- **Holes SN-H**: **three round holes about Ø 7 mm** in a row along X (across the robot) at about y = −5, at x ≈ −12, 0, +12, about 6 mm deep (blind pockets, orange floors visible). They are lightening holes or **sockets for a removable link/tool** **(guess: lightening)**.
- **Triangular pocket SN-T**: in front of the holes, a **triangular recess** (about 18 mm along each side, 6 mm deep) with its point toward the front, at about (0, +8). It leaves two diagonal ribs running forward to the mount arm and the right cheek: a **truss** that stiffens the weapon supports.

### 2.4 Motor mount arm (MA) and screws (MA-S)
- **Shape**: a thick orange **bracket**, about **10 mm thick (X) × 30 mm long (Y) × 28 mm tall**, forming the **left side of the weapon notch** at x ≈ −14 … −4, from y ≈ +14 to +44. Its top is level with the spine (z ≈ 30) and its **front-top corner is chamfered** at about 45° (a sloping face about 12 mm long). Its outer (left) face is flat and vertical.
- **Screws MA-S**: on the outer face, **four black socket-head M2 screws** in a **square rotated 45°** (a diamond), on a circle about **Ø 9–10 mm**, around a **central hole about Ø 4 mm** (the motor's shaft/bearing clearance), centred at about **(−14, +32, 16)**. These are the **stator screws**: the motor is bolted to the inner face of the arm with its bell spinning in the notch.
- **Material**: orange, the same print as the chassis; probably printed **integral** with it.

### 2.5 Weapon notch (NT) and right cheek (CK-R)
- **Notch**: an open gap at the front centre about **22 mm wide (X)** (x ≈ −4 … +18) and about **32 mm deep (Y)** (from y ≈ +12 to the front at +44), open at the top and front. The weapon ring spins in it.
- **Right cheek CK-R**: the right side of the notch is the left inner wall of the right pod, forward of the spine. It is an orange block with a **chamfered top-front edge** matching the mount arm. No bearing or screw is visible on it, so the weapon is probably **cantilevered from the motor** (no outboard bearing) **(guess, medium)**.

### 2.6 Weapon motor (WM)
- **Look**: a **blue anodised outrunner bell** about **Ø 14–16 mm × 10–12 mm**, with a silver/black base ring where it meets the mount. Axis **along X** at about **(−2, +32, 16)**.
- **Class**: 1306–1407 size **(guess)**.

### 2.7 Weapon (WP) and hub (WP-H)
- **Outline**: a **closed D-shaped ring** lying in the **YZ plane** (perpendicular to the motor axis), about **36 mm tall × 30 mm wide** in the photo, with a fairly **straight/flat side** (upper-left in the photo) and a **rounded side** (lower-right). The ring's band is about **5–6 mm wide** (radially) and its outer corners are softly rounded.
- **Construction**: **four stacked plates** about **1.2–1.5 mm each** (total thickness about **5–6 mm** along X), dark charcoal grey with a satin texture and visible seams between layers, the layers slightly misaligned at the edges. They look like **laser-cut steel or carbon-fibre/G10 laminations**, possibly printed **(guess: hardened steel laminations, low–medium)**. A **small screw/rivet head** sits on the top of the ring (at its 12 o'clock in the photo) holding the layers together.
- **Hub WP-H**: inside the ring, a **curved inner web** (a C-shaped dark grey arc, about 4 mm wide) wraps around the motor bell's end and joins the ring on its lower side. A **black screw** at its centre (seen just right of the bell) fixes it to the bell. So the ring is attached to the motor by a hub on one side of its interior: the rotation axis passes through the ring's interior, **off-centre toward the rounded side** **(seen, medium)**.
- **Balance**: a D-shape with the hub off-centre is a **single-impactor** design: the far (flat) side and the mass on the round side balance about the axis **(guess)**.
- **Swept circle**: radius about **20 mm** about the axis → tip circle Ø 40, top at z ≈ 36, bottom at z ≈ −4 (it would hit the floor; see §13).

### 2.8 Wheels (WH)
- **Size**: about **Ø 30 × 10 mm**.
- **Hubs**: **orange printed**, flat outer face with **three round holes about Ø 6 mm** at 120° on a circle about Ø 14, and a small centre hole/boss. The hub face is slightly recessed from the tyre.
- **Tyres**: **black**, with **fine straight transverse ribs** (about 60 ribs), about 4 mm thick: printed TPU or moulded rubber.
- **Positions**: outboard of the pods at the four corners: centre planes at **x = ±44** (inner faces ±39, outer ±49); front axles at **y = +30**, rear axles at **y = −30**; axle height **z = 15**.
- **Height**: tops at z = 30, level with the spine and about 4 mm above the lids, so the robot can drive inverted (the weapon ring then sticks up over the floor; see §6).

### 2.9 Wires, switch and other visible items
- **SW**: the red switch in the left lid (see §2.2).
- **BL**: the blue "25°C"/"25C" label part at the left lid's front-inner corner (see §2.2), with a white thin wire/edge beside it.
- **Wires**: none clearly visible outside; red/orange shapes inside the lids.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 AWS63 (left-front-top, 45° down)
- **Outline**: a wide, flat **H/bone shape** running diagonally across the image from the lower left to the upper right, with **orange wheel discs at the four corners** (two near ones showing their faces fully, the far two edge-on). The central spine with three dark round holes is in the middle top. The **dark grey D-ring** stands up at the right centre, in front of the orange mount arm with its diamond of four black screws and the blue motor.
- **Colours**: dominant bright orange; frosted white-clear lids; black tyres; dark grey ring; blue motor; a small red switch.

### 3.2 Top view (synthesised)
- Two 30 × 80 rectangles (pods) at x = ±24, joined by the spine (18–40 wide, wider at the front), with the 22 × 32 notch at the front centre holding the ring (5.5 thick, 36 long in Y). Wheels as 10 × 30 rectangles at the four corners outside the pods: overall **98 × 90**.

### 3.3 Front view (synthesised)
- Two pods (24 tall) with wheel discs (30) outboard, the notch in the middle with the ring standing up to z ≈ 36, the mount arm on its left with the motor between.

### 3.4 Left side view (synthesised)
- A 80 × 24 pod rectangle, two Ø 30 wheels at y = ±30 overlapping it, the mount arm's chamfered top at the front, the ring's D outline peeking above and in front.

### 3.5 Rear and right views
- Not photographed; assumed symmetric except the mount arm (left only) **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W (98) | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | H-shaped tub | 78 × 80 × 24 | 0.8 × 0.82 × 0.24 | orange FDM | — | 1 |
| PD | pod box | 30 × 80 × 24 | 0.31 × 0.82 | orange | integral | 2 |
| LD | flat lid | 28 × 70 × 2 | 0.29 × 0.71 | frosted clear FDM | 3–4 × M2 black socket | 2 |
| SN | raised bridge | 18–40 × 50 × 30 | — | orange | integral | 1 |
| SN-H | round pocket | Ø 7 × 6 | 0.07 | — | — | 3 |
| SN-T | triangle pocket | 18 side × 6 deep | — | — | — | 1 |
| MA | bracket | 10 × 30 × 28 | 0.1 × 0.31 × 0.29 | orange | integral | 1 |
| MA-S | socket screw | M2, head Ø 3.8 | — | black | into the stator | 4 |
| NT | notch | 22 × 32 | 0.22 × 0.33 | — | — | 1 |
| WM | outrunner | Ø 15 × 11 | 0.15 | blue anodised | 4 × M2 | 1 |
| WP | D-ring | 36 × 30 × 5.5 (4 layers) | 0.37 × 0.31 | dark grey steel/CF laminate | hub screw + rivet | 1 |
| WP-H | inner web | 4 wide C-arc | — | dark grey | screw to the bell | 1 |
| WH | wheel | Ø 30 × 10 | 0.31 × 0.1 | orange hub, black ribbed tyre | motor shaft | 4 |
| SW | slide switch | 10 × 7 × 4 visible | — | red | in the left lid | 1 |
| BL | label/part | 10 × 5 | — | blue, "25°C" | inside (guess battery) | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD ↔ PD rims | inset, screwed | 0 |
| SN ↔ PD inner walls | integral | 0 |
| MA ↔ SN / CH | integral | 0 |
| WM stator ↔ MA inner face | bolted (4 × M2) | 0 |
| WM bell ↔ MA inner face | rotating clearance | 0.5–1 |
| WP-H ↔ WM bell | screwed | 0 |
| WP left face ↔ WM bell end / MA | clearance | 2–3 |
| WP right face ↔ CK-R | clearance | 3–5 |
| WP swept circle ↔ notch floor/back wall (y +12) | clearance | 2–4 |
| WP swept circle ↔ floor | clearance | 1–3 (requires axis z ≥ 22; see §13) |
| WH inner face ↔ PD outer wall | near | 1–2 |
| WH-F ↔ WH-R tyres | fore-aft gap | 30 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ LD top | wheel above | +4 |
| CH floor ↔ ground | clearance | 3 |
| SW ↔ LD cut-out | through | 1 |

---

## 6. Mechanism

1. **Drive**: four-wheel skid steer. Each wheel probably has its own N20 gearmotor in the pods, two per pod **(guess, medium)**; two motors with one wheel each and two idlers is also possible (low).
2. **Weapon**: a direct-drive vertical spinner. The outrunner, bolted to the mount arm, spins the laminated D-ring about the X axis. The ring rises at the front (if it spins "forward", toward +Y at the top) or bites down at the front (if it spins backward). Usually the front of a vertical spinner moves **up**, launching opponents **(guess)**. With a radius of about 20 mm and an outrunner of ~2000 kV on 2S (≈ 15,000 rpm), the tip speed is about 30 m/s **(guess)**.
3. **Invertible**: wheels above and below the body. Inverted, the ring would still sit in the notch; its direction relative to the floor reverses, so the driver would reverse the weapon spin **(guess)**.

---

## 7. Assembly order (suggested rebuild)

1. Print the chassis CH (pods, spine, mount arm, right cheek) in orange, and the two lids in clear PETG.
2. Fit four drive gearmotors in the pods, shafts out through the outer walls; press on the wheels.
3. Bolt the weapon motor to the inside of the mount arm with 4 × M2 from the outside.
4. Bolt the weapon ring's hub to the bell (central screw), checking the ring clears the notch, the floor and the cheek.
5. Fit the battery (left pod), receiver and ESCs (right pod) and the weapon ESC; route the wires under the spine.
6. Fit the switch so it pokes through the left lid; screw both lids on.

---

## 8. Hidden / uncertain list
- **Everything on the right side, the rear and the underside** (one photo only).
- Weapon material and exact D-ring geometry; the axis height; whether there is an outboard bearing in the right cheek.
- Motor count; battery position.
- All mm ±15–20% (anchored on a Ø 30 wheel).

---

## 9. Coordinate frame (restated)
- Origin on the floor under the chassis footprint centre; +X right, +Y forward, +Z up; mm.
- Chassis x ∈ [−39, +39], y ∈ [−40, +44] (the mount arm and cheek reach +44), z ∈ [3, 30]. Lids z 24–26. Wheels: centre planes x = ±44, axles y = ±30, z = 15, Ø 30. Notch x ∈ [−4, +18], y ∈ [+12, +44]. Weapon axis along X through (y +30, z 22) after §13.1; the ring's mid-plane is at x ≈ +7.
- Overall bounding box: **98 × 90 × 42** (fits the cube).

## 10. Profiles as math (for rebuilding curves)

**10.1 Chassis plan (XY, H shape).** Union of:
- left pod: x ∈ [−39, −9], y ∈ [−40, +40];
- right pod: x ∈ [+9, +39], y ∈ [−40, +44];
- spine: the region between the pods, x ∈ [−9, +9], for y ∈ [−40, +12], widening at y = +12 to join the mount arm (x −14) and the cheek (x +18);
- mount arm: x ∈ [−14, −4], y ∈ [+12, +44];
- notch (removed): x ∈ [−4, +18], y ∈ [+12, +44] (the right pod's inner wall moves in to x = +18 at the front, forming the cheek).

**10.2 Mount arm side profile (YZ, x ∈ [−14, −4]).** Polygon (12, 3), (44, 3), (44, 18), (32, 30), (12, 30): a rectangle with a 45° chamfer (12 × 12) at the top front.

**10.3 Spine top.** z = 30 for the spine region; the holes are vertical cylinders centred at (−12, −5), (0, −5), (+12, −5), r = 3.5, depth 6. The triangle pocket has vertices (−9, 0), (+9, 0), (0, +16), depth 6.

**10.4 D-ring (YZ plane, centred on the motor axis A = (y 30, z 22)).** Outer boundary in polar form about A, using u = angle from +Y:
- rounded side (u from −110° to +110°, the front/lower part): r_out(u) = 20;
- flat side (|u| > 110°): the chord y = 30 − 20 cos 70° ≈ 30 − 6.8 = 23.2 joining the arc ends at z = 22 ± 18.8.
Inner boundary: the same shape offset inward by 5.5 mm. Hub web: an arc of radius 9 about A, from u = 150° to 330°, 4 mm wide, joining the ring at u ≈ −30°.
(The photo shows the flat side toward the upper left, i.e. at that instant u ≈ 135°.)

**10.5 Wheels.** (y ∓ 30)² + (z − 15)² = 15². Hub holes: three Ø 6 at radius 7, 120° apart.

## 11. Pixel-based measurements (independent check)

All on the 1398 × 1003 photo. The camera is close and at about 45°, so near objects (the left wheels) are larger than far ones by up to about 1.6×.
- **Left-front wheel** (nearest): face ellipse ≈ **170 px wide × 270 px tall**, its tyre width ≈ **55 px**. Taking the 270 px height as Ø 30 → **9 px/mm** at that depth. Tyre width 55/9 ≈ **6 mm** (seen obliquely) → 10 mm real ✓.
- **Left-rear wheel**: ≈ **190 × 250 px** → similar scale, 8.3 px/mm.
- **Wheelbase (left)**: centres at (120, 560) and (430, 830) ≈ **410 px** apart. The direction is foreshortened at about 45° → true ≈ 410/8.6/0.8 ≈ **60 mm** ✓ (axles at ±30).
- **Track**: left-front wheel centre (430, 830) to right-front (1270, 420) ≈ **935 px**; at the mid-depth scale (≈ 7 px/mm, farther away) and foreshortening ≈ 0.85 → about **88–100 mm** between wheel centres. Take 88 (centre planes at ±44), which keeps the robot inside the cube.
- **Mount arm screw circle**: diamond ≈ **75 px** across at ≈ 7.5 px/mm → **10 mm** ✓.
- **D-ring height** ≈ **280 px** (y 320 → 600 in the full image) at ≈ 7 px/mm → **40 mm** (partly the ring's slant toward the camera) → **36**.
- **Motor bell** ≈ **95 px** long (along its axis, obliquely) and **75 px** across → **11 × 14–16 mm** ✓.
- **Lid screw head** ≈ **30 px** → **3.8–4 mm** ✓ (M2 socket).

## 12. Several independent estimates of key sizes

| Quantity | Method A (rules / parts) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width | ≤ 101.6 | 1.0 W | track 88 + wheel width 10 = 98 | **98** |
| Overall length | ≤ 101.6 | 0.92 W | wheelbase 60 + 30 = 90 | **90** |
| Pod width | — | 0.31 W | left lid ≈ 260 px across at 8.5 px/mm → 30 | **30** |
| Body height | wheel Ø − 6 | 0.24 W | pod wall ≈ 200 px at 8.5 → 23 | **24 (lids 26)** |
| Wheel Ø | common 30 printed | 0.31 W | anchor | **30** |
| Ring size | fits the 22-wide notch, ≤ 2 × axis height | 0.37 W | 36–40 | **36 × 30** |
| Motor | 1306–1407 | 0.15 W | 11 × 15 | **Ø 15 × 11** |
| Spine holes | — | 0.07 W | ≈ 60 px → 7 | **Ø 7** |

## 13. Consistency check: conflicts and reconciliation
1. **Weapon vs floor**: the photo shows the motor axis at roughly **mid-height of the mount arm** (z ≈ 16). A ring of radius 20 about z = 16 would reach z = −4, below the floor. Either the ring's swept radius is smaller (the D-ring's hub is off-centre, so the far side reaches farther than the near side, but it is the **maximum** radius that matters), or the axis is higher. Reading the photo again, the screw diamond's centre is about **55%** of the way up the arm (arm 28 tall from z 3 → centre at z ≈ 18), and the ring's lowest point seen is about level with the pod's bottom edge. **Reconciled: axis at z = 22, maximum ring radius 20 → lowest point z = 2**, clearing the floor by about 2 mm. (The mount-arm screw centre is then at z = 22; adjust §2.4.)
2. **Notch width vs ring thickness**: notch 22 mm, ring 5.5 mm plus motor bell 11 mm plus clearances 2 + 3 = 21.5 ✓.
3. **Overall width**: pods 78 + 2 × (1.5 gap + 10 wheel) = 101 → just inside the cube. Use **98** by narrowing the pods to 76 (x ±38).
4. **Spec says vertical_spinner**: ✓.
5. **Lid colour**: the lids look white/frosted, which could be white PLA; the internal colours showing through mean **clear/translucent PETG** ✓.

---

## 14. Why the designer did it (per part, from several angles)

Common lens: **adversarial**. For each part: what can attack it (spinners, wedges, lifters, flippers, wall slams, inversion), how it survives, and how it helps win. Then construction reasons.

- **Laminated D-ring weapon**
  - Fight: a single-impactor ring gives a **big bite**: the weapon reaches far and hits with most of its mass on one side, transferring more energy per hit than a symmetric disc of the same weight. A closed ring is stiff and has no thin arms to snap. Laminating several thin plates lets the builder cut a thick weapon from thin sheet; if one layer cracks, the others hold.
  - Weak points: cantilevered on the motor bearings, so big hits load the motor; the ring is narrow (5.5 mm) and can be bent sideways.
  - Construction: laser/waterjet-cut plates stacked and riveted (screw at the top).
- **Blue outrunner bolted to a printed arm**
  - Fight: direct drive has no belt to slip or break; the arm and the right cheek shield the motor's sides.
  - Weak points: the printed arm is the only support; a hard hit can snap it at its root (the spine's triangle truss reinforces exactly this joint).
  - Construction: 4 screws and done; easy to swap motors.
- **H-shaped chassis with a front notch**
  - Fight: the weapon sits **inside** the body footprint, protected on both sides by the pods and wheels; the front is formed by the ring plus the pod fronts, so an opponent approaching head-on meets the ring first.
  - Weak points: the notch is open at the top and front: a wedge can push into it and stop the ring; an overhead weapon can hit the ring.
  - Construction: one print; the spine's holes and pocket save weight while the remaining ribs make a truss.
- **Pods with clear lids**
  - Fight: the pods hold the heavy parts (battery, motors) low and outboard (a stable robot that resists gyroscopic tipping from the vertical spinner).
  - Construction: clear lids let the builder see the electronics and LEDs without opening; four screws for battery access.
- **Four outboard wheels, tops above the lids**
  - Fight: four-wheel drive gives traction and stability against the weapon's gyroscopic forces when turning. Wheels above the body make it **invertible**, important because a vertical spinner's recoil often flips its own robot.
  - Weak points: exposed outer faces can be hit by horizontal spinners.
- **Red switch through the lid**
  - Rules: an easily reached power switch/link; recessed below the wheels' height so opponents do not knock it.
- **Bright orange**
  - Visibility and identity; makes the robot easy to follow on camera.
- **Name**
  - A joke name; no design meaning.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors along X, two per pod | 12 × 10 × 25 | (±27, ±30, 15) | medium |
| Battery | 2S 7.4 V LiPo 300–450 mAh, 25C (blue label seen) | 50 × 22 × 10 | left pod (−24, 0, 12) | medium |
| Receiver + drive ESC | combined dual-ESC/receiver board | 25 × 20 × 5 | right pod (+24, −10, 14) | medium |
| Weapon ESC | 12–20 A brushless ESC | 25 × 12 × 5 | right pod (+24, +15, 12) | medium |
| Switch | red slide switch or link | 10 × 7 × 8 | (−22, −12, 22) | high (seen) |
| Wiring | weapon leads from the right pod under the spine to the motor; battery to the switch | — | under SN | medium |
| Pod floors | integral 1.5 mm | — | z 3–4.5 | medium |
| Outboard bearing | none (cantilevered weapon) | — | — | medium |
| Ring rivet/bolts | M2 bolt through the 4 layers at the top (seen) plus 1–2 hidden | — | on the ring | medium |

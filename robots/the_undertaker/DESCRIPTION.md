# The Undertaker: full rebuild description from reference photos

Source photos:
- `robots/the_undertaker/reference/the_undertaker.aws67.webp` (1776 × 1540 px, the best photo, cut out onto white). AWS 67. Seen from the **front, about 50–55° down**, front toward the bottom of the image. It shows the top deck with **"The UNDERTAKER"** lettering, the **"Rest in pieces"** lid, both **teal-green wheels**, both **long black side plates**, the **4-screw motor boss with its bearing and shaft end**, the **curved black nose guard strip** with 2 screws, and the **flat steel ring blade** underneath the nose.
- `robots/the_undertaker/reference/the_undertaker.aws65.webp` (512 × 469 px, pit photo on wood). AWS 65. An earlier **grey** version seen from the front-left, about 40° down. Its front is a **rounded D-shape** following the blade, with green-filled "REST IN PIECES" on the lid, white "UNDERTAKER" arched along the front, and a small green logo. The blade has a different spoke layout (see §16).
- `robots/the_undertaker/reference/the_undertaker.aws66.webp` (428 × 356 px, pit photo on a yellow table). AWS 66. The black version seen from the front-right, about 35° down. It shows **"The Undertaker"** in white script, **4 raised screw bosses** on the front, the side plates' **down-pointing front legs**, and the ring under the nose.

Everything stated as fact is read from these photos. Inferences are marked **(guess)**. Dimensions are **estimates**. Scale anchors: AWS 150 g / 101.6 mm cube; the **flanged ball bearing** at the shaft (typical 3 × 8 mm motor bearing, flange Ø ≈ 9 mm); the wheel (Ø ≈ 28 mm). Reference width **W = outer width across the side plates ≈ 98 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) **directly under the weapon shaft axis** (the centre of the 4-screw boss).
- **+X** = robot's right, **+Y** = forward (toward the nose), **+Z** = up; mm.
- Envelope: x ∈ [−49, +49], y ∈ [−64, +36] (blade front at y ≈ +36), z ∈ [0, 30].

| ID | Part |
|---|---|
| CH | black printed chassis / body |
| DK | top deck (flat rear-centre and front plate with lettering) |
| NS | nose (front faceted shroud around the weapon motor) |
| MB | motor boss: raised round pad with 4 screws |
| S-MB | 4 black countersunk socket screws on MB |
| BRG | flanged bearing + shaft end at the boss centre |
| WM | weapon motor (brushless outrunner, hidden, guess) |
| BL | flat steel ring blade (the weapon) |
| BL-T | the blade's single hooked tooth |
| BL-S | the blade's diametral spoke bar |
| BL-H | the blade hub (hidden under the nose) |
| NG | curved black nose guard strip (metal) |
| S-NG | 2 screws holding NG |
| LD | "Rest in pieces" raised lid (rear-centre) |
| S-LD | lid screws (4 corners + 1 front tab) |
| SW | power switch (white marking right of the lid) |
| TXT | lettering ("The UNDERTAKER", "Rest in pieces") |
| SP-L / SP-R | long black side plates outboard of the wheels |
| SPL | side plate front legs (down-pointing tips) |
| SPS | side-plate-to-chassis supports (front plate ends + rear posts) |
| WH-L / WH-R | two teal-green drive wheels |
| M-L / M-R | drive gearmotors (hidden, guess N20) |
| MM | plastic drive motor mounts (hidden) |
| ESC-W, ESC-D, RX, BAT | electronics (hidden) |

---

## 1. Overall description in one paragraph

The Undertaker is a **two-wheel horizontal ring spinner** (an undercutter-style "shell ring" on a low disc). Its body is a **black printed block**, about **84 mm wide and 70 mm long**, with a flat rear deck between the two wheels. At the front it narrows into a **faceted pointed nose** that houses the weapon motor. On top of the nose sits a **round raised boss with four countersunk screws** around a **ball bearing with the shaft end** showing. Under the nose, close to the floor, spins a **thin flat steel ring**, about **72 mm across**, with a **single straight spoke across its diameter** and **one hooked tooth** cut into its rim. The ring sticks out about 28 mm in front of the nose and well out to the sides. A **curved black metal strip** wraps the very tip of the nose just above the ring, as a bumper. At the rear corners, two **teal TPU wheels with ribbed tread** sit in notches, and outside each wheel a **long thin black side plate** runs from behind the wheel forward along the body and ends in a **down-pointing leg** that touches the floor beside the blade. The deck carries **"The UNDERTAKER"** in white and a raised **"Rest in pieces"** lid over the electronics, with the power **switch** to its right.

---

## 2. Part-by-part description

### 2.1 Chassis (CH) and deck (DK)
- **Plan outline** (AWS67): a **wide rear section plus a tapered nose**.
  - The **front plate section** (with "UNDERTAKER"): a full-width band, **84 mm wide (x ±42) × 20 mm long (Y)**, in front of the wheels, y ∈ [−34, −14].
  - The **rear centre section** (between the wheels): **50 mm wide (x ±25) × 30 mm long**, y ∈ [−64, −34]. It carries the lid. The rear corners outside it are the **wheel notches**.
  - The **nose**: from the front plate the outline tapers with two straight sides at about **±55° to the Y axis** (front facets) toward a **blunt point** at y ≈ +6, cut off by the nose guard arc (r ≈ 14 about the shaft).
- **Height**: the deck top is at **z ≈ 24**. The body underside is at about **z ≈ 8** behind the blade (the blade passes beneath the nose) **(guess, from the ring being visible under the nose edge in AWS67 and AWS66)**.
- **Front facets**: in AWS67 the nose top is not flat. From the lettering line forward, the top surface slopes down at about **20–25°** toward the nose tip, and the two side facets slope down and outward. The boss MB sits on this sloped area, on a **flat round pad set into it**. The lower front edge of the facets is about z ≈ 10 at the tip.
- **Surface**: strong **diagonal 45° top-layer lines** on the deck and facets, **horizontal layer lines** on the vertical faces. Colour: matt black (AWS66/67), grey (AWS65).
- **Small screw holes**: several **Ø 1.5–2 mm** holes are visible on the front plate's left and right ends (2 each side, near the side plates) and at the nose (one near the boss). They are the screw holes for the side plates and the nose guard, or empty pilot holes **(guess)**.

### 2.2 Motor boss (MB), screws (S-MB), bearing (BRG)
- **MB**: a **round raised/recessed pad**, **Ø ≈ 26 mm**, on the nose, centred on the shaft axis (x = 0, y = 0). Its top is roughly horizontal at **z ≈ 20**. The pad edge is a clear circular step against the sloping facets (the pad is cut flat into the slope: at the rear it is recessed about 2 mm below the deck, at the front it stands about 2 mm above the facet).
- **S-MB**: **4 black countersunk socket (hex) head screws**, head Ø ≈ **4 mm** (M2), in a **square pattern** about **12 × 12 mm** (on a **circle of Ø ≈ 16–17 mm**), at 45° positions round the shaft. These fix the weapon motor's mount face to the underside of the pad **(guess)**.
- **BRG**: in the centre, a **flanged ball bearing** (outer Ø ≈ 8–9 mm, gold/brass-coloured seal) with the **silver shaft end (Ø ≈ 3 mm)** protruding about **1–2 mm** above it, with a **small circlip/E-clip** visible. This is either the motor's own top bearing (outrunner base) or an extra bearing supporting the weapon shaft **(guess: the motor's base bearing, the motor hanging upside down below the pad)**.

### 2.3 Weapon motor (WM), hidden
- **Guess**: a **small brushless outrunner**, about **Ø 22–28 × 12–16 mm** (1806 / 2204 class), mounted **upside down**: its stator base is screwed to the underside of MB by the 4 screws, and its **bell spins below**, inside the nose shroud, with the blade fixed to the bottom of the bell or to the shaft below it.
- **Confidence**: medium (the 4-screw square + central bearing + shaft end is the standard look of an outrunner's base).

### 2.4 Blade (BL), tooth (BL-T), spoke (BL-S), hub (BL-H)
- **Shape**: a **flat ring cut from steel sheet**, **outer Ø ≈ 72 mm**, **ring width ≈ 9 mm** (inner Ø ≈ 54 mm), **thickness ≈ 2–2.5 mm**. The surface is **bright, slightly scratched/ground steel** with darker scuffed edges.
- **Spoke BL-S**: a **straight bar about 7 mm wide** across the ring's diameter, through the hub. In AWS67 it runs from about the **10 o'clock** position on the ring (left, under the nose guard) to the **3 o'clock** position (right), passing under the nose. The hub is the spoke's middle.
- **Tooth BL-T**: at about the **8 o'clock** position (front-left in AWS67), the ring's rim is **cut with a notch**, forming a **hooked tooth**: the outer edge runs at full radius, then **steps outward by about 3 mm into a sharp point**, then a **concave cut-back** runs inward (radius about 10 mm) to the ring's inner edge. Behind the point the ring's rim is slightly reduced. So there is **one impactor** (a single-tooth ring): the **point leads in the direction of spin**. From the hook's shape (point facing up-left in the image, cut-back below it), the spin is **clockwise seen from above** **(guess)**.
- **Balance**: a single tooth plus a notch is self-balancing to first order (material removed opposite the point is about equal). There are no visible balancing holes.
- **Height**: the ring's top is at about **z ≈ 6**, its bottom at **z ≈ 3.5** (so about 3–4 mm above the floor) **(guess)**.
- **Hub**: hidden under the nose: presumably a **bolt pattern or a press fit onto the bell** (2–3 small screws).

### 2.5 Nose guard (NG) and screws (S-NG)
- **Shape**: a **curved strip of black metal (sheet steel or aluminium, painted/anodised black, edge shows bright metal)**, about **10 mm tall × 1 mm thick**, bent into an **arc of radius ≈ 14 mm about the shaft axis**, spanning about **110°** (from about −55° to +55° about +Y). Its ends are **flat tabs** that lie against the nose's front facets.
- **Fixing**: **2 small black pan or countersunk screws** (head Ø ≈ 3.5 mm), one through each end tab, into the facets.
- **Position**: the strip's bottom edge is about **1–2 mm above the blade**, its top edge flush with the nose top.
- **Visible damage**: the strip's top edge shows **bright scuffs** where it has been hit.

### 2.6 Lid (LD), screws (S-LD), lettering (TXT)
- **LD**: a **raised rectangular panel**, about **44 × 24 mm**, standing about **3 mm above the deck** (z ≈ 27), centred on the rear section, y ∈ [−62, −38]. It has a **front tab** (a small semicircular extension about 10 mm wide at the front centre) carrying one screw.
- **S-LD**: **5 small black screws** (M2), one at each corner and one in the front tab.
- **Text "Rest in pieces"** (with quotation marks): **engraved/embossed script** in two lines, about **6 mm tall**, filled with **silver/white paint** (AWS67). AWS65: **green capital letters "REST IN PIECES"** in three lines.
- **"The UNDERTAKER"**: on the front plate. "The" is small, embossed in black (AWS67); "UNDERTAKER" is **bold capitals about 8 mm tall, filled white**, spanning about **74 mm**. AWS66: white script "The Undertaker" across the nose. AWS65: white capitals arched along the curved front edge.

### 2.7 Switch (SW)
- To the right of the lid, at about (x +24, y −50), a **small rectangular slot** (about 8 × 4 mm) with a **white marking** (white paint or a white slider). It is the **power switch** (a slide switch or a removable link pushed through the deck) **(medium)**.

### 2.8 Side plates (SP-L, SP-R) and legs (SPL)
- **Shape**: each is a **flat vertical plate**, about **3 mm thick (X)**, running **from behind the wheel to beyond the front plate**, about **84 mm long (Y)**, y ∈ [−66, +18].
  - The **rear part** (beside the wheel) is about **28 mm tall** (z 0–28), wheel-height, with a rounded rear-top corner (r ≈ 6 mm).
  - Toward the front the plate's top edge drops, and the **front end turns down into a leg**: a **tapered tip** pointing **forward and down**, touching the floor at about **y ≈ +18** (beside the blade, about 10 mm outboard of the blade's rim). In AWS66 and AWS65 these legs are clearly seen as **two down-pointing prongs** at the front corners.
- **Position**: their inner faces are at x ≈ ±46, so they stand **about 1–2 mm outboard of the wheels' outer faces**.
- **Colour**: black (AWS66/67), grey (AWS65).
- **Function**: wheel guards plus front **skids/forks** that hold the front of the robot up at the right height so the blade clears the floor, and get under opponents beside the blade.

### 2.9 Side-plate-to-chassis supports (SPS)
- The plates are attached at the **ends of the front plate section** (the "UNDERTAKER" band runs out to x ±42 and meets the plates' inner faces): **two screws per side** through the plate into the front plate's end face (the small holes seen at the front plate's ends) **(guess)**.
- At the rear, a **post or rib** behind each wheel (y ≈ −62) ties the plate to the rear centre section **(guess)**: without it the plate would be a 60 mm cantilever. In AWS67 a dark block is visible behind each wheel at the rear corner, about **6 mm wide**, the likely rear spacer.

### 2.10 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 28 mm × 10 mm**, **teal/turquoise-green TPU tyres** with about **36 transverse ribs** (fine, about 1 mm pitch-depth) on black hubs.
- **Position**: centres at **x = ±38, y = −46, z = 14**. Inner faces about 1–2 mm from the rear centre section's side walls, outer faces about 1–2 mm from the side plates.
- **Height**: tops at **z ≈ 28**, about **4 mm above the deck** and about level with the lid. Bottoms on the floor. So the robot is **invertible** at the rear. When inverted, the blade is then on top and nearer the arena "floor" level of the opponent? No: inverted, the blade is about 24 mm above the floor and would hit taller robots. Whether it is meant to fight inverted is unclear **(guess: it can drive inverted but the weapon is less useful)**.

### 2.11 Drive motors (M-L, M-R) and plastic motor mounts (MM), hidden
- **Guess**: **2 × N20 gearmotors** lying along X under the rear deck, shafts out to the wheels at z ≈ 14, held in **printed cradles** clamped by the lid (the lid is directly between the wheels) **(medium)**.

### 2.12 Electronics and wires (hidden)
- **Guess**: a **2S LiPo** (about 300 mAh), a **brushless ESC** for the weapon (about 12 A, about 25 × 12 mm), a **dual brushed ESC** for the drive and a **receiver**, all in the body between the nose and the rear deck. The weapon motor's 3 phase wires run back from the nose cavity to the ESC under the front plate. No wires are visible externally.

---

## 3. Per-view descriptions

### 3.1 Top view (plan)
- A wide band (84 × 20) with "UNDERTAKER" across it. Behind it a narrower raised-lid block (50 × 30) with the wheels in the rear corner notches. Outside the wheels the thin side plates run the whole length and stick out ahead as two prongs. In front, the nose tapers to a point with a round 4-screw boss and a bearing in it, and a curved strip at the tip. Under and around the nose, a **ring of 72 mm Ø** with one spoke and one hooked tooth sticks out: about 28 mm ahead of the nose, and to x ≈ ±36 at its widest (inside the side plates).
- Overall length ≈ **102 mm** (rear of side plates to blade front); overall width ≈ **98 mm** (side plates).

### 3.2 Front view
- At the bottom, the **thin steel ring** edge-on as a bright horizontal line at z ≈ 3–6 across about 72 mm. Above it, the nose guard strip (an arc seen as a band) and the faceted nose rising to the deck. At each side, the **side plate legs** come down to the floor outside the ring. The wheel tops show above the deck at the rear corners.

### 3.3 Side view (left)
- The side plate covers most of the side: a long low plate (84 × 28 at the rear, tapering forward to a floor-touching tip). The wheel is hidden behind the plate except its top 1–2 mm. The ring sticks out ahead at floor level, about 18 mm beyond the leg tip.

### 3.4 Rear view (not photographed; inferred)
- The rear centre block (50 wide, z up to 27 with the lid) and the two wheels either side, with the side plates' rounded rear corners outboard.

### 3.5 Underside (not photographed; inferred)
- A flat floor under the rear section; a hollow shroud under the nose open at the bottom, through which the motor bell and blade hub are visible. Ground clearance about 2 mm at the rear and 8 mm under the nose.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 98 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | tapered block | 84 × 70 × 16–24 | 0.86 × 0.71 | black (grey AWS65) FDM | — | 1 |
| MB | round pad | Ø 26 | 0.27 | black | integral | 1 |
| S-MB | CSK socket | M2, head Ø 4, on PCD 16.5 | — | black steel | into WM | 4 |
| BRG | flanged bearing + shaft | Ø 9 flange / Ø 3 shaft | — | steel/brass | in WM | 1 |
| WM | outrunner | Ø 25 × 14 | — | — | 4 × M2 | 1 (hidden) |
| BL | ring blade | Ø 72 OD / 54 ID × 2.5 | 0.73 | steel | to WM bell | 1 |
| BL-S | spoke | 7 wide, across Ø | — | steel | integral | 1 |
| BL-T | hooked tooth | 3 mm proud, 10 mm cut-back | — | steel | integral | 1 |
| NG | curved strip | r 14, 110°, 10 × 1 | — | black metal | 2 screws | 1 |
| LD | raised lid | 44 × 24 × 3 | 0.45 × 0.24 | black + silver text | 5 × M2 | 1 |
| SW | slot switch | 8 × 4 | — | white | — | 1 |
| SP | side plate | 84 × 28 × 3 | 0.86 × 0.29 | black | 2 screws + rear spacer | 2 |
| WH | ribbed wheel | Ø 28 × 10 | 0.29 × 0.10 | teal TPU / black hub | motor shaft | 2 |
| M | N20 gearmotor | 12 × 10 × 25 | — | — | cradle | 2 (hidden) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WM ↔ MB underside | screwed (4) | 0 |
| BRG ↔ MB | concentric, through the pad | 0 |
| BL ↔ WM bell / shaft | bolted (hidden) | 0 |
| BL top ↔ NS bottom edge | below the nose | 2–4 |
| BL bottom ↔ floor | above | 3–4 |
| BL rim ↔ SPL legs | inside the legs | ~10 |
| BL rim (rear part) ↔ wheels | ahead of the wheels | ~4 (BL rear edge y −36 vs wheel front y −32: overlap in Y but the ring passes under the front plate, not reaching the wheels in X: ring x ≤ 36 at y −30 → **clear by about 8**) |
| NG ↔ NS facets | screwed (2) | 0 |
| NG bottom ↔ BL | above | 1–2 |
| LD ↔ deck | screwed (5) | 0 |
| SP inner face ↔ WH outer face | side by side | 1–2 |
| SP ↔ front plate ends | screwed | 0 |
| SP rear ↔ rear spacer | joined | 0 |
| SPL tip ↔ floor | touching | 0 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ deck | wheel proud | +4 |
| WH inner face ↔ rear centre walls | near | 1–2 |
| CH rear floor ↔ floor | above | ~2 |

---

## 6. Mechanism
1. **Weapon**: a brushless outrunner directly drives the steel ring. A ring puts most of the mass at the rim, giving high moment of inertia for its weight. A Ø 72 ring of 2.5 mm steel (OD 72, ID 54) has mass ≈ 7.85 g/cm³ × π/4·(7.2² − 5.4²)·0.25 ≈ 35 g minus the notch plus the spoke (≈ 5 g) ≈ **38 g**. Its tip speed at 15 000 rpm is about 57 m/s.
2. **Drive**: 2WD rear-wheel skid steer. The front of the robot rides on the two side plate legs (skids), which set the blade height.
3. **Single tooth**: one impactor gives maximum "bite" (the opponent's edge can travel further into the ring between hits).

---

## 7. Assembly order (suggested rebuild)
1. Print **CH** (rear section with wheel notches, front plate band, faceted nose shroud with the MB pad, lid seat, motor cradles).
2. Screw the **weapon motor** upside down under MB with **4 × M2 countersunk** screws from above.
3. Fit the **drive N20s** in their cradles and press on the **wheels**.
4. Fit the electronics (battery, weapon ESC, drive ESC, receiver) and the **switch**. Route the 3 weapon phase wires back from the nose.
5. Screw on the **lid** (5 screws).
6. Bolt the **ring blade** to the motor bell from below.
7. Screw the **nose guard strip** to the nose tip (2 screws).
8. Screw the **side plates** to the front plate ends and the rear spacers. Check that the leg tips touch the floor and the blade clears the floor by 3–4 mm.
9. Paint the lettering.

---

## 8. Hidden / uncertain list
- Weapon motor type and how the ring attaches to it.
- Underside shape of the nose shroud.
- Drive motor type.
- Side plate fixings.
- Spin direction.
- All dims ±15 %.

## 9. Coordinate frame (restated)
Origin on the floor under the weapon shaft. +X right, +Y forward, +Z up, mm. Weapon axis: the vertical line (0, 0, z). Wheels at (±38, −46, 14). Body rear at y = −64, nose tip y ≈ +8, blade front y = +36.

## 10. Profiles as math

**10.1 Blade (plan, in the blade's own frame, angle φ from +Y, clockwise positive).**
- Outer edge: r_o(φ) = 36 for all φ except the tooth zone.
- Inner edge: r_i = 27.
- Tooth zone (centred at φ_t): for φ ∈ [φ_t − 25°, φ_t]: r_o = 36 + 3·(φ − (φ_t − 25°))/25° (a ramp outward to the point); at φ_t the edge drops along a concave arc (centre at radius 33 at φ_t + 12°, r = 10) back to the inner edge. Use φ_t = 240° (8 o'clock in AWS67).
- Spoke: the strip |x′| ≤ 3.5 along the diameter at φ = 105° / 285° (roughly 10 o'clock to 3 o'clock in AWS67's view), clipped to r ≤ 27.
- Thickness 2.5 mm, z from 3.5 to 6.

**10.2 Body plan outline (XY at deck height).** Polygon: rear centre (±25, −64) to (±25, −34); front plate (±42, −34) to (±42, −14); facets: from (±42, −14) to (±12, +4); nose arc: centre (0, 0), r = 14, from φ = −55° to +55° (front tip at y = +14 … trimmed to the guard's inner radius 13).
(Use y_tip = +13.)

**10.3 Nose facet surface.** The deck top z = 24 for y ≤ −14; facets descend: z(y) = 24 − tan(22°)·(y + 14) for y ∈ [−14, +13] → z ≈ 13 at the tip. The pad MB cut flat at z = 20, circle r = 13 about (0, 0).

**10.4 Side plate (YZ at x = ±47.5).** Outline: (y −66, z 0) → (−66, 22) → arc r 6 to (−60, 28) → (−30, 28) → line falling to (+4, 16) → line to the leg tip (+18, 0) → floor line back to (−20, 0)… the plate's lower edge is cut up between the wheel and the leg: a straight lower edge from (+18, 0) to (−20, 8) then down to (−30, 0) and the floor line to (−66, 0) (clears the floor except at the leg and the rear).

**10.5 Nose guard arc.** Points (14·sin φ, 14·cos φ, z) for φ ∈ [−55°, +55°], z ∈ [7, 17]; end tabs 5 mm long tangent to the facets.

**10.6 Wheel tread.** r(φ) = 13.0 + 1.0·[sin(36φ) > 0], width 10.

## 11. Pixel-based measurements (AWS67 thumbnail 1200 px wide = native × 0.676; ±8 px)
- Side plate outer edges: x ≈ 65 and ≈ 1135 → 1070 px.
- Wheel tread (left): x ≈ 115–205 (90 px wide); vertical extent y ≈ 40–230.
- "UNDERTAKER" lettering: x ≈ 210–1000 (790 px), height ≈ 60 px.
- Lid: x ≈ 350–800 (450 px) × y ≈ 50–200.
- MB pad: x ≈ 480–700 (220 px). Screw spacing ≈ 110 px. Bearing ≈ 60 px.
- Blade: x ≈ 195–970 (775 px). Blade bottom y ≈ 1000; blade top hidden under the nose at y ≈ 560.
- Nose guard: x ≈ 380–810 (430 px).

## 12. Several independent estimates

| Quantity | Method A (W = 98 at side plates) | Method B (bearing 9 mm) | Method C (wheel width 10 mm) | Reconciled |
|---|---|---|---|---|
| px/mm at deck | 1070 / 98 = 10.9 | 60 / 9 = 6.7?? (bearing farther down in a recess and partly hidden) | 90 / 10 = 9.0 (wheel tread at the rear, farther) | **10.9** front, **9** rear |
| Lettering length | 790 / 10.9 = 72 | — | — | **72–74** |
| Blade Ø | 775 / 10.9 = 71; blade is lower but nearer the camera → ±5 | — | — | **72** |
| MB pad Ø | 220 / 10.9 = 20 | 220 / 6.7 = 33 | — | **26** |
| Screw PCD (square side) | 110 / 10.9 = 10 | 110 / 6.7 = 16 | — | **12** side, PCD 17 |
| Wheel Ø | 190 px vertical (foreshortened) / 9 / cos 35° = 26 | — | — | **28** |

## 13. Consistency check
1. **Blade vs cube**: blade Ø 72 + nose overhang: overall length = 64 (rear) + 36 (blade front) = 100 mm ≤ 101.6. **Consistent.** Overall width 98 ≤ 101.6. **Consistent.**
2. **Blade vs side plates**: ring radius 36 < 46 (plate inner face), so the ring spins inside the legs. **Consistent** with AWS67 where the ring's left and right edges sit inside the plates.
3. **Blade vs wheels**: the ring's rear arc at y = −36 lies under the front plate (y −34 to −14); the wheels start at y ≈ −32 (front of tread) but at |x| ≥ 33, where the ring's rear arc is at y = −√(36² − 33²) = −14.4. So the ring is ahead of the wheels by about 18 mm at their x. **Consistent; no clash.**
4. **Mass**: blade 38 g, weapon motor 15 g, ESC 5 g, chassis 35 g, side plates 8 g, 2 N20 + wheels 24 g, battery 15 g, RX/ESC 6 g, screws 4 g, total ≈ 150 g. **At the limit, consistent.**
5. **MB pad size**: the two methods disagree; the bearing method is unreliable (partly hidden). An 1806/2204 outrunner needs a 16–19 mm PCD, which matches the reconciled 17. **Consistent.**

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Ring blade (BL)**
  - Attack: a ring puts the mass at the rim, giving the most stored energy for the weight. A **single tooth** gives the deepest bite: each hit lands a large chunk of energy rather than many small taps. Spinning just above the floor, it hits opponents' **wheels and low edges** and **gets under wedges' sides**.
  - Getting under vs contact: an opponent's wedge that gets under the ring lifts the robot, but the ring then hits the wedge's surface. The ring's low height (3.5 mm) lets it meet most wedges' faces rather than their edges.
  - Weak points: a thin ring can bend if it hits a hard wedge at speed; the spoke carries all the torque.
- **Spoke (BL-S)**: a single straight spoke is the lightest way to connect the ring to the hub, and keeps the inner area open so the ring's mass stays at the rim.
- **Nose shroud + motor boss**: the motor sits inside a printed shroud with only the bell exposed beneath. Mounting from above with 4 screws means the motor can be swapped without taking the robot apart.
- **Nose guard strip (NG)**: the tip of the nose is the part closest to opponents above the ring. A metal strip there stops opponents' wedges or spinners chewing the printed nose and protects the motor. It also stops an opponent's edge from riding up over the ring and hitting the shaft.
- **Side plates and legs (SP, SPL)**
  - Adversarial: they shield the **wheels from the sides**, and the legs give **two extra floor-touching points** at the front corners. That keeps the blade at a fixed height and makes the front corners act as small forks, so an opponent's wedge from the side or the front corners meets a skid, not the ring's underside.
  - When the robot is hit and spins round, the legs keep the ring from digging into the floor.
  - Construction: separate plates are replaceable and can be printed flat (strong in-plane).
- **SPS supports (front screws + rear spacer)**: a two-point fixing keeps the long plates from flexing into the wheels under a side hit.
- **Wheels at the rear, teal TPU**: the rear position keeps them away from the ring and the front of the robot. Ribbed TPU grips well. Wheels slightly taller than the deck allow driving inverted.
- **Lid over the electronics**: raised just enough to clear the battery/ESC, with 5 screws for strength; it sits behind the front plate, out of the line of frontal attack.
- **Switch next to the lid**: accessible from above, protected by the lid's height on one side and the wheel on the other.
- **Lettering**: show/identity ("Rest in pieces" is the robot's catchphrase).

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Weapon motor | 1806/2204 outrunner, 2300 kV, inverted | Ø 25 × 14 | (0, 0, 8–18) | medium |
| Blade hub fixing | blade bolted to the bell with 2–3 M2 screws, or clamped on a shaft collet | — | (0, 0, 4–6) | low |
| Weapon ESC | 12 A brushless ESC | 25 × 12 × 4 | under the front plate, (0, −24, 12) | medium |
| Drive motors | 2 × N20 | 12 × 10 × 25 | (±22, −46, 14) | medium |
| Drive ESC | dual brushed micro ESC | 20 × 12 × 4 | under the lid | low |
| Receiver | micro 2.4 GHz | 18 × 12 × 4 | under the lid | low |
| Battery | 2S LiPo 250–300 mAh | 40 × 20 × 10 | across the rear, under the lid | medium |
| Switch | slide/link switch | 10 × 5 × 5 | (+24, −50, 20) | medium |
| Rear plate spacers | printed posts linking the plates to the rear section | 6 × 6 × 20 | (±44, −62, 10) | low |
| Wiring | battery → switch → both ESCs; weapon ESC → 3 phase wires forward to the nose; drive ESC → 2 motors | — | inside | medium |

---

## 16. Version differences
- **AWS65 (grey)**: the front is a **rounded D-shape** following the ring (the front plate and nose are one curved front). The deck shows **4 small screw holes** around a central hole on top of the front (the motor pattern, no raised pad). Lettering: green "REST IN PIECES", white arched "UNDERTAKER", small green logo. The ring has a **straight spoke** and a **single tooth with a long hooked tail** (the hook is at the front-right in that photo). The side plates have **down-pointing legs** at the front corners.
- **AWS66 (black)**: front faceted like AWS67, but the top of the nose has **4 raised round screw bosses** (domed screw caps) instead of a flat pad, and the lettering is white script "The Undertaker".
- **AWS67 (black)**: the flat pad with 4 countersunk screws and a visible bearing, the nose guard strip, and "The UNDERTAKER" / "Rest in pieces" lettering as described above.

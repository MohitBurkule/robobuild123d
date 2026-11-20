# Vampire: full rebuild description from reference photos

Source photos (all cut out onto white, with masks):
- `robots/vampire/reference/vampire.aws71.webp` (1200 × 725 px in the PNG conversion). AWS 71. Seen from the **front-left, about 35–40° down**. The left side wall with the word **"VAMPIRE"** is at the lower left; the open front with the **carbon-fibre base plate** and the **outrunner motor** is at the lower centre-right; the **asymmetric spinning bar** lies diagonally from upper left (short, wide end) to lower right (long, narrow end with a chewed tip). Both wheels are visible (left wheel just inside the VAMPIRE wall, right wheel at the upper right). The top plate looks **translucent** (a black label and coloured parts show through).
- `robots/vampire/reference/vampire.aws74.webp` (1200 × 750). AWS 74. Seen from the **front-right, about 35° down**. The right side wall and front-right corner facet at the lower right; the bar lies from the lower left (long narrow end, flared and chewed) to the upper right (short wide paddle). Everything metal reflects green (studio surroundings), so the colours are tinted; the motor label reads **"…Todar"** (script, partly hidden). Shows the right wheel and its black motor block with a standoff, a bent **clear tab** of the top plate, a **blue** item behind the motor.
- `robots/vampire/reference/vampire.aws76.webp` (1200 × 579). AWS 76. Seen from the **left side, slightly front, about 15–20° down**. The best **side profile**: the long left side wall with "VAMPIRE", the motor standing on the carbon base with the bar across its top (seen nearly edge-on), the bar's long end reaching far to the right beyond the base plate, the short paddle to the left over the rear, the **stepped edge** of the carbon base.

Everything stated as fact is read from these photos. Inferences are marked **(guess)** with a confidence. Dimensions are **estimates**. Scale anchors: (1) the **weapon motor**: a black **22xx-class outrunner** (bell Ø ≈ 28 mm, can height ≈ 22 mm incl. base) with **five spoke windows** in the bell top and four black **M3 socket cap screws** (head Ø 5.5) in a square on it; (2) the **drive wheels** (fine-ribbed black tyres, Ø ≈ 24 mm, the common N20 wheel); (3) the AWS 150 g / 101.6 mm cube rule (the body fits the cube; the bar is long enough that it must lie across the **cube's face diagonal, 143.7 mm**). Reference **W = body width over the side walls ≈ 96 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the **centre of the body** (the wall polygon's centre, not the motor).
- **+X** = robot's right, **+Y** = forward (the open side with the motor), **+Z** = up; mm. Weapon angle θ measured in the XY plane from +X toward +Y.
- Envelope (body only): x ∈ [−48, +48], y ∈ [−46, +48], z ∈ [0, 26]. With the bar: the bar's tips sweep a circle of radius ≈ 80 about the motor axis (0, +20), z 31–35.

| ID | Part |
|---|---|
| BP | carbon-fibre base plate (bottom) |
| BP-F | stepped/castellated front extension of the base plate |
| WL | folded aluminium wall band (perimeter wall), facets WL-1..WL-7 |
| TXT | "VAMPIRE" lettering on the left wall facet |
| TPL | top plate (clear, frosted polycarbonate, guess) with a front V-notch |
| TAB-L / TAB-R | bent-down tabs of the top plate beside the motor |
| CS | countersunk silver top screws |
| SO | standoffs / posts between base and top (hidden except bottoms) |
| NT | hex nuts on the base at the wall corners / motor-block screws |
| WH-L / WH-R | drive wheels |
| DM-L / DM-R | drive gearmotors in black blocks (motor mounts) |
| MB-L / MB-R | black motor blocks / clamps |
| WM | weapon outrunner motor |
| WMS | weapon motor mount screws (through the base) |
| BAR | asymmetric spinning bar (BAR-S short wide paddle, BAR-L long narrow arm, BAR-T flared tip) |
| BS | 4 × M3 bar screws + centre shaft hole |
| ESC | weapon/drive electronics (blue item seen, guess ESC) |
| BAT, RX, SW, WR | battery, receiver, switch, wires (hidden) |

---

## 1. Overall description in one paragraph

Vampire is a **two-wheel antweight with a top-mounted horizontal bar spinner on an exposed front outrunner**. The body is a flat, low **heptagonal "half-octagon" box about 96 mm wide, 85 mm long and 26 mm tall**: a **2 mm carbon-fibre base plate**, a **perimeter wall** of thin **folded aluminium sheet** (about 22 mm tall) running round the left side, the rear corners, the rear and the right side, ending in **two short angled facets at the front corners**, and a **thin clear/frosted top plate** that covers the rear two-thirds and ends at the front in a **V-shaped notch** around the weapon motor. The front is **open**: the carbon base plate continues forward past the wall with a **stepped edge**, and on it, ahead of the wheel axle, stands a **black 22xx outrunner (Ø 28)** whose bell carries a **long, asymmetric flat steel bar** (≈ 138 mm long, 3 mm thick) bolted on with **four socket screws**. One end of the bar is a **short wide paddle** (≈ 58 mm from the axis, 26 mm wide), the other a **long narrow arm** (≈ 80 mm, 14 mm wide) ending in a **slightly flared, chewed striking tip**. The bar spins **above the top plate and the walls**, sweeping a circle about 160 mm across that overhangs the whole body. Two **N20 gearmotors** in **black blocks** drive two **Ø 24 mm ribbed wheels** just inside the left and right walls. "VAMPIRE" is printed in black block capitals on the left wall.

---

## 2. Part-by-part description

### 2.1 Base plate (BP, BP-F)
- **Material**: **carbon-fibre sheet**, clearly showing a **twill weave** (diagonal zig-zag pattern), matt black, **≈ 2 mm thick** (edges look 2 mm next to the 3 mm bar).
- **Rear and sides**: its outline follows the wall polygon (2.2) exactly; the wall stands on its top face at the edge (or wraps its edge).
- **Front (BP-F)**: the plate continues **forward past the wall's front-corner facets** by about 10–14 mm, with a **stepped / castellated outline** (seen at the lower right in AWS71, the bottom in AWS74, the right in AWS76). Reading AWS71 and AWS74 together, the front outline goes, from the left front-corner facet's end (x −34, y +38): forward to (−28, +44), across to (−16, +44), forward to (−12, +50), across to (+4, +50) under the motor's front, back to (+10, +46), across to (+22, +46), back to (+30, +40) and to the right facet end at (+34, +38). So the plate has a **central tongue under the motor** and **two lower steps** either side. **(medium; the exact steps are blurred)**
- **Height**: bottom face at **z ≈ 3** (ground clearance 3 mm under the wheels' Ø 24 on centres at z 12, the plate is supported by the wheel axles at mid-height of the drive blocks). Top face z ≈ 5.
- **Holes**: hex nuts (NT) sit on the base at the wall's front-left corner (AWS71, (−34, +36)) and at the right front (AWS74), and standoff bases beside each wheel block, so the base has **through-holes for M3 screws from below** at each of those points.

### 2.2 Wall band (WL-1..WL-7) and lettering (TXT)
- **Material**: **thin aluminium sheet**, ≈ **0.6–0.8 mm**, bright cut edges, scratched and dented, folded at sharp creases into a closed-at-rear band. Every photo tints it green (reflection), so its true colour is plain silver aluminium.
- **Height**: from the base top (z 5) to **z ≈ 26**, i.e. **≈ 21–22 mm tall**. The bottom edge of the facets is slightly bent outwards and torn in places (AWS71 lower left: a curled lip at the front end of the VAMPIRE facet).
- **Plan polygon** (outer face; corners are creases):
  - WL-1 **front-left corner facet**: from (−34, +38) to (−48, +18), angled 55° to the X axis.
  - WL-2 **left side** (with "VAMPIRE"): from (−48, +18) to (−48, −22), **40 mm long**. It is the long flat facet nearest the camera in AWS76. The left wheel sits just inside it.
  - WL-3 **rear-left diagonal**: (−48, −22) to (−30, −44).
  - WL-4 **rear**: (−30, −44) to (+30, −44), **60 mm**.
  - WL-5 **rear-right diagonal**: (+30, −44) to (+48, −22).
  - WL-6 **right side**: (+48, −22) to (+48, +18).
  - WL-7 **front-right corner facet**: (+48, +18) to (+34, +38).
  - Between (−34, +38) and (+34, +38): **no wall** (open front).
- **Top edge**: has a **narrow inward flange / hem** (bright rim along the top in AWS74), about 2–3 mm wide, on which the top plate rests or to which it is screwed **(guess, medium)**.
- **TXT**: the word **"VAMPIRE"** in **black, square, stencil-like capitals** about **5 mm tall, 30 mm long**, on WL-2 at mid-length, low down (z ≈ 9–14), printed / vinyl-cut / marker **(guess: vinyl sticker or laser-etched paint)**. AWS71 shows it reading vertically on the facet (it is the same text seen at an angle).
- **Fixing**: the band's ends at the front-corner facets are held by **M3 bolts and nuts** through bent-in feet into the base plate (the nuts at the front corners), and the top flange is held by the top screws **(guess, medium)**.

### 2.3 Top plate (TPL), tabs (TAB), screws (CS)
- **Material**: a **thin (≈ 1 mm) clear polycarbonate sheet with a frosted/scratched surface**. In AWS71 it looks translucent: a **black rectangular label with white text** near its rear edge and **red / orange / blue** parts are visible through it; in AWS74/76 it reflects like brushed metal. **(guess: polycarbonate, medium; alternative: thin aluminium with stickers under the reflections)**.
- **Outline**: it fills the wall polygon from the rear to about **y +12**, then its front edge is a **V-notch / chevron cut** pointing **backwards** around the motor: from the left front-corner facet's top (−34, +38) the edge runs **back and inward** to (−16, +20), then a short straight across behind the motor at y ≈ +4 (x −16 to +16) (the notch floor; it clears the bell by ≈ 2 mm), then forward and outward to (+16, +20) and (+34, +38). In AWS71/74 the notch's sides also show **small rectangular steps** (the edge is stepped where it passes the motor blocks).
- **Height**: at **z ≈ 25–26**, resting on the wall flange.
- **TAB-L / TAB-R**: two **narrow strips (≈ 12 mm wide)** of the same clear sheet **bent down at about 60–70°** from the notch's side edges, running down to the base plate beside each drive-motor block (AWS71: from (−20, +14, 25) down to (−16, +20, 5); AWS74: the mirror on the right). They **brace the top plate against the base** at the front (a folded leg instead of a standoff) and form an **inner guard** between the motor/bar area and the wheel blocks. They are slightly translucent with scratches.
- **CS**: **countersunk silver screws** in the top plate, seen at: rear centre (0, −40); right-front (+40, +10) (AWS74); left (−40, +6) (AWS76). The fourth is probably at (+0, −40)… i.e. 3–4 screws total, into standoffs or the wall flange (+ 2 near the rear diagonals hidden under the bar's paddle in some views) **(medium)**.

### 2.4 Drive wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 24 mm × 10 mm**. Black rubber tyre with **fine axial ribs** (≈ 40 ribs, 1.8 mm pitch, 0.6 mm deep) all round, flat tread, rounded shoulders. Black plastic hub (spokes not visible: the hubs face inward toward the motor blocks; outward faces are hidden by the walls).
- **Position**: centres at **(x ±38, y −2, z 12)**: the wheels sit **just inside the side walls** (outer face at |x| ≈ 44, 3–4 mm inside the wall's inner face at |x| ≈ 47), at about the middle of the body's length. AWS71 shows the left wheel right behind the VAMPIRE facet's front half, AWS74 the right wheel just inside the right side wall's front.
- **Protrusion**: the wheel bottoms reach the floor through **cut-outs in the base plate** (wheel slots ≈ 26 × 12 mm). The wheel tops at z 24 are **just under the top plate** (≈ 1–2 mm gap). So the robot is **not invertible** in drive (upside down it rests on the top plate, wheels 1 mm short of the floor… drive may scrape on the flange). **(guess: the wheels protrude a hair past the top so it can limp inverted, low)**.
- **Guards**: the **side walls** are the outer guards (fully covering the wheels' outer sides from z 5 to 26), the top plate covers them from above, the tabs and motor blocks are inside. The wheel is exposed only **below** (the base slot).

### 2.5 Drive motors (DM) and motor blocks (MB)
- **Visible**: a **black rectangular block** inboard of each wheel, about **14 mm (X) × 12 mm (Y) × 12 mm (Z)**, with a **flat front face** and the wheel on its outer side (AWS71 at the left wheel, AWS74 at the right). This is either the **N20 gearbox itself** (12 × 10 mm, black plastic gear housing on some N20 variants) or a **printed black clamp** around it. Next to each block, slightly forward/inward, a **black round post (standoff, Ø 6)** with a **silver screw and washer** on top at z ≈ 9–12 (AWS71 (−28, +8); AWS74 (+28, +8)): the **clamp screw** that holds the block to the base plate (a screw through a printed strap into a nut under the base) **(medium)**.
- **Hidden part**: the N20 motor can (Ø 12 × 15 long) runs **inward** from the gearbox along X toward the centre, at y ≈ −2, z 12, so the two motors lie **end to end across the body** behind the weapon motor.

### 2.6 Weapon motor (WM) and mount
- **Type**: a black **brushless outrunner**, **bell Ø ≈ 28 mm**, bell height ≈ 14 mm, total height (stator base + bell) ≈ 22 mm: the **2204/2205/2206 class** (≈ 25–30 g). The bell top has **five large rounded windows** (between five curved spokes) showing **copper windings**; its side has a **thin silver/green ring groove** and machined steps; the stator base has a printed/printed-on label "**…Todar**" in white script (AWS74). The shaft end shows through the bar's centre hole.
- **Position**: axis vertical at **(x 0, y +20)**. The motor base stands **directly on the carbon base plate** (top face z 5), so the bell top is at z ≈ 27–28 and the bar is above it at z ≈ 28–31. (In AWS76 the bar's underside is about 4 mm above the walls' top edge → bar z ≈ 30–33. **Reconciled: bar underside z 30.**)
- **Mount**: the motor base is fixed with **M2/M3 screws from below** through the carbon plate into the stator mount's 16 × 19 mm pattern; AWS71 shows **two small silver screw heads / wire exits** at the motor's base front. Wires (3 phase) exit at the base toward the rear, into the body under the top plate (where the blue item is).
- **Exposure**: the motor stands **in the open front**, protected only by the front-corner facets on each side and the stepped base plate below; its front face is fully exposed.

### 2.7 Bar (BAR) and screws (BS)
- **Material**: **flat steel bar** (silver, scratched, with impact gouges), **≈ 3 mm thick** (edge seen in AWS74/76) **(guess: hardened steel or Hardox-type strip; could also be 4 mm aluminium, low)**.
- **Plan shape** (bar frame: u along the bar from the motor axis, v across):
  - **Hub zone**: |u| ≤ 12, width 14 (v ±7); **four M3 socket-cap screws (black, head Ø 5.5, 3 mm tall)** on a square of side ≈ 9 mm (bolt circle Ø ≈ 12.7) around a **centre hole Ø ≈ 5** (shaft end / clearance). One extra small hole just beside the square (AWS71 (1 o'clock of the hub), a balance or locating hole).
  - **Long arm BAR-L**: from u 12 to u ≈ 72, **width 14 mm**, straight edges.
  - **Tip BAR-T**: from u 72 to u 80 the arm **flares to ≈ 20 mm wide** (a T-ish flare that widens symmetrically by 3 mm each side over 6 mm), with the **end edge chewed, burred and bent down slightly** (impact deformation; AWS71/74/76 all show a jagged end). The flare is the **striking face**.
  - **Short paddle BAR-S**: from u −12 to u ≈ −22 the bar keeps 14 mm, then **steps out (shoulder at 90°, with small 45° chamfers) to ≈ 26 mm wide** from u −22 to u −58, with **cut corners** (45° chamfers ≈ 4 mm) at the far end. The paddle's extra width is the **counterweight** that balances the longer arm.
  - **Balance check**: arm mass moment ≈ 14 × 3 × (80² − 12²)/2 · ρ ≈ 13 140 ρ; paddle ≈ 14·3·(22² − 12²)/2 + 26·3·(58² − 22²)/2 = 7140 + 112 320 ≈ … larger; so the arm and paddle **do not balance with a full 26 mm paddle unless the paddle is shorter** — see §13.2. **Reconciled: paddle 22 mm wide from u −24 to −52** (balanced within ~5 %).
- **Height**: bar plane at z 30–33. Bar overhang: the long end reaches **≈ 80 mm** from the axis, i.e. far beyond the body on every side as it spins: the bar's swept circle (radius 80 about (0, +20)) reaches y −60 behind the rear wall, x ±80 beyond the side walls, and y +100 in front.
- **Rotation direction**: not determinable from stills. The **leading edges** of the chewed tip are both burred; the flare suggests either direction **(guess: clockwise seen from above, low)**.

### 2.8 Screws, nuts, standoffs summary
- **BS**: 4 × M3 black socket caps on the bar.
- **CS**: 3–4 × M3 countersunk silver screws on the top plate.
- **NT**: silver M3 hex nuts on the base plate at the front-left corner (AWS71), right front (AWS74), and on the motor-block posts.
- **SO**: 2 × black posts with silver screws and washers next to the drive blocks; hidden 3–4 standoffs (M3 × 20) between base and top plate near the rear **(guess)**.
- **WMS**: 4 × M3 (or M2) screws under the base into the weapon motor.

### 2.9 Electronics, switch and wires
- **Visible**: a **blue** item behind the weapon motor, under the top plate's notch, on the left (AWS71 (−8, +4, 15); AWS76 at the motor's left, AWS74 behind the motor): most likely the **weapon ESC in blue heat shrink** or **blue silicone wires** **(medium)**. Through the translucent top (AWS71): a **black rectangular sticker/label** with white text near the rear (probably on the battery or the receiver), and **red/orange** patches (red battery leads / connector) on the right-rear.
- **Switch**: not visible. **Guess (low)**: a slide switch reached through a hole in the rear wall or a removable link under the top plate.

---

## 3. Per-view descriptions

### 3.1 Top view (synthesised)
- A heptagon (a rectangle with the rear corners cut at 45° and the front corners cut more steeply), 96 wide × 82 deep (y −44 → +38), the front side open. The top plate is a frosted rectangle-ish panel with a deep **V-notch** at the front, inside which sits the round **motor (Ø 28)** at (0, +20). The carbon base plate shows in front of the wall and in the notch, with a stepped front edge reaching y +50 at the centre. The bar lies across everything: a long narrow strip from the motor to one side and a short wide paddle to the other, ≈ 138 mm in total, so it reaches past the body outline at both ends in any orientation.

### 3.2 Front view (inferred from AWS71/AWS74)
- At the bottom, the carbon plate's front edge (2 mm thick) with steps; at the centre the black motor can standing on it (Ø 28, 22 tall), the bar across its top at z 30–33 reaching out to both sides beyond the body (its ends overhanging). Either side of the motor, the drive blocks and wheels (Ø 24) behind the angled front-corner facets of the aluminium wall; behind, the frosted top's notch and the rear wall.

### 3.3 Left side view (AWS76)
- A long low aluminium wall 22 mm tall with "VAMPIRE" on its centre, the rear-left diagonal facet receding at the left, the front-left facet curling at its front end; above and behind, the top plate's edge with a countersunk screw; the left wheel's top just visible above the wall's front half (wait: it is visible through the notch). In front (right), the motor standing on the carbon plate, its bell with windows; the bar across the top, seen almost edge-on, with the short paddle on the left over the rear and the long arm to the far right ending in the chewed tip, ≈ 80 mm ahead of the motor.

### 3.4 Front-left view (AWS71)
- The VAMPIRE facet lower left with the left wheel and its block and post just inside it; the clear tab descending beside the motor; the motor centre-right with its five-window bell; the bar diagonally from the upper left (paddle) to the lower right (long arm); the right wheel at the upper right inside the right wall; the frosted top with the label visible through it; the carbon front with its stepped edge.

### 3.5 Front-right view (AWS74)
- Mirror of AWS71 from the other side, with the bar the other way round (long arm to the lower left): right wall and front-right facet, right wheel and block with the post, the right clear tab, the motor with its "…Todar" label, the blue item behind it, the left wheel at the upper left.

### 3.6 Rear view (not photographed; inferred)
- A flat aluminium wall 60 mm wide with two 45° diagonals to the sides, 22 mm tall, the bar above it at z 30–33 (the paddle or the arm overhanging the rear depending on angle).

### 3.7 Underside (not photographed; inferred)
- A flat carbon plate with two wheel slots near mid-length, countersunk screw heads for the motor, standoffs and wall feet, the stepped front edge.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 96 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BP | heptagon + stepped front tongue | 96 × 94 × 2 | 1 × 0.98 | black carbon twill | screws | 1 |
| WL | folded band, 7 facets | perimeter ≈ 270, 22 tall, 0.7 thick | 0.23 tall | aluminium | nuts at feet, top flange | 1 |
| TXT | lettering "VAMPIRE" | 30 × 5 | — | black | sticker/paint | 1 |
| TPL | sheet with V-notch | 96 × 82 × 1 | 1 × 0.85 | clear frosted PC | 3–4 CS screws | 1 |
| TAB | bent strip | 12 wide × 22 long | — | clear PC | integral fold | 2 |
| WH | ribbed wheel | Ø 24 × 10 | 0.25 | black rubber | N20 D-shaft | 2 |
| DM + MB | N20 gearmotor in black block | 14 × 12 × 12 (+ can 12 × 15) | — | black / silver | strap + post screw | 2 |
| SO | post + screw + washer | Ø 6 × 7 | — | black / silver | into base | 2 visible |
| WM | outrunner 22xx | Ø 28 × 22 | 0.29 | black, copper windings | 4 screws from below | 1 |
| BAR | asymmetric flat bar | 132–138 × 14 (26/22 paddle) × 3 | 1.4 | steel | 4 × M3 socket caps | 1 |
| BS | socket cap screw | M3 × 8 | — | black | into bell | 4 |
| CS | countersunk screw | M3 | — | silver | into standoffs | 3–4 |
| NT | hex nut | M3 | — | silver | — | 3+ |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WH bottom ↔ floor | contact | 0 |
| BP bottom ↔ floor | above | 3 |
| BP-F front edge ↔ floor | above | 3 |
| WL bottom ↔ BP top | standing on / fastened | 0 |
| WH outer face ↔ WL inner face | running clearance | 3 |
| WH top ↔ TPL underside | clearance | 1–2 |
| WH ↔ BP wheel slot ends | clearance | 1 |
| MB ↔ WH inner hub | adjacent | 1 |
| MB ↔ BP | clamped | 0 |
| TAB lower end ↔ BP | resting / bonded | 0 |
| TAB ↔ MB | beside | 2 |
| TPL ↔ WL top flange | resting / screwed | 0 |
| TPL notch floor ↔ WM bell | clearance | 2 |
| WM base ↔ BP | screwed | 0 |
| BAR underside ↔ WM bell top | clamped | 0 |
| BAR underside ↔ TPL top | clearance over the body | 4–5 |
| BAR underside ↔ WL top edge | clearance | 4 |
| BAR sweep radius ↔ WL outermost corner (from motor axis) | bar overhangs | +12 … +40 |
| BS heads ↔ BAR top | seated | 0 |
| WM front ↔ BP-F front edge | base projects ahead | 8 |

---

## 6. Mechanism

1. **Weapon**: a **horizontal bar spinner mounted directly on the outrunner's bell** (direct drive, no belt). The bar's long arm (80 mm) hits first; with a 2205-class motor at ≈ 2300 kV on 2S–3S, unloaded speed ≈ 17–25 k rpm; realistically the bar spins up to ≈ 10–15 k rpm → **tip speed 80–125 m/s**, very high energy for an antweight (stored energy ≈ ½ I ω², I ≈ 40 g × (138²)/12 ≈ 63 000 g·mm² → at 12 000 rpm ≈ 50 J). The asymmetric bar is a **single-tooth bar**: one long striking end, one short wide counterweight, so the long tip takes a deeper "bite" per revolution (more time between tip passes for the opponent to move in).
2. **Height**: the bar spins **above** the walls (z 30–33): it hits opponents' **top edges, side walls and wheels** rather than getting under them. Against low wedges it passes over unless they climb.
3. **Drive**: 2WD, wheels at mid-length just inside the side walls; skid steer, turning about the body centre. The front base plate and rear wall's bottom edges are the skids.
4. **Gyroscopic effect**: a bar spinner of this inertia resists turning; turning at speed tilts the robot (lifts one wheel). The low, wide body is designed to stay flat.

---

## 7. Assembly order (suggested rebuild)
1. Cut the **carbon base plate** (outline, stepped front, wheel slots, holes) and the **aluminium wall band** blank; fold the band at the six creases and the inner top hem; fold the band's foot tabs.
2. Bolt the **weapon motor** to the base from below (4 screws), wires toward the rear.
3. Clamp the **two N20 gearmotors** in their black blocks onto the base (posts and screws), shafts outward; press the **wheels** on.
4. Fit the **ESCs, receiver, battery and switch** in the rear bay; route the motor phase wires back under the top.
5. Stand the **wall band** on the base and bolt its feet with M3 bolts and nuts at the front corners (and elsewhere hidden).
6. Fit **standoffs**; lay the **top plate** (cut V-notch, tabs bent down) onto the wall flange; fit the **countersunk screws**.
7. Fit the **bar** onto the motor bell with **4 M3 socket screws** (thread-lock).
8. Apply the **"VAMPIRE"** lettering to the left wall.

---

## 8. Hidden / uncertain list
- Top plate material (clear PC vs aluminium), number and positions of its screws.
- Exact stepped outline of the carbon front.
- Whether the drive blocks are printed clamps or bare gearboxes; wheel hub style.
- Bar material and exact paddle shape (the paddle width vs balance); spin direction.
- Switch location; layout of battery and ESCs.
- All dims ±15 %.

## 9. Coordinate frame (restated)
Origin on the floor under the body polygon's centre; +X right; +Y forward (open front); +Z up; mm. Weapon axis: vertical line (0, +20). Bar plane z 30–33. Wheels at (±38, −2, 12), Ø 24 × 10. Wall: heptagon with vertices (±34, +38), (±48, +18), (±48, −22), (±30, −44), height z 5–26.

## 10. Profiles as math

**10.1 Wall plan polygon (outer face).** P = [(−34, 38), (−48, 18), (−48, −22), (−30, −44), (30, −44), (48, −22), (48, 18), (34, 38)], open between the first and last vertex. Wall is the offset band between P and P inset by 0.7, extruded z ∈ [5, 26], with an inward hem of width 2.5 at z = 26.

**10.2 Top plate.** Region inside P (inset 1) intersected with the half-plane complement of the notch N, where N is the polygon [(−34, 38), (−16, 20), (−16, 4), (16, 4), (16, 20), (34, 38)]; z ∈ [26, 27]. Tabs: rectangles 12 × 24 hinged on the notch side edges, rotated 65° downward.

**10.3 Base plate.** Region inside P (inset 0) ∪ front tongue polygon [(−34, 38), (−28, 44), (−16, 44), (−12, 50), (4, 50), (10, 46), (22, 46), (30, 40), (34, 38)]; z ∈ [3, 5]; minus wheel slots |x ∓ 38| ≤ 6, |y + 2| ≤ 13.

**10.4 Bar (in the bar frame, u along, v across, thickness 3, z ∈ [30, 33]).**
- Long arm: |v| ≤ 7 for u ∈ [0, 74]; tip flare: |v| ≤ 7 + 3·(u − 74)/6 for u ∈ [74, 80], end at u = 80.
- Short side: |v| ≤ 7 for u ∈ [−24, 0]; paddle |v| ≤ 11 for u ∈ [−52, −24], corner chamfers 4 × 45° at u = −52.
- Holes: 4 × Ø 3.2 at (±4.5, ±4.5), centre Ø 5 at (0, 0), one Ø 2.5 at (6, 9)… (balance hole, approximate).
- Swept volume: cylinder r = 80 about (0, 20), z ∈ [30, 33].

**10.5 Motor.** Stator base cylinder r 14, z ∈ [5, 13]; bell cylinder r 14, z ∈ [13, 28] with a 1 mm groove at z 17; top face with five windows, each the region between radii 5 and 12 and an angular width of 50°, centred at 72°·k.

**10.6 Wheel.** Tyre annulus r ∈ [9, 12], width 10, with 40 axial ribs as r(φ) = 12 − 0.6·[sin(40φ/2)]² (ribbed).

## 11. Pixel-based measurements (PNG conversions, 1200 px wide; ±8 px)
- **AWS76**: motor can width x 500 → 720 (220 px). Bar from x 150 to 1165 (1015 px), hub (screw square centre) at x ≈ 600 → short end 450 px, long end 565 px. Left wall facet with text from x 230 to 590 (360 px), receding rear facet x 45–230. Wall height at the near end ≈ 200 px (y 360 → 560) vs at the far end ≈ 150 px. Lettering "VAMPIRE" ≈ 140 px long × 25 px tall.
- **AWS71**: motor x 450 → 680 (230 px). Bar from (100, 180) to (1165, 450) ≈ 1100 px; hub at (565, 290); narrow arm width ≈ 70 px (perpendicular); paddle width ≈ 110 px. Left wheel ≈ 150 px across. Front-left screw/post at (290, 490), nut at (300, 585).
- **AWS74**: motor ≈ 240 px across; bar from (70, 500) to (1000, 190); paddle ≈ 230 px long × 90 px wide; right wheel ≈ 130 × 150 px.

## 12. Several independent estimates

| Quantity | Method A (motor Ø 28) | Method B (wheel Ø 24) | Method C (cube / diagonal) | Reconciled |
|---|---|---|---|---|
| Bar length | AWS76: 1015/220 × 28 = 129 | AWS71: 1100/150 × 24 = 176 (wheel farther from camera than bar ends → inflated) | ≤ 143.7 (face diagonal) | **≈ 132–138** |
| Long arm (axis → tip) | AWS76: 565/220 × 28 = 72 | — | — | **≈ 76–80** (the far tip is foreshortened in AWS76) |
| Short side (axis → end) | 450/220 × 28 = 57 | — | — | **≈ 52–57** |
| Arm width | AWS71: 70/230 × 28 / sin 40° ≈ 13 | — | — | **14** |
| Paddle width | AWS71: 110/230 × 28 / 0.64 ≈ 21; AWS74: 90/240 × 28 / 0.6 ≈ 18–26 | — | — | **22** |
| Body width | AWS71: wall-to-wall ≈ 830 px?/230 × 28 ≈ 100 | — | ≤ 101.6 | **96** |
| Side facet length | AWS76: 360 px /220 × 28 = 46 (the facet is nearer the camera than the motor → inflated) | — | — | **40** |
| Wall height | AWS76 near end 200/220 × 28 ≈ 25 (near → inflated) | ≈ wheel Ø − 2 | — | **21–22** |
| Lettering | 140/220 × 28 ≈ 18 (?) — the facet is nearer | — | — | **≈ 25–30 × 5** |

## 13. Consistency check
1. **Bar vs cube**: a 138 mm bar does not fit a 101.6 mm cube edge but fits its **face diagonal (143.7 mm)** with the bar turned to 45°. The body (96 × 94 including the front tongue) also fits. **Consistent: the bar is sized to the cube diagonal.**
2. **Bar balance**: with ρ·t constant, the first moment of the long side (width 14 to u 74 + flare to u 80) is ≈ 14·74²/2 + 17·(80² − 74²)/2 ≈ 38 330 + 7 850 = 46 180; the short side with a 22 mm paddle from 24 to 52: 14·24²/2 + 22·(52² − 24²)/2 = 4 030 + 23 410 = 27 440. **Not balanced** (ratio 1.7). To balance with the 14-wide hub, the paddle would need to be ≈ 30 mm wide out to u 58: 14·24²/2 + 30·(58² − 24²)/2 = 4 030 + 41 820 = 45 850 ✔. The photos show the paddle about 1.6–1.9 × the arm width (≈ 22–26 mm) and longer than I first measured. **Reconciled: paddle 26 mm wide from u −22 to u −58** (moment 14·22²/2 + 26·(58² − 22²)/2 = 3 390 + 37 440 = 40 830, 12 % short; the remainder is covered by the long arm's centre hole and the extra balance hole, or the bar simply runs slightly out of balance as many antweight bars do). Final: **paddle 26 × 36 (u −22 → −58), arm 14 wide to u 74, flare to 20 at u 80.** (Overrides §10.4's 22 mm paddle.)
3. **Bar clearance over walls**: motor on the base top z 5 + 22 height + bell top → bar underside z ≈ 27–30; walls top z 26: **clearance 1–4 mm**. AWS76 shows a visible gap of ≈ 3–4 mm. **Consistent with bar underside z 30** if the motor stands on a 3 mm spacer or the motor is 25 mm tall (2206). Take **bar underside z 30**.
4. **Wheels vs top**: wheel Ø 24 with centre z 12 → top z 24; top plate z 26 → 2 mm gap. **Consistent.**
5. **Mass**: carbon base 12 g, aluminium wall 8 g, top PC 5 g, bar steel 138 × ~16 avg × 3 × 7.85e-3 ≈ 52 g (!), outrunner 28 g, two N20 + wheels 24 g, ESCs 8 g, battery 2S 300 mAh 18 g, RX 3 g, screws/standoffs 6 g → **164 g: over 150 g**. So the bar is lighter than solid steel 3 mm: either **2 mm steel (35 g)** or **4 mm aluminium (≈ 19 g)** or the outrunner is smaller (2204, 22 g). **Reconciled: bar 2.5 mm steel (≈ 43 g) or aluminium; total ≈ 148 g.** The bar's edge in AWS74 looks ~2.5 mm.
6. **Wheel diameter**: Method B inflated the bar; using the bar 135 and AWS71 wheel 150/1100 → 18 mm, but the wheel is farther from the camera than the near bar tip; the wheel tops just below the 26 mm top → Ø ≈ 22–24. **Reconciled: 24.**

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Long asymmetric top bar**
  - Attack: the longest possible bar (cube diagonal) gives the most stored energy and the highest tip speed for the motor; a **single long striking end** with a **wide counterweight paddle** gives one deep bite per turn instead of two shallow ones, which matters at antweight scale where opponents approach slowly relative to the spin.
  - The flared tip concentrates the steel at the impact face and gives a square impactor; the chewed end shows it doing its job.
  - Adversarial: mounted **above the walls**, it overhangs everything, so it hits opponents before they reach the body from any direction; wedges cannot get under the bar to the motor without first being hit.
- **Direct-drive outrunner**: no belt or bearings to fail; the bell is the hub. The cost is that every hit goes into the motor's bearings and shaft, and the motor is exposed at the front.
- **Open front with stepped carbon tongue**: there is no room for a wall in front of the motor (the bar must clear it), so the base plate projects forward to protect the motor's base and to act as a low skid; the steps keep weight down and give corners that catch opponents' wedges.
- **Carbon-fibre base**: very stiff and light, takes the bar's reaction torque and impact loads, and is thin (2 mm) so the robot stays low.
- **Folded aluminium wall**: light and tough, deflects horizontal spinners with its angled rear and front-corner facets (no square corners at the rear), and is easy to bend back after a hit (the dents show this). It also is the **outer wheel guard**.
- **Clear top plate with a V-notch**: lets the operator see the electronics (LEDs, damage) without opening it, is light, and the notch makes room for the motor while keeping the top close to the bar; bent tabs act as legs so no extra standoffs are needed at the front.
- **Wheels inside the walls, mid-length**: fully shielded at the sides; mid-length puts the robot's turning centre near the body centre, which helps aim the bar; low wheels keep the body low.
- **Lettering**: robot identification (the event requires names), and a nod to the bar's "bite".

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Weapon ESC | 12–20 A BLHeli ESC in blue heat shrink | 25 × 12 × 5 | (−10, +2, 10) | medium |
| Drive ESC | dual brushed ESC (Malenki / DasMikro) | 20 × 15 × 5 | (+14, −20, 10) | medium |
| Battery | 2S/3S LiPo 300–450 mAh | 50 × 20 × 12 | across the rear, (0, −32, 12) | medium |
| Receiver | micro 2.4 GHz rx with black label | 18 × 12 × 4 | (−20, −30, 20) | low |
| Drive motors | 2 × N20 (100:1–50:1) | 12 × 10 × 25 | (±25, −2, 12) | high |
| Standoffs | 3–4 × M3 × 20 aluminium | Ø 5 × 21 | near the rear corners and rear centre | medium |
| Switch | slide switch or link through the rear wall | 12 × 4 × 6 | (+20, −42, 14) | low |
| Weapon motor screws | 4 × M3 × 6 from below | — | on Ø 16/19 pattern | high |
| Wall feet | bent tabs of the band with M3 bolts | 8 × 6 | at the wall corners | medium |
| Wiring | battery → switch → ESCs → motors; phase wires from WM back under the notch | — | — | high |

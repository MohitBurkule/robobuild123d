# I Never Asked For This: full rebuild description from reference photos

Source photo (cut out onto white by the AWS wiki):
- `robots/i_never_asked_for_this/reference/i_never_asked_for_this.aws71.webp`: AWS 71, native 2194 × 1431 px. It shows the **front-left-top three-quarter**: the camera is about 30–35° above the floor and about 30–35° to the robot's left of straight-on. The whole front wedge, the top lid, the two left wheels, both right wheels and the right side guard are visible. The underside, the rear wall and the left side guard are not visible.

This is the **only** photo, so the rear, the underside and the left outer guard are inferred by symmetry. It is still a clear, sharp, close photo, so the top and front can be described in full detail. Everything stated as fact is read from that photo. Anything inferred is marked **(guess)**. Dimensions in mm are **estimates**, scaled from the AWS antweight limit (150 g, must fit a 101.6 mm / 4 in cube) and cross-checked against the project kit draft (`kit.json`: body 92 × 80 × 24 mm, four wheels r 12 × 9 mm wide at y = −30 and +22, front plate profile from (y 44, z 26) to (y 64, z 1.5)). Ratios are given against **W = central body width ≈ 66 mm**.

A note on colour: the whole photo has a **strong green colour cast** (the white background was masked, but the robot itself is lit green; even the grey aluminium wedge reads greenish). The body is either **very dark bottle-green** plastic or **black** plastic under green light. The kit draft chose `#1f4a38` (dark green). This description calls it **dark green/black** and treats the colour as uncertain.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the wedge), **+Z** = up. Units are mm.
- **Origin O** = the point on the floor (z = 0) directly under the centre of the central body footprint (mid-width, mid-length of the box between the wheel slots).
- **Front** = the end with the silver wedge. In the photo the front faces the lower-left of the image; the robot's width runs from image left (robot left) to image right (robot right), descending about 20°; the robot's length runs into the image toward the upper-right.
- **Left/right** are the robot's own. The robot's left is on the image left.
- Angles in side profiles are measured from the floor (+Y axis) in the YZ plane unless stated otherwise.

| ID | Part |
|---|---|
| CB | central body (dark green/black printed tub, between the wheel slots) |
| LID | top lid (flat dark plate over CB and over the wheel slot bridges) |
| OV-A, OV-B, OV-C, OV-D | raised top overlay strips (thin second layer on the lid, each ending in a screw lobe) |
| S-LID1…S-LID4 | four silver Torx/pozi-star pan screws through the overlay lobes into the lid/body |
| WS-L, WS-R | wheel slots (open channels each side between CB and the side guards) |
| WH-FL, WH-RL, WH-FR, WH-RR | four wheels: grey ribbed tyres on dark hubs |
| HB-x | wheel hubs (dark, inside the tyres) |
| M-x | drive gearmotors (hidden, guess) |
| SG-L, SG-R | side guards (outer wheel guard plates, stadium-shaped, vertical) |
| BR-L, BR-R | guard-to-body bridges (lid tabs crossing the wheel slots between the wheels, joining LID to SG) |
| SP-x | guard spacers/axle bosses (hidden, guess) |
| WD | front wedge plate (silver metal, two facets with a crease) |
| WD-U, WD-L | upper facet and lower facet of WD |
| S-WD1…S-WD4 | four silver star-drive pan screws holding WD to the body front |
| FW | body front wall (hidden behind WD; shape guessed) |
| BAT, ESC, RX, SW | battery, ESC/receiver board, switch (hidden, guess) |
| WR | wires (one thin wire just visible inside the right front wheel slot) |

---

## 1. Overall description in one paragraph

I Never Asked For This is a **low, wide, four-wheel wedge**. Seen from the front-left it is a **flat, dark green/black slab about 96 mm wide, 86 mm long and 25 mm tall**, with a **single full-width silver metal wedge plate** bolted across the whole front of the central body. The wedge plate is **two-faceted**: a steeper upper facet (about 55° from the floor) runs down from the lid's front edge, and at a straight crease line about two thirds of the way down it turns into a **shallower lower facet** (about 30–35°) that carries the leading edge to the floor. The lower facet shows a different, **spangled/crystalline galvanised texture**, and four **silver star-drive pan screws** (two per facet, in two columns) hold the plate on. Behind the wedge, the **flat lid** covers the central body and carries a **raised pattern of thin overlay strips** whose edges stand about 1–1.5 mm proud and which end in **rounded lobes**, each lobe held down by one silver star-drive screw (four in all). Each side of the central body has an **open wheel slot** holding **two wheels with grey, axially ribbed tyres**, one near each corner. Outside the wheels, a **tall stadium-shaped side guard plate** (same dark plastic) runs the length of the side and shields the outer faces of both wheels. The guards are tied to the body by **bridge tabs** of the lid that cross the wheel slot between the front and rear wheels. The wheels stand slightly taller than the guards and the lid, so the robot can drive inverted. There is no active weapon.

---

## 2. Part-by-part description

### 2.1 Central body (CB)
- **Shape**: a rectangular box. Plan about **66 mm wide (x ±33) × 80 mm long (y ±40)**; height from about **z = 2** (floor clearance, guess) to the underside of the lid at **z ≈ 22.5**, so about **20–21 mm** of wall. The vertical long edges are not seen. The top long edges are crisp under the lid (any radius under 1 mm), although the kit draft rounded them at 5 mm; the photo shows the **lid**, not the body, forms the top edges, and the lid edges are square with a slight burr.
- **Colour/material**: dark green/black, matte, no visible print layer lines on the surfaces we see (the lid hides them). The walls inside the wheel slots show a smooth, slightly glossy surface, so the body may be **printed with a smooth finish or machined from black HDPE/polycarbonate sheet** **(guess; printed PETG/nylon is most likely for a 150 g bot)**.
- **Walls**: the inner wall of the right wheel slot is visible in the crop behind WH-FR: a flat vertical face, dark, at about x = +33. A **thin dark wire** (WR, Ø ≈ 1 mm) is just visible running fore-aft low in the slot, in front of the front-right wheel hub, at about z ≈ 6–8 mm. This suggests either a motor lead that exits the body there or a lead that runs along the slot to a motor mounted outboard (see 2.13).
- **Front wall FW**: completely covered by the wedge plate WD. Because WD has two facets and is screwed flat at four points, the front wall is most likely **itself a two-facet sloped face** matching WD (upper facet about 55°, lower facet about 32°), or a vertical wall with two printed ribs/bosses that the screws thread into **(guess; the sloped printed nose is more likely because the plate is screwed through both facets)**.
- **Rear wall**: never seen. Presumably plain, about 66 × 21 mm, probably carrying the switch **(guess)**.
- **Underside**: never seen. Presumed flat at z ≈ 2 with possibly a switch slot **(guess)**.

### 2.2 Top lid (LID)
- **Shape**: a flat plate, about **2 mm thick**, covering the whole central body and extending outward at the bridges (BR) to the side guards. Plan outline: a rectangle about **66 × 80 mm** over CB, plus a **bridge tab each side** (see 2.9). The lid's front edge meets the top edge of the wedge plate WD at about **y = +40, z ≈ 24**. Top surface at **z ≈ 24.5**.
- **Colour**: the same dark green/black as CB, with a slightly satin finish and small white specks/dust.
- **Corners**: at the right-front, where the lid turns outward into the right bridge, the lid's outer edge forms a **concave curve** following the wheel slot; the edge here has a **rounded, almost tubular 3–4 mm radius** (seen as a soft highlight in the crop). At the left-front, the lid edge curves back behind the front-left wheel. At the right-rear, the lid edge has a **step/notch** where it meets the guard (visible as a small vertical step about 3 mm tall near the rear-right wheel).
- **Fasteners**: the lid itself shows no screws except the four through the overlay lobes (S-LID1…4). These almost certainly pass through the overlay, through the lid, and into bosses or posts in the body **(guess)**.

### 2.3 Raised overlay strips (OV-A…OV-D)
- **What is seen**: the lid surface carries a pattern of **thin raised layers** whose edges are visible as **dark, slightly frayed or chamfered outlines** (the edges catch light and show a burr, typical of laser-cut or knife-cut thin sheet). Inside the outlines the surface is level and of the same colour. The step height is about **1–1.5 mm**.
- **Shapes** (described in plan, with estimated positions):
  - **OV-A (left/front arm)**: a band about **10–12 mm wide** that starts near the **rear-left** of the lid (y ≈ −35, x ≈ −25), runs forward and inward diagonally, and ends in a **rounded lobe** (radius about 6 mm) around **S-LID1** at about **(x −16, y +15)**. Near its rear end it is joined to OV-B in a shallow V, so OV-A + OV-B together form a **λ / wishbone shape** in the left-rear quadrant.
  - **OV-B (rear centre)**: an outline that forms a **"U" or bracket shape** in the rear-centre: a band running rightward along the rear part of the lid from about x −10 to x +5, turning forward at both ends, and ending in a rounded lobe around **S-LID2** at about **(x −2, y −30)**. Inside the U is a recessed pocket (lid level). Its inner outline has a smooth bulbous curve at the left (like a rounded hook).
  - **OV-C (right rear)**: a band starting at a rounded lobe around **S-LID3** at about **(x +20, y −15)** and sweeping rearward and outward toward the right-rear guard/bridge region, widening slightly. Its trailing edge runs along about y = −22 to the lid's right edge.
  - **OV-D (right front)**: a band starting at a rounded lobe around **S-LID4** at about **(x +6, y +16)**, sweeping outward to the **right bridge BR-R**, curving around the front of the front-right wheel slot, and merging into the right bridge/guard top. Its front outline runs nearly parallel to the wedge top edge, about 6–8 mm behind it.
- **Interpretation (guess, medium)**: these are most likely **thin (1–1.5 mm) polycarbonate or HDPE straps/armour sheets laid on the printed lid**, each fixed with one screw. Two likely purposes: (a) they are **a second skin of armour** shaped to cover the electronics below and leave other areas as plain lid, saving weight; (b) they are **retaining straps** that clamp the lid down and the internal parts (battery, ESC) in position. A third, cosmetic possibility is that they form a **stylised "graffiti" logo**. The rounded screw lobes strongly suggest the strap/armour reading. An alternative reading (low) is that the lid itself is pocketed (weight-relief cut-outs 1–1.5 mm deep) and the "strips" are the unpocketed ribs between the pockets.
- **Pattern symmetry**: the pattern is **not mirror-symmetric**. The left side has the λ/wishbone (OV-A + OV-B); the right side has two separate S-curves (OV-C, OV-D).

### 2.4 Lid screws (S-LID1…S-LID4)
- **Type**: silver (zinc-plated or stainless) **pan or wafer heads** with a **six/eight-point star (Torx or pozi-star) recess**, head Ø ≈ **4.5–5 mm**, so **M2.5 or M3** with a wide wafer head, or **3 mm wood/plastic self-tappers** (the head form is typical of "pozi/Torx chipboard screws" sold for plastic). Each sits on a **flat lobe** of overlay. The heads are about 1.5 mm tall.
- **Positions** (estimates, ±8 mm): S-LID1 (−16, +15); S-LID2 (−2, −30); S-LID3 (+20, −15); S-LID4 (+6, +16). All at z ≈ 26 (head top ≈ 27.5).
- **Pixel locations** in the native image (±10 px): S-LID1 (730, 357), S-LID2 (1060, 176), S-LID3 (1535, 325), S-LID4 (1232, 533).

### 2.5 Wedge plate (WD, with facets WD-U and WD-L)
- **Shape**: a **single bent metal plate** spanning the full width of the central body, about **68 mm wide** (it overhangs CB by about 1 mm each side; its right end lines up with the inner face of the front-right wheel; its left end lines up with the inner face of the front-left wheel). Thickness about **1.5 mm** (a thin edge line is visible at the chamfered right-bottom corner).
- **Side profile** (constant across X):
  1. Top edge at **(y +40, z 24)**, tucked just under the front edge of the lid (no visible gap between them).
  2. **Upper facet WD-U** slopes down and forward at about **55°** to the floor, about **18 mm** long down the slope, reaching the crease at about **(y +50, z 9.5)**.
  3. **Crease** (bend line), straight and parallel to X across the full width; it appears as a fine dark line with a very slight step (the lower facet looks 0.2–0.5 mm "proud" in the photo, which also fits a separate overlapping strip; see below).
  4. **Lower facet WD-L** continues at about **32°** to the floor, about **16 mm** long down the slope, to the **leading edge** at about **(y +63.5, z 0.5)** touching or just skimming the floor.
- **Plan outline**: a rectangle about 68 mm wide; the **top two corners are chamfered** (the left top corner shows an angled cut of about 6 × 6 mm), and the **bottom right corner** shows a **small 45° chamfer of about 4 mm** where the leading edge meets the side edge. The left bottom corner is square or slightly chamfered (hidden partly by the image edge).
- **Surface/material**: the upper facet is **dull grey, abraded/sanded aluminium**, with dark smudges and scratches typical of fighting. The lower facet has a **distinct spangled, crystalline texture** like **hot-dip galvanised steel**, lighter in tone. Two readings:
  - (a) **one plate** of galvanised steel, bent at the crease; the upper facet has been painted/dulled or scuffed to grey **(medium)**;
  - (b) a **grey aluminium upper plate** with a **separate galvanised steel lip strip** overlapping it along the crease line and held by the lower screws **(medium-low)**.
  Either way the lower facet is harder and thinner-edged, built to take floor scraping.
- **Screws (S-WD1…4)**: four silver **star-drive pan heads** (head Ø ≈ 5 mm, slightly larger than the lid screws), each sitting on a small **dimpled/countersunk ring** pressed into the plate. They are in **two columns**, each column one screw on the upper facet and one on the lower facet:
  - Left column at about **x ≈ −23**: S-WD1 on WD-U at about mid-facet (y +45, z 17); S-WD2 on WD-L just below the crease (y +53, z 7.5).
  - Right column at about **x ≈ +14**: S-WD3 on WD-U (y +45, z 17); S-WD4 on WD-L (y +53, z 7.5).
  - The columns are **not symmetric about the centreline**: the left column is about 10 mm in from the left end and the right column about 19 mm in from the right end. The perspective (the right end is nearer the camera, which should make it look *bigger*) reinforces rather than explains the asymmetry, so the asymmetry is probably real **(medium)**. A likely reason is that the screws thread into internal bosses placed to clear the battery or ESC **(guess)**.
  - Pixel locations: S-WD1 (495, 478), S-WD2 (390, 643), S-WD3 (1155, 759), S-WD4 (1034, 935).

### 2.6 Wheel slots (WS-L, WS-R)
- **Shape**: open channels each side of CB, from front to rear, about **11 mm wide** (x from ±33 to ±44), open at the top except where the bridge crosses, and open at the bottom (the wheels touch the floor through them). The inner wall is the body side wall; the outer wall is the side guard.
- Seen clearly on the right: the front-right wheel sits in the slot with the guard immediately outside and the dark body wall immediately inside; above the wheel, the slot is open to the sky in front of the bridge.

### 2.7 Wheels (WH-FL, WH-RL, WH-FR, WH-RR)
- **Shape**: a short cylinder about **Ø 26 mm × 9 mm wide**. The tyre is **light grey**, with about **48–56 fine axial ribs** (ridges running across the full tread width, about 0.8 mm tall, pitch about 1.5 mm), like a ribbed TPU or silicone tyre or a moulded "Pololu-style" rubber tyre with a knurled tread. The tyre's sidewall is about 3 mm deep (radially), so the **hub** is about Ø 20 mm. The **hubs are dark** (black/dark green), recessed about 1–2 mm from the tyre's outer edge; one hub face (front-right) shows a small **silver glint at the centre**, likely a **set screw or the motor shaft end**.
- **Positions** (wheel centres, estimates):
  - WH-FL (−38.5, +24, 13); WH-RL (−38.5, −26, 13); WH-FR (+38.5, +24, 13); WH-RR (+38.5, −26, 13).
  - So the **wheelbase is about 50 mm**, the **track (centre to centre) about 77 mm**, and the **wheel inner faces sit about 1 mm from the body walls** (x ±34) and the **outer faces about 1 mm from the guard inner faces** (x ±43).
- **Height relations**: tyre top at z ≈ 26, about **1–1.5 mm above the lid** and about **0.5 mm above the overlay strips**, so the robot can run inverted on the wheels if the overlay is no taller. Tyre bottom at z = 0. The guard bottom is at z ≈ 2 and the guard top at z ≈ 24, so each tyre peeks out by about 2 mm above and below the guard.
- **Pixel data**: WH-FR tread visible over native x 1560–1810, y 680–1095; WH-RR x 1880–2060, y 445–575 (mostly hidden behind the guard top); WH-FL x 225–505, y 185–405 (the left half, the right half being hidden behind the wedge's upper corner); WH-RL x 640–790, y 50–120 (only its top arc).

### 2.8 Side guards (SG-L, SG-R)
- **Shape**: a **vertical flat plate** in the YZ plane, about **3.5–4 mm thick** (x from ±44 to ±48), outline a **stadium/rounded rectangle**: about **86 mm long (y −43 to +43) × 22 mm tall (z 2 to 24)**, with **fully rounded ends** (end radius about 10–11 mm, i.e. nearly half the height) at the front and a tighter radius (about 6 mm) at the top-rear corner. On SG-R the front end sweeps down in a smooth large-radius curve from the top edge to the floor-side edge, so the front of the guard reads as a **"D" nose**.
- **Top edge**: straight and level at z ≈ 24 over most of the length, with a **small step down of about 3 mm** just ahead of the rear wheel where the bridge meets it (on SG-R; visible as a notch near the rear-right wheel). The rear wheel's top arc shows above the guard behind this notch.
- **Colour/material**: same dark green/black as the body, smooth, with a slight satin sheen; the edges are slightly rounded. Printed in the same material or cut from 4 mm black plastic sheet **(guess: printed, because the guard is joined to the bridge with a smooth fillet)**.
- **Outer face features**: no screws visible on SG-R's outer face. The **axle ends do not show through** it, so the wheels are **not** carried on through-axles fixed in the guard; they are either on the motor shafts (motors in the body) with the guard only as a shield, or the guard has blind bosses inside **(guess)**.
- **Fit**: guard inner face about 1 mm from the tyre outer face; guard bottom about 2 mm above the floor (so it never drags).

### 2.9 Guard-to-body bridges (BR-L, BR-R)
- **Shape**: a **tab of the lid** about **14–16 mm long (fore-aft) × 11 mm wide (across the slot) × 2–3 mm thick**, crossing the wheel slot **between the front and rear wheels** (at about y −8 to +8), joining the lid to the top edge of the side guard. Its **front edge is a smooth concave curve** that follows the front wheel's top arc with about **2 mm clearance**, and at the guard end it rolls over in a **round fillet (r ≈ 3–4 mm)** into the guard's top. On BR-R this bridge reads in the photo as a **rounded bar** with a highlight along it, directly above the front-right wheel's rear quadrant.
- **Function**: the only visible connection that holds each guard to the body. Probably reinforced by a **hidden spacer block or rib** below the bridge between the wheels, from the body wall to the guard (SP-x, guess, medium), because a 2 mm lid tab alone would let the guard flap.

### 2.10 Front wall (FW), hidden
- **Guess**: the printed nose of CB forms a sloped support face behind WD with **four bosses** (Ø 7 mm) at the screw positions, holding heat-set inserts or taking self-tappers. The nose is probably **solid or heavily ribbed** to back the wedge plate against hits **(guess, medium)**.

### 2.11 Wires (WR)
- One thin **dark wire** (Ø ≈ 1 mm) is seen in the right wheel slot, low down and behind the front-right wheel, running fore-aft at z ≈ 6–8 mm, with a hint of copper colour where it meets the hub (or a reflection). This is probably a **motor lead** leaving the body through a small hole in the slot wall to a motor that is partly in the slot, or a lead to the rear motor routed along the outside **(guess, low)**.
- No other wiring is visible. No switch or LED is visible on any seen face.

### 2.12 Electronics (hidden, guess)
- Battery, ESC/receiver board and switch are inside CB below the lid. The kit draft used a 2S 180 mAh LiPo, a Malenki Nano (combined receiver + dual ESC) and a 12 × 4 slide switch on the floor; those choices are consistent with the photo's internal volume (about 60 × 74 × 18 mm usable).

### 2.13 Drive motors (hidden, guess)
- **Four N20-class gearmotors** (about 12 × 10 × 25 mm + 9 mm shaft), one per wheel, lying transversely inside CB at z ≈ 13, shafts out through the side walls into the wheel hubs. Alternatively **two motors** each driving a side, with the front and rear wheels coupled internally (no belts visible). Four motors are more likely given four independent wheel slots with a full-depth guard and no visible belt (medium).

---

## 3. Per-view sections (for silhouette matching)

### 3.1 The photo view (front-left-top three-quarter, AWS 71)
- Dominant element: the **silver wedge**, a broad slanted rectangle across the lower-left half of the image, with the crease line running parallel to its leading edge and four screw heads in two columns. The wedge's left end shows the angled top chamfer; the right end shows the bottom chamfer.
- Above and behind: the **dark lid** with the raised overlay outlines and four screws.
- Left: the **front-left wheel** (grey ribs) peeking out above and behind the wedge's left corner; the **rear-left wheel's** top arc at the far upper-left.
- Right: the **front-right wheel** in its slot, partly enclosed by the **right side guard's rounded "D" nose**, with the **bridge** rolling over above; the **rear-right wheel's** top just showing above the guard at the far right, with a green glint from inside the slot.
- Silhouette: a flat parallelogram (top) with a protruding wedge "skirt" along the lower-left edge and round wheel/guard lumps at the right end.

### 3.2 Top view (plan; synthesised)
- Outline: a rectangle about **96 mm wide × 86 mm long** (guards included), plus the wedge projecting about **23.5 mm** forward of the body front (to y ≈ +63.5) across the central 68 mm. Total length about **106 mm** (body rear −43 to wedge tip +63.5). **Note**: 106 mm exceeds the 101.6 mm cube in length alone; the wedge must start further back or the body is shorter (see conflict 2 in section 12; reconciled length 80 mm overall body, 100 mm total).
- On top: the central dark lid with the λ-shaped left overlay, the U-shaped rear overlay, two right S-strips and four screw dots; two wheel slots each side showing grey tread bands at the four corners; the bridges in the middle of each slot; the guards as thin dark rails on the outside.

### 3.3 Front view
- Bottom: the wedge as a 68 mm wide band from the floor up to z ≈ 24, showing two facets (lower one wider in projection because it is shallower). Four screws in two columns at x −23 and +14.
- Each side: a wheel slot with a grey tyre (9 mm wide, Ø 26) then the 4 mm guard with the rounded nose. Tyre tops just above the lid and guard tops.
- Overall front silhouette: a low rectangle 96 × 26 mm with the wedge's slope in front of the middle 68 mm.

### 3.4 Left side view (inferred, mirror of the right side)
- A long stadium-shaped dark guard (86 × 22 mm) with the tops and bottoms of two grey tyres peeking out at the front and rear, the bridge fillet in the middle of the top edge, and the silver wedge's triangular side edge sticking out in front (from z 24 at y 40 down to the floor at y 63.5).

### 3.5 Rear view (not photographed; inferred)
- A plain dark rear wall 66 × 21 mm between two wheel slots and guards; probably a switch slot and possibly a charge plug **(guess)**. The guard rear ends rounded.

### 3.6 Underside (not photographed; inferred)
- Flat floor at z ≈ 2; four tyre contact patches through the slots; the wedge's leading edge on the floor. Probably 4–8 screw heads closing the floor and a switch access slot **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CB | box tub | 66 × 80 × 21 | 1 × 1.21 × 0.32 | dark green/black, printed (guess) | — | 1 |
| LID | flat plate + bridge tabs | 66 × 80 × 2 (+2 tabs 15 × 11) | 1 × 1.21 × 0.03 | dark green/black | 4 screws via overlays | 1 |
| OV-A…D | thin strips with lobes | 10–12 wide, 25–45 long, 1–1.5 thick | 0.17 × ~0.5 | dark, cut sheet | 1 screw each | 4 |
| S-LID | star-drive wafer/pan | head Ø 4.5–5 | 0.07 | silver | into body bosses | 4 |
| WD | 2-facet bent plate | 68 wide; facets 18 + 16 long; 1.5 thick | 1.03 | aluminium / galvanised steel | 4 star pan screws | 1 |
| S-WD | star-drive pan | head Ø 5 | 0.08 | silver | into nose bosses | 4 |
| WH | ribbed tyre wheel | Ø 26 × 9 | 0.39 × 0.14 | grey tyre, dark hub | motor shaft + set screw | 4 |
| SG | stadium plate | 86 × 22 × 4 | 1.30 × 0.33 × 0.06 | dark | via bridge (+ hidden spacer) | 2 |
| BR | lid tab with fillet | 15 × 11 × 2.5 | 0.23 × 0.17 | dark | integral with LID/SG (guess) | 2 |
| WR | wire | Ø 1 | — | dark/copper | — | ≥1 visible |
| M | N20 gearmotor | 12 × 10 × 25 | — | — | clamps (guess) | 4 (guess) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LID bottom ↔ CB wall tops | rests on, screwed | 0 |
| OV-x ↔ LID | laid on, screwed | 0 |
| S-LID ↔ OV lobe | head clamps lobe | 0 |
| WD top edge ↔ LID front edge | butt, under lid lip | 0–0.5 |
| WD back ↔ FW nose | screwed flat | 0 |
| WD leading edge ↔ floor | touching/skimming | 0–0.5 |
| WD side ends ↔ front wheel tyres (WH-FL/FR inner faces) | side by side | 1–2 |
| WD rear corners ↔ front wheel tread | near | 2–3 |
| WH inner face ↔ CB side wall | near | 1 |
| WH outer face ↔ SG inner face | near | 1 |
| WH top ↔ LID top plane | wheel above | +1.5 |
| WH top ↔ SG top edge | wheel above | +2 |
| WH bottom ↔ floor | touching | 0 |
| WH-FR tread ↔ BR-R front curve | under the bridge | 2 |
| WH-FL tyre ↔ WH-RL tyre | fore-aft gap | 24 |
| SG bottom ↔ floor | above | 2 |
| SG top ↔ BR | joined (fillet) | 0 |
| BR ↔ LID | integral or butt-screwed | 0 |
| SG ↔ CB (hidden spacer between wheels) | joined (guess) | 0 |
| CB floor ↔ floor | above | 2 (guess) |
| WR ↔ slot wall | runs along | 0–1 |

---

## 6. Mechanism
1. **Drive**: four-wheel skid steer, each wheel turned by its own gearmotor **(guess)**. The wheels are fully enclosed at the sides by body and guard, and peek out top and bottom, so the robot drives either way up.
2. **Weapon**: none active. The wedge is the weapon: drive under the opponent, lift its edge on the two-facet ramp, and push it into the wall or pit, or unbalance it so it flips.
3. **Invertibility**: the wedge's top edge is at z ≈ 24 and its tip on the floor. When upside down, the wedge tip is about 24–26 mm above the floor and the wedge is **useless** inverted (it slopes the wrong way: from the floor-side, the lid side, its leading edge is up at z ≈ 24). So inverted, the robot is a pure pusher. This is common on simple wedges **(design observation)**.

---

## 7. Assembly order (suggested rebuild)
1. Print **CB** with its sloped nose bosses (FW), internal motor cradles, the hidden guard spacers and the side guards **SG** if they are integral (they may be printed as one part with the lower body and the bridges as part of the lid).
2. Fit four **gearmotors** into their cradles, shafts out through the slot walls at z 13, y +24 and −26.
3. Fit the **electronics** (battery, receiver/ESC board, switch) and route the wires (one lead visible in the right front slot).
4. Press the **wheels** onto the motor shafts, tighten their set screws.
5. Fit the **side guards** if separate (screws through hidden spacers).
6. Place the **LID**, bridging to the guards.
7. Lay on the **overlay strips OV-A…D** and drive in the four **S-LID** screws, clamping the overlay, lid and body together.
8. Bend the **wedge plate WD** (crease at about 18 mm from the top edge, from 55° to 32°), drill four holes with dimples, and screw it to the nose with **S-WD1…4**.

---

## 8. Coordinate frame (restated)
- Origin O on the floor under the centre of CB. +X right, +Y forward, +Z up. mm.
- CB extents: x ∈ [−33, +33], y ∈ [−40, +40], z ∈ [2, 22.5]; lid to z 24.5; overlay to z 26.
- Wheel slots: x ∈ ±[33, 44]. Guards: x ∈ ±[44, 48], y ∈ [−43, +43], z ∈ [2, 24].
- Wedge: x ∈ [−34, +34], from (y 40, z 24) to (y 63.5, z 0.5).

## 9. Profiles as math (for rebuilding curves)

**9.1 Wedge side profile (YZ plane, outer face of WD, constant over x ∈ [−34, +34]).**
- Upper facet: line from P1 = (40, 24) to P2 = (50, 9.5); slope angle atan(14.5/10) = 55.4°. Parametric: (y, z) = (40 + 10t, 24 − 14.5t), t ∈ [0, 1].
- Lower facet: line from P2 = (50, 9.5) to P3 = (63.5, 0.5); slope angle atan(9/13.5) = 33.7°. Parametric: (y, z) = (50 + 13.5t, 9.5 − 9t).
- Crease: inside bend radius 1.5 mm (one plate thickness). Thickness 1.5 mm offset behind (toward −Y/−Z) the line.
- Facet lengths: upper √(10² + 14.5²) = 17.6 mm; lower √(13.5² + 9²) = 16.2 mm. Flat blank height = 33.8 mm, width 68 mm.

**9.2 Wedge plate corner chamfers (in the plate's own flat blank, u across width, v down the slope from the top edge).**
- Top corners: lines from (u ±34, v 6) to (u ±28, v 0), i.e. 6 × 6 mm at 45°.
- Bottom right corner: line from (u 34, v 29.8) to (u 30, v 33.8), i.e. 4 × 4 mm.
- Screw holes Ø 3.2 at (u −23, v 9), (u −23, v 21), (u +14, v 9), (u +14, v 21), each with a 7 mm dimple.

**9.3 Side guard outline (YZ plane, extruded along X by 4 mm at x = ±44 to ±48).**
- Stadium with unequal ends: the bottom edge z = 2 for y ∈ [−37, +32]; the top edge z = 24 for y ∈ [−37, +32] except the notch.
- Front end: arc centre (y 32, z 13), r = 11, from θ = −90° to +90° (i.e. the "D" nose reaching y = +43).
- Rear end: arc centre (y −37, z 18), r = 6 for the top-rear corner (θ from 90° to 180°), then a vertical line y = −43 from z 18 down to z 8, then arc centre (−37, 8), r = 6, θ 180° to 270°.
- Notch: z drops to 21 for y ∈ [−18, −12] (where the bridge meets the guard top, rear side).

**9.4 Wheel tread (in the wheel's own frame, disc in the YZ plane).**
- r(φ) = 12.2 + 0.8·[sin(N·φ) > 0], N = 52, φ ∈ [0, 2π). Width 9 mm. Hub disc r = 10, recessed 1.5 mm from both tyre faces. Shaft bore D-shaped, Ø 3 with a 0.5 mm flat.

**9.5 Bridge BR front edge (in plan, XY plane).**
- Arc following the front wheel top with clearance: centre (x ±38.5, y +24), r = 15 (13 + 2 clearance), between y = +8 and y = +11; the bridge rear edge is a straight line y = −8; outer end fillet: a quarter-round r = 3.5 rolling down into the guard top.

**9.6 Overlay strips (plan, approximate polylines, band width w).**
- OV-A: centreline from (−25, −35) to (−16, +15), w = 11, lobe circle r = 6 at (−16, +15).
- OV-B: U polyline (−12, −24) → (−12, −36) → (+6, −36) → (+6, −24), w = 9, lobe circle r = 6 at (−2, −30) on the base of the U.
- OV-C: centreline arc from (+20, −15) to (+33, −24), w = 10, lobe r = 6 at (+20, −15).
- OV-D: centreline from (+6, +16) to (+33, +10) to (+38, +2) (on the bridge), w = 10, lobe r = 6 at (+6, +16).

## 10. Pixel-based measurements (independent check)
Native image 2194 × 1431 px. Coordinates (x, y) from the top-left, read by eye, ±10 px.
- Wedge leading edge: from (105, 703) to (1430, 1205): length √(1325² + 502²) ≈ 1417 px.
- Wedge top edge: from (330, 320) to (1530, 715): length ≈ 1263 px (farther from the camera than the leading edge, so shorter).
- Crease line: from (175, 575) to (1500, 990).
- Left screw column: (495, 478) and (390, 643). Right column: (1155, 759) and (1034, 935).
- Right guard: front-bottom of the "D" nose at about (1700, 1090); outer face top-front at (2130, 560); thickness seen at the nose ≈ 35 px.
- WH-FR tread visible band: x 1560–1810, height y 680–1095 (≈ 415 px tall, partly the tyre's front face).
- Lid rear edge (top silhouette): from (720, 80) to (1700, 420).

## 11. Several independent estimates of key quantities

| Quantity | Method A (kit / rules) | Method B (ratio in photo) | Method C (pixels + scale) | Reconciled |
|---|---|---|---|---|
| Central body width | kit 80 incl. part of slots | wedge ≈ 0.71 of total front width (1417 / (1417 + 2·290)) → 0.71 × 96 = 68 | leading edge 1417 px at ≈ 20.8 px/mm (scale from screw head Ø 5 mm = 104 px at the front) → 68 | **66 body, 68 wedge** |
| Overall width | ≤ 101.6 cube | body + 2 × (1 + 9 + 1 + 4) = 66 + 30 = 96 | right slot + guard ≈ 290 px at 20.8 → 14 mm per side → 96 | **96** |
| Wheel Ø | kit r 12 → 24 | tyre ≈ 1.1 × guard height (22) = 24–26 | WH-FR 415 px tall, of which ≈ 80% is diameter (the rest is tread face seen obliquely) → 332 px / (≈ 13 px/mm at the slot depth) = 25.5 | **26** |
| Body height (to lid top) | kit 24 | guard ≈ 0.92 of wheel → 24 | wedge vertical rise 24 from the profile fit | **24.5** |
| Wedge depth (horizontal) | kit 20 (44→64) | facets 18 + 16 along the slope → 10 + 13.5 = 23.5 | crease-to-edge projected 128 px vs top-to-crease 255 px at the left end; with the angles above the ratio 16.2·cos… predicts 0.5, measured 0.50 | **23.5** |
| Upper facet angle | kit ≈ 52° overall | facet looks steep, near 55° | ratio of vertical pixel extents vs facet lengths → 53–57° | **55°** |
| Lower facet angle | — | visibly shallower, about 30–35° | 33° from the fit | **33°** |
| Wheelbase | kit 52 (−30 to +22) | wheel gap ≈ the bridge length + 2 × clearance → 24 + 26 = 50 | WH-FL centre (365, 295) to WH-RL centre (715, 100) = 400 px along the depth axis; foreshortened ≈ 0.4 → 1000 px / 20.8 ≈ 48 | **50** |
| Screw head Ø | M2.5 wafer 5 mm | head ≈ 0.07 W | 104 px at front scale → 5.0 | **5** |
| Guard thickness | — | ≈ 0.4 of the tyre width | 35 px at ≈ 9 px/mm (rear depth) → 3.9 | **4** |

## 12. Consistency check: conflicts and reconciliation
1. **Wheel diameter**: kit 24 vs pixel 25.5 vs ratio 24–26. The pixel value includes some perspective enlargement at the nearer right side. **Reconciled Ø 26 mm** (tyre peeks 1.5 mm above the lid). If Ø 24 is used, the tops would sit level with the lid and inverted driving would be marginal, which contradicts the visible tyre tops standing above the guard. Keep 26.
2. **Overall length vs the 4 in cube**: body 80 + guard nose 3 + wedge 23.5 = 106.5 > 101.6. Either the body is shorter (75 mm) or the wedge starts at the body front at z 24 and the rear guard ends do not extend beyond the body. The photo shows the guard nose roughly level with the front wheel front, i.e. about 3–5 mm behind the wedge top edge, and the rear is unseen. **Reconciled: body y ∈ [−37, +37] (74 mm), guards y ∈ [−40, +39], wedge to y +60.5, total 100.5 mm**. Shift all y values above by −3 for the wedge (P1 = (37, 24), P2 = (47, 9.5), P3 = (60.5, 0.5)) and scale the wheel y positions to +21 and −24 (wheelbase 45, tyre gap 19). The bridge (15 mm) still fits in the 19 mm gap with 2 mm clearance each side.
3. **Body width vs kit width 80**: the kit width 80 includes half of each wheel slot; the photo clearly shows the wedge only spanning between the front wheels. **Reconciled: body 66, overall 96.**
4. **Wedge material**: grey upper vs spangled lower facet. Either is consistent with all other evidence; the mass budget allows 1.5 mm aluminium (≈ 9 g) or 0.8 mm galvanised steel (≈ 15 g). **Reconciled: model as one 1.5 mm plate with a visual seam at the crease; note the material as uncertain.**
5. **Screw column asymmetry** (x −23 vs +14): perspective cannot explain it (it would exaggerate the right end). **Kept as real.**
6. **Top overlay height vs tyre top**: overlay top at 26 equals the tyre top at 26 (Ø 26, centre 13). Inverted, the robot may rest on the overlay strips and lose traction. Since the designer clearly runs this robot, the tyre is probably slightly larger (Ø 27) or the overlay thinner (1 mm). **Reconciled: tyre Ø 26.5, overlay 1 mm, lid top 24.5, overlay top 25.5, tyre top 26.5: 1 mm clearance.**

---

## 13. Why the designer did it (per part, mostly adversarial)

Common lens: for each part, what attacks can reach it (spinners horizontal and vertical, enemy wedges and lifters, flippers, wall slams, inversion), how the part survives, and how it helps win (getting under the opponent first). Then construction reasons: printability, assembly, weight, repair.

- **Low, wide, flat body (CB, 24.5 mm tall, 96 mm wide)**
  - Fight: a low profile gives a vertical spinner very little face to bite and gives flippers and lifters little under-edge to get beneath; a wide stance resists being turned and makes the robot hard to flip side-over-side. Wide also means the wedge covers more of the arena front, so an opponent who drives at it almost always meets metal.
  - Weak points: the long flat sides are exposed to horizontal spinners, which is why the guards exist.
  - Construction: a simple printed tub with a lid, easy to print with no supports; everything mounts from the top.

- **Two-facet metal wedge (WD)**
  - Getting under vs contact: the **lower 33° facet** is the "get under" part: its shallow angle and thin metal edge on the floor slip under opponents' edges and wedges. Once under, the **steeper 55° upper facet** lifts the opponent quickly in a short distance, so the opponent's wheels come off the floor sooner (they lose traction and get pushed). A single 33° wedge would need to be about 40 mm long to reach the same height; the two facets keep the robot inside the 4 in cube.
  - Against spinners: a sloped metal face deflects horizontal spinner teeth upward and over the lid, and deflects vertical spinner hits into the floor instead of taking them square. Metal survives where a printed wedge would shatter.
  - Against enemy wedges: the edge sits on the floor (0–0.5 mm), so in a wedge-vs-wedge meeting it has a fair chance of getting under. The galvanised/hard lower facet resists being rolled up or chipped by the floor and by opponents' edges.
  - Full width between the wheels: there is no gap for an opponent's fork to slip between wedge sections.
  - Screws in two rows on both facets: the upper row takes the bending load when the upper facet lifts; the lower row stops the lower facet peeling up when an opponent rides onto it. The dimpled seats keep the heads low so an opponent's edge slides over them. Asymmetric columns probably clear internal parts **(guess)**.
  - Construction: a single bent plate is cheap and fast to replace; star-drive screws resist cam-out when tight.

- **Wheel slots with full guards (WS, SG)**
  - Fight: the guards protect the wheels from **horizontal spinners and side wedges**: a spinner tooth hitting the side meets a smooth rounded plastic plate instead of a soft tyre or a motor shaft. The rounded **"D" nose** at the front of each guard deflects glancing hits and keeps the guard from snagging on arena walls or on an opponent's wedge corner. The guards also stop opponents getting a fork **between the wheels and the body**.
  - Getting under: the guard bottom at 2 mm above the floor keeps the guards out of the floor contact so all the weight stays on the wheels and on the wedge edge.
  - Weak points: the guards are held only by the bridges (and probably hidden spacers); a heavy vertical spinner hit on the guard top could crack the bridge.
  - Construction: printed, with a fillet at the bridge to avoid a stress corner.

- **Bridges BR (guard-to-chassis supports)**
  - Fight: they tie each guard to the main body so the guard spreads a side hit into the body; placed between the wheels so they never touch the tyres, and curved around the front wheel for clearance. The rounded top fillet sheds overhead hits.
  - Construction: part of the lid, so taking the lid off releases the guards for wheel changes **(guess)**.

- **Grey ribbed tyres, Ø ≈ 26 mm**
  - Fight: the axial ribs grip the arena floor for pushing matches, which matter for a weaponless wedge. Being slightly taller than the body lets the robot keep driving after being flipped.
  - Weak points: tyres peek out above and below the guards; a vertical spinner can still clip the tyre tops.
  - Construction: off-the-shelf moulded tyres or printed TPU, pressed on.

- **Top lid with raised overlay strips (LID, OV)**
  - Fight: the top is hit by overhead weapons (vertical spinners from above, hammers) and is what an opponent's wedge rides over. The strips add a second layer of armour where it matters (over the battery and ESC, guess) without the weight of a full double lid. Their edges are low (1 mm) so an opponent sliding over the top does not catch.
  - Construction: the four screws each clamp a strip, the lid and the body together; one screw per strip makes armour replacement quick. The pattern may also double as the robot's graphic identity.

- **Star-drive screws throughout**
  - Construction: Torx/pozi-star heads resist stripping and keep their heads round after impacts, which matters on a front plate that gets hit. All silver, probably from one box of screws.

- **No active weapon**
  - Fight: everything goes into the wedge, armour and drive. A full-width wedge with four-wheel drive is the classic reliable antweight pusher; with no weapon motor, more mass budget is left for a metal front and guards.

- **Hidden switch and low wire routing**
  - Fight: nothing to snag or to be switched off by an opponent; the only visible lead is tucked low in the slot behind the wheel.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 6 V gearmotors, about 300–500 rpm | 12 × 10 × 25 (+9 mm shaft) | transverse, shafts at z 13; y +21 and −24; bodies at x ±20 | medium |
| Motor cradles | printed U-slots in the floor, closed by the lid or by printed clamps | 14 × 12 × 26 | over each motor | medium |
| Battery | 2S 7.4 V LiPo 180–300 mAh | 40 × 18 × 10 | centre-rear, x −5, y −8, z 8 | medium |
| ESC + receiver | combined board (Malenki Nano class) | 30 × 20 × 6 | centre-front behind the nose, x +5, y +18, z 8 | medium |
| Switch | slide switch on the floor or a link on the rear wall | 12 × 4 × 6 | x +15, y −30, z 4 | low |
| Nose bosses | four printed bosses with heat-set M2.5/M3 inserts or self-tapper pilot holes | Ø 7 × 8 | behind the S-WD screws | medium |
| Lid posts | four posts under the S-LID screws | Ø 6 × 20 | at the S-LID positions | medium |
| Guard spacers | a printed rib each side between the wheels, from the body wall to the guard, under the bridge | 15 × 11 × 18 | x ±38.5, y −1, z 12 | medium |
| Wires | motor leads (four pairs) to the ESC; one front-right lead seen in the slot; battery to switch to ESC | — | low along the walls | medium |
| Floor screws | 4–6 screws closing a separate floor plate, or none if the tub is one print | — | underside | low |

**Wiring path summary (guess)**: battery in the middle, switch near the rear floor, ESC/receiver behind the nose, motor leads along the side walls at floor level, all under the lid and inside the guards; nothing exposed except the short lead seen in the right front slot.

## 15. What the photo cannot show (uncertain list)
- The rear wall, the underside, and the left guard (mirror assumed).
- Wedge material (aluminium vs galvanised steel, one plate vs two).
- Whether the guards are integral with the body or separate pieces.
- The true colour (dark green vs black under a green cast).
- The exact overlay-strip shapes (described within ±5 mm).
- All mm values are scaled estimates (±10–15%).

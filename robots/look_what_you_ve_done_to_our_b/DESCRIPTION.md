# Look What You've Done To Our Breakfast: full reference description

This document describes the real robot from its three reference photos in enough detail to rebuild it from the text alone.
Each statement is tagged:

- **[seen]**: directly visible in at least one photo.
- **[inferred]**: follows from what is visible, for example from symmetry or from how such parts are normally made.
- **[guess]**: not visible. It is an estimate, and the photos neither confirm nor contradict it.

All sizes are in millimetres. Absolute sizes are estimated from one assumption [guess]: the tyres are about 28 mm in diameter, the usual size of N20 rubber wheels on antweights. Every size below scales with that number. Ratios between parts are measured from the photos and are more reliable than the absolute numbers. Pixel coordinates are given as (x, y) in each photo's own frame, origin top-left, measured on the full-size image.

Coordinate convention, the same as the CAD spec:
- +y is forward (towards the end called "front" here).
- +x is the robot's right.
- +z is up.
- z = 0 is the wheel axle height.
- The floor is at z = -14, the bottom of the tyres.

The robot is front/back symmetric, so "front" just means the end that faces the camera's left in aws74 and the camera in aws68. Nothing on the outside tells the two ends apart, except the switch slot in aws74 (see the top plate section).

---

## 1. Photo inventory

| Photo | Event | Camera | Background / quality | Version of robot |
|---|---|---|---|---|
| `aws68` | AWS 68 (oldest) | Nearly straight on to one end ("front"), elevation about 25-30 deg, slightly left of centre. | In the pits, on a white table with a grey back; other robots cut off at the left and right edges (orange). Soft, low resolution (542 x 460). | Early version: white masking/gaffer tape on the ramp, 4 corner screws on the lid. |
| `aws71` | AWS 71 | Front-right three-quarter view, elevation about 30-35 deg. The front wedge is at the image's lower right and the wheels on the robot's right side face the camera. | Cut out on white. Strong blue/cyan colour cast: the red hubs read dark blue and the tyres teal-black. Hi-res (2098 x 1329). | Middle version: a clear polycarbonate (or thick clear tape) skin on the ramp, 4 corner screws on the lid. |
| `aws74` | AWS 74 (newest) | Front-left three-quarter view, elevation about 25-30 deg. The front wedge runs along the image's lower left and the left-side wheels are at the lower right. | Cut out on white, true colours. Hi-res. | Latest version: clear polycarbonate on the ramp, about 11 lid screws (black and silver mixed), a switch slot, a hand-drawn marker circle. |

The three photos show one design that has been repaired and rebuilt over time, not three different robots [inferred]. The outer shape, the colours, the wheel layout and the double-ended wedge are the same in all three. Where versions differ (ramp covering, number of screws, switch slot), each version is described separately.

---

## 2. Overall form

1. **Type.** A four-wheel-drive pusher wedge (a "rammer/wedge") with a wedge at both ends [seen]. There is no active weapon: the weapon is the two passive ramps [seen: there is no spinner, flipper arm, lifter, crusher or grabber in any photo, and no slot or hinge line where one could hide].
2. **Symmetry.** The robot is mirror-symmetric left-right [seen in aws68, where the camera looks almost straight along the length axis and both halves match]. It is also mirror-symmetric front-back [seen: in aws74 the rear end block, top right of the image, has the same chamfered plan corner and vertical inner face as the front block; in aws68 the far end block peeks out behind the lid with the same chamfered corners]. In plan view it is a "two-way arrow": a narrower rectangular centre section between two wider end blocks, and each end block tapers to a straight tip edge.
3. **Footprint.** Overall length is about 96-100 mm [estimate]. Overall width is about 104 mm [estimate], set by the end blocks, which reach slightly past the outside faces of the tyres. Width / length is about 1.0-1.08, so the robot reads as almost square in plan, but its rectangle is "pinched" at the waist by the wheel notches.
4. **Height.** The top surface is about 28 mm above the floor (z = -12 bottom of chassis to z = +16 top) [estimate]. The height / length ratio of the silhouette is about 0.6 in the iso photos. The tyres reach about the same height as the top plate, within 1-2 mm [seen in aws68 and aws74]. In aws71 they look slightly proud of the top, because of the camera angle.
5. **Visual impression.** It looks like a flat blue brick, a bit like a toaster lying on its side, with clear-faced ramps at both ends and four fat black wheels tucked into side notches in the middle. Everything is flat-faced and straight-edged; there are no fillets larger than about 1 mm, no curves except the wheels, and no visible text or logo [seen].

### Plan outline (top view), one quarter, x >= 0 and y >= 0 from the centre

Walk anticlockwise from the centre line. The other three quarters are mirror images [inferred from symmetry].

| Point | x | y (from mid) | Meaning |
|---|---|---|---|
| P0 | 0 | 0 | centre |
| P1 | 39 | 0 | centre-section side wall (waist) |
| P2 | 39 | 34.5 | end of the wheel notch; the notch is about 69 mm long in total |
| P3 | 52 | 34.5 | end block inner (wheel-facing) corner |
| P4 | 52 | 39 | start of the arrow chamfer |
| P5 | 36 | 48 | tip corner |
| P6 | 0 | 48 | tip centre |

Ratios that drive the look:
- Waist width / max width is about 0.75 [seen aws68: lid width vs end-block width].
- Tip edge width / max width is about 0.65-0.7 [seen aws68].
- End-block plan depth (P3 to P6) / total length is about 0.14 each. The two wheel pairs fill the centre section.

### Side profile (looking along x), y >= 0 half

| Point | y (from mid) | z | Meaning |
|---|---|---|---|
| S0 | 0 | -12 | belly |
| S1 | 48 | -12 | tip bottom |
| S2 | 48 | -10.5 | tip lip (1.5 mm thick nose) |
| S3 | 31 | 16 | top edge of the ramp |
| S4 | 0 | 16 | flat top |

Ramp angle is about 55 deg from the floor [estimate: aws71 shows the blue cheek triangle about as tall as it is long, slightly taller]. The ramp is a single flat plane, with no curve, step or second facet [seen in aws71 and aws74, where the clear skin reflects as one flat plane].

### Front view (looking along y)

Seen from either end, the robot is a wide trapezoid (the end block):
- Its bottom tip edge is about 72 mm wide.
- Its widest part is about 104 mm, at the inner corners.
- Its top band is level with the lid.

Behind it, the tyres just show over the top at the sides [seen aws68]. The centre section is hidden behind the end block in this view.

---

## 3. Part-by-part description

### 3.1 Chassis / main body (one print)

- **Material/colour.** Blue FDM print [seen]. True colour in aws74 is a medium "process blue", about #1f86d8 to #2f8fe0. Matte, with layer lines visible as horizontal stripes on the cheek faces in aws74 (lower right of the front block) [seen], so it was printed lying flat (z-up) [inferred]. aws74 shows small scuffs, white scratches and a few chips on the top [seen]. The material is probably PLA or PETG; at this colour and finish it is hard to tell from nylon [guess].
- **Construction.** A single monolithic print that includes both end blocks [inferred: no seam is visible between the centre section and the end blocks in any photo. In aws74 the top surface runs continuously from the front ramp edge to the rear end].
- **Centre section.** A rectangular box about 78 mm wide (x ±39), about 69 mm long between the end blocks, and about 28 mm tall [estimate].
  - Its two long side walls are vertical and form the inner faces of the wheel notches [seen in aws74: a blue vertical wall is visible behind and between the two near tyres].
  - The wall is pierced only by the motor shafts [inferred].
  - The wall's outer surface is flat. No screws, vents or holes are visible on it [seen aws74, the only photo where a side wall shows between the tyres].
- **Wheel notches.** One notch on each side. It is open to the side, to the floor and upward [seen in aws68 and aws74: the tyre tops are visible from above]. The end blocks close it at its front and rear [seen].
  - Notch length is about 69 mm, holding 2 tyres of 28-30 mm plus a 3-5 mm gap between them and 1-3 mm at each end [estimate].
  - Notch depth (inward from the end-block outside face) is about 13 mm, which is the tyre width (about 12 mm) plus about 1 mm side clearance [estimate].
- **End blocks (2, identical).** Each one spans the full width (x ±52) [seen in aws68: the end block's outer corners reach the outside of the tyres; in aws74 the near cheek at about (900,700) is in line with the outside face of the near front tyre].
  - **Inner face** (towards the wheels): vertical and flat. It faces the tyre tread with about 1-3 mm of gap [seen aws74: the tyre almost touches the cheek's rear face]. This face is the full body height, from the belly to the top band.
  - **Top face:** a narrow flat band, 3-5 mm deep (along y), level with the top plate, then the ramp starts [seen aws74: a thin blue strip runs along the top of the clear ramp skin].
  - **Ramp face:** one inclined plane, about 55 deg, from the top band down to a sharp lip 1-2 mm above or touching the floor [seen aws71: the lower edge of the clear skin meets the floor line].
  - **Cheeks:** the two side faces of each end block. Each is triangular in side view, with a vertical rear edge (against the wheel notch), the floor edge, and the ramp edge [seen aws71: the blue triangle left of the clear skin]. In plan each cheek has the arrow chamfer: from the inner corner it runs straight for about 4-5 mm, then angles inward at about 30 deg off the length axis to the tip corner [seen aws68: angled faces at both ends of the front block; aws74: the angled near cheek of the rear block at the image's upper right]. The chamfer face is vertical, not sloped [seen aws68: the chamfer edges are vertical lines in the near end-on view].
  - **Ramp skin:** the ramp face is covered by a clear sheet (see 3.3).
- **Belly.** Not visible in any photo [guess: flat and closed, with an access slot or hole for the switch on the earlier versions; about 1.5-2 mm skin].
- **Ground clearance.** About 2 mm between the belly and the floor at the centre (chassis bottom at z = -12, tyres at z = -14) [estimate: aws68 shows a thin dark gap under the front block]. The ramp lips sit at about 0-1.5 mm, closer to the floor than the belly, because the lip is the lowest point of the body [inferred].
- **Internal hollowing.** Not visible [guess: pockets for the four motors, battery and receiver, walls about 1.5-2 mm; the CAD uses a 1.6 mm shell]. For an antweight to stay under 150 g at this size, the body must be largely hollow [inferred].

### 3.2 Top plate (lid)

- **Shape.** A flat rectangular plate that covers the centre section. Its long edges are flush with the centre-section side walls (x ±37.5 to ±39) and its short edges stop at the end blocks' top bands [seen aws68: a lighter rectangular panel bounded by visible edge lines; it is inset slightly from the end blocks]. The corners are square or have a very small radius [seen aws68].
- **Size.** About 75 x 64 mm, about 2-3 mm thick [estimate: aws68 shows a visible edge step of about 1-2 mm at the lid's front edge].
- **Colour.** The same blue, but in aws68 it reads lighter (pale sky blue, about #6cb4ec) than the end blocks [seen aws68: probably a different print or filament batch, or a lighter top skin]. In aws74 the lid and body look the same colour [seen].
- **Flush/inset.** The lid's top is flush with the end-block tops within about 1 mm [seen aws74: no step is visible along the front edge; aws68 shows a faint step].
- **Fastening.**
  - aws68 and aws71: 4 screws, one near each corner, about 4-5 mm in from each edge [seen]. They are pan or button heads, silver in aws68 and dark in aws71 (colour cast).
  - aws74: about 11 screws [seen]:
    - Along the far long edge (robot's right in aws74), 3 black Phillips pan heads, evenly spaced over the front half to centre: about 12-15 mm apart, about 4 mm from the edge.
    - Near the front edge, 1 black and 2 silver Phillips pan heads. The 2 silver ones are either side of the switch slot.
    - Along the near long edge (robot's left), 4 heads: 2 black, 1 large silver pan head with a raised domed washer or countersink ring (centre of the near edge), and 1 black near the rear.
    - Near the rear right corner, 1 black head.
  - The irregular pattern shows that screws were added during repairs [inferred]. Screw size is about M2-M2.5 self-tappers into the printed body [inferred: there are no nuts on the top surface; heads about 4 mm across, which is 0.13-0.15 of the tyre diameter].
  - The screw heads stand about 1-1.5 mm proud of the lid; they are not countersunk, except possibly the large silver one [seen aws74: small shadows beside each head].
- **Switch slot (aws74 only).** A small rectangular through-slot, about 6 x 2.5 mm [estimate], on the centreline about 10-12 mm behind the front ramp's top edge, long axis along x [seen at about (430,315) in aws74]. A dark switch lever or a removable link shows in the slot [seen: a dark tab]. This is the only external feature that tells front from back [seen].
- **Markings (aws74).** A white-marker hand-drawn circle or loop (about 15 mm across) near the rear right quadrant [seen], plus scratches. These are cosmetic and need not be modelled.

### 3.3 Ramp skins (2, one per end)

- **Material.** Clear polycarbonate sheet or very thick clear packing tape. In aws71 and aws74 it is translucent with scratches and a frosted, scuffed texture; the blue body shows through [seen]. In aws68 it is opaque white/cream masking tape or gaffer tape with a torn patch at the right end [seen].
- **Coverage.** It covers the ramp face across almost the full tip width. It stops about 3-5 mm short of each cheek [seen aws71: the blue cheek triangle is uncovered; aws74: blue cheek visible at the near end].
  - Upper edge: about 2-4 mm below the ramp's top edge, leaving a thin blue band [seen aws74].
  - Lower edge: at or slightly beyond the blue lip, forming the actual leading edge [seen aws71: the clear edge reaches the floor and looks slightly proud of the blue].
  - In aws68 the tape is narrower: about 60% of the block width, centred, and about 15 mm tall along the slope [seen].
- **Thickness.** About 0.5-1.5 mm [estimate: the edges are visible as bright lines in aws74, with a slight thickness at the near end at about (700,670)].
- **Fastening.** Probably double-sided tape or glue, or wrapped tape [guess: no screws are visible on the skin in any photo].
- **Function.** A slippery, hard leading surface. It lets the ramp edge get under opponents and spreads impact [inferred].
- **Position relative to other parts.** It lies on the ramp face of the end block, between the two cheeks, below the top band and the top plate's short edge. It is about 30-35 mm in front of the nearest tyre tread, measured along the floor [estimate]. It never touches the wheels or the lid.

### 3.4 Wheels (4), tyres and hubs

- **Layout.** Two wheels per side in the side notches, side by side along y, centred on the robot's length midpoint [seen aws74 and aws71: both wheel pairs sit in the middle; the end blocks are equal].
- **Spacing.**
  - Axle centres are about 32-34 mm apart along y [estimate: tyre-to-tyre gap of about 3-5 mm in aws74 and aws68].
  - Axles are at about y = ±16 to ±17 from the middle. (The CAD keeps the internal motor layout at ±19, giving a 10 mm gap, which is a known difference.)
  - Left and right wheels are on the same axle lines: the four axles form a rectangle, not a staggered pattern [seen aws68].
- **Tyres.**
  - Black rubber or foam, about 28-30 mm outside diameter and about 12 mm wide [estimate: width/diameter is about 0.4 in aws74].
  - Square shoulders, flat tread with no visible tread pattern, slightly worn and dusty grey on the tread [seen aws74].
  - Tyre wall thickness (radial) is about 4-5 mm, i.e. hub rim diameter / tyre diameter is about 0.68 [seen aws74: the red hub fills about 2/3 of the face].
- **Hubs.**
  - Red plastic (true colour about #c8303a, slightly pink-red) [seen aws74; aws68 shows red rims].
  - Three curved spokes in a "triskelion" pattern; the spokes curve the same way [seen aws74], with an outer rim flush with the tyre's outer face. Spoke width is about 2-3 mm; the openings between spokes are dark (they show the shadowed hub interior) [seen].
  - Central boss about 6 mm across [estimate], with a small metal (silver/grey) centre that is the motor shaft end or a grub-screw insert [seen aws74: a small light dot with a hexagonal look at each hub centre].
  - The spokes are recessed about 1-2 mm behind the rim face [seen: shadowed].
  - These look like the generic red "N20 3-spoke 30 mm" hobby wheels [guess].
- **Outboard faces.** The hub face points outward; no outer bearing, axle nut or guard is visible [seen]. The wheel is cantilevered on the motor shaft [inferred].
- **Height.** Tyre top is about z = +14 to +15, about flush with the top plate (z = +16) [seen aws68, aws74]. Tyre bottom is the lowest point of the robot (z = -14).
- **Lateral position.**
  - The tyre's outer face is at about x = ±51 to ±52, flush with or 0-1 mm inboard of the end block's widest point [seen aws68: the end block corners line up with the tyre sides].
  - The inner face of the tyre is about 0.5-1 mm from the centre-section side wall at x = ±39 [estimate]. The red hub is outermost.
- **Wheel guards.** None as separate parts [seen]. The end blocks act as guards: they cover the front and rear of each wheel pair over the full height except the top 2-3 mm [seen aws74, aws68]. Nothing covers the wheels from above or outside.

### 3.5 Drive motors (4), internal, not visible

- They are probably N20 micro-gearmotors (12 x 10 x 25 mm gearbox + motor), one per wheel [guess: the standard choice for 150 g antweights and the usual mate for the red N20 wheels].
- They lie along x, shafts outward through the centre-section side walls at axle height (z = 0) [inferred from the wheel position].
- Held by printed pockets in the body (press fit, clamped by the lid) [guess: no external motor clamps or screws are visible on the side walls in aws74].
- Front and rear motors on each side are about 32-34 mm apart (centres). The two motors on one side sit in front of each other, and the two sides' motors sit back to back near the centreline: their inner ends are about 10-15 mm apart across x = 0 [inferred].

### 3.6 Electronics, internal, not visible

- **Battery.** 2S LiPo, about 150-300 mAh, about 30 x 20 x 12 mm [guess], lying flat in the middle of the centre section between the motor rows.
- **Receiver/ESC.** A combined 4-channel antweight board (e.g. Malenki Nano or a DasMikro-style board) [guess], flat under the lid.
- **Power switch / link.**
  - In aws74 it is under the slot near the front edge of the lid [seen slot].
  - In older versions it may have been reached from below [guess].
- **Wires.** No wires are visible in any photo [seen: nothing protrudes]. Internally there are the battery to switch to ESC leads (22 AWG) and four motor pairs (26 AWG), each routed in the cavity from the ESC to the inner ends of the motors [guess]. The front and rear motors on the same side are probably wired in parallel to one ESC channel (tank steer) [guess].
- **Antenna.** Not visible [guess: internal].

### 3.7 Screws and fasteners (visible)

| Type | Count (aws74) | Head | Colour | Where | Into |
|---|---|---|---|---|---|
| Phillips pan/button self-tapper, about M2 | about 8 | about 4 mm round, low dome | black (oxide) | lid edges | printed body bosses [inferred] |
| Phillips pan, about M2 | 2 | about 4 mm | silver (zinc) | either side of the switch slot | body |
| Phillips pan with domed washer/cup | 1 | about 5-6 mm incl. washer | silver, with a lighter blue ring around it (filled countersink or scuff) | middle of the near (left) long edge | body |
| Corner screws (aws68/71) | 4 | about 4 mm | silver (aws68) | lid corners, about 4 mm from the edges | body |

No screws are visible on the end blocks, the cheeks, the ramp skins or the side walls [seen].

---

## 4. Per-view descriptions

### 4.1 aws68: end view (front), low and slightly left

- **Foreground (bottom 40% of image).** The front end block fills the width: a pale-blue trapezoid.
  - Its top edge is long and straight (the ramp top edge).
  - Its lower edge (tip) is slightly shorter.
  - Its two short side edges slope inward towards the bottom-front (the arrow chamfers). The left chamfer is visible from (15,235) to (45,330); the right one from (365,285) to (395,360).
  - A strip of white/cream tape (about 60% of the block width, centred, about 15 mm tall) is stuck on the ramp face, torn at the right end.
- **Middle.** The lid: a lighter-blue rectangle with 4 silver screws at its corners. The front two are at about (130,230) and (320,268); the rear two at about (220,100) and (395,128).
- **Wheels.** The black tyres with red rims sit either side of the lid, two per side.
  - Left pair: tyre faces at about (60-130, 100-240).
  - Right pair: at about (360-500, 140-350).
  - The tyres' outer faces are about in line with the end block's widest corners. The two tyres on each side almost touch (gap of about 3-5 mm).
  - Only the red outer rim ring of each hub shows from this angle; the spokes face sideways [seen].
- **Far end.** The rear end block appears behind the lid (top of the image), with the same width and its own chamfered corners at the top left and top right. Its top edge is level with the lid.
- **What this view proves.**
  - Left-right symmetry.
  - The end blocks are wider than the centre section.
  - The arrow chamfers.
  - The wheels are in the middle, not at the ends.
  - The wheel tops are about level with the lid.

### 4.2 aws71: front-right three-quarter, colour-cast blue

- The front ramp runs diagonally from the image centre to the lower right. Its face is covered with a clear, scratched skin, with a blue lip/band above it at about (1500-1690, 210-290).
- The near cheek (robot's right front) is a blue triangle at about (630-790, 730-1080): vertical edge at the rear against the wheel, bottom edge on the floor, hypotenuse along the ramp. A thin dark line marks where the clear skin starts at about x = 780 [seen].
- The top surface is a large flat parallelogram, with 4 screws in a rectangle at about (655,200), (1220,155), (1200,400) and (530,470).
- The right-side wheels sit at the lower left: front wheel at about (400-700, 560-990), rear wheel at about (15-300, 370-760). The tyres look teal-black and the hubs dark blue (colour cast); 3 curved spokes are visible.
- The front tyre sits directly behind the cheek's vertical edge, with only a sliver of gap [seen at about (690,750)].
- Far-side wheels: only their tops peek out above the top surface at about (1000-1200, 20-120) and (1370-1610, 120-220), which shows the tyres reach about the same height as the top.
- The rear end block is not visible (hidden behind the near wheels at the left edge).

### 4.3 aws74: front-left three-quarter, true colour

- **Front end block.** Lower left. The ramp is covered by a clear skin from about (120,250) to (900,800). The blue top band and the end of the cheek are visible at the upper left (210-250, 200-240) and at the lower right (690-900, 560-810, the near cheek). The near cheek shows horizontal print lines.
- **Top surface.** Upper middle. About 11 screws, a switch slot at about (430,315), and a white marker circle at about (700-830, 110-190).
- **Near (left-side) wheels.** Lower right, red 3-spoke hubs: front wheel centre at about (975,650), rear wheel centre at about (1185,550). Their tyre treads almost touch each other.
  - The front tyre sits right behind the front block's vertical inner face.
  - The rear tyre sits just in front of the rear block, whose angled cheek and corner show at about (1200-1330, 340-600).
- **Far (right-side) wheels.** Upper left, behind the body: tops of two tyres with red hub rims at about (270-400, 140-210) and (440-610, 90-160).
- **Rear end block.** At the upper right, about (1200-1330, 330-600). Its top surface ends in a chamfered corner, and its outer cheek face is angled inward, confirming front-back symmetry.

---

## 5. Part table

| # | Part | Qty | Colour | Shape | Size (x * y * z), mm | Centre position (x, y, z) | Held by | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Chassis body incl. both end blocks | 1 | blue #2f8fe0 | two-way arrow prism with double ramps, wheel notches, hollow | 104 * 96 * 28 | (0, 0, +2) | - | seen |
| 2 | Top plate (lid) | 1 | blue, lighter in aws68 | flat plate | 75 * 64 * 2.5 | (0, 0, +14.75) | 4 (old) / about 11 (new) self-tap screws | seen |
| 3 | Front ramp skin | 1 | clear (white tape in aws68) | flat sheet on the ramp | about 70 wide * 32 along the slope * 1 | on the front ramp, centred x = 0 | adhesive/tape | seen; adhesive is a guess |
| 4 | Rear ramp skin | 1 | clear | as #3 | as #3 | on the rear ramp | adhesive/tape | inferred from symmetry (the rear ramp is not visible) |
| 5-8 | Tyres | 4 | black | cylinder ring | OD 28-30, ID about 20, W 12 | (±45.5, ±16..19, 0) | stretched over the hub | seen |
| 9-12 | Hubs | 4 | red #c8303a | 3-curved-spoke disc with rim | OD about 20, W about 10 | inside the tyres, face outward | pressed on the motor D-shaft | seen; fixing is inferred |
| 13-16 | Drive gearmotors | 4 | silver/black | N20 box + can | 12 * 34 * 10 (along x) | (±25, ±16..19, 0) | printed pocket press fit | guess |
| 17 | LiPo 2S | 1 | - | pouch | 30 * 20 * 12 | (0, about -7, -5) | pocket + velcro | guess |
| 18 | Receiver/ESC board | 1 | - | board | 28 * 21 * 6 | (0, about -2, +9) | pocket under the lid | guess |
| 19 | Power switch/link | 1 | black | slide switch or link | 12 * 4 * 6 | (0, about +25, +12), under the slot | pocket | slot seen, part is a guess |
| 20 | Lid screws | 4 to 11 | black / silver | M2 pan Phillips | head about 4 dia | lid edges (see 3.2) | threads into the body | seen |
| 21 | Wires | about 6 runs | red/black | 22/26 AWG | - | internal cavity | - | guess (none visible) |

There is **no** separate weapon, wheel guard, side armour, bracket, standoff, external motor mount or bumper [seen: none appear in any of the three photos].

---

## 6. Contact / gap matrix (outside parts)

"Touch" means a shared face; a number is a clear gap in mm (estimated). "-" means no relation (far apart). Where the robot is symmetric, one representative pair is given.

| | Body side wall (x = ±39) | End block inner face | End block top band | Lid | Ramp skin | Tyre (same side, other wheel) | Floor |
|---|---|---|---|---|---|---|---|
| **Tyre, front wheel** | 0.5-1 (tyre inner face to wall) | 1-3 (tread to the front block's inner face) | - | about 0-2 below the lid top level (no contact) | - | 3-5 (tread to tread) | touch (contact patch) |
| **Tyre, rear wheel** | 0.5-1 | 1-3 to the rear block | - | as above | - | 3-5 | touch |
| **Hub** | 1-2 (hub back to wall; motor shaft passes through) | - | - | - | - | - | - |
| **Lid** | sits on the top edge of the wall (touch, screwed) | butts against the end blocks' top band (touch or about 0.5) | flush, touch | - | 2-4 (lid edge to the top of the skin) | - | - |
| **Ramp skin** | - | - | 2-4 below the band | 2-4 | - | - | 0-1.5 at the lip |
| **End block lip** | - | - | - | - | covered by the skin | - | 0-1.5 |
| **Body belly** | - | - | - | - | - | - | about 2 clear |

Faces in contact:
- **Lid to body:** the lid's underside lies on the top edges of the centre-section walls and on internal bosses [inferred], clamped by screws from above.
- **Ramp skin to body:** the skin's underside is bonded to the ramp face of the end block.
- **Tyre to hub:** the tyre's bore is stretched onto the hub rim's outer cylinder; the hub's outer face is flush with the tyre's outer face.
- **Hub to motor:** the hub's central bore takes the motor's D-shaft; the shaft end shows at the hub centre [seen as a silver dot].
- **Motor to body:** the gearbox sits in a pocket on the inside of the side wall; the shaft passes through a hole about 4 mm across in the wall [inferred].

---

## 7. Mechanism and function

- **Drive.** Four-wheel direct drive, skid steer: left pair and right pair [inferred]. Because the wheels sit at mid-length and are not much taller than the body, the robot cannot drive inverted unless the tyres stand proud of the lid. They roughly do (flush within about 1-2 mm), so inverted driving is marginal [inferred].
- **Weapon.** Passive double wedge. Either ramp gets under an opponent and lifts it as the robot pushes. The clear hard skin gives a low-friction, hard-wearing leading edge. Because the robot is symmetric there is no "back" to attack, so the driver never needs to turn round [inferred].
- **Protection.** The end blocks shield the wheel pairs from front and rear hits. The tyres are exposed only from the sides (the waist) and from above [seen]. The arrow chamfers deflect glancing side hits off the corners [inferred].
- **Serviceability.** Removing the lid (4 or about 11 screws) exposes everything. The switch is reachable through the lid slot (aws74) [seen slot].

---

## 8. Rebuild recipe (text only)

1. Draw the plan quarter P0-P6 (section 2). Mirror it in x, then mirror the half in y to get the closed two-way arrow outline.
2. Draw the side-profile half S0-S4. Mirror it in y. Extrude it across x wider than the plan (±53).
3. Intersect the plan extrusion with the profile extrusion to get the outer body. Hollow it to a 1.6-2 mm shell, keeping solid pockets for the motors.
4. Cut the top recess 75 x 64 x 2.5 at the centre top and fill it with the lid part (same blue). Add four corner M2 pan-head screws 4 mm from the lid corners for the aws68/71 look. For aws74, add three more screws along each long edge and two silver screws beside a 6 x 2.5 mm slot on the centreline about 11 mm behind one ramp top edge.
5. Place four wheels, OD 28-30 x 12, at x = ±45.5 and y = ±16..19, with axle z = 0. Make black tyres with red three-curved-spoke hubs facing outward and a silver dot at each hub centre.
6. Lay a 1 mm clear sheet on each ramp face, inset about 4 mm from each cheek and 3 mm below the top band, with its lower edge at the lip.
7. Colours: body #2f8fe0, lid slightly lighter, tyres #1a1a1a, hubs #c8303a, screws black or silver, skins clear/white with about 40% opacity.

---

## 9. Size ratios (measured from the photos, independent of the absolute scale)

| Ratio | Value | Photo |
|---|---|---|
| Overall width / overall length | 1.0-1.08 | aws68 + aws74 |
| Waist (centre-section) width / overall width | about 0.75 | aws68 |
| Tip edge width / overall width | about 0.65-0.7 | aws68 |
| Body height / tyre diameter | about 0.95-1.0 | aws74 |
| Tyre width / tyre diameter | about 0.4 | aws74 |
| Hub rim diameter / tyre diameter | about 0.68 | aws74 |
| Tyre gap / tyre diameter | about 0.1-0.15 | aws74, aws68 |
| End-block plan depth / overall length | about 0.14 per end | aws74 |
| Ramp run / ramp rise | about 0.65-0.75 (angle about 55 deg) | aws71 |
| Lid length / overall length | about 0.65 | aws68, aws71 |
| Screw head / tyre diameter | about 0.13-0.15 | aws74 |
| Switch slot length / lid width | about 0.08 | aws74 |

---

## 10. Uncertainties and open questions

- The absolute scale rests on the 28 mm tyre assumption. If the tyres are 30-32 mm, everything grows by 7-14%. The 150 mm floor-square rule would still be met.
- The rear ramp skin is never directly visible. It is assumed to be the same as the front because the ramp shape is symmetric and the robot is meant to drive either way.
- The belly is never visible. Its features (switch access, vents, skid pads) are unknown.
- The ramp angle is estimated from oblique views. It could be anywhere from 50 to 60 deg.
- The lid may be a separate print or a top layer of the body; the visible edge line in aws68 and the screws argue for a separate plate.

---

## 11. Differences between the current CAD (commit on `ref/look_what_you_ve_done_to_our_b`) and the photos

- The wheel pairs are at y = -28 and +10 (midline -9, pitch 38 mm). The photos suggest a pitch of about 32-34 mm (tyre gap about 3-5 mm, the CAD has about 10 mm).
- The ramp skins are not modelled; the ramp is bare blue.
- Tyres render red and hubs pink in the CAD. The photos show black tyres with red hubs.
- The CAD has 4 lid screws (aws68/71 pattern) and no switch slot on top. aws74 has about 11 screws and a top slot.
- The end-block plan depth and ramp angle (55 deg) are tuned to the silhouettes: IoU 0.81 (aws71) and 0.83 (aws74).

---

## 12. Every part in all dimensions (mm guess for each)

The frame is the one defined at the top: origin at the robot centre (midway between the wheel pairs, on the centreline), at axle height. +x is right, +y is forward, +z is up, and the floor is z = -14. "v" means |y| from the centre.

### 12.1 Chassis body

| Feature | L (y) | W (x) | H (z) | Thickness | Radii | Angles |
|---|---|---|---|---|---|---|
| Whole body | 96 | 104 (max, end blocks) / 78 (waist) | 28 (z -12..+16) | shell 1.6-2 [guess] | outside edges sharp, r <= 1 (print) [seen: crisp edges] | - |
| Centre section | 69 (v <= 34.5) | 78 | 28 | side wall about 2-5 [guess] | inside notch corners r about 0.5 [guess] | walls 90 deg to the floor |
| End block (each) | 13.5 in plan (v 34.5..48) | 104 at v = 34.5..39, tapering to 72 at v = 48 | 28 at the inner face, falling to 1.5 at the lip | lip 1.5 thick | - | ramp 55 deg from the floor; chamfer 30.6 deg off the y axis in plan |
| Top band on the end block | 0-4 deep (v 31..35) | 104 | - | - | - | horizontal |
| Wheel notch (each side) | 69 | 13 deep (x 39..52) | open to the floor and the top | - | - | - |
| Motor shaft holes | - | - | - | through the 2-5 wall | r about 2 [guess] | axis along x, at z = 0, v = 19 |

### 12.2 Lid

L 64 (v ±32) * W 75 (x ±37.5) * H 2.5 (z 13.5..16). Corner radius about 0-1 [seen square]. Screw holes: 2.4 clearance dia, plus a counterbore 3.9 dia * 1.4 deep (CAD) [guess]. In aws74, the slot is 6 * 2.5 at (0, +21, 16) [estimate].

### 12.3 Ramp skin

About 70 wide (x ±35) * 32 along the slope (the ramp slope length is sqrt(17^2 + 26.5^2) = 31.5) * 1 thick. Corners square [seen aws74]. It lies in the ramp plane (12.6) offset 1 mm outward.

### 12.4 Tyre

OD 28 (r = 14), ID 20 (r = 10), width 12. Shoulder radius about 1 [guess]. Axis along x at (±45.5, ±19 CAD / ±16.5 photo, 0). Tyre x-span: 39.5..51.5.

### 12.5 Hub

- Rim: OD 20, ID 17 (rim thickness 1.5), width 10.
- Boss: dia 6, length 8.
- Spokes: 3, about 2.5 wide, 2 thick, recessed 1.5 behind the rim face.
- Bore: D-shaft, 3 mm with a 2.5 flat [guess].

### 12.6 N20 motor [guess]

Gearbox 12 W * 10 H * 9 L, can 12 dia (with 10 flats) * 15 L, shaft 3 dia * 10 L, total about 34 along x. Centre at x = ±25. The shaft tip is at x = ±42.5, inside the hub.

### 12.7 Screws

M2: head dia 3.8-4, head height 1.3-1.6, length 8 (grip about 2.5, thread about 5.5 into the body) [guess].

### 12.8 Battery, ESC, switch [guess]

- Battery: 30 * 20 * 12 pouch with r 1 edges.
- ESC: 28 * 21 * 6.
- Switch: 12 * 4 * 6 body with a 2 * 2 * 3 lever.

---

## 13. Curves and planes as maths (in the frame above)

- **Tyre outer surface:** (y - yw)^2 + z^2 = 14^2 for |x| in [39.5, 51.5], with yw in {-28, +10} (CAD) or {±16.5} (photo). Inner bore: (y - yw)^2 + z^2 = 10^2.
- **Hub rim:** (y - yw)^2 + z^2 = 10^2 (outer) and 8.5^2 (inner).
- **Hub spokes (triskelion):** each spoke centreline is a circular arc in the hub face plane. In local polar coordinates (r, theta) about the axle, the arc runs from (r = 3, theta_k) to (r = 8.5, theta_k + 40 deg), for k = 0, 1, 2 with theta_k = 0, 120, 240 deg. Equivalently, in cartesian coordinates it is an arc of radius about 7 centred at r = 6, theta = theta_k - 70 deg [estimate from aws74]. All three curve the same way (clockwise, seen from outside on the left side) [seen].
- **Ramp plane (front end, v >= 0):** z = 16 - (26.5 / 17) * (v - 31) for v in [31, 48]. That is a slope of -1.559, which is 57.3 deg (photo estimate 50-60 deg, reconciled to 55-57 deg). At the lip, v = 48 gives z = -10.5. The rear ramp is the same with v = -y.
- **Arrow chamfer (plan, quadrant x >= 0, v >= 0):** x = 52 - (16 / 9) * (v - 39) for v in [39, 48], so from (52, 39) to (36, 48). Its angle off the y axis is atan(16 / 9) = 60.6 deg, so the chamfer face makes 29.4 deg with the x axis (the tip edge).
  - Correction to 12.1: the "30.6 deg off the y axis" there should read about 60 deg off the y axis, or about 30 deg off the tip line. The visual impression in aws68 is a shallow bevel, which agrees with the tip-line value.
- **Cheek triangle (side view, x = ±52 face, then chamfered):** its vertices are (v, z) = (34.5, -12), (34.5, 16 - 1.559 * 3.5 = 10.5), and the lip (48, -10.5).
  - Because the ramp starts at v = 31 but the wing starts at v = 34.5, the cheek's vertical inner edge is 22.5 tall (-12..10.5), not 28.
  - The top band at full width exists only over the waist (x <= 39).
- **Lid outline:** the rectangle |x| <= 37.5, |y - y0| <= 32, z in [13.5, 16].
- **Tip edge:** the line y = y0 ± 48, z = -10.5, |x| <= 36.

---

## 14. The same quantities described independently (dimension / ratio / pixels / coordinates)

| Quantity | By dimension guess | By ratio to the tyre (D = 28) | By photo pixels | By coordinates (CAD) | Reconciled |
|---|---|---|---|---|---|
| Overall length | 96-100 | 3.4-3.6 D | aws74: about 830 px along the length vs a tyre height of about 210 px gives 3.9 D, but the length is foreshortened about 0.85, so about 3.4 D | y -57..39, i.e. 96 | 96 |
| Overall width | 104 | 3.7 D | aws68: end block about 380 px vs tyre width about 70 px (12 mm), giving 65 mm? (see the conflict list) | x ±52 | 104 |
| Body height | 28 | 1.0 D | aws71: cheek vertical edge about 310 px vs tyre diameter about 330 px gives 0.94 D | z -12..16 | 28 |
| Tyre gap | 3-5 | 0.1-0.15 D | aws74: about 20 px vs tyre dia about 210 px gives 0.1 D, so 2.8 mm | 10 (CAD) | 3-5 photo; CAD 10 (known difference) |
| Ramp angle | 55 | - | aws71: cheek edges about 310 px tall * 170 px deep gives 61 deg (perspective) | atan(26.5 / 17) = 57.3 | 55-57 |
| End-block plan depth | 13.5 | 0.48 D | aws74: front cheek about 200 px deep vs tyre about 210 px gives about 1 D (includes the slope) | v 34.5..48 | 13.5 at the floor, plus 3.5 of top band |
| Lid size | 75 * 64 | 2.7 D * 2.3 D | aws71: screw rectangle about 690 * 300 px | x ±37.5, v ±32 | 75 * 64 |
| Screw head | 4 | 0.14 D | aws74: about 25 px vs tyre about 210 px gives 0.12 D, so 3.3 mm | M2 button 3.5 | 3.5-4 |
| Hub rim / tyre | 20 / 28 | 0.71 | aws74: about 140 / 205 px gives 0.68 | - | 0.68-0.71 |

---

## 15. Consistency check (conflicts and reconciled values)

1. **Overall width from aws68 pixels (about 65 mm) vs ratios (104 mm).**
   - Cause: in aws68, the "tyre width about 70 px" used for scale was measured on the far tyre, which is foreshortened. Measured on the near tyre face (about 100 px), the width comes out at about 95-104 mm.
   - Reconciled: 104 mm (x ±52), which also matches the tyre outer faces at ±51.5.
2. **Ramp angle: 61 deg (aws71 pixels) vs 55 deg (eye estimate) vs 57.3 deg (CAD).**
   - Cause: perspective in aws71 exaggerates the vertical.
   - Reconciled: 55-57 deg; the CAD keeps 57.3.
3. **Chamfer angle wording.**
   - Section 3.1 says the chamfer is about 30 deg "off the length axis"; the maths in section 13 gives 60.6 deg off the y axis (29.4 deg off the tip line).
   - The photos (aws68) show a shallow corner bevel, about 30 deg off the tip line.
   - Reconciled: 29-31 deg relative to the tip edge. The wording in 3.1 should read "angles inward at about 30 deg relative to the tip edge".
4. **Tyre gap: photo 3-5 mm vs CAD 10 mm.**
   - Unresolved in the CAD on purpose: the internal motor/battery layout is fixed at y = -28 and +10.
   - Photo value: 3-5 mm.
5. **Tyre top vs lid: flush (aws68, aws74) vs proud (aws71).**
   - aws71 is shot from lower on the wheel side, so the far tyre tops appear above the lid edge.
   - Reconciled: tyre top z = +14, lid top z = +16, so the tyre is 2 mm below the lid. A flush look in photos at about 1-2 mm is consistent.
6. **Lid screw count: 4 (aws68, aws71) vs about 11 (aws74).**
   - These are different versions, not a conflict. The CAD models 4.
7. **Ramp covering: white tape (aws68) vs clear (aws71, aws74).**
   - Different versions. The latest is clear.
8. **Body length: 3.4-3.6 D vs CAD 96 / 28 = 3.43 D.**
   - These agree.
9. **End-block plan depth: about 1 D (aws74 pixels) vs 13.5 mm (0.48 D, CAD).**
   - The pixel figure includes the sloped ramp and the top band seen at an angle. The floor-level depth of the block beyond the wheel notch is about 13.5 mm, and the ramp's top edge is at v = 31, so the ramp spans 17 mm of plan depth (about 0.6 D).
   - Reconciled: ramp plan run 17, block beyond the notch 13.5.
10. **Body height vs wheel height: body 28 tall from z = -12, tyre 28 tall from z = -14.**
    - The body sits 2 mm higher than the tyres (ground clearance), so its top is 2 mm above the tyre tops.
    - This is consistent with conflict 5.

---

## 16. Why the designer did it (per part, several angles)

### 16.1 Two-way arrow body (double wedge, front-back symmetric)

- **Fight.**
  - The robot has no back: whichever end faces the opponent is a wedge, so it never needs to turn round. That saves time against spinners and pushers.
  - A wedge at each end also means there is no weak flat rear to get pushed or lifted from.
  - The plan chamfers deflect hits off the corners, and they stop the corners catching on arena walls and opponents' forks.
- **Construction.**
  - One print with no supports, printed flat: the ramps are 55 deg overhangs facing up, so they need no support.
  - Symmetric CAD: the designer can draw one quarter and mirror it.
  - One part means no joints to fail between the body and the wedges.
- **Weight.** End blocks of shell construction give a long, low wedge for a few grams.
- **Rules.** About 104 * 96 mm fits easily in the AWS 150 mm floor square; the designer used a compact size, probably from the older 4 in (101.6 mm) cube rule [inferred: the robot predates AWS 2025].

### 16.2 Narrow waist with wheel notches

- **Fight.**
  - The wheels are inside the robot's outline (the end blocks are as wide as the tyres), so front and rear hits land on the body, not the tyres.
  - The tyres still touch the side walls of the arena for wall-riding [guess].
- **Construction.**
  - The motors fit straight into the side walls, and the hub sits just outside the wall, so short motor shafts are enough. No outboard bearings or axles are needed.
  - Wheels can be swapped from the side without opening the robot [inferred].

### 16.3 Ramp angle about 55 deg and a sharp lip

- **Fight.** A steep ramp is strong, being short in plan, and still gets under robots that have a ground-scraping front. The sharp 1.5 mm lip is the scoop edge.
- **Construction.** 55 deg prints cleanly without support. The 1.5 mm printed lip is fragile, which is why it is covered by a ramp skin (16.4).

### 16.4 Clear polycarbonate (earlier: tape) ramp skin

- **Fight.** A hard, slick, replaceable leading edge. Polycarbonate does not chip like PLA, and it glides under opponents.
- **Repair/cost.** It is cheap and easy to replace between fights. In aws68 tape was used before the designer upgraded to polycarbonate [inferred from the photo history].
- **Weight.** About 1-2 g per skin.

### 16.5 Separate lid with screws

- **Construction / repair.** It gives access to all the electronics. The lid is a flat print, which is fast and supportless.
- The screw count rose from 4 to about 11 [seen]. The lid probably flexed or popped off under hits, so the designer added screws along the edges [inferred]. The mixed black and silver screws show repairs with whatever was in the pit box [inferred].
- **Weight.** A 2.5 mm lid of about 8-9 g is the main top armour.

### 16.6 Switch slot in the lid (aws74)

- **Rules.** AWS needs a power switch or link that can be reached without tools. A slot on top, near one end, lets a key or pen work the switch while the robot is on the arena floor [inferred].
- **Construction.** The switch sits in its own pocket, so the slot is the only opening in the lid.

### 16.7 Four-wheel drive with direct N20s

- **Fight.** All four wheels grip, which gives more pushing power. Losing one wheel still leaves drive on that side.
- **Construction.** N20s are cheap and light (about 10 g each), and the hub presses directly on the motor shaft. The wheel spacing is set by the length of the motors: the motors sit side by side along y, and each pair of wheels sits close together.
- **Cost.** These are generic hobby parts [guess].

### 16.8 Red 3-spoke hubs and black tyres

- **Construction.** Off-the-shelf N20 wheels with a D-bore. No printing, true running, and grippy rubber tyres [guess].
- **Fight.** A diameter of about the body height lets the robot run almost invertible.

### 16.9 Blue PLA/PETG print colour

- This is the designer's look. A bright colour helps the driver see the robot's orientation in the arena; for this symmetric robot the slot and screw pattern are the only orientation cues [inferred].

---

## 17. Unseen and inner parts (guesses, with confidence)

Confidence levels:
- **high:** almost certainly so for a robot like this.
- **med:** likely.
- **low:** a plausible guess.

Positions are in the frame at the top, with the CAD y0 = -9 as the centre. Photo-true positions would be centred on y = 0.

| Part | Size guess | Position guess | How held | Confidence | Why |
|---|---|---|---|---|---|
| Drive gearmotors (4) | N20 12 * 10 * 34 | axles at z = 0, v = 16-19; bodies across x 6..39 from each side | pressed into printed pockets in the side wall, clamped by the lid | high (type), med (fit) | wheel and hub style is N20 |
| Motor shafts | 3 dia D, 10 long, protruding about 4 past the wall | x ±39..43 | part of the motor | high | hub centre shows a metal dot |
| Bearings / outboard axles | none | - | - | high (none) | no outer support is visible; wheels are cantilevered |
| Battery | 2S LiPo 180-300 mAh, 30 * 20 * 12, 12-18 g | centre, between the motor rows, low (z -11..+1) | pocket + velcro or foam | med | standard for 150 g ants; the low battery keeps the centre of gravity low |
| Receiver + ESC | combined board (Malenki Nano class), 28 * 21 * 6, 3.5 g | above the battery under the lid (z +6..+12) | pocket, foam | med | the usual combined board; no separate ESC heat sinks are visible |
| Separate receiver | none (combined) | - | - | med | - |
| Power switch | slide switch 12 * 4 * 6, or a removable link | under the lid slot, v about 30 at the "front" end, z +8..+13 | pocket under the lid | med (aws74), low (older versions) | the slot is seen |
| Wiring path | battery to switch: 22 AWG, about 40 mm, along the centreline; switch to ESC about 30 mm; ESC to each motor 26 AWG, 30-50 mm, across the top of the motors to the inner motor terminals at x about ±6 | inside the cavity, over the motors | loose, taped | med | the shortest routes in a closed box |
| Lid screw bosses | dia 6, 8-9 tall, under each screw | (±33, ±30, 5-13.5) for the 4 corners; more along the edges in aws74 | part of the body print | med | self-tappers need about 6-8 mm of plastic |
| Internal ribs / walls | 1.5-2 thick walls between the motor pockets and the battery bay; a cross rib at the centre | x = ±6 and y = 0 | part of the print | low | stiffens the thin shell against wedge hits |
| Belly | 1.5-2 skin, flat, possibly with a switch access hole on older versions | z -12..-10 | part of the print | med | - |
| End-block interior | hollow, or 15-30% infill | v 34..48 | - | low | weight |
| Weight distribution | about 40% motors, 25% body, 12% battery, 15% wheels | - | - | med | typical |
| Antenna | about 30 mm wire coiled under the lid | near the ESC | taped | low | not visible outside |
| Fuses / LEDs | none or the ESC LED shows through the slot | - | - | low | - |

Total-mass check with these guesses:
- motors 4 * 9.7 = 39
- wheels + hubs 4 * 7.7 = 31
- battery 12.5
- ESC 3.5
- switch + wire 3
- screws 1-3
- body about 50
- lid about 8
- skins about 3

This sums to about 150 g, at the AWS 150 g limit, which supports the guessed hollow shell construction (med).

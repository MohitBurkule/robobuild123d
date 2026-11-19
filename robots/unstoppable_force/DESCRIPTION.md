# Unstoppable Force: full description of the reference photos

This file describes in text everything the three reference photos show, so the robot can be rebuilt without them.
Every measurement is estimated from the photos (no scale object is visible). Measurements are scaled from the body
width, which is taken as about 94 mm. **[G]** marks a guess or inference, meaning the photo does not show it directly.
Unmarked statements are things the photos show.

Frame used throughout (the same as the model): **+y = front** (the weapon end), **+x = robot's right**, **+z = up**,
z = 0 at the wheel axles, floor at z = -15.5 mm. "Near" and "far" are relative to the camera in each photo.

Photos:
- `reference/unstoppable_force.aws69.webp` (AWS 69). Drum version: plain silver drum, black tyres.
- `reference/unstoppable_force.aws71.webp` (AWS 71). Scoop or beater version: bent aluminium plate weapon with a
  window, salmon tyres.
- `reference/unstoppable_force.aws72.webp` (AWS 72). Taped weapon (pink and silver), salmon tyres.

All three are taken from the robot's **front-right, above** (camera azimuth about 120 deg from straight ahead,
elevation about 25-45 deg). The weapon is at the left of each picture, the robot's right side wall is the large near
face at the bottom of the picture, and the rear runs away to the upper right. The robot's left side wall is never seen
directly; it is taken to be a mirror of the right side **[G]**.

---

## 1. Summary

A small (150 g UK antweight) two-wheel-drive horizontal-axis weapon robot (a drum or beater). It has six main
assemblies:

1. **Tub (chassis).** A low, black, 3D-printed, open-top box. In plan it is a rectangle with large 45 deg chamfers at
   both rear corners. The front between the weapon arms is set back as a pocket for the weapon.
2. **Top plate (lid).** A flat black sheet over the whole tub, held by small screws round its edge. It has a
   rectangular notch over each wheel, a centred slide power switch and a small square window.
3. **Weapon arms (forks).** Two separate black printed plates, one at each front corner, standing upright. Seen from
   the side each is a stadium (rounded oblong), taller than the tub. They carry the weapon axle.
4. **Weapon.** A horizontal-axis rotor across the front between the arms: a cylindrical drum (AWS69), a bent aluminium
   scoop or beater plate (AWS71), or a taped drum or scoop (AWS72). A brushless outrunner at its right-hand end drives it.
5. **Drive.** Two wheels in wells inside the side walls, near the rear, each driven directly by a small gearmotor.
6. **Electronics** (hidden). Battery, receiver/ESC, weapon ESC, switch and wiring.

Overall it reads as a squat "dustpan": a flat, nearly square black slab with a rotor across the front between two
upright ears, and two wheels showing through slots near the back.

---

## 2. Overall dimensions and proportions

| Quantity | Estimate | Ratio to body width W (94 mm) | Basis |
|---|---|---|---|
| Body (tub) width, side wall to side wall | 94 mm | 1.00 | assumed scale |
| Body length, rear face to front face of the side walls | 68 mm | 0.72 | aws72 near side wall: about 0.7 of W |
| Overall length including the weapon | 100-105 mm | 1.07-1.12 | the weapon sticks out about 30 mm ahead of the walls |
| Body height, floor skin to top of the plate | 28-30 mm | 0.31 | aws69/aws72 near wall height |
| Ground clearance under the tub | 1-2 mm **[G]** | 0.02 | the wall nearly touches the floor in every photo |
| Arm height | 34-36 mm | 0.37 | the arms stand about 3 mm above the plate and reach down to about 1 mm off the floor |
| Arm length (front to back) | 20-24 mm | 0.23 | aws72 near arm |
| Arm thickness (x) | 7-9 mm | 0.08 | aws71 near arm edge |
| Weapon width between the arms | 66-72 mm | 0.72 | aws71 scoop, aws69 drum |
| Drum diameter (AWS69) | 24-27 mm | 0.27 | aws69 |
| Wheel diameter | 30-32 mm | 0.33 | the tyres just reach plate level |
| Wheel width | 9-10 mm | 0.10 | aws71/72 tyres |
| Wheel centre from the rear face | about 30 mm | 0.32 | wheel notch position |
| Rear chamfer legs | 12-14 mm each | 0.14 | aws69/aws72 near rear corner |
| Top plate thickness | 1.5 mm | 0.016 | its edge shows as a thin layer |

The robot is left-right symmetric except for the weapon drive: the motor sits at the right (+x) end of the weapon, and
the nyloc nut shows on the right arm only.

---

## 3. Per-view descriptions

### 3.1 AWS69 photo (front-right, high, about 45 deg)
- The **drum** fills the lower left of the picture: a silver cylinder (an aluminium tube, or silver tape over one),
  about 25 mm in diameter, its axis across the robot. Its surface is smooth with tape creases. No raised teeth are
  visible; any impact bars are hidden on the far side **[G]**.
- At the **near (right) end of the drum**, between the drum and the near arm, a ring of **copper and red** shows: the
  windings of an outrunner. So the brushless motor sits at the right end, inside or beside the drum, and the drum is
  the motor's bell or is fixed to it.
- **Near arm (right):** a black upright stadium at the front-right corner. Its rounded top stands slightly above the
  top plate. Its rear edge touches the front of the right side wall and the front-right corner of the top plate. A
  plate screw sits just behind it. The far arm (left) is the same, seen past the drum's far end at the left edge of
  the picture.
- **Front pocket:** behind the drum, between the arms, the top plate's front edge is cut back in a rectangle about
  40 mm wide and 15 mm deep, showing a dark rectangular cavity. The drum sits partly inside the body in this pocket.
  The pocket's back wall is vertical and black (the tub's front wall), and its side walls are the inner faces of the
  tub's front corners.
- **Top plate:** black and slightly textured. One dark tape patch covers its middle, and a small silver slide switch
  shows through a slot in the tape. There is a rectangular notch at the far wheel (top left) and at the near wheel
  (right). Screws: the front-left corner, the front-right corner (beside the arms), the front of each wheel notch, and
  one at the near rear corner of the notch. All are small (about 3 mm heads), black or dark, cross-head or hex **[G]**.
- **Wheels:** black rubber tyres on black hubs. The far one shows through the top-left notch and the near one through
  the bottom-right notch. Each sits inside a well whose outer face is the full-height side wall.
- **Near side wall:** a flat vertical black face from the near arm back to the rear chamfer. Two small dark holes,
  about 8-10 mm apart, sit at mid height near the front: the screws that hold the arm. A chamfer of about 12 mm takes
  off the rear-right corner.

### 3.2 AWS71 photo (front-right, low, about 25 deg)
- **Weapon:** a bent **aluminium plate scoop** instead of a drum. The sheet is about 1.5-2 mm thick, 65 mm wide and
  35 mm deep, bent along a line parallel to the axle. Its upper part wraps round or hangs from the axle; its lower
  part reaches forward and down to an edge about 2 mm off the floor, with the corners slightly turned up (a shallow
  curl). In its centre is a large **rounded-rectangle window** about 30 mm wide and 22 mm tall, with a corner radius
  of about 5 mm. Through the window a **black round bar** (about 6 mm in diameter and 35 mm long) runs across, parallel
  to the axle. **Two small coil springs and wire clips** hold its ends: a sprung striker or tensioner **[G]**. The
  metal is matt, with brushed lines along x.
- **Near arm (right):** a thick black stadium standing upright, about 22 mm long and 35 mm tall, rounded top and
  bottom. On its outer face, a little below centre, a **silver M5 flanged nyloc nut with a thin washer** sits on the
  end of the axle: the axle is a bolt or threaded rod clamped through the arm. Behind the arm, at the plate's
  front-right corner, is a cross-head screw.
- **Between the near arm and the scoop:** a **black ribbed cylinder** about 18-20 mm in diameter and 8-10 mm long,
  with fine grooves round it. This is the outrunner's black anodised bell, or a threaded black spacer **[G: motor
  bell]**. The scoop's right side plate is attached to it.
- **Far end:** a matching large black round boss or disc (about 25 mm in diameter) at the left arm, partly hidden:
  the far bearing housing or a second spacer **[G]**.
- **Top plate:** wide and flat. A **small square hole** (about 8 x 6 mm) sits a little forward of the centre, toward
  the left. The **slide switch** is in the centre on a strip of black tape, its lever moving along x. The notch over
  each wheel shows a salmon tyre. Screws: the front-left corner (beside the far arm), the front-right corner, and the
  rear corners at the notches.
- **Wheels:** rough salmon or coral-red tyres (foam or cast silicone, `#e07a6a`), about 9 mm wide, on black hubs. The
  far wheel is visible at the top left, the near wheel at the right.
- **Near side wall** (the large black face at the bottom right): one screw hole about 10 mm behind the arm at mid
  height, then a long flat face back to the rear chamfer.

### 3.3 AWS72 photo (front-right, about 25 deg)
- **Weapon:** taped pink and silver. It seems to be a **bent plate scoop like AWS71's**, folded into a shallow U and
  wrapped in tape, with a top roll (about 12 mm in diameter) at axle height and a flat apron going down and forward
  **[G: it could also be a small drum with a tape skirt]**. The left part shows a dark circular end: the far motor or
  bearing.
- **Near arm:** the same black stadium with the silver nyloc nut and washer. Here the nut is clearly in the arm's
  lower half, about 40 % up from the bottom. The arm's top is level with the top plate or just above it, and its
  bottom reaches below the tub's bottom edge, nearly to the floor.
- **Front pocket:** between the arms the tub's front wall is set back. A dark slot shows a black wire or bar running
  across inside it (a motor lead or a stiffening bar) **[G]**.
- **Top plate:** the same square window forward-left of the switch, and the switch with its silver tab and black
  lever. Screws sit at the front corners (just behind each arm), at the front of each wheel notch and at the rear
  corners. The plate's front-right corner is cut at about 45 deg where it meets the arm.
- **Near side wall:** one dark round screw head or hole at mid height about 15 mm behind the arm, and a second further
  back at the same height **[G]**. The rear chamfer shows clearly at the bottom right.
- **Wheels:** salmon tyres, the near wheel in its notch next to the chamfer.

---

## 4. Part-by-part description

### 4.1 Tub (chassis), 1 part
- **Material and colour:** black matt printed plastic (PLA, PETG or nylon), `#22262a`. The layer lines are horizontal,
  so it was printed flat with the open side up **[G: orientation]**.
- **Shape in plan:** an outline of about 94 x 68 mm. The front-left and front-right corners are square; the rear-left
  and rear-right corners are chamfered at 45 deg with legs of about 12 mm. The full-width front face exists only at the
  outer corners (|x| = 33 to 47) **[G]**; between them the front wall is set back about 12-15 mm, making the weapon
  pocket.
- **Height:** the tub walls are about 27 mm tall (underside of the floor skin to the wall top), and the plate on top
  brings the body to about 29 mm.
- **Walls:** about 2 mm thick **[G]**. Each side wall is one flat vertical face from the front corner to the rear
  chamfer, unbroken by the wheels. The wheels sit **inside** it, in wells, and the wall outboard of each wheel is the
  **wheel guard**. It is part of the same print as the tub. Its supports are the joins to the well's front wall and to
  the rear wall and chamfer, plus the floor strip under the ends of the well **[G]**.
- **Wheel wells:** a rectangular slot from the top (the notch in the plate) right through to the floor, since the
  wheel must touch the ground. About 12 mm wide in x and 34 mm long in y. The outer face is the side wall (guard),
  about 1.5 mm from the tyre. The inner face is a bulkhead about 1 mm from the hub. The wells start about 1 mm behind
  the depth of the front pocket and end about 13 mm in front of the rear face, just ahead of where the chamfer starts.
- **Front pocket for the weapon:** a box-shaped recess in the front of the tub, about 66-72 mm wide (between the arms)
  and 12-15 mm deep, open at the front and the top (the plate's front edge is cut back to match). The weapon sits in
  it with 1-2 mm clearance.
- **Holes:** two small screw holes about 10 mm apart in each side wall, near the front at mid height, for the arm
  screws (M2 or M3 **[G]**). Pilot holes in the wall tops take the lid screws.
- **Inside (not visible, [G]):** a floor about 1.5 mm thick; a motor cradle on each side between the wells; bays for
  the battery (rear), the receiver/ESC (front, behind the pocket) and the weapon ESC; corner columns under the lid screws.

### 4.2 Top plate (lid), 1 part
- **Material and colour:** black, a shade glossier than the tub, about `#2b3034`. Printed plastic, or 1-1.5 mm carbon
  fibre or G10 **[G]**.
- **Outline:** the tub's outline (rear chamfers the same), with:
  - a **rectangular notch over each wheel**, about 14 x 36 mm, open to the side edge, so the tyre shows from above and
    the plate never touches it;
  - the **front edge cut back between the arms** to the depth of the weapon pocket;
  - **front corners cut at 45 deg** where they meet the arms (aws72) **[G: small]**.
- **Openings:** a **switch slot** of about 8 x 4 mm in the centre, with the lever of a slide switch showing (silver
  tab, black lever). A **square window** of about 8 x 6 mm about 15 mm forward-left of the switch, for the receiver LED
  or bind button **[G: purpose]**.
- **Tape:** black electrical-tape patches over the middle: one large patch at aws69, two smaller ones either side of
  the switch at aws71 and aws72. They are not structural.
- **Fasteners: about 6 screws**, all small black button or cross-head screws (M2 **[G]**), seated flush or 1 mm proud
  and screwed into the tub wall tops or columns:
  1. the front-left corner, right behind the left arm;
  2. the front-right corner, right behind the right arm;
  3. the front inner corner of the left wheel notch;
  4. the front inner corner of the right wheel notch;
  5. rear left, near the start of the chamfer (behind the left notch);
  6. rear right, near the start of the chamfer (behind the right notch).

### 4.3 Weapon arms, 2 parts (mirror pair)
- **Material and colour:** black printed plastic like the tub, thick and solid.
- **Shape:** seen from the side, an upright **stadium** (a rectangle with semicircular top and bottom) about 22 mm long
  (y), 35 mm tall (z) and 7-9 mm thick (x), with all edges slightly rounded. At AWS69 the arms look a little shorter
  and more lobed: a rounded block of about 18 x 30 mm.
- **Position:** one at each front corner, **in front of** the tub's front corner. The arm's rear face touches the front
  faces of the side wall and of the plate's front corner, and its outer face is **flush with the side wall's outer
  face** in x. It reaches from about 1 mm above the floor to about 3 mm above the top plate.
- **Axle hole:** about 40 % of the way up from the arm's bottom, halfway along its length. The right arm carries a
  **steel M5 nyloc nut and washer** on its outer face. The left arm's outer face is not visible.
- **Fastening to the tub [G]:** screws along x through the arm's rear part into the tub. More likely, given the side
  wall holes 8-15 mm behind the arm, they go through the tub side wall into a rear tab on the arm. The top plate's
  front-corner screws also clamp the top of the arm.
- **Mechanism:** the arms are the weapon's bearings. Every weapon load goes through them into the tub's front corners.

### 4.4 Weapon (rotor)
- **AWS69, drum:** a cylinder about 25 mm in diameter and 66 mm long, silver (an aluminium tube, or silver tape over a
  printed core). It is smooth, with no visible teeth **[G: 1-2 low impact bars likely]**. Gaps: about 1-2 mm to each
  arm and about 2 mm to the pocket's back wall. Its lowest point is about 1-2 mm off the floor. The copper and red
  windings at its right end show that the drum is the **outrunner bell or is bonded to it** (an in-drum motor).
- **AWS71, scoop or beater:** a bent aluminium plate about 65 x 35 mm and 1.5-2 mm thick, hung from the axle, with a
  large rounded-rectangle window (about 30 x 22 mm) and a sprung black cross bar (about 6 mm in diameter) in the
  window. Its straight leading lower edge is about 2 mm off the floor and reaches about 8 mm ahead of the arms. This
  version probably spins as a "beater bar", with the plate as the tooth **[G]**.
- **AWS72:** taped pink and silver, with an outline like AWS71's (a top roll plus an apron).
- **Colour for the model:** aluminium, `#b9b9b4`.
- **Axle:** about M5 (it takes the M5 nyloc): a dead axle, clamped by the nut through the right arm **[G: M5]**.

### 4.5 Weapon motor
- **Seen:** copper and red windings (aws69) and a black ribbed bell about 18-20 mm in diameter and 8-10 mm long
  (aws71), at the **right (+x) end of the weapon, just inboard of the right arm**.
- **Mechanism [G]:** a small brushless outrunner (1404 to 1806 class). Its stator is fixed to the dead axle, which is
  nutted to the right arm. The bell turns and drives the weapon, which is bolted or bonded to it. The far (left) end of
  the weapon runs on a bearing on the axle in the left arm; a black round boss shows there at aws71.
- **Plastic weapon-motor mount:** nothing is visible apart from the arm itself; the axle clamp holds the stator. A
  black printed spacer boss may sit between the arm's inner face and the motor base, and the "black ribbed cylinder"
  could be partly that spacer **[G]**.
- **Phase leads:** not visible. They probably run through the hollow axle, or along the arm's inner face and into the
  tub through the pocket's back wall **[G]**.

### 4.6 Wheels and hubs, 2 + 2 parts
- **Tyres:** black rubber at AWS69; salmon or coral red (`#e07a6a`) at AWS71/72, with a rough cast or foam texture.
  About 31 mm outside diameter, 9-10 mm wide, with a section about 4-5 mm deep.
- **Hubs:** recessed black or dark-brown printed discs, plain, with no visible spokes.
- **Position:** axle across the robot, about 30 mm in front of the rear face (about 0.32 W). Wheel centres at about
  x = +/-38 mm. The tyre top is level with the top surface of the plate (within about 0.5 mm), so the robot can drive
  upside down. The tyre bottom is the lowest point of the robot.
- **Gaps:** about 1.5 mm from tyre to guard wall, about 1 mm from hub to bulkhead, about 1.5-2 mm from tyre to the
  front and rear walls of the well, and about 1 mm from tyre to the edges of the plate notch.
- **Drive [G]:** each wheel is pressed on the D-shaft of an N10/N20 gearmotor inboard of it. The motor body lies along
  x inside the tub, with its gearbox face against the bulkhead.

### 4.7 Drive motors, 2 (hidden) [G]
- N10 or N20 micro gearmotors (about 12 x 10 x 24-34 mm), one per wheel, with their axes along x at wheel-axle height.
  They sit back to back near the middle of the tub in printed cradles, and the lid stops them lifting.

### 4.8 Electronics (hidden) [G]
- **Battery:** a flat 2S LiPo, 180-300 mAh (about 36 x 20 x 10 mm), in the rear bay between the wheel wells.
- **Receiver and drive ESC:** a Malenki-Nano class board (about 32 x 19 x 3 mm) in the front bay behind the weapon
  pocket. The square window in the plate sits over its LED and bind button.
- **Weapon ESC:** a small brushless ESC (about 22 x 11 x 4 mm) in a side bay.
- **Switch:** the visible slide switch in the centre of the plate, mounted to the plate's underside with its lever up
  through the slot, taped round.
- **Wires:** none are visible from outside. Silicone leads run from the battery to the switch, from the switch to the
  two ESCs, from the ESC to the drive motors (between the cradles), and from the ESC to the weapon motor (through the
  front wall to the right arm).

### 4.9 Screws and nuts (visible)
| Where | Count | Type (est.) | Direction |
|---|---|---|---|
| Top plate edge (front corners, notch fronts, rear corners) | 6 | M2 button or cross-head, black | down (-z) into the tub |
| Right side wall, near the front, mid height | 1-2 visible (aws71/72), 2 holes (aws69) | M2/M3 | across (-x) into the arm or tub |
| Left side wall (mirror, not seen) | 1-2 **[G]** | M2/M3 | +x |
| Weapon axle, outer face of the right arm | 1 | M5 flanged nyloc + washer, silver | on an axle along x |
| Weapon axle, left arm | 1 **[G]** | bolt head or nut | along x |
| Sprung bar clips in the scoop window (aws71) | 2 springs + 2 clips | wire | - |

---

## 5. Part table

| # | Part | Qty | Colour | Material (est.) | Size (mm) | Position (centre, mm) |
|---|---|---|---|---|---|---|
| 1 | tub | 1 | black `#22262a` | printed | 94 x 68 x 27 | (0, -16, -0.5) |
| 2 | top plate | 1 | black `#2b3034` | printed or CF | 94 x 68 x 1.5 | top at z ~ 15 |
| 3 | right arm | 1 | black | printed | 8 x 22 x 35 | (+43, +30, 0) |
| 4 | left arm | 1 | black | printed | 8 x 22 x 35 | (-43, +30, 0) |
| 5 | weapon (drum or scoop) | 1 | silver | aluminium | dia 25 x 68 | axle (0, +34, 0) |
| 6 | weapon motor | 1 | black bell, copper | bought | dia 18-20 x 10 | right end of the weapon |
| 7 | axle + nyloc | 1 | silver | steel | M5 x ~90 | along x at (y 34, z 0) |
| 8,9 | tyres | 2 | salmon or black | TPU/rubber | dia 31 x 10 | (+/-38, -18, 0) |
| 10,11 | hubs | 2 | black | printed | dia 20 x 10 | in the tyres |
| 12,13 | drive gearmotors | 2 | metal | bought | 12 x 10 x 24-34 | inboard of the wheels |
| 14 | battery | 1 | - | 2S LiPo | 36 x 20 x 10 | rear bay |
| 15 | receiver/ESC | 1 | - | Malenki class | 32 x 19 x 3 | front bay |
| 16 | weapon ESC | 1 | - | bought | 22 x 11 x 4 | side or rear bay |
| 17 | slide switch | 1 | silver/black | bought | 11 x 6 x 4 | plate centre |
| 18 | lid screws | 6 | black | M2 | - | plate edge |
| 19 | arm screws | 2-4 | black | M2/M3 | - | side walls near the front |

---

## 6. Contact and gap matrix (touching faces, gaps in mm)

| A | B | Relationship |
|---|---|---|
| top plate (underside) | tub wall tops | touch round the whole perimeter; screwed (6) |
| top plate front corners | arms (rear tops) | touch, or 0-1 mm; the corner screws clamp beside the arms |
| arm rear face | tub front-corner faces | touch (bolted interface) |
| arm outer face | side wall outer face | flush (coplanar in x) |
| arm inner face | weapon end | 1-2 mm running gap |
| weapon | pocket back wall (tub front wall) | about 2 mm gap |
| weapon lowest point | floor | 1-2 mm |
| weapon top | plate top | weapon top about level with the plate |
| motor bell | right arm inner face | 1-2 mm gap (the stator is on the axle) |
| motor bell | weapon right end | touch (bonded or bolted) |
| axle | right arm | clamped by the nyloc and washer on the outer face |
| axle | left arm | in a bearing or bushing **[G]** |
| tyre | guard wall | about 1.5 mm |
| hub | bulkhead | about 1 mm |
| tyre | well front/rear walls | about 1.5-2 mm |
| tyre | plate notch edges | about 1 mm (in plan) |
| tyre top | plate top | level (within about 0.5 mm) |
| tyre bottom | floor | touches (the lowest point) |
| tub floor | floor | about 1.5 mm clearance |
| switch flange | plate underside | touch, with the lever through the slot |
| drive motor gearbox | bulkhead | touch, shaft through a hole **[G]** |

---

## 7. Mechanism and load paths
- **Weapon:** a rotor spinning about an axis along x, driven by an outrunner at its right end whose stator is clamped
  on a dead axle nutted to the right arm. Impact loads run from the weapon to the axle, the arms, the arm bolts and the
  tub's front corners, which is why the arms are stout (8 mm).
- **Drive:** two-wheel skid steer. The wheels are about 30 % of the length from the rear, so the robot rests on the
  wheels plus the weapon or the front edge **[G]**, with the centre of mass ahead of the axle. The tyres are level with
  the top plate, so it drives upside down too (the weapon then hits from the other side).
- **Armour:** no separate armour. The 2 mm walls and the full-height side walls guard the wheels, and the rear
  chamfers deflect hits.
- **Service:** remove the 6 lid screws to reach the electronics. Remove the right nyloc to drop the weapon out.

---

## 8. What the model should copy (priority order)
1. The plan outline: straight sides, rear corner chamfers, the front pocket between the arms, and the wheel notches near
   the rear.
2. Upright stadium arms at the front corners, flush with the sides, slightly taller than the body, with the axle in the
   lower middle.
3. A weapon between the arms about 0.27 W in diameter and 0.72 W wide, reaching nearly to the floor.
4. Wheels inside the side walls, with the tyre tops level with the plate, and salmon tyres.
5. A flat lid with 6 edge screws, the centre switch and a square window.
6. A silver nyloc and washer on the right arm, and a black outrunner bell visible at the right end of the weapon.

---

## 9. Coordinate frame (the one frame used in this whole file)

- Origin: the midpoint between the two wheel centres. +x = the robot's right, +y = forward (toward the weapon),
  +z = up. Units are mm and angles are degrees.
- Floor plane z = -15.5 (the wheel radius). The wheel axle line is y = -18, z = 0.
- Photo pixel coordinates are (u, v) in the **original** image, u to the right and v down, origin at the top left.
  Image sizes: aws69 1331 x 1206, aws71 1931 x 1231, aws72 1078 x 776.

## 10. Every part in all dimensions (mm, with angles and radii)

| Part | L (y) | W (x) | H (z) | Wall/thickness | Radii / angles | Extent in the frame |
|---|---|---|---|---|---|---|
| Tub outer | 68 | 94 | 27.5 | walls 2.0, floor 1.5 | rear chamfers 45 deg, legs 12; vertical edges sharp (r < 1) | x -47..47, y -50..18, z -14..13.5 |
| Tub front pocket | 13 deep | 72 wide | open top | back wall 2.0 | square corners | x -36..36, y 5..18 **[G: depth 12-15]** |
| Wheel well (each) | 34 | 12.5 | through | guard wall 2.5 outboard, bulkhead 2.0 inboard | square | \|x\| 32..44.5, y -35..-1 |
| Top plate | 68 | 94 | 1.5 | 1.5 | same chamfers; notch corners square | z 13.5..15 |
| Plate wheel notch | 36 | 15 | through | - | square | \|x\| 32..47, y -36..0 |
| Plate square window | 6 | 7-8 | through | - | square | centre (-14, 6) |
| Switch slot | 4 | 7.5 | through | - | square | centre (1.75, -6) |
| Arm (each) | 22 | 8 | 34-36 | solid | stadium: ends r 11 about a vertical axis (or r 13.5 front lobe **[G]**), edge fillets ~1 | \|x\| 39..47, y ~12..47, z -14.5..+19 **[G]** |
| Axle hole in arm | - | through | - | - | dia 5 (M5) | centre y 34, z 0 |
| Nyloc + washer | - | 5 (proud) | - | washer 1 thick | nut 8 AF, washer dia 10-11 | on the right arm outer face, x 47..52 |
| Drum (aws69) | dia 25 | 72-74 | dia 25 | tube wall 1-1.5 **[G]** | r 12.5 | x -37..37, centre (y 34, z 0) |
| Scoop (aws71) | 35 developed | 65 | - | 1.5-2 sheet | bend r ~13 round the axle, tip curl r ~3, window corners r 5 | hangs from the axle down to z -14 |
| Scoop window | 22 | 30 | - | - | corner r 5 | centred on the scoop face |
| Sprung bar | dia 6 | 35 | - | - | - | inside the window, parallel to x |
| Motor bell | dia 18-20 | 8-10 | - | - | r 9-10 | x ~ 27..37, on the axle |
| Tyre (each) | dia 31 | 10 | dia 31 | section 4-5 | outer r 15.5, inner r ~10.5 | centre (+/-38, -18, 0) |
| Hub (each) | dia 21 | 10 | - | - | r 10.5 | inside the tyre |
| Lid screws | head dia 3.5-4 | - | head 1.3 | M2 | button head | listed in section 4.2 |
| Arm screws | head dia 3.5-4 | - | - | M2-M3 | - | right wall, (x 47, y ~4 and ~14, z ~0) **[G]** |
| Switch lever | 3 | 3 | 3 proud | - | - | in the slot, z 15..17 |

## 11. Curves and outlines as math

All in the frame of section 9.

- **Tub plan outline** (closed polygon, counter-clockwise, x then y):
  (-35,-50) -> (35,-50) -> (47,-38) -> (47,1) -> (39,1) -> (39,18) -> (-39,18) -> (-39,1) -> (-47,1) -> (-47,-38) -> back.
  Right rear chamfer: the segment of the line **x - y = 85** for y in [-50, -38]. Left rear chamfer: **-x - y = 85**.
  (The step at y = 1 from |x| = 47 to 39 is where the arms sit beside the narrow front of the tub. The photo shows the
  arm flush with the side, so the outer silhouette is the full rectangle |x| <= 47 for y in [-38, 47].)
- **Front pocket** (seen from above): a rectangle |x| <= 36, 5 <= y <= 18, open at y = 18 and at the top.
- **Arm side profile** (in the y-z plane, extruded over |x| in [39, 47]): a stadium,
  { (y,z) : 12 <= y <= 34, -13.5 <= z <= 13.5 } UNION { (y - 34)^2 + z^2 <= 13.5^2 }.
  That is a rectangle with a semicircular front end, centre (34, 0), radius 13.5, spanning angles -90 to +90 deg
  measured from +y. In the photos the top edge rises toward the rear to about z = +17 **[G]**; an alternative reading
  is a vertical stadium of length 22 with end-circle centres at z = -3 and z = +6, radius 11 (see section 12).
- **Drum** (aws69): the solid of revolution about the line (y, z) = (34, 0) along x:
  (y - 34)^2 + z^2 <= 12.5^2 for |x| <= 37, hollow with bore radius 11 **[G]**.
  Impact bars **[G]**: two blocks 4 mm wide (in y) and 2.5 mm high, at polar angles 90 deg and 270 deg, each along half
  the length.
- **Scoop cross-section** (aws71, in the y-z plane, about the axle (34, 0)):
  1. an arc of radius 13 centred on (34, 0), from theta = 100 deg to 200 deg (theta from +y toward +z);
  2. from the arc end at (34 + 13 cos 200, 13 sin 200) = (21.8, -4.4), a straight segment tangent to it, running down
     and forward to the lip at (44, -13.5), a slope of about **z = -0.41 (y - 21.8) - 4.4**;
  3. a tip curl of radius 3 turning up through 60 deg.
  The window is a rounded rectangle in the developed sheet: |u| <= 15 (along x), |v| <= 11 (along the sheet), with
  corner radius 5: { max(|u| - 10, 0)^2 + max(|v| - 6, 0)^2 <= 5^2 }.
- **Wheel**: (y + 18)^2 + z^2 <= 15.5^2 for |x| in [33, 43]. Hub: radius 10.5 over the same x range.
- **Plate wheel notch**: the rectangle |x| in [32, 47], y in [-36, 0].
- **Plate window**: x in [-17.5, -10.5], y in [3, 9]. Switch slot: x in [-2, 5.5], y in [-8, -4].

## 12. Each feature measured several independent ways

| Feature | Way 1 (dimension) | Way 2 (ratio) | Way 3 (photo pixels) | Way 4 (frame coordinates) |
|---|---|---|---|---|
| Body width | 94 mm (assumed scale) | 1.00 W | aws72: rear-right corner to the left edge of the far wheel notch at about u 1030 -> 320 (heavily foreshortened) | x -47..47 |
| Body length (no weapon) | 68 mm | 0.72 W | aws72 near wall: u 440 -> 1030 (590 px) vs the near arm height of 310 px | y -50..18 |
| Body height incl. plate | 29 mm | 0.31 W | aws72 near wall at the front: v 500 -> 690 (190 px); aws71 near wall: v 540 -> 1010 (470 px) | z -14..15 |
| Arm height | 34-36 mm | 1.2-1.6 x body height | aws71: v 500 -> 1100 (600 px, 1.28 x the wall's 470); aws72: v 410 -> 720 (310 px, 1.6 x 190) | z about -14.5..+19 |
| Arm length | 22 mm | 0.23 W | aws71: u 830 -> 1100 (270 px) vs the wall's 470 px height, so about 0.57 x 29 = 17-22 mm | y about 12..34 (+ the 13.5 front lobe) |
| Axle height in the arm | 40-53 % up from the arm bottom | - | aws71: nut v 780 in the arm's 500..1100 (53 %); aws72: nut v 600 in 410..720 (39 %) | z about 0 |
| Weapon width | 70 mm | 0.74 W | aws69 drum u 140 -> 640 (500 px) vs near arm to far arm about 560 px | x -37..37 |
| Drum diameter | 25 mm | 0.27 W, 0.86 x body height | aws69 drum v 470 -> 900 seen at a slant (end ellipse about 170 px vs the near wall's 300 px height, so 0.57 x 29 = 16-26) | r 12.5 |
| Wheel diameter | 31 mm | 0.33 W, about 1.07 x body height | aws72 near wheel v 350 -> 500 in its notch (only the top half visible) | r 15.5 |
| Wheel y position | 30-32 mm ahead of the rear | 0.45 of body length from the rear | aws72 near wheel centre u ~815, between the arm (u 440) and the rear corner (u 1030): 0.64 of the way back | y -18 |
| Rear chamfer | legs 12 mm | 0.13 W | aws72 bottom right: chamfer about 120 px long vs the side wall's 590 px for 68 mm, so 14 mm | x - y = 85 |
| Plate window | 7 x 6 mm | 0.075 W | aws72 u 370 -> 440 (70 px) | centre (-14, 6) |
| Switch | 11 mm body | 0.12 W | aws72 silver tab about 75 px | centre (0, -6) |
| Nyloc | M5, 8 AF | 0.09 W | aws71 nut about 110 px wide, 0.18 of the arm's 600 px height, so 6.5 mm (ok for M4-M5) | x 47..52, y 34, z 0 |

## 13. Consistency check (conflicts and reconciled values)

| # | Conflict | Values seen | Reconciled value | Why |
|---|---|---|---|---|
| 1 | Arm height vs body height | 1.28 x (aws71) vs 1.6 x (aws72) | 1.25 x, about 35 mm | aws72's arm is much nearer the camera than the wall it was compared with (perspective) |
| 2 | Axle height in the arm | 53 % vs 39 % up | 45 %, z ~ 0 (axle at about wheel-axle height) | the nut sits low in aws72 because of the camera tilt; the drum must reach within ~1 mm of the floor |
| 3 | Arm position: beside or in front of the tub corner | aws69 looks beside (plate screw right behind the arm top); aws72 looks in front (the arm's rear face against the wall's front edge) | the arm's rear part overlaps the tub's narrow front section (beside), flush with the side wall, and its front lobe projects ahead | satisfies both: from the front-right both readings show the same silhouette |
| 4 | Weapon type | drum (aws69) vs plate scoop (aws71, aws72) | model the aws69 drum, with 2 impact bars | REFERENCE.json says drum; the drum is the weapon whose motor shows (in-drum outrunner) |
| 5 | Weapon motor position | windings at the right end (aws69) vs black bell at the right end (aws71) | right (+x) end, stator on the arm side | both photos agree on the side |
| 6 | Tyre colour | black (aws69) vs salmon (aws71/72) | salmon `#e07a6a` | 2 of 3 photos, and it is the newer build |
| 7 | Body length | 68 mm (aws72 wall) vs about 75 mm (aws69 wall, more foreshortened) | 68 mm | aws72 is the most side-on view of the near wall |
| 8 | Front pocket depth | 15 mm (aws69 top view of the cut) vs not visible (aws71) | 13 mm | aws69 is the only direct evidence; leave the drum 1.5-2 mm gap |
| 9 | Wheel top vs plate | level (aws71) vs 1 mm below (aws69) | level, within 0.5 mm | needed to drive upside down |
| 10 | Arm-screw count on the side wall | 2 holes (aws69) vs 1 visible (aws71/72) | 2 per side | the second one is hidden by the arm or the weapon in aws71/72 |

---

## 14. Why the designer did it (each part, several angles)

- **Tub (open-top box, rear chamfers).**
  - Fight: the 45 deg rear chamfers deflect spinners and make the robot harder to pin in a corner. Full-height side
    walls hide the wheels from horizontal spinners. Low height (29 mm) keeps the centre of mass low and gives
    opponents' wedges little face to get under.
  - Construction: an open-top box prints flat with no supports, one print in 2-3 h. Walls of about 2 mm are the lightest
    that survive ant hits in PLA or PETG.
  - Repair: the electronics drop in from the top. The tub is cheap to reprint.
  - Weight: a box of plain walls is the lightest way to enclose ~95 x 68 mm.
- **Front pocket.**
  - Fight: the drum sits partly inside the body, so the robot is shorter (better in a 150 mm box) and the drum is
    shielded from side hits.
  - Construction: just a missing wall section; costs nothing.
- **Top plate (separate lid, 6 screws).**
  - Fight: it stiffens the open tub into a closed box and takes top hits (vertical spinners). The flat top means the
    robot works upside down.
  - Construction and repair: it gives access for electronics and charging. It prints flat; carbon or G10 could be
    laser cut. The wheel notches let the wheels be full height without a taller body.
  - Weight: 1.5 mm is the thinnest that will not flex under the hits.
- **Square window in the plate.**
  - Practical: you can see the receiver LED (failsafe or bind state) without opening the lid **[G]**.
- **Switch in the centre of the lid, taped.**
  - Rules: the switch must be reachable without tools and away from the weapon; the centre top is the safest place.
  - Tape: it stops debris getting in and the lever being knocked off by hits **[G]**.
- **Weapon arms (thick separate uprights).**
  - Fight: they take the full weapon reaction. Separate parts can be reprinted alone when bent, and 8 mm of plastic
    gives stiffness so the drum does not rub. They stick out past the body to protect the drum ends from side hits.
  - Construction: printed lying flat (layers parallel to the side face), so the axle load runs in the layer plane and
    does not peel them. They bolt to the tub with side screws, so the tub stays a simple print.
  - Rules: the axle sits in both arms, so the weapon is supported at both ends.
- **Dead axle with a nyloc nut.**
  - Construction: an off-the-shelf M5 bolt or rod plus a nyloc. The weapon and motor slide off for repair.
  - Fight: a steel axle through both arms ties the arms together like a cross-member.
- **Drum (aws69) or scoop (aws71/72).**
  - Fight: a drum gives a vertical upward hit that flips opponents. Its compact energy store is safe on a small
    robot. The scoop version gets under robots like a wedge while still spinning (a "beater"), and its window saves
    weight. The sprung bar may be a tooth that pops out at speed **[G]**.
  - Weight: tube or sheet metal is lighter than a solid drum.
  - Cost: tape over a printed core (aws72) is the cheap spare.
- **In-drum or end-mounted outrunner.**
  - Fight: no belt to throw. Direct drive, and the motor is shielded by the drum.
  - Construction: the motor is the bearing on one end, with fewer parts. The drum bonds to the bell.
- **Wheels inside the walls, near the rear, tyres level with the top.**
  - Fight: protected from spinners. Invertible. Near the rear for steering with the drum at the front. Grippy cast tyres.
  - Construction: wells cut straight through the tub; the gearmotors push straight in.
- **Small screws (M2) throughout.**
  - Weight: light. Cost: one screw type and one driver. They thread into the printed walls without inserts **[G]**.

## 15. Unseen and inner parts (guesses with confidence)

Confidence: **H** = high, almost certainly there; **M** = medium, likely as described; **L** = low, a plausible
design only.

| Part | Guess | Size (mm) | Position (frame of section 9) | Conf. |
|---|---|---|---|---|
| Battery | 2S LiPo 180-300 mAh, in a flat pack | 36 x 20 x 10 | rear bay, centre (0, -37, -7.5), long side along x | M |
| Receiver + drive ESC | Malenki-Nano (receiver with 2 brushed ESCs and 1 PWM out) | 32 x 19 x 2.5 | front bay floor, centre (0, 6, -11) | M |
| Weapon ESC | small brushless ESC, heat-shrunk | 22 x 11 x 4 | rear bay beside the battery, (24, -37, -10.5) | M |
| Power switch | slide switch with a flanged body, screwed or glued under the lid | 11 x 6 x 4 + flange 20 | under the lid at (0, -6, 11) | H (visible) |
| Drive gearmotors | 2 x N10 or N20 gearmotors, 1000 rpm class | 12 x 10 x 24-34 | (+/-18.5, -18, 0), axis along x, shafts outward | H |
| Motor cradles | printed saddles moulded into the tub floor, plus lid ribs pressing the motors down | 4 mm ribs, 16 wide | under each motor | M |
| Bulkheads | 2 mm walls between the motor bay and each wheel well, with a shaft hole | 2 x 34 x 26 | \|x\| 30-32, y -35..-1 | H |
| Weapon motor | 1404-1806 brushless outrunner, stator fixed to the right arm or axle | dia 18-23 x 12-15 | +x end of the drum, axis along x at (y 34, z 0) | M |
| Weapon motor mount | printed boss or spacer on the right arm's inner face, M2 screws into the stator base | dia 11 x 2 | x 37-39 | L |
| Far-end bearing | flanged ball bearing or plain bushing in the left arm or the drum end cap | 4-5 bore, 10-13 OD | -x end, in the arm or the drum end | M |
| Drum end cap | aluminium or printed disc closing the drum's -x end, running on the axle | dia 22 x 3 | x -37..-34 | L |
| Locking pin hole | a hole through the arm into the drum (rules need a weapon lock) | dia 2.5-3 | through the -x arm into the drum end | M |
| Arm screws | 2 per side, M2 x 12, along x through the arm into tub columns | - | (+/-47 -> 33, y 4 and 15, z -5) | M |
| Lid screw columns | printed columns or thickened wall tops under each lid screw | 6 x 6, full height | front corners, notch fronts, rear corners | M |
| Wiring | battery -> switch -> both ESCs; Malenki -> drive motors between the cradles; Malenki PWM -> weapon ESC; weapon ESC -> motor phases through a channel in the right arm and a hole in the tub's front side wall | 22-28 AWG silicone | inside the tub above the floor, over the motors | M |
| Velcro / tape | holds the battery and boards to the floor | - | under each part | M |
| Ribs | none visible; the floor-to-lid columns and bulkheads do the stiffening | - | - | L |

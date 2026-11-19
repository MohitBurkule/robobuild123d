# RBMK: full reference description (rebuild-from-text)

## Sources

All three photos are in `robots/rbmk/reference/`.

| Photo | View | Camera height | Size |
|---|---|---|---|
| `rbmk.aws71.webp` | front-right three-quarter | about 35 deg up | 2938 x 1761 px, the most detailed |
| `rbmk.aws74.webp` | straight front | about 20-25 deg up | 1678 x 721 px |
| `rbmk.aws76.webp` | front-left three-quarter | about 40-45 deg up | 1330 x 886 px |

- All three photos have the background cut out. The green halo on every edge comes from the masking and colour cast, not paint.
- It is the same machine in all three. Only the angles of the two spinning bars differ between photos.

## Conventions

- **Robot frame.** Front = +y (the end with the blue rollers). Right = +x (the robot's own right, seen from behind). Up = +z. Floor = z 0.
- **"Box"** means the central body.
- **Scale.** All mm values come from pixel measurement on aws74 at about **0.105 mm per pixel**. That scale assumes the weapon motors are 1806-class outrunners, about 23 mm across the bell. The motor class is itself a guess.
- **Tags on values:**
  - **(G)** guess.
  - **(S)** read from a single photo only.
  - **(M)** measured in two or more photos that agree within about 10 %.

---

## 1. Summary

RBMK is a small antweight "shuffler" with two separate horizontal spinners.

- **Body box:** a flat, rectangular, bare-aluminium box with a clear polycarbonate lid held by four button-head screws.
- **Base sheet:** one aluminium sheet under the box, folded three ways.
  - Two **wings**, one each side of the front half of the box, folded down and outward.
  - One **rear plate**, folded up and back behind the box.
- **Weapon motors:** one black outrunner stands on each wing.
- **Weapon bars:** each motor bell has a dark steel bar bolted straight to its top. Each bar has a T-shaped hammer end and a long tapered tail.
- **Nose rollers:** two blue cylinders sit side by side at the front centre, in a small bracket assembly bolted to the box front.
- The two spinners turn in tilted planes, roughly parallel to their wings. Each bar's inner half sweeps just above the lid.
- **Drive:** there is no drive train under or beside the body. The user's brief says the robot moves only by changing the two spinner speeds (gyro and vibration). **However, see 9.4:** the blue nose rollers appear to contain motor parts.

---

## 2. Part list (master table)

| # | Part | Count | Material / colour | Envelope (W x L x H mm) | Where (centre) | Fastened by |
|---|---|---|---|---|---|---|
| P1 | Body box (tub) | 1 | bare brushed aluminium sheet, silver-grey, scuffed | 56-58 x 62-66 x 12-14 (M) | x 0, y about +2, z 5..18 | no rivets or screws visible; the lid screws go into it |
| P2 | Lid | 1 | clear polycarbonate, milky with scratches, grey tint | about 48 x 62 x 1 (thickness G) | on top of P1, z about 18 | 4 x M2-class button-head socket screws (M) |
| P3 | Base sheet: centre panel | 1 (part of P3) | aluminium, about 1 mm (G) | about 58 x 64 | under P1, z about 4..5 | screws not visible (G: up through the box floor) |
| P3a | Base sheet: right wing | 1 | same sheet, folded down about 10 deg (S: aws74) | reaches 25-28 outboard of the box side, 30-36 long | right side of the box, front half | continuous with P3 through a fold (G) |
| P3b | Base sheet: left wing | 1 | mirror of P3a | same | left side of the box, front half | same |
| P3c | Base sheet: rear plate | 1 | same sheet, folded up and back 40-50 deg | about 58 wide at the fold, 26-30 wide at the top, 30-38 long up the slope | behind P1 | continuous with P3 through a fold (G) |
| P4 | Weapon motor, right | 1 | black anodised outrunner, silver stripes, copper windings | dia about 23, height about 18 with base | on P3a, x about +40, y about +10..+16 | screws from under the wing (G, not visible) |
| P5 | Weapon motor, left | 1 | same, with white "Le Todaro..."-style text on the bell side band | same | on P3b, mirror of P4 | same |
| P6 | Weapon bar, right | 1 | dark grey / black steel (G: hardened tool steel or Ti), tips worn bright | about 70-75 long, arm about 9 wide, T 20-22 wide, 2-3 thick | on P4's bell | 4 small silver Torx + 2 black button heads + 1 centre screw (M) |
| P7 | Weapon bar, left | 1 | same | same | on P5's bell | same |
| P8 | Front bracket plates, left and right | 2 | aluminium, 1.5-2 mm (G) | each about 14 x 14 face plus a forward fold | front face of P1, either side of the centre line | 2 screws each into P1's front (M) |
| P9 | Outer roller side plates | 2 | dark grey steel (G), D-shaped | about 4 (x) x 16 tall x 16 long | outboard of each roller | 2 small socket screws through each (S: aws76) |
| P10 | Centre divider plates | 2 | aluminium, back to back, bent forward and down | about 1.5 thick each, 0.5-1 gap between them | x about 0, between the rollers | continuous with P8 (folded) (G) |
| P11 | Blue rollers | 2 | translucent blue polyurethane / TPU, clear blue | dia about 13-14, width about 11-12 each | y about +40..+48, x about ±7 | on one shared axis between P9 and P10 |
| P12 | Roller hub internals | 2 | silver hex spider; copper windings visible (S: aws76, aws74) | inside P11 | - | see 9.4 |
| P13 | Nut on the front bracket | 1 visible | silver hex nut, M2 or M2.5 | about 4 across flats | on P8-left, above the left roller, near the centre | holds a screw that runs back into the box |
| P14 | Small socket screws on the front face | 3-4 visible | black and silver socket heads | heads about 3.5 dia | on P8-left and P8-right | into P1's front face |

**Visible fasteners (best count, total about 27):**

| Where | Count |
|---|---|
| Lid | 4 silver button-head screws |
| Each bar hub | 7: 4 silver Torx flat/pan heads, 2 black button heads, 1 small centre screw (14 for both bars) |
| Front brackets | 5: left plate has 1 silver socket + 1 black socket + 1 nut; right plate has 1 silver socket + 1 black socket |
| Outer D plates | 2 small silver socket heads each, 4 in all (S: left plate seen in aws76; right side in aws74 shows a screw stack) |

---

## 3. Parts in detail

### P1: Body box

**Shape:** a shallow rectangular tray.

- **Front face.** Flat, vertical and rectangular: about 56 wide x 13 tall in aws74.
- **Side walls.** Straight. The top long edges (left and right) are bevelled or folded in at about 45 deg as a strip about 4 mm wide.
  - Evidence (M): aws76 (left side) and aws71 (right side) both show a narrow bright sloped strip between the lid edge and the vertical side.
  - So the lid is about 8 mm narrower than the box base (G).
- **Front top edge.** A lip, not a bevel. In aws74 and aws71 the lid edge runs straight across with a dark seam under it, and the front face meets it at a sharp corner.
- **Rear wall.** Hidden behind the rear plate in every photo.

**Size ratios (M):** width : length : height is about 1 : 1.12 : 0.23.

**Colour:** raw brushed aluminium with random scratches and swirl marks. Bright where it catches the light, dark grey elsewhere.

**Position relative to other parts:**
- **Bottom face.** Rests on the base-sheet centre panel P3.
- **Side walls.** Meet the wing folds (P3a/b) along the lower side edges, front half only.
- **Weapon motors.** P4/P5 stand about 2-4 mm outboard of the side walls. aws71 and aws76 show a thin dark gap between motor body and wall.
- **Front face.** Carries the bracket plates P8.
- **Rear wall.** Meets the rear-plate fold P3c.

**Inside (seen or inferred through the lid):**
- a red-sleeved lead and a white connector (aws71, near the right front, about 60 % of the way back);
- something red under the right half (aws76, a red patch);
- a dark board toward the rear left (receiver or ESC);
- probably the battery: the large pale rectangle in the middle (G).

**Fixing:** the lid screws thread into it (G: tapped holes in corner blocks or folded tabs). No rivets are visible.

### P2: Lid

- **Shape.** A flat rectangle. It covers the flat top between the two side bevels and runs the full length front to back. Corners look square.
- **Screws.** About 6-8 mm in from each corner, toward the centre, on a pattern of roughly 40 (x) x 52 (y) mm (G, from aws74 and aws71; the front pair is about 43 apart).
- **Colour.** Clear with grey-white scratches. You can see through it; it is milky where scuffed. Thickness about 1 mm (G).
- **Contacts.** It sits on the box top all round. Nothing else touches it at rest.
- **Bar clearance (M).** Both weapon bars pass over it with an estimated **4-8 mm gap**:
  - aws74: the left bar's T-end hovers above the left half of the lid.
  - aws71: the left bar's tail crosses over the lid's front-left corner and its screw.
  - aws76: the left bar's T-end crosses the lid near the left rear screw.

### P3: Base sheet

The base is assumed to be one aluminium sheet folded three ways (G). It could also be three plates bolted to the box, but no seams or screws show at the folds.

**Centre panel:** hidden under the box; the same size as the box.

**Wings (P3a right, P3b left):**
- **Plan shape.** A trapezoid, wider at the box than at its tip.
  - It hangs off the bottom of the box side from about the box's mid-length (y about -4) to its front corner (y about +30).
  - The front edge runs outward and slightly back. The rear edge runs outward and forward.
  - The outer edge is straight, parallel to the box side, roughly 18-22 mm long.
  - aws76 shows the left wing clearly: a quadrilateral with its front-outer corner pointing forward-left, and the motor standing on its middle.
- **Droop.** It drops away from the box at **about 10 deg below horizontal** (S: aws74). There the left wing's top edge falls about 5 mm over about 26 mm, from the box bottom to the outer tip.
- **Floor contact.** In aws74 the outer edge is the lowest point on each side, so the wing tips are the side skids.
- **Edges.** Sheared and a little rough, with small burrs. The left tip is worn in aws76.
- **Reach (M).** About 26 mm from the box side to the tip, so the full width across the wing tips is about 110-115 mm.

**Rear plate (P3c):**
- **Angle.** Folds up and back from the bottom rear edge of the box at **about 45 deg** (G: 40-50).
- **Outline.** Seen in aws74 (nearly face-on but foreshortened) and aws71, it is a symmetric hexagon, or "coffin" shape:
  - full box width (about 58) for the first 12-14 mm;
  - then both sides taper inward at about 45 deg;
  - ending in a flat top about 26-30 mm wide.
- **Height (M).** The top edge stands about 12-15 mm above the lid top. It is the highest point of the robot, about 30-33 mm off the floor (G).
- **Clearance.** The weapon bars do not reach it.
- **Purpose (G).** A rear wedge or self-righting ramp, and a shield for the back of the box.

**Colour:** the same bare aluminium as the box, a little more scratched.

### P4 / P5: Weapon motors

- **Type (G).** Outrunner brushless, by eye about 2204-2306 class. The model uses an 1806 for mass, diameter about 21-23.
- **Bell.**
  - Black anodised, with 3-4 large kidney-shaped spoke windows on top. Copper windings show through them, and through the side band in aws71.
  - Two thin bright silver stripes run round the bell rim.
  - A silver ring band sits at the base (the stator base or mount ring).
- **Markings.**
  - Left motor: white text on the side band, something like "Le Todaro ... 2300KV" (S: aws71).
  - Right motor: a white "T" logo and "Le Todaro" (S: aws74).
- **Height (M).** About 16-18 mm from the wing to the top of the bell, about 1.25x the box height.
- **Position.**
  - Right motor centre: x about +40 (12 mm outboard of the box side wall), y about +10..+16 (front half), base on the wing. The left motor mirrors it.
  - Each axis is square to its wing, so it **tilts outward about 10 deg** from vertical (S: in aws74 both motors lean outward).
- **Gap to the box side wall (M).** 2-4 mm at the base. The motor does not touch the box.
- **Mount.**
  - The base sits flat on top of the wing.
  - No screws are visible (G: 2-4 M2/M3 screws from under the wing into the stator base).
  - In aws71 a dark block sits between the right motor base and the box side, just above the wing. It could be a printed spacer or the motor-lead exit, perhaps phase leads in heat-shrink (G).
- **Wires.** No phase wires show outside. They must run from the motor base through the box side wall near the wing fold (G). The black blob beside the right motor base in aws71 is the most likely lead exit.

### P6 / P7: Weapon bars

- **Material and colour.** Dark grey or black steel plate (G: tool steel, possibly black-oxided). Worn edges and tips show bright metal.
- **Thickness (M).** About 2.5-3 mm, about 1/8 of the bar width in the edge views of aws71 and aws76.

**Outline:** asymmetric, one bar per motor. Its three sections:

- **Hub.**
  - A parallel arm about 9-10 mm wide.
  - 4 silver Torx flat or pan heads on a circle or square of about 9 mm (the bell's 4-hole pattern).
  - 1 small silver centre screw, or the shaft end.
  - 2 black button-head socket screws on the bar's long axis, one each side of the 4-screw pattern, about 6 mm from centre. Heads are about 4 mm, marked "010" / "ES".
  - No washer plate.
- **Hammer arm.**
  - About 28-30 mm long from the hub centre.
  - A long lightening slot, about 2.5 wide, runs down its centre from about 8 mm off the hub to about 4 mm short of the end.
  - It ends in a **T-head**: a cross-bar about 20-22 mm wide and 6 mm deep, square-cornered on top.
  - One side of the T (the leading side) has a downward-hooked **tooth** that drops a little below the bar's lower face (S: aws71, both bars).
- **Tail arm.**
  - About 38-42 mm long from the hub centre: longer than the hammer arm, so its length is the counterweight.
  - Tapers from about 9 to 6 mm, with its own long central slot about 2.5 wide.
  - Ends in a rounded or chisel tip about 6-7 mm wide, with the end face ground bright (aws76, front-left bar).

**Total length (M):** about 70-75 mm tip to tip.

**Position.**
- Each bar lies flat on top of its motor bell. The bar plane is about 1-2 mm above the bell and tilts about 10 deg, outer end lower.
- Swept circle: radius about 40 (to the tail tip).
- **Inward:** the sweep passes over the lid and reaches to about 2-6 mm from the robot's centre line (G). The two sweep circles do not overlap: about 5-10 mm separates the inner tail tips at the centre line.
- **Outward:** the sweep reaches about 15 mm beyond the wing tips.

**Gaps.**
- Bar to lid: about 4-8 mm at the inner reach (M).
- Bar to rear plate: clear.
- Bar to roller brackets: clear (the brackets are lower and nearer the centre).

**Fixing.** Bolted straight to the bell with 4 + 2 screws. **There is no upper bearing or top bridge** (M: nothing above the bars in any photo).

### P8 to P14: Front roller assembly

**Overall:** a compact block centred on the box front, about 28-30 wide (x). It sticks out about 14 mm in front of the front face and is about 16 tall.

**P8, front plates.**
- Two plates lie flat on the front face, one each side of the centre line, each about 13 wide x 13 tall.
- A vertical seam about 0.5-1 mm wide separates them at x 0.
- Each plate's inner edge folds forward and slightly down to form the centre divider P10. So the assembly is two mirrored L-brackets, one per roller (G).
- Screws:
  - left plate: one silver socket head upper-right, one black socket head lower-left;
  - right plate: one silver socket head upper-left, one black socket head lower-left.
- The nut P13 is on the left plate, just left of the seam, about mid-height. It holds a screw or standoff that runs back into the box (G: possibly also locks an axle end).

**P10, centre divider.**
- Two thin aluminium plates back to back: the folded edges of the left and right P8 plates.
- In side view they curve down and forward (aws71: they sweep forward like a fin). They end a little below the roller axis.
- They separate the two rollers. Each roller nearly touches its divider plate, with a gap of about 0.5-1 mm.

**P9, outer side plates.**
- Dark grey steel, with a rounded "D" profile in side view: a straight back edge against the box front and a rounded front edge concentric with the roller.
- They carry the ends of the roller axle.
- Each has 2 small silver socket screws, one above the other about 4 mm apart, at the axle centre. Seen on the left plate in aws76; in aws74 the left plate shows a stack of 2 screws plus washers.
- They stand about 1 mm outboard of the roller ends.
- Their bottom tip reaches about 1-2 mm lower than the roller in aws74. **They may be the actual front floor skids (G).**

**P11, rollers.**
- Two blue, translucent, smooth cylinders with rounded shoulders.
- Diameter about 13-14 mm, width about 11-12 mm each.
- A slight groove runs round the middle of each (aws76 shows a darker ring at mid-width).
- Axis is lateral (x), at y about +42..+44, z about 6-7.
- Bottoms are level with, or about 1 mm above, the wing tips (M). In aws74 the rollers end at pixel row about 610 against about 640 for the wing tips, but they are nearer the camera, so roughly level.

**P12, hub internals.**
- aws76: a silver hexagonal spider and copper-coloured coils show through the left roller's open end.
- aws74: the outer end of the left roller shows a silver star or spider and screws.
- This looks like **an outrunner motor inside each blue tyre** (G; see 9.4).

### Wires

- No wires show outside the box, except possibly the motor leads at the right motor base (aws71, the dark block).
- Inside the lid you can see a red lead and a white JST-style connector (aws71, aws76).
- No antenna wire is visible.
- No switch is visible in any of the three photos. It must be at the rear, underneath, or under the rear plate (G).

### Graphics and colours

| Item | Colour |
|---|---|
| Aluminium (box, base sheet, wings, rear plate, front plates) | #b9c0c4..#d0d6d8 |
| Lid | clear, #d4e6ea tint |
| Bars | #2c2e31, with bright tips |
| Motors | #1d1e21, with silver stripes |
| Rollers | #2b8bd8, translucent |
| Outer D plates | #3a3c3f |
| Screws | silver #c8c8c8; the two button heads per hub are black |

There are no decals and no name on the robot.

---

## 4. Notes per view

### aws74 (front, about 22 deg up)

- **Order from left to right:**
  1. left bar's tail tip, at the far left;
  2. left wing tip;
  3. left motor, leaning outward;
  4. box front;
  5. roller block, in the centre;
  6. right motor;
  7. right bar.
- **Rear plate.** Shows above the box as a hexagon. Its flat top edge spans about the middle 45 % of the box width. It rises above the lid by about one box height.
- **Left bar.** Its T-end sits over the lid's left front screw. Its tail points out and forward-left, down to below wing height.
- **Right bar.** Its T-end sits over the lid's right rear screw. Its tail points out and forward-right.
- **Roller block.** Its bottom is at about the height of the wing tips.

### aws71 (front-right, about 35 deg up)

- **Right side.** Shows clearly:
  - the right wing: a trapezoid, its tip under the right bar's T-end;
  - the spoke windows of the right motor;
  - the full hub screw pattern on both bars;
  - the lid, with electronics visible under it.
- **Front plates.** The seam between them shows as a vertical line at the centre of the roller block. The left plate has the nut and a socket screw; the right plate has a socket screw at its upper left.
- **Left side.** The left wing appears as a large trapezoid in front of the left motor, its outer front corner pointing toward the camera's left. The left bar's T-end overhangs the wing tip, and its tooth hooks down.
- **Rear plate.** Its top edge shows above the box: a hexagon with angled shoulders.

### aws76 (front-left, about 45 deg up)

- **Box, left side.** Shows the 45 deg top bevel strip and the vertical lower side wall.
- **Rear plate.** Seen at an angle, sloping back. Its left edge drops from its top corner to the box's rear-left bottom.
- **Left wing and motor.** The motor stands on its wing. The wing's front-left corner pokes forward-left like an arrowhead.
- **Left bar.** Seen almost end-on:
  - The T-end is at the far end, over the rear part of the box, with a slot near the T.
  - The near end is the tapered tail, with a bright ground tip, resting over the wing tip.
- **Roller block.**
  - The left outer D-plate has 2 screws.
  - The left roller is open at the end, showing the spider and copper coils.
  - The right roller is partly hidden behind it.
- **Right bar.** In the background, over the right side.

---

## 5. Contact and gap matrix (at rest; estimates)

| | Box P1 | Lid P2 | Base / wing P3 | Motor P4/5 | Bar P6/7 | Front plates P8/10 | D plates P9 | Rollers P11 |
|---|---|---|---|---|---|---|---|---|
| **Box P1** | - | touches (top, all round) | touches (bottom face) | gap 2-4 | gap >5 | touches (front face, screwed) | gap about 1 (rear edge near the front face) (G) | gap 2-4 (front face to tyre) |
| **Lid P2** | | - | none | gap about 3 (at the side) | gap 4-8 (above) | may touch the front edge (G) | none | none |
| **Base / wing P3** | | | - | touches (motor base) | gap ≥8 (outer reach above the wing tip) | none, or nearly (G) | none | none |
| **Motor P4/5** | | | | - | touches (bell top, bolted) | none | none | none |
| **Bar P6/7** | | | | | - | gap >5 | gap >5 | gap >8 |
| **Front plates P8/10** | | | | | | - | touches (axle, screws) (G) | gap 0.5-1 (divider to tyre) |
| **D plates P9** | | | | | | | - | gap about 1 (to the tyre end) |

**Floor contact:** the outer edges of both wings, plus the roller block (the rollers, or the tips of the D plates). The rear-plate fold line is about 4-5 mm above the floor (G).

---

## 6. Mechanism (inferred)

- **Weapons.**
  - Each bar is driven straight by its own outrunner: no reduction and no support above the bar.
  - Each bar is bolted to its bell with 4 small screws (the motor's own prop-mount pattern), plus 2 extra button screws through the bar into the bell (G).
  - The asymmetric T / tail shape concentrates impact mass in the T-head, balanced by the longer tail.
- **Motion.**
  - A difference in spinner speed gives a yaw reaction on the body.
  - Spin-up and spin-down transients give gyroscopic precession. Because the motors tilt about 10 deg, the gyro moments rock the body onto one wing tip and then the other, which "walks" it.
  - This needs the two bars to spin in opposite directions (G).
- **Electronics (G).** All in the box under the clear lid:
  - one 2S LiPo;
  - a receiver;
  - two brushless weapon ESCs, one per spinner, so each can be throttled on its own;
  - a switch.

---

## 7. Proportions checklist for the CAD

| Item | Value |
|---|---|
| Box | 56-58 wide x 62-66 long x 12-14 tall, plus a 1 mm lid; bottom about 4-5 above the floor |
| Wings | reach about 26 outboard of the box; droop about 10 deg; hinge span y about -6..+30; outer edge about 20 long |
| Rear plate | folds at the box's rear bottom edge at 45 deg (40-50); 30-38 long up the slope; flat top 26-30 wide; shoulders about 13 up the slope |
| Motors | dia 21-23, height 16-18, tilted 10 deg outward; centre x about ±40, y about +12 |
| Bars | about 72 long (hammer arm about 30, tail about 42); arm 9 wide; T 20-22 x 6; 2-3 thick; slots 2.5 wide; bar plane about 20 above the floor at the hub |
| Rollers | 2 x dia 13.5 x 11.5 wide; axis y about +43, z about 6.5 |
| Roller plates | dividers 2 x 1.5 plates at x 0; outer D plates at x about ±14 |

---

## 8. What the model must not invent

- No wheels under the body.
- No wheel guards and no guard-to-chassis supports: none are in the photos.
- No printed weapon-motor mounts: the motors sit straight on the aluminium wings. The only candidate is the dark block beside the right motor base in aws71 (G: a lead exit or spacer).
- No top bridge over the spinners.
- No decals.

---

## 9. Uncertainties

1. **Wing mounting.** One folded sheet, or separate plates bolted to the box? No fold radius or screws are visible (G: folded).
2. **Rear plate.** It could be a separate plate screwed to the hidden back of the box. The model assumes a fold.
3. **Inner fixings.** How the box, base sheet and front brackets are held together inside is not visible.
4. **Blue rollers.** Copper windings and a hex spider show inside the blue tyres (aws76, left roller; aws74, left roller end). That is what a small outrunner motor with a tyre pressed onto its bell looks like.
   - **If so, the rollers are driven front wheels, not passive rollers, and RBMK is not purely a spinner-shuffler.**
   - The brief says there are no drive wheels, so the model treats them as passive rollers. This needs confirming with the user.
5. **Spin directions.** Unknown; assumed opposite.
6. **Weapon motor size.** Unknown, somewhere between 1806 and 2306 class. A larger motor makes every other dimension about 20 % larger.

---

## 10. Rebuild recipe (text only)

1. **Box.** Draw a 58 x 64 x 13 box, bottom at z 5. Bevel the two top long edges by 4 x 4. Put a 1 mm clear lid on the flat top (50 x 64). Add 4 button screws at (±19.5, -25.5) and (±19.5, +29.5).
2. **Base sheet.** Draw a 1 mm sheet under the box, 58 x 64.5.
   - At each side, from y -6 to +30, fold it down 10 deg into a 27 mm wing. Trim the wing to a trapezoid: root 36 long, tip 20 long, centred on y +12.
   - At the rear edge, fold it up 50 deg into a 36 mm plate. Trim that plate to a hexagon: full width for 13 mm, then tapering to a 26 mm flat top.
3. **Motors.** Stand a dia 21-23 x 14 motor on each wing at 11.5 mm from the fold, y +12, axis square to the wing. Add a 4 mm boss on top.
4. **Bars.** Put a 2 mm bar on each bell, with its long axis along y at rest:
   - arm 9 wide;
   - T-head 22 x 6 on the hammer end, tooth hooked on one side;
   - tail tapering to 6 wide;
   - slots 2.5 wide in both arms;
   - 4 screws on a 9.2 mm circle, plus 2 black button heads on the axis.
5. **Nose rollers.** Build the roller block at the front centre:
   - a fork of three thin plates at x 0, ±13.5, reaching 14 mm forward of the box front;
   - an axle at y +43, z 6.5;
   - two blue rollers, dia 13 x 10.5 wide, between the plates.
6. **Colours.** Use the table in section 3.

---

## 11. Exact geometry per part (frame: origin at the floor under the box centre; +x right, +y front, +z up; mm, deg)

All values are guesses fitted to the photos unless they are tagged (M) or (S).

### 11.1 Box P1
- **Envelope.** x in [-28, 28], y in [-30, 34], z in [5, 17.5]. Wall 1-1.5 mm (G). Floor 1 mm (G).
- **Section in the x-z plane** (the same at every y): the polygon (-28, 5), (28, 5), (28, 13.5), (24, 17.5), (-24, 17.5), (-28, 13.5).
- **Bevel.** The line x + z = 41.5 on the right, and its mirror on the left; 45 deg.
- **Corners in plan.** Square. Any radius is under 1 mm (folded sheet).

### 11.2 Lid P2
- **Plate.** x in [-24, 24], y in [-30, 34], z in [17.5, 18.5].
- **Holes.** dia 2.4 at (±19.5, -25.5) and (±19.5, 29.5).
- **Screw heads.** ISO 7380 M2: head dia 3.5, height 1.1; dome radius about 2.

### 11.3 Base sheet P3 (thickness t = 1, inside bend radius r_i = 1.5)
- **Centre panel.** x in [-29, 29], y in [-30.5, 34], z in [4, 5].
- **Right wing fold.**
  - Axis along y through (x 29, z 2.5).
  - The top surface is an arc of radius 2.5 from 90 deg to 80 deg (measured from +x toward +z).
  - The bottom surface is an arc of radius 1.5 over the same angles.
  - The wing plane then runs straight along the direction (cos 10, 0, -sin 10).
- **Right wing outline.** In wing coordinates (u along the slope from the end of the fold, v = y), the polygon (0, -6), (27, 2), (27, 22), (0, 30).
  - The tip edge runs from u = 27, v = 2 to v = 22.
  - Its mid-surface height is z = 4.47 - 27 sin 10 = -0.22, so its bottom edge is at about -0.7: the floor contact.
- **Left wing.** Mirror of the right wing in x = 0.
- **Rear fold.**
  - Axis along x through (y -30.5, z 6.5).
  - Arc of radius 1.5 / 2.5 from -90 deg to -140 deg (in the y-z plane, measured from +y toward +z).
  - The plate then runs straight along the direction (0, -cos 50, sin 50).
- **Rear plate outline.** In plate coordinates (w = x, s up the slope), the hexagon (-29, 0), (29, 0), (29, 13), (13, 36), (-13, 36), (-29, 13).
  - The shoulder edges follow the line s = 13 + (29 - |w|) * 23/16, an angle of about 55 deg to the bottom edge.
  - Top edge: z = 5.2 + 36 sin 50 = 32.8 (mid surface); y = -32.0 - 36 cos 50 = -55.2.

### 11.4 Motors P4 / P5
- **Shape.** A cylinder of radius 10.5-11.5, height 14 (stator plus bell), with a top boss of radius 2.5 and height 4.
- **Axis.** Right motor: n = (sin 10, 0, cos 10). Left motor: (-sin 10, 0, cos 10).
- **Base centre.** The right motor stands on the wing top at u = 11.5, v = 12.
  - World coordinates: (29.35 + 11.5 cos 10 + 0.5 sin 10, 12, 4.47 - 11.5 sin 10 + 0.5 cos 10) = (40.8, 12, 3.0).
  - Motor centre = base + 7n = (42.0, 12, 9.9).
- **Bell windows.** 4 kidney slots, each an annulus sector with r in [4, 8.5] spanning 60 deg, at 0 / 90 / 180 / 270 deg (G: photos show 3-4).
- **Bell stripes.** Two silver bands 0.6 wide, at 1 mm and 2.5 mm below the top rim.

### 11.5 Bars P6 / P7 (bar frame: origin on the spin axis at the bar's mid-plane; +y toward the T; thickness 2-3 along the axis)
- **Hub.** A circle of radius 7.5 centred at (0, 0). Holes:
  - centre hole r 2.6;
  - 4 holes r 1.1 at radius 4.6 and angles 45 / 135 / 225 / 315 deg;
  - 2 button-screw holes r 1.1 at (0, ±6.5) (G).
- **Hammer arm.** The strip |x| <= 4.5 for y in [7, 24].
  - T-head: the rectangle x in [-11, 11], y in [24, 30].
  - Tooth: the triangle (11, 24), (12.2, 29), (11, 30), hooked toward -z by 0.5 mm at the leading side (G).
  - Slot: x in [-1.25, 1.25], y in [9, 22], ends rounded with r 1.25.
- **Tail arm.**
  - Edges: x = ±(4.5 - 1.5 (|y| - 7)/35) for y in [-42, -7]. This tapers from half-width 4.5 to 3.0.
  - Tip: a semicircle of radius 3 centred at (0, -42).
  - Slot: x in [-1.25, 1.25], y in [-38, -9].
- **Swept radius.** 42 at the tail, 30.6 at the T corners (sqrt(11^2 + 30^2) = 32.0 with the tooth).
- **In the model:** the bar is drawn symmetric, T-ends on both arms, radius 34, so the swept width stays inside the 150 mm square: 2 x (42 + 34) = 152 would fail. That is a deliberate difference from the photo.

### 11.6 Front roller block
- **Front plates P8.** Two plates in the x-z plane at y in [34, 35.5]: x in [-14, -0.4] and x in [0.4, 14]; z in [3, 16].
- **Centre dividers P10.** Plates in the y-z plane at x = ±0.4..1.9. Profile in (y, z): from (35.5, 16) to (44, 12) along an arc of radius 12 centred at (35.5, 4), then down to (47, 3). Approximation: the line z = 16 - 0.6 (y - 35.5).
- **Outer D plates P9.** In the y-z plane at x = ±(12.5..14.5). Profile: the union of the rectangle y in [34, 43], z in [2.3, 13] and the circle centre (43, 6.5), r 7 (front edge concentric with the roller).
- **Rollers P11.** Solids of revolution about the x axis through (y 43, z 6.5). Profile r(x) = 6.5 for |x - x_c| <= 4.2, then a 45 deg chamfer down to r 5.6 at |x - x_c| = 5.25. Centres x_c = ±6.75.
- **Axle.** dia 3, along x, from x -14 to 14.

---

## 12. Each part described several independent ways

| Part | Dimensions (mm) | Ratio to box width (56) | aws74 pixels (0.105 mm/px) | Coordinates (frame of section 11) |
|---|---|---|---|---|
| Box width | 56 | 1.0 | 520 px (610..1130) | x ±28 |
| Box height | 13 | 0.23 | about 135 px front face, 345..480 | z 5..17.5 |
| Box length | 64 | 1.14 | not measurable; aws71 gives about 1.1-1.2x the width | y -30..34 |
| Wing reach | 27 | 0.48 | 380..610 = 230 px, which is 24 mm in projection | x 29..56 |
| Overall width over the wing tips | 112 | 2.0 | 380..1370 = 990 px, i.e. 104 mm (the outer bar tails hide part) | x ±56 |
| Motor diameter | 21-23 | 0.39 | about 210-230 px | centre x ±42 |
| Motor height | 14 + 4 boss | 0.32 | about 160 px with the base ring | z 3..19 |
| Bar length | 72 (model 68) | 1.29 | about 650 px in projection = 68 | centre at the motor axis |
| T width | 22 | 0.39 | about 200 px (left bar T in aws74) | - |
| Bar arm width | 9 | 0.16 | about 85 px | - |
| Rear plate rise above the lid | 14 | 0.25 | 130 px (lid edge 160, plate top 30) | top z about 33 |
| Rear plate top width | 26-30 | 0.5 | about 260-300 px (aws74 top edge) | w ±13 |
| Roller diameter | 13.5 | 0.24 | about 130 px | centre (y 43, z 6.5) |
| Roller width | 11 | 0.2 | about 110 px | x ±(1.5..12) |
| Roller block width | 28 | 0.5 | 740..1060 = 320 px, i.e. 34 mm with the outer plates | x ±14.5 |
| Lid screw pattern | 39 x 55 | 0.7 x 0.98 | front pair 610..1000 = 390 px, i.e. 41 mm (perspective) | x ±19.5, y -25.5 / 29.5 |

---

## 13. Consistency check (conflicts and reconciled values)

| # | Quantity | Conflict | Reconciled |
|---|---|---|---|
| 1 | Scale | aws74 gives 0.105 mm/px if the motor is 22 mm. If the motor is a 2306 (27.5 mm), the scale is 0.12 and the box is 62 wide. | **0.105.** An 1806-class motor keeps the mass realistic for an antweight. |
| 2 | Box length | aws71 suggests 1.2x the width (70 mm); aws76 suggests 1.05x (59). | **64** (1.14x). |
| 3 | Wing droop | aws74 left wing reads 12 deg, right wing 8 deg (perspective). | **10 deg.** |
| 4 | Rear plate angle | aws76 suggests about 55 deg; aws74 (plate top seen over the lid) suggests 40-45. | **50 deg.** |
| 5 | Bar length | aws74 projection 68; aws71 left bar about 75 (foreshortened less). | Photo **72**, model 68: limited by the 150 mm square with both bars pointing sideways. |
| 6 | Bar ends | aws71 and aws76 show one T-end plus one tapered tail; aws74 shows a T over the lid and the tail outboard. | **Asymmetric bar (T + tail).** The model uses two T-ends: a known difference. |
| 7 | Rollers | Passive (brief) vs motor internals visible (aws76). | Model: **passive.** Flagged for the user. |
| 8 | Roller bottom vs wing tips | aws74 shows rollers about 3 mm higher in the image, but they are nearer the camera. | **Level**, both at floor contact. |
| 9 | Motor position y | aws74 cannot show it; aws71 puts it about 40 % back from the box front (y about +8); aws76 about 30 % (y about +14). | **+12.** |
| 10 | Box material | Photo: aluminium sheet. | Model: printed nylon tub coloured aluminium, so wiring and inserts can be checked. A known difference. |

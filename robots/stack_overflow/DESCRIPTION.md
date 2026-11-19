# Stack Overflow: full reference description (rebuild-from-text)

## 0. Coordinate frame and conventions

- The origin is at the robot's centre in plan. z = 0 is the axle height, and the floor is at z = -10 (wheel r about 15, but the body floor at -10). [inferred from the CAD]
- +y is forward (the wedge tip), +x is the robot's right, +z up. Units are mm and degrees.
- Tags:
  - **[seen]** is visible;
  - **[inferred]** is reasoned;
  - **[guess]** is not visible.

Photos:

| File | px | View | Use |
|---|---|---|---|
| `stack_overflow.aws65.webp` | 150 x 103 | low left-side view on a wooden table, front to the image left | proportions (tiny) |
| `stack_overflow.aws66.webp` | 730 x 612 | top view from the rear-left, about 45-55 degrees; lid off; wheels and gears visible | internals |
| `stack_overflow.aws67.webp` | 1172 x 972 | front view from about 25 degrees up, background removed; the likeness photo | outline and colours |

## 1. Per-view description

### 1.1 aws67 (front, the likeness photo)
- **Wedge [seen]:** the lower 60% of the image is a big brushed-aluminium wedge, colour (214, 189, 193) where lit and (121, 122, 117) in shade. It is made of three facets:
  - a central trapezoid face, running from the floor tip at the image bottom (about (230, 690) to (1110, 520) at the lower edge) up to the box front at about y_px 330-420;
  - a left triangular facet, from the box's front-left corner (180, 640) down to the tip;
  - a right facet, from (1120, 500) to the box's right corner (1100, 420).
  In plan this makes a blunt chevron or pentagonal nose.
- **Wedge screws [seen]:** three silver cross-head pan screws in a vertical line on the central face, at (600, 495), (640, 630) and (685, 755), about 130 px apart. Two more are on the left box edge, at (215, 465) and (270, 590). The wedge edges at the sides show the folded flange.
- **Arm [seen]:** a grey-blue printed arm (53, 59, 68 to 90, 100, 120), 70 px wide.
  - It starts at a hub block at the top centre (550-720, 140-260), with 3 silver screws in a diagonal row at (605, 180), (630, 200) and (660, 225).
  - It bends down over the wedge and continues as a straight flat finger (690, 380) to (980, 780), lying on the wedge's right half.
  - The finger's outer 60% is wrapped in black tape or heat-shrink (40, 40, 45), and its tip is square.
- **Box [seen]:** behind the wedge, a clear polycarbonate box with visible internals:
  - yellow, blue and red wires, a gold motor can, a black gear, a lilac or white small block (a cable tie or foam);
  - a green PCB side panel (54, 100, 78) on the left outer side and another at the right rear (66, 87, 73);
  - silver screws at the box corners (about 10 visible).
- **Wheels [seen]:** two black treaded tyres at the rear top corners, (110-230, 110-240) and (780-880, 40-130), seen inside or behind the box at the rear. They stand above the box top by about 0.1 of the box height.

### 1.2 aws66 (top, lid off)
- The clear box shows its silver aluminium base or side, engraved with text on the front side: "STACK OVERFLOW"-like letters on the clear front panel. [seen, blurred]
- Two black treaded wheels with grey hubs sit at the rear corners, OUTSIDE the clear side walls (the robot faces the upper right). [seen]
- The grey-blue gearbox runs across the middle: 3-4 stacked spur gears, a motor (gold can), and the arm root on top. [seen]
- A green PCB and the ESC with wires sit at the right rear, and a white JST plug at the top. [seen]
- The aluminium wedge runs at the far side (upper right), with 4-5 screws along its top flange. [seen]
- A label "S2" sits on a black stand at the lower right (not part of the robot).

### 1.3 aws65 (side)
- A long low silhouette: the wedge is a long triangle, about 0.45 of the length, with a slope of about 20 degrees.
- The box is behind it. The rear wheel is large (about 0.4 of the length) and its top is above the box top.
- The arm lies on the wedge.

## 2. Overall form
- About 115 mm long (wedge tip to rear tyre), 105 mm wide (over the wheels), and 35 mm tall at the box, 40 at the wheel tops.
- Box: about 60 x 95 x 32 mm. Wedge: about 50 mm long in plan.
- Silhouette in front view: a wide flat trapezoid with the arm crossing it.

## 3. Parts

| ID | Part | Shape | L x W x H / thickness (mm) | Colour | Position | Fixing | Why | Conf. |
|---|---|---|---|---|---|---|---|---|
| B | clear box | 5-sided PC box, screwed corners | 60 (y) x 95 (x) x 32, PC 1.5-2 | clear; renders light blue-grey #b9c4c9 | y -47 to +13, z -10 to +22 | about 3 M2 per edge | light, shows the internals, cheap laser-cut | seen |
| WG | wedge | 3-facet bent aluminium: centre trapezoid 60 wide at the box tapering to 50 at the tip; side facets triangular | 50 plan length, 1.0-1.2 thick | aluminium #d6bdc1 / #7a7a75 | from the box front (y +13, z +22) to the tip (y +47.5, z -10) | 3 screws centre + 2 per side flange | a wide wedge to get under opponents; the facets deflect spinners | seen |
| A | lifter arm | L-shaped strip: hub block 40 x 25 x 14 at the pivot, then a flat 14-wide, 6-thick finger 75 long | 14 wide | grey-blue #5a6478, black tip #28282d (outer 60%) | pivot at the box top front, about (0, -10, +22); the finger lies on the wedge's right of centre | hub screwed to a gear with 3 M2 | lifts the opponent off the wedge | seen |
| G | gear train | 3-4 spur gears, module 0.5-0.8, the largest r about 12 | 6 thick | grey-blue | across the box centre | on steel pins | reduction for lifting torque | seen (aws66) |
| AM | arm motor | N20 or N10 gearmotor | 12 x 10 x 25 | gold can | across, left of centre | printed clamp | drives the gears | seen (aws66) |
| W | wheels (2) | treaded rubber on grey hubs | dia 30, w 10 | black | (+-54, -30, 0), outside the box sides | on the motor shafts | invertible, high ground clearance | seen |
| DM | drive motors | N20 | 10 x 12 x 25 | metal | (+-35, -30, 0) | clamp | | inferred |
| SP | green side plates | FR4 / PCB sheets | 1.6 x 45 x 30 | green #36644e | the outer sides near the rear | screws | wheel guards or decorative | seen (aws67) |
| E | ESC + Rx | green PCB | 30 x 20 x 5 | green | right rear inside the box | foam tape | | seen |
| BAT | battery | 2S LiPo | 45 x 17 x 10 | - | floor, right | velcro | | guess |
| SW | switch | slide or link | 12 x 4 x 6 | black | rear left (aws66 dark part) | screws | | seen (dark block) |

## 4. Curves
- Wheel: (y + 30)^2 + z^2 = 15^2.
- Gears: pitch circles r = 12 (arm gear) and r = 4 (pinion). Centre distance 16 along y. [guess]
- Arm bend: an arc of r about 10 joins the hub to the finger, at about 35 degrees of bend.
- Wedge plan outline (z = floor): polyline (-50, 7.5), (-25, 47.5), (25, 47.5), (50, 7.5). The facet lines are straight.

## 5. Contact and gap matrix (at rest)

| | B box | WG wedge | A arm | W wheels | floor |
|---|---|---|---|---|---|
| B | - | the top flange screwed to the box front, 0 gap | hub 1 mm above the box top | 1.5-2 mm between the tyre and the side wall | box floor 2-3 mm up |
| WG | - | - | the finger rests 0.5-1 mm above the wedge surface | - | tip 0-0.5 mm |
| A | - | - | - | - | - |
| W | - | - | - | - | contact |

## 6. Mechanism
- The arm motor drives the gears; the large gear on the arm pivot turns the arm 0-80 degrees.
- The finger tip rises from the wedge surface, lifting whatever sits on the wedge.

## 7. Several measures and consistency check

| Quantity | Pixels | Ratio | Engineering | Reconciled |
|---|---|---|---|---|
| Wedge length (plan) | aws65 about 45% of the length | 0.45 x 115 = 52 | the 20-degree slope over a 32 mm height gives 88 (too long), so the slope is steeper, about 32 degrees | 48-50, with the slope at about 33 degrees |
| Arm width | 70 px against the 880 px wedge width at the tip | 0.08 x 100 | 14 is reasonable for printed PLA | 14 |
| Wheel dia | aws65: 0.4 of the length | 46 (implausible) | the box is only 32 tall, and aws66 shows wheels about 1.2 x the box height | 30 |

Conflicts:
1. **Wheel size:** aws65's tiny photo exaggerates it. Reconciled to 30 mm, as in the CAD.
2. **Colours:** the CAD is all grey #c9cdd3, but the photo has an aluminium wedge, a clear box, a grey-blue arm with a black tip, and green side plates. Reconciled: decals on the wedge faces (aluminium), arm colour #5a6478 with a black tip decal.
3. **Arm position:** aws67 shows the finger right of centre, while the CAD has it on the centre line. A small offset is possible, but kept centred because of the sweep cut.

## 8. Why (design reasoning)
- **Clear PC box:** light, tough, shows the internals (a team signature), and quick to laser-cut.
- **Faceted aluminium wedge:** metal survives spinners. Facets give a wide front with a pointed nose for getting under opponents, while the side facets stop them sliding round.
- **Narrow single lifter arm:** a small, light printed arm with a geared motor. The black tip is heat-shrink, for grip and so the printed finger survives scraping.
- **Wheels outside the box at the rear:** bigger wheels for invertibility, and simple direct drive.
- **Green PCB plates:** off-cut FR4 as cheap stiff guards.

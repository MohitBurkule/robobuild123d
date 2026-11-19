# The Golden Nuggets: full reference description

This file is meant to be detailed enough to rebuild the robot from the text alone. It covers every visible part: shape, colour, size ratios, position against every other part, which faces touch, gaps, fastening and likely mechanism.

- Anything marked **(guess)** is inferred, not seen directly. Everything else is read off the photo.
- Sizes come from the one photo. The scale yardstick is the tyre outer diameter **D = 24 mm**. Every other size is a ratio of D, then converted to mm.
- Frame used below: **+y = front** (the end with the two chamfered pods and the lid hinges), **+x = robot's right**, **+z = up**, origin at the body centre at axle height. The ground is at z = -12 mm (bottom of the tyres).

---

## 1. Source photo and camera

There is one photo: `reference/the_golden_nugget.aws67.webp`, 1660 x 1128 px. It is a studio cut-out on white, and it is sharp.

**Camera.** From the front right, looking down about 30-35 deg. Measured from the image axes:
- The robot's x axis (the front edge, left pod tip to right pod tip) runs from about image (20, 620) to (960, 1000), a slope of +0.40.
- The robot's y axis (the line of wheel centres on the right side) runs about (+160, -130) per wheel pitch, a slope of -0.81.
- Solving gives the view direction about 35 deg off the front axis (likeness azimuth about 55-60, where 0 = right and 90 = front) and elevation about 30-35 deg.

The REFERENCE.json label (front_right_iso, elevation 45, azimuth 30) is wrong in azimuth. At azimuth 30 the wheel side would dominate, but in the photo the front face is the widest face. The checker's own best camera (elevation 25, azimuth 60) agrees with this measurement.

**What is visible:**
- the whole front (both pods, the channel, both hinge knuckles, the lid nose)
- the whole top (lid, both side rails, 4 screws)
- the whole right side (3 wheels, gear train, side slot)
- the tops of the 3 left wheels above the left rail

**What is not visible:** the rear face, the underside, the left side face, the switch, the battery, the motors.

---

## 2. Overall form

- A **flat, wide, low six-wheel box** with a **yellow lid/flipper plate** on top in the centre, two **blue side "rails"** (top cover strips) beside it, and two **chamfered blue pods** at the front corners.
- The six **black foam tyres on yellow hubs** stick out of both sides, three per side, almost touching each other. They are driven through a **yellow spur-gear train** visible along the right side under the rail overhang.
- The silhouette has no curves except the wheels. Every body face is flat, and the printed edges are sharp with no fillets.
- Approximate envelope:
  - Width over the tyres about 3.4 D = 82-84 mm.
  - Body width (pods outer face to outer face) about the same.
  - Rail-to-rail body width under the lid about 2.75 D = 66 mm.
  - Length from the pod tips to the rear end about 4.1-4.3 D = 98-104 mm (**guess** for the rear end, which is not visible; taken as the rear wheel's rear edge plus about 4 mm).
  - Height to the top of the lid about 1.25 D = 30 mm above the ground. Rail top about 1.05 D = 25-26 mm above the ground. Tyre top 24 mm above the ground.
- Colours:
  - Body: one matte, slightly glossy **sky blue**, FDM print with fine layer lines (about #3a8fe0, lighter where the light hits about #6fb0f0, shade about #2f6fc0).
  - Lid: **saturated lemon yellow**, smooth, slightly glossy (about #f2d21c).
  - Hubs and gears: a slightly warmer yellow (about #f0c800).
  - Tyres: **matte charcoal black** foam (about #1e1e1e).
  - Screws: **bright steel/chrome**.
  - Through the gap beside the lid: a little **red** wire insulation and **black** internals.

---

## 3. Part list (visible parts)

| # | Part | Count | Colour | Material (guess where marked) | Size (mm, guess where marked) |
|---|------|-------|--------|-------------------------------|-------------------------------|
| P1 | Chassis tub (centre box under the lid) | 1 | blue | FDM PLA/PETG (guess) | 66 W x about 95 L x about 24 H |
| P2 | Right side rail cover / top strip | 1 | blue (slightly lighter) | FDM | about 14 W x about 80 L x about 2-3 T |
| P3 | Left side rail cover | 1 | blue | FDM | mirror of P2 |
| P4 | Right front pod | 1 | blue | FDM, one piece with P1 (guess) | about 22 W x about 20 L x about 24 H |
| P5 | Left front pod | 1 | blue | FDM | mirror of P4 |
| P6 | Front floor plate / channel floor | 1 | blue | FDM, one piece with P1 (guess) | about 38 W x about 16 L x about 3 T |
| P7 | Lid / flipper plate (top panel) | 1 | yellow | FDM | about 38 W x about 80 L x about 4.5 T |
| P8 | Lid nose (bent-down front of P7) | 1 (same part) | yellow | FDM | about 38 W x about 20 slant x about 4.5 T |
| P9 | Hinge knuckles | 2 | blue | FDM | about 6 dia x about 7 long, pin hole about 1.5 |
| P10 | Hinge pin | 1-2 | not visible (steel, guess) | steel | about 1.5-2 dia |
| P11 | Wheels (tyre + hub) | 6 | black tyre / yellow hub | foam on a printed or moulded hub | 24 OD x about 9 wide |
| P12 | Wheel retaining screw | 6 | chrome | steel pan/button head | about M2-M2.5 |
| P13 | Wheel gears (on the hub's inner side) | 6 | yellow | moulded/printed | about 14-16 OD (guess) |
| P14 | Idler gears between wheels | 4 (2 per side) | yellow | moulded/printed | about 12-14 OD (guess) |
| P15 | Rail screws | 4 visible (2 per rail) | chrome | button/pan head M2 (guess) | head about 4 dia |
| P16 | Wires (seen in the lid gap) | some | red / black | silicone wire | about 1 dia |
| P17 | Drive motors | 2 (guess) | not visible | N20-type geared (guess) | inside P1 |
| P18 | Lid actuator | 1 (guess) | not visible | servo or N20 + linkage (guess) | inside P1 |
| P19 | Battery, receiver/ESC, switch | 1 each (guess) | not visible | | inside P1 |

---

## 4. Each part in detail

### P1: chassis tub (centre body)

- **Shape:** a rectangular box. Its top surface is hidden under the lid (P7) and under the rail covers (P2/P3).
  - The right side face is visible below the right rail cover. It is a vertical flat face that reads as two horizontal bands:
    - Upper band, about 2-3 mm tall: the rail cover edge.
    - A recessed slot in the middle, about 0.35 D = 8-9 mm tall, running the full length. The yellow gear train shows through it.
    - Lower band: the side wall bottom, about 0.2 D = 5 mm tall.
  - The slot depth is about 3-4 mm into the side (**guess**). The gears sit half inside it.
- **Width:** about 66 mm at the side faces. The wheel inner faces sit about 1-2 mm outside it, and the gears sit partly inside the slot.
- **Height:** bottom at about z = -10 (2 mm ground clearance, **guess**: the underside is not visible, but the pod lips nearly touch the ground). The side wall top, under the rail covers, is at about z = +11.
- **Interior:** a cavity. Through the gap between the lid and the right rail cover you see dark cavity space with red and black wires about 5-10 mm below the lid underside.
- **Rear:** not visible. Assumed to be a flat vertical rear wall, flush with the rail cover ends (**guess**).
- **Touches:**
  - P2/P3 on its top outer strips (face contact, screwed).
  - P4/P5 (one piece at the front corners, **guess**).
  - P6 (one piece).
  - The wheel axles through its side walls.
  - P7 does not touch it except at the hinge. The lid rests on internal stops or on the tub top edge (**guess**).

### P2/P3: side rail covers (top strips)

- **Shape:** flat rectangular strips, about 0.55-0.6 D = 13-15 mm wide and about 2-3 mm thick, running from the back of the pods (y about +34) to the rear end (y about -48).
  - The top is flat and level.
  - The outer and inner edges are square.
  - A thin **lighter border line** runs round the top face edge. It reads as a small step/rebate about 0.5-1 mm, as if the strip is a separate lid sitting in a recess of the tub rim, or the tub rim stands slightly above it. In the photo, the near (right) strip shows a lighter rim along its outer edge and front end.
- **Position:**
  - The outer edge is flush with the tub side face (x = +/-33).
  - The inner edge is at x about +/-19 to +/-20. It meets the lid's side edge with a **gap of about 4-6 mm on the right side**. Dark interior and wires show in that gap. On the left, the gap is hidden by the camera angle. Assume it is symmetric.
  - The top is at about z = +13.5 to +14. That is about 1.5-2 mm above the tyre tops and about one lid thickness (4.5 mm) below the lid top.
- **Front end:** butts against the rear of the pod's sloped face. The pod slope starts right where the rail ends (the rail top and the pod top edge are at the same height).
- **Screws (P15):** 2 per strip.
  - Front screw about 3 mm behind the pod slope's top edge (y about +31).
  - Rear screw about 0.15 x strip length from the rear end (y about -40, **guess**: the rear screw on the left strip shows at about that point).
  - Both on the strip centreline (x = +/-26).
  - Chrome **button/pan heads**, head diameter about 0.17 D = 4 mm, Phillips or hex recess (too small to tell), heads sitting proud by about 1 mm.
  - So 4 rail screws in total. They fasten the strip down into the tub wall/bosses (**guess**: M2 self-tapping into the print).
- **Overhang:** the strip's outer edge is at the tub side face. The gears in the side slot are below the strip and partly shaded by it.

### P4/P5: front pods (corner wedges)

- These are the most distinctive blue features: two **solid wedge blocks** at the front corners.
  - Inner face at x about +/-19.5 (the side walls of the central channel).
  - Outer face at about x = +/-41.5, flush with the tyre outer faces.
  - Each pod is about 0.9 D = 22 mm wide.
  - From the back of its slope (y about +34) to its tip (y about +54), about 20 mm long.
  - Its back merges into the tub and rail.
- **Faces of each pod:**
  1. **Top-front chamfer (largest face):** a flat plane falling from the rail top height (z about +14) at y about +34 down to about z = -6 at y about +54. That is about 55-60 deg from horizontal, at the full pod width. In the photo it is the big bright-blue lit parallelogram on each pod.
  2. **Front lip:** a short vertical face at the tip, from z about -10 up to about z = -6, about 3-5 mm tall, the full pod width minus the corner bevel. It reads as a narrow darker band right at the ground.
  3. **Outer corner bevel:** the outer-front vertical edge is bevelled off by a plane at about 45 deg in plan, with legs about 5-7 mm. Where this bevel meets the top chamfer it makes a triangular facet. So the pod tip looks faceted: a large slope, a small triangular corner face, and a narrow lip.
  4. **Outer side face:** vertical. It runs back from the bevel to the front tyre. It stops about 2 mm ahead of the front tyre's front (the front tyre sits just behind the pod: gap pod-to-tyre about 1-3 mm).
  5. **Inner face:** vertical, flat, facing the channel. It is the full height from the floor plate (z about -7) to the pod top edge.
- **Behind the pod, outboard of the tub (x 33..41.5):** the pod does not run back past the front tyre. Above the front tyre it ends, and the tyre sits in the notch between the pod's rear face and the tub side.
- **Pod vs wheel:** the pod's outer face lines up with the tyre outer faces (within about 1 mm). Seen from the front, the pods hide the front tyres completely. They act as wheel guards for the front wheels.
- **Fastening:** printed as one piece with the tub (**guess**: no seam or screw visible on the pods).

### P6: front floor plate / channel floor

- A **thin flat blue plate at ground level** between the two pods' inner faces.
  - x from -19.5 to +19.5.
  - From the tub front wall (y about +38) to the pod tips (y about +54).
  - Top at about z = -7, bottom at about z = -10. Thickness about 3 mm.
- Its front edge is flush with the pods' front lips. Its top surface is flat with a few print specks.
- It carries the two **hinge knuckles (P9)** on its top surface, about 4-8 mm behind its front edge (**guess**: they look about one third of the way back along the floor).
- Above the floor between the pods is **open**: no front wall. You see straight in to the lid nose.

### P7/P8: lid / flipper plate and its nose (yellow)

- **Plan:** a rectangle about 1.6 D = 38 mm wide (x +/-19) and about 3.3 D = 80 mm long on top (y from about -40 to about +40).
- **Thickness:** about 4.5 mm. The visible front and side edges show a thick slab.
- **Top:** flat, at z about +18.5. It is the highest point of the robot.
- **Nose (P8):** at the front, the plate **bends down** in one sharp bend line at y about +40, at about 60-65 deg below horizontal, into a sloped nose about 20-23 mm long on the slant. It ends at about z = -5 to -6, y about +50, just above the floor plate.
  - The bend is a crisp edge, not a radius.
  - The nose is the same width as the top.
  - The nose's lower edge has **two tabs/cheeks** at its outer corners. The outer edge strips of the nose continue down the inside of the pods' inner faces with about 1 mm clearance to each pod.
  - Between the tabs the lower edge is cut back so the two **blue knuckles (P9)** show **in front of** the yellow, nested in the cut-outs.
  - The nose and the knuckles form a simple **knuckle hinge**: yellow tab, blue knuckle, (centre), blue knuckle, yellow tab.
- **Sides:**
  - The lid's side edges are about 0.5-1 mm inside the pod inner faces at the front.
  - Further back, the gap to each rail cover is about 4-6 mm, wider than at the pods because the lid is narrower than the channel between the rails.
- **Mechanism (guess):**
  - The hinge axis is along x at the bottom front (about y +48, z -5).
  - The lid is a **front-hinged flipper/lifter panel**. A motor inside drives it, and its **rear end lifts**.
  - Both readings fit the photo: a self-righting rear flipper, or an opponent-lifting plate.
  - The current CAD models a revolute lid with its pivot at the rear and a separate static nose. That **differs** from the photo. The photo's pivot is at the **front-bottom knuckles**.
- **Fastening:** only through the hinge pin(s). There are no screws on the lid.

### P9/P10: hinge knuckles and pin

- **Two blue cylinders**, each about 0.25 D = 6 mm diameter and about 0.3 D = 7 mm long, axis along x, lying on the floor plate P6.
- They sit at about x = -12 and x = +5 (as seen: one near the left pod, the other just right of centre; **guess**: likely symmetric at x about +/-9).
- Each has a **small dark pin hole** (about 1.5 mm) on its end face, so a steel pin or M1.6 screw runs through it (**guess**).
- They are attached to the floor plate. They are printed blocks (a cylinder on a small web), part of P6 (**guess**).
- Gap knuckle-to-lid tab: about 0.5 mm.

### P11-P14: wheels and gear train

- **Tyres:** 6 black foam tyres, each with a smooth, slightly porous surface.
  - Outer diameter 24 mm (yardstick), width about 0.38 D = 9 mm, tyre wall (radial) about 0.15 D = 3.5 mm.
  - Square shoulders, slightly rounded.
- **Hubs:** yellow, **deep-dish** on the outer face.
  - Rim outer diameter about 0.7 D = 17 mm.
  - The dish is recessed about 3-4 mm.
  - At the centre is a **chrome screw head (P12)**, about 4 mm diameter, holding the wheel on its axle.
- **Wheel gear (P13):** on the inner side of each hub is a **yellow spur gear**, about 12-14 teeth, OD about 0.6 D = 14-15 mm, width about 3 mm. It sits in the side slot of the tub.
- **Idler gears (P14):** between each pair of neighbouring wheels, a yellow spur gear the same size meshes with both wheel gears. They are visible between front and middle, and between middle and rear, on the right side.
  - So the drive is **one motor per side driving a 5-gear chain**: wheel-idler-wheel-idler-wheel (**guess**: the motor output gear position is not visible; likely on the middle wheel or an idler).
- **Axle positions (right side; left mirrored):**
  - Rear wheel y about -30, middle y = 0, front y about +30. Pitch about 1.2-1.25 D = 29-30 mm.
  - Axle height z = 0 (wheel centre 12 mm above the ground).
  - Tyre inner face about 1-2 mm outside the tub side (x about +34). Tyre outer face at x about +41.5-43.
- **Gaps:**
  - Tyre-to-tyre about 5-6 mm.
  - Front tyre to the pod's rear face about 2 mm.
  - Tyre top to rail cover top: the rail is about 1.5-2 mm higher.
  - Tyre outer face to pod outer face: about 0-1 mm.
- **Wheels inside or outside the body:** **outside**. The tyres are fully outboard of the tub sides. Only the front pods extend out to the tyre plane, and only ahead of the front wheels.

### P16: wires

- In the gap between the lid and the right rail cover (about 4-6 mm wide), there are:
  - a **red** wire loop (about 1 mm) at about mid-length
  - black wire/insulation and dark internals, about 5-10 mm down
- They run from the battery to the electronics (**guess**). No wires are outside the body.

### Hidden internals (all guesses)

- Two N20-size geared motors, one per side, along the side walls behind the gear slots.
- A lid actuator in the rear half: a micro servo or a third N20 with a crank, pushing the lid underside.
- A small 2S LiPo and an antweight receiver/ESC in the centre.
- The power switch is not visible. It is on the underside or rear face (**guess**).

---

## 5. Per-view descriptions

### 5.1 Photo view (front right, about 30-35 deg elevation, about 35 deg off the front axis)

Read left to right in the image:
1. The **left pod**: big lit slope, faceted outer corner, dark lip at the ground.
2. Then the **channel**: blue floor, two blue knuckles, the yellow nose sloping up-back to the bend.
3. Then the **right pod**: its slope and its outer bevel facing the camera.
4. Then, receding up-right, the **right side**: front, middle and rear tyres with yellow dish hubs and chrome centre screws, the yellow gear train visible between and behind the tyres in the side slot, and the blue rail cover strip above with its two chrome screws and lighter rim.

Above, the **yellow lid** fills the centre top as a large parallelogram. Its front edge (the bend) runs left to right across the image at about one third of its height. To its right is the dark gap with a red wire, then the right rail cover. To its left, the left rail cover with two chrome screws. Behind it, the three left tyres stick up above the left rail as black arcs with yellow hub edges.

### 5.2 Front view (inferred, orthographic)

- Width about 83 mm.
- Two pod blocks at the outer thirds, each about 22 mm wide, with slopes rising to rail height.
- In the middle third, the channel (about 39 mm wide) with the floor plate at the bottom (3 mm), the two knuckles on it, and behind them the yellow nose rising to the lid at about 18.5 mm.
- The tyres are hidden behind the pods (same width).

### 5.3 Top view (inferred)

- Centre: a yellow rectangle 38 x about 80 mm plus the nose (seen foreshortened, about 10 mm deep in plan) ending at y about +50.
- Each side of the lid: a 4-6 mm dark gap, then a blue rail strip about 14 mm wide with 2 screws.
- Outside the strips: the three tyres per side (9 mm wide, at y -30/0/+30).
- At the front corners: the pods, extending from the rails/tyres to y about +54, with the outer front corners bevelled.
- Between the pods at the front: the blue floor plate, visible to y about +54.

### 5.4 Side view (right, inferred)

- Ground line, three tyres touching it.
- The body bottom at about 2 mm clearance.
- The side shows a horizontal slot with gears between and behind the tyres, and the rail top at about 26 mm above the ground.
- The lid adds 4.5 mm on top (about 30.5 mm above the ground).
- At the front, the pod profile: rail height, then a straight slope down to a short lip ahead of the front tyre by about 10-12 mm.
- The rear face is vertical (guess).

### 5.5 Rear view (not visible, guesses)

- A flat blue rear wall over the full width of the tub, 66 mm wide and about 24 mm tall, with the lid's rear edge at the top and the rear tyres outboard.
- Possibly the switch and charge plug here.

---

## 6. Contact and gap matrix (main parts)

| A \ B | Tub P1 | Rail P2/3 | Pod P4/5 | Floor P6 | Lid P7/8 | Knuckle P9 | Wheel P11 | Gear P13/14 |
|---|---|---|---|---|---|---|---|---|
| Tub | - | face contact (top strips), screwed | one piece (guess) | one piece (guess) | none, or a rest on the internal edge (guess) | via the floor | axle through the side wall, about 1-2 mm side gap | in the side slot, about 0.5-1 mm clearance |
| Rail | - | - | butts against the pod slope top edge, flush | none | 4-6 mm side gap | none | rail about 2 mm above the tyre top, about 0-1 mm plan overlap with the tyre inner edge | above the gears, shades them |
| Pod | - | - | - | inner face meets the floor (one piece) | about 0.5-1 mm gap to the lid nose tabs | about 3-5 mm | about 2 mm gap pod rear face to front tyre | none |
| Floor | - | - | - | - | about 1 mm above the floor at the nose bottom | knuckles sit on it (one piece) | none | none |
| Lid | - | - | - | - | - | hinge (pin through), about 0.5 mm between knuckle and tab | none | none |
| Wheel | - | - | - | - | - | - | tyre-tyre about 5-6 mm | wheel gear on the hub's inner side (one piece, guess) |

---

## 7. Fasteners summary

- **4 visible rail screws**: chrome button/pan heads about M2, 2 per rail strip, at about y +31 and about y -40 on x = +/-26, driven straight down into the tub.
- **6 wheel screws**: chrome pan heads about M2-M2.5 at each hub centre, along x into the axle/motor shaft or a printed stub.
- **Hinge pin(s)**: 1 long pin through both knuckles and the nose tabs (guess), or 2 short screws (guess). Diameter about 1.5-2 mm.
- No screws on the pods, lid or floor.

---

## 8. Mechanism summary

1. **Drive:** six-wheel drive, all 6 wheels geared together per side by a spur train (wheel-idler-wheel-idler-wheel). Probably one N20 motor per side (guess). Skid steer.
2. **Weapon:** the yellow lid is a hinged plate. The hinge is at the front-bottom knuckles (axis along x at about y +48, z -5), so actuation lifts the rear of the lid (guess). The pods and floor make a low front wedge that gets under opponents. The yellow nose slope continues the wedge line between the pods.
3. **Protection:** the front tyres are fully shielded from the front by the pods. The side and rear tyres are exposed.

---

## 9. Size ratios (for checking a rebuild)

- Lid width / body (rail-to-rail) width = 38 / 66 = 0.58.
- Rail strip width / lid width = 14 / 38 = 0.37.
- Pod width / lid width = 22 / 38 = 0.58.
- Pod length (slope run) / D = 20 / 24 = 0.83.
- Pod lip height / pod height = 4 / 24 = 0.17.
- Lid thickness / D = 4.5 / 24 = 0.19.
- Lid top above rail top = 4.5 mm (one lid thickness).
- Rail top above tyre top = about 2 mm.
- Wheel pitch / D = 30 / 24 = 1.25.
- Overall length / overall width = about 100 / 83 = 1.2.
- Overall height / overall length = about 30 / 100 = 0.30.

---

## 10. Differences seen in the current CAD (for the fixer)

- Pivot position: the CAD pivots the lid at the rear (y -38). The photo hinges it at the front bottom (knuckles). This is kept for now (mechanism change, out of scope). Noted here.
- Not modelled: the gear train, the rail-strip rebate, the hinge knuckles. These are optional details.
- Modelled: the tyres are black with yellow hubs.
- Modelled: the pods with a top chamfer and an outer bevel, the open channel with a floor, and the nose sloping to the floor.

---

## 11. Coordinate frame (used everywhere in this file)

- Right-handed frame, in mm.
- Origin: the body centreline (x = 0), at the middle-wheel axle (y = 0), at axle height (z = 0).
- +x is the robot's right, +y is forward (pods/hinge end), +z is up.
- The ground plane is z = -12.
- Photo pixel coordinates (u, v): u to the right, v down, in the original 1660 x 1128 image.

## 12. Every part in all dimensions (mm; G = guess)

| Part | Along x | Along y | Along z | Thickness / radii / angles | Placement (min..max) |
|---|---|---|---|---|---|
| Tub P1 | 66 | 82 (y -48..+34) plus the front wall to +38 | 24 (z -10..+14) | wall about 2.5 (G); side gear slot 8.5 tall x 3.5 deep, z -3..+5.5 (G) | x -33..33, y -48..38, z -10..14 |
| Rail cover P2 (right) | 14 | 80 | 2.5 | rebate 0.75 x 0.75 round the top edge (G); square edges, r = 0 | x 19..33, y -46..+34, z 11.5..14 |
| Rail cover P3 (left) | mirror | | | | x -33..-19 |
| Pod P4 (right) | 22 | 20 (on top 0) | 24 | slope plane through (y 34, z 14) and (y 54, z -6): angle atan(20/20) = 45 deg on the 20 x 20 run/rise (photo reads 55-60 deg; see the consistency check); lip 4 tall; outer bevel 45 deg plan, legs 6 | x 19.5..41.5, y 34..54 (outboard part x 33..41.5 only for y >= 44), z -10..14 |
| Floor P6 | 39 | 16 | 3 | flat | x -19.5..19.5, y 38..54, z -10..-7 |
| Lid top P7 | 38 | 80 | 4.5 | square edges | x -19..19, y -40..40, z 14..18.5 |
| Lid nose P8 | 38 | 10 in plan | 21 drop | slant length sqrt(10^2 + 21^2) = 23.3; angle atan(21/10) = 64.5 deg below horizontal | from the line (y 40.5, z 16) to (y 50.5, z -5) |
| Knuckle P9 (x2) | 7 | 6 dia | 6 dia | cylinder r = 3, axis x; bore r = 0.75 | centres (x +/-9 G, y 47, z -4) |
| Tyre P11 (x6) | 9 | 24 dia | 24 dia | torus-like band: outer r = 12, inner r = 8.5; shoulder fillet r about 1 | centres (x +/-38, y -30/0/+30, z 0) |
| Hub (x6) | 9 | 17 dia | 17 dia | dish depth 3.5, dish inner r = 7; centre boss r = 2 | same centres |
| Wheel gear P13 (x6) | 3 | 14.5 OD | 14.5 OD | 13 teeth (G), module about 1 (G): pitch d = 13 | x +/-32.5..+/-35.5 |
| Idler P14 (x4) | 3 | 14.5 OD | | 13 teeth (G) | centres (x +/-34, y +/-15, z about -2 G) |
| Rail screw P15 (x4) | 4 dia head | | 1.2 head | button head r = 2, dome | (x +/-26, y +31 and -40, z 14..15.2) |
| Wheel screw P12 (x6) | 1.5 head | 4 dia | 4 dia | pan head | on each axle, outer face of the dish |

## 13. Curves and planes as maths

- **Tyre outline (side view):** a circle (y - yc)^2 + (z - 0)^2 = 12^2, with yc in {-30, 0, 30}. In the photo view it projects to an ellipse with semi-axes about 12 (vertical, times cos 30 = 10.4 apparent) by 12 x sin(about 35 deg) = 6.9 apparent.
- **Hub rim:** a circle of r = 8.5 about the same centres. Dish floor: a circle of r = 7 at 3.5 mm inside the outer face.
- **Pod slope plane (right pod):** z = 14 - (y - 34) x (20 / 20), so z = 48 - y for y in [34, 54], x in [19.5, 41.5]. Where it meets the lip plane y = 54, z = -6.
- **Pod outer bevel plane:** x + y = 41.5 + 48 = 89.5 for the corner from (41.5, 48) to (35.5, 54) (legs 6). The left pod mirrors it: -x + y = 89.5.
- **Lid nose centre line:** z = 16 - 2.1 x (y - 40.5) for y in [40.5, 50.5]. Slope -2.1 means 64.5 deg.
- **Gear pitch circles:** r = 6.5 about each wheel and idler centre. Neighbouring centres are 15 apart, so 2 x 6.5 = 13 < 15. That means the wheel gear and idler need r_p about 7.5 each to mesh (G). Reconciled: gears about 16 OD (see the consistency check).
- No splines: every body edge is straight.

## 14. Each feature measured independent ways

| Feature | (a) Dimension from the D = 24 scale | (b) Ratio to another part | (c) Photo pixels (u, v) | (d) Frame coordinates |
|---|---|---|---|---|
| Tyre dia | 24 (yardstick) | about 0.63 x lid width | front-right tyre ellipse height about 260 px (v 650..910) at its centre about (1180, 780) | outer r 12 about (38, 30, 0) |
| Wheel pitch | 30 | 1.25 D | centres about (1180, 780), (1340, 650), (1520, 520): steps of about 206 px | y = -30, 0, +30 |
| Lid width | 38 | 1.6 D; 0.58 x body | front bend edge from about (370, 600) to (700, 690): 342 px along x; the x axis is about 9 px/mm at this depth, so 38 mm | x +/-19 |
| Lid length | 80 | 3.3 D | left edge from the bend about (370, 600) to the rear corner about (780, 80): 662 px along y; about 8.3 px/mm, so 80 | y -40..40 |
| Rail width | 14 | 0.37 x lid | right rail across about 120-140 px at mid-length | x 19..33 |
| Lid-rail gap | 5 | 0.13 x lid | about 40-50 px dark band right of the lid | x 19..24 visible gap (G: this means the rail inner edge is at 24, not 19; see the check) |
| Pod width | 22 | 0.58 x lid | left pod front from about (20, 620) to (370, 700): 360 px | x -41.5..-19.5 |
| Pod slope length | 28 (slant) | 1.2 D | right pod slope from the top edge about (700, 690) to the lip about (760, 900): about 220 px | (34, 14) to (54, -6) |
| Pod lip | 4 | 0.17 D | dark ground band about 30-40 px | z -10..-6 |
| Lid thickness | 4.5 | 0.19 D | edge band about 40 px at the front bend | z 14..18.5 |
| Knuckle dia | 6 | 0.25 D | about 60-70 px at about (380, 640) and (600, 760) | r 3 |
| Rail screw head | 4 | 0.17 D | about 35 px | (+/-26, 31 / -40) |
| Body height (rail top) | 26 above the ground | 1.08 D | right side from the rail top about (1000, 380) to the ground about (1010, 690)... minus the tyre: about 280 px vertical over 0.87 cos | z -12..14 |

## 15. Consistency check (conflicts and reconciled values)

1. **Pod slope angle.**
   - The photo appearance reads 55-60 deg.
   - A run of 20 mm (y 34 to 54) with a rise of 20 mm gives 45 deg.
   - Foreshortening at about 32 deg elevation makes slopes facing the camera look steeper.
   - **Reconciled:** the true slope is about 45-50 deg, a run of 18-20 over a rise of 20. The CAD uses a run of 20 / rise of 18 (y 34 to 54, z 14 to -6 with a 4 mm lip): 42 deg. Acceptable.
2. **Lid-to-rail gap versus the rail inner edge.**
   - The rail is about 14 wide, the lid 38, the body 66. That gives 66 = 38 + 2 x 14, so no room for a 5 mm gap.
   - Either the rails are about 11 wide or the body is about 72 wide.
   - The pixel ratio of rail to lid (about 0.33-0.37) and the gap visible only on the right point to: rail about 11-12, gap about 2-3 on each side.
   - **Reconciled:** body 66, lid 38, gap 2.5, rail 11.5. The CAD keeps the lid at 38 and the body at 66, with no gap modelled (the top skin is continuous under the lid).
3. **Wheel pitch versus gears.**
   - A 30 mm pitch with 14.5 OD gears does not mesh through one idler: it needs 2 x (wheel pitch radius + idler pitch radius) = 30, so radii of 7.5 each, about 16 OD.
   - **Reconciled:** gears about 16 OD, module 1, 15 teeth (G).
4. **Overall length.**
   - The rear is not visible.
   - From the pitch: rear tyre rear edge y = -42, plus a wall of 4-6, gives -46 to -48.
   - From the lid length (80) plus the nose (10): y -40 to +50.
   - **Reconciled:** body y -47.5..+54, 101.5 long.
5. **Camera.**
   - The REFERENCE label is azimuth 30 / elevation 45.
   - The pixel axes say about 55-60 / 32.
   - The checker best is 60 / 25.
   - **Reconciled:** about 58 / 30. The label is wrong, but that file is collector-owned and is not edited.
6. **Lid hinge end.**
   - The knuckles are at the front bottom (seen). The CAD pivot is at the rear (y -38).
   - **Reconciled:** the photo wins for looks. The CAD mechanism is kept and flagged as a difference.

---

## 16. Why the designer did it (per part)

- **Tub P1 (plain rectangular box)**
  - Fight: a low centre of gravity and a flat top resist being flipped. Square walls take side hits.
  - Build: the easiest FDM print (flat bottom on the bed, no supports). One part holds everything, so it is cheap and quick to reprint.
  - Weight: the hollow tub with 2-2.5 mm walls keeps it under 150 g with six wheels.
  - Repair: the top strips come off with 4 screws for access.
- **Rail covers P2/P3 (separate screwed strips)**
  - Build: they let the tub print open-topped (no bridging over the gear slot) and give access to the gear trains and motors.
  - Fight: they cap the gear slot so debris and opponents' forks cannot jam the gears.
  - Repair: 2 screws each.
  - Looks: the rebate hides the seam.
- **Front pods P4/P5 (chamfered blocks covering the front tyres)**
  - Fight: wedge faces deflect hits and ride opponents up. They shield the front tyres from spinners and pushers. The outer bevel stops the corner catching on walls.
  - Build: they print as part of the tub (45-60 deg slopes need no support).
  - Weight: small, solid or with infill.
- **Floor plate P6**
  - Fight: a low leading edge, so the nose gets under opponents. It carries the hinge load into the tub.
  - Build: it is the first layers of the tub print, so it costs nothing.
- **Lid / flipper P7/P8 (yellow)**
  - Fight: the active weapon. A big flat panel flips or lifts opponents or self-rights the robot. The nose continues the wedge. The contrasting colour is for show and branding ("golden nuggets").
  - Build: a flat print with the nose printed as the bend (or as a separate part bonded on, G). The knuckle hinge is printable with a steel pin.
  - Repair: one pin to remove.
- **Knuckles P9 and pin P10**
  - Fight: a low hinge keeps the pivot under opponents. A steel pin takes the shock.
  - Build: printed on the floor plate. A drill-through pin hole.
- **Wheels P11, outside the tub, 6 off**
  - Fight: 6WD gives traction and pushing power, keeps driving if one wheel is lifted, and has no high-centring.
  - Build: cheap foam tyres on stock hubs.
  - The outboard tyres keep the tub narrow, so more internal room.
- **Gear train P13/P14**
  - Fight: all six wheels driven from 2 motors (saves mass and cost over 6 motors) and torque is shared.
  - Build: stock or printed spur gears on pins. The side slot keeps the train thin.
- **Screws P12/P15:** standard M2 hardware, self-tapping into plastic. Fast to service.
- **Colours:** blue and yellow. Probably a team or sponsor scheme and good visibility on camera (G).

## 17. Unseen and inner parts (guesses with confidence)

| Part | Size (mm) | Position (frame above) | Confidence | Notes |
|---|---|---|---|---|
| Drive motors (2) | N20 12 x 10 x 34 | along y inside each side wall, x +/-24, y -10..+24, z -3..+7 | medium | One per side, output gear meshing with the middle wheel gear through the side wall. |
| Motor clamps | printed saddles 14 x 12 x 8 | over each motor, screwed to the tub floor with 2 x M2 | low | Alternatively press-fit pockets. |
| Idler pins | steel 2 dia x 8 | through the side wall at y +/-15, z -2 | medium | Idlers spin on them. |
| Wheel axles | steel 3 dia x 12 or M3 screws | through the side wall at y -30/0/30, z 0 | medium | The centre screw P12 retains each wheel. |
| Lid actuator | micro servo 23 x 12 x 22 (9 g) or N20 + crank | centre rear, y -30..-10, under the lid | low | The horn pushes the lid underside about 30 mm behind the hinge (if the hinge is at the front). |
| Battery | 2S 180-300 mAh, 30 x 18 x 10 | centre, y 0..+25, z -8..+2 | medium | Taped/strapped to the floor. |
| Receiver + dual ESC | 25 x 18 x 5 (combined antweight board, e.g. a Malenki-type) | centre, y -20..0, stacked on the floor | medium | |
| Power switch / link | 12 x 6 slide switch or removable link | rear wall or underside | low | AWS rules require it to be reachable. |
| Wiring path | battery -> switch -> board -> motors along the floor | the red lead seen in the right gap at mid-length is the battery-to-switch run | medium | |
| Internal ribs | 2 mm ribs between the motor bays | x +/-15 | low | |
| Lid stops | small ledges on the tub inner walls at z 13.5 | the lid rests on them when closed | low | |
| Hidden screws | 2-4 M2 under the lid (lid hinge bracket or tub joins) | | low | |

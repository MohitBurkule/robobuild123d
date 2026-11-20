# I Saw That: full rebuild description from reference photos

Source photo (cut out onto white by the AWS wiki):
- `robots/i_saw_that/reference/i_saw_that_.aws76.webp`: AWS 76, native 1634 × 1524 px. It shows the robot from the **front-right, high**: the camera is about 25–30° above the floor and about **55–65° round from the front toward the robot's right side** (so the right side is seen more squarely than the front). The phone was close, so there is **strong perspective**: the fork tips (nearest the camera) look much bigger than the rear wheel area. Visible: the whole front jaw with both forks, the right side of the body, the top lid, the right wheel, the top of the left wheel, the mast and the whole face of the saw disc. Not visible: the left side, the rear wall, the underside, the back face of the disc and the motor behind it.

Only one photo exists, so the left side, rear and underside are inferred by symmetry and by function. Everything stated as fact is read from the photo. Anything inferred is marked **(guess)**. Dimensions in mm are **estimates**. The best absolute scale in the photo is the **saw disc**: its printed label reads "Ø50×10 mm … 80 m/s … max 30600 min⁻¹ … Carbide Multi Wheel … Swiss Made", i.e. a **Bosch Carbide Multi Wheel, 50 mm diameter with a 10 mm bore**. (Check: π × 0.050 m × 30600 / 60 s = 80.1 m/s, matching the printed 80 m/s.) Everything else is scaled from that disc, from the AWS 150 g / 101.6 mm cube limit, and from the project kit draft (`kit.json`: body 62 × 60 × 28, two wheels r 13 × 10 at y −18, disc at x −8 with axis along X). Ratios are given against **W = body width ≈ 60 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the forks), **+Z** = up. Units mm.
- **Origin O** = the point on the floor (z = 0) directly under the centre of the **blue body tub's** footprint (mid-width, mid-length of the blue box, not counting the black jaw).
- **Front** = the end with the two steel forks and the black jaw. In the photo the front points to the lower-left. The right side faces the lower-right of the photo. The rear (with the wheels) is to the right.
- In the photo the +Y direction runs toward the lower-left (about 25° below horizontal), +X toward the lower-right (about 40° below horizontal), +Z straight up.

| ID | Part |
|---|---|
| BT | blue body tub (rear electronics box) |
| LID-F, LID-R | blue isogrid lid plates (front-left plate and rear-right plate) |
| WIN | rectangular window in the lid (over the arm drive) |
| CLP | small blue printed cable clip/guide block on the lid |
| SW | power switch on a small green PCB on the lid |
| LED | small dark flat component beside the switch (indicator or link, guess) |
| S-LID | black Phillips pan screws on the lid |
| JW | black printed front jaw frame (one print: front wall + two side walls + floor) |
| FW | black front wall of the body (part of JW), with the arm slot |
| SL | vertical arm slot in FW |
| JS-L, JS-R | jaw side walls (sloped, with saw-tooth top edges) |
| TT-L, TT-R | printed saw teeth on the jaw side wall tops |
| JF | jaw floor plate (channel between the side walls) |
| FB-L, FB-R | blocks/posts inside the jaw that hold the fork blades |
| FK-L, FK-R | steel fork blades (flat strips with barbed points) |
| S-JW | black socket screws on the jaw side walls |
| AR | black mast / weapon arm (curved post) |
| SLV | black braided sleeve/wrap on the arm |
| PW | three motor phase wires running up the arm |
| WM | weapon motor (small brushless outrunner at the top of the arm, hidden behind the disc, guess) |
| HB | blue printed disc hub/clamp with 4 socket screws |
| S-HB | 4 small socket cap screws in the hub |
| DS | Bosch Carbide Multi Wheel saw disc, Ø 50 |
| AS | arm drive (servo or gearmotor inside the body, seen only through WIN, guess) |
| WH-L, WH-R | two rear drive wheels |
| M-L, M-R | drive gearmotors (hidden, guess) |
| BAT, ESC, RX | battery, ESCs, receiver (hidden; some coloured parts glimpsed through the lid holes) |

---

## 1. Overall description in one paragraph

I Saw That is a **two-wheel "hammer-saw"/overhead-saw robot with a forked trapping jaw**. At the back is a **compact blue printed box** about 60 mm wide, 45 mm long and 28 mm tall, covered by **blue isogrid (triangular-hole) lid plates** held with black Phillips screws, with a **slide switch on a green PCB** at the rear-right of the lid. Two **black knurled, three-spoke wheels** (about Ø 33 mm) sit outboard at the rear corners. Bolted to the front of the box is a **black printed jaw**: a front wall with a vertical slot, two **tall triangular side walls whose sloped top edges carry rows of printed saw teeth**, and a **flat floor** between them, forming an open-fronted U about 52 mm wide inside. Under/along each side wall a **thin steel fork blade with a barbed, harpoon-like tip** reaches forward beyond the plastic. From the slot in the front wall a **curved black arm, wrapped in a braided sleeve with three motor wires alongside it**, rises about 50 mm and carries at its top a **small brushless motor (hidden) driving a 50 mm black Bosch carbide-grit cutting disc** in a vertical plane, held on by a **blue printed hub with four tiny socket screws**. The intended action is clear: the forks get under or trap the opponent in the jaw, and the arm **swings the spinning saw forward and down** into it **(arm actuation is a guess, medium-high)**.

---

## 2. Part-by-part description

### 2.1 Blue body tub (BT)
- **Shape**: a rectangular box, about **60 mm wide (x ±30) × 45 mm long (y −25 to +20) × 26 mm tall (z 2 to 28)** to the lid top. The vertical corners are square with small (≈ 1 mm) radii. The **front-right vertical edge**, where blue meets the black jaw, shows a narrow **chamfer/fillet strip about 3 mm wide** running down the full height, and at the bottom a small **sloped foot chamfer** (a 45° triangle about 4 mm) that blends into the black jaw side wall.
- **Colour/material**: **royal blue** FDM print (PLA or PETG), matt, with visible horizontal layer lines on the right wall and slightly rough top-layer texture.
- **Right side wall**: plain flat blue face about **45 × 26 mm**, with **no visible screws**, and the right wheel immediately behind its rear half. Probably the axle hole of the right motor is behind the wheel **(hidden)**.
- **Front**: the blue tub's front is covered by the black front wall FW (section 2.7). The seam between the blue tub and black FW is a clean vertical line at the front-right corner, so the jaw is a **separate print bolted to the tub**.
- **Rear wall / left wall / floor**: not visible. Presumed plain, with the left wheel mirror-imaged **(guess)**.
- **Lid seat**: a **thin white/silver line** runs along the top edges of the walls just under the blue lid plates (seen along the right edge and along the front edge of the rear plate). This is most likely a **thin sheet of white/clear plastic or foam tape** between lid and tub, or the white edge of a polycarbonate inner lid **(guess)**.

### 2.2 Lid plates (LID-F, LID-R)
- **Shape**: two flat **blue isogrid plates**, each about **2 mm thick**, sitting on the tub. The pattern is a regular **triangular lattice**: rows of equilateral-triangle holes (side about 5 mm) alternating point-up and point-down, separated by ribs about **1.5 mm** wide, i.e. a hole pitch of about **6.5 mm** along each row and about **5.6 mm** between rows. The lattice runs parallel to the robot's X and Y axes.
  - **LID-F** (front-left plate, seen farther from the camera): covers about x −30 to +2, y −20 to +20, and its front-left corner carries a screw. Its right edge stops at the arm slot.
  - **LID-R** (rear-right plate, nearest the camera): covers about x +2 to +30 (and wraps behind the window), y −25 to +20. It has an **L-shaped notch** in its front-left region that forms the window WIN. Its front-right corner is cut with a small 45° chamfer (about 3 mm).
  - Together the plates leave a **slot about 8–10 mm wide** over the arm (in line with SL) and the **window WIN** beside it.
- **Holes**: some lattice holes show **coloured internal parts** (green, red, white) beneath, i.e. a PCB and wires under the lid.
- **Screws (S-LID)**: **black Phillips pan heads**, head Ø about **4 mm** (M2 or M2.5). Seen positions (photo native px → est. robot mm):
  - (647, 677) → front-left corner of LID-F, about (−27, +18).
  - (1173, 737) → rear-right area of LID-R, about (+18, −20), just in front of the switch.
  - (1060, 867) → middle of LID-R, about (+10, +2).
  - (1053, 977) → front-right corner of LID-R, about (+27, +17).
  - (980, 800) → inside the window, on a lower level (a screw on the arm-drive mount or servo horn, about (+2, +5), z ≈ 22).
  - Probably 2 more on the unseen rear-left corner **(guess)**: total about **6 lid screws**.

### 2.3 Lid window (WIN)
- A **rectangular opening about 22 mm (X) × 10 mm (Y)**, at about x −6 to +16, y +2 to +12, beside the arm slot. Through it: a **dark interior**, a **black screw head on a lower level** (z ≈ 22), and a **thin bright curved edge** (a servo horn or a metal bracket edge). This is consistent with an **arm-drive servo output** or the arm's **pivot shaft** sitting just under the lid **(guess)**.

### 2.4 Cable clip block (CLP)
- A small **blue printed cube about 7 × 7 × 8 mm tall** standing on the front edge of LID-R, right beside the arm slot (about x +2, y +14, z 28–36), with a **round hole about 3 mm** through its side (axis along Y). It is next to where the arm wires leave the body.
- **Function (guess)**: a **wire guide/strain relief** for the phase wires going up the arm, or a **hard stop for the arm** in its raised position (the arm rests against it when upright). The second seems likely because the arm leans against this corner in the photo **(guess, medium)**.

### 2.5 Power switch (SW) and LED
- A **small green PCB about 10 × 6 mm** mounted on the rear-right of the lid (about x +22, y −16, z 30), carrying a **black slide-switch lever** about 2 × 2 × 4 mm sticking up/out. A short **black wire** or flat leg runs from it back into the lid. A small **dark flat rectangle** (about 6 × 3 mm, black) lies beside it on the lid: possibly a **LED/indicator board** or a **removable link** **(guess)**.
- The switch is on **top** of the robot, which is unusual (easy to hit), but it is at the rear corner where the arm and opponents rarely reach.

### 2.6 Black jaw frame (JW)
A single black FDM print (or a few bolted parts) bolted to the front of the blue tub. It contains FW, JS-L, JS-R, JF and the fork blocks.

### 2.7 Front wall (FW) and arm slot (SL)
- **FW**: a vertical black wall across the front of the body, about **60 mm wide × 26 mm tall × 4 mm thick**, at y ≈ +20 to +24, its top flush with the blue lid. It looks flat, with print layer lines horizontal.
- **SL**: a **vertical slot** in FW about **6–8 mm wide**, from the top of FW down about **14 mm**, at **x ≈ −9**, through which the arm passes. Inside the slot a second, inner wall face is visible about 3 mm behind, so the slot is a recess through a double wall **(guess)**.
- On the left end of FW, a tall **black post/block** (about 6 × 6 × 26 mm) stands at the junction with JS-L, carrying **two small black screws** facing forward (at native px (632, 777) and (633, 893), i.e. about z 20 and z 8). These screws probably fix the jaw to the blue tub **(guess)**. The right end presumably has the same (hidden by the right wall).

### 2.8 Jaw side walls (JS-L, JS-R) and printed teeth (TT-L, TT-R)
- **Shape**: each side wall is a **vertical plate about 4 mm thick** (x from ±26 to ±30), with a **right-triangle/trapezoid side profile**: full body height (z ≈ 26) at the rear where it meets FW, the top edge then running **forward and down at about 30–35°** to the front, ending at the fork about **45 mm** ahead of FW. Total wall length about **48 mm** (y +20 to +68).
- **Saw teeth (TT)**: along the front ~60% of each sloped top edge there is a row of **4–5 printed teeth** like a ripsaw, each tooth a right triangle about **4 mm tall** with the **vertical face toward the rear** and the slope toward the front (barbs that let an opponent slide in but resist it sliding out). Tooth pitch about **6 mm**. The teeth are as thick as the wall (4 mm).
- **Right wall outer face**: plain black, with a **black socket cap screw** (head Ø about 4 mm, hex socket) at about (y +38, z 10). This probably clamps the right fork blade or the wall to the floor **(guess)**.
- **Right wall inner top**: at about (y +44, z 14) a **short silver edge** sticks out from the inner face: the rear end of the **right fork blade** passing into a slot in the wall.
- **Left wall**: seen from inside. Near its rear, a **tall black rectangular post** (about 8 × 6 × 20 mm, FB-L) stands on the floor against the inner face; the **left fork blade's rear end** bends inward and is screwed onto a lower block in front of this post.

### 2.9 Jaw floor (JF)
- **Shape**: a **flat black plate** spanning the inside of the jaw, about **52 mm wide** (between the side walls) × **28–30 mm long** (from FW at y +24 to its front edge at about y +52), about **2–3 mm thick**, its top at about **z ≈ 3–4**. Its front edge is straight and parallel to X. A **narrow raised ledge** (about 3 mm high, 4 mm deep) runs along the rear of the floor at the foot of FW.
- **Surface**: matt black with print lines along the length; dusty, with white specks.
- **Front edge**: about 15–20 mm **behind** the fork tips. The floor's front edge is thin and appears to taper (a small bevel) **(guess)**.

### 2.10 Fork blades (FK-L, FK-R)
- **Shape**: a **flat steel strip lying flat (in a horizontal plane)**, about **6–8 mm wide × 1 mm thick**, running forward along the inside foot of each jaw side wall, extending about **12–15 mm beyond** the plastic wall tip. The tip is a **harpoon**: the strip tapers on its inner side to a **sharp point** at the outer edge, with a **backward-facing barb/notch** about 4–5 mm behind the point on the inner edge (so from above each tip looks like an arrowhead with one barb). The outer edges of the blades are straight.
- **FK-R**: seen from above-right; its upper face has **green marker scribbles**. It runs at floor level (bottom at z ≈ 0, top at z ≈ 1) along x ≈ +24 to +31, from y ≈ +44 (where it enters a slot in the right wall) to the tip at about **y ≈ +78**. The plastic wall's lower edge sits on/over it.
- **FK-L**: seen from inside the jaw. It runs along x ≈ −24 to −31 to its tip at about y +78, but its **rear end has a dog-leg**: about 30 mm behind the tip it bends **inward by about 30°** for about 10 mm and then **upward/back** onto the top of the fork block FB-L (at about y +40, z 10), where it is clamped. The bent rear section is a separate visible flat tab about 8 mm wide.
- **Material**: bright **steel** (spring steel or hacksaw-blade style), with ground edges. The barb shape suggests it was cut from a **hacksaw blade / spring-steel strip** with an angle grinder **(guess)**.
- **Height**: the blade tips are on or just above the floor (0–0.5 mm), the lowest point of the robot at the front.

### 2.11 Fork blocks (FB-L, FB-R)
- **FB-L**: a black printed block about **10 × 8 × 10 mm** inside the left wall at y ≈ +38..+46, under the left blade's bent tab, plus the taller post behind it (2.8). A screw (hidden) clamps the blade.
- **FB-R**: hidden; the right blade enters a **horizontal slot** in the right wall at about z 0–2 and is clamped by the outer socket screw (2.8) **(guess)**.

### 2.12 Weapon arm (AR), sleeve (SLV) and phase wires (PW)
- **Shape**: a **curved post**, about **9–10 mm wide (X) × 8 mm deep (Y)** in section, rising from the slot SL at about (x −9, y +20, z ≈ 22) to the top at the disc hub at about (x −9, y +10…+14, z ≈ 74). Its centre line is **gently curved**: from the base it goes **straight up and slightly back**, then bends **forward** in its upper third so that the top leans about **10–15° forward of vertical**; total length along the curve about **55 mm**. The arm narrows slightly toward the top.
- **Surface**: **fuzzy black**: a **black braided cable sleeve** (expandable PET braid) or black fabric tape wrapped around a printed or metal core. Loose fibres stick out at the bottom where the sleeve ends, just above the lid.
- **Phase wires (PW)**: **three black silicone wires** (each Ø ≈ 1.2 mm) run in a bundle up the **right/rear face** of the arm, under or beside the sleeve, from the body to the motor at the top. They appear as a separate strand about 3–4 mm from the arm core in the lower half, rejoining it higher up.
- **Function**: carries the weapon motor and disc. Whether it pivots is not directly shown. Evidence for a **pivoting arm**: the arm base sits in an open **vertical slot** rather than a fitted hole; the **window** next to it exposes a mechanism with a screw; the blue **clip block** looks like a stop; and the robot has a trapping jaw that only makes sense if the saw can be brought down into it. **Reconciled: the arm pivots about a transverse (X) axis inside the body near (y +14, z 18), driven by a servo, swinging forward about 70–90° to bring the disc down into the jaw (medium-high).**

### 2.13 Weapon motor (WM), hidden
- **Guess**: a small **brushless outrunner** (1104/1106/1306 class: about Ø 14–16 × 10–12 mm) fixed to the top of the arm with its **shaft along X**, bell facing **+X**. The disc is clamped to the **bell** by the blue hub (four screws into the bell's tapped holes). The motor would sit on the **left face of the disc** (x ≈ −9 to −1), hidden behind it in this view.

### 2.14 Disc hub (HB) and screws (S-HB)
- **Shape**: a **blue printed cylinder**, about **Ø 16 mm × 4 mm thick**, on the right face of the disc, concentric with it, with a **slightly domed/chamfered edge**. Its colour is a deeper **violet-blue** than the body (a different blue filament, or the same blue in shade).
- **Screws**: **4 small socket cap screws** in a **tight square**, heads about **Ø 2.8–3 mm** (M1.6 or M2 low-head), centres on a square about **4 mm** across (diagonal about 5.7 mm), around the centre. They clamp the hub and disc to the motor bell. Natively at px (725, 368), (757, 352), (739, 395), (771, 380) approximately.

### 2.15 Saw disc (DS)
- **Shape**: a flat **Ø 50 mm disc, about 1 mm thick at the hub and 1.5–2 mm at the gritted rim**, centre bore 10 mm (covered by the hub). It has **6 radial expansion slots** at 60° pitch, each about **2 mm wide × 6–7 mm deep**, cut in from the rim with **round keyhole ends** (Ø ≈ 2.5 mm). The rim (about 4 mm deep radially) is coated with **tungsten-carbide grit**, giving a rough, sparkly grey-black edge.
- **Face graphics**: black face with **white text** in arcs ("BOSCH", "80 m/s", "Ø50×10 mm", "max 30600 min⁻¹", "1600A015SP", "Carbide Multi Wheel", "Swiss Made", "Wood, Nails, Plastic" and a safety pictogram), confirming the identification.
- **Position**: centre at about **(x −1, y +12, z 74)**, plane parallel to YZ (axis along X). Bottom of the disc at z ≈ 49, top at z ≈ 99, front edge at y ≈ +37, rear edge at y ≈ −13. The disc is directly above the front half of the body and the rear of the jaw.
- **Speed**: up to the printed 30 600 rpm limit; a small outrunner on 2S–3S would spin it at about 15 000–30 000 rpm unloaded **(guess)**.

### 2.16 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 33 mm × 10 mm wide**. The tread is a **printed knurl**: about **40 straight axial ribs**, each about 1 mm tall, so the outer profile looks like a coarse spur gear. The outer face is a **flat disc recessed about 2 mm** inside the tread rim, with **three curved spokes** (like a Y with swept arms, each about 5 mm wide) and three large **lens-shaped openings**, around a **central hub about Ø 9 mm** (black, with the motor shaft inside).
- **Colour/material**: matt black, layer lines visible: printed **TPU** (tread) or PLA with a TPU tyre **(guess: TPU)**.
- **Positions**: WH-R centre at about **(x +36, y −14, z 16.5)**; WH-L mirrored at (x −36, y −14, z 16.5). Track (centre to centre) about **72 mm**; outer faces at x ±41. Only the top arc of WH-L is visible above the lid at the rear-left.
- **Height**: wheel top at z ≈ 33, about **5 mm above the lid**, so the robot can drive inverted (but see section 7 about the arm).
- **Mount**: directly on the motor shafts through the tub side walls; no outer guards; the outer faces are fully exposed.

### 2.17 Drive motors (M-L, M-R), hidden
- **Guess**: two **N20 micro gearmotors** lying transversely inside the rear of BT, shafts out at z ≈ 16.5, y ≈ −14.

### 2.18 Electronics (hidden; glimpsed)
- Through the lid holes: something **green** (PCB), **red and black wires**, and a **white** item (servo case or label). Likely a **2S LiPo**, a **receiver**, a **dual brushed ESC** for drive, a **brushless ESC** for the saw, and the **arm servo** **(guess)**.

---

## 3. Per-view sections

### 3.1 The photo view (front-right, high)
- Left half of the image: the **open black jaw** with its floor, the two toothed walls and the two silver barbed fork tips pointing toward the lower-left, the near (right) fork largest.
- Centre: the black front wall with its slot and the **sleeved arm** rising from it; at the top-left, the **big black disc** facing the camera with its white text and the **blue hub** with 4 screws.
- Right: the **blue box** with its triangle-lattice lid, black screws, switch on the green board, the small blue clip and the window; the **right wheel** with three swept spokes at the lower right.

### 3.2 Top view (plan, synthesised)
- Rear: a **60 × 45 mm blue rectangle** with lattice holes, a slot at x −9, a window right of it, and the switch at the rear-right; **two wheels** 10 mm wide sticking out each side at the rear (overall width about **82 mm**).
- Front: the **black U** of the jaw: two 4 mm wall strips at x ±28 running 48 mm forward from the front wall; the floor between them; the **steel forks** sticking out about 10–14 mm beyond the wall tips as narrow arrowheads. Overall length about **100 mm** (wheel rear y −30.5 to fork tip y +70, see section 11).
- The disc, seen from above, is a thin line (2 mm) along Y at x ≈ −1, from y −13 to +37, with the motor (Ø 15) on its left side at the top of the arm.

### 3.3 Right side view
- A **26 mm tall blue rectangle** (body) with a **33 mm wheel** at its rear; in front, the **black triangular jaw wall** sloping from 26 mm down to the floor over 48 mm, with saw teeth on its slope and a socket screw low down; the **steel fork** sticking out at floor level as a sharp point.
- Above: the **arm** rising from the front of the body and the **Ø 50 disc** seen as a full circle, its bottom about 21 mm above the lid and its top at about 99 mm.

### 3.4 Front view
- The **jaw opening**: a 52 mm wide, 26 mm tall U (shallowing toward the front), with the floor at the bottom; two fork tips at the lower corners; the black front wall at the back with the slot; the wheels peeking out at both sides behind; the **disc edge-on** as a tall thin line (2 mm wide, 50 mm tall) on top of the arm, slightly left of centre, with the motor bulge on its left.

### 3.5 Rear view (not photographed; inferred)
- Blue rear wall 60 × 26 mm between the two wheels; the disc and arm visible above; the switch on the lid at the top right.

### 3.6 Underside (not photographed; inferred)
- Flat blue floor of the tub, the jaw floor slightly higher, two wheel contact patches at the rear, the two fork blades at the front contacting the floor: a **three-point stance** (two wheels + forks/jaw front).

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BT | box tub | 60 × 45 × 26 | 1 × 0.75 × 0.43 | blue FDM | bolted to JW | 1 |
| LID-F/R | isogrid plate | ≈ 32 × 40 × 2 / 28 × 45 × 2 | 0.5 × 0.7 | blue FDM | ~6 × M2 black pan | 2 |
| WIN | window | 22 × 10 | 0.37 × 0.17 | — | — | 1 |
| CLP | cube with hole | 7 × 7 × 8, hole Ø 3 | 0.12 | blue | glued/printed on lid | 1 |
| SW | slide switch on PCB | 10 × 6 × 6 | 0.17 | green PCB, black lever | glued/screwed | 1 |
| JW-FW | wall with slot | 60 × 4 × 26, slot 7 × 14 | 1 × 0.07 × 0.43 | black FDM | screws to BT | 1 |
| JS-L/R | toothed triangle wall | 48 × 4 × 26 | 0.8 × 0.07 × 0.43 | black FDM | integral with FW/JF | 2 |
| TT | saw teeth | 4–5 per wall, 4 tall, 6 pitch | — | black | integral | 9–10 |
| JF | floor plate | 52 × 30 × 2.5 | 0.87 × 0.5 | black FDM | integral | 1 |
| FB-L/R | blade blocks | 10 × 8 × 10 | 0.17 | black | integral | 2 |
| FK-L/R | barbed steel strip | 6–8 wide × 1 thick × ≈ 40 long | 0.13 × 0.67 | steel | screw clamp | 2 |
| S-JW | socket cap | head Ø 4 | 0.07 | black | into JW | ≥ 3 |
| AR | curved post | 10 × 8, ≈ 55 along curve | 0.17 × 0.92 | black braid over core | pivot in body (guess) | 1 |
| PW | 3 wires | Ø 1.2 each | — | black silicone | along AR | 3 |
| WM | brushless outrunner | Ø 15 × 11 | 0.25 | — | screws to AR top | 1 (guess) |
| HB | hub disc | Ø 16 × 4 | 0.27 | violet-blue FDM | 4 × M1.6/M2 socket | 1 |
| DS | carbide grit disc | Ø 50 × 1–2, 6 slots | 0.83 | black, carbide rim | clamped by HB | 1 |
| WH | knurled 3-spoke wheel | Ø 33 × 10 | 0.55 × 0.17 | black TPU (guess) | motor shaft | 2 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LID ↔ BT walls | rest on (with thin white layer), screwed | 0 |
| LID-F right edge ↔ AR | side by side in the slot | 1–2 |
| LID-R window edge ↔ AR | side by side | 2–4 |
| CLP ↔ LID-R | fixed on | 0 |
| CLP ↔ AR (raised position) | stop contact (guess) | 0–1 |
| SW ↔ LID-R | fixed on | 0 |
| FW ↔ BT front | bolted | 0 |
| FW slot sides ↔ AR | clearance | 1–2 each side |
| JS ↔ FW / JF | integral | 0 |
| JF top ↔ floor | above | 3–4 |
| JF bottom ↔ floor | above | 0.5–1 |
| FK bottom ↔ floor | touching/skimming | 0–0.5 |
| FK ↔ JS lower edge | clamped in slot/on block | 0 |
| FK tip ↔ JS tip (Y) | blade extends ahead | 10–14 |
| AR base ↔ pivot (inside BT) | pinned (guess) | 0 |
| AR top ↔ WM | screwed (guess) | 0 |
| WM bell ↔ DS ↔ HB | clamped (4 screws) | 0 |
| DS bottom ↔ LID top (raised) | above | 21 |
| DS left face ↔ AR side | beside (motor between) | ≈ 8 (motor length) |
| DS ↔ JS tooth tips (raised) | clear | > 20 |
| DS bottom ↔ JF top (arm lowered, guess) | near/into the jaw | 0–5 |
| WH inner face ↔ BT side walls | near | 1–2 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ LID top | wheel above | +5 |
| BT floor ↔ floor | above | 2 |

---

## 6. Mechanism
1. **Drive**: two-wheel differential drive at the rear; the front rests on the fork blades and jaw. Turning pivots about the rear axle, so the forks sweep sideways quickly to catch opponents.
2. **Trap**: the toothed jaw walls funnel an opponent's corner or wheel into the U; the **rear-facing tooth faces** stop it backing out; the **barbed fork tips** do the same at floor level.
3. **Saw**: the brushless motor spins the Bosch carbide disc at high speed. With the arm **swung forward** (guess), the disc comes down through about 70–90° and its rim cuts into whatever sits in the jaw (top armour, wheels, wires). With the arm upright, the disc also acts as a **tall vertical spinner** that can hit opponents who climb over the forks.
4. **Self-righting** (guess): if inverted, the arm swinging could lever the robot back over, using the arm tip/disc as a contact point (the disc would then touch the floor, so the designer probably stops the disc first). The wheels are taller than the tub, so inverted driving works in principle, but the jaw would then be useless.

---

## 7. Assembly order (suggested rebuild)
1. Print **BT** (open-top tub with motor cradles, servo pocket and a pivot bearing seat), **JW** (front wall + toothed side walls + floor + fork blocks), **LID-F/LID-R**, **CLP**, **HB**, **AR** core and the wheels.
2. Fit the two **drive motors** in BT and press on the **wheels**.
3. Fit the **arm servo/pivot** in the front of BT under the window; fit the **arm** through the slot onto its pivot/horn.
4. Fit the **brushless motor** onto the top of the arm, run the **three phase wires** down the arm, slip the **braided sleeve** over arm + wires, and route the wires into the body past the clip block.
5. Fit the battery, ESCs, receiver; mount the **switch** board on the lid.
6. Bolt **JW** to the front of BT (screws through the black end posts), slide the **steel forks** into their slots/blocks and clamp them (socket screws).
7. Screw down the **lid plates** (about 6 black pan screws), glue/screw the **clip block**.
8. Put the **disc** on the motor bell, place the **blue hub** over it and drive in the **4 tiny socket screws**.

---

## 8. Coordinate frame (restated)
- Origin O on the floor under the centre of the blue tub. +X right, +Y forward, +Z up. mm.
- BT: x ∈ [−30, +30], y ∈ [−25, +20], z ∈ [2, 28]. FW: y ∈ [+20, +24]. Jaw walls to y +68; fork tips to y +78 (raw) or +70 after the cube reconciliation (section 11).
- Wheels: centres (±36, −14, 16.5). Disc centre (−1, +12, 74), axis X.

## 9. Profiles as math

**9.1 Jaw side wall side profile (YZ plane, extruded along X over ±[26, 30]).**
- Rear edge: vertical line y = +24, z from 0 to 26.
- Top edge (envelope): line from (y 24, z 26) to (y 68, z 2): z = 26 − 0.545·(y − 24), slope 28.6°.
- Teeth on the front 60% of the top edge: for k = 0…4, tooth k has its rear vertical face at y_k = 40 + 6k from z_env(y_k) up to z_env(y_k) + 4, and its sloped face from that top point down to (y_k + 6, z_env(y_k + 6)). I.e. a sawtooth z = z_env(y) + 4·(1 − frac((y − 40)/6)) for y ∈ [40, 70].
- Bottom edge: z = 0 from y 24 to y 68 (with the blade slot at z 0–1.5 on the right wall).

**9.2 Fork blade plan outline (XY plane, at z 0–1, right blade; left blade mirrored plus the dog-leg).**
- Outer edge: x = +31 from y +44 to y +78 (tip).
- Inner edge: x = +24 from y +44 to y +64; barb notch: from (24, 64) a line inward-forward to (22, 68), then back outward to (25, 67) (the barb's rear-facing step); then the taper from (25, 67) to the tip (31, 78).
- Left-blade dog-leg: from (−24, +48) a line to (−18, +40) and a tab up to z 10 on FB-L.

**9.3 Arm centre line (YZ plane at x = −9).**
- Quadratic Bézier from P0 = (y 20, z 22) via P1 = (y 18, z 55) to P2 = (y 12, z 74). Points: B(t) = (1 − t)²·P0 + 2t(1 − t)·P1 + t²·P2. Section 10 × 8 mm, rounded corners r 2.
- Pivot (guess) at (y 14, z 18) on X.

**9.4 Disc.**
- Circle r = 25 at (y 12, z 74), plane x = −1, thickness 1.2 (rim 1.8 over the outer 4 mm). Slots: for k = 0…5, a slot of width 2 from r = 18.5 to r = 25 at angle 30° + 60°k, ending in a circle r 1.25 at r = 18.5.
- Hub: circle r 8 at the same centre, x from −1 to +3 (+X side); four screw heads r 1.4 at (±2, ±2) around the centre in the disc plane.

**9.5 Wheel.**
- Outer profile r(φ) = 15.5 + 1.0·[sin(40φ) > 0]. Face recessed 2 mm; 3 spokes as swept arcs: each spoke centre-line is the curve r ∈ [4.5, 13], φ(r) = φ_k + 0.04·(r − 4.5) rad, φ_k = 0°, 120°, 240°, width 5 mm.

**9.6 Lid isogrid.**
- Triangle holes of side 5 at a pitch of 6.5 mm along X and 5.63 mm along Y (row spacing = 6.5·√3/2), alternate rows offset by 3.25 mm; alternate holes flipped. Border rim 3 mm wide with no holes, and solid pads (Ø 8) around each screw.

## 10. Pixel-based measurements (independent check)
Native image 1634 × 1524 px; (x, y) from the top-left, ±10 px.
- Disc: x 455–975, y 45–610 (520 × 565 px). Centre ≈ (712, 330). Hub: x 630–800, y 285–455 (≈ 170 px).
- Arm: base at (800, 770), top joins the disc behind the hub at ≈ (790, 560) on screen; width ≈ 60 px at the base.
- Blue tub right wall: front edge x ≈ 1045 from y 835 to 1110; right wheel x 1275–1605, y 885–1255; right wheel centre ≈ (1440, 1070).
- Front wall: left end post at (630, 700–960), right corner at (1050, 1050).
- Right fork tip (270, 1415); left fork tip (45, 1000). Right wall socket screw (915, 1240).
- Arm slot in FW: x 760–800, y 840–925.
- Switch: (1100–1160, 660–745). Clip block: (875–925, 770–835).

## 11. Several independent estimates of key quantities

| Quantity | Method A (label / rules / kit) | Method B (ratio in photo) | Method C (pixels + scale) | Reconciled |
|---|---|---|---|---|
| Disc Ø | label: **50** | kit r 34 → 68 (too big for the cube) | — (it is the scale) | **50** |
| Scale at disc depth | — | — | 520–565 px / 50 mm = 10.4–11.3 px/mm | **10.8 px/mm** |
| Body height | kit 28 | wheel ≈ 1.25 × body wall → 26 | right wall 275 px at ≈ 10.6 px/mm (similar depth to the disc) → 26 | **26 to the lid top (z 28 incl. 2 floor gap)** |
| Body width | kit 60 | 2 × fork span ≈ wall spacing 56 + 2 × 4 = 60 | FW 410 px horizontal along a direction foreshortened to ≈ 0.6 → 680 px true / 10.8 → 63 | **60** |
| Wheel Ø | kit r 13 → 26 | ≈ 0.66 × disc → 33 | 330–370 px at ≈ 10.6 px/mm (nearer, so slightly enlarged) → 31–35 | **33** |
| Disc centre height | kit z 84 (with r 34) | disc bottom ≈ 0.8 disc Ø above the lid → 28 + 20 + 25 = 73 | lid at the arm base y 770 to disc centre y 330 = 440 px / 10.8 / cos 25° → 45 above the lid → 73 | **74** |
| Disc top height | ≤ 101.6 (cube) | 74 + 25 = 99 | — | **99 (fits)** |
| Jaw length (FW to wall tip) | kit jaw to y 96–100 | ≈ 1.0 × body width (photo impression, inflated by perspective) | 842 px along Y at the near end (≈ 18 px/mm, near camera) → 47 | **44–48** |
| Overall length | ≤ 101.6 | wheel rear (−14 − 16.5 = −30.5) to fork tip | — | **fork tips at y +70 → total 100.5** |
| Fork overhang beyond wall | — | ≈ 1/3 of jaw length | ≈ 230 px near the tip at ≈ 18 px/mm → 13 | **12** |
| Lid hole size | — | ≈ 1/9 of LID width | ≈ 50 px / 10.6 → 4.7 | **5** |

## 12. Consistency check: conflicts and reconciliation
1. **Disc size**: the kit draft used r 34 (Ø 68). The label clearly states Ø 50. A Ø 68 disc centred at z 84 would stand 118 mm tall, outside the 101.6 mm cube. **Reconciled Ø 50, centre z 74, top z 99.**
2. **Overall length**: the raw perspective reading puts the fork tips at y +78 (wheel rear at −30.5, total 108.5 mm), which breaks the cube. The near-camera magnification of the forks explains the excess. **Reconciled: the jaw is 44 mm long (FW front at y +24 to wall tip +68 → shorten to +60) and the blades overhang 10 mm to y +70; total 100.5 mm.** Shift the jaw-profile maths in 9.1 accordingly (scale Y offsets by 36/44).
3. **Width with wheels**: 60 + 2 × (1.5 gap + 10 wheel) = 83 mm < 101.6. Consistent.
4. **Arm position**: slot at x ≈ −9 (FW fraction 0.34) and the kit's x −8 agree; the disc on the motor's +X side ends near the centreline (x ≈ −1), so a lowered disc lands in the middle of the 52 mm wide jaw. Consistent.
5. **Arm pivot vs fixed mast**: no photo of motion. The slot, window, stop block and trap jaw all point to a pivot; a fixed mast would not need an open slot. **Kept as pivoting (medium-high).**
6. **Wheel vs lid height**: wheel Ø 33 at z centre 16.5 gives the top at z 33, 5 mm above the lid; the arm and disc stick up 70 mm more, so inverted driving is only possible if the arm folds flat (then the disc would rest on the jaw). Likely the robot is **not** designed to run inverted; it would rely on the arm to self-right **(guess)**.

---

## 13. Why the designer did it (per part, mostly adversarial)

Common lens: what attacks can reach each part (horizontal spinners, vertical spinners, wedges, lifters/flippers, wall hits, inversion), how it survives, and how it helps win: here, **trap the opponent and cut it**, rather than get under and push.

- **Toothed jaw walls (JS, TT)**
  - Fight: the walls form a **funnel** that guides an opponent's corner into the U when the robot drives at it. The teeth face backward like barbs, so the opponent can slide in but catches when it tries to reverse out. The sloped top lets an opponent ride up a little, lifting its wheels and reducing its traction so it cannot escape.
  - Against attacks: the walls are the first thing a horizontal spinner meets from the front; thick printed walls (4 mm) are sacrificial and cheap. A vertical spinner hitting a wall will mostly bite the teeth.
  - Construction: printed teeth cost nothing; the triangular wall profile keeps the jaw light while staying stiff at the root.

- **Steel barbed forks (FK)**
  - Getting under vs contact: the forks are the **lowest and most forward** parts. Their thin steel tips get under the edges of wedges and boxes better than any printed edge can (plastic can't be ground to a 1 mm edge without chipping). Once under, the opponent rests on the forks, inside the jaw, where the saw can reach it.
  - The barbs grip the opponent's underside edge or armour lip and resist pull-out; they also make the forks harder to push sideways out of position.
  - Weak points: long thin blades bend under heavy hits; the clamps (one screw each) allow quick replacement. The green marker on FK-R suggests marking/realignment after bending.
  - Construction: cut from cheap spring steel / hacksaw blade; flat strips need no bending (except the left dog-leg for clamping).

- **Jaw floor (JF)**
  - Fight: stops a trapped opponent from dropping under the saw's reach, and gives a solid backing so the saw cuts **down into** the opponent instead of pushing it into the floor gap. Its raised height (3–4 mm) keeps it from scraping.
  - Construction: printed as one with the walls for stiffness; makes the jaw a rigid U.

- **Front wall FW with a narrow slot**
  - Fight: shields the electronics from anything the saw throws back and from opponents pushed into the jaw. The narrow slot only lets the arm through; the double wall stiffens the slot.

- **Overhead saw on an arm (AR, WM, HB, DS)**
  - Fight: a cutting disc attacks the **top armour** of an opponent, which on antweights is often the thinnest part (lids of 1–2 mm plastic). Coming from above, it avoids the opponent's wedge and front armour entirely. The carbide grit disc **cuts** rather than impacts, which suits a weight-limited robot that cannot carry a large energy-storing spinner. When raised, the spinning disc also deters opponents from driving over the forks (they hit the disc).
  - Against attacks: the arm is the most exposed part. The braided sleeve protects the phase wires from cuts and abrasion. The disc is small and hard. The motor sits on the disc's far side, partially shielded by it from a right-side view, but exposed from the left **(weak point)**.
  - Construction: an off-the-shelf Bosch disc is cheap and widely available, already balanced, rated for 30 600 rpm; the 10 mm bore matches a printed hub; four tiny screws into the motor bell give a positive drive without a shaft adaptor.

- **Blue hub with four socket screws (HB)**
  - Construction: spreads the clamping load across the thin disc around its bore, so the disc does not crack at the screw holes; four screws share the impact torque when the disc hits.

- **Clip block (CLP)**
  - Construction/fight: a hard stop and/or wire guide at the arm root; stopping the arm at a fixed upright position keeps it from over-travelling backward and prevents the wires being yanked.

- **Blue isogrid lid**
  - Fight: the top of the tub is not the primary target (the arm and disc stand above it), so the lid is lightened with a triangle lattice that stays stiff in all directions. The holes also **ventilate** the ESCs, which work hard with a brushless saw.
  - Weak point: a vertical spinner or another saw could poke through the holes; acceptable because the lid is mainly a cover.
  - Construction: printed flat; screws in each corner; easy access.

- **Switch on top at the rear-right**
  - Construction: easy to reach for the operators before and after fights; placed at the corner farthest from the jaw and the saw path.
  - Weak point: exposed to overhead hits; the rear corner is the least likely place to be hit.

- **Two rear wheels, outboard, no guards**
  - Fight: placing wheels at the rear keeps the forks low and loaded with the front weight; wide track resists tipping when the arm swings forward. Knurled TPU tread for grip in pushing matches.
  - Weak points: exposed to horizontal spinners from the sides and rear; no wheel guards to save weight for the saw system.

- **Blue/black colour split**
  - Construction: blue for the electronics box, black for the wearing jaw; the jaw is a separate print that can be replaced after a fight without touching the electronics.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Weapon motor | brushless outrunner 1104–1306 class, KV 4000–6000 | Ø 15 × 11 | (−5, +12, 74), shaft along X | medium |
| Weapon ESC | small brushless ESC 6–12 A | 20 × 12 × 4 | under LID-R, (+12, −5, 10) | medium |
| Arm servo | 9 g / micro metal-gear servo, output along X | 23 × 12 × 23 | front-centre of BT under the window, (+2, +8, 14) | medium |
| Arm pivot | arm root clamped to the servo horn or a pin through BT walls at (y 14, z 18) | — | — | medium |
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | transverse at the rear, shafts at (±31, −14, 16.5) | medium |
| Drive ESC | dual brushed ESC or combined board | 25 × 15 × 5 | rear-centre | low |
| Receiver | 2.4 GHz micro receiver | 20 × 12 × 5 | rear-left under LID-F | low |
| Battery | 2S 7.4 V LiPo 180–300 mAh | 40 × 18 × 10 | across the rear above the motors or along the left side | medium |
| Jaw screws | 2–4 screws through the black end posts into the blue tub front | M2 × 8 | at the front corners, z 8 and 20 | medium |
| Fork clamps | right: blade in a printed slot clamped by the side socket screw; left: screwed to FB-L | M2/M2.5 | as described | medium |
| Arm core | printed PETG/nylon or an aluminium strip inside the braid | 8 × 6 | inside AR | low |
| Wires | 3 phase wires up the arm; servo lead; 2 × motor pairs; battery → switch → ESCs | — | under the lid | high (phase wires seen) |

**Wiring path summary (guess)**: battery → switch (on the lid at the rear-right) → drive ESC/receiver and weapon ESC; the weapon ESC's three phase wires leave the body beside the arm (past the clip block) and run up the arm under the braid to the motor; the servo lead stays inside; drive motor leads are short, at the rear.

## 15. What the photo cannot show (uncertain list)
- Whether the arm actually pivots, and its range; the arm drive type.
- The left side, rear, underside, and the motor behind the disc.
- Exact fork-blade outline on the left (partly hidden), and whether the right blade has the same dog-leg.
- Exact number of lid screws (4 seen, about 6 assumed).
- All mm values except the disc are scaled estimates (±10–15%); the near-camera perspective makes the jaw and forks look longer than they are.

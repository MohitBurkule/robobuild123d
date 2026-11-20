# Mutant: full description of the reference photos

Purpose: a rebuild-from-text description of the AWS antweight **Mutant** as it appears in the three wiki photos in
`reference/`. Every part is described with its shape, size ratios, colour, position relative to the other parts, the
faces that touch, the gaps, how it is fastened and how it works. Anything that cannot be seen directly is marked
**(guess)**. Sizes are ratios first and mm second; the mm values assume a pod length (front to back) of about 76 mm
and a total width of about 134 mm, which is what the existing kit draft measured from the photo masks (±10 %).

Frame: **+y forward** (the end with the grey metal plates, the floor skirts and the disc hook), **+x = robot's right**,
**+z up**, floor at z = 0 in this document. Mutant is a **shuffler** (non-wheeled walker class): it moves on rotating
lobed cams, not round wheels.

Two versions of the robot appear: **blue** (aws72, aws74: translucent blue prints, white cams with green TPU pads,
grey metal plates, clear ribbed skirts) and **white** (aws76: cream prints, black cams with yellow pads, dark grey
metal plates, yellow ribbed skirts, blue lettering). The geometry is the same; the description follows the blue
version and notes where the white one differs.

---

## 1. The photos and what each one shows

### 1.1 `mutant.aws72.webp` (1200 x 1068) — labelled front_right_iso
- Camera high on one side and in front of a corner, looking down at about 35 deg. The metal front plates and the floor
  skirts are at the image lower right; the long side of one pod (with two small blue triangular fins and a centre
  screw with a green insert) faces the camera along the image bottom left; the rear of the far pod with a rounded lower
  block is at the image far left.
- Visible: both pods' tops with their cam windows (three white cam discs with green pads in each), the triangular
  disc-guard hump between the pods, the red 2-pin **charging port** on the near pod top near its front edge, a small
  black square (switch or link) on the far pod top near its rear-left, the "MUTANT" label on the far pod's front plate,
  one disc hook showing between the plates, both skirts, a red component behind the near cams (a red motor or wire,
  guess), black screw heads round the top edges.

### 1.2 `mutant.aws74.webp` (1153 x 964) — labelled rear_right_iso (this label was chosen for silhouette fit; the
  photo itself shows the plates and skirts on the image left, so the camera is actually at the robot's front-right or
  front-left looking along the front face; treat the label with care)
- Shows the front face of both pods in strong perspective: two grey metal plates, one per pod, with a vertical slot
  between them in which a thin steel disc with a large hook tooth is visible; the "MUTANT" label on the near plate; both
  ribbed skirts on the floor in front; the triangular hump above the slot; the near pod's side with one triangular fin,
  a centre screw with a green insert, a small black switch/lever slot and a white tab near its rear edge; cam stacks
  through both top windows; the red charging port on the far pod top at its front-left corner.

### 1.3 `mutant.aws76.webp` (1624 x 1247) — labelled front, elevation 25
- White version, camera low at the front-left corner: the two curved dark grey front plates run across the left two
  thirds of the image, the cream pod sides fill the right third; the rounded/chamfered rear-bottom edge of the right
  pod is visible at the image right; yellow ribbed skirts lie on the floor under the plates.
- Visible on the top: two cam windows with black/yellow cams, "MUTANT" in raised blue letters across the right pod
  top, "ON / OFF" printed beside a black slide switch, a red plug (the charging connector) standing up at the slot end of
  the right pod top, tiny silver screw heads at the top corners, the disc (dark green/grey hook disc) in the slot, and a
  light grey cylinder in the slot behind the disc (the weapon motor bell, guess).

---

## 2. Overall layout

- Two identical rectangular **pods** side by side, joined behind/below the slot (guess: a bridge at the rear and the
  floor). Each pod is about 61 mm wide (x), 76 mm long (y) and 38 mm tall (z): width : length : height ≈ 0.8 : 1 : 0.5.
- A **centre slot** between the pods, about 10-12 mm wide (0.09 of the total width), open at the front and top front,
  holding a thin vertical **disc** on a lateral (x) axle.
- **Front:** each pod's front face is covered by a grey metal sheet plate (flat-angled in the blue version, a convex
  curved quarter-round in the white version) that runs from the top front edge down to about 3-5 mm above the floor.
  Below it a flexible ribbed **skirt** lies on the floor and projects forward about 22-28 mm (0.3-0.35 of the pod
  length), full pod width.
- **Top:** a rectangular window in each pod's rear half shows a stack of three **cam** discs; a triangular **disc
  guard hump** rises over the slot's rear half; the charging port, switch and screws are on the top.
- **Rear:** the rear-bottom edge of each pod is cut by a large chamfer/round (about 10-12 mm), the rear top edge is
  square; one block on the rear of the left pod (aws72 far left) projects a little (guess: the cam motor housing).
- Overall: 134 mm wide, about 100 mm long including the skirts (76 body + 24 skirt), 38 mm tall body; cams protrude
  2-4 mm above the top and below the bottom.

---

## 3. Part table

| # | Part | Count | Shape | Approx size (mm) | Colour / material | Held by |
|---|------|-------|-------|------------------|-------------------|---------|
| 1 | Pod shell | 2 | open-sided rectangular box, chamfered rear bottom | 61 W x 76 L x 38 H, walls 2 | translucent blue PETG (white: cream PLA) | joined by the rear bridge (guess) |
| 2 | Pod top lid | 2 | flat plate with a cam window | 61 x 76 x 2.5 | same blue, matte top skin | 4-6 black M2 screws round the edge |
| 3 | Side panel (outer) | 2 | flat panel on each pod's outer side | 76 x 38 x 2 | blue | 4 corner screws + 1 centre screw with green insert |
| 4 | Side fins | 2-4 | small right-triangle tabs, pointing down/back | 15 long x 10 tall x 3 | blue | printed on the side panel |
| 5 | Bridge (rear/bottom join) | 1 | box under/behind the slot | 12 x 25 x 38 | blue | screws into both pods (guess) |
| 6 | Disc guard hump | 1 | triangular fin across the slot | 30 long x 12 wide x 14 tall | blue | printed on the inner lid edges (guess) |
| 7 | Front plates | 2 | bent metal sheet over each pod front | 61 wide x 45 developed x 1 | grey steel / titanium (white: dark grey) | 2-3 screws along the top edge + side screws |
| 8 | Floor skirts | 2 | flexible ribbed flap | 58 wide x 25 long x 1.5 | clear/white PETG ribbed (white: yellow TPU) | clamped under the plate bottom edge (guess) |
| 9 | Disc (weapon) | 1 | thin hook disc | 40-45 dia x 2-3 | bare steel (white: dark green tint) | on the weapon motor in the slot |
| 10 | Weapon motor | 1 | small outrunner | 18 dia x 12 | light grey/silver | inside the slot, stator on the pod wall (guess) |
| 11 | Cam stacks | 2 | 3 lobed discs on one axle | each disc 26-30 dia x 5-6 | white PLA + green TPU pads (white: black + yellow) | axle in the pod walls |
| 12 | Cam motors | 2 | N20 gearmotor (guess) | 12 x 10 x 25 | silver/red | inside each pod |
| 13 | Charging port | 1 | 2-pin JST-style socket | 6 x 4 x 6 | red housing | in a recess in the right pod top |
| 14 | Power switch | 1 | small slide switch | lever 3 x 3 | black | in a small top slot (left pod front-left in blue; centre-front in white) |
| 15 | "MUTANT" label | 1 | rectangular sticker (white: raised printed letters) | 30 x 12 | white paper, black text | adhesive on the right/near front plate |
| 16 | Screws | ~24 | M2 black button/pan heads | - | black (white: silver) | - |
| 17 | Battery, ESCs, receiver | - | hidden | - | - | inside the pods (guess) |

---

## 4. Pods (body)

### 4.1 Shape
- Each pod is a straight-sided box: vertical outer side, vertical inner (slot) side, vertical rear face, flat top.
- **Rear-bottom edge:** a large 45 deg chamfer (white version) or round (blue version, aws72 left) about 10-12 mm
  (0.3 of the height) along the whole pod width, so the robot can rock back over it and does not dig in.
- **Front:** the front face is set back under the metal plate; the top front edge of the shell is square and carries
  the plate's top flange.
- Top: flat lid, 2-2.5 mm thick, with a slight perimeter lip. Black screws at the four corners and one at mid-side
  (about 6 visible per lid in aws72), M2 pan heads, 4 mm from the edges.
- Walls 2 mm; translucent so the cam motor (red, guess) and wires are faintly visible through the blue.

### 4.2 Sizes and positions
- Pod outer x: from ±6 (slot face) to ±67 mm. Pod y: from -38 (rear) to +38 (front face under the plate).
- Top at z = 38-40 mm; underside at z = 2-3 mm (2-3 mm floor clearance), cams poking 1-3 mm below.

### 4.3 Side panels and fins
- Each outer side is a separate flat panel (seam visible at the top edge and front edge, aws72), screwed at its four
  corners (black screws about 5 mm in from the corners) and at the centre (a screw with a green ring/insert at about
  45 % of the length from the front and 45 % of the height).
- Two small blue triangular fins per side (aws72: one near the front lower corner pointing back-down, one at about
  60 % of the length lower down; aws74: one fin near the middle). Each fin is a right triangle about 15 mm long,
  10 mm tall, 3 mm thick, standing out 8-10 mm from the side, its long edge sloping down towards the rear. Purpose
  (guess): stops the robot lying flat on its side and lets it roll back onto its cams.
- aws74 near side: a small black lever slot (switch/link, guess) near the top rear corner and a white tab beside it.

### 4.4 Bridge and slot
- The slot between the pods is 10-12 mm wide, open at the front and at the top front; the disc guard hump closes its
  top rear half; behind the disc the slot is closed by a bridge block (guess) joining the pods, which also carries the
  weapon motor.
- Slot depth: from the front faces back to about 40-45 % of the pod length (the hump's rear end).

### 4.5 Disc guard hump
- A blue printed triangular fin straddling the slot, about 12 mm wide (just wider than the slot), 30 mm long, rising
  from the lid tops at its rear to a peak about 14 mm above the lids at about 1/3 of its length from the front, then
  dropping steeply at the front: a shark fin. Its sides blend into the lids with a concave fillet (aws72: big curved
  flank on the near side).
- A round hole about 3 mm near the top of each flank (aws72, aws74): the **locking pin** hole through the disc guard
  (guess) or the disc axle end.
- A small shiny metal tab sticks up just in front of the hump on the near side (aws72 right of the hump): the disc
  hook tip or a lock pin end (guess).

---

## 5. Front plates and skirts

### 5.1 Plates
- One per pod, sheet metal about 1 mm (steel or titanium), the full pod width less 1-2 mm.
- **Blue version:** a flat face sloping back at about 20-25 deg from vertical from the top front edge down to a bend at
  about 70 % of the height, then a short steeper lip down to 3-5 mm above the floor (aws72, aws74: straight sloped face
  with a crease near the bottom).
- **White version:** a convex quarter-cylinder of radius about 30 mm wrapping from the lid's top front edge round to
  the floor (aws76: smooth curved grey sheets).
- Held by a top flange under the lid edge (2-3 screws visible on the top edge in aws72/aws74) and by side screws at
  the front corners (aws74: screws at the plate's top and bottom at the outer edge).
- "MUTANT" sticker (white with black capitals) on the robot's right plate, centred, about half the plate width.
- The two plates stop 1-2 mm short of the slot so the disc can come out between them.

### 5.2 Skirts
- One per pod: a flat flexible flap, ribbed along x on its top (fine ridges about 1 mm pitch), about 1.5 mm thick,
  almost the full pod width, projecting forward 22-28 mm from the plate's bottom edge and lying on the floor (front
  edge 0-0.5 mm off the floor).
- Clear/white translucent PETG (blue version) or yellow TPU/PLA (white version). Rear edge clamped between the plate
  bottom and the pod floor (guess) so it can flex up.
- The two skirts are separate, with a 10-12 mm gap in line with the slot.

---

## 6. Weapon

- A thin vertical disc (2-3 mm steel) in the slot, axle along x at about z = 18-20 mm and y ≈ +20 to +25 mm (front
  part of the slot). Diameter about 40-45 mm so its lower edge clears the floor by 2-4 mm and its top passes under the
  hump.
- Outline: a "hook" disc: one large curved tooth (aws74: a C-shaped claw curving forward and down out of the slot
  between the plates, about 12-15 mm proud of the disc body) and a second smaller hook opposite (aws72: a silver hook
  near the bottom of the slot). Treat as 2 teeth 180 deg apart.
- Drive (guess): a small outrunner (light grey cylinder seen behind the disc in aws76) with the disc bolted to its
  bell, the stator on the bridge/pod inner wall; no belt visible.
- Clearances: disc to each pod inner wall 4-5 mm; disc to the plates 1-2 mm; teeth to floor 2-4 mm.

---

## 7. Shuffle drive (the internals)

- Each pod has one lateral cam axle (along x) at about y = -15 to -20 mm (rear half) and z = 19 mm (mid-height).
- On it a **stack of three cam discs**, each about 5-6 mm thick with 1 mm gaps, total stack about 20 mm wide, centred
  in the pod window. Each disc is a rounded lobe (a "D" or tear-drop: one large curved lobe of radius about 15-17 mm
  and a flat or small-radius back), and the three lobes are phased 120 deg apart. The lobe faces carry green TPU pads
  (blue version) or yellow pads (white version) about 2 mm thick along their curved edge for grip.
- The lobes stick out through the top window (aws72/aws74: up to 4-6 mm above the lid) and, as they turn, through a
  matching bottom window to the floor (guess: the bottom is not visible). With the rest of the robot resting on the
  skirts at the front, each lobe in turn presses the floor and pushes the pod forward/back: shuffling. Left and right
  pods are driven independently for steering, like a 2WD robot.
- Motor: one gearmotor per pod (guess N20), along x beside the cam stack, direct on the axle or through a short gear
  train; aws72 shows a red part behind the near pod's cams (a red-wired motor or red gear, guess).
- Windows: about 28 mm (x) x 22 mm (y), in the rear half of each lid, offset towards the outer side; cam stacks fill
  them with 1-2 mm clearance at the sides.

---

## 8. Electronics, connectors, controls

- **Charging port:** a red 2-pin JST-style socket recessed flush in a small rectangular pocket in the **right** pod's
  lid, near its front edge and about 1/3 of the pod width from the slot (aws72 near pod; aws74 far pod top-left). In
  the white version a red plug stands up from the top near the slot (aws76). It is the balance/charge lead connector,
  not a weapon or a link.
- **Switch:** a small black slide switch lever in a slot in the top (blue version: on the left pod top near its outer
  front corner, aws72 "small black square"; white version: centre-front of the right pod lid with "ON / OFF" printed
  beside it). Operated from the top.
- Battery (2S LiPo, guess), drive ESC/receiver and weapon ESC: hidden in the pods; wires not visible.

---

## 9. Contact / gap matrix

| A | B | Relation | Gap (mm) | Notes |
|---|---|----------|----------|-------|
| Pod L inner wall | Pod R inner wall | across the slot | 10-12 | joined by the bridge |
| Disc | pod inner walls | between | 4-5 each side | |
| Disc | front plates | between their inner edges | 1-2 | |
| Disc teeth | floor | above | 2-4 | |
| Hump | lids | fused/printed on | 0 | |
| Plate | pod front/top edge | screwed flange | 0 | 2-3 screws per plate on top |
| Skirt | plate bottom | clamped | 0 | |
| Skirt | floor | resting | 0-0.5 | |
| Cam lobes | lid window edges | inside | 1-2 | |
| Cam lobes | floor | contact in turn | 0 | only ground contact besides the skirts |
| Pod underside | floor | above | 2-3 | |
| Side fins | side panel | printed on | 0 | |
| Charging port | right lid | recessed | flush | |

---

## 10. Rebuild checklist
1. Two 61 x 76 x 38 pods, 10-12 mm apart, rear-bottom chamfer 10-12 mm, lids with cam windows in the rear half.
2. Bridge behind the slot; shark-fin hump over the slot rear with a pin hole.
3. Grey metal front plates (sloped flat or quarter-round) per pod, "MUTANT" sticker on the right one; ribbed skirts
   on the floor 25 mm ahead.
4. Thin hook disc (40-45 dia) on an outrunner in the slot, axle z ≈ 19, y ≈ +22.
5. Per pod: lateral cam axle in the rear half with three 120 deg phased lobed cams (green TPU pads) driven by a
   gearmotor; lobes through top and bottom windows.
6. Red charging port on the right lid near the front; black slide switch on the top; black M2 screws on lids and side
   panels; two small triangular fins per side.

---

## 11. Coordinate frame (used by every number below)

Origin on the floor at the centre of the robot in x (middle of the slot) and in y (half way between the pods' rear
faces and the front faces under the plates). +x = robot's right, +y = forward, +z = up; mm and deg.

## 12. Every part in all dimensions (mm, guesses ±10 %)

| Part | L (y) | W (x) | H (z) | Thickness | Radii / angles | Centre (x, y, z) |
|------|-------|-------|-------|-----------|----------------|------------------|
| Pod (each) | 76 (y -38 .. 38) | 61 (x 6 .. 67) | 38 (z 2 .. 40) | walls 2, lid 2.5 | rear-bottom chamfer 11 x 11 at 45 deg (blue: round r 11) | (±36.5, 0, 21) |
| Slot | 40 deep (y -2 .. 38) | 12 (x ±6) | 38 | - | - | (0, 18, 21) |
| Bridge | 36 (y -38 .. -2) | 12 | 38 | solid shell | - | (0, -20, 21) |
| Disc guard hump | 30 (y -5 .. 25) | 14 | 14 above lid (z 40 .. 54) | 2 walls | profile below | (0, 10, 47) |
| Front plate (blue) | 12 in y | 59 | 36 | 1.0 | face 22 deg from vertical; bend at z 12 | (±36.5, 44, 21) |
| Front plate (white) | 30 | 59 | 36 | 1.0 | quarter cylinder r 30 | - |
| Skirt | 25 (y 46 .. 71) | 58 | 1.5 + ribs 0.6 | 1.5 | ribs 1 mm pitch along x | (±36.5, 58, 0.75) |
| Disc | 44 dia | 2.5 | 44 | 2.5 | body r 18, hooks to r 22 | (0, 22, 22) |
| Weapon motor | 18.2 dia | 16 | 18.2 | - | - | (±8 .. in bridge, 22, 22) (guess) |
| Cam (each disc) | 30 | 5.5 | 30 | 5.5 | lobe r 15, hub r 6, 120 deg phase | stacks at (±36.5, -18, 21) |
| Cam stack | 30 | 19 (3 x 5.5 + 2 gaps) | 30 | - | - | (±36.5, -18, 21) |
| Lid window | 22 | 28 | through | - | corner r 1 | (±40, -18, 40) |
| Cam motor | 12 | 30 | 10 | - | N20 | (±52, -18, 21) (guess) |
| Charging port | 4 | 6 | 6 (recessed) | - | 2 pins on 2.54 | (22, 25, 40) |
| Switch slot | 4 | 8 | through | - | - | (-55, 28, 40) blue / (25, 30, 40) white |
| Side fin | 15 | 3 | 10 | 3 | right triangle, hypotenuse falling to the rear at 34 deg | (±68.5, 22 and -5, 10) |
| MUTANT label | 12 | 32 | 0.1 | - | - | on right plate (36.5, 44, 24) |

## 13. Curves as maths

- **Hump side profile** (y, z above lid): polyline (−5, 0) (8, 14) (13, 14) (25, 0) with the rear flank
  concave: z = 14 (1 - ((8 - y)/13)^2) for -5 ≤ y ≤ 8; front flank line z = 14 - 1.17 (y - 13) for 13 ≤ y ≤ 25.
- **Cam disc outline** (polar about the axle): r(φ) = 6 + 9 · max(0, cos(φ/2))^2 for φ in [-180, 180] (one big lobe
  of r 15 at φ = 0, hub r 6 behind); pads: a 2 mm band on 6 + 9cos²(φ/2) - 2 ≤ r ≤ 6 + 9cos²(φ/2) for |φ| < 60.
  Discs 1, 2, 3 rotated 0, 120, 240 deg.
- **Disc outline:** circle r 18 plus two hooks: r(θ) = 18 + 4 (θ/80)^1.5 for 0 ≤ θ ≤ 80, then back to 18 over 10 deg;
  second hook at θ + 180.
- **White front plate:** arc centre (y = 38 - 30, z = 40 - 30) = (8, 10), radius 30, from 90 deg (top) to 0 deg
  (front) to -20 deg (floor tangent).
- **Blue front plate:** line from (y 38, z 40) to (y 48, z 14), then line to (y 50, z 3).
- **Rear chamfer:** line from (y -38, z 13) to (y -27, z 2).

## 14. Independent measurements

| Quantity | From dimensions | From ratios | From photo pixels | Reconciled |
|----------|-----------------|-------------|-------------------|------------|
| Total width / pod length | 134 / 76 = 1.76 | 2 pods + slot | aws76: plates span 760 px vs pod side ~640 px (oblique) ≈ 1.2-1.8 | 1.75 |
| Height / pod length | 38 / 76 = 0.5 | - | aws74: near side 380 px tall vs 470 px long ≈ 0.55 (perspective) | 0.5 |
| Slot / total width | 12 / 134 = 0.09 | ≈ disc + 2 x 4.5 | aws74: slot 60 px vs plates 2 x 300 px ≈ 0.1 | 0.09 |
| Skirt projection / pod length | 25 / 76 = 0.33 | - | aws72: skirt 230 px vs pod side 600 px (oblique) ≈ 0.35 | 0.33 |
| Cam dia / pod height | 30 / 38 = 0.79 | - | aws72: cam 190 px vs side 300 px ≈ 0.65 (cam partly hidden) | 0.75 |
| Hump height above lid | 14 | 0.37 H | aws72: 120 px vs pod height 320 px ≈ 0.38 | 14 |
| Disc dia / height | 44 / 38 = 1.16 | fills the slot | aws74: hook arc 280 px vs plate 330 px | 1.1 |

## 15. Consistency check

1. **Front plate shape:** flat sloped (blue photos) vs curved (white photo). Chosen: flat sloped face + bottom lip (the
   blue version is two of three photos).
2. **aws74 view label:** REFERENCE.json says rear_right_iso but the plates (front) face the camera. The label was set
   for silhouette fit; the description uses the front.
3. **Switch position:** different in the two versions; chosen the blue position (left lid, front outer corner).
4. **Charging port:** recessed socket (blue) vs a red plug standing up (white). Chosen: recessed red socket on the
   right lid near the front, modelled as a connector, not a weapon.
5. **Cam count:** 3 discs per pod in every photo; the earlier model used 2 cam parts per side. Chosen: 3.
6. **Weight class:** shuffler = AWS walker class (225 g in this toolchain via `locomotion: walker`).

---

## 16. Why the designer did it (per part)

| Part | Fight benefit | Construction (print / assembly / cost / weight / repair) | Other |
|------|---------------|-----------------------------------------------------------|-------|
| Shuffle cams instead of wheels | walker class (higher weight limit) for a heavier, tougher body; cams are hard to stall on debris | printed discs with TPU pads, easy to replace | the novelty of a shuffler |
| Twin pods with a centre slot | disc is shielded on both sides; pods are independent drive units | each pod prints without supports; one design printed twice | symmetric, self-righting not needed if cams reach both faces |
| Rear-bottom chamfer | lets the robot tip back and recover; nothing to grab at the rear | removes mass from an unloaded corner | helps the cams find the floor when rocking |
| Flat lids with windows | invertible: cams work both ways up | windows give access to the cams; lids screwed for service | - |
| Side panels with fins | fins stop the robot lying flat on a side | panels unscrew to reach the internals | - |
| Grey metal front plates | wedge-like face deflects and lifts; metal resists spinner bites | bent sheet, cheap; screwed on top edge | - |
| Ribbed floor skirts | get under opponents (low leading edge); flexible so they hug the floor | ribbed print stiffens along x but flexes in y | the robot rests on them at the front between cam steps |
| Thin hook disc in the slot | vertical-spinner bite upward, hooks catch and flip | small disc, low energy but cheap; slot protects it | weight saved goes into the walker body |
| Disc guard hump | protects the disc and motor top from overhead hits; stops the disc touching the arena wall | printed as part of the lids | carries the lock-pin hole |
| Charging port on top | charge without opening the robot | panel-mount JST, glued in a pocket | - |
| Switch on the top | reachable for the rules, recessed against hits | - | - |
| Black screws on the lids/panels | lids and panels are serviceable | M2 into heat-set inserts or self-tapped | - |

## 17. Unseen and inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (frame of section 11) | Confidence |
|------|-------|-----------|--------------------------------|------------|
| Battery | 2S LiPo 300 mAh | 52 x 12 x 12 | in the left pod front half along y, (-36, 15, 12) | medium |
| Drive ESC + receiver | Malenki-Nano class | 32 x 19 x 2.5 | right pod front half, (36, 15, 10) | medium |
| Weapon ESC | small brushless ESC | 23 x 12 x 4 | bridge or right pod front, (20, 5, 10) | low |
| Cam motors | 2 x N20 gearmotor (high-torque 100:1 or 150:1) | 12 x 10 x 24 | in each pod beside the cam stack, axis x, (±56, -18, 21) | medium |
| Cam axles | 3-4 mm steel or the motor D-shaft extended | 3 dia x 30 | through each stack at (±40, -18, 21), outer end in a printed bearing boss | medium |
| Cam bottom windows | same as the top windows | 28 x 22 | in each pod floor under the stacks | high (needed to walk) |
| Weapon motor | 1105-1306 outrunner | 14-18 dia x 12 | in the slot behind/under the disc, stator on the bridge or one pod wall, (±7, 22, 22) | medium |
| Disc fixing | 2-3 M2 screws into the bell | M2 x 4 | on the bell face | medium |
| Lock pin | 2-3 mm pin through the hump hole and the disc | 3 x 30 | along x at (0, 18, 46) | low |
| Lid screws | about 6 x M2 per lid into bosses in the pod walls | M2 x 8 | 4 corners + 2 mid-sides | high (visible heads) |
| Side panel screws | 4 corners + 1 centre (green insert) per side | M2 x 6 | as section 4.3 | high |
| Front plate screws | 2-3 on top flange + 2 at the outer side | M2 x 6 | top edge y 36, outer side z 10/30 | medium |
| Skirt clamp | skirt rear strip clamped between plate lip and pod floor, 2 screws | - | y 40-46 | low |
| Wiring | battery (left) -> switch (left top) -> through the bridge to the right pod ESC; ESC -> both cam motors (one through the bridge); weapon ESC -> motor phases in the slot; charge lead from the battery balance tap to the red port on the right lid | 20-28 AWG | across the bridge at z 25-35 | medium |
| Internal ribs | a cross wall in each pod between the electronics bay (front) and the cam bay (rear) | 2 thick | y ≈ -5 | low |

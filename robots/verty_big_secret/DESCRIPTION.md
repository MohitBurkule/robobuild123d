# Verty Big Secret: full description from the reference photos

This file describes the robot from the three reference photos only, in enough detail to rebuild it without the photos. No CAD, drawings or measurements of the real robot were available.

**How dimensions were worked out.**
- Each dimension is derived from pixel ratios in the photos.
- The scale comes from the drive wheel: an AWS antweight on N20-class gearmotors almost always runs 26-30 mm wheels. Here the diameter is taken as **28 mm**, and every other size is a ratio of that.

**How sure each statement is.**
- `[seen]`: directly visible in at least one photo.
- `[inferred]`: follows from what is visible plus how such robots are normally built.
- `[guess]`: hidden or ambiguous; the most likely reading.

Model axes used throughout:
- **+y** is forward (the fork tips point +y).
- **+x** is the robot's right.
- **+z** is up.
- **z = 0** is the wheel axle height.
- The floor is z = -14 (the bottom of a 28 mm wheel).

"Inner" means toward the centre slot. "Outer" means toward the wheels.

---

## 1. The photos and what each one shows

### 1.1 `reference/verty_big_secret.aws72.webp`

**Camera.** About 35 deg above the floor, looking at the front-right corner. The fork tips point to the lower left of the frame. The right pod is nearest the camera, and its rear wheel is at the right edge of the frame.

**Weapon fitted.** A two-plate weapon `[seen]`:
- A thin ring-like disc with bright ground edges. The edge light is green/white from the studio lighting.
- A black, eccentric two-lobed disc. One lobe has a large round lightening hole that makes it look like a "C".

**Also visible.**
- A red anodised outrunner with the white "FLASH HOBBY" lettering on its can.
- A large silver nyloc nut and washer on the axle at the near (right) side plate.
- A red JST-style connector, with a short red lead, lying on top of the right pod deck.
- The black rear cross tube between the pods, high up behind the weapon.
- Silver button-head screws in the front faces of both pods, and black button-head screws with washers on the deck corners.

### 1.2 `reference/verty_big_secret.aws74.webp`

**Camera.** Low, about 20-25 deg above the floor, looking from the front-right toward the left side. The fork tips point to the lower right.

**Weapon fitted.** A ring with about 8 saw teeth `[seen]`. Each tooth has a hooked front and a ground (bright) flank. The ring has large spoke windows inside it.

**Side plate.** The left pod's side plate fills the middle of the frame, seen from its outer/left side. It shows:
- 4 screws around the motor: 2 small black cap screws plus 2 counterbored holes.
- An oval wire window low down, with the twisted motor phase leads visible through it.
- A tall curved horn at the top-rear.

**Motor.** The same red FLASH HOBBY outrunner; "B6" is visible on the can.

**Pod rear.** Far left of the frame:
- An oval hole in the outer side/rear face of the left pod `[seen]`. It is a switch or charge access hole, or a wheel-motor access hole `[guess]`.
- A sloped flat panel near the rear wheel `[seen]`, possibly a rear wheel guard `[guess, only in this photo]`.

### 1.3 `reference/verty_big_secret.aws76.webp`

**Camera.** High, about 45 deg, looking from the front-left. The fork tips point to the lower right. The left pod and its rear wheel are nearest, at the lower left of the frame.

**Weapon fitted.** A single large curved hook tooth `[seen]`:
- Shaped like a shark fin or crescent.
- A triangular lightening window in the middle.
- Ground bright edges.
- It stands very tall: the tip is about 2.5 times the pod height above the deck.

**Motor.** Black, with "CE RoHS" printed on it.

**Left side plate.** Seen in full from the outer side:
- 2 silver cap screws and 1 black cap screw around a central bore.
- A second small hole below the bore.
- An oval wire window lower down.
- A horn at the top-rear with a coarse, knurled/stippled tip `[seen]`. The tip looks melted or textured, perhaps a grip-texture print artefact.

**Other details.**
- A second horn is visible behind it. That horn belongs to the right side plate, on the far side of the slot.
- The left pod deck plate shows clearly. It is a smooth, slightly glossy black sheet with a notch where the side plate passes through it.
- The left pod side wall has a small round hole near the front, about 2 mm `[seen]`.

**Event-to-event differences.** The chassis, side plates, forks and wheels are the same in all three photos `[seen]`. Only the weapon changes, plus the motor colour (red in aws72/74, black in aws76). Unless stated otherwise, the rebuild should use the aws72 configuration, because that photo shows the most parts.

---

## 2. Overall architecture

The robot is a **vertical spinner on a twin-pod chassis**:
- Two rectangular box pods run front to back, one on each side.
- They are separated by an open centre slot, and are joined only behind the slot.
- The weapon, a disc or hook on an axle along x, spins in the slot, carried between two tall vertical side plates. The plates stand on the inner edges of the two pods.
- The weapon motor is a direct-drive outrunner. It is bolted to one side plate and sits in the slot beside the weapon.
- Two long tapered forks stick out forward from the bottom of each pod's nose and rest on the floor.
- One wheel per side sits at the rear outer corner of each pod, in a notch of the pod outline. The robot has 2WD skid steer, and the forks are the front skids.

Overall proportions `[inferred from aws72/aws76]`:

| Quantity | Ratio | mm (wheel = 28) |
|---|---|---|
| Pod length (rear face to nose tip, without forks) | ~2.8 × wheel dia | ~78-80 |
| Pod height (floor gap excluded, deck plate included) | ~0.7 × wheel dia | ~20 |
| Pod width (outer face to slot face) | ~0.8 × wheel dia | ~22-23 |
| Slot width | ~0.85 × wheel dia | ~24 |
| Overall width across wheels | ~3.3 × wheel dia | ~92 |
| Fork length beyond the pod nose | ~1.1-1.2 × wheel dia | ~30-34 |
| Side plate height above the deck (to the top of the round boss) | ~1.0 × pod height | ~20-24 |
| Horn tip height above the deck | ~1.6 × pod height | ~34-38 |
| aws72 disc diameter | ~0.75 × pod length | ~56-60 |
| Weapon axle height above the floor | ~1.2 × wheel dia | ~32-34 (z ≈ +18 to +20) |
| Motor can | ~0.65 × wheel dia across, ~0.55 long | ~18 dia × 16 |

---

## 3. Part list

| # | Part | Count | Material / colour | Size (mm, approx.) | Held by |
|---|---|---|---|---|---|
| 1 | Pod body (left, right) | 2 (or one U print) | Black PLA/PETG, matte, visible layer lines | 80 L × 23 W × 18 H each | Joined at the rear by a bridge or tube |
| 2 | Deck plate | 2 | Black, smooth, slightly glossy: polycarbonate, G10 or a printed smooth-face plate `[guess]` | ~70 × 22 × 1.5 | 4 black button screws with black washers each `[seen]` |
| 3 | Nose block / fork mount | 2 | Black print, visibly coarser layers than the pod | Triangular prism ~20 W × 14 L × 18 H | 2 silver button-head screws per side `[seen]` |
| 4 | Fork | 2 | Black print | ~34 L × 10 W root, 3 W tip | Part of the nose block print, or clamped into it `[guess]` |
| 5 | Side plate (motor side) | 1 | Black print, ~3 mm, printed flat | ~36 L × 26-30 H above the deck, plus horn | Tabs through the deck plate into the pod `[inferred]` |
| 6 | Side plate (bearing side) | 1 | Same | Same outline, mirrored | Same |
| 7 | Weapon motor | 1 | Red anodised (aws72/74) or black (aws76) outrunner | ~18 dia × 16 L | Screwed to the side plate with 2-4 M2 screws on a ~9 mm PCD `[seen 2 screws + holes]` |
| 8 | Weapon | 1 | Hardened steel, black oxide/powder coat, ground bright edges | aws72 version ~56-60 dia, ~3 thick | On the motor bell with the axle; nyloc nut outboard `[seen nut]` |
| 9 | Weapon axle / bolt | 1 | Steel, silver | M4-M5 × ~30 `[guess]` | Nyloc nut and washer on the bearing-side plate `[seen]` |
| 10 | Rear cross tube | 1 | Black: carbon tube or printed `[guess]` | ~6-8 dia, spans the slot | Ends in the side plates or the pod inner walls `[guess]` |
| 11 | Wheel | 2 | Black print, knurled tread (gear-like ridges), 3-spoke hub | 28 dia × ~9 W | Press-fit on the gearmotor D-shaft `[inferred]` |
| 12 | Drive gearmotor | 2 | N20 / Pololu micro metal gearmotor `[inferred]` | 12 × 10 × ~25 + 9 gearbox | In a pocket in the rear of each pod `[inferred]` |
| 13 | LiPo | 1 | Hidden | 2S 300-450 mAh `[guess]` | Inside a pod |
| 14 | Drive ESC / receiver | 1 | Hidden | Malenki-style ~32 × 19 board `[guess]` | Inside a pod |
| 15 | Weapon ESC | 1 | Hidden | ~23 × 12 `[guess]` | Inside a pod |
| 16 | Wires | several | Black silicone motor phase leads (3, twisted) `[seen]`; a red lead with JST `[seen]` | | Through the side plate window into the pod |
| 17 | Power switch / link | 1 | Hidden | | Behind the small round or oval side hole `[guess]` |

---

## 4. Part-by-part description

### 4.1 Pods (chassis)

**Shape.** Each pod is a closed rectangular box `[seen]`:
- Vertical outer and inner side walls.
- A flat top covered by the deck plate.
- A flat bottom sitting about 2 mm above the floor `[inferred]`. A sliver of light shows under the pods in aws74; the robot rests on the wheels and fork tips.
- The vertical edges are sharp: no visible fillets.
- A thin raised lip, about 1 mm, runs round the top of the walls on which the deck plate sits `[seen in aws76 as a darker line between the plate and the wall]`.

**Size.** Each pod is about 80 long × 23 wide. The body is about 18 tall, with a 1.5 mm deck plate on top, so the top of the plate is at z ≈ +8.

**Rear end.**
- The rear end of each pod is cut into an inward notch at the outer side, around the wheel `[seen aws72 rear crop]`. The deck outline curves inward with a concave radius of about 6 mm, just ahead of the wheel. Behind that, the pod continues narrower, by about one wheel width, to the rear face.
- So the wheel sits partly inside the full-width pod envelope. Its outer face sits about 2-4 mm proud of the forward part of the outer wall `[inferred]`.
- The rear face of each pod is flat and vertical, at about the wheel axle line or 4-6 mm behind it. The rear half of the wheel tyre protrudes behind the pod by roughly 8-10 mm `[seen aws76]`.

**Slot.**
- Between the pods there is an open slot about 24 wide. It is open at the front, the top and the bottom.
- The pods are joined behind the slot. The rear section is about 25-30 long and contains the two drive gearmotors, back to back along x `[inferred]`.
- High up at the rear of the slot, a black cross tube joins the two side plates or pod walls `[seen aws72]`. It sits behind the weapon's sweep at about deck height + 10 mm.

**Openings.**
- A small round hole, about 2-3 mm, in the left pod outer wall about 10 mm behind the nose block, at mid height `[seen aws76]`. It is probably a switch-pin or LED hole `[guess]`.
- An oval hole, about 8 × 5, in the outer/rear face of the pod near the wheel `[seen aws74]`. It is probably the power switch or a link access `[guess]`.

**Colour.** Matte black. The visible layer lines show the pods are printed upright, with layers horizontal.

### 4.2 Deck plates

**Shape and position.**
- One flat sheet per pod, about 1.5 thick, covering the whole top of that pod from just behind the nose block to the rear face `[seen aws72, aws76]`.
- The plate follows the pod outline, including the concave notch in front of the wheel `[seen aws72]`.
- It is slightly wider than the pod walls (overhang ≤ 0.5 mm) and has square corners.
- On the inner long edge there is a rectangular notch, about 3 × 30, where the side plate's foot passes down through it into the pod `[seen aws76: the plate edge steps around the side plate, and there is a small printed fillet/rib on the pod at the front of the notch]`.

**Fixing.** 4 black button-head screws (M2 or M2.5) with black washers per plate, one about 4 mm in from each corner `[seen: aws72 near pod shows front-inner, front-outer, rear-outer and rear-inner; aws76 shows front-outer and rear-outer on the left pod]`. They thread into the pod walls (heat-set inserts or self-tapping into printed bosses `[guess]`).

**Colour.** Slightly glossier black than the pods. It reads as a smooth sheet with scuffs and white scratches `[seen aws76]`. Material is likely black polycarbonate or a smooth-face printed plate `[guess]`.

### 4.3 Nose blocks (fork mounts)

**Shape.** At the front end of each pod, a separate block forms the nose `[seen: a visible seam, different layer texture]`:
- A wedge/pyramid, with its outer face sloping down and outward from the deck edge toward the fork root.
- In aws76 the outer face of the left nose block is a steep triangular facet. In aws72 the right nose block's front face is a vertical rectangle, about 20 wide × 12 high, with a chamfer down into the fork.

**Fixing.** Each nose block is fixed to the pod by 2 silver button-head hex screws, M3 `[guess on size]`. The screws enter horizontally from the front/outer faces `[seen aws72]`:
- One in the front face upper-outer corner.
- One in the inner face near the slot, low down.
- In aws76 the screws also show nyloc nuts on the inner face of the slot `[seen silver hex nuts]`.

So the screws pass across the nose block through both walls and are nutted. In other words, through-bolts clamp the fork arm in the nose block `[inferred]`.

**Position and colour.** The block's top is flush with the deck plate's top or 1 mm below it. Its bottom is flush with the pod bottom. Black.

### 4.4 Forks

**Count and position.** 2 `[seen]`, one per pod, centred on the pod width (fork centreline x ≈ ±23).

**Shape.**
- Each fork starts at the bottom of the nose block as an arm about 8-10 wide × 8-10 tall.
- It curves down and forward with a concave upper edge, a cove of radius about 15 `[seen aws72: the arm swoops from mid-pod height down to the floor]`.
- It then runs straight and level along the floor, tapering in plan to a blunt point about 3 mm wide.
- The top surface of the straight part slopes down toward the tip, giving a thin wedge cross-section.
- At the very tip there is a small vertical end face, about 3 × 2 `[seen aws72: the tips look cut square]`.

**Length.**
- From the nose face to the tip: about 32-36.
- The straight floor-contact part is about 22 long.
- The underside is flat and touches the floor along its last 15-20 mm `[inferred]`.

**Gaps and alignment.**
- Gap between the two forks: about 30 between their inner edges.
- They are parallel, with no toe-in.
- They do not reach under the weapon: the weapon is between them and further back.

**Colour.** Black print with coarse diagonal infill marks on the top `[seen]`.

### 4.5 Side plates (weapon supports)

**Count and position.** Two, one on each pod's inner edge, facing each other across the slot `[seen aws72 both, aws74/aws76 left one clearly]`.

**Thickness and fixing.** About 3 mm thick. The face shows layer lines in a fine pattern parallel to the face, so the plates are printed flat `[seen aws76]`. A plate stands vertical in the yz plane, with its inner face flush with the pod's inner wall (the slot face). It passes through the deck plate notch and continues down inside the pod, held by tabs or screws `[guess]`.

**Outline, left plate as seen in aws76, from the rear going clockwise:**
1. A vertical rear edge rises from the deck at about y = -8 (10 mm ahead of the wheel axle).
2. This becomes the **rear horn**: a crescent curving up and backward. Its tip is about 30 above the deck and about 6 behind the rear edge. Its root is about 10 wide, tapering to about 3 at the tip.
3. The horn's front edge curves down into a U-shaped valley. The bottom of the valley is about 12 above the deck.
4. The edge then rises in a smooth convex curve into the **motor boss**: a large disc-shaped part of the plate, about 32 dia, centred on the weapon axle.
5. The boss's outline runs over the top and down the front of the plate as a full semicircle.
6. A straight front edge then runs down to the deck at about y = +32.

**Holes in the plate.**
- A central bore, about 6 dia, for the motor shaft and circlip `[seen aws76: a bright green-tinted spot, the motor shaft end]`.
- 3-4 motor screws on a 9-12 PCD round the bore `[seen: 2 silver M2 cap screws + 1 black M2 cap screw + 1 smaller hole]`.
- A small hole about 6 below the bore.
- An **oval wire window**, about 12 × 8, with its long axis vertical, about 8 above the deck and 4 behind the boss centre. The three twisted motor phase leads pass through it into the pod `[seen aws74, aws76]`.

**Second horn.** Behind the left plate in aws76 there is a second horn `[seen]`. It is the same shape and belongs to the **right** side plate.

**Right plate (bearing side) in aws72.**
- It carries the axle nut.
- Its boss outline is the same.
- Its horn is at the rear-top, pointing up and back.
- It has no motor holes. It has a single axle bore with a large flat washer and a nyloc nut on its outer face `[seen]`.

**Dimensions relative to other parts.**
- Plate boss radius is about 16. That is 1.8 × the motor can radius and 0.55 × the aws72 disc radius.
- Axle height is about 20 above the deck top, which puts it at z ≈ +20 in model coordinates.
- Horn tip height is about 36 above the deck. It is below the top of the aws72 disc and well below the aws76 hook.

**Colour.** Black, matte, with a fine layer texture. The aws76 left horn tip is grey-black and stippled.

### 4.6 Weapon motor

**Type.** An outrunner about 18 dia × 16 long, the FLASH HOBBY 1404/1406 class `[seen lettering]`:
- aws72/74: red anodised can with slotted windows. Copper windings show through the windows `[seen aws74]`.
- aws76: black can with a white "CE RoHS" print.

**Mounting.**
- The stator base is screwed flat to the slot face of the **left** side plate `[seen aws76: the screws are on the outside of that plate, the motor is on the slot side]`.
- The can turns in the slot.
- The motor occupies about 16 of the 24 slot width, starting about 0.5 mm from the left plate.

**Drive.** The weapon is clamped to the bell end, the side facing +x `[seen aws72: the disc sits directly against the right end of the red can]`.

**Gaps.**
- Bell end to the right side plate: about 7-8 mm, the space for the weapon plates, a washer and spacers.
- Can to the deck: the bottom of the can is about 10 above the deck.
- Can to the rear tube: about 4 `[guess]`.

### 4.7 Weapon (aws72 configuration, used for the rebuild)

**Two parts.** The weapon has two parts clamped together on the axle `[seen]`:

1. **Disc ring.**
   - A thin steel disc, about 2-3 mm, with a large central opening. It looks like a ring with a band about 8-10 wide.
   - Outer diameter about 56-60.
   - The edge is ground bright all round.
   - It is offset toward the motor, next to the can.
2. **Two-lobed plate.**
   - A black steel plate, about 3 mm, shaped as a lopsided two-lobe disc.
   - The bigger lobe carries a large round window, about 18-20 dia, which leaves a C-shaped rim.
   - The smaller lobe ends in a hooked tooth.
   - Outer radius at the tooth is about 30; the minimum radius is about 22.
   - It sits nearest the right (bearing-side) plate, about 1-2 mm from it.

In model terms: a two-tooth disc, radius about 29, about 3 thick total, with large lightening holes. The weapon's lowest point is about 5-6 above the floor. At the front, the tooth tips pass about level with the pod noses, and well behind the fork tips.

**Other events.**
- aws74: an 8-tooth saw ring, about 60 dia, with spoke windows.
- aws76: a single crescent hook with a triangular window. Its tip radius is about 45 and it rises far above the side plates. Its heel is a wide round hub about 32 dia that hides behind the motor.

### 4.8 Weapon axle

- A silver steel bolt runs through the right plate, the weapon plates and spacers, into the motor bell `[inferred]`.
- On the right plate's outer face there is a large silver nyloc nut (about M5) over a flat washer `[seen aws72]`.
- The nut stands about 5 proud of the plate, inside the right pod's deck area. It sits above the deck, not over the slot.

### 4.9 Rear cross tube

- A black cylinder about 7 dia, running across the slot at the rear, behind the weapon `[seen aws72: a dark tube between the disc and the far pod at upper right, with wires running past it]`.
- About 10-12 above the deck, at y ≈ -8.
- Probably fixed between the two side plates' rear edges, stiffening them `[guess]`.

### 4.10 Wheels

**Count, size and tread.**
- Two, about 28 dia × 9 wide `[seen]`.
- The tread is a printed knurl: about 48 square ridges round the circumference, about 1 mm deep, giving a gear-like edge `[seen aws72, aws76]`.

**Hub.**
- The outer face is a flat disc recessed about 1 mm inside the tread rim.
- The 3-spoke hub has three curved triangular windows, about 7 mm each, between spokes 3 wide `[seen aws76: three large windows with curved sides]`.
- A small central boss carries a screw or the shaft end `[seen]`.

**Colour.** Black. The tread shows grey scuffing.

**Position.**
- At the rear outer corner of each pod, in the notch (see 4.1).
- The wheel's inner face is about 1-1.5 mm from the notch wall.
- The axle (gearmotor shaft) is at z = 0, about 10 above the pod bottom.
- The tyre protrudes about 4 below the pod bottom (pod bottom at about z = -12).
- No wheel guard in aws72 and aws76 `[seen]`. aws74 may show a sloped guard panel by the left wheel `[guess]`.

**Fixing.** The wheel presses onto a 3 mm D-shaft `[inferred]`. A small central screw is visible in aws76.

### 4.11 Drive motors

- Hidden. They are in the rear part of each pod, axis along x, gearbox outboard, shaft through the notch wall into the wheel `[inferred]`.
- Behind the slot they would sit back to back.

### 4.12 Electronics

- Hidden under the deck plates `[seen: nothing visible]`.
- A 2S LiPo (about 36 × 17 × 11) lies lengthwise in one pod.
- A drive ESC/receiver board (about 32 × 19) and a weapon ESC (about 23 × 12) lie lengthwise in the other `[guess]`.

**Wires.**
- **Motor phase leads.** Three black twisted motor phase leads run from the motor base through the side plate's oval window into the left pod `[seen]`.
- **Red lead with JST plug.** A short red lead with a red JST plug sits on top of the right pod deck, next to the side plate `[seen aws72]`. It is probably a removable power link (the "switch") plugged in from the top `[guess]`.

---

## 5. Contact and gap matrix (model coordinates)

| Part A | Part B | Relation | Gap / overlap |
|---|---|---|---|
| Pod (left) | Pod (right) | Joined behind the slot | Slot 24 wide in front of y ≈ -10 |
| Deck plate | Pod | Sits on the pod top lip | 0 (screwed, 4×) |
| Deck plate | Side plate | Plate foot passes through the deck notch | ~0.3 clearance |
| Side plate | Pod inner wall | Inner face flush with the slot face, tab inside | 0 (tab / screws) |
| Nose block | Pod front | Face to face | 0 (2 through-bolts) |
| Fork | Nose block | One piece, or clamped | 0 |
| Fork | Floor | Last ~15-20 mm touch the floor | 0 |
| Fork | Weapon | Fork tips ahead of the weapon; forks outside the slot width | ≥ 6 in x |
| Weapon | Side plate (right) | Weapon plate face to plate face | ~1-2 |
| Weapon | Motor bell | Clamped to the bell | 0 |
| Motor base | Side plate (left) | Screwed face to face | 0 |
| Motor can | Deck | Above the deck, inside the slot | ~10 |
| Weapon bottom | Floor | Weapon sweeps the slot | ~5-6 |
| Weapon | Slot rear wall / cross tube | Sweep circle | ≥ 2 |
| Wheel inner face | Pod notch wall | Side by side | ~1-1.5 |
| Wheel | Floor | Contact | 0 |
| Pod bottom | Floor | Clearance | ~2 |
| Axle nut | Right side plate | Clamped on the outer face | 0 |
| Cross tube | Side plates | Ends fixed in the plates | 0 `[guess]` |
| Horn | Side plate | One piece | 0 |

## 6. Mechanism summary

**Drive.** Two rear wheels driven by gearmotors give skid steer. The front of the robot rests on the two fork tips sliding on the floor.

**Weapon.** The direct-drive outrunner spins the steel disc in the centre slot about the x axis. The tooth comes up at the front, so it hits upward. The weapon is carried at both ends:
- by the motor bearings on the left plate;
- by the axle bolt and nut in the right plate.

**Forks.** They get under opponents and lift them into the disc. They are bolted on and replaceable.

**Horns.** They are cosmetic. They also act as top guards that stop an opponent riding up onto the deck and stop the robot resting on its back. On its back, the robot rests on the horns and weapon. So it is not invertible: it is a self-righting-by-weapon design `[inferred]`.

## 7. Notes for the rebuild

**Matching the outline.** These features drive the silhouette:
1. The twin pods and open slot.
2. The disc large and low in the slot.
3. The forks as long thin spikes reaching the floor.
4. The tall side plates with rear horns.
5. The wheels at the rear corners in notches.

**Details that matter visually.**
- 4 deck screws per pod.
- 2 silver bolts per nose block.
- The axle nut.
- The red motor can.
- The knurled tread and the 3-spoke hubs.

**Proportions.** Keep the mass under 150 g. The real robot uses a 3 mm steel weapon, about 30-35 g, and a lot of the chassis volume is empty. The pods are thin-walled shells about 1.2-1.5 mm thick.

---

## 8. Shapes as mathematical curves

All curves below are in the model frame: x is right, y is forward, z is up, in mm. The origin is the midpoint between the two wheel axle centres at axle height. The floor is the plane z = -14. Each curve says which plane it lies in.

### 8.1 Pod plan outline (xy plane, right pod; the left pod is the mirror x → -x)

A closed polygon with one concave arc:
- **Straight edges, from the rear-inner corner:**
  - (12, -38) → (35, -38). Rear face. `[inferred]`, ±3.
  - (35, -38) → (35, -22). The wheel-notch zone. Here the outer wall is at x = 35 - 9 = 26 when the notch is modelled. In the simplified build the wheel sits fully outboard and the wall stays at x = 35.
  - (35, -22) → (35, 32). Outer side wall.
  - (35, 32) → (27, 40). Outer front chamfer at 45 deg: the nose block's sloped outer facet. In 3D it is a pyramid facet, see 8.3.
  - (27, 40) → (12, 40). Front face.
  - (12, 40) → (12, -10). Inner (slot) wall.
  - (12, -10) → (-12, -10). Slot rear wall (shared with the left pod).
- **Wheel-notch concave fillet (if modelled).**
  - A quarter circle with centre (26 + 6, -22 + 6) = (32, -16) and r = 6, spanning angles 180 deg → 270 deg. Points: (26, -16), (27.76, -20.24), (32, -22).
  - Its job is to let the deck curve inward toward the wheel `[seen aws72 rear crop]`.

### 8.2 Pod side profile (yz plane)

- A rectangle from y = -38 to 40 and z = -12 to 6.5 (the body).
- The deck plate adds z = 6.5 to 8.
- The bottom is flat at z = -12, which is 2 above the floor.

### 8.3 Nose block

The nose block is the volume y = 32 to 40, x = 12 to 35, z = -12 to 8, minus a chamfer plane on the outer front vertical edge, x + y ≥ 67.

- **Outer front facet.** A rotated plane: the facet contains the vertical line (35, 32, z) and the line (27, 40, z). In aws76 it also leans in toward the top, losing about 3 mm over the 20 mm height `[guess]`.
- **Bolt holes.** Two horizontal bolt holes, diameter 3.2:
  - axis along x at (y = 36, z = 2);
  - axis along y at (x = 31, z = -6) `[guess on positions; seen counts]`.

### 8.4 Fork (right; left is mirrored)

The fork is the intersection of a plan prism and a side prism.

- **Plan** (xy plane, extruded along z): the trapezoid (17.5, 39), (29.5, 39), (24.7, 72), (22.3, 72).
  - Root width 12, tip width 2.4.
  - Taper half-angle: atan((6 - 1.2) / 33) = 8.3 deg.
- **Side** (yz plane, extruded along x): the polygon (39, -15.5), (72, -15.5), (72, -12), (39, 6).
  - Top edge as a line: z(y) = 6 - (18 / 33)(y - 39) for 39 ≤ y ≤ 72. That is a slope of 28.6 deg down toward the tip.
  - The photo shows the top as a concave cove instead `[seen aws72]`. As a circle: centre (y = 39, z = -12 + 30) = (39, 18), r = 30, from angle 270 deg (point (39, -12)) toward 315 deg... Simplified: the cove is z(y) = 18 - sqrt(30² - (y - 39)²) for 39 ≤ y ≤ 60. After that the top is flat at z = -10 out to the tip at y = 72.
- **Bottom.** z = -14 (on the floor) for y from 55 to 72. The model uses -13.5 so the fork does not decide the floor.

### 8.5 Side plate (yz plane, 2.5-3 thick)

Outline points, clockwise from the rear foot:
- A straight line from (-4, 8) to (30, 8): the foot on the deck.
- A straight line from (30, 8) to (30, 20): the front edge.
- **Motor boss arc.** Centre (16, 20), r = 14, from 0 deg to 90 deg. Points: y = 16 + 14cos(t), z = 20 + 14sin(t), t = 0 to 90 deg. It ends at (16, 34).
- **Valley.** A line from (16, 34) to (8, 33.5), then into the horn.
- **Horn front edge.** A quadratic Bezier with control points P0 = (8, 33.5), P1 = (2, 40), P2 = (-6, 48): the tip.
- **Horn rear edge.** A quadratic Bezier with control points P0 = (-6, 48), P1 = (-2, 38), P2 = (-4, 26).
- A straight line from (-4, 26) down to (-4, 8).
- **Holes:**
  - The axle bore, a circle at (16, 20) with r = 2 (bearing side) or r = 4 (motor side, shaft clearance).
  - Motor screws at (16 ± 4.5, 20), r = 1.2 (aws76 shows 3-4 on the 9 mm PCD).
  - The wire window, an ellipse with centre (12, 13), semi-axes a_y = 3 and a_z = 5 `[seen shape; position ±3]`.
- The horn tip height of 48 above the axle line gives 40 above the deck. This is checked against the photos in section 10.

### 8.6 Weapon (aws72-style two-lobe disc, plane of the disc = yz, thickness along x)

**Profile.** Polar form, r(θ) about the axle:
- r(θ) = 29 for the tooth lobes. The tooth is a spiral ramp: r rises from 23 at θ = θ0 to 29 at θ0 + 150 deg, then drops radially back to 23 (the hook face).
- Two teeth, 180 deg apart.

**Spiral.** r(θ) = 23 + 6 (θ - θ0) / 150 deg, for θ0 ≤ θ < θ0 + 150 deg.

**Spline approximation used in the model.** 104 points with radius scaled from the 26 mm base spline to 29 mm (×1.115).

**Lightening holes:**
- Two big holes of r = 9.5 centred at polar (16, 90 deg) and (16, 270 deg).
- Two small holes of r = 6 centred at (13.5, 0 deg) and (13.5, 180 deg).

**Centre and thickness.** The centre bore has r = 2. The disc is 2.5 thick (two plates of 1.25 to 3 in the photo; 3 total `[guess]`).

### 8.7 Wheel

**Cylinder.** r = 14, width 9, axis along x, centre at (±40.5, -30, 0).

**Tread knurl.** 48 teeth. In polar form about the axle:
- r(φ) = 14 for φ mod 7.5 deg < 3.75 deg.
- r(φ) = 13 otherwise.

**Hub windows.** 3 windows, each bounded by:
- an inner arc with r = 3.5;
- an outer arc with r = 10;
- two lines at the angles of the spokes, spoke width 3 mm.

The windows are centred at 0, 120 and 240 deg.

---

## 9. Pixel measurements from the photos (independent check)

Original photo pixel coordinates; the origin is the top-left of the frame.

**aws72 (1348 × 1024).**
- **Near (right) wheel.** Ellipse bbox x 1130-1320, y 365-650. Its height is 285 px, which equals the 28 mm diameter, so the local scale is ≈ 10.2 px/mm at that depth.
- **Near fork.** From the nose bottom (700, 690) to the tip (480, 1000): 380 px ≈ 37 mm in the image plane. That is foreshortened by about cos(25 deg), so ≈ 33-38 mm true. Consistent with 33 (§8.4).
- **Near pod front face width.** x 620-940 ≈ 320 px. At the front the depth is closer, ≈ 12 px/mm, so ≈ 26 mm. This includes the nose block's outer facet. The pod width is 23, so the result is consistent.
- **Disc vertical extent.** y 135-620 = 485 px. At ≈ 9 px/mm (mid depth) that is ≈ 54 mm. Corrected for the 35 deg elevation, the vertical extent of a vertical disc is foreshortened by cos(35) = 0.82 → 54 / 0.82 ≈ 66. The disc's edge is not seen side-on in the image, so this measurement is unreliable. Taken as 56-62.
- **Nyloc nut.** About 75 px across → ≈ 7 mm across the flats, which fits an M4 nut (7 mm). The axle is therefore **M4**, refining the M5 guess in §4.8.

**aws76 (1831 × 1520).**
- **Near (left) wheel.** Bbox x 50-410, y 830-1250. The height is 420 px = 28 mm, so ≈ 15 px/mm.
- **Near fork.** Root (900, 1160) to tip (1440, 1440) ≈ 610 px ≈ 40 mm at 15 px/mm. The fork points partly toward the camera, so the true length is ≈ 33-40.
- **Side plate.** From the deck at (700, 900) to the horn tip at (520, 480): 420 px vertical ≈ 28 mm at ≈ 15 px/mm, with elevation 45 deg foreshortening the vertical by about 0.7 → ≈ 40 mm. The horn tip is 34-40 above the deck.
- **Motor can.** About 300 px diameter at ≈ 16 px/mm ≈ 19 mm. That fits a 1404-size motor (18.2 mm).
- **Hook weapon.** From the hub centre (980, 600) to the hook tip (950, 70): 530 px ≈ 33-45 mm with foreshortening. That is the aws76 hook radius.

**aws74 (1291 × 923).**
- **Motor can.** About 190 px across → at ≈ 10 px/mm ≈ 19 mm, consistent.
- **Saw ring.** The visible diameter is ≈ 600 px → ≈ 60 mm.

---

## 10. Consistency check (conflicts and the values chosen)

Each row gives the conflicting readings, the value chosen, and why.

| Quantity | Readings | Value chosen and reason |
|---|---|---|
| Pod length | Ratio method ~78-80 (§2). The model needs about 76 so the wheel motor pockets fit (y -36 to -24) and the slot can start at y -10. | **78** (y -38 to 40). The rear face sits 8 behind the axle, so the tyre still protrudes about 6 behind the pod, as seen in aws76. |
| Axle height above the deck | §4.5 says ~20; the aws76 pixels give 20-24. | §2 says the axle is 32-34 above the floor, i.e. z = +18 to +20. The deck is at z = 8, so the axle is 12 above the deck, not 20. The "20 above the deck" in §4.5 is the top of the boss above the deck, misread. Resolved: the axle is **at z = 20, 12 above the deck**. The plate boss (r 14) reaches z = 34, 26 above the deck, which matches "plate height above the deck ≈ 20-24 to the top of the boss" within tolerance. |
| Horn tip height | §4.5 ~36 above the deck; aws76 pixels 34-40; the §8.5 curve gives 40 above the deck. | **38-40 above the deck** (z ≈ 46-48). The model uses 48 (z = 46 + 2). |
| Weapon radius | aws72 disc 28-30 (§4.7); pixels unreliable (54-66 dia). The plate boss r 16 vs disc r 29 ratio of 0.55 matches §4.5. | **R = 29**. |
| Weapon lowest point | ~5-6 above the floor (§4.7). Axle z 20 - 29 = -9, which is 5 above the floor (z = -14). | **Consistent: 5**. |
| Axle size | The nut reads as M4 (pixels); §4.8 guessed M5. | **M4** in the description. The model shaft is 4 mm diameter. |
| Wheel position | §4.1 says the wheel sits in a notch with its outer face 2-4 proud. The simplified model puts the wheel fully outboard: the inner face 1 mm from the pod wall at x = 35, wheel centre x = 40.5. | The model is **outboard, without the notch**. The overall width becomes 2 × 45 = 90 against 92 from the photo ratio: consistent. The notch is a known visual difference. |
| Slot width vs motor + weapon | Slot 24 (§2). Motor 16 + 1.5 gap + disc 2.5 + 3.75 gap to the right plate = 23.75. | **24 holds**. |
| Fork length | Ratio 30-34; pixels 33-40 (aws72), 33-40 (aws76). | **33** (y 39 to 72). |
| Pod height | Ratio 0.7 × 28 = 19.6; model 20 (z -12 to 8). | **20**. |
| Motor side | aws76 shows the motor screwed to the left plate. aws72 shows the nyloc nut on the right plate. | **Motor on the left (-x) plate, bearing and nut on the right (+x) plate**: consistent across the photos. |
| Number of deck screws | aws72 shows 4 per pod; aws76 shows 2 visible per pod (the others hidden by the plate and horn). | **4 per pod**. |
| Rear cross tube | Seen only in aws72; not identifiable in aws74/76 (hidden behind the side plate). | **Present** `[seen once]`. Not modelled: it would sit inside the weapon swept circle's clearance zone in the model, and the rear bridge does its job. |

---

## 11. Why the designer did it (per part)

### 11.1 Twin pods with an open centre slot

**Fight benefit.**
- The disc can sit low, with its bottom about 5 mm off the floor, and still be fully enclosed at the sides. So the weapon meets opponents at fork height, right where the forks deliver them.
- The pods shield the disc's flanks from horizontal spinners.

**Construction.**
- Each pod is a simple prism that prints flat without supports. Two small pods fit a small print bed more easily than one wide tub.
- A damaged pod can be reprinted alone.
- The slot is open at the bottom, so nothing is printed under the weapon. That saves weight and gives debris a way out.

**Other.** The slot gives straight, fast access to the weapon motor and axle: undo the nut and the weapon slides out.

### 11.2 Deck plates (separate, 4 screws each)

**Fight benefit.**
- A smooth, slightly glossy top (PC or G10) lets opponents' weapons glance off.
- A flat top with no protrusions apart from the horns.

**Construction.**
- It is the service lid: the electronics in each pod are reached by removing 4 screws.
- A cut plate is stiffer per gram than a printed top skin, and it spreads hits over the whole pod wall.

**Repair.** A scuffed plate (aws76 shows deep white scratches) can be swapped without reprinting the pod.

### 11.3 Nose blocks, separate and through-bolted

**Fight benefit.** The front corners take the most hits. A sacrificial nose block absorbs them and protects the pod and its electronics.

**Construction.**
- The forks need a different print orientation: printed flat, so the layers run along the fork's length for bending strength.
- They also need a different infill: the coarse, solid-looking texture.
- Making them a separate part allows both.

**Repair and tuning.** Fork length and angle can be changed between fights (the forks changed little across the three events). The 2 through-bolts with nyloc nuts survive vibration better than screws into plastic.

### 11.4 Forks, long and thin, touching the floor

**Fight benefit.**
- They get under wedges and walls first.
- The ground contact keeps the front low so the opponent is lifted straight into the disc.
- Two separated forks also let the disc strike between them.

**Construction.**
- The thin wedge section is light (about 3-4 g each).
- They are printed flat, so the floor contact face is the bed face: smooth and flat.

**Other.** As skids, they carry the front of the robot without a front wheel or caster.

### 11.5 Side plates with horns

**Fight benefit.**
- They hold the weapon axle at both ends, so the disc stays aligned under impacts.
- The horns act as top bumpers: when the robot is flipped it rests on horns and weapon instead of the deck.
- The horns also deflect overhead hits and catch opponents climbing over the slot.

**Construction.**
- They are printed flat, with layers in the plate plane, so the axle loads run along the layers and not across them.
- Plates are cheap to reprint. The motor mount is just 2-4 screw holes on a 9 mm PCD.
- The oval window lets the motor leads pass straight into the pod, with no loose wire in the slot.

**Looks.** The shark-fin horns are part of the robot's identity: they are the "secret" profile.

### 11.6 Direct-drive outrunner

**Fight benefit.** No belt or gears means no drive train to fail, with full motor speed on the weapon. A small 1404 motor at about 3800 kV on 2S gives about 28 000 rpm unloaded.

**Construction.** Fewest parts. The weapon bolts to the bell, and the motor's own bearings carry the weapon on one side.

**Cost.** One about-£15 motor; swapping weapons between events is trivial (seen: 3 different weapons on the same motor and plates).

### 11.7 Steel weapon variations

**Fight benefit.**
- Fewer teeth (aws72's 2 teeth, aws76's single hook) give a bigger bite per hit.
- The 8-tooth saw (aws74) is for grinding contact against flat opponents.

**Construction.** The weapons are laser-cut sheet. Their large lightening windows keep the moment of inertia at the rim while saving mass for the 150 g limit.

### 11.8 Wheels at the rear, knurled

**Fight benefit.**
- The rear placement balances the robot with weight on the drive wheels, opposite the forks.
- The knurled tread grips the arena floor.
- The 3-spoke hubs save mass.

**Construction.** The wheels are printed in one piece, and the knurl is printed geometry, so no tyres need gluing. The notch in the pod lets the wheel sit inboard for a narrower robot `[seen aws72]`.

### 11.9 Rear cross tube

**Fight benefit.** It ties the two side plates together at the rear, stopping them spreading apart when the disc hits.

**Construction.** It is a short piece of stock tube or rod, light and stiff `[guess]`.

### 11.10 Red JST link on the deck

**Construction and rules.** A removable link is a cheap, light power switch that the AWS rules accept, and it is easy to reach on top `[guess]`.

---

## 12. Unseen and internal parts (guesses)

Each part below gives a position, a size, why it is likely there, and a confidence (high, medium or low). Coordinates are in the model frame.

### 12.1 Drive gearmotors (2)

- **Part:** Pololu / N20 micro metal gearmotor, 50:1 to 100:1. Body 12 × 10 × 24, gearbox 9 long, shaft 3 mm D.
- **Position:** axis along x at y = -30, z = 0. Gearbox and shaft outboard at |x| ≈ 31-36, motor can inboard to |x| ≈ 8.
- **Why:** the standard drive for an AWS antweight. The wheel size (28 mm) and the hub D-bore fit it.
- **Confidence:** high.

### 12.2 Gearmotor clamps

- **What:** a printed U-saddle in the pod floor holds each motor, with a strap or the deck plate pressing it down.
- **Size:** saddle walls 1.5 thick; the motor pocket is 12.5 × 10.5.
- **Confidence:** medium.

### 12.3 Battery

- **Part:** 2S LiPo, 300-450 mAh, about 36 × 17 × 11 (for example a 350 mAh).
- **Position:** lengthwise (long axis y) in the right pod, sitting on the floor: x 15-32, y -24 to 12, z -10 to 1.
- **Why:** it is the only pod volume long enough; the other pod takes the ESCs.
- **Confidence:** medium on position, high on type.

### 12.4 Drive ESC with built-in receiver

- **Part:** a Malenki Nano-class board, 32 × 19 × 2.5, wrapped in kapton.
- **Position:** flat on the left pod floor: x -33 to -14, y -21 to 11, z -10 to -7.5.
- **Confidence:** medium.

### 12.5 Weapon ESC

- **Part:** a 10-20 A brushless antweight ESC, 23 × 12 × 4.
- **Position:** flat in the left pod, ahead of the drive ESC: y 15 to 38, z -10 to -6. Short leads from there reach the motor phases through the left plate's oval window.
- **Confidence:** medium.

### 12.6 Power link

- **Part:** a red JST or XT30 removable link, on top of the right pod, about 15 × 6.
- **Wiring:** the leads go down through a slot in the deck plate to the battery.
- **Confidence:** medium. The red plug is seen in aws72; its purpose is a guess.

### 12.7 Wiring path

- **Battery and switch:** battery (right pod) → link (top of right pod) → down through the rear bridge (behind the slot, under the drive motors) → left pod → both ESCs.
- **Drive motors:** drive ESC → leads back to each gearmotor's tabs, across the rear bridge.
- **Weapon motor:** weapon ESC → 3 phase leads up through the left plate window → motor base.
- **Wire sizes:** 20-22 AWG silicone for power, 26 AWG for the drive motors.
- **Confidence:** medium.

### 12.8 Weapon motor screws

- **What:** 2-4 M2 × 4-5 cap screws through the left plate into the motor base (9 mm PCD).
- **Seen:** 3 heads (2 silver, 1 black) in aws76 and 2 black in aws74.
- **Confidence:** high.

### 12.9 Weapon axle and bearings

- **What:**
  - An M4 bolt, about 30 long, from the motor bell side through the weapon plates and a spacer.
  - It passes through the right plate's bore, which is possibly fitted with an MR74/MR84 flanged bearing `[guess]`.
  - It is nutted outside with a nyloc nut and washer (seen).
- **Clamping:** the weapon plates are clamped between the bell and a spacer.
- **Confidence:** medium.

### 12.10 Hidden screws

- **Side plate to pod:** 2 per plate `[guess]`, either through tabs into the pod inner wall from inside the pod (under the deck plate), or vertical screws through a foot flange.
- **Nose block bolts:** M3 through-bolts with nyloc nuts.
- **Deck screws:** these go into heat-set inserts or 3-4 mm printed bosses in the pod corners.
- **Confidence:** low on the method, medium on the existence.

### 12.11 Internal ribs and bosses

- **Corner bosses:** 4 screw bosses per pod for the deck plate, 5-6 dia, full height.
- **Rib:** one transverse rib per pod at the side plate foot (y ≈ 0-30) to carry the plate load into the floor.
- **Boss:** a boss around any lock-pin bore.
- **Confidence:** low-medium.

### 12.12 Weapon lock

- **What:** a pin or bolt through a hole in a pod inner wall into a weapon window, used for transport.
- **Seen:** not seen; the small hole in the left pod wall in aws76 could be it.
- **Confidence:** low.

### 12.13 Floor

- **What:** a solid printed floor 1-1.5 thick with an opening under the slot; the slot is open at the bottom.
- **Confidence:** medium (aws74 shows light under the slot).

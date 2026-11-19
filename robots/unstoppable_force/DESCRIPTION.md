# Unstoppable Force: what the reference photos show

Photos: `reference/unstoppable_force.aws69.webp` (event AWS69), `aws71.webp`, `aws72.webp`. All three are taken from
front-right, above: the drum is on the left of each picture, the robot's right side wall is the near face, and the rear
runs off to the upper right. Model axes: front +y, right +x, up +z.

## Overall layout
- Two-wheel drum spinner (an antweight "drum"). From front to back: the drum between two side arms, then a low flat
  box body with a flat top plate. The wheels are near the back, inside the body.
- Plan view: roughly square, about as wide as it is long (about 95 mm wide, about 100 mm long including the drum). Left
  and right are mirror images. The front edge is straight and the drum sits across all of it. Both REAR corners have a
  large 45 degree chamfer (about 12-15 mm). The rear edge between the chamfers is straight. The front is NOT rounded.
- Side view: low, about 28-30 mm tall. Flat top, flat bottom, vertical side walls. The drum axle sits at about mid height
  and the drum reaches down nearly to the floor.

## Body (tub)
- Black, matte, 3D printed (PLA or nylon), with visible layer lines. It is an open-top tub: side walls, rear wall and floor.
- The side walls are full height and run outside the wheels, so the wheels sit in wells inside the body outline. The
  near wall in aws69 and aws72 runs past the near wheel without a break, then turns into the rear chamfer.
- Two small dark holes (screw or insert holes) are on the right side wall near the front, at mid height (aws69, aws71,
  aws72): these are the side screws that hold the arm to the body.
- The front of the body between the arms is set back. A dark rectangular pocket behind the drum (aws69) lets the drum
  sit partly inside the body outline.

## Top plate
- A separate flat black plate (about 1.5 mm, printed or carbon) covering the whole tub, the same colour as the tub and
  slightly glossier. Its edge shows as a thin separate layer on top of the walls (aws71, aws72).
- Its outline follows the body: straight front edge behind the drum, chamfered rear corners, and a rectangular notch at
  each wheel, so each wheel shows from above through an open slot just inside the side wall.
- Held by about 6 small black button or cross-head screws: one at each front corner (over the arm or front of the side
  wall), one at each wheel notch (front and rear of the notch), and one at each rear corner. They are flush and small
  (M2 class).
- In the centre there is a slide power switch (silver lever in a slot), slightly forward of the plate's middle. It sits
  on black or dark tape patches (aws69 has a taped area; aws71 and aws72 have two tape squares either side). A small
  square hole sits forward-left of the switch (aws71, aws72), probably for the receiver LED or bind button.

## Wheels
- Two wheels, one each side, inside the body outline, axles across the robot (along x). The axle is about 55-70 % of the
  way back from the front of the body, just in front of the rear chamfers.
- Diameter about 30-34 mm (nearly the full body height, the tyre top level with or just above the top plate). Width about
  10 mm.
- Tyres: black rubber in aws69. Salmon or orange-red foam or silicone in aws71 and aws72 (`#e07a6a`-ish), on dark hubs.
- Driven directly by small gearmotors (N10/N20) mounted inboard. Nothing shows outside the side walls.

## Drum (weapon)
- A horizontal drum across the front, spinning about the x axis, filling the gap between the arms (about 60-70 % of the
  robot's width). Diameter about 25-28 mm.
- aws69: a plain cylinder in silver tape (or aluminium), with copper and red windings showing at its left end: an
  in-drum outrunner (the motor's bell is inside the drum).
- aws71: a different weapon fitted: a bent silver aluminium "scoop" or beater bar, about the drum's width, with a large
  rounded-rectangle window in its middle and a solid bar (an axle or a bar with springs) across the window. It hangs
  forward and down to nearly floor level, like a small plow, on the same axle.
- aws72: the drum again, wrapped in pink and silver tape, with two impact bars or teeth along it.
- Lowest point of the drum is about 1-3 mm above the floor. The drum sticks out ahead of the arms slightly.

## Drum arms (side supports)
- Two black printed side plates, one each side of the drum, about 8-10 mm thick, flush with or just inside the body's
  side walls. Seen from the side they are lozenge shaped: rounded front end around the drum axle, running back into
  the body's front corners. They reach from near the floor to about the top plate.
- The near (right) arm carries the axle end: a steel flanged nyloc nut and washer over a bearing on the outer face
  (aws71, aws72). So there is a steel through-axle or dead shaft, bolted at both arms.
- The arms are held to the body by side screws through the side wall (the two dark holes) and by the top plate's front
  corner screws.

## Colours
- Body, top plate and arms: black `#22262a`.
- Drum: silver aluminium `#b9b9b4` (it was taped pink and silver at aws72).
- Tyres: salmon red `#e07a6a` (aws71/72) or black (aws69).
- Hardware: silver nyloc nut and washer on the arm, black screws on the plate, silver switch lever.

## Relative sizes (body width = 1.0)
- Body width 1.0 (about 94 mm). Body length without the drum is about 0.7, and about 1.05 with the drum.
- Height 0.3. Drum diameter 0.28, drum length 0.7. Wheel diameter 0.33, wheel width 0.1. Arm thickness 0.09, arm
  length 0.45. Rear chamfer legs 0.13.

## Likely mechanism
- An in-drum brushless outrunner. The stator is fixed to one arm and the drum is bonded to its bell. The other end of
  the drum runs on a bearing on a dead shaft, nutted on the outer face of the arm.
- Two N10/N20 gearmotors drive the wheels directly. Power: a 2S LiPo, a Malenki-style receiver with brushed ESCs, a
  brushless weapon ESC, and the slide switch through the top plate.
- Invertible-ish: the wheels are about the body height, so it can drive upside down.

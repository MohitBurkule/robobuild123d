# The Golden Nuggets: reference description

Photo: `reference/the_golden_nugget.aws67.webp`. It is the only photo. It is a studio cut-out on white, taken from the front right at about 30-35 deg elevation. Measured from the image axes, the camera is about 35 deg off the front axis (likeness azimuth about 55-60). In this photo the front face, with the two pods and the lid hinges, is the widest face. The right side, with three wheels, runs away to the upper right. The rear is not visible.

Frame used below: front +y, right +x, up +z. Wheel radius 12 mm is the scale, and it matches the model.

## Overall
- This is a low, flat six-wheel box (lifter class). It is wider than it looks, and its plan is close to square once the wheels are counted: about 83 mm over the wheels and about 100 mm long including the front pods.
- There are three colours. The body is matte sky blue (about #3a8fe0). The lid/lifter is saturated yellow (about #f2d21c). The tyres are black foam with yellow hubs.
- The silhouette is flat. The highest point is the yellow lid, about one lid thickness (4-5 mm) above the blue side rails. The rail tops are level with the wheel tops or slightly higher.

## Chassis (blue, one printed part)
- **Centre tub** (under the lid): a rectangular box that runs the full length. You see it only through the gap between the lid and the right rail, where it is dark inside with red/black wires. This means the lid is the real top in the centre: there is no blue skin over the electronics under the lid.
- **Side rails**: two long blue strips that form the top outer edges, between the lid and the wheels. Each is about 12-15 mm wide, roughly 0.4-0.5 of the lid width. Their tops are flat and level, below the lid top. Each rail has 2 visible screws: silver pan/button heads, about M2-M2.5. One sits near the front, just behind where the pod slope starts. The other sits near the rear end, about 1/4 of the rail length from the rear. That makes 4 screws on top in total. The screws hold the rails/top to the tub.
- **Lower side face** (right side, between the wheels): you can see a lighter blue band at axle height. A yellow spur gear train (about 12-14 teeth, 10-12 mm diameter) sits between the wheels, just inside the tyres. The geared drive links all 3 wheels per side to one motor (one motor per side, chain of gears). The gears sit outside the side wall, under the rail overhang.
- **Front pods** (left and right): the largest blue features. Each pod is a solid block at the front corner, as wide as the space from the lid edge out to the outer face of the wheels, so it covers the front wheel's front. It ends about 1 wheel radius ahead of the front tyre. Faces:
  - A large flat chamfer (about 55-60 deg from horizontal) runs from the rail top, at about the front-axle line, down to a low vertical lip about 3-5 mm tall at the ground.
  - The outer front corner is chamfered as well: a second, smaller triangular facet bevels the outside corner, so the pod tip reads as a faceted wedge.
  - The inner face is vertical and faces the centre channel.
- **Floor plate / front channel**: between the pods, a thin blue plate (about 3 mm) runs forward at ground level to the pod front line. The front of the robot is open above it, with no front wall. This channel holds the lid hinge.

## Lid / lifter (yellow, printed)
- A flat yellow plate about 38 mm wide, about 4-5 mm thick, covering the centre from the rear end to the front. Near the front it bends down at about 60-65 deg into a short sloped nose. The nose ends low in the channel, about halfway along the pods' length, above the floor plate.
- Hinge: two blue cylindrical knuckles (about 5-6 mm diameter, about 6 mm long) at the bottom corners of the yellow nose. Each has a small pin hole. They sit on the floor plate, one near each inner pod face. The yellow nose wraps round them (tabs between). The pivot axis is along x, low, at the front.
- Likely mechanism: the nose and the hinge are at the front. The lid is a single-piece flipper/lifter plate pushed from inside by a servo or geared motor. Because the hinge is at the low front edge, the rear lifts (or the lid acts as a self-righter). The lid width is about 0.45 of the body width. Its edges are crisp with no fillets.

## Wheels (6, outside the body)
- 3 per side at an even pitch of about 28-30 mm. The wheels nearly touch (small gaps). The front wheel is just behind the pod, and the rear wheel is at the rear end.
- Each wheel is a black foam tyre about 24 mm in diameter and about 8-9 mm wide on a yellow plastic hub. The hub is about 0.7 of the tyre diameter, with a deep dish and a silver centre screw/axle end.
- The wheels sit fully outside the side walls. Their outer faces are about flush with the pods' outer faces. They are held on stub axles from the side walls, gear-driven.

## Relative sizes (from the photo)
- Lid width is about 1.6x the wheel diameter. A pod is about 1x the wheel diameter wide and about 0.7x the wheel diameter tall.
- The body (rail) height is about the wheel diameter. The lid top is the rail top plus about 0.2x the wheel diameter.
- The pods stick out about 0.5-0.8x the wheel diameter ahead of the front tyres.

## Notes for the model
- The declared camera (front_right_iso, elevation 45, azimuth 30) disagrees with the photo. Both the measured image axes and the checker's own best camera (elevation 25, azimuth 60) put the camera about 55-60 deg off the side axis. REFERENCE.json is collector-owned and is not edited here.
- Things to model: the pods with a big top chamfer and an outer corner chamfer, the open front channel with a floor plate, the lid bending down to the front, black tyres with yellow hubs, and 4 rail screws. The gears and hinge knuckles are optional details.

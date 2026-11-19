# Refined for the Roboteers Pleasure: reference photo description

Photos: `aws73` (front-left, high angle, on a grey table), `aws74` (left side, low elevation, front on the left, cut out on white),
`aws76` (front-left iso, about 35 degrees up, cut out on white). Model axes: +y forward, +x right, z up.

## Overall layout
- 2WD antweight, about 110-115 mm long, about 90 mm wide over the wheels; the low body is about 25 mm tall to the top plate.
  A tall white arm rises from the middle and roughly doubles the overall height (the arm top is about 100 mm above the floor).
- From front to back: a red (aws73/74) or orange (aws76) printed **plough** wraps the front ~60 % of the robot. A black
  **chassis** with a slotted black **top plate** fills the rear ~55 %. A big white **spur gear** with the white **arm** sits on
  the centreline where the plough meets the top plate. Two black **wheels** sit outside the body at the rear corners.
- The body is left/right symmetric apart from the arm head (the weapon motor and disc hang off one side of the arm).

## Plough (red/orange, printed, the largest part)
- Wraps the front and both sides. The front face is wide and flat, about the full body width, and slopes up and back at
  about 45-55 degrees from a lip near the floor. Clear tape covers it (lighter streaks in aws73/aws76).
- Above the slope a short steeper band rises to a horizontal top edge. That top edge stands a few mm above the black top plate.
- Plan view: the front corners are cut off by angled facets (chamfers about 8-10 mm), then straight side walls run back
  to just ahead of the wheels (the plough ends about 2-3 mm in front of the tyre).
- Side walls are vertical in the upper part. A lower facet angles inward toward the floor (chamfered skirt, seen as the darker
  lower band in aws74/aws76).
- The top edge has a scalloped notch/cut-out in the middle where the gear sits (aws76), so the gear teeth pass through it.
- It is a shell, held to the black chassis (screws are not clearly visible on the plough itself, but it is screwed on).
- Size: the plough is about 75-80 % of the robot length in side view (aws74). The front lip is about 1-2 mm off the floor.

## Chassis + top plate (black, printed)
- A rectangular tub, slightly narrower than the plough. A flat black top plate sits on it with **4 countersunk/button screws
  at the corners** (silver heads visible in all three photos) plus extra screws along the side edges (aws73 shows ~6).
- The top plate has rows of parallel **slots** (3-4 slots each side of the centre, angled in aws73, running front-back), with
  blue/black internals visible through them.
- The rear of the top plate has a small raised ridge. aws76 shows a small orange **U-shaped fork/holder** sticking up at
  the rear centre (likely an arm rest or the switch/key holder). aws74 shows small red tabs at the rear (same holder in red).
- The sides of the tub in aws74 show rectangular lightening windows (4-5 slots) along the lower side.

## Wheels (black)
- 2 wheels, outside the body at the rear corners. Diameter about 22-26 mm, width about 10 mm. Ribbed rubber treads
  (aws76 chunky tread, aws74 fine knurl). The hub is black with 3 spokes (aws74) or a clear/grey dished hub (aws76).
- The wheel centre is about 8-12 mm in from the rear end. The wheels stick out slightly beyond the plough side line.
- They are driven directly by gearmotors inside the tub (no visible belts).

## Gear + arm drive (white)
- A large white spur gear, about 30-34 mm in diameter, ~16-18 teeth, ~10-12 mm thick, on the centreline (slightly left of
  centre in aws73). Its axle is about 12-15 mm above the floor, near the plough's back edge, about half the length from the front.
  The lower half of the gear sinks into the body through a slot in the top plate.
- Two short black **side plates/links** (bearing cheeks) hold the gear axle; aws76 shows a black lever with a screw at the
  axle, aws74 a black bracket with a hex screw. The gear and arm pivot about the x axis.
- The arm is printed as one with the gear (white, the same material) and rises from the gear hub. Likely mechanism: a
  servo or geared motor inside drives a pinion on the gear to swing the arm (a hammer/axe or a saw that is raised and
  dropped). The arm pose differs between photos: nearly vertical with a slight rearward bow in aws74, leaning well forward (~30-40 deg) in aws76.

## Arm (white)
- A flat, slightly curved bar about 8-10 mm thick (x) and 8-12 mm wide (y), about 80-90 mm long.
- aws74/aws73: the arm widens near the top into a fin/blade that sweeps rearward (white "ear" behind the head). A black
  heat-shrink **sleeve** (about 12 mm long) wraps the arm at mid height, holding the 3 motor leads that run up the arm.
- aws76: a plain curved arm that leans forward and ends in a steel **axe/pick blade** (hooked, pointing forward-down),
  held by 2 screws.

## Weapon head
- aws73/aws74: a small outrunner brushless motor (TC-type, about 18 mm dia, black/silver) bolted to the side of the arm top.
  A **6-tooth saw disc** (about 25-30 mm dia, black with green edge in aws74, steel in aws73) sits on its bell, axis along x
  (spins in the robot's y-z plane). Wires run down the arm under the black sleeve.
- aws76: the motor and disc are replaced by the axe blade (alternative weapon fit).

## Relative sizes (approx)
- Gear diameter ≈ 1.3 x wheel diameter. Arm length ≈ body length x 0.75. Disc diameter ≈ wheel diameter.
- Plough height at the front ≈ wheel diameter. Top plate ≈ 55 % of the length, 85 % of the width.

## Modelling notes (what drives the fixes)
- One pose has to serve both photos: aws74 (arm upright, saw) and aws76 (arm forward, axe). REFERENCE.json requires a 6-tooth x-axis disc, so model the saw head.
- The plough is a thin shell: front slope, chamfered corners, side wings to just ahead of the wheels, notch at the gear.
- The wheels are outside the body at the rear and must not stick up above the plough's top line.

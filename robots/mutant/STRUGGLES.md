# mutant: struggles

Mutant is a shuffling walker: no wheels. It moves on cam-driven feet under each side skirt.

## What the model has
- `locomotion: "walker"` (225 g class limit), two side pods + bridge, four `leg_cam_*` parts (two per side) as the feet, hidden by the skirts as in the photos.
- The cams are placed and sized from the photos; they are not yet a working linkage.

## What the toolchain lacks for walkers
1. No leg/crank part. `kit.json legs` gives static feet; there is no crank + follower (or cam + sliding foot) shape with a joint pair, so the drive cannot be modelled as a mechanism. Wanted: a kit part `shuffler_cam {n, throw_mm, phase_deg, foot_w, shaft_d}` that emits the camshaft (one revolute joint), N eccentric cams at stated phases and N feet on prismatic/rocker joints coupled to the shaft.
2. No coupled joints. A joint cannot be declared as driven by another joint (gear, cam, crank ratio), so the sweep check treats each cam alone and the feet as fixed.
3. Ground checks assume wheels: `ground.wheel_floating` and the stance test look for `kind: wheel` contact patches. A walker needs "at least 3 feet (or 2 feet + skid) on the floor at every crank angle".
4. Drive checks assume wheels: speed, torque and pushing force are computed from wheel radius. A shuffler needs speed = throw x rpm x duty and traction from the feet in contact.
5. The fight sim has no walker gait, so the robot is simulated as a sliding box.
6. `legal` knows the 225 g walker allowance only by the `locomotion` tag; nothing checks that the model really has no rolling contact (a camshaft that touches the floor would be a wheel).

Time lost: about 25 minutes over the rounds, mostly finding out that feet could only be static parts.

## Round 4: walker drive as modelled
- Per side: one N20 gearmotor (`drive_l`, `drive_r`, catalog `bbb_n20_600rpm`) drives a 3 mm steel camshaft (`cam_shaft_l/r`) across the pod; the two eccentric cams of that side (`leg_cam_*0`, `leg_cam_*1`) are revolute about the camshaft axis and sit 180 degrees out of phase (2 mm and 3.6 mm throw), so one foot is always on the floor and the robot shuffles forward by the throw each turn.
- Still not expressible: the cams are four independent joints (no coupling to the shaft or to each other), the feet are the cam rims themselves (no separate follower foot), and no check knows the gait. See the list above.

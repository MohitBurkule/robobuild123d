# rbmk: struggles

RBMK has NO wheels and NO legs. It moves only by the gyroscopic effect and vibration of its TWO spinning weapons: changing the two spinner speeds makes the body precess and skate on its skids.

## What the model has
- Body, two spinners (`weapon`, `bar2`) with their motors, two skids. No wheel parts, no leg parts. `locomotion` is tagged "walker" only because the profile offers no other non-wheeled value.

## What the toolchain lacks: a "gyro-vibration locomotion" mode
1. `locomotion` values are roller / walker (shuffler). Needed: `gyro` (or `vibration`): movement from weapon reaction, no drive train.
2. Checks that assume wheels and fail or mislead here: `ground.wheel_floating` / stance (looks for wheel contact), drive speed / torque / pushing force (need wheel radius and drive motors), `power` drive current budget, `drive_recess`, `retention.axial` for wheels, `legal` mobility demonstration (controlled movement), the "2 drive motors" assumption in the electronics check, and the kit itself (`wheels.n: 0` works, but motors and the receiver mix are still laid out for a 2-wheel drive).
3. Fight sim: no model where translation comes from spinner speed difference and floor friction on skids; the robot is simulated as a static box with weapons.
4. Wanted check instead: with both spinners at speed, net yaw torque from the speed difference must exceed skid friction torque; and the robot must still be controllable when one weapon stalls.
5. Two weapons: the kit takes one `weapon`; the second is a hand-added part. Wanted: `weapons: [...]`.

# gyronino: struggles

Gyronino is a gyro-walker: one big vertical ring spinner on a tilted frame; precession of the spinner rocks the robot from foot to foot. No wheels.

## What the model has
- `locomotion: "walker"`, body + ring spinner + the two blade feet and the tail, placed from the photos.

## What the toolchain lacks
1. No gyro-walk locomotion: speed and steering come from spinner angular momentum x tilt rate, not from wheels. The drive, dynamics and fight checks have no model for it and score the robot as immobile.
2. Ground checks want wheel contact patches; here the contact is two feet + tail, lifting in turn.
3. No coupled "tilt servo" joint that is checked against the spinner (the servo that tips the frame is what makes it walk).
4. The likeness templates are all wheeled, so "no worse than the closest template" compares against an irrelevant shape.
See also mutant/STRUGGLES.md for the general walker gaps (leg parts, coupled joints, walker gait in the sim).

# Camera audit

Camera labels in REFERENCE.json corrected from the photo itself (which face is nearest, which side the front is on, how much top is visible), not from which camera scores best. Azimuth convention (robot/checks/likeness.py): 0 = robot right, 90 = front, 180 = left; a front-right camera puts the front on the image right.

| robot | photo | before | after | visual reasoning |
|---|---|---|---|---|
| stack_overflow | stack_overflow.aws67.webp | front, el 25 | front, el 45 | Head-on front view is right, but the camera looks well down into the open chassis (deck, wiring and the tops of both tyres visible above the wedge). At 25 deg the wedge plate would hide the interior. High view, about 45. |

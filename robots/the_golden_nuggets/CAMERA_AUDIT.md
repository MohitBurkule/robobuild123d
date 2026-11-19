# Camera audit

Camera labels in REFERENCE.json corrected from the photo itself (which face is nearest, which side the front is on, how much top is visible), not from which camera scores best. Azimuth convention (robot/checks/likeness.py): 0 = robot right, 90 = front, 180 = left; a front-right camera puts the front on the image right.

| robot | photo | before | after | visual reasoning |
|---|---|---|---|---|
| the_golden_nuggets | the_golden_nugget.aws67.webp | front_right_iso, el 45 | front_left_iso, el 45 (az about 115-120) | Lifter front (yellow plate, blue hinges) is at the image lower LEFT and nearest the camera; the 6-wheel side runs off to the image right. Front-on-left = camera at front-left (cf. likeness grid az 120 render). Top plate strongly visible, so elevation 45 kept. |

# Camera audit

Camera labels in REFERENCE.json corrected from the photo itself (which face is nearest, which side the front is on, how much top is visible), not from which camera scores best. Azimuth convention (robot/checks/likeness.py): 0 = robot right, 90 = front, 180 = left; a front-right camera puts the front on the image right.

| robot | photo | before | after | visual reasoning |
|---|---|---|---|---|
| valkyrie | valkyrie.aws71.webp | left, el 25 | front_right_iso, el 45 (az about 60, el about 35-40) | Drum (front, blue end bearings) runs along the image lower RIGHT, the lettered side wall along the lower left, lid top widely visible. Front-on-right = camera at front-right (matches the az 60 grid render, front arrow lower right). A pure left view would hide the drum face. NOTE: the lettered wall is therefore the robot's RIGHT wall, not left as DESCRIPTION.md assumes. |
| valkyrie | valkyrie.aws74.webp | front_left_iso, el 45 | front_right_iso, el 45 | Same quadrant as aws71: drum along the image right, lettered wall facing the camera at lower left. The front_left_iso render puts the drum at the image lower left, the opposite of the photo. |

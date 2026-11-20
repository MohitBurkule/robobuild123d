# Camera audit

Camera labels in REFERENCE.json corrected from the photo itself (which face is nearest, which side the front is on, how much top is visible), not from which camera scores best. Azimuth convention (robot/checks/likeness.py): 0 = robot right, 90 = front, 180 = left; a front-right camera puts the front on the image right.

| robot | photo | before | after | visual reasoning |
|---|---|---|---|---|
| mutant | mutant.aws74.webp | rear_right_iso, el 45 | front_left_iso, el 45 (az about 120) | The front (twin wedgelet flaps, disc tip between the halves) is at the image lower LEFT, nearest the camera; the right-hand side panel recedes to the image right. Front visible and near = a front camera, front on the left = front-left. Not a rear view. |
| mutant | mutant.aws76.webp | front, el 25 | front_left_iso, el 25 (az about 115-120) | Flaps/front face at lower left; a long side panel (white) is clearly visible receding to the right, so not a straight front view. Low camera (top barely visible), el 25 kept. |

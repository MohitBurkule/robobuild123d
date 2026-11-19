# Camera audit

Camera labels in REFERENCE.json corrected from the photo itself (which face is nearest, which side the front is on, how much top is visible), not from which camera scores best. Azimuth convention (robot/checks/likeness.py): 0 = robot right, 90 = front, 180 = left; a front-right camera puts the front on the image right.

| robot | photo | before | after | visual reasoning |
|---|---|---|---|---|
| bzwroink | bzwroink.aws68.webp | front_left_iso, el 45 | rear_right_iso, el 45 | The clear scoop (front) is at the image upper RIGHT and FARTHEST from the camera; the near deep-pink wheels at lower left are the rear wheels of the side facing the camera. Front far and on the right = camera behind on the robot's right (grid az 300 render: front arrow points up-right). Low-res two-robot photo, so the least certain fix here; the caller's note suggested rear-left, but rear-left would put the front at the upper LEFT. |

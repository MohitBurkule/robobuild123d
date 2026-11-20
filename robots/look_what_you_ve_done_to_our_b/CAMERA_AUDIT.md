# Camera audit

Camera labels in REFERENCE.json corrected from the photo itself (which face is nearest, which side the front is on, how much top is visible), not from which camera scores best. Azimuth convention (robot/checks/likeness.py): 0 = robot right, 90 = front, 180 = left; a front-right camera puts the front on the image right.

| robot | photo | before | after | visual reasoning |
|---|---|---|---|---|
| look_what_you_ve_done_to_our_b | look_what_you_ve_done_to_our_breakfast.aws74.webp | front_left_iso, el 25 | front_left_iso, el 45 | View is right (wedge at lower left, wheels on the right). But the top plate fills most of the image and the screws on it are seen nearly face-on; a 25 deg camera would compress the top to a thin band. High view, about 45. |

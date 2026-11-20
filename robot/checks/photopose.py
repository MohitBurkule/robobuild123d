"""Photo-pose warnings (`photopose.*`): how well the CAD can be posed against each reference photo. WARNINGS only.

Active when `<robot>/pose/*.pose.json` exists (made by `robot pose-photo`; `robot part-pose` adds part_pose.json).
- photopose.fit          best camera fit for a photo has silhouette IoU < 0.85 or depth correlation < 0.6: the model's
                         shape or proportions differ from the photo (the camera, not the likeness score, was solved).
- photopose.depth_calib  part_pose.json metric depth calibration r < 0.6: part 3D poses from that photo are unreliable.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..finding import WARNING, fail, ok

G = "photopose"
IOU_MIN, CORR_MIN, CALIB_MIN = 0.85, 0.6, 0.6


def folder_key(spec) -> str:
    import hashlib
    h = hashlib.sha256()
    b = Path(getattr(spec, "base_dir", ".") or ".")
    for p in sorted(b.glob("pose/*.pose.json")) + sorted(b.glob("reference/segments/*/part_pose.json")):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def run(ctx):
    b = Path(getattr(ctx.r.spec, "base_dir", ".") or ".")
    poses = sorted(b.glob("pose/*.pose.json"))
    if not poses:
        return []
    out = []
    for pj in poses:
        d = json.loads(pj.read_text())
        sc = d["scores"]
        if sc["iou"] < IOU_MIN or sc["depth_corr"] < CORR_MIN:
            out.append(fail("photopose.fit", G, WARNING, "Model does not fit the photo under any camera",
                            f"{d['photo']}: best camera az {d['camera']['azimuth']} el {d['camera']['elevation']} gives mask IoU "
                            f"{sc['iou']} (min {IOU_MIN}), depth corr {sc['depth_corr']} (min {CORR_MIN}); declared view "
                            f"{d.get('declared_view')}").fix("Compare pose/<photo>.overlay.png: fix body proportions / wedge / weapon "
                                                             "size the overlay shows as off."))
        else:
            out.append(ok("photopose.fit", G, "Model fits the photo", f"{d['photo']}: IoU {sc['iou']}, depth corr {sc['depth_corr']}"))
    for pp in sorted(b.glob("reference/segments/*/part_pose.json")):
        r = json.loads(pp.read_text())["calibration"]["r"]
        if r < CALIB_MIN:
            out.append(fail("photopose.depth_calib", G, WARNING, "Part depth calibration weak",
                            f"{pp.parent.name}: photo depth vs model depth r={r} (min {CALIB_MIN}); part 3D poses unreliable"))
    return out

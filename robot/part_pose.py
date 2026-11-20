"""`robot part-pose SPEC SEGDIR`: depth + 3D pose of every segmented part (from `robot partseg export`), in the robot frame.

Inputs: `<robot>/pose/<photo>.pose.json` + `.depth.png` (from `robot pose-photo`) and a partseg export dir
(`segments/<stem>/index.json` + masks). Evidence only: photo depth + the fitted camera. The relative monocular depth
is made metric by a 2-parameter fit of 1/z to the model's own depth over the robot silhouette (scale + shift), then
each part's pixels are back-projected through the fitted pinhole camera into the robot frame (mm, x right, y front,
z up, origin = model bbox centre).

Writes `<segdir>/part_pose.json`:  per part {median_z_mm, centroid_robot_mm, centroid_cam_mm, normal_robot (plane fit,
unit, towards camera), extent_mm (PCA sizes), height_range_mm, offset_from_body_mm, n_px} plus `pairs` (centroid offsets
between every two parts) and `calibration` {a, b, r, n} (r = depth fit correlation, low = untrustworthy).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from . import pose_photo as pp


def _canvas_params(cam, W, H):
    s = pp.WORK / max(W, H)
    K = cam["intrinsics_px"]
    return np.array([cam["azimuth"], cam["elevation"], cam["roll"], cam["distance_mm"], K["fx"] * s, K["cx"] * s, K["cy"] * s]), s


def run(spec_path, segdir, pose_json=None, log=print):
    from PIL import Image
    segdir = Path(segdir)
    idx = json.loads((segdir / "index.json").read_text())
    base = Path(spec_path).parent
    photo = idx["photo"]
    stem = Path(photo).stem
    pj = Path(pose_json or base / "pose" / f"{stem}.pose.json")
    pose = json.loads(pj.read_text())
    cam = pose["camera"]
    K = cam["intrinsics_px"]
    W0, H0 = K["width"], K["height"]
    depth = np.asarray(Image.open(pj.with_name(f"{stem}.depth.png")), np.float32) / 65535
    T, _ = pp.model_triangles(spec_path)
    p, s = _canvas_params(cam, W0, H0)
    cw, ch = int(round(W0 * s)), int(round(H0 * s))
    m, inv = pp.render(T, p, (ch, cw))
    d_c = np.asarray(Image.fromarray(depth, mode="F").resize((cw, ch), Image.BILINEAR))
    # metric calibration: model inverse depth (1/mm) ~ a * relative disparity + b over the model silhouette
    pos, right, up, dd = pp.basis(*p[:4])
    sel = m
    A = np.stack([d_c[sel], np.ones(sel.sum())], 1)
    (a, b), *_ = np.linalg.lstsq(A, inv[sel], rcond=None)
    r = float(np.corrcoef(d_c[sel], inv[sel])[0, 1]) if sel.sum() > 10 else 0.0
    # camera: robot_in_camera 4x4 (rows: x right, y down, z forward)
    M = np.array(cam["robot_in_camera_4x4"])
    Rm, t = M[:3, :3], M[:3, 3]
    x0, y0, x1, y1 = idx.get("crop") or (0, 0, 1, 1)
    mw, mh = idx["size"]
    res = {}
    allpts = []
    for row in idx["parts"]:
        mk = np.asarray(Image.open(segdir / row["mask"])) > 0
        ys, xs = np.nonzero(mk)
        if len(xs) < 20:
            continue
        u = (x0 + (xs + 0.5) / mw * (x1 - x0)) * W0
        v = (y0 + (ys + 0.5) / mh * (y1 - y0)) * H0
        dv = depth[np.clip(v.astype(int), 0, H0 - 1), np.clip(u.astype(int), 0, W0 - 1)]
        invz = np.maximum(a * dv + b, 1e-6)  # 1/mm in the canvas metric (scale-free of canvas: z is mm)
        z = 1.0 / invz
        Xc = np.stack([(u - K["cx"]) / K["fx"] * z, (v - K["cy"]) / K["fy"] * z, z], 1)
        Xr = (Xc - t) @ Rm  # robot frame (Rm orthonormal)
        allpts.append(Xr)
        c = Xr.mean(0)
        w, V = np.linalg.eigh(np.cov((Xr - c).T)) if len(Xr) > 5 else (np.ones(3), np.eye(3))
        n = V[:, 0]
        if n @ (np.array(cam["camera_position_mm"]) - c) < 0:
            n = -n
        res[row["slug"]] = {"label": row.get("label"), "n_px": int(len(xs)), "median_z_mm": round(float(np.median(z)), 1),
                            "centroid_robot_mm": [round(float(x), 1) for x in c],
                            "centroid_cam_mm": [round(float(x), 1) for x in Xc.mean(0)],
                            "normal_robot": [round(float(x), 3) for x in n],
                            "extent_mm": [round(float(2 * np.sqrt(max(x, 0))), 1) for x in w[::-1]],
                            "height_range_mm": [round(float(np.percentile(Xr[:, 2], 5)), 1),
                                                round(float(np.percentile(Xr[:, 2], 95)), 1)]}
    body = np.concatenate(allpts).mean(0) if allpts else np.zeros(3)
    for k, e in res.items():
        e["offset_from_body_mm"] = [round(float(x), 1) for x in np.array(e["centroid_robot_mm"]) - body]
    names = list(res)
    pairs = {f"{i}->{j}": [round(float(x), 1) for x in np.array(res[j]["centroid_robot_mm"]) - res[i]["centroid_robot_mm"]]
             for ii, i in enumerate(names) for j in names[ii + 1:]}
    out = {"photo": photo, "camera_from": pj.name, "calibration": {"a": float(a), "b": float(b), "r": round(r, 3), "n": int(sel.sum())},
           "body_centroid_robot_mm": [round(float(x), 1) for x in body], "parts": res, "pairs": pairs,
           "note": "metric depth = fit of photo disparity to the model's depth; trust only when pose.json confidence/iou are good and calibration.r is high"}
    (segdir / "part_pose.json").write_text(json.dumps(out, indent=1))
    log(f"{photo}: {len(res)} parts, depth fit r={r:.2f}")
    return out


def add_cli(sub):
    p = sub.add_parser("part-pose", help="depth + 3D pose of each segmented part in the robot frame (needs pose-photo + partseg export)")
    p.add_argument("spec")
    p.add_argument("segdir", nargs="?", help="segments/<stem> folder with index.json (default: every export that has a pose.json)")
    p.set_defaults(func=lambda a: print(run_all(a.spec)) or 0 if not a.segdir else
                   print(json.dumps({k: v for k, v in run(a.spec, a.segdir).items() if k != "pairs"})) or 0)


def run_all(spec_path, log=print):
    """part-pose for every segments/<stem> export that has a matching pose.json (writes part_pose.json in each)."""
    base = Path(spec_path).parent
    n = 0
    for idxf in sorted((base / "reference" / "segments").glob("*/index.json")):
        stem = Path(json.loads(idxf.read_text())["photo"]).stem
        if (base / "pose" / f"{stem}.pose.json").exists():
            try:
                run(spec_path, idxf.parent, log=log)
                n += 1
            except Exception as ex:  # noqa: BLE001
                log(f"{idxf.parent.name}: failed {ex}")
    return n


def quality(spec_path):
    """One line per photo: poor = iou < 0.85 or depth corr < 0.6 (builders should look at the shape/proportions)."""
    base = Path(spec_path).parent
    rows = []
    for pj in sorted((base / "pose").glob("*.pose.json")):
        d = json.loads(pj.read_text())
        sc = d["scores"]
        rows.append((base.name, d["photo"], sc["iou"], sc["depth_corr"], d["confidence"], d.get("declared_view"),
                     d["camera"]["view_string"], sc["iou"] < 0.85 or sc["depth_corr"] < 0.6))
    return rows

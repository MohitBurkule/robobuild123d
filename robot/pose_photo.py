"""`robot pose-photo SPEC [--photo NAME]`: monocular depth + camera/robot pose from each reference photo.

Evidence used (and nothing else): the photo, its own silhouette mask (`reference/<photo>_mask.png`) and a monocular
depth map (Depth Anything V2 small, ONNX, CPU). The CAD model is rendered through a pinhole camera; the search moves
the camera (az, el, roll, distance, focal length, principal point) to maximise silhouette IoU with the mask plus
agreement of the model's inverse depth with the monocular depth over the overlap. The likeness score is never an input
and the declared REFERENCE.json `view` is only reported, never used to initialise the search (so it is an independent
check of that label).

Writes next to the spec:  pose/<photo>.pose.json  (intrinsics, extrinsics, robot-in-camera 4x4, scores, runner-up
cameras), pose/<photo>.depth.png (16-bit relative inverse depth, 1 = near) and pose/<photo>.overlay.png.
Frame: robot x = right, y = front, z = up, mm, origin at the model's bbox centre. Camera az 0 = robot's right (+x),
90 = front (+y); el = degrees above the floor plane. The robot is assumed to sit flat (no tilt of its own): tilt is
indistinguishable from camera roll/elevation from one photo. Articulated parts (raised flipper) are as the spec has them.
"""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

import numpy as np

MODEL_URL = "https://huggingface.co/onnx-community/depth-anything-v2-small/resolve/main/onnx/model.onnx"
MODEL_PATH = Path(os.environ.get("ROBOT_DEPTH_MODEL") or Path.home() / ".cache" / "robot" / "da2_small.onnx")
WORK = 200  # long side of the fitting canvas, px
W_DEPTH = 0.35  # weight of the depth term against 1 - IoU
FOV_MIN, FOV_MAX = 15.0, 100.0  # horizontal... of the long image side, degrees: soft prior on plausible lenses


# ---------------------------------------------------------------- depth
def _session():
    import onnxruntime as ort
    if not MODEL_PATH.exists():
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = MODEL_PATH.with_suffix(".part")
        urllib.request.urlretrieve(MODEL_URL, tmp)
        tmp.rename(MODEL_PATH)
    so = ort.SessionOptions()
    so.intra_op_num_threads = int(os.environ.get("ROBOT_POSE_THREADS", "2"))  # leave CPUs to other jobs
    return ort.InferenceSession(str(MODEL_PATH), so, providers=["CPUExecutionProvider"])


def depth_map(img, size=518):
    """Relative inverse depth (H, W) float32 in 0..1 at the photo's resolution (1 = nearest)."""
    from PIL import Image
    im = img.convert("RGB")
    w, h = im.size
    s = size / max(w, h)
    nw, nh = max(14, int(round(w * s / 14)) * 14), max(14, int(round(h * s / 14)) * 14)
    a = np.asarray(im.resize((nw, nh), Image.BICUBIC), np.float32) / 255
    a = (a - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    out = _session().run(None, {"pixel_values": a.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    d = np.asarray(Image.fromarray(out.astype(np.float32), mode="F").resize((w, h), Image.BILINEAR))
    lo, hi = np.percentile(d, [1, 99])
    return np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1).astype(np.float32)


# ---------------------------------------------------------------- model + camera
def model_triangles(spec_path, max_tris=7000):
    from . import spec as spec_mod, world as world_mod
    s = spec_mod.load(spec_path)
    r = world_mod.resolve(s, fast=True)
    w = world_mod.World.build(r)
    T = np.concatenate([b.mesh.triangles for b in w.bodies
                        if b.mesh is not None and not getattr(b, "is_wire", False)]).astype(float)
    if len(T) > max_tris:  # keep the big faces: small ones barely move a 200 px silhouette
        a = np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1)
        T = T[np.argsort(-a)[:max_tris]]
    c = (T.reshape(-1, 3).min(0) + T.reshape(-1, 3).max(0)) / 2
    return T - c, c


def basis(az, el, roll, D):
    a, e = np.radians(az), np.radians(el)
    pos = D * np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    d = -pos / D
    right = np.cross(d, [0, 0, 1.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, d)
    r = np.radians(roll)
    right, up = right * np.cos(r) + up * np.sin(r), up * np.cos(r) - right * np.sin(r)
    return pos, right, up, d


def project(T, p, shape):
    """p = (az, el, roll, D, f, cx, cy); returns (u, v, z) per triangle vertex, (n, 3) each."""
    pos, right, up, d = basis(*p[:4])
    q = T - pos
    z = q @ d
    z = np.maximum(z, 1e-3)
    return p[5] + p[4] * (q @ right) / z, p[6] - p[4] * (q @ up) / z, z


def render(T, p, shape):
    """(mask bool, inverse depth float) on the canvas by painter's algorithm."""
    from PIL import Image, ImageDraw
    H, W = shape
    u, v, z = project(T, p, shape)
    order = np.argsort(-z.mean(1))  # far first
    zm = Image.new("F", (W, H), 0.0)
    dr = ImageDraw.Draw(zm)
    inv = 1.0 / z.mean(1)
    for i in order:
        dr.polygon([(u[i, 0], v[i, 0]), (u[i, 1], v[i, 1]), (u[i, 2], v[i, 2])], fill=float(inv[i]))
    inv_img = np.asarray(zm)
    return inv_img > 0, inv_img


def _blur(m, s=2.0):
    from scipy import ndimage as nd
    return nd.gaussian_filter(m.astype(np.float32), s)


def score(T, p, mask, bmask, depth, use_depth=True):
    """loss = 1 - softIoU (+ W_DEPTH * (1 - depth corr)) + lens prior. Lower is better."""
    m, inv = render(T, p, mask.shape)
    a, b = _blur(m), bmask
    iou = float(np.minimum(a, b).sum() / max(np.maximum(a, b).sum(), 1e-6))
    corr = 0.0
    both = m & mask
    if use_depth and both.sum() > 80:
        x, y = inv[both], depth[both]
        if x.std() > 1e-9 and y.std() > 1e-9:
            corr = float(np.corrcoef(x, y)[0, 1])
    fov = np.degrees(2 * np.arctan(max(mask.shape) / 2 / max(p[4], 1e-3)))
    pen = 0.002 * (max(0, FOV_MIN - fov) + max(0, fov - FOV_MAX))
    pen += 0.05 * max(0.0, abs(p[2]) - 20) / 20  # photos are rarely rolled much
    loss = (1 - iou) + (W_DEPTH * (1 - corr) if use_depth else 0.0) + pen
    return loss, iou, corr


def init_params(T, az, el, mask, D=None):
    """Pinhole at distance D looking at the origin, f / principal point set so the model bbox matches the mask bbox."""
    R = np.linalg.norm(T.reshape(-1, 3), axis=1).max()
    D = D or 4.0 * R
    p = np.array([az, el, 0.0, D, 1.0, 0.0, 0.0])
    u, v, _ = project(T, p, mask.shape)
    ys, xs = np.nonzero(mask)
    sx = (xs.max() - xs.min() + 1) / max(u.max() - u.min(), 1e-6)
    sy = (ys.max() - ys.min() + 1) / max(v.max() - v.min(), 1e-6)
    f = min(sx, sy)
    p[4] = f
    u, v, _ = project(T, p, mask.shape)
    p[5] = (xs.min() + xs.max()) / 2 - (u.min() + u.max()) / 2
    p[6] = (ys.min() + ys.max()) / 2 - (v.min() + v.max()) / 2
    return p


def fit(T, mask, depth, top=5, progress=None):
    """Global grid over (az, el) -> refine the best `top` with Nelder-Mead on all 7 parameters."""
    from scipy.optimize import minimize
    bmask = _blur(mask)
    cands = []
    for el in (10, 25, 40, 55, 70, 85):
        for az in range(0, 360, 20):
            p = init_params(T, az, el, mask)
            cands.append((score(T, p, mask, bmask, depth, use_depth=False)[0], p))
    cands.sort(key=lambda c: c[0])
    # keep distinct (az, el) starts
    starts = []
    for _, p in cands:
        if all(abs(((p[0] - q[0] + 180) % 360) - 180) > 30 or abs(p[1] - q[1]) > 20 for q in starts):
            starts.append(p)
        if len(starts) == top:
            break
    res = []
    scale = np.array([8.0, 6.0, 4.0, 0.3, 0.1, 0.03, 0.03])  # relative step per parameter

    def f_(x, p0):
        p = p0 * 1.0
        p[:4] = x[:4] * np.array([1, 1, 1, 1])
        p[4] = p0[4] * np.exp(x[4])
        p[5:] = p0[5:] + x[5:] * max(mask.shape)
        return score(T, p, mask, bmask, depth)[0]

    for p0 in starts:
        x0 = np.array([p0[0], p0[1], 0.0, p0[3], 0.0, 0.0, 0.0])
        sim = [x0]
        for i, sc in enumerate(np.array([10.0, 8.0, 5.0, 0.5 * p0[3], 0.15, 0.04, 0.04])):
            x = x0.copy()
            x[i] += sc
            sim.append(x)
        r = minimize(f_, x0, args=(p0,), method="Nelder-Mead",
                     options={"maxiter": 260, "xatol": 0.05, "fatol": 1e-4, "initial_simplex": np.array(sim)})
        p = p0 * 1.0
        x = r.x
        p[:4] = x[:4]
        p[4] = p0[4] * np.exp(x[4])
        p[5:] = p0[5:] + x[5:] * max(mask.shape)
        p[0] %= 360
        loss, iou, corr = score(T, p, mask, bmask, depth)
        res.append({"loss": loss, "iou": iou, "depth_corr": corr, "p": p})
        if progress:
            progress(len(res), len(starts), res[-1])
    res.sort(key=lambda r: r["loss"])
    return res


# ---------------------------------------------------------------- output
def _cam_json(p, scale, size, offset=(0, 0)):
    """p on the canvas -> JSON dict in photo pixels (scale = photo px per canvas px)."""
    pos, right, up, d = basis(*p[:4])
    Rcr = np.stack([right, -up, d])  # rows: camera x (right), y (down), z (forward) in robot axes
    t = -Rcr @ pos
    M = np.eye(4)
    M[:3, :3], M[:3, 3] = Rcr, t
    f = float(p[4] * scale)
    cx, cy = float((p[5]) * scale + offset[0]), float((p[6]) * scale + offset[1])
    W, H = size
    return {"azimuth": round(float(p[0] % 360), 2), "elevation": round(float(p[1]), 2), "roll": round(float(p[2]), 2),
            "distance_mm": round(float(p[3]), 1),
            "intrinsics_px": {"fx": round(f, 1), "fy": round(f, 1), "cx": round(cx, 1), "cy": round(cy, 1),
                              "width": W, "height": H,
                              "fov_deg_long_side": round(float(np.degrees(2 * np.arctan(max(W, H) / 2 / f))), 1)},
            "camera_position_mm": [round(float(x), 1) for x in pos],
            "robot_in_camera_4x4": [[round(float(x), 5) for x in row] for row in M],
            "view_string": f"{int(round(p[0] % 360))},{int(round(p[1]))}!"}


def overlay(photo, T, p, canvas_shape, mask):
    """Side by side: photo with model outline (cyan) + photo mask outline (yellow) | shaded CAD from the fitted camera."""
    from PIL import Image, ImageDraw
    ch, cw = canvas_shape
    S = 3  # supersample the render for a readable picture
    big = (ch * S, cw * S)
    q = p * 1.0
    q[4:] *= S
    pos, right, up, d = basis(*p[:4])
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    n = np.where((n @ d)[:, None] > 0, -n, n)  # face the camera
    shade = 0.25 + 0.75 * np.clip(n @ (-d * 0.6 + up * 0.5 + right * -0.3), 0, 1)
    u, v, z = project(T, q, big)
    img = Image.new("RGB", (cw * S, ch * S), (235, 235, 235))
    dr = ImageDraw.Draw(img)
    for i in np.argsort(-z.mean(1)):
        g = int(255 * shade[i])
        dr.polygon([(u[i, 0], v[i, 0]), (u[i, 1], v[i, 1]), (u[i, 2], v[i, 2])], fill=(g // 3, g, g // 2))
    m, _ = render(T, p, canvas_shape)
    ph = np.asarray(photo.convert("RGB").resize((cw, ch)), np.uint8).copy()
    ph[m ^ (_blur(m, 1.0) > 0.6)] = (0, 255, 255)
    ph[mask ^ (_blur(mask, 1.0) > 0.6)] = (255, 255, 0)
    L = Image.fromarray(ph).resize((cw * 2, ch * 2), Image.NEAREST)
    R = img.resize((cw * 2, ch * 2), Image.LANCZOS)
    out = Image.new("RGB", (cw * 4 + 10, ch * 2), "white")
    out.paste(L, (0, 0))
    out.paste(R, (cw * 2 + 10, 0))
    return out


def run(spec_path, photo=None, out=None, top=5, log=print):
    from PIL import Image
    spec_path = Path(spec_path)
    base = spec_path.parent
    ref = json.loads((base / "REFERENCE.json").read_text()) if (base / "REFERENCE.json").exists() else {}
    photos = [photo] if photo else (ref.get("photos") or [p.name for p in sorted((base / "reference").glob("*"))
                                                           if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
                                                           and not p.stem.endswith("_mask")])
    out = Path(out or base / "pose")
    out.mkdir(parents=True, exist_ok=True)
    T, centre = model_triangles(spec_path)
    results = {}
    for name in photos:
        path = base / "reference" / name
        mpath = path.with_name(path.stem + "_mask.png")
        if not mpath.exists():
            log(f"{name}: no mask, skipped")
            continue
        im = Image.open(path)
        W, H = im.size
        mk = np.asarray(Image.open(mpath).convert("L").resize((W, H))) > 127
        d_full = depth_map(im)
        Image.fromarray((d_full * 65535).astype(np.uint16)).save(out / f"{path.stem}.depth.png")
        s = WORK / max(W, H)
        cw, ch = int(round(W * s)), int(round(H * s))
        mk_c = np.asarray(Image.fromarray(mk.astype(np.uint8) * 255).resize((cw, ch), Image.BILINEAR)) > 127
        d_c = np.asarray(Image.fromarray(d_full, mode="F").resize((cw, ch), Image.BILINEAR))
        res = fit(T, mk_c, d_c, top=top, progress=lambda i, n, r: log(f"  {name} start {i}/{n} loss {r['loss']:.3f} "
                                                                    f"iou {r['iou']:.3f} corr {r['depth_corr']:.2f}"))
        best = res[0]
        cam = _cam_json(best["p"], 1 / s, (W, H))
        alts = [{"azimuth": round(float(r["p"][0] % 360), 1), "elevation": round(float(r["p"][1]), 1),
                 "loss": round(r["loss"], 3), "iou": round(r["iou"], 3), "depth_corr": round(r["depth_corr"], 3)}
                for r in res[1:]]
        far = [r for r in res[1:] if abs(((r["p"][0] - best["p"][0] + 180) % 360) - 180) > 25
               or abs(r["p"][1] - best["p"][1]) > 15]  # runner-ups that are genuinely another viewpoint
        gap = (far[0]["loss"] - best["loss"]) if far else None
        entry = {"photo": name, "evidence": ["photo mask", "monocular depth (Depth Anything V2 small)"],
                 "declared_view": (ref.get("view") or {}).get(name), "camera": cam,
                 "scores": {"iou": round(best["iou"], 3), "depth_corr": round(best["depth_corr"], 3)},
                 "confidence": "high" if gap is None or gap > 0.06 else "ambiguous",
                 "runner_up_loss_gap": None if gap is None else round(gap, 3), "alternatives": alts,
                 "model_bbox_centre_mm": [round(float(x), 1) for x in centre],
                 "assumptions": ["robot flat on floor", "square pixels", "spec articulation as built"]}
        (out / f"{path.stem}.pose.json").write_text(json.dumps(entry, indent=1))
        overlay(im, T, best["p"], (ch, cw), mk_c).save(out / f"{path.stem}.overlay.png")
        results[name] = entry
        log(f"{name}: az {cam['azimuth']} el {cam['elevation']} roll {cam['roll']} fov {cam['intrinsics_px']['fov_deg_long_side']} "
            f"iou {best['iou']:.3f} corr {best['depth_corr']:.2f} {entry['confidence']} (declared {entry['declared_view']})")
    return results


def add_cli(sub):
    p = sub.add_parser("pose-photo", help="monocular depth + camera/robot pose per reference photo (writes <robot>/pose/)")
    p.add_argument("spec")
    p.add_argument("--photo", help="one photo file name (default: every photo in REFERENCE.json)")
    p.add_argument("--out", help="output folder (default: <spec folder>/pose)")
    p.add_argument("--starts", type=int, default=5, help="candidate cameras refined (default 5)")

    def go(a):
        run(a.spec, a.photo, a.out, a.starts)
        return 0
    p.set_defaults(func=go)

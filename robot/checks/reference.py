"""Silhouette comparison against reference photos (`reference` in the spec): catches "does not look like the photo".

Each entry: {"image": "photo.png", "view": "side|front|top|iso|iso_back", "mask": "mask.png" (optional, white = robot),
"scale_hint": mm/px (optional), "dir": [x, y, z] (optional camera direction, overrides the view's), "approximate": bool}.
The model's orthographic silhouette from the same view and the photo mask are both cropped to their bounding boxes,
scaled to the same length (aspect preserved) and aligned at the ground line and the front tip, then compared:
IoU overall and per third (front / middle / rear), plus the Hausdorff distance between the outlines.
IoU < 0.80 is a blocker, 0.80-0.88 a warning (an `approximate` entry, e.g. a perspective render, caps at warning).
Model convention: +y forward, +z up, +x right. Views put the front on the LEFT of the image (like a CAD side view).
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok

G = "reference"
BLOCK_IOU, WARN_IOU = 0.80, 0.88
CANVAS = 400  # normalised length in px

# camera direction, image-up; image-right = dir x up. Front (+y) on the left wherever that is defined.
VIEWS = {
    "side": ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),  # looking at the robot's left flank, +y to the left
    "front": ((0.0, -1.0, 0.0), (0.0, 0.0, 1.0)),
    "top": ((0.0, 0.0, -1.0), (1.0, 0.0, 0.0)),  # +y to the left
    "iso": ((0.75, -0.45, -0.5), (0.0, 0.0, 1.0)),  # front-left, from above (ref2-style CAD render)
    "iso_back": ((0.6, -0.7, -0.55), (0.0, 0.0, 1.0)),
}


def _norm(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def silhouette(world, dir, up, px_mm=0.25):
    """Binary orthographic silhouette (H, W) of the non-wire bodies, row 0 at the top. Returns (mask, mm per px)."""
    from PIL import Image, ImageDraw

    d = _norm(dir)
    right = _norm(np.cross(d, up))
    u = _norm(np.cross(right, d))
    tris = [b.mesh.triangles for b in world.bodies if not getattr(b, "is_wire", False) and b.mesh is not None]
    if not tris:
        return None, px_mm
    T = np.concatenate(tris)
    x, y = T @ right, T @ u
    x0, y1 = x.min(), y.max()
    W = int(np.ceil((x.max() - x0) / px_mm)) + 4
    H = int(np.ceil((y1 - y.min()) / px_mm)) + 4
    if W * H > 4000 * 4000:
        px_mm *= np.sqrt(W * H) / 4000
        return silhouette(world, dir, up, px_mm)
    X = (x - x0) / px_mm + 2
    Y = (y1 - y) / px_mm + 2
    img = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(img)
    for tx, ty in zip(X, Y):
        dr.polygon([(tx[0], ty[0]), (tx[1], ty[1]), (tx[2], ty[2])], fill=255)
    from scipy import ndimage as nd

    return nd.binary_fill_holes(np.asarray(img) > 0), px_mm  # outlines only, like the traced photo masks


def load_mask(path):
    from PIL import Image

    a = np.asarray(Image.open(path).convert("L"))
    return a > 127


def _crop(m):
    ys, xs = np.nonzero(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def normalise(m, n=CANVAS):
    """Crop to the bounding box and rescale so the width is n px (aspect kept)."""
    from PIL import Image

    c = _crop(m)
    h, w = c.shape
    nh = max(1, int(round(h * n / w)))
    return np.asarray(Image.fromarray(c.astype(np.uint8) * 255).resize((n, nh), Image.BILINEAR)) > 127


def _pad_bottom_left(a, b):
    """Common canvas; both anchored at bottom (ground) and left (front tip)."""
    H = max(a.shape[0], b.shape[0])
    W = max(a.shape[1], b.shape[1])

    def put(m):
        out = np.zeros((H, W), bool)
        out[H - m.shape[0]:, :m.shape[1]] = m
        return out

    return put(a), put(b)


def _iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 1.0


def _outline(m):
    from scipy import ndimage as nd

    return m & ~nd.binary_erosion(m)


def compare(model_mask, ref_mask):
    """IoU, per-third IoU, Hausdorff (in fraction of length) and the two aligned masks."""
    from scipy import ndimage as nd

    a, b = _pad_bottom_left(normalise(model_mask), normalise(ref_mask))
    W = a.shape[1]
    regions = {}
    for name, (s, e) in zip(("front", "middle", "rear"), ((0, W // 3), (W // 3, 2 * W // 3), (2 * W // 3, W))):
        regions[name] = round(_iou(a[:, s:e], b[:, s:e]), 3)
    oa, ob = _outline(a), _outline(b)
    da = nd.distance_transform_edt(~ob)[oa].max() if oa.any() and ob.any() else W
    db = nd.distance_transform_edt(~oa)[ob].max() if oa.any() and ob.any() else W
    return {"iou": round(_iou(a, b), 3), "regions": regions, "hausdorff_frac": round(float(max(da, db)) / W, 3),
            "aspect_model": round(_crop(model_mask).shape[0] / _crop(model_mask).shape[1], 3),
            "aspect_ref": round(_crop(ref_mask).shape[0] / _crop(ref_mask).shape[1], 3)}, a, b


def overlay_png(a, b) -> bytes:
    """Model red, photo blue, overlap purple, on white."""
    import io

    from PIL import Image

    img = np.full(a.shape + (3,), 255, np.uint8)
    img[b & ~a] = (80, 120, 255)
    img[a & ~b] = (235, 60, 60)
    img[a & b] = (150, 90, 190)
    for m, c in ((a, (160, 0, 0)), (b, (0, 0, 160))):
        img[_outline(m)] = c
    out = io.BytesIO()
    Image.fromarray(img).save(out, format="PNG")
    return out.getvalue()


def entries(spec):
    """Photo entries: `reference` is a list, or {"views": [...], "features": {...}}."""
    ref = (spec.raw or {}).get("reference") or []
    return list(ref.get("views") or []) if isinstance(ref, dict) else list(ref)


def features(spec):
    """Feature checklist {name: part id}: `reference.features` (dict form of `reference`) or top-level `reference_features`."""
    ref = (spec.raw or {}).get("reference")
    f = (ref.get("features") if isinstance(ref, dict) else None) or (spec.raw or {}).get("reference_features") or {}
    return dict(f) if isinstance(f, dict) else {str(x): str(x) for x in f}


def evaluate(world, spec, entry):
    """-> (stats dict, overlay png bytes). Raises ValueError for an unusable entry."""
    view = entry.get("view") or "side"
    if view not in VIEWS and not entry.get("dir"):
        raise ValueError(f"unknown view `{view}` (use one of {', '.join(VIEWS)} or give `dir`)")
    d, up = VIEWS.get(view, (None, (0.0, 0.0, 1.0)))
    d = entry.get("dir") or d
    base = Path(getattr(spec, "base_dir", ".") or ".")
    mp = entry.get("mask")
    if not mp:
        raise ValueError("no `mask` given (segmenting the raw photo automatically is not supported; trace a mask PNG)")
    ref = load_mask(base / mp)
    if not ref.any():
        raise ValueError(f"mask `{mp}` is empty")
    sil, px = silhouette(world, d, up)
    if sil is None or not sil.any():
        raise ValueError("the model has no visible bodies")
    stats, a, b = compare(sil, ref)
    length_mm = _crop(sil).shape[1] * px
    stats["hausdorff_mm"] = round(stats["hausdorff_frac"] * length_mm, 1)
    stats["view"] = view
    return stats, overlay_png(a, b)


def run(ctx):
    out = []
    for fn in (feature_direction, curvature, wheel_enclosure, weapon_profile, feature_presence):
        try:
            out += fn(ctx)
        except Exception as ex:  # noqa: BLE001 - fail closed per sub-check
            out.append(fail("checks.crashed", G, WARNING, "A shape check crashed", f"`{fn.__name__}`: {type(ex).__name__}: {ex}"))
            ctx.not_checked.append(f"shape.{fn.__name__} crashed")
    return out + silhouettes(ctx)


def silhouettes(ctx):
    spec = ctx.r.spec
    out = []
    refs = entries(spec)
    if not refs:
        return []  # optional, like `targets`
    odir = Path(os.environ.get("ROBOT_REFERENCE_OUT") or Path(tempfile.gettempdir()) / "robot_reference")
    odir.mkdir(parents=True, exist_ok=True)
    per_view = {}
    for i, e in enumerate(refs):
        view = e.get("view") or "side"
        try:
            stats, png = evaluate(ctx.world, spec, e)
        except Exception as ex:  # noqa: BLE001 - fail closed
            out.append(fail("reference.unusable", G, WARNING, "Reference photo could not be compared",
                            f"Reference #{i} ({view}): {ex}").fix("Give a binary `mask` PNG (white = robot) next to the spec."))
            ctx.not_checked.append(f"Silhouette vs reference photo #{i} ({view})")
            continue
        safe = (spec.name or "robot").replace("/", "_").replace(" ", "_")
        path = odir / f"{safe}_compare_{view}.png"
        path.write_bytes(png)
        stats["overlay"] = str(path)
        per_view[view] = stats
        iou, reg = stats["iou"], stats["regions"]
        worst = min(reg, key=reg.get)
        msg = (f"{view} view: silhouette IoU {iou:.2f} with `{e.get('image') or e.get('mask')}` (front {reg['front']:.2f}, "
               f"middle {reg['middle']:.2f}, rear {reg['rear']:.2f}); outlines differ by up to {stats['hausdorff_mm']:.0f} mm. "
               f"Worst region: {worst}. Height/length {stats['aspect_model']:.2f} model vs {stats['aspect_ref']:.2f} photo. "
               f"Overlay (model red, photo blue): {path}")
        if iou >= WARN_IOU:
            out.append(ok("reference.silhouette", G, "Matches the reference photo", msg))
        else:
            sev = BLOCKER if iou < BLOCK_IOU and not e.get("approximate") else WARNING
            out.append(fail("reference.silhouette", G, sev, "Does not look like the reference photo", msg)
                       .fix(f"Compare {path}: red = model only, blue = photo only. Fix the {worst} of the robot first."))
    ctx.metrics["reference"] = per_view
    return out


# ---- shape-intent checks (reviewer list) -------------------------------------------------------------------------------
FWD = np.array([0.0, 1.0, 0.0])


def _solid(world):
    return [b for b in world.bodies if not b.is_wire and b.mesh is not None]


def _praw(ctx, b):
    if b.part_idx is None:
        return {}
    parts = (ctx.r.spec.raw or {}).get("parts") or []
    pid = ctx.r.spec.parts[b.part_idx].id if b.part_idx < len(ctx.r.spec.parts) else None
    return next((p for p in parts if p.get("id") == pid), {})


def _ground(ctx):
    gz = ctx.r.spec.ground_z
    return float(gz) if gz is not None else float(min(b.aabb[0][2] for b in _solid(ctx.world)))


def feature_direction(ctx):
    """Blades/wedgelets must point forward (+y): tip vector, frontmost point and tip height above the floor."""
    out, gz = [], _ground(ctx)
    blades = [b for b in _solid(ctx.world) if b.kind in ("wedge", "blade", "wedgelet")]
    allv = np.concatenate([b.mesh.vertices for b in _solid(ctx.world)])
    front_y = float(allv[:, 1].max())
    for b in blades:
        V = np.asarray(b.mesh.vertices)
        tip = V[np.argmax(V[:, 1])]
        d = tip - V.mean(0)
        d = d / (np.linalg.norm(d) or 1)
        h = float(tip[2] - gz)
        ctx.metrics.setdefault("feature_direction", {})[b.id] = {"tip": [round(float(x), 1) for x in tip],
                                                                "dir": [round(float(x), 2) for x in d], "tip_height_mm": round(h, 1)}
        msg = (f"`{b.id}` tip at {np.round(tip, 1).tolist()} points {np.round(d, 2).tolist()} (forward = +y, dot {d @ FWD:.2f}); "
               f"tip {h:.1f} mm above the floor; robot front is y = {front_y:.1f}.")
        if d @ FWD < 0.5:
            out.append(fail("shape.feature_direction", G, BLOCKER, "Blade does not point forward", msg).on(b.id).here(tip)
                       .fix("Rotate the blade so its tip faces +y."))
        elif h > 5.0 or tip[1] < front_y - 15.0:
            out.append(fail("shape.feature_direction", G, WARNING, "Blade tip not at the front floor line", msg).on(b.id).here(tip))
        else:
            out.append(ok("shape.feature_direction", G, "Blade points forward", msg).on(b.id))
    return out


def curvature(ctx):
    """Parts tagged `organic: true` must actually have curved (BSpline/cylindrical/toroidal...) faces, not just boxes."""
    out = []
    for b in _solid(ctx.world):
        if not _praw(ctx, b).get("organic"):
            continue
        solid = getattr(b.geom, "solid", None)
        if solid is None:
            ctx.not_checked.append(f"shape.curvature of `{b.id}`: no B-rep")
            continue
        types = [str(f.geom_type).split(".")[-1].upper() for f in solid.faces()]
        curved = [t for t in types if t != "PLANE"]
        frac = len(curved) / max(len(types), 1)
        msg = f"`{b.id}`: {len(curved)} of {len(types)} faces curved ({', '.join(sorted(set(curved))) or 'none'})."
        if frac < 0.2 or not any(t in ("BSPLINE", "BEZIER", "TORUS", "CYLINDER") for t in curved):
            out.append(fail("shape.curvature", G, WARNING, "Organic part is boxy", msg).on(b.id)
                       .fix("Use splines/lofts and fillet the edges (photo shows smooth shapes)."))
        else:
            out.append(ok("shape.curvature", G, "Organic part is curved", msg).on(b.id))
    return out


def wheel_enclosure(ctx):
    """Fraction of each wheel (side projection) inside the pod/arch envelope (parts with `pod` or `arch` in id/role)."""
    sol = _solid(ctx.world)
    pods = [b for b in sol if any(k in (b.id + str(_praw(ctx, b).get("role") or "")).lower() for k in ("pod", "arch"))]
    wheels = [b for b in sol if b.kind == "wheel"]
    if not pods or not wheels:
        return []
    out = []
    for w in wheels:
        V = np.asarray(w.mesh.vertices)
        inside = np.zeros(len(V), bool)
        for p in pods:
            lo, hi = p.aabb
            inside |= (V[:, 1] >= lo[1]) & (V[:, 1] <= hi[1]) & (V[:, 2] >= lo[2]) & (V[:, 2] <= hi[2])
        f = float(inside.mean())
        ctx.metrics.setdefault("wheel_enclosure", {})[w.id] = round(f, 2)
        msg = f"`{w.id}`: {f:.0%} of the wheel (side view) lies inside the pod envelope."
        out.append((ok("shape.wheel_enclosure", G, "Wheel sits in its pod", msg) if f >= 0.5 else
                    fail("shape.wheel_enclosure", G, WARNING, "Wheel sticks out of its pod", msg)).on(w.id))
    return out


def _teeth(ctx, i):
    """Tooth count = radius peaks of the weapon's outline around its spin axis (None when no axis is declared)."""
    from .power import spin_axis

    sa = spin_axis(ctx.world, ctx.r, i)
    if sa is None:
        return None
    o, ax = sa
    tmp = np.array([0.0, 0.0, 1.0]) if abs(ax[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    from types import SimpleNamespace

    m, px = silhouette(SimpleNamespace(bodies=[ctx.world.bodies[i]]), ax, tmp, 0.25)
    # silhouette() frames on the mesh; recover the axis point in pixel coordinates the same way
    d = _norm(ax)
    right = _norm(np.cross(d, tmp))
    u = _norm(np.cross(right, d))
    T = ctx.world.bodies[i].mesh.triangles
    cx = (o @ right - (T @ right).min()) / px + 2
    cy = ((T @ u).max() - o @ u) / px + 2
    ys, xs = np.nonzero(_outline(m))
    ang = np.arctan2(ys - cy, xs - cx)
    r = np.hypot(ys - cy, xs - cx)
    nb = 180
    bins = np.zeros(nb)
    np.maximum.at(bins, ((ang + np.pi) / (2 * np.pi) * nb).astype(int) % nb, r)
    bins = (bins + np.roll(bins, 1) + np.roll(bins, -1)) / 3
    if bins.max() - bins.min() < 0.06 * bins.max():
        return 0
    hi = bins > bins.min() + 0.5 * (bins.max() - bins.min())
    return int(np.sum(hi & ~np.roll(hi, 1))) or 1


def weapon_profile(ctx):
    """Tooth count from radius peaks of the weapon outline vs `weapon.teeth`; motor inside hub when `weapon.motor_in_hub`."""
    w = (ctx.r.spec.raw or {}).get("weapon") or {}
    sol = _solid(ctx.world)
    out = []
    for i, b in enumerate(ctx.world.bodies):
        if b.kind != "weapon" or b.is_wire:
            continue
        n = _teeth(ctx, i)
        want = w.get("teeth", _praw(ctx, b).get("teeth"))
        ctx.metrics.setdefault("weapon_teeth", {})[b.id] = n
        if want is None:
            continue
        msg = f"`{b.id}`: {n} teeth found in the outline, spec says {want}."
        out.append((ok("shape.weapon_profile", G, "Weapon tooth count matches", msg) if n == int(want) else
                    fail("shape.weapon_profile", G, WARNING, "Weapon tooth count differs", msg)).on(b.id))
    if w.get("motor_in_hub"):
        mot = [b for b in sol if b.kind == "weapon_motor"]
        hubs = [b for b in sol if b.kind in ("hub", "weapon")]
        good = mot and hubs and all(any(np.all(m.aabb[0] >= h.aabb[0] - 1) and np.all(m.aabb[1] <= h.aabb[1] + 1) for h in hubs)
                                    for m in mot)
        msg = "Weapon motor " + ("is" if good else "is NOT") + " inside the hub/disc envelope (`weapon.motor_in_hub`)."
        out.append(ok("shape.weapon_profile", G, "Motor in hub", msg) if good else
                   fail("shape.weapon_profile", G, WARNING, "Motor not in hub", msg))
    return out


def feature_presence(ctx):
    """Every feature in the reference checklist maps to a part id that exists."""
    feats = features(ctx.r.spec)
    if not feats:
        return []
    ids = {p.id for p in ctx.r.spec.parts}
    out = []
    for name, pid in feats.items():
        pids = pid if isinstance(pid, list) else [pid]
        miss = [p for p in pids if p not in ids]
        msg = f"Feature `{name}` -> {', '.join(f'`{p}`' for p in pids)}" + (f": missing {miss}" if miss else " present.")
        out.append(fail("shape.feature_presence", G, BLOCKER, "Photo feature missing from the model", msg) if miss else
                   ok("shape.feature_presence", G, "Photo feature present", msg))
    return out


# ---- design-proportion ratios measured on reference photos ------------------------------------------------------------
# `reference.ratios` (dict form of `reference`) or top-level `reference_ratios`: a list of
#   {"name", "num": term | [terms summed], "den": term | [terms] (optional, default 1), "value", "tol" (abs) or
#    "tol_frac" (relative), "severity": "warning"|"blocker" (default warning), "source": "photo + how measured"}
# Terms (all generic, no robot names in the code):
#   overall.L | overall.W | overall.H        robot bounding box (y, x, z), wires excluded
#   part:<glob>.<q>   kind:<glob>.<q>        q = L W H (union bbox along y x z), cx cy cz (bbox centre), mass, vol, count
#   mass.total, count.fasteners, metric:<key> (any report metric from an earlier group), or a number
def ratios(spec):
    ref = (spec.raw or {}).get("reference")
    rs = (ref.get("ratios") if isinstance(ref, dict) else None) or (spec.raw or {}).get("reference_ratios") or []
    return list(rs)


def _bodies_for(ctx, sel):
    import fnmatch

    how, pat = sel.split(":", 1)
    out = []
    for b in ctx.world.bodies:
        if b.is_wire:
            continue
        if how == "part" and fnmatch.fnmatch(b.id, pat):
            out.append(b)
        elif how == "kind" and b.part_idx is not None and not b.fastener and fnmatch.fnmatch(ctx.r.parts[b.part_idx].part.kind, pat):
            out.append(b)
    return out


def term_value(ctx, t):
    """Model value of one ratio term. Raises KeyError/ValueError when it cannot be measured (-> NOT CHECKED)."""
    if isinstance(t, (int, float)):
        return float(t)
    t = str(t).strip()
    try:
        return float(t)
    except ValueError:
        pass
    if t.startswith("overall."):
        lo, hi = ctx.world.bounds(skip_wires=True)
        return float({"L": hi[1] - lo[1], "W": hi[0] - lo[0], "H": hi[2] - lo[2]}[t.split(".", 1)[1]])
    if t == "mass.total":
        if "mass_total_g" not in ctx.metrics:
            raise KeyError("mass group has not run (no mass_total_g)")
        return float(ctx.metrics["mass_total_g"])
    if t.startswith("metric:"):
        k = t.split(":", 1)[1]
        if k not in ctx.metrics:
            raise KeyError(f"metric `{k}` not computed (its group did not run or does not apply)")
        return float(ctx.metrics[k])
    if t == "count.fasteners":
        return float(sum(1 for b in ctx.world.bodies if b.fastener))
    if t.startswith(("part:", "kind:")):
        sel, q = t.rsplit(".", 1)
        bs = _bodies_for(ctx, sel)
        if q == "count":
            return float(len(bs))
        if not bs:
            raise KeyError(f"`{sel}` matches no body")
        if q == "mass":
            ms = [ctx.metrics.get(f"part_mass_g.{b.id}") for b in bs]
            if any(m is None for m in ms):
                raise KeyError(f"no mass for {[b.id for b, m in zip(bs, ms) if m is None]}")
            return float(sum(ms))
        if q == "vol":
            return float(sum(b.geom.volume for b in bs)) / 1000.0
        lo = np.min([b.aabb[0] for b in bs], axis=0)
        hi = np.max([b.aabb[1] for b in bs], axis=0)
        ax = {"L": 1, "W": 0, "H": 2, "cx": 0, "cy": 1, "cz": 2}[q]
        return float(hi[ax] - lo[ax]) if q in ("L", "W", "H") else float((hi[ax] + lo[ax]) / 2)
    raise ValueError(f"unknown term `{t}`")


def _sum(ctx, ts):
    return sum(term_value(ctx, x) for x in (ts if isinstance(ts, list) else [ts]))


def feature_ratios(ctx):
    """`reference.feature_ratio`: design proportions measured on the photos (ratios, so photo scale cancels) vs the model."""
    out = []
    for i, e in enumerate(ratios(ctx.r.spec)):
        name = e.get("name") or f"#{i}"
        try:
            num = _sum(ctx, e["num"])
            den = _sum(ctx, e.get("den", 1))
            if abs(den) < 1e-9:
                raise ValueError("denominator is zero")
            want = float(e["value"])
            tol = float(e["tol"]) if "tol" in e else abs(want) * float(e.get("tol_frac", 0.1))
        except Exception as ex:  # noqa: BLE001 - fail closed
            out.append(fail("reference.feature_ratio", G, WARNING, "Reference proportion could not be measured",
                            f"`{name}`: {type(ex).__name__}: {ex}").fix("Fix the term (see GUIDE: reference ratios)."))
            ctx.not_checked.append(f"Reference proportion `{name}`")
            continue
        got = num / den
        ctx.metrics[f"reference_ratio.{name}"] = round(got, 4)
        msg = (f"`{name}`: model {got:.3f} vs photo {want:.3f} ± {tol:.3f}" + (f" ({e['source']})" if e.get("source") else "")
               + (f". {e['lesson']}" if e.get("lesson") else ""))
        if abs(got - want) <= tol:
            out.append(ok("reference.feature_ratio", G, "Proportion matches the reference", msg))
        else:
            sev = BLOCKER if str(e.get("severity", "warning")).lower() == "blocker" else WARNING
            out.append(fail("reference.feature_ratio", G, sev, "Proportion differs from the reference", msg)
                       .fix(e.get("fix") or f"Move `{name}` {'up' if got < want else 'down'} by {abs(got - want):.3f}."))
    return out

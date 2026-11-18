"""`robot fit-photo SPEC`: fit a simple parametric envelope to the reference photo masks and print the proportions.

Small models cannot read polygons off a photo. This searches a wedge-box envelope (length L, width, height, front ramp
length) plus an optional weapon cylinder (radius, axis across / up, position along the length) for the best silhouette
IoU against every mask in the spec's `reference` entries, over the same cameras the `likeness` gate uses. Prints the
proportions as mm for a chosen length (`--length`, default: the spec's current length) so they can go straight into a
`robot gen build --intent` file or the chassis shape. It is a guide, not a design: the gate still judges the real model.
"""

from __future__ import annotations

import itertools
import json

import numpy as np

N = 100  # coarse canvas for the search


def _norm(m, n=N):
    from PIL import Image
    ys, xs = np.nonzero(m)
    c = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = c.shape
    nh = max(1, int(round(h * n / w)))
    return np.asarray(Image.fromarray(c.astype(np.uint8) * 255).resize((n, nh), Image.BILINEAR)) > 127


def _iou(a, b):
    H, W = max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1])
    A = np.zeros((H, W), bool); B = np.zeros((H, W), bool)
    A[H - a.shape[0]:, :a.shape[1]] = a
    B[H - b.shape[0]:, :b.shape[1]] = b
    u = (A | B).sum()
    return float((A & B).sum() / u) if u else 0.0


def _box(lo, hi):
    import trimesh
    return trimesh.creation.box(bounds=[lo, hi])


def envelope(p):
    """Mesh for params p (L = 1): w, h, ramp, disc_r, disc_axis ('x' | 'z' | None), disc_y, disc_t."""
    import trimesh
    L, w, h, ramp = 1.0, p["w"], p["h"], p["ramp"]
    y1 = L - ramp
    pts = []
    for x in (-w / 2, w / 2):
        pts += [(x, 0, 0), (x, 0, h), (x, y1, 0), (x, y1, h), (x, L, 0), (x, L, h * 0.05)]
    m = trimesh.convex.convex_hull(np.array(pts))
    if p.get("disc_axis"):
        r, t = p["disc_r"], p["disc_t"]
        c = trimesh.creation.cylinder(radius=r, height=t, sections=24)
        if p["disc_axis"] == "x":
            c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
            c.apply_translation([0, p["disc_y"], r * 0.9])
        else:
            c.apply_translation([0, p["disc_y"], h + t / 2])
        m = trimesh.util.concatenate([m, c])
    return m


def _sil(mesh, d, up):
    from PIL import Image, ImageDraw
    d = np.asarray(d, float); d /= np.linalg.norm(d)
    right = np.cross(d, up); right /= np.linalg.norm(right)
    u = np.cross(right, d)
    T = mesh.triangles
    x, y = T @ right, T @ u
    s = 300 / max(x.max() - x.min(), y.max() - y.min())
    X, Y = (x - x.min()) * s + 2, (y.max() - y) * s + 2
    img = Image.new("L", (int(X.max()) + 4, int(Y.max()) + 4), 0)
    dr = ImageDraw.Draw(img)
    for tx, ty in zip(X, Y):
        dr.polygon([(tx[0], ty[0]), (tx[1], ty[1]), (tx[2], ty[2])], fill=255)
    return np.asarray(img) > 0


def score(p, masks, dirs):
    m = envelope(p)
    sils = []
    for d in dirs:
        up = (0, 1.0, 0) if abs(d[2]) > 0.99 else (0, 0, 1.0)
        s = _norm(_sil(m, d, up))
        sils += [s, s[:, ::-1]]
    return float(np.mean([max(_iou(s, mk) for s in sils) for mk in masks]))


def fit(masks, weapon=None, rounds=3):
    from .checks.likeness import _dirs
    dirs = _dirs()
    masks = [_norm(m) for m in masks]
    p = {"w": 0.8, "h": 0.3, "ramp": 0.3, "disc_axis": None, "disc_r": 0.3, "disc_y": 0.5, "disc_t": 0.08}
    if weapon in ("x", "z"):
        p["disc_axis"] = weapon
    grid = {"w": [0.5, 0.65, 0.8, 0.95, 1.1], "h": [0.15, 0.22, 0.3, 0.4, 0.5], "ramp": [0.1, 0.2, 0.3, 0.45, 0.6]}
    if p["disc_axis"]:
        grid.update({"disc_r": [0.15, 0.22, 0.3, 0.4], "disc_y": [0.3, 0.5, 0.7, 0.9]})
    best = (score(p, masks, dirs), dict(p))
    for _ in range(rounds):
        improved = False
        for k, vals in grid.items():
            for v in vals:
                q = dict(best[1]); q[k] = v
                sc = score(q, masks, dirs)
                if sc > best[0] + 1e-4:
                    best, improved = (sc, q), True
        if not improved:
            break
    return best


def main(spec_path, length=None, weapon=None):
    from pathlib import Path
    from .checks import reference as ref
    raw = json.loads(Path(spec_path).read_text())
    base = Path(spec_path).parent
    ents = [e for e in ref.entries(type("S", (), {"raw": raw})) if e.get("mask")]
    if not ents:
        print("no `reference` entries with a mask: run `robot mask` first")
        return 1
    masks = [ref.load_mask(base / e["mask"]) for e in ents]
    if weapon == "none":
        weapon = False
    if weapon is None:
        rj = base / "REFERENCE.json"
        w = json.loads(rj.read_text()).get("weapon") if rj.exists() else None
        weapon = w.get("axis") if isinstance(w, dict) and w.get("kind") in ("disc", "drum", "bar") else None
    sc, p = fit(masks, weapon)
    L = float(length or (148.0 / max(1.0, p["w"])))  # default: the largest robot that fits the 150 mm square
    print(f"best mean silhouette IoU {sc:.2f} (coarse envelope; the real model adds detail)")
    print(f"length {L:.0f} mm (y), width {p['w'] * L:.0f} mm (x), height {p['h'] * L:.0f} mm, front ramp {p['ramp'] * L:.0f} mm long")
    big = max(L, p["w"] * L)
    if big > 150.0:
        print(f"NOTE: {big:.0f} mm exceeds the 150 mm floor square; use --length {L * 148 / big:.0f}")
    if p.get("disc_axis"):
        where = "front" if p["disc_y"] > 0.66 else "rear" if p["disc_y"] < 0.34 else "middle"
        print(f"weapon: radius {p['disc_r'] * L:.0f} mm, axis {p['disc_axis']}, centre {p['disc_y'] * L:.0f} mm from the back ({where})")
    print(json.dumps({"fit": {k: (round(v * L, 1) if isinstance(v, float) else v) for k, v in p.items()}, "iou": round(sc, 3)}))
    return 0


def add_cli(sub):
    p = sub.add_parser("fit-photo", help="fit box/ramp/weapon proportions to the reference photo masks (prints mm)")
    p.add_argument("spec")
    p.add_argument("--length", type=float, help="robot length in mm (default: largest that fits the 150 mm square)")
    p.add_argument("--weapon-axis", choices=("x", "z", "none"),
                   help="weapon cylinder turning about x or z; none for wedges (default: REFERENCE.json weapon)")
    p.set_defaults(func=lambda a: main(a.spec, a.length, a.weapon_axis))

"""`robot colors SPEC [--dry] [--parts a,b] [--min-frac F]`: give each visible part the colour it has in the photos.

WHY: hand-picked part colours drifted from the photos (a white deck rendered grey, yellow bumpers rendered black), and
the photo-vs-model review (`robot diff-photo`, Haiku notes) then reports a "different part" where the shape is right.

How: for every `reference` entry with an image and a mask, the model is rendered from the camera that `likeness`
picks for that photo, with one flat ID colour per part (z-buffered, so only the faces you can see count). The ID image
is mapped onto the photo by cropping both to their bounding boxes and stretching each axis to the photo's box, so
a model that is still a little too tall or short samples the right rows. For each part, the photo pixels that fall
on it, inside the photo mask and at least 2 px from the part's edge, give a median RGB, lifted by 1/0.9 to undo the
renderer's average shading. A part is sampled only when it covers at least --min-frac of the photo mask (default
3 %) across all photos, and only from photos whose silhouette IoU is at least 0.6. Only made body parts are sampled
(structure, plates, armour, weapons...): bought parts, wheels, fasteners and wires keep their colours unless named
with --parts, because where the model still differs from the photo they are the parts that land on the wrong pixels. Only placeholder colours are replaced (none, or a
plain mid grey: the generators' default), and only when the photo shows a different colour, not the same colour lit
differently (hue within 35 deg, lightness within 0.35). A colour someone chose is kept: clear and reflective parts
sample as whatever is behind or reflected in them. --force writes every sampled colour.

Only `color` fields change: no geometry, mass or check result moves (likeness compares masks, not colours). Re-run it
after a big reshape. Use --dry to print the colours without writing.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

SHADE = 0.9
SKIP_KINDS = {"wheel", "tyre", "motor", "weapon_motor", "battery", "esc", "receiver", "servo", "switch"}
MIN_IOU = 0.6  # below this the model is too far from the photo for per-part pixels to mean anything
ERODE = 2


def _id_image(world, d, up, width=900):
    """(H, W) int array: 0 = background, i + 1 = world.bodies[i] (visible faces only)."""
    from . import render as R

    bodies = [(i, b) for i, b in enumerate(world.bodies)
              if not getattr(b, "is_wire", False) and b.mesh is not None]
    if not bodies:
        return None
    lo, hi = world.bounds(skip_wires=True)
    cam = R._Cam(lo - 1.0, hi + 1.0, R.View("ids", np.asarray(d, float), np.asarray(up, float), None, width, 0.0))
    img = np.zeros((cam.h, cam.w, 3), np.uint8)
    zbuf = np.full((cam.h, cam.w), np.inf)
    for i, b in bodies:
        T = b.mesh.triangles
        if not len(T):
            continue
        n = i + 1
        cols = np.tile(np.array([(n >> 16) & 255, (n >> 8) & 255, n & 255], np.uint8), (len(T), 1))
        S = cam.project(T.reshape(-1, 3)).reshape(-1, 3, 3)
        R._raster(cam, S, cols, zbuf, img)
    ids = (img[..., 0].astype(np.int64) << 16) | (img[..., 1].astype(np.int64) << 8) | img[..., 2]
    ids[~np.isfinite(zbuf)] = 0
    return ids


def _bbox(m):
    ys, xs = np.nonzero(m)
    return ys.min(), ys.max() + 1, xs.min(), xs.max() + 1


def sample(spec_path, min_frac=0.03, parts=None, debug=None):
    """{part id: (hex colour, pixel count)} for the parts seen in the reference photos, plus a list of notes."""
    from PIL import Image
    from scipy import ndimage as nd

    from . import spec as spec_mod
    from . import world as world_mod
    from .checks import likeness as L
    from .checks import reference as ref

    s = spec_mod.load(spec_path)
    base = Path(s.base_dir)
    r = world_mod.resolve(s, fast=True)
    w = world_mod.World.start(r)
    sils = L._sils(w)
    dirs = L._dirs()
    raw = json.loads(Path(spec_path).read_text())
    fast_ids = {f.get("id") for f in raw.get("fasteners") or []}
    skip_ids = {q["id"] for q in raw.get("parts") or [] if q.get("catalog") or q.get("kind") in SKIP_KINDS}
    acc, notes, total = {}, [], 0
    for e in ref.entries(s):
        if not (e.get("mask") and e.get("image")):
            continue
        mask = ref.load_mask(base / e["mask"])
        iou, _, ci = L.best_match(sils, mask, L.allowed(*L.photo_view(L._refjson(s), e)))
        if ci < 0:
            notes.append(f"{e['image']}: no allowed camera")
            continue
        if iou < MIN_IOU:
            notes.append(f"{e['image']}: skipped, silhouette IoU {iou:.2f} < {MIN_IOU} (parts would land on the wrong pixels)")
            continue
        k, mir = divmod(ci, 2)
        d = np.asarray(dirs[k], float)
        up = np.array([0, 1.0, 0]) if abs(d[2]) > 0.99 else np.array([0, 0, 1.0])
        ids = _id_image(w, d, up)
        if ids is None or not (ids > 0).any():
            continue
        if mir:
            ids = ids[:, ::-1]
        photo = np.asarray(Image.open(base / e["image"]).convert("RGB").resize(mask.shape[::-1]), float)
        my0, my1, mx0, mx1 = _bbox(ids > 0)
        py0, py1, px0, px1 = _bbox(mask)
        sx = (mx1 - mx0) / max(px1 - px0, 1)  # model px per photo px; each axis stretched to the bounding box so a
        sy = (my1 - my0) / max(py1 - py0, 1)  # model that is still too tall or short samples the right rows
        yy, xx = np.mgrid[py0:py1, px0:px1]
        mxs = np.clip((mx0 + (xx - px0) * sx).astype(int), 0, ids.shape[1] - 1)
        mys = np.clip((my0 + (yy - py0) * sy).astype(int), 0, ids.shape[0] - 1)
        on = ids[mys, mxs]
        inside = mask[py0:py1, px0:px1]
        total += int(inside.sum())
        pix = photo[py0:py1, px0:px1]
        if debug:  # photo with the model's part outlines in red: check the mapping before trusting a colour
            edge = np.zeros(on.shape, bool)
            edge[:-1] |= on[:-1] != on[1:]
            edge[:, :-1] |= on[:, :-1] != on[:, 1:]
            dbg = photo.astype(np.uint8).copy()
            dbg[py0:py1, px0:px1][edge] = (255, 0, 0)
            Path(debug).mkdir(parents=True, exist_ok=True)
            Image.fromarray(dbg).save(Path(debug) / f"colors_{Path(e['image']).stem}.png")
        for n in np.unique(on[inside]):
            if n <= 0:
                continue
            b = w.bodies[n - 1]
            if b.part_idx is None or b.fastener or b.id in fast_ids or str(b.id).startswith("wire:"):
                continue
            if (parts and b.id not in parts) or (not parts and b.id in skip_ids):
                continue
            sel = nd.binary_erosion(on == n, iterations=ERODE) & inside
            if sel.sum() < 30:
                continue
            acc.setdefault(b.id, []).append(pix[sel])
        notes.append(f"{e['image']}: camera {L.cam_name(ci)}")
    out = {}
    for pid, chunks in acc.items():
        P = np.concatenate(chunks)
        if len(P) < max(150, min_frac * max(total, 1)):
            continue
        c = np.clip(np.median(P, axis=0) / SHADE, 0, 255).astype(int)
        out[pid] = ("#{:02x}{:02x}{:02x}".format(*c), len(P))
    return out, notes


def different(old, new):
    """True when the photo colour is a different colour, not the same one lit differently: hue more than 35 deg
    apart (both saturated), grey vs saturated, or lightness more than 0.35 apart."""
    import colorsys

    from .world import parse_color
    a, b = parse_color(old or ""), parse_color(new or "")
    if a is None or b is None:
        return True
    ha, la, sa = colorsys.rgb_to_hls(*[x / 255 for x in a])
    hb, lb, sb = colorsys.rgb_to_hls(*[x / 255 for x in b])
    sat_a, sat_b = sa > 0.3 and 0.12 < la < 0.9, sb > 0.3 and 0.12 < lb < 0.9
    if sat_a != sat_b and abs(sa - sb) > 0.3:
        return True
    if sat_a and sat_b and min(abs(ha - hb), 1 - abs(ha - hb)) * 360 > 35:
        return True
    return abs(la - lb) > 0.35


def placeholder(c):
    """True for no colour or a plain mid grey (the generators' default for printed parts): a colour nobody chose."""
    import colorsys

    from .world import parse_color
    rgb = parse_color(c or "")
    if rgb is None:
        return True
    _, lt, s = colorsys.rgb_to_hls(*[x / 255 for x in rgb])
    return s < 0.1 and 0.2 < lt < 0.8


def apply(spec_path, cols, force=False):
    p = Path(spec_path)
    txt = p.read_text()
    raw = json.loads(txt)
    changed = []
    for part in raw.get("parts") or []:
        if part.get("id") in cols and part.get("color") != cols[part["id"]][0] and (
                force or (placeholder(part.get("color")) and different(part.get("color"), cols[part["id"]][0]))):
            changed.append((part["id"], part.get("color"), cols[part["id"]][0]))
            part["color"] = cols[part["id"]][0]
    ind = 1 if txt.startswith("{\n ") and not txt.startswith("{\n  ") else 2
    p.write_text(json.dumps(raw, indent=ind) + "\n")
    return changed


def main(a):
    parts = set(a.parts.split(",")) if a.parts else None
    cols, notes = sample(a.spec, a.min_frac, parts, a.debug)
    for n in notes:
        print("  " + n)
    if not cols:
        print("no part covers enough of the photos to sample")
        return 1
    if a.dry:
        for pid, (c, n) in sorted(cols.items()):
            print(f"{pid}: {c} ({n} px)")
        return 0
    for pid, old, new in apply(a.spec, cols, a.force):
        print(f"{pid}: {old} -> {new} ({cols[pid][1]} px)")
    return 0


def add_cli(sub):
    p = sub.add_parser("colors", help="set each visible part's colour from the reference photos (no geometry change)")
    p.add_argument("spec")
    p.add_argument("--dry", action="store_true", help="print the sampled colours, do not write the spec")
    p.add_argument("--parts", help="only these part ids (comma separated)")
    p.add_argument("--min-frac", type=float, default=0.03, help="least share of the photo mask a part must cover")
    p.add_argument("--force", action="store_true", help="also replace colours that are only a shade off the photo")
    p.add_argument("--debug", help="folder for photo + part-outline sheets (colors_<photo>.png)")
    p.set_defaults(func=main)

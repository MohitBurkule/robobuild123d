"""`robot partseg`: fine part segmentation of REFERENCE photos (drawn by a vision LLM) and a score against the model.

Segment file (one per photo): robots/<name>/reference/segments/<photo stem>.json

    {"photo": "x.aws74.webp",
     "segments": [{"id": "s01", "label": "left front wheel", "kind": "wheel",
                   "polygon": [[x, y], ...]}, ...]}      # x, y = fractions 0..1 of the FULL photo (0,0 = top-left)

BETTER WAY (regions): `regions ROBOT_DIR PHOTO` cuts the robot into ~100 numbered regions with exact boundaries. The labeller
then only groups them: <stem>.json = {"photo": ..., "parts": [{"label": "left front wheel", "kind": "wheel", "regions": [12, 14]}]}.
A file may hold BOTH: `segments` (rough brush polygons, fast) and `parts` (region groups, exact). `fuse` lets the brush
polygons split regions that straddle two of them and carve out small things the auto cut swallowed (screws), then the
labeller regroups. At most 3 rounds per photo. check lists regions left out of every part (the gaps) and regions used twice.

Sub-commands
  grid PHOTO [OUT]      photo with a labelled 10 % grid so polygon corners can be read off
  check SEGFILE         rasterise: coverage of the photo mask, overlaps, tiny / outside-robot segments; writes
                        <stem>.parts.png (coloured, numbered) next to the segment file. A segment may carry "holes": [[[x,y],...]] cut out of it
  score SPEC            per photo render the model parts (visible only, id buffer) from the photo's camera, align like the
                        silhouette gate (bbox crop, bottom-left) and report per-segment best IoU, area weighted mean IoU,
                        F1@0.5; writes reference/segments/score.json + <stem>.model.png / <stem>.compare.png

Segments are meant to be FINE; merge them later for bigger parts (`merge` key: {"big label": ["s01", "s02"]} in the file).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

PALETTE = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240),
           (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40),
           (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128)]
CANVAS = 400


# ---------------------------------------------------------------- photo side
def _load_ref(base: Path):
    p = base / "REFERENCE.json"
    return json.loads(p.read_text()) if p.exists() else {}


def photo_mask_for(base: Path, photo: str, max_px: int = 900):
    """Robot mask of a photo in the cropped, thumbnailed frame the likeness gate uses. Returns (mask, crop)."""
    from .mask import THR, photo_mask

    rj = _load_ref(base)
    crop = (rj.get("crop") or {}).get(photo)
    thr = (rj.get("mask_thr") or {}).get(photo, THR)
    mode = (rj.get("mask_mode") or {}).get(photo, "plain")
    m = photo_mask(base / "reference" / photo, thr=thr, max_px=max_px, crop=crop, mode=mode)
    return m, crop


def raster_parts(d: dict, base: Path, shape, crop=None):
    """Masks of the parts of a segment file: region based (`parts` [{label, kind, regions: [ids]}]) or polygon based
    (`segments`). Returns (parts list, masks list)."""
    if d.get("parts"):
        lab = load_regions(base, d["photo"])
        if lab is None or lab.shape != tuple(shape):
            raise SystemExit("run `robot partseg regions` first (regions.png missing or from another mask)")
        parts = d["parts"]
        for i, p in enumerate(parts):
            p.setdefault("id", f"p{i + 1:02d}")
        return parts, [np.isin(lab, p["regions"]) for p in parts]
    return d["segments"], raster_segments(d["segments"], shape, crop)


def raster_segments(segs, shape, crop=None):
    """List of boolean masks (H, W) for polygons given as fractions of the full photo; `crop` [x0,y0,x1,y1] fractions."""
    from PIL import Image, ImageDraw

    H, W = shape
    x0, y0, x1, y1 = crop or (0, 0, 1, 1)
    out = []
    for s in segs:
        im = Image.new("L", (W, H), 0)
        pts = [((x - x0) / (x1 - x0) * W, (y - y0) / (y1 - y0) * H) for x, y in s["polygon"]]
        d = ImageDraw.Draw(im)
        if len(pts) >= 3:
            d.polygon(pts, fill=255)
        for h in s.get("holes") or []:  # polygons cut out of this segment (a part around another part)
            hp = [((x - x0) / (x1 - x0) * W, (y - y0) / (y1 - y0) * H) for x, y in h]
            if len(hp) >= 3:
                d.polygon(hp, fill=0)
        out.append(np.asarray(im) > 127)
    return out


def regions(base: Path, photo: str, n: int = 400, merge_thr: float = 14.0, max_px: int = 900, method: str = "edges"):
    """Exact-boundary over-segmentation of the robot in a photo (SLIC superpixels, then colour-similar neighbours merged).
    Returns (labels (H, W) int, 0 = background, 1..N regions) in the cropped, thumbnailed mask frame. Saves
    <stem>.regions.png (16 bit label map) and <stem>.regions.view.png (numbered) in reference/segments/."""
    from PIL import Image, ImageDraw
    from scipy import ndimage as nd
    from skimage import color, graph, segmentation

    m, crop = photo_mask_for(base, photo, max_px)
    im = Image.open(base / "reference" / photo).convert("RGB")
    if crop:
        W0, H0 = im.size
        im = im.crop((int(crop[0] * W0), int(crop[1] * H0), int(crop[2] * W0), int(crop[3] * H0)))
    im = im.resize((m.shape[1], m.shape[0]))
    a = np.asarray(im)
    prim = None
    if method == "edges":
        lab, prim = edge_regions(a, m)
    else:
        lab = segmentation.slic(a, n_segments=n, compactness=8, sigma=1, mask=m, start_label=1, channel_axis=-1)
        g = graph.rag_mean_color(a, lab)
        lab = graph.merge_hierarchical(lab, g, thresh=merge_thr, rag_copy=False, in_place_merge=True,
                                       merge_func=lambda g_, s_, d_: None,
                                       weight_func=lambda g_, s_, d_, n_: {"weight": float(np.linalg.norm(g_.nodes[d_]["mean color"] - g_.nodes[n_]["mean color"]))})
        lab[~m] = 0
    # drop tiny regions into their biggest neighbour
    ids, cnt = np.unique(lab[lab > 0], return_counts=True)
    for i, c in zip(ids, cnt):
        if c < 0.0004 * m.sum():
            ring = nd.binary_dilation(lab == i, iterations=2) & (lab != i) & (lab > 0)
            if ring.any():
                lab[lab == i] = np.bincount(lab[ring]).argmax()
    _, lab = np.unique(lab, return_inverse=True)  # relabel 0..N (0 = background)
    lab = lab.reshape(m.shape)
    if not (lab == 0).any() or not m.any():
        pass
    sd = base / "reference" / "segments"
    sd.mkdir(parents=True, exist_ok=True)
    stem = Path(photo).stem
    Image.fromarray(lab.astype(np.uint16)).save(sd / f"{stem}.regions.png")
    b = segmentation.find_boundaries(lab, mode="inner")
    v = a.copy()
    v[~m] = 255
    v[b] = (255, 0, 255)
    img = Image.fromarray(v)
    dr = ImageDraw.Draw(img)
    for k in range(1, lab.max() + 1):
        ys, xs = np.nonzero(lab == k)
        if len(ys):
            cy, cx = nd.center_of_mass(lab == k)
            dr.text((cx - 6, cy - 5), str(k), fill=(255, 255, 0), stroke_width=1, stroke_fill=(0, 0, 0))
    img.save(sd / f"{stem}.regions.view.png")
    return lab


def fuse(segfile, big=0.006, split_frac=0.15) -> dict:
    """Let the rough brush polygons (`segments`) correct the auto regions, in place (round N of at most 3):
    - a region that two or more BIG brush polygons each cover >= `split_frac` of is split along those polygons;
    - a SMALL brush polygon (< `big` of the robot, e.g. a screw the auto cut swallowed) is carved out as its own region.
    `parts` (region groups) are kept in step: pieces inherit the parent's part, carved regions leave their old part and
    start unassigned. Writes the new regions.png / view and returns a report: what was split / carved, and for every
    brush polygon the parts its pixels fall in (so labels from the two views can be reconciled)."""
    from PIL import Image

    sf = Path(segfile)
    base = sf.parents[2]
    d = load_segments(sf)
    m, crop = photo_mask_for(base, d["photo"])
    lab = load_regions(base, d["photo"])
    if lab is None:
        lab = regions(base, d["photo"])
    brush = [s for s in d.get("segments", []) if s.get("polygon")]
    bm = raster_segments(brush, m.shape, crop)
    tot = m.sum()
    nxt = int(lab.max()) + 1
    parts = d.get("parts") or []
    rep = {"split": [], "carved": [], "round_notes": "run `partseg regions`-view again, regroup the new region ids"}
    inherit = {}  # new id -> parent id
    isbig = [r.sum() >= big * tot for r in bm]
    for k in [int(v) for v in np.unique(lab[lab > 0])]:
        reg = lab == k
        a = reg.sum()
        cov = [i for i, r in enumerate(bm) if isbig[i] and (r & reg).sum() >= split_frac * a and (r & reg).sum() > 30]
        if len(cov) >= 2:
            left = reg.copy()
            for i in cov:
                piece = reg & bm[i] & left
                if piece.sum() > 30 and piece.sum() < left.sum():
                    lab[piece] = nxt
                    inherit[nxt] = k
                    rep["split"].append({"region": k, "into": nxt, "by": brush[i].get("label", brush[i].get("id"))})
                    nxt += 1
                    left &= ~piece
    for i, r in enumerate(bm):
        if isbig[i] or not r.any():
            continue
        carve = r & m
        if carve.sum() < 12:
            continue
        mine = int(np.bincount(lab[carve]).argmax()) if (lab[carve] > 0).any() else 0
        if mine and (carve & (lab == mine)).sum() >= 0.8 * (lab == mine).sum():
            continue  # a region of its own already
        lab[carve] = nxt
        rep["carved"].append({"region": nxt, "from": int(mine), "by": brush[i].get("label", brush[i].get("id"))})
        for p_ in parts:  # carved regions are unassigned
            pass
        nxt += 1
    for p_ in parts:
        extra = [n for n, par in inherit.items() if par in p_["regions"]]
        p_["regions"] = sorted(set(p_["regions"]) | set(extra))
    Image.fromarray(lab.astype(np.uint16)).save(base / "reference" / "segments" / f"{Path(d['photo']).stem}.regions.png")
    _view(base, d["photo"], lab, m, crop)
    # which parts each brush polygon falls in
    owner = np.zeros(lab.shape, int)
    for pi, p_ in enumerate(parts, 1):
        owner[np.isin(lab, p_["regions"])] = pi
    rep["brush_vs_parts"] = []
    for s_, r in zip(brush, bm):
        o = np.bincount(owner[r & m], minlength=len(parts) + 1)
        tot_ = max(1, o.sum())
        rep["brush_vs_parts"].append({"brush": s_.get("label"), "parts": {(parts[j - 1]["label"] if j else "unassigned"): round(float(o[j] / tot_), 2)
                                                                           for j in np.argsort(-o)[:3] if o[j] / tot_ >= 0.1}})
    sf.write_text(json.dumps(d))
    rep["regions"] = int(lab.max())
    return rep


def _view(base, photo, lab, m, crop):
    from PIL import Image, ImageDraw
    from scipy import ndimage as nd
    from skimage import segmentation

    im = Image.open(base / "reference" / photo).convert("RGB")
    if crop:
        W0, H0 = im.size
        im = im.crop((int(crop[0] * W0), int(crop[1] * H0), int(crop[2] * W0), int(crop[3] * H0)))
    a = np.asarray(im.resize((m.shape[1], m.shape[0]))).copy()
    a[~m] = 255
    a[segmentation.find_boundaries(lab, mode="inner")] = (255, 0, 255)
    img = Image.fromarray(a)
    dr = ImageDraw.Draw(img)
    for k in np.unique(lab[lab > 0]):
        cy, cx = nd.center_of_mass(lab == k)
        dr.text((cx - 6, cy - 5), str(int(k)), fill=(255, 255, 0), stroke_width=1, stroke_fill=(0, 0, 0))
    img.save(base / "reference" / "segments" / f"{Path(photo).stem}.regions.view.png")


def _ring_support(edge_near, x, y, r, k=90):
    """Fraction of a circle's perimeter that lies on an image edge (rejects Hough circles that cross flat areas)."""
    t = np.linspace(0, 2 * np.pi, k, endpoint=False)
    xs, ys = np.round(x + r * np.cos(t)).astype(int), np.round(y + r * np.sin(t)).astype(int)
    ok = (xs >= 0) & (xs < edge_near.shape[1]) & (ys >= 0) & (ys < edge_near.shape[0])
    return float(edge_near[ys[ok], xs[ok]].sum() / max(1, k))


def edge_regions(a, m, min_len=0.03, max_circles=40):
    """Region label map from STRAIGHT and ROUND edges only: robot parts are mostly flat faces, discs and smooth curves, so
    texture and grain must not cut regions. a = RGB image, m = robot mask. Edges used: Canny chains longer than `min_len`
    of the image diagonal (smooth outlines), line segments (LSD) and circles (Hough). Regions = pieces of the mask the
    edges separate; small pieces join their neighbour. Returns (labels, primitives) with primitives = {"lines","circles"}."""
    import cv2
    from scipy import ndimage as nd

    H, W = m.shape
    diag = float(np.hypot(H, W))
    g = cv2.cvtColor(np.ascontiguousarray(a), cv2.COLOR_RGB2GRAY)
    g = cv2.medianBlur(g, 5)
    g = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6, 6)).apply(g)  # dark parts have faint edges; stretch local contrast
    g = cv2.bilateralFilter(g, 7, 30, 7)
    inside = nd.binary_erosion(m, iterations=3)
    edges = cv2.Canny(g, 25, 70) > 0
    edges &= inside
    # keep only long, smooth edge pieces: cut the Canny network at junctions, keep pieces that are long and not squiggly
    nb = nd.convolve(edges.astype(int), np.ones((3, 3), int), mode="constant") - 1
    junction = edges & (nb > 2)
    pieces = edges & ~junction
    lab, n = nd.label(pieces, structure=np.ones((3, 3)))
    keep = np.zeros_like(edges)
    for k, sl in enumerate(nd.find_objects(lab), 1):
        npx = int((lab[sl] == k).sum())
        d = float(np.hypot(sl[0].stop - sl[0].start, sl[1].stop - sl[1].start))
        if npx >= min_len * diag and npx <= 1.7 * d:
            keep[sl] |= lab[sl] == k
    keep = nd.binary_dilation(keep, iterations=2) & edges | keep  # take the junction pixels the kept pieces touch
    B = keep.copy()
    lines, circles = [], []
    edge_near = nd.binary_dilation(cv2.Canny(g, 25, 70) > 0, iterations=2)
    try:
        lsd = cv2.createLineSegmentDetector(0)
        det = lsd.detect(g)[0]
        for x1, y1, x2, y2 in (det[:, 0, :] if det is not None else []):
            if np.hypot(x2 - x1, y2 - y1) >= 0.04 * diag:
                mid = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                if 0 <= mid[1] < H and 0 <= mid[0] < W and inside[mid[1], mid[0]]:
                    cv2.line(B.view(np.uint8), (int(x1), int(y1)), (int(x2), int(y2)), 1, 1)
                    lines.append([float(x1) / W, float(y1) / H, float(x2) / W, float(y2) / H])
    except Exception:
        pass
    c = cv2.HoughCircles(cv2.GaussianBlur(g, (5, 5), 1.5), cv2.HOUGH_GRADIENT, dp=1.2, minDist=max(8, int(0.02 * diag)),
                         param1=100, param2=30, minRadius=max(4, int(0.006 * diag)), maxRadius=int(0.06 * diag))
    if c is not None:
        for x, y, r in c[0][:max_circles]:
            xi, yi = int(x), int(y)
            if 0 <= yi < H and 0 <= xi < W and inside[yi, xi] and _ring_support(edge_near, x, y, r) >= 0.6:
                cv2.circle(B.view(np.uint8), (xi, yi), int(r), 1, 1)
                circles.append([float(x) / W, float(y) / H, float(r) / diag])
    from skimage.feature import peak_local_max
    from skimage.segmentation import watershed

    B = nd.binary_dilation(B, iterations=1) | ~m
    dist = nd.distance_transform_edt(~B)
    pk = peak_local_max(dist, min_distance=max(4, int(0.03 * diag)), threshold_abs=max(3.0, 0.008 * diag), exclude_border=False)
    mk = np.zeros(m.shape, int)
    for i, (y, x) in enumerate(pk, 1):
        mk[y, x] = i
    if not len(pk):
        return m.astype(int), {"lines": lines, "circles": circles}
    full = watershed(-dist, mk, mask=m)  # cells grow from interior peaks and meet on the ridges between edges
    # tiny cells join their biggest neighbour
    ids, cnt = np.unique(full[full > 0], return_counts=True)
    for i, c_ in zip(ids, cnt):
        if c_ < 0.0006 * m.sum():
            ring = nd.binary_dilation(full == i, iterations=2) & (full != i) & (full > 0)
            if ring.any():
                full[full == i] = np.bincount(full[ring]).argmax()
    return full, {"lines": lines, "circles": circles}


def load_regions(base: Path, photo: str):
    from PIL import Image

    p = base / "reference" / "segments" / (Path(photo).stem + ".regions.png")
    return np.asarray(Image.open(p)).astype(int) if p.exists() else None


def load_segments(path) -> dict:
    d = json.loads(Path(path).read_text())
    d.setdefault("segments", [])
    return d


def merged(d: dict) -> list:
    """Segments with the optional `merge` groups applied (big part = union of its small ones)."""
    segs = {s["id"]: s for s in d["segments"]}
    groups = d.get("merge") or {}
    used = {i for ids in groups.values() for i in ids}
    out = [s for s in d["segments"] if s["id"] not in used]
    for label, ids in groups.items():
        pts = [segs[i] for i in ids if i in segs]
        out.append({"id": "+".join(ids), "label": label, "kind": pts[0].get("kind", "") if pts else "",
                    "members": ids, "polygons": [p["polygon"] for p in pts]})
    return out


def grid(photo, out=None, step=0.1):
    from PIL import Image, ImageDraw

    im = Image.open(photo).convert("RGB")
    im.thumbnail((1000, 1000))
    W, H = im.size
    d = ImageDraw.Draw(im)
    n = int(round(1 / step))
    for k in range(n + 1):
        x, y = k * step * W, k * step * H
        d.line([(x, 0), (x, H)], fill=(255, 0, 255) if k % 5 == 0 else (255, 160, 255), width=1)
        d.line([(0, y), (W, y)], fill=(255, 0, 255) if k % 5 == 0 else (255, 160, 255), width=1)
        d.text((x + 2, 2), f"{k * step:.1f}", fill=(255, 0, 0))
        d.text((2, y + 2), f"{k * step:.1f}", fill=(255, 0, 0))
    out = out or str(Path(photo).with_suffix("")) + ".grid.png"
    im.save(out)
    return out


def check(segfile, write=True) -> dict:
    """Quality of a segment file vs the photo mask."""
    from PIL import Image, ImageDraw

    sf = Path(segfile)
    base = sf.parents[2]
    d = load_segments(sf)
    m, crop = photo_mask_for(base, d["photo"])
    H, W = m.shape
    segs, ms = raster_parts(d, base, m.shape, crop)
    segs = [dict(s) for s in segs]
    if d.get("parts"):  # region based: unassigned regions are the gaps
        lab = load_regions(base, d["photo"])
        used = {r for p_ in d["parts"] for r in p_["regions"]}
        left = [int(k) for k in np.unique(lab[lab > 0]) if int(k) not in used]
        dup = sorted(k for k in used if sum(k in p_["regions"] for p_ in d["parts"]) > 1)
    else:
        left, dup = [], []
    union = np.zeros_like(m)
    cnt = np.zeros(m.shape, int)
    for r in ms:
        union |= r
        cnt += r
    rep = {"photo": d["photo"], "segments": len(segs), "robot_px": int(m.sum()),
           "coverage": round(float((union & m).sum() / max(1, m.sum())), 3),
           "outside_frac": round(float((union & ~m).sum() / max(1, union.sum())), 3),
           "overlap_frac": round(float((cnt > 1).sum() / max(1, union.sum())), 3), "issues": []}
    for s, r in zip(segs, ms):
        a = int(r.sum())
        if a < 0.0001 * m.size:
            rep["issues"].append(f"{s['id']} {s['label']}: tiny ({a} px) or bad polygon")
        elif (r & m).sum() < 0.7 * a:
            rep["issues"].append(f"{s['id']} {s['label']}: {1 - (r & m).sum() / a:.0%} outside the robot mask")
    from scipy import ndimage as nd

    def boxes(mask, min_frac):
        lab, n = nd.label(mask)
        out = []
        for k, sl in enumerate(nd.find_objects(lab), 1):
            a = int((lab[sl] == k).sum())
            if a >= min_frac * m.sum():
                out.append({"x": [round(sl[1].start / W, 2), round(sl[1].stop / W, 2)],
                            "y": [round(sl[0].start / H, 2), round(sl[0].stop / H, 2)], "share_of_robot": round(a / m.sum(), 3)})
        return sorted(out, key=lambda b: -b["share_of_robot"])[:8]

    gaps = boxes(m & ~union, 0.004)
    if gaps:  # box coordinates are fractions of the CROPPED frame; without a crop they are fractions of the photo
        rep["uncovered_regions"] = gaps
    clash = {}
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            o = int((ms[i] & ms[j]).sum())
            if o > 0.15 * min(ms[i].sum(), ms[j].sum()) and o > 20:
                clash[f"{segs[i]['id']}~{segs[j]['id']}"] = round(float(o / max(1, min(ms[i].sum(), ms[j].sum()))), 2)
    if clash:
        rep["issues"].append(f"overlapping segments (share of the smaller one): {clash}")
    ids = [s["id"] for s in segs]
    if len(set(ids)) != len(ids):
        rep["issues"].append("duplicate segment ids")
    if rep["coverage"] < 0.9:
        rep["issues"].append(f"only {rep['coverage']:.0%} of the robot is covered, segment the rest")
    if left:
        rep["issues"].append(f"regions not in any part: {left}")
    if dup:
        rep["issues"].append(f"regions in more than one part: {dup}")
    if write:
        full = Image.open(Path(base) / "reference" / d["photo"]).convert("RGB")
        if crop:
            Wf, Hf = full.size
            full = full.crop((int(crop[0] * Wf), int(crop[1] * Hf), int(crop[2] * Wf), int(crop[3] * Hf)))
        full = full.resize((W, H))
        ov = np.asarray(full, float)
        for i, r in enumerate(ms):
            ov[r] = 0.45 * ov[r] + 0.55 * np.array(PALETTE[i % len(PALETTE)])
        img = Image.fromarray(ov.astype(np.uint8))
        dr = ImageDraw.Draw(img)
        for i, (s, r) in enumerate(zip(segs, ms)):
            if r.any():
                ys, xs = np.nonzero(r)
                dr.text((xs.mean() - 6, ys.mean() - 5), s["id"][1:] if s["id"].startswith("s") else s["id"], fill=(0, 0, 0))
        out = sf.with_name(sf.stem + ".parts.png")
        img.save(out)
        rep["overlay"] = str(out)
    return rep


# ---------------------------------------------------------------- model side
def camera_for(base: Path, photo: str):
    """(azimuth, elevation) of the camera: renders/view_match.json, else the likeness gate's best camera is not
    re-derived here (run `robot likeness` first)."""
    p = base / "renders" / "view_match.json"
    if p.exists():
        v = json.loads(p.read_text()).get(photo)
        if v:
            return float(v["azimuth"]), float(v["elevation"])
    return None


def id_buffer(world, az, el, px_mm=0.5):
    """Painter's-algorithm orthographic id buffer: (H, W) int (-1 background, else body index), and body ids."""
    from PIL import Image, ImageDraw

    a, e = np.radians(az), np.radians(el)
    d = np.array([-np.cos(e) * np.cos(a), -np.cos(e) * np.sin(a), -np.sin(e)])
    up = np.array([0, 0, 1.0])
    right = np.cross(d, up)
    right /= np.linalg.norm(right)
    u = np.cross(right, d)
    u /= np.linalg.norm(u)
    tris, ids = [], []
    bodies = [b for b in world.bodies if not getattr(b, "is_wire", False) and b.mesh is not None]
    for i, b in enumerate(bodies):
        t = b.mesh.triangles
        tris.append(t)
        ids.append(np.full(len(t), i))
    T = np.concatenate(tris)
    I = np.concatenate(ids)
    x, y, z = T @ right, T @ u, T @ d  # z grows away from the camera
    x0, y1 = x.min(), y.max()
    W = int(np.ceil((x.max() - x0) / px_mm)) + 4
    H = int(np.ceil((y1 - y.min()) / px_mm)) + 4
    X, Y = (x - x0) / px_mm + 2, (y1 - y) / px_mm + 2
    order = np.argsort(-z.mean(axis=1))  # far first
    img = Image.new("I", (W, H), 0)
    dr = ImageDraw.Draw(img)
    for k in order:
        dr.polygon([(X[k, 0], Y[k, 0]), (X[k, 1], Y[k, 1]), (X[k, 2], Y[k, 2])], fill=int(I[k]) + 1)
    return np.asarray(img).astype(int) - 1, [b.id for b in bodies]


def _frame(mask):
    ys, xs = np.nonzero(mask)
    return ys.min(), ys.max() + 1, xs.min(), xs.max() + 1


def _to_canvas(m, fr, scale, H, W):
    """Crop to the silhouette bbox `fr`, scale by `scale`, anchor bottom-left on an (H, W) canvas."""
    from PIL import Image

    y0, y1, x0, x1 = fr
    c = m[y0:y1, x0:x1]
    h, w = c.shape
    nh, nw = max(1, int(round(h * scale))), max(1, int(round(w * scale)))
    r = np.asarray(Image.fromarray(c.astype(np.uint8) * 255).resize((nw, nh), Image.NEAREST)) > 127
    out = np.zeros((H, W), bool)
    hh, ww = min(H, nh), min(W, nw)
    out[H - hh:, :ww] = r[:hh, :ww]
    return out


def _iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0


def score_photo(world, base: Path, segfile: Path, cam=None):
    d = load_segments(segfile)
    photo = d["photo"]
    cam = cam or camera_for(base, photo)
    if cam is None:
        raise SystemExit(f"no camera for {photo}: run `robot likeness` first (writes renders/view_match.json) or pass --az/--el")
    pm, crop = photo_mask_for(base, photo)
    if d.get("parts"):
        segs, rm = raster_parts(d, base, pm.shape, crop)
    else:
        segs = merged(d)
        rm = raster_segments([{"polygon": s.get("polygon", []), "holes": s.get("holes")} for s in segs], pm.shape, crop)
        for i, s in enumerate(segs):  # merged groups: union of member polygons
            if "polygons" in s:
                rm[i] = np.any(raster_segments([{"polygon": p} for p in s["polygons"]], pm.shape, crop), axis=0)
    ib, names = id_buffer(world, *cam)
    sil = ib >= 0
    from scipy import ndimage as nd
    sil = nd.binary_fill_holes(sil)
    fr_m, fr_p = _frame(sil), _frame(pm)
    # silhouette alignment identical to checks.reference.compare: same width, bottom-left anchored
    sm = CANVAS / (fr_m[3] - fr_m[2])
    sp = CANVAS / (fr_p[3] - fr_p[2])
    Hc = int(max((fr_m[1] - fr_m[0]) * sm, (fr_p[1] - fr_p[0]) * sp)) + 2
    mod_sil = _to_canvas(sil, fr_m, sm, Hc, CANVAS + 2)
    ref_sil = _to_canvas(pm, fr_p, sp, Hc, CANVAS + 2)
    parts = [_to_canvas(ib == i, fr_m, sm, Hc, CANVAS + 2) for i in range(len(names))]
    refs = [_to_canvas(r, fr_p, sp, Hc, CANVAS + 2) for r in rm]
    res = []
    used = set()
    for i in sorted(range(len(refs)), key=lambda k: -refs[k].sum()):  # big segments pick first
        best = (0.0, -1)
        for j, p in enumerate(parts):
            if not p.any():
                continue
            v = _iou(refs[i], p)
            if v > best[0]:
                best = (v, j)
        res.append({"id": segs[i]["id"], "label": segs[i].get("label", ""), "area": int(refs[i].sum()),
                    "best_part": names[best[1]] if best[1] >= 0 else None, "iou": round(best[0], 3)})
        if best[1] >= 0:
            used.add(best[1])
    # part-level view: unmatched visible model parts (extra)
    extra = [names[j] for j, p in enumerate(parts) if p.sum() > 40 and j not in used]
    tot = sum(r["area"] for r in res) or 1
    out = {"photo": photo, "camera": {"azimuth": cam[0], "elevation": cam[1]},
           "silhouette_iou": round(_iou(mod_sil, ref_sil), 3),
           "mean_iou": round(sum(r["iou"] for r in res) / max(1, len(res)), 3),
           "area_weighted_iou": round(sum(r["iou"] * r["area"] for r in res) / tot, 3),
           "f1_at_0.5": round(2 * sum(r["iou"] >= 0.5 for r in res) / max(1, len(res) + len([p for p in parts if p.sum() > 40])), 3),
           "segments": sorted(res, key=lambda r: r["iou"]), "unmatched_model_parts": extra}
    # pictures: model id map and compare (green = both, red = model only, blue = photo only)
    from PIL import Image

    cmp_ = np.full(mod_sil.shape + (3,), 255, np.uint8)
    cmp_[mod_sil & ~ref_sil] = (255, 80, 80)
    cmp_[ref_sil & ~mod_sil] = (80, 80, 255)
    cmp_[mod_sil & ref_sil] = (170, 220, 170)
    mp = np.full(mod_sil.shape + (3,), 255, np.uint8)
    for j, p in enumerate(parts):
        mp[p] = PALETTE[j % len(PALETTE)]
    Image.fromarray(cmp_).save(segfile.with_name(segfile.stem + ".compare.png"))
    Image.fromarray(mp).save(segfile.with_name(segfile.stem + ".model.png"))
    return out


def score(spec_path, az=None, el=None):
    from . import spec as spec_mod, world as world_mod

    s = spec_mod.load(spec_path)
    base = Path(getattr(s, "base_dir", None) or Path(spec_path).parent)
    r = world_mod.resolve(s, fast=True)
    w = world_mod.World.build(r)
    sd = base / "reference" / "segments"
    res = []
    for f in sorted(sd.glob("*.json")):
        if f.name == "score.json":
            continue
        try:
            res.append(score_photo(w, base, f, (az, el) if az is not None else None))
        except SystemExit as e:
            res.append({"photo": load_segments(f)["photo"], "error": str(e)})
    good = [x for x in res if "error" not in x]
    agg = {"photos": len(good), "area_weighted_iou": round(sum(x["area_weighted_iou"] for x in good) / max(1, len(good)), 3),
           "mean_iou": round(sum(x["mean_iou"] for x in good) / max(1, len(good)), 3)}
    (sd / "score.json").write_text(json.dumps({"aggregate": agg, "photos": res}, indent=1))
    return agg, res


def add_cli(sub):
    p = sub.add_parser("partseg", help="segment reference photos into parts (LLM drawn polygons) and score against the model")
    ps = p.add_subparsers(dest="pcmd", required=True)
    g = ps.add_parser("grid")
    g.add_argument("photo")
    g.add_argument("out", nargs="?")
    g.set_defaults(func=lambda a: print(grid(a.photo, a.out)) or 0)
    r = ps.add_parser("regions", help="exact-boundary numbered regions of the photo (then group them into parts)")
    r.add_argument("spec_dir", help="robot folder (robots/<name>)")
    r.add_argument("photo", help="photo file name in reference/")
    r.add_argument("--n", type=int, default=400)
    r.add_argument("--merge", type=float, default=14.0, help="slic only: colour distance below which neighbours merge")
    r.add_argument("--method", choices=("edges", "slic"), default="edges", help="edges = straight lines, circles and long smooth edges only (default)")
    r.set_defaults(func=lambda a: print(f"{regions(Path(a.spec_dir), a.photo, a.n, a.merge, method=a.method).max()} regions; view: {a.spec_dir}/reference/segments/{Path(a.photo).stem}.regions.view.png") or 0)
    f = ps.add_parser("fuse", help="round of brush polygons correcting the auto regions (split / carve), in place")
    f.add_argument("segfile")
    f.add_argument("--split-frac", type=float, default=0.15, help="a region is split along a big brush polygon covering this share of it")
    f.set_defaults(func=lambda a: print(json.dumps(fuse(a.segfile, split_frac=a.split_frac), indent=1)) or 0)
    c = ps.add_parser("check")
    c.add_argument("segfile")
    c.set_defaults(func=lambda a: print(json.dumps(check(a.segfile), indent=1)) or 0)
    s = ps.add_parser("score")
    s.add_argument("spec")
    s.add_argument("--az", type=float)
    s.add_argument("--el", type=float)

    def run(a):
        agg, res = score(a.spec, a.az, a.el)
        print(json.dumps({"aggregate": agg}, indent=1))
        for x in res:
            print(x.get("photo"), x.get("error") or f"sil {x['silhouette_iou']} area-weighted {x['area_weighted_iou']} mean {x['mean_iou']} F1@.5 {x['f1_at_0.5']}")
        return 0
    s.set_defaults(func=run)

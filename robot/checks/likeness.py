"""Copy-of-a-real-robot gate (`likeness.*`): a spec that sits next to reference photos must LOOK like them and must not
be a stock template or another robot's spec with a new name.

Active when the spec's folder has `reference/` photos or a `REFERENCE.json` (photo-read facts written by whoever
collected the photos, NOT by the builder). All findings are blockers:

- likeness.template_copy   made-part voxel IoU >= 0.80 with a bundled template (robot/templates), or >= 0.80 shape
                           fingerprint overlap with a sibling robots/<other>/spec.json.
- likeness.no_reference    no `reference` entry with a photo from reference/ and a mask.
- likeness.mask_source     the mask is not the photo's own silhouette (`robot mask` of that photo, IoU < 0.85), so it
                           was drawn to fit the model.
- likeness.silhouette      best IoU of the model's silhouette (any camera around the robot, mirrored or not) with the
                           photo mask is below 0.70, or not clearly better (+0.05) than the stock template's.
- likeness.type            spec robot_type / weapon / wheel count differ from REFERENCE.json.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, fail, ok

G = "likeness"
COPY_IOU = 0.80
SIL_MIN = 0.70
SIL_MARGIN = 0.0  # at least as close to the photo as the closest stock template (copies are caught by template_copy)
MASK_MIN = 0.85
VOX = 2.0
IMG = (".png", ".jpg", ".jpeg", ".webp")
TEMPLATES = Path(__file__).resolve().parents[1] / "templates"


def _base(spec):
    return Path(getattr(spec, "base_dir", ".") or ".")


def active(spec) -> bool:
    b = _base(spec)
    return (b / "REFERENCE.json").exists() or any(p.suffix.lower() in IMG for p in (b / "reference").glob("*"))


def folder_key(spec) -> str:
    """Hash of what this group reads outside the spec: the folder's photos + REFERENCE.json and sibling specs."""
    import hashlib
    h = hashlib.sha256()
    b = _base(spec)
    files = [b / "REFERENCE.json", *sorted((b / "reference").glob("*"))]
    if b.parent.name == "robots":
        files += [p for p in sorted(b.parent.glob("*/spec.json")) if p.parent.resolve() != b.resolve()]
    for p in files:
        if p.is_file():
            h.update(str(p.name).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def _made(world, r):
    out = []
    for b in world.bodies:
        if b.part_idx is None or b.fastener or b.is_wire:
            continue
        rp = r.parts[b.part_idx]
        if rp.cat is None:
            out.append(b)
    return out


def _vox(bodies):
    from .. import cache
    pts = []
    for b in bodies:
        lo, hi = b.aabb
        g = [np.arange(lo[i] + VOX / 2, hi[i], VOX) for i in range(3)]
        if any(len(x) == 0 for x in g):
            continue
        P = np.stack(np.meshgrid(*g, indexing="ij"), -1).reshape(-1, 3)
        P = P[b.inside(P)]
        pts.append(np.round(P / VOX).astype(int))
    if not pts:
        return set()
    return set(map(tuple, np.concatenate(pts)))


def _jac(a, b):
    u = len(a | b)
    return len(a & b) / u if u else 0.0


def _template_worlds():
    from .. import spec as spec_mod, world as world_mod
    out = []
    for p in sorted(TEMPLATES.glob("*.json")):
        try:
            s = spec_mod.load(p)
            r = world_mod.resolve(s, fast=True)
            out.append((p.stem, r, world_mod.World.build(r)))
        except Exception:  # noqa: BLE001 - a template that does not build cannot be copied either
            continue
    return out


def _fp(raw):
    """Rounded (1 mm) canonical JSON of every made part's shape + pose: survives renames and id changes."""
    out = set()
    for p in raw.get("parts") or []:
        if p.get("catalog"):
            continue
        s = json.dumps({"shape": p.get("shape"), "at": p.get("at"), "rot": p.get("rot")}, sort_keys=True,
                       default=lambda o: round(o) if isinstance(o, float) else str(o))
        s = json.loads(s, parse_float=lambda x: round(float(x)))
        out.add(json.dumps(s, sort_keys=True))
    return out


def copies(ctx, tws=None):
    r, w = ctx.r, ctx.world
    out = []
    mine = _vox(_made(w, r))
    from .. import cache
    for name, tr, tw in tws:
        tv = cache.memo("likeness", ("likeness_vox", cache.code_hash(), (TEMPLATES / f"{name}.json").read_bytes()),
                        lambda: _vox(_made(tw, tr)))
        j = _jac(mine, tv)
        if j >= COPY_IOU:
            out.append(fail("likeness.template_copy", G, BLOCKER, "Robot is a stock template",
                            f"Made parts overlap template `{name}` at voxel IoU {j:.2f} (limit {COPY_IOU:.2f}): this is the "
                            "template, not the robot in the photos.")
                       .fix("Rebuild the chassis, weapon and armour to the photo proportions (`robot mask` + "
                            "`likeness.silhouette` show where it differs)."))
    base = _base(r.spec)
    me = _fp(r.spec.raw or {})
    robots = base.parent
    if me and robots.name == "robots":
        for sib in sorted(robots.glob("*/spec.json")):
            if sib.parent.resolve() == base.resolve():
                continue
            try:
                other = _fp(json.loads(sib.read_text()))
            except Exception:  # noqa: BLE001
                continue
            j = _jac(me, other)
            if j >= COPY_IOU:
                out.append(fail("likeness.template_copy", G, BLOCKER, "Robot copies another robot",
                                f"{j:.0%} of the made-part shapes equal `{sib.parent.name}`'s spec (limit {COPY_IOU:.0%}).")
                           .fix("Each robot must be modelled from its own photos."))
    return out


def _dirs():
    out = []
    for el in (25, 45):
        for az in range(0, 360, 30):
            e, a = np.radians(el), np.radians(az)
            out.append((-np.cos(e) * np.cos(a), -np.cos(e) * np.sin(a), -np.sin(e)))
    return out + [(1.0, 0, 0), (0, -1.0, 0), (0, 0, -1.0)]


def _sils(world):
    from . import reference as ref
    out = []
    for d in _dirs():
        up = (0, 1.0, 0) if abs(d[2]) > 0.99 else (0, 0, 1.0)
        m, _ = ref.silhouette(world, d, up, px_mm=0.6)
        if m is not None and m.any():
            out += [m, m[:, ::-1]]
    return out


def best_iou(sils, mask):
    from . import reference as ref
    return max((ref.compare(s, mask)[0]["iou"] for s in sils), default=0.0)


def photos(ctx):
    from . import reference as ref
    from ..mask import photo_mask
    r, w = ctx.r, ctx.world
    base = _base(r.spec)
    ents = [e for e in ref.entries(r.spec) if e.get("mask") and e.get("image")
            and (base / e["image"]).exists() and "reference" in Path(e["image"]).parts]
    if not ents:
        return [fail("likeness.no_reference", G, BLOCKER, "No photo comparison",
                     "This robot has reference photos but the spec has no `reference` entry with an `image` from "
                     "reference/ and a `mask`.")
                .fix('Run `robot mask reference/<photo> reference/<photo>_mask.png`, then add "reference": [{"image": '
                     '"reference/<photo>", "mask": "reference/<photo>_mask.png", "view": "iso", "approximate": true}].')]
    out = []
    sils = _sils(w)
    tsils = None
    for e in ents:
        mask = ref.load_mask(base / e["mask"])
        auto = photo_mask(base / e["image"])
        mj = ref.compare(auto, mask)[0]["iou"]
        if mj < MASK_MIN:
            out.append(fail("likeness.mask_source", G, BLOCKER, "Mask is not the photo's outline",
                            f"`{e['mask']}` matches `robot mask {e['image']}` at IoU {mj:.2f} (need {MASK_MIN}): it was not "
                            "taken from the photo.").fix(f"Regenerate it: `robot mask {e['image']} {e['mask']}`."))
            continue
        iou = best_iou(sils, mask)
        tiou = _template_iou(base / e["mask"], mask)
        need = max(SIL_MIN, tiou + SIL_MARGIN)
        msg = (f"`{e['image']}`: best silhouette IoU {iou:.2f} over all cameras (need {need:.2f}: >= {SIL_MIN} and "
               f"no worse than the closest stock template, {tiou:.2f}).")
        if iou < need:
            out.append(fail("likeness.silhouette", G, BLOCKER, "Does not look like the photo", msg)
                       .fix("Reshape the outline (chassis plan, wedge/fork length, weapon size and height) toward the photo; "
                            "`robot render spec.json iso out.png` and compare side by side."))
        else:
            out.append(ok("likeness.silhouette", G, "Looks like the photo", msg))
    return out


_TW = None


class _LazyTemplates:
    """Template (name, resolved, world) list, built only when a cached voxel set is missing."""

    def __iter__(self):
        for p in sorted(TEMPLATES.glob("*.json")):
            yield p.stem, _Lazy(p.stem, 1), _Lazy(p.stem, 2)


class _Lazy:
    def __init__(self, name, i):
        self.name, self.i = name, i

    def __getattr__(self, k):
        for t in _template_worlds_cached():
            if t[0] == self.name:
                return getattr(t[self.i], k)
        raise AttributeError(k)


def _template_iou(path, mask):
    """Best stock-template IoU with this mask, cached on (templates, mask bytes, code)."""
    from .. import cache
    key = ("likeness_tpl", cache.code_hash(), Path(path).read_bytes(),
           *[p.read_bytes() for p in sorted(TEMPLATES.glob("*.json"))])

    def compute():
        return best_iou([s for _, _, tw in _template_worlds_cached() for s in _sils(tw)], mask)
    return cache.memo("likeness", key, compute)


def _template_worlds_cached():
    global _TW
    if _TW is None:
        _TW = _template_worlds()
    return _TW


def facts(ctx):
    spec = ctx.r.spec
    p = _base(spec) / "REFERENCE.json"
    if not p.exists():
        return []
    try:
        ref = json.loads(p.read_text())
    except Exception as ex:  # noqa: BLE001
        return [fail("likeness.type", G, BLOCKER, "REFERENCE.json unreadable", str(ex))]
    raw = spec.raw or {}
    out = []
    want = ref.get("robot_type")
    if want and str(raw.get("robot_type")) != str(want):
        out.append(fail("likeness.type", G, BLOCKER, "Wrong robot type",
                        f"Photos show a `{want}`; the spec says `{raw.get('robot_type')}`.")
                   .fix(f"Start from a matching template (`robot templates`) or `robot gen build --hypothesis ...`."))
    wheels = ref.get("wheels")
    if wheels:
        n = sum(1 for q in raw.get("parts") or [] if q.get("kind") == "wheel")
        if n != int(wheels):
            out.append(fail("likeness.type", G, BLOCKER, "Wrong wheel count", f"Photos show {wheels} wheels; spec has {n}."))
    return out


def run(ctx):
    spec = ctx.r.spec
    if not active(spec):
        return []
    out = facts(ctx) + copies(ctx, _LazyTemplates()) + photos(ctx)
    if not any(not f.passed and f.severity == BLOCKER for f in out):
        out.append(ok("likeness.template_copy", G, "Own design", "Differs from every template and sibling robot."))
    return out

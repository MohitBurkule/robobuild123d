"""Orthographic renders of the placed meshes (numpy z-buffer): fixed views, sections, failure markers.

Same views, camera framing, shading, outline and marker conventions as the Rust crate's render.rs, but the bodies are
rasterised triangle meshes (the cached build123d tessellation) instead of sphere-traced distance fields.
"""

from __future__ import annotations

import io
from dataclasses import dataclass

import numpy as np

from . import xform

VIEW_NAMES = ["iso", "exploded", "iso_back", "top", "bottom", "front", "back", "side", "section_z", "section_x"]


def with_section_z(view, h: float):
    """The view cut by the plane z = h, keeping everything below it (look down on the inside of a closed body)."""
    from dataclasses import replace

    return replace(view, name=f"{view.name}_z{h:g}", section=(np.array([0.0, 0, 1.0]), float(h)))


@dataclass
class View:
    name: str
    dir: np.ndarray  # camera looks along this
    up: np.ndarray
    section: tuple | None  # keep the half-space n . p <= d
    width: int
    explode: float


def render_scale() -> float:
    """ROBOT_RENDER_SCALE (default 1): 0.5 gives half-width proxy renders, about 4x fewer pixels."""
    import os

    try:
        return float(np.clip(float(os.environ.get("ROBOT_RENDER_SCALE") or 1.0), 0.1, 4.0))
    except ValueError:
        return 1.0


def named(name: str, width: int = 1100) -> View | None:
    z = (0.0, 0.0, 1.0)
    table = {
        "top": ((0, 0, -1), (0, 1, 0), None),
        "bottom": ((0, 0, 1), (0, -1, 0), None),
        "front": ((0, -1, 0), z, None),
        "back": ((0, 1, 0), z, None),
        "side": ((-1, 0, 0), z, None),
        "iso": ((-0.55, 0.75, -0.62), z, None),
        "exploded": ((-0.5, 0.78, -0.55), z, None),
        "iso_back": ((0.6, -0.7, -0.55), z, None),
        "section_z": ((0, 0, -1), (0, 1, 0), (np.array(z), 0.0)),
        "section_x": ((-1, 0, 0), z, (np.array([1.0, 0, 0]), 0.0)),
    }
    if name not in table:
        return None
    d, up, sec = table[name]
    width = max(64, int(round(width * render_scale())))
    return View(name, xform.norm(np.asarray(d, float)), np.asarray(up, float), sec, width,
                1.0 if name == "exploded" else 0.0)


@dataclass
class Marker:
    at: np.ndarray
    number: int


class _Cam:
    def __init__(self, lo, hi, v: View):
        d = xform.norm(v.dir)
        right = xform.norm(np.cross(d, v.up))
        up = xform.norm(np.cross(right, d))
        c = (lo + hi) / 2
        corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]) - c
        px, py = corners @ right, corners @ up
        pad = 6.0
        wmm, hmm = px.max() - px.min() + 2 * pad, py.max() - py.min() + 2 * pad
        self.w = max(int(v.width), 64)
        self.scale = wmm / self.w
        self.h = int(np.clip(np.ceil(hmm / self.scale), 32, 4000))
        self.center = c + right * (px.min() + px.max()) / 2 + up * (py.min() + py.max()) / 2
        self.right, self.up, self.dir = right, up, d

    def project(self, P):
        q = np.atleast_2d(P) - self.center
        return np.stack([self.w / 2 + q @ self.right / self.scale, self.h / 2 - q @ self.up / self.scale,
                         q @ self.dir], axis=1)


def _clip(mesh, section):
    if section is None:
        return mesh
    n, d = section
    if mesh.bounds is None:
        return None
    lo, hi = mesh.bounds
    far = np.where(n > 0, hi, lo) @ n  # largest n . p over the bounding box
    near = np.where(n > 0, lo, hi) @ n
    if far <= d:  # wholly kept: nothing to cut
        return mesh
    if near > d:  # wholly cut away
        return None
    try:
        m = mesh.slice_plane(n * d, -n, cap=True)
    except Exception:  # noqa: BLE001 - non-watertight pieces: cut without a cap
        try:
            m = mesh.slice_plane(n * d, -n, cap=False)
        except Exception:  # noqa: BLE001
            return None
    return m if m is not None and len(m.faces) else None


def _raster_one(k, tris, colors, zbuf, img, xa, xb, ya, yb, det):
    """One (large) triangle: dense barycentric test over its pixel box."""
    a, b, c = tris[k]
    d = det[k]
    X, Y = np.meshgrid(np.arange(xa[k], xb[k] + 1) + 0.5, np.arange(ya[k], yb[k] + 1) + 0.5)
    l1 = ((b[1] - c[1]) * (X - c[0]) + (c[0] - b[0]) * (Y - c[1])) / d
    l2 = ((c[1] - a[1]) * (X - c[0]) + (a[0] - c[0]) * (Y - c[1])) / d
    l3 = 1 - l1 - l2
    m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
    if not m.any():
        return
    z = l1 * a[2] + l2 * b[2] + l3 * c[2]
    sub = zbuf[ya[k]:yb[k] + 1, xa[k]:xb[k] + 1]
    upd = m & (z < sub)
    if upd.any():
        sub[upd] = z[upd]
        img[ya[k]:yb[k] + 1, xa[k]:xb[k] + 1][upd] = colors[k]


def _raster_block(k, w, h, tris, colors, zf, imf, W, xa, xb, ya, yb, det):
    """Many small triangles at once: (n, h, w) barycentric block, then one depth resolve per touched pixel
    (nearest wins; equal depth -> lowest triangle index, as in the sequential loop)."""
    def e(v):
        return v[:, None, None]

    A, B, C = tris[k, 0], tris[k, 1], tris[k, 2]
    PX = e(xa[k]) + np.arange(w)[None, None, :]
    PY = e(ya[k]) + np.arange(h)[None, :, None]
    X, Y = PX + 0.5, PY + 0.5
    d = e(det[k])
    l1 = (e(B[:, 1] - C[:, 1]) * (X - e(C[:, 0])) + e(C[:, 0] - B[:, 0]) * (Y - e(C[:, 1]))) / d
    l2 = (e(C[:, 1] - A[:, 1]) * (X - e(C[:, 0])) + e(A[:, 0] - C[:, 0]) * (Y - e(C[:, 1]))) / d
    l3 = 1 - l1 - l2
    m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6) & (PX <= e(xb[k])) & (PY <= e(yb[k]))
    if not m.any():
        return
    z = l1 * e(A[:, 2]) + l2 * e(B[:, 2]) + l3 * e(C[:, 2])
    ti, yi, xi = np.nonzero(m)
    tk = k[ti]
    pix = (ya[tk] + yi) * W + (xa[tk] + xi)
    zz = z[ti, yi, xi]
    o = np.lexsort((tk, zz, pix))
    pix, zz, tk = pix[o], zz[o], tk[o]
    first = np.ones(len(pix), bool)
    first[1:] = pix[1:] != pix[:-1]
    pix, zz, tk = pix[first], zz[first], tk[first]
    upd = zz < zf[pix]
    if upd.any():
        zf[pix[upd]] = zz[upd]
        imf[pix[upd]] = colors[tk[upd]]


def _raster(cam, tris, colors, zbuf, img):
    """Z-buffer rasterise screen-space triangles (N,3,3: x, y, depth) with flat colours (N,3).

    Small triangles (nearly all of a fine tessellation) are evaluated in numpy blocks grouped by pixel-box size;
    only the few large ones take the per-triangle path."""
    from . import _batch

    W, H = cam.w, cam.h
    if not len(tris):
        return
    xa = np.maximum(np.floor(tris[:, :, 0].min(1)).astype(np.int64), 0)
    xb = np.minimum(np.ceil(tris[:, :, 0].max(1)).astype(np.int64), W - 1)
    ya = np.maximum(np.floor(tris[:, :, 1].min(1)).astype(np.int64), 0)
    yb = np.minimum(np.ceil(tris[:, :, 1].max(1)).astype(np.int64), H - 1)
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    det = (b[:, 1] - c[:, 1]) * (a[:, 0] - c[:, 0]) + (c[:, 0] - b[:, 0]) * (a[:, 1] - c[:, 1])
    idx = np.nonzero((xb >= xa) & (yb >= ya) & (np.abs(det) >= 1e-12))[0]
    if not len(idx):
        return
    if not (zbuf.flags.c_contiguous and img.flags.c_contiguous):  # flat views below need contiguous buffers
        for k in idx:
            _raster_one(k, tris, colors, zbuf, img, xa, xb, ya, yb, det)
        return
    small, large = _batch.chunks(idx, (xb - xa + 1)[idx], (yb - ya + 1)[idx])
    zf, imf = zbuf.reshape(-1), img.reshape(-1, 3)
    for k, w, h in small:
        _raster_block(k, w, h, tris, colors, zf, imf, W, xa, xb, ya, yb, det)
    for k in large:
        _raster_one(k, tris, colors, zbuf, img, xa, xb, ya, yb, det)


def _background(cam, ground_z, view):
    W, H = cam.w, cam.h
    img = np.empty((H, W, 3), np.uint8)
    img[:] = (222, 222, 226)
    if ground_z is None or abs(cam.dir[2]) <= 0.2 or view.section is not None:
        return img
    xs = (np.arange(W) + 0.5 - W / 2) * cam.scale
    ys = (H / 2 - (np.arange(H) + 0.5)) * cam.scale
    U, V = np.meshgrid(xs, ys)
    O = cam.center + U[..., None] * cam.right + V[..., None] * cam.up
    t = (ground_z - O[..., 2]) / cam.dir[2]
    P = O + t[..., None] * cam.dir
    line = ((P[..., 0] / 10) % 1 < 0.04) | ((P[..., 1] / 10) % 1 < 0.04)
    fade = np.clip(1 - np.hypot(P[..., 0], P[..., 1]) / 220, 0, 1)
    v = np.where(line, 150.0, 188.0) * (0.7 + 0.3 * fade)
    g = np.stack([v, v, np.minimum(v * 1.03, 255)], -1).astype(np.uint8)
    img[t > 0] = g[t > 0]
    return img


_FONT = [[7, 5, 5, 5, 7], [2, 6, 2, 2, 7], [7, 1, 7, 4, 7], [7, 1, 7, 1, 7], [5, 5, 7, 1, 1],
         [7, 4, 7, 1, 7], [7, 4, 7, 5, 7], [7, 1, 2, 2, 2], [7, 5, 7, 5, 7], [7, 5, 7, 1, 7]]
RED = (235, 40, 40)


def _put(img, x, y, c):
    if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
        img[y, x] = c


def _ring(img, cx, cy, r):
    n = int(r * 14)
    for i in range(n):
        a = i / n * 2 * np.pi
        for dr in (-1, 0, 1):
            _put(img, int(round(cx + (r + dr) * np.cos(a))), int(round(cy + (r + dr) * np.sin(a))), RED)


def _digits(img, x0, y0, n):
    s = 3
    for ci, ch in enumerate(str(n)):
        for ry, row in enumerate(_FONT[int(ch)]):
            for rx in range(3):
                if row >> (2 - rx) & 1:
                    for sy in range(s):
                        for sx in range(s):
                            _put(img, int(x0) + (ci * 4 + rx) * s + sx, int(y0) + ry * s + sy, RED)


def _closed(b) -> bool:
    """Watertight, consistently wound part mesh (memoised on the shared part geometry)."""
    g = getattr(b, "geom", None)
    src = g.mesh if g is not None and hasattr(g, "mesh") else b.mesh
    v = getattr(g, "_closed", None) if g is not None else None
    if v is None:
        try:
            v = bool(src.is_watertight and src.is_winding_consistent and src.volume > 0)
        except Exception:  # noqa: BLE001
            v = False
        if g is not None:
            try:
                g._closed = v
            except Exception:  # noqa: BLE001
                pass
    if not v:
        return False
    return float(np.linalg.det(np.asarray(b.M, float)[:3, :3])) > 0 if hasattr(b, "M") else False


def render_views(world, views, ground_z=None, markers=(), workers: int | None = None) -> list:
    """PNG bytes for several views of one world, rendered in threads (numpy releases the GIL in the heavy steps).
    Placed meshes are materialised once up front so the threads share them."""
    import os
    from concurrent.futures import ThreadPoolExecutor

    views = list(views)
    for b in world.bodies:
        b.mesh  # noqa: B018 - fill the lazy placed-mesh cache before the threads start
    n = workers or int(os.environ.get("ROBOT_RENDER_JOBS") or min(4, os.cpu_count() or 1))
    if n <= 1 or len(views) <= 1:
        return [render_png(world, v, ground_z, markers) for v in views]
    with ThreadPoolExecutor(n) as ex:
        return list(ex.map(lambda v: render_png(world, v, ground_z, markers), views))


def render_array(world, view: View, ground_z=None, markers=()) -> np.ndarray | None:
    """Render `view` of the world to an (H, W, 3) uint8 array, or None for an empty world."""
    if view.explode > 0:
        world = world.exploded(view.explode)
    if not world.bodies:
        return None
    lo, hi = world.bounds()
    lo, hi = lo - 1.0, hi + 1.0
    cam = _Cam(lo, hi, view)
    img = _background(cam, ground_z, view)
    zbuf = np.full((cam.h, cam.w), np.inf)
    light = xform.norm(np.array([-0.4, 0.5, 0.8]))
    for b in world.bodies:
        m = _clip(b.mesh, view.section)
        if m is None:
            continue
        T = m.triangles
        N = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
        ln = np.linalg.norm(N, axis=1)
        ok = ln > 1e-12
        T, N = T[ok], N[ok] / ln[ok, None]
        facing = N @ cam.dir
        if m is b.mesh and _closed(b):  # closed and uncut: faces pointing away are always hidden by nearer ones
            front = facing <= 0
            T, N, facing = T[front], N[front], facing[front]
        N = np.where((facing > 0)[:, None], -N, N)  # two-sided (caps and open meshes)
        lam = np.clip(N @ light, 0, None)
        rim = (1 - np.clip(-(N @ cam.dir), 0, 1)) ** 2 * 0.25
        k = 0.5 + 0.55 * lam - rim * 0.25
        base = np.asarray(b.color or [200, 200, 200], float)
        cols = np.clip(base[None, :] * k[:, None], 0, 255).astype(np.uint8)
        S = cam.project(T.reshape(-1, 3)).reshape(-1, 3, 3)
        _raster(cam, S, cols, zbuf, img)
    # Dark outlines where luminance or depth jumps.
    L = img.astype(float) @ np.array([0.3, 0.59, 0.11])
    e = np.zeros_like(L)
    e[:-1, :-1] = np.maximum(abs(L[:-1, :-1] - L[:-1, 1:]), abs(L[:-1, :-1] - L[1:, :-1]))
    zf = np.where(np.isfinite(zbuf), zbuf, 1e6)
    dz = np.zeros_like(L)
    dz[:-1, :-1] = np.maximum(abs(zf[:-1, :-1] - zf[:-1, 1:]), abs(zf[:-1, :-1] - zf[1:, :-1]))
    edge = (e > 38) | (dz > 3 * cam.scale + 1.5)
    edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = False
    img[edge] = img[edge] // 2 + 8
    for mk in markers:
        p = cam.project(np.asarray(mk.at, float))[0]
        _ring(img, p[0], p[1], 10.0)
        _digits(img, p[0] + 12, p[1] - 12, mk.number)
    return img


def png_bytes(img: np.ndarray | None) -> bytes:
    if img is None:
        return b""
    from PIL import Image

    out = io.BytesIO()
    Image.fromarray(img, "RGB").save(out, format="PNG")
    return out.getvalue()


def scene_hash(world, view: View, ground_z=None, markers=()) -> str:
    from . import _batch, cache

    bodies = [(b.id, cache.body_sig(b), repr(b.color)) for b in world.bodies]
    mk = [(np.asarray(m.at, float) if hasattr(m, "at") else repr(m), repr(m)) for m in markers]
    return cache.h("render", cache.source_hash(__file__, _batch.__file__), bodies, repr(view), ground_z, mk)


def render_png(world, view: View, ground_z=None, markers=()) -> bytes:
    """PNG of a view; whole renders are cached by scene hash (part meshes come from the geometry cache)."""
    from . import cache

    return cache.memo("render", (scene_hash(world, view, ground_z, markers),),
                      lambda: png_bytes(render_array(world, view, ground_z, markers)))


def failure_markers(rep) -> list:
    """Numbered markers for every failed finding that has a position (numbering = order in the report)."""
    out, n = [], 0
    for f in rep.findings:
        if f.passed:
            continue
        n += 1
        if f.at is not None:
            out.append(Marker(np.asarray(f.at, float), n))
    return out


def axle_sections(world, r, width: int = 1100) -> list:
    """Section views through each spinning weapon's axle: `section_axle_x` (cut across the axle, at the weapon centre)
    and `section_axle_y` (cut along the axle, front-back through it). Empty when there is no spinning weapon."""
    from .checks.power import spin_axis

    out = []
    for i, b in enumerate(world.bodies):
        if b.part_idx is None or r.parts[b.part_idx].part.kind != "weapon":
            continue
        sa = spin_axis(world, r, i)
        if sa is None:
            continue
        o = sa[0]
        sfx = "" if not out else f"_{b.id}"
        z = np.array([0.0, 0, 1.0])
        out.append(View(f"section_axle_x{sfx}", np.array([-1.0, 0, 0]), z, (np.array([1.0, 0, 0]), float(o[0])), width, 0.0))
        out.append(View(f"section_axle_y{sfx}", np.array([0.0, -1.0, 0]), z, (np.array([0.0, 1.0, 0]), float(o[1])), width, 0.0))
    return out


def world_for(spec, opts=None):
    """Verify, then build the start-pose world with wire routes and the assembly plan. Returns (world, report, resolved)."""
    from . import checks, world as world_mod

    opts = opts or checks.Options()
    r = world_mod.resolve(spec, fast=opts.fast)
    rep = checks.verify_resolved(r, opts)
    w = world_mod.World.start(r).with_routes(rep.routes).with_assembly(rep.assembly)
    return w, rep, r


LID_WORDS = ("lid", "cover", "top_panel", "top_plate")


def _is_lid(p: dict) -> bool:
    tags = p.get("tags") or []
    tags = [tags] if isinstance(tags, str) else list(tags)
    words = [str(p.get(k) or "").lower() for k in ("id", "name", "role")] + [str(t).lower() for t in tags]
    return any(w in t for w in LID_WORDS for t in words)


def lid_ids(spec) -> set:
    """Ids of the lid/cover parts (id, name, role or tags naming a lid, cover or top panel) plus every fastener
    that passes through or threads into one of them - what a lid-off view must leave out."""
    raw = spec.raw if hasattr(spec, "raw") else spec
    lids = {p["id"] for p in raw.get("parts") or [] if _is_lid(p)}
    out = set(lids)
    for f in raw.get("fasteners") or []:
        touched = set(f.get("through") or []) | {f.get("threads_into")}
        if touched & lids or _is_lid(f):
            out.add(f.get("id"))
    return out


def without_lid(world, spec):
    """The world with the lid/cover parts and their bolts removed (for `render --no-lid`)."""
    from .world import World

    drop = lid_ids(spec)
    w = World([b for b in world.bodies if b.id not in drop], world.joints)
    w.plan = getattr(world, "plan", {})
    return w


# material palette for presentation renders: light, distinct colours per material family
MATERIAL_COLORS = {
    "pla": "#6b7078", "petg": "#6b7078", "nylon": "#7a7f87", "cf": "#5c6067",
    "tpu": "#ff8a2a", "titanium": "#c9cdd3", "aluminium": "#d4d8dd", "aluminum": "#d4d8dd", "steel": "#b9bec5",
    "hardox": "#e2e5e9", "brass": "#d8b45a", "rubber": "#3e4146",
}
STRUCTURE_COLOR = "#5a5e66"  # tub/base: dark grey, still readable


def _material_color(mat):
    from .world import parse_color

    m = str(mat or "").lower()
    for k, c in MATERIAL_COLORS.items():
        if k in m:
            return parse_color(c)
    return None


def material_palette(world, spec):
    """Recolour bodies by material (metal silver, TPU orange, printed structure dark grey); bodies with no
    known material keep their colour, lifted if it is near black."""
    from .world import World

    raw = spec.raw if hasattr(spec, "raw") else spec
    mats = {p["id"]: p.get("material") for p in raw.get("parts") or []}
    kinds = {p["id"]: p.get("kind") for p in raw.get("parts") or []}
    fmat = {f.get("id"): f.get("material") or "steel" for f in raw.get("fasteners") or []}
    out = []
    for b in world.bodies:
        c = _material_color(mats.get(b.id) or fmat.get(b.id))
        if c is not None and kinds.get(b.id) == "structure":
            c = _material_color("pla") if "pla" in str(mats.get(b.id)) else c
            if b.id in ("tub", "base_panel"):
                from .world import parse_color
                c = parse_color(STRUCTURE_COLOR)
        if c is None:
            c = list(b.color or [200, 200, 200])
            if sum(c) < 180:
                c = [min(255, int(v * 1.6) + 40) for v in c]
        nb = b.placed(b.M)
        nb.color = c
        out.append(nb)
    w = World(out, world.joints)
    w.plan = getattr(world, "plan", {})
    return w


def _ground(spec, world):
    if spec.ground_z is not None:
        return float(spec.ground_z)
    try:
        return float(world.bounds(skip_wires=True)[0][2])
    except Exception:  # noqa: BLE001
        return None


def cli(a):
    from pathlib import Path

    from . import checks, spec as spec_mod

    view = named(a.view, a.width)
    if view is None:
        print(f"unknown view {a.view}; views: {', '.join(VIEW_NAMES)}")
        return 1
    if getattr(a, "section_z", None) is not None:
        view = with_section_z(view, a.section_z)
    s = spec_mod.load(a.spec)
    if getattr(a, "no_checks", False):  # no full verify: only the wiring group, so wire routes are still drawn and recorded
        w, rep, _ = world_for(s, checks.Options(deep=True, fast=a.fast, only=["wiring"]))
        rep.findings = []
    else:
        w, rep, _ = world_for(s, checks.Options(deep=not a.quick, fast=a.fast))
    if a.no_lid:
        w = without_lid(w, s)
    if a.palette == "material":
        w = material_palette(w, s)
    marks = failure_markers(rep) if a.markers else []
    if a.markers:
        for i, f in enumerate([f for f in rep.findings if not f.passed], 1):
            print(f"{i}: {f.id} - {f.message}")
    Path(a.out).write_bytes(render_png(w, view, _ground(s, w), marks))
    write_record(a.out, a.spec, w, getattr(rep, "routes", None) or [])
    print(f"wrote {a.out}")
    return 0


def write_record(out, spec_path, w, routes):
    """Sidecar `<png>.json`: what the render shows (bodies, wire endpoints), read by wire.render_present."""
    import json
    import time
    from pathlib import Path

    rec = {"spec": str(Path(spec_path).resolve()), "rendered_at": time.time(),
           "bodies": [b.id for b in w.bodies if not b.is_wire],
           "wires": {rt.id: {"from": [float(v) for v in rt.points[0]], "to": [float(v) for v in rt.points[-1]]}
                     for rt in routes if len(rt.points) >= 2}}
    try:
        Path(str(out) + ".json").write_text(json.dumps(rec, indent=1))
    except OSError:
        pass


def add_cli(sub):
    p = sub.add_parser("render", help="render one view of a spec to PNG")
    p.add_argument("spec")
    p.add_argument("view", help=", ".join(VIEW_NAMES))
    p.add_argument("out")
    p.add_argument("--markers", action="store_true", help="numbered red rings on failures that have a position")
    p.add_argument("--width", type=int, default=1100)
    p.add_argument("--fast", action="store_true")
    p.add_argument("--quick", action="store_true", help="skip slow sweeps (no wire routes drawn)")
    p.add_argument("--palette", choices=("material", "spec"), default="material",
                   help="material: light per-material colours (default); spec: colours as written in the spec")
    p.add_argument("--section-z", type=float, default=None, metavar="H",
                   help="cut the view at height H and keep what is below (e.g. top view under a closed deck)")
    p.add_argument("--no-checks", action="store_true",
                   help="skip the full verify pass (much faster and lighter; wire routes are still computed and drawn, no markers)")
    p.add_argument("--no-lid", action="store_true", help="leave out lid/cover/top-panel parts and their bolts")
    p.set_defaults(func=cli)

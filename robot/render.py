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


@dataclass
class View:
    name: str
    dir: np.ndarray  # camera looks along this
    up: np.ndarray
    section: tuple | None  # keep the half-space n . p <= d
    width: int
    explode: float


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
    try:
        m = mesh.slice_plane(n * d, -n, cap=True)
    except Exception:  # noqa: BLE001 - non-watertight pieces: cut without a cap
        try:
            m = mesh.slice_plane(n * d, -n, cap=False)
        except Exception:  # noqa: BLE001
            return None
    return m if m is not None and len(m.faces) else None


def _raster(cam, tris, colors, zbuf, img):
    """Z-buffer rasterise screen-space triangles (N,3,3: x, y, depth) with flat colours (N,3)."""
    W, H = cam.w, cam.h
    x0 = np.floor(tris[:, :, 0].min(1)).astype(int)
    x1 = np.ceil(tris[:, :, 0].max(1)).astype(int)
    y0 = np.floor(tris[:, :, 1].min(1)).astype(int)
    y1 = np.ceil(tris[:, :, 1].max(1)).astype(int)
    keep = (x1 >= 0) & (y1 >= 0) & (x0 < W) & (y0 < H)
    for k in np.nonzero(keep)[0]:
        a, b, c = tris[k]
        xa, xb = max(x0[k], 0), min(x1[k], W - 1)
        ya, yb = max(y0[k], 0), min(y1[k], H - 1)
        if xb < xa or yb < ya:
            continue
        det = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(det) < 1e-12:
            continue
        X, Y = np.meshgrid(np.arange(xa, xb + 1) + 0.5, np.arange(ya, yb + 1) + 0.5)
        l1 = ((b[1] - c[1]) * (X - c[0]) + (c[0] - b[0]) * (Y - c[1])) / det
        l2 = ((c[1] - a[1]) * (X - c[0]) + (a[0] - c[0]) * (Y - c[1])) / det
        l3 = 1 - l1 - l2
        m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
        if not m.any():
            continue
        z = l1 * a[2] + l2 * b[2] + l3 * c[2]
        sub = zbuf[ya:yb + 1, xa:xb + 1]
        upd = m & (z < sub)
        if upd.any():
            sub[upd] = z[upd]
            img[ya:yb + 1, xa:xb + 1][upd] = colors[k]


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
        N = np.where((facing > 0)[:, None], -N, N)  # two-sided (caps and open meshes)
        lam = np.clip(N @ light, 0, None)
        rim = (1 - np.clip(-(N @ cam.dir), 0, 1)) ** 2 * 0.25
        k = 0.32 + 0.68 * lam - rim * 0.3
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


def render_png(world, view: View, ground_z=None, markers=()) -> bytes:
    return png_bytes(render_array(world, view, ground_z, markers))


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
    s = spec_mod.load(a.spec)
    w, rep, _ = world_for(s, checks.Options(deep=not a.quick, fast=a.fast))
    marks = failure_markers(rep) if a.markers else []
    if a.markers:
        for i, f in enumerate([f for f in rep.findings if not f.passed], 1):
            print(f"{i}: {f.id} - {f.message}")
    Path(a.out).write_bytes(render_png(w, view, _ground(s, w), marks))
    print(f"wrote {a.out}")
    return 0


def add_cli(sub):
    p = sub.add_parser("render", help="render one view of a spec to PNG")
    p.add_argument("spec")
    p.add_argument("view", help=", ".join(VIEW_NAMES))
    p.add_argument("out")
    p.add_argument("--markers", action="store_true", help="numbered red rings on failures that have a position")
    p.add_argument("--width", type=int, default=1100)
    p.add_argument("--fast", action="store_true")
    p.add_argument("--quick", action="store_true", help="skip slow sweeps (no wire routes drawn)")
    p.set_defaults(func=cli)

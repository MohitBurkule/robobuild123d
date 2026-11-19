"""Outline details the reference photo shows, on one static printed part, without breaking the inside.

`robot outline SPEC PART --edge EDGE (--chamfer A [B] | --step A [B]) [--span LO,HI] [--wall MM] [--force] [--dry]`
    EDGE names two faces of the part's box, e.g. `+y+z` (front-top edge), `+y+x` (front-right vertical edge, a plan
    taper), `-y+z` (rear-top). A is measured along the first face (from the edge, inward along the second face's
    normal), B along the second face (default B = A):
      `--edge +y+z --chamfer 6 10` -> the front face loses its top 6 mm, the top face its front 10 mm, on a straight bevel;
      `--edge +y+z --step 6 10`    -> a 6 mm deep, 10 mm long rectangular notch on that edge (a stepped deck or nose);
      `--chamfer 8 20` on both `--edge +y+x` and `--edge=+y-x` tapers the front in plan.
    --span limits the cut along the edge (world mm), e.g. `--span=-20,20` for a centre-only step. A corner of the part's
    box that is already empty (a rounded or bevelled part) removes nothing: the command says so.
    If the part is hollow, a `--wall` (default 1.6 mm) skin is kept behind the new face (the cut is grown by the wall
    and refilled inside the part's outer solid), so the cavity never opens. Refuses, and says why, when the cut or the
    new skin would touch another part (a wheel, motor, the battery...) unless --force (only for the cut, never the skin).

`robot window SPEC PART --over COMPONENT [--face +z] [--lip 2] [--dry]`
    A see-through opening in PART's wall right over an internal component (battery, ESC, receiver, PCB), where the
    photo shows electronics through an open top or side. The opening is the component's footprint shrunk by `--lip`
    on every side, so the component stays captive behind the rim. Refuses when anything but PART, the component and
    wires lies between the outside and the component.

Both write the cut into PART's shape (a `subtract`), print what they did and the removed volume. Re-run verify and the
likeness gate afterwards: an outline change must raise the photo IoU, not lower it.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

AX = {"x": 0, "y": 1, "z": 2}
E = 3.0   # how far each cut runs past the part's box


def _faces(edge):
    a, b = edge[:2], edge[2:4]
    out = []
    for f in (a, b):
        s = -1.0 if f[0] == "-" else 1.0
        out.append((AX[f[1]], s))
    if out[0][0] == out[1][0]:
        raise SystemExit(f"edge {edge}: the two faces must be on different axes")
    return out


def _euler_for(R):
    from . import xform
    for r in itertools.product((0, 90, 180, 270), repeat=3):
        if np.allclose(xform.euler(r), R, atol=1e-6):
            return [float(x) for x in r]
    raise SystemExit("only axis-aligned parts are supported")


def _frame(i1, i2):
    """Rotation whose local x, y, z are world axes i1, i2 and the remaining one (right-handed)."""
    e = np.eye(3)
    x, y = e[i1], e[i2]
    return np.column_stack([x, y, np.cross(x, y)])


def _local_place(p, shape, R_w, at_w):
    from . import xform
    Rp = xform.euler(p.get("rot", [0, 0, 0]))
    at_l = Rp.T @ (np.asarray(at_w, float) - np.asarray(p.get("at", [0, 0, 0]), float))
    return {"type": "place", "shape": shape, "at": [round(float(v), 3) for v in at_l], "rot": _euler_for(Rp.T @ R_w)}


def _polygon(kind, c1, c2, s1, s2, A, B):
    """2-D cut region in (axis1, axis2) world coordinates for a corner at (c1, c2) pointing outward (s1, s2)."""
    if kind == "step":
        return [(c1 - s1 * B, c2 - s2 * A), (c1 + s1 * E, c2 - s2 * A), (c1 + s1 * E, c2 + s2 * E), (c1 - s1 * B, c2 + s2 * E)]
    k = E / max(A, B)
    p0 = (c1 + s1 * B * k, c2 - s2 * A * (1 + k))          # on the bevel line, past the face
    p1 = (c1 - s1 * B * (1 + k), c2 + s2 * A * k)
    return [p0, (c1 + s1 * (B * k + E), c2 + s2 * (A * k + E)), p1]


def _inside_poly(P2, poly):
    from matplotlib.path import Path as MPath
    return MPath(np.asarray(poly)).contains_points(P2)


def _prism(poly, i1, i2, lo3, hi3):
    """(shape, R, at) of a prism with the 2-D region `poly` in the world (i1, i2) plane spanning lo3..hi3 on the third
    axis: local x, y are world i1, i2 (so the points stay in world coordinates) and local z runs along the third axis."""
    R = _frame(i1, i2)
    at = np.zeros(3)
    at[3 - i1 - i2] = (lo3 + hi3) / 2
    pts = [[round(float(u), 3), round(float(v), 3)] for u, v in poly]
    return {"type": "prism", "points": pts, "height": round(float(hi3 - lo3), 3)}, R, at


def _base_solid(shape):
    """The part's outer solid before its cavities and pockets (through subtract bases and first union items)."""
    while shape.get("type") in ("subtract", "union"):
        shape = shape["base"] if shape["type"] == "subtract" else shape["items"][0]
    return shape


def _add_cut(p, item):
    sh = p["shape"]
    if sh.get("type") == "subtract":
        sh.setdefault("cut", []).append(item)
    else:
        p["shape"] = {"type": "subtract", "base": sh, "cut": [item]}


def _load(path, part):
    from . import spec as spec_mod
    from . import world as world_mod
    raw = json.loads(Path(path).read_text())
    byid = {p["id"]: p for p in raw["parts"]}
    if part not in byid:
        raise SystemExit(f"no part {part}")
    P = byid[part]
    if "catalog" in P or "shape" not in P or P.get("joint") or P.get("parent") or P.get("rotates_with"):
        raise SystemExit(f"{part} must be a static printed part with a shape")
    w = world_mod.World.build(world_mod.resolve(spec_mod.load(path), fast=True))
    return raw, byid, P, {b.id: b for b in w.bodies}


def _inside_box(G, lo, hi):
    return np.all((G > lo + 0.2) & (G < hi - 0.2), axis=1)


def _grid(lo, hi, h):
    ax = [np.arange(lo[k] + h / 2, hi[k], h) for k in range(3)]
    return np.stack(np.meshgrid(*ax, indexing="ij"), -1).reshape(-1, 3)


def outline(path, part, kind, edge, A, B=None, span=None, wall=1.6, force=False, dry=False):
    raw, byid, P, Bd = _load(path, part)
    B = A if B is None else B
    (i1, s1), (i2, s2) = _faces(edge)
    i3 = 3 - i1 - i2
    lo, hi = Bd[part].aabb
    c1 = hi[i1] if s1 > 0 else lo[i1]
    c2 = hi[i2] if s2 > 0 else lo[i2]
    lo3, hi3 = (lo[i3] - E, hi[i3] + E) if not span else tuple(float(x) for x in span.split(","))
    poly = _polygon(kind, c1, c2, s1, s2, A, B)
    # sample the cut region and the new skin behind it
    G = _grid(np.minimum(lo, hi) - 0.5, np.maximum(lo, hi) + 0.5, 0.7)
    G = G[(G[:, i3] >= lo3) & (G[:, i3] <= hi3)]
    incut = _inside_poly(G[:, [i1, i2]], poly)
    # skin: points within `wall` of the cut region (2-D distance by dilating the polygon test on offsets)
    near = np.zeros(len(G), bool)
    for du, dv in itertools.product(np.linspace(-wall, wall, 5), repeat=2):
        if du * du + dv * dv <= wall * wall + 1e-9:
            near |= _inside_poly(G[:, [i1, i2]] + np.array([du, dv]), poly)
    skin = near & ~incut
    mine = Bd[part].inside(G)
    removed = int((incut & mine).sum())
    if removed == 0:
        raise SystemExit(f"{edge} {kind} {A}x{B}: removes nothing from {part}")
    others = [b for i, b in Bd.items() if i != part and not getattr(b, "is_wire", False)
              and byid.get(i, {}).get("fused_with") != part]
    hit_cut = sorted({b.id for b in others if b.inside(G[incut]).any()})
    hit_skin = sorted({b.id for b in others if b.inside(G[skin]).any()})
    if hit_cut and not force:
        raise SystemExit(f"{edge} {kind}: the cut would leave {hit_cut} standing proud or cut into them (use --force only for decorative overlaps)")
    hollow = bool((skin & ~mine & _inside_box(G, lo, hi)).any())   # air behind the new face inside the part's box: a cavity
    if hit_skin:
        raise SystemExit(f"{edge} {kind}: the {wall:g} mm skin kept behind the new face would run into {hit_skin}")
    shape, R, at = _prism(poly, i1, i2, lo3, hi3)
    cut = _local_place(P, shape, R, at)
    vol = removed * 0.7 ** 3
    if dry:
        print(f"{part}: {kind} {edge} {A:g}x{B:g} would remove ~{vol:.0f} mm3" + (" and keep a skin behind it" if hollow else ""))
        return 0
    if hollow:
        grown = _polygon(kind, c1, c2, s1, s2, A + wall * 1.5, B + wall * 1.5)
        gshape, _, _ = _prism(grown, i1, i2, lo3, hi3)
        outer = _base_solid(P["shape"])
        skin_shape = {"type": "intersect", "items": [outer, {"type": "subtract", "base": _local_place(P, gshape, R, at), "cut": [cut]}]}
        _add_cut(P, cut)
        P["shape"] = {"type": "union", "items": [P["shape"], skin_shape]}
    else:
        _add_cut(P, cut)
    Path(path).write_text(json.dumps(raw, indent=1))
    print(f"{part}: {kind} {edge} {A:g}x{B:g}, ~{vol:.0f} mm3 removed" + (f", {wall:g} mm skin kept behind it" if hollow else ""))
    return 0


def window(path, part, over, face="+z", lip=2.0, dry=False):
    raw, _, P, Bd = _load(path, part)
    if over not in Bd:
        raise SystemExit(f"no body {over}")
    k = AX[face[1]]
    s = -1.0 if face[0] == "-" else 1.0
    clo, chi = Bd[over].aabb
    plo, phi = Bd[part].aabb
    lo, hi = clo.copy(), chi.copy()
    for j in range(3):
        if j != k:
            lo[j] += lip
            hi[j] -= lip
    if np.any(hi - lo <= 1.0):
        raise SystemExit(f"{over} is too small for a {lip:g} mm rim")
    if s > 0:
        lo[k], hi[k] = chi[k] + 0.3, phi[k] + E
    else:
        lo[k], hi[k] = plo[k] - E, clo[k] - 0.3
    G = _grid(lo, hi, 0.7)
    others = [b for i, b in Bd.items() if i not in (part, over) and not getattr(b, "is_wire", False) and not getattr(b, "fastener", False)]
    hit = sorted({b.id for b in others if b.inside(G).any()})
    if hit:
        raise SystemExit(f"window over {over}: {hit} lie between it and the outside")
    removed = int(Bd[part].inside(G).sum())
    if removed == 0:
        raise SystemExit(f"window over {over}: {part} has no wall there")
    area = float(np.prod([hi[j] - lo[j] for j in range(3) if j != k]))
    box = {"type": "box", "size": [round(float(v), 3) for v in hi - lo]}
    cut = _local_place(P, box, np.eye(3), (lo + hi) / 2)
    if dry:
        print(f"{part}: window over {over} on {face}, {area:.0f} mm2 opening, rim {lip:g} mm")
        return 0
    _add_cut(P, cut)
    Path(path).write_text(json.dumps(raw, indent=1))
    print(f"{part}: window over {over} on {face}, {area:.0f} mm2 opening, rim {lip:g} mm")
    return 0


def add_cli(sub):
    p = sub.add_parser("outline", help="chamfer / step / plan taper on one edge of a printed part, keeping a skin if hollow")
    p.add_argument("spec")
    p.add_argument("part")
    p.add_argument("--edge", required=True, help="two faces of the part's box, e.g. +y+z; write --edge=-y+x when it starts with -")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--chamfer", nargs="+", type=float, metavar="MM", help="A [B]: bevel legs along the first and second face")
    g.add_argument("--step", nargs="+", type=float, metavar="MM", help="A [B]: notch depth and length")
    p.add_argument("--span", help="LO,HI world mm along the edge (default: the whole edge)")
    p.add_argument("--wall", type=float, default=1.6, help="skin kept behind the new face when the part is hollow")
    p.add_argument("--force", action="store_true", help="cut even if another part overlaps the removed corner")
    p.add_argument("--dry", action="store_true")

    def _run(a):
        kind, v = ("chamfer", a.chamfer) if a.chamfer else ("step", a.step)
        return outline(a.spec, a.part, kind, a.edge, v[0], v[1] if len(v) > 1 else None, a.span, a.wall, a.force, a.dry)
    p.set_defaults(func=_run)
    q = sub.add_parser("window", help="see-through opening over an internal component where the photo shows it")
    q.add_argument("spec")
    q.add_argument("part")
    q.add_argument("--over", required=True, help="component to show (battery, esc, receiver ...)")
    q.add_argument("--face", default="+z")
    q.add_argument("--lip", type=float, default=2.0, help="rim kept on every side so the component stays captive")
    q.add_argument("--dry", action="store_true")
    q.set_defaults(func=lambda a: window(a.spec, a.part, a.over, a.face, a.lip, a.dry))

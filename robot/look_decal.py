"""`robot decal SPEC HOST --face +y --shape circle|ellipse|rect|stripe|poly|text --size W [H] [--at U,V] [--pair D]
[--text STR] [--points ...] [--color #hex] [--depth 0.8] [--id ID] [--dry]`: photo graphics (eyes, stripes, logos,
lettering) as a real colour-split face on a part.

WHY: the photo review keeps reporting "photo front plate has printed eyes / a striped top / the robot's name, model
is one flat colour". Real robots get these from stickers or multi-colour prints. A colour is per part, so a graphic
has to be its own part, and a loose sticker part fails support, fastening and disassembly checks.

How: the face under the graphic is found by ray casting HOST's mesh along -face over the graphic's footprint. It
must be one plane (normals within 3 deg, points within 0.3 mm): a sloped front plate works, a curved one does not.
On that plane

    HOST  = HOST subtract  footprint x [face - depth, outside]       (a pocket `depth` deep)
    DECAL = footprint x [face - depth - 0.4, face]                   (fills the pocket, 0.4 mm deeper)

DECAL is printed in HOST's material and declared `fused_with` HOST (a multi-colour print, the 0.4 mm overlap makes
them one solid). Its outer face is flush with HOST's, so the outline and `likeness` IoU do not change, and the
render shows the graphic in the decal's colour. For a host that is not printed (aluminium, carbon), the decal is a
`pc` sticker in the pocket on a keyed `glue` connection instead; refused on wedges, weapons, armour and forks, where
glue is a blocker (`connection.glue_on_impact`). Refuses when the decal would not lie inside HOST's solid
(a wall thinner than depth + 0.4 under it) or the face is not flat.

Footprint, in world mm on the two axes across the face (for +y/-y: x and z; +z/-z: x and y; +x/-x: y and z),
centred on --at (default the face centre):
  circle W, ellipse W H, almond W H (a pointed eye or leaf),
  star W H (5 points, W across the tips, H across the inner corners), ring W H (H the band width), rect W H, stripe H (a band H wide across the whole face along U, --at V only),
  poly --points u1,v1 u2,v2 ... (absolute world mm), text --text STR --size H [W] (bold sans; W squeezes it).
--angle turns the shape about its centre (degrees, U toward V). --pair D places two copies D apart along U (a pair
of eyes), mirrored about --at. A graphic on another decal (an iris on an eye) works: use the eye's id as HOST and
a --depth of 0.4. Several pieces in one call (a pair, letters) are joined into one solid by a hidden 0.8 mm web
inside HOST, or become separate parts where HOST is too thin for the web.
--color is the graphic's colour (hex); leave it out and run `robot colors SPEC --parts ID --force` to sample it.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from .look_outline import AX, E, _add_cut

OVERLAP = 0.25   # decal runs this far below the pocket floor: shared volume that makes it one print with HOST
FLOOR = 0.15     # HOST material kept under the decal (and its web), so nothing below it is touched
UV = {0: (1, 2), 1: (0, 2), 2: (0, 1)}


def _footprints(shape, W, H, at, pair, points, text, face_lo, face_hi, angle=0.0):
    """List of (outer polygon, [hole polygons]) in world (u, v) mm."""
    u0, v0 = at
    if shape == "poly":
        pts = [tuple(float(c) for c in p.split(",")) for p in points]
        return [(pts, [])]
    if shape == "stripe":
        h = W if H is None else H
        return [([(face_lo[0] - E, v0 - h / 2), (face_hi[0] + E, v0 - h / 2), (face_hi[0] + E, v0 + h / 2),
                  (face_lo[0] - E, v0 + h / 2)], [])]
    if shape == "text":
        polys = _text(text, W, H, angle)
        base = [([(u + u0, v + v0) for u, v in o], [[(u + u0, v + v0) for u, v in h] for h in hs]) for o, hs in polys]
    else:
        H = (W * 0.4 if shape == "star" else W * 0.1 if shape == "ring" else W) if H is None else H
        if shape == "rect":
            loc = [(-W / 2, -H / 2), (W / 2, -H / 2), (W / 2, H / 2), (-W / 2, H / 2)]
        elif shape == "almond":   # pointed eye / leaf: two arcs meeting at the ends of W
            n = 24
            ts = np.linspace(-1, 1, n)
            top = [(W / 2 * x, H / 2 * (1 - x * x)) for x in ts]
            loc = top + [(u, -v) for u, v in top[-2:0:-1]]
        elif shape == "star":     # n-point star (5), W across the points, H across the inner corners
            n = 5
            loc = [((W if i % 2 == 0 else H) / 2 * math.cos(math.pi / 2 + math.pi * i / n),
                    (W if i % 2 == 0 else H) / 2 * math.sin(math.pi / 2 + math.pi * i / n)) for i in range(2 * n)]
        elif shape == "ring":     # circle band: W outer diameter, H band width
            n = 48
            ring = [(W / 2 * math.cos(2 * math.pi * i / n), W / 2 * math.sin(2 * math.pi * i / n)) for i in range(n)]
            hole = [((W / 2 - H) * u / (W / 2), (W / 2 - H) * v / (W / 2)) for u, v in ring]
            return _pairs([([(u + u0, v + v0) for u, v in ring], [[(u + u0, v + v0) for u, v in hole]])], pair, u0)
        elif shape in ("circle", "ellipse"):
            n = 48   # same as ring, so a disc fills a ring's hole exactly
            loc = [(W / 2 * math.cos(2 * math.pi * i / n), H / 2 * math.sin(2 * math.pi * i / n)) for i in range(n)]
        else:
            raise SystemExit(f"unknown shape {shape}")
        ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        base = [([(u * ca - v * sa + u0, u * sa + v * ca + v0) for u, v in loc], [])]
    return _pairs(base, pair, u0)


def _pairs(base, pair, u0):
    if not pair:
        return base
    out = []
    for o, hs in base:
        for s in (-1, 1):
            # mirror the right copy so a pair of eyes or ears is symmetric
            f = (lambda p, s=s: (u0 + s * pair / 2 + (p[0] - u0) * s, p[1]))
            out.append(([f(p) for p in o], [[f(p) for p in h] for h in hs]))
    return out


def _text(s, W, H, angle=0.0):
    """Glyph outlines of `s` (bold sans), H tall, centred at 0; W (optional) squeezes it to that width."""
    from matplotlib.font_manager import FontProperties
    from matplotlib.path import Path as MPath
    from matplotlib.textpath import TextPath
    if not s:
        raise SystemExit("--shape text needs --text")
    tp = TextPath((0, 0), s, size=10, prop=FontProperties(family="DejaVu Sans", weight="bold"))
    rings = [np.asarray(r) for r in tp.to_polygons() if len(r) >= 3]
    allp = np.vstack(rings)
    lo, hi = allp.min(0), allp.max(0)
    k = H / (hi[1] - lo[1])
    kx = k if W is None else W / (hi[0] - lo[0])
    rings = [np.column_stack([(r[:, 0] - (lo[0] + hi[0]) / 2) * kx, (r[:, 1] - (lo[1] + hi[1]) / 2) * k]) for r in rings]
    if angle:
        ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        rings = [r @ np.array([[ca, sa], [-sa, ca]]) for r in rings]
    depth = [sum(MPath(o).contains_point(r[0]) for j, o in enumerate(rings) if j != i) for i, r in enumerate(rings)]
    out = []
    for i, r in enumerate(rings):
        if depth[i] % 2 == 0:
            holes = [h for j, h in enumerate(rings) if depth[j] == depth[i] + 1 and MPath(r).contains_point(h[0])]
            out.append(([tuple(p) for p in r], [[tuple(p) for p in h] for h in holes]))
    return out


def _clean(ring, tol=0.03, gap=0.12):
    """Drop near-duplicate and nearly collinear points (text outlines carry 0.001 mm segments, which become
    geom.tiny_edge blockers)."""
    from shapely.geometry import LinearRing
    r = np.asarray(LinearRing(ring).simplify(tol).coords)[:-1]
    out = [r[0]]
    for q in r[1:]:
        if np.hypot(*(q - out[-1])) >= gap:
            out.append(q)
    if len(out) > 3 and np.hypot(*(out[0] - out[-1])) < gap:
        out.pop()
    return [tuple(map(float, q)) for q in out]


def _lift(G, k, body):
    """Footprint sample points on lines through HOST's box along k (a coarse 'is an earlier decal here' test)."""
    lo, hi = body.aabb
    a, b = UV[k]
    G = G[:: max(1, len(G) // 300)]
    out = []
    for z in np.arange(lo[k] + 0.1, hi[k], 0.3):
        P = np.zeros((len(G), 3))
        P[:, a], P[:, b], P[:, k] = G[:, 0], G[:, 1], z
        out.append(P)
    return np.vstack(out)


def _rot_to_euler(R):
    """Inverse of xform.euler (R = Rz Ry Rx), degrees."""
    ry = math.degrees(math.asin(max(-1.0, min(1.0, -R[2, 0]))))
    rx = math.degrees(math.atan2(R[2, 1], R[2, 2]))
    rz = math.degrees(math.atan2(R[1, 0], R[0, 0]))
    return [round(rx, 4), round(ry, 4), round(rz, 4)]


def _plane(mesh, k, s, uv_pts):
    """Fit the face plane under the footprint points: (point, unit normal) or a reason string."""
    a, b = UV[k]
    O = np.zeros((len(uv_pts), 3))
    O[:, a], O[:, b] = uv_pts[:, 0], uv_pts[:, 1]
    lo, hi = mesh.bounds
    O[:, k] = hi[k] + 5 if s > 0 else lo[k] - 5
    D = np.zeros_like(O)
    D[:, k] = -s
    loc, ri, ti = mesh.ray.intersects_location(O, D, multiple_hits=False)
    if len(ri) < 0.97 * len(O):
        return f"the graphic runs off the part ({len(O) - len(ri)} of {len(O)} sample points miss it)"
    N = mesh.face_normals[ti]
    n = N.mean(0)
    n /= np.linalg.norm(n)
    if n[k] * s < 0.5:
        return "the face under the graphic does not look along --face"
    if np.degrees(np.arccos(np.clip(N @ n, -1, 1))).max() > 3.0:
        return "the face under the graphic is not one flat plane (move or shrink it, or pick another face)"
    p0 = loc.mean(0)
    if np.abs((loc - p0) @ n).max() > 0.3:
        return ("the face under the graphic steps or is curved (points more than 0.3 mm off one plane), or it overlaps "
                "an earlier decal's pocket: put the new graphic on that decal as HOST, or beside it")
    return p0, n


def _frame(k, n):
    """Rotation whose z is n and x is the face's U axis projected onto the plane."""
    a, _ = UV[k]
    x = np.eye(3)[a] - n * n[a]
    x /= np.linalg.norm(x)
    return np.column_stack([x, np.cross(n, x), n])


def _to_local2(R, p0, k, n, uv):
    """World (u, v) points projected along axis k onto the plane, in the plane frame's (x, y)."""
    a, b = UV[k]
    P = np.zeros((len(uv), 3))
    P[:, a], P[:, b] = uv[:, 0], uv[:, 1]
    P[:, k] = p0[k] - ((P - p0) @ n - (P[:, k] - p0[k]) * n[k]) / n[k]
    return ((P - p0) @ R)[:, :2]


def _load(path, part):
    from . import spec as spec_mod
    from . import world as world_mod
    raw = json.loads(Path(path).read_text())
    byid = {p["id"]: p for p in raw["parts"]}
    if part not in byid:
        raise SystemExit(f"no part {part}")
    P = byid[part]
    if "catalog" in P or "shape" not in P:
        raise SystemExit(f"{part} must be a made part with a shape")
    w = world_mod.World.build(world_mod.resolve(spec_mod.load(path), fast=True))
    return raw, byid, P, {b.id: b for b in w.bodies}


def _slab(R, p0, k, n, fps, z0, z1, M):
    """Shape (in the frame of the body pose M) of the footprints extruded from z0 to z1 along the face normal."""
    M = np.asarray(M, float)
    Rp, tp = M[:3, :3], M[:3, 3]
    items = []
    for outer, holes in fps:
        def pr(poly):
            xy = _to_local2(R, p0, k, n, np.asarray(poly, float))
            return {"type": "prism", "points": [[round(float(x), 3), round(float(y), 3)] for x, y in xy], "height": round(z1 - z0, 3)}
        sh = pr(outer)
        if holes:
            sh = {"type": "subtract", "base": sh, "cut": [dict(pr(h), height=round(z1 - z0 + 2, 3)) for h in holes]}
        items.append(sh)
    shape = items[0] if len(items) == 1 else {"type": "union", "items": items}
    at_w = p0 + n * (z0 + z1) / 2
    at_l = Rp.T @ (at_w - tp)
    return {"type": "place", "shape": shape, "at": [round(float(v), 3) for v in at_l], "rot": _rot_to_euler(Rp.T @ R)}


def _samples(fps, step=0.6):
    from matplotlib.path import Path as MPath
    allp = np.vstack([np.asarray(o) for o, _ in fps])
    lo, hi = allp.min(0), allp.max(0)
    gu, gv = np.meshgrid(np.arange(lo[0] + step / 2, hi[0], step), np.arange(lo[1] + step / 2, hi[1], step), indexing="ij")
    G = np.column_stack([gu.ravel(), gv.ravel()])
    m = np.zeros(len(G), bool)
    for o, hs in fps:
        mo = MPath(np.asarray(o)).contains_points(G)
        for h in hs:
            mo &= ~MPath(np.asarray(h)).contains_points(G)
        m |= mo
    return G[m]


def decal(path, host, face="+y", shape="rect", size=(10.0,), at=None, pair=None, points=(), text="", color=None,
          depth=0.8, pid=None, dry=False, angle=0.0):
    raw, byid, P, Bd = _load(path, host)
    k = AX[face[1]]
    s = -1.0 if face[0] == "-" else 1.0
    a, b = UV[k]
    lo, hi = Bd[host].aabb
    W = float(size[0]) if size else None
    H = float(size[1]) if size and len(size) > 1 else None
    if shape == "text":   # --size H [W]
        W, H = H, W
    c = ((lo[a] + hi[a]) / 2, (lo[b] + hi[b]) / 2)
    if at:
        c = tuple(float(x) for x in at.split(","))
    fps = _footprints(shape, W, H, c, pair, points, text, (lo[a], lo[b]), (hi[a], hi[b]), angle)
    if shape == "stripe":   # clip the band to the part across U
        fps = [([(max(u, lo[a] + 0.01), v) if u < lo[a] else (min(u, hi[a] - 0.01), v) for u, v in o], hs) for o, hs in fps]
    fps = [(_clean(o), [_clean(h) for h in hs]) for o, hs in fps]
    G = _samples(fps)
    if len(G) < 4:
        raise SystemExit("the graphic is too small (under ~2 mm2)")
    # earlier graphics on the same face of HOST under this one: the new graphic replaces them where it lies
    # (an iris over an eye), so it takes their depth and they get its footprint cut out
    under = []
    for q in raw["parts"]:
        dm = q.get("decal") or {}
        if dm.get("host") == host and dm.get("face") == face and q["id"] in Bd and Bd[q["id"]].inside(_lift(G, k, Bd[host])).any():
            under.append(q)
    if under:
        depth = float(under[0]["decal"]["depth"])
    import trimesh
    mesh = trimesh.util.concatenate([Bd[host].mesh] + [Bd[q["id"]].mesh for q in under]) if under else Bd[host].mesh
    fit = _plane(mesh, k, s, G)
    if isinstance(fit, str):
        raise SystemExit(f"decal on {host} {face}: {fit}")
    p0, n = fit
    R = _frame(k, n)
    # the decal must lie inside HOST's solid down to depth + overlap (sampled just inside the bottom)
    d_all = depth + OVERLAP
    probe = []
    xy = _to_local2(R, p0, k, n, G)
    for z in (-0.15, -depth / 2, -d_all + 0.15, -d_all - FLOOR):
        probe.append(p0 + xy[:, :1] * R[:, 0] + xy[:, 1:2] * R[:, 1] + z * n)
    probe = np.vstack(probe)
    inside = Bd[host].inside(probe)
    for q in under:
        inside |= Bd[q["id"]].inside(probe)
    if inside.mean() < 0.97:
        raise SystemExit(f"decal on {host}: only {inside.mean():.0%} of it lies inside {host} (a wall under "
                         f"{d_all:g} mm there, a hole, or an edge); move it, shrink it or use a smaller --depth")
    others = [bd for i, bd in Bd.items() if i != host and not getattr(bd, "is_wire", False)]
    hidden = sorted({bd.id for bd in others if bd.inside(np.vstack([probe[:len(G)] + n * t for t in (0.6, 3.0)])).any()})
    from . import catalog
    printed = catalog.part_is_printed(P.get("process"), P.get("material"))
    from .checks.connections import IMPACT
    if not printed and P.get("kind") in IMPACT:
        raise SystemExit(f"decal on {host}: a sticker can only be glued, and glue on a {P.get('kind')} peels on the "
                         "first hit (connection.glue_on_impact); put the graphic on a printed part, or colour the plate")
    pid = pid or f"{host}_decal" + ("" if f"{host}_decal" not in byid else f"_{len(byid)}")
    if pid in byid:
        raise SystemExit(f"part id {pid} exists")
    area = len(G) * 0.6 ** 2
    msg = (f"{pid}: {shape} graphic on {host} {face}, ~{area:.0f} mm2, {depth:g} mm deep, "
           + ("fused (multi-colour print)" if printed else "pc sticker, glued into the pocket")
           + (f"; covered by {hidden} from outside" if hidden else ""))
    if dry:
        print(msg)
        return 0
    M = Bd[host].M
    cut = _slab(R, p0, k, n, fps, -depth, E, M)
    groups = [(pid, _slab(R, p0, k, n, fps, -d_all, 0.0, M))]
    if len(fps) > 1:
        # several pieces (a pair of eyes, letters): a hidden 0.8 mm web under the face, inside HOST, joins them into
        # one solid; where HOST is too thin for it each piece becomes its own part
        from shapely.geometry import MultiPoint
        hull = MultiPoint([q for o, _ in fps for q in o]).convex_hull.buffer(-0.3, join_style=2).simplify(0.05)
        hull = [tuple(q) for q in np.asarray(hull.exterior.coords)[:-1]]   # inset: no vertex shared with a piece
        Gh = _samples([(hull, [])])
        xh = _to_local2(R, p0, k, n, Gh)
        for wt in (0.6, 0.35):
            ph = p0 + xh[:, :1] * R[:, 0] + xh[:, 1:2] * R[:, 1] + (-d_all - wt - FLOOR) * n
            if Bd[host].inside(ph).mean() >= 0.97:
                web = _slab(R, p0, k, n, [(hull, [])], -d_all - wt, -d_all + 0.15, M)
                groups = [(pid, {"type": "union", "items": [groups[0][1], web]})]
                msg += ", joined by a hidden web"
                break
        else:
            groups = [(f"{pid}_{j + 1}", _slab(R, p0, k, n, [fp], -d_all, 0.0, M)) for j, fp in enumerate(fps)]
            msg += f", {len(groups)} separate pieces"
    _add_cut(P, cut)
    for q in under:   # the new graphic replaces the earlier one where it lies: cut it out of it, through its web
        _add_cut(q, _slab(R, p0, k, n, fps, -d_all - 1.0, E, Bd[q["id"]].M))
    if under:
        msg += f", over {[q['id'] for q in under]} (cut out of them, {depth:g} mm deep like them)"
    i = raw["parts"].index(P)
    for gid, gshape in groups:
        if gid in byid:
            raise SystemExit(f"part id {gid} exists")
        part = {"id": gid, "kind": "other", "shape": gshape, "decal": {"host": host, "face": face, "depth": depth}}
        if P.get("joint") or P.get("parent"):   # rides on a moving (or parented) host: same frame, follows its joint
            part.update(parent=host, at=[0, 0, 0], rot=[0, 0, 0])
        else:
            part.update(at=P.get("at", [0, 0, 0]), rot=P.get("rot", [0, 0, 0]))
        if printed:
            part.update(material=P.get("material"), process=P.get("process"), fused_with=host)
            if "print_orientation" in P:
                part["print_orientation"] = P["print_orientation"]
        else:
            part.update(material="pc", process="cnc")
            raw.setdefault("connections", []).append({"a": gid, "b": host, "method": "glue", "mechanical_key": True,
                                                      "reason": "sticker glued into a pocket that holds it on every side but the face"})
        if color:
            part["color"] = color
        i += 1
        raw["parts"].insert(i, part)
    Path(path).write_text(json.dumps(raw, indent=1))
    print(msg)
    if not color:
        print(f"next: `robot colors {path} --parts {pid} --force` to sample its colour from the photo")
    return 0


def add_cli(sub):
    p = sub.add_parser("decal", help="photo graphic (eyes, stripe, logo, lettering) as a flush colour-split face part")
    p.add_argument("spec")
    p.add_argument("host")
    p.add_argument("--face", default="+y", choices=["+z", "-z", "+x", "-x", "+y", "-y"],
                   help="write --face=-y when it starts with -")
    p.add_argument("--shape", default="rect", choices=["circle", "ellipse", "almond", "star", "ring", "rect", "stripe", "poly", "text"])
    p.add_argument("--size", nargs="+", type=float, default=[10.0], metavar="MM", help="W [H] (stripe: H; text: H [W])")
    p.add_argument("--at", help="U,V world mm across the face (default its centre); write --at=-5,3 when negative")
    p.add_argument("--angle", type=float, default=0.0, help="turn the shape (or text) this many degrees from U toward V")
    p.add_argument("--pair", type=float, help="two mirrored copies this far apart along U (eyes)")
    p.add_argument("--points", nargs="*", default=[], help="poly: u,v points in world mm")
    p.add_argument("--text", default="")
    p.add_argument("--color", help="hex colour, e.g. #f0f0f0 (default: none, then `robot colors --parts ID --force`)")
    p.add_argument("--depth", type=float, default=0.8, help="pocket depth in the host (the decal goes 0.4 mm deeper)")
    p.add_argument("--id")
    p.add_argument("--dry", action="store_true")
    p.set_defaults(func=lambda a: decal(a.spec, a.host, a.face, a.shape, a.size, a.at, a.pair, a.points, a.text,
                                        a.color, a.depth, a.id, a.dry, a.angle))

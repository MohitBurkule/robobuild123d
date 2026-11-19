"""`robot plate SPEC --part chassis --face +z [--thick 1.5] [--id top_plate] [--material M] [--inset 1.0] [--dry]`:
split the skin of a flat face off a printed part as its own plate.

WHY: photos of real robots show thin deck, side and front plates (aluminium, carbon, polycarbonate or printed) screwed
onto a frame, while generated chassis are one solid block, so the photo review keeps reporting "model is one slab, photo
has separate plates". Splitting by hand meant measuring the face, guessing a box and fixing the slivers it left.

How: the part's mesh is ray cast along the face normal on a 0.75 mm grid. Hits on faces that point along the normal
are grouped by height (0.25 mm bins); the level with the largest area wins (or the outermost with --level outer). The
largest axis-aligned rectangle inside that level (shrunk by --inset) becomes the plate outline. Then

    plate  = part  intersect  box(rectangle x [level - thick, level + 1])
    part   = part  subtract   that box

so the union of the two is exactly the old part: the outside does not change and `likeness` is unaffected. Both new
solids are built and refused if either is not one solid, if the part grows tiny edges (geom.tiny_edge), or if less
than 85 % of the slab under the rectangle was solid (a pocket under the skin would make a lid with holes).

Writes the new `plate` part (same at/rot as the part, `kind: plate`, a shade lighter than the part, material/process
from --material, else the part's own), the cut on the part, and fresh `volume_mm3` for both when the part had one. It does NOT fix the plate
on: follow with real screws (`robot screws SPEC <id> --face +z --pattern corners`) or a connection, then
`robot fasteners SPEC --fill`, then `robot colors SPEC` so the plate gets its own photo colour.
Only parts at identity `rot` are supported (all generated chassis are).
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

STEP = 0.75
PROCESS = {"aluminium": "cnc", "steel": "waterjet", "titanium": "waterjet", "cf_plate": "cnc", "fr4": "cnc",
           "pc": "cnc", "hdpe": "cnc", "uhmw": "cnc", "pp": "cnc", "brass": "cnc", "copper": "cnc"}


def _largest_rect(m):
    """(r0, r1, c0, c1) of the largest all-True axis-aligned rectangle in a 2D bool array (half-open), or None."""
    H, W = m.shape
    h = np.zeros(W, int)
    best, out = 0, None
    for r in range(H):
        h = np.where(m[r], h + 1, 0)
        st = []
        for c in range(W + 1):
            cur = h[c] if c < W else 0
            s = c
            while st and st[-1][1] >= cur:
                s, hh = st.pop()
                a = hh * (c - s)
                if a > best:
                    best, out = a, (r - hh + 1, r + 1, s, c)
            st.append((s, cur))
    return out


def find_face(mesh, axis, sign, level="largest", inset=1.0, min_area=150.0, others=()):
    """Rectangle on the flat face: dict(level, lo (u, v), hi (u, v), area) in world mm, or None. Cells where another
    body (`others`) reaches into the top 3 mm of the part or lies on the face are left out, so the plate never takes
    over an overlap or a contact that belonged to the part."""
    a = axis
    u, v = [i for i in range(3) if i != a]
    lo, hi = mesh.bounds
    gu = np.arange(lo[u] + STEP / 2, hi[u], STEP)
    gv = np.arange(lo[v] + STEP / 2, hi[v], STEP)
    U, V = np.meshgrid(gu, gv, indexing="ij")
    O = np.zeros((U.size, 3))
    O[:, u], O[:, v] = U.ravel(), V.ravel()
    O[:, a] = hi[a] + 5 if sign > 0 else lo[a] - 5
    D = np.zeros_like(O)
    D[:, a] = -sign
    loc, ri, ti = mesh.ray.intersects_location(O, D, multiple_hits=False)
    Hm = np.full(U.size, np.nan)
    ok = np.abs(mesh.face_normals[ti][:, a] * sign - 1) < 0.02
    Hm[ri[ok]] = loc[ok, a]
    Hm = Hm.reshape(U.shape)
    hs = np.round(Hm[np.isfinite(Hm)] / 0.25) * 0.25
    if not len(hs):
        return None
    vals, cnt = np.unique(hs, return_counts=True)
    keep = cnt * STEP * STEP >= min_area
    if not keep.any():
        return None
    vals, cnt = vals[keep], cnt[keep]
    lev = (vals.max() if sign > 0 else vals.min()) if level == "outer" else vals[np.argmax(cnt)]
    flat = np.isfinite(Hm) & (np.abs(Hm - lev) <= 0.2)
    if len(others) and flat.any():
        Q = np.zeros((flat.sum(), 5, 3))
        Q[..., u] = U[flat][:, None]
        Q[..., v] = V[flat][:, None]
        Q[..., a] = lev + sign * np.array([0.3, -0.5, -1.25, -2.0, -3.0])[None, :]
        busy = np.zeros(len(Q), bool)
        for o in others:
            busy |= o.inside(Q.reshape(-1, 3)).reshape(len(Q), -1).any(1)
        idx = np.argwhere(flat)
        bm = np.zeros_like(flat)
        bm[idx[busy, 0], idx[busy, 1]] = True
        from scipy import ndimage as nd
        flat &= ~nd.binary_dilation(bm, iterations=3)  # 2 mm clear of any contact or overlap
    k = int(np.ceil(inset / STEP))
    if k:
        from scipy import ndimage as nd
        flat = nd.binary_erosion(flat, iterations=k)
    rc = _largest_rect(flat)
    if rc is None:
        return None
    r0, r1, c0, c1 = rc
    lo_uv = (gu[r0] - STEP / 2, gv[c0] - STEP / 2)
    hi_uv = (gu[r1 - 1] + STEP / 2, gv[c1 - 1] + STEP / 2)
    return {"level": float(lev), "lo": lo_uv, "hi": hi_uv, "area": (hi_uv[0] - lo_uv[0]) * (hi_uv[1] - lo_uv[1]),
            "u": u, "v": v}


def _box(face, axis, sign, thick):
    a, u, v = axis, face["u"], face["v"]
    size, at = [0.0] * 3, [0.0] * 3
    for i, (l, h) in ((u, (face["lo"][0], face["hi"][0])), (v, (face["lo"][1], face["hi"][1]))):
        size[i], at[i] = round(h - l, 3), round((l + h) / 2, 3)
    a0 = face["level"] - sign * thick
    a1 = face["level"] + sign * 1.0
    size[a], at[a] = round(abs(a1 - a0), 3), round((a0 + a1) / 2, 3)
    return {"type": "place", "shape": {"type": "box", "size": size}, "at": at, "rot": [0, 0, 0]}


def _shade(hexc, dl=0.12):
    """The part colour a little lighter (darker for light colours), so the plate's outline reads in renders."""
    import colorsys

    from .world import parse_color
    c = parse_color(hexc or "")
    if c is None:
        return hexc
    h, lt, s = colorsys.rgb_to_hls(*[x / 255 for x in c])
    lt = lt + dl if lt < 0.75 else lt - dl
    return "#" + "".join(f"{round(x * 255):02x}" for x in colorsys.hls_to_rgb(h, min(max(lt, 0), 1), s))


def _rot_for(axis):
    return [[0, 90, 0], [90, 0, 0], [0, 0, 0]][axis]


def route_points(spec_name):
    """(N, 4) points (x, y, z, wire radius) along the wires the router last found for this robot (the proxy
    baseline), every 0.5 mm, or an empty array. Bosses must stay off them or the wiring stops routing."""
    from .proxy import baseline_path
    try:
        d = json.loads(baseline_path(spec_name).read_text())
    except (OSError, ValueError):
        return np.zeros((0, 4))
    out = []
    for rt in d.get("routes") or []:
        P = np.asarray(rt.get("points") or [], float)
        r = float(rt.get("od_mm") or 2.0) / 2
        for a, b in itertools.pairwise(P):
            k = max(2, int(np.linalg.norm(b - a) / 0.5) + 1)
            for t in np.linspace(0, 1, k):
                out.append([*(a + (b - a) * t), r])
    return np.asarray(out) if out else np.zeros((0, 4))


def sweeps_of(raw, w):
    """[(pivot (3,), radius)] for every part with a joint: a sphere that holds everything it can sweep."""
    out = []
    byid = {b.id: b for b in w.bodies}
    for q in raw.get("parts") or []:
        j = q.get("joint")
        if not j or q["id"] not in byid:
            continue
        b = byid[q["id"]]
        piv = np.asarray(j.get("pivot") or b.center, float)
        if q.get("parent"):
            piv = np.asarray(b.center, float)  # pivot is in the parent's frame: fall back to the part centre
        r = float(np.linalg.norm(b.mesh.vertices - piv[None, :], axis=1).max())
        out.append((piv, r))
    return out


def screw_spots(body, others, f, axis, sign, thick, n, depth=8.5, edge=2.6, boss_r=3.0, routes=None, sweeps=None):
    """Up to n spots on the plate for flush M2 screws, spread out from the plate's corners inwards:
    [((u, v), boss)] where boss is False when the part already has `depth` mm of solid under the plate around the
    pilot (1.6 mm ring), True when a printed boss (radius boss_r, `depth` long) can hang from the part's wall inside
    its own closed cavity: at least 20 % of the boss already in the part, the rest enclosed by the part on every
    side but the plate, and nothing else within 0.3 mm."""
    u, v = f["u"], f["v"]
    gu = np.arange(f["lo"][0] + edge, f["hi"][0] - edge + 1e-6, 1.5)
    gv = np.arange(f["lo"][1] + edge, f["hi"][1] - edge + 1e-6, 1.5)
    if not len(gu) or not len(gv):
        return []
    U, V = np.meshgrid(gu, gv, indexing="ij")
    C = np.stack([U.ravel(), V.ravel()], 1)
    ds = f["level"] - sign * (thick + 0.1 + np.arange(0, depth, 0.5))

    def pts(rr, k=8):
        offs = [(0.0, 0.0)] + [(rr * np.cos(x), rr * np.sin(x)) for x in np.linspace(0, 2 * np.pi, k, endpoint=False)]
        P = np.zeros((len(C), len(offs), len(ds), 3))
        for j, (du, dv) in enumerate(offs):
            P[:, j, :, u] = (C[:, 0] + du)[:, None]
            P[:, j, :, v] = (C[:, 1] + dv)[:, None]
        P[..., axis] = ds[None, None, :]
        return P.reshape(len(C), -1, 3)

    P16 = pts(1.6, 6)
    solid = body.inside(P16.reshape(-1, 3)).reshape(len(C), -1).all(1)
    PB = np.concatenate([pts(boss_r * 0.5), pts(boss_r)], 1)
    m = PB.shape[1]
    inb = body.inside(PB.reshape(-1, 3)).reshape(len(C), m)
    frac = inb.mean(1)
    cand = ~solid & (frac >= 0.2)
    if cand.any():
        PC = np.concatenate([pts(r_, 24)[cand] for r_ in (1.0, 2.0, boss_r + 0.4)], 1)  # dense: no part may poke in
        hit = np.zeros(len(PC), bool)
        flat_pc = PC.reshape(-1, 3)
        lo_pc, hi_pc = flat_pc.min(0) - 1, flat_pc.max(0) + 1
        for o in others:
            olo, ohi = o.aabb
            if np.any(olo > hi_pc) or np.any(ohi < lo_pc):
                continue
            hit |= o.inside(flat_pc).reshape(len(PC), -1).any(1)
        for c, rr in sweeps or []:  # moving parts: stay out of the sphere they can sweep about their pivot
            seg = PC[:, 0, :]
            hit |= np.linalg.norm(seg - c[None, :], axis=1) < rr + boss_r + 1.5 + depth
        Q = PB[cand][~inb[cand]]
        idx = np.repeat(np.arange(cand.sum()), (~inb[cand]).sum(1))
        enc = np.ones(cand.sum(), bool)
        if len(Q):
            dirs = [np.eye(3)[i] * s for i in range(3) for s in (1, -1) if not (i == axis and s == sign)]
            for d in dirs:
                ok = body.mesh.ray.intersects_any(Q, np.tile(d, (len(Q), 1)))
                bad = np.bincount(idx[~ok], minlength=cand.sum()) > 0
                enc &= ~bad
        if routes is not None and len(routes):  # keep 1.5 mm clear of the wire routes
            ci = np.nonzero(cand)[0]
            R = routes[(routes[:, axis] >= ds.min() - 2.5) & (routes[:, axis] <= ds.max() + 2.5)]
            if len(R):
                du = C[ci][:, None, 0] - R[None, :, u]
                dv = C[ci][:, None, 1] - R[None, :, v]
                near = (np.hypot(du, dv) < boss_r + R[None, :, 3] + 1.5).any(1)
                hit[near] = True
        boss = np.zeros(len(C), bool)
        boss[np.nonzero(cand)[0][~hit & enc]] = True
    else:
        boss = np.zeros(len(C), bool)
    good = solid | boss
    if good.any():  # the driver needs a clear line above the head
        A = np.zeros((len(C), 24, 3))
        A[..., u], A[..., v] = C[:, 0:1], C[:, 1:2]
        A[..., axis] = f["level"] + sign * np.arange(0.3, 12.0, 0.5)[None, :]
        clear = np.ones(len(C), bool)
        for o in others:
            clear &= ~o.inside(A.reshape(-1, 3)).reshape(len(C), -1).any(1)
        good &= clear
    if not good.any():
        return []
    Cg, Bg = C[good], boss[good]
    lo, hi = np.array(f["lo"]), np.array(f["hi"])
    corners = np.array([[a, b] for a in (lo[0], hi[0]) for b in (lo[1], hi[1])])
    out = []
    for c in corners:  # nearest good spot to each corner (solid preferred within 3 mm), then fill by farthest-point
        dd = np.linalg.norm(Cg - c, axis=1) + 3.0 * Bg
        k = int(np.argmin(dd))
        if all(np.linalg.norm(Cg[k] - Cg[q]) > 8.0 for q in out):
            out.append(k)
    while len(out) < n:
        dmin = np.min([np.linalg.norm(Cg - Cg[q], axis=1) for q in out], axis=0)
        k = int(np.argmax(dmin))
        if dmin[k] < 8.0:
            break
        out.append(k)
    return [((round(float(Cg[k][0]), 2), round(float(Cg[k][1]), 2)), bool(Bg[k])) for k in out[:n]]


def _boss(f, axis, sign, thick, uv, at, depth=8.5, boss_r=3.0):
    c = [0.0] * 3
    c[f["u"]], c[f["v"]] = uv
    c[axis] = f["level"] - sign * (thick + depth / 2 + 0.05)  # top flush with the plate underside
    return {"type": "place", "shape": {"type": "cylinder", "radius": boss_r, "height": depth + 0.1},
            "at": [round(float(c[i] - at[i]), 3) for i in range(3)], "rot": _rot_for(axis)}


def split(spec_path, part_id, face="+z", thick=1.5, new_id=None, material=None, process=None, inset=1.0,
          level="largest", dry=False, screws=0, _retry=2):
    """Split, and when the kernel leaves a bad solid or mesh, retry with the plate 0.5 mm further inside the face
    (a different cut usually tessellates cleanly)."""
    info, res = _split(spec_path, part_id, face, thick, new_id, material, process, inset, level, dry, screws)
    if info is None and _retry and str(res).startswith(("refused (meshes", "refused (would not", "refused (tiny")):
        info2, res2 = split(spec_path, part_id, face, thick, new_id, material, process, inset + 0.5, level, dry, screws,
                            _retry - 1)
        return (info2, res2) if info2 is not None else (None, f"{res2} | first try: {res}")
    return info, res


def _split(spec_path, part_id, face="+z", thick=1.5, new_id=None, material=None, process=None, inset=1.0,
           level="largest", dry=False, screws=0):
    from . import shapes
    from . import spec as spec_mod
    from . import world as world_mod
    from .checks.geom_sanity import tiny_edges

    sign = 1 if face[0] == "+" else -1
    axis = "xyz".index(face[1])
    p = Path(spec_path)
    txt = p.read_text()
    raw = json.loads(txt)
    if not part_id:  # the chassis root: the first structure part
        part_id = next((q["id"] for q in raw["parts"] if q.get("kind") == "structure"), "chassis")
    part = next((q for q in raw["parts"] if q["id"] == part_id), None)
    if part is None or not part.get("shape"):
        return None, f"no made part `{part_id}`"
    if any(abs(float(x)) > 1e-9 for x in (part.get("rot") or [0, 0, 0])):
        return None, f"`{part_id}` has a rotation; only parts at identity rot are supported"
    new_id = new_id or f"{part_id}_plate_{'pn'[sign < 0]}{face[1]}"
    if any(q["id"] == new_id for q in raw["parts"]):
        return None, f"a part `{new_id}` already exists"
    s = spec_mod.load(spec_path)
    r = world_mod.resolve(s, fast=True)
    w = world_mod.World.start(r)
    body = next((b for b in w.bodies if b.id == part_id), None)
    if body is None:
        return None, f"`{part_id}` did not build"
    others = [b for b in w.bodies if b.id != part_id and not getattr(b, "is_wire", False)
              and not getattr(b, "fastener", False)]
    f = find_face(body.mesh, axis, sign, level, inset, others=others)
    if f is None:
        return None, f"no flat {face} face of 150 mm2 or more on `{part_id}`"
    side = min(f["hi"][0] - f["lo"][0], f["hi"][1] - f["lo"][1])
    if side < 15.0 or f["area"] < 600.0:
        return None, (f"the free flat {face} face is only {f['hi'][0] - f['lo'][0]:.1f} x {f['hi'][1] - f['lo'][1]:.1f}"
                      " mm: too small to read as a plate (needs 15 mm sides and 600 mm2)")
    at = np.asarray(part.get("at") or [0, 0, 0], float)
    why = []
    tries = [thick] if thick > 0 else [2.0, 2.5, 3.0, 1.5]
    for th in tries:  # --thick 0: the first that leaves no thin skin
        box = _box(f, axis, sign, th)
        # slab must be (nearly) solid under the rectangle, else the plate would be a lid with holes
        lo = np.array(box["at"]) - np.array(box["shape"]["size"]) / 2
        hi = np.array(box["at"]) + np.array(box["shape"]["size"]) / 2
        g = [np.linspace(lo[i] + 0.5, hi[i] - 0.5, 12) for i in range(3)]
        g[axis] = np.array([f["level"] - sign * th / 2])
        P = np.stack(np.meshgrid(*g, indexing="ij"), -1).reshape(-1, 3)
        solid_frac = float(body.inside(P).mean())
        if solid_frac < 0.85:
            why.append(f"{th} mm: only {solid_frac:.0%} of the skin under the {face} face is solid (pockets below)")
            continue
        g[axis] = np.array([f["level"] - sign * (th + 0.1)])
        P1 = np.stack(np.meshgrid(*g, indexing="ij"), -1).reshape(-1, 3)
        P2 = P1.copy()
        P2[:, axis] -= sign * 0.85
        thin = float((body.inside(P1) & ~body.inside(P2)).mean())
        if thin > 0.05:
            why.append(f"{th} mm: {thin:.0%} of the part under the plate would be a skin thinner than 0.9 mm")
            continue
        break
    else:
        return None, "no plate thickness fits: " + "; ".join(why)
    thick = th
    box["at"] = [round(float(x - at[i]), 3) for i, x in enumerate(box["at"])]  # into the part frame (rot is identity)
    old = part["shape"]
    cands = []
    if screws:
        cands = screw_spots(body, others, f, axis, sign, thick, 3 * screws, routes=route_points(s.name),
                            sweeps=sweeps_of(raw, w))
    plate_shape = {"type": "intersect", "items": [old, box]}
    cut_shape = {"type": "subtract", "base": old, "cut": [box]}
    base = Path(spec_path).parent
    try:
        so, sp, sc = (shapes.to_solid(x, base) for x in (old, plate_shape, cut_shape))
    except Exception as e:  # noqa: BLE001
        return None, f"CAD failed: {e}"
    te0 = len(tiny_edges(sc))
    spots, skipped = [], 0
    for uv, bs in cands:  # bosses one at a time: keep only those that add no tiny edge and stay one solid
        if len(spots) >= screws:
            break
        if bs:
            try:
                t1 = sc.fuse(shapes.to_solid(_boss(f, axis, sign, thick, uv, at), base))
                t1 = t1.clean() if hasattr(t1, "clean") else t1
                if len(t1.solids()) != len(sc.solids()) or len(tiny_edges(t1)) > te0:
                    skipped += 1
                    continue
            except Exception:  # noqa: BLE001
                skipped += 1
                continue
        spots.append((uv, bs))
    bosses = [_boss(f, axis, sign, thick, uv, at) for uv, bs in spots if bs]
    if bosses:
        cut_shape = {"type": "union", "items": [cut_shape] + bosses}
        try:
            sc = shapes.to_solid(cut_shape, base)
        except Exception as e:  # noqa: BLE001
            return None, f"CAD failed with bosses: {e}"
    ns_p, ns_c, ns_o = len(sp.solids()), len(sc.solids()), len(so.solids())
    te_o, te_p, te_c = len(tiny_edges(so)), len(tiny_edges(sp)), len(tiny_edges(sc))
    info = (f"{face} face at {f['level']:.2f} mm, plate {f['hi'][0] - f['lo'][0]:.1f} x {f['hi'][1] - f['lo'][1]:.1f}"
            f" x {thick} mm; solids plate {ns_p}, part {ns_c} (was {ns_o}); tiny edges plate {te_p}, part {te_c}"
            f" (was {te_o}); skin {solid_frac:.0%} solid")
    extra = float(sp.volume) + float(sc.volume) - float(so.volume)  # the bosses add at most pi r^2 h each
    vol_ok = -0.01 * float(so.volume) <= extra <= 0.01 * float(so.volume) + 250.0 * sum(1 for _, bs in spots if bs)
    if ns_p != 1 or ns_c != ns_o or not sp.is_valid or not sc.is_valid or not vol_ok:
        return None, "refused (would not stay one valid solid each): " + info
    from .checks.integrity import (
        shells,  # the mesh the verifier sees (integrity.solids) must stay closed too
    )
    from .geom import geom_for
    sh = [shells(geom_for(x, base).mesh) for x in (old, plate_shape, cut_shape)]
    if sh[1] != (1, 0) or sh[2] != sh[0]:
        return None, f"refused (meshes: plate {sh[1]}, part {sh[2]}, was {sh[0]} (closed, open)): " + info
    if te_c > max(10, te_o) or te_p > 10:
        return None, "refused (tiny edges): " + info
    if screws:
        info += "; screw spots " + ", ".join(f"({x}, {y}){' boss' if bs else ''}" for (x, y), bs in spots)
        info += f" ({skipped} boss spot(s) skipped: tiny edges)" if skipped else ""
        if len(spots) < 2:
            return None, "refused (fewer than 2 screw spots with 8.5 mm of material, or room for a boss, under the plate): " + info
    if dry:
        return info, None
    mat = material or part.get("material")
    proc = process or (PROCESS.get(mat) if material else None) or part.get("process")
    plate = {"id": new_id, "kind": "plate", "material": mat, "process": proc, "shape": plate_shape,
             "at": list(part.get("at") or [0, 0, 0]), "rot": [0, 0, 0],
             "color": _shade(part.get("color")), "print_orientation": part.get("print_orientation") or face}
    if part.get("volume_mm3"):
        part["volume_mm3"] = round(float(sc.volume), 1)
        plate["volume_mm3"] = round(float(sp.volume), 1)
    part["shape"] = cut_shape
    raw["parts"].insert(raw["parts"].index(part) + 1, plate)
    ind = 1 if txt.startswith("{\n ") and not txt.startswith("{\n  ") else 2
    p.write_text(json.dumps(raw, indent=ind) + "\n")
    return info + f"; wrote `{new_id}`", ([uv for uv, _ in spots], new_id)


def main(a):
    before = Path(a.spec).read_text()
    info, res = split(a.spec, a.part, a.face, a.thick, a.id, a.material, a.process, a.inset, a.level, a.dry, a.screws)
    if info is None:
        print(res)
        return 1
    print(info)
    if a.dry:
        return 0
    if a.screws and res and res[0]:
        from . import look_screws
        spots, pid = res
        look_screws.main(a.spec, pid, a.face, "at", len(spots), 0.0, ";".join(f"{x},{y}" for x, y in spots))
        raw = json.loads(Path(a.spec).read_text())
        n = sum(1 for f in raw.get("fasteners") or [] if pid in (f.get("through") or []))
        if n < 2:  # an unattached plate is worse than none: put the spec back
            Path(a.spec).write_text(before)
            print(f"only {n} screw(s) fixed `{pid}` on; spec restored, no plate")
            return 1
        print("next: `robot colors` so the plate gets its photo colour, then `robot verify`")
    else:
        print("next: fix it on with screws (`robot screws`) or a connection, `robot fasteners --fill`, `robot colors`")
    return 0


def add_cli(sub):
    p = sub.add_parser("plate", help="split a flat face's skin off a printed part as its own plate (outside unchanged)")
    p.add_argument("spec")
    p.add_argument("--part", help="default: the first structure part (the chassis root)")
    p.add_argument("--face", default="+z", choices=["+z", "-z", "+x", "-x", "+y", "-y"])
    p.add_argument("--thick", type=float, default=0.0, help="plate thickness; 0 (default) tries 2, 2.5, 3, 1.5 mm and "
                   "takes the first that is solid under the face and leaves no skin under 0.9 mm on the part")
    p.add_argument("--id", help="new part id (default <part>_plate_<p|n><axis>)")
    p.add_argument("--material", help="plate material (`robot materials`), default the part's")
    p.add_argument("--process", help="default cnc/waterjet for sheet and metal, else the part's")
    p.add_argument("--inset", type=float, default=1.0, help="keep the plate this far inside the flat face's edge")
    p.add_argument("--level", default="largest", choices=["largest", "outer"])
    p.add_argument("--screws", type=int, default=0, help="also fix the plate on with this many flush M2 screws "
                   "(`robot screws`) at spots with 8.5 mm of material (or room for a boss) under them; refuses the split if fewer than 2 fit")
    p.add_argument("--dry", action="store_true")
    p.set_defaults(func=main)

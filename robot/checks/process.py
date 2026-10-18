"""Process-aware manufacturability on the exact B-rep.

Every made part declares `process`; the geometry must be makeable that way:
  sheet_cut (laser / waterjet / ...): a constant-thickness extrusion of one 2D profile, stock gauge, hole >= t (hard
    metals) or 0.5 t, internal corner radius >= kerf, web between features >= t; no pockets/chamfers/countersinks unless
    declared in `secondary_ops`.
  sheet_bent: planar + cylindrical faces only, inside bend radius >= k t, flange >= 3 t + r, holes >= 2 t from bends.
  turned: surfaces of revolution about one axis (+ declared flat / keyway / cross_hole / drilled).
  milled: no internal corner radius < tool radius, no sharp vertical internal corner, every face reachable along +-X/Y/Z.
  fdm / sla: geometry left to `mfg` / `printability`; `print_orientation` required, weapon supports print layer-safe.
  cots: free geometry must match a stock rod / bearing.
Spinner weapons must not be printed. Anything not evaluated goes to NOT CHECKED.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from .. import catalog
from ..finding import BLOCKER, fail, ok
from ..spec import ELECTRONIC

G = "process"
TOL = 0.02
ANG = 1e-3
AXES = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)
ORIENT = {"+x": 0, "-x": 1, "+y": 2, "-y": 3, "+z": 4, "-z": 5}


# ---------------------------------------------------------------- B-rep helpers
def _v(x):
    if callable(x.X):
        return np.array([x.X(), x.Y(), x.Z()], float)
    return np.array([x.X, x.Y, x.Z], float)


def _unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def face_info(f):
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_Cone, GeomAbs_Cylinder, GeomAbs_Plane, GeomAbs_Sphere, GeomAbs_Torus

    ad = BRepAdaptor_Surface(f.wrapped)
    t = ad.GetType()
    d = {"f": f, "area": f.area, "kind": "other"}
    if t == GeomAbs_Plane:
        c = f.center()
        d.update(kind="plane", n=_unit(_v(f.normal_at(c))), c=_v(c))
        return d
    ax = None
    if t == GeomAbs_Cylinder:
        cy = ad.Cylinder()
        ax = cy.Axis()
        d.update(kind="cylinder", r=cy.Radius(), arc=math.degrees(ad.LastUParameter() - ad.FirstUParameter()))
    elif t == GeomAbs_Cone:
        ax = ad.Cone().Axis()
        d["kind"] = "cone"
    elif t == GeomAbs_Torus:
        ax = ad.Torus().Axis()
        d["kind"] = "torus"
    elif t == GeomAbs_Sphere:
        d.update(kind="sphere", loc=_v(ad.Sphere().Location()))
        return d
    if ax is not None:
        d["dir"] = _unit(_v(ax.Direction()))
        d["loc"] = _v(ax.Location())
        q = f.position_at(0.5, 0.5)
        d["q"] = _v(q)
        rad = d["q"] - d["loc"]
        rad = rad - (rad @ d["dir"]) * d["dir"]
        nq = _v(f.normal_at(q))
        d["concave"] = bool(nq @ rad < 0)
        verts = np.array([_v(x) for x in f.vertices()]) if f.vertices() else d["q"][None]
        s = (verts - d["loc"]) @ d["dir"]
        d["len"] = float(s.max() - s.min())
    return d


def edge_faces(shape):
    """[(edge, [face, face])] for every edge of the shape."""
    groups = {}
    for f in shape.faces():
        for e in f.edges():
            lst = groups.setdefault(hash(e), [])
            for ent in lst:
                if ent[0].wrapped.IsSame(e.wrapped):
                    if not any(f.wrapped.IsSame(x.wrapped) for x in ent[1]):
                        ent[1].append(f)
                    break
            else:
                lst.append((e, [f]))
    return [ent for lst in groups.values() for ent in lst]


def _same_face(infos, f):
    for d in infos:
        if d["f"].wrapped.IsSame(f.wrapped):
            return d
    return None


def _hole_groups(infos):
    """Concave cylinders grouped by axis line + radius; total arc >= 359 deg is a hole. Returns (holes, corners)."""
    groups = []
    for d in infos:
        if d["kind"] != "cylinder" or not d["concave"]:
            continue
        for g in groups:
            h = g[0]
            off = d["loc"] - h["loc"]
            off = off - (off @ h["dir"]) * h["dir"]
            if abs(abs(d["dir"] @ h["dir"]) - 1) < ANG and np.linalg.norm(off) < TOL and abs(d["r"] - h["r"]) < TOL:
                g.append(d)
                break
        else:
            groups.append([d])
    holes = [g for g in groups if sum(x["arc"] for x in g) >= 359.0]
    corners = [g for g in groups if sum(x["arc"] for x in g) < 359.0]
    return holes, corners


def _normals_perp(f, n, k=6):
    """Sampled normals of a free-form face all perpendicular to n."""
    for u in np.linspace(0.1, 0.9, k):
        for v in (0.25, 0.75):
            if abs(_unit(_v(f.normal_at(f.position_at(u, v)))) @ n) > 1e-3:
                return False
    return True


def _concave_edge(solid, e, f1, f2, eps=0.02):
    mid = e.position_at(0.5)
    n1, n2 = _unit(_v(f1.normal_at(mid))), _unit(_v(f2.normal_at(mid)))
    if abs(n1 @ n2) > 1 - 1e-6:
        return None
    p = _v(mid) + eps * (n1 - n2)
    q = _v(mid) + eps * (n2 - n1)
    return _inside(solid, p) and _inside(solid, q), n1, n2


def _inside(solid, p):
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_IN

    return BRepClass3d_SolidClassifier(solid.wrapped, gp_Pnt(*map(float, p)), 1e-6).State() == TopAbs_IN


def _secondary(p):
    s = p._extra.get("secondary_ops") or []
    return {str(x).lower() for x in s}


# ---------------------------------------------------------------- per-process analysis (part frame)
def analyse_sheet_cut(solid, material, kerf, secondary):
    """Returns (problems, info). problems: list of (severity, id, text)."""
    probs = []
    infos = [face_info(f) for f in solid.faces()]
    planes = [d for d in infos if d["kind"] == "plane"]
    if not planes:
        return [(BLOCKER, "process.geometry", "no planar faces: not a flat plate")], {}
    big = max(planes, key=lambda d: d["area"])
    n = big["n"]
    caps = [d for d in planes if abs(abs(d["n"] @ n) - 1) < ANG]
    bad = {}
    for d in infos:
        k = d["kind"]
        if k == "plane":
            if abs(abs(d["n"] @ n) - 1) < ANG or abs(d["n"] @ n) < ANG:
                continue
            bad.setdefault("chamfer", []).append(d)
        elif k == "cylinder":
            if abs(abs(d["dir"] @ n) - 1) < ANG:
                continue
            bad.setdefault("3d", []).append(d)
        elif k == "cone":
            bad.setdefault("countersink", []).append(d)
        elif k == "other":
            if not _normals_perp(d["f"], n):
                bad.setdefault("3d", []).append(d)
        else:
            bad.setdefault("3d", []).append(d)
    levels = sorted({round(float(d["c"] @ n), 2) for d in caps})
    lv = []
    for x in levels:
        if not lv or x - lv[-1] > TOL:
            lv.append(x)
    t = lv[-1] - lv[0] if lv else 0.0
    info = {"t": t, "n": n, "levels": lv}
    if len(lv) > 2 and "pocket" not in secondary:
        probs.append((BLOCKER, "process.geometry",
                      f"{len(lv)} planar levels along the plate normal ({', '.join(f'{x - lv[0]:.2f}' for x in lv)} mm): "
                      "a blind pocket, step or a feature standing proud of the plate; a cut part has exactly two faces"))
    if bad.get("3d"):
        a = sum(d["area"] for d in bad["3d"])
        probs.append((BLOCKER, "process.geometry",
                      f"{len(bad['3d'])} face(s) ({a:.0f} mm2) are neither the two plate faces nor walls perpendicular to "
                      "them: 3D features (bumps, drum surfaces, raised teeth) cannot be laser/waterjet cut"))
    if bad.get("chamfer"):
        t_est = abs(float((caps[0]["c"] - big["c"]) @ n)) if len(caps) > 1 else 0.0
        t_est = max(t_est, max((abs(float((d["c"] - big["c"]) @ n)) for d in caps), default=0.0))
        bent = [d for d in bad["chamfer"]
                if d["area"] / max(sum(x.length for x in d["f"].edges()), 1e-9) > 0.75 * max(t_est, 1e-3)]
        if bent:
            probs.append((BLOCKER, "process.geometry", f"{len(bent)} broad face(s) at an angle to the plate: an angled "
                          "flange / bend, not a flat cut part; declare `process: sheet_bent` with cylindrical bends or "
                          "split into flat parts"))
            bad["chamfer"] = [d for d in bad["chamfer"] if not any(d is x for x in bent)]
    if bad.get("chamfer") and "chamfer" not in secondary:
        probs.append((BLOCKER, "process.geometry", f"{len(bad['chamfer'])} oblique planar face(s): chamfer/bevel; "
                      "declare `secondary_ops: [\"chamfer\"]` or remove"))
    if bad.get("countersink") and "countersink" not in secondary:
        probs.append((BLOCKER, "process.geometry", f"{len(bad['countersink'])} conical face(s): countersink; "
                      "declare `secondary_ops: [\"countersink\"]` or use pan heads"))
    if len(lv) < 2:
        probs.append((BLOCKER, "process.geometry", "no pair of parallel plate faces"))
        return probs, info
    # Stock gauge.
    fam = catalog.sheet_family(material)
    if fam is None:
        info["no_stock"] = f"material `{material}` has no sheet stock table"
    else:
        stock = catalog.SHEET_STOCK_MM[fam]
        if not any(abs(t - s) <= TOL for s in stock):
            near = min(stock, key=lambda s: abs(s - t))
            probs.append((BLOCKER, "mfg.stock", f"thickness {t:.2f} mm is not a stock {fam} gauge "
                          f"({', '.join(f'{s:g}' for s in stock)}); nearest {near:g} mm"))
    # Holes and corner radii.
    holes, corners = _hole_groups(infos)
    hmin = t if fam in catalog.HARD_SHEET else 0.5 * t
    small = [g[0]["r"] * 2 for g in holes if g[0]["r"] * 2 < hmin - TOL]
    if small:
        probs.append((BLOCKER, "process.geometry", f"{len(small)} hole(s) of dia {min(small):.2f} mm < {hmin:.2f} mm "
                      f"({'1' if fam in catalog.HARD_SHEET else '0.5'} x thickness): cut holes that small distort or "
                      "do not pierce; drill/ream them as a secondary op or enlarge"))
    tight = [g[0]["r"] for g in corners if g[0]["r"] < kerf - 1e-6]
    if tight:
        probs.append((BLOCKER, "process.geometry", f"{len(tight)} internal corner radius {min(tight):.2f} mm < kerf "
                      f"{kerf:g} mm"))
    sharp = 0
    for e, fl in edge_faces(solid):
        if len(fl) != 2 or e.geom_type.name != "LINE":
            continue
        dirn = _unit(_v(e.position_at(1)) - _v(e.position_at(0)))
        if abs(abs(dirn @ n) - 1) > ANG:
            continue
        r = _concave_edge(solid, e, fl[0], fl[1])
        if r and r[0]:
            sharp += 1
    if sharp:
        probs.append((BLOCKER, "process.geometry", f"{sharp} sharp internal corner(s): radius 0 < kerf {kerf:g} mm "
                      "(add a fillet >= kerf or the mating part will not seat)"))
    # Web between features (between distinct profile loops of one cap).
    top = max((d for d in caps if abs(float(d["c"] @ n) - lv[-1]) < TOL), key=lambda d: d["area"])
    wires = top["f"].wires()
    if len(wires) > 1:
        web = min(wires[i].distance_to(wires[j]) for i in range(len(wires)) for j in range(i + 1, len(wires)))
        info["web"] = web
        if web < t - TOL:
            probs.append((BLOCKER, "process.geometry", f"thinnest web between cut features is {web:.2f} mm < "
                          f"thickness {t:.2f} mm"))
    info["holes"] = len(holes)
    return probs, info


def analyse_sheet_bent(solid, material, secondary):
    probs = []
    infos = [face_info(f) for f in solid.faces()]
    others = [d for d in infos if d["kind"] not in ("plane", "cylinder")]
    if others:
        probs.append((BLOCKER, "process.geometry", f"{len(others)} face(s) neither planar nor cylindrical: not unfoldable"))
    planes = [d for d in infos if d["kind"] == "plane"]
    if not planes:
        return probs + [(BLOCKER, "process.geometry", "no planar faces")], {}
    big = max(planes, key=lambda d: d["area"])
    seps = [abs(float((d["c"] - big["c"]) @ big["n"])) for d in planes if d["n"] @ big["n"] < -1 + ANG]
    seps = [s for s in seps if s > 0.05]
    if not seps:
        return probs + [(BLOCKER, "process.geometry", "no opposite face to the largest face: thickness undefined")], {}
    t = min(seps)
    info = {"t": t}
    fam = catalog.sheet_family(material)
    if fam is None:
        info["no_stock"] = f"material `{material}` has no sheet stock table"
    elif not any(abs(t - s) <= TOL for s in catalog.SHEET_STOCK_MM[fam]):
        probs.append((BLOCKER, "mfg.stock", f"thickness {t:.2f} mm is not a stock {fam} gauge"))
    k = catalog.BEND_MIN_R_OVER_T.get(fam, 1.0)
    holes, _ = _hole_groups(infos)
    # Bends: cylinders longer than the thickness along their axis, not holes.
    hole_faces = [d["f"] for g in holes for d in g]
    bends = []
    for d in infos:
        if d["kind"] != "cylinder" or any(d["f"].wrapped.IsSame(h.wrapped) for h in hole_faces):
            continue
        if d["len"] <= 1.5 * t:
            continue  # a profile corner round, not a bend
        for g in bends:
            h = g[0]
            off = d["loc"] - h["loc"]
            off = off - (off @ h["dir"]) * h["dir"]
            if abs(abs(d["dir"] @ h["dir"]) - 1) < ANG and np.linalg.norm(off) < 0.05:
                g.append(d)
                break
        else:
            bends.append([d])
    ef = edge_faces(solid)
    info["bends"] = len(bends)
    for g in bends:
        radii = sorted({round(x["r"], 3) for x in g})
        rin = radii[0]
        if not any(abs(r - rin - t) < 0.05 for r in radii[1:]):
            probs.append((BLOCKER, "process.geometry", f"bend at r {rin:.2f} has no matching outer radius r+t: "
                          "thickness not constant through the bend"))
        if rin < k * t - TOL:
            probs.append((BLOCKER, "process.geometry", f"inside bend radius {rin:.2f} mm < {k:g} x t = {k * t:.2f} mm"))
        # Flanges: planar faces sharing an edge with the bend.
        ax = g[0]["dir"]
        for e, fl in ef:
            if not any(any(f.wrapped.IsSame(x["f"].wrapped) for x in g) for f in fl):
                continue
            for f in fl:
                d = _same_face(infos, f)
                if d is None or d["kind"] != "plane" or abs(d["n"] @ ax) > ANG:
                    continue
                dirn = _unit(np.cross(d["n"], ax))
                vs = np.array([_v(x) for x in f.vertices()])
                ln = float((vs @ dirn).max() - (vs @ dirn).min())
                need = 3 * t + rin
                if ln < need - TOL:
                    probs.append((BLOCKER, "process.geometry", f"flange {ln:.2f} mm < 3t + r = {need:.2f} mm"))
        for hg in holes:
            dist = min(hg[0]["f"].distance_to(x["f"]) for x in g)
            if dist < 2 * t - TOL:
                probs.append((BLOCKER, "process.geometry", f"hole dia {2 * hg[0]['r']:.2f} is {dist:.2f} mm from a bend "
                              f"(< 2t = {2 * t:.2f} mm): it will distort"))
    # Sharp bends: two broad planar faces meeting at an angle along an edge.
    sharp = 0
    for e, fl in ef:
        if len(fl) != 2:
            continue
        ds = [_same_face(infos, f) for f in fl]
        if any(d is None or d["kind"] != "plane" for d in ds):
            continue
        if abs(abs(ds[0]["n"] @ ds[1]["n"]) - 1) < ANG:
            continue
        broad = [d["area"] / max(sum(x.length for x in d["f"].edges()), 1e-9) > 0.75 * t for d in ds]
        if all(broad):
            sharp += 1
    if sharp:
        probs.append((BLOCKER, "process.geometry", f"{sharp} sharp bend edge(s) (inside radius 0 < {k:g} x t): "
                      "model the bend as a cylindrical fold"))
    return probs, info


def analyse_turned(solid, secondary):
    probs = []
    infos = [face_info(f) for f in solid.faces()]
    rev = [d for d in infos if d["kind"] in ("cylinder", "cone", "torus")]
    if not rev:
        return [(BLOCKER, "process.geometry", "no surface of revolution: nothing a lathe makes")], {}
    main = max(rev, key=lambda d: d["area"])
    a, o = main["dir"], main["loc"]

    def on_axis(p):
        q = p - o
        return np.linalg.norm(q - (q @ a) * a) < TOL

    found = {}
    for d in infos:
        k = d["kind"]
        if k in ("cylinder", "cone", "torus"):
            if abs(abs(d["dir"] @ a) - 1) < ANG and on_axis(d["loc"]):
                continue
            if k == "cylinder" and abs(d["dir"] @ a) < ANG:
                found.setdefault("cross_hole", []).append(d)
            elif k == "cylinder" and abs(abs(d["dir"] @ a) - 1) < ANG:
                found.setdefault("drilled", []).append(d)
            else:
                found.setdefault("3d", []).append(d)
        elif k == "plane":
            if abs(abs(d["n"] @ a) - 1) < ANG:
                continue
            if abs(d["n"] @ a) < ANG:
                found.setdefault("flat", []).append(d)
            else:
                found.setdefault("3d", []).append(d)
        elif k == "sphere":
            if not on_axis(d["loc"]):
                found.setdefault("3d", []).append(d)
        else:
            found.setdefault("3d", []).append(d)
    for key, fs in found.items():
        if key == "3d":
            probs.append((BLOCKER, "process.geometry", f"{len(fs)} face(s) not about the turning axis and not a flat, "
                          "keyway or cross hole"))
        elif key == "flat" and not ({"flat", "keyway"} & secondary):
            probs.append((BLOCKER, "process.geometry", f"{len(fs)} flat face(s) along the axis: declare "
                          "`secondary_ops: [\"flat\"]` (or keyway) or remove"))
        elif key in ("cross_hole", "drilled") and key not in secondary:
            probs.append((BLOCKER, "process.geometry", f"{len(fs)} {key.replace('_', ' ')} face(s): declare "
                          f"`secondary_ops: [\"{key}\"]`"))
    return probs, {"axis": a}


def analyse_milled(solid, mesh, secondary):
    probs = []
    infos = [face_info(f) for f in solid.faces()]
    holes, corners = _hole_groups(infos)
    tight = [g[0]["r"] for g in corners if g[0]["r"] < catalog.MILL_MIN_TOOL_RADIUS_MM - 1e-6]
    if tight:
        probs.append((BLOCKER, "process.geometry", f"{len(tight)} internal corner radius {min(tight):.2f} mm < "
                      f"{catalog.MILL_MIN_TOOL_RADIUS_MM:g} mm tool radius"))

    def escapes(p, d):
        return not bool(mesh.ray.intersects_any(np.array([p]), np.array([d]))[0])

    sharp = 0
    for e, fl in edge_faces(solid):
        if len(fl) != 2 or e.geom_type.name != "LINE":
            continue
        r = _concave_edge(solid, e, fl[0], fl[1])
        if not r or not r[0]:
            continue
        _, n1, n2 = r
        mid = _v(e.position_at(0.5))
        good = False
        for nn in (n1, n2):
            for ax in AXES:
                if nn @ ax > 1 - ANG and escapes(mid + 0.05 * (n1 + n2), ax):
                    good = True
        if not good:
            sharp += 1
    if sharp:
        probs.append((BLOCKER, "process.geometry", f"{sharp} sharp internal corner(s) parallel to every reachable tool "
                      f"axis: an end mill leaves r >= {catalog.MILL_MIN_TOOL_RADIUS_MM:g} mm there"))
    blocked = 0
    for d in infos:
        f = d["f"]
        try:
            verts, tris = f.tessellate(0.2)
        except Exception:  # noqa: BLE001
            continue
        if not tris:
            continue
        V = np.array([_v(x) for x in verts])
        pts = [V[list(t)].mean(axis=0) for t in tris[:: max(len(tris) // 4, 1)]][:5]
        reach = False
        for p in pts:
            n = _unit(_v(f.normal_at(f.project_to_surface(p) if hasattr(f, "project_to_surface") else p)))
            for ax in AXES:
                if n @ ax >= -1e-6 and escapes(p + 0.02 * n, ax):
                    reach = True
                    break
            if reach:
                break
        if not reach:
            blocked += 1
    if blocked:
        probs.append((BLOCKER, "process.geometry", f"{blocked} face(s) unreachable along +-X/Y/Z: undercut"))
    return probs, {}


# ---------------------------------------------------------------- cots stock
def check_cots(p, g):
    """(ok, text) for a bought part with free geometry."""
    lo, hi = g.bounds
    s = sorted(float(x) for x in hi - lo)
    if p.kind == "bearing":
        txt = f"{p.label or ''} {p._extra.get('stock') or ''}".lower()
        for des, (bore, od, w) in catalog.BEARINGS.items():
            if des in txt.replace("zz", " ").replace("2rs", " ").split() or f"{des}zz" in txt or f"{des} " in txt + " ":
                if abs(s[1] - od) < 0.1 and abs(s[2] - od) < 0.1 and abs(s[0] - w) < 0.1:
                    return True, f"bearing {des.upper()} {bore:g}x{od:g}x{w:g}"
                return False, f"drawn {s[1]:.1f} x {s[0]:.1f} mm does not match bearing {des.upper()} ({od:g} x {w:g})"
        return False, "bearing with no known designation (684, MR84, ...) in its label or `stock`"
    if p.kind == "belt" and p.belt is not None and p.belt.kind == "o_ring" and p.belt.length_mm and p.belt.width_mm:
        return True, f"O-ring {p.belt.width_mm:g} x {p.belt.length_mm:g} mm"
    fam = catalog.sheet_family(p.material)
    rods = catalog.ROD_STOCK_MM.get(fam if fam != "spring_steel" else "steel")
    if rods and abs(s[0] - s[1]) < 0.05 and s[2] > s[1]:
        if any(abs(s[0] - d) < 0.05 for d in rods):
            return True, f"{s[0]:g} mm {fam} rod cut to {s[2]:.1f} mm"
        return False, f"{s[0]:.2f} mm is not a stock {fam} rod diameter ({', '.join(f'{d:g}' for d in rods)})"
    return False, "bought part with free geometry and no catalog SKU or stock rod/bearing match"


# ---------------------------------------------------------------- group
def _check_part(rp, process_raw, canon, ctx):
    p, g = rp.part, rp.geom
    sec = _secondary(p)
    solid = g.solid if g is not None else None
    if solid is None:
        ctx.not_checked.append(f"Process geometry of `{p.id}` ({process_raw}): no B-rep")
        return []
    if canon == "sheet_cut":
        kerf = catalog.KERF_MM.get(str(process_raw).lower(), 0.5)
        return analyse_sheet_cut(solid, p.material, kerf, sec)
    if canon == "sheet_bent":
        return analyse_sheet_bent(solid, p.material, sec)
    if canon == "turned":
        return analyse_turned(solid, sec)
    if canon == "milled":
        return analyse_milled(solid, g.mesh, sec)
    return [], {}


FIX = {
    "sheet_cut": "Make it one 2D profile extruded to one stock thickness (teeth part of the outline), or change `process`.",
    "sheet_bent": "Model it as a constant-thickness sheet with cylindrical bends (r >= k t), flanges >= 3t + r.",
    "turned": "Keep it axisymmetric; declare flats/keyways/cross holes in `secondary_ops`, or change `process`.",
    "milled": "Add >= 1 mm radii in internal corners; remove undercuts or split the part.",
}


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    n_ok = 0
    by_id = {rp.part.id: rp for rp in r.parts}
    for rp in r.parts:
        p = rp.part
        if p.catalog is not None or p.kind in ELECTRONIC:
            continue
        raw = p.process
        canon = catalog.process_canon(raw)
        if raw is None:
            out.append(fail("process.undeclared", G, BLOCKER, "Process undeclared",
                            f"`{p.id}` is a made part with no `process`.").on(p.id)
                       .fix("Set `process`: fdm, sla, laser/waterjet (sheet_cut), sheet_bent, turned, milled, cots, "
                            "molded or cast."))
            continue
        if canon is None:
            out.append(fail("process.unknown", G, BLOCKER, "Unknown process", f"`{p.id}`: process `{raw}` is unknown.")
                       .on(p.id).fix("Use one of: " + ", ".join(sorted(set(catalog.PROCESS_ALIASES)))))
            continue
        if p.kind == "weapon" and canon in ("fdm", "sla"):
            teeth = [q.part.id for q in r.parts if q.part.id != p.id and (q.part.parent == p.id or q.part.fused_with == p.id)
                     and catalog.sheet_family(q.part.material) in catalog.HARD_SHEET]
            if not teeth:
                out.append(fail("process.weapon_printed", G, BLOCKER, "Printed weapon",
                                f"Weapon `{p.id}` is {raw}-printed with no hardened metal insert teeth.").on(p.id)
                           .fix("Make it metal (sheet_cut / turned / milled) or add hardened steel tooth parts "
                                "(`parent` = the weapon)."))
        if canon in ("fdm", "sla"):
            po = p._extra.get("print_orientation")
            if po is None:
                out.append(fail("process.print_orientation", G, BLOCKER, "Print orientation undeclared",
                                f"`{p.id}` ({raw}) has no `print_orientation`.").on(p.id)
                           .fix("Add `print_orientation`: the part-frame axis pointing up from the bed (+x/-x/+y/-y/+z/-z)."))
            elif str(po).lower() not in ORIENT:
                out.append(fail("process.print_orientation", G, BLOCKER, "Print orientation invalid",
                                f"`{p.id}`: `{po}` is not one of +x/-x/+y/-y/+z/-z.").on(p.id))
            else:
                n_ok += 1
            continue  # geometry: mfg / printability
        if canon in ("molded", "cast"):
            ctx.not_checked.append(f"Process geometry of `{p.id}` ({raw}): draft/parting line not checked")
            continue
        if canon == "cots":
            if rp.geom is None:
                ctx.not_checked.append(f"Stock of bought `{p.id}`: no geometry")
                continue
            good, txt = check_cots(p, rp.geom)
            if good:
                n_ok += 1
            else:
                out.append(fail("mfg.stock", G, BLOCKER, "Bought part has no stock match", f"`{p.id}`: {txt}.").on(p.id)
                           .fix("Use a catalog part, or size it to a stock rod/bearing and name it in `stock`."))
            continue
        try:
            probs, info = _check_part(rp, raw, canon, ctx)
        except Exception as e:  # noqa: BLE001 - fail closed per part
            out.append(fail("process.geometry", G, BLOCKER, "Process geometry not evaluable",
                            f"`{p.id}` ({raw}): {type(e).__name__}: {e}").on(p.id))
            ctx.not_checked.append(f"Process geometry of `{p.id}`: {type(e).__name__}")
            continue
        if info.get("no_stock"):
            ctx.not_checked.append(f"Stock gauge of `{p.id}`: {info['no_stock']}")
        for sev, fid, txt in probs:
            out.append(fail(fid, G, sev, f"Not makeable as {canon}", f"`{p.id}` ({raw}): {txt}.").on(p.id)
                       .fix(FIX.get(canon, "")))
        if not probs:
            n_ok += 1
    out.extend(layer_load(ctx, by_id))
    if n_ok:
        out.append(ok("process.ok", G, "Geometry matches the process", f"{n_ok} part(s) are makeable as declared."))
    ctx.not_checked.append("Process: single-profile neck width (web inside one outline), bent-part flat-pattern unfold "
                           "and fdm overhangs per declared orientation are not checked here")
    return out


def layer_load(ctx, by_id):
    """FDM parts that carry the weapon axle must be printed with the spin axis along the build direction, so the radial
    impact load lies in the layer plane instead of peeling layers apart."""
    from .power import spin_axis

    r, w = ctx.r, ctx.world
    out = []
    for i, b in enumerate(w.bodies):
        if b.part_idx is None:
            continue
        wp = r.parts[b.part_idx].part
        if wp.kind != "weapon" or wp.weapon is None:
            continue
        sa = spin_axis(w, r, i)
        if sa is None:
            continue
        o, a = sa
        span = (b.mesh.vertices - o) @ a
        lo, hi = span.min() - 25.0, span.max() + 25.0
        for j, s in enumerate(w.bodies):
            if s.part_idx is None or j == i:
                continue
            sp = r.parts[s.part_idx].part
            if sp.catalog is not None or catalog.process_canon(sp.process) not in ("fdm", "sla"):
                continue
            q = s.mesh.vertices - o
            t = q @ a
            rad = np.linalg.norm(q - np.outer(t, a), axis=1)
            if not np.any((rad < 8.0) & (t > lo) & (t < hi)):
                continue
            po = str(sp._extra.get("print_orientation") or "").lower()
            if po not in ORIENT:
                ctx.not_checked.append(f"Layer direction of weapon support `{sp.id}`: no valid print_orientation")
                continue
            up = _unit(s.M[:3, :3] @ AXES[ORIENT[po]])
            if abs(up @ a) < 0.9:
                out.append(fail("mfg.layer_load", G, BLOCKER, "Weapon support printed across its layers",
                                f"`{sp.id}` carries the `{wp.id}` axle but is printed with build direction {po} "
                                f"(world {np.round(up, 2).tolist()}), not along the spin axis "
                                f"{np.round(a, 2).tolist()}: impact load peels layers apart.").on(sp.id, wp.id)
                           .fix("Print it lying flat so the spin axis is the build direction, or make it a cut metal plate."))
            else:
                out.append(ok("mfg.layer_load", G, "Weapon support layers carry the hit",
                              f"`{sp.id}` is printed along the spin axis."))
    return out


# ---------------------------------------------------------------- DXF export
def export_dxf(r, out_dir):
    """Write dxf/<part>.dxf for every sheet_cut part (its profile in the plate plane). Returns (files, failures)."""
    import build123d as bd

    files, fails = [], []
    d = Path(out_dir) / "dxf"
    for rp in r.parts:
        p = rp.part
        canon = catalog.process_canon(p.process)
        if p.catalog is not None or canon not in ("sheet_cut", "sheet_bent"):
            continue
        try:
            if canon == "sheet_bent":
                raise NotImplementedError("flat-pattern unfold of bent parts is not implemented; supply the DXF")
            solid = rp.geom.solid if rp.geom is not None else None
            if solid is None:
                raise ValueError("no B-rep")
            probs, info = analyse_sheet_cut(solid, p.material, 0.0, _secondary(p))
            geo = [x for x in probs if x[1] == "process.geometry"]
            if geo:
                raise ValueError("not a 2D profile: " + geo[0][2])
            n = info["n"]
            infos = [face_info(f) for f in solid.faces()]
            cap = max((x for x in infos if x["kind"] == "plane" and x["n"] @ n < -1 + ANG), key=lambda x: x["area"])
            pl = bd.Plane(origin=tuple(cap["c"]), z_dir=tuple(-cap["n"]))
            flat = pl.to_local_coords(cap["f"])
            d.mkdir(parents=True, exist_ok=True)
            exp = bd.ExportDXF()
            exp.add_layer("cut")
            exp.add_shape(flat.wires(), layer="cut")
            name = "".join(c if c.isalnum() or c in "-_" else "_" for c in p.id)
            exp.write(str(d / f"{name}.dxf"))
            files.append(f"dxf/{name}.dxf")
        except Exception as e:  # noqa: BLE001
            fails.append((p.id, f"{type(e).__name__}: {e}"))
    return files, fails


def export_findings(fails):
    return [fail("mfg.export", G, BLOCKER, "No flat pattern", f"DXF for `{pid}` could not be made: {why}").on(pid)
            .fix("Make the part a true 2D profile (or bent sheet with an unfoldable pattern) and re-export.")
            for pid, why in fails]

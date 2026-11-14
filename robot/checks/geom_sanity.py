"""B-rep / mesh hygiene of every MADE part (`geom` group, module geom_sanity): what LLM-written CAD typically gets
wrong, judged on the part alone (no reference, no other part). Catalog parts (rp.cat is not None) are skipped.

  geom.tiny_edge           B-rep edges shorter than min_edge_mm (0.05): leftovers of near-miss booleans. WARNING;
                           BLOCKER when one part has more than max_tiny_edges (10).
  geom.sliver_face         B-rep faces (area > 0) whose narrow width 2 * area / perimeter is below min_face_width_mm
                           (0.05), or whose area / perimeter^2 is below min_face_ratio (2e-4) while narrower than
                           4 x min_face_width_mm (a long plate edge or chamfer is thin in ratio but not a sliver). WARNING.
  geom.near_coplanar_step  two parallel planar faces facing the same way, adjacent or overlapping (boxes within
                           adjacent_mm 0.5), offset by 0 < d < min_step_mm (0.1): a face meant flush. WARNING.
  geom.near_miss_hole      two cylindrical faces (arc >= 120 deg, so not fillets) with parallel axes offset by
                           0 < d < min_axis_miss_mm (0.1) that overlap or touch along the axis: a counterbore / through
                           hole pair that is not concentric. BLOCKER.
  geom.open_shell          mesh edges not shared by exactly two triangles. `integrity.solids` already blocks on an open
                           or inconsistently wound shell, so this id is judged ONLY when the spec opted out of
                           `integrity`; otherwise it is skipped (no finding, nothing passed here). BLOCKER.
  geom.zero_thickness      a bounding-box extent below min_extent_mm (0.2) on a non-sheet part, or volume / bounding-box
                           volume below min_fill (0.5 %): a part that booleaned itself away. BLOCKER.
  geom.off_axis_face       planar faces whose normal is 0 < angle < max_skew_deg (0.5) off a part axis (X, Y, Z of the
                           part frame): a rotation typed 89.5, a loft off by a hair. WARNING.
  (geom.disconnected_feature is not here: more than one solid / lump per part is `integrity.solids`.)

Thresholds: spec `review.geom` {..., reason} (clamped to BOUNDS). Per-part opt out: `geom_ok: {"<check suffix>":
"<reason, >= 20 chars>"}`, e.g. {"off_axis_face": "0.3 deg draft on the pocket walls for demoulding"}.
Fail closed: a part with only a mesh (no B-rep), whose geometry failed to load, or with a face that cannot be read
is listed in ctx.not_checked for the affected check and gets no pass for it.
Cheap (inner tier): loops over faces and edges with numpy; no booleans, no rays.

Differs from visual.sliver / visual.faceting: those work on the tessellated MESH (coplanar triangle groups), need a
`reference_cad` entry and only report what the reference does not also have (parity, nightly). The checks here read
the exact B-rep faces and edges, need no reference and run on every made part.
"""

from __future__ import annotations

import math

import numpy as np

from ..finding import BLOCKER, WARNING, fail, note, ok
from ._review import BOUNDS as _RB
from ._review import override_findings, params

G = "geom"
DEFAULTS = {"min_edge_mm": 0.05, "max_tiny_edges": 10, "min_face_width_mm": 0.05, "min_face_ratio": 2e-4,
            "min_step_mm": 0.1, "min_axis_miss_mm": 0.1, "adjacent_mm": 0.5, "min_extent_mm": 0.2, "min_fill": 0.005,
            "max_skew_deg": 0.5, "max_listed": 5}
BOUNDS = {"min_edge_mm": (0.005, 0.5), "max_tiny_edges": (0, 100), "min_face_width_mm": (0.005, 0.5),
          "min_face_ratio": (1e-5, 1e-3), "min_step_mm": (0.01, 0.5), "min_axis_miss_mm": (0.01, 0.5),
          "adjacent_mm": (0.0, 2.0), "min_extent_mm": (0.05, 1.0), "min_fill": (0.0005, 0.05),
          "max_skew_deg": (0.05, 2.0), "max_listed": (1, 20)}
_RB.setdefault("geom", BOUNDS)

BREP_CHECKS = ("tiny_edge", "sliver_face", "near_coplanar_step", "near_miss_hole", "off_axis_face")
MESH_CHECKS = ("open_shell", "zero_thickness")
CHECKS = BREP_CHECKS + MESH_CHECKS
MIN_REASON = 20
SHEET = ("sheet_cut", "sheet_bent")

ZERO_LEN = 1e-7      # an edge this short is a degenerate one (sphere pole, cone apex), not a modelling leftover
ZERO_AREA = 1e-9     # mm2; "area > 0"
PAR_COS = 1 - 1e-6   # planes / axes within ~0.08 deg count as parallel
STEP_EPS = 1e-4      # mm; offsets below this are the same plane / the same axis (numeric noise)
SKEW_EPS_DEG = 1e-3  # a normal this close to an axis is on it
MIN_ARC_DEG = 120.0  # a cylinder face under this arc is a fillet / corner round, not a hole or boss
MIN_SKEW_AREA = 0.01  # mm2; smaller faces are slivers (reported as such), their normal is noise

TITLE_OK = {"tiny_edge": "No tiny edges", "sliver_face": "No sliver faces", "near_coplanar_step": "No near-flush steps",
            "near_miss_hole": "Coaxial holes are concentric", "off_axis_face": "No slightly skewed faces",
            "open_shell": "Mesh is closed and manifold", "zero_thickness": "Parts have real thickness and volume"}


class NotJudged(Exception):
    """A check that could not be judged on this part (goes to NOT CHECKED, never a pass)."""


def opted(p, check):
    """Reason string when part `p` opts `check` (suffix, e.g. "tiny_edge") out with a usable reason, else None."""
    ok_ = (getattr(p, "_extra", None) or {}).get("geom_ok") or {}
    why = str(ok_.get(check) or "").strip() if isinstance(ok_, dict) else ""
    return why if len(why) >= MIN_REASON else None


# ------------------------------------------------------------------------------------------------ B-rep readers
def _v(x):
    from .process import _v as pv

    return pv(x)


def _degenerate(e) -> bool:
    try:
        from OCP.BRep import BRep_Tool

        return bool(BRep_Tool.Degenerated_s(e.wrapped))
    except Exception:  # noqa: BLE001 - the length test below still drops zero-length edges
        return False


def _face_box(f):
    """(2, 3) bounding box of a face."""
    bb = f.bounding_box()
    return np.array([[bb.min.X, bb.min.Y, bb.min.Z], [bb.max.X, bb.max.Y, bb.max.Z]], float)


def _face_centre(f):
    try:
        return _v(f.center())
    except Exception:  # noqa: BLE001
        return _face_box(f).mean(axis=0)


def read_faces(shape):
    """(infos, unreadable): process.face_info of every face of the shape (kind, area, n / c for planes, dir / loc / r
    / arc for cylinders), and how many faces could not be read."""
    from .process import face_info

    infos, bad = [], 0
    for f in shape.faces():
        try:
            infos.append(face_info(f))
        except Exception:  # noqa: BLE001 - counted, so the caller does not pass what it did not read
            bad += 1
    return infos, bad


# ------------------------------------------------------------------------------------------------ pure checks
def tiny_edges(shape, min_len=0.05):
    """[(midpoint (3,), length mm)] of the non-degenerate B-rep edges shorter than `min_len`, shortest first."""
    out = []
    for e in shape.edges():
        L = float(e.length)
        if L >= min_len or L <= ZERO_LEN or _degenerate(e):
            continue
        out.append((_v(e.position_at(0.5)), L))
    return sorted(out, key=lambda x: x[1])


def face_width(area, perimeter):
    """(narrow width mm = 2 * area / perimeter, compactness = area / perimeter^2) of a face. A w x L strip gives
    ~w and ~w / (4 L); a square gives side / 2 and 1 / 16."""
    if perimeter <= 0:
        return math.inf, math.inf
    return 2.0 * area / perimeter, area / (perimeter * perimeter)


def sliver_faces(shape, min_width=0.05, min_ratio=2e-4):
    """[(centre (3,), area mm2, width mm, ratio)] of the faces with area > 0 that are needle-thin, narrowest first:
    width < min_width, or ratio < min_ratio while width < 4 * min_width. A face with no boundary (a whole sphere) is
    never a sliver."""
    out = []
    for f in shape.faces():
        a = float(f.area)
        if a <= ZERO_AREA:
            continue
        per = float(sum(e.length for e in f.edges()))
        w, ratio = face_width(a, per)
        if w < min_width or (ratio < min_ratio and w < 4.0 * min_width):
            out.append((_face_centre(f), a, float(w), float(ratio)))
    return sorted(out, key=lambda x: x[2])


def near_coplanar_steps(shape, min_step=0.1, adjacent=0.5, infos=None):
    """[(centre of the smaller face (3,), offset mm, its area mm2)] for every pair of parallel planar faces facing the
    same way whose planes are 0 < d < min_step apart and whose boxes overlap or lie within `adjacent` mm, smallest
    offset first."""
    if infos is None:
        infos, _ = read_faces(shape)
    P = [d for d in infos if d["kind"] == "plane" and d["area"] > ZERO_AREA]
    if len(P) < 2:
        return []
    N = np.array([d["n"] for d in P], float)
    C = np.array([d["c"] for d in P], float)
    boxes = {}

    def box(i):
        if i not in boxes:
            boxes[i] = _face_box(P[i]["f"])
        return boxes[i]

    out = []
    for i in range(len(P) - 1):
        dv = C[i + 1:] - C[i]
        off = np.abs(dv @ N[i])
        cand = np.nonzero(((N[i + 1:] @ N[i]) > PAR_COS) & (off > STEP_EPS) & (off < min_step))[0]
        for c in cand:
            j = i + 1 + int(c)
            # two planes a hair off parallel: their offset is only known to L * sin(tilt), so it must clear that
            tilt = float(np.linalg.norm(np.cross(N[i], N[j]))) * float(np.linalg.norm(dv[c]))
            if off[c] <= STEP_EPS + 2.0 * tilt:
                continue
            bi, bj = box(i), box(j)
            if np.all(bi[0] - adjacent <= bj[1]) and np.all(bj[0] - adjacent <= bi[1]):
                k = i if P[i]["area"] <= P[j]["area"] else j
                out.append((C[k].copy(), float(off[c]), float(P[k]["area"])))
    return sorted(out, key=lambda x: x[1])


def near_miss_holes(shape, min_miss=0.1, adjacent=0.5, min_arc=MIN_ARC_DEG, infos=None):
    """[(point between the two axes (3,), axis offset mm, r1, r2)] for every pair of cylindrical faces (arc >=
    min_arc) with parallel axes 0 < d < min_miss apart whose spans along the axis overlap or come within `adjacent`
    mm, smallest offset first. One entry per place (split faces of one hole are merged)."""
    if infos is None:
        infos, _ = read_faces(shape)
    cyl = []
    for d in infos:
        if d["kind"] != "cylinder" or float(d.get("arc") or 0.0) < min_arc:
            continue
        try:
            V = np.array([_v(x) for x in d["f"].vertices()], float).reshape(-1, 3)
        except Exception:  # noqa: BLE001
            V = np.zeros((0, 3))
        if not len(V):
            V = np.asarray(d["q"], float)[None]
        cyl.append((d, V))
    if len(cyl) < 2:
        return []
    D = np.array([d["dir"] for d, _ in cyl], float)
    O = np.array([d["loc"] for d, _ in cyl], float)
    out, seen = [], set()
    for a in range(len(cyl) - 1):
        ax, loc = D[a], O[a]
        rel = O[a + 1:] - loc
        perp = rel - np.outer(rel @ ax, ax)
        miss = np.linalg.norm(perp, axis=1)
        cand = np.nonzero((np.abs(D[a + 1:] @ ax) > PAR_COS) & (miss > STEP_EPS) & (miss < min_miss))[0]
        if not len(cand):
            continue
        sa = (cyl[a][1] - loc) @ ax
        for c in cand:
            b = a + 1 + int(c)
            tilt = float(np.linalg.norm(np.cross(ax, D[b]))) * float(np.linalg.norm(rel[c]))
            if miss[c] <= STEP_EPS + 2.0 * tilt:
                continue
            sb = (cyl[b][1] - loc) @ ax
            lo, hi = max(float(sa.min()), float(sb.min())), min(float(sa.max()), float(sb.max()))
            if lo - hi > adjacent:
                continue
            at = loc + ax * ((lo + hi) / 2.0) + perp[c] / 2.0
            key = tuple(np.round(at, 2).tolist())
            if key in seen:
                continue
            seen.add(key)
            out.append((at, float(miss[c]), float(cyl[a][0]["r"]), float(cyl[b][0]["r"])))
    return sorted(out, key=lambda x: x[1])


def skew_deg(n):
    """(angle in degrees between unit normal `n` and the nearest principal axis, that axis as "X" / "Y" / "Z")."""
    n = np.asarray(n, float)
    k = int(np.argmax(np.abs(n)))
    rest = np.delete(n, k)
    return math.degrees(math.atan2(float(np.linalg.norm(rest)), abs(float(n[k])))), "XYZ"[k]


def off_axis_faces(shape, max_skew_deg=0.5, min_skew_deg=SKEW_EPS_DEG, min_area=MIN_SKEW_AREA, infos=None):
    """[(centre (3,), skew deg, nearest axis "X" / "Y" / "Z", area mm2)] of the planar faces whose normal is
    min_skew_deg < angle < max_skew_deg off a principal axis of the part frame, largest face first."""
    if infos is None:
        infos, _ = read_faces(shape)
    out = []
    for d in infos:
        if d["kind"] != "plane" or d["area"] < min_area:
            continue
        ang, axis = skew_deg(d["n"])
        if min_skew_deg < ang < max_skew_deg:
            out.append((np.asarray(d["c"], float), float(ang), axis, float(d["area"])))
    return sorted(out, key=lambda x: -x[3])


def open_edges(mesh):
    """(boundary edges, non-manifold edges, midpoint of the first bad edge or None) of a triangle mesh: edges used by
    one triangle, and edges used by more than two."""
    F = np.asarray(mesh.faces, np.int64).reshape(-1, 3)
    if not len(F):
        return 0, 0, None
    E = np.sort(np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1)
    uniq, counts = np.unique(E, axis=0, return_counts=True)
    bad = np.nonzero(counts != 2)[0]
    at = None
    if len(bad):
        V = np.asarray(mesh.vertices, float)
        at = V[uniq[bad[0]]].mean(axis=0)
    return int((counts == 1).sum()), int((counts > 2).sum()), at


def zero_thickness(extents, volume, min_extent=0.2, min_fill=0.005, sheet=False):
    """Problems [str] of a part with bounding-box `extents` (3,) and solid `volume`: an extent under `min_extent`
    (not judged for a sheet part, whose gauge is the process group's job) or volume under `min_fill` of the box."""
    ext = np.asarray(extents, float)
    out = []
    k = int(np.argmin(ext))
    if not sheet and ext[k] < min_extent:
        out.append(f"only {ext[k]:.3f} mm thick along {'XYZ'[k]} (< {min_extent:g} mm)")
    box = float(np.prod(ext))
    fill = float(volume) / box if box > 0 else 0.0
    if box > 0 and fill < min_fill:
        out.append(f"volume {float(volume):.2f} mm3 is {fill:.2%} of its {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm "
                   f"bounding box (< {min_fill:.2%})")
    elif box <= 0 and sheet:
        out.append("bounding box has no volume")
    return out


# ------------------------------------------------------------------------------------------------ group
def _matrix(world, pid):
    try:
        b = world.body(pid) if world is not None else None
    except Exception:  # noqa: BLE001
        b = None
    M = getattr(b, "M", None)
    return None if M is None else np.asarray(M, float)


def _w(M, p):
    """Part-frame point -> world (as print_orient does); the part frame itself when the part has no body."""
    p = np.asarray(p, float)
    return p if M is None else M[:3, :3] @ p + M[:3, 3]


def _locs(M, items, cap, desc):
    txt = "; ".join(f"{np.round(_w(M, it[0]), 2).tolist()} {desc(it)}" for it in items[:cap])
    return txt + (f" (+{len(items) - cap} more)" if len(items) > cap else "")


def _tiny(pid, M, shape, prm):
    items = tiny_edges(shape, prm["min_edge_mm"])
    if not items:
        return None
    n, cap = len(items), int(prm["max_listed"])
    sev = BLOCKER if n > prm["max_tiny_edges"] else WARNING
    return (fail("geom.tiny_edge", G, sev, "Tiny B-rep edges (near-miss boolean leftovers)",
                 f"`{pid}`: {n} edge(s) shorter than {prm['min_edge_mm']:g} mm, shortest {items[0][1]:.4f} mm. World mm: "
                 + _locs(M, items, cap, lambda it: f"{it[1]:.4f} mm") + ".")
            .on(pid).here(_w(M, items[0][0])).expect(f"every edge >= {prm['min_edge_mm']:g} mm", f"{n} shorter, min {items[0][1]:.4f} mm")
            .fix("Two feature boundaries miss each other by the edge length at each listed point. Drive both from ONE "
                 "parameter or the same face / plane (not two numbers that should be equal), or extend the cutting / "
                 "added body clear past the wall before the boolean, so the boundaries coincide or clearly cross."))


def _sliver(pid, M, shape, prm):
    items = sliver_faces(shape, prm["min_face_width_mm"], prm["min_face_ratio"])
    if not items:
        return None
    n, cap = len(items), int(prm["max_listed"])
    return (fail("geom.sliver_face", G, WARNING, "Sliver faces",
                 f"`{pid}`: {n} face(s) narrower than {prm['min_face_width_mm']:g} mm. World mm: "
                 + _locs(M, items, cap, lambda it: f"{it[2]:.4f} mm wide, {it[1]:.4f} mm2") + ".")
            .on(pid).here(_w(M, items[0][0])).expect(f"face width >= {prm['min_face_width_mm']:g} mm", f"{n} narrower, min {items[0][2]:.4f} mm")
            .fix("A hair-thin face is two surfaces that were meant to coincide or to be clearly apart. Make the two "
                 "sketch lines / offsets one relation (same parameter), or move the feature so the strip is either gone "
                 "or a real, makeable width."))


def _step(pid, M, shape, prm, infos):
    items = near_coplanar_steps(shape, prm["min_step_mm"], prm["adjacent_mm"], infos)
    if not items:
        return None
    n, cap = len(items), int(prm["max_listed"])
    return (fail("geom.near_coplanar_step", G, WARNING, "Faces almost flush, not quite",
                 f"`{pid}`: {n} pair(s) of parallel faces stepped by less than {prm['min_step_mm']:g} mm. World mm: "
                 + _locs(M, items, cap, lambda it: f"step {it[1]:.4f} mm") + ".")
            .on(pid).here(_w(M, items[0][0])).expect(f"flush (0) or a step >= {prm['min_step_mm']:g} mm", f"{items[0][1]:.4f} mm")
            .fix("The two faces were meant to be one plane. Build both features from the same datum (extrude `until` "
                 "the existing face, or reuse its parameter) instead of two offsets that differ by the step; if the "
                 "step is intended, make it >= the threshold or list it in the part's `geom_ok`."))


def _hole(pid, M, shape, prm, infos):
    items = near_miss_holes(shape, prm["min_axis_miss_mm"], prm["adjacent_mm"], infos=infos)
    if not items:
        return None
    n, cap = len(items), int(prm["max_listed"])
    return (fail("geom.near_miss_hole", G, BLOCKER, "Coaxial holes are not concentric",
                 f"`{pid}`: {n} pair(s) of cylinders meant coaxial have axes less than {prm['min_axis_miss_mm']:g} mm "
                 "apart but not on one line. World mm: "
                 + _locs(M, items, cap, lambda it: f"axes {it[1]:.4f} mm apart (d{2 * it[2]:.2f} / d{2 * it[3]:.2f})") + ".")
            .on(pid).here(_w(M, items[0][0])).expect("axis offset 0", f"{items[0][1]:.4f} mm")
            .fix("Place the counterbore / second bore at the SAME centre as the through hole: one centre point "
                 "(one variable or one `Pos`) used by both cuts, not two typed coordinates."))


def _skew(pid, M, shape, prm, infos):
    items = off_axis_faces(shape, prm["max_skew_deg"], infos=infos)
    if not items:
        return None
    n, cap = len(items), int(prm["max_listed"])
    worst = max(items, key=lambda it: it[1])
    return (fail("geom.off_axis_face", G, WARNING, "Faces slightly off square",
                 f"`{pid}`: {n} planar face(s) lean less than {prm['max_skew_deg']:g} deg off a part axis. World mm: "
                 + _locs(M, items, cap, lambda it: f"{it[1]:.3f} deg off {it[2]}, {it[3]:.1f} mm2") + ".")
            .on(pid).here(_w(M, items[0][0])).expect("0 deg (square) or a deliberate angle", f"up to {worst[1]:.3f} deg off {worst[2]}")
            .fix("Look for a rotation typed as 89.5 / 0.5, a loft or sweep whose ends are not aligned, or sketch points "
                 "that should share a coordinate; make the face exactly square to the part axes, or state the "
                 "deliberate draft in `geom_ok`."))


def _open(pid, M, mesh):
    nb, nm, at = open_edges(mesh)
    if not nb and not nm:
        return None
    return (fail("geom.open_shell", G, BLOCKER, "Part mesh is open or non-manifold",
                 f"`{pid}`: {nb} boundary edge(s) (used by one triangle) and {nm} edge(s) used by more than two.")
            .on(pid).here(None if at is None else _w(M, at)).expect("every edge shared by exactly 2 triangles", f"{nb} open, {nm} non-manifold")
            .fix("The solid is not closed: a face is missing or two bodies touch along an edge. Rebuild the last "
                 "boolean so the bodies overlap by a real amount (not edge-to-edge) and return one solid."))


def _thin(pid, p, M, g, mesh, prm):
    from .. import catalog

    lo, hi = (np.asarray(x, float) for x in mesh.bounds)
    vol = float(getattr(g, "volume", 0.0) or 0.0)
    if vol <= 0:
        vol = abs(float(mesh.volume))
    sheet = catalog.process_canon(getattr(p, "process", None)) in SHEET
    probs = zero_thickness(hi - lo, vol, prm["min_extent_mm"], prm["min_fill"], sheet)
    if not probs:
        return None
    return (fail("geom.zero_thickness", G, BLOCKER, "Part has (almost) no thickness or volume",
                 f"`{pid}`: " + "; ".join(probs) + ".")
            .on(pid).here(_w(M, (lo + hi) / 2)).expect(f"extent >= {prm['min_extent_mm']:g} mm and fill >= {prm['min_fill']:.2%}", "; ".join(probs))
            .fix("A boolean removed (almost) the whole body or a sketch was extruded by ~0. Check the last cut's tool "
                 "body size and sign, and the extrude amount / direction; a real sheet part declares a sheet `process`."))


def run(ctx):
    from . import integrity

    r = ctx.r
    spec = r.spec
    raw = getattr(spec, "raw", None) or {}
    prm = params(spec, "geom", DEFAULTS)
    sec = (raw.get("review") or {}).get("geom")
    out = override_findings(sec, DEFAULTS, "geom", "geom.params", G) if sec else []
    integrity_on = integrity.enabled(raw)
    failed = {e[0]: e[1] for e in getattr(r, "load_errors", None) or []}
    world = getattr(ctx, "world", None)
    clean = {c: 0 for c in CHECKS}
    rows = {}

    def judge(p, check, fn):
        why = opted(p, check)
        if why:
            out.append(note(f"geom.{check}", G, "Opted out", f"`{p.id}` geom_ok.{check}: {why}").on(p.id))
            return
        try:
            f = fn()
        except NotJudged as e:
            ctx.not_checked.append(f"geom.{check} of `{p.id}`: {e}")
            return
        except Exception as e:  # noqa: BLE001 - fail closed per part and check
            ctx.not_checked.append(f"geom.{check} of `{p.id}`: {type(e).__name__}: {e}")
            return
        rows.setdefault(p.id, {})[check] = 0 if f is None else 1
        if f is None:
            clean[check] += 1
        else:
            out.append(f)

    for rp in r.parts:
        p = rp.part
        if getattr(rp, "cat", None) is not None:
            continue
        pid = p.id
        if pid in failed:
            ctx.not_checked.append(f"geom.* ({', '.join(CHECKS)}) of `{pid}`: its geometry did not load "
                                   f"({failed[pid]}); a stand-in solid is not judged")
            continue
        g = getattr(rp, "geom", None)
        M = _matrix(world, pid)
        mesh = getattr(g, "mesh", None)
        if mesh is None or not len(getattr(mesh, "faces", ())):
            ctx.not_checked.append(f"geom.{' / geom.'.join(MESH_CHECKS)} of `{pid}`: no mesh")
        else:
            if integrity_on:
                pass  # integrity.solids already blocks on an open / inconsistently wound shell of this part
            else:
                judge(p, "open_shell", lambda: _open(pid, M, mesh))
            judge(p, "zero_thickness", lambda: _thin(pid, p, M, g, mesh, prm))
        try:
            solid = getattr(g, "solid", None)
            why = "no B-rep shape (mesh only)"
        except Exception as e:  # noqa: BLE001 - the B-rep file would not load
            solid, why = None, f"B-rep did not load ({type(e).__name__}: {e})"
        if solid is None:
            ctx.not_checked.append(f"geom.{' / geom.'.join(BREP_CHECKS)} of `{pid}`: {why}")
            continue
        judge(p, "tiny_edge", lambda: _tiny(pid, M, solid, prm))
        judge(p, "sliver_face", lambda: _sliver(pid, M, solid, prm))
        try:
            infos, unread = read_faces(solid)
        except Exception as e:  # noqa: BLE001
            ctx.not_checked.append(f"geom.near_coplanar_step / geom.near_miss_hole / geom.off_axis_face of `{pid}`: "
                                   f"faces unreadable ({type(e).__name__}: {e})")
            continue

        def faces(fn):
            """A face check passes only when every face was read; a finding on the readable ones still stands."""
            def go():
                f = fn()
                if f is None and unread:
                    raise NotJudged(f"{unread} face(s) of the B-rep could not be read")
                return f
            return go

        judge(p, "near_coplanar_step", faces(lambda: _step(pid, M, solid, prm, infos)))
        judge(p, "near_miss_hole", faces(lambda: _hole(pid, M, solid, prm, infos)))
        judge(p, "off_axis_face", faces(lambda: _skew(pid, M, solid, prm, infos)))

    for c in CHECKS:
        if clean[c]:
            out.append(ok(f"geom.{c}", G, TITLE_OK[c], f"{clean[c]} made part(s) judged and clean."))
    metrics = getattr(ctx, "metrics", None)
    if isinstance(metrics, dict):
        metrics["geom"] = rows
    return out

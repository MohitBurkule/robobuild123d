"""dfm: design-for-manufacture rules per process that the other groups do not judge. Mesh / bbox / 2D maths only.

  dfm.bed_contact          FDM part in its declared `print_orientation`: the faces lying flat on the bed are smaller than
                           `min_bed_area_mm2` or than `min_bed_frac` of the part's bounding footprint: it will not stick
                           (needs a brim / raft or another orientation). WARNING.
  dfm.tall_thin            FDM part taller in the print direction than `max_aspect` x the smaller side of its bed
                           footprint: it wobbles and is knocked off the bed. WARNING.
  dfm.horizontal_hole      FDM round hole (full 360 deg concave cylinder in the B-rep) whose axis lies in the layer plane
                           and whose diameter exceeds `max_horizontal_hole_mm`: its roof droops. A teardrop or flat-roofed
                           hole is not a full cylinder and passes. WARNING.
  dfm.sheet_tab_width      sheet_cut part: a tab / neck of the OUTLINE narrower than `tab_k` x thickness (0.75 x for hard
                           plate, as process.WEB_HARD_T). `process` already judges the web BETWEEN cut loops (hole to hole,
                           hole to edge); this is the neck inside one outline it lists as not checked. WARNING.
  dfm.undeclared_tolerance a shaft / pin / bearing connection into an FDM part where neither the connection nor either
                           part declares a fit (`fit`, `clearance_mm`, `pocket_clearance_mm`, `interference_mm`): printed
                           holes shrink, so an undeclared bore is a guess. WARNING.

Not here because another check already owns it: a skin of one or two layers (mfg.thin_wall: its 0.9 mm printed minimum
is above 3 x 0.2 mm), holes near a bend (process.geometry on sheet_bent: hole < 2 t from a bend), webs between cut loops
(process.geometry on sheet_cut), press-fit interference (connection.press_fit_interference), catalog nut / insert /
bearing pockets (practice.drawn_vs_catalog).

Thresholds: `review.dfm` in the spec (needs a `reason`, see _review.params). Per-part opt out:
`dfm_ok: {"<check suffix>": "<reason, >= 20 chars>"}` (suffix = bed_contact, tall_thin, horizontal_hole,
sheet_tab_width, undeclared_tolerance). A missing input (no print orientation, no mesh, no B-rep, a connection naming a
missing part) is never a pass: it goes to NOT CHECKED.
"""

from __future__ import annotations

import numpy as np

from .. import catalog
from ..finding import WARNING, fail, ok
from ._review import params, x
from .printability import BED_TOL_MM, BRIDGE_COS, UPS, fdm

G = "dfm"
DEFAULTS = {"min_bed_area_mm2": 20.0, "min_bed_frac": 0.08, "max_aspect": 6.0, "max_horizontal_hole_mm": 6.0, "tab_k": 1.0}
MIN_REASON = 20
HORIZONTAL_COS = 0.2      # |hole axis . up| below this: the hole lies in the layer plane (within ~11 deg)
FIT_KEYS = ("fit", "clearance_mm", "pocket_clearance_mm", "interference_mm")
FIT_METHODS = ("shaft", "pin")                       # running / location fits whose bore size matters
NO_FIT_METHODS = ("press_fit", "none", "screw", "tape", "velcro")   # press_fit: connection.press_fit_interference owns it
PRACTICE_KINDS = ("nut", "insert", "bearing")        # catalog parts of these kinds: practice.drawn_vs_catalog owns them
CORNER_EAT = 0.22         # x width: grows the opened outline so the slivers lost at convex 90 deg corners (0.207 w) vanish
TAB_MIN_AREA = 0.15       # x width^2: smaller leftovers are corner noise, not a tab
TAB_FILL = 0.7            # a tab / neck fills its bounding rectangle; a pointed tooth tip (about 0.5) is not one
TITLES = {
    "bed_contact": "Enough flat area on the bed",
    "tall_thin": "Not tall and thin on the bed",
    "horizontal_hole": "No large round hole printed on its side",
    "sheet_tab_width": "Outline has no tab or neck under one thickness",
    "undeclared_tolerance": "Printed bores declare their fit",
}


# ------------------------------------------------------------------------------------------------ opt-out
def opted(p, check):
    """Reason string when part `p` opts `check` out through `dfm_ok` with a usable reason, else None."""
    ok_ = (getattr(p, "_extra", None) or {}).get("dfm_ok") or {}
    why = str(ok_.get(check) or "").strip() if isinstance(ok_, dict) else ""
    return why if len(why) >= MIN_REASON else None


# ------------------------------------------------------------------------------------------------ pure geometry
def _basis(up):
    """(unit up, u, v): u and v span the bed plane. Axis-aligned when `up` is."""
    up = np.asarray(up, float)
    up = up / np.linalg.norm(up)
    a = np.array([1.0, 0.0, 0.0]) if abs(up[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    u = np.cross(up, a)
    u /= np.linalg.norm(u)
    return up, u, np.cross(up, u)


def bed_contact(mesh, up, tol=BED_TOL_MM):
    """(area of the faces lying flat on the bed mm2, bounding footprint mm2, a point on the bed under the part) of
    `mesh` printed with build direction `up`. A face is on the bed when all its vertices are within `tol` of the lowest
    point and it faces straight down (within the bridge angle of printability)."""
    up, u, v = _basis(up)
    V = np.asarray(mesh.vertices, float)
    h = V @ up
    base = float(h.min())
    low = h[np.asarray(mesh.faces)].max(axis=1) <= base + tol
    down = -(np.asarray(mesh.face_normals, float) @ up) > BRIDGE_COS
    area = float(np.asarray(mesh.area_faces, float)[low & down].sum())
    pu, pv = V @ u, V @ v
    foot = float(np.ptp(pu) * np.ptp(pv))
    pt = up * base + u * float(0.5 * (pu.min() + pu.max())) + v * float(0.5 * (pv.min() + pv.max()))
    return area, foot, pt


def tall_thin(mesh, up):
    """(height along `up` mm, smaller side of the bed footprint mm, a point at the top centre) of `mesh`."""
    up, u, v = _basis(up)
    V = np.asarray(mesh.vertices, float)
    h, pu, pv = V @ up, V @ u, V @ v
    side = float(min(np.ptp(pu), np.ptp(pv)))
    top = up * float(h.max()) + u * float(0.5 * (pu.min() + pu.max())) + v * float(0.5 * (pv.min() + pv.max()))
    return float(np.ptp(h)), side, top


def drooping_holes(holes, up, max_d):
    """Of `holes` [(diameter, axis (3), point (3))], those lying in the layer plane (axis perpendicular to `up`) and
    wider than `max_d`. Widest first."""
    up = np.asarray(up, float)
    up = up / np.linalg.norm(up)
    out = []
    for d, axis, pt in holes:
        a = np.asarray(axis, float)
        n = np.linalg.norm(a)
        if n <= 0:
            continue
        if abs(float(a @ up)) / n < HORIZONTAL_COS and float(d) > float(max_d) + 1e-9:
            out.append((float(d), a / n, np.asarray(pt, float)))
    return sorted(out, key=lambda t: -t[0])


def brep_holes(solid):
    """[(diameter, axis, point on the wall)] of every round hole of the exact solid: concave cylinders that share an
    axis and a radius and together close the full turn (process._hole_groups). A teardrop or a flat-roofed hole does not
    close the turn and is not listed."""
    from . import process

    infos = [process.face_info(f) for f in solid.faces()]
    holes, _ = process._hole_groups(infos)
    return [(2.0 * float(g[0]["r"]), tuple(float(c) for c in g[0]["dir"]), tuple(float(c) for c in g[0]["q"])) for g in holes]


def plate_axis(mesh):
    """(unit normal, thickness) of a plate-like mesh: the direction most of its surface faces (both sides), and the
    extent along it. None for an empty mesh."""
    N, A = np.asarray(mesh.face_normals, float), np.asarray(mesh.area_faces, float)
    if not len(A) or float(A.sum()) <= 0:
        return None
    best, ba = None, -1.0
    for c in list(np.eye(3)) + [N[i] for i in np.argsort(-A)[:16]]:
        c = np.asarray(c, float)
        ln = np.linalg.norm(c)
        if ln <= 0:
            continue
        c = c / ln
        s = float(A[np.abs(N @ c) > 0.999].sum())
        if s > ba + 1e-9:
            best, ba = c, s
    if best is None:
        return None
    return best, float(np.ptp(np.asarray(mesh.vertices, float) @ best))


def outline_section(mesh, n):
    """Outline of a plate at mid thickness with its holes filled in: (shapely geometry in (u, v) mm, origin, u, v), or
    None when the section is empty. A 2D point (a, b) is origin + a u + b v in the mesh frame."""
    import trimesh
    from shapely.geometry import LineString, Polygon
    from shapely.ops import polygonize, unary_union

    n, u, v = _basis(n)
    V = np.asarray(mesh.vertices, float)
    t = V @ n
    c = n * float(0.5 * (t.min() + t.max()))
    segs = trimesh.intersections.mesh_plane(mesh, n, c)
    if segs is None or len(segs) == 0:
        return None
    q = np.asarray(segs, float) - c
    uv = np.round(np.stack([q @ u, q @ v], axis=-1), 3)
    lines = [LineString(sg) for sg in uv if np.linalg.norm(sg[0] - sg[1]) > 0]
    if not lines:
        return None
    faces = [f for f in polygonize(unary_union(lines)) if f.area > 0]
    if not faces:
        return None
    return unary_union([Polygon(f.exterior) for f in faces]), c, u, v


def narrow_features(outline, width):
    """Tabs and necks of a 2D outline narrower than `width`: [(about-width mm, area mm2, (x, y))], largest first.
    Morphological opening with a disc of diameter `width`: what the disc cannot enter is narrower than it. Slivers at
    convex corners and pointed tips (teeth) are dropped."""
    w = float(width)
    if outline is None or outline.is_empty or w <= 0:
        return []
    polys = list(outline.geoms) if hasattr(outline, "geoms") else [outline]
    out = []
    for poly in polys:
        if poly.geom_type != "Polygon" or poly.area <= 0:
            continue
        r = max((w - 0.02) / 2.0, 1e-6)
        opened = poly.buffer(-r).buffer(r)
        lost = poly if opened.is_empty else poly.difference(opened.buffer(CORNER_EAT * w))
        if lost.is_empty:
            continue
        for piece in (list(lost.geoms) if hasattr(lost, "geoms") else [lost]):
            if piece.geom_type != "Polygon" or piece.area < TAB_MIN_AREA * w * w:
                continue
            rect = piece.minimum_rotated_rectangle
            if rect.geom_type != "Polygon" or rect.area <= 0:
                continue
            if piece.area / rect.area < TAB_FILL:
                continue  # tapers to a point: a tooth tip, not a tab
            cs = np.asarray(rect.exterior.coords, float)
            short = float(min(np.linalg.norm(cs[1] - cs[0]), np.linalg.norm(cs[2] - cs[1])))
            p = piece.representative_point()
            out.append((short, float(piece.area), (float(p.x), float(p.y))))
    return sorted(out, key=lambda t: -t[1])


def tab_limit(material, thickness, tab_k):
    """Narrowest tab / neck (mm) a cut sheet of this material and thickness should carry."""
    hard = catalog.sheet_family(material) in catalog.HARD_SHEET
    from .process import WEB_HARD_T

    return float(tab_k) * (WEB_HARD_T if hard else 1.0) * float(thickness)


# ------------------------------------------------------------------------------------------------ pure spec rule
def _declares_fit(o):
    """True when a part or connection declares any fit / clearance key (attribute or extra key)."""
    return any(x(o, k) is not None for k in FIT_KEYS)


def undeclared_fits(spec):
    """(bad, judged, missing): shaft / pin / bearing connections into an FDM part.
    bad = [(connection, printed part, other part)] with no declared fit anywhere, judged = how many such connections
    were looked at, missing = [text] for connections that name a part that does not exist."""
    bad, judged, missing = [], 0, []
    for c in spec.connections:
        pa, pb = spec.part(c.a), spec.part(c.b)
        m = str(c.method or "").lower()
        if pa is None or pb is None:
            if m in FIT_METHODS:
                missing.append(f"dfm.undeclared_tolerance of `{c.a}`-`{c.b}` ({m}): a named part does not exist")
            continue
        bearing = "bearing" in (pa.kind, pb.kind)
        if not (m in FIT_METHODS or (bearing and m not in NO_FIT_METHODS)):
            continue
        for p, o in ((pa, pb), (pb, pa)):
            if p.catalog is not None or not fdm(p):
                continue
            if o.catalog is not None and o.kind in PRACTICE_KINDS:
                break  # the pocket of a catalog nut / insert / bearing: practice.drawn_vs_catalog
            judged += 1
            if not (_declares_fit(c) or _declares_fit(p) or _declares_fit(o)):
                bad.append((c, p, o))
            break
    return bad, judged, missing


# ------------------------------------------------------------------------------------------------ group
def _world(b, pt):
    if pt is None:
        return None
    pt = np.asarray(pt, float)
    return pt if b is None else b.M[:3, :3] @ pt + b.M[:3, 3]


def _holes_of(g):
    from .. import cache

    return cache.memo("part_check", ("dfm_holes", cache.source_hash(__file__), g.key), lambda: brep_holes(g.solid))


class _Tally:
    """Per check id: how many items were judged and how many passed, and the opted-out reasons."""

    def __init__(self):
        self.judged = {k: 0 for k in TITLES}
        self.good = {k: 0 for k in TITLES}
        self.out = []

    def item(self, check, p, bad_finding):
        """Record one judged item of `check` on part `p`: `bad_finding` is None when it passed."""
        self.judged[check] += 1
        if bad_finding is None:
            self.good[check] += 1
            return
        why = opted(p, check)
        if why:
            self.good[check] += 1
            self.out.append(ok(f"dfm.{check}", G, TITLES[check], f"`{p.id}`: opted out: {why}").on(p.id))
        else:
            self.out.append(bad_finding)

    def finish(self):
        for k, n in self.judged.items():
            if n and self.good[k]:
                self.out.append(ok(f"dfm.{k}", G, TITLES[k], f"{self.good[k]} of {n} judged item(s) pass."))
        return self.out


def _fdm_part(ctx, rp, P, T):
    p = rp.part
    b = ctx.world.body(p.id)
    mesh = rp.geom.mesh if rp.geom is not None else None
    if mesh is None or not len(mesh.faces):
        ctx.not_checked.append(f"dfm.bed_contact / tall_thin / horizontal_hole of `{p.id}`: part has no mesh")
        return
    po = str(x(p, "print_orientation") or "").lower()
    if po not in UPS:
        ctx.not_checked.append(f"dfm.bed_contact / tall_thin / horizontal_hole of `{p.id}`: no valid `print_orientation` "
                               f"({po or 'none'}), so the bed face and the layer plane are unknown")
        return
    up = np.asarray(UPS[po], float)
    # bed contact
    area, foot, pt = bed_contact(mesh, up)
    need = max(float(P["min_bed_area_mm2"]), float(P["min_bed_frac"]) * foot)
    bad = None
    if area + 1e-9 < need:
        bad = (fail("dfm.bed_contact", G, WARNING, "Too little flat area on the bed",
                    f"`{p.id}` printed build-up {po} rests on {area:.1f} mm2 of flat face; its bounding footprint is "
                    f"{foot:.0f} mm2, so it needs >= {need:.1f} mm2 (max of {float(P['min_bed_area_mm2']):g} mm2 and "
                    f"{float(P['min_bed_frac']):g} x footprint) to stay stuck.")
               .on(p.id).here(_world(b, pt)).expect(f">= {need:.1f} mm2", f"{area:.1f} mm2")
               .fix(f"Give `{p.id}` a flat face of >= {need:.0f} mm2 on the bed side (cut the bottom flat, or add a "
                    "foot), or set `print_orientation` to the axis whose opposite face is its largest flat."))
    T.item("bed_contact", p, bad)
    # tall and thin
    height, side, top = tall_thin(mesh, up)
    lim = float(P["max_aspect"])
    ratio = height / side if side > 1e-9 else float("inf")
    bad = None
    if ratio > lim + 1e-9:
        bad = (fail("dfm.tall_thin", G, WARNING, "Tall thin print",
                    f"`{p.id}` printed build-up {po} is {height:.1f} mm tall on a footprint only {side:.1f} mm wide "
                    f"(aspect {ratio:.1f}, limit {lim:g}): the nozzle drags it and it wobbles off the bed.")
               .on(p.id).here(_world(b, top)).expect(f"<= {lim:g} x footprint side", f"{ratio:.1f} x")
               .fix(f"Lay `{p.id}` down (set `print_orientation` to an axis across its {height:.0f} mm length), or "
                    f"widen its base to >= {height / lim:.1f} mm."))
    T.item("tall_thin", p, bad)
    # horizontal holes (exact B-rep)
    try:
        solid = rp.geom.solid
        holes = None if solid is None else _holes_of(rp.geom)
    except Exception as e:  # noqa: BLE001 - fail closed per part
        ctx.not_checked.append(f"dfm.horizontal_hole of `{p.id}`: holes not readable ({type(e).__name__})")
        return
    if holes is None:
        ctx.not_checked.append(f"dfm.horizontal_hole of `{p.id}`: no exact B-rep")
        return
    max_d = float(P["max_horizontal_hole_mm"])
    droop = drooping_holes(holes, up, max_d)
    bad = None
    if droop:
        d, axis, q = droop[0]
        bad = (fail("dfm.horizontal_hole", G, WARNING, "Large round hole printed on its side",
                    f"`{p.id}` printed build-up {po} has {len(droop)} round hole(s) with a horizontal axis up to "
                    f"{d:.2f} mm diameter (limit {max_d:g} mm): the top of the circle is an unsupported arc and droops.")
               .on(p.id).here(_world(b, q)).expect(f"<= {max_d:g} mm", f"{d:.2f} mm")
               .fix("Make the hole a teardrop (45 deg roof peak along the build direction) or give it a flat roof, or "
                    "turn `print_orientation` so the hole axis is the build direction."))
    T.item("horizontal_hole", p, bad)


def _sheet_part(ctx, rp, P, T):
    p = rp.part
    b = ctx.world.body(p.id)
    mesh = rp.geom.mesh if rp.geom is not None else None
    if mesh is None or not len(mesh.faces):
        ctx.not_checked.append(f"dfm.sheet_tab_width of `{p.id}`: part has no mesh")
        return
    try:
        pa = plate_axis(mesh)
        sec = outline_section(mesh, pa[0]) if pa is not None and pa[1] > 0 else None
    except Exception as e:  # noqa: BLE001 - fail closed per part
        ctx.not_checked.append(f"dfm.sheet_tab_width of `{p.id}`: outline not readable ({type(e).__name__})")
        return
    if sec is None:
        ctx.not_checked.append(f"dfm.sheet_tab_width of `{p.id}`: no plate outline found at mid thickness")
        return
    n, t = pa
    outline, c, u, v = sec
    wmin = tab_limit(p.material, t, P["tab_k"])
    tabs = narrow_features(outline, wmin)
    bad = None
    if tabs:
        w0, a0, (px, py) = tabs[0]
        bad = (fail("dfm.sheet_tab_width", G, WARNING, "Tab or neck narrower than the sheet is thick",
                    f"`{p.id}` ({p.process}, {t:.2f} mm {p.material or 'sheet'}) has {len(tabs)} tab(s) / neck(s) of its "
                    f"outline narrower than {wmin:.2f} mm; the largest is about {w0:.2f} mm wide ({a0:.1f} mm2): it "
                    "overheats, warps or snaps off when cut.")
               .on(p.id).here(_world(b, c + px * u + py * v)).expect(f">= {wmin:.2f} mm", f"about {w0:.2f} mm")
               .fix(f"Widen that tab / neck of `{p.id}` to >= {wmin:.2f} mm, or remove it from the outline."))
    T.item("sheet_tab_width", p, bad)


def run(ctx):
    r, w = ctx.r, ctx.world
    spec = r.spec
    P = params(spec, "dfm", DEFAULTS)
    T = _Tally()
    for rp in r.parts:
        p = rp.part
        if rp.cat is not None or p.catalog is not None:
            continue
        if fdm(p):
            _fdm_part(ctx, rp, P, T)
        elif catalog.process_canon(p.process) == "sheet_cut":
            _sheet_part(ctx, rp, P, T)
    bad, judged, missing = undeclared_fits(spec)
    ctx.not_checked.extend(missing)
    flagged = {id(c) for c, _, _ in bad}
    for c, p, o in bad:
        ob = w.body(o.id)
        T.item("undeclared_tolerance", p,
               fail("dfm.undeclared_tolerance", G, WARNING, "Printed bore with no declared fit",
                    f"`{c.a}`-`{c.b}` ({c.method}): `{o.id}` runs in printed `{p.id}` but neither the connection nor "
                    f"either part declares a fit ({', '.join(FIT_KEYS)}); FDM holes come out 0.1-0.3 mm small, so the "
                    "bore size is a guess.")
               .on(p.id, o.id).here(ob.center if ob is not None else None)
               .fix(f"Add `clearance_mm` (running fit: 0.1-0.2 per side) or `interference_mm` to the `{c.a}`-`{c.b}` "
                    f"connection and size the bore in `{p.id}` from it."))
    for _ in range(judged - len(flagged)):
        T.judged["undeclared_tolerance"] += 1
        T.good["undeclared_tolerance"] += 1
    return T.finish()

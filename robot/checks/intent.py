"""Design-intent checks: each one tests the PURPOSE of a feature, not its shape (`intent` list in the spec).

A reference-matching model can look right and still not work: a round bore where the drive needs a key, a nut that can
fall out of its pocket, a seat that does not locate the gearbox. Each entry names a rule and where the feature is; the
rule probes the geometry for the function. Findings are `intent.<rule>`; a failure is a BLOCKER unless the entry says
"severity": "warning". Every rule is a pure function of meshes (see the `*_probe` functions) so tests can run it on a
bad and a good part.

Rules (entry keys):
  keyed_bore        part, axis (x|y|z), at [x,y,z] on the bore axis, span [a0, a1] along the axis: every section of the
                    bore in the span must be a D (or hex); a round bore cannot transmit drive torque on a D-shaft.
  support_free      part, up (build direction +x|-x|...|-z), max_frac (0.02), angle (45), bridge_max (6): area of
                    downward regions steeper than `angle` that are too wide to bridge (bed face excluded) over total area.
  min_wall          part, min (1.8), max_frac (0.02), except [[lo], [hi]] boxes, envelope (only the outer X / Y skin):
                    wall thickness from inward rays.
  fillet            part, axis, h, at [[u, v], ...], r (0.8): no sharp outline corner within 1 mm of each load corner.
  insert_column     part, inserts [[x, y, z_bottom]], floor_z, r: material all the way from the floor to the insert.
  tyre_retention    hub, axis, at, span, tyre_id, min_interference (1.0 on diameter).
  captive_nut       nut, host (one or a list), move (0.3): the nut moved by `move` in any of 14 directions hits a host.
  wheel_clearance   wheel, exclude [ids] (its own hub / axle), min (1.0): gap from the tyre to every other body.
  flush_head        fastener, host, out [dx, dy, dz] (outward face normal), max_proud (0.2).
  notch_bears       part, lug, bolts [ids], dir [dx,dy,dz] (reaction direction): the part moved along dir hits the lug
                    before any bolt shank, so the notch carries the load and the bolts only clamp.
  seat_locates      part (motor), host, axis [dx,dy,dz], at [x,y,z], play (0.15), turn_deg (2): the part moved radially
                    by `play` or turned by `turn_deg` about its shaft hits the host.
  tool_count        max (2), module_max (1), module [fastener ids]: distinct drivers in the teardown / module swap.
  wire_clear_rotor  rotor [ids], axis [dx,dy,dz], at [x,y,z], min (2.0), via {wire id: [[x,y,z], ...]}: every wire
                    (polyline proxy: its ports plus the declared via points)
                    keeps `min` from the rotor's swept volume (a cylinder of its max radius over its axial span).
"""

from __future__ import annotations

import math

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok

G = "intent"
AX = {"x": 0, "y": 1, "z": 2}
DIRS = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0), "+z": (0, 0, 1), "-z": (0, 0, -1)}


def _unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def _surface(m, n=4000, seed=1):
    import trimesh

    p, _ = trimesh.sample.sample_surface_even(m, n, seed=seed)
    return np.vstack([p, m.vertices])


def _hits(pts, host):
    from ..world import _contains

    lo, hi = host.bounds
    k = np.all((pts >= lo) & (pts <= hi), axis=1)
    return bool(k.any() and _contains(host, pts[k]).any())


def _perp(a):
    a = _unit(a)
    t = np.array([1.0, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1.0, 0])
    u = _unit(np.cross(a, t))
    return u, np.cross(a, u)


# ------------------------------------------------------------------------------------------------ probes (pure)
def keyed_bore_probe(m, axis, at, span, n=4):
    """Shapes of the bore nearest `at` at n sections over span: list of 'D' / 'round' / ... / None (no bore)."""
    from .ref_features import holes, section

    ax = AX[axis]
    uv = [at[i] for i in range(3) if i != ax]
    out = []
    for h in np.linspace(span[0], span[1], n + 2)[1:-1]:
        hs = [x for x in holes(section(m, ax, float(h))) if math.dist(x[0], uv) < 1.5]
        out.append(hs[0][2] if hs else None)
    return out


def overhang_frac(m, up, angle=45.0):
    up = _unit(up)
    nz = m.face_normals @ up
    h = m.triangles_center @ up
    bed = h < h.min() + 0.05
    bad = (nz < -math.cos(math.radians(angle))) & ~bed
    return float(m.area_faces[bad].sum() / m.area), float(m.area_faces[bad].sum())


def unsupported(m, up, angle=45.0, bridge_max=6.0, ledge_max=1.0):
    """Overhang that needs support: connected regions of faces steeper than `angle` below horizontal (bed excluded)
    whose shorter horizontal span exceeds `bridge_max` (shorter spans bridge: hole roofs, slot tops) and whose width
    (2 x area / boundary length) exceeds `ledge_max` (a narrower ledge or ring prints as a short cantilever). Returns
    (area mm2, fraction of total area, [region centroids])."""
    import networkx as nx

    up = _unit(up)
    nz = m.face_normals @ up
    h = m.triangles_center @ up
    bad = (nz < -math.cos(math.radians(angle))) & (h > h.min() + 0.05)
    idx = np.flatnonzero(bad)
    if not len(idx):
        return 0.0, 0.0, []
    g = nx.Graph()
    g.add_nodes_from(idx)
    adj = m.face_adjacency
    k = bad[adj[:, 0]] & bad[adj[:, 1]]
    g.add_edges_from(adj[k])
    u, v = _perp(up)
    area, where = 0.0, []
    for comp in nx.connected_components(g):
        c = np.fromiter(comp, int)
        P = m.vertices[m.faces[c]].reshape(-1, 3)
        span = min(np.ptp(P @ u), np.ptp(P @ v))
        a = float(m.area_faces[c].sum())
        E = np.sort(m.faces[c][:, [0, 1, 1, 2, 2, 0]].reshape(-1, 2), axis=1)
        ue, cnt = np.unique(E, axis=0, return_counts=True)
        b = ue[cnt == 1]
        blen = float(np.linalg.norm(m.vertices[b[:, 0]] - m.vertices[b[:, 1]], axis=1).sum()) or 1.0
        if span > bridge_max and 2 * a / blen > ledge_max and a > 2.0:
            area += a
            where.append(np.round(m.triangles_center[c].mean(0), 1).tolist())
    return area, area / float(m.area), where


def wall_thickness(m, n=3000, seed=2):
    """(points, thickness) from rays cast inward from surface samples."""
    import trimesh

    p, fi = trimesh.sample.sample_surface_even(m, n, seed=seed)
    d = -m.face_normals[fi]
    o = p + d * 1e-3
    loc, ri, _ = m.ray.intersects_location(o, d, multiple_hits=False)
    t = np.full(len(p), np.inf)
    t[ri] = np.linalg.norm(loc - o[ri], axis=1)
    return p, t


def sharp_corners_near(m, axis, h, pts, tol=1.0):
    from .ref_features import corners, section

    g = section(m, AX[axis], h)
    cs = corners(g)
    return [tuple(p) for p in pts if any(math.dist(p, c[:2]) <= tol and c[2] > 60 for c in cs)]


def column_gaps(m, inserts, floor_z, r):
    """Inserts whose boss has air between the floor and the insert (sampled on a ring of radius r)."""
    from ..world import _contains

    bad = []
    for x, y, z in inserts:
        zs = np.arange(floor_z + 0.1, z - 0.05, 0.2)
        P = np.array([(x + r * math.cos(a), y + r * math.sin(a), q) for a in np.linspace(0, 2 * math.pi, 8, endpoint=False) for q in zs])
        if len(P) and not _contains(m, P).all():
            bad.append((x, y, z))
    return bad


def seat_radius(m, axis, at, span):
    """Max material radius about the axis over the span (the tyre seat crest)."""
    a = _unit(axis) if not isinstance(axis, str) else np.eye(3)[AX[axis]]
    v = m.vertices - np.asarray(at, float)
    s = v @ a
    k = (s >= span[0]) & (s <= span[1])
    r = np.linalg.norm(v[k] - np.outer(s[k], a), axis=1)
    return float(r.max()) if k.any() else 0.0


def escape_dirs(nut, hosts, move=0.3):
    """Directions in which the nut moved by `move` hits no host: [] means it is captive."""
    P = _surface(nut, 1500)
    dirs = [np.array(d, float) for d in DIRS.values()] + [_unit(d) for d in np.array(np.meshgrid(*[[-1, 1]] * 3)).T.reshape(-1, 3)]
    return [tuple(np.round(d, 2)) for d in dirs if not any(_hits(P + move * d, h) for h in hosts)]


def min_gap(a, others, n=2500):
    import trimesh

    P = _surface(a, n)
    best = (math.inf, None)
    for name, b in others:
        lo, hi = b.bounds
        if np.any(a.bounds[0] > hi + 5) or np.any(a.bounds[1] < lo - 5):
            continue
        d = trimesh.proximity.closest_point(b, P)[1]
        from ..world import _contains

        if _contains(b, P).any():
            return 0.0, name
        if d.min() < best[0]:
            best = (float(d.min()), name)
    return best


def proud(fast, host, out, at=None):
    """How far the fastener stands outside the host face along `out` (<= 0 is flush or sunk). The face level is
    the host's outermost surface in a ring just outside the head."""
    out = _unit(out)
    top = float((fast.vertices @ out).max())
    c = np.asarray(at if at is not None else fast.bounds.mean(0), float)
    v = _surface(host, 20000) - c
    s = v @ out
    r = np.linalg.norm(v - np.outer(s, out), axis=1)
    u, _ = _perp(out)
    rh = 0.5 * float(np.ptp(fast.vertices @ u))
    k = (r > rh + 0.2) & (r < rh + 2.0)
    if not k.any():
        return None
    return top - float((np.percentile(s[k], 90) + c @ out))


def first_contact(moving, fixed, d, step=0.05, reach=1.5, skip_seated=False):
    """Smallest move of `moving` along d that makes it touch a fixed body. skip_seated: ignore fixed-body surface
    already touching `moving` at rest (a screw head on its seat), so only clearance-hole contact counts."""
    import trimesh

    d = _unit(d)
    Q = []
    for f in fixed:
        q = _surface(f, 2500)
        if skip_seated:
            q = q[trimesh.proximity.closest_point(moving, q)[1] > 0.08]
        Q.append(q)
    for s in np.arange(step, reach + 1e-9, step):
        if any(len(q) and _hits(q - s * d, moving) for q in Q):
            return float(s)
    return math.inf


def seat_free(part, hosts, axis, at, play=0.15, turn=2.0):
    """Motions (radial shifts by play, +-turn about the axis) that do NOT hit the host: [] means it is located."""
    import trimesh

    hosts = hosts if isinstance(hosts, (list, tuple)) else [hosts]
    hit = lambda Q: any(_hits(Q, h) for h in hosts)  # noqa: E731
    P = _surface(part, 3000)
    a = _unit(axis)
    u, v = _perp(a)
    free = []
    for k in range(8):
        d = math.cos(k * math.pi / 4) * u + math.sin(k * math.pi / 4) * v
        if not hit(P + play * d):
            free.append(f"shift {np.round(d, 2).tolist()}")
    for sgn in (1, -1):
        R = trimesh.transformations.rotation_matrix(math.radians(sgn * turn), a, at)
        if not hit(trimesh.transform_points(P, R)):
            free.append(f"turn {sgn * turn:+.0f} deg")
    return free


def swept_gap(P, axis, at, rmax, a0, a1):
    """Distance from points to a solid cylinder (radius rmax, axial span a0..a1 about `at` along `axis`)."""
    a = _unit(axis)
    v = np.atleast_2d(P) - np.asarray(at, float)
    s = v @ a
    r = np.linalg.norm(v - np.outer(s, a), axis=1)
    dr = np.maximum(r - rmax, 0)
    ds = np.maximum(np.maximum(a0 - s, s - a1), 0)
    return np.hypot(dr, ds)


def rotor_envelope(meshes, axis, at):
    a = _unit(axis)
    V = np.vstack([m.vertices for m in meshes]) - np.asarray(at, float)
    s = V @ a
    r = np.linalg.norm(V - np.outer(s, a), axis=1)
    return float(r.max()), float(s.min()), float(s.max())


# ------------------------------------------------------------------------------------------------ runner
def _m(ctx, pid):
    b = ctx.world.body(pid)
    return b.mesh if b is not None else None


def _rule(ctx, e):
    """Return (passed, title, detail, subject, metric)."""
    r = e["rule"]
    if r == "keyed_bore":
        sh = keyed_bore_probe(_m(ctx, e["part"]), e["axis"], e["at"], e["span"])
        seen = [s for s in sh if s]
        good = bool(seen) and all(s in ("D", "hex") for s in seen)
        return good, "Bore keys the drive", f"bore sections along {e['axis']} are {sh}; a D-shaft needs a flat in the bore (a round printed bore slips under stall torque).", e["part"], sh
    if r == "support_free":
        a, f, where = unsupported(_m(ctx, e["part"]), DIRS[e.get("up", "+z")], e.get("angle", 45.0), e.get("bridge_max", 6.0))
        mx = e.get("max_frac", 0.02)
        return f <= mx, "Prints without supports", f"{a:.0f} mm2 ({f:.1%}) of overhang steeper than {e.get('angle', 45)} deg and wider than a {e.get('bridge_max', 6.0)} mm bridge, printed build-up {e.get('up', '+z')} (limit {mx:.0%}), at {where[:4]}.", e["part"], round(f, 4)
    if r == "min_wall":
        p, t = wall_thickness(_m(ctx, e["part"]))
        keep = np.ones(len(p), bool)
        if e.get("envelope"):   # only the outer skin: points on the part's X / Y bounding faces
            lo, hi = _m(ctx, e["part"]).bounds
            keep &= (np.abs(p[:, :2] - lo[:2]) < 0.05).any(1) | (np.abs(p[:, :2] - hi[:2]) < 0.05).any(1)
        for lo, hi in e.get("except", []):
            keep &= ~np.all((p >= lo) & (p <= hi), axis=1)
        mn = e.get("min", 1.8)
        thin = keep & (t < mn)
        f = float(thin.sum() / max(keep.sum(), 1))
        where = np.round(p[thin][:3], 1).tolist()
        return f <= e.get("max_frac", 0.02), f"Walls >= {mn} mm", f"{f:.1%} of the surface backs onto less than {mn} mm of material (e.g. {where}).", e["part"], round(f, 4)
    if r == "fillet":
        bad = sharp_corners_near(_m(ctx, e["part"]), e["axis"], e["h"], e["at"])
        return not bad, "Load corners are filleted", f"sharp corners at {bad} in the {e['axis']}={e['h']} section; concave load corners need r >= {e.get('r', 0.8)} so PLA does not crack there.", e["part"], len(bad)
    if r == "insert_column":
        bad = column_gaps(_m(ctx, e["part"]), e["inserts"], e["floor_z"], e.get("r", 2.2))
        return not bad, "Insert bosses stand on the floor", f"inserts with air below their boss: {bad}; a hanging boss has no load path and pulls out.", e["part"], len(bad)
    if r == "tyre_retention":
        rr = seat_radius(_m(ctx, e["hub"]), e["axis"], e["at"], e["span"])
        i = 2 * rr - e["tyre_id"]
        mn = e.get("min_interference", 1.0)
        return i >= mn - 1e-6, "Tyre cannot walk off", f"seat crest {2 * rr:.2f} mm on a {e['tyre_id']} mm ID tyre: {i:.2f} mm interference on diameter (need >= {mn}).", e["hub"], round(i, 3)
    if r == "captive_nut":
        hosts = [e["host"]] if isinstance(e["host"], str) else e["host"]
        free = escape_dirs(_m(ctx, e["nut"]), [_m(ctx, h) for h in hosts], e.get("move", 0.3))
        return not free, "Nut is captive", f"with the screw out the nut moves {e.get('move', 0.3)} mm freely along {free[:4]}.", e["nut"], len(free)
    if r == "wheel_clearance":
        ex = set(e.get("exclude", [])) | {e["wheel"]}
        others = [(b.id, b.mesh) for b in ctx.world.bodies if b.id not in ex and not b.is_wire and not b.id.startswith("belt")]
        g, who = min_gap(_m(ctx, e["wheel"]), others)
        mn = e.get("min", 1.0)
        return g >= mn, "Wheel runs clear", f"`{e['wheel']}` is {g:.2f} mm from `{who}` (need >= {mn}; a rub is a brake).", e["wheel"], round(g, 3)
    if r == "flush_head":
        p = proud(_m(ctx, e["fastener"]), _m(ctx, e["host"]), e["out"])
        if p is None:
            return False, "Head is flush", f"no `{e['host']}` face found beside `{e['fastener']}` along {e['out']}.", e["fastener"], None
        return p <= e.get("max_proud", 0.2), "Head is flush", f"`{e['fastener']}` head stands {p:+.2f} mm off the `{e['host']}` face (limit {e.get('max_proud', 0.2)}).", e["fastener"], round(p, 3)
    if r == "notch_bears":
        mv = _m(ctx, e["part"])
        gl = first_contact(mv, [_m(ctx, e["lug"])], e["dir"])
        gb = first_contact(mv, [_m(ctx, b) for b in e["bolts"]], e["dir"], skip_seated=True)
        return gl < gb, "Notch bears the hit, not the bolts", f"moving `{e['part']}` along {e['dir']}: lug contact at {gl:.2f} mm, bolt contact at {gb:.2f} mm.", e["part"], [gl, gb]
    if r == "seat_locates":
        hs = [e["host"]] if isinstance(e["host"], str) else e["host"]
        free = seat_free(_m(ctx, e["part"]), [_m(ctx, h) for h in hs], e["axis"], e["at"], e.get("play", 0.15), e.get("turn_deg", 2.0))
        return not free, "Seat locates the part", f"`{e['part']}` is free to {free} in `{e['host']}`; the seat must hold it concentric and stop it turning.", e["part"], len(free)
    if r == "tool_count":
        fs = ctx.r.spec.raw.get("fasteners", [])
        tools = sorted({f.get("tool") for f in fs if f.get("tool")})
        mod = sorted({f.get("tool") for f in fs if f.get("id") in set(e.get("module", [])) and f.get("tool")})
        good = len(tools) <= e.get("max", 2) and len(mod) <= e.get("module_max", 1)
        return good, "Pit kit is small", f"teardown needs {tools}; the module swap needs {mod} (limits {e.get('max', 2)} / {e.get('module_max', 1)}).", "fasteners", [len(tools), len(mod)]
    if r == "wire_clear_rotor":
        rmax, a0, a1 = rotor_envelope([_m(ctx, x) for x in e["rotor"]], e["axis"], e["at"])
        worst = (math.inf, None)
        for w in ctx.r.spec.raw.get("wires", []):
            try:
                pa, pb = ctx.world.port(ctx.r, w["from"]), ctx.world.port(ctx.r, w["to"])
                pa, pb = [np.asarray(p[0] if isinstance(p, tuple) else p, float).reshape(-1)[:3] for p in (pa, pb)]
            except Exception:  # noqa: BLE001
                continue
            pts = [pa] + [np.asarray(v, float) for v in (e.get("via") or {}).get(w["id"], [])] + [pb]
            P = np.vstack([a + np.linspace(0, 1, 40)[:, None] * (b - a) for a, b in zip(pts, pts[1:])])
            g = float(swept_gap(P, e["axis"], e["at"], rmax, a0, a1).min())
            if g < worst[0]:
                worst = (g, w["id"])
        mn = e.get("min", 2.0)
        return worst[0] >= mn, "Wires clear the disc", f"closest wire `{worst[1]}` is {worst[0]:.2f} mm from the rotor's swept volume (need >= {mn}).", "wires", round(worst[0], 3)
    raise KeyError(r)


def run(ctx):
    out = []
    for e in (ctx.r.spec.raw or {}).get("intent", []) or []:
        cid = f"intent.{e.get('rule')}"
        try:
            good, title, detail, subj, met = _rule(ctx, e)
        except Exception as ex:  # noqa: BLE001
            out.append(fail(cid, G, WARNING, "Intent check could not run", f"{e}: {type(ex).__name__}: {ex}"))
            ctx.not_checked.append(f"{cid} on {e.get('part') or e.get('wheel') or e.get('nut')}")
            continue
        ctx.metrics.setdefault("intent", []).append({"rule": e["rule"], "subject": subj, "value": met, "pass": bool(good)})
        why = f" Why: {e['why']}" if e.get("why") else ""
        if good:
            out.append(ok(cid, G, title, detail + why))
        else:
            sev = WARNING if e.get("severity") == "warning" else BLOCKER
            out.append(fail(cid, G, sev, title, detail + why).on(subj))
    return out

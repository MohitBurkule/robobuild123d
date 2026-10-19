"""Opt-out sharp internal corner check (`mfg.sharp_internal_corner`) for printed, moulded and cast parts.

Every fdm / sla / molded / cast part is scanned automatically; nothing has to be listed. Machined and cut parts are
left to `process` (analyse_milled / analyse_sheet_cut already enforce tool radius and kerf), so they are skipped here.

Method (pure mesh functions, also used on the reference meshes so both sides are measured the same way):
  concave_samples(m)      concave face adjacencies (trimesh dihedral + convexity), one sample per `grid` mm cell,
                          with the shared edge's direction.
  local_radius(m, p, t)   section the mesh by the plane through p normal to the edge direction t; on the outline
                          near p, walk the run of same-sign turns round the vertex closest to p and return
                          arc length / turn (0 for a sharp corner), and the total turn in degrees.
  regions(points)         chain flagged samples closer than `link_mm` into regions.

Severity per region (world frame):
  BLOCKER  r < load_min_r_mm (1.0) and the region lies in a load path: within load_dist_mm (3) of a fastener, of
           another structural part it joins (mount bases, bulkhead-to-deck), of a declared `sharp_corner_loads`
           entry [{part, near: [x,y,z], r_mm}] or `load_interfaces` [{near, r_mm}].
  WARNING  r < min_r_mm (0.5) anywhere else.
  INFO     the reference_cad part has the same corner: ours >= reference radius - ref_tol_mm (0.2), "matches original".
Opt-out (a non-empty reason is REQUIRED, otherwise `mfg.sharp_ok_reason` BLOCKER and the opt-out is ignored):
  part-level  "sharp_corners_ok": "reason"
  per region  spec "sharp_ok": [{"part", "near": [x,y,z], "r_mm": 3, "reason"}]
Parameters: spec "sharp_corner": {min_r_mm, load_min_r_mm, load_dist_mm, ref_tol_mm, window_mm, grid_mm, link_mm}.
Corners already declared in an `intent` `fillet` entry are reported there (intent.fillet), not again here.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from .. import catalog
from ..finding import BLOCKER, INFO, WARNING, fail, note, ok
from .process import FACET_DEG

G = "mfg"
CID = "mfg.sharp_internal_corner"
PROCESSES = ("fdm", "sla", "molded", "cast")
DEFAULTS = {"min_r_mm": 0.5, "load_min_r_mm": 1.0, "load_dist_mm": 3.0, "ref_tol_mm": 0.2, "window_mm": 4.0,
            "grid_mm": 1.5, "link_mm": 2.5, "min_turn_deg": 45.0}
LOAD_KINDS = ("structure",)


def params(spec_raw):
    p = dict(DEFAULTS)
    p.update({k: float(v) for k, v in ((spec_raw or {}).get("sharp_corner") or {}).items() if k in DEFAULTS})
    return p


# ---------------------------------------------------------------- mesh helpers
def _unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def concave_samples(m, grid=1.5, min_deg=0.5):
    """[(point, edge direction)] on concave edges turning more than min_deg, one per grid cell."""
    if len(m.faces) < 4:
        return []
    ang = np.degrees(m.face_adjacency_angles)
    k = (~m.face_adjacency_convex) & (ang > min_deg)
    if not k.any():
        return []
    E = m.face_adjacency_edges[k]
    a, b = m.vertices[E[:, 0]], m.vertices[E[:, 1]]
    out, seen = [], set()
    for pa, pb in zip(a, b):
        L = float(np.linalg.norm(pb - pa))
        t = _unit(pb - pa)
        for s in np.linspace(0, 1, max(int(L / grid) + 1, 1) + 1)[1:-1] if L > grid else (0.5,):
            p = pa + s * (pb - pa)
            key = tuple(np.floor(p / grid).astype(int))
            if key not in seen:
                seen.add(key)
                out.append((p, t))
    return out


def _frame(t):
    t = _unit(t)
    u = _unit(np.cross(t, [1, 0, 0] if abs(t[0]) < 0.9 else [0, 1, 0]))
    return u, np.cross(t, u)


def tri_boxes(m):
    T = m.triangles
    return T.min(axis=1), T.max(axis=1)


def local_radius(m, p, t, window=4.0, boxes=None):
    """(radius mm, turn deg) of the concave corner at p (a point on or within ~0.5 mm of m), section normal to t.
    None when the section has no outline there."""
    import trimesh

    p, t = np.asarray(p, float), _unit(t)
    if boxes is not None:   # only the triangles near p: a section of the whole part per sample is slow
        idx = np.nonzero(np.all(boxes[0] <= p + window, axis=1) & np.all(boxes[1] >= p - window, axis=1))[0]
        if not len(idx):
            return None
        sub = m.submesh([idx], append=True)
    else:
        sub = m
    segs = trimesh.intersections.mesh_plane(sub, t, p)
    if len(segs) == 0:
        return None
    u, v = _frame(t)
    S = np.stack([(segs - p) @ u, (segs - p) @ v], axis=-1)       # (n, 2, 2)
    S = S[np.minimum(np.linalg.norm(S[:, 0], axis=1), np.linalg.norm(S[:, 1], axis=1)) < window]
    chain = _chain(S)
    if chain is None or len(chain) < 3:
        return None
    P = _simplify(np.asarray(chain))
    if len(P) < 3:
        return None
    i0 = int(np.argmin(np.linalg.norm(P, axis=1)))
    if i0 == 0 or i0 == len(P) - 1:
        return None
    d = np.diff(P, axis=0)
    L = np.linalg.norm(d, axis=1)
    th = np.arctan2(d[:, 1], d[:, 0])
    turn = (np.diff(th) + np.pi) % (2 * np.pi) - np.pi           # turn at vertex i+1
    # the vertex nearest p, or its neighbour with the largest turn (p may sit on a fillet facet)
    cand = [j for j in (i0 - 1, i0, i0 + 1) if 1 <= j <= len(P) - 2]
    c = max(cand, key=lambda j: abs(turn[j - 1]))
    sg = np.sign(turn[c - 1])
    if sg == 0:
        return None
    lo = hi = c
    step = 1.5   # longest facet of a tessellated fillet
    while lo - 1 >= 1 and sg * turn[lo - 2] > math.radians(0.5) and L[lo - 1] <= step:
        lo -= 1
    while hi + 1 <= len(P) - 2 and sg * turn[hi] > math.radians(0.5) and L[hi] <= step:
        hi += 1
    tot = float(sg * turn[lo - 1:hi].sum())
    n = hi - lo + 1
    if n == 1:
        return 0.0, math.degrees(tot)
    # vertices on the arc (tangent points included): n - 1 chords, each subtending tot / (n - 1)
    chord = float(L[lo:hi].sum()) / (n - 1)
    return chord / (2 * math.sin(tot / (n - 1) / 2)), math.degrees(tot)


def _simplify(P, deg=0.1):
    """Drop collinear vertices (a section cuts each quad's two triangles, splitting straight runs)."""
    keep = [0]
    for i in range(1, len(P) - 1):
        a, b = P[i] - P[keep[-1]], P[i + 1] - P[i]
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na < 1e-6:
            continue
        if nb < 1e-6 or abs(math.atan2(a[0] * b[1] - a[1] * b[0], a @ b)) > math.radians(deg):
            keep.append(i)
    keep.append(len(P) - 1)
    return P[keep]


def _chain(S, tol=1e-4):
    """Order 2D segments into the polyline through the segment nearest the origin."""
    if len(S) == 0:
        return None
    key = lambda q: (round(q[0] / tol), round(q[1] / tol))  # noqa: E731
    adj = {}
    for a, b in S:
        ka, kb = key(a), key(b)
        if ka == kb:
            continue
        adj.setdefault(ka, []).append((kb, b))
        adj.setdefault(kb, []).append((ka, a))
    if not adj:
        return None
    mid = np.linalg.norm(S.mean(axis=1), axis=1)
    a0 = S[int(np.argmin(mid))][0]
    start = key(a0)
    pts = {kk: q for lst in adj.values() for kk, q in lst}
    pts[start] = a0

    def walk(frm, cur):
        out = []
        seen = {frm, cur}
        while True:
            nxt = [kk for kk, _ in adj.get(cur, []) if kk not in seen]
            if not nxt:
                return out
            cur = nxt[0]
            seen.add(cur)
            out.append(cur)

    nb = adj[start]
    fwd = walk(start, nb[0][0]) if nb else []
    back = walk(start, nb[1][0]) if len(nb) > 1 else []
    order = list(reversed(back)) + ([nb[1][0]] if len(nb) > 1 else []) + [start] + [nb[0][0]] + fwd
    # remove possible duplicate when the ring closes
    seen, uniq = set(), []
    for k in order:
        if k not in seen:
            seen.add(k)
            uniq.append(k)
    return [np.asarray(pts[k], float) for k in uniq if pts.get(k) is not None]


def scan(m, min_r, window=4.0, grid=1.5, min_turn=45.0):
    """[(point, dir, radius, turn deg)] of concave corners on mesh m whose local radius is below min_r."""
    boxes = tri_boxes(m)
    out = []
    for p, t in concave_samples(m, grid):
        r = local_radius(m, p, t, window, boxes)
        if r is None:
            continue
        rad, turn = r
        if turn >= min_turn and rad < min_r:
            out.append((p, t, rad, turn))
    return out


def regions(hits, link=2.5):
    """Chain hits closer than `link` into regions (lists of hits)."""
    n = len(hits)
    par = list(range(n))

    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    P = np.array([h[0] for h in hits]) if n else np.zeros((0, 3))
    for i in range(n):
        d = np.linalg.norm(P[i + 1:] - P[i], axis=1)
        for j in np.nonzero(d < link)[0]:
            par[f(i)] = f(i + 1 + int(j))
    g = {}
    for i in range(n):
        g.setdefault(f(i), []).append(hits[i])
    return list(g.values())


def ref_radius(ref, p, t, window=4.0, snap=1.0):
    """The reference mesh's radius at the same spot (nearest surface point within `snap` mm), or None."""
    import trimesh

    q, d, _ = trimesh.proximity.closest_point(ref, [p])
    if d[0] > snap:
        return None
    r = local_radius(ref, q[0], t, window, tri_boxes(ref))
    if r is None:
        return None
    return r[0] if r[1] >= 20.0 else math.inf     # no concave corner there: the reference is not sharp here


# ---------------------------------------------------------------- spec helpers
def _reason(x):
    return isinstance(x, str) and bool(x.strip())


def optouts(raw, parts):
    """(part-level {pid: reason}, region list, findings for missing reasons)."""
    bad, whole, local = [], {}, []
    for p in parts:
        if "sharp_corners_ok" in p._extra:
            v = p._extra.get("sharp_corners_ok")
            if _reason(v):
                whole[p.id] = v
            else:
                bad.append(fail("mfg.sharp_ok_reason", G, BLOCKER, "Sharp-corner opt-out has no reason",
                                f"`{p.id}`: `sharp_corners_ok` needs a non-empty reason string; the opt-out is ignored.")
                           .on(p.id).fix('Write why the sharp corner is fine, e.g. "sharp_corners_ok": "TPU, flexes"'))
    for e in (raw or {}).get("sharp_ok") or []:
        if _reason(e.get("reason")) and e.get("part") and e.get("near") is not None:
            local.append(e)
        else:
            bad.append(fail("mfg.sharp_ok_reason", G, BLOCKER, "Sharp-corner opt-out has no reason",
                             f"`sharp_ok` entry {e} needs `part`, `near` and a non-empty `reason`; it is ignored.")
                       .on(str(e.get("part"))))
    return whole, local, bad


def _near(e, p, default_r=3.0):
    return float(np.linalg.norm(np.asarray(e["near"], float) - p)) <= float(e.get("r_mm", default_r))


def intent_lines(raw):
    """{part: [(axis index, (u, v))]}: corners owned by an intent `fillet` entry (vertical lines through u, v)."""
    out = {}
    for e in (raw or {}).get("intent") or []:
        if e.get("rule") == "fillet":
            ax = "xyz".index(e["axis"])
            out.setdefault(e["part"], []).extend((ax, tuple(uv)) for uv in e.get("at", []))
    return out


def _on_intent(lines, p, tol=1.5):
    for ax, uv in lines:
        a, b = [i for i in range(3) if i != ax]
        if math.dist((p[a], p[b]), uv) <= tol:
            return True
    return False


def _ref_meshes(ctx):
    from .reference_cad import _cfg, ref_in_world

    cfg = _cfg(ctx.r.spec)
    base = Path(getattr(ctx.r.spec, "base_dir", ".") or ".")
    rdir = base / (cfg.get("dir") or ".")
    out = {}
    for e in cfg.get("parts") or []:
        if e.get("mode", "shape") != "shape" or e.get("ref_to_world", cfg.get("ref_to_world")) is None:
            continue
        out[e.get("part")] = (rdir / (e.get("file") or ""), e, cfg)
    return out


def _load_ref(entry):
    import trimesh

    from .reference_cad import ref_in_world

    path, e, cfg = entry
    if not path.is_file():
        return None
    return ref_in_world(trimesh.load(path, force="mesh"), e, cfg)


def load_zones(ctx, body, prm):
    """[(label, fn(point) -> bool)] for the load path of one part (world frame)."""
    from scipy.spatial import cKDTree

    raw = ctx.r.spec.raw or {}
    d = prm["load_dist_mm"]
    lo, hi = body.aabb
    zones = []
    for b in ctx.world.bodies:
        if b.id == body.id or b.is_wire:
            continue
        blo, bhi = b.aabb
        if np.any(blo > hi + d) or np.any(bhi < lo - d):
            continue
        rp = next((x for x in ctx.r.parts if x.part.id == b.id), None)
        if b.fastener:
            label = f"fastener `{b.id}`"
        elif rp is not None and rp.part.kind in LOAD_KINDS and body.kind in LOAD_KINDS:
            label = f"joint with `{b.id}`"
        else:
            continue
        pts = b.mesh.sample(4000, return_index=False) if len(b.mesh.faces) else b.mesh.vertices
        tr = cKDTree(np.vstack([pts, b.mesh.vertices]))
        zones.append((label, lambda p, tr=tr, b=b: tr.query(p)[0] <= d or bool(b.inside([p])[0])))
    for key in ("sharp_corner_loads", "load_interfaces"):
        for e in raw.get(key) or []:
            if e.get("part") not in (None, body.id) or e.get("near") is None:
                continue
            zones.append((f"declared load {e.get('near')}", lambda p, e=e: _near(e, p, d)))
    return zones


# ---------------------------------------------------------------- group
def run(ctx):
    raw = ctx.r.spec.raw or {}
    prm = params(raw)
    made = [rp for rp in ctx.r.parts if rp.part.catalog is None and catalog.process_canon(rp.part.process) in PROCESSES]
    whole, local, out = optouts(raw, [rp.part for rp in made])
    lines = intent_lines(raw)
    refs = _ref_meshes(ctx)
    n_clean, rows = 0, []
    for rp in made:
        p = rp.part
        body = ctx.world.body(p.id)
        if body is None or body.mesh is None or not len(body.mesh.faces):
            ctx.not_checked.append(f"Sharp internal corners of `{p.id}`: no mesh")
            continue
        if p.id in whole:
            out.append(note(CID, G, "Sharp corners accepted", f"`{p.id}` opts out: {whole[p.id]}").on(p.id))
            continue
        lim = max(prm["min_r_mm"], prm["load_min_r_mm"])
        try:
            hits = scan(body.mesh, lim, prm["window_mm"], prm["grid_mm"], prm["min_turn_deg"])
        except Exception as ex:  # noqa: BLE001 - fail closed
            out.append(fail(CID, G, WARNING, "Sharp-corner scan could not run", f"`{p.id}`: {type(ex).__name__}: {ex}").on(p.id))
            ctx.not_checked.append(f"Sharp internal corners of `{p.id}`")
            continue
        hits = [h for h in hits if not _on_intent(lines.get(p.id, []), h[0])]
        zones = load_zones(ctx, body, prm) if hits else []
        ref = None
        sev_groups = {BLOCKER: [], WARNING: [], INFO: []}
        for reg in regions(hits, prm["link_mm"]):
            worst = min(reg, key=lambda h: h[2])
            loads = sorted({lab for lab, fn in zones for h in reg if fn(h[0])})
            r_ours = worst[2]
            if loads:
                if r_ours >= prm["load_min_r_mm"]:
                    continue
                sev = BLOCKER
            else:
                if r_ours >= prm["min_r_mm"]:
                    continue
                sev = WARNING
            opt = next((e for e in local if e["part"] == p.id and any(_near(e, h[0]) for h in reg)), None)
            r_ref = None
            if p.id in refs:
                if ref is None:
                    try:
                        ref = _load_ref(refs[p.id]) or False
                    except Exception:  # noqa: BLE001
                        ref = False
                if ref is not False:
                    r_ref = ref_radius(ref, worst[0], worst[1], prm["window_mm"])
            row = {"part": p.id, "at": np.round(worst[0], 2).tolist(), "r_mm": round(r_ours, 2),
                   "turn_deg": round(worst[3], 0), "n": len(reg), "loads": loads[:3],
                   "ref_r_mm": None if r_ref is None else (round(r_ref, 2) if math.isfinite(r_ref) else "no corner"),
                   "severity": sev}
            if opt is not None:
                row.update(severity=INFO, why=f"opt-out: {opt['reason']}")
            elif r_ref is not None and r_ours >= r_ref - prm["ref_tol_mm"]:
                row.update(severity=INFO, why="matches original")
            rows.append(row)
            sev_groups[row["severity"]].append(row)
        for sev in (BLOCKER, WARNING):
            rs = sev_groups[sev]
            if not rs:
                continue
            lim_s = prm["load_min_r_mm"] if sev == BLOCKER else prm["min_r_mm"]
            txt = "; ".join(_fmt(r) for r in sorted(rs, key=lambda r: r["r_mm"])[:8])
            more = f" (+{len(rs) - 8} more)" if len(rs) > 8 else ""
            w = min(rs, key=lambda r: r["r_mm"])
            out.append(fail(CID, G, sev, "Sharp internal corner" + (" in a load path" if sev == BLOCKER else ""),
                            f"`{p.id}` ({p.process}): {len(rs)} concave corner region(s) below r {lim_s:g} mm: {txt}{more}.")
                       .on(p.id).here(w["at"]).expect(f"r >= {lim_s:g} mm", f"r {w['r_mm']:.2f} mm")
                       .fix("Fillet the inside corner (PLA cracks from a sharp notch), or opt out with "
                            "`sharp_ok: [{part, near, r_mm, reason}]` / part `sharp_corners_ok: \"reason\"`."))
        if sev_groups[INFO]:
            txt = "; ".join(_fmt(r) for r in sev_groups[INFO][:8])
            out.append(note(CID, G, "Sharp corners accepted", f"`{p.id}`: {len(sev_groups[INFO])} region(s): {txt}.").on(p.id))
        if not sev_groups[BLOCKER] and not sev_groups[WARNING]:
            n_clean += 1
    ctx.metrics["sharp_internal_corner"] = rows
    if n_clean:
        out.append(ok(CID + ".ok", G, "No sharp internal corners", f"{n_clean} printed/moulded part(s) have no internal "
                      f"corner below r {prm['min_r_mm']:g} mm (r {prm['load_min_r_mm']:g} mm in load paths)."))
    return out


def _fmt(r):
    s = f"({', '.join(f'{x:.1f}' for x in r['at'])}) r {r['r_mm']:.2f}"
    if r["loads"]:
        s += " near " + ", ".join(r["loads"])
    if r["ref_r_mm"] is not None:
        s += f", reference r {r['ref_r_mm']}"
    if r.get("why"):
        s += f" [{r['why']}]"
    return s

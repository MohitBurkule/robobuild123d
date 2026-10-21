"""practice: best-CAD-practice checks that need NO reference (no STEP, no SolidWorks dump). Each one is a cause from
review/code/MISSES.md (RV01 / RV17 rebuild vs the designer's feature tree) turned into a rule our own model must keep.

  practice.point_table        (code) a coordinate table of >= 4 points (module or function scope) not tagged
                              `# param: organic <why>`: geometry read off a reference as points instead of drawn from
                              dims + relations (RV01 Fillet7: tub2_lobes.SLIT, 4 measured (Y, Z) points).
  practice.symmetry           a part whose surface matches its own mirror (plane through the bbox centre, X, Y or Z)
                              over >= SYM_FRAC of its area is meant symmetric: every asymmetric blob over ASYM_MM x
                              ASYM_AREA_MM2 is flagged (RV01 -X rear corner block 0.5 mm proud, no +X twin).
  practice.mirror_consistency on such a part the blend at each edge sample must match the blend at its mirror image
                              (fillet radius / chamfer within RES_MM; sharp vs blended is a mismatch).
  practice.blend_consistency  along one straight edge run (samples sharing the crease axis, in line within LINE_MM) a
                              blend must not stop partway (a sharp stretch between blended ones: blends picked by edge
                              length, RV17 Fillet1) and one run carries one radius.
  practice.radius_palette     blend radii cluster into a small palette; a radius used on < PALETTE_FRAC of the blended
                              edges and within PALETTE_NEAR_MM of a common one is a slip (R1.5 where the part uses R1).
  practice.chamfer_corners    where a chamfer run ends at a plan corner the next edge round the corner must be
                              chamfered too (a sharp 90 deg corner within CORNER_MM of a chamfer end leaves a lump:
                              RV01 Chamfer3 at the front deck corners).
  practice.drawn_vs_catalog   a catalog part (nut, insert, bearing) sitting in a pocket of its host must be closed round
                              within its declared `pocket_clearance_mm` on every side (sampled round its outline); no
                              declared clearance is itself a finding (the pocket was sized from the catalogue alone).
  practice.waiver_bounds      (reference_cad) a deviation waiver covers ONE blob, the one at its centre; other blobs
                              inside its sphere are still differences (a lobe-tail waiver hid a hex pocket 0.15 off).

Every finding is a BLOCKER; opt out per part with `practice_ok: {"<check suffix>": "<reason, >= 20 chars>"}`.
Mesh measurements use ref_local (mirror gap field) and ref_radii (per-edge blend radius from sections).
"""

from __future__ import annotations

import ast
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, fail, ok

G = "practice"
SYM_FRAC = 0.95
SYM_TOL_MM = 0.2
ASYM_MM = 0.2
ASYM_AREA_MM2 = 2.0
RES_MM = 0.1
LINE_MM = 0.3
RUN_GAP_MM = 1.6
BLEND_MIN_MM = 0.2
PALETTE_FRAC = 0.1
PALETTE_NEAR_MM = 0.5
CHAMFER_TURN = (30.0, 60.0)
CORNER_MM = 1.5
DEFAULT_KINDS = ("structure", "plate", "fork", "armor", "wedge", "other", "weapon", "spacer")
MIN_REASON = 20


# ------------------------------------------------------------------------------------------------ opt-out
def opted(p, check):
    """Reason string when part `p` opts this check out with a usable reason, else None."""
    ok_ = (getattr(p, "_extra", {}) or {}).get("practice_ok") or {}
    why = str(ok_.get(check) or "").strip() if isinstance(ok_, dict) else ""
    return why if len(why) >= MIN_REASON else None


# ------------------------------------------------------------------------------------------------ point tables (code)
def _organic_lines(lines):
    from .param_lint import _organic

    ex, _, _ = _organic(lines)
    return ex


def point_tables(text):
    """[(line, name, n)] of coordinate tables (>= 4 tuples of 2-3 numbers) assigned at ANY scope, not organic-tagged."""
    from .param_lint import TAG

    lines = text.splitlines()
    ex = _organic_lines(lines)

    def tagged(i):
        for j in (i, i - 1):
            if 1 <= j <= len(lines):
                m = TAG.search(lines[j - 1])
                if m and m.group(1) == "organic" and m.group(2).strip():
                    return True
        return False

    def num(e):
        return isinstance(e, ast.Constant) and isinstance(e.value, (int, float)) or (
            isinstance(e, ast.UnaryOp) and isinstance(e.operand, ast.Constant) and isinstance(e.operand.value, (int, float)))

    def is_pt(e):
        return isinstance(e, (ast.Tuple, ast.List)) and len(e.elts) in (2, 3) and all(num(x) for x in e.elts)

    out = []
    for st in ast.walk(ast.parse(text)):
        if not isinstance(st, (ast.Assign, ast.AnnAssign)) or st.lineno in ex or tagged(st.lineno):
            continue
        tg = st.targets if isinstance(st, ast.Assign) else [st.target]
        names = [t.id for t in tg if isinstance(t, ast.Name)]
        v = st.value
        if names and isinstance(v, (ast.Tuple, ast.List)) and len(v.elts) >= 4 and all(is_pt(e) for e in v.elts):
            out.append((st.lineno, names[0], len(v.elts)))
    return out


def two_sided_code(text):
    """[(line, function, values)] of functions that place the same number on both sides (+v and -v literals, |v| >= 1)
    without mirror() / a sign loop: both copies built by hand, so an edit to one side misses the other."""
    out = []
    for fn in ast.walk(ast.parse(text)):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        src = ast.get_source_segment(text, fn) or ""
        if "mirror" in src.lower():
            continue
        if any(isinstance(n, ast.For) and isinstance(n.iter, (ast.Tuple, ast.List)) and len(n.iter.elts) == 2
               and all(isinstance(e, (ast.Constant, ast.UnaryOp)) for e in n.iter.elts) for n in ast.walk(fn)):
            continue   # `for s in (1, -1)`: one code path for both sides
        neg, pos = set(), set()
        for n in ast.walk(fn):
            if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub) and isinstance(n.operand, ast.Constant) \
                    and isinstance(n.operand.value, (int, float)) and abs(n.operand.value) >= 1:
                neg.add(float(n.operand.value))
        for n in ast.walk(fn):
            if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool) and n.value >= 1:
                pos.add(float(n.value))
        both = sorted(neg & pos)
        if len(both) >= 2:
            out.append((fn.lineno, fn.name, both[:6]))
    return out


def code_sources(spec):
    from .param_lint import sources

    try:
        return sources(spec)
    except Exception:  # noqa: BLE001
        return []


# ------------------------------------------------------------------------------------------------ symmetry (mesh)
def symmetry_plane(m, tol=SYM_TOL_MM, frac=SYM_FRAC):
    """(axis, c, fraction) of the best mirror plane through the bbox centre when >= frac of the surface (by area) lies
    within tol of the mirrored part, else None."""
    from .ref_local import gap_field, mirrored

    lo, hi = m.bounds
    best = None
    for ax in range(3):
        c = 0.5 * float(lo[ax] + hi[ax])
        _, d, _ = gap_field(m, mirrored(m, ax, c), tol, spacing=0.5)
        f = float((d <= tol).mean())
        if best is None or f > best[2]:
            best = (ax, c, f)
    return best if best and best[2] >= frac else None


def asymmetric_blobs(m, ax, c, tol=ASYM_MM, area=ASYM_AREA_MM2):
    from .ref_local import blobs, gap_field, mirrored

    P, d, ap = gap_field(m, mirrored(m, ax, c), tol)
    return blobs(P, d, ap, "asymmetric", tol, area)


# ------------------------------------------------------------------------------------------------ blends (mesh)
def blend_map(m):
    from .ref_radii import blend_map as bm

    return bm(m)


def _mirror_pt(p, ax, c):
    q = np.array(p, float)
    q[ax] = 2 * c - q[ax]
    return q


def mirror_mismatches(bmap, ax, c, res=RES_MM, link=1.0):
    """Edge samples whose blend differs from the sample at the mirror image (within link mm, same turn +-15 deg)."""
    from scipy.spatial import cKDTree

    if not bmap:
        return []
    P = np.array([x[0] for x in bmap])
    T = cKDTree(P)
    out = []
    for p, t, r, turn in bmap:
        q = _mirror_pt(p, ax, c)
        d, j = T.query(q)
        if d > link:
            continue
        _, _, r2, turn2 = bmap[j]
        if abs(turn - turn2) <= 15.0 and abs(r - r2) > res:
            out.append((p, r, r2))
    return out


def _runs(bmap, line=LINE_MM, gap=RUN_GAP_MM):
    """Group edge samples into straight runs: same crease axis (|cos| > 0.99), on one line (perpendicular offset <=
    line), consecutive samples <= gap apart. Returns lists of indices ordered along the run."""
    n = len(bmap)
    used = np.zeros(n, bool)
    P = np.array([x[0] for x in bmap]) if n else np.zeros((0, 3))
    runs = []
    for i in range(n):
        if used[i]:
            continue
        t = bmap[i][1]
        q = P - P[i]
        s = q @ t
        perp = np.linalg.norm(q - np.outer(s, t), axis=1)
        par = np.array([abs(float(x[1] @ t)) > 0.99 for x in bmap])
        mem = np.nonzero(par & (perp <= line) & ~used)[0]
        mem = mem[np.argsort(s[mem])]
        # split at gaps
        cur = [mem[0]] if len(mem) else []
        for a, b in zip(mem[:-1], mem[1:]):
            if s[b] - s[a] > gap:
                runs.append(cur)
                cur = []
            cur.append(b)
        if cur:
            runs.append(cur)
        used[mem] = True
    return runs


def blend_breaks(bmap, res=RES_MM):
    """[(point, kind, detail)] per run: a sharp stretch between blended samples (blend stops partway) or more than one
    radius on one run."""
    out = []
    for run in _runs(bmap):
        if len(run) < 3:
            continue
        r = np.array([bmap[i][2] for i in run])
        bl = r > BLEND_MIN_MM
        if bl.any() and (~bl).any():
            k = np.nonzero(bl)[0]
            inner = np.nonzero(~bl)[0]
            inner = inner[(inner > k.min()) & (inner < k.max())]
            if len(inner):
                out.append((bmap[run[int(inner[0])]][0], "stops", f"sharp for {len(inner)} sample(s) inside an R{np.median(r[bl]):.2f} run"))
                continue
        rb = r[bl]
        if len(rb) >= 3 and float(rb.max() - rb.min()) > res:
            out.append((bmap[run[int(np.argmax(r))]][0], "radius", f"R{rb.min():.2f}..R{rb.max():.2f} on one run"))
    return out


def palette_slips(bmap, frac=PALETTE_FRAC, near=PALETTE_NEAR_MM):
    """[(radius, count, common radius, common count, sample point)] one-off radii near a common one."""
    r = np.array([x[2] for x in bmap if x[2] > BLEND_MIN_MM and x[3] < 120.0])
    if not len(r):
        return []
    q = np.round(r / 0.05) * 0.05
    vals, cnt = np.unique(q, return_counts=True)
    # merge neighbours 0.05 apart into one palette entry
    groups = []
    for v, c in zip(vals, cnt):
        if groups and v - groups[-1][-1][0] <= 0.051:
            groups[-1].append((v, c))
        else:
            groups.append([(v, c)])
    pal = [(sum(v * c for v, c in g) / sum(c for _, c in g), sum(c for _, c in g)) for g in groups]
    tot = sum(c for _, c in pal)
    out = []
    for v, c in pal:
        if c >= frac * tot:
            continue
        common = [(w, k) for w, k in pal if k >= 3 * c and k >= frac * tot and 0.1 < abs(w - v) <= near]
        if common:
            w, k = max(common, key=lambda x: x[1])
            at = next(x[0] for x in bmap if abs(x[2] - v) < 0.06)
            out.append((round(v, 2), int(c), round(w, 2), int(k), at))
    return out


def chamfer_corner_lumps(bmap, corner=CORNER_MM):
    """Sharp ~90 deg corners within `corner` mm of a chamfer sample whose crease runs another way (the chamfer stops at
    a plan corner and leaves the corner square)."""
    from scipy.spatial import cKDTree

    ch = [x for x in bmap if x[2] <= BLEND_MIN_MM and CHAMFER_TURN[0] <= x[3] <= CHAMFER_TURN[1]]
    sq = [x for x in bmap if x[2] <= BLEND_MIN_MM and 75.0 <= x[3] <= 105.0]
    if not ch or not sq:
        return []
    T = cKDTree(np.array([x[0] for x in ch]))
    out = []
    for p, t, _, turn in sq:
        for j in T.query_ball_point(p, corner):
            if abs(float(ch[j][1] @ t)) < 0.7:   # the chamfer crease turns the corner: a different edge direction
                out.append((p, ch[j][0]))
                break
    return out


# ------------------------------------------------------------------------------------------------ pockets (world)
def pocket_gaps(cots_mesh, host_mesh, n=600):
    """Distances from samples on a catalog part's side surface to the host's surface: a pocket closes round it when
    every sample is within the clearance. Samples facing along the pocket axis (top / bottom faces) are skipped."""
    import trimesh

    from .ref_diff import closest_dist_chunked

    P, fi = trimesh.sample.sample_surface(cots_mesh, n, seed=7)
    N = cots_mesh.face_normals[fi]
    # pocket axis: the cots part's thinnest extent direction (a nut's axis)
    ax = int(np.argmin(cots_mesh.extents))
    side = np.abs(N[:, ax]) < 0.5
    if not side.any():
        return np.zeros(0)
    return closest_dist_chunked(host_mesh, P[side])


# ------------------------------------------------------------------------------------------------ run
def _mesh(ctx, pid):
    b = ctx.world.body(pid)
    return None if b is None else b.mesh


def run(ctx):
    out = []
    spec = ctx.r.spec
    # 1. point tables in the build code
    bad, two = [], []
    for path in code_sources(spec):
        try:
            text = Path(path).read_text()
        except OSError:
            continue
        bad += [f"{Path(path).name}:{ln} `{nm}` ({n} points)" for ln, nm, n in point_tables(text)]
        two += [f"{Path(path).name}:{ln} `{nm}` (+-{', +-'.join(f'{v:g}' for v in vs)})" for ln, nm, vs in two_sided_code(text)]
    out.append(fail("practice.symmetry", G, BLOCKER, "Both sides built by hand",
                    f"{len(two)} function(s) place the same numbers at + and - without mirror() or a sign loop: " + "; ".join(two[:12]))
               .fix("Build one side and mirror() it (or loop `for s in (1, -1)`), so an edit reaches both copies.") if two else
               ok("practice.symmetry", G, "Two-sided geometry comes from one code path", "No hand-built +/- pairs."))
    out.append(fail("practice.point_table", G, BLOCKER, "Coordinate tables in the build code",
                    f"{len(bad)} table(s) of measured points instead of dims + relations: " + "; ".join(bad[:12]))
               .fix("Draw the outline as a sketch with dims and relations (or tag `# param: organic <why>`).") if bad else
               ok("practice.point_table", G, "No coordinate tables", "Build code has no untagged point tables."))
    # mesh checks per printed / shaped part
    for rp in ctx.r.parts:
        p = rp.part
        if p.kind not in DEFAULT_KINDS or not isinstance(p.shape, dict) or p.process in (None, "cots"):
            continue
        m = _mesh(ctx, p.id)
        if m is None or len(m.faces) < 20:
            continue
        out += part_findings(p, m)
    out += pocket_findings(ctx)
    return out


def part_findings(p, m):
    out = []
    pid = p.id
    sym = symmetry_plane(m)
    bmap = None

    def emit(check, title, items, fmt, fix):
        why = opted(p, check)
        if not items:
            out.append(ok(f"practice.{check}", G, title, f"`{pid}`: none.").on(pid))
        elif why:
            out.append(ok(f"practice.{check}", G, title, f"`{pid}`: {len(items)} opted out: {why}").on(pid))
        else:
            out.append(fail(f"practice.{check}", G, BLOCKER, title, f"`{pid}`: " + "; ".join(fmt(x) for x in items[:10])
                            + (f" ... ({len(items)})" if len(items) > 10 else "")).on(pid).fix(fix))

    if sym is not None:
        ax, c, f = sym
        ab = asymmetric_blobs(m, ax, c)
        emit("symmetry", "Symmetric part is symmetric", ab,
             lambda b: f"{b['area_mm2']} mm2 up to {b['max_mm']} mm off its mirror at {b['centroid']} ({'XYZ'[ax]} = {c:.2f} plane, part {f:.0%} symmetric)",
             "Build one side and mirror() it; a one-sided leftover means the two copies were built separately.")
        bmap = blend_map(m)
        mm = mirror_mismatches(bmap, ax, c)
        emit("mirror_consistency", "Mirrored copies carry the same blends", _cluster_pts(mm),
             lambda g: f"{len(g)} edge sample(s) near {np.round(g[0][0], 2).tolist()}: R{g[0][1]:.2f} here vs R{g[0][2]:.2f} at the mirror image",
             "Blend the seed, then mirror / pattern the blended body so every copy carries the same fillets and chamfers.")
    if bmap is None:
        bmap = blend_map(m)
    emit("blend_consistency", "Blends run the whole edge", blend_breaks(bmap),
         lambda x: f"{x[1]} at {np.round(x[0], 2).tolist()}: {x[2]}",
         "Select the whole tangent edge chain for a blend (not edges by length) and give it one radius.")
    emit("radius_palette", "Blend radii from a small palette", palette_slips(bmap),
         lambda x: f"R{x[0]} on {x[1]} sample(s) (e.g. {np.round(x[4], 2).tolist()}) next to the part's common R{x[2]} ({x[3]})",
         "Use the part's common radius, or name the odd one as its own param with the reason.")
    emit("chamfer_corners", "Chamfers turn their corners", _cluster_pts([(a, b, 0) for a, b in chamfer_corner_lumps(bmap)]),
         lambda g: f"square corner at {np.round(g[0][0], 2).tolist()} beside a chamfer ending at {np.round(g[0][1], 2).tolist()}",
         "Run the chamfer round the corner (chamfer the whole loop, or the corner edge too).")
    return out


def _cluster_pts(items, link=2.0):
    """Group (point, ...) tuples within link mm: one entry (a list) per place."""
    from .ref_local import cluster

    if not items:
        return []
    P = np.array([np.asarray(x[0], float) for x in items])
    k, lab = cluster(P, link)
    return [[items[j] for j in np.nonzero(lab == i)[0]] for i in range(k)]


def _host_of(ctx, pid, cm, near=1.0):
    """The shaped part whose surface lies closest round a catalog part's sides (its pocket), within `near` mm."""
    import trimesh

    from .ref_diff import closest_dist_chunked

    P = trimesh.sample.sample_surface(cm, 60, seed=3)[0]
    lo, hi = cm.bounds[0] - near, cm.bounds[1] + near
    best = None
    for rp in ctx.r.parts:
        q = rp.part
        if q.id == pid or q.kind not in DEFAULT_KINDS or not isinstance(q.shape, dict):
            continue
        m = _mesh(ctx, q.id)
        if m is None or np.any(m.bounds[1] < lo) or np.any(m.bounds[0] > hi):
            continue
        d = float(np.median(closest_dist_chunked(m, P)))
        if d <= near and (best is None or d < best[0]):
            best = (d, q.id)
    return best[1] if best else None


def pocket_findings(ctx):
    """practice.drawn_vs_catalog: every catalog nut / insert / bearing seated in a host part closes within its declared
    clearance; one finding per robot."""
    out, bad, n = [], [], 0
    for rp in ctx.r.parts:
        p = rp.part
        if p.catalog is None or p.kind not in ("nut", "insert", "bearing"):
            continue
        host = getattr(p, "parent", None) or (getattr(p, "_extra", {}) or {}).get("host")
        cm = _mesh(ctx, p.id)
        if cm is None:
            continue
        if not host:
            host = _host_of(ctx, p.id, cm)
        hm = _mesh(ctx, host) if host else None
        if hm is None or cm is None:
            continue
        n += 1
        if opted(p, "drawn_vs_catalog"):
            continue
        clr = (getattr(p, "_extra", {}) or {}).get("pocket_clearance_mm")
        d = pocket_gaps(cm, hm)
        if not len(d):
            continue
        if clr is None:
            bad.append(f"`{p.id}` in `{host}`: no `pocket_clearance_mm` declared (wall gap {d.min():.2f}..{d.max():.2f} mm)")
        elif float(d.max()) > float(clr) + 0.05:
            bad.append(f"`{p.id}` in `{host}`: wall gap up to {d.max():.2f} mm vs declared clearance {float(clr):.2f}")
    if not n:
        return out
    out.append(fail("practice.drawn_vs_catalog", G, BLOCKER, "Pocket not drawn round its part", "; ".join(bad[:12]))
               .fix("Size the pocket from the part's outline plus a declared `pocket_clearance_mm`, closing on every side.") if bad else
               ok("practice.drawn_vs_catalog", G, "Pockets close round their parts", f"{n} catalog part pocket(s) within clearance."))
    return out

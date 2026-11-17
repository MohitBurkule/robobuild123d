"""`robot probe`: measured facts about a placed robot, so an LLM looks numbers up instead of deriving them.

    python3 -m robot probe spec.json                     every part: world box, volume, mass, contacts
    python3 -m robot probe spec.json battery             one part: box, ports in world, gap to each neighbour
    python3 -m robot probe spec.json --joint flipper     sweep a joint over its range (others at default, exactly
                                                          as the verifier does): closest approach per other part
    python3 -m robot probe spec.json --at 1.3,0,33.1     what is at / near a world point
    python3 -m robot probe spec.json --place battery     free (x, y, yaw) spots for a part, checked like the verifier

All numbers come from the same meshes the verifier uses (fast tessellation unless --fine).
"""

from __future__ import annotations

import json

import numpy as np

NEAR_MM = 3.0


def _load(spec_path, fine=False):
    from . import spec as spec_mod, world as world_mod

    s = spec_mod.load(spec_path)
    r = world_mod.resolve(s, fast=not fine)
    return s, r, world_mod.World.start(r)


def _fmt_box(b):
    lo, hi = b
    return f"x {lo[0]:.2f}..{hi[0]:.2f}  y {lo[1]:.2f}..{hi[1]:.2f}  z {lo[2]:.2f}..{hi[2]:.2f}"


def neighbours(w, body, r, near=NEAR_MM):
    """[(other id, gap mm (0 = touching), overlap depth mm)] for bodies within `near`."""
    from . import measure
    from .checks.interference import allowed_depth

    out = []
    for o in w.bodies:
        if o.id == body.id or o.is_wire or not measure.aabb_overlap(body.aabb, o.aabb, near):
            continue
        ov = measure.overlap(body, o)
        if ov is not None and ov.depth > 1e-4:
            out.append((o.id, 0.0, float(ov.depth), allowed_depth(r, body, o)))
            continue
        g = measure.min_gap(body, o, near)
        if np.isfinite(g):
            out.append((o.id, float(g), 0.0, allowed_depth(r, body, o)))
    return sorted(out, key=lambda t: (t[1], -t[2]))


def part_report(s, r, w, pid):
    b = w.body(pid)
    if b is None:
        return f"no part `{pid}`; parts: {', '.join(x.id for x in w.bodies)}"
    lines = [f"{pid}: {_fmt_box(b.aabb)}  size {' x '.join(f'{v:.2f}' for v in b.aabb[1] - b.aabb[0])} mm",
             f"  centre ({', '.join(f'{v:.2f}' for v in b.center)}), volume {b.geom.volume:.1f} mm3"]
    if b.part_idx is not None:
        rp = r.parts[b.part_idx]
        ports = dict(rp.cat.ports) if rp.cat is not None else {}
        ports.update(rp.part.ports or {})
        for name in sorted(ports):
            p = w.port(r, f"{pid}.{name}")
            if p is not None:
                lines.append(f"  port {name}: ({', '.join(f'{v:.2f}' for v in p)})")
        if rp.part.joint is not None:
            j = rp.part.joint
            lines.append(f"  joint {j.kind} axis {j.axis} pivot {j.pivot} range {j.min}..{j.max} default {j.default}")
        if rp.part.parent:
            lines.append(f"  parent {rp.part.parent} (moves with it)")
    for oid, gap, depth, allow in neighbours(w, b, r):
        if depth > 0:
            tag = "OVERLAP" if depth > allow else "overlap allowed"
            lines.append(f"  {tag} `{oid}` {depth:.2f} mm (allowed {allow:.2f})")
        else:
            lines.append(f"  gap to `{oid}` {gap:.2f} mm" + (" (touching)" if gap < 1e-3 else ""))
    return "\n".join(lines)


def joint_sweep(s, r, jid, n=24):
    """Closest approach of the joint's moving set to every other body over the joint range."""
    from . import measure, world as world_mod
    from .checks.interference import allowed_depth, descendants

    p = next((x for x in s.parts if x.id == jid), None)
    if p is None or p.joint is None:
        return f"`{jid}` has no joint"
    j = p.joint
    moving = descendants(r, jid)
    best = {}
    for k in range(n + 1):
        v = j.min + (j.max - j.min) * k / n
        w = world_mod.World.build(r, {jid: v})
        for a in w.bodies:
            if a.id not in moving:
                continue
            for o in w.bodies:
                if o.id in moving or o.is_wire or not measure.aabb_overlap(a.aabb, o.aabb, NEAR_MM):
                    continue
                ov = measure.overlap(a, o)
                if ov is not None and ov.depth > 1e-4:
                    m = -float(ov.depth)
                else:
                    g = measure.min_gap(a, o, NEAR_MM)
                    if not np.isfinite(g):
                        continue
                    m = float(g)
                if o.id not in best or m < best[o.id][0]:
                    best[o.id] = (m, v, a.id, allowed_depth(r, a, o))
    lines = [f"joint `{jid}` {j.kind} {j.min}..{j.max} ({n + 1} poses), moving: {', '.join(sorted(moving))}"]
    if not best:
        lines.append(f"  nothing comes within {NEAR_MM} mm")
    for oid, (m, v, aid, allow) in sorted(best.items(), key=lambda t: t[1][0]):
        what = f"HITS {-m:.2f} mm deep" if m < -allow else (f"overlap {-m:.2f} mm (allowed)" if m < 0 else f"closest {m:.2f} mm")
        lines.append(f"  `{oid}` vs `{aid}`: {what} at {v:.1f}")
    return "\n".join(lines)


def point_report(w, P):
    P = np.asarray(P, float)
    rows = []
    for b in w.bodies:
        if b.is_wire:
            continue
        lo, hi = b.aabb
        if np.all(P >= lo - NEAR_MM) and np.all(P <= hi + NEAR_MM):
            d = float(b.sdf(P[None])[0])
            rows.append((d, b.id))
    rows.sort()
    return "\n".join([f"point ({', '.join(f'{v:.2f}' for v in P)}):"] +
                     [f"  {'inside' if d < 0 else 'from'} `{i}` {abs(d):.2f} mm" for d, i in rows] or ["  nothing near"])


def mass_report(s, r, w):
    """Mass per part (same rules as the mass check), biggest first, plus parts that look like solid blocks."""
    from .checks import Ctx, Options
    from .checks import mass as mass_chk

    ctx = Ctx(r, w, Options(fast=True))
    fs = mass_chk.run(ctx)
    rows = sorted(((k.split(".", 1)[1], v) for k, v in ctx.metrics.items() if k.startswith("part_mass_g.")), key=lambda t: -t[1])
    total = ctx.metrics.get("mass_total_g", sum(v for _, v in rows))
    limit = ctx.metrics.get("mass_limit_g", 150)
    lines = [f"mass {total:.1f} g of {limit:.0f} g ({limit - total:+.1f} g margin)"]
    for pid, g in rows:
        b = w.body(pid)
        fill = ""
        if b is not None:
            bv = float(np.prod(b.aabb[1] - b.aabb[0]))
            frac = b.geom.volume / bv if bv > 0 else 0
            fill = f"  fills {frac:.0%} of its box" + ("  <- solid block? a tub should be a shell" if frac > 0.55 and g > 15 else "")
        lines.append(f"  {pid:<24} {g:7.2f} g{fill}")
    lines += [f"  {f.id}: {f.message}" for f in fs if not f.passed]
    return "\n".join(lines)


PLACE_STEP, PLACE_TOP, PLACE_ROTS = 2.0, 8, (0, 90, 180, 270)


def _rot_z(deg):
    t = np.radians(deg)
    R = np.eye(4)
    R[:2, :2] = [[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]]
    return R


def _occ(bodies, X, Y, Z):
    """Occupancy grid (len X, len Y, len Z) of the union of `bodies` sampled at voxel centres."""
    G = np.zeros((len(X), len(Y), len(Z)), bool)
    for o in bodies:
        lo, hi = o.aabb
        ix = np.nonzero((X >= lo[0]) & (X <= hi[0]))[0]
        iy = np.nonzero((Y >= lo[1]) & (Y <= hi[1]))[0]
        iz = np.nonzero((Z >= lo[2]) & (Z <= hi[2]))[0]
        if not (len(ix) and len(iy) and len(iz)):
            continue
        P = np.stack(np.meshgrid(X[ix], Y[iy], Z[iz], indexing="ij"), -1).reshape(-1, 3)
        ins = o.inside(P).reshape(len(ix), len(iy), len(iz))
        G[np.ix_(ix, iy, iz)] |= ins
    return G


def _largest_rect(M):
    """(i0, i1, j0, j1) inclusive of the largest all-True axis-aligned rectangle in a 2D bool array (histogram method)."""
    n, m = M.shape
    h = np.zeros(m, int)
    best = (0, None)
    for i in range(n):
        h = np.where(M[i], h + 1, 0)
        st = []
        for j in range(m + 1):
            cur = h[j] if j < m else 0
            start = j
            while st and st[-1][1] >= cur:
                s0, hh = st.pop()
                area = hh * (j - s0)
                if area > best[0]:
                    best = (area, (i - hh + 1, i, s0, j - 1))
                start = s0
            st.append((start, cur))
    return best[1]


def _exact_ok(rb, sh, obst, r):
    from . import measure
    from .checks.interference import allowed_depth
    for o in obst:
        if measure.aabb_overlap(rb.aabb + sh, o.aabb):
            al = allowed_depth(r, rb, o)
            ov = measure.overlap(rb, o, sh, cap=al)
            if ov is not None and ov.depth > al:
                return False
    return True


def _ranges(free, X, Y, plo, o0, zc, pitch, deg, rb, obst, r):
    """Safe x / y intervals for the part origin at one yaw, from the free-shift map eroded by one cell (margin for the
    voxel approximation); corners + centre of each interval re-checked exactly, shrunk until they pass."""
    from scipy import ndimage

    F = ndimage.binary_erosion(free, iterations=1)
    to_x = lambda i: X[i] - pitch / 2 - plo[0] + o0[0]  # noqa: E731
    to_y = lambda j: Y[j] - pitch / 2 - plo[1] + o0[1]  # noqa: E731
    sh_of = lambda x, y: np.array([x, y, zc]) - rb.M[:3, 3]  # noqa: E731
    out = []
    ic = int(round((plo[0] + pitch / 2 - X[0]) / pitch))
    jc = int(round((plo[1] + pitch / 2 - Y[0]) / pitch))
    if 0 <= ic < F.shape[0] and 0 <= jc < F.shape[1] and F[ic, jc]:
        row, col = F[:, jc], F[ic, :]
        a = ic
        while a > 0 and row[a - 1]:
            a -= 1
        b = ic
        while b < len(row) - 1 and row[b + 1]:
            b += 1
        c = jc
        while c > 0 and col[c - 1]:
            c -= 1
        d = jc
        while d < len(col) - 1 and col[d + 1]:
            d += 1
        out.append(f"  yaw +{deg}, y kept {o0[1]:.1f}: x in [{to_x(a):.1f}, {to_x(b):.1f}];  x kept {o0[0]:.1f}: "
                   f"y in [{to_y(c):.1f}, {to_y(d):.1f}]")
    rect = _largest_rect(F)
    for _ in range(6):
        if rect is None:
            break
        i0, i1, j0, j1 = rect
        pts = [(i0, j0), (i0, j1), (i1, j0), (i1, j1), ((i0 + i1) // 2, (j0 + j1) // 2)]
        if all(_exact_ok(rb, sh_of(to_x(i), to_y(j)), obst, r) for i, j in pts):
            out.append(f"  yaw +{deg} box: x in [{to_x(i0):.1f}, {to_x(i1):.1f}] AND y in [{to_y(j0):.1f}, {to_y(j1):.1f}] "
                       f"(any combination)")
            break
        rect = (i0 + 1, i1 - 1, j0 + 1, j1 - 1) if i1 - i0 > 2 and j1 - j0 > 2 else None
    return out


def place(s, r, w, pid, step=PLACE_STEP, rots=PLACE_ROTS, z=None, top=PLACE_TOP, region=None, pitch=0.5):
    """Free spots for one part: every x,y shift (its z kept) x extra yaw about its own origin. Collision-free shifts for
    ALL positions at once by voxel correlation (FFT), then the best few re-checked with the verifier's own exact overlap
    test and allowances. Wires and screws ignored; the part's children are left out and must move with it. Ranked by
    clearance (distance to the nearest colliding shift), then distance from now. Replaces hand packing in the head."""
    from scipy import ndimage, signal

    from . import measure
    from .checks.interference import allowed_depth, descendants
    from .world import Body

    b = w.body(pid)
    if b is None:
        return f"no part `{pid}`"
    kids = descendants(r, pid)
    obst = [o for o in w.bodies if o.id not in kids and not o.is_wire and not o.fastener]
    structs = [o for o in obst if o.kind in ("structure", "plate", "armor", "chassis", "panel")] or obst
    if region is None:
        lo = np.min([o.aabb[0] for o in structs], axis=0)
        hi = np.max([o.aabb[1] for o in structs], axis=0)
        region = (lo[0], hi[0], lo[1], hi[1])
    o0 = b.M[:3, 3].copy()
    zc = o0[2] if z is None else float(z)
    res, rng_lines = [], []
    for deg in rots:
        M = b.M.copy()
        M[:3, :3] = _rot_z(deg)[:3, :3] @ b.M[:3, :3]
        M[:3, 3] = [o0[0], o0[1], zc]
        rb = Body(pid, b.kind, b.geom, M, b.color, b.part_idx)
        plo, phi = rb.aabb
        # part voxels, on a grid anchored at its own box corner
        PX = np.arange(plo[0] + pitch / 2, phi[0], pitch)
        PY = np.arange(plo[1] + pitch / 2, phi[1], pitch)
        PZ = np.arange(plo[2] + pitch / 2, phi[2], pitch)
        Pg = _occ([rb], PX, PY, PZ)
        # world voxels over the region (part box may sit anywhere inside it), same z planes
        X = np.arange(region[0] + pitch / 2, region[1], pitch)
        Y = np.arange(region[2] + pitch / 2, region[3], pitch)
        if len(X) < len(PX) or len(Y) < len(PY):
            continue
        Og = _occ(obst, X, Y, PZ)
        C = sum(signal.fftconvolve(Og[:, :, k].astype(float), Pg[::-1, ::-1, k].astype(float), mode="valid")
                for k in range(len(PZ)) if Pg[:, :, k].any())
        free = C < 0.5
        if not free.any():
            continue
        clear = ndimage.distance_transform_edt(free) * pitch
        try:
            rng_lines += _ranges(free, X, Y, plo, o0, zc, pitch, deg, rb, obst, r)
        except Exception as e:  # noqa: BLE001
            rng_lines.append(f"  yaw +{deg}: ranges not measured ({e})")
        # shift index (i, j): part box corner at X[i]-pitch/2, Y[j]-pitch/2 -> origin position
        ii, jj = np.nonzero(free)
        ox = X[ii] - pitch / 2 - plo[0] + o0[0]
        oy = Y[jj] - pitch / 2 - plo[1] + o0[1]
        cl = clear[ii, jj]
        dist = np.hypot(ox - o0[0], oy - o0[1])
        # snap to the requested step so answers are round numbers, keep the best per cell
        seen = set()
        for k in np.lexsort((dist, -np.round(cl, 1))):
            key = (round(ox[k] / step), round(oy[k] / step))
            if key in seen:
                continue
            seen.add(key)
            res.append((float(cl[k]), float(dist[k]), float(ox[k]), float(oy[k]), deg, rb))
            if len(seen) > 4 * top:
                break
    res.sort(key=lambda t: (-round(t[0], 1), t[1]))
    lines, n = [], 0
    for g, dist, x, y, deg, rb in res:
        sh = np.array([x, y, zc]) - rb.M[:3, 3]
        bad = []
        for o in obst:
            if measure.aabb_overlap(rb.aabb + sh, o.aabb):
                al = allowed_depth(r, rb, o)
                ov = measure.overlap(rb, o, sh, cap=al)
                if ov is not None and ov.depth > al:
                    bad.append(o.id)
        if bad:
            continue
        box = rb.aabb + sh
        lines.append(f"  at ({x:.1f}, {y:.1f}, {zc:.2f}) yaw +{deg}: >= {g:.1f} mm free travel every way, {dist:.1f} mm from now; "
                     f"box x {box[0][0]:.1f}..{box[1][0]:.1f} y {box[0][1]:.1f}..{box[1][1]:.1f}")
        n += 1
        if n >= top:
            break
    if not lines:
        return (f"`{pid}`: no free spot at z {zc:.2f} with yaw {list(rots)} inside x {region[0]:.1f}..{region[1]:.1f} "
                f"y {region[2]:.1f}..{region[3]:.1f}. Something else must move (try `probe --place` on it), or change z / the part.")
    return "\n".join([f"`{pid}` free spots (yaw added to its current rot; spec `at` = origin; children "
                      f"{sorted(kids - {pid}) or 'none'} move with it; exact-checked like the verifier):"] + lines
                     + ([f"`{pid}` SAFE RANGES (any value inside is clear; assumes every other part stays put; "
                         "re-run after moving another part):"] + rng_lines if rng_lines else []))


def overview(s, r, w):
    out = []
    for b in w.bodies:
        if b.is_wire:
            continue
        out.append(f"{b.id:<24} {_fmt_box(b.aabb)}  vol {b.geom.volume:8.1f} mm3")
    return "\n".join(out)


def add_cli(sub):
    p = sub.add_parser("probe", help="measured boxes, ports, gaps and joint sweeps (look numbers up, don't derive them)")
    p.add_argument("spec")
    p.add_argument("part", nargs="?")
    p.add_argument("--joint", help="sweep this part's joint over its range")
    p.add_argument("--at", help="x,y,z world point: which parts contain / are near it")
    p.add_argument("--place", metavar="PART", help="list free spots (x, y, yaw) for this part, checked like the verifier")
    p.add_argument("--step", type=float, default=PLACE_STEP, help="--place grid step mm")
    p.add_argument("--region", help="--place: xlo,xhi,ylo,yhi (default: the structure box)")
    p.add_argument("--mass", action="store_true", help="mass budget per part (flags solid blocks)")
    p.add_argument("--fine", action="store_true")
    p.add_argument("--json", action="store_true", help="(overview) JSON boxes")
    p.set_defaults(func=_cli)


def _cli(a):
    s, r, w = _load(a.spec, a.fine)
    if a.place:
        reg = tuple(float(v) for v in a.region.split(",")) if a.region else None
        print(place(s, r, w, a.place, step=a.step, region=reg))
    elif a.mass:
        print(mass_report(s, r, w))
    elif a.joint:
        print(joint_sweep(s, r, a.joint))
    elif a.at:
        print(point_report(w, [float(v) for v in a.at.split(",")]))
    elif a.part:
        print(part_report(s, r, w, a.part))
    elif a.json:
        print(json.dumps({b.id: [list(map(float, b.aabb[0])), list(map(float, b.aabb[1]))] for b in w.bodies}, indent=1))
    else:
        print(overview(s, r, w))
    return 0

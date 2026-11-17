"""Real-build / real-fight failure modes that had no check (audit 2026-11-17, robot/docs/CHECK_AUDIT.md). Cheap: no
router, no sweeps; uses the router's routes when present, else the declared port -> via -> port polylines, so the
inner tier sees them too.

- wire.outside            any point of a wire's TUBE (centreline +- radius, not just the centreline) outside the closed
                          envelope of the armour/chassis, or below the floor. `external: true` needs `exposed_reason`.
                          The first PORT_FREE_MM next to a port on a part that itself sits outside (exposed weapon
                          motor) are allowed.
- wire.spans_rotation     a wire whose two ends are in different motion groups (static <-> weapon / wheel) winds up and
                          rips off on the first spin. `slip_ring: true` opts out.
- wire.gauge_current      wire gauge vs the current it carries (power: peak robot current; motor: that motor's max).
- wire.strain_relief      a wire soldered to a part (esc, motor, battery, switch, receiver) needs a hold (hole, channel,
                          clip: material on both sides) within STRAIN_MM of the joint, or `strain_relief: "<how>"`.
- connector.rating        battery / power connector rating vs peak current (JST-PH on a spinner melts).
- fastener.lock           machine screws into metal (nut, metal part) on a rotating or motor joint vibrate loose: they
                          need `lock: nyloc | threadlock | thread_forming | locknut | safety_wire`.
- battery.armour_gap      LiPo surface closer than BATTERY_GAP_MM to the outer envelope: a hit dents armour into it.
- battery.rotor_gap       LiPo within BATTERY_ROTOR_MM of a revolved rotor volume.
- heat.neighbour          battery / ESC / receiver touching a motor can (heat soak; ESC thermal cut-out, LiPo puff).
- rf.antenna              receiver whose every line out ends on conductive armour (Faraday cage: failsafe trips).
- led.visible             some power indicator (part kind `led`, else the receiver) visible from outside: judges and
                          pit crew need to see the robot is live (warning).
"""

from __future__ import annotations

import math

import numpy as np

from ..finding import BLOCKER, WARNING, fail, note, ok
from ._review import fastener_rotates, rotating, x
from .wire_review import _route_points, bundle_radius, enclosed, rotor_groups, swept_bands, band_dist
from .wiring import _from, default_awg, wire_od

G = "realworld"
SHELL = {"structure", "armor", "armour", "plate", "wedge", "lid", "cover", "tub", "fork"}
SOLDERED = {"esc", "motor", "weapon_motor", "battery", "switch", "receiver", "servo", "led"}
CONDUCTIVE = ("alu", "titan", "steel", "carbon", "cf", "copper", "brass", "metal")
LOCKS = {"nyloc", "threadlock", "loctite", "thread_forming", "locknut", "safety_wire", "lockwasher", "self_tap"}
TOL_MM = 0.3
PORT_FREE_MM = 4.0
STRAIN_MM = 15.0
BATTERY_GAP_MM = 2.0
BATTERY_ROTOR_MM = 3.0
HEAT_GAP_MM = 0.5
# continuous A for short silicone runs (fine-strand, ~105 C rated); conservative chassis-wiring figures
AMPACITY = [(32, 0.8), (30, 1.5), (28, 2.5), (26, 4.0), (24, 6.0), (22, 9.0), (20, 13.0), (18, 18.0), (16, 25.0)]
# (substring, continuous A) of common ant connectors
CONNECTORS = [("xt60", 60.0), ("xt30", 15.0), ("ec2", 20.0), ("deans", 40.0), ("t-plug", 40.0), ("mr30", 15.0),
              ("jst-rcy", 3.0), ("rcy", 3.0), ("bec", 3.0), ("jst-xh", 3.0), ("ph2.0", 2.0), ("jst-ph", 2.0),
              ("jst-sh", 1.0), ("jst", 2.0), ("servo", 3.0), ("dupont", 3.0)]


def ampacity(awg: float) -> float:
    return min(AMPACITY, key=lambda t: abs(t[0] - awg))[1]


def connector_rating(name):
    n = str(name or "").lower().replace("_", "-")
    for k, a in CONNECTORS:
        if k in n:
            return a
    return None


def samples(pts, step=0.5):
    pts = np.asarray(pts, float)
    out = []
    for a, b in zip(pts, pts[1:]):
        n = max(int(np.linalg.norm(b - a) / step), 1)
        out += [a + (b - a) * t for t in np.linspace(0, 1, n, endpoint=False)]
    out.append(pts[-1])
    return np.asarray(out)


def tube(Q, rad, k=8):
    """Points on the wire's outer surface: k around each centreline sample."""
    T = np.gradient(Q, axis=0) if len(Q) > 1 else np.array([[0.0, 0.0, 1.0]])
    T /= np.maximum(np.linalg.norm(T, axis=1), 1e-9)[:, None]
    ref = np.where(np.abs(T[:, 2:3]) < 0.9, [[0.0, 0.0, 1.0]], [[1.0, 0.0, 0.0]])
    U = np.cross(T, ref)
    U /= np.maximum(np.linalg.norm(U, axis=1), 1e-9)[:, None]
    V = np.cross(T, U)
    ang = np.linspace(0, 2 * math.pi, k, endpoint=False)
    S = Q[:, None, :] + rad * (np.cos(ang)[None, :, None] * U[:, None, :] + np.sin(ang)[None, :, None] * V[:, None, :])
    return S.reshape(-1, 3), np.repeat(np.arange(len(Q)), k)


def shell_hull(ctx):
    import trimesh

    kind = {p.id: p.kind for p in ctx.r.spec.parts}
    V = [np.asarray(b.mesh.vertices) for b in ctx.world.bodies
         if not b.is_wire and b.mesh is not None and len(b.mesh.faces) and kind.get(b.id) in SHELL]
    if not V:
        return None
    return trimesh.Trimesh(vertices=np.vstack(V), process=False).convex_hull


def hull_out(hull, P, tol=TOL_MM):
    """Signed: > tol outside the convex hull (plane distances, exact for a convex mesh)."""
    n = hull.face_normals
    o = hull.triangles[:, 0, :]
    d = np.einsum("pfk,fk->pf", P[:, None, :] - o[None], n)
    return d.max(1) > tol, d.max(1)


def _body_out(ctx, hull, pid):
    b = ctx.world.body(pid)
    if b is None or b.mesh is None or not len(b.mesh.vertices):
        return False
    return bool(hull_out(hull, np.asarray(b.mesh.vertices))[0].any())


def wire_outside(ctx):
    r = ctx.r
    if not r.spec.wires:
        return []
    hull = shell_hull(ctx)
    if hull is None:
        ctx.not_checked.append("wire.outside: no armour/chassis parts")
        return []
    floor = min((b.aabb[0][2] for b in ctx.world.bodies if not b.is_wire), default=-math.inf)
    out, n = [], 0
    for wr in r.spec.wires:
        if x(wr, "external", False) and str(x(wr, "exposed_reason", "") or "").strip():
            continue
        pts, _ = _route_points(ctx, wr)
        if pts is None or len(pts) < 2:
            continue
        n += 1
        Q = samples(pts)
        rad = bundle_radius(wr)
        S, idx = tube(Q, rad)
        bad, depth = hull_out(hull, S)
        bad |= S[:, 2] < floor - 0.05
        # next to a port on a part that itself pokes out (exposed weapon motor), the lead has to be outside
        L = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))])
        for end, li in ((_from(wr), L[idx]), (wr.to, L[-1] - L[idx])):
            pid = str(end).split(".")[0]
            if _body_out(ctx, hull, pid):
                bad &= ~(li <= PORT_FREE_MM)
        if bad.any():
            k = int(np.argmax(np.where(bad, depth, -np.inf)))
            span = len(np.unique(idx[bad])) * 0.5
            why = "" if not x(wr, "external", False) else " It is `external: true` but gives no `exposed_reason`."
            out.append(fail("wire.outside", G, BLOCKER, "Part of a wire is outside the robot",
                            f"wire `{wr.id}` ({rad * 2:.1f} mm bundle): about {span:.1f} mm of its run has insulation "
                            f"outside the armour envelope or below the floor, worst {max(depth[k], 0):.1f} mm out at "
                            f"{np.round(S[k], 1).tolist()}.{why}")
                       .on(wr.id).here(S[k]).expect(f"<= {TOL_MM:g} mm out", f"{max(depth[k], 0):.1f} mm")
                       .fix("Add / move `via` points inside the chassis (or open a channel), or declare "
                            "`external: true` + `exposed_reason` for a deliberate outside lead."))
    if n and not out:
        out.append(ok("wire.outside", G, "Every wire stays inside the robot",
                      f"{n} wire tubes (with insulation radius) stay inside the armour envelope and above the floor."))
    return out


def _group(spec, pid):
    for grp, _piv, _ax, ids in rotor_groups(spec):
        if pid in ids:
            return grp
    p = spec.part(pid)
    rw = getattr(p, "rotates_with", None) if p is not None else None
    return rw if rw not in (None, "fixed") else None


def spans_rotation(ctx):
    spec = ctx.r.spec
    out = []
    for wr in spec.wires:
        a, b = (str(e).split(".")[0] for e in (_from(wr), wr.to))
        ga, gb = _group(spec, a), _group(spec, b)
        if ga != gb and not x(wr, "slip_ring", False):
            out.append(fail("wire.spans_rotation", G, BLOCKER, "Wire joins a spinning part to a static one",
                            f"wire `{wr.id}` runs `{a}` ({ga or 'static'}) to `{b}` ({gb or 'static'}); it winds up and "
                            "tears off on the first turn.").on(wr.id, a, b)
                       .fix("End the wire on the static side (outrunner phases come off the stator), or declare "
                            "`slip_ring: true`."))
    return out


BURST = 3.0


def kind_of(ctx, pid):
    p = ctx.r.spec.part(pid)
    return p.kind if p is not None else None


def gauge_current(ctx):
    r = ctx.r
    out = []
    peak = ctx.metrics.get("peak_current_a")
    cat = {rp.part.id: rp.cat for rp in r.parts}
    for wr in r.spec.wires:
        awg = float(wr.awg) if wr.awg is not None else default_awg(wr.kind)
        amp = None
        ends = [str(e).split(".")[0] for e in (_from(wr), wr.to)]
        if x(wr, "current_a") is not None:
            amp = float(x(wr, "current_a"))
        elif wr.kind == "motor":
            for e in ends:
                c = cat.get(e)
                if c is not None:
                    amp = c.props.get("max_current_a") or c.props.get("stall_current_a") or amp
        elif wr.kind == "power":
            low = any(k in ("receiver", "servo", "led") for k in (kind_of(ctx, e) for e in ends))
            amp = None if low else peak
        if amp is None:
            if wr.kind in ("power", "motor"):
                ctx.not_checked.append(f"wire.gauge_current `{wr.id}`: current unknown (set `current_a`)")
            continue
        cap = ampacity(awg) * BURST   # fight current comes in bursts on short runs
        if amp > cap:
            sev = BLOCKER if amp > 1.5 * cap else WARNING
            out.append(fail("wire.gauge_current", G, sev, "Wire too thin for its current",
                            f"wire `{wr.id}` is {awg:g} AWG (about {cap:g} A burst) but carries {amp:.1f} A.")
                       .on(wr.id).expect(f"<= {cap:g} A", f"{amp:.1f} A")
                       .fix(f"Use {next((a for a, c in sorted(AMPACITY, key=lambda t: -t[0]) if c >= amp), 16)} AWG or thicker."))
    return out


def strain_relief(ctx):
    r, w = ctx.r, ctx.world
    kind = {p.id: p.kind for p in r.spec.parts}
    out = []
    spinning = {i for *_, ids in rotor_groups(r.spec, w) for i in ids}
    for wr in r.spec.wires:
        if str(x(wr, "strain_relief", "") or "").strip():
            continue
        pts, _ = _route_points(ctx, wr)
        if pts is None or len(pts) < 2:
            continue
        Q = samples(pts)
        L = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))])
        rad = bundle_radius(wr)
        for end, near in ((_from(wr), L <= STRAIN_MM), (wr.to, L >= L[-1] - STRAIN_MM)):
            pid = str(end).split(".")[0]
            if kind.get(pid) not in SOLDERED:
                continue
            seg = Q[near & (np.minimum(L, L[-1] - L) > 2.0 * rad + 1.0)]   # past the joint itself
            if not len(seg):
                continue
            cloud = [np.vstack([b.mesh.vertices, b.mesh.sample(3000, seed=0)]) for b in w.bodies
                     if not b.is_wire and b.mesh is not None and len(b.mesh.faces) and b.id not in spinning
                     and np.all(np.asarray(b.aabb[0]) <= seg.max(0) + 3) and np.all(np.asarray(b.aabb[1]) >= seg.min(0) - 3)]
            held = enclosed(seg, np.zeros(len(seg), bool), np.vstack(cloud) if cloud else np.zeros((0, 3)), rad + 1.5)
            if not held.any():
                out.append(fail("wire.strain_relief", G, WARNING, "Solder joint has no strain relief",
                                f"wire `{wr.id}` leaves `{pid}` with nothing holding it (hole, channel, clip) within "
                                f"{STRAIN_MM:g} mm; impacts flex the joint until it cracks.").on(wr.id, pid).here(seg[0])
                           .fix("Route it through a slot / clip near the part, or declare `strain_relief: "
                                "\"hot glue|heatshrink|zip tie\"`."))
    return out


def connector_rating_check(ctx):
    r = ctx.r
    peak = ctx.metrics.get("peak_current_a")
    names = []
    for rp in r.parts:
        c = rp.part._extra.get("connector") or (rp.cat.props.get("connector") if rp.cat is not None else None)
        if c and (rp.part.kind in ("battery", "connector", "switch") or "connector" in rp.part._extra):
            names.append((rp.part.id, c))
    for wr in r.spec.wires:
        if x(wr, "connector"):
            names.append((wr.id, x(wr, "connector")))
    if not names:
        if any(rp.part.kind == "battery" for rp in r.parts):
            ctx.not_checked.append("connector.rating: battery connector not declared (`connector: \"XT30\"`)")
        return []
    out = []
    for who, c in names:
        a = connector_rating(c)
        if a is None:
            ctx.not_checked.append(f"connector.rating `{who}`: unknown connector {c!r}")
            continue
        a *= BURST
        if peak is not None and peak > a:
            out.append(fail("connector.rating", G, BLOCKER if peak > 1.5 * a else WARNING, "Connector under-rated",
                            f"`{who}` uses {c} (about {a:g} A burst) but the robot peaks at {peak:.1f} A.")
                       .on(who).expect(f"<= {a:g} A", f"{peak:.1f} A").fix("Use an XT30 (15 A) or bigger on the power path."))
    return out


def fastener_lock(ctx):
    spec = ctx.r.spec
    kinds = {p.id: p.kind for p in spec.parts}
    mats = {p.id: str(p.material or "").lower() for p in spec.parts}
    groups = [g for g, *_ in rotor_groups(spec)]
    out = []
    for f in spec.fasteners:
        lock = str(x(f, "lock", "") or "").lower()
        if any(k in lock for k in LOCKS):
            continue
        into = f.threads_into or ""
        metal = into == "" or "nut" in str(into).lower() or any(m in mats.get(into, "") for m in ("steel", "alu", "titan", "brass"))
        if not metal:
            continue    # thread in plastic / heat-set grips by itself (fastener.engagement judges it)
        spin = any(fastener_rotates(spec, f, g) for g in groups)
        motor = any(kinds.get(p) in ("motor", "weapon_motor") for p in list(f.through) + [into])
        if spin or motor:
            out.append(fail("fastener.lock", G, WARNING, "Screw can vibrate loose",
                            f"`{f.id}` ({f.designation}) threads metal-to-metal on a {'spinning' if spin else 'motor'} joint "
                            "with no locking declared; ant weapons shake these out within a fight.").on(f.id)
                       .fix("Declare `lock: nyloc | threadlock | locknut` (and model the nyloc height)."))
    return out


def _min_gap(A, B):
    from scipy.spatial import cKDTree

    return float(cKDTree(B).query(A)[0].min())


def battery_checks(ctx):
    r, w = ctx.r, ctx.world
    out = []
    hull = shell_hull(ctx)
    bands = []
    for grp, piv, ax, ids in rotor_groups(r.spec, w):
        bs = [b for b in (w.body(i) for i in ids) if b is not None and b.mesh is not None and len(b.mesh.faces)]
        if bs:
            bands.append((grp, piv, ax, swept_bands(bs, piv, ax)))
    for p in r.spec.parts:
        if p.kind != "battery" or p._extra.get("exposed"):
            continue
        b = w.body(p.id)
        if b is None or b.mesh is None or not len(b.mesh.vertices):
            continue
        P = np.asarray(b.mesh.vertices)
        if hull is not None:
            gap = float(-hull_out(hull, P, 0.0)[1].max())
            if gap < BATTERY_GAP_MM:
                out.append(fail("battery.armour_gap", G, BLOCKER if gap < 1.0 else WARNING, "LiPo too close to the outside",
                                (f"`{p.id}` sits {gap:.1f} mm inside the armour envelope; a hit dents the wall into the cell." if gap >= 0 else
                                 f"`{p.id}` pokes {-gap:.1f} mm outside the armour envelope; nothing protects it there."))
                           .on(p.id).expect(f">= {BATTERY_GAP_MM:g} mm", f"{gap:.1f} mm")
                           .fix("Move it inward, add foam / a thicker wall in front of it."))
        for grp, piv, ax, bd in bands:
            g = float((band_dist(P, piv, ax, bd)).min())
            if g < BATTERY_ROTOR_MM:
                out.append(fail("battery.rotor_gap", G, BLOCKER, "LiPo next to a spinning part",
                                f"`{p.id}` is {g:.1f} mm from the volume swept by `{grp}`.").on(p.id, grp)
                           .expect(f">= {BATTERY_ROTOR_MM:g} mm", f"{g:.1f} mm").fix("Move the battery or add a wall."))
    return out


def heat_neighbour(ctx):
    r, w = ctx.r, ctx.world
    kind = {p.id: p.kind for p in r.spec.parts}
    hot = [b for b in w.bodies if kind.get(b.id) in ("motor", "weapon_motor") and b.mesh is not None and len(b.mesh.vertices)]
    out = []
    for b in w.bodies:
        if kind.get(b.id) not in ("battery", "esc", "receiver") or b.mesh is None or not len(b.mesh.vertices):
            continue
        for m in hot:
            if np.any(b.aabb[0] > m.aabb[1] + 2) or np.any(m.aabb[0] > b.aabb[1] + 2):
                continue
            g = _min_gap(np.asarray(b.mesh.vertices), np.vstack([m.mesh.vertices, m.mesh.sample(2000, seed=0)]))
            if g < HEAT_GAP_MM:
                out.append(fail("heat.neighbour", G, WARNING, "Electronics touch a motor",
                                f"`{b.id}` is {g:.1f} mm from motor `{m.id}`; the can reaches 80+ C in a fight.")
                           .on(b.id, m.id).fix("Leave an air gap or a printed wall between them."))
    return out


def _escape(w, skip, P, conductive_only=None):
    """Fraction of rays (26 dirs) from P that leave the robot; with conductive_only, rays count as blocked only by those."""
    D = [np.array(v, float) - 1 for v in np.ndindex(3, 3, 3)]
    D = [d / np.linalg.norm(d) for d in D if np.any(d != 0)]
    bodies = [b for b in w.bodies if not b.is_wire and b.id not in skip and b.mesh is not None and len(b.mesh.faces)]
    if conductive_only is not None:
        bodies = [b for b in bodies if b.id in conductive_only]
    esc = 0
    for d in D:
        hit = any(b.mesh.ray.intersects_any(P[None] + d * 0.05, d[None])[0] for b in bodies)
        esc += not hit
    return esc / len(D)


def rf_antenna(ctx):
    r, w = ctx.r, ctx.world
    cond = {p.id for p in r.spec.parts if any(m in str(p.material or "").lower() for m in CONDUCTIVE)
            and p.kind not in ("motor", "weapon_motor", "battery", "esc")}
    out = []
    for p in r.spec.parts:
        if p.kind != "receiver":
            continue
        b = w.body(p.id)
        if b is None or b.mesh is None or not cond:
            continue
        if _escape(w, {p.id}, np.asarray(b.mesh.centroid), cond) == 0.0 and not p._extra.get("antenna_out"):
            out.append(fail("rf.antenna", G, BLOCKER, "Receiver boxed in by conductive armour",
                            f"`{p.id}`: every line out hits conductive armour ({', '.join(sorted(cond)[:4])}); the "
                            "signal drops and failsafe trips mid-fight.").on(p.id)
                       .fix("Leave a plastic window / route the antenna out (`antenna_out: true`)."))
    return out


def led_visible(ctx):
    r, w = ctx.r, ctx.world
    leds = [p for p in r.spec.parts if p.kind == "led"] or [p for p in r.spec.parts if p.kind == "receiver"]
    if not leds:
        return []
    for p in leds:
        b = w.body(p.id)
        if b is not None and b.mesh is not None and len(b.mesh.vertices):
            if _escape(w, {p.id}, np.asarray(b.mesh.centroid)) > 0.0:
                return [ok("led.visible", G, "Power light visible", f"`{p.id}` can be seen from outside.")]
    return [fail("led.visible", G, WARNING, "No power light visible",
                 f"{', '.join(p.id for p in leds)}: no straight line out; nobody can see the robot is live.")
            .on(*[p.id for p in leds]).fix("Add a `led` part behind a hole or clear window, or a slot over the receiver LED.")]


def run(ctx):
    out = []
    for fn in (wire_outside, spans_rotation, gauge_current, strain_relief, connector_rating_check, fastener_lock,
               battery_checks, heat_neighbour, rf_antenna, led_visible):
        try:
            out += fn(ctx)
        except Exception as e:  # noqa: BLE001  one sub-check crashing must not hide the others
            out.append(note(f"{G}.crashed", G, f"{fn.__name__} crashed", f"{type(e).__name__}: {e}"))
    return out

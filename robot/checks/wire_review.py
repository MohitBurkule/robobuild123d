"""Wiring against the current layout, without needing the slow router (group `wiring`):

- wire.rotating_clearance: every fastener and nut that turns with the weapon sweeps a ring about the spin axis; each
  wire run (port -> via -> port, as a bundle of `count` strands) and the weapon motor's phase-wire exit must keep at
  least `review.wire.rotating_clearance_mm` (default 1) from the swept band (see `swept_bands`).
- wire.render_present: every declared wire must appear in the latest renders. `render` writes a sidecar
  `<png>.json` (spec path, wire endpoints); renders in `renders.dir` (spec key, relative to the spec) with no sidecar,
  with no wires, older than the spec, or whose wire endpoints sit more than `endpoint_tol_mm` (3) from the port's
  current position (a part moved since) fail. With no `renders` key it only checks every wire end resolves.
- wire.render_wires (opt-out): every robot-level PNG (not part_* / section_*, sidecar shows >= half the parts) in
  `renders.dir` (default renders/) and `review_renders` dirs must have a sidecar listing every declared wire. A robot
  render made without routes (render_present only needed ONE render with wires) is a BLOCKER; `render_ok` exempts a file.
- wire.render_count: each render record lists exactly the spec's wires (count and ids).
- wire.rotor_clearance (opt-out): every routed wire keeps >= 2 mm from the revolved volume of every revolute group (the
  whole weapon rotor and each wheel+hub, not only rotating fasteners); `rotor_ok: reason` on a wire exempts it.
- wire.exterior_support (opt-out): a wire outside the chassis hull must run along a hole wall / channel / clip (a body
  within 1.5 mm); a free span over 8 mm is a BLOCKER unless the wire declares `exposed_reason`.
"""

from __future__ import annotations

import fnmatch
import json
import math
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok
from ._physics import weapons
from ._review import fastener_rotates, params, polyline_dist, rotating, x
from .wiring import _from, default_awg, wire_od

G = "wire_review"
DEFAULTS = {"rotating_clearance_mm": 1.0, "endpoint_tol_mm": 3.0}


def wire_path(world, r, w):
    a, b = world.port(r, _from(w)), world.port(r, w.to)
    if a is None or b is None:
        return None
    return np.array([a] + [list(v) for v in (w.via or [])] + [b], float)


def bundle_radius(w):
    awg = float(w.awg) if w.awg is not None else default_awg(w.kind)
    n = int(x(w, "count", 1) or 1)
    od = wire_od(awg)
    if n <= 3:   # leads run twisted together: circumscribed circle of 1 / 2 / 3 touching round leads
        return 0.5 * od * (1.0, 2.0, 1.0 + 2.0 / math.sqrt(3.0))[n - 1]
    return 0.5 * n * (od + 0.3)


def swept_bands(bodies, origin, axis, n=600):
    """One (t0, t1, rho0, rho1) per rotating body: the axial span and radial band it sweeps about the spin axis. A band
    is the solid of revolution of the body's (t, rho) extent, so the gap to it does not depend on how densely the body's
    surface was sampled (a point cloud of samples leaves gaps and reads a lead as clear between two vertices)."""
    out = []
    for b in bodies:
        q = np.vstack([b.mesh.vertices, b.mesh.sample(n)]) - origin
        t = q @ axis
        rho = np.linalg.norm(q - np.outer(t, axis), axis=1)
        out.append((float(t.min()), float(t.max()), float(rho.min()), float(rho.max())))
    return np.array(out)


def band_dist(Q, origin, axis, bands):
    """Distance from points Q to the nearest swept band (t0, t1, rho0, rho1), measured in the (t, rho) half plane."""
    q = np.atleast_2d(Q) - origin
    tq = q @ axis
    rq = np.linalg.norm(q - np.outer(tq, axis), axis=1)
    dt = np.maximum(np.maximum(bands[None, :, 0] - tq[:, None], tq[:, None] - bands[None, :, 1]), 0.0)
    dr = np.maximum(np.maximum(bands[None, :, 2] - rq[:, None], rq[:, None] - bands[None, :, 3]), 0.0)
    return np.sqrt(dt ** 2 + dr ** 2).min(axis=1)


def _samples(path, step=0.5):
    out = []
    for a, b in zip(path[:-1], path[1:]):
        k = max(2, int(math.ceil(np.linalg.norm(b - a) / step)) + 1)
        out.append(a + np.linspace(0, 1, k)[:, None] * (b - a))
    return np.vstack(out)


def rotating_clearance(ctx):
    r, w = ctx.r, ctx.world
    spec = r.spec
    par = params(spec, "wire", DEFAULTS)
    need = float(par["rotating_clearance_mm"])
    wp = weapons(ctx)
    if not wp:
        return []
    _, _, origin, axis = wp[0]
    ids = [f.id for f in spec.fasteners if fastener_rotates(spec, f)]
    ids += [p.id for p in spec.parts if p.kind == "nut" and rotating(spec, p.id)]
    bodies = [b for b in (w.body(i) for i in ids) if b is not None]
    if not bodies:
        return [ok("wire.rotating_clearance", G, "No rotating hardware", "No fastener or nut turns with the weapon.")]
    bands = swept_bands(bodies, origin, axis)
    out, worst = [], None
    targets = []
    for wr in spec.wires:
        path = wire_path(w, r, wr)
        if path is not None:
            targets.append((f"wire `{wr.id}`", _samples(path), bundle_radius(wr), wr.id))
    for rp in r.parts:
        if rp.part.kind == "weapon_motor":
            ph = w.port(r, f"{rp.part.id}.phases")
            if ph is not None:
                targets.append((f"phase-wire exit of `{rp.part.id}`", np.atleast_2d(ph), 0.0, rp.part.id))
    for name, Q, rad, pid in targets:
        d = band_dist(Q, origin, axis, bands) - rad
        k = int(np.argmin(d))
        gap = float(d[k])
        worst = gap if worst is None else min(worst, gap)
        if gap < need:
            out.append(fail("wire.rotating_clearance", G, BLOCKER, "Wire too close to rotating hardware",
                            f"{name} passes {gap:.1f} mm from the band swept by the weapon's own fasteners/nuts "
                            f"({', '.join(ids[:4])}{'...' if len(ids) > 4 else ''}); a nut that grazes a lead cuts it.")
                       .on(pid, *ids[:4]).here(Q[k]).expect(f">= {need:.1f} mm", f"{gap:.1f} mm")
                       .fix("Reroute the run (via points) away from the weapon, or remove / recess the rotating hardware."))
    if not out and targets:
        out.append(ok("wire.rotating_clearance", G, "Wires clear the rotating hardware",
                      f"{len(targets)} wire runs/exits keep >= {need:.1f} mm (closest {worst:.1f} mm)."))
    ctx.metrics["wire_rotating_clearance_mm"] = worst
    return out


def render_present(ctx):
    r, w = ctx.r, ctx.world
    spec = r.spec
    if not spec.wires:
        return []
    par = params(spec, "wire", DEFAULTS)
    tol = float(par["endpoint_tol_mm"])
    out = []
    ends = {}
    for wr in spec.wires:
        a, b = w.port(r, _from(wr)), w.port(r, wr.to)
        if a is None or b is None:
            out.append(fail("wire.render_present", G, BLOCKER, "Wire end does not resolve",
                            f"Wire `{wr.id}` runs `{_from(wr)}` to `{wr.to}`; one end is not a port of the current parts.").on(wr.id))
            continue
        ends[wr.id] = (np.asarray(a, float), np.asarray(b, float))
    cfg = (spec.raw or {}).get("renders")
    if not cfg:
        ctx.not_checked.append("wire.render_present: no `renders` dir declared, rendered wiring not checked")
        return out
    d = Path(cfg.get("dir", "."))
    d = d if d.is_absolute() else Path(spec.base_dir) / d
    pngs = sorted(p for p in d.glob("*.png") if any(fnmatch.fnmatchcase(p.name, g) for g in cfg.get("views", ["*.png"])))
    spec_path = Path(spec.base_dir) / cfg.get("spec", "spec.json")
    t_spec = spec_path.stat().st_mtime if spec_path.is_file() else 0.0
    with_wires, stale, moved, bare = [], [], [], []
    for p in pngs:
        side = p.with_suffix(p.suffix + ".json")
        if not side.is_file():
            bare.append(p.name)
            continue
        try:
            man = json.loads(side.read_text())
        except Exception:  # noqa: BLE001
            bare.append(p.name)
            continue
        wires = man.get("wires") or {}
        if not wires:
            continue
        with_wires.append(p.name)
        if p.stat().st_mtime < t_spec:
            stale.append(p.name)
        for wid, (a, b) in ends.items():
            got = wires.get(wid)
            if got is None:
                moved.append(f"{p.name}: `{wid}` not drawn")
                continue
            for name, want, have in (("from", a, got.get("from")), ("to", b, got.get("to"))):
                if have is not None and np.linalg.norm(want - np.asarray(have, float)) > tol:
                    moved.append(f"{p.name}: `{wid}` {name} end drawn at {np.round(have, 1).tolist()}, port now at "
                                 f"{np.round(want, 1).tolist()}")
    if not with_wires:
        out.append(fail("wire.render_present", G, BLOCKER, "No render shows the wiring",
                        f"{len(spec.wires)} wire runs are declared, but none of the {len(pngs)} renders in `{d}` draws a wire "
                        f"({len(bare)} have no render record, so nothing says what they show).")
                   .fix("Render with checks on (not --no-checks / --quick) so wire routes are drawn, e.g. "
                        "`python3 -m robot render spec.json top wiring_top.png --no-lid`."))
    if stale:
        out.append(fail("wire.render_present", G, WARNING, "Wiring render is older than the spec",
                        f"{', '.join(stale)} predate the spec; the layout may have moved since.").fix("Re-render the wiring views."))
    if moved:
        out.append(fail("wire.render_present", G, BLOCKER, "Rendered wire ends are off their terminals",
                        "; ".join(moved[:6]) + ("..." if len(moved) > 6 else "")).fix("Re-render the wiring views."))
    if not out:
        out.append(ok("wire.render_present", G, "Wiring rendered", f"{len(with_wires)} render(s) draw all {len(ends)} wires on their current terminals."))
    return out


PART_VIEW = ("part_", "section_", "compare_")  # single-part and section renders do not show the wiring by design


def render_dirs(spec):
    """Directories holding robot renders: `renders.dir` (default `renders/` next to the spec) and `review_renders`."""
    base = Path(spec.base_dir)
    raw = spec.raw or {}
    ds = [(raw.get("renders") or {}).get("dir", "renders")] + list(raw.get("review_renders") or [])
    out = []
    for d in ds:
        p = Path(d) if Path(d).is_absolute() else base / d
        if p.is_dir() and p not in out:
            out.append(p)
    return out


def robot_render_wires(png: Path, wire_ids, n_parts):
    """None when `png` is not a robot-level render, else the list of problems (empty = every wire drawn)."""
    side = png.with_suffix(png.suffix + ".json")
    if png.name.startswith(PART_VIEW):
        return None
    if not side.is_file():
        return ["no render record (`<png>.json`), so nothing says the wires were drawn"]
    try:
        man = json.loads(side.read_text())
    except Exception:  # noqa: BLE001
        return ["render record unreadable"]
    bodies = man.get("bodies") or []
    if n_parts and len(bodies) < 0.5 * n_parts:
        return None  # a close-up of a few parts
    drawn = man.get("wires") or {}
    miss = [w for w in wire_ids if w not in drawn]
    if len(miss) == len(wire_ids):
        return ["rendered without wires (checks off or no routes)"]
    return [f"wire `{w}` not drawn" for w in miss]


def render_wires(ctx):
    """wire.render_wires (opt-out): every robot-level render in the render dirs draws every declared wire route.
    Exempt one file with spec `render_ok: [{"file": "<name>.png", "reason": "..."}]`."""
    spec = ctx.r.spec
    if not spec.wires:
        return []
    ids = [w.id for w in spec.wires]
    okd = {e.get("file"): e.get("reason") for e in (spec.raw or {}).get("render_ok") or [] if str(e.get("reason") or "").strip()}
    bad, n = [], 0
    for d in render_dirs(spec):
        for png in sorted(d.glob("*.png")):
            probs = robot_render_wires(png, ids, len(spec.parts))
            if probs is None:
                continue
            n += 1
            if probs and png.name not in okd:
                bad.append(f"{d.name}/{png.name}: {probs[0]}" + (f" (+{len(probs) - 1})" if len(probs) > 1 else ""))
    if bad:
        return [fail("wire.render_wires", G, BLOCKER, "Robot render made without the wire routes",
                     f"{len(bad)} of {n} robot render(s) do not draw all {len(ids)} wires: " + "; ".join(bad[:8]) + ("..." if len(bad) > 8 else ""))
                .fix("Re-render with checks on so routes are drawn (`python3 -m robot render spec.json iso out.png`), or "
                     "exempt the file in `render_ok` with a reason.")]
    if n:
        return [ok("wire.render_wires", G, "Every robot render shows the wiring", f"{n} robot render(s) draw all {len(ids)} wires.")]
    ctx.not_checked.append("wire.render_wires: no robot renders found in the render dirs")
    return []


# ------------------------------------------------------------------------------------------------ rotor clearance
ROTOR_MIN_MM = 2.0      # wire.rotor_clearance: route to the revolved envelope of every revolute group
SUPPORT_MM = 1.5        # wire.exterior_support: a wire point outside the chassis is held when a body is this close
UNSUPPORTED_MAX_MM = 8.0  # longest run outside the chassis with nothing (hole wall, channel, clip) within SUPPORT_MM


def rotor_groups(spec, world=None):
    """[(group, pivot, unit axis, [part ids])] for every revolute joint: the weapon and each wheel. The group is the
    jointed part's `rotates_with` (else its id); members are every part that rotates with it."""
    out = []
    for p in spec.parts:
        j = getattr(p, "joint", None) or (getattr(p, "_extra", None) or {}).get("joint")
        if not j:
            continue
        j = j if isinstance(j, dict) else getattr(j, "__dict__", {})
        if j.get("kind") != "revolute" or j.get("axis") is None or j.get("pivot") is None:
            continue
        grp = p.rotates_with if p.rotates_with not in (None, "fixed") else p.id
        if any(g == grp for g, *_ in out):
            continue
        ids = [q.id for q in spec.parts if q.id == p.id or rotating(spec, q.id, grp)]
        ids += [f.id for f in spec.fasteners if fastener_rotates(spec, f, grp)]
        a, piv = np.asarray(j["axis"], float), np.asarray(j["pivot"], float)
        pb = world.body(p.parent) if world is not None and p.parent else None
        if pb is not None:   # a joint's pivot and axis are in its parent's frame
            a, piv = pb.M[:3, :3] @ a, pb.M[:3, :3] @ piv + pb.M[:3, 3]
        out.append((grp, piv, a / np.linalg.norm(a), ids))
    return out


def rotor_gaps(Q, rad, origin, axis, bands):
    """Clearance of a wire (sample points Q, bundle radius rad) to the swept bands: (gap, index of the worst point)."""
    d = band_dist(Q, origin, axis, bands) - rad
    k = int(np.argmin(d))
    return float(d[k]), k


def _route_points(ctx, wr):
    rt = next((x for x in (getattr(ctx, "routes", None) or []) if x.id == wr.id), None)
    if rt is not None and len(rt.points) >= 2:
        return np.asarray(rt.points, float), True
    path = wire_path(ctx.world, ctx.r, wr)
    return path, False


def rotor_clearance(ctx):
    """wire.rotor_clearance (opt-out): every wire keeps ROTOR_MIN_MM from the revolved volume of every revolute group
    (the whole rotor, not only its fasteners). Exempt a wire with `rotor_ok: "reason"`."""
    r, w = ctx.r, ctx.world
    spec = r.spec
    if not spec.wires:
        return []
    groups = []
    for grp, piv, ax, ids in rotor_groups(spec, w):
        bodies = [b for b in (w.body(i) for i in ids) if b is not None and b.mesh is not None and len(b.mesh.faces)]
        if bodies:
            groups.append((grp, piv, ax, ids, swept_bands(bodies, piv, ax)))
    out, worst, routed = [], None, 0
    for wr in spec.wires:
        pts, real = _route_points(ctx, wr)
        if pts is None:
            continue
        routed += real
        Q = _samples(pts)
        rad = bundle_radius(wr)
        for grp, piv, ax, ids, bands in groups:
            gap, k = rotor_gaps(Q, rad, piv, ax, bands)
            worst = gap if worst is None else min(worst, gap)
            if gap < ROTOR_MIN_MM and not str(x(wr, "rotor_ok", "") or "").strip():
                out.append(fail("wire.rotor_clearance", G, BLOCKER, "Wire runs too close to a spinning part",
                                f"wire `{wr.id}` passes {gap:.1f} mm from the volume swept by the `{grp}` rotor "
                                f"({', '.join(ids[:4])}{'...' if len(ids) > 4 else ''}) at {np.round(Q[k], 1).tolist()}.")
                           .on(wr.id, *ids[:2]).here(Q[k]).expect(f">= {ROTOR_MIN_MM:g} mm", f"{gap:.1f} mm")
                           .fix("Route the run away from the rotor (via points) or shield it; exempt with `rotor_ok`."))
    if not routed and spec.wires:
        ctx.not_checked.append("wire.rotor_clearance: routes not computed in this run (wiring group); used port + via polylines")
    if not out and groups:
        out.append(ok("wire.rotor_clearance", G, "Wires clear every rotor",
                      f"{len(spec.wires)} wires keep >= {ROTOR_MIN_MM:g} mm from {len(groups)} rotor(s) (closest {worst:.1f} mm)."))
    ctx.metrics["wire_rotor_clearance_mm"] = worst
    return out + exterior_support(ctx)


def chassis_hull(ctx):
    """Convex hull of the chassis (the largest-volume `structure` part), the wires' 'inside'."""
    best = None
    for p in ctx.r.spec.parts:
        if p.kind != "structure":
            continue
        b = ctx.world.body(p.id)
        if b is None or b.mesh is None or not len(b.mesh.faces):
            continue
        v = abs(float(b.mesh.volume))
        if best is None or v > best[0]:
            best = (v, b)
    return None if best is None else best[1].mesh.convex_hull


def unsupported_runs(Q, inside, near, step=0.5):
    """Longest runs (mm) of consecutive samples outside the chassis with no supporting body near: [(length, i0, i1)]."""
    out, i0 = [], None
    bad = (~inside) & (~near)
    for i, b in enumerate(list(bad) + [False]):
        if b and i0 is None:
            i0 = i
        elif not b and i0 is not None:
            out.append(((i - i0) * step, i0, i - 1))
            i0 = None
    return out


def exterior_support(ctx):
    """wire.exterior_support (opt-out): a wire outside the chassis hull must lie along a body (hole wall, channel, clip)
    within SUPPORT_MM; a free span over UNSUPPORTED_MAX_MM hangs loose. Exempt with `exposed_reason` on the wire."""
    from scipy.spatial import cKDTree

    r, w = ctx.r, ctx.world
    hull = chassis_hull(ctx)
    if hull is None or not r.spec.wires:
        return []
    out, n = [], 0
    for wr in r.spec.wires:
        pts, _ = _route_points(ctx, wr)
        if pts is None or str(x(wr, "exposed_reason", "") or "").strip():
            continue
        Q = _samples(pts)
        inside = hull.contains(Q)
        if inside.all():
            continue
        n += 1
        out_pts = Q[~inside]
        near = np.zeros(len(Q), bool)
        rad = bundle_radius(wr)
        for b in w.bodies:
            if b.is_wire or b.mesh is None or not len(b.mesh.faces):
                continue
            lo, hi = b.aabb
            k = np.all((Q >= np.asarray(lo) - SUPPORT_MM - rad) & (Q <= np.asarray(hi) + SUPPORT_MM + rad), axis=1) & ~inside
            if not k.any():
                continue
            pts_b = np.vstack([b.mesh.vertices, b.mesh.sample(3000)])
            d, _ = cKDTree(pts_b).query(Q[k])
            near[np.nonzero(k)[0]] |= d - rad <= SUPPORT_MM
        runs = [x_ for x_ in unsupported_runs(Q, inside, near) if x_[0] > UNSUPPORTED_MAX_MM]
        if runs:
            L, i0, i1 = max(runs)
            out.append(fail("wire.exterior_support", G, BLOCKER, "Wire hangs loose outside the chassis",
                            f"wire `{wr.id}` runs {L:.1f} mm outside the chassis with nothing within {SUPPORT_MM:g} mm to hold it "
                            f"(from {np.round(Q[i0], 1).tolist()} to {np.round(Q[i1], 1).tolist()}).")
                       .on(wr.id).here(Q[(i0 + i1) // 2])
                       .fix("Run it through a hole or channel, or clip it; declare `exposed_reason` if it must be free."))
    if n and not out:
        out.append(ok("wire.exterior_support", G, "Wires outside the chassis are held", f"{n} wire(s) leave the chassis; every run is along a hole, channel or clip."))
    return out


def render_count(ctx):
    """wire.render_count: every robot render record lists exactly the spec's wires (no stale or missing routes)."""
    spec = ctx.r.spec
    ids = {w.id for w in spec.wires or []}
    bad, n = [], 0
    for d in render_dirs(spec):
        for png in sorted(d.glob("*.png")):
            side = png.with_suffix(png.suffix + ".json")
            if png.name.startswith(PART_VIEW) or not side.is_file():
                continue
            try:
                drawn = set((json.loads(side.read_text()).get("wires") or {}).keys())
            except Exception:  # noqa: BLE001
                continue
            if not drawn:
                continue
            n += 1
            if drawn != ids:
                bad.append(f"{png.name}: {len(drawn)} routes vs {len(ids)} spec wires"
                           + (f" (extra {sorted(drawn - ids)[:3]})" if drawn - ids else "") + (f" (missing {sorted(ids - drawn)[:3]})" if ids - drawn else ""))
    if bad:
        return [fail("wire.render_count", G, BLOCKER, "Render shows a different set of wires than the spec", "; ".join(bad[:6]))
                .fix("Re-render: the render record must list exactly the spec's wires.")]
    return [ok("wire.render_count", G, "Render wire count matches", f"{n} render record(s) list all {len(ids)} spec wires.")] if n else []


def run(ctx):
    return rotating_clearance(ctx) + render_present(ctx) + render_wires(ctx) + rotor_clearance(ctx) + render_count(ctx)

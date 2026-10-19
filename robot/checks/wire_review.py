"""Wiring against the current layout, without needing the slow router (group `wiring`):

- wire.rotating_clearance: every fastener and nut that turns with the weapon sweeps a ring about the spin axis; each
  wire run (port -> via -> port, as a bundle of `count` strands) and the weapon motor's phase-wire exit must keep at
  least `review.wire.rotating_clearance_mm` (default 3) from that swept ring.
- wire.render_present: every declared wire must appear in the latest renders. `render` writes a sidecar
  `<png>.json` (spec path, wire endpoints); renders in `renders.dir` (spec key, relative to the spec) with no sidecar,
  with no wires, older than the spec, or whose wire endpoints sit more than `endpoint_tol_mm` (3) from the port's
  current position (a part moved since) fail. With no `renders` key it only checks every wire end resolves.
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
DEFAULTS = {"rotating_clearance_mm": 3.0, "endpoint_tol_mm": 3.0}


def wire_path(world, r, w):
    a, b = world.port(r, _from(w)), world.port(r, w.to)
    if a is None or b is None:
        return None
    return np.array([a] + [list(v) for v in (w.via or [])] + [b], float)


def bundle_radius(w):
    awg = float(w.awg) if w.awg is not None else default_awg(w.kind)
    n = int(x(w, "count", 1) or 1)
    return 0.5 * (n * (wire_od(awg) + 0.3) if n > 1 else wire_od(awg))


def swept_rings(bodies, origin, axis, n=600):
    """(t, rho) of surface samples of rotating bodies about the spin axis: each sweeps a circle."""
    P = np.vstack([np.vstack([b.mesh.vertices, b.mesh.sample(n)]) for b in bodies])
    q = P - origin
    t = q @ axis
    rho = np.linalg.norm(q - np.outer(t, axis), axis=1)
    return t, rho


def ring_dist(Q, origin, axis, t, rho):
    """Distance from points Q to the nearest swept circle (t, rho)."""
    q = np.atleast_2d(Q) - origin
    tq = q @ axis
    rq = np.linalg.norm(q - np.outer(tq, axis), axis=1)
    d = np.sqrt((tq[:, None] - t[None]) ** 2 + (rq[:, None] - rho[None]) ** 2)
    return d.min(axis=1)


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
    t, rho = swept_rings(bodies, origin, axis)
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
        d = ring_dist(Q, origin, axis, t, rho) - rad
        k = int(np.argmin(d))
        gap = float(d[k])
        worst = gap if worst is None else min(worst, gap)
        if gap < need:
            out.append(fail("wire.rotating_clearance", G, BLOCKER, "Wire too close to rotating hardware",
                            f"{name} passes {gap:.1f} mm from the circle swept by the weapon's own fasteners/nuts "
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


def run(ctx):
    return rotating_clearance(ctx) + render_present(ctx)

"""Snug fit: a component sitting in a pocket, bay or between internal walls must have a clearance per side inside the
fit band of the wall's process (printed 0.1-0.5 mm per side by default). Gaps are measured by rays from all six faces."""

from __future__ import annotations

import numpy as np

from .. import catalog, measure
from ..finding import BLOCKER, WARNING, fail, ok

G = "fit"
COMPONENT_KINDS = {"battery", "esc", "receiver", "motor", "weapon_motor", "servo", "switch", "bearing"}
NOT_WALL = COMPONENT_KINDS | {"wheel", "tyre", "weapon", "belt", "pulley", "insert", "nut", "shaft", "pin", "locking_bar"}
SEARCH_MM = 3.0  # a face with a wall nearer than this is "in a pocket" on that side
BANDS = {"printed": (0.1, 0.5), "other": (0.05, 0.3)}
AXES = ("x", "y", "z")


def band_for(r, wall_part, comp_part):
    f = comp_part._extra.get("fit")
    if isinstance(f, dict) and "min_mm" in f and "max_mm" in f:
        return float(f["min_mm"]), float(f["max_mm"]), "declared"
    printed = catalog.part_is_printed(wall_part.process, wall_part.material) if wall_part is not None else True
    lo, hi = BANDS["printed" if printed else "other"]
    return lo, hi, "printed" if printed else "machined"


def side_gaps(b, walls, n=5):
    """Per face (axis, sign): (min gap mm or inf, wall body id). Rays start 0.02 mm inside the face."""
    lo, hi = b.aabb
    sc = measure.Scene(walls)
    res = {}
    for ax in range(3):
        o = [i for i in range(3) if i != ax]
        g1 = np.linspace(lo[o[0]], hi[o[0]], n + 2)[1:-1]
        g2 = np.linspace(lo[o[1]], hi[o[1]], n + 2)[1:-1]
        for sgn in (-1, 1):
            P = []
            for a in g1:
                for c in g2:
                    p = np.zeros(3)
                    p[o[0]], p[o[1]] = a, c
                    p[ax] = (hi if sgn > 0 else lo)[ax] - sgn * 0.02
                    P.append(p)
            P = np.array(P)
            D = np.zeros_like(P)
            D[:, ax] = sgn
            dist, who = sc.first_hit(P, D, SEARCH_MM + 0.02)
            # rays that start inside the component hit its own face first: only walls are in the scene, so fine
            k = int(np.argmin(dist))
            res[(ax, sgn)] = (float(dist[k]) - 0.02, walls[who[k]].id if who[k] >= 0 else None)
    return res


def run(ctx):
    r, w = ctx.r, ctx.world
    out, checked = [], 0
    walls_all = [b for b in w.bodies if b.part_idx is not None and r.parts[b.part_idx].part.kind not in NOT_WALL]
    for b in w.bodies:
        if b.part_idx is None:
            continue
        p = r.parts[b.part_idx].part
        if p.kind not in COMPONENT_KINDS or p._extra.get("fit") == "none":
            continue
        grown = np.array([b.aabb[0] - SEARCH_MM, b.aabb[1] + SEARCH_MM])
        walls = [o for o in walls_all if o.id != p.id and o.id != p.parent and measure.aabb_overlap(o.aabb, grown)]
        if not walls:
            continue
        for o in walls:
            ov = measure.overlap(b, o)
            if ov is not None and getattr(ov, "depth", 0) > 0.05 and not _allowed(r, p.id, o.id):
                out.append(fail("fit.interference", G, BLOCKER, "Component does not fit its pocket",
                                f"`{p.id}` overlaps wall `{o.id}` by {ov.depth:.2f} mm: it will not go in.")
                           .on(p.id, o.id).here(b.center).fix("Grow the pocket to the component size plus the per-side fit clearance."))
        try:
            gaps = side_gaps(b, walls)
        except Exception as e:  # noqa: BLE001
            ctx.not_checked.append(f"fit: gaps round `{p.id}` not measured ({e})")
            continue
        walled = {k: v for k, v in gaps.items() if np.isfinite(v[0]) and v[0] <= SEARCH_MM}
        if len(walled) < 2:
            continue
        checked += 1
        ctx.metrics[f"fit.{p.id}.gaps"] = {f"{'-+'[s > 0]}{AXES[a]}": round(v[0], 3) for (a, s), v in walled.items()}
        for ax in range(3):
            pair = [walled.get((ax, -1)), walled.get((ax, 1))]
            if pair[0] is None or pair[1] is None:
                continue
            wp = r.spec.part(pair[0][1]) or r.spec.part(pair[1][1])
            lo, hi, src = band_for(r, wp, p)
            g0, g1 = max(pair[0][0], 0.0), max(pair[1][0], 0.0)
            tot = g0 + g1
            where = f"along {AXES[ax]}: {g0:.2f} mm to `{pair[0][1]}`, {g1:.2f} mm to `{pair[1][1]}`"
            if tot > 2 * hi + 1e-6:
                out.append(fail("fit.loose", G, WARNING, "Component rattles in its pocket",
                                f"`{p.id}` has {tot:.2f} mm total play {where}; the {src} fit band is {lo:g}-{hi:g} mm per side.")
                           .on(p.id, pair[0][1], pair[1][1]).here(b.center)
                           .fix("Close the pocket to the band, add a crush rib, or declare `retained` foam/tape with `fit: none`."))
            elif tot < 2 * lo - 1e-6:
                out.append(fail("fit.tight", G, WARNING, "Pocket too tight for the process",
                                f"`{p.id}` has only {tot:.2f} mm total clearance {where}; the {src} fit band needs at least {lo:g} mm per side.")
                           .on(p.id, pair[0][1], pair[1][1]).here(b.center)
                           .fix("Open the pocket so print tolerance cannot make it an interference fit."))
            decl = p._extra.get("clearance_mm")
            if decl is not None and abs(tot / 2 - float(decl)) > 0.1:
                out.append(fail("fit.declared_mismatch", G, WARNING, "Declared clearance differs from the model",
                                f"`{p.id}` declares {float(decl):.2f} mm per side but measures {tot / 2:.2f} mm {where}.").on(p.id))
    if checked and not any(not f.passed for f in out):
        out.append(ok("fit.snug", G, "Pocketed components fit snugly", f"{checked} components in pockets are within their fit bands on every walled axis."))
    return out


def _allowed(r, a, b):
    return any({x.a, x.b} == {a, b} for x in r.spec.allow_overlap)

"""cots.fidelity: a bought part must look like the real one. Each catalog motor in FEATURES lists the features that
identify it (outrunner: bell diameter, stator-base diameter, shaft diameter, the mount bolt circle on the stator face);
the modelled solid (part frame, motor axis = catalog shaft dir, default +X) must carry every one within TOL_MM.

A motor with no feature table is a warning: nobody can tell whether its model is right. Override or add per robot with
part `features: {...}` (same keys). Screw-head drive recesses are modelled by fastener_shape (world.py) and are not
judged here.
"""

from __future__ import annotations

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok
from ._review import x

G = "cots"
TOL_MM = 0.3
MOTOR_KINDS = ("motor", "weapon_motor")

# Catalog id -> identifying features (mm). Outrunners: bell_d, stator_d (base flange at the -axis end), shaft_d (the
# part of the shaft that leaves the bell at the +axis end), bolt_circle_d / bolt_n / bolt_d (tapped holes in the stator
# face). Gearmotors: can_d, shaft_d.
FEATURES = {
    "gr1507": {"bell_d": 19.6, "stator_d": 19.6, "shaft_d": 5.0, "bolt_circle_d": 12.0, "bolt_n": 4, "bolt_d": 2.0,
               "source": "GR1507 datasheet / RVRN 2.0 STEP GR1507_1 (19.6 x 19.6 x 30.5)"},
    "n10_2200rpm_spicy": {"can_d": 12.6, "shaft_d": 3.0, "source": "N10 micro-metal gearmotor, 3 mm D shaft"},
}


def _frame(rp):
    sh = rp.cat.shaft if rp.cat is not None else None
    ax = np.asarray((sh or {}).get("dir") or [1.0, 0.0, 0.0], float)
    return ax / np.linalg.norm(ax)


def profile(mesh, axis, n=4000):
    """Axial coordinate t and radius rho of surface samples (the motor's turned profile)."""
    pts = np.vstack([mesh.vertices, mesh.sample(n)])
    t = pts @ axis
    rho = np.linalg.norm(pts - np.outer(t, axis), axis=1)
    return pts, t, rho


def max_radius_near(t, rho, lo, hi):
    m = (t >= lo) & (t <= hi)
    return float(rho[m].max()) if m.any() else 0.0


def has_radius(t, rho, r, tol, bins=60):
    """True when some axial slice of the profile reaches radius r (within tol) as its maximum."""
    edges = np.linspace(t.min(), t.max(), bins + 1)
    best = None
    for a, b in zip(edges, edges[1:]):
        m = (t >= a) & (t <= b)
        if m.any():
            d = abs(float(rho[m].max()) - r)
            best = d if best is None else min(best, d)
    return best is not None and best <= tol, best


def bolt_holes(mesh, axis, face_t, inward, rc, n, depth=0.6):
    """How many of n points on the bolt circle, `depth` into the stator face, are open (a modelled hole)."""
    u = np.cross(axis, [0, 0, 1.0])
    if np.linalg.norm(u) < 1e-6:
        u = np.cross(axis, [0, 1.0, 0])
    u /= np.linalg.norm(u)
    v = np.cross(axis, u)
    best = 0
    for phase in np.linspace(0, 2 * np.pi / n, 12, endpoint=False):
        a = phase + 2 * np.pi * np.arange(n) / n
        P = (face_t + inward * depth) * axis + rc * (np.outer(np.cos(a), u) + np.outer(np.sin(a), v))
        try:
            inside = mesh.contains(P)
        except Exception:  # noqa: BLE001 - non-watertight: treat as solid
            inside = np.ones(len(P), bool)
        best = max(best, int((~inside).sum()))
    return best


def judge(rp, feat, tol=TOL_MM):
    """List of (feature, want, got) misses for one motor."""
    mesh = rp.geom.mesh
    axis = _frame(rp)
    _, t, rho = profile(mesh, axis)
    miss = []
    lo, hi = float(t.min()), float(t.max())
    if "bell_d" in feat:
        good, d = has_radius(t, rho, feat["bell_d"] / 2, tol)
        if not good:
            miss.append(("bell", f"d{feat['bell_d']}", f"no section within {tol} mm (closest off by {2 * (d or 0):.2f})"))
    if "can_d" in feat:
        good, d = has_radius(t, rho, feat["can_d"] / 2, tol)
        if not good:
            miss.append(("can", f"d{feat['can_d']}", f"closest section off by {2 * (d or 0):.2f}"))
    if "stator_d" in feat:
        got = 2 * max_radius_near(t, rho, lo, lo + 3.0)
        if abs(got - feat["stator_d"]) > 2 * tol:
            miss.append(("stator base", f"d{feat['stator_d']}", f"d{got:.2f} at the base face"))
    if "shaft_d" in feat:
        got = 2 * max_radius_near(t, rho, hi - 1.0, hi)
        if abs(got - feat["shaft_d"]) > 2 * tol:
            miss.append(("shaft", f"d{feat['shaft_d']}", f"d{got:.2f} at the shaft end"))
    if "bolt_circle_d" in feat:
        n = int(feat.get("bolt_n", 4))
        rc = feat["bolt_circle_d"] / 2
        wide = t[rho >= rc + feat.get("bolt_d", 2.0) / 2]
        face = float(wide.min()) if len(wide) else lo
        k = bolt_holes(mesh, axis, face, 1.0, rc, n)
        if k < n:
            miss.append(("mount bolt circle", f"{n} x M{feat.get('bolt_d', 2):g} on d{feat['bolt_circle_d']}", f"{k} holes open"))
    return miss


def run(ctx):
    out, n = [], 0
    for rp in ctx.r.parts:
        p = rp.part
        if p.kind not in MOTOR_KINDS:
            continue
        feat = dict(FEATURES.get(p.catalog or "", {}))
        feat.update(x(p, "features") or {})
        if not feat:
            out.append(fail("cots.fidelity", G, WARNING, "Bought part has no identifying features",
                            f"`{p.id}` ({p.catalog or 'no catalog'}) has no feature table, so its model is not checked "
                            "against the real part.").on(p.id)
                       .fix("Add the catalog id to cots_fidelity.FEATURES or give the part `features`."))
            continue
        miss = judge(rp, feat)
        if miss:
            out.append(fail("cots.fidelity", G, BLOCKER, "Bought part is missing its identifying features",
                            f"`{p.id}` ({p.catalog}) does not look like the real part: "
                            + "; ".join(f"{a} {w}: {g}" for a, w, g in miss) + f". Source: {feat.get('source', 'catalog')}.")
                       .on(p.id).expect(", ".join(f"{a} {w}" for a, w, _ in miss), ", ".join(g for *_, g in miss))
                       .fix("Model the real part: the bell, the stator base flange, the shaft and the tapped mount holes."))
        else:
            n += 1
    if n:
        out.append(ok("cots.fidelity", G, "Bought parts carry their features", f"{n} motor(s) match their feature tables."))
    return out

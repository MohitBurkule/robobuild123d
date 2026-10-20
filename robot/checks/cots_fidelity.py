"""cots.fidelity: a bought part must look like the real one. Each catalog motor in FEATURES lists the features that
identify it (outrunner: bell diameter, stator-base diameter, shaft diameter, the mount bolt circle on the stator face);
the modelled solid (part frame, motor axis = catalog shaft dir, default +X) must carry every one within TOL_MM.

A motor with no feature table is a warning: nobody can tell whether its model is right. Override or add per robot with
part `features: {...}` (same keys). Screw-head drive recesses are modelled by fastener_shape (world.py) and are not
judged here.

Outrunners (a catalog entry with `bell_d`, or any `weapon_motor*` part) must be modelled as two parts, a rotating can
`<base>_can` (alias `_bell`) and a fixed stator `<base>_stator`, because the can spins with the weapon and the stator is
bolted down: a single fused motor part is a BLOCKER (cots.motor_split), and so is a can whose bore has no stator in it
(cots.motor_bore: less than BORE_FILL_MIN of the bore is stator). The feature table is then judged on can + stator
together in the can's frame. When a `reference_cad` entry maps the motor (its `part` or `with_parts` names the base, the
can or the stator) the motor's ENVELOPE must match the reference's within REF_VOL_TOL, else BLOCKER (cots.motor_volume).
The envelope is the union of can + stator (+ any part declaring `shaft_of` the motor, since the STEP draws the shaft
inside the motor body) with interior voids filled: the solid of revolution of the max radius per axial slice
(envelope_volume). The reference mesh is filled the same way. Raw solid volume is not compared because the RVRN 2.0
STEP GR1507_1 (2303 mm3) is a simplified solid, a hollow can with an r4 core standing in for the stator, so a real
stator inflates raw volume by ~22% while the outer envelope (what clearance and parity depend on) is unchanged. Both raw
and envelope volumes are reported as metrics.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok
from ._review import x

G = "cots"
TOL_MM = 0.3
MOTOR_KINDS = ("motor", "weapon_motor")
ROLES = {"_can": "can", "_bell": "can", "_stator": "stator"}
REF_VOL_TOL = 0.05  # motor envelope vs the reference envelope (RVRN 2.0 STEP GR1507_1, filled the same way)
ENV_SLICE_MM = 0.25
BORE_FILL_MIN = 0.25  # a real stator (core + windings) fills most of the bell bore; less than this is an empty can

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


def _split(pid):
    for suf, role in ROLES.items():
        if pid.endswith(suf):
            return pid[: -len(suf)], role
    return pid, None


def groups(parts):
    """{base id: {"whole"|"can"|"stator": rp}} for every motor (kind in MOTOR_KINDS or a `weapon_motor*` can/stator)."""
    out = {}
    for rp in parts:
        p = rp.part
        base, role = _split(p.id)
        if p.kind in MOTOR_KINDS or (role and (base.startswith("weapon_motor") or p.kind in MOTOR_KINDS)):
            out.setdefault(base, {})[role or "whole"] = rp
    return out


def _feat(g):
    feat = {}
    for rp in g.values():
        feat.update(FEATURES.get(rp.part.catalog or "", {}))
    for rp in g.values():
        feat.update(x(rp.part, "features") or {})
    return feat


def bore_fill(can, stator, n=4000):
    """Fraction of the can's bore (inside its convex hull, outside its material) that the stator occupies (world meshes)."""
    hull = can.convex_hull
    lo, hi = hull.bounds
    P = np.random.default_rng(0).uniform(lo, hi, size=(n, 3))
    P = P[hull.contains(P)]
    if not len(P):
        return 0.0
    bore = P[~can.contains(P)]
    return float(stator.contains(bore).mean()) if len(bore) else 0.0


def envelope_volume(mesh, axis=None, slice_mm=ENV_SLICE_MM, n=40000):
    """Volume (mm3) of the solid of revolution of the max radius per axial slice, interior voids filled. The axis runs
    through the bounding-box centre; with no axis given it is the bbox axis whose cross-section is most nearly square."""
    lo, hi = mesh.bounds
    if axis is None:
        ext = hi - lo
        k = min(range(3), key=lambda i: (abs(ext[(i + 1) % 3] - ext[(i + 2) % 3]) / max(ext.max(), 1e-9), -ext[i]))
        axis = np.eye(3)[k]
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    pts = np.vstack([mesh.vertices, mesh.sample(n)]) - (lo + hi) / 2
    t = pts @ axis
    rho = np.linalg.norm(pts - np.outer(t, axis), axis=1)
    nb = max(1, int(np.ceil((t.max() - t.min()) / slice_mm)))
    idx = np.minimum(((t - t.min()) / (t.max() - t.min() + 1e-12) * nb).astype(int), nb - 1)
    rmax = np.zeros(nb)
    np.maximum.at(rmax, idx, rho)
    return float(np.pi * (rmax ** 2).sum() * (t.max() - t.min()) / nb)


def ref_volume(ctx, ids):
    """(raw volume mm3, envelope mm3, file) of the reference_cad mesh mapped to any of `ids`, or None."""
    from .reference_cad import _cfg

    cfg = _cfg(ctx.r.spec)
    rdir = Path(getattr(ctx.r.spec, "base_dir", ".") or ".") / (cfg.get("dir") or ".")
    for e in cfg.get("parts") or []:
        if ({e.get("part")} | set(e.get("with_parts") or [])) & ids and e.get("file"):
            path = rdir / e["file"]
            try:
                import trimesh

                rm = trimesh.load(path, force="mesh")
                return abs(float(rm.volume)), envelope_volume(rm), e["file"]
            except Exception:  # noqa: BLE001 - unreadable reference: not checked
                ctx.not_checked.append(f"cots.motor_volume: reference `{path}` not readable")
                return None
    return None


def _judge_report(out, pid, cat, feat, miss):
    out.append(fail("cots.fidelity", G, BLOCKER, "Bought part is missing its identifying features",
                    f"`{pid}` ({cat}) does not look like the real part: "
                    + "; ".join(f"{a} {w}: {g}" for a, w, g in miss) + f". Source: {feat.get('source', 'catalog')}.")
               .on(pid).expect(", ".join(f"{a} {w}" for a, w, _ in miss), ", ".join(g for *_, g in miss))
               .fix("Model the real part: the bell, the stator base flange, the shaft and the tapped mount holes."))


def run(ctx):
    out, n = [], 0
    for base, g in groups(ctx.r.parts).items():
        feat = _feat(g)
        outrunner = "bell_d" in feat or base.startswith("weapon_motor")
        if not outrunner:
            rp = g.get("whole") or next(iter(g.values()))
            p = rp.part
            if not feat:
                out.append(fail("cots.fidelity", G, WARNING, "Bought part has no identifying features",
                                f"`{p.id}` ({p.catalog or 'no catalog'}) has no feature table, so its model is not checked "
                                "against the real part.").on(p.id)
                           .fix("Add the catalog id to cots_fidelity.FEATURES or give the part `features`."))
                continue
            miss = judge(rp, feat)
            if miss:
                _judge_report(out, p.id, p.catalog, feat, miss)
            else:
                n += 1
            continue
        ids = {base} | {rp.part.id for rp in g.values()}
        can, st = g.get("can"), g.get("stator")
        if can is None or st is None:
            pid = (g.get("whole") or can or st).part.id
            have = "a single fused part" if "whole" in g and can is None and st is None else \
                f"only a {'can' if can else 'stator'}"
            out.append(fail("cots.motor_split", G, BLOCKER, "Outrunner not split into can and stator",
                            f"`{pid}` is an outrunner modelled as {have}; the bell spins with the weapon while the stator "
                            "is bolted down, so they must be separate parts.").on(pid)
                       .fix(f"Model `{base}_can` (rotating bell) and `{base}_stator` (fixed stator, base and windings)."))
            continue
        wc, ws = ctx.world.body(can.part.id), ctx.world.body(st.part.id)
        fill = bore_fill(wc.mesh, ws.mesh)
        if fill < BORE_FILL_MIN:
            out.append(fail("cots.motor_bore", G, BLOCKER, "Motor can is empty",
                            f"`{can.part.id}`: the stator `{st.part.id}` fills {fill:.0%} of the can's bore "
                            f"(min {BORE_FILL_MIN:.0%}); a real outrunner has its stator inside the bell.")
                       .on(can.part.id, st.part.id).fix("Put the stator core (and windings) inside the can's bore."))
        else:
            out.append(ok("cots.motor_bore", G, "Stator sits inside the can", f"`{st.part.id}` fills {fill:.0%} of the bore.")
                       .on(can.part.id, st.part.id))
        if feat:
            import trimesh

            m = trimesh.util.concatenate([wc.mesh, ws.mesh])
            m.apply_transform(np.linalg.inv(wc.M))
            cat = next((rp.cat for rp in (can, st) if rp.cat is not None), None)
            miss = judge(SimpleNamespace(geom=SimpleNamespace(mesh=m), cat=cat), feat)
            if miss:
                _judge_report(out, can.part.id, can.part.catalog or st.part.catalog or base, feat, miss)
            else:
                n += 1
        import trimesh

        extra = [rp.part.id for rp in ctx.r.parts if x(rp.part, "shaft_of") in ids]
        bodies = [ctx.world.body(i).mesh for i in [can.part.id, st.part.id] + extra]
        vol = sum(abs(float(b.volume)) for b in bodies)
        um = trimesh.util.concatenate(bodies)
        um.apply_transform(np.linalg.inv(wc.M))
        env = envelope_volume(um, _frame(can))
        ctx.metrics[f"cots.motor.{base}"] = {"volume_mm3": round(vol, 1), "envelope_mm3": round(env, 1),
                                             "bore_fill": round(fill, 3)}
        rv = ref_volume(ctx, ids)
        if rv is not None:
            rraw, ref, fn = rv
            ctx.metrics[f"cots.motor.{base}"].update(ref_volume_mm3=round(rraw, 1), ref_envelope_mm3=round(ref, 1))
            d = env / ref - 1 if ref > 0 else 0.0
            msg = (f"`{base}` envelope of can + stator{' + ' + ', '.join(extra) if extra else ''} {env:.0f} mm3 vs "
                   f"reference `{fn}` envelope {ref:.0f} mm3 ({d:+.1%}, tol ±{REF_VOL_TOL:.0%}, per RVRN 2.0 STEP "
                   f"GR1507_1); raw solid {vol:.0f} vs {rraw:.0f} mm3 (not judged: the STEP stator is a simplified core)")
            out.append(ok("cots.motor_volume", G, "Motor envelope matches the reference", msg).on(can.part.id, st.part.id)
                       if abs(d) <= REF_VOL_TOL else
                       fail("cots.motor_volume", G, BLOCKER, "Motor envelope differs from the reference", msg)
                       .on(can.part.id, st.part.id).fix("Match the bell, base flange and shaft outline to the reference CAD."))
    if n:
        out.append(ok("cots.fidelity", G, "Bought parts carry their features", f"{n} motor(s) match their feature tables."))
    return out

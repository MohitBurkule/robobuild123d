"""Declared target dimensions (`targets` in the spec, e.g. measured off photos of the real robot) checked against the
model. Optional: a spec without `targets` gets no findings."""

from __future__ import annotations

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok
from .power import rim_radius, spin_axis

G = "targets"
DEFAULT_TOL_MM = 2.0
DEFAULT_TOL_PCT = 3.0  # for masses
ALIASES = {"length": "length_mm", "width": "width_mm", "height": "height_mm", "disc_dia": "disc_dia_mm",
           "weapon_dia": "disc_dia_mm", "wheel_dia": "wheel_dia_mm", "mass": "mass_g", "wheelbase": "wheelbase_mm"}
META = {"tol_mm", "tol_pct", "source", "note"}


def _role(p):
    return getattr(p, "role", None) or (getattr(p, "_extra", None) or {}).get("role")


def measure_targets(ctx):
    """Model values for every target key we know how to measure (None when it cannot be measured)."""
    r, w = ctx.r, ctx.world
    vals = {}
    solid = [b for b in w.bodies if not b.is_wire]
    if solid:
        lo = np.min([b.aabb[0] for b in solid], axis=0)
        hi = np.max([b.aabb[1] for b in solid], axis=0)
        ext = hi - lo
        vals.update(width_mm=float(ext[0]), length_mm=float(ext[1]), height_mm=float(ext[2]))
    wheels = [b for b in w.bodies if b.kind == "wheel"]
    if wheels:
        vals["wheel_dia_mm"] = max(float(sorted(b.aabb[1] - b.aabb[0])[-1]) for b in wheels)
        ys = [float(b.center[1]) for b in wheels]
        vals["wheelbase_mm"] = max(ys) - min(ys) if len(wheels) > 2 else None
    dias = []
    for i, b in enumerate(w.bodies):
        sa = spin_axis(w, r, i) if b.part_idx is not None and b.kind == "weapon" else None
        if sa is not None:
            dias.append(2.0 * rim_radius(b, *sa))
            # a spider / hub weapon carries its blades as separate parts riding the same rotor: the disc is the biggest
            rw = getattr(r.parts[b.part_idx].part, "rotates_with", None)
            for o in w.bodies:
                if o is not b and o.part_idx is not None and not o.is_wire and rw and getattr(r.parts[o.part_idx].part, "rotates_with", None) == rw \
                        and _role(r.parts[o.part_idx].part) == "blade":
                    dias.append(2.0 * rim_radius(o, *sa))
    vals["disc_dia_mm"] = max(dias) if dias else None
    vals["mass_g"] = ctx.metrics.get("mass_total_g")
    return vals


def run(ctx):
    t = ctx.r.spec.raw.get("targets")
    if not t:
        return []
    out = []
    if not isinstance(t, dict):
        return [fail("targets.invalid", G, BLOCKER, "Targets are not a table", "`targets` must map names to numbers.")]
    tol_mm = float(t.get("tol_mm", DEFAULT_TOL_MM))
    tol_pct = float(t.get("tol_pct", DEFAULT_TOL_PCT))
    vals = measure_targets(ctx)
    bad = n = 0
    for k, want in t.items():
        if k in META:
            continue
        key = ALIASES.get(k, k)
        if key not in vals:
            out.append(fail("targets.unknown", G, WARNING, "Target cannot be measured",
                            f"`{k}` is not a known target ({', '.join(sorted(set(vals)))})."))
            ctx.not_checked.append(f"Target `{k}`: no measurement for it")
            continue
        got = vals[key]
        if got is None:
            ctx.not_checked.append(f"Target `{k}`: the model has nothing to measure it on")
            continue
        n += 1
        want = float(want)
        tol = abs(want) * tol_pct / 100.0 if key == "mass_g" else tol_mm
        unit = "g" if key == "mass_g" else "mm"
        if abs(got - want) > tol:
            bad += 1
            out.append(fail("targets.mismatch", G, BLOCKER, "Model differs from the target",
                            f"`{k}` is {got:.1f} {unit} in the model, target {want:.1f} {unit} (tolerance {tol:.1f} {unit}).")
                       .expect(f"{want:.1f} +/- {tol:.1f} {unit}", f"{got:.1f} {unit}")
                       .fix("Resize the model to the target, or correct the target if it was misread."))
    if n and bad == 0:
        out.append(ok("targets.match", G, "Model matches the targets", f"{n} target dimensions within tolerance."))
    return out

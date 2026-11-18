"""Requirements block (`requirements.*`, group `requirements`, B1).

WHY: users speak intent ("fast pusher, survives vertical spinners, under £80"),
not enums. The spec may declare a top-level `requirements` object; this group
compares each declared requirement against the metrics earlier groups measured,
so a design that misses the intent fails with expected/actual stated.

Supported keys (metric, how it is judged):
  weapon_energy_j      metrics.weapon_energy_j          min
  weapon_tip_speed_mps metrics.tip_speed_mph * 0.44704  min/max
  peak_current_a       metrics.peak_current_a           max
  runtime_min          metrics.runtime_min              min
  mass_max_g           metrics.mass_total_g             max
  mass_margin_g        limit - metrics.mass_hi_g        min
  footprint_max_mm     metrics.footprint_mm             max
  budget_gbp           metrics.bom_cost_gbp             max
  top_speed_mps / push_force_n - no metric yet: NOT CHECKED with a note saying which group would supply it.

An unknown requirement key is a blocker (the intent silently doing nothing is
worse than an error). A metric that never got computed is NOT CHECKED, never a pass.
"""

from __future__ import annotations

from ..finding import BLOCKER, fail, ok

G = "requirements"
MPH_TO_MS = 0.44704

# key -> (metric, op, unit); op "min" | "max"
SUPPORTED = {
    "weapon_energy_j": ("weapon_energy_j", "min", "J"),
    "weapon_tip_speed_mps": ("tip_speed_mph", "min", "m/s"),
    "peak_current_a": ("peak_current_a", "max", "A"),
    "runtime_min": ("runtime_min", "min", "min"),
    "mass_max_g": ("mass_total_g", "max", "g"),
    "mass_margin_g": ("__mass_margin__", "min", "g"),
    "footprint_max_mm": ("footprint_mm", "max", "mm"),
    "budget_gbp": ("bom_cost_gbp", "max", "GBP"),
}
NO_METRIC_YET = {"top_speed_mps": "the drive-performance group", "push_force_n": "the drive-performance group",
                 "must_survive": "the threat group's verdicts", "invertible": "the dynamics group's invert check"}


def metric_value(key, metrics):
    m, _op, _u = SUPPORTED[key]
    if m == "__mass_margin__":
        if "mass_hi_g" not in metrics:
            return None
        return metrics.get("mass_limit_g", 150.0) - metrics["mass_hi_g"]
    v = metrics.get(m)
    return None if v is None else (v * MPH_TO_MS if m == "tip_speed_mph" else v)


def run(ctx):
    req = (getattr(ctx.r.spec, "raw", None) or {}).get("requirements")
    out = []
    if not isinstance(req, dict) or not req:
        ctx.not_checked.append("Requirements: the spec declares no requirements block")
        return out
    for key, want in sorted(req.items()):
        if key in NO_METRIC_YET:
            ctx.not_checked.append(f"Requirement {key}: no metric yet ({NO_METRIC_YET[key]} would judge it)")
            continue
        if key not in SUPPORTED:
            out.append(fail("requirements.unknown_key", G, BLOCKER, f"Unsupported requirement {key!r}",
                            f"{key!r} is not a requirement the verifier can judge; supported: {sorted(SUPPORTED)}.")
                       .fix(f"Remove {key}, or move it into the design settings it maps to."))
            continue
        _metric, op, unit = SUPPORTED[key]
        v = metric_value(key, ctx.metrics)
        if v is None:
            ctx.not_checked.append(f"Requirement {key}: its metric was not computed this run")
            continue
        lo = want.get("min") if isinstance(want, dict) else (want if op == "min" else None)
        hi = want.get("max") if isinstance(want, dict) else (want if op == "max" else None)
        bad = (lo is not None and v < lo) or (hi is not None and v > hi)
        target = f"{'>=' + str(lo) if lo is not None else ''}{' <= ' + str(hi) if hi is not None else ''}".strip()
        if not bad:
            out.append(ok(f"requirements.{key}", G, f"Requirement {key} met",
                          f"{v:.2f} {unit} vs {target} {unit}."))
        else:
            out.append(fail(f"requirements.{key}", G, BLOCKER, f"Requirement {key} not met",
                            f"{v:.2f} {unit} vs {target} {unit}.")
                       .expect(target, f"{v:.2f} {unit}")
                       .fix("Change the design toward this requirement (a setting swap or dimension), "
                            "or relax the requirement if it was aspirational."))
    return out

"""Mass budget vs the class limit. Uses check metrics/mass lines when a report is given, else spec/catalog."""

from __future__ import annotations

from .. import catalog
from ._util import x

LIMIT_G = 150.0  # Antweight World Series; profile overrides via spec.raw['mass_limit_g']


def mass_budget(spec, report=None, limit_g=None):
    limit = float(limit_g or spec.raw.get("mass_limit_g") or LIMIT_G)
    lines = []
    if report is not None and getattr(report, "mass", None):
        for m in report.mass:  # finding.MassLine(id, kind, grams, tol_g, source); tol_g is absolute grams
            lines.append({"id": m.id, "g": float(m.grams), "tol": float(getattr(m, "tol_g", 0.0) or 0.0),
                          "source": getattr(m, "source", "check")})
    else:
        for p in spec.parts:
            g, src = None, "unknown"
            for k in ("scale_mass_g", "slicer_mass_g", "mass_g"):
                if x(p, k) is not None:
                    g, src = float(x(p, k)), k
                    break
            if g is None and x(p, "catalog"):
                e = catalog.find(x(p, "catalog"))
                if e:
                    g, src = e.mass_g, "catalog"
            lines.append({"id": p.id, "g": g, "tol": 0.0, "source": src})
    known = sum(l["g"] for l in lines if l["g"] is not None)
    tol = sum(l["tol"] for l in lines if l["g"] is not None)
    unknown = [l["id"] for l in lines if l["g"] is None]
    return {"limit_g": limit, "total_g": round(known, 2), "tol_g": round(tol, 2),
            "margin_g": round(limit - known - tol, 2), "ok": not unknown and known + tol <= limit,
            "unknown": unknown, "lines": sorted(lines, key=lambda l: -(l["g"] or 0))}

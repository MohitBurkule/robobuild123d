"""Sheet cut list: flat (laser/waterjet/bent) parts grouped by material + thickness, with nested-area estimate."""

from __future__ import annotations

from ._util import x

SHEET_PROCESSES = ("laser", "waterjet", "sheet", "bent_sheet", "cnc_plate")


def _thk(p):
    for k in ("thickness_mm", "stock_mm", "t"):
        v = x(p, k) or (x(p, "params") or {}).get(k)
        if v:
            return float(v)
    return None


def cut_list(spec, world=None, dxf_dir="dxf"):
    rows = []
    for p in spec.parts:
        if (x(p, "process") or "").lower() not in SHEET_PROCESSES:
            continue
        area = None
        if world is not None:
            b = world.body(p.id)
            if b is not None and _thk(p):
                try:
                    area = round(float(b.geom.volume) / _thk(p), 1)  # flat area = volume / stock
                except Exception:  # noqa: BLE001
                    area = None
        rows.append({"id": p.id, "material": x(p, "material"), "thickness_mm": _thk(p),
                     "process": x(p, "process"), "bend": (x(p, "process") or "") == "bent_sheet",
                     "dxf": f"{dxf_dir}/{p.id}.dxf", "area_mm2": area, "qty": int(x(p, "qty", 1) or 1)})
    groups = {}
    for r in rows:
        groups.setdefault((r["material"], r["thickness_mm"]), []).append(r)
    return {"rows": rows, "sheets": [{"material": m, "thickness_mm": t, "parts": [r["id"] for r in rs],
                                      "area_mm2": sum((r["area_mm2"] or 0) * r["qty"] for r in rs) or None}
                                     for (m, t), rs in groups.items()]}

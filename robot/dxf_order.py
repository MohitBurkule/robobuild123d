"""DXF sheet/turned-part order pack (D6): what to order when parts are not printed.

`rows(spec)` classifies every made part by its canonical process: sheet parts (`laser`,
`waterjet`, `sheet`, `bent_sheet`, ...) become cut blanks - stock thickness snapped to the
material's real sheet sizes (catalog.SHEET_STOCK_MM), blank size = profile + clamping margin,
a DXF outline on layer `CUT` when a mesh is supplied; turned parts become bar orders - stock
diameter snapped up to the material's rod sizes (catalog.ROD_STOCK_MM), length + facing
allowance per end. `write(spec, out_dir, meshes=None)` writes `dxf/<id>.dxf`,
`order_sheet.csv`, `order_turned.csv` and `dxf_order.json`; a part whose thickness or stock
is not a real size is flagged in the row, never silently rounded away.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from . import catalog
from .mfg._util import x

SHEET_MARGIN_MM = 3.0      # clamping margin around the profile on the blank
FACE_ALLOWANCE_MM = 1.0    # parting-off / facing stock per end of a turned part


def _canon(process):
    """Canonical process, with a substring fallback for spec spellings the alias table misses."""
    c = catalog.process_canon(process)
    if c:
        return c
    p = str(process or "").lower()
    if any(k in p for k in ("sheet", "laser", "waterjet", "bend", "brake")):
        return "sheet_cut"
    if "lathe" in p or "turn" in p:
        return "turned"
    return None


LOCAL_FAMILY = (("7075", "aluminium"), ("6061", "aluminium"), ("5052", "aluminium"),
                 ("2024", "aluminium"), ("gr5", "titanium"), ("gr9", "titanium"),
                 ("acetal", "pom"), ("delrin", "pom"))


def _family(material):
    """Sheet/rod stock family: exact alias match, else a substring match (titanium_gr5, hardox500, al7075)."""
    m = str(material or "").lower()
    f = catalog.sheet_family(m)
    if f:
        return f
    for key, fam in LOCAL_FAMILY:
        if key in m:
            return fam
    for key, fam in catalog.SHEET_FAMILY.items():
        if key in m:
            return fam
    return m or None


def _thk(p):
    for k in ("thickness_mm", "stock_mm", "t"):
        v = x(p, k) or (x(p, "params") or {}).get(k)
        if v:
            return float(v)
    return None


def _od_len(p):
    """Turned part's (od_mm, len_mm) from declared params, else (None, None)."""
    pr = x(p, "params") or {}
    od = x(p, "od_mm") or pr.get("od_mm") or pr.get("diameter_mm")
    ln = x(p, "len_mm") or pr.get("len_mm") or pr.get("length_mm")
    return (float(od) if od else None, float(ln) if ln else None)


def _snap_up(value, sizes):
    """Smallest stock size >= value, or None when the part is bigger than any stock size."""
    for s in sizes:
        if value <= s + 1e-9:
            return s
    return None


def _outline(mesh):
    """(rings, w, d) - polygon rings of the mid-thickness slice and the bbox size, or None."""
    import numpy as np

    lo, hi = mesh.bounds
    z = (lo[2] + hi[2]) / 2
    try:
        sec = mesh.section(plane_normal=[0, 0, 1], plane_origin=[0, 0, z])
        if sec is None:
            return None
        res = sec.to_2D() if hasattr(sec, "to_2D") else sec.to_planar()
        p2 = res[0] if isinstance(res, tuple) else res
        rings = []
        for poly in p2.polygons_full:
            rings.append([(float(px), float(py)) for px, py in poly.exterior.coords])
            for hole in poly.interiors:
                rings.append([(float(px), float(py)) for px, py in hole.coords])
        if not rings:
            return None
        pts = np.asarray([q for r in rings for q in r])
        return rings, float(np.ptp(pts[:, 0])), float(np.ptp(pts[:, 1]))
    except Exception:  # noqa: BLE001
        return None


def rows(spec, meshes=None):
    """spec parts -> {"sheet": [...], "turned": [...]}. meshes: {id: mesh} for outlines/sizes."""
    meshes = meshes or {}
    sheet, turned = [], []
    for p in spec.parts:
        canon = _canon(x(p, "process"))
        if x(p, "catalog") or canon not in ("sheet_cut", "sheet_bent", "turned"):
            continue
        if canon == "turned":
            od, ln = _od_len(p)
            m = meshes.get(p.id)
            if m is not None and (od is None or ln is None):
                lo, hi = m.bounds
                od = od or float(max(hi[0] - lo[0], hi[1] - lo[1]))
                ln = ln or float(hi[2] - lo[2])
            if od is None or ln is None:
                turned.append({"id": p.id, "material": x(p, "material"), "od_mm": od,
                               "len_mm": ln, "stock_dia_mm": None, "stock_len_mm": None,
                               "qty": int(x(p, "qty", 1) or 1), "note": "size undeclared"})
                continue
            fam = _family(x(p, "material"))
            stock_d = _snap_up(od, catalog.ROD_STOCK_MM.get(fam, []))
            stock_l = round(ln + 2 * FACE_ALLOWANCE_MM, 2)
            turned.append({"id": p.id, "material": x(p, "material"), "od_mm": od, "len_mm": ln,
                           "stock_dia_mm": stock_d, "stock_len_mm": stock_l,
                           "qty": int(x(p, "qty", 1) or 1),
                           "note": None if stock_d else f"no {fam or 'known'} rod stock >= {od:.1f} mm"})
            continue
        t = _thk(p)
        m = meshes.get(p.id)
        if t is None and m is not None:
            lo, hi = m.bounds
            t = float(hi[2] - lo[2])
        fam = _family(x(p, "material"))
        stock_t = _snap_up(t, catalog.SHEET_STOCK_MM.get(fam, [])) if t is not None else None
        out = _outline(m) if m is not None else None
        w = out[1] if out else None
        d = out[2] if out else None
        note = None
        if t is None:
            note = "thickness undeclared"
        elif stock_t is None:
            note = f"no {fam} sheet stock {t:g} mm"
        elif abs(stock_t - t) > 1e-9:
            note = f"thickness {t:g} mm is not stock; nearest up is {stock_t:g} mm"
        sheet.append({"id": p.id, "material": x(p, "material"), "thickness_mm": t,
                      "stock_thickness_mm": stock_t, "process": x(p, "process"),
                      "blank_x_mm": None if w is None else round(w + 2 * SHEET_MARGIN_MM, 1),
                      "blank_y_mm": None if d is None else round(d + 2 * SHEET_MARGIN_MM, 1),
                      "qty": int(x(p, "qty", 1) or 1), "dxf": f"dxf/{p.id}.dxf" if out else None,
                      "note": note})
    return {"sheet": sheet, "turned": turned}


def _write_dxf(rings, path):
    import ezdxf

    doc = ezdxf.new("R2010")
    doc.layers.add("CUT", color=1)
    msp = doc.modelspace()
    for ring in rings:
        msp.add_lwpolyline(ring, close=True, dxfattribs={"layer": "CUT"})
    doc.saveas(str(path))


def write(spec, out_dir, meshes=None):
    """Writes dxf/<id>.dxf, order_sheet.csv, order_turned.csv, dxf_order.json; returns the rows dict."""
    out = Path(out_dir)
    (out / "dxf").mkdir(parents=True, exist_ok=True)
    data = rows(spec, meshes)
    for r in data["sheet"]:
        m = (meshes or {}).get(r["id"])
        if m is None:
            r["dxf"] = None
            continue
        o = _outline(m)
        if o is None:
            r["dxf"] = None
            continue
        _write_dxf(o[0], out / "dxf" / f"{r['id']}.dxf")
    for name, key in (("order_sheet.csv", "sheet"), ("order_turned.csv", "turned")):
        with open(out / name, "w", newline="") as fh:
            rs = data[key]
            w = csv.DictWriter(fh, fieldnames=list(rs[0].keys()) if rs else ["id"])
            w.writeheader()
            w.writerows(rs)
    (out / "dxf_order.json").write_text(json.dumps(data, indent=2, default=str))
    return data

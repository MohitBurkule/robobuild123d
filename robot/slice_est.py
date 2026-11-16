"""Slice-based mass & print-time estimate (D5): what a part will weigh and cost in machine time.

`estimate(mesh)` slices an oriented mesh at layer height and sums the extrusion each layer
needs: `walls` perimeter passes at the bead section (nozzle x layer) plus a solid skin at the
top and bottom and `infill_pct` of the section area elsewhere. Extruded volume gives both
numbers a builder orders around: filament mass (volume x spool density) and print time
(volume / (bead section x speed) + per-layer overhead). `write(parts, out_dir)` takes the
same `(id, mesh, print_orientation)` tuples as `robot/plate.py`, orients them the same way,
and writes `slice_est.json` + `slice_est.csv`.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

FILAMENT_MM = 1.75          # 1.75 mm filament cross section (2.405 mm2)
SOLID_SKIN_MM = 0.6         # solid top/bottom depth before sparse infill starts
LAYER_OVERHEAD_S = 2.0      # retract / travel / z-hop per layer
PART_OVERHEAD_S = 60.0      # heat-up + first-layer fuss per part


def _layers(mesh, layer_mm):
    """(area_mm2, perimeter_mm) per slice, from bed to top; None where slicing fails."""
    z0, z1 = mesh.bounds[0][2], mesh.bounds[1][2]
    z, out = z0 + layer_mm / 2, []
    while z < z1 - 1e-9:
        area = perim = None
        try:
            sec = mesh.section(plane_normal=[0, 0, 1], plane_origin=[0, 0, z])
            if sec is not None:
                res = sec.to_2D() if hasattr(sec, "to_2D") else sec.to_planar()
                p2 = res[0] if isinstance(res, tuple) else res
                polys = p2.polygons_full
                if polys:
                    area = float(sum(abs(p.area) for p in polys))
                    perim = float(sum(p.exterior.length + sum(r.length for r in p.interiors) for p in polys))
        except Exception:  # noqa: BLE001
            pass
        out.append((area, perim))
        z += layer_mm
    return out


def estimate(mesh, printer="ender3", filament="pla", walls=2, infill_pct=15,
              layer_mm=None, speed_mm_s=None):
    """One oriented mesh -> {layers, extruded_mm3, mass_g, filament_m, time_min, mesh_mass_g}."""
    from . import mfg_profiles

    p = mfg_profiles.printer(printer)
    f = mfg_profiles.filament(filament)
    layer = float(layer_mm or min(p.nozzle_mm / 2, 0.2))
    speed = float(speed_mm_s or 50.0)
    bead = p.nozzle_mm * layer
    skin = max(1, int(SOLID_SKIN_MM / layer + 0.5))
    slices = _layers(mesh, layer)
    vol, mesh_vol = 0.0, float(mesh.volume)
    for i, (area, perim) in enumerate(slices):
        if area is None:  # slicing failed: fall back to the mean section over the whole part
            area, perim = mesh_vol / max(1e-9, mesh.bounds[1][2] - mesh.bounds[0][2]), 0.0
        solid = i < skin or i >= len(slices) - skin
        frac = 1.0 if solid else max(0.0, infill_pct) / 100.0
        vol += walls * (perim or 0.0) * bead + area * frac * layer
    fil_len = vol / (3.141592653589793 * (FILAMENT_MM / 2) ** 2)
    time_s = vol / (bead * speed) + len(slices) * LAYER_OVERHEAD_S + PART_OVERHEAD_S
    return {"layers": len(slices), "extruded_mm3": round(vol, 1),
            "mass_g": round(vol / 1000.0 * f.density_g_cc, 2),
            "filament_m": round(fil_len / 1000.0, 2), "time_min": round(time_s / 60.0, 1),
            "mesh_mass_g": round(mesh_vol / 1000.0 * f.density_g_cc, 2)}


def parts(items, printer="ender3", filament="pla", walls=2, infill_pct=15,
          layer_mm=None, speed_mm_s=None):
    """[(id, mesh, print_orientation or None)] -> {parts: [...], total: {...}} (oriented like plate.py)."""
    from . import plate

    rows, tot = [], {"mass_g": 0.0, "filament_m": 0.0, "time_min": 0.0, "extruded_mm3": 0.0}
    for pid, mesh, up in items:
        e = estimate(plate.orient(mesh, up or "+z"), printer, filament, walls,
                     infill_pct, layer_mm, speed_mm_s)
        e["id"] = pid
        rows.append(e)
        for k in tot:
            tot[k] = round(tot[k] + e[k], 2)
    return {"printer": printer, "filament": filament, "parts": rows, "total": tot}


def write(items, out_dir, printer="ender3", filament="pla", walls=2, infill_pct=15,
          layer_mm=None, speed_mm_s=None):
    """items: [(id, mesh, print_orientation or None)]. Writes slice_est.json/csv; returns the summary."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    info = parts(items, printer, filament, walls, infill_pct, layer_mm, speed_mm_s)
    (out / "slice_est.json").write_text(json.dumps(info, indent=2))
    with open(out / "slice_est.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "layers", "extruded_mm3", "mass_g",
                                          "filament_m", "time_min", "mesh_mass_g"])
        w.writeheader()
        w.writerows(info["parts"])
    return info

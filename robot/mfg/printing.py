"""Print settings per FDM/resin part: material, orientation (declared, as print_orient checks it), supports."""

from __future__ import annotations

from .. import catalog
from ._util import x

# conservative antweight defaults per material; spec part `print: {...}` overrides any key
DEFAULTS = {
    "tpu": {"nozzle_c": 225, "bed_c": 50, "walls": 4, "infill_pct": 30, "layer_mm": 0.2, "speed_mm_s": 25},
    "petg": {"nozzle_c": 240, "bed_c": 80, "walls": 4, "infill_pct": 40, "layer_mm": 0.2, "speed_mm_s": 50},
    "pla": {"nozzle_c": 210, "bed_c": 60, "walls": 4, "infill_pct": 40, "layer_mm": 0.2, "speed_mm_s": 60},
    "nylon": {"nozzle_c": 255, "bed_c": 70, "walls": 5, "infill_pct": 50, "layer_mm": 0.2, "speed_mm_s": 40},
    "pa_cf": {"nozzle_c": 270, "bed_c": 80, "walls": 5, "infill_pct": 50, "layer_mm": 0.2, "speed_mm_s": 40},
}


def print_settings(spec, metrics=None, max_overhang_mm2=None):
    """Rows for printed parts. `metrics` = check ctx.metrics (print_declared_overhang_mm2.<id>) when available."""
    from ..checks.printability import MAX_OVERHANG_MM2
    lim = float(max_overhang_mm2 or MAX_OVERHANG_MM2)
    rows = []
    for p in spec.parts:
        if x(p, "catalog") or not catalog.part_is_printed(x(p, "process"), x(p, "material")):
            continue
        mat = (x(p, "material") or "pla").lower()
        s = dict(DEFAULTS.get(mat, DEFAULTS["pla"]))
        s.update(x(p, "print") or {})
        ov = (metrics or {}).get(f"print_declared_overhang_mm2.{p.id}")
        rows.append({"id": p.id, "material": mat, "process": x(p, "process") or "fdm",
                     "up_axis": x(p, "print_orientation") or "UNDECLARED",
                     "overhang_mm2": ov, "supports": None if ov is None else ov > lim,
                     "solid_fraction": x(p, "solid_fraction"), **s})
    return rows

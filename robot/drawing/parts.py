"""[drawing] Part registry: how to build a part, its spec material, and named params to cross-check dims against.

`<part>` on the command line is a registry name (e.g. revron.chassis), a STEP / BREP file, or module:function."""
from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@dataclass
class PartInfo:
    name: str
    shape: object
    title: str = ""
    dwg_no: str = ""
    material: str = ""            # spec material id, e.g. pla_st
    solid_fraction: float = 1.0   # print infill fraction from the spec (mass note)
    params: list = field(default_factory=list)   # [(param name, expected value, probe)] cross-checks
    source: str = ""
    hole_roles: list = field(default_factory=list)   # [(d, axis, role)] named on hole callouts
    insert_bores: list = field(default_factory=list)  # [(insert catalog id, insert OD, [(x, y)], axis)] heat-set bores
    ref_matrix: object = None    # 4x4 reference (STEP) frame -> part frame


def _revron_path():
    """Put this tree's revron sources on the path unless a revron package is already importable (another tree's on PYTHONPATH)."""
    import importlib.util
    p = ROOT / "robots" / "revron" / "src"
    if importlib.util.find_spec("revron") is None and str(p) not in sys.path:
        sys.path.insert(0, str(p))


def revron_chassis():
    _revron_path()
    from revron import tub
    from revron import params_chassis as pc
    try:
        from revron import tub2_params as tp
        bore_r, ins = tp.BORE_R, tp.INS
    except Exception:         # noqa: BLE001 - older trees without the tub2 masters
        bore_r, ins = None, pc.INS
    shape = tub.chassis()
    mat, frac = "pla_st", 1.0
    try:
        from revron.spec import make_spec
        part = next(p for p in make_spec("model.py")["parts"] if p["id"] == "tub")
        mat, frac = part.get("material", mat), part.get("solid_fraction", 1.0)
    except Exception:         # noqa: BLE001 - the spec needs the full robot tree; keep the default
        pass
    params = [("CH_Y0", pc.CH_Y0, {"k": "bbox", "i": 1, "which": "min"}),
              ("CH_Z1", pc.CH_Z1, {"k": "bbox", "i": 2, "which": "max"}),
              ("FLOOR_Z", pc.FLOOR_Z, {"k": "bbox", "i": 2, "which": "min"}),
              ("CH_Z1 - FLOOR_Z", pc.CH_Z1 - pc.FLOOR_Z, {"k": "extent", "i": 2}),
              ("CH_WALL (top chamfer)", pc.CH_WALL, {"k": "chamfer_max"})]
    if bore_r is not None:
        params.append(("2 * BORE_R", 2 * bore_r, {"k": "hole_d_near", "pts": [[x, y] for x, y in ins], "axis": [0, 0, 1]}))
    params += [(f"INS[{i}]", (x, y), {"k": "hole_xy", "xy": [x, y], "axis": [0, 0, 1]}) for i, (x, y) in enumerate(ins)]
    info = PartInfo("revron.chassis", shape, "REVRON CHASSIS (TUB)", "RV01", mat, frac, params, "robots/revron tub.chassis()")
    od = insert_od("heatset_m2_4")
    if bore_r is not None:
        info.hole_roles.append((2 * bore_r, (0, 0, 1), "HEAT-SET INSERT BORE"))
        info.insert_bores.append(("heatset_m2_4", od, [list(p) for p in ins], (0, 0, 1)))
    info.hole_roles.append((1.7, (0, 0, 1), "SWITCH SCREW PILOT"))   # tub.py: M2x3 thread-forming into the 1.7 pilot
    info.ref_matrix = pc.REF_TO_WORLD
    return info


def insert_od(cid):
    """Insert OD from the catalogue: the outer cylinder radius of its shape (base of the subtract tree)."""
    from robot.catalog import find
    s = find(cid).shape
    while s.get("type") in ("subtract", "place"):
        s = s["base"] if s["type"] == "subtract" else s["shape"]
    return 2 * s["radius"]


REGISTRY = {"revron.chassis": revron_chassis, "RV01": revron_chassis, "chassis": revron_chassis}


def load(part: str) -> PartInfo:
    if part in REGISTRY:
        return REGISTRY[part]()
    p = Path(part)
    if p.suffix.lower() in (".step", ".stp", ".brep"):
        from build123d import import_brep, import_step
        shp = import_step(str(p)) if p.suffix.lower() != ".brep" else import_brep(str(p))
        return PartInfo(p.stem, shp, p.stem.upper(), p.stem, source=str(p))
    if ":" in part:
        mod, fn = part.split(":", 1)
        return PartInfo(part, getattr(importlib.import_module(mod), fn)(), fn.upper(), fn, source=part)
    raise SystemExit(f"unknown part {part!r}: use one of {sorted(REGISTRY)}, a .step/.brep file or module:function")

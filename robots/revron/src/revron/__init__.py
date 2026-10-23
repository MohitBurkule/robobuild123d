"""[fix-S] Revron generator package (split from build_revron.py; geometry unchanged).

Modules share one namespace: after import every module sees every other module's names (cross-group calls such as
the chassis using weapon-mount profiles resolve at call time)."""
import os as _os, sys as _sys
_SHARED = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", "..", "shared", "src"))
if _SHARED not in _sys.path:   # the shared robocad helpers (geom, plate, prism, rig)
    _sys.path.insert(0, _SHARED)
from . import (variants, params, common, tub2_params, tub2_util, tub2_arcs, tub2_body, tub2_cols, tub2_blocks, tub2_pockets, tub2_seat, tub2_fillets, tub2_lobes, tub2_front, tub2_switch, tub2_lug, tub2_tab, tub2_flange, tub2_lattice, tub2, tub,
               side_wall, side, side_joint, fork, hubs, wedgelet, mount, drisk, weapon, assembly, joints, spec)

MODULES = (variants, params, common, tub2_params, tub2_util, tub2_arcs, tub2_body, tub2_cols, tub2_blocks, tub2_pockets, tub2_seat, tub2_fillets, tub2_lobes, tub2_front, tub2_switch, tub2_lug, tub2_tab, tub2_flange, tub2_lattice, tub2, tub,
           side_wall, side, side_joint, fork, hubs, wedgelet, mount, drisk, weapon, assembly, joints, spec)
NAMESPACE = {}
for _m in MODULES:
    NAMESPACE.update({k: v for k, v in vars(_m).items() if not k.startswith("__") and k not in ("_m",)})
for _m in MODULES:
    for _k, _v in NAMESPACE.items():
        vars(_m).setdefault(_k, _v)
del _m, _k, _v

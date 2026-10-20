"""[fix-S] Revron generator package (split from build_revron.py; geometry unchanged).

Modules share one namespace: after import every module sees every other module's names (cross-group calls such as
the chassis using weapon-mount profiles resolve at call time)."""
from . import params, common, tub, side, mount, drisk, weapon, assembly, spec

MODULES = (params, common, tub, side, mount, drisk, weapon, assembly, spec)
NAMESPACE = {}
for _m in MODULES:
    NAMESPACE.update({k: v for k, v in vars(_m).items() if not k.startswith("__") and k not in ("_m",)})
for _m in MODULES:
    for _k, _v in NAMESPACE.items():
        vars(_m).setdefault(_k, _v)
del _m, _k, _v

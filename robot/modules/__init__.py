"""Robot part modules (UNTESTED: written without running).

REGISTRY maps a config `type` name to its module class. Imports are tolerant so a half-written module
does not break the others.
"""
from __future__ import annotations

import importlib

from .base import Module, ModuleResult, Mount, place

REGISTRY: dict[str, type] = {}
_SPECS = {
    "wheel": ("wheel", "Wheel"),
    "drive_pod": ("drive_pod", "DrivePod"),
    "weapon": ("weapon", "WeaponModule"),
    "electronics_bay": ("electronics_bay", "ElectronicsBay"),
    "tub": ("tub", "TubShell"),
}
IMPORT_ERRORS: dict[str, str] = {}
for _name, (_mod, _cls) in _SPECS.items():
    try:
        _c = getattr(importlib.import_module(f".{_mod}", __name__), _cls)
        REGISTRY[_name] = _c
        globals()[_cls] = _c
    except Exception as _e:  # noqa: BLE001
        IMPORT_ERRORS[_name] = repr(_e)


def make(kind: str, **kwargs) -> Module:
    """Instantiate a registered module by name; unknown kwargs are dropped if the class rejects them."""
    if kind not in REGISTRY:
        raise KeyError(f"unknown module {kind!r} (have {sorted(REGISTRY)}; import errors {IMPORT_ERRORS})")
    cls = REGISTRY[kind]
    try:
        return cls(**kwargs)
    except TypeError:
        import inspect
        ok = set(inspect.signature(cls).parameters)
        return cls(**{k: v for k, v in kwargs.items() if k in ok})


__all__ = ["Module", "ModuleResult", "Mount", "place", "REGISTRY", "IMPORT_ERRORS", "make", *[c for _, c in _SPECS.values()]]

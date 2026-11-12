"""Revron helper modules reused as-is (no copies). UNTESTED.

The revron package __init__ imports every Revron module into one shared namespace (and builds nothing), but only
these self-contained modules are needed, so they are loaded by file path: plate.py (sketch fillets, bolt circles,
PolarLocations hole sets), weapon_motor.py (describe(): GR1507 fit features from the catalogue, pick_bearing()),
hw.py (catalogue part solids: size(), placed()). Each imports only build123d / math / robot.catalog.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
REVRON = os.path.join(ROOT, "robots", "revron", "src", "revron")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def _load(name):
    key = f"scythe._revron_{name}"
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, os.path.join(REVRON, f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod


plate = _load("plate")              # round_corners, holes, polar, ring_window, placed
weapon_motor = _load("weapon_motor")  # describe, pick_bearing, WeaponMotorError
hw = _load("hw")                    # size, reach, placed, switch_mount

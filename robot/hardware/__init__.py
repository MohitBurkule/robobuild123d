"""Standard hardware: typed, sourced dimensions for screws, nuts, washers, inserts, standoffs, pins, circlips,
bearings, O-rings and shafts, plus derived hole features, build123d solids and hole cutters.

    from robot import hardware as hw
    p = hw.get("M3x8 DIN7991")            # Part(kind="screw", record=ScrewHead(...), length=8.0)
    hw.features.clearance(3).value          # 3.4 (ISO 273 normal)
    hw.solids.screw(p)                      # build123d solid (imports build123d lazily)

`solids` and `cutters` import build123d only when a builder is called.
"""

from . import features, registry
from .registry import KINDS, Part, get, list_family, load_errors, nearest_length, records, thread
from .types import (Bearing, Circlip, Insert, Nut, ORing, Pin, ScrewHead, Shaft, Source, Standoff, Thread,
                    Washer)

__all__ = [
    "features", "registry", "solids", "cutters", "KINDS", "Part", "get", "list_family", "load_errors",
    "nearest_length", "records", "thread", "Bearing", "Circlip", "Insert", "Nut", "ORing", "Pin", "ScrewHead",
    "Shaft", "Source", "Standoff", "Thread", "Washer",
]


def __getattr__(name):  # lazy submodules that touch build123d / numpy
    if name in ("solids", "cutters"):
        import importlib

        return importlib.import_module(f"{__name__}.{name}")
    raise AttributeError(name)

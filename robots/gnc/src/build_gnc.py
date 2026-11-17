"""GNC geometry entry point for spec.json model references."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (ROOT, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from gnc import parts as PP  # noqa: E402

_BUILDERS = {
    "tub": PP.tub,
    "lid_l": PP.lid_left,
    "lid_r": PP.lid_right,
    "fork_l": PP.fork,
    "fork_r": PP.fork,
    "arm": PP.arm,
    "wheel_fl": PP.wheel,
    "wheel_rl": PP.wheel,
    "wheel_fr": PP.wheel_right,
    "wheel_rr": PP.wheel_right,
}


def build(part="tub"):
    if part not in _BUILDERS:
        raise ValueError(f"unknown part: {part}")
    return _BUILDERS[part]()

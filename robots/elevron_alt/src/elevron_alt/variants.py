"""Deliberate departures from the original Elevron 3.0 Alt, all OFF by default (parity first). Override with the env
var ELEVRON_VARIANTS="name,..." (or "all") before import, or set_variants(...) at run time.

One switch runs the other way: `step_forks` restores the STEP's fork underside, which reaches 2.25 mm below the
wheels' floor (the TPU forks are preloaded onto the floor). As drawn the forks, not the wheels, would carry the robot
(contain.wheel_ground), so the default build stops them FORK_FLOOR_CLR above the floor."""
import os

NAMES = ("step_forks",)
VARIANTS = {n: False for n in NAMES}


def set_variants(*names):
    names = NAMES if names == ("all",) else names
    bad = [n for n in names if n not in VARIANTS]
    if bad:
        raise KeyError(f"unknown variant {bad}; known: {NAMES}")
    for n in VARIANTS:
        VARIANTS[n] = n in names


def variant(name):
    return VARIANTS[name]


set_variants(*[t.strip() for t in os.environ.get("ELEVRON_VARIANTS", "").split(",") if t.strip()])

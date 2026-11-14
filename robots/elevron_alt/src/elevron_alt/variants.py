"""Deliberate departures from the original Elevron 3.0 Alt, all OFF by default (parity first). Override with the env
var ELEVRON_VARIANTS="name,..." (or "all") before import, or set_variants(...) at run time.

`clip_forks` stops the forks FORK_FLOOR_CLR above the floor. As drawn in the STEP (the default) the TPU fork tips reach
2.25 mm below the wheels' floor (preloaded onto it); the side pods carry a cited contain.wheel_ground waiver for that.

One switch runs the other way: `step_cross_bolt`: the STEP threads the M3 cross bolt 2.5 mm into the TPU pod tongue (2.6 pilot), short of the
1.5 d a thread needs not to strip (fastener.engagement), so the default build holds it in a thin nut captive in the
module prong (the STEP prong has a plain 3.2 hole) with the tongue as a shear pin."""
import os

NAMES = ("clip_forks", "step_cross_bolt")
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

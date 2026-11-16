"""RF placement (`rf.*`, G6).

WHY: a receiver buried under a carbon or aluminium plate, or seated next to a
brushed motor / ESC, glitches and reboots mid-fight and it looks like a radio
failure. 2.4 GHz is blocked by conductive material; brushed motors and ESCs
are PWM switching noise sources. The receiver's antenna exits its top face, so
the check judges (a) the distance from every receiver to every motor / ESC and
(b) whether conductive material sits over the receiver top within the antenna's
first stretch - the exit path.
"""

from __future__ import annotations

import numpy as np

from ..finding import WARNING, fail, ok
from ._physics import part

G = "rf"
NOISE_KINDS = ("motor", "weapon_motor", "esc")
MIN_NOISE_MM = 20.0  # under this the noise coupling is severe
WARN_NOISE_MM = 30.0  # under this it is a risk worth a warning
OVERHEAD_MM = 15.0  # conductive material this close above the receiver smothers the antenna exit
CONDUCTIVE_METALS = ("aluminium", "steel", "titanium", "brass", "copper", "cf_plate", "fr4")


def _conductive(ctx, b):
    """True when the body is metal / carbon-filled (2.4 GHz does not pass through it)."""
    if b.fastener:
        return True
    p = part(ctx, b)
    if p is None:
        return False
    if p.kind in ("motor", "weapon_motor", "battery"):
        return True  # a metal can / cell pouch over the receiver is as bad as a plate
    m = p.material or ""
    return m in CONDUCTIVE_METALS or m.endswith("_cf") or "carbon" in m


def _receivers(ctx):
    out = []
    for b in ctx.world.bodies:
        if b.fastener or b.kind != "receiver":
            continue
        out.append(b)
    return out


def run(ctx):
    rxs = _receivers(ctx)
    out = []
    if not rxs:
        ctx.not_checked.append("RF placement: no receiver in the spec (distance to noise sources and antenna exit not judged)")
        return out
    conductive = [b for b in ctx.world.bodies if not b.is_wire and _conductive(ctx, b)]
    for rx in rxs:
        c = np.asarray(rx.center, float)
        rx_top = float(rx.aabb[1][2])
        # (a) distance to every noise source (brushed motors, ESCs)
        worst_d, worst_id = None, None
        for b in ctx.world.bodies:
            if b.fastener or b.kind not in NOISE_KINDS or b is rx:
                continue
            d = float(np.linalg.norm(np.asarray(b.center, float) - c))
            if worst_d is None or d < worst_d:
                worst_d, worst_id = d, b.id
        if worst_d is not None:
            ctx.metrics[f"rf_min_noise_mm.{rx.id}"] = round(worst_d, 1)
        # (b) the antenna exit path: conductive material over the receiver top
        blocker = None
        for b in conductive:
            if b is rx:
                continue
            lo, hi = np.asarray(b.aabb, float)
            if lo[0] <= c[0] <= hi[0] and lo[1] <= c[1] <= hi[1] and lo[2] < rx_top + OVERHEAD_MM and hi[2] > rx_top + 1.0:
                blocker = b
                break
        if worst_d is not None and worst_d < MIN_NOISE_MM:
            out.append(fail("rf.noise_proximity", G, WARNING, "Receiver sits on a noise source",
                            f"`{rx.id}` is {worst_d:.1f} mm from `{worst_id}` ({', '.join(sorted({b.kind for b in ctx.world.bodies if b.kind in NOISE_KINDS}))} "
                            f"noise); under {MIN_NOISE_MM:.0f} mm the PWM switching noise swamps 2.4 GHz.")
                       .on(rx.id, worst_id)
                       .fix("Move the receiver to the far corner of the chassis from the motors/ESCs, or shield and twist the motor wires."))
        elif worst_d is not None and worst_d < WARN_NOISE_MM:
            out.append(fail("rf.noise_proximity", G, WARNING, "Receiver close to a noise source",
                            f"`{rx.id}` is {worst_d:.1f} mm from `{worst_id}`; margin is thin (aim for {WARN_NOISE_MM:.0f} mm+ from motors and ESCs).")
                       .on(rx.id, worst_id)
                       .fix("A few more millimetres of separation, or route the motor wires along the other wall, buys clean radio."))
        if blocker is not None:
            bp = part(ctx, blocker)
            what = (bp.material if bp is not None and bp.material else blocker.kind)
            out.append(fail("rf.antenna_blocked", G, WARNING, "Antenna exit path blocked by conductive material",
                            f"`{blocker.id}` (conductive: {what}) "
                            f"sits over `{rx.id}`'s top face within {OVERHEAD_MM:.0f} mm - the antenna radiates from there and 2.4 GHz "
                            f"does not pass through metal or carbon.")
                       .on(rx.id, blocker.id)
                       .fix("Cut a window in the plate, use plastic there, or stand the antenna out through a tube before the plate."))
        if not out:
            noise = f", nearest noise source {worst_id} at {worst_d:.1f} mm" if worst_id is not None else ", no motor/ESC in the spec"
            out.append(ok("rf.ok", G, "Receiver clear of noise with an open antenna exit",
                          f"`{rx.id}`{noise}, nothing conductive within {OVERHEAD_MM:.0f} mm above its top face."))
    return out

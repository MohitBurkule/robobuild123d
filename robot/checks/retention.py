"""Axial retention of rotating parts (`retention.axial`).

WHY: a part that spins (disc, spider, spacer, wheel, hub) must be held in both axial directions by hardware, not by the
weapon's own centrifugal grip or a pocket: a fastener head clamps one way and a thread (or nut, press fit, shaft
shoulder, fuse) the other. A rotating part that no clamping fastener passes through, and that declares no other hold,
walks off its shaft in a hit.
"""

from __future__ import annotations

from ..finding import BLOCKER, fail, note, ok
from ._review import x
from .kinematics import SPIN_KINDS, declared_rot, is_spin_weapon
from .support import HOLD_METHODS

G = "retention"
CARRIER_KINDS = {"motor", "weapon_motor", "bearing", "fastener", "nut", "structure"}  # held by their own checks / are the frame


def spins(spec, p):
    return p.kind not in CARRIER_KINDS and (p.kind in SPIN_KINDS or is_spin_weapon(spec, p) or bool(declared_rot(p)))


DECLARED = "declared"   # prefix of holds taken on trust (no geometric check): they need a reason and are listed


def captured_by(r, p):
    """Why `p` is held both ways, or None: a threading/clamping fastener, or a declared positive hold. A declared hold
    (part `retained` + `retained_reason`, or a hold connection with a `reason`) is not checked geometrically, so one
    without a reason does not count."""
    if p.retained is not None and str(p.retained) in HOLD_METHODS and str(x(p, "retained_reason", "") or "").strip():
        return f"{DECLARED} `{p.retained}`: {x(p, 'retained_reason')}"
    if p.fused_with:
        return f"fused with `{p.fused_with}`"
    nuts = {q.id for q in r.spec.parts if q.kind == "nut"}
    for f in r.spec.fasteners:
        if f.threads_into == p.id:
            return f"thread of `{f.id}`"
        if p.id in (f.through or []) and (f.threads_into or any(n in (f.through or []) for n in nuts)):
            return f"clamped by `{f.id}` (head one side, {'thread in ' + f.threads_into if f.threads_into else 'nut'} the other)"
    for c in r.spec.connections:
        if c.method in HOLD_METHODS and p.id in (c.a, c.b) and str(c.reason or "").strip():
            return f"{DECLARED} `{c.method}` to `{c.b if c.a == p.id else c.a}`: {c.reason}"
    return None


def run(ctx):
    r = ctx.r
    out, good, trusted = [], 0, []
    for p in r.spec.parts:
        if not spins(r.spec, p):
            continue
        why = captured_by(r, p)
        if why is None:
            out.append(fail("retention.axial", G, BLOCKER, "Rotating part not held in both axial directions",
                            f"`{p.id}` rotates but no fastener clamps or threads into it and it declares no reasoned press fit, pin, shaft or fuse hold.")
                       .on(p.id).fix("Pass a screw through it into a thread or nut, or declare the hold that captures it with a `reason`."))
        else:
            good += 1
            if why.startswith(DECLARED):
                trusted.append(f"`{p.id}` ({why})")
    if trusted:   # not a pass on geometry: list them for review
        out.append(note("retention.declared", G, "Axial holds taken on declaration (not checked geometrically)", "; ".join(trusted)))
    if good and not any(not f.passed for f in out):
        out.append(ok("retention.axial", G, "Rotating parts held both ways", f"{good} rotating parts each captured (head one way, thread/nut/hold the other)."))
    return out

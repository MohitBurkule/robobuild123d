"""fastener.drive_recess: every screw head carries a tool recess (hex socket). A head that is a plain disc cannot be
driven, and renders like a button. Probed on the modelled solid: a ray down the screw axis, from the head side, must
meet material at least `min_depth_mm` (default 0.3) below the head's outermost plane, i.e. the head has a pocket.
"""

from __future__ import annotations

import numpy as np

from ..finding import BLOCKER, fail, ok
from ._review import params

G = "drive_recess"
DEFAULTS = {"min_depth_mm": 0.3}


def recess_depth(mesh, at, axis):
    """Depth (mm) of the pocket on the head side of a screw mesh, 0.0 when the head top is flat. `axis` points tip-ward."""
    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    top = float((mesh.vertices @ a).min())
    p = np.asarray(at, float)
    start = p + a * (top - float(p @ a) - 2.0)
    loc, _, _ = mesh.ray.intersects_location([start], [a])
    if len(loc) == 0:
        return 0.0
    first = float((np.asarray(loc) @ a).min())
    return first - top


def run(ctx):
    r, w = ctx.r, ctx.world
    need = float(params(r.spec, "drive_recess", DEFAULTS)["min_depth_mm"])
    out, n = [], 0
    for f in r.spec.fasteners:
        b = w.body(f.id)
        if b is None:
            continue
        d = recess_depth(b.mesh, f.at, f.dir)
        if d < need:
            out.append(fail("fastener.drive_recess", G, BLOCKER, "Screw head has no tool recess",
                            f"`{f.id}` ({f.designation}) head is a plain disc (recess {d:.2f} mm deep, need {need:.1f}): no hex socket to drive it.")
                       .on(f.id).expect(f">= {need:.1f} mm recess", f"{d:.2f} mm")
                       .fix("Set the fastener `head` (countersunk / button / cap) so the screw model carries its hex socket."))
        else:
            n += 1
    if n:
        out.append(ok("fastener.drive_recess", G, "Screw heads carry a tool recess", f"{n} screw head(s) have a drive pocket."))
    return out

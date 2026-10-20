"""fastener.drive_recess: every screw head carries a tool recess (hex socket). A head that is a plain disc cannot be
driven, and renders like a button. Probed on the modelled solid: a ray down the screw axis, from the head side, must
meet material at least `min_depth_mm` (default 0.3) below the head's outermost plane, i.e. the head has a pocket.
"""

from __future__ import annotations

import numpy as np

from .. import catalog
from ..cad import fastener_catalog as fc
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


def expected_depth(f):
    """Catalog socket depth for this screw (DIN 7991 csk: M3 2.0 AF x 1.9), at most the head height + 0.5 into the shank."""
    dl = catalog.parse_designation(f.designation)
    if not dl:
        return 0.0
    d = dl[0]
    head = "countersunk" if f.head == "countersunk" else f.head
    _, t = fc.drive_key(d, head)
    k = world_head_height(d, head)
    return min(t, k + 0.5)


def world_head_height(d, head):
    from .. import world
    if head == "countersunk":
        return world.csk_dims(d)[1]
    if head == "button":
        return world.button_dims(d)[1]
    return catalog.screw_dims(d)[1]


def run(ctx):
    r, w = ctx.r, ctx.world
    need = float(params(r.spec, "drive_recess", DEFAULTS)["min_depth_mm"])
    out, n = [], 0
    for f in r.spec.fasteners:
        b = w.body(f.id)
        if b is None:
            continue
        d = recess_depth(b.mesh, f.at, f.dir)
        want = max(need, 0.8 * expected_depth(f))
        if d < want:
            out.append(fail("fastener.drive_recess", G, BLOCKER, "Screw head has no tool recess",
                            f"`{f.id}` ({f.designation}) head is a plain disc (recess {d:.2f} mm deep, need {want:.1f}): no hex socket to drive it.")
                       .on(f.id).expect(f">= {want:.1f} mm recess", f"{d:.2f} mm")
                       .fix("Set the fastener `head` (countersunk / button / cap) so the screw model carries its hex socket."))
        else:
            n += 1
    if n:
        out.append(ok("fastener.drive_recess", G, "Screw heads carry a tool recess", f"{n} screw head(s) have a drive pocket."))
    return out

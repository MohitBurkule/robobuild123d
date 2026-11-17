"""Fight-sim readiness: what robot/fight needs per robot (spec `sim` block, robot/fight/profile.py) and that it is sane.

No physics runs here (cheap, inner tier). A spec with no `sim` block gets one warning: it can still fight, but forward,
drive speed, weapon speed, lifter stroke and danger arcs are guessed. A `sim` block that is present but wrong is a blocker.
"""

from __future__ import annotations

from ..finding import BLOCKER, WARNING, fail, note, ok

G = "fight"
SHAKE_G = 40.0  # a welded part must at least hold its own weight at this many g (drive bumps, wall hits)


def run(ctx):
    from ..fight import profile

    sp = ctx.r.spec
    out = []
    req = profile.requirements(sp)
    if req and req[0][0] == "sim":
        out.append(fail("fight.sim_block", G, WARNING, "No fight-sim description",
                        req[0][1] + ". Add a `sim` block (robot/docs/FIGHT.md)."))
    else:
        for k, why in req:
            out.append(fail(f"fight.{k}", G, BLOCKER, f"Fight sim: {k}", why))
        if not req:
            out.append(ok("fight.sim_block", G, "Fight-sim description complete", "forward, drive, weapon/lifter declared"))
    prof = profile.build(sp)
    mass_g = {}
    for b in ctx.world.bodies:
        if b.part_idx is not None and b.mesh is not None:
            try:
                mass_g[b.id] = float(b.mesh.volume) * 1.24e-3  # PLA estimate, g; only for the shake floor
            except Exception:  # noqa: BLE001
                pass
    weak = []
    for pid, n in prof.breakable.items():
        m = mass_g.get(pid)
        if m and n < m * 1e-3 * 9.81 * SHAKE_G:
            weak.append(f"{pid} {n:.0f} N < {m * 1e-3 * 9.81 * SHAKE_G:.0f} N")
    if weak:
        out.append(fail("fight.weld_floor", G, BLOCKER, "Breakable part would fall off by itself",
                        "break force below its own weight at %d g: %s" % (SHAKE_G, "; ".join(weak))))
    if prof.breakable:
        out.append(note("fight.welds", G, "Breakable parts and break forces",
                        ", ".join(f"{k} {v:.0f} N" for k, v in prof.breakable.items())
                        + (" (from fasteners; calibrate with robot/fight/radioss.py)" if "breakable" in prof.defaults else "")))
    return out

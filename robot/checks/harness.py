"""harness.*: the planned wiring harness (robot/wiring) judged as a builder would judge real wiring.

Runs robot.wiring.plan.build (typed terminals -> netlist -> bundled B-spline routes -> channels / tie points) and the
checks of robot/wiring/checks.py: netlist, route, clearance, rotating parts, fasteners, bend radius, exit axis, slack,
length, ampacity, connector fit, lid pinch, exposure to hits, retention. Needs no reference model.

Opt-in per robot until the package has field time: `"harness": {"enabled": true}` in the spec. Without it the group
only notes that it did not judge.
"""

from __future__ import annotations

from ..finding import WARNING, fail, note

G = "harness"


def run(ctx):
    from ..wiring import settings

    r = ctx.r
    if not settings.section(r.spec).get("enabled", settings.for_spec(r.spec).get("enabled", False)):
        ctx.not_checked.append("harness.*: the wiring harness is not planned (set `harness.enabled` in the spec)")
        return [note("harness.off", G, "Harness not judged", "The spec does not enable the wiring harness group.")]
    try:
        from ..wiring import checks, plan

        h, space = plan.build(r, ctx.world)
        found = checks.run(h, ctx.world, r, space, h.settings)
        ctx.metrics.update(checks.metrics(h))
    except Exception as e:  # noqa: BLE001 - a planner crash must not take the whole verify run down
        ctx.not_checked.append(f"harness.*: the planner failed ({type(e).__name__}: {e})")
        return [fail("harness.plan", G, WARNING, "Harness could not be planned",
                     f"The wiring planner stopped with {type(e).__name__}: {e}. Nothing in this group was judged.")]
    return found

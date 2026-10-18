"""Fastener orientation and service access from the shared disassembly graph (robot/analysis/disassembly.py).

* `disasm.cycle` (BLOCKER): the graph has a cycle, so nothing on it can ever be taken apart.
* `disasm.unreachable` (BLOCKER): a fastener cannot be freed (its dependency set contains a cycle).
* `disasm.service_depth` (WARNING): a serviceable part (battery, weapon, wheels, armour, plus any `serviceable: true`)
  needs more than N removals; N is `service.max_removals` in the spec (default 8).
* `disasm.elastic_stretch` (BLOCKER): an O-ring / elastic belt must stretch past its material limit to come off over the
  largest flange on its path. Elastic parts with a stretch path are not treated as trapped.
"""

from __future__ import annotations

import numpy as np

from ..analysis import disassembly as D
from ..finding import BLOCKER, WARNING, fail, ok
from . import tension

G = "disasm"
SERVICE_KINDS = {"battery", "weapon", "wheel", "armor", "armour"}
DEFAULT_MAX_REMOVALS = 8
# Install stretch limits (fraction) for elastic belts / O-rings by material.
INSTALL_STRAIN = {"nitrile": 0.5, "nbr": 0.5, "epdm": 0.6, "silicone": 0.8, "viton": 0.3, "fkm": 0.3, "polyurethane": 0.6,
                  "urethane": 0.6, "tpu": 0.3, "rubber": 0.5}
DEFAULT_STRAIN = 0.3


def _flange_r(b):
    e = np.sort(b.aabb[1] - b.aabb[0])
    return float(e[2]) / 2


def elastic(ctx, out):
    """Elastic parts that can be stretched off; returns their ids. Adds findings for those that cannot."""
    r, w = ctx.r, ctx.world
    free = set()
    for p in r.spec.parts:
        b = p.belt
        if b is None or (b.kind or "o_ring").lower() not in tension.ELASTIC:
            continue
        bodies = [w.body(x) for x in (b.pulleys or [])]
        if len(bodies) != 2 or any(x is None for x in bodies) or not b.length_mm:
            ctx.not_checked.append(f"disasm.elastic_stretch `{p.id}`: belt pulleys/length not declared")
            continue
        c = float(np.linalg.norm(bodies[0].center - bodies[1].center))
        L = float(b.length_mm)
        r_ = [tension.pulley_radius(x) for x in bodies]
        need = min(tension.loop_length(c, _flange_r(bodies[0]), r_[1]), tension.loop_length(c, r_[0], _flange_r(bodies[1])))
        strain = need / L - 1
        mat = (p.material or "nitrile").lower()
        lim = next((v for k, v in INSTALL_STRAIN.items() if k in mat), DEFAULT_STRAIN)
        ctx.metrics[f"install_stretch.{p.id}"] = strain
        if strain > lim:
            out.append(fail("disasm.elastic_stretch", G, BLOCKER, "Belt cannot be stretched over its flange",
                            f"`{p.id}` must stretch {strain * 100:.0f} % to pass the largest flange on its path; {mat} allows {lim * 100:.0f} %.")
                       .on(p.id, *b.pulleys).fix("Lower the flange, make one pulley removable, or use a longer belt with a tensioner."))
        else:
            free.add(p.id)
            out.append(ok("disasm.elastic_stretch", G, "Belt can be stretched on and off",
                          f"`{p.id}` needs {strain * 100:.0f} % stretch over the flange ({mat} limit {lim * 100:.0f} %)."))
    return free


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    free = elastic(ctx, out)
    captive = {k: v for k, v in ctx.captive.items() if k not in free}
    if not ctx.captive and not (ctx.opts.only is None or "interference" in ctx.opts.only):
        ctx.not_checked.append("disasm: interference group not run, trapped-part edges missing from the graph")
    g, unknown = D.build(r, w, captive)
    for fid in unknown:
        ctx.not_checked.append(f"disasm: driver line of `{fid}` not evaluated")
    cyc = g.cycles()
    on_cycle = set()
    for comp in cyc:
        on_cycle |= set(comp)
        edges = "; ".join(f"{g.before[n][m]}" for n in comp for m in g.before[n] if m in comp)
        out.append(fail("disasm.cycle", G, BLOCKER, "Disassembly deadlock",
                        f"{', '.join(f'`{x}`' for x in comp)} each need another removed first: {edges}.").on(*comp)
                   .fix("Turn a screw so its driver line exits through an open face, or split the trapping part."))
    for f in r.spec.fasteners:
        if f.id in g.nodes and (g.deps(f.id) | {f.id}) & on_cycle:
            out.append(fail("disasm.unreachable", G, BLOCKER, "Screw can never be reached",
                            f"`{f.id}` depends on parts locked in a disassembly cycle.").on(f.id))
    nmax = int((r.spec.raw.get("service") or {}).get("max_removals", DEFAULT_MAX_REMOVALS))
    ctx.metrics["disasm.removals"] = {}
    for p in r.spec.parts:
        if not (p.kind in SERVICE_KINDS or p._extra.get("serviceable")) or p.id in on_cycle:
            continue
        seq = g.order(p.id)
        if seq is None:
            out.append(fail("disasm.unreachable", G, BLOCKER, "Serviceable part can never be removed", f"`{p.id}` sits behind a disassembly cycle.").on(p.id))
            continue
        ctx.metrics["disasm.removals"][p.id] = len(seq)
        if len(seq) > nmax:
            out.append(fail("disasm.service_depth", G, WARNING, "Serviceable part is buried",
                            f"`{p.id}` needs {len(seq)} removals (limit {nmax}): {', '.join(seq)}.").on(p.id)
                       .fix("Give it its own hatch or move the screws that hold it to an outer face."))
    if not any(not x.passed for x in out):
        out.append(ok("disasm.graph", G, "Disassembly graph is acyclic and serviceable",
                      f"{len(g.nodes)} nodes; every screw is reachable; serviceable parts within {nmax} removals "
                      f"({', '.join(f'{k}:{v}' for k, v in ctx.metrics['disasm.removals'].items())})."))
    return out

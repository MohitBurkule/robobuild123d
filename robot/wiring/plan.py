"""The harness pipeline: one call turns a resolved robot into its wiring (terminals, netlist, routes, features).

Nothing is stored: a part swap or a moved device changes the terminals, and the harness is planned again from them.
"""

from __future__ import annotations

from . import channels, devices, field, netlist, router, settings, solids
from .model import Harness

ENABLED = "enabled"   # spec `harness.enabled` / settings key: the robot opts in to the harness group gating its verdict


def enabled(spec) -> bool:
    """True when the spec asks for the harness to be planned and judged (`"harness": {"enabled": true}`)."""
    return bool(settings.section(spec).get(ENABLED, settings.for_spec(spec).get(ENABLED, False)))


def bare(world):
    """`world` without the wire / connector bodies of an earlier routing pass (wires never route round themselves)."""
    from ..world import World

    w = World([b for b in world.bodies if not _is_harness_body(b)], world.joints)
    w.plan = getattr(world, "plan", {})
    return w


def _is_harness_body(b) -> bool:
    return b.is_wire or b.id.startswith(solids.CONNECTOR_PREFIX)


def build(r, world, cfg: dict | None = None, space=None):
    """Plan the whole harness of resolved robot `r` in `world`. Returns (Harness, FreeSpace)."""
    cfg = cfg or settings.for_spec(r.spec)
    world = bare(world)
    terms = devices.world_terminals(r, world, cfg)
    nl = netlist.build(r, terms, cfg)
    space = space or field.FreeSpace.from_world(world, r, cfg)
    paths, bundles = router.route(nl, terms, space, cfg)
    h = Harness(netlist=nl, terminals=terms, paths=paths, bundles=bundles, settings=cfg)
    h.channels, h.ties = channels.derive(h, space, r, cfg)
    h.connectors = channels.place_connectors(h, cfg)
    h.length_mm = float(sum(p.length_mm for p in paths.values()))
    h.mass_g = solids.mass_g(h)
    return h, space


def world_with_harness(r, world, cfg: dict | None = None):
    """`world` with its wires replaced by the planned harness (coloured round wires + connector bodies), for renders
    and export. Returns (World, Harness)."""
    cfg = cfg or settings.for_spec(r.spec)
    base = bare(world)
    h, _ = build(r, base, cfg)
    return solids.add_to_world(base, h, cfg), h


def chassis_cuts(r, world, part_id: str, cfg: dict | None = None) -> list:
    """Shape trees (part local frame) of the channels and tie slots the harness wants cut into chassis part `part_id`:
    a part builder subtracts them, so the tub's cable features follow the routes instead of being drawn by hand."""
    h, _ = build(r, world, cfg)
    return channels.cuts_for(h, part_id, bare(world))

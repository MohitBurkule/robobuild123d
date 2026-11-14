"""Scythe: 150 g horizontal undercutter bar spinner (AWS 2025). UNTESTED: never built, run, rendered or verified.

Small per-part modules, explicit imports (no shared namespace, unlike revron/__init__.py). build(part) is the
single geometry entry point the spec's {"type": "model", "file": "src/build_scythe.py", "params": {"part": ...}} uses.
"""
from . import params, bar, weapon_hub, tub, drive, skids, panels, assembly, variants

PARTS = {
    "tub": tub.tub,
    "bar": bar.bar,
    "weapon_hub": weapon_hub.hub,
    "top_panel": panels.top_panel,
    "skid_foot": skids.foot,
    "skid_dome": skids.dome,
}


def build(part="assembly", angle_deg=0.0):
    """One custom part in its own frame (bar, hub) or world frame (tub, panels, skids); 'assembly' = compound."""
    if part == "assembly":
        return assembly.compound(angle_deg)
    if part not in PARTS:
        raise KeyError(f"unknown Scythe part `{part}`; one of {sorted(PARTS)} or 'assembly'")
    return PARTS[part]()

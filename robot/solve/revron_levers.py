"""Revron mass levers. UNTESTED. Names are master params; settings with these names do not exist yet in
robots/revron/src/revron/settings.py -> hook needed (add Setting(..., "float") per lever and read it in the part)."""
from .mass import Lever

LEVERS = [
    Lever("chassis.wall_t", 1.2, 2.4, 1.6, priority=0, step=0.4, doc="tub wall, 0.4 nozzle lines"),
    Lever("chassis.infill", 0.15, 1.0, 0.4, priority=1, step=0.05, doc="print infill fraction (non-structural regions)"),
    Lever("armour.top_t", 1.0, 2.5, 1.5, priority=2, step=0.5, doc="top panel thickness"),
    Lever("weapon.disc_t", 3.0, 6.0, 4.0, priority=3, step=0.5, doc="disc sheet stock thickness (weapon energy, keep last)"),
]


def mass_fn(values: dict) -> float:
    """Build the Revron spec with lever values and return total mass g (robot.checks mass group, metrics mass_total_g).

    Lever names must be real Revron settings; until they are added to revron/settings.py, SCHEMA.design raises
    DesignError naming the unknown setting. UNTESTED."""
    import sys
    from pathlib import Path
    from robot.checks import Options, verify
    from robot.spec import Spec
    root = Path(__file__).resolve().parents[2] / "robots" / "revron"
    src = str(root / "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    from revron.settings import build_revron
    data = build_revron({k: str(v) for k, v in values.items()})
    rep = verify(Spec(data, root), Options(only=["mass"]))
    return float(rep.metrics["mass_total_g"])

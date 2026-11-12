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
    """Build Revron with lever values and return total mass g (via design + robot.measure). Hook point; UNTESTED."""
    from robot.design import use
    from revron.settings import SCHEMA  # noqa: assumes schema export name
    from robot import measure
    d = SCHEMA.design({k: str(v) for k, v in values.items()})
    with use(d):
        return measure.total_mass_g()  # TODO wire to real mass sum (metrics mass_total_g)

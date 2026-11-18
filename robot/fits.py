"""Named fits with process compensation (D2).

WHY: an FDM hole prints 0.1 to 0.2 mm tight (elephant foot, shrinkage, first-layer
squash), so a bore modelled at the bearing's nominal size will not take the
bearing. A named fit says what the hole is FOR; this module says what CAD
diameter that means for the declared hole process, and whether a measured (or
modelled) diameter is in band.

cad_diameter(fit, nominal, hole_process, printer=None) is the number a CAD hole
should get; check(fit, nominal, measured, hole_process) returns (ok, lo, hi, why).
Processes: "fdm" (default, the tight one), "sla", "cnc", "cast", "none" (the
nominal size, for bought-in parts and reference models).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fit:
    name: str
    kind: str  # press | running | clearance | thread
    delta_mm: float  # added to the nominal bore for an FDM hole
    note: str = ""


# name -> (FDM, SLA, CNC) deltas; a name missing from a process column falls back to FDM's.
FITS: dict[str, dict] = {
    "bearing_press": Fit("bearing_press", "press", 0.10, "bearing pressed in; printed bore slightly over nominal so the press is firm, not destructive"),
    "bearing_slip": Fit("bearing_slip", "running", 0.20, "bearing slips out by hand for swaps"),
    "shaft_running": Fit("shaft_running", "running", 0.25, "shaft turns freely in the printed bore"),
    "shaft_press": Fit("shaft_press", "press", 0.05, "shaft pressed in and stays (wheels on D-shafts, pins)"),
    "screw_clear_tight": Fit("screw_clear_tight", "clearance", 0.20, "screw clearance hole, head side, minimal play"),
    "screw_clear": Fit("screw_clear", "clearance", 0.30, "standard M-series clearance hole"),
    "screw_clear_loose": Fit("screw_clear_loose", "clearance", 0.45, "clearance hole with play for alignment"),
    "self_tap_plastic": Fit("self_tap_plastic", "thread", -0.35, "pilot hole for a screw tapping into the plastic (smaller than the screw)"),
    "heatset_m2": Fit("heatset_m2", "thread", -0.10, "heat-set insert bore (knurled inserts bite the walls)"),
    "heatset_m2.5": Fit("heatset_m2.5", "thread", -0.10, "heat-set insert bore"),
    "heatset_m3": Fit("heatset_m3", "thread", -0.10, "heat-set insert bore (3.2 mm nominal for a standard M3 insert)"),
    "axle_dflat_n20": Fit("axle_dflat_n20", "running", 0.20, "N20 D-shaft bore; the flat needs the play to seat"),
    "pocket_snug": Fit("pocket_snug", "clearance", 0.15, "part pushed in by hand, no rattle"),
    "pocket_loose": Fit("pocket_loose", "clearance", 0.40, "part drops in with room for tape/foam"),
}

PROCESS_DELTA = {"fdm": 1.0, "sla": 0.5, "cnc": 0.0, "cast": 0.75, "none": 0.0}
BAND_MM = {"press": 0.06, "running": 0.10, "clearance": 0.12, "thread": 0.08}


def get(name: str) -> Fit | None:
    return FITS.get(name)


def cad_diameter(name: str, nominal: float, hole_process: str = "fdm") -> float:
    """The CAD bore diameter for `nominal` under `hole_process` (unknown process -> no compensation)."""
    f = FITS.get(name)
    if f is None:
        raise KeyError(f"unknown fit {name!r}; known: {sorted(FITS)}")
    scale = PROCESS_DELTA.get(hole_process)
    if scale is None:
        raise KeyError(f"unknown hole process {hole_process!r}; known: {sorted(PROCESS_DELTA)}")
    return round(nominal + f.delta_mm * scale, 3)


def band(name: str, nominal: float, hole_process: str = "fdm") -> tuple:
    """(lo, hi) acceptable measured diameters for the fit."""
    d = cad_diameter(name, nominal, hole_process)
    f = FITS[name]
    b = BAND_MM[f.kind] * PROCESS_DELTA.get(hole_process, 1.0)
    return round(d - b, 3), round(d + b, 3)


def check(name: str, nominal: float, measured: float, hole_process: str = "fdm") -> tuple:
    """(ok, lo, hi, why) for a measured (or modelled) hole diameter."""
    if name not in FITS:
        return False, None, None, f"unknown fit {name!r}"
    lo, hi = band(name, nominal, hole_process)
    okd = lo <= measured <= hi
    why = (f"in band" if okd else
           f"{'tight' if measured < lo else 'loose'}: measured {measured:.2f}, band [{lo:.2f}, {hi:.2f}] "
           f"for {name} at {nominal:.2f} nominal ({hole_process})")
    return okd, lo, hi, why

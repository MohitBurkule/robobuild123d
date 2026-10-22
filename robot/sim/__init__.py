"""Physics simulation (MuJoCo): gravity, drop/tilt tests, props and robot-vs-robot interaction.

    from robot import sim
    model = sim.load("robots/wedge_2wd/spec.json")
    s = sim.Sim(); s.add_robot(model); s.compile(); s.step(1.0)
"""

from .engine import Sim
from .model import RobotModel, extract, load
from .scene import Placement, Scene

__all__ = ["Sim", "Scene", "Placement", "RobotModel", "extract", "load"]

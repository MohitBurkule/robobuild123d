# Physics simulation (`robot.sim`, MuJoCo)

`pip install -e .[sim]`. Pure-numpy extraction (`sim/model.py`) turns a verified robot into rigid groups (chassis, each
wheel, the weapon) with per-part mass (same source as the verifier's mass check), COM and inertia from the meshes, and
hinges from the spec's `joint` + `rotates_with`. Un-jointed wheels spin about their symmetry axis. `sim/engine.py` builds the
MuJoCo model (convex-hull collision, torque-limited velocity servos, own-robot geoms never collide). SI units.

```python
from robot import sim
from robot.sim import scenarios, viz
a = sim.load("robots/revron/spec.json")
s = sim.Sim(sim.Scene().box("block", (.03,.03,.03), (.15, 0, .03), mass=.03))
n = s.add_robot(a, sim.Placement("A", (0, -.2)))
s.compile().step(0.5); s.drive(n, 60, 60); s.spin_weapon(n, 300); s.step(1.0)
viz.save(s, "out.png", view="top")          # software render, no GL needed
scenarios.drop_test(a, 0.3)                   # peak g, settled tilt
scenarios.ram_test(a, b)                      # robot vs robot
```
CLI: `python -m robot.sim robots/revron/spec.json [drop|drive|ramp|push|all]`.
Scene: gravity, floor friction, walled arena, boxes/spheres (static or dynamic), ramps, any number of robots.
Limits: fasteners and wires are not simulated (mass slightly low); hulls are convex; no motor curves yet (flat torque cap).

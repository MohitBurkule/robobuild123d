"""Power switch: a slide switch in a slot against the outer wall, open through the roof so a finger (no tool) reaches
it, recessed 1.2 mm under the roof so the robot's own motion or a hit cannot flip it."""

from __future__ import annotations

from .plan import Pocket

SIZE = (11.8, 3.8, 4.0)
RECESS = 1.2


def add_switch(plan, x, y, rot_z=0.0, cid="power_switch"):
    f = plan.frame
    z = f.zt - RECESS - SIZE[2] / 2
    plan.part(id=cid, kind="switch", catalog="switch_slide_12x4", at=[x, y, z], rot=[0.0, 0.0, float(rot_z)],
              label="ON/OFF", marked=True, tool_free=True, retained="adhesive")
    sx, sy = (SIZE[1], SIZE[0]) if int(round(rot_z)) % 180 == 90 else (SIZE[0], SIZE[1])
    pk = Pocket(cid, x - sx / 2 - 0.3, x + sx / 2 + 0.3, y - sy / 2 - 0.3, y + sy / 2 + 0.3,
                f.zb + f.floor, f.zt + 0.5, housing=1.4, wire_through=True)
    pk.notches.append((pk.x0, pk.x1, pk.y0, pk.y1, pk.z0, pk.z1))  # the slot under the switch carries its wires
    plan.pockets.append(pk)
    return z

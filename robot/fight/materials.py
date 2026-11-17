"""Contact properties per material, from published data (not tuned to make fights look good).

mu: dry sliding friction against steel (the arena floor is steel sheet). Sources: Engineering Toolbox friction tables
(steel-steel 0.5-0.8 dry, Al-steel 0.47, Ti-steel ~0.4), FDM polymer-on-steel tribology (PLA 0.3-0.4, PETG ~0.4,
PC 0.31-0.35: Bustillos et al. 2018, Hanon et al. 2021), TPU/urethane and silicone rubber tyres on steel 0.8-1.2.
e: coefficient of restitution for an impact on a hard surface (ball-drop data: PLA ~0.4-0.5, PC ~0.5, TPU ~0.2-0.3,
rubber ~0.3-0.6, Al ~0.5, steel ~0.6).
Robot-vs-robot contacts use MuJoCo's default (larger of the two mu); the floor is set below every material so the part's
own value is what touches it.
"""

from __future__ import annotations

import math

TABLE = {
    "pla": (0.35, 0.45), "pla_st": (0.35, 0.45), "petg": (0.40, 0.40), "pc": (0.33, 0.50), "abs": (0.35, 0.45),
    "nylon": (0.30, 0.45), "tpu": (0.80, 0.25), "rubber": (1.00, 0.35), "silicone": (1.10, 0.35),
    "aluminium": (0.47, 0.50), "aluminum": (0.47, 0.50), "steel": (0.55, 0.60), "hardox": (0.55, 0.60),
    "titanium": (0.40, 0.55), "carbon": (0.30, 0.40), "brass": (0.45, 0.50),
}
DEFAULT = (0.40, 0.45)  # unknown printed part
KIND_DEFAULT = {"wheel": "rubber", "tyre": "rubber"}
FLOOR_MU = 0.05  # below every material: MuJoCo takes the larger mu of a pair


def props(material: str | None, kind: str = ""):
    m = (material or KIND_DEFAULT.get(kind, "") or "").lower()
    return TABLE.get(m, DEFAULT)


def damp_ratio(e: float) -> float:
    """MuJoCo contact damping ratio giving restitution e for a linear spring-damper contact."""
    e = min(max(e, 1e-3), 0.99)
    ln = math.log(e)
    return -ln / math.sqrt(math.pi ** 2 + ln ** 2)

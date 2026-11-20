"""Arena presets from real UK antweight events (sources in robot/docs/FIGHT.md, "Arenas").

Every preset is a steel-topped platform with its top at z=0; anything off the platform (an open edge, a ditch, a pit
hole) drops to a lower floor. A robot whose centre of mass goes below `out_z` has touched the pit / out-of-arena floor:
that is an immediate loss in AWS, Beetle Champs and CCRL rules, bouncing back does not count.

- closed:        old sim box, 1.2 m walled + roof, no way out (fights go to the judges).
- aws2025:       AWS 2025 rules: 1 m square recommended (750 mm minimum), at least one unwalled 200 mm gap
                 ("pit / drop-off"). Here: 400 mm drop-off slot mid east edge + 200 mm square pit, 300 mm walls + lid.
- aws_classic:   older AWS raised platform: 762 mm (30") square, 50% of the perimeter unwalled (south + east edges).
- beetle_champs: Bristol-style 1.2 m walled box with an out-of-the-arena (OOTA) gap and a 250 mm pit whose cover
                 drops after 30 s (pit "switched on" partway through).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import mujoco
import numpy as np

EDGES = ("n", "s", "e", "w")


@dataclass
class Arena:
    name: str
    half: float  # platform half size (m)
    wall_h: float = 0.3
    roof: bool = True  # polycarbonate lid at wall height: thrown robots stay in, the gaps are slots under it
    gaps: dict = field(default_factory=dict)  # edge -> [(a0, a1)] unwalled spans along that edge (m, -half..half)
    pits: list = field(default_factory=list)  # [(cx, cy, hx, hy, open_at_s)] holes in the platform
    drop_z: float = -0.1  # pit / ditch floor
    out_z: float = -0.03  # COM below this = touched the floor outside the arena
    seams: bool = False
    spawn: float = 0.3  # robots start at x = +-spawn

    def open_pits(self, t):
        return [p for p in self.pits if t >= p[4]]

    def on_platform(self, xy, t=1e9):
        x, y = float(xy[0]), float(xy[1])
        if abs(x) > self.half or abs(y) > self.half:
            return False
        return not any(abs(x - cx) < hx and abs(y - cy) < hy for cx, cy, hx, hy, _ in self.open_pits(t))

    def hazards(self, t):
        """Points a pusher wants to shove the opponent onto: open pit centres and just past each open edge span."""
        pts = [np.array([cx, cy]) for cx, cy, *_ in self.open_pits(t)]
        h = self.half + 0.06
        for e, spans in self.gaps.items():
            for a0, a1 in spans:
                m = (a0 + a1) / 2
                pts.append(np.array({"n": (m, h), "s": (m, -h), "e": (h, m), "w": (-h, m)}[e]))
        return pts

    def build(self, w):
        """Add platform tiles, walls and pit covers to a world body. Returns the pit cover geom names."""
        xs = sorted({-self.half, self.half, *[c for cx, _, hx, _, _ in self.pits for c in (cx - hx, cx + hx)]})
        ys = sorted({-self.half, self.half, *[c for _, cy, _, hy, _ in self.pits for c in (cy - hy, cy + hy)]})
        th = 0.01
        k = 0
        covers = []
        for x0, x1 in zip(xs, xs[1:]):
            for y0, y1 in zip(ys, ys[1:]):
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                pit = next((i for i, (px, py, hx, hy, _) in enumerate(self.pits) if abs(cx - px) < hx and abs(cy - py) < hy), None)
                if pit is not None and self.pits[pit][4] <= 0:
                    continue
                name = f"floor_t{k}" if pit is None else f"floor_cover{pit}_{k}"
                w.add_geom(name=name, type=mujoco.mjtGeom.mjGEOM_BOX, size=[(x1 - x0) / 2, (y1 - y0) / 2, th],
                           pos=[cx, cy, -th], rgba=[0.3, 0.32, 0.35, 1] if pit is None else [0.55, 0.45, 0.1, 1])
                if pit is not None:
                    covers.append((name, self.pits[pit][4]))
                k += 1
        for i, (cx, cy, hx, hy, _) in enumerate(self.pits):  # pit walls (dark) so the hole reads in the video
            w.add_geom(name=f"pitfloor{i}", type=mujoco.mjtGeom.mjGEOM_BOX, size=[hx, hy, 0.002],
                       pos=[cx, cy, self.drop_z + 0.002], rgba=[0.08, 0.08, 0.08, 1])
        t, h, wh = 0.01, self.half, self.wall_h
        for e in EDGES:
            spans = sorted(self.gaps.get(e, []))
            cuts, a = [], -h - 2 * t
            for a0, a1 in spans:
                cuts.append((a, a0))
                a = a1
            cuts.append((a, h + 2 * t))
            for j, (a0, a1) in enumerate(cuts):
                if a1 - a0 < 1e-3:
                    continue
                m, L = (a0 + a1) / 2, (a1 - a0) / 2
                pos, size = {"n": ((m, h + t), (L, t)), "s": ((m, -h - t), (L, t)),
                             "e": ((h + t, m), (t, L)), "w": ((-h - t, m), (t, L))}[e]
                w.add_geom(name=f"wall_{e}{j}", type=mujoco.mjtGeom.mjGEOM_BOX, size=[*size, wh / 2],
                           pos=[*pos, wh / 2], rgba=[0.7, 0.8, 0.9, 0.25])
        if self.roof:
            w.add_geom(name="roof", type=mujoco.mjtGeom.mjGEOM_BOX, size=[h + 2 * t, h + 2 * t, 0.005],
                       pos=[0, 0, wh + 0.005], rgba=[0.6, 0.7, 0.8, 0.0])
        return covers


PRESETS = {
    "closed": None,
    "aws2025": Arena("aws2025", 0.5, gaps={"e": [(-0.2, 0.2)]}, pits=[(0.0, 0.32, 0.1, 0.1, 0.0)]),
    "aws_classic": Arena("aws_classic", 0.381, gaps={"s": [(-0.381, 0.381)], "e": [(-0.381, 0.381)]}, spawn=0.2),
    "beetle_champs": Arena("beetle_champs", 0.6, gaps={"n": [(-0.15, 0.15)]},
                           pits=[(0.0, -0.38, 0.125, 0.125, 30.0)]),
}


def get(name):
    if name is None or isinstance(name, Arena):
        return name
    if name not in PRESETS:
        raise KeyError(f"unknown arena {name!r}; one of {sorted(PRESETS)}")
    return PRESETS[name]

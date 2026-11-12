"""ElectronicsBay: battery / receiver / ESC bays packed in one row (UNTESTED: written without running).

Wraps robot.cad.bay: each catalogue id becomes a `derive_bay`, the set is laid out with `pack_row`, and the result
gives the host the cut solids, the retention sites as Mounts and the packed keep-in envelope. A set that does not fit
`host_max_size` raises `bay.BayUnfit` (a verdict, not a crash).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from build123d import Box, Location, Pos

from robot import catalog
from robot.cad import bay as bay_lib
from robot.modules.base import ModuleResult, Mount


@dataclass
class ElectronicsBay:
    name: str = "electronics_bay"
    part_ids: tuple = ("battery", "rx", "esc")      # catalogue ids, packed in this order
    axis: str = "x"
    insert_dir: str = "+z"                          # parts drop in from above (open face = -z ... see bay.py frames)
    wall: float = bay_lib.DEFAULT_WALL
    gap: float = 0.0
    share_walls: bool = True
    host_max_size: tuple | None = None
    bays: list = field(default_factory=list, init=False)
    packing: object = field(default=None, init=False)

    def derive(self):
        bays = [bay_lib.derive_bay(catalog.find(pid), wall=self.wall, insert_dir=self.insert_dir) for pid in self.part_ids]
        self.packing = bay_lib.pack_row(bays, axis=self.axis, gap=self.gap, share_walls=self.share_walls,
                                        host_max_size=self.host_max_size)
        self.bays = self.packing.placed(bays)
        return self.bays

    @property
    def envelope_size(self):
        if self.packing is None:
            self.derive()
        return self.packing.size

    def build(self) -> ModuleResult:
        self.derive()
        res = ModuleResult(self.name, bom=list(self.part_ids))
        for b in self.bays:
            res.parts[f"cut_{b.part_id}"] = b.cut_solid()
            for i, site in enumerate(b.retention.sites):
                kind = "screw" if site.kind == "screw" else "rigid"
                res.mounts[f"{b.part_id}_{site.kind}_{i}"] = Mount(
                    f"{b.part_id}_{site.kind}_{i}", b.placement * Location(site.at), kind, site.thread)
        size = self.packing.size
        res.envelope = Pos(*(s / 2 for s in size)) * Box(*size)
        return res

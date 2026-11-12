"""Shared interface for robot part modules (UNTESTED: written without running).

Every module is a small dataclass: catalogue part ids + a few named masters. `build()` returns a `ModuleResult`
with the solids, named joints (build123d RigidJoint) and the keep-in envelope the host must provide.
Relations, not numbers: every dimension derives from catalogue props or masters.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from build123d import Box, Location, Part


@dataclass
class Mount:
    """A named interface point: where another module attaches (frame in module coords)."""
    name: str
    location: Location
    kind: str = "rigid"          # rigid | revolute | screw
    screw: str | None = None     # fastener catalogue id when kind == screw


@dataclass
class ModuleResult:
    name: str
    parts: dict[str, Part] = field(default_factory=dict)       # name -> solid (module frame)
    mounts: dict[str, Mount] = field(default_factory=dict)
    envelope: Box | None = None                               # keep-in the host must leave clear
    bom: list[str] = field(default_factory=list)              # catalogue ids used
    mass_g: float = 0.0


class Module(Protocol):
    name: str

    def build(self) -> ModuleResult: ...


def place(result: ModuleResult, at: Location) -> ModuleResult:
    """Move every solid + mount of a result into host frame."""
    return ModuleResult(
        name=result.name,
        parts={k: at * p for k, p in result.parts.items()},
        mounts={k: Mount(m.name, at * m.location, m.kind, m.screw) for k, m in result.mounts.items()},
        envelope=(at * result.envelope) if result.envelope is not None else None,
        bom=list(result.bom),
        mass_g=result.mass_g,
    )

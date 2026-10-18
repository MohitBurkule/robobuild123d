"""Weapon modules. `prepare` runs before the layout (reserves space, adds fixed parts and keep-outs); `add` runs after
(parts that depend on the placed electronics). One module per buildable weapon type."""

from __future__ import annotations

MODULES = {}


def module(name):
    def deco(cls):
        MODULES[name] = cls
        return cls
    return deco


def prepare(plan, h, g):
    m = MODULES.get(h.weapon)
    if m:
        m.prepare(plan, h, g)


def add(plan, h, g):
    m = MODULES.get(h.weapon)
    if m:
        m.add(plan, h, g)

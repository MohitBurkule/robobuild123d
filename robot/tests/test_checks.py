"""Port of crates/robot/tests/checks.rs. Mutation tests: each check must catch the mistake it exists for."""

import importlib.util

import pytest

from robot import spec
from robot.checks import Options, verify


def _has(group):
    return importlib.util.find_spec(f"robot.checks.{group}") is not None


def part(id, kind, shape, at, material, process, **kw):
    return {"id": id, "kind": kind, "shape": shape, "at": list(at), "material": material, "process": process, **kw}


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def failed(rep, fid):
    return any(not f.passed and f.id == fid for f in rep.findings)


def run(d, only=None):
    return verify(spec.Spec(d), Options(fast=True, only=only))


mfg_needed = pytest.mark.skipif(not _has("mfg"), reason="robot.checks.mfg not ported yet")


@mfg_needed
def test_thin_printed_wall_is_flagged():
    thin = {"type": "subtract", "base": box(30, 30, 10), "cut": [box(29.2, 29.2, 12)]}
    d = {"name": "thin", "parts": [part("shell", "structure", thin, (0, 0, 0), "petg", "fdm")]}
    assert failed(run(d, ["mfg"]), "mfg.thin_wall")


@mfg_needed
def test_thick_printed_wall_is_fine():
    ok = {"type": "subtract", "base": box(30, 30, 10), "cut": [box(27, 27, 12)]}
    d = {"name": "ok", "parts": [part("shell", "structure", ok, (0, 0, 0), "petg", "fdm")]}
    assert not failed(run(d, ["mfg"]), "mfg.thin_wall")


def screw_spec(with_overhang):
    parts = [part("base", "structure", box(30, 30, 6), (0, 0, 0), "nylon", "fdm")]
    if with_overhang:
        parts.append(part("cap", "structure", box(30, 30, 3), (0, 0, 9), "nylon", "fdm"))
    f = {"id": "s1", "designation": "M2x6", "at": [0, 0, 3], "dir": [0, 0, -1], "through": ["base"],
         "tool": "hex1.5", "head": "socket"}
    return {"name": "screw", "parts": parts, "fasteners": [f]}


def test_screw_under_overhang_cannot_be_reached():
    assert failed(run(screw_spec(True), ["fasteners"]), "fastener.access")


def test_open_screw_can_be_reached():
    assert not failed(run(screw_spec(False), ["fasteners"]), "fastener.access")


def test_floating_part_is_flagged():
    d = {"name": "float", "parts": [part("base", "structure", box(30, 30, 6), (0, 0, 0), "nylon", "fdm"),
                                    part("lid", "armor", box(30, 30, 2), (0, 0, 12), "nylon", "fdm")]}
    assert failed(run(d, ["interference", "connections"]), "connection.floating")


def test_vertical_switch_is_flagged():
    sw = {"id": "sw", "kind": "switch", "catalog": "switch_slide_12x4", "at": [0, 0, 5], "tool_free": True, "marked": True,
          "actuation": [0, 0, 1]}
    d = {"name": "sw", "parts": [part("base", "structure", box(30, 30, 6), (0, 0, 0), "nylon", "fdm"), sw]}
    assert failed(run(d, ["legal"]), "switch.vertical_axis")


@mfg_needed
def test_cots_o_ring_is_not_a_thin_wall():
    """VERIFIER_ISSUES #5: a stock 1.0 mm O-ring (process cots, kind belt) has no made walls."""
    ring = {"type": "subtract", "base": {"type": "cylinder", "radius": 10, "height": 1.0}, "cut": [{"type": "cylinder", "radius": 9, "height": 2}]}
    d = {"name": "oring", "parts": [part("belt", "belt", ring, (0, 0, 0), "rubber", "cots")]}
    assert not failed(run(d, ["mfg"]), "mfg.thin_wall")

"""COTS sizes, snug fit, containment by role, disassembly graph and coverage: a bad and a good design per check id."""

import copy

from robot import spec
from robot.checks import Options, verify

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731
PLA = {"material": "pla", "process": "fdm"}


def pl(shape, at):
    return {"type": "place", "shape": shape, "at": list(at), "rot": [0, 0, 0]}


def cyl(r, h, at=(0, 0, 0), rot=(0, 0, 0)):
    return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": h}, "at": list(at), "rot": list(rot)}


def run(d, *groups):
    rep = verify(spec.Spec(copy.deepcopy(d)), Options(fast=True, only=list(groups)))
    return [f for f in rep.findings if f.group in groups]


def failed(fs, fid):
    return [f for f in fs if f.id == fid and not f.passed]


def passed(fs, fid):
    return [f for f in fs if f.id == fid and f.passed]


# ---- cots ----
def _bearing(label, r=4.0, h=2.5):
    return {"name": "t", "parts": [{"id": "b", "kind": "bearing", "label": label, "shape": cyl(r, h)}]}


def test_cots_unlisted_bearing():
    assert failed(run(_bearing("some bearing"), "cots"), "cots.unlisted")


def test_cots_bearing_dims_mismatch_and_good():
    assert failed(run(_bearing("MR85ZZ", r=5.0), "cots"), "cots.dims_mismatch")
    fs = run(_bearing("MR85ZZ 5x8x2.5"), "cots")
    assert passed(fs, "cots.listed") and not [f for f in fs if not f.passed]


def test_cots_catalog_dims_declared():
    d = {"name": "t", "parts": [{"id": "bat", "kind": "battery", "catalog": "lipo_2s_180", "dims": [40, 30, 20]}]}
    assert failed(run(d, "cots"), "cots.dims_mismatch")
    d["parts"][0].pop("dims")
    assert not failed(run(d, "cots"), "cots.dims_mismatch")


def test_cots_fastener_size():
    d = {"name": "t", "parts": [dict(id="blk", kind="structure", shape=BOX(20, 20, 10), **PLA)],
         "fasteners": [{"id": "s", "designation": "M2x7", "at": [0, 0, 5], "dir": [0, 0, -1], "through": ["blk"]}]}
    assert failed(run(d, "cots"), "cots.fastener_size")
    d["fasteners"][0]["designation"] = "M2x6"
    assert not failed(run(d, "cots"), "cots.fastener_size")


# ---- fit ----
def _pocket(cx, cy):
    return {"name": "t", "parts": [
        dict(id="tray", kind="structure", shape={"type": "subtract", "base": pl(BOX(40, 30, 10), (0, 0, 0)),
                                                  "cut": [pl(BOX(cx, cy, 10), (0, 0, 3))]}, **PLA),
        {"id": "rx", "kind": "receiver", "shape": BOX(20, 10, 6), "at": [0, 0, 1]}]}


def test_fit_snug():
    fs = run(_pocket(20.6, 10.6), "fit")
    assert passed(fs, "fit.snug") and not [f for f in fs if not f.passed]


def test_fit_loose():
    assert failed(run(_pocket(23, 13), "fit"), "fit.loose")


def test_fit_tight_and_interference():
    assert failed(run(_pocket(20.05, 10.05), "fit"), "fit.tight")
    assert failed(run(_pocket(19.4, 9.4), "fit"), "fit.interference")


# ---- contain ----
def _shell(esc_at=(0, 0, 0), slot=False, inverted=False, wheel_r=8.0):
    cuts = [pl(BOX(36, 36, 16), (0, 0, 0))]
    if slot:
        cuts.append(pl(BOX(4, 4, 10), (10, 10, 8)))
    return {"name": "t", "can_run_inverted": inverted, "parts": [
        dict(id="shell", kind="structure", shape={"type": "subtract", "base": BOX(40, 40, 20), "cut": cuts}, **PLA),
        {"id": "esc", "kind": "esc", "shape": BOX(10, 10, 4), "at": list(esc_at)},
        {"id": "sw", "kind": "switch", "shape": BOX(3, 3, 3), "at": [10, 10, 6.5]},
        dict(id="wheel", kind="wheel", shape=cyl(wheel_r, 4, rot=(0, 90, 0)), at=[23, 0, -3], **PLA)]}


def test_contain_electronics():
    assert failed(run(_shell(esc_at=(0, 0, 14)), "contain"), "contain.electronics_exposed")
    assert passed(run(_shell(), "contain"), "contain.electronics")


def test_contain_switch_access():
    assert failed(run(_shell(), "contain"), "contain.switch_access")
    assert passed(run(_shell(slot=True), "contain"), "contain.switch_access")


def test_contain_wheel_invert():
    assert failed(run(_shell(inverted=True), "contain"), "contain.wheel_invert")
    assert not failed(run(_shell(inverted=True, wheel_r=14.0), "contain"), "contain.wheel_invert")


# ---- disasm ----
def _deadlock(open_=False):
    d = {"name": "t", "parts": [
        dict(id="a", kind="structure", shape=pl(BOX(30, 30, 2), (0, 0, 1)), **PLA),
        dict(id="b", kind="plate", shape=pl(BOX(30, 30, 2), (0, 0, 9)), **PLA)],
        "fasteners": [
            {"id": "sa", "designation": "M2x6", "at": [5, 0, 2], "dir": [0, 0, -1], "through": ["a"], "tool": "hex1.5"},
            {"id": "sb", "designation": "M2x6", "at": [-5, 0, 8], "dir": [0, 0, 1], "through": ["b"], "tool": "hex1.5"}]}
    if open_:
        d["fasteners"][1].update(at=[-5, 0, 10], dir=[0, 0, -1])
    return d


def test_disasm_cycle():
    fs = run(_deadlock(), "disasm")
    assert failed(fs, "disasm.cycle") and failed(fs, "disasm.unreachable")
    assert passed(run(_deadlock(open_=True), "disasm"), "disasm.graph")


def test_disasm_service_depth():
    d = _deadlock(open_=True)
    d["parts"].append({"id": "bat", "kind": "battery", "shape": BOX(10, 10, 4), "at": [0, 0, 5], "retained": "tape"})
    d["fasteners"][0]["through"] = ["a"]
    d["fasteners"][1]["through"] = ["b", "bat"]
    d["fasteners"][1]["at"] = [0, 0, 10]
    d["service"] = {"max_removals": 0}
    assert failed(run(d, "disasm"), "disasm.service_depth")
    d["service"] = {"max_removals": 8}
    assert not failed(run(d, "disasm"), "disasm.service_depth")


def _belt(length, mat):
    return {"name": "t", "parts": [
        dict(id="p1", kind="pulley", shape=cyl(5, 4, rot=(0, 90, 0)), at=[0, 0, 0], **PLA),
        dict(id="p2", kind="pulley", shape=cyl(5, 4, rot=(0, 90, 0)), at=[0, 30, 0], **PLA),
        {"id": "o", "kind": "belt", "material": mat, "shape": BOX(1, 1, 1), "at": [3, 15, 6],
         "belt": {"pulleys": ["p1", "p2"], "kind": "o_ring", "length_mm": length}}]}


def test_disasm_elastic_stretch():
    assert failed(run(_belt(60, "viton"), "disasm"), "disasm.elastic_stretch")
    assert passed(run(_belt(85, "nitrile"), "disasm"), "disasm.elastic_stretch")


# ---- coverage ----
def test_coverage_uncovered_pair():
    d = {"name": "t", "parts": [dict(id="a", kind="structure", shape=pl(BOX(10, 10, 2), (0, 0, 1)), **PLA),
                                dict(id="b", kind="structure", shape=pl(BOX(10, 10, 2), (0, 0, 3)), **PLA)]}
    fs = run(d, "coverage")
    assert failed(fs, "coverage.uncovered") and "pair `a`/`b`" in failed(fs, "coverage.uncovered")[0].message
    d["connections"] = [{"a": "a", "b": "b", "method": "glue", "reason": "test"}]
    assert passed(run(d, "coverage"), "coverage.uncovered")


def test_coverage_missing_process():
    d = {"name": "t", "parts": [{"id": "a", "kind": "structure", "shape": BOX(10, 10, 2)}]}
    assert "no material" in failed(run(d, "coverage"), "coverage.uncovered")[0].message

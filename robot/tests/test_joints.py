"""Joint design defaults (checks/joints.py): one bad design that fails and one good design that passes per check id."""

import copy

import pytest

from robot import spec
from robot.checks import Options, verify

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731


def cyl(r, h, at, rot=(0, 0, 0)):
    return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": h}, "at": list(at), "rot": list(rot)}


def placed(shape, at):
    return {"type": "place", "shape": shape, "at": list(at), "rot": [0, 0, 0]}


SCREWS_XY = [(-12.0, 0.0), (12.0, 0.0)]


def top_plate(xy=SCREWS_XY, plate_hole=1.15, cb=None, boss_cut=None):
    """Good default: a 2 mm aluminium plate bolted down (along its assembly direction) onto a printed block, M2 into heat-set
    inserts, with a 1 mm locating spigot. Returns the spec dict."""
    pcuts = [cyl(plate_hole, 4, (x, y, 1)) for x, y in xy]
    if cb:
        pcuts += [cyl(cb[0], cb[1] * 2, (x, y, 2)) for x, y in xy]
    bcuts = [cyl(1.6, 3.0, (x, y, -1.5)) for x, y in xy] + [cyl(1.0, 6, (x, y, -3)) for x, y in xy]
    if boss_cut:
        bcuts += boss_cut
    parts = [
        {"id": "block", "kind": "structure", "material": "pla", "process": "fdm",
         "shape": {"type": "subtract", "base": placed(BOX(40, 30, 10), (0, 0, -5)), "cut": bcuts}},
        {"id": "plate", "kind": "plate", "material": "aluminium", "process": "laser",
         "shape": {"type": "subtract", "base": {"type": "union", "items": [placed(BOX(40, 30, 2), (0, 0, 1)),
                                                                          placed(BOX(4, 4, 1), (0, 8, -0.5))]},
                   "cut": pcuts}},
    ]
    # spigot pocket in the block so the plate registers (locating feature)
    parts[0]["shape"]["cut"].append(placed(BOX(4, 4, 1), (0, 8, -0.5)))
    fs = []
    for i, (x, y) in enumerate(xy):
        parts.append({"id": f"ins{i}", "kind": "insert", "catalog": "heatset_m2", "at": [x, y, -1.5]})
        fs.append({"id": f"s{i}", "designation": "M2x6", "at": [x, y, 2.0], "dir": [0, 0, -1], "through": ["plate"],
                   "threads_into": f"ins{i}", "tool": "hex1.5", "removable": True, "head": "countersunk"})
    return {"name": "t", "parts": parts, "fasteners": fs}


def side_panel(screw_dir="side", reason=None):
    """A 2 mm panel standing against the side of a block. Bad: screws come from the top through a tab under the panel."""
    parts = [
        {"id": "block", "kind": "structure", "material": "pla", "process": "fdm",
         "shape": {"type": "subtract",
                   "base": {"type": "union", "items": [placed(BOX(40, 40, 10), (0, 0, 0)), placed(BOX(2, 40, 4), (21, 0, -7))]},
                   "cut": [cyl(1.6, 3, (21, y, -6.5)) for y in (-12, 12)] if screw_dir == "top" else
                   [c for y in (-12, 12) for c in (cyl(1.6, 3, (18.5, y, 0), (0, 90, 0)), cyl(1.0, 8, (16, y, 0), (0, 90, 0)))]}},
        {"id": "panel", "kind": "plate", "material": "aluminium", "process": "laser",
         "shape": {"type": "subtract", "base": placed(BOX(2, 40, 10), (21, 0, 0)),
                   "cut": [cyl(1.15, 12, (21, y, 0)) for y in (-12, 12)] if screw_dir == "top" else
                   [cyl(1.15, 4, (21, y, 0), (0, 90, 0)) for y in (-12, 12)]}},
    ]
    fs = []
    for i, y in enumerate((-12, 12)):
        if screw_dir == "top":
            parts.append({"id": f"ins{i}", "kind": "insert", "catalog": "heatset_m2", "at": [21, y, -6.5]})
            f = {"at": [21, y, 5], "dir": [0, 0, -1], "designation": "M2x12"}
        else:
            parts.append({"id": f"ins{i}", "kind": "insert", "catalog": "heatset_m2", "at": [18.5, y, 0], "rot": [0, 90, 0]})
            f = {"at": [22, y, 0], "dir": [-1, 0, 0], "designation": "M2x6"}
        f.update({"id": f"s{i}", "through": ["panel"], "threads_into": f"ins{i}", "tool": "hex1.5", "removable": True,
                  "head": "countersunk"})
        if reason:
            f["reason"] = reason
        fs.append(f)
    return {"name": "t", "parts": parts, "fasteners": fs,
            "connections": [{"a": "panel", "b": "block", "method": "screw", "reason": "panel located on a lip", "mechanical_key": True}]}


def run(d, groups=("joints",), deep=False):
    return verify(spec.Spec(d), Options(only=list(groups), deep=deep, fast=True))


def mod(d, fn):
    d = copy.deepcopy(d)
    fn(d)
    return d


def _set_fast(key, val, idx=None):
    def f(d):
        for i, x in enumerate(d["fasteners"]):
            if idx is None or i == idx:
                x[key] = val
    return f


GOOD = top_plate()


def _single(d):
    d["fasteners"] = d["fasteners"][:1]


def _bunched(d):
    pass


CASES = {
    # id: (bad spec, good spec)
    "joint.axis_vs_interface": (side_panel("top"), side_panel("side")),
    "joint.clearance_hole": (top_plate(plate_hole=0.9), GOOD),
    "joint.counterbore": (mod(top_plate(cb=(1.6, 1.0)), _set_fast("at", None)), GOOD),
    "joint.single_fastener": (mod(GOOD, _single), GOOD),
    "joint.bolt_spread": (top_plate(xy=[(-2.0, 0.0), (2.0, 0.0)]), GOOD),
    "joint.bolt_symmetry": (top_plate(xy=[(14.0, -8.0), (18.0, 8.0)]), GOOD),
    "joint.head_proud": (mod(GOOD, _set_fast("head", "socket")), GOOD),
    "joint.standard_length": (mod(GOOD, _set_fast("designation", "M2x7")), GOOD),
}


def _fix_counterbore(d):
    for i, f in enumerate(d["fasteners"]):
        f["at"] = [SCREWS_XY[i][0], SCREWS_XY[i][1], 1.5]
        f["head"] = "socket"


CASES["joint.counterbore"] = (mod(top_plate(cb=(1.6, 1.0)), _fix_counterbore), GOOD)


def _lift(dz, ln="M2x6"):
    def f(d):
        d["parts"][1]["at"] = [0, 0, dz]
        for x in d["fasteners"]:
            x["at"][2] += dz
            x["designation"] = ln
    return f


def _no_spigot(d):
    d["parts"][1]["shape"]["base"]["items"] = d["parts"][1]["shape"]["base"]["items"][:1]
    d["parts"][0]["shape"]["cut"] = d["parts"][0]["shape"]["cut"][:-1]


def _parallel(d):
    d["fasteners"][0].update(at=[-24.0, 0.0, 0.0], dir=[1, 0, 0])


def _selftap(designation="M2x6", removable=True):
    def f(d):
        for x in d["fasteners"]:
            x.update(threads_into="block", designation=designation, removable=removable)
    return f


def _edge(d):
    for x in d["fasteners"]:
        x["threads_into"] = "block"
        x["at"][0] = 19.0 if x["at"][0] > 0 else -19.0


def _nut(trapped):
    def f(d):
        d["parts"] = [p for p in d["parts"] if not p["id"].startswith("ins")]
        for i, x in enumerate(d["fasteners"]):
            z = -5.0 if trapped else -10.8
            d["parts"].append({"id": f"nut{i}", "kind": "nut", "catalog": "nut_m2", "at": [x["at"][0], x["at"][1], z]})
            if trapped:
                d["parts"][0]["shape"]["cut"].append(cyl(2.1, 1.7, (x["at"][0], x["at"][1], z)))
            d["parts"][0]["shape"]["cut"].append(cyl(1.0, 12, (x["at"][0], x["at"][1], -5)))
            x.update(threads_into=f"nut{i}", designation="M2x12" if not trapped else "M2x8")
    return f


def _tpu_plate(d):
    d["parts"][1].update(material="tpu", process="fdm")
    for x in d["fasteners"]:
        x["head"] = "socket"


def _ground_screw(d):
    d["fasteners"].append({"id": "s9", "designation": "M2x6", "at": [0.0, -10.0, -10.0], "dir": [0, 0, 1], "through": ["block"],
                           "threads_into": "plate", "tool": "hex1.5", "head": "socket"})


def _bracket(kind):
    def f(d):
        d["parts"].append({"id": "bracket", "kind": kind, "material": "pla", "process": "fdm",
                           "shape": placed(BOX(8, 8, 2), (-12, 0, 12))})
    return f


def _sizes(d):
    for i, ds in enumerate(("M1.6x4", "M2.5x6", "M3x8")):
        d["fasteners"].append({"id": f"x{i}", "designation": ds, "at": [0, -10 - i, 40], "through": []})


def _variety(d):
    for i, ds in enumerate(("M2x3", "M2x4", "M2x8", "M2x10", "M2x12")):
        d["fasteners"].append({"id": f"x{i}", "designation": ds, "at": [0, -10 - i, 40], "through": []})


CASES.update({
    "joint.no_contact": (mod(GOOD, _lift(6.0, "M2x14")), GOOD),
    "joint.through_contact": (mod(GOOD, _lift(0.6)), GOOD),
    "joint.parallel_interface": (mod(GOOD, _parallel), GOOD),
    "joint.no_locator": (mod(GOOD, _no_spigot), GOOD),
    "joint.selftap_removable": (mod(GOOD, _selftap()), mod(GOOD, _selftap(removable=False))),
    "joint.layer_tension": (mod(GOOD, _selftap()), GOOD),
    "joint.plastic_engagement": (mod(GOOD, _selftap("M2x3")), mod(GOOD, _selftap("M2x8"))),
    "joint.thin_wall": (mod(GOOD, _edge), mod(GOOD, _selftap("M2x8"))),
    "joint.insert_boss": (top_plate(xy=[(-18.5, 0.0), (18.5, 0.0)]), GOOD),
    "joint.insert_length": (mod(GOOD, _set_fast("designation", "M2.5x6")), GOOD),
    "joint.loose_nut": (mod(GOOD, _nut(False)), mod(GOOD, _nut(True))),
    "joint.head_bearing": (mod(GOOD, _tpu_plate), GOOD),
    "joint.head_ground": (mod(GOOD, _ground_screw), GOOD),
    "joint.service_access": (mod(GOOD, _bracket("structure")), mod(GOOD, _bracket("lid"))),
    "joint.screw_sizes": (mod(GOOD, _sizes), GOOD),
    "joint.screw_variety": (mod(GOOD, _variety), GOOD),
})


def _lipped(d):
    """Block grows a top lip over the panel: the panel can now only slide on sideways, yet the screws come from the top."""
    blk = d["parts"][0]["shape"]
    blk["base"]["items"].append(placed(BOX(2, 40, 2), (21, 0, 6)))
    blk["cut"] += [cyl(1.15, 3, (21, y, 6)) for y in (-12, 12)]
    for f in d["fasteners"]:
        f.update(at=[21.0, f["at"][1], 7.0], designation="M2x14", head="socket")   # head on the lip (no countersink cut there)


def test_assembly_dir():
    rb = run(mod(side_panel("top"), _lipped), ("assembly", "joints"), deep=True)
    assert rb.failed("joint.assembly_dir"), [(f.id, f.message) for f in rb.findings if not f.passed]
    good = side_panel("side")
    for f in good["fasteners"]:
        f["head"] = "socket"   # the panel has plain holes: a countersunk head would now be modelled inside it
    rg = run(good, ("assembly", "joints"), deep=True)
    assert not rg.failed("joint.assembly_dir") and not any("assembly direction" in n for n in rg.not_checked)


@pytest.mark.parametrize("fid", sorted(CASES))
def test_bad_and_good(fid):
    bad, good = CASES[fid]
    rb = run(bad)
    assert rb.failed(fid), [(f.id, f.message) for f in rb.findings if not f.passed]
    rg = run(good)
    assert not rg.failed(fid), rg.get(fid).message


def test_good_plate_is_clean():
    rep = run(GOOD)
    bad = [(f.id, f.message) for f in rep.findings if not f.passed]
    assert not bad and rep.get("joint.ok").passed


def test_axis_reason_accepts_off_axis():
    rep = run(side_panel("top", reason="shear pin through the tab"))
    assert not rep.failed("joint.axis_vs_interface") and rep.get("joint.axis_reason").passed

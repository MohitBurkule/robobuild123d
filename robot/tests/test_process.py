"""Process-aware manufacturability (checks/process.py) on the exact B-rep."""

from robot import spec
from robot.checks import Options, verify


def _rep(parts):
    return verify(spec.Spec({"name": "t", "parts": parts}), Options(only=["process"], deep=False, fast=True))


def _fails(rep, pid=None):
    return [f for f in rep.findings if f.group == "process" and not f.passed and (pid is None or pid in f.parts)]


def _cyl(r, h, at=(0, 0, 0), rot=(0, 0, 0)):
    return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": h}, "at": list(at), "rot": list(rot)}


def _box(sx, sy, sz, at):
    return {"type": "place", "shape": {"type": "box", "size": [sx, sy, sz]}, "at": list(at)}


FLAT_DISC = {"type": "subtract", "base": _cyl(40, 3),
             "cut": [_cyl(4, 5)] + [_cyl(3, 5, (x, y, 0)) for x, y in ((20, 0), (-20, 0), (0, 20), (0, -20))]}
BAD_DISC = {"type": "union", "items": [FLAT_DISC, _box(8, 6, 6, (36, 0, 3))]}  # 3D tooth bump proud of the face


def _disc(shape, process="laser", material="steel", **kw):
    return dict({"id": "disc", "kind": "plate", "material": material, "process": process, "shape": shape}, **kw)


def test_flat_laser_disc_passes():
    rep = _rep([_disc(FLAT_DISC)])
    assert not _fails(rep), [f.message for f in _fails(rep)]
    assert rep.get("process.ok").passed


def test_disc_with_3d_tooth_fails():
    f = _fails(_rep([_disc(BAD_DISC)]))
    assert any(x.id == "process.geometry" and x.severity == "blocker" for x in f)


def test_non_stock_gauge_and_small_hole():
    bad = {"type": "subtract", "base": _cyl(40, 3.3), "cut": [_cyl(1.0, 5, (20, 0, 0))]}
    ids = {x.id for x in _fails(_rep([_disc(bad)]))}
    assert "mfg.stock" in ids and "process.geometry" in ids


def _bent(r_in, t=1.0, w=20.0, flange=15.0):
    tube = {"type": "revolve", "profile": [[r_in, 0], [r_in + t, 0], [r_in + t, w], [r_in, w]], "angle": 90}
    return {"type": "union", "items": [
        tube,
        _box(t, flange, w, (r_in + t / 2, -flange / 2, w / 2)),
        _box(flange, t, w, (-flange / 2, r_in + t / 2, w / 2)),
    ]}


def test_bent_plate_radius():
    good = _rep([{"id": "b", "kind": "bracket", "material": "aluminium", "process": "sheet_bent", "shape": _bent(1.5)}])
    assert not _fails(good), [f.message for f in _fails(good)]
    tight = _fails(_rep([{"id": "b", "kind": "bracket", "material": "aluminium", "process": "sheet_bent", "shape": _bent(0.5)}]))
    assert any("bend radius" in x.message for x in tight)


def test_turned_shaft_with_flat():
    shaft = {"type": "subtract", "base": _cyl(2, 30), "cut": [_box(2, 6, 10, (2.6, 0, 10))]}
    p = {"id": "s", "kind": "shaft", "material": "steel", "process": "turned", "shape": shaft}
    assert any("flat" in x.message for x in _fails(_rep([p])))
    ok = _rep([dict(p, secondary_ops=["flat"])])
    assert not _fails(ok), [f.message for f in _fails(ok)]


def test_undeclared_and_printed_spinner():
    f = _fails(_rep([{"id": "p", "kind": "plate", "material": "steel", "shape": FLAT_DISC}]))
    assert [x.id for x in f] == ["process.undeclared"]
    w = _rep([{"id": "disc", "kind": "weapon", "material": "pla", "process": "fdm", "print_orientation": "+z",
               "shape": FLAT_DISC}])
    assert any(x.id == "process.weapon_printed" for x in _fails(w))


def test_fdm_needs_orientation():
    p = {"id": "c", "kind": "structure", "material": "pla", "process": "fdm", "shape": _box(10, 10, 10, (0, 0, 0))}
    assert any(x.id == "process.print_orientation" for x in _fails(_rep([p])))
    assert not _fails(_rep([dict(p, print_orientation="+z")]))


def test_cots_rod_stock():
    p = {"id": "pin", "kind": "pin", "material": "steel", "process": "bought", "shape": _cyl(1.5, 17)}
    assert not _fails(_rep([p]))
    assert any(x.id == "mfg.stock" for x in _fails(_rep([dict(p, shape=_cyl(1.6, 17))])))


def test_milled_sharp_pocket_corner():
    pocket = {"type": "subtract", "base": _box(20, 20, 10, (0, 0, 0)), "cut": [_box(10, 10, 6, (0, 0, 3))]}
    f = _fails(_rep([{"id": "m", "kind": "structure", "material": "aluminium", "process": "milled", "shape": pocket}]))
    assert any("sharp internal" in x.message for x in f)


def test_dxf_export(tmp_path):
    from robot import world
    from robot.checks.process import export_dxf

    r = world.resolve(spec.Spec({"name": "t", "parts": [_disc(FLAT_DISC), dict(_disc(BAD_DISC), id="bad")]}), fast=True)
    files, fails = export_dxf(r, tmp_path)
    assert files == ["dxf/disc.dxf"] and (tmp_path / "dxf/disc.dxf").stat().st_size > 0
    assert [p for p, _ in fails] == ["bad"]


def _flat(shape, tmp_path):
    from robot import world
    from robot.checks import process

    r = world.resolve(spec.Spec({"name": "t", "parts": [
        {"id": "b", "kind": "bracket", "material": "aluminium", "process": "sheet_bent", "shape": shape}]}), fast=True)
    files, fails = process.export_dxf(r, tmp_path)
    return r, files, fails


def test_bent_plate_flat_pattern_dxf(tmp_path):
    import math

    import ezdxf

    from robot.checks import process

    shape = {"type": "subtract", "base": _bent(1.5), "cut": [_cyl(2, 5, (-8, 1, 10), (90, 0, 0))]}
    r, files, fails = _flat(shape, tmp_path)
    assert not fails and files == ["dxf/b.dxf"], fails
    flat, bends = process.unfold_sheet_bent(r.parts[0].geom.solid, 1.0)
    ba = math.pi / 2 * (1.5 + process.K_FACTOR * 1.0)
    size = sorted([flat.bounding_box().size.X, flat.bounding_box().size.Y])
    assert abs(size[0] - 20) < 1e-3 and abs(size[1] - (30 + ba)) < 1e-3
    assert abs(flat.area - (20 * (30 + ba) - math.pi * 4)) < 0.05  # the flange hole survives
    assert len(bends) == 1
    doc = ezdxf.readfile(str(tmp_path / "dxf" / "b.dxf"))
    layers = {e.dxf.layer for e in doc.modelspace()}
    assert layers == {"cut", "bend"}
    assert sum(1 for e in doc.modelspace() if e.dxf.layer == "bend") == 1


def test_u_channel_two_bends(tmp_path):
    import math

    from robot.checks import process

    t, ri, w = 1.0, 1.5, 20.0
    tube = lambda ang, at: {"type": "place", "shape": {"type": "revolve", "angle": 90, "profile":
                            [[ri, 0], [ri + t, 0], [ri + t, w], [ri, w]]}, "at": at, "rot": [0, 0, ang]}
    # web along x at y = -(ri+t)..-ri, two 90 degree bends up into flanges along +y
    shape = {"type": "union", "items": [
        _box(20, t, w, (0, -(ri + t / 2), w / 2)),
        tube(180, (-10, 0, 0)), tube(270, (10, 0, 0)),
        _box(t, 12, w, (-10 - ri - t / 2, 6, w / 2)), _box(t, 12, w, (10 + ri + t / 2, 6, w / 2))]}
    r, files, fails = _flat(shape, tmp_path)
    assert not fails, fails
    flat, bends = process.unfold_sheet_bent(r.parts[0].geom.solid, t)
    ba = math.pi / 2 * (ri + process.K_FACTOR * t)
    assert len(bends) == 2
    assert abs(max(flat.bounding_box().size.X, flat.bounding_box().size.Y) - (20 + 24 + 2 * ba)) < 1e-3

"""Build-plate export (robot/plate.py): orientation, packing, bed-fit errors, files."""

import json

import pytest
import trimesh


def box(w, d, h):
    return trimesh.creation.box((w, d, h))


def test_orient_puts_up_axis_down_and_lifts_to_zero():
    m = box(20, 10, 5)
    o = __import__("robot.plate", fromlist=["orient"]).orient(m, "+x")
    size = o.bounds[1] - o.bounds[0]
    assert abs(size[0] - 5) < 1e-6  # the +x dimension becomes the print height
    assert abs(o.bounds[0][2]) < 1e-6


def test_pack_shelves_by_footprint():
    from robot.plate import pack

    meshes = [("big", box(60, 40, 5)), ("small", box(10, 10, 5)), ("wide", box(50, 20, 5))]
    plates, positioned = pack(meshes, bed_mm=(220, 220), gap=4)
    assert len(plates) == 1 and len(plates[0]) == 3
    xs = {pid: at for pid, (_p, x, y) in positioned.items() for at in [x]}
    assert positioned["small"][1] > 0  # the small box is placed after a bigger one


def test_pack_splits_when_bed_full():
    from robot.plate import pack

    meshes = [(f"p{i}", box(100, 110, 5)) for i in range(4)]
    plates, positioned = pack(meshes, bed_mm=(220, 220), gap=4)
    assert len(plates) == 2


def test_part_too_big_for_bed_raises():
    from robot.plate import pack

    with pytest.raises(ValueError):
        pack([("huge", box(300, 90, 5))], bed_mm=(220, 220))


def test_write_outputs(tmp_path):
    from robot.plate import write

    info = write([("tub", box(60, 40, 10), "+z"), ("lid", box(50, 30, 4), None)], tmp_path,
                 printer="ender3", filament="pla")
    assert info["printer"] == "ender3" and len(info["plates"]) >= 1
    names = {p.name for p in tmp_path.iterdir()}
    assert {"tub.stl", "lid.stl", "plates.json"} <= names
    assert any(n.startswith("plate_") for n in names)
    data = json.loads((tmp_path / "plates.json").read_text())
    assert set(data["positioned"]) == {"tub", "lid"}


def test_bed_fit_error_names_the_printer(tmp_path):
    from robot.plate import write

    with pytest.raises(ValueError, match="ender3"):
        write([("big", box(300, 100, 5), None)], tmp_path, printer="ender3")

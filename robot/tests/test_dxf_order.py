"""DXF sheet/turned-part order pack (robot/dxf_order.py): stock snapping, rows, files."""

import json
from types import SimpleNamespace

import trimesh

from robot import dxf_order


def _part(pid, process="laser", material="steel", **kw):
    kw.setdefault("catalog", None)
    return SimpleNamespace(id=pid, process=process, material=material, **kw)


def _spec(*parts):
    return SimpleNamespace(parts=list(parts))


def test_sheet_row_snaps_thickness_to_stock():
    r = dxf_order.rows(_spec(_part("plate", thickness_mm=1.4)))
    row = r["sheet"][0]
    assert row["stock_thickness_mm"] == 1.5 and "not stock" in row["note"]


def test_sheet_row_exact_stock_has_no_note():
    r = dxf_order.rows(_spec(_part("plate", thickness_mm=2.0)))
    assert r["sheet"][0]["note"] is None


def test_thickness_undeclared_flagged():
    r = dxf_order.rows(_spec(_part("plate")))
    assert r["sheet"][0]["note"] == "thickness undeclared" and r["sheet"][0]["stock_thickness_mm"] is None


def test_mesh_gives_blank_size_and_dxf():
    m = trimesh.creation.box((40, 20, 2))
    r = dxf_order.rows(_spec(_part("plate", thickness_mm=2.0)), meshes={"plate": m})
    row = r["sheet"][0]
    assert row["blank_x_mm"] == 46 and row["blank_y_mm"] == 26  # profile + 3 mm margin
    assert row["dxf"] == "dxf/plate.dxf"


def test_turned_row_snaps_rod_and_adds_facing():
    r = dxf_order.rows(_spec(_part("axle", process="turned", material="steel",
                                   params={"od_mm": 2.6, "len_mm": 28})))
    row = r["turned"][0]
    assert row["stock_dia_mm"] == 3.0 and row["stock_len_mm"] == 30.0
    assert row["note"] is None


def test_turned_part_bigger_than_stock_is_flagged():
    r = dxf_order.rows(_spec(_part("hub", process="turned", material="steel",
                                   params={"od_mm": 40, "len_mm": 10})))
    assert r["turned"][0]["stock_dia_mm"] is None and "no steel rod stock" in r["turned"][0]["note"]


def test_turned_size_from_mesh_when_undeclared():
    m = trimesh.creation.cylinder(radius=2, height=20)
    r = dxf_order.rows(_spec(_part("pin", process="turned", material="steel")), meshes={"pin": m})
    row = r["turned"][0]
    assert row["stock_dia_mm"] == 4.0 and row["stock_len_mm"] == 22.0


def test_spec_spellings_the_alias_table_misses():
    r = dxf_order.rows(_spec(_part("skirt", process="cnc_sheet", material="titanium_gr5", thickness_mm=0.8),
                               _part("hub", process="lathe", material="al7075", params={"od_mm": 5, "len_mm": 8})))
    assert [x["id"] for x in r["sheet"]] == ["skirt"] and r["sheet"][0]["stock_thickness_mm"] == 0.8
    assert r["turned"][0]["stock_dia_mm"] == 5.0


def test_printed_and_catalog_parts_excluded():
    r = dxf_order.rows(_spec(_part("tub", process="fdm"), _part("bolt", process="cots", catalog="m3")))
    assert r["sheet"] == [] and r["turned"] == []


def test_write_outputs_dxf_and_csvs(tmp_path):
    import ezdxf

    m = trimesh.creation.box((40, 20, 2))
    spec = _spec(_part("plate", thickness_mm=2.0), _part("axle", process="turned", material="steel",
                                                         params={"od_mm": 3, "len_mm": 30}))
    data = dxf_order.write(spec, tmp_path, meshes={"plate": m})
    doc = ezdxf.readfile(str(tmp_path / "dxf" / "plate.dxf"))
    assert "CUT" in doc.layers and len(doc.modelspace().query("LWPOLYLINE")) >= 1
    sheet_csv = (tmp_path / "order_sheet.csv").read_text()
    assert "plate" in sheet_csv and "stock_thickness_mm" in sheet_csv
    assert "axle" in (tmp_path / "order_turned.csv").read_text()
    j = json.loads((tmp_path / "dxf_order.json").read_text())
    assert j["sheet"][0]["id"] == "plate" and j["turned"][0]["id"] == "axle"
    assert data["turned"][0]["stock_len_mm"] == 32.0

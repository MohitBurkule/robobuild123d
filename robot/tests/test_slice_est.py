"""Slice-based mass & print-time estimate (robot/slice_est.py): layers, mass, time, files."""

import json

import trimesh


def box(w, d, h):
    return trimesh.creation.box((w, d, h))


def test_layer_count_and_volume_of_a_solid_box():
    from robot.slice_est import estimate

    e = estimate(box(20, 20, 10), layer_mm=0.2, walls=2, infill_pct=0)
    assert e["layers"] == 50  # 10 mm at 0.2 mm
    # 2 wall passes around an 80 mm perimeter: 2*80*0.08 = 12.8 mm3/layer
    assert e["extruded_mm3"] > 12.8 * 50 - 1 and e["extruded_mm3"] < 12.8 * 50 + 20 * 0.4 * 400 * 0.2 + 1


def test_mass_tracks_extruded_volume_and_density():
    from robot.slice_est import estimate

    pla = estimate(box(20, 20, 10), layer_mm=0.2, infill_pct=100)
    cf = estimate(box(20, 20, 10), layer_mm=0.2, infill_pct=100, filament="petg_cf")
    assert abs(pla["mass_g"] - pla["extruded_mm3"] / 1000 * 1.24) < 0.05
    assert cf["mass_g"] > pla["mass_g"]  # PETG-CF is the denser spool here
    assert pla["mesh_mass_g"] == 4.96  # 4000 mm3 of PLA


def test_more_walls_more_mass_more_time():
    from robot.slice_est import estimate

    thin = estimate(box(20, 20, 10), layer_mm=0.2, walls=1, infill_pct=0)
    fat = estimate(box(20, 20, 10), layer_mm=0.2, walls=4, infill_pct=0)
    assert fat["mass_g"] > thin["mass_g"] and fat["time_min"] > thin["time_min"]
    assert thin["filament_m"] > 0 and thin["time_min"] > 1  # 50 layers * 2 s + heat-up


def test_parts_orients_and_totals():
    from robot.slice_est import parts

    info = parts([("tub", box(60, 40, 10), "+z"), ("lid", box(50, 30, 4), "-z")],
                 layer_mm=0.2, infill_pct=15)
    assert [r["id"] for r in info["parts"]] == ["tub", "lid"]
    assert info["total"]["mass_g"] == round(sum(r["mass_g"] for r in info["parts"]), 2)
    assert info["total"]["time_min"] == round(sum(r["time_min"] for r in info["parts"]), 1)


def test_write_outputs(tmp_path):
    from robot.slice_est import write

    info = write([("tub", box(60, 40, 10), None)], tmp_path, layer_mm=0.2)
    assert info["total"]["mass_g"] > 0
    data = json.loads((tmp_path / "slice_est.json").read_text())
    assert data["printer"] == "ender3" and data["parts"][0]["id"] == "tub"
    assert "slice_est.csv" in {p.name for p in tmp_path.iterdir()}
    assert "time_min" in (tmp_path / "slice_est.csv").read_text().splitlines()[0]

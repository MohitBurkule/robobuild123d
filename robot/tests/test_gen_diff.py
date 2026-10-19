import copy

from robot.gen import diff as D


def _spec():
    return {"parts": [
        {"id": "tub", "kind": "structure", "material": "nylon", "process": "fdm", "shape": {"type": "box", "size": [10, 10, 5]},
         "at": [0, 0, 0], "rot": [0, 0, 0]},
        {"id": "motor_l", "kind": "motor", "catalog": "n10", "at": [10, 0, 0], "rot": [0, 0, 0]},
        {"id": "ins", "kind": "insert", "catalog": "m2", "at": [0, 5, 0], "rot": [0, 0, 0]},
    ], "fasteners": [{"id": "f1", "designation": "M2x6", "at": [0, 5, 0]}],
        "wires": [{"id": "w1", "from": "motor_l.a", "to": "tub.x"}],
        "connections": [{"a": "motor_l", "b": "tub", "method": "screw"}]}


def test_identical_specs_have_no_changes():
    d = D.diff(_spec(), _spec())
    assert d["total"] == 0 and d["architectural"] == []


def test_renamed_part_matches_by_kind_and_catalog():
    b = _spec()
    b["parts"][1]["id"] = "drive_left"
    b["wires"][0]["from"] = "drive_left.a"
    b["connections"][0]["a"] = "drive_left"
    d = D.diff(_spec(), b)
    assert d["total"] == 0 and d["matched"]["motor_l"] == "drive_left"


def test_each_category_is_counted():
    b = copy.deepcopy(_spec())
    b["parts"][0]["material"] = "pla"
    b["parts"][0]["shape"] = {"type": "box", "size": [12, 10, 5]}
    b["parts"][1]["at"] = [15, 0, 0]
    b["parts"][1]["rot"] = [0, 0, 90]
    b["parts"].append({"id": "wheel", "kind": "wheel", "at": [0, 0, 0]})
    del b["parts"][2]
    b["fasteners"].append({"id": "f2", "designation": "M3x8", "at": [1, 1, 1]})
    b["wires"] = []
    b["connections"][0]["method"] = "interlock"
    d = D.diff(_spec(), b)
    c = d["counts"]
    assert c["parts_added"] == 1 and c["parts_removed"] == 1 and c["moved"] == 1 and c["rotated"] == 1
    assert c["reshaped"] == 1 and c["material_process"] == 1 and c["fasteners"] == 1 and c["wires"] == 1
    assert c["connections"] == 2
    assert any("wheel" in s for s in d["architectural"])
    assert not any("insert" in s for s in d["architectural"])  # hardware is detail
    assert any("interlock instead of screw" in s for s in d["architectural"])
    assert d["n_architectural"] + d["n_detail"] == d["total"]

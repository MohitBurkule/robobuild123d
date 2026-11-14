"""Assembly instructions (robot/assembly_doc.py): steps from the reversed disassembly order."""

from robot.assembly_doc import steps, write


def _report(asm):
    return {"assembly": asm}


def test_order_is_reversed_disassembly():
    rep = _report([{"order": 1, "id": "lid", "dir": [0, 0, 1], "travel_mm": 30},
                   {"order": 2, "id": "weapon", "dir": [0, 0, 1], "travel_mm": 40}])
    st = steps(rep)
    ids = [p for s in st for p in s["parts"]]
    assert ids == ["weapon", "lid"]  # last out is first in


def test_prep_and_checklist_bracket_the_steps():
    st = steps(_report([{"order": 1, "id": "lid", "dir": [1, 0, 0], "travel_mm": 10}]))
    assert "Print" in st[0]["title"] and "check" in st[-1]["title"].lower()
    assert len(st) == 3  # prep + 1 part + close-up


def test_direction_text():
    rep = _report([{"order": 1, "id": "lid", "dir": [0, 1, 0], "travel_mm": 10}])
    st = steps(rep)
    assert "front" in st[1]["body"]


def test_cap_on_steps():
    asm = [{"order": i, "id": f"p{i}", "dir": [0, 0, 1], "travel_mm": 5} for i in range(30)]
    st = steps(_report(asm), max_steps=10)
    assert len(st) <= 11


def test_write_build_md(tmp_path):
    info = write(_report([{"order": 1, "id": "lid", "dir": [0, 0, 1], "travel_mm": 10}]), tmp_path)
    text = (tmp_path / "build.md").read_text()
    assert "# Build sheet" in text and "Pre-flight checklist" in text and "Fit lid" in text
    assert info["steps"][0]["n"] == 1

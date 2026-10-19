"""Reference BOM, weapon-lock part, stock O-ring, module wire cut, switch OFF direction, reference write-up."""

from robot import spec
from robot.checks import Options, verify

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731


def run(d, base_dir=None):
    return verify(spec.Spec(d, base_dir), Options(only=["bom"], deep=False, fast=True))


def base(**kw):
    d = {"name": "t", "parts": [
        {"id": "chassis", "kind": "structure", "material": "pla", "process": "fdm", "shape": BOX(40, 40, 4)},
        {"id": "lid", "kind": "plate", "material": "pla", "process": "fdm", "shape": BOX(40, 40, 2), "at": [0, 0, 3]},
        {"id": "nut0", "kind": "nut", "catalog": "nut_m2", "at": [0, 0, -3]},
    ], "fasteners": [{"id": "s0", "designation": "M2x6", "head": "button", "at": [0, 0, 4], "through": ["lid", "chassis"], "threads_into": "nut0"}]}
    d.update(kw)
    return d


ROW = {"role": "lid screws", "match": ["s*"], "count": 1, "designation": "M2x6", "head": "countersunk", "threads_into": "nut"}


def test_bom_head_mismatch_is_blocker_and_deviation_passes():
    assert run(base(reference_bom=[ROW])).failed("reference.bom")
    assert not run(base(reference_bom=[dict(ROW, deviation="button heads: the 1 mm lid is too thin to countersink")])).failed("reference.bom")
    assert not run(base(reference_bom=[dict(ROW, head="button")])).failed("reference.bom")


def test_bom_count_size_and_host():
    assert run(base(reference_bom=[dict(ROW, head="button", count=2)])).failed("reference.bom")
    assert run(base(reference_bom=[dict(ROW, head="button", designation="M2x8")])).failed("reference.bom")
    assert run(base(reference_bom=[dict(ROW, head="button", threads_into="insert")])).failed("reference.bom")


def test_bom_wire_connector():
    d = base(wires=[{"id": "w", "from": "lid.a", "to": "chassis.b", "awg": 24}],
             reference_bom=[{"role": "battery lead", "kind": "wire", "match": ["w"], "count": 1, "connector": "jst_rcy"}])
    assert run(d).failed("reference.bom")
    d["wires"][0]["connector"] = "jst_rcy"
    assert not run(d).failed("reference.bom")


def _spinner(lock=None):
    d = base(robot_type="vertical_spinner")
    d["parts"].append({"id": "disc", "kind": "weapon", "material": "steel", "process": "laser", "shape": BOX(4, 30, 30), "at": [0, 0, 30],
                       "weapon": {"kind": "disc", "locking_bar": lock}})
    d["weapon_lock"] = {"type": "removable_pin", "holes": ["chassis"], "require_part": True}
    return d


def test_weapon_lock_part_required():
    assert run(_spinner()).failed("legal.weapon_lock_part")
    d = _spinner("lockp")
    d["parts"].append({"id": "lockp", "kind": "locking_bar", "material": "tpu", "process": "fdm", "shape": BOX(4, 4, 4), "at": [0, 0, 14]})
    f = run(d).get("legal.weapon_lock_part")
    assert f and f.passed


def _belt(**b):
    d = base()
    d["parts"].append({"id": "belt", "kind": "belt", "material": "rubber", "process": "cots", "shape": BOX(1, 1, 1),
                       "belt": dict({"pulleys": [], "kind": "o_ring", "length_mm": 141.4, "width_mm": 1.0}, **b)})
    return d


def test_belt_stock():
    assert run(_belt()).failed("kin.belt_stock")
    assert run(_belt(stock={"id_mm": 46, "cs_mm": 1.0})).failed("kin.belt_stock")      # 46 is not a CS 1.0 stock ID here
    f = run(_belt(stock={"id_mm": 45, "cs_mm": 1.0})).get("kin.belt_stock")
    assert f and f.passed


def test_wire_cut():
    d = base(wires=[{"id": "ph", "from": "lid.a", "to": "chassis.b", "awg": 24}], modules=[{"id": "m", "root": "lid", "parts": []}])
    assert run(d).failed("disasm.wire_cut")
    d["wires"][0]["connector"] = "bullet2"
    f = run(d).get("disasm.wire_cut")
    assert f and f.passed


def test_switch_direction():
    d = base()
    d["parts"].append({"id": "sw", "kind": "switch", "catalog": "switch_slide_12x4", "at": [0, -18, 6]})
    assert run(d).failed("electrical.switch_direction")
    d["parts"][-1]["off_dir"] = [0, 1, 0]
    assert run(d).failed("electrical.switch_direction")
    d["parts"][-1]["off_dir"] = [0, -1, 0]
    f = run(d).get("electrical.switch_direction")
    assert f and f.passed


def test_doc_consistency(tmp_path):
    (tmp_path / "REF.md").write_text("Drisk on an MF85ZZ.")
    d = base(reference_doc={"path": "REF.md", "must_mention": ["MF85ZZ"], "must_not_mention": ["F683ZZ"]})
    assert not run(d, tmp_path).failed("reference.doc_consistency")
    (tmp_path / "OLD.md").write_text("Spider on an F683ZZ.")
    d["reference_doc"]["path"] = "OLD.md"
    assert run(d, tmp_path).failed("reference.doc_consistency")

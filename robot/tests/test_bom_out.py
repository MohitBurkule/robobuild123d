"""Purchasable BOM (robot/bom_out.py): lines, spares, packs, cost, files."""

import csv
from pathlib import Path
from types import SimpleNamespace

from robot import bom_out


def _robot(parts, fasteners=()):
    rps = [SimpleNamespace(part=p, cat=SimpleNamespace(id=p.id, kind=p.kind, name=p.id, props={}))
           for p in parts]
    spec = SimpleNamespace(raw={}, parts=[rp.part for rp in rps], connections=[], fasteners=list(fasteners))
    return SimpleNamespace(spec=spec, parts=rps)


def _p(pid, kind="printed"):
    return SimpleNamespace(id=pid, kind=kind, printed=kind == "printed")


def test_printed_parts_become_free_lines():
    lines = bom_out.build(_robot([_p("tub"), _p("lid")]))
    assert all(l.printed for l in lines) and bom_out.cost(lines) == 0.0
    assert bom_out.unsourced(lines) == []


def test_catalogued_parts_dedupe_and_count():
    a = SimpleNamespace(id="motor_l", kind="motor", printed=False)
    b = SimpleNamespace(id="motor_r", kind="motor", printed=False)
    rps = [SimpleNamespace(part=a, cat=SimpleNamespace(id="n20_600", kind="motor", name="n20", props={})),
           SimpleNamespace(part=b, cat=SimpleNamespace(id="n20_600", kind="motor", name="n20", props={})),
           SimpleNamespace(part=_p("esc1", "esc"), cat=SimpleNamespace(id="esc1", kind="esc", name="esc", props={}))]
    spec = SimpleNamespace(raw={}, parts=[rp.part for rp in rps], connections=[], fasteners=[])
    lines = bom_out.build(SimpleNamespace(spec=spec, parts=rps))
    motors = next(l for l in lines if l.kind == "motor")
    assert motors.qty == 2 and motors.spares == 0  # SPARES["motor"] = 0


def test_fasteners_group_by_size():
    r = _robot([_p("tub")], fasteners=[SimpleNamespace(size="M2x6"), SimpleNamespace(size="M2x6")])
    lines = bom_out.build(r)
    f = next(l for l in lines if l.kind == "fastener")
    assert f.qty == 2 and f.to_buy() == 3  # +1 spare


def test_pack_ceil_rounds_up():
    l = bom_out.Line("x", "x", "esc", 3, 10.0, "s", "u", pack_qty=2, spares=0)
    assert l.packs() == 2 and l.cost() == 20.0


def test_unsourced_listed_never_invented():
    r = _robot([_p("esc1", "esc"), _p("bat1", "battery")])
    lines = bom_out.build(r)
    for l in lines:
        assert l.unit_gbp is None or l.supplier  # a price always carries a supplier
    assert bom_out.unsourced(lines) == [l.id for l in lines if l.unit_gbp is None]


def test_write_outputs(tmp_path):
    r = _robot([_p("tub"), _p("esc1", "esc")], fasteners=[SimpleNamespace(size="M2x6")])
    lines = bom_out.build(r)
    info = bom_out.write(lines, tmp_path)
    assert "bom.csv" in info["files"] and "bom.md" in info["files"]
    assert Path(tmp_path / "bom.md").exists()
    with (tmp_path / "bom.csv").open() as fh:
        rows = list(csv.reader(fh))
    assert rows[0][:4] == ["id", "name", "kind", "qty"] and len(rows) >= 3

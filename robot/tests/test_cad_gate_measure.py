import json
import os
import subprocess
import sys
from pathlib import Path

import build123d as bd
import pytest

from robot.cad import fastener_catalog, gate, measure_ref
from robot.cad.holes import hole
from robot.finding import BLOCKER, WARNING, Report, fail, ok

ROOT = Path(__file__).resolve().parents[2]


def _rep(*fs):
    r = Report(name="t", profile="p")
    r.findings = list(fs)
    return r


def _setup(tmp_path, renders=True):
    sp = tmp_path / "spec.json"
    sp.write_text("{}")
    if renders:
        (tmp_path / "renders").mkdir()
        for n in gate.DEFAULT_RENDERS:
            (tmp_path / "renders" / n).write_bytes(b"png")
    return sp


def test_gate_all_pass(tmp_path):
    sp = _setup(tmp_path)
    rep = _rep(ok("reference_cad.diff", "reference", "t", "m"), ok("intent.support_free", "intent", "t", "m"),
               fail("x.warn", "x", WARNING, "t", "m"))
    assert all(r[1] for r in gate.evaluate(rep, sp))


def test_gate_fails_closed(tmp_path):
    sp = _setup(tmp_path, renders=False)
    rows = dict((n, o) for n, o, _ in gate.evaluate(_rep(fail("a.b", "a", BLOCKER, "t", "m")), sp))
    assert rows == {"verify": False, "ref_diff": False, "support": False, "renders": False}


def test_gate_stale_render(tmp_path):
    sp = _setup(tmp_path)
    old = sp.stat().st_mtime - 100
    os.utime(tmp_path / "renders" / "iso.png", (old, old))
    rows = {n: o for n, o, _ in gate.evaluate(_rep(), sp)}
    assert rows["renders"] is False


@pytest.fixture(scope="module")
def ref_stl(tmp_path_factory):
    d = tmp_path_factory.mktemp("ref")
    b = bd.Box(40, 24, 6)
    b = bd.fillet(b.edges().filter_by(bd.Axis.Z), 3)
    b, _ = hole(b, (-10, 0, 3), (0, 0, -1), "M3x10", "csk", "through")
    b, _ = hole(b, (10, 0, 3), (0, 0, -1), "M3x10", "cap", "nut", grip=2, cbore=0, nut_entry="none")
    p = d / "ref.stl"
    bd.export_stl(b, str(p), tolerance=0.01, angular_tolerance=0.1)
    return p


def test_measure_ref_numbers(ref_stl):
    d = measure_ref.measure(ref_stl, fit=True, stations=[("z", 0.0)])
    measure_ref.check_no_geometry(d)
    assert d["bbox"]["size"] == pytest.approx([40, 24, 6], abs=0.05)
    hz = [h for h in d["holes"] if h["axis"] == "z"]
    csk = min(hz, key=lambda h: abs(h["centre"][0] + 10))
    assert csk["diameter"] == pytest.approx(3.4, abs=0.15) and csk["profile"] == "csk"
    assert csk["csk_angle_deg"] == pytest.approx(90, abs=12) and csk["csk_dia"] == pytest.approx(fastener_catalog.CSK[3.0][0] + 0.2, abs=0.6)  # M3 = DIN 7991 dk 6.0, cut 6.2
    assert any("hex" in h.get("shapes_along_axis", [h["shape"]]) for h in hz)
    assert any(abs(r - 3) < 0.3 for r in d["fillet_radii"]["z"])
    assert d["wall_thickness"]["median"] > 0
    top = d["fit"]["views"]["top"]
    assert top["n_ctrl"] <= 8 and top["max_err"] < 1.5
    assert sum(s["type"] == "arc" for s in top["segments"]) >= 4


def test_measure_ref_cli_json(ref_stl):
    out = subprocess.run([sys.executable, "-m", "robot", "measure-ref", str(ref_stl), "--sections", "2"],
                         cwd=ROOT, capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr
    d = json.loads(out.stdout)
    assert set(d["sections"]) == {"x", "y", "z"} and len(d["sections"]["z"]) == 2


def test_no_geometry_guard():
    with pytest.raises(AssertionError):
        measure_ref.check_no_geometry({"outline": [[0.0, 0.0]] * 20})

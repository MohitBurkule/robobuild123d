"""Part integrity group (robot.checks.integrity): one closed solid, no volume collapse."""

import json
from types import SimpleNamespace as NS

import trimesh

from robot.checks import integrity as I
from robot.finding import BLOCKER, WARNING


def _ctx(tmp_path, monkeypatch, mesh, extra=None, raw=None, volume=None):
    monkeypatch.setattr(I, "store_path", lambda name: tmp_path / "store" / f"{name}.json")
    g = NS(mesh=mesh, volume=abs(mesh.volume) if volume is None else volume)
    rp = NS(part=NS(id="tub", _extra=extra or {}), geom=g)
    spec = NS(raw=raw or {}, base_dir=str(tmp_path), name="t")
    return NS(r=NS(spec=spec, parts=[rp]), not_checked=[], metrics={})


def _fails(out):
    return {(f.id, f.severity) for f in out if not f.passed}


def tub():
    return trimesh.creation.box([40, 30, 20]).difference(trimesh.creation.box([36, 26, 20]).apply_translation([0, 0, 2]))


def shredded():
    return trimesh.util.concatenate([trimesh.creation.box([2, 2, 2]).apply_translation([5 * i, 0, 0]) for i in range(7)])


def test_good_single_solid_passes(tmp_path, monkeypatch):
    out = I.run(_ctx(tmp_path, monkeypatch, tub(), extra={"volume_mm3": abs(tub().volume)}))
    assert not _fails(out) and any(f.id == "integrity.solids" and f.passed for f in out)


def test_collapsed_tub_blocks(tmp_path, monkeypatch):
    out = I.run(_ctx(tmp_path, monkeypatch, shredded(), extra={"volume_mm3": 15988}))
    assert {("integrity.solids", BLOCKER), ("integrity.volume", BLOCKER)} <= _fails(out)


def test_collapse_against_previous_run(tmp_path, monkeypatch):
    assert not _fails(I.run(_ctx(tmp_path, monkeypatch, tub())))  # stores the baseline
    out = I.run(_ctx(tmp_path, monkeypatch, tub(), volume=413.0))
    assert ("integrity.volume", BLOCKER) in _fails(out)
    assert json.loads((tmp_path / "store" / "t.json").read_text())["tub"] > 1000  # collapse never becomes baseline


def test_moderate_change_warns(tmp_path, monkeypatch):
    v = abs(tub().volume)
    assert ("integrity.volume", WARNING) in _fails(I.run(_ctx(tmp_path, monkeypatch, tub(), extra={"volume_mm3": v * 1.3})))


def test_reference_cad_volume(tmp_path, monkeypatch):
    tub().export(tmp_path / "tub.stl")
    raw = {"reference_cad": {"dir": ".", "parts": [{"part": "tub", "file": "tub.stl"}]}}
    assert not _fails(I.run(_ctx(tmp_path, monkeypatch, tub(), raw=raw)))
    assert ("integrity.volume", BLOCKER) in _fails(I.run(_ctx(tmp_path, monkeypatch, tub(), raw=raw, volume=400.0)))


def test_declared_solids_needs_reason(tmp_path, monkeypatch):
    m = shredded()
    assert not _fails(I.run(_ctx(tmp_path, monkeypatch, m, extra={"solids": 7, "solids_reason": "loose spacer set"})))
    f = _fails(I.run(_ctx(tmp_path, monkeypatch, m, extra={"solids": 7})))
    assert ("integrity.solids_reason", BLOCKER) in f and ("integrity.solids", BLOCKER) in f


def test_open_mesh_blocks(tmp_path, monkeypatch):
    m = tub()
    m.update_faces(list(range(len(m.faces) - 1)))
    assert ("integrity.solids", BLOCKER) in _fails(I.run(_ctx(tmp_path, monkeypatch, m)))


def test_opt_out_and_runs_first(tmp_path, monkeypatch):
    ctx = _ctx(tmp_path, monkeypatch, shredded(), raw={"integrity": {"enabled": False}})
    assert I.run(ctx) == [] and ctx.not_checked
    from robot.checks import GROUPS
    from robot.proxy import GROUPS as PG
    assert GROUPS[0][0] == "integrity" and "integrity" in PG

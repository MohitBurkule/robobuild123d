"""robot.design: typed design settings (schema, Design from a dict / JSON, use / current, env fallback) and the Revron
schema (robots/revron/src/revron/settings.py) with its in-process build_revron(design)."""
import ast
import json
import os
import sys
from pathlib import Path

import pytest

from robot import design as D

ROOT = Path(__file__).resolve().parents[2]
REVRON = ROOT / "robots" / "revron"
PKG = REVRON / "src" / "revron"
SCHEMA = D.load_schema(REVRON)
REVRON_ENVS = ["REVRON_WEAPON_TYPE", "REVRON_WEAPON_MOTOR", "REVRON_MOTOR_VARIANT", "REVRON_MOUNT_VARIANT", "REVRON_LEAD_GROOVE", "REVRON_REAR_WHEEL", "REVRON_COMPARTMENTS",
               "REVRON_SIZE_WIDTH", "REVRON_SIZE_LENGTH", "REVRON_SIZE_HEIGHT", "REVRON_DRIVE_LOCATION", "REVRON_DRIVE_MOTOR", "REVRON_SWITCH", "REVRON_BATTERY", "REVRON_RXESC",
               "REVRON_WESC", "REVRON_VARIANTS"]


@pytest.fixture(autouse=True)
def no_revron_env(monkeypatch):
    for k in [k for k in os.environ if k.startswith("REVRON_")]:
        monkeypatch.delenv(k)


def _read_sites():
    """{env: (target name, default)} of every module-level `X = setting("REVRON_...", "default")` read in the package,
    and {NAME: keys} of the module-level dict literals."""
    sites, dicts = {}, {}
    for f in sorted(PKG.glob("*.py")):
        tree = ast.parse(f.read_text())
        for st in tree.body:
            if isinstance(st, ast.Assign) and isinstance(st.targets[0], ast.Name) and isinstance(st.value, ast.Dict):
                dicts[st.targets[0].id] = [k.value for k in st.value.keys if isinstance(k, ast.Constant)]
        for st in tree.body:
            for n in ast.walk(st):
                if isinstance(n, ast.Call) and ast.unparse(n.func) == "setting" and len(n.args) == 2 and isinstance(n.args[0], ast.Constant):
                    tgt = st.targets[0].id if isinstance(st, ast.Assign) and isinstance(st.targets[0], ast.Name) else None
                    sites[n.args[0].value] = (tgt, n.args[1].value)
    return sites, dicts


# ---------------------------------------------------------------- schema
def test_schema_lists_every_revron_setting():
    assert sorted(SCHEMA.by_env) == sorted(REVRON_ENVS)
    assert len(SCHEMA.settings) == 17
    for s in SCHEMA.settings:
        assert s.doc and s.type in D.TYPES and s.env.startswith("REVRON_")
        assert (s.type in ("choice", "set")) == bool(s.choices)
        assert s.type != "choice" or s.default in s.choices


def test_schema_json_is_what_an_llm_needs(capsys):
    assert D.main(["schema", str(REVRON)]) == 0
    js = json.loads(capsys.readouterr().out)
    assert js["robot"] == "revron" and [s["name"] for s in js["settings"]] == [s.name for s in SCHEMA.settings]
    by = {s["name"]: s for s in js["settings"]}
    assert by["drive.motor"] == dict(name="drive.motor", type="choice", default="n10_2200rpm_spicy", choices=list(SCHEMA.find("drive.motor").choices),
                                     doc=SCHEMA.find("drive.motor").doc, env="REVRON_DRIVE_MOTOR")
    assert by["weapon.lead_groove"]["default"] is False and by["variants"]["default"] == [] and "choices" not in by["size.width"]
    assert SCHEMA.design({s["name"]: s["default"] for s in js["settings"]}).values == {s.name: s.default for s in SCHEMA.settings}   # the defaults are a valid design


def test_revron_sources_read_settings_only_through_the_layer():
    """No os.environ left in the generator; every read names a declared setting with the declared default; every
    declared setting is read; the allowed values cover the generator's own tables."""
    for f in PKG.glob("*.py"):
        assert "os.environ" not in f.read_text() and "getenv" not in f.read_text(), f.name
    sites, dicts = _read_sites()
    assert sorted(sites) == sorted(REVRON_ENVS)
    for env, (tgt, default) in sites.items():
        s = SCHEMA.by_env[env]
        assert default == s.default, f"{env}: read-site default {default!r} != declared {s.default!r}"
        table = dicts.get(tgt + "S") or dicts.get(tgt + "ES") if tgt else None
        if table and s.type == "choice":
            assert set(table) <= set(s.choices), f"{s.name}: {tgt}S names values the schema does not allow: {set(table) - set(s.choices)}"
    assert SCHEMA.find("variants").choices == _names()


def _names():
    tree = ast.parse((PKG / "variants.py").read_text())
    return next(tuple(e.value for e in st.value.elts) for st in tree.body if isinstance(st, ast.Assign) and st.targets[0].id == "NAMES")


def test_schema_agrees_with_hooks_json():
    hooks = json.loads((REVRON / "hooks.json").read_text())["hooks"]
    seen = 0
    for name, h in hooks.items():
        if not h.get("env"):
            continue
        s = SCHEMA.by_env[h["env"]]
        seen += 1
        assert s.name == name and s.default == h["default"]
        if s.type == "choice" and isinstance(h.get("values"), list):
            assert list(s.choices) == h["values"], name
        if s.type == "size":
            for v in h["values"]:
                assert s.parse(v) == v
    assert seen == 15   # lead groove and variants have no hook


# ---------------------------------------------------------------- Design: parsing and errors
def test_design_normalises_json_native_values():
    d = SCHEMA.design({"size.width": 4, "size.length": "-3.5", "size.height": " 10% ", "weapon.lead_groove": True, "variants": ["esc_tray", "battery_pad"],
                       "REVRON_DRIVE_MOTOR": "n10_300rpm_6v"})
    assert d.values == {"size.width": "4", "size.length": "-3.5", "size.height": "10%", "weapon.lead_groove": "on", "variants": "battery_pad,esc_tray",
                        "drive.motor": "n10_300rpm_6v"}
    assert d.env() == {"REVRON_SIZE_WIDTH": "4", "REVRON_SIZE_LENGTH": "-3.5", "REVRON_SIZE_HEIGHT": "10%", "REVRON_LEAD_GROOVE": "on",
                       "REVRON_VARIANTS": "battery_pad,esc_tray", "REVRON_DRIVE_MOTOR": "n10_300rpm_6v"}
    assert d["drive.motor"] == "n10_300rpm_6v" and d["battery.pack"] == "lipo_2s_180_turnabot"
    assert SCHEMA.design(d.to_dict()) == d and SCHEMA.design({"robot": "revron", "settings": d.to_dict()}) == d
    assert SCHEMA.design({"variants": "all"}).values == {"variants": "all"} and SCHEMA.design().values == {}


def test_design_from_json_file(tmp_path):
    p = tmp_path / "d.json"
    p.write_text(json.dumps({"drive.motor": "n10_300rpm_6v", "weapon.lead_groove": False}))
    assert SCHEMA.load(p).values == {"drive.motor": "n10_300rpm_6v", "weapon.lead_groove": "off"}


@pytest.mark.parametrize("values, says", [
    ({"drive.motr": "n10_300rpm_6v"}, "unknown setting 'drive.motr' for revron; did you mean ['drive.motor'"),
    ({"REVRON_NOPE": "1"}, "unknown setting 'REVRON_NOPE'"),
    ({"drive.motor": "n10_300rpm"}, "setting 'drive.motor': bad value 'n10_300rpm': did you mean ['n10_300rpm_6v'"),
    ({"drive.motor": 3}, "setting 'drive.motor': bad value 3: expected a string"),
    ({"size.width": "wide"}, "setting 'size.width': bad value 'wide': expected mm"),
    ({"size.width": True}, "setting 'size.width': bad value True"),
    ({"weapon.lead_groove": "yes"}, "setting 'weapon.lead_groove': bad value 'yes'"),
    ({"variants": ["esc_tray", "turbo"]}, "setting 'variants': bad value ['esc_tray', 'turbo']: unknown ['turbo']"),
    ({"drive.motor": "n10_300rpm_6v", "REVRON_DRIVE_MOTOR": "n10_300rpm_6v"}, "given twice"),
    ({"robot": "wedge", "settings": {}}, "design is for 'wedge', not 'revron'"),
    (["drive.motor"], "a design is a JSON object"),
])
def test_bad_design_raises_a_clear_error(values, says):
    with pytest.raises(D.DesignError) as e:
        SCHEMA.design(values)
    assert says in str(e.value)


def test_cli_reports_a_bad_design(tmp_path, capsys):
    p = tmp_path / "d.json"
    p.write_text(json.dumps({"battery.pack": "car_battery"}))
    assert D.main(["spec", str(REVRON), str(p)]) == 2
    assert "design error: setting 'battery.pack': bad value 'car_battery'" in capsys.readouterr().err


# ---------------------------------------------------------------- reading: design > env > default
def test_value_priority_design_then_env_then_default(monkeypatch):
    assert D.current() is None
    assert D.value("REVRON_DRIVE_MOTOR", "dflt") == "dflt"
    monkeypatch.setenv("REVRON_DRIVE_MOTOR", "from_env")
    monkeypatch.setenv("REVRON_BATTERY", "env_pack")
    assert D.value("REVRON_DRIVE_MOTOR", "dflt") == "from_env"   # env fallback, unvalidated as before
    d = SCHEMA.design({"drive.motor": "n10_300rpm_6v"})
    with D.use(d) as active:
        assert D.current() is active is d
        assert D.value("REVRON_DRIVE_MOTOR", "dflt") == "n10_300rpm_6v"   # the design wins over the env
        assert D.value("REVRON_BATTERY", "dflt") == "env_pack"            # unset in the design: the env still applies
        assert D.value("REVRON_SWITCH", "dflt") == "dflt"
        assert d.resolved()["drive.motor"] == ("n10_300rpm_6v", "design") and d.resolved()["battery.pack"] == ("env_pack", "env")
        assert d.resolved()["switch.power"] == ("switch_bbb_ant_rvrn2", "default")
        with D.use(None):
            assert D.value("REVRON_DRIVE_MOTOR", "dflt") == "from_env"
        assert D.value("REVRON_DRIVE_MOTOR", "dflt") == "n10_300rpm_6v"
    assert D.current() is None and os.environ["REVRON_DRIVE_MOTOR"] == "from_env"


def test_use_env_exports_for_child_processes_and_restores(monkeypatch):
    monkeypatch.setenv("REVRON_BATTERY", "before")
    with D.use(SCHEMA.design({"battery.pack": "lipo_2s_350", "size.width": "10%"}), env=True):
        assert os.environ["REVRON_BATTERY"] == "lipo_2s_350" and os.environ["REVRON_SIZE_WIDTH"] == "10%"
    assert os.environ["REVRON_BATTERY"] == "before" and "REVRON_SIZE_WIDTH" not in os.environ


# ---------------------------------------------------------------- Revron in one process
def _params(design, *names):
    """Revron's import-time params under `design`: the package imported afresh, the previous modules put back."""
    import importlib
    with D.use(SCHEMA.design(design)), D.fresh_import("revron", PKG.parent):
        P = importlib.import_module("revron.params")
        V = importlib.import_module("revron.variants")
        return {n: getattr(P, n) for n in names} | {"variants": sorted(n for n in V.NAMES if V.variant(n))}


def test_two_designs_in_one_process_give_different_params():
    names = ("DRIVE_MOTOR", "GB", "CH_HALF_W", "SIZE_DW", "BATTERY", "LEAD_GROOVE", "WHEEL_OD_R")
    before = {k: v for k, v in sys.modules.items() if k == "revron" or k.startswith("revron.")}
    a = _params(None, *names)
    b = _params({"drive.motor": "bbb_hpn20_1000rpm", "size.width": "10%", "weapon.lead_groove": True, "wheel.rear": "wheel_28x10", "variants": ["esc_tray"]}, *names)
    c = _params({"size.width": 4}, *names)
    assert a["DRIVE_MOTOR"] == "n10_2200rpm_spicy" and b["DRIVE_MOTOR"] == "bbb_hpn20_1000rpm" and a["GB"] != b["GB"]
    assert (a["CH_HALF_W"], a["SIZE_DW"]) == (29.5, 0.0) and b["SIZE_DW"] == pytest.approx(2.95) and b["CH_HALF_W"] == pytest.approx(32.45)
    assert c["CH_HALF_W"] == pytest.approx(33.5) and c["DRIVE_MOTOR"] == a["DRIVE_MOTOR"]
    assert (a["LEAD_GROOVE"], b["LEAD_GROOVE"], a["WHEEL_OD_R"], b["WHEEL_OD_R"]) == (False, True, 21.5, 28.0)
    assert (a["variants"], b["variants"]) == ([], ["esc_tray"])
    assert _params(None, *names) == a   # nothing of b or c is left behind
    assert not [k for k in os.environ if k.startswith("REVRON_")]
    assert {k: v for k, v in sys.modules.items() if k == "revron" or k.startswith("revron.")} == before   # the caller's modules are back


def test_env_fallback_reaches_the_generator(monkeypatch):
    monkeypatch.setenv("REVRON_DRIVE_MOTOR", "n10_300rpm_6v")
    assert _params(None, "DRIVE_MOTOR")["DRIVE_MOTOR"] == "n10_300rpm_6v"
    assert _params({"drive.motor": "bbb_n10_600rpm"}, "DRIVE_MOTOR")["DRIVE_MOTOR"] == "bbb_n10_600rpm"


def test_build_revron_twice_with_two_designs():
    mod = D.load_settings(REVRON)
    stock = json.loads(json.dumps(mod.build_revron()))
    assert stock == json.loads((REVRON / "spec.json").read_text())   # the default design is the committed spec
    other = mod.build_revron({"drive.motor": "n10_300rpm_6v", "variants": ["esc_tray"]})
    cat = lambda spec: {p.get("catalog") for p in spec["parts"]}   # noqa: E731
    assert "n10_300rpm_6v" in cat(other) and "n10_300rpm_6v" not in cat(stock) and "n10_2200rpm_spicy" in cat(stock)
    assert len(other["parts"]) == len(stock["parts"]) + 1   # the esc_tray variant adds its part
    assert json.loads(json.dumps(D.build_spec(REVRON))) == stock   # and back again


def test_unbuilt_design_fails_with_the_generators_reason():
    with pytest.raises(NotImplementedError, match="front_motors_rear_driven"):
        D.load_settings(REVRON).build_revron({"drive.location": "front_motors_rear_driven"})
    assert _params(None, "DRIVE_LOCATION")["DRIVE_LOCATION"] == "rear"   # a failed build leaves nothing behind


def test_robust_discovery_still_finds_the_settings():
    from robot.checks.robust import discover as R
    files = R.package_files(REVRON / "src" / "build_revron.py")
    sw = {s.name: s for s in R.switches_in_package(files) if s.kind == "choice"}
    assert sw["REVRON_DRIVE_MOTOR"].default == "n10_2200rpm_spicy" and "n10_300rpm_6v" in sw["REVRON_DRIVE_MOTOR"].alternatives
    assert sw["REVRON_LEAD_GROOVE"].alternatives == ["on"]
    assert R.env_setting(files, "REVRON_SIZE_WIDTH").symbol == "SIZE_WIDTH" and R.reads_env(files, "REVRON_VARIANTS")

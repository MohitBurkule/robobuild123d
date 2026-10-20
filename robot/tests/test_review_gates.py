"""Design-review gates: reference.unmapped_part, cots.fidelity, wire.rotating_clearance, wire.render_present,
fastener.hole_record, cots.belt_wrap, print.orientation_declared. One bad and one good spec each."""

import json
import os
import time

import numpy as np

from robot import spec
from robot.checks import Options, verify

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731
CYL = lambda r, h: {"type": "cylinder", "radius": r, "height": h}  # noqa: E731
PLACE = lambda s, at, rot=(0, 0, 0): {"type": "place", "shape": s, "at": list(at), "rot": list(rot)}  # noqa: E731
CYLX = lambda r, h, x=0.0, y=0.0, z=0.0: PLACE(CYL(r, h), (x, y, z), (0, 90, 0))  # noqa: E731


def run(d, group, base_dir=None):
    return verify(spec.Spec(d, base_dir), Options(only=[group], deep=False, fast=True))


def chassis(**kw):
    d = {"name": "t", "parts": [{"id": "chassis", "kind": "structure", "material": "pla", "process": "fdm",
                                  "print_orientation": "+z", "shape": BOX(40, 40, 4)}]}
    d.update(kw)
    return d


# ------------------------------------------------------------------------------------------- reference.unmapped_part
def _ref(tmp_path, extra_parts=(), rows=()):
    ref = tmp_path / "ref"
    ref.mkdir(exist_ok=True)
    for stem in ("RV01_Chassis_1", "FS8_1", "RV15_BBB_Switch_1"):
        (ref / f"{stem}.stl").write_text("solid x\nendsolid x\n")
    d = chassis(reference_cad={"dir": str(ref), "parts": [{"part": "chassis", "file": "RV01_Chassis_1.stl"}]},
                reference_bom=list(rows))
    d["parts"] += list(extra_parts)
    return d


def test_unmapped_part_invented_hardware_fails(tmp_path):
    nut = {"id": "disc_nut", "kind": "nut", "catalog": "nut_m2", "at": [0, 0, 10]}
    # our own BOM row (cites no reference part) does not map it
    rows = [{"role": "disc nuts (not in the STEP)", "kind": "part", "match": ["disc_nut"]}]
    rep = run(_ref(tmp_path, [nut], rows), "ref_map")
    f = [f for f in rep.findings if f.id == "reference.unmapped_part" and not f.passed]
    assert f and f[0].parts == ["disc_nut"]


def test_unmapped_part_reference_row_or_deviation_passes(tmp_path):
    sw = {"id": "power_switch", "kind": "switch", "catalog": "switch_bbb_ant_rvrn2", "at": [0, 0, 10]}
    rows = [{"role": "RV15 BBB switch", "kind": "part", "match": ["power_switch"]}]
    assert not run(_ref(tmp_path, [sw], rows), "ref_map").failed("reference.unmapped_part")
    nut = {"id": "disc_nut", "kind": "nut", "catalog": "nut_m2", "at": [0, 0, 10], "deviation": "clamps the disc pack"}
    assert not run(_ref(tmp_path, [nut]), "ref_map").failed("reference.unmapped_part")


# ------------------------------------------------------------------------------------------------- cots.fidelity
def test_cots_fidelity_catalog_gr1507_has_its_bolt_circle():
    """The catalog GR1507 now carries the real base cross with the 4 M2 holes on 12 mm."""
    d = chassis()
    d["parts"].append({"id": "wm", "kind": "weapon_motor", "catalog": "gr1507", "at": [0, 0, 30]})
    f = [f for f in run(d, "cots_fidelity").findings if f.id == "cots.fidelity" and not f.passed]
    assert not any("bolt circle" in x.message for x in f)


FEAT = {"bell_d": 19.6, "stator_d": 19.6, "shaft_d": 5.0, "bolt_circle_d": 12.0, "bolt_n": 4}
HOLES = [CYLX(1.0, 3.0, -10.4, 6.0 * c, 6.0 * s) for c, s in ((1, 0), (0, 1), (-1, 0), (0, -1))]


def _outrunner(stator_at=(0, 0, 30), ref=None):
    """Split outrunner: a rotating bell (open at -X, shaft out of +X) and a stator (base flange with 4 M2 holes + core)."""
    can = {"type": "union", "items": [{"type": "subtract", "base": CYLX(9.8, 8.6, 0.0), "cut": [CYLX(8.0, 8.0, -0.3)]},
                                      CYLX(2.5, 4.0, 6.3)]}
    stator = {"type": "subtract", "base": {"type": "union", "items": [CYLX(9.8, 2.0, -9.4), CYLX(7.5, 11.8, -2.5)]},
              "cut": HOLES}
    d = chassis()
    d["parts"] += [
        {"id": "weapon_motor_can", "kind": "weapon_motor", "material": "steel", "process": "cots", "at": [0, 0, 30],
         "shape": can, "features": FEAT},
        {"id": "weapon_motor_stator", "kind": "structure", "material": "steel", "process": "cots",
         "at": list(stator_at), "shape": stator}]
    if ref is not None:
        d["reference_cad"] = ref
    return d


def test_cots_fidelity_real_outrunner_passes():
    rep = run(_outrunner(), "cots_fidelity")
    assert not [f for f in rep.findings if not f.passed and f.severity == "blocker"], [f.message for f in rep.findings]
    assert rep.get("cots.motor_bore").passed


def test_cots_motor_fused_single_part_fails():
    body = {"type": "union", "items": [CYLX(9.8, 2.0, -9.4), CYLX(9.8, 8.6, 0.0), CYLX(2.5, 4.0, 6.3)]}
    d = chassis()
    d["parts"].append({"id": "weapon_motor", "kind": "weapon_motor", "material": "steel", "process": "cots",
                       "at": [0, 0, 30], "shape": {"type": "subtract", "base": body, "cut": HOLES}, "features": FEAT})
    f = run(d, "cots_fidelity").get("cots.motor_split")
    assert f is not None and not f.passed and f.parts == ["weapon_motor"]


def test_cots_motor_empty_can_fails():
    rep = run(_outrunner(stator_at=(0, 60, 30)), "cots_fidelity")  # stator beside the can, not in its bore
    f = rep.get("cots.motor_bore")
    assert f is not None and not f.passed


def _ref_stl(tmp_path, scale, core_r=4.0):
    """A GR1507_1 stand-in: hollow can with an r`core_r` core, sized so its filled envelope is `scale` x ours."""
    import trimesh

    env = scale * run(_outrunner(), "cots_fidelity").metrics["cots.motor.weapon_motor"]["envelope_mm3"]
    h = env / (np.pi * 9.8 ** 2)
    shell = trimesh.creation.annulus(r_min=9.0, r_max=9.8, height=h, sections=256)
    core = trimesh.creation.cylinder(radius=core_r, height=h, sections=128)
    (tmp_path / "GR1507_1.stl").write_bytes(trimesh.util.concatenate([shell, core]).export(file_type="stl"))
    return {"dir": str(tmp_path), "parts": [{"part": "weapon_motor_can", "with_parts": ["weapon_motor_stator"],
                                             "file": "GR1507_1.stl", "mode": "envelope"}]}


def test_cots_motor_envelope_off_reference_fails(tmp_path):
    f = run(_outrunner(ref=_ref_stl(tmp_path, 1.10)), "cots_fidelity").get("cots.motor_volume")
    assert f is not None and not f.passed and f.severity == "blocker"


def test_cots_motor_real_stator_envelope_close_passes(tmp_path):
    rep = run(_outrunner(ref=_ref_stl(tmp_path, 1.02)), "cots_fidelity")
    f, m = rep.get("cots.motor_volume"), rep.metrics["cots.motor.weapon_motor"]
    assert f is not None and f.passed, f and f.message
    assert abs(m["volume_mm3"] / m["ref_volume_mm3"] - 1) > 0.05  # raw volume alone would have blocked
    assert m["envelope_mm3"] > m["volume_mm3"]


# ---------------------------------------------------------------------------------------- wire.rotating_clearance
def _spinner(via):
    d = chassis()
    d["parts"] += [
        {"id": "disc", "kind": "weapon", "material": "steel", "process": "laser", "at": [0, 0, 30], "shape": CYLX(15, 3),
         "weapon": {"kind": "disc", "spin_axis": [1, 0, 0]}},
        {"id": "dnut", "kind": "nut", "catalog": "nut_m2", "parent": "disc", "at": [3, 0, 10], "rot": [0, 90, 0]},
        {"id": "bat", "kind": "structure", "material": "pla", "process": "fdm", "print_orientation": "+z", "shape": BOX(4, 4, 4),
         "at": [0, -30, 4], "ports": {"p": [0, 0, 2]}},
        {"id": "esc", "kind": "structure", "material": "pla", "process": "fdm", "print_orientation": "+z", "shape": BOX(4, 4, 4),
         "at": [0, 30, 4], "ports": {"q": [0, 0, 2]}},
    ]
    d["wires"] = [{"id": "w", "from": "bat.p", "to": "esc.q", "awg": 24, "kind": "power", "via": via}]
    return d


def test_wire_too_close_to_rotating_nut_fails():
    rep = run(_spinner([[5, 0, 40.5]]), "wire_review")  # passes the nut's swept circle (r~10 about the disc axis)
    assert rep.failed("wire.rotating_clearance")


def test_wire_clear_of_rotating_nut_passes():
    rep = run(_spinner([[20, 0, 6]]), "wire_review")
    f = rep.get("wire.rotating_clearance")
    assert f is not None and f.passed, [x.message for x in rep.findings]


def test_wire_clearance_is_to_the_swept_band_of_the_nut():
    # the nut sweeps t 2.2..3.8 x rho ~8..12 about the disc axis: a lead 2.0 mm behind its back face passes the 1 mm default,
    # one 1.0 mm behind it does not (the 0.4 mm bundle radius counts)
    ok_ = run(_spinner([[5.8, -30, 40], [5.8, 30, 40]]), "wire_review").get("wire.rotating_clearance")
    assert ok_ is not None and ok_.passed, ok_ and ok_.message
    assert run(_spinner([[4.8, -30, 40], [4.8, 30, 40]]), "wire_review").failed("wire.rotating_clearance")


# -------------------------------------------------------------------------------------------- wire.render_present
def _rendered(tmp_path, wires_drawn, end=None):
    d = _spinner([[20, 0, 6]])
    (tmp_path / "spec.json").write_text(json.dumps(d))
    rd = tmp_path / "renders"
    rd.mkdir()
    png = rd / "top.png"
    png.write_bytes(b"x")
    rec = {"wires": {"w": {"from": end or [0, -30, 6], "to": [0, 30, 6]}} if wires_drawn else {}}
    (rd / "top.png.json").write_text(json.dumps(rec))
    later = time.time() + 5
    os.utime(png, (later, later))
    d["renders"] = {"dir": "renders"}
    return d


def test_render_without_wires_fails(tmp_path):
    assert run(_rendered(tmp_path, False), "wire_review", tmp_path).failed("wire.render_present")


def test_render_with_stale_endpoint_fails(tmp_path):
    rep = run(_rendered(tmp_path, True, end=[0, -36, 6]), "wire_review", tmp_path)  # the battery moved 6 mm since
    assert rep.failed("wire.render_present")


def test_render_with_current_wires_passes(tmp_path):
    rep = run(_rendered(tmp_path, True), "wire_review", tmp_path)
    assert not rep.failed("wire.render_present"), [f.message for f in rep.findings if not f.passed]


# ------------------------------------------------------------------------------------------ fastener.hole_record
def _screwed(hole, designation="M2x4", into="chassis"):
    d = chassis()
    d["parts"].append({"id": "lid", "kind": "plate", "material": "titanium", "process": "laser", "shape": BOX(40, 40, 1), "at": [0, 0, 2.5]})
    d["parts"].append({"id": "ins", "kind": "insert", "catalog": "heatset_m2", "at": [10, 10, 0]})
    d["fasteners"] = [{"id": "s", "designation": designation, "at": [10, 10, 3], "dir": [0, 0, -1], "through": ["lid"],
                       "threads_into": into, "hole": hole}]
    return d


def test_fastener_without_hole_record_fails():
    assert run(_screwed(None, "M2x8"), "fastener_record").failed("fastener.hole_record")


def test_fastener_short_thread_in_plastic_fails():
    rep = run(_screwed({"d": 2.0, "grip": 1.0}, "M2x4"), "fastener_record")  # 3 mm < 2.5 d = 5 mm
    assert rep.failed("fastener.hole_record")


def test_fastener_long_engagement_or_insert_passes():
    assert not run(_screwed({"d": 2.0, "grip": 1.0}, "M2x8"), "fastener_record").failed("fastener.hole_record")
    assert not run(_screwed({"d": 2.0, "grip": 1.0}, "M2x4", "ins"), "fastener_record").failed("fastener.hole_record")


# ------------------------------------------------------------------------------------------------ cots.belt_wrap
def _belt(shape):
    d = chassis()
    d["parts"] += [
        {"id": "pa", "kind": "pulley", "material": "pla", "process": "fdm", "print_orientation": "+x", "shape": CYLX(5, 2), "at": [0, 13, 20]},
        {"id": "pb", "kind": "pulley", "material": "pla", "process": "fdm", "print_orientation": "+x", "shape": CYLX(5, 2), "at": [0, -13, 20]},
        {"id": "belt", "kind": "belt", "material": "rubber", "process": "cots", "shape": shape, "at": [0, 0, 20],
         "belt": {"pulleys": ["pa", "pb"], "kind": "o_ring", "length_mm": 80, "width_mm": 1.0}},
    ]
    return d


def test_flat_strip_belt_fails():
    assert run(_belt(PLACE(BOX(1, 26, 1.0), (0, 0, 5.5))), "belt_wrap").failed("cots.belt_wrap")


def test_closed_loop_belt_passes():
    ring = {"type": "subtract", "base": BOX(1, 38, 12), "cut": [BOX(3, 36, 10)]}
    rep = run(_belt(ring), "belt_wrap")
    f = rep.get("cots.belt_wrap")
    assert f is not None and f.passed, [x.message for x in rep.findings]


def test_closed_loop_belt_in_an_off_centre_groove_passes():
    ring = {"type": "subtract", "base": BOX(1, 38, 12), "cut": [BOX(3, 36, 10)]}
    rep = run(_belt(PLACE(ring, (0.9, 0, 0))), "belt_wrap")
    f = rep.get("cots.belt_wrap")
    assert f is not None and f.passed, [x.message for x in rep.findings]


def test_belt_beside_the_hub_fails():
    ring = {"type": "subtract", "base": BOX(1, 38, 12), "cut": [BOX(3, 36, 10)]}
    rep = run(_belt(PLACE(ring, (6.0, 0, 0))), "belt_wrap")
    assert rep.failed("cots.belt_wrap")
    assert any("beside" in x.message for x in rep.findings), [x.message for x in rep.findings]


# ---------------------------------------------------------------------------------- print.orientation_declared
def _printed(po, shape=None):
    d = chassis()
    p = {"id": "bracket", "kind": "structure", "material": "pla", "process": "fdm", "at": [0, 0, 20],
         "shape": shape or BOX(10, 10, 10)}
    if po:
        p["print_orientation"] = po
    d["parts"].append(p)
    return d


def test_print_orientation_missing_fails():
    assert run(_printed(None), "print_orient").failed("print.orientation_declared")


def test_print_orientation_with_overhang_fails_and_good_passes():
    tee = {"type": "union", "items": [BOX(4, 4, 20), PLACE(BOX(30, 30, 2), (0, 0, 9))]}  # mushroom: flat cap on a stem
    assert run(_printed("+z", tee), "print_orient").failed("print.orientation_declared")
    assert not run(_printed("-z", tee), "print_orient").failed("print.orientation_declared")


def _outrunner_sep_shaft(shaft_r):
    """Split outrunner whose shaft is its own part (`shaft_of` the can): the can ends in a d6 hub, the shaft runs on past it."""
    d = _outrunner()
    can = next(p for p in d["parts"] if p["id"] == "weapon_motor_can")
    can["shape"] = {"type": "union", "items": [{"type": "subtract", "base": CYLX(9.8, 8.6, 0.0), "cut": [CYLX(8.0, 8.0, -0.3)]},
                                               CYLX(3.0, 1.0, 4.8)]}
    d["parts"].append({"id": "wshaft", "kind": "shaft", "material": "steel", "process": "cots", "shaft_of": "weapon_motor_can",
                       "at": [0, 0, 30], "shape": CYLX(shaft_r, 14.0, 3.0)})
    return d


def test_cots_fidelity_judges_separate_shaft_part():
    rep = run(_outrunner_sep_shaft(2.5), "cots_fidelity")
    bad = [f.message for f in rep.findings if f.id == "cots.fidelity" and not f.passed]
    assert not bad, bad


def test_cots_fidelity_separate_shaft_wrong_diameter_fails():
    rep = run(_outrunner_sep_shaft(1.5), "cots_fidelity")
    assert any("shaft" in f.message for f in rep.findings if f.id == "cots.fidelity" and not f.passed)

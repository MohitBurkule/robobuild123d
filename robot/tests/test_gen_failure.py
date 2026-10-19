from robot.gen.failure import interact as I
from robot.gen.failure.ontology import ent, agent, ENTITIES, AGENTS
from robot.gen.failure.catalog import entry


def test_toggle_by_contact_aligned_vs_oblique():
    sw = ent("switch_slide")  # slide axis x
    a = I.toggle_by_contact(sw, agent("wedge"), "nominal")  # sweep x
    b = I.toggle_by_contact(sw, agent("hspin_bar"), "nominal")  # sweep y
    assert a and b and a["likelihood"] > b["likelihood"]
    assert "OFF" in a["title"]


def test_toggle_not_for_internal_or_magnetic():
    assert I.toggle_by_contact(ent("switch_electronic"), agent("vspin_disc"), "nominal") is None
    assert I.toggle_by_contact(ent("battery"), agent("vspin_disc"), "nominal") is None


def test_handling_toggle_on():
    h = I.toggle_on_handling(ent("switch_slide"), agent("operator_handling"), "nominal")
    assert h and "ON" in h["title"]


def test_inverted_state_swaps_bands():
    e = I.apply_state(ent("lid"), "inverted")
    assert "bottom" in e.bands and "top" not in e.bands


def test_post_impact_jam_rule():
    h = I.post_impact_jam(ent("tyre"), ent("shell"), "nominal")
    assert h and "rub" in h["title"]
    assert I.post_impact_jam(ent("shell"), ent("tyre"), "nominal") is None


def test_wire_entangle_and_vibration():
    assert I.wire_entangle(ent("wire_motor"), ent("pulley"), "nominal")
    assert I.vibration_loosen(ent("screw"), agent("vibration"), "nominal")
    assert I.vibration_loosen(ent("battery"), agent("vibration"), "nominal") is None


def test_full_generation_has_switch_toggle_and_is_large():
    cl = I.cascades(I.cluster(I.generate()))
    es = [entry(c) for c in cl]
    new = [e for e in es if e["status"] == "NEW"]
    assert len(new) >= 150
    hits = [e for e in new if e["entity"] == "switch_slide" and "toggle_by_contact" in e["mechanism"] and e["state"] == "nominal"]
    assert hits and any("vspin_disc" in e["cause"] for e in hits) and any("flipper_servo" in e["cause"] for e in hits)
    assert any(e["state"] == "inverted" for e in new)
    assert any(e["cascade"] and len(e["cascade"][0]["steps"]) >= 2 for e in new)
    assert len({e["id"] for e in es}) == len(es)
    assert all(e["id"].startswith("CFX-") for e in es)

"""Hypothesis space, compatibility rules and budgets of the template engine (robot/gen)."""

import itertools

import pytest

from robot.gen import budget, rules
from robot.gen import hypothesis as H


def test_axes_cover_requested_values():
    for w in ("none_pusher", "wedge", "lifter", "lifting_wedge", "flipper", "grabber_clamp", "hspin_bar", "vspin_disc",
              "vspin_drum", "vspin_drisk", "hammer_axe", "overhead_saw", "hspin_shell", "hspin_ring", "expandabot"):
        assert w in H.WEAPONS
    assert set(H.MOUNTS) >= {"top", "front", "side", "rear", "centre", "under"}
    assert set(H.ORIENTATIONS) >= {"flat", "slanted", "vertical"}
    assert set(H.ATTACHMENTS) >= {"hub_motor", "shaft_bearings", "belt", "direct", "servo_horn"}
    assert set(H.FRONTS) >= {"wedge", "forks", "wedgelets", "skirt", "none"}
    assert {"2WD", "4WD"} <= set(H.DRIVE_LAYOUTS)


def test_axes_aligned_with_taxonomy():
    tax = H.taxonomy()
    if not tax:
        pytest.skip("taxonomy snapshot missing")
    for w in tax["axes"]["weapon_type"]:
        assert H.normalise(w, H.WEAPONS) in H.WEAPONS, w
    for d in tax["axes"]["drive_layout"]:
        assert H.normalise(d, H.DRIVE_LAYOUTS) in H.DRIVE_LAYOUTS or d in ("2WD+skid/caster",), d


def test_taxonomy_types_are_allowed_by_weapon_classes():
    """Every (weapon, mount/orientation/attachment/front) the research lists is a legal value in our tables."""
    for name in H.taxonomy().get("types", {}):
        w = H.normalise(name, H.WEAPONS)
        if w not in H.WEAPON_CLASSES:
            continue
        wc, t = H.WEAPON_CLASSES[w], H.taxonomy_weapon_class(name)
        assert set(t["position"]) <= set(wc.mounts) | {"none"}, (name, t["position"])
        assert set(t["orientation"]) <= set(wc.orientations) | {"none"}, (name, t["orientation"])


@pytest.mark.parametrize("weapon", sorted(H.WEAPON_CLASSES))
def test_every_weapon_has_valid_hypotheses(weapon):
    assert H.count_hypotheses({"weapon": weapon}) > 0


def test_real_robots_map_to_valid_hypotheses():
    """Each robot in the taxonomy's list maps (weapon type -> preset) to a hypothesis no rule rejects."""
    names = {w.split("(")[0] for w in H.WEAPONS}
    n = 0
    for r in H.taxonomy().get("robots", []):
        token = str(r.get("weapon", "")).split(" ")[0].split("(")[0].strip(";,")
        w = H.normalise(token, H.WEAPONS)
        if w not in names:
            continue
        h = H.preset(w)
        assert rules.violations(h) == [], (r["name"], rules.violations(h))
        n += 1
    assert n >= 5


def test_enumeration_prunes_and_matches_count():
    fixed = {"weapon": "vspin_drisk", "battery": "lipo_2s_350"}
    hs = list(H.enumerate_hypotheses(fixed))
    assert len(hs) == H.count_hypotheses(fixed) > 0
    assert all(not rules.violations(h) for h in hs[:200])
    assert len({h.slug for h in hs}) == len(hs)


def test_enumeration_limit():
    assert len(list(H.enumerate_hypotheses(limit=7))) == 7


def test_parse_and_aliases():
    h = H.Hypothesis.parse("weapon=vertical_spinner_drisk,wheel_dia=22")
    assert h.weapon == "vspin_drisk" and h.wheel_dia == 22 and h.attachment == "drisk"
    assert H.Hypothesis.parse("horizontal_spinner").weapon == "hspin_bar"
    assert H.Hypothesis.from_dict(h.to_dict()) == h


@pytest.mark.parametrize("w", sorted(H.PRESETS))
def test_presets_valid_and_buildable(w):
    h = H.preset(w)
    assert rules.violations(h) == []
    assert H.buildable(h)


# ---- one test per rule: a violating and a passing example
def _h(**kw):
    return H.Hypothesis(**{**H.preset(kw.get("weapon", "wedge")).to_dict(), **kw})


RULE_CASES = {
    "weapon_mount": (dict(weapon="vspin_drisk", mount="rear"), dict(weapon="vspin_drisk", mount="front")),
    "weapon_orientation": (dict(weapon="vspin_drisk", orientation="flat"), dict(weapon="vspin_drisk")),
    "weapon_attachment": (dict(weapon="lifter", attachment="belt"), dict(weapon="lifter")),
    "weapon_front": (dict(weapon="hspin_shell", front="wedge"), dict(weapon="wedge", front="wedge")),
    "vertical_not_under": (dict(weapon="undercutter", mount="under", orientation="vertical"), dict(weapon="wedge")),
    "walker_drive": (dict(weapon="meltybrain", drive_layout="2WD"), dict(weapon="wedge", drive_layout="2WD")),
    "belt_needs_axles": (dict(transmission="belt", drive_layout="2WD"), dict(transmission="belt", drive_layout="4WD")),
    "wheel_size_for_motor": (dict(drive_motor="n20", wheel_dia=16), dict(drive_motor="n20", wheel_dia=28)),
    "invertible_wheels": (dict(invertible=True, wheel_dia=16), dict(invertible=True, wheel_dia=28)),
    "battery_voltage": (dict(battery="lipo_1s_300", drive_motor="n10"), dict(battery="lipo_2s_180")),
    "battery_for_weapon": (dict(weapon="hspin_bar", battery="lipo_1s_300"), dict(weapon="hspin_bar")),
    "weapon_esc_matches": (dict(weapon="hspin_bar", weapon_esc="none"), dict(weapon="hspin_bar")),
    "receiver_integration": (dict(drive_esc="c_malenki_nano_antweight_esc_receiver", rx="rx_fs_ia6_decased"),
                             dict(drive_esc="c_malenki_nano_antweight_esc_receiver", rx="integrated")),
    "esc_channels": (dict(drive_layout="6WD", drive_esc="esc_dual_brushed"), dict(drive_layout="2WD")),
    "servo_on_2s": (dict(weapon="lifter", battery="lipo_1s_300", drive_motor="n20"), dict(weapon="lifter")),
    "weapon_invertible": (dict(weapon="hspin_shell", mount="full_body", attachment="hub_motor", front="none", invertible=False),
                          dict(weapon="wedge")),
    "mass_budget": (dict(weapon="full_body_spinner", drive_layout="8WD", wheel_dia=25, battery="lipo_2s_350",
                         weapon_esc="esc_brushless_12a", drive_esc="c_bbb_antweight_dual_esc_v3_1"), dict(weapon="wedge")),
    "size_budget": (dict(drive_motor="n20", wheel_dia=40, wheel_guards=True, weapon="vspin_drisk", front="forks"),
                    dict(weapon="wedge")),
}


def test_every_rule_has_a_case():
    assert {r.name for r in rules.RULES} == set(RULE_CASES)


@pytest.mark.parametrize("name", sorted(RULE_CASES))
def test_rule(name):
    rule = next(r for r in rules.RULES if r.name == name)
    bad, good = RULE_CASES[name]
    assert rule.check(_h(**bad)) is not None
    assert rule.check(_h(**good)) is None


def test_budget_monotone_in_battery():
    a, b = _h(battery="lipo_2s_180"), _h(battery="lipo_2s_350")
    assert budget.mass_low(b) - budget.mass_low(a) == pytest.approx(9.0, abs=0.1)
    assert budget.width_low(_h(drive_motor="n20", wheel_dia=28)) > budget.width_low(_h(drive_motor="n10", wheel_dia=28))


def test_counts_are_large_but_pruned():
    full = 1
    for v in H.AXES.values():
        full *= len(v)
    n = sum(H.count_by_weapon().values())
    assert 10_000 < n < full / 100


def test_slug_unique_over_sample():
    hs = list(itertools.islice(H.enumerate_hypotheses({"weapon": "wedge"}), 500))
    assert len({h.slug for h in hs}) == len(hs)

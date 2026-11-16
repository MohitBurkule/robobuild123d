"""Selectable rules profiles (E4, robot/profiles/*.json): loading, validation, drift."""

import dataclasses
import json
from pathlib import Path

import pytest

from robot import profile


def test_available_lists_shipped_profiles():
    names = profile.available()
    assert "aws2025" in names and "dev" in names and "strict" in names


def test_named_empty_is_aws2025_defaults():
    p = profile.named("")
    assert p.name == "aws2025" and p.roller_mass_g == 150.0


def test_named_overrides_thresholds():
    d = profile.named("dev")
    s = profile.named("strict")
    assert d.min_wall_fdm_mm < 0.9 < s.min_wall_fdm_mm
    assert d.contact_tol_mm > s.contact_tol_mm
    assert d.name == "dev" and s.name == "strict"


def test_legality_numbers_are_strict_in_every_profile():
    for n in profile.available():
        p = profile.named(n)
        assert p.roller_mass_g == 150.0 and p.footprint_mm == 150.0
        assert p.max_tip_speed_mph == 600.0
        assert p.require_locking_bar and p.require_tool_free_switch


def test_unknown_profile_lists_available():
    with pytest.raises(ValueError, match="aws2025"):
        profile.named("nope")


def test_unknown_key_rejected():
    bad = Path(profile.DIR) / "_bad.json"
    bad.write_text(json.dumps({"min_wall_fdm_mm": 1.0, "min_walll_fdm_mm": 2.0}))
    try:
        with pytest.raises(ValueError, match="min_walll_fdm_mm"):
            profile.named("_bad")
    finally:
        bad.unlink()


def test_tuple_fields_become_tuples():
    p = profile.named("dev")
    assert isinstance(p.wedge_gap_mm, tuple) and len(p.wedge_gap_mm) == 2


def test_aws2025_json_matches_dataclass_defaults():
    """Drift: the canonical profile file and the Profile() defaults must say the same thing."""
    d = json.loads((profile.DIR / "aws2025.json").read_text())
    p = profile.Profile()
    for f in dataclasses.fields(profile.Profile):
        got = d[f.name]
        want = list(getattr(p, f.name)) if isinstance(getattr(p, f.name), tuple) else getattr(p, f.name)
        assert got == want, f"aws2025.json {f.name}={got} but Profile default is {want}"


def test_every_shipped_profile_loads_and_has_description():
    for n in profile.available():
        assert profile.description(n)
        profile.named(n)  # no raise

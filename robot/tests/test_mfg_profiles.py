"""Printer/filament profiles (robot/mfg_profiles.py): capability, bed fit, hole compensation."""

import pytest

from robot import mfg_profiles as mp


def test_pla_prints_anywhere():
    assert mp.capability("pla", "ender3") == []


def test_pa6_cf_needs_enclosure_hardened_and_dry():
    reasons = mp.capability("pa6_cf", "ender3")
    assert any("enclosed" in r for r in reasons)
    assert any("hardened" in r for r in reasons)
    assert mp.capability("pa6_cf", "bambu_x1c") == []


def test_tpu_needs_direct_drive():
    assert any("direct drive" in r for r in mp.capability("tpu", "ender3"))
    assert mp.capability("tpu", "voron_24") == []


def test_nozzle_temp_limit():
    assert any("tops out" in r for r in mp.capability("pa6_cf", "prusa_mk4"))


def test_bed_fit():
    assert mp.bed_fit("ender3", (100, 100, 40)) is True
    assert mp.bed_fit("ender3", (250, 100, 40)) is False
    assert mp.bed_fit("ender3", (100, 100, 260)) is False
    assert mp.bed_fit("voron_24", (250, 100, 40)) is True


def test_hole_compensation_varies():
    assert mp.hole_compensation("ender3") > 0


def test_unknown_ids_raise():
    with pytest.raises(KeyError):
        mp.printer("nope")
    with pytest.raises(KeyError):
        mp.filament("nope")

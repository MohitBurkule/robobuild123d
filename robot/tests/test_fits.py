"""Named fits (robot/fits.py): FDM compensation, bands, and the check() verdicts."""

import pytest

from robot import fits


def test_fdm_bearing_press_compensates_tight():
    d = fits.cad_diameter("bearing_press", 8.0, "fdm")
    assert 8.05 <= d <= 8.15


def test_cnc_gets_no_compensation():
    assert fits.cad_diameter("screw_clear", 3.2, "cnc") == 3.2


def test_heatset_pilot_is_under_nominal():
    assert fits.cad_diameter("heatset_m3", 3.2, "fdm") < 3.2


def test_band_and_check_round_trip():
    lo, hi = fits.band("shaft_running", 3.0, "fdm")
    okd, lo2, hi2, why = fits.check("shaft_running", 3.0, (lo + hi) / 2, "fdm")
    assert okd and lo2 == lo and hi2 == hi


def test_check_flags_tight_and_loose():
    okd, lo, hi, why = fits.check("bearing_press", 8.0, 7.9, "fdm")
    assert not okd and "tight" in why
    okd, _lo, _hi, why = fits.check("bearing_press", 8.0, 8.4, "fdm")
    assert not okd and "loose" in why


def test_unknown_fit_and_process_raise():
    with pytest.raises(KeyError):
        fits.cad_diameter("nope", 1.0)
    with pytest.raises(KeyError):
        fits.cad_diameter("screw_clear", 3.2, "waterjet")


def test_every_fit_has_kind_band_and_note():
    for name, f in fits.FITS.items():
        assert f.kind in fits.BAND_MM and f.note, name


def test_every_fit_is_tested_by_name_here():
    assert set(fits.FITS) >= {"bearing_press", "bearing_slip", "shaft_running", "shaft_press", "screw_clear",
                              "self_tap_plastic", "heatset_m3", "axle_dflat_n20", "pocket_snug", "pocket_loose"}

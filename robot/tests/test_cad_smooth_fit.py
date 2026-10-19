import math

import build123d as bd
import numpy as np
import pytest
import shapely.geometry as sg
from scipy.spatial import cKDTree

from robot.cad import fit, smooth

CTRL6 = [[14, 0], [9, 8], [-6, 9], [-15, 1], [-7, -8], [8, -7]]


def test_fit_recovers_known_spline():
    dense = fit.bspline_eval(CTRL6, True, 500)
    f = fit.fit_bspline(dense, rms_target=0.02)
    assert f["n_ctrl"] <= 6 and f["rms"] <= 0.02
    got = fit.bspline_eval(f["ctrl"], True, 2000)
    assert cKDTree(got).query(dense)[0].max() < 0.05


def test_fit_open_curve_endpoints_and_cap():
    x = np.linspace(0, 40, 300)
    y = 6 * np.sin(x / 40 * math.pi) + 0.02 * x
    f = fit.fit_bspline(np.column_stack([x, y]), closed=False, max_ctrl=20, rms_target=0.01)
    assert f["n_ctrl"] <= fit.MAX_CTRL  # capped: a sketch, not a copy
    assert f["ctrl"][0] == [0.0, 0.0] and f["ctrl"][-1] == pytest.approx([40, 0.8], abs=1e-3)
    assert f["rms"] < 0.3


def test_fit_noisy_ellipse_meets_target_with_few_points():
    rng = np.random.default_rng(1)
    th = np.linspace(0, 2 * math.pi, 400, endpoint=False)
    P = np.column_stack([20 * np.cos(th), 9 * np.sin(th)]) + rng.normal(0, 0.05, (400, 2))
    f = fit.fit_bspline(P)
    assert f["rms"] <= 0.3 and f["n_ctrl"] <= 8


def test_segments_lines_and_fillets():
    poly = np.array(sg.box(-10, -5, 10, 5).buffer(2, quad_segs=32).exterior.coords)
    seg = fit.segments(poly)
    assert sum(s["type"] == "line" for s in seg) == 4 and sum(s["type"] == "arc" for s in seg) == 4
    assert all(abs(r - 2) < 0.15 for r in fit.fillet_radii(poly))
    lines = sorted(s["length"] for s in seg if s["type"] == "line")
    assert lines[0] == pytest.approx(10, abs=1.0) and lines[-1] == pytest.approx(20, abs=1.0)


def test_segments_circle_radius():
    th = np.linspace(0, 2 * math.pi, 200, endpoint=False)
    seg = fit.segments(np.column_stack([7 * np.cos(th), 7 * np.sin(th)]))
    assert [s["type"] for s in seg] == ["arc"] and seg[0]["radius"] == pytest.approx(7, abs=0.02)


def _loft_from_fit():
    th = np.linspace(0, 2 * math.pi, 300, endpoint=False)
    f = fit.fit_bspline(np.column_stack([12 * np.cos(th), 7 * np.sin(th)]))
    return smooth.loft_stations([smooth.Station(z, {"type": "bspline", "ctrl": (np.array(f["ctrl"]) * (1 - z / 60)).tolist()})
                                 for z in (0, 10, 20, 30)])


def test_loft_from_fitted_params_is_smooth_solid():
    s = _loft_from_fit()
    assert s.is_valid and s.volume > 0
    m = smooth.smoothness(s)
    assert m["steps"] == 0 and m["max_crease_deg"] < 20 and m["profile_curvature_max"] < 0.5


def test_stacked_extrusions_flagged_as_steps():
    ps = [bd.Pos(0, 0, 10 * i) * bd.extrude(bd.Ellipse(12 * (1 - i / 6), 7 * (1 - i / 6)), 10) for i in range(3)]
    m = smooth.smoothness(ps[0] + ps[1] + ps[2])
    assert m["steps"] >= 2 and m["max_crease_deg"] > 60 and m["profile_curvature_max"] > 2


def test_mixed_profiles_and_fillet():
    st = [smooth.Station(0, {"type": "rounded_rect", "w": 20, "h": 10, "r": 3}),
          smooth.Station(15, {"type": "ellipse", "rx": 8, "ry": 4}),
          smooth.Station(25, {"type": "ellipse", "rx": 5, "ry": 3, "center": [2, 0]})]
    s = smooth.loft_stations(st)
    assert s.is_valid
    f, ok = smooth.fillet_all(s, 1.0)
    assert f.is_valid and (not ok or f.volume < s.volume)


def test_sweep_along_path():
    s = smooth.sweep_profile({"type": "ellipse", "rx": 3, "ry": 2}, [(0, 0, 0), (10, 0, 5), (20, 5, 8)])
    assert s.is_valid and s.volume > 0

"""mfg.layer_load only applies to printed parts that wrap the weapon axle (bore, seat, clamp), not to parts that merely
pass within 8 mm of the axle line (e.g. a wedglet nose under the disc)."""

import numpy as np

from robot.checks.process import surrounds_axis


def _ring(r, n=36):
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.c_[np.zeros(n), r * np.cos(a), r * np.sin(a)]


def test_bore_round_the_axle_surrounds_it():
    q = _ring(4.0)
    assert surrounds_axis(q, q[:, 0], [1.0, 0.0, 0.0])


def test_part_below_the_axle_does_not():
    q = np.array([[x, y, -6.5] for x in (0.0, 2.0) for y in (-3.0, 0.0, 3.0)])
    assert not surrounds_axis(q, q[:, 0], [1.0, 0.0, 0.0])


def test_three_quarter_clamp_counts_half_does_not():
    q = _ring(4.0)
    q = q[np.arctan2(q[:, 2], q[:, 1]) < np.pi / 2 + 0.01]  # 270 deg of a ring
    assert surrounds_axis(q, q[:, 0], [1.0, 0.0, 0.0])
    q2 = _ring(4.0)
    q2 = q2[(np.arctan2(q2[:, 2], q2[:, 1]) > 0.05) & (np.arctan2(q2[:, 2], q2[:, 1]) < np.pi - 0.05)]  # upper half only
    assert not surrounds_axis(q2, q2[:, 0], [1.0, 0.0, 0.0])

import numpy as np

from robot import fit_photo


def test_fit_recovers_proportions():
    p = {"w": 0.65, "h": 0.3, "ramp": 0.3, "disc_axis": None, "disc_r": 0.3, "disc_y": 0.5, "disc_t": 0.08}
    m = fit_photo._sil(fit_photo.envelope(p), (0.6, -0.5, -0.6), (0, 0, 1.0))
    sc, q = fit_photo.fit([m])
    assert sc > 0.9
    assert abs(q["w"] - 0.65) <= 0.16 and abs(q["h"] - 0.3) <= 0.1

"""Combat failure modes (robot/checks/threat): a good and a bad case for every CF-* mode on facts (fast, exact)."""

import pytest

from robot.checks import threat
from robot.checks.threat import rules as R
from robot.finding import BLOCKER, INFO, WARNING


def lip(**kw):
    d = {"id": "wedge", "kind": "wedge", "front": True, "ymax": 60.0, "gap": 0.3, "material": "steel", "metal": True, "printed": False,
         "U_j": 20.0, "backed": False, "x0": -40.0, "x1": 40.0, "width": 80.0, "hinged": False, "preload_n": 0.0, "deflection": 0.5,
         "alpha_deg": 15.0, "tip_r": 0.4, "chamfer_mm": 1.2, "tip_low": 0.3, "gap_floor": 0.3, "tip_w": 80.0, "side_chamfer": True,
         "replaceable": False, "E": 200000.0, "t_mid": 1.0, "overhang": 20.0}
    d.update(kw)
    return d


def fork(**kw):
    d = lip(id="fork_l", kind="fork", width=12.0, tip_w=12.0, x0=-20.0, x1=-8.0, material="tpu", metal=False, printed=True,
            E=30.0, t_mid=2.0, overhang=15.0)
    d.update(kw)
    return d


def base(**kw):
    T = {"family": "wedge", "bite_mm": 6.0, "vs01.step_mm": 1.0, "vs01.where": ("tub", 90, 0.0, None), "vs05.blunt_frac": 0.05,
         "hs01.vert_frac": 0.1, "hs02.exposed": [], "hs03.top_parts": [], "front_lips": [lip()], "lips": [lip()], "side_lips": [],
         "forks": [], "fork_open_mm": None, "mass_g": 150.0, "gap_p20.front": 0.3, "cog_h": 12.0, "half_x": 45.0, "half_y": 50.0,
         "weapon_vertical": False, "vs06.sf": None, "vs06.bolts": None, "ha01.min_cap_j": 8.0, "ha01.where": "lid", "ha02.bad": [],
         "n_routes": 3, "n_wires": 3, "ha03.min_mm": (6.0, "w1"), "wl01.win_front": 0.9, "wl01.ref_mm": 0.3, "wl02.com_rear_frac": 0.45,
         "wl02.lift_j": 0.05, "wl03.pocket": (2.0, "top"), "wl04.defl_mm": 0.5, "wl04.gap_mm": 3.0, "wl04.plate": "lid", "self_right": True,
         "mu": 1.1, "driven_share": 0.95, "stall_torque_gcm": [3000.0, 3000.0], "wheel_dia": 30.0, "gap_med.front": 0.5,
         "gap_med.left": 1.0, "gap_med.right": 1.0, "wheel_max_x": 38.0, "body_max_x": 42.0, "wheel_min_x": -38.0, "body_min_x": -42.0,
         "wheel_front_y": 20.0, "body_front_y": 60.0, "wheel_rear_y": -30.0, "body_rear_y": -40.0, "motor_rpm": 1000.0,
         "ar03.trapped": [], "ld01.min": (2.0, "tub", 3.0), "wheel_y": [40.0], "ld02.worst": (5.0, "wl", 6.0, 3.0), "ld03.loose": [],
         "db01.bad": [], "db02.bad": [], "db03.visible": [], "db04.open": [], "db05.visible": [], "db06.grooved": [],
         "st01.min": (2.0, "tub", 0.4), "st02.thin": [], "st03.sharp": [], "st04.min": (2.0, "b1"), "st05.brittle": [],
         "st06.min": (3.0, "tub", "front-rear", 0.0), "gd01.alive_frac": 0.9, "gd01.n_hits": 50, "gd02.min_mm": (12.0, "w1"),
         "gd03.depth": (15.0, "battery"), "gd04.depth": (12.0, "rx"), "gd04.caged": [], "gd05.per_side": (2, 2),
         "gd06": ("sw", 2.0, False), "gd07.short": [], "n_weapons": 1, "gd08.min": (8.0, "w1", "disc", None), "gd09.hard": [],
         "wheelbase_wheels": 60.0, "ow01.min": (4.0, "disc", 5.0), "ow02.ratio": 1.5, "ow03.unflanged": [], "ow04.supports": [("disc", 2)],
         "ow05.battery_held": True}
    T.update(kw)
    return T


TWO_FORKS = [fork(), fork(id="fork_r", x0=8.0, x1=20.0)]
# mode id -> (good overrides, bad overrides)
CASES = {
    "CF-VS01": ({}, {"vs01.step_mm": 8.0}),
    "CF-VS02": ({}, {"front_lips": [lip(U_j=4.0)]}),
    "CF-VS03": ({"forks": TWO_FORKS, "fork_open_mm": 6.0}, {"forks": TWO_FORKS, "fork_open_mm": 16.0}),
    "CF-VS04": ({}, {"mass_g": 60.0, "gap_p20.front": 12.0}),
    "CF-VS05": ({}, {"vs05.blunt_frac": 0.4}),
    "CF-VS06": ({"weapon_vertical": True, "vs06.sf": (3.0, "up"), "vs06.bolts": (2, "up")},
                {"weapon_vertical": True, "vs06.sf": (1.2, "up"), "vs06.bolts": (1, "up")}),
    "CF-HS01": ({}, {"hs01.vert_frac": 0.6}),
    "CF-HS02": ({}, {"hs02.exposed": [0, 5, 10]}),
    "CF-HS03": ({}, {"hs03.top_parts": ["power_switch"]}),
    "CF-HS04": ({}, None),  # info report only: always passes
    "CF-HS05": ({}, {"lips": [lip(hinged=True)]}),
    "CF-HA01": ({}, {"ha01.min_cap_j": 1.0}),
    "CF-HA02": ({}, {"ha02.bad": [("battery", "lid", 3.0, 1.0)]}),
    "CF-HA03": ({}, {"ha03.min_mm": (2.0, "w1")}),
    "CF-WL01": ({}, {"wl01.win_front": 0.2}),
    "CF-WL02": ({}, {"wl02.com_rear_frac": 0.8}),
    "CF-WL03": ({}, {"wl03.pocket": (12.0, "left side")}),
    "CF-WL04": ({}, {"wl04.defl_mm": 6.0}),
    "CF-WL05": ({}, {"self_right": False}),
    "CF-WL06": ({}, {"mu": 0.3}),
    "CF-WL07": ({}, {"gap_med.left": 4.0}),
    "CF-AR01": ({}, {"wheel_max_x": 45.0}),
    "CF-AR02": ({}, None),
    "CF-AR03": ({}, {"ar03.trapped": ["left side"]}),
    "CF-LD01": ({}, {"ld01.min": (0.5, "tub", 1.2)}),
    "CF-LD02": ({}, {"ld02.worst": (1.0, "wl", 40.0, 2.0)}),
    "CF-LD03": ({}, {"ld03.loose": [("battery", ["+z"])]}),
    "CF-DB01": ({}, {"db01.bad": [(4.0, "wl", 90)]}),
    "CF-DB02": ({}, {"db02.bad": [(5.0, "disc", 270)]}),
    "CF-DB03": ({}, {"db03.visible": ["belt_l"]}),
    "CF-DB04": ({}, {"db04.open": ["rx"]}),
    "CF-DB05": ({}, {"db05.visible": ["motor_l"]}),
    "CF-DB06": ({}, {"db06.grooved": ["tyre_l"]}),
    "CF-ST01": ({}, {"st01.min": (0.6, "tub", 0.4)}),
    "CF-ST02": ({}, {"st02.thin": [(1.2, "tub", 2.5)]}),
    "CF-ST03": ({}, {"st03.sharp": [(40, "tub")]}),
    "CF-ST04": ({}, {"st04.min": (0.8, "b1")}),
    "CF-ST05": ({}, {"st05.brittle": ["tub"]}),
    "CF-ST06": ({}, {"st06.min": (0.5, "tub", "front-rear", 3.0)}),
    "CF-GD01": ({}, {"gd01.alive_frac": 0.5}),
    "CF-GD02": ({}, {"gd02.min_mm": (3.0, "w_bat")}),
    "CF-GD03": ({}, {"gd03.depth": (2.0, "battery")}),
    "CF-GD04": ({}, {"gd04.caged": ["rx"]}),
    "CF-GD05": ({}, {"gd05.per_side": (1, 1)}),
    "CF-GD06": ({}, {"gd06": ("sw", -1.0, True)}),
    "CF-GD07": ({}, {"gd07.short": ["w1"]}),
    "CF-GD08": ({}, {"gd08.min": (1.0, "w1", "disc", None)}),
    "CF-GD09": ({}, {"gd09.hard": ["esc"]}),
    "CF-AS01": ({}, {"front_lips": [lip(alpha_deg=45.0)]}),
    "CF-AS02": ({}, {"front_lips": [lip(chamfer_mm=0.0)]}),
    "CF-AS03": ({}, {"front_lips": [lip(tip_r=0.01, width=1.0)], "driven_share": 0.2}),
    "CF-AS04": ({"forks": [fork()]}, {"forks": [fork(tip_w=4.0, tip_r=0.3)]}),
    "CF-AS05": ({"side_lips": [lip(id="sk", front=False)]}, {"side_lips": [lip(id="sk", front=False, side_chamfer=False)]}),
    "CF-AS06": ({}, {"wheelbase_wheels": 20.0}),
    "CF-AS07": ({"forks": TWO_FORKS, "fork_open_mm": 0.0}, {"forks": [fork(), fork(id="fork_r", x0=40.0, x1=52.0)], "fork_open_mm": 30.0}),
    "CF-AS08": ({}, {"front_lips": [lip(metal=False, material="petg")]}),
    "CF-OW01": ({}, {"ow01.min": (-2.0, "disc", 5.0)}),
    "CF-OW02": ({}, {"ow02.ratio": 0.8}),
    "CF-OW03": ({}, {"ow03.unflanged": ["pulley_a"]}),
    "CF-OW04": ({}, {"ow04.supports": [("disc", 1)]}),
    "CF-OW05": ({}, {"ow05.battery_held": False}),
}


def test_every_mode_has_a_rule_and_cases():
    assert len(threat.MODES) == 61
    assert set(threat.MODES) == set(R.RULES) == set(CASES)


def test_catalogue_severities():
    assert threat.MODES["CF-GD08"]["severity"] == "blocker" and threat.MODES["CF-OW01"]["severity"] == "blocker"
    assert threat.judge("CF-GD08", base(**CASES["CF-GD08"][1]))[0] == BLOCKER
    assert threat.judge("CF-OW01", base(**CASES["CF-OW01"][1]))[0] == BLOCKER
    assert threat.judge("CF-VS01", base(**CASES["CF-VS01"][1]))[0] == WARNING
    assert threat.judge("CF-DB04", base(**CASES["CF-DB04"][1]))[0] == INFO


@pytest.mark.parametrize("mid", sorted(CASES))
def test_mode_good_and_bad(mid):
    good, bad = CASES[mid]
    sev, st, msg, *_ = threat.judge(mid, base(**good))
    assert st is True, (mid, msg)
    if bad is not None:
        sev, st, msg, *_ = threat.judge(mid, base(**bad))
        assert st is False, (mid, st, msg)


def test_launch_apex_escalates_to_warning():
    sev, st, msg, *_ = threat.judge("CF-VS04", base(mass_g=40.0, **{"gap_p20.front": 12.0}))
    assert st is False and sev == WARNING, msg


def test_missing_routes_are_not_checked_not_passed():
    for mid in ("CF-GD08", "CF-HA03", "CF-GD02", "CF-GD07"):
        _, st, *_ = threat.judge(mid, base(n_routes=0))
        assert st == R.SKIP, mid


def test_missing_data_is_not_a_pass():
    _, st, *_ = threat.judge("CF-WL06", base(mu=None))
    assert st is None

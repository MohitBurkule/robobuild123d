"""Scythe variants: each swaps ONE setting, and params re-derives the bar, track and tub from it. UNTESTED.

  rules=aws_v43_cube : 101.6 mm cube envelope (AWS v4.3 2b) instead of the default robot/profile.py 150 mm square.
                       Bar comes out 90 mm (tyre-clearance limited), track widens to 83.6 mm.
  3s                 : gnb_3s_300_80c_hv pack (+12 g). The mass relation shortens the bar to ~77 mm, so stored
                       energy DROPS (~52 J vs ~82 J on 2S at 150 mm square): 2S is the default for a reason.
  dual               : bbb_dual_esc_v31 drive ESC instead of the Malenki-Nano (separate receiver then needed).
  dead               : dead-shaft risk mitigation - fixed M5 12.9 bolt from the top panel through the motor, bar + hub
                       on two MR85 (revron weapon_motor.pick_bearing(5.0)), driven by the bell. Not modelled.
Both envelope and battery are read by params at import (env SCYTHE_RULES / SCYTHE_BATTERY), so set_variants
sets them and reloads params; modules that did `from . import params as P` see the reloaded values.
"""
import importlib
import os

from . import params as P

ENV = {"aws_v43_cube": ("SCYTHE_RULES", "aws_v43_cube"), "3s": ("SCYTHE_BATTERY", "gnb_3s_300_80c_hv")}
SIMPLE = {"dual": {"DRIVE_RX": "bbb_dual_esc_v31"}}


def set_variants(*names):
    for n in names:
        if n in ENV:
            k, v = ENV[n]
            os.environ[k] = v
    importlib.reload(P)
    for n in names:
        for k, v in SIMPLE.get(n, {}).items():
            setattr(P, k, v)
    return P

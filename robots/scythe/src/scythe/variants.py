"""Scythe variants (cf. revron/variants.py set_variants): swap catalogue ids only, geometry follows. UNTESTED.

  3s   : gnb_3s_300_80c_hv pack (+12 g): ~1.5x rpm, ~84 J, tip ~314 mph (< 600 mph rule); est. 144 g total,
         fits the 150 g budget with ~6 g margin (BRIEF mass table).
  dual : bbb_dual_esc_v31 drive ESC instead of the Malenki-Nano (separate receiver then needed).
  dead : dead-shaft risk mitigation - a fixed M5 12.9 bolt from the top panel through the motor, bar + hub on a pair
         of MR85 (revron weapon_motor.pick_bearing(5.0)), driven by the bell through the hub pins. Not modelled.
"""
from . import params as P

VARIANTS = {
    "3s": {"BATTERY": P.BATTERY_3S},
    "dual": {"DRIVE_RX": "bbb_dual_esc_v31"},
}


def set_variants(*names):
    for n in names:
        for k, v in VARIANTS[n].items():
            setattr(P, k, v)

"""Undertow one-line settings. Every swap the brief asks for is ONE key here; nothing else in the package changes.

Read once at import from the env var UNDERTOW_SETTINGS (JSON object), so `build_undertow.py --set front=plough` can set it
before `undertow` is imported. UNTESTED: never built, run, rendered or verified.
"""
import json
import os

DEFAULTS = dict(
    front="forks",                 # "forks" (hinged sheet-steel forks on the common pin) | "plough" (TPU wedge + steel face, same pin)
    motor="bbb_n10_1000rpm",       # robot/cots_alts.py GEARMOTORS id; "bbb_n10_600rpm" is the slower, harder-pushing variant
    wheel="bbb_wheel_22x10",       # robot/cots_alts.py WHEELS id; "durahubs_25" is the grippier, larger alternative
    esc="bbb_dual_esc_v31",        # robot/cots_alts.py ESCS id; "bbb_malenki_nano" is lighter but 1 A/channel (see BRIEF.md risks)
    rx="rx_fs_ia6_decased",        # robot/catalog.py builtin receiver; ignored when the esc has a built-in receiver
    battery="tattu_2s_300_75c_hv", # robot/cots_alts.py BATTERIES id
    switch="fingertech_mini_switch",
)
ESC_WITH_RX = ("bbb_malenki_nano",)   # ESC ids that carry their own receiver (catalog name: "receiver + 3x 1 A brushed ESC")


def current():
    s = dict(DEFAULTS)
    raw = os.environ.get("UNDERTOW_SETTINGS")
    if raw:
        user = json.loads(raw)
        unknown = set(user) - set(DEFAULTS)
        if unknown:
            raise KeyError(f"unknown Undertow settings {sorted(unknown)}; known: {sorted(DEFAULTS)}")
        s.update(user)
    if s["front"] not in ("forks", "plough"):
        raise ValueError(f"front must be forks | plough, not {s['front']!r}")
    return s


SETTINGS = current()

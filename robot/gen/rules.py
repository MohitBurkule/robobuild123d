"""Compatibility rules that prune the hypothesis space. Each rule is a small named function over the axes it `needs`.

A rule returns None when the (partial) hypothesis is fine, or a short reason string when it is not. The enumerator runs each rule
as soon as all its axes are bound, pruning early.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Callable

from . import budget
from .hypothesis import MUST_INVERT, WEAPON_CLASSES


@dataclass(frozen=True)
class Rule:
    name: str
    needs: tuple
    fn: Callable

    def check(self, h) -> str | None:
        return self.fn(h if not isinstance(h, dict) else SimpleNamespace(**h))


RULES: list[Rule] = []


def rule(*needs):
    def deco(fn):
        RULES.append(Rule(fn.__name__, tuple(needs), fn))
        return fn
    return deco


def _wc(h):
    return WEAPON_CLASSES[h.weapon]


@rule("weapon", "mount")
def weapon_mount(h):
    return None if h.mount in _wc(h).mounts else f"{h.weapon} does not mount {h.mount}"


@rule("weapon", "orientation")
def weapon_orientation(h):
    return None if h.orientation in _wc(h).orientations else f"{h.weapon} is not {h.orientation}"


@rule("weapon", "attachment")
def weapon_attachment(h):
    return None if h.attachment in _wc(h).attachments else f"{h.weapon} cannot be driven by {h.attachment}"


@rule("weapon", "front")
def weapon_front(h):
    return None if h.front in _wc(h).fronts else f"{h.weapon} does not pair with a {h.front} front"


@rule("mount", "orientation")
def vertical_not_under(h):
    return "a vertical weapon cannot sit under the robot" if (h.mount == "under" and h.orientation == "vertical") else None


@rule("weapon", "drive_layout")
def walker_drive(h):
    walkers = {"gyro_walker": "gyro_walker", "walker_shuffler": "shuffle", "meltybrain": "melty"}
    need = walkers.get(h.weapon)
    if need:
        return None if h.drive_layout == need else f"{h.weapon} needs {need} drive"
    return f"{h.drive_layout} drive is only for walkers/melty" if h.drive_layout in ("gyro_walker", "shuffle", "melty") else None


@rule("drive_layout", "transmission")
def belt_needs_axles(h):
    if h.transmission == "belt" and h.drive_layout in ("2WD", "2WD_skid", "melty", "shuffle", "gyro_walker"):
        return "a belt drive needs a second axle to drive"
    return None


@rule("drive_layout", "drive_motor", "wheel_dia")
def wheel_size_for_motor(h):
    if h.drive_motor == "n20" and h.wheel_dia < 20:
        return "an N20 gearbox (12 mm) needs a wheel of 20 mm or more for floor clearance"
    if h.drive_motor == "n10" and h.wheel_dia < 16:
        return "an N10 gearbox needs a 16 mm wheel or more"
    if h.drive_layout in ("6WD", "8WD") and h.wheel_dia > 25:
        return "6/8WD only fit in 150 mm with wheels of 25 mm or less"
    return None


@rule("wheel_guards", "invertible", "wheel_dia")
def invertible_wheels(h):
    if h.invertible and h.wheel_dia < 20:
        return "invertible drive needs wheels that stand proud of a body at least 12 mm tall"
    return None


@rule("battery", "drive_motor")
def battery_voltage(h):
    if h.battery == "lipo_1s_300" and h.drive_motor == "n10":
        return "1S (3.7 V) runs a 6 V N10 at too low speed"
    return None


@rule("battery", "weapon")
def battery_for_weapon(h):
    wc = _wc(h)
    if wc.actuator == "brushless" and h.battery == "lipo_1s_300":
        return "a brushless weapon needs 2S"
    return None


@rule("weapon", "weapon_esc")
def weapon_esc_matches(h):
    wc = _wc(h)
    if wc.actuator == "brushless":
        return None if h.weapon_esc != "none" else "a brushless weapon needs a brushless ESC"
    return None if h.weapon_esc == "none" else "only brushless weapons carry a weapon ESC"


@rule("drive_esc", "rx")
def receiver_integration(h):
    integrated = h.drive_esc == "c_malenki_nano_antweight_esc_receiver"
    if integrated and h.rx != "integrated":
        return "the Malenki-Nano already is the receiver"
    if not integrated and h.rx == "integrated":
        return "this ESC has no receiver built in"
    return None


@rule("drive_layout", "drive_esc")
def esc_channels(h):
    if budget.N_DRIVEN[h.drive_layout] > 4 and h.drive_esc == "esc_dual_brushed":
        return "6+ motors exceed a small dual brushed ESC (2.5 A)"
    return None


@rule("weapon", "drive_esc", "battery")
def servo_on_2s(h):
    if _wc(h).actuator == "servo" and h.battery == "lipo_1s_300":
        return "an HV servo weapon wants 2S"
    return None


@rule("weapon", "invertible")
def weapon_invertible(h):
    if h.weapon in MUST_INVERT and not h.invertible:
        return "full-body spinners are symmetric and must run inverted"
    return None


@rule(*tuple(["weapon", "front", "drive_layout", "drive_motor", "wheel_dia", "transmission", "wheel_guards", "battery",
              "drive_esc", "weapon_esc", "rx"]))
def mass_budget(h):
    m = budget.mass_low(h)
    return f"lightest build {m:.0f} g exceeds {budget.MASS_LIMIT_G:.0f} g" if m > budget.MASS_LIMIT_G else None


@rule("weapon", "mount", "front", "drive_layout", "drive_motor", "wheel_dia", "wheel_guards")
def size_budget(h):
    w, l = budget.width_low(h), budget.length_low(h)
    if max(w, l) > budget.SIZE_LIMIT_MM:
        return f"needs {w:.0f} x {l:.0f} mm, more than the {budget.SIZE_LIMIT_MM:.0f} mm square"
    return None


def violations(h, rules=RULES) -> list[tuple[str, str]]:
    """All (rule, reason) pairs a complete hypothesis breaks."""
    out = []
    for r in rules:
        msg = r.check(h)
        if msg:
            out.append((r.name, msg))
    return out

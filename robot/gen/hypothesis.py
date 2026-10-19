"""The hypothesis space: every axis a 150 g antweight design is chosen along, enumerated with pruning.

A `Hypothesis` is one point (one value per axis). `enumerate_hypotheses()` walks the axes in `AXIS_ORDER` and drops a
partial assignment as soon as a rule from `rules.RULES` whose axes are all bound rejects it, so the full product
(billions) is never materialised. Value lists follow `data/antweight_taxonomy.json` (research pass, 36 real robots);
`TAXONOMY_ALIASES` maps the taxonomy's spellings to the short axis values used here.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).parent / "data" / "antweight_taxonomy.json"

# Weapon types (taxonomy `weapon_type`, normalised: parentheses dropped, long names shortened).
WEAPONS = (
    "none_pusher", "wedge", "lifter", "lifting_wedge", "flipper", "grabber_clamp", "crusher", "hspin_bar", "hspin_disc",
    "hspin_shell", "hspin_ring", "undercutter", "vspin_disc", "vspin_drum", "vspin_eggbeater", "vspin_drisk", "hammer_axe",
    "overhead_saw", "full_body_spinner", "meltybrain", "expandabot", "walker_shuffler", "flail_or_other", "air_blower",
    "pneumatic_flipper", "passive_scoop_loader", "gyro_walker", "counter_gyro_vspin", "drone_arm",
)
MOUNTS = ("none", "front", "top", "centre", "rear", "under", "side", "full_body")
ORIENTATIONS = ("none", "flat", "slanted", "vertical")
ATTACHMENTS = ("none", "hub_motor", "drisk", "shaft_bearings", "belt", "direct", "servo_horn", "servo_linkage", "gear_train")
FRONTS = ("none", "wedge", "wedgelets", "forks", "skirt", "plow", "weapon_is_front")
DRIVE_LAYOUTS = ("2WD", "2WD_skid", "4WD", "4WD_skid", "6WD", "8WD", "oring_track", "rotating_pods", "shuffle", "melty",
                 "gyro_walker")
DRIVE_MOTORS = ("n10", "n20")
WHEEL_DIAS = (16, 20, 22, 25, 28, 30, 34, 40)
TRANSMISSIONS = ("direct", "belt")
BATTERIES = ("lipo_2s_180", "lipo_2s_350", "lipo_1s_300", "c_typical_2s_300mah_lipo_lihv_betafpv_tbs_")
DRIVE_ESCS = ("esc_dual_brushed", "c_malenki_nano_antweight_esc_receiver", "c_bbb_antweight_dual_esc_v3_1")
WEAPON_ESCS = ("none", "c_bbb_antweight_spinner_brushless_esc", "esc_brushless_12a")
RECEIVERS = ("rx_fs_ia6_decased", "integrated")
# chassis construction: two printed halves split at the axle plane, or an open tub (walls + floor ribs) closed by a
# screwed base panel below and a top sheet above, with standoff-mounted weapon uprights (Revron)
CHASSIS = ("clamshell", "tub")
# disc weapons: one disc, or a spider bolted to the bell carrying two floating discs (RVRN 2.0)
DISC_STACKS = ("single", "spider_pair")
# ground game beyond the front: a low ramped skirt round the sides and rear (so a wedge, fork or lifter arriving from any
# bearing meets a lip at the floor, not a 4 mm door under the belly), the rear only, or none
SKIRTS = ("sides_rear", "rear", "none")

AXES = {
    "weapon": WEAPONS, "mount": MOUNTS, "orientation": ORIENTATIONS, "attachment": ATTACHMENTS, "front": FRONTS,
    "drive_layout": DRIVE_LAYOUTS, "drive_motor": DRIVE_MOTORS, "wheel_dia": WHEEL_DIAS, "transmission": TRANSMISSIONS,
    "wheel_guards": (True, False), "invertible": (True, False), "battery": BATTERIES, "drive_esc": DRIVE_ESCS,
    "weapon_esc": WEAPON_ESCS, "rx": RECEIVERS, "chassis": CHASSIS, "disc_stack": DISC_STACKS,
    "skirts": SKIRTS,
}
AXIS_ORDER = tuple(AXES)

# Taxonomy spelling -> axis value (prefix match, first hit wins).
TAXONOMY_ALIASES = {
    "flat_horizontal": "flat", "slanted_tilted": "slanted", "hub_motor": "hub_motor", "drisk": "drisk",
    "shaft_on_bearings": "shaft_bearings", "belt_drive": "belt", "direct_on_motor": "direct", "direct": "direct",
    "servo_horn": "servo_horn", "servo_linkage": "servo_linkage", "gearmotor_gear_train": "gear_train",
    "full_wedge": "wedge", "wedgelets": "wedgelets", "forks": "forks", "skirt_flexible": "skirt", "plow_scoop": "plow",
    "weapon_is_front": "weapon_is_front", "none": "none", "air_blower": "air_blower", "gyro_walker": "gyro_walker",
    "thagomiser_drone_arm": "drone_arm", "2WD+skid": "2WD_skid", "2WD_rear": "2WD", "2WD_centre": "2WD",
    "melty_2wheel": "melty", "rotating_drive_pods": "rotating_pods",
}
MUST_INVERT = ("hspin_shell", "hspin_ring", "full_body_spinner", "meltybrain")
# Friendly names accepted on the command line.
WEAPON_ALIASES = {
    "none": "none_pusher", "pusher": "none_pusher", "grabber": "grabber_clamp", "horizontal_spinner": "hspin_bar",
    "vertical_spinner_disc": "vspin_disc", "vertical_spinner_drum": "vspin_drum", "vertical_spinner_drisk": "vspin_drisk",
    "drisk": "vspin_drisk", "drum": "vspin_drum", "overhead_hammer": "hammer_axe", "hammer": "hammer_axe",
    "shell_spinner": "hspin_shell", "ring_spinner": "hspin_ring", "fbs": "full_body_spinner",
}


def normalise(value: str, allowed=None) -> str:
    """Map a taxonomy or friendly spelling onto an axis value (or return it unchanged)."""
    v = str(value).split("(")[0].strip()
    if v in WEAPON_ALIASES:
        return WEAPON_ALIASES[v]
    if allowed is not None and v in allowed:
        return v
    for k, out in TAXONOMY_ALIASES.items():
        if v.startswith(k):
            return out
    return v


@dataclass(frozen=True)
class WeaponClass:
    """What a weapon type allows: where it mounts, how it is oriented/attached, what front it pairs with."""

    mounts: tuple
    orientations: tuple
    attachments: tuple
    fronts: tuple
    actuator: str  # none | brushless | servo | gearmotor | drive | air
    weapon_mass_g: tuple  # (lo, hi) of weapon + actuator
    spinner: bool = False


_NOP = ("none",)
WEAPON_CLASSES = {
    "none_pusher": WeaponClass(_NOP, _NOP, _NOP, ("plow", "skirt", "wedge", "none"), "none", (0, 5)),
    "wedge": WeaponClass(_NOP, _NOP, _NOP, ("wedge", "wedgelets"), "none", (0, 10)),
    "lifter": WeaponClass(("front",), ("vertical",), ("servo_horn", "servo_linkage"), ("forks", "weapon_is_front", "wedge"), "servo", (15, 30)),
    "lifting_wedge": WeaponClass(("front",), ("slanted",), ("servo_horn",), ("wedge", "forks"), "servo", (15, 30)),
    "flipper": WeaponClass(("front", "rear"), ("vertical",), ("servo_linkage", "servo_horn"), ("forks", "wedgelets"), "servo", (15, 30)),
    "grabber_clamp": WeaponClass(("front", "top"), ("vertical",), ("servo_linkage", "gear_train"), ("forks", "wedge"), "servo", (20, 35)),
    "crusher": WeaponClass(("top", "front"), ("vertical",), ("servo_linkage", "gear_train"), ("wedge", "forks"), "servo", (20, 35)),
    "hspin_bar": WeaponClass(("front", "centre", "top"), ("flat", "slanted"), ("shaft_bearings", "hub_motor", "belt"), ("wedgelets", "skirt", "wedge"), "brushless", (40, 65), True),
    "hspin_disc": WeaponClass(("front", "centre"), ("flat",), ("hub_motor", "shaft_bearings"), ("wedgelets",), "brushless", (40, 65), True),
    "hspin_shell": WeaponClass(("full_body", "top"), ("flat",), ("hub_motor", "belt"), ("none",), "brushless", (60, 90), True),
    "hspin_ring": WeaponClass(("full_body",), ("flat",), ("belt",), ("none",), "brushless", (60, 90), True),
    "undercutter": WeaponClass(("front", "under"), ("flat", "slanted"), ("hub_motor", "shaft_bearings"), ("weapon_is_front",), "brushless", (40, 65), True),
    "vspin_disc": WeaponClass(("front", "centre"), ("vertical",), ("shaft_bearings", "belt"), ("wedgelets", "forks"), "brushless", (40, 60), True),
    "vspin_drum": WeaponClass(("front",), ("vertical",), ("hub_motor", "belt"), ("wedgelets", "forks"), "brushless", (40, 60), True),
    "vspin_eggbeater": WeaponClass(("front",), ("vertical",), ("belt", "shaft_bearings"), ("forks",), "brushless", (40, 60), True),
    "vspin_drisk": WeaponClass(("front",), ("vertical",), ("drisk", "hub_motor"), ("wedgelets", "skirt", "forks"), "brushless", (40, 60), True),
    "hammer_axe": WeaponClass(("top", "centre"), ("vertical",), ("servo_horn", "gear_train"), ("wedge", "wedgelets"), "servo", (25, 40)),
    "overhead_saw": WeaponClass(("top",), ("vertical",), ("direct",), ("wedge",), "brushless", (25, 40), True),
    "full_body_spinner": WeaponClass(("full_body",), ("flat",), ("hub_motor", "belt", "direct"), ("none",), "brushless", (60, 90), True),
    "meltybrain": WeaponClass(("full_body",), ("flat",), ("direct",), ("none",), "drive", (10, 25), True),
    "expandabot": WeaponClass(("top", "side", "front"), ("vertical", "flat"), ("servo_horn", "servo_linkage"), ("wedge", "forks", "none"), "servo", (15, 30)),
    "walker_shuffler": WeaponClass(_NOP, _NOP, _NOP, ("wedge", "none"), "none", (0, 10)),
    "flail_or_other": WeaponClass(("top", "rear"), ("flat", "vertical"), ("direct", "servo_horn"), ("wedge", "none"), "servo", (10, 30)),
    "air_blower": WeaponClass(("top", "rear"), ("vertical", "flat"), ("direct",), ("wedge", "none"), "brushless", (20, 35)),
    "pneumatic_flipper": WeaponClass(("front",), ("vertical",), ("servo_linkage",), ("forks", "wedge"), "air", (30, 50)),
    "passive_scoop_loader": WeaponClass(("front",), ("slanted", "flat"), ("shaft_bearings",), ("plow", "wedge"), "none", (5, 15)),
    "gyro_walker": WeaponClass(("full_body",), ("vertical",), ("direct",), ("none",), "brushless", (40, 70), True),
    "counter_gyro_vspin": WeaponClass(("front",), ("vertical",), ("shaft_bearings", "belt"), ("wedgelets", "forks"), "brushless", (45, 70), True),
    "drone_arm": WeaponClass(("top", "front"), ("flat", "slanted"), ("hub_motor",), ("wedge", "none"), "brushless", (30, 50), True),
}

# Weapon types the assembler (`build.py`) can turn into a full verified spec today.
BUILDABLE = {
    "none_pusher": {"front": ("wedge", "skirt", "plow"), "drive_layout": ("2WD",)},
    "wedge": {"front": ("wedge",), "drive_layout": ("2WD",)},
    "lifter": {"front": ("forks",), "attachment": ("servo_horn",), "drive_layout": ("2WD",)},
    "hspin_bar": {"front": ("wedgelets", "skirt", "wedge"), "mount": ("top",), "attachment": ("hub_motor",), "drive_layout": ("2WD",)},
    "vspin_drisk": {"front": ("forks", "wedgelets"), "mount": ("front",), "attachment": ("drisk",), "drive_layout": ("2WD", "4WD"),
                    "chassis": ("clamshell",), "disc_stack": ("single", "spider_pair")},
}
# ------------------------------------------------------------------------------------------------ ground game
# How each axis value plays the top threat class (get under, lift and throw): the opponent's wedge, fork, lifter or
# flipper wants to get under our lowest leading edge; a vertical spinner's tooth wants a step, hook or square face.
OPP_LIP_MM = (0.3, 0.5)  # a well-set opponent fork / acetate lip
GROUND_GAME = {
    "front": {
        "wedge": ("printed ramp, lip 0.6 mm off the floor, 1 mm thick at the edge: contests an opponent lip at 0.3-0.5 mm "
                  "and deflects a rising tooth up its face instead of taking it square", "printed nylon"),
        "skirt": ("TPU skirt drags on the floor and flexes over seams: wins the under-contest against rigid wedges that "
                  "must ride 0.5 mm high; loses to a sharp metal lip, which it rides up instead of snagging", "tpu"),
        "plow": ("V nose: deflects opponents sideways as well as up; printed lip at 0.6 mm contests", "printed nylon"),
        "forks": ("forks = a lightweight wedge: thin hard tines at 0.6 mm get under wedges with less mass than a full "
                  "ramp; the gap between tines is closed by the weapon so an opposing fork cannot slip in", "titanium"),
        "wedgelets": ("wedgelets either side of the disc: TPU ramps at 0.6 mm feed the opponent into the teeth and soak "
                      "up the disc's own debris; cheap, two screws each, replaced between fights", "tpu"),
    },
    "skirts": {
        "sides_rear": "low ramped skirt round the sides and rear, 0.5 mm off the floor and protruding 3 mm, so no bearing "
                      "has a door under the belly; its outer face slopes up 40 deg so a rising tooth glances off",
        "rear": "rear skirt only: the sides are left to the tyres and wells (accepted risk below)",
        "none": "no skirts beyond the front: a side or rear wedge gets under the belly (accepted risk below)",
    },
    "trade": ("against an opposing wedge, the lower lip wins: ours sits at 0.5-0.6 mm, a flexible acetate or TPU lip can "
              "sit on the floor and beat a rigid one; forks win by mass (more reach per gram) but leave tine gaps an "
              "opposing fork can enter, so the gaps are kept under the opponent's fork width or covered by the weapon"),
}


def ground_game(h: "Hypothesis") -> dict:
    """The hypothesis's statement of how it plays the ground game, and the lift-and-throw risks it accepts (by
    direction, `<dir>` = un-skirted there, `<dir>.bite` = an edge a tooth can catch there), each with its reason."""
    front, lip = GROUND_GAME["front"].get(h.front, (f"{h.front}: no ground-game statement", "?"))
    acc = {}
    if h.skirts in ("rear", "none"):
        for d in ("left", "right", "front_left", "front_right", "rear_left", "rear_right"):
            acc[d] = f"skirts={h.skirts}: the hypothesis leaves the sides to the wheels and wells"
    if h.skirts == "none":
        acc["rear"] = "skirts=none"
    if h.weapon == "vspin_drisk":
        acc["front"] = ("the disc is the front: it sweeps 2 mm above the floor between the forks/wedgelets, so a wedge "
                        "that reaches the gap under it meets the teeth (combat.R053 measures the sweep)")
        acc["front.bite"] = ("the uprights' undersides stand behind the disc: a tooth reaching them has already met our "
                             "disc; the uprights are the replaceable weapon module")
        for d in ("front_left", "front_right"):
            acc[d + ".bite"] = ("the upright feet flank the disc: a tooth reaching them past the corner wedgelet has "
                                "met the disc first; the uprights are spares (CF-OW04)")
    if h.front in ("wedge", "plow", "skirt"):
        for d in ("front_left", "front_right"):
            acc[d + ".bite"] = ("the ramp's underside at its outer corner, 3-5 mm up behind the 0.5 mm lip: a tooth must "
                                "pass under the lip first, and the ramp is the replaceable front part (CF-VS01)")
    if h.front == "plow":
        for d in ("front", "front_left", "front_right"):
            acc[d] = ("the V nose is swept back 25 deg: it trades a flat floor-skimming lip for deflecting opponents "
                      "into the wall; it loses the straight-on ground game to a flat wedge by design")
            acc[d + ".bite"] = acc[d]
    if h.weapon == "hspin_bar":
        for d in ("left", "right"):
            acc[d + ".bite"] = ("the top bridge of the bar module stands 10 mm up the side: the bar sweeps below it, so a "
                                "tooth reaching it has crossed our bar's arc first; the bridge is a bolt-on spare")
    if h.front in ("forks", "wedgelets"):
        for d in ("left", "right"):
            acc[d + ".bite"] = ("button heads on the outer tine roots of the replaceable sheet stand 1.3 mm proud: a "
                                "tooth that catches one bends a spare sheet, not the chassis (CF-AS04, CF-VS03)")
    if h.weapon == "lifter":
        for d in ("left", "right"):
            acc[d] = "the scoop cheeks swing outside the side walls: a side skirt would foul them; the cheeks cover the sides"
    return {"front": front, "lip_material": lip, "skirts": GROUND_GAME["skirts"][h.skirts],
            "trade": GROUND_GAME["trade"], "opponent_lip_mm": list(OPP_LIP_MM), "accepted": acc}


# options the generator builds but that do not verify clean yet: built only on request (user {"experimental": true}).
# chassis=tub (open tub + base panel + top sheet, uprights on standoffs): 6 blockers left on the 4WD drisk - 2.7 g over
# the limit, the upright neck flexes 1.1 mm (the verifier roots it at the foot contact, not at the standoff screws), the
# upper standoff screws' driver path crosses the disc, one 0.6 mm sliver at a rear corner.
EXPERIMENTAL = {"vspin_drisk": {"chassis": ("tub",)}}
# axes a weapon type must leave at the default when it is not listed above
DEFAULT_ONLY = {"chassis": "clamshell", "disc_stack": "single"}
# drive combinations the drive generator builds: 2WD direct on the motors, 4WD = 2 motors + O-ring belts
BUILDABLE_DRIVES = {("2WD", "direct"), ("4WD", "belt")}


@lru_cache(maxsize=1)
def taxonomy() -> dict:
    try:
        return json.loads(DATA.read_text())
    except (OSError, ValueError):
        return {}


def taxonomy_weapon_class(name: str) -> dict:
    """Allowed values for one weapon from the taxonomy `types` table, normalised to axis values."""
    t = (taxonomy().get("types") or {}).get(name) or {}
    out = {}
    for key, axis in (("position", MOUNTS), ("orientation", ORIENTATIONS), ("attachment", ATTACHMENTS), ("front", FRONTS)):
        vals = t.get(key) or []
        out[key] = sorted({normalise(v, axis) for v in vals} & set(axis))
    return out


@dataclass(frozen=True)
class Hypothesis:
    weapon: str = "wedge"
    mount: str = "none"
    orientation: str = "none"
    attachment: str = "none"
    front: str = "wedge"
    drive_layout: str = "2WD"
    drive_motor: str = "n10"
    wheel_dia: int = 28
    transmission: str = "direct"
    wheel_guards: bool = True
    invertible: bool = False
    battery: str = "lipo_2s_180"
    drive_esc: str = "esc_dual_brushed"
    weapon_esc: str = "none"
    rx: str = "rx_fs_ia6_decased"
    chassis: str = "clamshell"
    disc_stack: str = "single"
    skirts: str = "sides_rear"

    @property
    def weapon_class(self) -> WeaponClass:
        return WEAPON_CLASSES[self.weapon]

    @property
    def is_spinner(self) -> bool:
        return self.weapon_class.spinner

    @property
    def slug(self) -> str:
        bits = [self.weapon, self.mount, self.orientation, self.attachment, self.front, self.drive_layout,
                f"{self.drive_motor}{self.transmission[0]}{self.wheel_dia}", "g" if self.wheel_guards else "ng",
                "inv" if self.invertible else "up", self.battery.replace("lipo_", "").replace("c_typical_", ""),
                self.drive_esc[:10], self.weapon_esc[:6], self.rx[:5]]
        bits += [b for b in (self.chassis, self.disc_stack) if b not in ("clamshell", "single")]
        bits += [f"sk-{self.skirts}"] if self.skirts != "sides_rear" else []
        return "-".join(str(b) for b in bits)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Hypothesis":
        names = {f.name for f in fields(cls)}
        clean = {k: v for k, v in d.items() if k in names}
        if "weapon" in clean:
            clean["weapon"] = normalise(clean["weapon"], WEAPONS)
        if "wheel_dia" in clean:
            clean["wheel_dia"] = int(clean["wheel_dia"])
        for k in ("wheel_guards", "invertible"):
            if isinstance(clean.get(k), str):
                clean[k] = clean[k].lower() in ("1", "true", "yes", "y")
        return cls(**clean)

    @classmethod
    def parse(cls, text: str) -> "Hypothesis":
        """`weapon=vspin_drisk,front=forks,...` or a JSON object; unspecified axes come from `preset()` for the weapon."""
        text = text.strip()
        if text.startswith("{"):
            d = json.loads(text)
        else:
            d = dict(kv.split("=", 1) for kv in text.split(",") if "=" in kv)
            if "=" not in text and text:
                d = {"weapon": text}
        base = preset(normalise(d.get("weapon", "wedge"), WEAPONS)).to_dict()
        base.update(d)
        return cls.from_dict(base)


PRESETS = {
    "wedge": dict(weapon="wedge", front="wedge"),
    "none_pusher": dict(weapon="none_pusher", front="skirt"),
    "lifter": dict(weapon="lifter", mount="front", orientation="vertical", attachment="servo_horn", front="forks"),
    "hspin_bar": dict(weapon="hspin_bar", mount="top", orientation="flat", attachment="hub_motor", front="wedge",
                      wheel_dia=22, weapon_esc="c_bbb_antweight_spinner_brushless_esc",
                      battery="c_typical_2s_300mah_lipo_lihv_betafpv_tbs_",
                      drive_esc="c_malenki_nano_antweight_esc_receiver", rx="integrated"),
    "vspin_drisk": dict(weapon="vspin_drisk", mount="front", orientation="vertical", attachment="drisk", front="forks",
                        drive_layout="2WD", wheel_dia=22, weapon_esc="c_bbb_antweight_spinner_brushless_esc",
                        battery="c_typical_2s_300mah_lipo_lihv_betafpv_tbs_", invertible=False, drive_esc="c_malenki_nano_antweight_esc_receiver",
                        rx="integrated"),
}


def preset(weapon: str) -> Hypothesis:
    """A sensible complete hypothesis for a weapon type (the axes nobody specified)."""
    w = normalise(weapon, WEAPONS)
    if w in PRESETS:
        return Hypothesis(**PRESETS[w])
    wc = WEAPON_CLASSES[w]
    h = Hypothesis(weapon=w, mount=wc.mounts[0], orientation=wc.orientations[0], attachment=wc.attachments[0],
                      front=wc.fronts[0], weapon_esc="c_bbb_antweight_spinner_brushless_esc" if wc.actuator == "brushless" else "none",
                   invertible=w in MUST_INVERT or Hypothesis.invertible)
    from .rules import violations
    bad = {r for r, _ in violations(h)}
    if bad:  # keep the defaults that are fine, let the search pick the axes the broken rules need
        from .rules import RULES
        free = {a for r in RULES if r.name in bad for a in r.needs} - {"weapon"}
        fixed = {k: v for k, v in h.to_dict().items() if k not in free}
        h = next(enumerate_hypotheses(fixed), None) or next(enumerate_hypotheses({"weapon": w}))
    return h


def _rules_by_depth(rules):
    """Each rule fires at the depth where its last needed axis is bound (so it runs once per partial assignment)."""
    out = [[] for _ in AXIS_ORDER]
    for r in rules:
        out[max(AXIS_ORDER.index(a) for a in r.needs)].append(r)
    return out


def _ok(cur, rs):
    return all(r.check({k: cur[k] for k in r.needs}) is None for r in rs)


def _values(axis, fixed):
    return (fixed[axis],) if axis in fixed else AXES[axis]


def _fixed(fixed):
    return {k: (normalise(v, AXES[k]) if k == "weapon" else v) for k, v in (fixed or {}).items()}


def enumerate_hypotheses(fixed: dict | None = None, rules=None, limit: int | None = None):
    """Yield every valid hypothesis (depth-first over AXIS_ORDER, pruning partial assignments). `fixed` pins axes."""
    from .rules import RULES

    by_depth = _rules_by_depth(RULES if rules is None else rules)
    fixed = _fixed(fixed)
    n = 0

    def walk(i, cur):
        nonlocal n
        if i == len(AXIS_ORDER):
            n += 1
            yield Hypothesis(**cur)
            return
        axis = AXIS_ORDER[i]
        for v in _values(axis, fixed):
            if limit is not None and n >= limit:
                return
            cur[axis] = v
            if _ok(cur, by_depth[i]):
                yield from walk(i + 1, cur)
            del cur[axis]

    yield from walk(0, {})


def count_hypotheses(fixed: dict | None = None, rules=None) -> int:
    """Number of valid hypotheses by memoised depth-first counting (exact; no hypothesis is materialised)."""
    from .rules import RULES

    by_depth = _rules_by_depth(RULES if rules is None else rules)
    fixed = _fixed(fixed)
    # axes bound before depth i that a rule firing at depth >= i still reads
    live = [sorted({a for d in range(i, len(AXIS_ORDER)) for r in by_depth[d] for a in r.needs
                    if AXIS_ORDER.index(a) < i}) for i in range(len(AXIS_ORDER) + 1)]
    memo = {}

    def walk(i, cur):
        if i == len(AXIS_ORDER):
            return 1
        key = (i, tuple(cur[a] for a in live[i]))
        if key in memo:
            return memo[key]
        axis, total = AXIS_ORDER[i], 0
        for v in _values(axis, fixed):
            cur[axis] = v
            if _ok(cur, by_depth[i]):
                total += walk(i + 1, cur)
            del cur[axis]
        memo[key] = total
        return total

    return walk(0, {})


def count_by_weapon(fixed: dict | None = None) -> dict:
    """Valid hypothesis counts per weapon type."""
    return {w: count_hypotheses({**(fixed or {}), "weapon": w}) for w in WEAPONS}


def buildable(h: Hypothesis, experimental: bool = False) -> bool:
    b = BUILDABLE.get(h.weapon)
    if b is None:
        return False
    if experimental:
        b = {k: tuple(v) + EXPERIMENTAL.get(h.weapon, {}).get(k, ()) for k, v in b.items()}
    return (all(getattr(h, k) in v for k, v in b.items()) and (h.drive_layout, h.transmission) in BUILDABLE_DRIVES
            and all(getattr(h, k) == v for k, v in DEFAULT_ONLY.items() if k not in b))

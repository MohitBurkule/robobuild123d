"""Ontology of robot part entities and environment agents for a 150 g UK antweight.

Every entity / agent is a plain dataclass with typed properties so the
mechanism rules in :mod:`interact` can be pure functions of properties.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict

BANDS = ("front", "side", "rear", "top", "bottom", "internal")
CRIT_W = {"power": 1.0, "radio": 1.0, "drive": 0.9, "safety": 0.8, "weapon": 0.7,
          "structure": 0.6, "armour": 0.4, "cosmetic": 0.1}


@dataclass(frozen=True)
class Entity:
    kind: str
    label: str
    bands: frozenset              # where it sits
    exposure: str = "internal"    # exposed | flush | recessed | guarded | internal
    protrusion_mm: float = 0.0
    stiffness: str = "med"        # low | med | high
    fragility: float = 0.3        # 0..1
    criticality: frozenset = frozenset({"structure"})
    moving: str = "static"        # static | rotating | translating | flexing
    mass_g: float = 1.0
    material: str = "pla"
    retention: str = "screw"      # screw|press|friction|tape|glue|clip|solder|insert|thread|captive|none
    actuation: str = ""           # '' | slide | toggle | rocker | rotary | push | pin | magnetic
    actuation_axis: str = ""      # x (fore-aft) | y (lateral) | z (vertical) | ''
    conductive: bool = False
    live: bool = False            # carries battery voltage
    heat_source: bool = False
    thermal_limit_c: float = 120.0
    magnetic: bool = False
    rf_sensitive: bool = False
    threaded: bool = False
    wired: bool = False
    has_edge: bool = False
    visual_indicator: bool = False
    orientation_sensitive: bool = False
    tags: frozenset = frozenset()

    def d(self):
        x = asdict(self)
        return {k: (sorted(v) if isinstance(v, frozenset) else v) for k, v in x.items()}


@dataclass(frozen=True)
class Agent:
    kind: str
    label: str
    reach: frozenset              # bands it can contact
    contacts: frozenset           # impact|scrape|lift|clamp|heat|vibration|snag|ingress|short|handling|magnetic|inversion|shock|rf
    height: str = "low"           # low (0-15) | mid (15-35) | high (>35) | any
    motion_axis: str = ""         # x|y|z|'' dominant tangential direction of contact sweep
    energy_j: float = 1.0
    phase: str = "fight"          # fight | handling | pre | post | charging
    external: bool = True
    tags: frozenset = frozenset()

    def d(self):
        x = asdict(self)
        return {k: (sorted(v) if isinstance(v, frozenset) else v) for k, v in x.items()}


def F(*a):
    return frozenset(a)


ENTITIES = [
    # --- power / electronics
    Entity("switch_slide", "slide power switch", F("side", "top"), "flush", 2.0, "low", 0.6, F("power", "safety"), mass_g=1,
           retention="glue", actuation="slide", actuation_axis="x", conductive=True, live=True, wired=True,
           visual_indicator=False, orientation_sensitive=False, tags=F("switch", "toggles")),
    Entity("switch_toggle", "toggle/rocker switch", F("top", "side"), "exposed", 6.0, "low", 0.7, F("power", "safety"),
           retention="thread", actuation="toggle", actuation_axis="x", conductive=True, live=True, wired=True, threaded=True,
           tags=F("switch", "toggles")),
    Entity("link_pin", "removable link / locking-pin power link", F("top", "rear"), "recessed", 3.0, "med", 0.4, F("power", "safety"),
           retention="friction", actuation="pin", actuation_axis="z", conductive=True, live=True, wired=True, tags=F("switch", "removable")),
    Entity("switch_electronic", "electronic (MOSFET) switch board", F("internal"), "internal", 0, "low", 0.6, F("power", "safety"),
           retention="tape", actuation="magnetic", conductive=True, live=True, wired=True, heat_source=True, thermal_limit_c=100,
           tags=F("switch", "electronic")),
    Entity("battery", "LiPo battery (2S/3S 300-450 mAh)", F("internal"), "internal", 0, "low", 0.9, F("power"), mass_g=30,
           retention="tape", conductive=True, live=True, wired=True, thermal_limit_c=60, tags=F("lipo",)),
    Entity("esc_drive", "drive ESC (dual brushed)", F("internal"), "internal", 0, "low", 0.6, F("drive"), mass_g=4,
           retention="tape", conductive=True, live=True, wired=True, heat_source=True, thermal_limit_c=100, rf_sensitive=False),
    Entity("esc_weapon", "weapon ESC (brushless)", F("internal"), "internal", 0, "low", 0.6, F("weapon"), mass_g=6,
           retention="tape", conductive=True, live=True, wired=True, heat_source=True, thermal_limit_c=100),
    Entity("receiver", "receiver", F("internal"), "internal", 0, "low", 0.6, F("radio"), mass_g=2,
           retention="tape", conductive=True, wired=True, rf_sensitive=True, thermal_limit_c=85),
    Entity("antenna", "receiver antenna", F("internal", "top", "rear"), "exposed", 15, "low", 0.7, F("radio"), mass_g=0.2,
           retention="tape", conductive=True, wired=True, rf_sensitive=True, moving="flexing", tags=F("whip",)),
    Entity("led", "power/status LED", F("top", "rear"), "flush", 1.5, "low", 0.5, F("safety"), mass_g=0.2,
           retention="glue", conductive=True, live=True, wired=True, visual_indicator=True, orientation_sensitive=True),
    Entity("wire_power", "battery/power wiring (18-22 AWG)", F("internal"), "internal", 0, "low", 0.4, F("power"),
           retention="solder", conductive=True, live=True, wired=True, moving="flexing"),
    Entity("wire_signal", "servo/signal leads", F("internal"), "internal", 0, "low", 0.5, F("radio", "drive"),
           retention="clip", conductive=True, wired=True, moving="flexing"),
    Entity("wire_motor", "motor leads", F("internal", "side"), "internal", 0, "low", 0.5, F("drive", "weapon"),
           retention="solder", conductive=True, live=True, wired=True, moving="flexing"),
    Entity("conn_xt30", "XT30 battery connector", F("internal"), "internal", 0, "med", 0.3, F("power"), mass_g=2,
           retention="friction", conductive=True, live=True, wired=True, tags=F("connector",)),
    Entity("conn_jst", "JST / servo connector", F("internal"), "internal", 0, "low", 0.5, F("radio", "drive"),
           retention="friction", conductive=True, wired=True, tags=F("connector",)),
    Entity("solder_joint", "solder joints on motor tabs/switch", F("internal"), "internal", 0, "low", 0.6, F("power", "drive"),
           retention="solder", conductive=True, live=True, wired=True),
    Entity("heatshrink", "heatshrink / insulation", F("internal"), "internal", 0, "low", 0.4, F("power"), retention="none",
           thermal_limit_c=125),
    # --- drive
    Entity("drive_motor", "N20 drive gearmotor", F("internal", "side"), "guarded", 0, "med", 0.4, F("drive"), mass_g=10,
           retention="clip", conductive=True, live=True, wired=True, heat_source=True, thermal_limit_c=90, moving="rotating",
           magnetic=True, tags=F("gearbox",)),
    Entity("gearbox", "N20 metal gearbox", F("internal", "side"), "guarded", 0, "high", 0.4, F("drive"), moving="rotating",
           retention="clip", tags=F("gearbox",)),
    Entity("motor_mount", "motor clamp / mount", F("internal"), "internal", 0, "med", 0.4, F("drive", "structure"), retention="screw"),
    Entity("wheel", "drive wheel", F("side", "bottom"), "exposed", 3, "med", 0.4, F("drive"), mass_g=4, moving="rotating",
           retention="press", has_edge=True),
    Entity("tyre", "tyre (silicone/TPU/O-ring)", F("side", "bottom"), "exposed", 3, "low", 0.4, F("drive"), moving="rotating",
           retention="friction", material="silicone"),
    Entity("hub", "wheel hub / D-shaft adapter", F("side"), "exposed", 0, "med", 0.5, F("drive"), moving="rotating",
           retention="press"),
    Entity("drive_shaft", "drive output D-shaft (3 mm)", F("side"), "guarded", 0, "high", 0.4, F("drive"), material="steel",
           moving="rotating", retention="press"),
    # --- weapon
    Entity("weapon_motor", "weapon brushless outrunner", F("internal", "front"), "guarded", 0, "med", 0.4, F("weapon"), mass_g=18,
           retention="screw", conductive=True, live=True, wired=True, heat_source=True, thermal_limit_c=100, moving="rotating",
           magnetic=True),
    Entity("belt", "weapon belt / O-ring", F("front", "internal"), "exposed", 0, "low", 0.6, F("weapon"), moving="rotating",
           retention="friction", material="rubber", thermal_limit_c=90),
    Entity("pulley", "pulley", F("front", "internal"), "exposed", 0, "med", 0.4, F("weapon"), moving="rotating",
           retention="press", has_edge=True),
    Entity("weapon_shaft", "weapon shaft / dead axle", F("front"), "guarded", 0, "high", 0.3, F("weapon"), material="steel",
           moving="rotating", retention="captive", threaded=True),
    Entity("bearing", "weapon bearing", F("front"), "guarded", 0, "high", 0.4, F("weapon"), material="steel", moving="rotating",
           retention="press"),
    Entity("upright", "weapon upright / fork arm", F("front", "side"), "exposed", 0, "med", 0.5, F("weapon", "structure"),
           retention="screw", has_edge=True),
    Entity("weapon_disc", "spinning disc / bar / drum / beater", F("front"), "exposed", 0, "high", 0.3, F("weapon"), mass_g=25,
           material="steel", moving="rotating", retention="thread", threaded=True, has_edge=True),
    Entity("weapon_nut", "weapon retaining nut / grub screw", F("front"), "exposed", 0, "high", 0.3, F("weapon"), material="steel",
           threaded=True, retention="thread"),
    # --- chassis / armour
    Entity("fork", "fork / tine", F("front", "bottom"), "exposed", 0, "med", 0.4, F("armour"), material="steel", has_edge=True,
           retention="screw", moving="flexing"),
    Entity("lip", "lip / acetate scoop", F("front", "bottom"), "exposed", 0, "low", 0.5, F("armour"), material="acetate",
           has_edge=True, retention="screw", moving="flexing"),
    Entity("skirt", "skirt / side lip", F("side", "bottom"), "exposed", 0, "low", 0.5, F("armour"), material="acetate",
           has_edge=True, retention="tape", moving="flexing"),
    Entity("wedgelet", "wedgelet", F("front", "bottom"), "exposed", 0, "med", 0.4, F("armour"), material="steel", has_edge=True,
           retention="screw", moving="flexing"),
    Entity("shell", "printed shell / tub", F("front", "side", "rear", "top"), "exposed", 0, "med", 0.5, F("structure"),
           mass_g=40, retention="screw", has_edge=True),
    Entity("lid", "lid / top plate", F("top"), "exposed", 0, "med", 0.5, F("structure", "armour"), retention="screw", has_edge=True),
    Entity("base_panel", "base panel", F("bottom"), "exposed", 0, "med", 0.4, F("structure"), retention="screw"),
    Entity("armour_plate", "bolt-on armour plate (Ti/Al/HDPE)", F("front", "side"), "exposed", 0, "high", 0.2, F("armour"),
           material="titanium", conductive=True, retention="screw", has_edge=True),
    Entity("screw", "M2/M3 machine screws", F("top", "bottom", "side", "front"), "flush", 1.0, "high", 0.2, F("structure"),
           material="steel", conductive=True, threaded=True, retention="thread", has_edge=True),
    Entity("insert", "heat-set inserts", F("internal"), "internal", 0, "high", 0.3, F("structure"), material="brass",
           threaded=True, retention="insert", thermal_limit_c=60),
    Entity("nut", "nyloc / plain nuts", F("internal", "bottom"), "recessed", 0, "high", 0.2, F("structure"), threaded=True,
           retention="captive", conductive=True),
    Entity("standoff", "standoffs / spacers", F("internal"), "internal", 0, "med", 0.3, F("structure"), threaded=True,
           retention="thread"),
    Entity("tape", "double-sided / gaffer tape mounts", F("internal", "side"), "internal", 0, "low", 0.6, F("structure"),
           retention="tape", thermal_limit_c=70),
    Entity("zip_tie", "zip ties / cable ties", F("internal"), "internal", 0, "low", 0.4, F("structure"), retention="clip"),
    Entity("glue_joint", "glue joint (CA / epoxy)", F("internal"), "internal", 0, "low", 0.7, F("structure"), retention="glue",
           thermal_limit_c=80),
    Entity("foam", "foam packing / battery cushion", F("internal"), "internal", 0, "low", 0.2, F("structure"), retention="friction"),
    Entity("self_righter", "srimech / righting geometry", F("top", "rear"), "exposed", 0, "med", 0.3, F("drive"), retention="screw"),
]

AGENTS = [
    Agent("vspin_disc", "vertical spinner disc", F("front", "side", "bottom"), F("impact", "lift", "shock", "inversion", "scrape"),
          "low", "z", 25),
    Agent("vspin_drum", "drum spinner", F("front", "side", "bottom"), F("impact", "lift", "shock", "inversion"), "low", "z", 20),
    Agent("eggbeater", "eggbeater", F("front", "side", "top"), F("impact", "shock", "inversion", "scrape"), "mid", "z", 25),
    Agent("hspin_bar", "horizontal bar spinner", F("front", "side", "rear"), F("impact", "shock", "scrape"), "mid", "y", 40),
    Agent("hspin_disc", "horizontal disc spinner", F("front", "side", "rear"), F("impact", "shock", "scrape"), "mid", "y", 30),
    Agent("undercutter", "undercutter", F("front", "side", "rear", "bottom"), F("impact", "shock", "lift", "inversion", "scrape"),
          "low", "y", 35),
    Agent("overcutter", "overcutter", F("top", "front", "side"), F("impact", "shock", "scrape"), "high", "x", 25),
    Agent("hammer_axe", "hammer / axe", F("top"), F("impact", "shock"), "high", "z", 8),
    Agent("hammer_saw", "hammer-saw / top saw", F("top"), F("scrape", "impact", "heat"), "high", "x", 3),
    Agent("wedge", "opponent wedge", F("front", "side", "rear", "bottom"), F("lift", "scrape", "snag"), "low", "x", 2),
    Agent("fork_opp", "opponent forks", F("front", "side", "rear", "bottom"), F("lift", "snag", "scrape"), "low", "x", 2),
    Agent("lifter", "lifter", F("bottom", "front", "side"), F("lift", "inversion", "scrape"), "low", "z", 3),
    Agent("flipper_servo", "servo flipper", F("bottom", "front", "side", "rear"), F("lift", "inversion", "impact", "shock", "scrape"),
          "low", "z", 5),
    Agent("flipper_pneu", "pneumatic flipper", F("bottom", "front", "side", "rear"), F("lift", "inversion", "impact", "shock", "scrape"),
          "low", "z", 15),
    Agent("grabber", "grabber", F("top", "side", "front", "rear"), F("clamp", "lift", "snag"), "mid", "y", 3),
    Agent("crusher", "crusher", F("top", "side"), F("clamp", "impact"), "high", "z", 5),
    Agent("pusher", "pusher / rammer", F("front", "side", "rear"), F("impact", "scrape"), "mid", "x", 2),
    Agent("floor_wood", "wooden arena floor", F("bottom"), F("scrape", "snag", "shock"), "low", "x", 1),
    Agent("floor_steel", "steel arena floor / plates", F("bottom"), F("scrape", "short", "shock"), "low", "x", 1),
    Agent("floor_splinters", "floor splinters / gouges", F("bottom"), F("snag", "ingress"), "low", "x", 0.5),
    Agent("floor_seams", "floor seams / panel steps", F("bottom"), F("snag", "shock"), "low", "x", 0.5),
    Agent("arena_screws", "arena screws / hazard plates", F("bottom"), F("snag", "scrape", "short"), "low", "x", 0.5),
    Agent("floor_wall_gap", "floor-wall gap", F("front", "side", "bottom"), F("snag", "ingress"), "low", "x", 0.5),
    Agent("wall", "arena wall", F("front", "side", "rear", "top"), F("impact", "scrape", "shock"), "mid", "y", 3),
    Agent("pit", "pit / out-of-arena", F("bottom"), F("snag", "inversion"), "low", "z", 1),
    Agent("ceiling", "arena roof / polycarbonate lid", F("top"), F("impact", "shock", "inversion"), "high", "z", 5),
    Agent("debris_small", "small debris (screws, filament)", F("bottom", "internal", "side", "front"), F("ingress", "short", "snag"),
          "low", "", 0.1),
    Agent("debris_large", "large debris (armour chunks, teeth)", F("bottom", "side", "front"), F("snag", "impact"), "low", "", 1),
    Agent("start_square", "start square / pre-fight wait", F("internal"), F("heat", "rf"), "any", "", 0, "pre"),
    Agent("own_weapon_gyro", "own weapon gyro / reaction torque", F("internal", "front"), F("inversion", "shock", "vibration"),
          "any", "y", 5, external=False),
    Agent("own_weapon_spin", "own spinning weapon proximity", F("front", "internal"), F("scrape", "impact", "ingress"), "low", "z",
          20, external=False),
    Agent("own_wheels", "own rotating wheels", F("side", "bottom"), F("scrape", "snag"), "low", "x", 1, external=False),
    Agent("operator_handling", "operator carrying / switching on/off", F("top", "side", "rear"), F("handling", "impact"), "any",
          "x", 0.5, "handling"),
    Agent("pin_insertion", "pin/link insertion at activation", F("top", "rear"), F("handling",), "any", "z", 0.2, "pre"),
    Agent("charging", "charging / balance lead", F("internal"), F("heat", "handling"), "any", "", 0, "charging"),
    Agent("temperature", "ambient & self-heating", F("internal"), F("heat",), "any", "", 0),
    Agent("vibration", "weapon/drive vibration", F("internal", "front", "side", "top", "bottom", "rear"), F("vibration",), "any",
          "", 0.5, external=False),
    Agent("magnets", "magnetic arena / magnets", F("bottom", "internal"), F("magnetic",), "low", "", 0),
    Agent("sparks", "sparks / steel-on-steel", F("front", "side", "bottom"), F("heat", "short", "ingress"), "low", "", 0.1),
    Agent("inversion_state", "driving inverted", F("top", "bottom", "internal"), F("inversion", "scrape"), "low", "x", 1),
    Agent("rf_noise", "RF crowding / weapon EMI", F("internal"), F("rf",), "any", "", 0),
    Agent("landing", "landing after flip / launch", F("bottom", "top", "side"), F("shock", "impact"), "any", "z", 4),
]


def properties():
    """All property names across entities and agents."""
    ent = [f for f in Entity.__dataclass_fields__ if f not in ("kind", "label")]
    ag = [f for f in Agent.__dataclass_fields__ if f not in ("kind", "label")]
    return ent, ag


def ent(kind):
    return next(e for e in ENTITIES if e.kind == kind)


def agent(kind):
    return next(a for a in AGENTS if a.kind == kind)

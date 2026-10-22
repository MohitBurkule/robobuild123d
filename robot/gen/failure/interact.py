"""Enumerate entity x agent x state and entity x entity interactions through a
rule table of named mechanisms; dedupe, cluster, rank, cascade, diff vs catalog."""
from __future__ import annotations
import hashlib
import itertools
from dataclasses import replace
from .ontology import ENTITIES, AGENTS, CRIT_W, Entity, Agent, F

# ------------------------------------------------------------------ robot states
FLIP = {"top": "bottom", "bottom": "top"}
STATES = {
    "nominal": dict(desc="upright, all functions"),
    "inverted": dict(desc="upside down", band_map=FLIP),
    "on_side_or_walled": dict(desc="on its side / wedged against a wall", band_map={"side": "bottom", "bottom": "side"}),
    "one_drive_dead": dict(desc="one drive side dead, spinning in place", band_map={"side": "front"}),
    "weapon_dead": dict(desc="weapon dead / spinning down; uprights become the front"),
    "inverted_weapon_spinning": dict(desc="inverted with weapon still spinning (gyro)", band_map=FLIP),
    "shell_or_fork_lost": dict(desc="part of shell or a fork lost; internals exposed",
                               expose=F("battery", "receiver", "esc_drive", "esc_weapon", "wire_power", "wire_signal", "wire_motor",
                                        "conn_xt30", "conn_jst", "insert", "tape", "foam", "drive_motor", "solder_joint")),
    "stuck_on_debris": dict(desc="beached on debris, wheels off floor", band_map={"bottom": "front"}),
    "partial_power": dict(desc="brownout / sagging cell"),
    "radio_failsafe": dict(desc="radio failsafe, robot motionless"),
    "airborne_landing": dict(desc="airborne or landing"),
}
STATE_LIKELIHOOD = {"nominal": 1.0, "inverted": 0.6, "on_side_or_walled": 0.4, "one_drive_dead": 0.3, "weapon_dead": 0.4,
                    "inverted_weapon_spinning": 0.35, "shell_or_fork_lost": 0.3, "stuck_on_debris": 0.2, "partial_power": 0.25,
                    "radio_failsafe": 0.15, "airborne_landing": 0.4}


def apply_state(e: Entity, s: str) -> Entity:
    st = STATES[s]
    bm = st.get("band_map", {})
    bands = frozenset(bm.get(b, b) for b in e.bands) | (frozenset(b for b in e.bands if b in bm) if s == "one_drive_dead" else frozenset())
    exp = e.exposure
    if e.kind in st.get("expose", ()):  # internals now open
        bands, exp = bands | F("front", "side"), "exposed"
    if s == "weapon_dead" and e.kind == "upright":
        bands = bands | F("front")
    return replace(e, bands=bands, exposure=exp)


# ------------------------------------------------------------------ helpers
EXPOSED = ("exposed", "flush")
REACHABLE = ("exposed", "flush", "recessed")


def reach(e, a):
    return len(e.bands & a.reach) > 0


def H(mech, title, likelihood, loses="", **kw):
    return dict(mechanism=mech, title=title, likelihood=likelihood, loses=loses, **kw)


RULES = []  # (name, family, kind 'ea' or 'ee', fn)


def rule(family, kind="ea"):
    def deco(fn):
        RULES.append((fn.__name__, family, kind, fn))
        return fn
    return deco


# ------------------------------------------------------------------ entity x agent rules
@rule("switch")
def toggle_by_contact(e, a, s):
    if not e.actuation or e.actuation in ("magnetic",) or e.exposure not in REACHABLE or not reach(e, a):
        return None
    if not (a.contacts & F("impact", "scrape", "lift")) or a.phase != "fight":
        return None
    aligned = bool(e.actuation_axis) and e.actuation_axis == a.motion_axis
    lk = 0.8 if aligned else 0.45
    if e.exposure == "recessed":
        lk *= 0.3
    what = "pulled/knocked out" if e.actuation == "pin" else "flicked OFF"
    return H("toggle_by_contact", f"{a.label} contact {what} the {e.label} mid-fight", lk, "power",
             detail=f"actuator axis {e.actuation_axis or '-'} vs sweep {a.motion_axis or '-'} ({'parallel: toggles' if aligned else 'oblique'})")


@rule("switch")
def toggle_on_handling(e, a, s):
    if e.actuation and e.actuation not in ("magnetic",) and "handling" in a.contacts and e.exposure in REACHABLE:
        return H("toggle_on_handling", f"{e.label} knocked ON (or OFF) by {a.label}", 0.5, "safety")


@rule("switch")
def actuator_rip(e, a, s):
    if "switch" in e.tags and e.protrusion_mm > 0 and e.exposure in EXPOSED and reach(e, a) and a.contacts & F("impact", "scrape", "snag"):
        return H("actuator_rip", f"{a.label} shears off / rips out the {e.label} actuator or body", min(1, 0.15 * e.protrusion_mm), "power")


@rule("switch")
def switch_contact_bounce(e, a, s):
    if "toggles" in e.tags and a.contacts & F("shock", "vibration"):
        return H("switch_contact_bounce", f"{e.label} contacts bounce under {a.label} shock -> brownout/receiver reboot", 0.35, "power")


@rule("switch")
def electronic_switch_trigger(e, a, s):
    if e.actuation == "magnetic" and a.contacts & F("magnetic", "rf", "short"):
        return H("electronic_switch_trigger", f"{e.label} spuriously latched/unlatched by {a.label}", 0.3, "power")


@rule("indicator")
def indicator_hidden(e, a, s):
    if e.visual_indicator and (s in ("inverted", "on_side_or_walled", "inverted_weapon_spinning") or a.kind in ("operator_handling", "start_square")):
        return H("indicator_hidden", f"{e.label} not visible during {a.label} ({s}) -> armed state unknown", 0.4, "safety")


@rule("protrusion")
def protrusion_shear(e, a, s):
    if "switch" in e.tags or e.protrusion_mm <= 0 or e.exposure not in EXPOSED or not reach(e, a):
        return None
    if a.contacts & F("impact", "scrape", "snag"):
        return H("protrusion_shear", f"{a.label} shears protruding {e.label} ({e.protrusion_mm} mm)", min(1, 0.06 * e.protrusion_mm + 0.2),
                 e.criticality and sorted(e.criticality)[0])


@rule("impact")
def penetration_crush(e, a, s):
    if e.fragility >= 0.55 and reach(e, a) and a.contacts & F("impact", "clamp") and (e.exposure != "internal" or a.energy_j >= 8):
        lk = e.fragility * min(1, a.energy_j / 20)
        if e.kind == "battery":
            title = f"{a.label} punctures/crushes LiPo -> fire, power loss"
        else:
            title = f"{a.label} transmits through shell and crushes {e.label}"
        return H("penetration_crush", title, lk, sorted(e.criticality)[0])


@rule("impact")
def shock_dislodge(e, a, s):
    if e.retention in ("friction", "tape", "press", "glue", "clip") and a.contacts & F("shock", "impact") and e.kind != "foam":
        lk = {"friction": 0.6, "tape": 0.5, "press": 0.4, "glue": 0.5, "clip": 0.3}[e.retention] * min(1, (a.energy_j + 2) / 15)
        return H("shock_dislodge", f"{e.label} ({e.retention}-retained) unseats under {a.label} shock", lk, sorted(e.criticality)[0])


@rule("impact")
def mass_tear_out(e, a, s):
    if e.mass_g >= 10 and a.contacts & F("shock", "impact") and e.retention != "captive":
        return H("mass_tear_out", f"{e.label} ({e.mass_g:.0f} g) inertia tears its mount under {a.label} (a=v/dt)", 0.35, sorted(e.criticality)[0])


@rule("impact")
def edge_bite(e, a, s):
    if e.has_edge and e.exposure in EXPOSED and reach(e, a) and a.contacts & F("impact") and a.energy_j >= 10 and e.kind not in ("weapon_disc",):
        return H("edge_bite", f"{a.label} bites the edge of the {e.label} and transfers full energy", 0.5, sorted(e.criticality)[0])


@rule("impact")
def brittle_fracture(e, a, s):
    if e.material in ("pla", "acetate") and e.exposure in EXPOSED and reach(e, a) and a.contacts & F("impact", "shock") and e.stiffness != "low":
        return H("brittle_fracture", f"{e.label} ({e.material}) cracks/shatters under {a.label}", 0.45, sorted(e.criticality)[0])


@rule("impact")
def flex_fatigue_crack(e, a, s):
    if e.moving == "flexing" and e.material in ("acetate", "steel", "pla") and a.contacts & F("impact", "scrape", "lift"):
        return H("flex_fatigue_crack", f"{e.label} cracks at clamp line after repeated {a.label} deflections", 0.35, sorted(e.criticality)[0])


@rule("electrical")
def electrical_short(e, a, s):
    if e.live and a.contacts & F("short") and (e.exposure != "internal" or a.kind in ("debris_small", "sparks") or s == "shell_or_fork_lost"):
        return H("electrical_short", f"{a.label} bridges live {e.label} -> short, magic smoke", 0.35 if e.exposure == "internal" else 0.55, "power")


@rule("debris")
def debris_ingress(e, a, s):
    if e.moving == "rotating" and a.contacts & F("ingress") and e.kind not in ("weapon_disc",):
        return H("debris_ingress", f"{a.label} enters {e.label} -> jam / derail", 0.4, sorted(e.criticality)[0])


@rule("debris")
def snag_protrusion(e, a, s):
    if (e.protrusion_mm > 0 or e.has_edge) and "bottom" in e.bands and a.contacts & F("snag") and e.exposure in EXPOSED:
        return H("snag_protrusion", f"{e.label} on underside catches {a.label} -> stall/pivot", 0.4, "drive")


@rule("fastener")
def vibration_loosen(e, a, s):
    if e.threaded and a.contacts & F("vibration", "shock") and e.retention in ("thread", "screw", "insert"):
        return H("vibration_loosen", f"{e.label} backs out under {a.label}", 0.5, sorted(e.criticality)[0])


@rule("fastener")
def insert_pullout(e, a, s):
    if e.retention == "insert" and a.contacts & F("impact", "shock", "heat", "lift", "clamp"):
        return H("insert_pullout", f"heat-set insert pulls through plastic under {a.label}", 0.4, "structure")


@rule("fastener")
def screw_head_bite(e, a, s):
    if e.kind == "screw" and e.protrusion_mm > 0 and a.contacts & F("impact", "scrape") and reach(e, a):
        return H("screw_head_bite", f"proud screw head gives {a.label} a bite point / gets sheared", 0.5, "structure")


@rule("thermal")
def thermal_overrun(e, a, s):
    if a.contacts & F("heat") and (e.heat_source or e.thermal_limit_c <= 70):
        lk = 0.5 if s in ("one_drive_dead", "stuck_on_debris", "on_side_or_walled") else 0.3
        return H("thermal_overrun", f"{e.label} exceeds {e.thermal_limit_c:.0f} C under {a.label} ({s})", lk, sorted(e.criticality)[0])


@rule("thermal")
def stall_heat(e, a, s):
    if e.heat_source and e.moving == "rotating" and (a.contacts & F("clamp", "snag", "lift") or s in ("stuck_on_debris", "on_side_or_walled")):
        return H("stall_heat", f"{e.label} stalls against {a.label} -> motor/ESC overheat", 0.45, sorted(e.criticality)[0])


@rule("rf")
def rf_degrade(e, a, s):
    if e.rf_sensitive and (a.contacts & F("rf", "magnetic") or (s in ("inverted", "on_side_or_walled") and e.kind == "antenna")):
        return H("rf_degrade", f"{e.label} link degraded by {a.label} ({s})", 0.35, "radio")


@rule("rf")
def antenna_snag(e, a, s):
    if e.kind == "antenna" and a.contacts & F("scrape", "snag", "clamp", "impact") and reach(e, a):
        return H("antenna_snag", f"exposed antenna caught/cut by {a.label}", 0.55, "radio")


@rule("lift")
def lift_lose_traction(e, a, s):
    if e.kind in ("wheel", "tyre") and a.contacts & F("lift") and reach(e, a):
        return H("lift_lose_traction", f"{a.label} lifts {e.label} off floor -> no traction, carried", 0.5, "drive")


@rule("clamp")
def clamp_crush(e, a, s):
    if "clamp" in a.contacts and e.stiffness != "high" and reach(e, a):
        return H("clamp_crush", f"{a.label} deforms {e.label} until internals contact", 0.4, sorted(e.criticality)[0])


@rule("abrasion")
def abrasion_cut(e, a, s):
    if (e.wired or e.material in ("silicone", "rubber") or e.retention == "tape") and "scrape" in a.contacts and \
            (e.exposure in EXPOSED or s == "shell_or_fork_lost") and reach(e, a):
        return H("abrasion_cut", f"{a.label} abrades through {e.label}", 0.4, sorted(e.criticality)[0])


@rule("fatigue")
def wire_fatigue(e, a, s):
    if e.wired and e.moving == "flexing" and a.contacts & F("vibration", "shock"):
        return H("wire_fatigue", f"{e.label} fatigues at solder joint/hinge under {a.label}", 0.4, sorted(e.criticality)[0])


@rule("weapon")
def weapon_drive_shock(e, a, s):
    if e.kind in ("belt", "pulley", "bearing", "weapon_shaft", "weapon_disc", "weapon_nut") and a.contacts & F("impact", "shock"):
        m = {"belt": "belt jumps pulley", "pulley": "pulley slips on shaft", "bearing": "bearing walks out of seat",
             "weapon_shaft": "shaft bends -> wobble", "weapon_disc": "disc loosens / slips on hub",
             "weapon_nut": "retaining nut loosens"}[e.kind]
        return H("weapon_drive_shock", f"{a.label} hit: {m}", 0.45, "weapon")


@rule("inversion")
def inversion_effect(e, a, s):
    inv = "inversion" in a.contacts or s in ("inverted", "inverted_weapon_spinning")
    if not inv:
        return None
    if e.kind in ("lip", "fork", "wedgelet", "skirt"):
        return H("inversion_effect", f"inverted by {a.label}: {e.label} now on top, useless", 0.6, "armour")
    if e.kind in ("battery", "foam") or e.retention in ("tape",) and e.mass_g >= 4:
        return H("inversion_effect", f"inverted by {a.label}: {e.label} shifts under gravity/landing", 0.3, sorted(e.criticality)[0])
    if e.kind == "self_righter":
        return H("inversion_effect", f"cannot self-right after {a.label} (righting geometry/{s})", 0.5, "drive")
    if e.kind in ("switch_slide", "switch_toggle", "link_pin", "base_panel"):
        return H("inversion_effect", f"inverted: {e.label} now faces {a.label} / floor", 0.5, sorted(e.criticality)[0])


@rule("gyro")
def gyro_effect(e, a, s):
    if a.kind == "own_weapon_gyro" and e.kind in ("weapon_disc", "wheel", "self_righter", "bearing", "upright"):
        return H("gyro_effect", f"own weapon gyro loads {e.label} when turning/hit ({s})", 0.4 if s != "inverted_weapon_spinning" else 0.7, "drive")


@rule("state")
def state_exposure(e, a, s):
    if s == "nominal":
        return None
    base = next(x for x in ENTITIES if x.kind == e.kind)
    newly = e.bands - base.bands
    if newly & a.reach and a.contacts & F("impact", "scrape", "lift", "clamp") and a.phase == "fight":
        return H("state_exposure", f"in {s}, {e.label} now presents {sorted(newly & a.reach)} to {a.label}",
                 0.5 * base.fragility + 0.2, sorted(e.criticality)[0])


@rule("state")
def state_helpless(e, a, s):
    if s in ("radio_failsafe", "partial_power", "one_drive_dead") and e.kind in ("wheel", "self_righter") and a.phase == "fight" \
            and a.external and a.contacts & F("impact", "lift", "clamp"):
        return H("state_helpless", f"{s}: cannot evade/turn, {a.label} gets free repeated hits", 0.5, "drive")


# ------------------------------------------------------------------ entity x entity rules (internal)
ADJ = {  # physically adjacent pairs (a, b) for internal interactions
    ("wire_motor", "pulley"), ("wire_motor", "belt"), ("wire_power", "pulley"), ("wire_signal", "wheel"), ("wire_motor", "wheel"),
    ("battery", "esc_drive"), ("battery", "esc_weapon"), ("battery", "weapon_motor"), ("battery", "screw"), ("battery", "standoff"),
    ("receiver", "weapon_motor"), ("receiver", "esc_weapon"), ("antenna", "armour_plate"), ("antenna", "weapon_motor"),
    ("antenna", "wire_power"), ("switch_slide", "wheel"), ("switch_toggle", "wheel"), ("switch_slide", "lid"),
    ("switch_electronic", "weapon_motor"), ("switch_electronic", "drive_motor"), ("receiver", "drive_motor"),
    ("conn_xt30", "lid"), ("conn_jst", "receiver"), ("led", "lid"), ("tape", "esc_weapon"), ("tape", "drive_motor"),
    ("insert", "esc_drive"), ("glue_joint", "weapon_motor"), ("heatshrink", "esc_weapon"), ("battery", "lid"), ("battery", "base_panel"),
    ("wheel", "shell"), ("tyre", "shell"), ("tyre", "base_panel"), ("hub", "motor_mount"), ("drive_shaft", "motor_mount"),
    ("gearbox", "motor_mount"), ("belt", "upright"), ("pulley", "upright"), ("weapon_disc", "upright"), ("weapon_disc", "shell"),
    ("weapon_disc", "fork"), ("weapon_disc", "lip"), ("weapon_disc", "wedgelet"), ("wheel", "fork"), ("wheel", "skirt"),
    ("tyre", "screw"), ("belt", "screw"), ("weapon_disc", "screw"), ("pulley", "shell"), ("weapon_motor", "motor_mount"),
    ("bearing", "upright"), ("weapon_shaft", "upright"), ("wheel", "lid"), ("drive_motor", "motor_mount"), ("wire_power", "lid"),
    ("wire_motor", "lid"), ("wheel", "armour_plate"), ("weapon_disc", "armour_plate"), ("belt", "shell"), ("tyre", "wire_signal"),
    ("battery", "drive_motor"), ("wire_power", "shell"), ("conn_xt30", "battery"), ("solder_joint", "drive_motor"),
}


def adjacent(a, b):
    return (a.kind, b.kind) in ADJ or (b.kind, a.kind) in ADJ


@rule("internal", "ee")
def wire_entangle(e, o, s):
    if e.wired and e.moving == "flexing" and o.moving == "rotating" and adjacent(e, o):
        return H("wire_entangle", f"{e.label} wraps into rotating {o.label}", 0.5, sorted(e.criticality)[0])


@rule("internal", "ee")
def heat_coupling(e, o, s):
    if o.heat_source and e.thermal_limit_c <= 90 and adjacent(e, o):
        return H("heat_coupling", f"{o.label} heats adjacent {e.label} past {e.thermal_limit_c:.0f} C", 0.4 if e.kind == "battery" else 0.3,
                 sorted(e.criticality)[0])


@rule("internal", "ee")
def magnetic_interference(e, o, s):
    if e.rf_sensitive and (o.magnetic or o.conductive) and adjacent(e, o):
        return H("magnetic_interference", f"{o.label} detunes/blocks/EMI on {e.label}", 0.35, "radio")


@rule("internal", "ee")
def self_toggle(e, o, s):
    if "toggles" in e.tags and o.moving == "rotating" and adjacent(e, o):
        return H("self_toggle", f"own {o.label} (or debris it throws) flicks the {e.label}", 0.4, "power")


@rule("internal", "ee")
def internal_puncture(e, o, s):
    if e.fragility >= 0.55 and (o.threaded or o.has_edge or o.stiffness == "high") and adjacent(e, o) and o.moving == "static":
        return H("internal_puncture", f"{o.label} driven into {e.label} when hull deflects", 0.45 if e.kind == "battery" else 0.3,
                 sorted(e.criticality)[0])


@rule("internal", "ee")
def internal_short(e, o, s):
    if e.live and o.conductive and not o.live and adjacent(e, o):
        return H("internal_short", f"live {e.label} chafes to conductive {o.label} -> short", 0.3, "power")


@rule("internal", "ee")
def stray_access(e, o, s):
    if e.kind in ("conn_xt30", "led", "switch_slide", "wire_power", "wire_motor") and o.kind == "lid" and adjacent(e, o):
        return H("stray_access", f"{e.label} trapped/pinched when {o.label} is closed", 0.35, sorted(e.criticality)[0])


# --- post-impact deformation family: every moving part x adjacent static part
DEFL = {"low": 1.5, "med": 0.7, "high": 0.2}  # mm plastic set per reference 20 J hit at nearest structure
CLEAR = {"wheel": 1.5, "tyre": 1.0, "hub": 0.8, "drive_shaft": 0.3, "belt": 2.0, "pulley": 1.0, "weapon_disc": 2.0, "gearbox": 0.1,
         "drive_motor": 0.2, "weapon_motor": 0.5, "bearing": 0.05, "weapon_shaft": 0.05}
DEFORM_TXT = {
    "shell": "shell/wheel guard pushed in", "lid": "lid dished", "base_panel": "base cracked flap drags / pushes up",
    "fork": "fork bent up", "lip": "lip curled", "skirt": "skirt folded", "wedgelet": "wedgelet bent back",
    "upright": "upright bent", "motor_mount": "motor mount bent / motor knocked from pocket", "screw": "screw head driven in",
    "armour_plate": "armour plate dented", "standoff": "standoff bent",
}


@rule("deformation", "ee")
def post_impact_jam(e, o, s):
    if e.moving != "rotating" or o.moving == "rotating" or o.kind not in DEFORM_TXT or not adjacent(e, o):
        return None
    defl = DEFL[o.stiffness]
    clr = CLEAR.get(e.kind, 1.0)
    if defl < 0.5 * clr and o.kind not in ("motor_mount",):
        return None
    effect = {"wheel": "tyre rubs / wheel jams", "tyre": "tyre rubs -> drive stalls", "hub": "hub binds", "drive_shaft": "shaft binds",
              "gearbox": "gear loses mesh", "belt": "belt loses tension / rubs", "pulley": "pulley rubs / misaligns",
              "weapon_disc": "disc rubs chassis", "drive_motor": "pinion loses mesh", "weapon_motor": "belt tension lost",
              "bearing": "bearing cocked -> drag", "weapon_shaft": "shaft misaligned -> drag"}.get(e.kind, "jams")
    return H("post_impact_jam", f"{DEFORM_TXT[o.kind]} -> {effect}", min(1, 0.3 + 0.4 * defl / clr / 3), sorted(e.criticality)[0],
             detail=f"running clearance ~{clr} mm vs plastic set ~{defl} mm ({o.stiffness}-stiffness {o.label})")


@rule("deformation", "ee")
def cracked_flap_drag(e, o, s):
    if e.kind in ("base_panel", "skirt", "lip", "shell") and o.kind in ("tyre", "wheel") and adjacent(e, o):
        return H("cracked_flap_drag", f"cracked {e.label} flap drags on floor / into {o.label}", 0.35, "drive")


# ------------------------------------------------------------------ generation
PREVALENCE = {"vspin_disc": 0.9, "vspin_drum": 0.7, "eggbeater": 0.6, "hspin_bar": 0.6, "hspin_disc": 0.5, "undercutter": 0.5,
              "overcutter": 0.3, "hammer_axe": 0.3, "hammer_saw": 0.2, "wedge": 0.8, "fork_opp": 0.6, "lifter": 0.4, "flipper_servo": 0.6,
              "flipper_pneu": 0.3, "grabber": 0.2, "crusher": 0.15, "pusher": 0.5, "floor_wood": 1.0, "floor_steel": 0.5,
              "floor_splinters": 0.6, "floor_seams": 0.7, "arena_screws": 0.5, "floor_wall_gap": 0.5, "wall": 0.9, "pit": 0.3,
              "ceiling": 0.2, "debris_small": 0.6, "debris_large": 0.4, "start_square": 0.7, "own_weapon_gyro": 0.6,
              "own_weapon_spin": 0.6, "own_wheels": 0.8, "operator_handling": 0.9, "pin_insertion": 0.6, "charging": 0.5,
              "temperature": 0.6, "vibration": 1.0, "magnets": 0.1, "sparks": 0.4, "inversion_state": 0.6, "rf_noise": 0.4,
              "landing": 0.6}


def _key(*parts):
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:6].upper()


def raw_pairs():
    ea = len(ENTITIES) * len(AGENTS) * len(STATES)
    ee = len(ENTITIES) * (len(ENTITIES) - 1) * len(STATES)
    return ea, ee


def generate():
    """Return raw hypothesis records (one per rule firing)."""
    out = []
    for s in STATES:
        ents = [apply_state(e, s) for e in ENTITIES]
        for e in ents:
            for a in AGENTS:
                for name, fam, kind, fn in RULES:
                    if kind != "ea":
                        continue
                    h = fn(e, a, s)
                    if h:
                        out.append(dict(h, entity=e.kind, entity_label=e.label, agent=a.kind, family=fam, state=s, crit=sorted(e.criticality)))
            if s != "nominal":
                continue  # internal interactions are state-independent
            for o in ents:
                if o is e:
                    continue
                for name, fam, kind, fn in RULES:
                    if kind != "ee":
                        continue
                    h = fn(e, o, s)
                    if h:
                        out.append(dict(h, entity=e.kind, entity_label=e.label, agent="internal:" + o.kind, family=fam, state=s,
                                        crit=sorted(e.criticality)))
    return out


def cluster(raw):
    """Dedupe to (mechanism, entity, state[, partner]) clusters; drop state variants whose agent set equals nominal."""
    cl = {}
    for h in raw:
        partner = h["agent"] if h["agent"].startswith("internal:") else ""
        k = (h["mechanism"], h["entity"], h["state"], partner, h["title"] if partner else "")
        c = cl.setdefault(k, dict(h, agents=set(), likelihood=-1, titles=set()))
        c["agents"].add(h["agent"])
        c["titles"].add(h["title"])
        w = h["likelihood"] * (PREVALENCE.get(h["agent"], 0.6))
        if w > c["likelihood"]:
            c["likelihood"], c["rep_title"], c["rep_agent"] = w, h["title"], h["agent"]
    nominal = {(k[0], k[1], k[3]): v["agents"] for k, v in cl.items() if k[2] == "nominal"}
    res = []
    for k, c in cl.items():
        if k[2] != "nominal" and nominal.get((k[0], k[1], k[3])) == c["agents"] and c["mechanism"] not in ("state_exposure", "state_helpless",
                                                                                                         "inversion_effect", "indicator_hidden"):
            continue  # state adds nothing
        c["agents"] = sorted(c["agents"])
        c["titles"] = [c["rep_title"]] + sorted(c["titles"] - {c["rep_title"]})
        res.append(c)
    for c in res:
        ext = [a for a in c["agents"] if not a.startswith("internal:")]
        reach_score = min(1.0, 0.3 + 0.07 * len(ext)) if ext else 0.6
        crit = max(CRIT_W.get(x, 0.3) for x in c["crit"])
        c["rank"] = round(reach_score * crit * c["likelihood"] * STATE_LIKELIHOOD[c["state"]], 4)
        c["id"] = "CFX-" + _key(c["mechanism"], c["entity"], c["state"], c["agents"][0] if c["agents"][0].startswith("internal:") else "")
    res.sort(key=lambda c: -c["rank"])
    return res


# ------------------------------------------------------------------ coverage vs existing catalog
COVERED = {  # (mechanism, entity or '*') -> CF id; only nominal-state near-exact matches
    ("penetration_crush", "battery"): "CF-GD03", ("penetration_crush", "receiver"): "CF-GD04", ("antenna_snag", "antenna"): "CF-GD04",
    ("wire_entangle", "wire_motor"): "CF-GD08", ("heat_coupling", "battery"): "CF-GD09", ("thermal_overrun", "esc_weapon"): "CF-GD09",
    ("thermal_overrun", "esc_drive"): "CF-GD09", ("shock_dislodge", "conn_xt30"): "CF-GD07", ("shock_dislodge", "conn_jst"): "CF-GD07",
    ("weapon_drive_shock", "belt"): "CF-OW03", ("debris_ingress", "belt"): "CF-DB03", ("debris_ingress", "pulley"): "CF-DB03",
    ("debris_ingress", "gearbox"): "CF-DB05", ("debris_ingress", "drive_shaft"): "CF-DB05", ("debris_ingress", "tyre"): "CF-DB06",
    ("debris_ingress", "wheel"): "CF-DB01", ("debris_ingress", "weapon_shaft"): "CF-DB02", ("snag_protrusion", "screw"): "CF-AS05",
    ("snag_protrusion", "fork"): "CF-AS01", ("snag_protrusion", "lip"): "CF-AS03", ("snag_protrusion", "wedgelet"): "CF-AS01",
    ("snag_protrusion", "skirt"): "CF-HS05", ("inversion_effect", "battery"): "CF-OW05", ("gyro_effect", "wheel"): "CF-OW02",
    ("gyro_effect", "weapon_disc"): "CF-VS06", ("clamp_crush", "shell"): "CF-WL04", ("abrasion_cut", "wire_power"): "CF-HA03",
    ("edge_bite", "shell"): "CF-VS01", ("edge_bite", "armour_plate"): "CF-HS01", ("screw_head_bite", "screw"): "CF-VS01",
    ("brittle_fracture", "shell"): "CF-ST05", ("lift_lose_traction", "wheel"): "CF-WL02", ("mass_tear_out", "battery"): "CF-LD03",
    ("penetration_crush", "lid"): "CF-HA01", ("weapon_drive_shock", "bearing"): "CF-OW04", ("edge_bite", "lid"): "CF-VS05",
    ("inversion_effect", "self_righter"): "CF-WL05",
}


def coverage(c):
    if c["state"] != "nominal":
        return None
    return COVERED.get((c["mechanism"], c["entity"])) or COVERED.get((c["mechanism"], "*"))


# ------------------------------------------------------------------ cascades
LOSS_TO_STATE = {"power": "radio_failsafe", "radio": "radio_failsafe", "drive": "one_drive_dead", "weapon": "weapon_dead",
                 "armour": "shell_or_fork_lost", "structure": "shell_or_fork_lost", "safety": "partial_power"}
INVERTING = {"inversion_effect", "lift_lose_traction"}


def cascades(clusters, top_n=3):
    """For each cluster, 2- and 3-step chains: its lost function -> induced state -> best hypotheses in that state."""
    by_state = {}
    for c in clusters:
        by_state.setdefault(c["state"], []).append(c)
    for v in by_state.values():
        v.sort(key=lambda c: -c["rank"])

    def nxt(c):
        st = "inverted" if c["mechanism"] in INVERTING else LOSS_TO_STATE.get(c["loses"] or "", None)
        if not st or st == c["state"]:
            return st, []
        return st, [x for x in by_state.get(st, []) if x["entity"] != c["entity"]][:top_n]

    for c in clusters:
        chains = []
        st, n1 = nxt(c)
        for b in n1:
            p2 = c["likelihood"] * STATE_LIKELIHOOD[st] * b["likelihood"]
            chains.append(dict(steps=[c["id"], b["id"]], text=f"{c['titles'][0]} -> [{st}] -> {b['titles'][0]}", likelihood=round(p2, 4)))
            st2, n2 = nxt(b)
            for d in n2[:2]:
                if d["id"] in (c["id"], b["id"]):
                    continue
                p3 = p2 * STATE_LIKELIHOOD[st2] * d["likelihood"]
                chains.append(dict(steps=[c["id"], b["id"], d["id"]], text=f"{c['titles'][0]} -> [{st}] -> {b['titles'][0]} -> [{st2}] -> {d['titles'][0]}",
                                   likelihood=round(p3, 4)))
        chains.sort(key=lambda x: -x["likelihood"])
        c["cascade"] = chains[:5]
    return clusters

"""Combat ground game: the rules of robot/rules/combat_rules.md that can be judged from geometry and the spec.

"Whoever gets under the other wins": skirts, wedges and forks must sit a fraction of a millimetre above the floor around
as much of the perimeter as possible, wheels must not be the first thing an opponent meets, the weight must sit on the
driven wheels, and the robot must keep its ground game upside down. Each rule id (Rnnn) is the finding id
`combat.Rnnn`; the knowledge base gives rationale, criterion, threshold, applicability and severity for every rule,
including the ones listed here as NOT CHECKED.

Measurements come from `combat_ground.facts`; each rule is a pure function of those facts so it can be tested on its
own. Fail-closed: a rule whose facts are missing gives a WARNING finding and a NOT CHECKED line, never a silent pass. A
rule that does not apply to the robot's archetype (`archetype`, else `robot_type`) is skipped.
"""

from __future__ import annotations

import math

from ..finding import BLOCKER, WARNING, fail, ok
from . import combat_ground as cg

G = "combat"
NA = "na"
ALL = None
W, V, H, L = "wedge", "vspin", "hspin", "lifter"
LOWGAME = {W, V, L, "other"}  # robots that fight for the floor with a skirt, wedge or forks
SEAM_MM = 2.0  # arena floor seams and plate steps


def _f(v, d=1):
    return "?" if v is None else f"{v:.{d}f}"


def le(v, t, unit, what):
    if v is None:
        return None, f"{what}: not measured.", f"<= {t:g} {unit}", "?"
    return v <= t, f"{what} is {_f(v, 2)} {unit} (limit {t:g} {unit}).", f"<= {t:g} {unit}", f"{_f(v, 2)} {unit}"


def ge(v, t, unit, what):
    if v is None:
        return None, f"{what}: not measured.", f">= {t:g} {unit}", "?"
    return v >= t, f"{what} is {_f(v, 2)} {unit} (needs {t:g} {unit}).", f">= {t:g} {unit}", f"{_f(v, 2)} {unit}"


def rng(v, lo, hi, unit, what):
    if v is None:
        return None, f"{what}: not measured.", f"{lo:g} to {hi:g} {unit}", "?"
    return lo <= v <= hi, f"{what} is {_f(v, 2)} {unit} (range {lo:g} to {hi:g} {unit}).", f"{lo:g} to {hi:g} {unit}", f"{_f(v, 2)} {unit}"


def pct_ge(v, t, what):
    if v is None:
        return None, f"{what}: not measured.", f">= {t * 100:.0f}%", "?"
    return v >= t, f"{what} is {v * 100:.0f}% (needs {t * 100:.0f}%).", f">= {t * 100:.0f}%", f"{v * 100:.0f}%"


def pct_le(v, t, what):
    if v is None:
        return None, f"{what}: not measured.", f"<= {t * 100:.0f}%", "?"
    return v <= t, f"{what} is {v * 100:.0f}% (limit {t * 100:.0f}%).", f"<= {t * 100:.0f}%", f"{v * 100:.0f}%"


def worst(F, key, items, fn):
    """Apply a per-item rule and return the worst result (False beats None beats True); NA when there are no items."""
    if not items:
        return NA, "No such part.", None, None
    res = [(fn(d), d) for d in items]
    for want in (False, None):
        for (s, m, e, a), d in res:
            if s is want:
                return s, f"`{d['id']}`: {m}", e, a
    (s, m, e, a), d = res[0]
    return True, "; ".join(f"`{d['id']}`: {r[1]}" for r, d in res[:4]), e, a


def need(F, *keys):
    return all(F.get(k) is not None for k in keys)


def fam(F):
    return F.get("family", "other")


def front_skirts(F):
    return F.get("front_skirts") or []


def no_front_skirt(F):
    """A low-game robot without a front skirt fails the skirt rules; others skip them."""
    if fam(F) in (W, L):
        return False, "No wedge, fork or skirt reaches the front of the robot.", "a front skirt", "none"
    return NA, "No front skirt.", None, None


# ---- the rules ------------------------------------------------------------------------------------------------------

def r001(F):
    t = {W: 1.0, L: 1.0, V: 1.5}.get(fam(F), 3.0)
    return le(F.get("gap_med.front"), t, "mm", "Median edge gap across the front")


def r002(F):
    return pct_ge(F.get("cover_1.5.front"), 0.8, "Share of the front edge with a skirt within 1.5 mm of the floor")


def r003(F):
    return pct_ge(F.get("cover_3.left"), 0.6, "Share of the left (+X) side edge within 3 mm of the floor")


def r004(F):
    return pct_ge(F.get("cover_3.right"), 0.6, "Share of the right (-X) side edge within 3 mm of the floor")


def r005(F):
    return pct_ge(F.get("cover_3.rear"), 0.5, "Share of the rear edge within 3 mm of the floor")


def _corner(c):
    return lambda F: le(F.get(f"gap_max.{c}"), 5.0, "mm", f"Highest edge gap at the {c.split('_')[1].upper()} corner")


def r010(F):
    return pct_ge(F.get("cover_3.all"), 0.6, "Share of the whole perimeter within 3 mm of the floor")


def r011(F):
    return le(F.get("open_arc_deg"), 45.0, "deg", "Longest arc of the perimeter with nothing within 5 mm of the floor")


def r012(F):
    return le(F.get("gap_max.all"), 12.0, "mm", "Highest edge gap anywhere on the perimeter")


def r013(F):
    if fam(F) not in LOWGAME:
        return NA, "", None, None
    return le(F.get("gap_p20.front"), 0.6, "mm", "Front lip gap (20th percentile) against a typical 0.5 mm opponent wedge")


def r014(F):
    return le(F.get("gap_med.left") if (F.get("gap_med.left") or 0) >= (F.get("gap_med.right") or 0) else F.get("gap_med.right"),
              2.0, "mm", "Median side edge gap (worse side) when T-boned by a wedge")


def r015(F):
    return le(F.get("front_open_mm"), 8.0, "mm", "Widest stretch of the front edge with no skirt within 1.5 mm of the floor")


def r016(F):
    return le(F.get("front_gap_spread"), 3.0, "mm", "Spread of the edge gap across the front")


def r020(F):
    fs = front_skirts(F)
    if not fs:
        return no_front_skirt(F)
    return worst(F, "gap", fs, lambda d: ge(d["gap"], 0.2, "mm", "Lowest point above the floor"))


def r021(F):
    fs = [d for d in front_skirts(F) if not d["hinged"]]
    if not fs:
        return no_front_skirt(F) if not front_skirts(F) else (NA, "", None, None)
    return worst(F, "gap", fs, lambda d: le(d["gap"], 1.0, "mm", "Lip height above the floor"))


def r022(F):
    fs = [d for d in front_skirts(F) if d["kind"] == "wedge"]
    if not fs:
        return no_front_skirt(F) if fam(F) == W else (NA, "", None, None)
    hi = 35.0 if fam(F) == W else 45.0
    return worst(F, "ramp", fs, lambda d: rng(d["ramp_deg"], 10.0, hi, "deg", "Ramp angle (median over the lower 70% of the face)"))


def r023(F):
    fs = [d for d in front_skirts(F) if d["kind"] == "wedge"]
    if not fs:
        return NA, "", None, None
    return worst(F, "entry", fs, lambda d: le(d["entry_deg"], 25.0, "deg", "Entry angle over the first 10 mm"))


def r024(F):
    fs = front_skirts(F)
    if not fs:
        return no_front_skirt(F)
    return worst(F, "t1", fs, lambda d: le(d["t1"], 1.2, "mm", "Lip thickness 1 mm behind the edge"))


def r025(F):
    fs = front_skirts(F)
    if not fs:
        return no_front_skirt(F)
    return worst(F, "t3", fs, lambda d: le(d["t3"], 2.5, "mm", "Lip thickness 3 mm behind the edge"))


def r026(F):
    fs = front_skirts(F)
    if not fs:
        return no_front_skirt(F)
    return worst(F, "blunt", fs, lambda d: le(d["blunt_h"], 0.6, "mm", "Height of the vertical front face at the lip"))


def r027(F):
    fs = front_skirts(F)
    if not fs:
        return no_front_skirt(F)
    hard = {"steel", "hardox", "stainless", "304", "titanium", "aluminium", "aluminum", "cf_plate", "fr4", "g10", "uhmw"}
    bad = [d for d in fs if d["material"] not in hard]
    if any(d["material"] is None for d in fs):
        return None, "A skirt has no material.", "metal or laminate lip", "?"
    return (not bad, f"Lip material: {', '.join(f'`{d['id']}` {d['material']}' for d in fs)}; a printed lip chips and rounds over.",
            "metal or laminate lip", ", ".join(d["material"] for d in fs))


def r028(F):
    if not need(F, "skirt_width", "body_width"):
        return no_front_skirt(F) if not front_skirts(F) else (None, "Width not measured.", None, None)
    t = 0.85 if fam(F) in (W, L) else 0.4
    return pct_ge(F["skirt_width"] / F["body_width"], t, "Front skirt width over body width")


def r029(F):
    if not need(F, "skirt_front_y", "body_front_y"):
        return no_front_skirt(F) if not front_skirts(F) else (None, "", None, None)
    return ge(F["skirt_front_y"] - F["body_front_y"], -0.5, "mm", "Skirt lead over the rest of the body (spinning parts excluded)")


def r030(F):
    fs = front_skirts(F)
    if not fs:
        return no_front_skirt(F)
    def one(d):
        if d["tip_low"] is None or d["heel_low"] is None:
            return None, "Tip not measured.", None, None
        return ge(d["heel_low"] - d["tip_low"], -0.05, "mm", "Underside 3-13 mm behind the tip relative to the tip")
    return worst(F, "dig", fs, one)


def r031(F):
    fs = front_skirts(F)
    if not fs:
        return no_front_skirt(F)
    return worst(F, "spread", fs, lambda d: le(d["tip_spread"], 0.5, "mm", "Lip height variation across its width"))


def r032(F):
    fs = [d for d in front_skirts(F) if not d["hinged"]]
    if not fs:
        return no_front_skirt(F) if not front_skirts(F) else (NA, "", None, None)
    return worst(F, "defl", fs, lambda d: le(d.get("deflection"), 1.0, "mm", f"Tip deflection under {cg.TEST_LOAD_N:g} N (cantilever)"))


def r033(F):
    fs = front_skirts(F)
    if not fs:
        return no_front_skirt(F)
    def one(d):
        if d["t_mid"] is None:
            return (True, "No unsupported overhang.", None, None) if d["overhang"] == 0 or (d["overhang"] or 0) <= 0.5 else (None, "Thickness not measured.", None, None)
        metal = d["E"] is not None and d["E"] >= 60000
        return ge(d["t_mid"], 0.8 if metal else 2.0, "mm", "Skirt thickness at mid-overhang")
    return worst(F, "thick", fs, one)


def r034(F):
    fs = [d for d in front_skirts(F) if d["overhang"] is not None]
    if not front_skirts(F):
        return no_front_skirt(F)
    return worst(F, "over", fs, lambda d: le(d["overhang"], 45.0, "mm", "Unsupported overhang past the last support"))


def r035(F):
    fs = [d for d in F.get("skirts") or [] if d["hinged"]]
    if not fs:
        return NA, "", None, None
    return worst(F, "hinge", fs, lambda d: le(d["gap"], 0.5, "mm", "Hinged skirt resting gap"))


def r036(F):
    fs = [d for d in F.get("skirts") or [] if d["hinged"]]
    if not fs:
        return NA, "", None, None
    def one(d):
        j = d["joint"]
        span = abs(float(j.max) - float(j.min)) if j is not None else None
        return ge(span, 10.0, "deg" if j is None or j.kind != "prismatic" else "mm", "Hinged skirt travel")
    return worst(F, "travel", fs, one)


def r037(F):
    fs = [d for d in F.get("skirts") or [] if "wheel_gap" in d]
    if not fs:
        return NA, "", None, None
    return worst(F, "wgap", fs, lambda d: ge(d["wheel_gap"] - (d.get("deflection") or 0.0), 1.0, "mm",
                                              "Skirt clearance to the nearest wheel minus its load deflection"))


def r038(F):
    fs = [d for d in F.get("skirts") or [] if not d["hinged"]]
    if not fs:
        return NA, "", None, None
    return worst(F, "fast", fs, lambda d: ge(float(d["fasteners"]), 2.0, "", "Fasteners holding the skirt"))


def r040(F):
    forks = F.get("forks") or []
    if fam(F) not in (V, L) or not forks:
        return NA, "", None, None
    return ge(float(len(forks)), 2.0, "", "Fork tines")


def r041(F):
    if F.get("fork_open_mm") is None:
        return NA, "", None, None
    return le(F["fork_open_mm"], 25.0, "mm", "Widest gap between tines with nothing within 3 mm of the floor")


def r042(F):
    if F.get("fork_tip_spread") is None:
        return NA, "", None, None
    return le(F["fork_tip_spread"], 0.5, "mm", "Height difference between fork tips")


def r043(F):
    forks = F.get("forks") or []
    if not forks or F.get("struct_front_y") is None:
        return NA, "", None, None
    return ge(min(d["ymax"] for d in forks) - F["struct_front_y"], 0.0, "mm", "Fork tips ahead of the chassis")


def _wv(F, vertical):
    return [d for d in F.get("weapon") or [] if d.get("axis") is not None and d["vertical"] == vertical]


def r050(F):
    ws = _wv(F, True)
    if not ws:
        return NA, "", None, None
    return worst(F, "wgap", ws, lambda d: rng(d["gap"], 0.8, 6.0, "mm", "Vertical weapon sweep above the floor"))


def r051(F):
    ws = _wv(F, True) + _wv(F, False)
    if not ws:
        return NA, "", None, None
    return worst(F, "wfloor", ws, lambda d: ge(d["gap"], 0.3, "mm", "Weapon sweep above the floor"))


def r052(F):
    ws = _wv(F, False)
    if not ws:
        return NA, "", None, None
    return worst(F, "hgap", ws, lambda d: rng(d["gap"], 1.0, 15.0, "mm", "Horizontal blade above the floor"))


def r053(F):
    ws = _wv(F, True)
    if not ws:
        return NA, "", None, None
    def one(d):
        cover = [s for s in front_skirts(F) if s["x1"] >= d["x0"] - 3 and s["x0"] <= d["x1"] + 3 and s["gap"] <= 1.5]
        if cover:
            return True, f"A skirt ({', '.join(s['id'] for s in cover)}) closes the floor under the weapon.", "<= 5 mm or a skirt", "skirt"
        return le(d["gap"], 5.0, "mm", "Open floor gap under the weapon (no skirt below it)")
    return worst(F, "under", ws, one)


def r054(F):
    ws = _wv(F, True)
    if not ws or not front_skirts(F):
        return NA, "", None, None
    lead = max(d["front"] for d in ws) - F["skirt_front_y"]
    return rng(lead, -12.0, 3.0, "mm", "Weapon front relative to the skirt lip (negative = lip leads)")


def r060(F):
    s = F.get("driven_share")
    if F.get("com") is None or "driven_share" not in F:
        return None, "No centre of mass.", None, None
    if s is None:
        return False, "Nothing but the wheels touches the floor on the heavy side; the robot rests on its nose or tail.", ">= 70%", "?"
    return pct_ge(s, 0.7, "Weight on the driven wheels")


def r061(F):
    s = F.get("driven_share")
    if F.get("com") is None or "driven_share" not in F or s is None:
        return None, "Not measured.", None, None
    return pct_le(1.0 - s, 0.15, "Weight resting on the skirt or skids")


def r062(F):
    if not need(F, "cog_h", "track") or F["track"] <= 1:
        return None, "Not measured.", None, None
    return le(F["cog_h"] / F["track"], 0.5, "", "Centre-of-mass height over track")


def r063(F):
    if not need(F, "cog_h", "wheelbase") or F["wheelbase"] <= 1:
        return None, "Not measured.", None, None
    return le(F["cog_h"] / F["wheelbase"], 0.6, "", "Centre-of-mass height over wheelbase")


def r064(F):
    if not need(F, "cog_h", "body_height") or F["body_height"] <= 1:
        return None, "Not measured.", None, None
    return pct_le(F["cog_h"] / F["body_height"], 0.5, "Centre-of-mass height as a share of body height")


def r065(F):
    if not need(F, "com_lat_off", "track") or F["track"] <= 1:
        return None, "Not measured.", None, None
    return pct_le(F["com_lat_off"] / F["track"], 0.05, "Sideways centre-of-mass offset over track")


def r066(F):
    if not need(F, "com_long_margin", "wheelbase"):
        return None, "Not measured.", None, None
    return pct_ge(F["com_long_margin"] / F["wheelbase"], 0.1, "Centre of mass inside the wheelbase (share of wheelbase from the nearer end)")


def r067(F):
    mats = F.get("tyre_mats")
    if mats is None:
        return NA, "", None, None
    if any(m is None for m in mats):
        return None, "A wheel has no material.", None, None
    bad = [m for m in mats if m not in cg.GRIP]
    return not bad, f"Tyre materials: {', '.join(mats)}.", "tpu/silicone/rubber/urethane", ", ".join(mats)


def r068(F):
    return ge(F.get("wheel_dia"), 10.0 * SEAM_MM, "mm", "Smallest wheel diameter (10x a 2 mm seam)")


def r069(F):
    return ge(F.get("wheel_width"), 6.0, "mm", "Narrowest wheel width")


def r070(F):
    if F.get("driven_sides") is None:
        return NA, "", None, None
    return ge(float(F["driven_sides"]), 2.0, "", "Sides of the robot with a wheel")


def r071(F):
    if not need(F, "wheelbase_wheels", "track") or F["track"] <= 1 or F.get("n_wheels", 0) < 4:
        return NA, "", None, None
    return le(F["wheelbase_wheels"] / F["track"], 1.0, "", "4WD wheelbase over track (turning scrub)")


def r072(F):
    if not need(F, "track", "body_width"):
        return None, "Not measured.", None, None
    return pct_ge(F["track"] / F["body_width"], 0.5, "Track over body width")


def r073(F):
    if not need(F, "stall_torque_gcm", "wheel_dia", "mass_g", "mu"):
        return None, "Motor torque, wheel size, mass or tyre grip not known.", None, None
    r_m = F["wheel_dia"] / 2000.0
    thrust = sum(t * 9.81e-5 for t in F["stall_torque_gcm"]) / r_m
    grip = F["mu"] * F["mass_g"] * 1e-3 * 9.81 * (F.get("driven_share") or 1.0)
    return ge(thrust / grip, 1.0, "x", f"Motor stall thrust {thrust:.1f} N over traction limit {grip:.1f} N")


def r074(F):
    if not need(F, "motor_rpm", "wheel_dia"):
        return None, "Motor speed or wheel size not known.", None, None
    v = F["motor_rpm"] * math.pi * F["wheel_dia"] / 60000.0
    lo = 1.2 if fam(F) in (V, H) else 1.5
    return rng(v, lo, 8.0, "m/s", "Top speed at nominal voltage")


def r080(F):
    t = F.get("touching")
    if t is None:
        return None, "", None, None
    return (not t, ("Non-wheel parts within 0.1 mm of the floor: " + ", ".join(f"`{i}`" for i in t[:5])) if t else
            "Only the wheels touch the floor.", "wheels only", ", ".join(t[:5]) or "wheels only")


def r081(F):
    if F.get("n_wheels", 0) < 3:
        return NA, "", None, None
    return le(F.get("wheel_low_spread"), 0.3, "mm", "Height difference between wheel contacts")


def r082(F):
    return ge(F.get("belly_gap"), 1.0, "mm", "Lowest point of the chassis (skirts and wheels excluded)")


def r083(F):
    return ge(F.get("interior_gap"), 1.5, "mm", "Underside clearance away from the edges (high-centring on a seam)")


def r084(F):
    return le(F.get("drag_area_mm2"), 50.0, "mm2", "Flat chassis underside within 0.5 mm of the floor")


def r085(F):
    return ge(F.get("fastener_gap"), 0.5, "mm", "Lowest screw head above the floor")


def r086(F):
    if F.get("switch_gap") is None:
        return NA, "", None, None
    return ge(F["switch_gap"], 2.0, "mm", "Switch above the floor")


def r090(F):
    if F.get("inv_shortfall") is None:
        return NA, "", None, None
    if fam(F) == L:
        return True, "Lifter/flipper archetype: self-rights with its arm.", "invertible or self-righting", "self-righting"
    return le(F["inv_shortfall"], 0.5, "mm", "Body above the wheel tops (upside down the wheels must still reach the floor)")


def r091(F):
    if F.get("inv_shortfall") is None or F["inv_shortfall"] > 0.5:
        return NA, "", None, None
    return pct_ge(F.get("inv_cover_3.front"), 0.5, "Upside down, share of the front edge within 3 mm of the floor")


def r092(F):
    if F.get("inv_shortfall") is None or F["inv_shortfall"] > 0.5:
        return NA, "", None, None
    return ge(F.get("inv_min_gap"), 0.2, "mm", "Upside down, lowest non-wheel edge above the floor")


def r093(F):
    if F.get("inv_shortfall") is None or F["inv_shortfall"] > 0.5 or not F.get("inv_weapon_gap"):
        return NA, "", None, None
    return rng(min(F["inv_weapon_gap"]), 0.3, 10.0, "mm", "Upside down, weapon sweep above the floor")


def r094(F):
    if F.get("inv_shortfall") is None or F["inv_shortfall"] > 0.5:
        return NA, "", None, None
    return le(F.get("body_height"), (F.get("wheel_dia") or 0) - 1.0, "mm", "Body height for an invertible robot (wheel diameter - 1 mm)")


def r100(F):
    return le(F.get("body_height"), 45.0, "mm", "Body height without wheels and weapon")


def r101(F):
    if fam(F) not in (W, L):
        return NA, "", None, None
    return pct_le(F.get("vertical_frac.front"), 0.5, "Vertical share of the front-facing outer surface")


def r102(F):
    if fam(F) == H:
        return NA, "", None, None
    return pct_le(F.get("vertical_frac.sides"), 0.9, "Vertical share of the side-facing outer surface")


def r110(F):
    return pct_le(F.get("wheel_edge.front"), 0.0, "Share of front bearings where a wheel is the outermost part")


def r111(F):
    v = [F.get("wheel_edge.left"), F.get("wheel_edge.right")]
    return pct_le(None if None in v else max(v), 0.25, "Share of the worse side where a wheel is the outermost part")


def r112(F):
    return pct_le(F.get("wheel_edge.rear"), 0.25, "Share of rear bearings where a wheel is the outermost part")


def r113(F):
    return pct_le(F.get("wheel_edge.all"), 0.10, "Share of the whole perimeter where a wheel is the outermost part (horizontal spinner target)")


def r114(F):
    if not need(F, "body_front_y", "wheel_front_y"):
        return None, "Not measured.", None, None
    return ge(F["body_front_y"] - F["wheel_front_y"], 5.0, "mm", "Body ahead of the front-most wheel")


def r115(F):
    if not need(F, "body_max_x", "wheel_max_x"):
        return None, "Not measured.", None, None
    return ge(min(F["body_max_x"] - F["wheel_max_x"], F["wheel_min_x"] - F["body_min_x"]), 0.0, "mm", "Side wall outboard of the wheels")


def r116(F):
    if F.get("wheel_top") is None or F.get("body_height") is None:
        return None, "Not measured.", None, None
    if F.get("inv_shortfall") is not None and F["inv_shortfall"] <= 0.5:
        return NA, "", None, None
    return le(F["wheel_top"] - F["floor"] - F["body_height"], 0.0, "mm", "Wheel top above the body top (non-invertible: wheels proud of the top get hit)")


def r120(F):
    return ge(F.get("battery_front_clear"), 10.0, "mm", "Battery behind the front outline")


def r121(F):
    return ge(F.get("battery_side_clear"), 5.0, "mm", "Battery inside the side outline")


# (id, severity, title, fix, fn, applies-to families or None for all)
RULES = [
    ("R001", WARNING, "Front edge sits on the floor", "Lower the front skirt/wedge lip to 0.3-1 mm.", r001, None),
    ("R002", WARNING, "Front edge covered by a low skirt", "Run the wedge/skirt across the whole front at 0.3-1 mm.", r002, LOWGAME),
    ("R003", WARNING, "Left side has a low skirt", "Add a side skirt or bring the side wall within 3 mm of the floor.", r003, LOWGAME | {H}),
    ("R004", WARNING, "Right side has a low skirt", "Add a side skirt or bring the side wall within 3 mm of the floor.", r004, LOWGAME | {H}),
    ("R005", WARNING, "Rear edge is guarded", "Add a rear skirt or lower the rear wall to within 3 mm.", r005, None),
    ("R006", WARNING, "Front-left corner closed", "Wrap the skirt round the corner or chamfer it down to the floor.", _corner("corner_fl"), None),
    ("R007", WARNING, "Front-right corner closed", "Wrap the skirt round the corner or chamfer it down to the floor.", _corner("corner_fr"), None),
    ("R008", WARNING, "Rear-right corner closed", "Wrap the skirt round the corner or chamfer it down to the floor.", _corner("corner_rr"), None),
    ("R009", WARNING, "Rear-left corner closed", "Wrap the skirt round the corner or chamfer it down to the floor.", _corner("corner_rl"), None),
    ("R010", WARNING, "Perimeter mostly skirted", "Bring more of the outline down to within 3 mm of the floor.", r010, None),
    ("R011", WARNING, "No wide open arc", "Close the open arc with a skirt or a low wall.", r011, None),
    ("R012", WARNING, "No open door anywhere", "Nothing on the outline should leave more than 12 mm under it.", r012, None),
    ("R013", WARNING, "Gets under a typical wedge", "Lip at or below 0.5 mm wins the who-gets-under contest.", r013, LOWGAME),
    ("R014", WARNING, "Sides resist a T-bone", "Lower the side skirts so a wedge hitting the side cannot get under.", r014, None),
    ("R015", WARNING, "No fork-sized gap in the front edge", "Close gaps in the front skirt wider than 8 mm (opponent forks slip in).", r015, LOWGAME),
    ("R016", WARNING, "Front edge level", "Make the front edge height even across the width.", r016, LOWGAME),
    ("R020", WARNING, "Lip clears the floor", "Raise the lip to >= 0.2 mm so it does not drag or catch seams.", r020, None),
    ("R021", WARNING, "Lip is low enough", "Lower a fixed lip to <= 1.0 mm (or hinge it to rest on the floor).", r021, None),
    ("R022", WARNING, "Ramp angle", "Set the wedge face between 10 and 35 deg (wedges) / 45 deg (others).", r022, None),
    ("R023", WARNING, "Shallow entry", "Make the first 10 mm of the wedge no steeper than 25 deg.", r023, None),
    ("R024", WARNING, "Sharp lip", "Bevel the lip to <= 1.2 mm thick 1 mm back (or use 1 mm sheet).", r024, None),
    ("R025", WARNING, "Thin lip", "Keep the lip <= 2.5 mm thick 3 mm behind the edge.", r025, None),
    ("R026", WARNING, "No blunt nose", "Remove the vertical face at the lip (> 0.6 mm stops it sliding under).", r026, None),
    ("R027", WARNING, "Hard lip", "Make the lip from steel/titanium/aluminium/laminate, or face it with metal.", r027, LOWGAME),
    ("R028", WARNING, "Skirt spans the front", "Widen the front skirt.", r028, None),
    ("R029", WARNING, "Skirt is the front-most part", "Bring the skirt lip forward of every other body part.", r029, LOWGAME),
    ("R030", WARNING, "Tip does not dig in", "Make the lip the lowest point; raise the underside behind it.", r030, None),
    ("R031", WARNING, "Lip parallel to the floor", "Level the lip across its width (<= 0.5 mm variation).", r031, None),
    ("R032", WARNING, "Skirt stiff under push", f"Thicken, shorten or support the skirt so it bends <= 1 mm under {cg.TEST_LOAD_N:g} N.", r032, None),
    ("R033", WARNING, "Skirt thick enough", "Metal skirts >= 0.8 mm, printed or plastic >= 2 mm at mid-overhang.", r033, None),
    ("R034", WARNING, "Skirt overhang short", "Support the skirt within 45 mm of its tip.", r034, None),
    ("R035", WARNING, "Hinged skirt rests on the floor", "Let a hinged skirt rest at <= 0.5 mm.", r035, None),
    ("R036", WARNING, "Hinged skirt can lift", "Give a hinged skirt >= 10 deg of travel.", r036, None),
    ("R037", WARNING, "Skirt clears the wheels", "Keep >= 1 mm between skirt and wheels after deflection.", r037, None),
    ("R038", WARNING, "Skirt bolted down", "Fix each skirt with >= 2 fasteners.", r038, None),
    ("R040", WARNING, "At least two tines", "Use two or more forks.", r040, {V, L}),
    ("R041", WARNING, "Tines close together", "Keep gaps between tines <= 25 mm, or close them with the weapon/skirt.", r041, None),
    ("R042", WARNING, "Tines level", "Set every fork tip at the same height (<= 0.5 mm).", r042, None),
    ("R043", WARNING, "Tines lead the chassis", "Make the fork tips the front of the chassis.", r043, None),
    ("R050", WARNING, "Vertical weapon sweeps low", "Sweep the disc/drum 0.8-6 mm above the floor to hit wedges.", r050, {V}),
    ("R051", BLOCKER, "Weapon clears the floor", "Raise the weapon axle: the weapon would strike the floor.", r051, None),
    ("R052", WARNING, "Horizontal blade height", "Keep a horizontal blade 1-15 mm above the floor.", r052, {H}),
    ("R053", WARNING, "No gap under the weapon", "Close the floor under the weapon with a skirt or lower the weapon to <= 5 mm.", r053, {V}),
    ("R054", WARNING, "Weapon and lip in step", "The lip should lead the weapon sweep by 0-12 mm (or the weapon lead by <= 3 mm).", r054, {V}),
    ("R060", WARNING, "Weight on the driven wheels", "Move mass over the axle (>= 70% on driven wheels).", r060, None),
    ("R061", WARNING, "Skirt is not carrying the robot", "Lift the skirt or move mass back (<= 15% on skirts/skids).", r061, None),
    ("R062", WARNING, "Low centre of mass (track)", "Lower the battery and motors or widen the track.", r062, None),
    ("R063", WARNING, "Low centre of mass (wheelbase)", "Lower the mass or lengthen the wheelbase.", r063, None),
    ("R064", WARNING, "Not top-heavy", "Keep the centre of mass in the lower half of the body.", r064, None),
    ("R065", WARNING, "Centred sideways", "Balance left and right (<= 5% of track).", r065, None),
    ("R066", WARNING, "Centre of mass inside the wheelbase", "Keep the centre of mass >= 10% of the wheelbase from either contact line.", r066, None),
    ("R067", WARNING, "Grippy tyres", "Use TPU, silicone, rubber or urethane tyres.", r067, None),
    ("R068", WARNING, "Wheels roll over seams", "Use wheels >= 20 mm diameter.", r068, None),
    ("R069", WARNING, "Wide enough tyres", "Use tyres >= 6 mm wide.", r069, None),
    ("R070", BLOCKER, "Wheels on both sides", "Put a driven wheel on each side for skid steering.", r070, None),
    ("R071", WARNING, "4WD turns", "Shorten the wheelbase to <= the track (skid-steer scrub).", r071, None),
    ("R072", WARNING, "Wide track", "Track >= 50% of body width.", r072, None),
    ("R073", WARNING, "Drive can spin the wheels", "More torque or a lower gear: the drive should be traction-limited.", r073, None),
    ("R074", WARNING, "Drive speed", "Pick a gear/wheel size for 1.5-8 m/s (1.2 for spinners).", r074, None),
    ("R080", WARNING, "Only wheels touch the floor", "Raise rigid parts off the floor (no drag, no rocking).", r080, None),
    ("R081", WARNING, "Wheels coplanar", "Put every wheel contact within 0.3 mm (no rocking).", r081, None),
    ("R082", WARNING, "Belly clears the floor", "Raise the chassis underside to >= 1 mm.", r082, None),
    ("R083", WARNING, "No high-centring", "Keep >= 1.5 mm under the interior so a 2 mm seam does not lift the wheels.", r083, None),
    ("R084", WARNING, "No flat dragging belly", "Recess flat underside areas that sit within 0.5 mm of the floor.", r084, None),
    ("R085", WARNING, "Screw heads off the floor", "Countersink or recess screw heads on the underside.", r085, None),
    ("R086", WARNING, "Switch off the floor", "Mount the switch >= 2 mm above the floor.", r086, None),
    ("R090", WARNING, "Invertible or self-righting", "Make the wheels stand proud of the top, or add a self-righting mechanism.", r090, None),
    ("R091", WARNING, "Ground game upside down", "Give the top side a skirt/wedge edge too (double-sided wedge).", r091, LOWGAME),
    ("R092", WARNING, "No drag upside down", "Keep the top edges >= 0.2 mm off the floor when inverted.", r092, None),
    ("R093", WARNING, "Weapon works upside down", "Inverted weapon sweep 0.3-10 mm above the floor.", r093, None),
    ("R094", WARNING, "Body fits inside the wheels", "Body height <= wheel diameter - 1 mm for an invertible robot.", r094, None),
    ("R100", WARNING, "Low profile", "Keep the body under 45 mm tall.", r100, None),
    ("R101", WARNING, "Front armour sloped", "Slope the front faces (<= 50% vertical).", r101, None),
    ("R102", WARNING, "Side armour angled", "Angle or round the side walls (<= 90% vertical).", r102, None),
    ("R110", WARNING, "No wheel at the front edge", "Put a skirt or wall ahead of the wheels.", r110, None),
    ("R111", WARNING, "Wheels shielded at the sides", "Add side pods/walls outboard of the wheels.", r111, None),
    ("R112", WARNING, "Wheels shielded at the rear", "Add a rear wall or skirt behind the wheels.", r112, None),
    ("R113", WARNING, "Wheels not the spinner target", "Shield the wheels on the perimeter (<= 10% exposed).", r113, None),
    ("R114", WARNING, "Body ahead of the wheels", "Keep >= 5 mm of body ahead of the front-most wheel.", r114, None),
    ("R115", WARNING, "Side wall outboard of wheels", "Move the wheels inboard of the side walls.", r115, None),
    ("R116", WARNING, "Wheels below the top", "On a non-invertible robot keep wheels below the top armour.", r116, None),
    ("R120", WARNING, "Battery away from the front", "Keep the battery >= 10 mm behind the front outline.", r120, None),
    ("R121", WARNING, "Battery away from the sides", "Keep the battery >= 5 mm inside the side outline.", r121, None),
]

NOT_CHECKED = [
    ("R017", "Arena seam crossing at speed (dynamic bounce over a 1-2 mm step)"),
    ("R018", "Skirt wear and lip rounding over a fight"),
    ("R039", "Countersunk skirt screws flush with the ramp (head protrusion above the ramp face)"),
    ("R044", "Fork tine stiffness under a 50 N side load"),
    ("R045", "Fork tip shape (pointed vs square) against opponent wedge lips"),
    ("R055", "Vertical weapon spin direction (checked by kin.spin_dir)"),
    ("R056", "Weapon hit reaction: hop and recoil wheelie of the robot"),
    ("R057", "Gyroscopic lift/walk of a vertical spinner while turning (see dynamics gyro)"),
    ("R058", "Horizontal spinner recoil spin-out after a hit"),
    ("R059", "Weapon spin-up time vs closing distance"),
    ("R075", "Acceleration and closing time across the arena"),
    ("R076", "Tyre hardness (Shore) and dust pickup"),
    ("R077", "Tyre compression under load lowering the skirt"),
    ("R078", "Drive current limit while pushing (ESC/BEC)"),
    ("R079", "Driver control: steering response and drive mixing"),
    ("R087", "Ground effect of wires and loose tape under the robot"),
    ("R088", "Battery puncture risk from floor impacts"),
    ("R095", "Self-righting mechanism actually rights the robot"),
    ("R096", "Inverted controls (remote mixing flip)"),
    ("R097", "Behaviour on its side (rolls back onto wheels)"),
    ("R103", "Top armour protrusions that a lifter can hook"),
    ("R104", "Overhangs on the outline that trap an opponent's wedge"),
    ("R105", "Armour material per face vs the expected weapon"),
    ("R117", "Wheel hubs survive a side hit (hub/axle strength)"),
    ("R118", "Wheel guards stiff enough to stop a spinner"),
    ("R122", "Pit and arena edge: rear overhang falling into the pit"),
    ("R123", "Arena wall: skirt catching the wall bottom rail"),
    ("R124", "Pushing match outcome vs a heavier opponent (mass + grip)"),
    ("R125", "Lifter/flipper arm stays below the skirt line when lowered"),
]


def run(ctx):
    out = []
    F = cg.facts(ctx)
    if "floor" not in F:
        ctx.not_checked.append("Combat ground game: no solid parts")
        return [fail("combat.no_geometry", G, WARNING, "No geometry", "No solid parts to judge the ground game on.")]
    family = F["family"]
    ctx.metrics["combat.family"] = family
    for k in ("gap_med.front", "cover_3.all", "open_arc_deg", "driven_share", "front_open_mm"):
        if isinstance(F.get(k), (int, float)):
            ctx.metrics[f"combat.{k}"] = float(F[k])
    for rid, sev, title, fix, fn, fams in RULES:
        if fams is not None and family not in fams:
            continue
        try:
            res = fn(F)
        except Exception as e:  # noqa: BLE001 - one bad rule must not hide the others
            res = (None, f"rule raised {type(e).__name__}: {e}", None, None)
        st, msg, exp, act = res
        fid = f"combat.{rid}"
        if st == NA:
            continue
        if st is None:
            ctx.not_checked.append(f"{fid} {title}: {msg}")
            out.append(fail(fid, G, WARNING, f"{title} (not measured)", msg).fix("Supply the missing data (mass, material, catalog motor)."))
        elif st:
            out.append(ok(fid, G, title, msg))
        else:
            f = fail(fid, G, sev, title, msg).fix(fix)
            if exp is not None:
                f.expect(exp, act)
            out.append(f)
    for rid, what in NOT_CHECKED:
        ctx.not_checked.append(f"combat.{rid}: {what}")
    return out

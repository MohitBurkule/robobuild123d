"""The 61 combat failure modes (research/combat_failure_modes.json, copied as `modes.json`) as pure rules on the facts
of `threat.facts`. Each rule returns (status, message, expected, actual):

  True  pass            False  fail at the catalogue severity        WARN  fail, escalated to a warning (VS04 >= 300 mm)
  None  not measured (warning + NOT CHECKED)     NA  does not apply      SKIP  not measured in this run mode (NOT CHECKED)

Assumptions where the catalogue leaves a number open are in each rule's docstring; the attack model and capacities are
in `attack.py`.
"""

from __future__ import annotations

import math

from . import attack as A

NA, SKIP, WARN = "na", "skip", "warn"
LOWGAME = ("wedge", "vspin", "lifter", "other")


def _f(v, d=1):
    return "?" if v is None else f"{v:.{d}f}"


def _need(*vals):
    return all(v is not None for v in vals)


def _mass(T):
    return T.get("mass_g")


# ---------------------------------------------------------------------------------------------------- A. vertical spinners

def vs01(T):
    """Largest exposed vertical step (faces within 35 deg of facing the attacker) a vertical-spinner tooth meets in the
    front/side band z 0-40 mm, elevation 0 and 30 deg. Step height = longest run of such faces in a 2 mm column.
    Threshold 0.5 * bite depth (reference 3 m/s, 2 teeth, 15000 rpm -> 6 mm bite, 3 mm step)."""
    s, d = T.get("vs01.step_mm"), T.get("bite_mm")
    if not _need(s, d):
        return None, "Front/side faces not measured.", None, None
    lim = 0.5 * d
    w = T.get("vs01.where")
    at = f" at `{w[0]}` (attack bearing {w[1]} deg, elevation {w[2]:.0f} deg)" if w else ""
    return s < lim, f"Tallest exposed bite step is {s:.1f} mm{at}; a {d:.0f} mm tooth bite catches steps >= {lim:.1f} mm.", f"< {lim:.1f} mm", f"{s:.1f} mm"


def vs02(T):
    """Front lips: metal lips need impact capacity U >= 0.5 * 25 J (elastic + ductile energy of the lip volume, see
    `attack.energy_capacity_j`); printed lips must be TPU or backed by a metal part within 1 mm."""
    lips = T.get("front_lips")
    if lips is None:
        return None, "Lips not measured.", None, None
    if not lips:
        return NA, "", None, None
    need = 0.5 * A.E_TIP_REF_J
    bad = []
    for x in lips:
        if x["metal"]:
            if x["U_j"] is None or x["U_j"] < need:
                bad.append(f"`{x['id']}` metal lip absorbs {_f(x['U_j'])} J (needs {need:.1f} J)")
        elif not (str(x["material"]).startswith("tpu") or x["backed"]):
            bad.append(f"`{x['id']}` is {x['material']} with no metal backing")
    if bad:
        return False, "; ".join(bad) + ".", f">= {need:.1f} J metal / TPU or metal-backed print", "; ".join(bad)
    return True, f"{len(lips)} front lip(s) survive a glancing 25 J hit.", None, None


def vs03(T):
    """Fork tine gap vs a reference tooth (6-12 mm): a gap <= 8 mm (or a solid lip) keeps the tooth out. Bolt failsafe
    (tine fixings weaker than the chassis) is not measured - reported in the message only."""
    forks = T.get("forks")
    if forks is None:
        return None, "Forks not measured.", None, None
    if len(forks) < 2:
        return NA, "", None, None
    g = T.get("fork_open_mm")
    if g is None:
        return None, "Tine gap not measured.", None, None
    return g <= 8.0, f"Widest open gap between tines at the lip is {g:.1f} mm (a 6-12 mm tooth fits gaps > 8 mm). Make tine fixings the weak link.", "<= 8 mm", f"{g:.1f} mm"


def vs04(T):
    """Launch apex after a vertical-spinner hit. Assumption: impulse J = 2 * 25 J / 40 m/s; 35% goes vertical, scaled by
    how high the contact sits relative to the CG (s = clamp(0.2 + 0.8 h_c / z_cg, 0.2, 1)); apex = v_z^2 / 2g.
    > 100 mm -> info, >= 300 mm -> warning."""
    m, hc, zc = _mass(T), T.get("gap_p20.front"), T.get("cog_h")
    if not _need(m, hc, zc):
        return None, "Mass, CG height or front contact height not measured.", None, None
    J = 2 * A.E_TIP_REF_J / A.V_TIP_REF_MS
    sh = min(max(0.2 + 0.8 * max(hc, 0.0) / max(zc, 1.0), 0.2), 1.0)
    vz = 0.35 * sh * J / (m * 1e-3)
    apex = vz * vz / (2 * 9.81) * 1000
    msg = f"Predicted launch apex {apex:.0f} mm (contact {hc:.1f} mm vs CG {zc:.1f} mm above the floor, mass {m:.0f} g)."
    if apex >= 300:
        return WARN, msg + " Landing damage (CF-LD*) likely.", "< 300 mm", f"{apex:.0f} mm"
    return apex <= 100, msg, "<= 100 mm", f"{apex:.0f} mm"


def vs05(T):
    """Share of the front silhouette in the drum band (z 15-45 mm) whose faces are within 30 deg of facing the drum."""
    v = T.get("vs05.blunt_frac")
    if v is None:
        return None, "Front face not measured.", None, None
    return v < 0.15, f"{v * 100:.0f}% of the front at drum height (15-45 mm) is a vertical catch face.", "< 15%", f"{v * 100:.0f}%"


def vs06(T):
    """Own vertical weapon: upright SF = yield / (2 x strength.upright stress) >= 2 and >= 2 bolts M2+ per upright."""
    if not T.get("weapon_vertical"):
        return NA, "", None, None
    sf, bolts = T.get("vs06.sf"), T.get("vs06.bolts")
    if sf is None:
        return None, "No upright stress from the strength group.", None, None
    bad = []
    if sf[0] < 2.0:
        bad.append(f"upright `{sf[1]}` SF {sf[0]:.2f} at 2x dynamic load")
    if bolts is not None and bolts[0] < 2:
        bad.append(f"upright `{bolts[1]}` has {bolts[0]} M2+ bolts")
    if bad:
        return False, "; ".join(bad) + ".", "SF >= 2, >= 2 M2+ bolts", "; ".join(bad)
    return True, f"Uprights SF {sf[0]:.2f} at 2x dynamic load, bolted M2+ x2.", None, None


# ---------------------------------------------------------------------------------------------------- B. horizontal spinners

def hs01(T):
    """Share of bearings (all round, every 10 deg) where the first faces hit at z 2-15 mm are vertical (+/-15 deg) and not
    a skirt/wedge."""
    v = T.get("hs01.vert_frac")
    if v is None:
        return None, "Side band not measured.", None, None
    return v < 0.3, f"{v * 100:.0f}% of the perimeter shows a vertical wall to a horizontal blade at 2-15 mm.", "< 30%", f"{v * 100:.0f}%"


def hs02(T):
    e = T.get("hs02.exposed")
    if e is None:
        return None, "Wheel exposure not measured.", None, None
    if not e:
        return True, "No wheel is the first thing hit at wheel-centre height (outside the rear +/-20 deg).", None, None
    return False, f"A wheel is hit first at wheel-centre height from {len(e)} bearings (e.g. {', '.join(str(x) for x in e[:6])} deg; 90 = front).", "0 bearings", f"{len(e)} bearings"


def hs03(T):
    p = T.get("hs03.top_parts")
    if p is None:
        return None, "Top not measured.", None, None
    return not p, ("No switch, receiver, belt, ESC or battery in the top 5 mm." if not p else f"In the top 5 mm (overcutter reach): {', '.join(p)}."), "none", ", ".join(p) or "none"


def hs04(T):
    """Info: yaw rate after a 25 J horizontal hit at the outline corner (J = 2E/v, I_z = m (L^2 + W^2) / 12)."""
    m, hx, hy = _mass(T), T.get("half_x"), T.get("half_y")
    if not _need(m, hx, hy):
        return None, "Mass or outline not measured.", None, None
    J = 2 * A.E_TIP_REF_J / A.V_TIP_REF_MS
    Iz = m * 1e-3 * ((2 * hx * 1e-3) ** 2 + (2 * hy * 1e-3) ** 2) / 12
    w = J * max(hx, hy) * 1e-3 / Iz / (2 * math.pi)
    return True, f"Predicted spin after a 25 J side hit: {w:.1f} rev/s (wider track and low CG reduce it).", None, f"{w:.1f} rev/s"


def hs05(T):
    """Skirt lip lift under a 2 N upward pull: rigid lips use the cantilever deflection (combat ground facts, scaled from
    50 N); hinged lips lift freely unless the part declares `preload_n` >= 2."""
    lips = T.get("lips")
    if lips is None:
        return None, "Skirts not measured.", None, None
    if not lips:
        return NA, "", None, None
    bad = []
    for x in lips:
        if x["hinged"]:
            if x["preload_n"] < 2.0:
                bad.append(f"`{x['id']}` hinged, no 2 N preload")
        elif x.get("deflection") is not None and x["deflection"] * 2.0 / 50.0 > 1.0:
            bad.append(f"`{x['id']}` lifts {x['deflection'] * 2 / 50:.1f} mm")
    if bad:
        return False, "; ".join(bad) + ".", "<= 1 mm at 2 N", "; ".join(bad)
    return True, "Skirt lips stay down under a 2 N lift.", None, None


# ---------------------------------------------------------------------------------------------------- C. hammers / saws

def ha01(T):
    """Top-plate punch capacity over critical parts: plate ductile energy over a disc of radius = distance to its edge
    (5-30 mm), scaled by `ENERGY_FRACTION`; >= 5 J."""
    v = T.get("ha01.min_cap_j")
    if v is None:
        return None, "Top plate not measured.", None, None
    return v >= A.E_HAMMER_J, f"Weakest top cell over electronics/motors holds {v:.1f} J (`{T.get('ha01.where')}`); a 5 J axe blow.", ">= 5 J", f"{v:.1f} J"


def ha02(T):
    b = T.get("ha02.bad")
    if b is None:
        return None, "Top plate not measured.", None, None
    if not b:
        return True, "No battery/ESC/receiver within 10 mm under a top cell weaker than 5 J.", None, None
    s = "; ".join(f"`{c}` {g} mm under `{p}` ({cap} J)" for c, p, g, cap in b[:4])
    return False, s + ".", "none", s


def ha03(T):
    if not T.get("n_routes"):
        return (SKIP if T.get("n_wires") else NA), "No routed wires in this run (wiring routes come from --full).", None, None
    v = T.get("ha03.min_mm")
    if v is None:
        return None, "Routes not measured.", None, None
    return v[0] > 4.0, f"Wire `{v[1]}` passes {v[0]:.1f} mm under the top surface.", "> 4 mm", f"{v[0]:.1f} mm"


# ---------------------------------------------------------------------------------------------------- D. wedges / lifters

def wl01(T):
    """Front win fraction: share of front bearings whose edge gap <= the median reference opponent lip (0.3 mm)."""
    if T.get("family") not in LOWGAME:
        return NA, "", None, None
    v = T.get("wl01.win_front")
    if v is None:
        return None, "Front edge not measured.", None, None
    return v >= 0.7, f"Front edge beats a {T.get('wl01.ref_mm', 0.3):.1f} mm reference lip on {v * 100:.0f}% of bearings.", ">= 70%", f"{v * 100:.0f}%"


def wl02(T):
    f, W = T.get("wl02.com_rear_frac"), T.get("wl02.lift_j")
    if f is None:
        return None, "CG not measured.", None, None
    msg = f"CG sits {f * 100:.0f}% of the length back from the front; lifting the nose 45 deg takes {_f(W, 2)} J."
    return f <= 0.6, msg, "<= 60% toward the rear", f"{f * 100:.0f}%"


def wl03(T):
    """Grab pockets: concave pockets deeper than 5 mm in the side or top outline (sampled by `m_pockets`)."""
    p = T.get("wl03.pocket")
    if p is None:
        return None, "Outline not measured.", None, None
    return p[0] <= 5.0, f"Deepest concave pocket in the {p[1]} outline is {p[0]:.1f} mm.", "<= 5 mm", f"{p[0]:.1f} mm"


def wl04(T):
    """Crusher: 200 N centre load on the top plate over the battery (simply supported, span = plate width, beam width =
    battery width) must deflect less than the gap to the battery."""
    d, g = T.get("wl04.defl_mm"), T.get("wl04.gap_mm")
    if g is None:
        return NA, "", None, None
    if d is None:
        return None, "Plate material unknown.", None, None
    return d < g, f"`{T.get('wl04.plate')}` deflects {d:.2f} mm under 200 N; the battery is {g:.1f} mm below.", f"< {g:.1f} mm", f"{d:.2f} mm"


def wl05(T):
    """Flip landing recovery: runs inverted, self-rights or has a flipper/lifter (see combat.R090-R093)."""
    return bool(T.get("self_right")), ("Can fight or recover upside down." if T.get("self_right") else
                                       "No invertible drive or self-righting after a flip (see combat.R090)."), "invertible or self-righting", None


def wl06(T):
    """Stalemate push = min(traction mu * share * m g, motor stall force) per 100 g of robot."""
    m, mu, sh, tq, D = _mass(T), T.get("mu"), T.get("driven_share"), T.get("stall_torque_gcm"), T.get("wheel_dia")
    if not _need(m, mu, sh, D) or not m:
        return None, "Mass, tyre grip, weight share or wheel size not measured.", None, None
    trac = mu * sh * m * 1e-3 * 9.81
    push = trac
    if tq:
        push = min(trac, sum(tq) * 9.81e-5 / (D / 2000))
    per = push / (m / 100)
    return per >= 1.3, f"Push {push:.2f} N = {per:.2f} N per 100 g.", ">= 1.3 N / 100 g", f"{per:.2f}"


def wl07(T):
    f, l, r = T.get("gap_med.front"), T.get("gap_med.left"), T.get("gap_med.right")
    if not _need(f, l, r):
        return None, "Edge gaps not measured.", None, None
    s = max(l, r)
    return s <= f + 1.0, f"Side median edge gap {s:.1f} mm vs front {f:.1f} mm.", f"<= {f + 1:.1f} mm", f"{s:.1f} mm"


# ---------------------------------------------------------------------------------------------------- E. arena

def ar01(T):
    keys = ("wheel_max_x", "body_max_x", "wheel_min_x", "body_min_x", "wheel_front_y", "body_front_y")
    if not all(T.get(k) is not None for k in keys):
        return NA if T.get("wheel_max_x") is None else None, "No wheels / body extents.", None, None
    out = {"left": T["wheel_max_x"] - T["body_max_x"], "right": T["body_min_x"] - T["wheel_min_x"],
           "front": T["wheel_front_y"] - T["body_front_y"]}
    if T.get("wheel_rear_y") is not None and T.get("body_rear_y") is not None:
        out["rear"] = T["body_rear_y"] - T["wheel_rear_y"]
    side, v = max(out.items(), key=lambda kv: kv[1])
    return v <= 0.0, f"Wheels reach {v:.1f} mm past the body on the {side}." if v > 0 else "The body meets a wall before any wheel.", "<= 0 mm", f"{v:.1f} mm"


def ar02(T):
    """Info: top speed and push (pit drift)."""
    rpm, D = T.get("motor_rpm"), T.get("wheel_dia")
    if not _need(rpm, D):
        return None, "Motor rpm or wheel size unknown.", None, None
    v = rpm * math.pi * D / 60000
    return True, f"Top speed about {v:.1f} m/s: a fast robot drifts into pits; check combat.R122.", None, f"{v:.1f} m/s"


def ar03(T):
    t = T.get("ar03.trapped")
    if t is None:
        return None, "Rest poses not measured.", None, None
    return not t, ("No trapped rest pose." if not t else f"Stable rest pose(s) with no wheel on the floor and no self-right: {', '.join(t)}."), "none", ", ".join(t) or "none"


# ---------------------------------------------------------------------------------------------------- F. landing

def ld01(T):
    """Corner landing capacity: wall thickness at each outline corner x 30 x 30 mm patch, energy capacity per
    `attack.energy_capacity_j`; >= 1.5 J."""
    v = T.get("ld01.min")
    if v is None:
        return None, "Corners not measured.", None, None
    return v[0] >= 1.5, f"Weakest corner `{v[1]}` ({v[2]:.1f} mm wall) absorbs {v[0]:.2f} J.", ">= 1.5 J", f"{v[0]:.2f} J"


def ld02(T):
    """Wheel shaft bending at a 20 g landing, load split over the wheels, cantilever to the first support (no shaft body
    -> a 3 mm steel N20-class motor shaft)."""
    v = T.get("ld02.worst")
    if v is None:
        return (NA if not T.get("wheel_y") else None), "Wheel overhang not measured.", None, None
    return v[0] >= 1.5, f"`{v[1]}` shaft (d {v[3]:.1f} mm, overhang {v[2]:.1f} mm) SF {v[0]:.2f} at a 20 g landing.", ">= 1.5", f"{v[0]:.2f}"


def ld03(T):
    """Heavy parts (electronics, motors, anything >= 10 g) are held in all 6 directions: a fastener/strap/glue connection,
    or another solid within 1.5 mm on every side."""
    v = T.get("ld03.loose")
    if v is None:
        return None, "Retention not measured.", None, None
    if not v:
        return True, "Every heavy part is held in all 6 directions.", None, None
    s = "; ".join(f"`{i}` free toward {'/'.join(d)}" for i, d in v[:5])
    return False, s + ".", "held in 6 directions", s


# ---------------------------------------------------------------------------------------------------- G. debris

def db01(T):
    v = T.get("db01.bad")
    if v is None:
        return (NA if not T.get("wheel_y") else None), "Wheel gaps not measured.", None, None
    if not v:
        return True, "No wheel-to-structure gap in the 1.5-15 mm debris band.", None, None
    s = "; ".join(f"`{w}` {g} mm (sector {a} deg)" for g, w, a in v[:5])
    return False, f"Debris-trapping gaps: {s}.", "< 1.5 or >= 15 mm", s


def db02(T):
    v = T.get("db02.bad")
    if v is None:
        return NA, "", None, None
    if not v:
        return True, "No weapon-to-frame gap in the 1.5-10 mm band below the weapon axis.", None, None
    s = "; ".join(f"`{w}` {g} mm (sector {a} deg)" for g, w, a in v[:5])
    return False, f"Weapon jam gaps: {s}.", "< 1.5 or >= 10 mm", s


def db03(T):
    v = T.get("db03.visible")
    if v is None:
        return None, "", None, None
    return not v, ("Belts and pulleys are enclosed." if not v else f"Visible from outside: {', '.join(v)}."), "enclosed", ", ".join(v) or "none"


def db04(T):
    v = T.get("db04.open")
    if v is None:
        return None, "", None, None
    return not v, ("Nothing electronic is open from above." if not v else f"Open to debris from above: {', '.join(v)}."), "none", ", ".join(v) or "none"


def db05(T):
    v = T.get("db05.visible")
    if v is None:
        return None, "", None, None
    return not v, ("Motors and gearboxes are shrouded." if not v else f"Visible from outside: {', '.join(v)}."), "shrouded", ", ".join(v) or "none"


def db06(T):
    v = T.get("db06.grooved")
    if v is None:
        return NA, "", None, None
    return not v, ("Smooth tyres." if not v else f"Tread grooves > 1 mm on {', '.join(v)} trap debris."), "smooth", ", ".join(v) or "none"


# ---------------------------------------------------------------------------------------------------- H. structure

def st01(T):
    """Printed parts on the front/side skin: knockdown 0.4 when most hit faces are perpendicular to the build direction
    (`print_dir`/`build_dir` on the part, default +Z). SF = yield * k * (20 mm x t^2 / 6) / (25% of the 100 g design
    impact x 10 mm lever)."""
    v = T.get("st01.min")
    if v is None:
        return NA, "", None, None
    return v[0] >= 1.5, f"`{v[1]}` front/side wall SF {v[0]:.2f} (layer knockdown {v[2]:g}).", ">= 1.5", f"{v[0]:.2f}"


def st02(T):
    v = T.get("st02.thin")
    if v is None:
        return None, "", None, None
    if not v:
        return True, "Exposed walls meet 2.5 mm (printed) / 0.8 mm (metal).", None, None
    s = "; ".join(f"`{i}` {t} mm (needs {lim})" for t, i, lim in v[:5])
    return False, f"Thin exposed walls (10th percentile): {s}.", ">= 2.5 printed / 0.8 metal", s


def st03(T):
    v = T.get("st03.sharp")
    if v is None:
        return None, "", None, None
    if not v:
        return True, "No sharp concave corners on the shells.", None, None
    s = "; ".join(f"`{i}` {L} mm" for L, i in v[:4])
    return False, f"Sharp concave edges (dihedral < 120 deg, unfilleted): {s}.", "fillets >= 1 mm", s


def st04(T):
    v = T.get("st04.min")
    if v is None:
        return NA, "", None, None
    return v[0] >= 1.5, f"Fastener `{v[1]}` pull-out SF {v[0]:.2f} at dynamic factor 3.", ">= 1.5", f"{v[0]:.2f}"


def st05(T):
    v = T.get("st05.brittle")
    if v is None:
        return None, "", None, None
    return not v, ("No brittle material on the front/side skin." if not v else f"Brittle material on the impact faces: {', '.join(v)}."), "no PLA", ", ".join(v) or "none"


def st06(T):
    """Main structure as a simply supported beam under the 100 g design impact: min over 2 mm slices of
    yield * Z / M(x)."""
    v = T.get("st06.min")
    if v is None:
        return NA, "", None, None
    return v[0] >= 1.0, f"`{v[1]}` weakest {v[2]} section at {v[3]} mm: SF {v[0]:.2f}.", ">= 1", f"{v[0]:.2f}"


# ---------------------------------------------------------------------------------------------------- I. guts

def gd01(T):
    """Chunk removal: 12 mm spheres 4 mm inside front/side hit points kill the parts and routed wires they touch; the
    robot still drives if the battery reaches a drive motor and the receiver through surviving wires."""
    v = T.get("gd01.alive_frac")
    if v is None:
        return NA, "", None, None
    return v >= 0.8, f"Drive survives {v * 100:.0f}% of {T.get('gd01.n_hits')} front/side hits.", ">= 80%", f"{v * 100:.0f}%"


def gd02(T):
    if not T.get("n_routes"):
        return (SKIP if T.get("n_wires") else NA), "No routed wires in this run.", None, None
    v = T.get("gd02.min_mm")
    if v is None:
        return None, "", None, None
    if v == 99.0:
        return True, "No main power lead routed.", None, None
    return v[0] > 8.0, f"Main lead `{v[1]}` passes {v[0]:.1f} mm from the outer skin.", "> 8 mm", f"{v[0]:.1f} mm"


def gd03(T):
    v = T.get("gd03.depth")
    if v is None:
        return NA, "", None, None
    return v[0] > 10.0, f"`{v[1]}` sits {v[0]:.1f} mm inside the outer skin.", "> 10 mm", f"{v[0]:.1f} mm"


def gd04(T):
    v, cg_ = T.get("gd04.depth"), T.get("gd04.caged") or []
    if v is None:
        return NA, "", None, None
    ok = v[0] > 8.0 and not cg_
    msg = f"Receiver `{v[1]}` is {v[0]:.1f} mm inside the skin" + (f"; enclosed in metal only: {', '.join(cg_)}" if cg_ else "") + "."
    return ok, msg, "> 8 mm, not in a metal box", f"{v[0]:.1f} mm"


def gd05(T):
    v = T.get("gd05.per_side")
    if v is None:
        return NA, "", None, None
    return min(v) >= 2, f"Drive motors per side: {v[0]} left, {v[1]} right.", ">= 2 per side", f"{v[0]}/{v[1]}"


def gd06(T):
    v = T.get("gd06")
    if v is None:
        return NA, "", None, None
    sid, rec, front = v
    rec_ok = rec is None or rec >= 1.0
    msg = f"Switch `{sid}` " + ("is enclosed" if rec is None else f"is recessed {rec:.1f} mm") + (" and sits in the front 30% of the length." if front else ".")
    return rec_ok and not front, msg, "recessed >= 1 mm, not in the front 30%", msg


def gd07(T):
    if not T.get("n_routes"):
        return (SKIP if T.get("n_wires") else NA), "No routed wires in this run.", None, None
    v = T.get("gd07.short") or []
    return not v, ("Every wire has >= 5 mm slack." if not v else f"Less than 5 mm slack: {', '.join(v[:6])}."), ">= 5 mm", ", ".join(v) or "ok"


def gd08(T):
    """BLOCKER: every routed wire stays > 3 mm (surface to surface) from the weapon's swept cylinder."""
    if not T.get("n_weapons"):
        return NA, "", None, None
    if not T.get("n_routes"):
        return (SKIP if T.get("n_wires") else NA), "No routed wires in this run (run with --full).", None, None
    v = T.get("gd08.min")
    if v is None:
        return None, "Weapon sweep not measured.", None, None
    return v[0] > 3.0, f"Wire `{v[1]}` comes within {v[0]:.1f} mm of `{v[2]}`'s swept volume.", "> 3 mm", f"{v[0]:.1f} mm"


def gd09(T):
    v = T.get("gd09.hard")
    if v is None:
        return NA, "", None, None
    return not v, ("ESCs are isolated." if not v else f"ESC on hard frame without foam: {', '.join(v)}."), "foam mounted", ", ".join(v) or "ok"


# ---------------------------------------------------------------------------------------------------- J. arena surface

def as01(T):
    lips = T.get("front_lips")
    if lips is None:
        return None, "", None, None
    if not lips:
        return NA, "", None, None
    bad = [x for x in lips if x["alpha_deg"] > 30.0 or x["tip_r"] < 0.1]
    if bad:
        s = "; ".join(f"`{x['id']}` underside {x['alpha_deg']:.0f} deg, tip r {x['tip_r']:.2f} mm" for x in bad[:4])
        return False, s + ".", "alpha <= 30 deg, r >= 0.1 mm", s
    return True, "; ".join(f"`{x['id']}` {x['alpha_deg']:.0f} deg r {x['tip_r']:.2f}" for x in lips[:4]), None, None


def as02(T):
    lips = T.get("front_lips")
    if lips is None:
        return None, "", None, None
    if not lips:
        return NA, "", None, None
    bad = [x for x in lips if not x["hinged"] and x["chamfer_mm"] < 0.5 and (x.get("tip_low") or x["gap_floor"]) <= 0.5]
    if bad:
        s = "; ".join(f"`{x['id']}` under-chamfer {x['chamfer_mm']:.1f} mm" for x in bad[:4])
        return False, s + ": a rigid lip at the floor with no under-chamfer catches seams.", ">= 1 mm or hinged", s
    return True, "Front lips ride over 0.5 mm seams.", None, None


def as03(T):
    """Tip pressure p = weight on the lip (1 - driven share) / (width x 2 r) < 5 MPa; forks also need tine stiffness
    3EI/L^3 within 0.5-5 N/mm (full-width rigid lips judged on pressure only)."""
    lips, sh, m = T.get("front_lips"), T.get("driven_share"), _mass(T)
    if lips is None or sh is None or m is None:
        return None, "Lips, weight share or mass not measured.", None, None
    if not lips:
        return NA, "", None, None
    W = max(1.0 - sh, 0.0) * m * 1e-3 * 9.81
    bad = []
    fork_ids = {x["id"] for x in T.get("forks") or []}
    for x in lips:
        p = W / max(x["width"] * 2 * max(x["tip_r"], 0.05), 1e-6)
        if p >= 5.0:
            bad.append(f"`{x['id']}` tip pressure {p:.1f} MPa")
        if x["id"] in fork_ids and x.get("E") and x.get("t_mid") and x.get("overhang"):
            k = 3 * x["E"] * (x["tip_w"] * x["t_mid"] ** 3 / 12) / x["overhang"] ** 3
            if not 0.5 <= k <= 5.0:
                bad.append(f"`{x['id']}` tine stiffness {k:.2f} N/mm")
    if bad:
        return False, "; ".join(bad) + ".", "p < 5 MPa, k 0.5-5 N/mm", "; ".join(bad)
    return True, f"Lip tips carry {W:.2f} N without digging in.", None, None


def as04(T):
    forks = T.get("forks")
    if forks is None:
        return None, "", None, None
    if not forks:
        return NA, "", None, None
    joined = len(forks) >= 2 and T.get("fork_open_mm") == 0.0
    bad = [x for x in forks if not (x["tip_w"] > 8.0 or joined or x["tip_r"] >= x["tip_w"] / 2)]
    if bad:
        s = "; ".join(f"`{x['id']}` tip {x['tip_w']:.1f} mm wide" for x in bad[:4])
        return False, s + ": narrow free tines wedge into floor/wall gaps.", "> 8 mm, joined or blunt", s
    return True, "Tines are wide, joined or blunt.", None, None


def as05(T):
    side = T.get("side_lips")
    if side is None:
        return None, "", None, None
    if not side:
        return NA, "", None, None
    bad = [x["id"] for x in side if not x["side_chamfer"]]
    return not bad, ("Side skirt bottom edges are chamfered." if not bad else f"No bottom-edge chamfer on side skirts: {', '.join(bad)}."), "chamfered >= 30 deg", ", ".join(bad) or "ok"


def as06(T):
    lips, wy = T.get("front_lips"), T.get("wheel_y")
    if not lips or not wy:
        return NA, "", None, None
    ov = max(x["ymax"] for x in lips) - max(wy)
    wb = T.get("wheelbase_wheels") or 0.0
    if wb < 5.0 and T.get("body_rear_y") is not None:
        wb = max(wy) - T["body_rear_y"]
    if wb <= 0:
        return None, "Wheelbase not measured.", None, None
    return ov <= 0.5 * wb, f"Lip overhangs the front axle by {ov:.0f} mm on a {wb:.0f} mm wheelbase.", f"<= {0.5 * wb:.0f} mm", f"{ov:.0f} mm"


def as07(T):
    forks = T.get("forks")
    if not forks or len(forks) < 2:
        return NA, "", None, None
    c = [(x["x0"] + x["x1"]) / 2 for x in forks]
    span = max(c) - min(c)
    joined = T.get("fork_open_mm") == 0.0
    return joined or span <= 30.0, f"{len(forks)} independent tines {span:.0f} mm apart: one snag pivots the robot.", "linked or <= 30 mm", f"{span:.0f} mm"


def as08(T):
    lips = T.get("front_lips")
    if not lips:
        return NA, "", None, None
    bad = [x["id"] for x in lips if not (x["metal"] or x["replaceable"])]
    return not bad, ("Lips are metal or replaceable." if not bad else f"Printed lips wear 0.2-0.5 mm per fight: {', '.join(bad)}."), "metal or replaceable", ", ".join(bad) or "ok"


# ---------------------------------------------------------------------------------------------------- K. own weapon

def ow01(T):
    """BLOCKER: pitched nose-down about the front wheel contact by 5 deg (or less if a front part touches the floor
    first), the weapon's swept rim stays above the floor."""
    if not T.get("n_weapons"):
        return NA, "", None, None
    v = T.get("ow01.min")
    if v is None:
        return None, "Weapon pitch clearance not measured.", None, None
    return v[0] > 0.0, f"At {v[2]:.1f} deg nose-down `{v[1]}` clears the floor by {v[0]:.1f} mm.", "> 0 mm", f"{v[0]:.1f} mm"


def ow02(T):
    """Info: vertical-spinner gyro bounce; track narrower than the weapon diameter tips onto its back on turns
    (combat.R057 quantifies it)."""
    v = T.get("ow02.ratio")
    if v is None:
        return NA, "", None, None
    return v >= 1.0, f"Track is {v:.2f}x the weapon diameter.", ">= 1.0", f"{v:.2f}"


def ow03(T):
    """Pulleys carrying a belt are flanged (or grooved): the rim at both axial ends is >= 0.4 mm proud of the middle.
    Wrap angle is not measured."""
    v = T.get("ow03.unflanged")
    if v is None:
        return NA, "", None, None
    return not v, ("Belt pulleys are flanged/grooved." if not v else f"Unflanged pulleys: {', '.join(v)}."), "flanged", ", ".join(v) or "ok"


def ow04(T):
    v = T.get("ow04.supports")
    if not v:
        return NA, "", None, None
    bad = [i for i, n in v if n < 2]
    return not bad, ("Weapon shaft supported both sides." if not bad else f"Single-sided weapon support: {', '.join(bad)}."), "2 supports", ", ".join(bad) or "ok"


def ow05(T):
    v = T.get("ow05.battery_held")
    if v is None:
        return NA, "", None, None
    return bool(v), ("Battery held upward (stays put inverted)." if v else "Battery is free to drop onto the lid when inverted."), "held", str(v)


RULES = {
    "CF-VS01": vs01, "CF-VS02": vs02, "CF-VS03": vs03, "CF-VS04": vs04, "CF-VS05": vs05, "CF-VS06": vs06,
    "CF-HS01": hs01, "CF-HS02": hs02, "CF-HS03": hs03, "CF-HS04": hs04, "CF-HS05": hs05,
    "CF-HA01": ha01, "CF-HA02": ha02, "CF-HA03": ha03,
    "CF-WL01": wl01, "CF-WL02": wl02, "CF-WL03": wl03, "CF-WL04": wl04, "CF-WL05": wl05, "CF-WL06": wl06, "CF-WL07": wl07,
    "CF-AR01": ar01, "CF-AR02": ar02, "CF-AR03": ar03,
    "CF-LD01": ld01, "CF-LD02": ld02, "CF-LD03": ld03,
    "CF-DB01": db01, "CF-DB02": db02, "CF-DB03": db03, "CF-DB04": db04, "CF-DB05": db05, "CF-DB06": db06,
    "CF-ST01": st01, "CF-ST02": st02, "CF-ST03": st03, "CF-ST04": st04, "CF-ST05": st05, "CF-ST06": st06,
    "CF-GD01": gd01, "CF-GD02": gd02, "CF-GD03": gd03, "CF-GD04": gd04, "CF-GD05": gd05, "CF-GD06": gd06, "CF-GD07": gd07,
    "CF-GD08": gd08, "CF-GD09": gd09,
    "CF-AS01": as01, "CF-AS02": as02, "CF-AS03": as03, "CF-AS04": as04, "CF-AS05": as05, "CF-AS06": as06, "CF-AS07": as07,
    "CF-AS08": as08,
    "CF-OW01": ow01, "CF-OW02": ow02, "CF-OW03": ow03, "CF-OW04": ow04, "CF-OW05": ow05,
}

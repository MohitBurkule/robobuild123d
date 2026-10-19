"""Top clusters of the extended catalogue (research/combat_failure_modes_ext.json, 622 part x threat x state modes).
Rankings there are uncalibrated, so every check here is a WARNING. Finding ids `threat.CFX-*`."""

from __future__ import annotations

from .rules import NA, SKIP

STATE_TEXT = {
    "inverted": "upside down (no invertible drive / ground game, no self-right)",
    "one_drive_dead": "one drive side dead (fewer than 2 motors per side)",
    "weapon_dead": "weapon dead (no wedge/skirt ground game left on the front)",
    "radio_failsafe": "radio lost (spinner without declared failsafe)",
    "on_side_or_walled": "on its side / against a wall (trapped rest pose)",
}


def sw(T):
    """Switch flicked off or ripped out: hit first by a spinner (side band, z <= 40 mm), or within 2 mm of the top, which is
    the floor/wedge contact face when inverted."""
    rows = T.get("x.switch")
    if rows is None:
        return None, "Switch not measured.", None, None
    if not rows:
        return NA, "", None, None
    bad = []
    for r in rows:
        if r["side_hit"]:
            bad.append(f"`{r['id']}` is the first thing a spinner/wedge meets from the side")
        if r["top_gap"] <= 2.0 and r["top_visible"]:
            bad.append(f"`{r['id']}` is {r['top_gap']:.1f} mm below the top: it drags on the floor when inverted")
    if bad:
        return False, "; ".join(bad) + ".", "recessed, not first-hit, > 2 mm below the top", "; ".join(bad)
    return True, "Switch is shielded from the side and from the floor when inverted.", None, None


def antenna(T):
    """Antenna shear: a modelled antenna (part id containing `antenna`/`aerial`) visible on the outer skin."""
    a = T.get("x.antenna")
    if a is None:
        return (SKIP if T.get("x.has_rx") else NA), "No antenna modelled: route it internally or model it as a part.", None, None
    return not a, ("Antenna is inside the hull." if not a else f"Exposed antenna: {', '.join(a)}."), "inside hull", ", ".join(a) or "ok"


def friction(T):
    v = T.get("x.friction")
    if v is None:
        return None, "", None, None
    return not v, ("No friction-only pins or tyres." if not v else f"Held only by friction/press fit: {', '.join(v)}."), "keyed, glued or fastened", ", ".join(v) or "ok"


def tape(T):
    v = T.get("x.tape")
    if v is None:
        return None, "", None, None
    return not v, ("No electronics held by tape alone." if not v else f"Held only by tape/velcro: {', '.join(v)}."), "pocket, strap or screw", ", ".join(v) or "ok"


def states(T):
    """Parametrised state x threat check: for each robot state of the extended catalogue, does the robot still have an
    answer to the threats that exploit it?"""
    st = T.get("x.states")
    if st is None:
        return None, "", None, None
    bad = [STATE_TEXT[k] for k, ok in st.items() if not ok]
    return not bad, ("Robot keeps an answer in every degraded state." if not bad else "No answer when: " + "; ".join(bad) + "."), "an answer in every state", "; ".join(bad) or "ok"


EXT = {
    "CFX-SWITCH": ("Switch flicked off or ripped by spinner, wedge or floor when inverted", sw,
                   "A switch the opponent or the floor touches turns the robot off or is torn out (ext cluster: switch x spinner/wedge/inverted).",
                   "Recess the switch below the skin, away from the front and the top face; guard it with a lip."),
    "CFX-ANTENNA": ("Antenna shear", antenna, "A protruding antenna is sheared by walls, wedges and spinners -> failsafe.",
                    "Route the antenna inside a non-metal part of the hull or under a guard."),
    "CFX-FRICTION": ("Friction-fit pins / tyres unseat under shock", friction,
                     "Shock loads of 50-200 g walk friction fits out; tyres roll off rims.",
                     "Add a key, grub screw, glue, retaining lip or fastener."),
    "CFX-TAPE": ("Taped electronics loosen", tape, "Tape and velcro creep and peel under repeated impacts; parts then rattle and rip wires.",
                 "Pocket the part in the frame, strap it, or screw it down; tape only as a secondary hold."),
    "CFX-STATE": ("Degraded-state answers (state x threat)", states,
                  "Fights are lost in degraded states (inverted, one side dead, weapon dead, failsafe, walled), not in the nominal one.",
                  "Add invertibility/self-right, 4WD, a ground-game lip, failsafe and rounded sides as reported."),
}

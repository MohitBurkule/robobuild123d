"""Thermal and voltage-sag budget (`thermal.*`, F4).

WHY: a pack that sags below the receiver/ESC brownout point mid-fight looks like
a radio glitch or a dead robot. The pack's internal resistance is in the catalogue
and unused; the peak current comes from the power group's metric when it ran
(else from the motors' rated max current - a lower bound, noted as such).
V_loaded = nominal_v - I_peak * R_pack. Brownout when V_loaded < 3.3 V/cell.
"""

from __future__ import annotations

from ..finding import BLOCKER, WARNING, fail, ok

G = "thermal"
CELL_MIN_V = 3.3  # LiPo under load
CELL_SAG_WARN_V = 3.5
CELL_NOMINAL_V = 3.7


def _battery(r):
    for rp in r.parts:
        cat = rp.cat
        if cat is not None and cat.kind == "battery":
            return rp, cat
    return None, None


def peak_current(ctx, r):
    """Best available peak current estimate (A), or None: the power group's metric, else the sum of motor max currents."""
    v = ctx.metrics.get("peak_current_a")
    if v is not None:
        return float(v), "power group metric"
    total, known = 0.0, False
    for rp in r.parts:
        mc = (rp.cat.props.get("max_current_a") if rp.cat is not None else None) \
            or (rp.part._extra.get("max_current_a") if isinstance(getattr(rp.part, "_extra", None), dict) else None)
        if mc is not None and rp.part.kind in ("weapon", "weapon_motor", "drive_motor", "motor"):
            total += float(mc)
            known = True
    return (total, "sum of motor max currents (lower bound)") if known else (None, "")


def run(ctx):
    r = ctx.r
    out = []
    rp, cat = _battery(r)
    if cat is None:
        ctx.not_checked.append("Thermal/brownout: no catalogue battery in the spec")
        return out
    props = cat.props or {}
    cells = props.get("cells")
    ir_mohm = props.get("internal_resistance_mohm")
    i_peak, src = peak_current(ctx, r)
    missing = [name for name, v in (("cells", cells), ("internal_resistance_mohm", ir_mohm), ("peak current", i_peak)) if v is None]
    if missing:
        ctx.not_checked.append(f"Thermal/brownout: battery props missing {', '.join(missing)}")
        return out
    v_nom = CELL_NOMINAL_V * cells
    r_ohm = ir_mohm / 1000.0
    v_loaded = v_nom - i_peak * r_ohm
    v_cell = v_loaded / cells
    ctx.metrics["pack_v_loaded"] = round(v_loaded, 2)
    ctx.metrics["pack_sag_v"] = round(v_nom - v_loaded, 2)
    if v_cell < CELL_MIN_V:
        out.append(fail("thermal.brownout", G, BLOCKER, "Pack browns out at peak current",
                        f"{v_nom:.1f} V pack sags to {v_loaded:.1f} V at {i_peak:.1f} A "
                        f"({r_ohm * 1000:.0f} mOhm), below {CELL_MIN_V:.1f} V/cell - the receiver resets mid-fight.")
                   .on(cat.id).fix("Use a pack with more capacity / higher C rating (lower internal resistance), "
                                   "or cut the peak current (smaller weapon motor, softer gearing)."))
    elif v_cell < CELL_SAG_WARN_V:
        out.append(fail("thermal.sag", G, WARNING, "Pack sag close to brownout",
                        f"Loaded cell voltage {v_cell:.2f} V is under {CELL_SAG_WARN_V:.1f} V at peak current "
                        f"({i_peak:.1f} A from {src}).")
                   .on(cat.id).fix("A higher-C or larger pack adds margin; a fresh charge matters most in the last fight."))
    else:
        out.append(ok("thermal.ok", G, "Pack voltage holds at peak current",
                      f"{v_loaded:.1f} V loaded ({v_cell:.2f} V/cell) at {i_peak:.1f} A ({src})."))
    esc = next((rp2 for rp2 in r.parts if rp2.cat is not None and rp2.cat.kind == "esc"), None)
    if esc is not None:
        esc_max = (esc.cat.props or {}).get("max_current_a")
        if esc_max is not None and i_peak > float(esc_max):
            out.append(fail("thermal.esc_overcurrent", G, WARNING, "Peak current above the ESC rating",
                            f"{i_peak:.1f} A demanded, {esc.cat.id} is rated {float(esc_max):.1f} A.")
                       .on(esc.cat.id).fix("Pick an ESC with more headroom or limit the weapon motor current."))
    return out

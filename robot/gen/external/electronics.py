"""Electronics: catalog boxes, port maps and the wiring harness for each ESC/receiver choice."""

from __future__ import annotations

from ... import catalog

# Explicit port maps where the catalog only has generic in/out ports (local frame, mm).
PORTS = {
    "c_malenki_nano_antweight_esc_receiver": {"bat": [-16.0, -4.0, 0.0], "m1": [16.0, 4.0, 0.0], "m2": [-16.0, 4.0, 0.0],
                                              "wpn": [16.0, -4.0, 0.0]},
    "c_bbb_antweight_dual_esc_v3_1": {"bat": [-10.0, -4.0, 0.0], "m1": [10.0, 4.0, 0.0], "m2": [-10.0, 4.0, 0.0],
                                      "rx": [10.0, -4.0, 0.0]},
    "c_bbb_antweight_spinner_brushless_esc": {"bat": [11.5, -3.0, 0.0], "motor": [11.5, 3.0, 0.0], "rx": [-11.5, 0.0, 0.0]},
}


def size_of(cid: str) -> tuple:
    e = catalog.find(cid)
    s = e.shape
    if s.get("type") == "box":
        return tuple(float(v) for v in s["size"])
    raise ValueError(f"{cid}: not a box-shaped catalog part")


def mass_of(cid: str) -> float:
    return float(catalog.find(cid).mass_g)


def ports_of(cid: str) -> dict:
    return {k: list(v) for k, v in (PORTS.get(cid) or catalog.find(cid).ports).items()}


# keep-away margins from the exposed skin, strictest first: (battery front, battery side/rear, rx/esc front, rx/esc
# side/rear). CF-GD03 battery 10 mm from any exposed face, CF-GD04 receiver/ESC 8 mm from the skin. The build tries
# them in order and records the tier it needed (a relaxed tier is an accepted risk in the spec).
MARGIN_TIERS = ((10.0, 10.0, 8.0, 8.0), (10.0, 8.0, 0.0, 0.0), (10.0, 5.0, 0.0, 0.0))
MARGIN_WHY = ("CF-GD03 battery 10 mm from every exposed face; CF-GD04 receiver/ESC 8 mm from the skin",
              "relaxed: the outline is too small for 8 mm round the ESC/receiver and 10 mm round the battery's sides; "
              "battery keeps 10 mm front / 8 mm sides+rear, ESC and receiver sit against the inner wall (CF-GD04 accepted)",
              "relaxed: battery 10 mm front / 5 mm sides+rear, ESC and receiver against the inner wall (CF-GD03/GD04 "
              "accepted on the sides: the wheels and wells stand outside them)")


def components(h, tier: int = 0) -> list[dict]:
    """The internal components the layout solver must place for hypothesis `h` (id, kind, catalog), with the
    keep-away margins of MARGIN_TIERS[tier]. The lifter's scoop cheeks cover its side walls: rx/ESC sides 4 mm."""
    bf, bs, ef, es = MARGIN_TIERS[tier]
    if h.weapon == "lifter" and es:
        es = 4.0
    out = [dict(id="battery", kind="battery", catalog=h.battery, min_front_mm=bf, min_side_mm=bs),
           dict(id="esc", kind="esc", catalog=h.drive_esc, min_front_mm=ef, min_side_mm=es)]
    if h.rx != "integrated":
        out.append(dict(id="rx", kind="receiver", catalog=h.rx, min_front_mm=ef, min_side_mm=es))
    if h.weapon_esc != "none":
        out.append(dict(id="wesc", kind="esc", catalog=h.weapon_esc, min_front_mm=ef, min_side_mm=es))
    return out


def harness(h, weapon_motor: str | None = None, servo: str | None = None) -> list[tuple]:
    """(wire id, from, to, kind, awg) for the whole robot."""
    integrated = h.rx == "integrated"
    w = [("w_bat_sw", "battery.xt30", "power_switch.in", "power", 22 if weapon_motor else 26),
         ("w_sw_esc", "power_switch.out", "esc.bat", "power", 26)]
    m_l, m_r = ("esc.m2", "esc.m1")
    w += [("w_esc_ml", m_l, "motor_l.terminals", "motor", 26), ("w_esc_mr", m_r, "motor_r.terminals", "motor", 26)]
    if not integrated:
        w.append(("w_rx_esc", "rx.esc", "esc.rx", "signal", 26))
    if weapon_motor:
        w.append(("w_sw_wesc", "power_switch.out", "wesc.bat", "power", 22))
        w.append(("w_wesc_m", "wesc.motor", f"{weapon_motor}.phases", "motor", 24))
        w.append(("w_rx_wesc", "esc.wpn" if integrated else "rx.servo", "wesc.rx", "signal", 30))
    if servo:
        w.append(("w_rx_servo", "esc.wpn" if integrated else "rx.servo", f"{servo}.signal", "signal", 28))
    return w

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


def components(h) -> list[dict]:
    """The internal components the layout solver must place for hypothesis `h` (id, kind, catalog)."""
    out = [dict(id="battery", kind="battery", catalog=h.battery, min_front_mm=10.0, min_side_mm=5.0),
           dict(id="esc", kind="esc", catalog=h.drive_esc)]
    if h.rx != "integrated":
        out.append(dict(id="rx", kind="receiver", catalog=h.rx))
    if h.weapon_esc != "none":
        out.append(dict(id="wesc", kind="esc", catalog=h.weapon_esc))
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

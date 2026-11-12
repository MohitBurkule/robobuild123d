"""Wheel geometry derived from ports (ROADMAP R2). UNTESTED: written without running.

Given a front/rear wheel id, return the hub/tyre numbers the builders use (seat radius, seat width, bore radius,
tyre envelope) from the WheelIface + the drive shaft port, instead of literals. "stock" returns None so the
stock build keeps its params_drive.py literals byte-identical. Not yet wired into params_drive.py: wire by
`d = derive(setting); if d: FH_SEAT_R = d.seat_r ...` once a run confirms.
"""
from __future__ import annotations

from dataclasses import dataclass

from robot import ports

MIN_WALL = ports.DEFAULTS["min_wall"]


class WheelUnfit(ValueError):
    pass


@dataclass(frozen=True)
class WheelGeom:
    cid: str
    od: float
    width: float
    seat_r: float        # hub radius the tyre sits on
    seat_w: float
    bore_r: float
    flange_r: float
    printed_hub: bool    # False = COTS wheel brings its own hub: skip printed RV19/RV21


def derive(cid: str, motor_cid: str | None = None, flange_over_seat=0.8) -> WheelGeom | None:
    if not cid or cid == "stock":
        return None
    try:
        w = ports.iface(cid)
    except ports.PortError as e:
        raise WheelUnfit(str(e)) from None
    if not isinstance(w, ports.WheelIface):
        raise WheelUnfit(f"{cid} is {w.kind}, not a wheel")
    if motor_cid:
        bad = ports.compatible(ports.iface(motor_cid), w)
        if bad:
            raise WheelUnfit("; ".join(f"{m.port}.{m.field}: have {m.have} need {m.need} ({m.why})" for m in bad))
    bore_r = (w.bore.d / 2) if w.bore else 0.0
    seat_r = w.rim_r if w.rim_r is not None else (w.boss_d / 2 if w.boss_d else bore_r + MIN_WALL)
    flange_r = seat_r + flange_over_seat
    if seat_r <= bore_r + MIN_WALL:
        raise WheelUnfit(f"{cid}: seat_r {seat_r} <= bore_r {bore_r} + wall {MIN_WALL}")
    if w.od / 2 <= flange_r:
        raise WheelUnfit(f"{cid}: od/2 {w.od / 2} <= flange_r {flange_r}")
    return WheelGeom(cid, w.od, w.width, seat_r, w.width, bore_r, flange_r, printed_hub=not w.own_hub)

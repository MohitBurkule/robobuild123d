"""Write spec.json from the masters in src/elevron_red/params.py (never hand-edit spec.json coordinates)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src" / "elevron_red"))
import params as P  # noqa: E402

MODEL = "src/elevron_red/parts.py"
RED, BLACK, GREY, WHITE = "#e8453a", "#202226", "#9a9b9d", "#f2f2f2"


def r(v):
    return [round(float(x), 3) for x in v]


def made(pid, kind, part, color, material="nylon", orient="+z", **kw):
    d = {"id": pid, "kind": kind, "material": material, "process": "fdm", "model": MODEL, "params": {"part": part},
         "at": [0, 0, 0], "rot": [0, 0, 0], "color": color, "print_orientation": orient}
    d.update(kw)
    return d


def main():
    old = json.loads((HERE / "spec.json").read_text())
    parts = [
        made("chassis", "structure", "chassis", BLACK),
        made("housing", "structure", "housing", RED, fused_with="chassis"),
        made("arm", "weapon", "arm", BLACK, orient="+x", weapon={"kind": "lifter"}, actuated_by="servo",
             joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": r((P.world_x(P.pivot()[0]),) + P.pivot()[1:]), "min": 0, "max": P.ARM_LIFT_DEG, "default": 0}),
        made("arm_rail", "other", "arm_rail", RED, orient="+x", parent="arm", fused_with="arm"),
        made("horn", "other", "horn", WHITE, orient="+x"),
        made("side_l", "wedge", "side_l", RED, material="tpu", orient="-z"),
        made("side_r", "wedge", "side_r", RED, material="tpu", orient="-z"),
    ]
    conns = []
    wires = []
    for sx, tag in ((1, "l"), (-1, "r")):
        for sy, i in ((-1, 0), (1, 1)):
            w, h, m = f"wheel_{tag}{i}", f"hub_{tag}{i}", f"motor_{tag}{i}"
            parts.append({"id": w, "kind": "wheel", "material": "tpu", "process": "fdm", "model": MODEL,
                          "params": {"part": "tyre", "sx": sx, "sy": sy}, "at": [0, 0, 0], "rot": [0, 0, 0],
                          "color": BLACK, "tyre_of": h, "print_orientation": "+x" if sx > 0 else "-x"})
            parts.append({"id": h, "kind": "other", "material": "nylon", "process": "fdm", "model": MODEL,
                          "params": {"part": "hub", "sx": sx, "sy": sy}, "at": [0, 0, 0], "rot": [0, 0, 0],
                          "color": GREY, "print_orientation": "+x" if sx > 0 else "-x"})
            parts.append({"id": m, "kind": "motor", "catalog": P.MOTOR, "at": r((sx * P.motor_origin_x(), sy * P.AXLE_Y, 0)),
                          "rot": [0, 0, 0 if sx > 0 else 180], "retained": "press_fit",
                          "retained_reason": "gearbox pressed into a 0.25 mm-per-side cradle in the chassis; the cradle closes round it on five faces"})
            conns += [
                {"a": m, "b": "chassis", "method": "press_fit", "interference_mm": 0.1,
                 "reason": "N10 gearbox pressed into its printed cradle; the cradle walls and the shaft wall hold it"},
                {"a": h, "b": m, "method": "press_fit", "interference_mm": 0.1,
                 "reason": "hub D-bore pressed on the 3 mm D-shaft; the flat carries the torque"},
                {"a": w, "b": h, "method": "press_fit", "interference_mm": 0.1,
                 "reason": "Scalextric-style tyre stretched over the hub, 0.1 mm interference"},
            ]
            wires.append({"id": f"w_{m}", "from": f"el_rx_esc.{'m1' if sx > 0 else 'm2'}", "to": f"{m}.terminals",
                          "kind": "motor", "awg": 26, "slack_mm": 10})
    ft = P.floor_top()
    parts += [
        {"id": "servo", "kind": "servo", "catalog": P.SERVO, "at": r((P.world_x(P.servo_center()[0]),) + P.servo_center()[1:]),
         "rot": [90, 0, 90 if P.MODULE_SIDE > 0 else -90], "retained": "pocket",
         "retained_reason": "servo body and ears sit in a closed 0.25 mm-per-side pocket in the housing printed on the chassis"},
        {"id": "el_battery", "kind": "battery", "catalog": P.BATTERY, "at": r(P.bat_center()),
         "rot": [0, 0, -90], "retained": "pocket", "retained_reason": "closed printed cradle, 0.25 mm per side, lead window on the inboard face"},
        {"id": "el_rx_esc", "kind": "esc", "catalog": P.ESC, "at": r(P.esc_center()),
         "rot": [0, 0, 90], "retained": "velcro", "retained_reason": "velcro pad on the cavity floor"},
        {"id": "el_switch", "kind": "switch", "catalog": P.SWITCH, "at": r((0, P.SW_Y, ft + P.SW_H / 2)), "rot": [180, 0, 0],
         "tool_free": True, "marked": True, "label": "POWER ON/OFF", "off_dir": [-1, 0, 0], "retained": "pocket",
         "retained_reason": "closed 0.25 mm-per-side cradle on the floor; two lips under the body carry it over a belly slot the size of the body"},
    ]
    conns += [
        {"a": "servo", "b": "housing", "method": "interlock", "reason": "servo body and ear plate captured in a closed pocket in the housing"},
        {"a": "el_battery", "b": "chassis", "method": "interlock", "reason": "closed printed cradle round the pack, 0.25 mm per side"},
        {"a": "el_rx_esc", "b": "chassis", "method": "velcro", "reason": "velcro pad on the cavity floor"},
        {"a": "el_switch", "b": "chassis", "method": "interlock", "reason": "closed cradle with two lips under the body; slider worked through the belly slot"},
        {"a": "side_l", "b": "chassis", "method": "interlock", "reason": "side panel web keyed into a slot in the chassis wall between the wheels"},
        {"a": "side_r", "b": "chassis", "method": "interlock", "reason": "side panel web keyed into a slot in the chassis wall between the wheels"},
        {"a": "horn", "b": "servo", "method": "press_fit", "interference_mm": 0.1,
         "reason": "horn hub pressed on the servo output spline (horn screw on the axis); its link drives the arm"},
        {"a": "arm", "b": "housing", "method": "shaft", "reason": "arm boss turns on the 3 mm steel hinge pin through the housing lug; the servo horn drives it through its link"},
    ]
    wires = [
        {"id": "w_bat_sw", "from": "el_battery.xt30", "to": "el_switch.in", "kind": "power", "awg": 22, "slack_mm": 10},
        {"id": "w_sw_esc", "from": "el_switch.out", "to": "el_rx_esc.bat", "kind": "power", "awg": 22, "slack_mm": 10},
        {"id": "w_servo", "from": "el_rx_esc.wpn", "to": "servo.signal", "kind": "signal", "awg": 28, "slack_mm": 10},
    ] + wires
    spec = {k: old[k] for k in ("name", "profile", "robot_type", "locomotion") if k in old}
    spec.update({"parts": parts, "fasteners": [], "wires": wires, "connections": conns,
                 "reference": old["reference"], "electronics": old["electronics"]})
    (HERE / "spec.json").write_text(json.dumps(spec, indent=1) + "\n")


if __name__ == "__main__":
    main()

"""Write spec.json from the masters in src/elevron_red/params.py (never hand-edit spec.json coordinates)."""
import json
import subprocess
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
    d = {"id": pid, "kind": kind, "material": material, "process": "fdm",
         "shape": {"type": "model", "file": MODEL, "params": {"part": part}},
         "at": [0, 0, 0], "rot": [0, 0, 0], "color": color, "print_orientation": orient}
    d.update(kw)
    return d


def main():
    old = json.loads((HERE / "spec.json").read_text())
    parts = [
        made("chassis", "structure", "chassis", BLACK),
        made("lid", "structure", "lid", BLACK, orient="-z"),
        made("housing", "structure", "housing", RED, fused_with="lid"),
        made("cover", "structure", "cover", RED, orient="-z"),
        made("pivot_cap", "other", "pivot_cap", RED, orient="+x"),
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
            parts.append({"id": w, "kind": "wheel", "material": "tpu", "process": "fdm",
                          "shape": {"type": "model", "file": MODEL, "params": {"part": "tyre", "sx": sx, "sy": sy}}, "at": [0, 0, 0], "rot": [0, 0, 0],
                          "color": BLACK, "tyre_of": h, "print_orientation": "+x" if sx > 0 else "-x"})
            parts.append({"id": h, "kind": "other", "material": "nylon", "process": "fdm",
                          "shape": {"type": "model", "file": MODEL, "params": {"part": "hub", "sx": sx, "sy": sy}}, "at": [0, 0, 0], "rot": [0, 0, 0],
                          "color": GREY, "print_orientation": "+x" if sx > 0 else "-x"})
            parts.append({"id": m, "kind": "motor", "catalog": P.MOTOR, "at": r((sx * P.motor_origin_x(), sy * P.AXLE_Y, 0)),
                          "rot": [0, 0, 0 if sx > 0 else 180], "retained": "press_fit",
                          "retained_reason": "drops into an open-top 0.25 mm-per-side cradle in the tub; the screwed lid's post clamps it from above"})
            conns += [
                {"a": m, "b": "chassis", "method": "press_fit", "interference_mm": 0.1,
                 "reason": "N10 gearbox pressed into its open-top cradle; the screwed lid's post clamps it down"},
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
         "retained_reason": "servo body and ears drop into a 0.25 mm-per-side pocket in the housing; the screwed cover closes it"},
        {"id": "el_battery", "kind": "battery", "catalog": P.BATTERY, "at": r(P.bat_center()),
         "rot": [0, 0, -90], "retained": "pocket", "retained_reason": "printed cradle walls, 0.25 mm per side, lead window on the inboard face; two lid posts hold it down"},
        {"id": "el_rx_esc", "kind": "esc", "catalog": P.ESC, "at": r(P.esc_center()),
         "rot": [0, 0, 90], "retained": "pocket", "retained_reason": "printed side walls and corner stops, 0.25 mm per side, ends open for the leads; two lid posts hold it down"},
        {"id": "el_switch", "kind": "switch", "catalog": P.SWITCH, "at": r((0, P.SW_Y, ft + P.SW_H / 2)), "rot": [180, 0, 0],
         "tool_free": True, "marked": True, "label": "POWER ON/OFF", "off_dir": [-1, 0, 0], "retained": "pocket",
         "retained_reason": "0.25 mm-per-side cradle on the floor; two lips under the body carry it over a belly slot, two lid posts hold its ends down"},
        {"id": "pivot_nut", "kind": "nut", "catalog": P.NUT, "rot": [0, 90, 0],
         "at": r((P.world_x(P.housing_x1() - P.LUG_T + P.NUT_T / 2),) + P.pivot()[1:]), "retained": "pocket",
         "retained_reason": "hex pocket in the lug's outer face; the pivot screw draws it in"},
    ]
    px, py, pz = P.pivot()
    head = P.world_x(P.arm_x1() + P.CAP_T)
    fasteners = [{"id": "fs_pivot", "designation": P.PIVOT_SCREW, "at": r((head, py, pz)), "dir": [-1 if P.world_x(1) > 0 else 1, 0, 0],
                  "through": ["pivot_cap", "arm", "cover"], "threads_into": "pivot_nut", "head": "button", "tool": "hex2",
                  "removable": True,
                  "reason": "photo: red-capped M3 pivot screw through the arm boss and the housing lug; its threaded end and nut stand out past the lug"}]
    conns += [
        {"a": "lid", "b": "chassis", "method": "screw", "mechanical_key": True,
         "reason": "2 M2 screws down through the lid into the side-wall columns; the lid's posts sit inside the motor, battery, ESC and switch cradles, so it cannot slide"},
        {"a": "cover", "b": "housing", "method": "screw", "reason": "3 M2 screws down through the cover into housing columns"},
        {"a": "servo", "b": "housing", "method": "interlock", "reason": "servo body and ear plate in a pocket in the housing, closed by the screwed cover"},
        {"a": "el_battery", "b": "chassis", "method": "interlock", "reason": "printed cradle round the pack, 0.25 mm per side; lid posts on top"},
        {"a": "el_rx_esc", "b": "chassis", "method": "interlock", "reason": "printed side walls and corner stops, 0.25 mm per side; lid posts on top"},
        {"a": "el_switch", "b": "chassis", "method": "interlock", "reason": "cradle with two lips under the body; lid posts on its ends; slider worked through the belly slot"},
        {"a": "side_l", "b": "chassis", "method": "screw", "mechanical_key": True,
         "reason": "web tongue keyed into the chassis flank slot; 2 M2 screws down through the web plate into the flank blocks"},
        {"a": "side_r", "b": "chassis", "method": "screw", "mechanical_key": True,
         "reason": "web tongue keyed into the chassis flank slot; 2 M2 screws down through the web plate into the flank blocks"},
        {"a": "horn", "b": "servo", "method": "press_fit", "interference_mm": 0.1,
         "reason": "horn hub pressed on the servo output spline (horn screw on the axis); its link drives the arm"},
        {"a": "arm", "b": "cover", "method": "shaft", "reason": "arm boss turns on the M3 pivot screw through the cover lug; the servo horn drives it through its link"},
    ]
    wires = [
        {"id": "w_bat_sw", "from": "el_battery.xt30", "to": "el_switch.in", "kind": "power", "awg": 22, "slack_mm": 10},
        {"id": "w_sw_esc", "from": "el_switch.out", "to": "el_rx_esc.bat", "kind": "power", "awg": 22, "slack_mm": 10},
        {"id": "w_servo", "from": "el_rx_esc.wpn", "to": "servo.signal", "kind": "signal", "awg": 28, "slack_mm": 10},
    ] + wires
    spec = {k: old[k] for k in ("name", "profile", "robot_type", "locomotion") if k in old}
    teardown = [{"parts": ["lid", "housing"], "dir": [0, 0, 1],
                 "reason": "the red housing is printed on the black lid (two-colour print, `fused_with`): they lift off as one"}]
    spec.update({"parts": parts, "fasteners": fasteners, "teardown": teardown, "wires": wires, "connections": conns,
                 "reference": old["reference"], "electronics": old["electronics"]})
    (HERE / "spec.json").write_text(json.dumps(spec, indent=1) + "\n")
    # photo screw heads as real fasteners (robot screws), then the "01" marking (robot decal)
    wx = P.world_x
    cols = ";".join(f"{wx(x):g},{y:g}" for x, y in P.COVER_COLS)
    runs = [["screws", "lid", "--face", "+z", "--pattern", "at", "--at=" + ";".join(f"{x:g},{y:g}" for x, y in P.LID_SCREWS)],
            ["screws", "cover", "--face", "+z", "--pattern", "at", "--at=" + cols],
            ["screws", "side_l", "--face", "+z", "--pattern", "at", f"--at={P.SIDE_SCREW_X:g},{P.SB_Y:g};{P.SIDE_SCREW_X:g},{-P.SB_Y:g}"],
            ["screws", "side_r", "--face", "+z", "--pattern", "at", f"--at={-P.SIDE_SCREW_X:g},{P.SB_Y:g};{-P.SIDE_SCREW_X:g},{-P.SB_Y:g}"],
            ["decal", "cover", "--face", "+z", "--shape", "text", "--text", "01", "--size", "5", f"--at={wx(P.MARK_X):g},{P.MARK_Y:g}",
             "--angle", "90", "--color", BLACK, "--depth", "0.6", "--id", "mark_01"]]
    root = HERE.parents[1]
    for a in runs:
        subprocess.run([sys.executable, "-m", "robot", a[0], str(HERE / "spec.json")] + a[1:], cwd=root, check=True)


if __name__ == "__main__":
    main()

"""Build robots/rammstein/spec.json: generator (2WD wedge) + 2 front idler wheels + thin shovel plate."""
import json, copy, subprocess, sys
R = "/tmp/work9_rammstein" if len(sys.argv) < 2 else sys.argv[1]
subprocess.check_call([sys.executable, "-m", "robot", "gen", "build", "--intent", "robots/rammstein/intent.json",
                       "--out", "out/", "--no-gate"], cwd=R)
d = json.load(open(f"{R}/out/wedge.json"))
P = {p["id"]: p for p in d["parts"]}
ax = P["wheel_l"]["at"][1]
FY = float(json.load(open(f"{R}/robots/rammstein/intent.json")).get("idler_y", 24))
for s in ("l", "r"):
    w = copy.deepcopy(P["wheel_" + s]); w["id"] = "wheel_f" + s; w["at"][1] = FY
    w["label"] = "front idler wheel"; d["parts"].append(w)
K = float(json.load(open(f"{R}/robots/rammstein/intent.json")).get("wedge_k", 0.65))
def walk(n):
    if isinstance(n, dict):
        if n.get("type") == "prism" and len(n["points"]) == 4 and n["points"][2][0] > float(json.load(open(f"{R}/robots/rammstein/intent.json"))["y1"]) + 40:
            p = n["points"]; y0, z0 = p[0]
            n["points"] = [[round(y0 + (y - y0) * K, 3), round(z0 + (z - z0) * K, 3)] for y, z in p]
        for v in n.values(): walk(v)
    elif isinstance(n, list):
        for v in n: walk(v)
walk(P["wedge"]["shape"])
zt = float(json.load(open(f"{R}/robots/rammstein/intent.json")).get("zt", 6))
plate = {"id": "carbon_plate", "kind": "structure", "material": "petg_cf", "process": "fdm",
 "shape": {"type": "prism", "points": [[-27,-44],[-18,-44],[-13,-33],[13,-33],[18,-44],[27,-44],[27,38],[-27,38]], "height": 1.6},
 "at": [0, 0, zt], "label": "carbon top plate"}
d["parts"].append(plate)
json.dump(d, open(f"{R}/robots/rammstein/spec.json", "w"), indent=1)

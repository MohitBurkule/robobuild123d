"""Hand patches on top of `robot gen build` output (reproduce: python3 robots/pantherk/patch.py out/wedge.json robots/pantherk/spec.json).

1. Two free-running idler wheels on the front axle (photos show 4 wheels, 2 per side; the generator's 2WD has 2).
2. Reference entries for the two photos (generator output has none).
"""
import copy
import json
import sys

IDLER_Y = 26.0  # front axle, mm (eyeballed from aws67 iso; wheels at rear axle y=-16)

src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src))
parts = d["parts"]
wl = next(p for p in parts if p["id"] == "wheel_l")
wr = next(p for p in parts if p["id"] == "wheel_r")
idl = copy.deepcopy(wl); idl["id"] = "idler_l"; idl["at"] = [abs(wl["at"][0]), IDLER_Y, 0.0]; idl["label"] = "left idler"
idr = copy.deepcopy(wr); idr["id"] = "idler_r"; idr["at"] = [-abs(wr["at"][0]), IDLER_Y, 0.0]; idr["label"] = "right idler"
parts.insert(parts.index(wr) + 1, idr)
parts.insert(parts.index(wl) + 1, idl)
reason = ("Free-running idler wheel on a fixed pin through the chassis side walls: carries its share of the robot "
          "weight and runs free, no drive torque.")
d["connections"] += [
    {"a": "idler_l", "b": "chassis_bottom", "method": "shaft", "reason": reason},
    {"a": "idler_r", "b": "chassis_bottom", "method": "shaft", "reason": reason},
]
d["reference"] = [
    {"image": "reference/pantherk_ii.aws67.webp", "view": "iso",
     "mask": "reference/pantherk_ii.aws67.webp_mask.png", "approximate": True},
    {"image": "reference/pantherk_ii.aws66.webp", "view": "front",
     "mask": "reference/pantherk_ii.aws66.webp_mask.png", "approximate": True},
]
json.dump(d, open(dst, "w"), indent=1)
print("wrote", dst)

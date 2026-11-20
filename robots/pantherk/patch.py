"""Hand patches on top of `robot gen build` output (reproduce: python3 robots/pantherk/patch.py out/wedge.json robots/pantherk/spec.json).

1. Two free-running idler wheels on the front axle (photos show 4 wheels, 2 per side; the generator's 2WD has 2).
2. Reference entries for the two photos (generator output has none).
"""
import copy
import json
import sys

IDLER_Y = 32.0  # front axle, mm (photos: wheels at the four corners, outboard of the plate)
DRIVE_Y = -20.0
WHEEL_X = 51.0  # outboard of the 92 mm body

src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src))
parts = d["parts"]
wl = next(p for p in parts if p["id"] == "wheel_l")
wr = next(p for p in parts if p["id"] == "wheel_r")
idl = copy.deepcopy(wl); idl["id"] = "idler_l"; idl["at"] = [abs(wl["at"][0]), IDLER_Y, 0.0]; idl["label"] = "left idler"
idr = copy.deepcopy(wr); idr["id"] = "idler_r"; idr["at"] = [-abs(wr["at"][0]), IDLER_Y, 0.0]; idr["label"] = "right idler"
for w, sx in ((wl, 1), (wr, -1)):
    w["at"] = [sx * WHEEL_X, DRIVE_Y, 0.0]
idl["at"][0] = WHEEL_X; idr["at"][0] = -WHEEL_X
parts.insert(parts.index(wr) + 1, idr)
parts.insert(parts.index(wl) + 1, idl)
reason = ("Free-running idler wheel on a fixed pin through the chassis side walls: carries its share of the robot "
          "weight and runs free, no drive torque.")
d["connections"] += [
    {"a": "idler_l", "b": "chassis_bottom", "method": "shaft", "reason": reason},
    {"a": "idler_r", "b": "chassis_bottom", "method": "shaft", "reason": reason},
]
# Photos: the front is two separate ramp blocks with an open notch between them, not one full-width plow.
wd = next(p for p in parts if p["id"] == "wedge")
GAP_W, GAP_Y0 = 34.0, 48.0
TIP_Y = 74.0  # blocks are short in the photo
wd["shape"] = {"type": "subtract", "base": wd["shape"], "cut": [
    {"type": "place", "shape": {"type": "box", "size": [200.0, 80.0, 80.0]}, "at": [0.0, TIP_Y + 40.0, 0.0], "rot": [0.0, 0.0, 0.0]},
    {"type": "place", "shape": {"type": "box", "size": [20.0, 80.0, 80.0]}, "at": [50.0, GAP_Y0 + 40.0, 0.0], "rot": [0.0, 0.0, 0.0]},
    {"type": "place", "shape": {"type": "box", "size": [20.0, 80.0, 80.0]}, "at": [-50.0, GAP_Y0 + 40.0, 0.0], "rot": [0.0, 0.0, 0.0]},
    {"type": "place", "shape": {"type": "box", "size": [GAP_W, 80.0, 80.0]}, "at": [0.0, GAP_Y0 + 40.0, 0.0], "rot": [0.0, 0.0, 0.0]}]}
wd["label"] = "two printed ramp blocks with a centre notch"
d["reference"] = [
    {"image": "reference/pantherk_ii.aws67.webp", "view": "iso",
     "mask": "reference/pantherk_ii.aws67.webp_mask.png", "approximate": True},
    {"image": "reference/pantherk_ii.aws66.webp", "view": "front",
     "mask": "reference/pantherk_ii.aws66.webp_mask.png", "approximate": True},
]
json.dump(d, open(dst, "w"), indent=1)
print("wrote", dst)

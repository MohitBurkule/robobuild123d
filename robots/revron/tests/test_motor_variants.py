"""Both weapon motor variants ("datasheet", "step") build the same part ids and mounting relations; only the catalog models differ."""
import json, os, subprocess, sys

SRC = os.path.join(os.path.dirname(__file__), "..", "src")
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))
CODE = """
import json, sys
sys.path.insert(0, %r); sys.path.insert(0, %r)
from revron.spec import make_spec
from revron.params import MOTOR
from robot import catalog, shapes
spec = make_spec("src/build_revron.py")
parts = {p["id"]: p for p in spec["parts"]}
for cid in (MOTOR["stator"], MOTOR["can"]):
    shapes.validate(catalog.find(cid).shape)
keep = ("weapon_motor_stator", "weapon_motor_can", "wshaft", "spider")
print(json.dumps({"ids": sorted(parts), "cat": [parts[k].get("catalog") for k in keep[:2]], "pos": {k: [parts[k].get("parent"), parts[k].get("at"), parts[k].get("rot")] for k in keep}}))
""" % (ROOT, SRC)


def _spec(variant):
    env = dict(os.environ, REVRON_MOTOR_VARIANT=variant)
    out = subprocess.run([sys.executable, "-c", CODE], env=env, capture_output=True, text=True, check=True, cwd=ROOT).stdout
    return json.loads(out.strip().splitlines()[-1])


def test_variants_swap_models_not_mounts():
    ds, st = _spec("datasheet"), _spec("step")
    assert ds["ids"] == st["ids"] and ds["pos"] == st["pos"]
    assert ds["cat"] != st["cat"] and st["cat"] == ["gr1507_step", "gr1507_step_can"]

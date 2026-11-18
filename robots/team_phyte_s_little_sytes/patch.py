"""Hand patches applied after `robot gen build` (reproducible: python3 robots/team_phyte_s_little_sytes/patch.py)."""
import json
import pathlib

SPEC = pathlib.Path(__file__).with_name("spec.json")
PHOTOS = ["aws74", "aws76", "aws77"]

spec = json.loads(SPEC.read_text())
# likeness.no_reference: the generator does not write photo references; link the three photos + masks.
spec["reference"] = [
    {"image": f"reference/team_phyte_s_little_sytes.{p}.webp",
     "mask": f"reference/team_phyte_s_little_sytes.{p}.webp_mask.png",
     "view": "iso", "approximate": True}
    for p in PHOTOS
]
SPEC.write_text(json.dumps(spec, indent=1) + "\n")
print("patched", SPEC)

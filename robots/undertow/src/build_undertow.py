"""Undertow generator entry (mirrors robots/revron/src/build_revron.py). UNTESTED: never built, run, rendered or verified.

spec.json references parts as {"type": "model", "file": "src/build_undertow.py", "params": {"part": "<name>"}};
`build(part=...)` is the only geometry entry point. Settings: env UNDERTOW_SETTINGS='{"front": "plough"}' or
`python build_undertow.py --set front=plough`.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REVRON_SRC = os.path.join(ROOT, "robots", "revron", "src")   # reused package `revron` (hw, plate)
for _p in (ROOT, REVRON_SRC, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _apply_cli_settings(argv):
    s = json.loads(os.environ.get("UNDERTOW_SETTINGS", "{}"))
    for i, a in enumerate(argv):
        if a == "--set" and i + 1 < len(argv):
            k, v = argv[i + 1].split("=", 1)
            s[k] = v
    if s:
        os.environ["UNDERTOW_SETTINGS"] = json.dumps(s)


def build(part="assembly", start_config=False):
    import undertow
    if part == "assembly":
        return undertow.assembly.assembly(start_config)
    return undertow.assembly.parts(start_config)[part]


def main():
    _apply_cli_settings(sys.argv[1:])
    import build123d as bd
    import undertow
    out = os.path.join(HERE, "..", "step")
    os.makedirs(out, exist_ok=True)
    bd.export_step(undertow.assembly.assembly(start_config=True), os.path.join(out, "undertow_start.step"))
    p = undertow.params
    print(json.dumps(dict(width=p.WIDTH_ALL, length_start=p.LENGTH_START, height_start=p.Z_TOP_START,
                          envelope_max=p.ENVELOPE_MAX, height_max=p.HEIGHT_MAX, rules=p.RULESET, fits=p.FITS_ENVELOPE), indent=1))


if __name__ == "__main__":
    main()

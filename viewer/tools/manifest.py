import json, sys
from pathlib import Path
B = Path(sys.argv[1]); slugs = Path(sys.argv[2]).read_text().split()
rows = []
for s in slugs:
    m = json.loads((B / "out/meta" / f"{s}.json").read_text())
    rows.append({"slug": s, "model": m.get("model"), "bbox": m.get("bbox"), "parts": m.get("parts"),
                 "photos": [{"name": p["name"], "src": f"photos/{s}/{p['name']}.jpg", "orig": p["file"], "w": p["w"], "h": p["h"],
                             "default": p["default"]} for p in m["photos"]], "errors": m.get("errors")})
(B / "out/robots.json").write_text(json.dumps({"convention": "model mm, Z up, front=+y, right=+x; azimuth of camera position from +x toward +y; elevation above XY plane", "robots": rows}, separators=(",", ":")))
print(len(rows), sum(len(r["photos"]) for r in rows), sum(1 for r in rows if r["model"]))

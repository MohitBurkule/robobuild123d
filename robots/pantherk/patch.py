"""One-shot patch: take generator output, set name, attach photo masks as likeness references."""
import json, glob, os, sys
here = os.path.dirname(os.path.abspath(__file__)); slug = os.path.basename(here)
src = glob.glob(f"out/{slug}/*.json")[0]
s = json.load(open(src)); s["name"] = slug
skip = {"pantherk": ["aws66", "aws68"]}.get(slug, [])  # bad masks (cluttered background)
refs = []
for m in sorted(glob.glob(f"{here}/reference/*_mask.png")):
    if any(k in m for k in skip): continue
    img = [p for p in glob.glob(f"{here}/reference/*.webp") if os.path.basename(m).startswith(os.path.basename(p).replace('.webp',''))][0]
    refs.append({"image": os.path.relpath(img, here), "view": "iso", "mask": os.path.relpath(m, here), "approximate": True})
s["reference"] = refs
json.dump(s, open(f"{here}/spec.json", "w"), indent=1)

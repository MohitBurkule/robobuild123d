"""`robot diff-photo spec.json`: side-by-side of each reference photo and the model rendered from the camera that
matches it best, plus a list of concrete differences.

Writes renders/diff_<photo>.png (photo | model render | silhouette overlay). With ANTHROPIC_API_KEY set (and the
`anthropic` package), a small model (Haiku) looks at each sheet and lists differences: wheels, ramp, weapon,
proportions, missing parts. Without it, open the sheet yourself and list them. Use it beside `robot likeness`: the
IoU says how far off the outline is, this says what to change.
"""

from __future__ import annotations

import base64
import io
import os
from pathlib import Path

import numpy as np

MODEL = os.environ.get("ROBOT_DIFF_MODEL", "claude-haiku-5-5")
PROMPT = ("Left: photo of a real antweight combat robot. Middle: our CAD model from about the same camera. Right: outline "
          "overlay (red = model only, blue = photo only). List the concrete differences that make the model not look "
          "like the photo, most important first, as short imperative edits with sizes relative to the robot length: "
          "body shape and proportions, wheels (count, size, position), front ramp/wedge/forks, weapon (type, size, "
          "position, teeth), missing or extra parts. Max 8 lines. No praise.")


def sheet(photo, render_png: bytes, overlay_png: bytes, h=360, label=None) -> bytes:
    from PIL import Image, ImageDraw
    ims = [Image.open(photo).convert("RGB"), Image.open(io.BytesIO(render_png)).convert("RGB"),
           Image.open(io.BytesIO(overlay_png)).convert("RGB")]
    ims = [im.resize((max(1, int(im.width * h / im.height)), h)) for im in ims]
    out = Image.new("RGB", (sum(i.width for i in ims) + 20, h), "white")
    x = 0
    for im in ims:
        out.paste(im, (x, 0))
        x += im.width + 10
    if label:
        d = ImageDraw.Draw(out)
        d.rectangle((0, h - 22, 9 * len(label) + 12, h), fill="black")
        d.text((6, h - 18), label, fill="white")
    b = io.BytesIO()
    out.save(b, format="PNG")
    return b.getvalue()


def ask(png: bytes) -> str | None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        import anthropic
    except ImportError:
        return None
    msg = anthropic.Anthropic().messages.create(
        model=MODEL, max_tokens=500,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                         "data": base64.b64encode(png).decode()}},
            {"type": "text", "text": PROMPT}]}])
    return "".join(getattr(c, "text", "") for c in msg.content).strip()


def main(spec_path, out_dir=None):
    from . import render as R, spec as spec_mod, world as world_mod
    from .checks import likeness as L, reference as ref
    s = spec_mod.load(spec_path)
    base = Path(s.base_dir)
    r = world_mod.resolve(s, fast=True)
    w = world_mod.World.start(r)
    sils = L._sils(w)
    dirs = L._dirs()
    od = Path(out_dir or base / "renders")
    od.mkdir(parents=True, exist_ok=True)
    ents = [e for e in ref.entries(s) if e.get("mask") and e.get("image")]
    if not ents:
        print("no `reference` entries with image + mask")
        return 1
    for e in ents:
        mask = ref.load_mask(base / e["mask"])
        ci = L.best_match(sils, mask, L.allowed(*L.photo_view(L._refjson(s), e)))[2]
        if ci < 0:
            print(f"== {e['image']}: no camera allowed for its declared view")
            continue
        k, mir = divmod(ci, 2)
        d = np.asarray(dirs[k], float)
        up = np.array([0, 1.0, 0]) if abs(d[2]) > 0.99 else np.array([0, 0, 1.0])
        png = R.render_png(w, R.View("diff", d, up, None, 700, 0.0))
        if mir:
            from PIL import Image, ImageOps
            b = io.BytesIO()
            ImageOps.mirror(Image.open(io.BytesIO(png))).save(b, format="PNG")
            png = b.getvalue()
        _, a, bm = ref.compare(sils[ci], mask)
        sh = sheet(base / e["image"], png, ref.overlay_png(a, bm), label=f"camera: {L.cam_name(ci)}")
        p = od / f"diff_{Path(e['image']).stem}.png"
        p.write_bytes(sh)
        print(f"== {e['image']}: sheet {p} (camera {L.cam_name(ci)})")
        txt = ask(sh)
        print(txt if txt else "   (no ANTHROPIC_API_KEY: open the sheet and list the differences yourself)")
    return 0


def add_cli(sub):
    p = sub.add_parser("diff-photo", help="photo | model | overlay sheets per reference photo + listed differences")
    p.add_argument("spec")
    p.add_argument("--out")
    p.set_defaults(func=lambda a: main(a.spec, a.out))

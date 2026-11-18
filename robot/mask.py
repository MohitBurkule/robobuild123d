"""`robot mask PHOTO OUT.png`: binary robot mask (white = robot) from a reference photo on a plain background.

Background colour = median of the image border; a pixel is robot when its colour differs from it by more than `--thr`
(0-255 RGB distance). Keeps the largest connected blob (plus blobs >= 2 % of it, e.g. a separate weapon), fills holes.
The `likeness` gate re-runs this on the photo to prove a spec's mask came from the photo, not from the model.
"""

from __future__ import annotations

import numpy as np

THR = 40.0


def photo_mask(path, thr: float = THR, max_px: int = 900, crop=None, mode: str = "plain") -> np.ndarray:
    """mode "textured" (wood, cardboard, carpet): blur away grain, threshold at max(thr, 2x the 80th-percentile border colour spread),
    keep only the blob nearest the photo centre (plus blobs >= 10 % of it)."""
    from PIL import Image
    from scipy import ndimage as nd

    im = Image.open(path).convert("RGB")
    if crop:  # [x0, y0, x1, y1] as fractions 0..1 of the photo (one robot when the photo shows two)
        W, H = im.size
        x0, y0, x1, y1 = (float(v) for v in crop)
        im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    im.thumbnail((max_px, max_px))
    a = np.asarray(im, float)
    k = max(2, min(a.shape[:2]) // 50)
    if mode == "textured":
        a = nd.uniform_filter(a, size=(k, k, 1))
    border = np.concatenate([a[:k].reshape(-1, 3), a[-k:].reshape(-1, 3), a[:, :k].reshape(-1, 3), a[:, -k:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    d = np.linalg.norm(a - bg, axis=2)
    if mode == "textured":
        bd = np.linalg.norm(border - bg, axis=1)
        thr = max(thr, 2.0 * float(np.percentile(bd, 80)))
    fg = d > thr
    fg = nd.binary_opening(fg, iterations=1)
    fg = nd.binary_closing(fg, iterations=3)
    lab, n = nd.label(fg)
    if n == 0:
        return fg
    sizes = nd.sum(fg, lab, range(1, n + 1))
    if mode == "textured":
        H, W = fg.shape
        com = nd.center_of_mass(fg, lab, range(1, n + 1))
        big = [i for i, s in enumerate(sizes) if s >= 0.01 * fg.size] or [int(np.argmax(sizes))]
        c = min(big, key=lambda i: (com[i][0] / H - 0.5) ** 2 + (com[i][1] / W - 0.5) ** 2)
        keep = [i + 1 for i, s in enumerate(sizes) if i == c or s >= 0.10 * sizes[c]]
    else:
        keep = [i + 1 for i, s in enumerate(sizes) if s >= 0.02 * sizes.max()]
    return nd.binary_fill_holes(np.isin(lab, keep))


def main(photo, out, thr=THR, crop=None, mode="plain"):
    from PIL import Image
    m = photo_mask(photo, thr, crop=[float(v) for v in crop.split(",")] if crop else None, mode=mode)
    Image.fromarray(m.astype(np.uint8) * 255).save(out)
    print(f"wrote {out}: {m.mean() * 100:.1f}% robot. Open it: white must be the robot only (raise --thr if the floor "
          f"shows, lower it if parts are missing).")
    return 0


def add_cli(sub):
    p = sub.add_parser("mask", help="robot silhouette mask PNG from a reference photo (plain background)")
    p.add_argument("photo")
    p.add_argument("out")
    p.add_argument("--thr", type=float, default=THR)
    p.add_argument("--crop", help="x0,y0,x1,y1 fractions 0..1: keep only this box (photo with two robots)")
    p.add_argument("--textured", action="store_true", help="wood/cardboard/carpet background; record it in "
                   "REFERENCE.json `mask_mode` {photo: \"textured\"} so the likeness gate re-runs the same mode")
    p.set_defaults(func=lambda a: main(a.photo, a.out, a.thr, a.crop, "textured" if a.textured else "plain"))

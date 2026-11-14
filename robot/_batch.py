"""Batching of many small 2D boxes for vectorised rasterisation (render z-buffer, voxel column parity).

Triangles are grouped by the power-of-two size of their pixel/cell box, so each group is evaluated as one dense
(n, h, w) numpy block instead of one python iteration per triangle."""

from __future__ import annotations

import numpy as np

CELLS = 1 << 21  # block elements per chunk (about 16 MB per float64 temporary)
BIG = 96  # boxes wider or taller than this go to the caller's per-triangle path (few, and each is already vectorised)


def _pow2(n: np.ndarray) -> np.ndarray:
    return np.left_shift(1, np.ceil(np.log2(np.maximum(n, 1))).astype(np.int64))


def chunks(idx: np.ndarray, bw: np.ndarray, bh: np.ndarray, cells: int = CELLS, big: int = BIG):
    """Split triangle indices `idx` (box sizes bw, bh, same length) into (small, large).

    small: list of (indices, w, h) with every box of the chunk fitting in w x h and n * w * h <= cells.
    large: indices whose box exceeds `big` on a side."""
    idx = np.asarray(idx)
    large = (bw > big) | (bh > big)
    small = []
    if (~large).any():
        si = idx[~large]
        cw, ch = _pow2(bw[~large]), _pow2(bh[~large])
        code = cw * (4 * big) + ch
        for u in np.unique(code):
            sel = si[code == u]
            w, h = int(u // (4 * big)), int(u % (4 * big))
            n = max(1, cells // (w * h))
            for s in range(0, len(sel), n):
                small.append((sel[s:s + n], w, h))
    return small, idx[large]

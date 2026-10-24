"""Round 15: SolidWorks Contents/DisplayLists tessellation reader (final-body display mesh).

Observed layout (little-endian): vertex arrays are introduced by
    u32 12 (stride bytes) | u32 100 | u32 prim | u32 N | f32[3N]
A position array is immediately followed by its normal array with the same header
(12, 100, prim, N).  prim 2 = triangle strips; the strip lengths are the u32 array (4, 8, 2, K, l1..lK)
that precedes the position header.
Coordinates are model space, metres.  Only the pattern is relied on; everything
between arrays (face headers, colours, edge display data) is skipped.
"""
import struct
import numpy as np
from . import container as C

HDR = struct.Struct('<4I')


def arrays(p):
    """yield (offset, prim, positions[N,3], normals[N,3] or None)."""
    i = 0; n = len(p)
    while True:
        i = p.find(b'\x0c\x00\x00\x00\x64\x00\x00\x00', i)
        if i < 0 or i + 16 > n: return
        _, _, prim, N = HDR.unpack_from(p, i)
        end = i + 16 + 12 * N
        if prim > 16 or N == 0 or N > 10_000_000 or end > n:
            i += 4; continue
        P = np.frombuffer(p, '<f4', 3 * N, i + 16).reshape(N, 3).astype(float)
        if not np.isfinite(P).all() or np.abs(P).max() > 100:
            i += 4; continue
        Nm = None
        if end + 16 <= n and p[end:end + 8] == p[i:i + 8] and HDR.unpack_from(p, end)[3] == N and end + 16 + 12 * N <= n:
            Nm = np.frombuffer(p, '<f4', 3 * N, end + 16).reshape(N, 3).astype(float)
            if not (np.abs(np.linalg.norm(Nm, axis=1) - 1) < 1e-2).all(): Nm = None
        if Nm is not None:
            yield i, prim, P, Nm
            i = end + 16 + 12 * N
        else:
            i = end


def display_payload(path_or_bytes):
    d = open(path_or_bytes, 'rb').read() if isinstance(path_or_bytes, str) else path_or_bytes
    for s in C.parse(d)[0]:
        if s.name == 'Contents/DisplayLists' and s.payload: return s.payload
    return None


def strip_lengths(p, i, N):
    """u32 array (4, 8, 2, K, l1..lK) ending right before the position header at i, sum(l) == N."""
    for K in range(1, min(N, 20000) + 1):
        j = i - 16 - 4 * K
        if j < 0: return None
        h = HDR.unpack_from(p, j)
        if h[0] == 4 and h[1] == 8 and h[2] == 2 and h[3] == K:
            L = struct.unpack_from(f'<{K}I', p, j + 16)
            if sum(L) == N: return L
    return None


def triangles(path_or_bytes):
    """triangle soup [T,3,3] in mm.  Each face is a set of triangle strips: strip lengths
    (u32 array 4|8|2|K|l...) precede the position array; winding is set from the normals."""
    p = display_payload(path_or_bytes)
    if p is None: return None
    out = []
    for i, prim, P, Nm in arrays(p):
        L = strip_lengths(p, i, len(P))
        if L is None: continue
        k = 0
        for l in L:
            S = P[k:k + l]; Ns = Nm[k:k + l]; k += l
            if l < 3: continue
            t = np.arange(l - 2)
            a = np.where(t % 2 == 0, t, t + 1); b = np.where(t % 2 == 0, t + 1, t); c = t + 2
            T = np.stack([S[a], S[b], S[c]], 1)
            n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
            flip = (n * (Ns[a] + Ns[b] + Ns[c])).sum(1) < 0
            T[flip] = T[flip][:, [0, 2, 1]]
            ok = np.linalg.norm(n, axis=1) > 1e-16
            out.append(T[ok] * 1e3)
    return np.concatenate(out) if out else None


def volume(T):
    return float(np.einsum('ij,ij->i', T[:, 0], np.cross(T[:, 1], T[:, 2])).sum() / 6)

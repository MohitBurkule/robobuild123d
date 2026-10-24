"""Per-part reference oracle from research/rvrn_step (assembly STLs + asmdump XFORM).

REFERENCE ONLY: the mesh is used to *choose* regions / blend edges / extents. No geometry from it is
ever written to the generated macro.
"""
import os
import re
import numpy as np

from . import SLDPRT

STEP_DIR = os.path.normpath(os.path.join(SLDPRT, '..', 'rvrn_step'))
ASM = os.path.join(SLDPRT, 'dumps_v2', 'rvrn 2.0.asmdump.txt')


def _norm(s):
    return re.sub(r'_+', '_', re.sub(r'[^A-Za-z0-9]', '_', s)).strip('_').lower()


def read_stl(path):
    """binary or ascii STL -> (n,3,3) triangles (file units, mm)."""
    data = open(path, 'rb').read()
    if len(data) > 84:
        n = int(np.frombuffer(data[80:84], '<u4')[0])
        if 84 + 50 * n == len(data):
            rec = np.frombuffer(data[84:], dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]))
            return rec['v'].astype(float)
    pts = [list(map(float, l.split()[1:4])) for l in data.decode('ascii', 'replace').splitlines() if l.strip().startswith('vertex')]
    return np.array(pts, float).reshape(-1, 3, 3)


def asm_xforms(path=ASM):
    """component instance name ('RV12 N10 2200 RPM-1') -> (file stem, rows 3x3, t mm)."""
    out = {}
    if not os.path.exists(path):
        return out
    cur = None
    for raw in open(path, encoding='utf-8', errors='replace'):
        s = raw.strip()
        if s.startswith('COMP '):
            name = s[5:].split('|')[0].strip()
            m = re.search(r'file=([^|]+)', s)
            stem = os.path.splitext(m.group(1).strip().replace('\\', '/').split('/')[-1])[0] if m else None
            cur = (name, stem)
        elif s.startswith('XFORM') and cur:
            v = [float(x) for x in s[5:].split(',') if x.strip()]
            out[cur[0]] = (cur[1], np.array(v[:9]).reshape(3, 3), np.array(v[9:12]) * 1000.0)
            cur = None
    return out


class RefMesh:
    def __init__(self, tris, name):
        self.tris = tris
        self.name = name
        self.fit = False      # True: orientation fitted to extents only (not used to choose)
        self.lo = tris.reshape(-1, 3).min(0)
        self.hi = tris.reshape(-1, 3).max(0)
        a = tris[:, 1] - tris[:, 0]; b = tris[:, 2] - tris[:, 0]
        self.vol = float(np.einsum('ij,ij->i', tris[:, 0], np.cross(a, b)).sum() / 6.0)

    def inside(self, P):
        """ray-parity point-in-mesh (ray along a slightly skewed +z)."""
        P = np.atleast_2d(np.asarray(P, float))
        out = np.zeros(len(P), bool)
        d = np.array([1e-4, 2.3e-4, 1.0]); d /= np.linalg.norm(d)
        v0, v1, v2 = self.tris[:, 0], self.tris[:, 1], self.tris[:, 2]
        e1, e2 = v1 - v0, v2 - v0
        h = np.cross(d, e2); a = np.einsum('ij,ij->i', e1, h)
        ok = np.abs(a) > 1e-12
        v0, e1, e2, h, a = v0[ok], e1[ok], e2[ok], h[ok], a[ok]
        f = 1.0 / a
        for i, p in enumerate(P):
            if np.any(p < self.lo - 1e-6) or np.any(p > self.hi + 1e-6):
                continue
            s = p - v0
            u = f * np.einsum('ij,ij->i', s, h)
            q = np.cross(s, e1)
            v = f * (q @ d)
            t = f * np.einsum('ij,ij->i', e2, q)
            out[i] = (((u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-9)).sum() % 2) == 1
        return out


def find_ref(part_name, part=None):
    """RefMesh in the PART frame (mm) for a dump part, or None.

    Instances (asmdump COMP, possibly nested 'sub-1/part-1') and STL files (<part>_<k>.stl) are not
    numbered consistently, so every (xform, stl) pair is mapped to the part frame and the pair whose
    part-frame bbox is shared by the most pairs wins (a correct pairing is frame-invariant).
    """
    pdir = os.path.join(STEP_DIR, 'parts')
    if not os.path.isdir(pdir):
        return None
    key = _norm(part_name)
    allx = asm_xforms()
    xfs = [(k, v) for k, v in allx.items() if v[0] and _norm(v[0]) == key]
    stls = sorted(f for f in os.listdir(pdir) if re.fullmatch(re.escape(key) + r'_\d+', _norm(os.path.splitext(f)[0])))
    if not xfs or not stls:
        return None
    cands = []
    for f in stls:
        tris = read_stl(os.path.join(pdir, f)).reshape(-1, 3)
        for inst, (_, R, t) in xfs:
            chain = inst.split('/')
            variants = [tris]
            if len(chain) > 1:          # nested placement may be root-relative or parent-relative
                loc = tris
                for i in range(1, len(chain)):
                    par = allx.get('/'.join(chain[:i]))
                    if par is not None:
                        loc = (loc - par[2]) @ par[1].T
                variants.append(loc)
            for v in variants:
                loc = (v - t) @ R.T      # p_asm = t + x*r0 + y*r1 + z*r2  ->  p_part = R (p_asm - t)
                cands.append((f, inst, loc, np.round(np.r_[loc.min(0), loc.max(0)], 1)))
    box = dump_box(part) if part is not None else None
    if box is not None:
        best = min(cands, key=lambda c: float(np.abs(c[3] - box).max()))
        tol = max(1.0, 0.05 * float(np.ptp(box.reshape(2, 3), 0).max()))
        if float(np.abs(best[3] - box).max()) > tol:
            # placement chain unknown (nested sub-assembly): axis-aligned fit of the mesh to the dump's
            # face extents; marked 'fit' (orientation of near-symmetric parts may be ambiguous)
            import itertools
            fits = []
            for perm in itertools.permutations(range(3)):
                for sg in itertools.product((1, -1), repeat=3):
                    Q = np.zeros((3, 3)); Q[range(3), perm] = sg
                    if np.linalg.det(Q) < 0:
                        continue
                    loc = cands[0][2] @ Q.T
                    lo, hi = loc.min(0), loc.max(0)
                    loc = loc + (box[:3] + box[3:]) / 2 - (lo + hi) / 2
                    bb = np.r_[loc.min(0), loc.max(0)]
                    fits.append((float(np.abs(bb - box).max()), loc))
            err, loc = min(fits, key=lambda x: x[0])
            if err > tol:
                return None
            r = RefMesh(loc.reshape(-1, 3, 3), f'{cands[0][0]} (fit to dump extents)')
            r.fit = True
            return r
    else:
        best = max(cands, key=lambda c: sum(np.allclose(c[3], d[3], atol=0.15) for d in cands))
    return RefMesh(best[2].reshape(-1, 3, 3), f'{best[0]} @ {best[1]}')


def dump_box(part):
    """union of the dump's FACE boxes (mm) of the final body, or None."""
    B = [F.box for g in part.features if g.idx >= 0 for F in (g.faces or []) if getattr(F, 'box', None)]
    if not B:
        return None
    B = np.array(B, float) * 1000.0
    return np.r_[B[:, :3].min(0), B[:, 3:].max(0)]


def body_agreement(ref, body, n=3000, seed=2):
    """fraction of points sampled in the ref bbox where ref-inside == body-inside (frame sanity check)."""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    from OCP.gp import gp_Pnt
    rng = np.random.default_rng(seed)
    P = rng.uniform(ref.lo, ref.hi, (n, 3))
    a = ref.inside(P)
    cls = BRepClass3d_SolidClassifier(body.wrapped)
    b = np.zeros(n, bool)
    for i, p in enumerate(P):
        cls.Perform(gp_Pnt(*p), 1e-6); b[i] = cls.State() == TopAbs_IN
    inter = (a & b).sum(); uni = (a | b).sum()
    return float(inter / uni) if uni else 0.0


def mc_iou(ref, body, n=6000, seed=3):
    """Monte-Carlo IoU of the replay body against the reference mesh over the union bbox."""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    from OCP.gp import gp_Pnt
    bb = body.bounding_box()
    lo = np.minimum(ref.lo, [bb.min.X, bb.min.Y, bb.min.Z]); hi = np.maximum(ref.hi, [bb.max.X, bb.max.Y, bb.max.Z])
    P = np.random.default_rng(seed).uniform(lo, hi, (n, 3))
    a = ref.inside(P)
    cls = BRepClass3d_SolidClassifier(body.wrapped)
    b = np.zeros(n, bool)
    for i, p in enumerate(P):
        cls.Perform(gp_Pnt(*p), 1e-6); b[i] = cls.State() == TopAbs_IN
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0

"""Loading: SolidWorks feature dump (via dump_parser), refs.txt (faces per feature) and asmdump MASS lines."""
from __future__ import annotations
import os, re

import numpy as np
from dataclasses import dataclass, field
from typing import Optional

from . import SLDPRT  # noqa: F401  (sets sys.path)
from dump_parser import parse_dump, parse_text, parse_surface, Part, Feature, blend_params  # noqa: F401

STD_PLANES = ('Front Plane', 'Top Plane', 'Right Plane')
# std plane normals in model space (from the dumps' PLANE lines: rows x, y, z(normal))
STD_NORMAL = {'Front Plane': (0.0, 0.0, 1.0), 'Top Plane': (0.0, 1.0, 0.0), 'Right Plane': (1.0, 0.0, 0.0)}
STD_FRAME = {'Front Plane': ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
             'Top Plane': ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
             'Right Plane': ((0, 0, -1), (0, 1, 0), (1, 0, 0))}


def load_part(path: str) -> Part:
    return parse_dump(path)


def part_name_from_path(path: str) -> str:
    b = os.path.basename(path)
    for suf in ('.dump.txt', '.refs.txt', '.txt'):
        if b.endswith(suf):
            return b[:-len(suf)]
    return os.path.splitext(b)[0]


# ----------------------------------------------------------------------------- refs.txt
@dataclass
class RefFace:
    index: int
    area: float
    surface: object           # dump_parser.Surface (kind, params, box)
    n_edges: int = 0
    pref: str = ''


@dataclass
class RefFeature:
    name: str
    type: str
    id: int
    faces: list = field(default_factory=list)


def _surface_from_refs(desc: str):
    """refs.txt surfaces: 'plane nx,ny,nz,ox,oy,oz, box=...' / 'cyl ox,oy,oz,ax,ay,az,r' ... -> Surface."""
    desc = desc.strip()
    box = None
    m = re.search(r'box=([^\s]+)', desc)
    if m:
        box = [float(x) for x in m.group(1).strip(',').split(',') if x]
        desc = desc[:m.start()].strip()
    head, _, rest = desc.partition(' ')
    vals = [float(x) for x in rest.strip().strip(',').split(',') if x.strip()]
    from dump_parser import Surface
    if head == 'plane' and len(vals) >= 6:
        p = dict(n=tuple(vals[0:3]), o=tuple(vals[3:6]))
    elif head == 'cyl' and len(vals) >= 7:
        p = dict(o=tuple(vals[0:3]), ax=tuple(vals[3:6]), r=vals[6])
    else:
        p = dict(values=vals)
    return Surface(head if head in ('plane', 'cyl', 'cone', 'torus', 'sphere') else 'other', p, box, None, desc)


def parse_refs(path: str) -> dict:
    """name -> RefFeature. EDGE lines carry only persistent ids (no geometry) and are only counted."""
    out = {}
    cur = None
    face = None
    if not path or not os.path.exists(path):
        return out
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for raw in fh:
            line = raw.rstrip('\r\n')
            s = line.strip()
            if s.startswith('FEATURE '):
                parts = [p.strip() for p in s[8:].split('|')]
                fid = -1
                for p in parts:
                    if p.startswith('id='):
                        try: fid = int(p[3:])
                        except ValueError: pass
                cur = RefFeature(parts[0], parts[1] if len(parts) > 1 else '', fid)
                out.setdefault(cur.name, cur)
                face = None
            elif s.startswith('FACE ') and cur is not None:
                m = re.match(r'FACE (\d+) fid=\S+ area=(\S+) (.*?)(?: pref=\S+)?$', s)
                if not m:
                    continue
                try:
                    srf = _surface_from_refs(m.group(3))
                except Exception:
                    continue
                face = RefFace(int(m.group(1)), float(m.group(2)), srf)
                cur.faces.append(face)
            elif s.startswith('EDGE') and face is not None:
                face.n_edges += 1
    return out


# ----------------------------------------------------------------------------- assembly MASS
def parse_asm_mass(path: str) -> dict:
    """part file stem -> dict(vol=m3, mass=kg, area=m2) from 'COMP ... | file=...' + 'MASS ...' lines."""
    out = {}
    if not path or not os.path.exists(path):
        return out
    stem = None
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for raw in fh:
            s = raw.strip()
            if s.startswith('COMP '):
                m = re.search(r'file=([^|]+)', s)
                stem = None
                if m:
                    f = m.group(1).strip().replace('\\', '/').split('/')[-1]
                    stem = os.path.splitext(f)[0]
            elif s.startswith('MASS ') and stem:
                kv = dict(re.findall(r'(\w+)=(\([^)]*\)|\S+)', s))
                try:
                    out.setdefault(stem, dict(vol=float(kv['vol']), mass=float(kv['mass']),
                                              area=float(kv.get('area', 'nan'))))
                except (KeyError, ValueError):
                    pass
    return out


def find_refs(dump_path: str) -> Optional[str]:
    """dumps_v2/<part>.dump.txt -> dumps_v3/revdev/<part>.refs.txt (or swtests/) if it exists."""
    name = part_name_from_path(dump_path)
    for sub in ('revdev', 'swtests'):
        p = os.path.join(SLDPRT, 'dumps_v3', sub, name + '.refs.txt')
        if os.path.exists(p):
            return p
    p = os.path.join(os.path.dirname(dump_path), name + '.refs.txt')
    return p if os.path.exists(p) else None


# ----------------------------------------------------------------------------- dumps_v4_edges (DumpEdges_macro)
_P3 = r'\(([^)]*)\)'


@dataclass
class EdgeRec:
    """one EDGE/BEDGE/BLEND_EDGE line (metres). mid_ok: the dumped m= point is usable."""
    kind: str
    s: tuple
    e: tuple
    m: tuple
    L: Optional[float]
    params: tuple = ()          # circle/ellipse params from the kind token
    mid_ok: bool = True
    pref: str = ''
    samples: tuple = ()         # DumpEdges v3 samp= points on bcurves (parameter steps)

    @property
    def closed(self):
        return float(np.linalg.norm(np.subtract(self.s, self.e))) < 1e-9


def _edge_rec(s, head):
    toks = s.split()
    kind = toks[head] if len(toks) > head and '=' not in toks[head] else 'curve'
    params = ()
    if len(toks) > head + 1 and '=' not in toks[head + 1]:
        try:
            params = tuple(float(x) for x in toks[head + 1].strip(',').split(',') if x)
        except ValueError:
            params = ()

    def p3(tag):
        m = re.search(r'(?:^|\s)' + tag + r'=' + _P3, s)
        if not m:
            return None
        try:
            return tuple(float(x) for x in m.group(1).split(','))
        except ValueError:
            return None
    st, en, mi = p3('s'), p3('e'), p3('m')
    if not (st and en):
        return None
    m = re.search(r'len=(\S+)', s)
    try:
        L = float(m.group(1)) if m else None
    except ValueError:
        L = None
    pr = re.search(r'pref=(\S+)', s)
    chord = tuple((a + b) / 2 for a, b in zip(st, en))
    ok = mi is not None
    if kind == 'line':
        # the macro evaluates the line at the mean of GetCurveParams3 U values, which is not the edge
        # mid point for most lines (70% of the dumped lines): the chord mid point is exact
        mi, ok = chord, True
    elif ok and L:
        # the mid point must lie on the edge: |s-m| + |m-e| <= length
        if np.linalg.norm(np.subtract(st, mi)) + np.linalg.norm(np.subtract(mi, en)) > L * 1.0001 + 1e-9:
            ok = False
    if not ok:
        mi = chord
    smp = ()
    sm = re.search(r'samp=(\S+)', s)
    if sm:
        try:
            v = [float(x) for x in sm.group(1).strip(',').split(',') if x]
            smp = tuple(tuple(v[i:i + 3]) for i in range(0, len(v) - 2, 3))
        except ValueError:
            smp = ()
    return EdgeRec(kind, st, en, mi, L, params, ok, pr.group(1)[-160:] if pr else '', smp)


def parse_edge_file(path: str) -> dict:
    """<part>.edges.txt -> dict(features=[(name, type, faces, blend_items, stale)], bedges=[EdgeRec]).
    faces = [(surface head, [EdgeRec])].

    stale: Feature.GetFaces failed for that feature (the call returns Nothing, the assignment to the
    Variant errors under On Error Resume Next) and the macro printed the PREVIOUS feature's face list
    again. Such a list (identical face prefs to the previous listed feature) is dropped."""
    feats, bedges = [], []
    cur = None
    if not path or not os.path.exists(path):
        return dict(features=feats, bedges=bedges)
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for raw in fh:
            s = raw.strip()
            if s.startswith('FEATURE '):
                parts = [x.strip() for x in s[8:].split('|')]
                cur = dict(name=parts[0], type=parts[1] if len(parts) > 1 else '', faces=[], prefs=[], items=[],
                           stale=False)
                feats.append(cur)
            elif s.startswith('BODY '):
                cur = None
            elif s.startswith('BEDGE '):
                e = _edge_rec(s, 1)
                if e:
                    bedges.append(e)
            elif cur is None:
                continue
            elif s.startswith('BLEND_EDGE'):
                e = _edge_rec(s, 2)
                if e:
                    cur['items'].append(e)
            elif s.startswith('FACE '):
                toks = s.split()
                head = toks[4] if len(toks) > 4 else ''
                pr = re.search(r'pref=(\S+)', s)
                cur['faces'].append((head, []))
                cur['prefs'].append(pr.group(1) if pr else s[:120])
            elif s.startswith('EDGE ') and cur['faces']:
                e = _edge_rec(s, 1)
                if e:
                    cur['faces'][-1][1].append(e)
    prev = None
    for f in feats:
        if not f['prefs']:
            continue
        if prev is not None and f['prefs'] == prev['prefs']:
            f['stale'] = True
        prev = f
    return dict(features=feats, bedges=bedges)


def _shares_vertex(a, b, tol=1e-7):
    return any(np.linalg.norm(np.subtract(p, q)) < tol for p in (a.s, a.e) for q in (b.s, b.e))


def blend_rails(edges):
    """the two rails of one blend face: same kind, no common vertex, longest pair. -> (a, b) or None."""
    best = None
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            a, b = edges[i], edges[j]
            if a.kind != b.kind or not a.L or not b.L:
                continue
            if a.closed != b.closed:
                continue
            if not a.closed and _shares_vertex(a, b):
                continue
            if min(a.L, b.L) / max(a.L, b.L) < 0.4:
                continue
            sc = a.L + b.L
            if best is None or sc > best[0]:
                best = (sc, a, b)
    return best[1:] if best else None


def parse_edges(path: str) -> dict:
    """<part>.edges.txt (DumpEdges_macro) -> {blend feature: [(kind, start, end, mid, length, sep)]}, metres.

    BLEND_EDGE lines (the blend's own items) are exact and used as-is (sep = 0). Without them, the sharp
    edges are DERIVED from the blend feature's own FACE/EDGE lines: each blend face is bounded by two rails
    (the tangent / chamfer edges: same kind, no shared vertex); the consumed sharp edge runs between
    them, so the hint is the rails' average with kind 'derived:<kind>' and sep = rail separation (the
    planner drops hints whose rails are further apart than the blend size allows). Derived hints are
    matched to the live body with a blend-size tolerance (replay, VBA) and replaced by the matched edge.
    Stale face lists (see parse_edge_file) are ignored.
    """
    out = {}
    d = parse_edge_file(path)
    for f in d['features']:
        if not re.search(r'fillet|chamfer', f['type'], re.I):
            continue
        if f['items']:
            out[f['name']] = [(e.kind, e.s, e.e, e.m, e.L, 0.0) for e in f['items']]
            continue
        if f['stale']:
            continue
        hints = []
        seen = set()
        for head, es in f['faces']:
            r = blend_rails(es)
            if r is None:
                continue
            a, b = r
            A, B = np.array(a.s), np.array(a.e)
            C, D = np.array(b.s), np.array(b.e)
            if not a.closed and np.linalg.norm(A - C) + np.linalg.norm(B - D) > np.linalg.norm(A - D) + np.linalg.norm(B - C):
                C, D = D, C
            if a.closed:
                # closed rails: start points are arbitrary seam points; use the rails' circle centres
                # when the kind carries them, else their mid points
                sep = float(np.linalg.norm(np.array(a.params[:3]) - np.array(b.params[:3]))) if len(a.params) >= 7 and len(b.params) >= 7 else 0.0
                if len(a.params) >= 7 and len(b.params) >= 7:
                    ra, rb = a.params[6], b.params[6]
                    sep = float(np.hypot(sep, ra - rb))
            else:
                sep = float(min(np.linalg.norm(A - C), np.linalg.norm(B - D)))
            mid = (np.array(a.m) + np.array(b.m)) / 2
            S_, E_ = tuple((A + C) / 2), tuple((B + D) / 2)
            key = tuple(np.round(np.r_[S_, E_, mid], 7))
            if key in seen:
                continue
            seen.add(key)
            hints.append(('derived:' + a.kind, S_, E_, tuple(mid), (a.L + b.L) / 2, sep))
        if hints:
            out[f['name']] = hints
    return out


def edge_curves(path: str) -> list:
    """all bcurve EdgeRecs of a <part>.edges.txt (body edges + non-stale feature face edges)."""
    d = parse_edge_file(path)
    out = [e for e in d['bedges'] if e.kind == 'bcurve']
    out += [e for f in d['features'] if not f['stale'] for _, es in f['faces'] for e in es if e.kind == 'bcurve']
    return out


def find_edges(dump_path: str):
    p = os.path.join(SLDPRT, 'dumps_v4_edges', part_name_from_path(dump_path) + '.edges.txt')
    return p if os.path.exists(p) else None

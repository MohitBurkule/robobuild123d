"""Parser for the SolidWorks API answer-key dumps (macro/DumpFeatures.swp.bas).

dumps_v2/<part>.dump.txt  ->  Dump(part, features=[Feat...]) where each Feat
holds the API-reported values used to train / validate the binary layouts.
Nested 'FEATURE -1' blocks (sub-features re-listed under their owner) are
kept in Feat.children; the canonical copy of a sketch is its top-level one.
"""
import re
from dataclasses import dataclass, field

NUM = r'[-+]?[0-9.]+(?:E[-+]?[0-9]+)?'


def _f(s):
    return float(s)


def _ids(s):
    return [tuple(int(x) for x in t.split('_')) for t in s.split()]


@dataclass
class Feat:
    idx: int
    name: str
    type: str
    id: int
    suppressed: bool
    level: int = 0
    dims: list = field(default_factory=list)        # [(fullname, value)]
    parents: list = field(default_factory=list)     # [(name, type)]
    sketch_to_model: list = None
    pts: dict = field(default_factory=dict)         # (a,b) -> (x,y,z)
    segs: list = field(default_factory=list)        # dicts
    rels: list = field(default_factory=list)        # (type, [ids])
    contours: list = field(default_factory=list)    # (closed, [ids])
    faces: list = field(default_factory=list)       # dicts
    extrude: dict = None
    fillet: dict = None
    chamfer: dict = None
    plane: list = None
    children: list = field(default_factory=list)


@dataclass
class Dump:
    part: str
    features: list

    def top(self):
        return [f for f in self.features if f.level == 0]

    def sketches(self):
        return [f for f in self.features if f.level == 0 and f.type == 'ProfileFeature']

    def by_type(self, *types):
        return [f for f in self.features if f.level == 0 and f.type in types]


def _seg(line):
    m = re.match(r'SEG (\d+)_(\d+) type=(\d+) constr=(\w+)(.*)', line)
    d = {'id': (int(m.group(1)), int(m.group(2))), 'type': int(m.group(3)), 'constr': m.group(4) == 'True'}
    rest = m.group(5)
    for k in ('c', 'p0', 'p1'):
        mm = re.search(r'\b' + k + r'=\(([^)]*)\)', rest)
        if mm:
            d[k] = tuple(_f(x) for x in mm.group(1).split(','))
    for k in ('r', 'dir'):
        mm = re.search(r'\b' + k + '=(' + NUM + ')', rest)
        if mm:
            d[k] = _f(mm.group(1))
    return d


def _face(line):
    m = re.match(r'FACE (\w+)\s*(.*)', line)
    d = {'kind': m.group(1), 'raw': m.group(2)}
    rest = m.group(2)
    for k in ('n', 'o', 'ax'):
        mm = re.search(r'\b' + k + r'=\(([^)]*)\)', rest)
        if mm:
            d[k] = tuple(_f(x) for x in mm.group(1).split(','))
    mm = re.search(r'\br=(' + NUM + ')', rest)
    if mm:
        d['r'] = _f(mm.group(1))
    mm = re.search(r'area=(' + NUM + ')', rest)
    if mm:
        d['area'] = _f(mm.group(1))
    mm = re.search(r'box=([^ ]*)', rest)
    if mm:
        d['box'] = [_f(x) for x in mm.group(1).split(',') if x]
    if d['kind'] in ('cone', 'torus', 'sphere'):
        d['params'] = [_f(x) for x in rest.split(' box=')[0].split(',') if x.strip()]
    return d


def parse(path):
    lines = open(path, encoding='latin-1').read().splitlines()
    part = lines[0][5:].rsplit('.', 1)[0] if lines and lines[0].startswith('PART ') else ''
    feats, cur, top = [], None, None
    for raw in lines[1:]:
        s = raw.strip()
        if not s:
            continue
        if s.startswith('FEATURE '):
            p = [x.strip() for x in s[8:].split('|')]
            lvl = 1 if p[0] == '-1' else 0
            f = Feat(int(p[0]), p[1], p[2], int(p[3][3:]), p[4].endswith('True'), lvl)
            if lvl == 0 or top is None:
                feats.append(f)
                top = f
            else:
                f.level = 1
                top.children.append(f)
            cur = f
            continue
        if cur is None:
            continue
        key = s.split(' ', 1)[0]
        body = s[len(key):].strip()
        if key == 'DIM':
            n, v = body.rsplit(' = ', 1)
            cur.dims.append((n, _f(v)))
        elif key == 'PARENT':
            n, t = body.rsplit(' | ', 1)
            cur.parents.append((n, t))
        elif key == 'SKETCH_TO_MODEL':
            cur.sketch_to_model = [_f(x) for x in body.split(',') if x]
        elif key == 'PLANE':
            cur.plane = [_f(x) for x in body.split(',') if x]
        elif key == 'PT':
            m = re.match(r'(\d+)_(\d+) \(([^)]*)\)', body)
            cur.pts[(int(m.group(1)), int(m.group(2)))] = tuple(_f(x) for x in m.group(3).split(','))
        elif key == 'SEG':
            cur.segs.append(_seg(s))
        elif key == 'REL':
            m = re.match(r'type=(\d+) ents=(.*)', body)
            cur.rels.append((int(m.group(1)), _ids(m.group(2))))
        elif key == 'CONTOUR':
            m = re.match(r'(\d+) closed=(\w+) segs=(.*)', body)
            cur.contours.append((m.group(2) == 'True', _ids(m.group(3))))
        elif key == 'FACE':
            cur.faces.append(_face(s))
        elif key == 'EXTRUDE':
            d = dict(re.findall(r'(\w+)=(\S+)', body))
            cur.extrude = {k: (v == 'True' if v in ('True', 'False') else _f(v)) for k, v in d.items()}
        elif key in ('FILLET', 'CHAMFER'):
            d = dict(re.findall(r'(\w+)=(\S*)', body))
            setattr(cur, key.lower(), {k: (_f(v) if v else None) for k, v in d.items()})
    return Dump(part, feats)


def _ends(sg):
    return [tuple(round(v, 9) for v in sg[k]) for k in ('p0', 'p1') if k in sg]


def resolve_contour(feat, ids):
    """Contour ids carry no segment type (lines and arcs have separate id spaces).
    Resolve each id to a seg dict: prefer non-construction, then the candidate whose
    end points touch the other segments of the contour."""
    by = {}
    for sg in feat.segs:
        by.setdefault(sg['id'], []).append(sg)
    out, used = [], set()
    for k, i in enumerate(ids):
        c = by.get(i, [])
        if ids.count(i) > 1:
            c = [s for s in c if (s['type'], s['id']) not in used] or c
        if len(c) > 1:
            nc = [s for s in c if not s['constr']]
            c = nc or c
        if len(c) > 1:
            others = set()
            for j in ids[:k] + ids[k + 1:]:
                for s in by.get(j, []):
                    others.update(_ends(s))
            sc = [(sum(e in others for e in _ends(s)), s['type'] == 1 and len(ids) == 1, s) for s in c]
            sc.sort(key=lambda t: (t[0], t[1]), reverse=True)
            c = [sc[0][2]]
        out.append(c[0] if c else None)
        if c:
            used.add((c[0]['type'], c[0]['id']))
    return out

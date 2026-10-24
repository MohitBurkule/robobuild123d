"""Parser for SolidWorks feature dumps written by research/sldprt/macro/DumpFeatures.swp.bas.

Usage:
    part = parse_dump(path)            # or parse_text(str)
    for f in part.features: ...        # top-level tree order (sub-features in f.children)
    part.sketch_of(feature)            # the ProfileFeature a feature consumes (via PARENT)

Line kinds (all values SI: metres / radians):
    PART <title>
    [indent]FEATURE <idx> | <name> | <type> | id=<n> | suppressed=<bool>
    DIM <FullName> = <SystemValue>
    PARENT <name> | <type>
    SKETCH_TO_MODEL 16 numbers (9 rotation, rows = images of sketch x/y/z; 3 translation; scale; 3 unused)
    PT <id> (x,y,z)                         sketch space
    SEG <id> type=<0 line|1 arc|2 ellipse|3 spline|4 text> constr=<bool> p0=() p1=() [c=() r= dir=] [len=]
    REL type=<swConstraintType_e> ents=<id> <id> ...
    CONTOUR <i> closed=<bool> segs=<id> ...
    EXTRUDE end1= d1= both= end2= d2= reverse= draft1= thin= merge=
    UPTO_REF1/UPTO_REF2 type=<n> <surface desc>          (v2)
    FILLET r= type= items= ;  CHAMFER type= d= angle=
    EDGE <i> start=() end=()                               (v2)
    FACE <surface desc> area=                              (v2)
    FACES <n>                                              (v1: face count only)
    PLANE 16 numbers
Surface desc: "plane n=() o=()", "cyl o=() ax=() r=", "cone|torus|sphere <csv>", "surf id=<n>",
optionally followed by " box=<6 csv>".
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional

# swEndConditions_e
END_COND = {0: 'blind', 1: 'through_all', 2: 'up_to_next', 3: 'up_to_vertex', 4: 'up_to_surface',
            5: 'offset_from_surface', 6: 'mid_plane', 7: 'up_to_body', 9: 'through_all_both'}
SEG_TYPE = {0: 'line', 1: 'arc', 2: 'ellipse', 3: 'spline', 4: 'text', 5: 'parabola'}

_NUM = r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'


def _f(s: str) -> float:
    return float(s.replace(',', '.')) if s.count(',') == 0 else float(s)


def _vec(s: str):
    return tuple(float(x) for x in s.strip('()').split(','))


def _csv(s: str):
    return [float(x) for x in s.strip().strip(',').split(',') if x.strip() != '']


def _bool(s: str) -> bool:
    return s.strip().lower() == 'true'


@dataclass
class Surface:
    kind: str                      # plane | cyl | cone | torus | sphere | surf | other
    params: dict = field(default_factory=dict)
    box: Optional[list] = None
    area: Optional[float] = None
    raw: str = ''


def parse_surface(desc: str) -> Surface:
    desc = desc.strip()
    area = None
    m = re.search(r'\sarea=(' + _NUM + r')\s*$', desc)
    if m:
        area = float(m.group(1)); desc = desc[:m.start()]
    box = None
    m = re.search(r'\sbox=([^\s]+)', desc)
    if m:
        box = _csv(m.group(1)); desc = desc[:m.start()] + desc[m.end():]
    kv = dict(re.findall(r'(\w+)=(\([^)]*\)|[^\s]+)', desc))
    head = desc.split(' ', 1)[0]
    p = {}
    if head == 'plane':
        p = dict(n=_vec(kv['n']), o=_vec(kv['o']))
    elif head == 'cyl':
        p = dict(o=_vec(kv['o']), ax=_vec(kv['ax']), r=float(kv['r']))
    elif head in ('cone', 'torus', 'sphere'):
        p = dict(values=_csv(desc.split(' ', 1)[1]) if ' ' in desc else [])
    elif head == 'surf':
        p = dict(id=kv.get('id'))
    else:
        head = 'other'
    return Surface(head, p, box, area, desc)


@dataclass
class Seg:
    id: str
    type: int
    construction: bool
    p0: Optional[tuple] = None
    p1: Optional[tuple] = None
    c: Optional[tuple] = None
    r: Optional[float] = None
    dir: Optional[int] = None
    length: Optional[float] = None

    @property
    def kind(self): return SEG_TYPE.get(self.type, f'type{self.type}')

    @property
    def is_circle(self):
        return self.type == 1 and self.p0 is not None and max(abs(a - b) for a, b in zip(self.p0, self.p1)) < 1e-12


@dataclass
class Contour:
    index: int
    closed: bool
    segs: list


@dataclass
class Sketch:
    rot: list            # 3 rows: model images of sketch x, y, z(normal)
    trans: tuple
    scale: float
    points: dict = field(default_factory=dict)
    segs: list = field(default_factory=list)
    rels: list = field(default_factory=list)    # (type, [ids])
    contours: list = field(default_factory=list)

    def to_model(self, p):
        x, y, z = p[0], p[1], (p[2] if len(p) > 2 else 0.0)
        R = self.rot
        return tuple(self.trans[i] + self.scale * (x * R[0][i] + y * R[1][i] + z * R[2][i]) for i in range(3))

    @property
    def normal(self): return tuple(self.rot[2])

    def profile_segs(self):
        return [s for s in self.segs if not s.construction]


@dataclass
class Extrude:
    end1: int; d1: float; both: bool; end2: int; d2: float; reverse: bool
    draft1: float = 0.0; thin: bool = False; merge: bool = True
    upto1: Optional[Surface] = None; upto1_type: Optional[int] = None
    upto2: Optional[Surface] = None; upto2_type: Optional[int] = None

    @property
    def end1_name(self): return END_COND.get(self.end1, f'end{self.end1}')

    @property
    def end2_name(self): return END_COND.get(self.end2, f'end{self.end2}')


@dataclass
class Feature:
    idx: int
    name: str
    type: str
    id: int
    suppressed: bool
    level: int
    dims: dict = field(default_factory=dict)
    parents: list = field(default_factory=list)     # (name, type)
    sketch: Optional[Sketch] = None
    extrude: Optional[Extrude] = None
    fillet: Optional[dict] = None
    chamfer: Optional[dict] = None
    plane: Optional[list] = None
    edges: list = field(default_factory=list)       # (start, end) metres
    faces: list = field(default_factory=list)       # Surface
    face_count: Optional[int] = None
    children: list = field(default_factory=list)    # sub-feature names

    def own_dims(self):
        return {k.split('@')[0]: v for k, v in self.dims.items() if k.split('@')[1:2] == [self.name]}


@dataclass
class Part:
    title: str
    features: list                  # top-level, tree order
    by_name: dict

    def sketch_of(self, feat: Feature) -> Optional[Feature]:
        for n, t in feat.parents:
            if t in ('ProfileFeature', '3DProfileFeature'):
                return self.by_name.get(n)
        for n in feat.children:
            f = self.by_name.get(n)
            if f is not None and f.sketch is not None:
                return f
        return None

    def solid_features(self):
        skip = {'ProfileFeature', '3DProfileFeature', 'RefPlane', 'OriginProfileFeature'}
        return [f for f in self.features if f.idx >= 0 and f.type not in skip and not f.type.endswith('Folder')
                and f.type not in ('DetailCabinet', 'EnvFolder', 'MaterialFolder')]


_FEAT = re.compile(r'^( *)FEATURE (-?\d+) \| (.*) \| ([^|]*) \| id=(-?\d+) \| suppressed=(\w+)\s*$')


def parse_text(text: str) -> Part:
    title = ''
    features, by_name = [], {}
    cur: Optional[Feature] = None
    top: Optional[Feature] = None
    for raw in text.splitlines():
        line = raw.rstrip('\r\n')
        if not line.strip():
            continue
        if line.startswith('PART '):
            title = line[5:].strip(); continue
        m = _FEAT.match(line)
        if m:
            lvl = len(m.group(1)) // 2
            f = Feature(int(m.group(2)), m.group(3).strip(), m.group(4).strip(), int(m.group(5)),
                        _bool(m.group(6)), lvl)
            if lvl == 0:
                features.append(f); top = f
                by_name.setdefault(f.name, f)
                if by_name[f.name] is not f and by_name[f.name].idx < 0:
                    by_name[f.name] = f
            else:
                if top is not None: top.children.append(f.name)
                if f.name not in by_name: by_name[f.name] = f
            cur = f
            continue
        if cur is None:
            continue
        s = line.strip()
        key, _, rest = s.partition(' ')
        try:
            _parse_line(cur, key, rest)
        except Exception as e:  # keep going, but record the problem
            cur.__dict__.setdefault('errors', []).append(f'{key}: {e}')
    return Part(title, features, by_name)


def _parse_line(f: Feature, key: str, rest: str):
    if key == 'DIM':
        n, _, v = rest.rpartition(' = ')
        f.dims[n.strip()] = float(v)
    elif key == 'PARENT':
        n, _, t = rest.rpartition(' | ')
        f.parents.append((n.strip(), t.strip()))
    elif key == 'SKETCH_TO_MODEL':
        a = _csv(rest)
        f.sketch = Sketch([a[0:3], a[3:6], a[6:9]], tuple(a[9:12]), a[12] if len(a) > 12 and a[12] else 1.0)
    elif key == 'PT':
        pid, v = rest.split(' ', 1)
        f.sketch.points[pid] = _vec(v)
    elif key == 'SEG':
        sid, body = rest.split(' ', 1)
        kv = dict(re.findall(r'(\w+)=(\([^)]*\)|[^\s]+)', body))
        sg = Seg(sid, int(kv['type']), _bool(kv.get('constr', 'False')))
        for k in ('p0', 'p1', 'c'):
            if k in kv: setattr(sg, k, _vec(kv[k]))
        if 'r' in kv: sg.r = float(kv['r'])
        if 'dir' in kv: sg.dir = int(kv['dir'])
        if 'len' in kv: sg.length = float(kv['len'])
        f.sketch.segs.append(sg)
    elif key == 'REL':
        m = re.match(r'type=(-?\d+)\s+ents=(.*)$', rest)
        f.sketch.rels.append((int(m.group(1)), m.group(2).split()))
    elif key == 'CONTOUR':
        m = re.match(r'(\d+)\s+closed=(\w+)\s+segs=(.*)$', rest)
        f.sketch.contours.append(Contour(int(m.group(1)), _bool(m.group(2)), m.group(3).split()))
    elif key == 'EXTRUDE':
        kv = dict(re.findall(r'(\w+)=([^\s]+)', rest))
        f.extrude = Extrude(int(kv['end1']), float(kv['d1']), _bool(kv['both']), int(kv['end2']),
                            float(kv['d2']), _bool(kv['reverse']), float(kv.get('draft1', 0)),
                            _bool(kv.get('thin', 'False')), _bool(kv.get('merge', 'True')))
    elif key in ('UPTO_REF1', 'UPTO_REF2'):
        m = re.match(r'type=(-?\d+)\s*(.*)$', rest)
        srf = parse_surface(m.group(2))
        if key == 'UPTO_REF1':
            f.extrude.upto1, f.extrude.upto1_type = srf, int(m.group(1))
        else:
            f.extrude.upto2, f.extrude.upto2_type = srf, int(m.group(1))
    elif key == 'FILLET':
        kv = dict(re.findall(r'(\w+)=([^\s]+)', rest))
        f.fillet = dict(r=float(kv['r']), type=int(kv['type']), items=int(kv['items']))
    elif key == 'CHAMFER':
        kv = dict(re.findall(r'(\w+)=([^\s]+)', rest))
        f.chamfer = dict(type=int(kv['type']), d=float(kv['d']), angle=float(kv['angle']))
    elif key == 'EDGE':
        m = re.match(r'(\d+)\s+start=(\([^)]*\))\s+end=(\([^)]*\))', rest)
        f.edges.append((_vec(m.group(2)), _vec(m.group(3))))
    elif key == 'FACE':
        f.faces.append(parse_surface(rest))
    elif key == 'FACES':
        f.face_count = int(rest)
    elif key == 'PLANE':
        f.plane = _csv(rest)


def parse_dump(path: str) -> Part:
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        return parse_text(fh.read())


def blend_params(f: Feature):
    """(kind, size_m) for a fillet/chamfer: dims are authoritative, fall back to the FILLET/CHAMFER line."""
    d = f.own_dims()
    if f.type == 'Fillet':
        return 'fillet', d.get('D1', (f.fillet or {}).get('r'))
    if f.type.startswith('Chamfer'):
        return 'chamfer', d.get('D1', (f.chamfer or {}).get('d')), d.get('D2', (f.chamfer or {}).get('angle'))
    return None


if __name__ == '__main__':
    import sys
    p = parse_dump(sys.argv[1])
    print(p.title)
    for f in p.features:
        sk = p.sketch_of(f)
        extra = ''
        if f.extrude:
            e = f.extrude
            extra = f'{e.end1_name} d1={e.d1*1e3:g} both={e.both} {e.end2_name} d2={e.d2*1e3:g} rev={e.reverse}'
        if f.fillet: extra = f'r={f.fillet["r"]*1e3:g}'
        print(f'{f.idx:3d} {f.name:18s} {f.type:16s} sketch={sk.name if sk else "-":10s} {extra}')

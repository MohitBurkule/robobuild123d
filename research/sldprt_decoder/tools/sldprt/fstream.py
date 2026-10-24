"""Feature-stream (Config-0-ResolvedFeatures, MFC CArchive) record layouts, round 5.

Every layout here was located by searching the bytes for values that the
SolidWorks API dump (dumps_v2/, see answer_key.py) reports, then fixed as
explicit offsets.  Kaitai versions of the same layouts are in ksy/*.ksy.
Field accuracy is measured by validate.py (train half / validation half).

Records (offsets in bytes, all little endian):

FeatureHeader  (every moXxx_c feature / folder object)
    CString name | u32 0 | u32 flags | u32 feature_id | u32 0 | CString comment
    feature_id == IFeature.GetID.  The record runs to the next header.

Sketch entity arrays  (sgSketch body)
    u32 count | u16 aux | count x entity record
    entity record = u32 serial | i32 persistent_id | 17-byte marker
                    FF FF 1F 00 03 <8> 00 00 80 BF | body
    Arrays appear in the order points, lines, arcs[, ellipses, splines ...].
    The API id pair of a point / segment is (index in its array, persistent_id).
    serial (the 'a' field) is a sketch-wide segment serial used by chains and
    by region / contour-chooser edge references.
    body R = marker_end + 47:
      point    u16 0x1E @R, f64 x @R+2, f64 y @R+10 (sketch metres)
      segment  u16 start @R, u16 end @R+2, u16 real @R+4 (1 real, 0 construction),
               f64 -1.0 @R+8, u16 type @R+16 (0 line, 1 arc, 0xFFFF arc),
               u16 centre @R+20 (arcs).  start/end/centre index the point array.

Relation record  (sgSketch body, after the entities)
    geometric:  u32 type | u16 2 | u16 hidden | u16 aux | u16 FFFE | u16 0 | slots
    dimension:  u32 type | u16 2 | u16 shown  | u16 aux | u16 0            | slots
    slot = u16 handle_class_ref | u16 entity_index | i32 -1 | u32 0   (12 bytes)
    type = swConstraintType_e.  The API lists geometric records with hidden==0
    and dimension records with shown==1 (duplicates are display copies).
    handle_class_ref -> sgPointHandle/sgLineHandle/sgArcHandle is resolved by
    MFC class order (tag_map).

moSketchChain_c  (one per closed/open contour = ISketchContour)
    u16 n | n x u32 segment serial | 60-byte tail (u16 closed, ...)
    preceded by the list header u32 N | u32 N.

Sketch regions and region selection
    region list : u16 1 | u32 100000+k | moOneContour_c   (region k of the sketch)
    moOneContour_c : u16 n_edges | n x moEdgeRef_c
    moEdgeRef_c : u32 kind (1, or 2 for a contour edge on shared geometry) | u32 0|1 |
                  05 00 00 00 xx 0[03] 00 00 00 00 00 00 ...
                  then refs  u16 cls | 00 00 | u16 cls2 | u16 ? | u32 sketch_feature_id
                             | u32 stamp | u32 segment_serial | u32 0
    moContourChooser_c (the selection used by the consuming feature):
                  u16 n_selected | n x moOneContour_c
    A selected contour is identified with a sketch region by its edge serial set.
    No chooser = every region of the sketch is used.

moEndSpec_c  (anchor S = class tag; first use = classdef, else learned tag)
    S+2 u16 0 | S+4 u16 dir1 (0 for dir-2-only 'through all both') |
    S+12 u8 reverse | S+18 u8 end_condition (swEndConditions_e) |
    S+22 u8 end_condition_2.  Depth = first DimValue after S (D1), second = D2.
"""
import math
import re
import struct
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict

from . import mfc

MARK = re.compile(rb'\xff\xff\x1f\x00\x03.{8}\x00\x00\x80\xbf', re.S)
NEG1 = struct.pack('<d', -1.0)


def u16(d, o): return struct.unpack_from('<H', d, o)[0]
def u32(d, o): return struct.unpack_from('<I', d, o)[0]
def i32(d, o): return struct.unpack_from('<i', d, o)[0]
def f64(d, o): return struct.unpack_from('<d', d, o)[0]


# ------------------------------------------------------------------ headers
@dataclass
class FeatureHeader:
    offset: int          # CString start
    end: int             # end of the fixed header fields
    name: str
    flags: int
    feature_id: int
    region_end: int = 0  # start of the next header


def feature_headers(d):
    out = []
    for r in mfc.cstrings(d):
        e = r.end
        if r.value and e + 19 <= len(d) and d[e + 16:e + 19] == b'\xff\xfe\xff' and u32(d, e) == 0 \
                and u32(d, e + 8) < 100000 and u32(d, e + 12) == 0:
            out.append(FeatureHeader(r.offset, e + 16, r.value, u32(d, e + 4), u32(d, e + 8)))
    out.sort(key=lambda h: h.offset)
    for k, h in enumerate(out):
        h.region_end = out[k + 1].offset if k + 1 < len(out) else len(d)
    return out


def header_index(d):
    """first header per feature id -> FeatureHeader"""
    m = {}
    for h in feature_headers(d):
        m.setdefault(h.feature_id, h)
    return m


# ------------------------------------------------------------------ sketch entities
@dataclass
class SketchPoint:
    index: int
    pid: int
    serial: int
    offset: int
    xy: tuple = None          # None for external / reference points without inline coords

    @property
    def api_id(self): return (self.index, self.pid)


@dataclass
class SketchSegment:
    index: int
    pid: int
    serial: int
    offset: int
    kind: str                 # 'line' | 'arc' | 'other'
    start: int = None
    end: int = None
    real: int = None          # 1 real geometry, 0 construction
    type: int = None
    centre: int = None

    @property
    def api_id(self): return (self.index, self.pid)

    @property
    def construction(self): return None if self.real is None else self.real == 0


@dataclass
class Sketch:
    points: list
    lines: list
    arcs: list
    others: list
    spans: list               # (start, end) bytes explained by entity arrays

    def seg(self, api_type, api_id):
        arr = self.lines if api_type == 0 else self.arcs if api_type == 1 else []
        i, pid = api_id
        return arr[i] if i < len(arr) and arr[i].pid == pid else None

    def by_serial(self):
        m = {}
        for s in self.lines + self.arcs:
            m.setdefault(s.serial, s)
        return m


REC_LEN = {'point': 0xA2, 'line': 0x5C, 'arc': 0x70}


def entity_arrays(d, s, e):
    offs = [m.start() - 8 for m in MARK.finditer(d, s, e)]
    out, k = [], 0
    while k < len(offs):
        o = offs[k]
        n = u32(d, o - 6) if o >= 6 else 0
        if 0 < n <= len(offs) - k and n < 5000:
            out.append((o - 6, offs[k:k + n]))
            k += n
        else:
            k += 1
    return out


def parse_sketch(d, s, e):
    P, L, C, O, spans = [], [], [], [], []
    arrs = entity_arrays(d, s, e)
    for ai, (h, recs) in enumerate(arrs):
        R = [o + 72 for o in recs]
        ks = Counter(u16(d, r + 16) for r in R if d[r + 8:r + 16] == NEG1)
        if ai == 0:
            kind = 'point'
        elif not ks:
            kind = 'other'
        else:
            mk = ks.most_common(1)[0][0]
            kind = {0: 'line', 1: 'arc', 0xFFFF: 'arc'}.get(mk, 'other')
            if kind == 'line' and L:
                kind = 'other'
            if kind == 'arc' and C:
                kind = 'other'
        for idx, o in enumerate(recs):
            r = o + 72
            if kind == 'point':
                xy = (f64(d, r + 2), f64(d, r + 10)) if u16(d, r) == 0x1E else None
                P.append(SketchPoint(idx, i32(d, o + 4), u32(d, o), o, xy))
            else:
                sg = SketchSegment(idx, i32(d, o + 4), u32(d, o), o, kind)
                if d[r + 8:r + 16] == NEG1:
                    sg.start, sg.end, sg.real = u16(d, r), u16(d, r + 2), u16(d, r + 4)
                    sg.type, sg.centre = u16(d, r + 16), u16(d, r + 20)
                {'line': L, 'arc': C}.get(kind, O).append(sg)
        last = recs[-1]
        nxt = MARK.search(d, last + 26, e)
        tail = min(last + REC_LEN.get(kind, 0x5C), (nxt.start() - 8) if nxt else e)
        spans.append((h, max(tail, last + 26)))
    return Sketch(P, L, C, O, spans)


# ------------------------------------------------------------------ handle classes
CLASSDEF = re.compile(rb'\xff\xff\x01\x00([\x05-\x40])\x00([A-Za-z_][A-Za-z0-9_]+)')
HANDLES = ('sgPointHandle', 'sgLineHandle', 'sgArcHandle', 'sgEntHandle', 'sgSplineHandle',
           'sgEllipseHandle', 'sgSlotHandle', 'sgParabolaHandle')
REL_HDR = re.compile(rb'([\x01-\x7f])\x00\x00\x00\x02\x00([\x00\x01])\x00([\x00-\x03])\x00(\xfe\xff\x00\x00|\x00\x00)',
                     re.S)
INLINE = re.compile(rb'\xff\xff\x01\x00([\x01-\x40])\x00')


def read_slots(d, j, maxn=8):
    out = []
    while len(out) < maxn and j + 12 <= len(d):
        m = INLINE.match(d, j)
        if m:
            ln = m.group(1)[0]
            name = d[m.end():m.end() + ln].decode('latin1')
            k = m.end() + ln
            if d[k + 2:k + 6] == b'\xff\xff\xff\xff':
                out.append((name, u16(d, k)))
                j = k + 10
                continue
            break
        tag = u16(d, j)
        if tag & 0x8000 and tag != 0xFFFF and d[j + 4:j + 8] == b'\xff\xff\xff\xff':
            out.append((tag, u16(d, j + 2)))
            j += 12
            continue
        break
    return out, j


def tag_map(d):
    """Round 10: an object tag is 0x8000 | class index (objnum numbering).  Use the
    numbered index of each handle ClassDef; fall back to stream-order mapping
    (tag_map_order) for tags the numbering does not hit exactly."""
    from . import objnum as ON
    order = tag_map_order(d)
    try:
        ev, _ = ON.numbering(d)
    except Exception:
        return order
    idx = {e.index: e.name for e in ev if e.kind == 'def' and e.name in HANDLES}
    out = dict(order)
    for t in set(order) | {t for t in _rel_tags(d)}:
        c = idx.get(t & 0x7fff)
        if c:
            out[t] = c
    return out


def _rel_tags(d):
    for m in REL_HDR.finditer(d):
        for t, _ in read_slots(d, m.end())[0]:
            if isinstance(t, int):
                yield t


def tag_map_order(d):
    """MFC class-ref tag -> sg*Handle class name.  MFC numbers classes in stream
    order, so sorted tag values map onto handle ClassDefs in stream order; each
    tag takes the earliest unassigned handle class defined before its first use."""
    hc = [(m.start(), m.group(2)[:m.group(1)[0]].decode()) for m in CLASSDEF.finditer(d)]
    hc = [x for x in hc if x[1] in HANDLES]
    first = {}
    for m in REL_HDR.finditer(d):
        for t, _ in read_slots(d, m.end())[0]:
            if isinstance(t, int):
                first.setdefault(t, m.start())
    out, k = {}, 0
    for t in sorted(first):
        if k < len(hc) and hc[k][0] < first[t]:
            out[t] = hc[k][1]
            k += 1
    return out


# ------------------------------------------------------------------ relations
@dataclass
class Relation:
    offset: int
    end: int
    type: int
    dimension: bool
    flag: int
    aux: int
    slots: list               # [(class, index)]
    ents: list = field(default_factory=list)   # [(class, (index, pid))]

    @property
    def api_visible(self):
        return (self.flag == 1) if self.dimension else (self.flag == 0)


def relations(d, s, e, sk, tmap):
    arr = {'sgPointHandle': sk.points, 'sgLineHandle': sk.lines, 'sgArcHandle': sk.arcs}
    hdrs = [m for m in REL_HDR.finditer(d, s, e)]
    out = []
    for k, m in enumerate(hdrs):
        sl, j = read_slots(d, m.end())
        geo0 = False
        if not sl and len(m.group(4)) == 2 and d[m.end():m.end() + 2] == b'\x00\x00':
            # geometric record whose kind word is 0000 instead of FEFF: slots at +14
            sl, j = read_slots(d, m.end() + 2)
            geo0 = bool(sl)
        if not sl:
            # Round 10: an entity-less geometric relation (API lists it with ents=[]):
            # u32 type | u16 2 | u16 0 | u16 0 | u16 0 | u16 0 | u16 1 (no FEFF, no slots)
            if len(m.group(4)) == 2 and m.group(2)[0] == 0 and m.group(3)[0] == 0 \
                    and d[m.end():m.end() + 4] == b'\x00\x00\x01\x00':
                out.append(Relation(m.start(), m.end() + 6, m.group(1)[0], False, 0, 0, []))
            continue
        nxt = hdrs[k + 1].start() if k + 1 < len(hdrs) else e
        end = nxt if nxt - j <= 100 else j
        r = Relation(m.start(), end, m.group(1)[0], len(m.group(4)) == 2 and not geo0, m.group(2)[0], m.group(3)[0], sl)
        for t, i in sl:
            c = t if isinstance(t, str) else tmap.get(t)
            a = arr.get(c)
            r.ents.append((c, (i, a[i].pid) if a is not None and i < len(a) else (i, -1)))
        out.append(r)
    return out


def api_relations(rels):
    """records the API reports: visible geometric ones, de-duplicated dimension ones."""
    # Round 10: a live dimension is written as a shown (flag 1) record AND a
    # parameter (flag 0) record; a shown record without a parameter twin is a
    # stale display copy of a deleted dimension and the API does not list it.
    def key_(r):
        return (r.type, tuple(sorted(x[1] for x in r.ents)))
    param = {key_(r) for r in rels if r.dimension and r.flag == 0}
    out, seen = [], set()
    for r in rels:
        if not r.api_visible:
            continue
        key = key_(r)
        if r.dimension:
            if key in seen or key not in param:
                continue
            seen.add(key)
        out.append(r)
    return out


# ------------------------------------------------------------------ chains (contours)
CHAIN_CD = b'\xff\xff\x01\x00\x0f\x00moSketchChain_c'
CHAIN_TAIL = 60


@dataclass
class Chain:
    offset: int
    end: int
    serials: list
    closed: int


def chains(d, s, e, chain_tag=None):
    """moSketchChain_c lists in [s,e).  The list header is u32 N | u32 N, then N
    objects (classdef on first use, else class-ref tag)."""
    out = []
    j0 = s
    while True:
        best = None
        for m in re.finditer(rb'([\x01-\x7f])\x00\x00\x00\1\x00\x00\x00', d[j0:e]):
            p = j0 + m.end()
            if d[p:p + len(CHAIN_CD)] == CHAIN_CD or (chain_tag is not None and u16(d, p) == chain_tag):
                best = (j0 + m.start(), m.group(1)[0], p)
                break
        if not best:
            break
        h, N, j = best
        items = []
        for _ in range(N):
            if d[j:j + len(CHAIN_CD)] == CHAIN_CD:
                j += len(CHAIN_CD)
            elif chain_tag is not None and u16(d, j) == chain_tag:
                j += 2
            else:
                break
            n = u16(d, j)
            if not 0 < n < 2000:
                break
            ser = [u32(d, j + 2 + 4 * i) for i in range(n)]
            closed = u16(d, j + 2 + 4 * n)
            k2 = j + 2 + 4 * n + CHAIN_TAIL
            items.append(Chain(j, k2, ser, closed))
            j = k2
        if items:
            items[0].offset = h
            out.extend(items)
        j0 = max(j, h + 8)
    return out


CHAIN_LIST = re.compile(rb'([\x01-\x7f])\x00\x00\x00\1\x00\x00\x00([\x00-\xff][\x80-\xfe])([\x01-\xff])\x00', re.S)


def chain_tag_of(d):
    """class-ref tag of moSketchChain_c: the tag following the first chain object
    (when the first list has >1 chain), else the most common tag that starts a
    plausible chain list 'N N <tag> <n> n*serial <closed 0|1>'."""
    p = d.find(CHAIN_CD)
    if p >= 0:
        j = p + len(CHAIN_CD)
        n = u16(d, j)
        t = u16(d, j + 2 + 4 * n + CHAIN_TAIL)
        if t & 0x8000 and t != 0xFFFF and u16(d, j - len(CHAIN_CD) - 8) > 1:
            return t
    c = Counter()
    for m in CHAIN_LIST.finditer(d):
        j = m.start(2) + 2
        n = m.group(3)[0]
        if j + 4 * n + 4 > len(d):
            continue
        ser = [u32(d, j + 2 + 4 * i) for i in range(n)]
        if all(0 < x < 5000 for x in ser) and u16(d, j + 2 + 4 * n) in (0, 1) and \
                u32(d, j + 2 + 4 * n + 6) == 6:
            c[u16(d, m.start(2))] += 1
    return c.most_common(1)[0][0] if c else None


def computed_contours(sk):
    """Fallback for sketches that store no moSketchChain_c: connected components of
    the real (non-construction) segments, joined at coincident end points."""
    def key(i):
        p = sk.points[i] if i is not None and i < len(sk.points) else None
        return ('xy', round(p.xy[0], 9), round(p.xy[1], 9)) if p is not None and p.xy else ('i', i)
    segs = [g for g in sk.lines + sk.arcs if g.start is not None and g.real == 1]
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for g in segs:
        a, b = key(g.start), key(g.end)
        parent[find(a)] = find(b)
    comp = defaultdict(list)
    for g in segs:
        comp[find(key(g.start))].append(g)
    out = []
    for gs in comp.values():
        deg = Counter()
        for g in gs:
            deg[key(g.start)] += 1
            deg[key(g.end)] += 1
        closed = all(v % 2 == 0 for v in deg.values())
        out.append(Chain(None, None, sorted(g.serial for g in gs), int(closed)))
    return out


# ------------------------------------------------------------------ regions / chooser
EDGE_SIG = re.compile(rb'[\x01\x02]\x00\x00\x00[\x00\x01]\x00\x00\x00\x05\x00\x00\x00[\x00-\xff][\x00\x03]\x00\x00\x00\x00\x00\x00', re.S)
EREF = re.compile(rb'[\x00-\xff][\x80-\xff]\x00\x00[\x00-\xff][\x80-\xff][\x00-\xff]{2}(.{4})(.{4})(.{4})\x00\x00\x00\x00', re.S)
CD_EDGE = b'\xff\xff\x01\x00\x0b\x00moEdgeRef_c'
CD_ONE = b'\xff\xff\x01\x00\x0e\x00moOneContour_c'
CC_NAME = b'moContourChooser_c'
REGION_STUB = re.compile(rb'\x01\x00[\xa0-\xff][\x86-\x89]\x01\x00\x00\x00', re.S)


@dataclass
class Region:
    rid: int                  # sketch region index (u32 100000 + k); None for the classdef form
    offset: int
    edges: list               # per moEdgeRef_c: [segment serial ...]; [] = edgeless stub
    how: str = None           # chooser contours: 'serials' | 'elimination'

    @property
    def serials(self): return sorted(set(x for e in self.edges for x in e) - {0})


@dataclass
class Chooser:
    offset: int
    n_selected: int
    contours: list            # [Region-like (rid matched later)]
    region_ids: list = field(default_factory=list)


EREF_EXT = True


def _ext_eref(d, a, b, sketch_id):
    """round 12: IdRep form with document / configuration CStrings (parts carrying an external
    reference, 1.8_wm1, Elevron 2.0 chassis): '... CString cfg | 14 x 00 | u32 fid | u32 stamp | u32 seq'."""
    out, k = [], d.find(b'\xff\xfe\xff', a, b)
    pat = struct.pack('<I', sketch_id)
    j = d.find(pat, a, b)
    while j >= 0:
        if j + 12 <= b and STAMP_LO < u32(d, j + 4) < STAMP_HI and d[j - 4:j] == b'\0\0\0\0' and u32(d, j + 8) < 100000:
            out.append(u32(d, j + 8))
        j = d.find(pat, j + 1, b)
    return out


STAMP_LO, STAMP_HI = 1_400_000_000, 1_900_000_000


def regions_and_choosers(d, s, e, sketch_id):
    items = [m.start() for m in EDGE_SIG.finditer(d, s, e)]
    heads = []
    for k, q in enumerate(items):
        cde = d.rfind(CD_EDGE, max(s, q - 20), q)
        p = cde if cde >= 0 else q - 2
        if cde < 0 and not (u16(d, p) & 0x8000):
            continue
        n_e, h = u16(d, p - 2), p - 2
        cdo = d.rfind(CD_ONE, max(s, h - 22), h)
        po = cdo if cdo >= 0 else h - 2
        if cdo < 0 and not (u16(d, po) & 0x8000):
            continue
        if not 0 < n_e < 2000:
            continue
        heads.append((k, q, n_e, po, 'cd' if cdo >= 0 else u16(d, po)))
    regs, chs, cur = [], [], None
    n_decl = 0
    for k, q, n_e, po, tag_oc in heads:
        edges = []
        for j in range(k, min(k + n_e, len(items))):
            a, b = items[j], (items[j + 1] if j + 1 < len(items) else e)
            ser = [u32(d, m.start(3)) for m in EREF.finditer(d, a, b) if u32(d, m.start(1)) == sketch_id]
            if not ser and EREF_EXT:
                ser = _ext_eref(d, a, b, sketch_id)
            edges.append(ser)
        if d[po - 6:po - 4] == b'\x01\x00' and 100000 <= u32(d, po - 4) < 101000:
            regs.append(Region(u32(d, po - 4) - 100000, q, edges))
            cur = None
        elif tag_oc == 'cd' and 100000 <= u32(d, po - 6) < 101000:
            # first region of the list (classdef form): u32 100000+k | u16 n_regions | classdef
            regs.append(Region(u32(d, po - 6) - 100000, q, edges))
            n_decl = max(n_decl, u16(d, po - 2)) if u16(d, po - 2) < 1000 else n_decl
            cur = None
        elif cur is not None and len(cur.contours) < cur.n_selected and (tag_oc == cur._tag or cur._tag == 'cd'):
            cur.contours.append(Region(None, q, edges))
            if cur._tag == 'cd':
                cur._tag = tag_oc
        elif d[po - 20:po - 2] == CC_NAME or (u16(d, po - 4) & 0x8000 and 0 < u16(d, po - 2) < 500):
            cur = Chooser(q, u16(d, po - 2), [Region(None, q, edges)])
            cur._tag = tag_oc
            chs.append(cur)
        elif not regs and tag_oc == 'cd':
            regs.append(Region(None, q, edges))
    # edgeless region stubs: 01 00 | u32 100000+k | u16 0 | class tag (bit 15) -- the
    # region's boundary is not stored (it is the remainder of the sketch plane's loops)
    have = {r.rid for r in regs}
    for m in REGION_STUB.finditer(d, s, e):
        k = u32(d, m.start() + 2) - 100000
        if 0 <= k < 1000 and k not in have and u16(d, m.start() + 8) & 0x8000:
            regs.append(Region(k, m.start(), []))
            have.add(k)
    for c in chs:
        for ct in c.contours:
            m = [r.rid for r in regs if r.edges and r.serials == ct.serials]
            ct.rid = m[0] if m else None
            ct.how = 'serials' if m else None
        c.region_ids = [ct.rid for ct in c.contours]
    stubs = [r.rid for r in regs if not r.edges]
    left = [ct for c in chs for ct in c.contours if ct.rid is None]
    if len(stubs) == 1 and len(left) == 1:   # by elimination
        left[0].rid, left[0].how = stubs[0], 'elimination'
        for c in chs:
            c.region_ids = [ct.rid for ct in c.contours]
    # round 12: a region whose list entry is missing (its only copy is the chooser's contour, e.g.
    # ELVRN Alt/SV01 sketch 187: 4 regions, 3 listed) -> the one missing index below the
    # declared region count / highest listed index
    left = [ct for c in chs for ct in c.contours if ct.rid is None and ct.serials]
    have = {r.rid for r in regs if r.rid is not None}
    if REGION_MISSING_ELIM and len(left) == 1 and have:
        miss = set(range(max(n_decl, max(have) + 1))) - have
        if len(miss) == 1:
            left[0].rid, left[0].how = miss.pop(), 'missing'
            for c in chs:
                c.region_ids = [ct.rid for ct in c.contours]
    return regs, chs


REGION_MISSING_ELIM = True


def _seg_polyline(sk, g, n=24):
    """sketch-plane polyline of a line / arc segment (arcs CCW start->end)."""
    P = lambda i: sk.points[i].xy if i is not None and i < len(sk.points) and sk.points[i].xy else None
    a, b = P(g.start), P(g.end)
    if a is None or b is None:
        return []
    if g.kind != 'arc' or P(g.centre) is None:
        return [a, b]
    c = P(g.centre)
    r = math.hypot(a[0] - c[0], a[1] - c[1])
    t0 = math.atan2(a[1] - c[1], a[0] - c[0])
    t1 = math.atan2(b[1] - c[1], b[0] - c[0])
    sweep = (t1 - t0) % (2 * math.pi) or 2 * math.pi
    return [(c[0] + r * math.cos(t0 + sweep * k / n), c[1] + r * math.sin(t0 + sweep * k / n)) for k in range(n + 1)]


def _inside(pt, edges):
    x, y = pt
    c = False
    for (x1, y1), (x2, y2) in edges:
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def _loop_geom(sk, serials):
    bs = sk.by_serial()
    edges, probe = [], None
    for x in serials:
        g = bs.get(x)
        if g is None:
            continue
        pl = _seg_polyline(sk, g)
        edges += list(zip(pl, pl[1:]))
        if probe is None and len(pl) >= 2:
            m = len(pl) // 2
            probe = pl[m] if len(pl) > 2 else ((pl[0][0] + pl[1][0]) / 2, (pl[0][1] + pl[1][1]) / 2)
    return edges, probe


def nested_loops(sk, outer, loops):
    """closed loops lying directly inside the outer serial set (holes of the region:
    SolidWorks removes them from a selected contour's face automatically)."""
    oe, _ = _loop_geom(sk, outer)
    if not oe:
        return []
    cand = []
    for L in loops:
        if set(L) & set(outer):
            continue
        e, pr = _loop_geom(sk, L)
        if pr is not None and _inside(pr, oe):
            cand.append((L, e, pr))
    out = []
    for L, e, pr in cand:   # direct children only (an island inside a hole is not a hole)
        if not any(M is not L and _inside(pr, eM) for M, eM, _ in cand):
            out.append(L)
    return out


def _split_crossings(pieces, tol=1e-12):
    """Round 8: split polylines where two of them cross (or touch) without a shared end point.
    pieces: [(serial, polyline)].  The crossing point is inserted (as the same tuple) into both
    polylines and each polyline is cut there, so the arrangement gets a vertex at every crossing."""
    n = len(pieces)
    bbox = []
    for sr, pl in pieces:
        xs = [p[0] for p in pl]; ys = [p[1] for p in pl]
        bbox.append((min(xs), min(ys), max(xs), max(ys)))
    cuts = defaultdict(list)       # piece -> [(edge index, t, point)]
    for i in range(n):
        ax0, ay0, ax1, ay1 = bbox[i]
        for j in range(i + 1, n):
            bx0, by0, bx1, by1 = bbox[j]
            if bx0 > ax1 + 1e-9 or ax0 > bx1 + 1e-9 or by0 > ay1 + 1e-9 or ay0 > by1 + 1e-9:
                continue
            P, Q = pieces[i][1], pieces[j][1]
            for u in range(len(P) - 1):
                (x1, y1), (x2, y2) = P[u], P[u + 1]
                for v in range(len(Q) - 1):
                    (x3, y3), (x4, y4) = Q[v], Q[v + 1]
                    den = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
                    if abs(den) < 1e-30:
                        continue
                    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / den
                    w = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / den
                    if not (-1e-9 <= t <= 1 + 1e-9 and -1e-9 <= w <= 1 + 1e-9):
                        continue
                    pt = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
                    # skip shared end points of the two pieces (already a vertex)
                    ends = (P[0], P[-1], Q[0], Q[-1])
                    if any(math.hypot(pt[0] - e[0], pt[1] - e[1]) < 1e-9 for e in ends):
                        continue
                    cuts[i].append((u, t, pt))
                    cuts[j].append((v, w, pt))
    if not cuts:
        return pieces
    out = []
    for k, (sr, pl) in enumerate(pieces):
        if k not in cuts:
            out.append((sr, pl))
            continue
        cs = sorted(cuts[k])
        cur = [pl[0]]
        ci = 0
        for u in range(len(pl) - 1):
            while ci < len(cs) and cs[ci][0] == u:
                pt = cs[ci][2]
                if math.hypot(pt[0] - cur[-1][0], pt[1] - cur[-1][1]) > 1e-12:
                    cur.append(pt)
                    out.append((sr, cur))
                    cur = [pt]
                ci += 1
            cur.append(pl[u + 1])
        if len(cur) >= 2:
            out.append((sr, cur))
    return out


SPLIT_CROSSINGS = True


def planar_faces(sk, nsamp=24, split=None, extra=()):
    """Faces of the planar arrangement of the real segments (lines / arcs joined at shared end
    points; round 8: crossings without a shared point are split into vertices too).  Returns
    [(signed area, [serials], probes)] for every face cycle; bounded faces have positive area (CCW)."""
    split = SPLIT_CROSSINGS if split is None else split
    def key(xy):
        return (round(xy[0], 9), round(xy[1], 9))
    pieces = []
    for g in sk.lines + sk.arcs:
        if (g.real != 1 and g.serial not in extra) or g.start is None:
            continue
        pl = _seg_polyline(sk, g, nsamp)
        if len(pl) >= 2:
            pieces.append((g.serial, pl))
    if split:
        pieces = _split_crossings(pieces)
    half = []          # (from, to, serial, polyline)
    for sr, pl in pieces:
        a, b = key(pl[0]), key(pl[-1])
        half.append((a, b, sr, pl))
        half.append((b, a, sr, pl[::-1]))
    out_at = defaultdict(list)
    for k, (a, b, sr, pl) in enumerate(half):
        q = pl[1]
        out_at[a].append((math.atan2(q[1] - pl[0][1], q[0] - pl[0][0]), k))
    for v in out_at.values():
        v.sort()
    twin = {}
    for k in range(0, len(half), 2):
        twin[k], twin[k + 1] = k + 1, k
    used, faces = set(), []
    for k0 in range(len(half)):
        if k0 in used:
            continue
        cyc, k = [], k0
        while k not in used and len(cyc) < 10000:
            used.add(k)
            cyc.append(k)
            a, b, sr, pl = half[k]
            if a == b and len(out_at[b]) == 2:           # isolated circle
                k = k0 if k == k0 else k
                break
            # at vertex b, arriving along pl[-2] -> pl[-1]; take the next edge clockwise from the twin
            t = twin[k]
            lst = out_at[b]
            pos = [j for j, (ang, h) in enumerate(lst) if h == t]
            if not pos:
                break
            k = lst[(pos[0] - 1) % len(lst)][1]
        area = 0.0
        for h in cyc:
            pl = half[h][3]
            for (x1, y1), (x2, y2) in zip(pl, pl[1:]):
                area += x1 * y2 - x2 * y1
        probes = []
        for h in cyc:
            pl = half[h][3]
            (x1, y1), (x2, y2) = pl[len(pl) // 2 - 1], pl[len(pl) // 2]
            L = math.hypot(x2 - x1, y2 - y1) or 1.0
            eps = 1e-6
            probes.append((half[h][2], ((x1 + x2) / 2 - eps * (y2 - y1) / L, (y1 + y2) / 2 + eps * (x2 - x1) / L)))
        faces.append((area / 2, sorted(set(half[h][2] for h in cyc)), probes))
    return faces


def face_expand(sk, contours):
    """Full planar region solve: for every selected contour C, add the boundary of each bounded
    face of the segment arrangement that lies inside C and touches C (the face's interior side of
    a shared edge is inside C).  This picks up loops attached to C at shared vertices."""
    # round 9: segments flagged construction (real 0) that a chooser contour uses as a boundary
    # are region boundaries (24 such segments; the dump calls them non-construction)
    extra = {x for C in contours for x in C}
    faces = [f for f in planar_faces(sk, extra=extra) if f[0] > 1e-14]
    out = set()
    for C in contours:
        Cs = set(C)
        ce, _ = _loop_geom(sk, C)
        if not ce:
            continue
        for a, fs, probes in faces:
            if any(sr in Cs and _inside(pt, ce) for sr, pt in probes):
                out |= set(fs)
    return out


def selected_serials(chs, regs, sk, chains_=None, faces=False):
    """segment serials bounding the selected regions (all segments when no chooser).
    A selected contour also selects the closed loops nested directly inside it."""
    if not chs:
        return set(s.serial for s in sk.lines + sk.arcs), False
    sel = set(x for c in chs for ct in c.contours for x in ct.serials)
    loops = []
    for c in list(chains_ or []) + computed_contours(sk):   # stored chains can omit loops
        L = sorted(c.serials)
        if c.closed == 1 and L not in loops:
            loops.append(L)
    for c in chs:
        for ct in c.contours:
            for L in nested_loops(sk, ct.serials, loops):
                sel |= set(L)
    if faces:
        sel |= face_expand(sk, [ct.serials for c in chs for ct in c.contours])
    return sel, True


# ------------------------------------------------------------------ end specs
CD_ES = b'\xff\xff\x01\x00\x0b\x00moEndSpec_c'
ES_MARK = re.compile(re.escape(b'\xff\xff\x00\x00\x03\xff\xff\xff\xff' + b'\x00' * 6 + b'\x80\xbf'))
DIMV = re.compile(rb'\xff\xfe\xff(.)((?:D\x00)(?:[0-9]\x00){1,3}).{0,24}?\xff\xfe\xff\x00\x00\x00(.{8})', re.S)
UPTO_ENDS = (3, 4, 5, 7)   # swEndCondUpToVertex/UpToSurface/OffsetFromSurface/UpToBody
ES_TAG_MAX = 0x3000       # round 13: tags above this are f64 high words (0xbf80 = -1.0)
ES_DIR0_BOTH = True
ES_TIE_FIRST = True
ES_TAG_MIN = 0x10
ES_CD_FIRST = True        # round 13: the classdef anchor wins over tag matches before it
ES_SPAN = 48              # fixed header bytes S..S+48 accounted for


@dataclass
class EndSpec:
    offset: int
    dir1: int
    reverse: int
    end1: int
    end2: int
    both: bool
    depth1: float = None
    depth2: float = None
    upto_ref: tuple = None    # (face owner feature id, stamp, serial, offset) for end 3/4/5/7


def endspec_tag(d, feats):
    c = Counter()
    for s, e in feats:
        for m in ES_MARK.finditer(d, s, e):
            for k in (44, 46):
                t = m.start() - k
                if u16(d, t) & 0x8000 and ES_TAG_MIN <= (u16(d, t) & 0x7fff) < ES_TAG_MAX and d[t + 2:t + 4] == b'\x00\x00':
                    c[u16(d, t)] += 1
    if c:
        return c.most_common(1)[0][0]
    # fallback: tag shape '<tag> 00 00 0[01] 00 00*6' present in most extrusion regions
    c, first = Counter(), {}
    for s, e in feats:
        seen = set()
        for m in re.finditer(rb'([\x00-\xff][\x80-\xfe])\x00\x00[\x00\x01]\x00\x00\x00\x00\x00\x00\x00', d[s:e]):
            a = s + m.start()
            if d[a + 18] <= 10 and d[a + 12] <= 1 and d[a + 22] <= 10 and ES_TAG_MIN <= (u16(d, a) & 0x7fff) < ES_TAG_MAX \
                    and u16(d, a) not in seen:
                first[u16(d, a)] = min(first.get(u16(d, a), 1 << 30), a - s)
                seen.add(u16(d, a))
        c.update(seen)
    if not c:
        return None
    # round 13: ties go to the tag met earliest in its region (the EndSpec precedes pattern data)
    if not ES_TIE_FIRST:
        return c.most_common(1)[0][0]
    return max(c, key=lambda t: (c[t], -first[t]))


def parse_endspec(d, s, e, tag, known_ids=None):
    cd = d.find(CD_ES, s, e)
    anc = []
    if cd >= 0:
        anc.append(cd + len(CD_ES) - 2)
    if tag is not None:
        pat = re.escape(struct.pack('<H', tag) + b'\x00\x00') + b'[\x00\x01]\x00'
        anc += [s + m.start() for m in re.finditer(pat, d[s:e])]
    anc = sorted(set(anc))
    if not anc:
        return None
    S = anc[0] if cd < 0 or not ES_CD_FIRST else cd + len(CD_ES) - 2
    es = EndSpec(S, u16(d, S + 4), d[S + 12], d[S + 18], d[S + 22], d[S + 22] != 0)
    if ES_DIR0_BOTH:
        # round 13: u16 S+4 is 1 for one direction, 0 for two (A/B BOSS 049-051, CUTEND 080);
        # end2 is stored (and reported by the API) even for single-direction features.
        es.both = es.dir1 == 0
    # depth by DimValue NAME: D1 = direction 1, D2 = direction 2 (a through-all
    # direction 1 has no D1, so order alone mislabels a lone D2)
    named = {}
    for m in DIMV.finditer(d, S, e):
        named.setdefault(m.group(2).decode('utf-16-le'), struct.unpack('<d', m.group(3))[0])
    es.depth1 = named.get('D1')
    if 'D2' in named and (es.both or 'D1' not in named):
        es.depth2 = named['D2']
        es.both = es.both or not ES_DIR0_BOTH        # direction 2 present (end2 0 = blind is a valid 2nd end)
    # up-to reference: first (fid, stamp, serial) entity ref after S.  Up to surface /
    # vertex / body: ~S+163 (S+159 older files); offset from surface: ~S+1900, after
    # the offset DimValue.  The face's owner feature is a parent of the extrusion.
    if es.end1 in UPTO_ENDS:
        m = None
        for m_ in FREF.finditer(d, S + 100, min(e, S + 2200)):
            if known_ids is None or u32(d, m_.start(1)) in known_ids:
                m = m_
                break
        if m:
            es.upto_ref = (u32(d, m.start(1)), u32(d, m.start(2)), u32(d, m.start(3)), m.start())
    return es


# ------------------------------------------------------------------ dims of a feature
def dim_number(raw8):
    """DimValue slot: f64 for length/angle parameters; integer parameters (pattern
    counts) store u32 count in the low half (the f64 reading is then tiny/huge)."""
    v = struct.unpack('<d', raw8)[0]
    if v != v or (v != 0 and not (1e-30 < abs(v) < 1e30)):
        return float(struct.unpack_from('<I', raw8)[0])
    return v


def feature_dims(d, s, e):
    """[(name, value, start, end)] DimValue records inside a feature region.
    A dimension is written several times (parameter, display copies); the API
    value is the LAST copy of each name in the feature's region (the first copy
    of a sketch dimension holds a text-position value)."""
    last = {}
    order = []
    for m in DIMV.finditer(d, s, e):
        n = m.group(2).decode('utf-16-le')
        if n not in last:
            order.append(n)
        last[n] = (dim_number(m.group(3)), m.start(), m.end())
    return [(n,) + last[n] for n in order]


# ------------------------------------------------------------------ face refs (patterns / mirrors / fillets)
FREF = re.compile(rb'[\x00-\xff][\x80-\xff]\x00\x00[\x00-\xff][\x80-\xff][\x00-\xff]{2}(.{4})(.{4})(.{4})', re.S)


def referenced_feature_ids(d, s, e, known_ids):
    """feature ids appearing in (fid, stamp, seq) entity references inside a region."""
    c = Counter()
    for m in FREF.finditer(d, s, e):
        f = u32(d, m.start(1))
        if f in known_ids:
            c[f] += 1
    return c


# ------------------------------------------------------------------ feature base block / entity refs

# ------------------------------------------------------------------ mirror plane
# round 12: the record's leading u32 is 68 42 00 00, 50 46 00 00 or 00 00 00 00 (A/B mirror parts,
# PRK, mhtsoc, shuffle_plate, vert2_*): accept all three and require a plausible stamp.
PLANE_REF = re.compile(rb'(?:\x68\x42|\x50\x46|\x00\x00)\x00\x00(.{4})(.{4})\x00\x00([\x00-\x0f])\x00', re.S)


def mirror_plane_ref(d, h, known_ids):
    """moMirrorPattern: the mirror plane is the LAST '68 42 00 00 | u32 plane fid |
    u32 stamp | u16 0 | u16 k' record of the feature region (region_end - 288 in
    every sample).  Returns (plane fid, stamp, k, offset) or None."""
    out = None
    for m in PLANE_REF.finditer(d, h.offset, h.region_end):
        if u32(d, m.start(1)) in known_ids and 1_400_000_000 < u32(d, m.start(2)) < 1_900_000_000:
            out = (u32(d, m.start(1)), u32(d, m.start(2)), m.group(3)[0], m.start())
    return out

BASE_MARK = re.compile(re.escape(b'\xff\xff\x00\x00\x03' + b'\xff' * 8 + b'\x00\x00\x80\xbf'))
BASE_TAIL = 46


def feature_base_span(d, h):
    """moFeature_c base block after the header: CString comment, u32 serial ...,
    the 17-byte marker FF FF 00 00 03 FF*8 00 00 80 BF at header.end+64/66, then
    46 bytes (u32 0 x3, u32 n, ..., i32 -1, u32 time_created, u32 time_modified,
    u16 2, u16 ?, u16 5, u16 1)."""
    m = BASE_MARK.search(d, h.end, min(h.region_end, h.end + 120))
    if not m:
        return None
    return (h.end, min(h.region_end, m.end() + BASE_TAIL))


ENT_REF = re.compile(rb'([\x00-\xff][\x80-\xff])\x00\x00([\x00-\xff][\x80-\xff])([\x00-\xff]{2})(.{4})(.{4})(.{4})', re.S)


@dataclass
class EntityRef:
    """(feature_id, stamp, seq) topological name used by every *IdRep_c / EdgeRef /
    FaceRef object: u16 cls | u16 0 | u16 cls2 | u16 doc | u32 fid | u32 stamp | u32 seq.
    (fid, stamp, seq) equals the Parasolid ATOM_ID_2001 [_, fid, stamp, 0, seq]."""
    offset: int
    feature_id: int
    stamp: int
    seq: int


def entity_refs(d, ids, s=0, e=None):
    e = len(d) if e is None else e
    return [EntityRef(m.start(), u32(d, m.start(4)), u32(d, m.start(5)), u32(d, m.start(6)))
            for m in ENT_REF.finditer(d, s, e) if u32(d, m.start(4)) in ids and u32(d, m.start(6)) < 100000]


# ------------------------------------------------------------------ whole stream
@dataclass
class Decoded:
    headers: list
    sketches: dict = field(default_factory=dict)      # feature_id -> dict
    endspecs: dict = field(default_factory=dict)      # feature_id -> EndSpec
    dims: dict = field(default_factory=dict)          # feature_id -> [(name, value)]
    spans: list = field(default_factory=list)


def decode(d, extrude_ids=None):
    """Decode a feature stream.  extrude_ids: ids of features whose end spec to read
    (all headers whose region holds an EndSpec when None)."""
    hs = feature_headers(d)
    first = {}
    for h in hs:
        first.setdefault(h.feature_id, h)
    out = Decoded(hs)
    tmap = tag_map(d)
    ctag = chain_tag_of(d)
    spans = []
    for h in hs:
        spans.append((h.offset, h.end))
        b = feature_base_span(d, h)
        if b:
            spans.append(b)
    spans += [(r.offset, r.offset + 20) for r in entity_refs(d, set(first))]
    for r in mfc.class_defs(d) + mfc.cstrings(d):
        spans.append((r.offset, r.end))
    sk_regions = []
    for fid, h in first.items():
        s, e = h.offset, h.region_end
        dims = feature_dims(d, s, e)
        out.dims[fid] = [(n, v) for n, v, _, _ in dims]
        spans += [(a, b) for _, _, a, b in dims]
        if d.find(b'\x1f\x00\x03', s, e) >= 0 and MARK.search(d, s, e):
            sk = parse_sketch(d, s, e)
            if not sk.points:
                continue
            rels = relations(d, s, e, sk, tmap)
            chs_ = chains(d, s, e, ctag)
            regs, choos = regions_and_choosers(d, s, e, fid)
            out.sketches[fid] = {'sketch': sk, 'relations': rels, 'chains': chs_, 'regions': regs,
                                 'choosers': choos}
            spans += sk.spans + [(r.offset, r.end) for r in rels] + [(c.offset, c.end) for c in chs_]
            for rg in regs + [ct for c in choos for ct in c.contours]:
                spans.append((rg.offset - 6, rg.offset + 24 * max(1, len(rg.edges))))
    feats = [(h.offset, h.region_end) for h in first.values()
             if extrude_ids is None or h.feature_id in extrude_ids]
    tag = endspec_tag(d, feats)
    for fid, h in first.items():
        if extrude_ids is not None and fid not in extrude_ids:
            continue
        es = parse_endspec(d, h.offset, h.region_end, tag, set(first))
        if es and (extrude_ids is not None or d.find(CD_ES, h.offset, h.region_end) >= 0 or tag):
            out.endspecs[fid] = es
            spans.append((es.offset, es.offset + ES_SPAN))
    out.spans = spans
    return out


def coverage(d, spans):
    spans = sorted((max(0, a), min(len(d), b)) for a, b in spans if b > a)
    cov, last = 0, 0
    for a, b in spans:
        if b > last:
            cov += b - max(a, last)
            last = b
    return 100.0 * cov / max(1, len(d))


def to_json(x):
    if hasattr(x, '__dataclass_fields__'):
        return {k: to_json(v) for k, v in asdict(x).items()}
    if isinstance(x, dict):
        return {str(k): to_json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [to_json(v) for v in x]
    return x

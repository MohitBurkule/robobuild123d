"""MFC CArchive object / class numbering for the feature stream (round 7).

CArchive keeps one map for classes and objects.  Index 0 is the null object.
    FF FF <schema u16> <len u16> <name>   new class: class gets index n, the object n+1
    0x8000 | c                            new object of the class with index c: object gets n
    u16 r (1 <= r < 0x7FFF)               back-reference to object / class r (no new index)
    7F FF <u32>                           big form of either (index >= 0x7FFF)
The feature stream continues an archive that was started elsewhere: its first
u32 is the running map count, so the first ClassDef gets that index.  Class
indices below it ("external" classes, e.g. 0x8004 = the class of the CString
holder in every feature header) are defined in an earlier stream.

Layouts of most classes are unknown, so tags are found by scanning, with
filters for false positives:
  * a tag must name a known class (or an external one followed by a plausible field);
  * not inside an IEEE double (any covering 8-byte window decodes to 1e-9..1e7);
  * not the low half of a timestamp u32 (high half 0x4000..0x72FF);
and with resynchronisation: if a tag v names no class but a class defined
nearby (|v - c| <= RESYNC_W) whose first object starts with the same bytes as
those following the tag, the class's true index is v; numbering is redone from
that ClassDef.  The count is exact wherever both the start value and every tag
between are right; resyncs repair it at the next class that is reused.
"""
import re
import struct
from bisect import bisect_right
from dataclasses import dataclass

from .mfc import CLASSDEF as CD

REF = re.compile(rb'(?=([\x01-\xff][\x80-\xff]))', re.S)
BIG = re.compile(rb'\xff\x7f(..)([\x00-\x7f]\x80)', re.S)  # 7FFF + u32 0x8000_0000|class
RESYNC_W = 1000
SIG = 4
MIN_DISTINCT = 3
MIN_VOTES = 2


def u16(d, o): return struct.unpack_from('<H', d, o)[0]


def in_float(d, o):
    for w in range(max(0, o - 6), o + 1):
        if w + 8 > len(d):
            break
        x = abs(struct.unpack_from('<d', d, w)[0])
        if 1e-9 < x < 1e7:
            return True
    return False


def is_stamp(d, o):
    return o + 4 <= len(d) and 0x40 <= d[o + 3] <= 0x72


def ext_ok(d, o):
    if o + 4 > len(d):
        return False
    h = d[o + 3]
    return h in (0x00, 0x01, 0xff) or 0x80 <= h <= 0x8f


@dataclass
class Ev:
    offset: int
    end: int
    index: int          # map index: class index for 'def' (object = index + 1), object index for 'new'
    cls: int            # class index
    name: str           # class name ('' for external classes)
    kind: str           # 'def' | 'new'

    @property
    def obj(self):
        return self.index + 1 if self.kind == 'def' else self.index


def _events(d):
    ev = []
    for m in CD.finditer(d):
        ln = m.group(2)[0]
        nm = m.group(3)[:ln]
        if len(nm) == ln:
            ev.append((m.start(), 0, ln, nm.decode()))
    for m in REF.finditer(d):
        ev.append((m.start(), 1, u16(d, m.start()) & 0x7fff, None))
    ev.sort()
    return ev


def number(d, fix=None, start=None, ev=None, reject=frozenset(), look=False):
    """One numbering pass. fix: {classdef offset: forced class index}."""
    fix = fix or {}
    start = struct.unpack_from('<I', d, 0)[0] if start is None else start
    ev = ev if ev is not None else _events(d)
    cnt, classes, i, out = start, {}, 0, []
    for o, k, a, nm in ev:
        if o < i or o in reject:
            continue
        if k == 0:
            if o in fix:
                cnt = fix[o]
            elif look:
                cnt = _lookahead(d, o + 6 + a, cnt, classes, start)
            classes[cnt] = nm
            out.append(Ev(o, o + 6 + a, cnt, cnt, nm, 'def'))
            cnt += 2
            i = o + 6 + a
            continue
        after_def = o == i and bool(out)
        if a in classes:
            ok = after_def or not (in_float(d, o) or is_stamp(d, o))
        elif 0 < a < start:
            ok = after_def or (ext_ok(d, o) and not in_float(d, o))
        else:
            ok = False
        if ok:
            out.append(Ev(o, o + 2, cnt, a, classes.get(a, ''), 'new'))
            cnt += 1
            i = o + 2
    return out


LOOK_W = 400
LOOK_K = 4


def _lookahead(d, e, pred, classes, start):
    """True index of the class whose first object starts at e: the value v of later tags
    0x8000|v that are followed by the same LOOK_K bytes, if they agree and differ from pred."""
    sig = d[e:e + LOOK_K]
    if len(sig) < LOOK_K or len(set(sig)) < MIN_DISTINCT:
        return pred
    from collections import Counter
    c = Counter()
    j = d.find(sig, e + 1)
    while j >= 0:
        v = struct.unpack_from('<H', d, j - 2)[0]
        if v & 0x8000:
            v &= 0x7fff
            if abs(v - pred) <= LOOK_W and v >= start and (v == pred or v not in classes):
                c[v] += 1
        j = d.find(sig, j + 1)
    if not c:
        return pred
    v, n = c.most_common(1)[0]
    if v != pred and n >= MIN_VOTES and n > 2 * c.get(pred, 0):
        return v
    return pred


def _sig(d, e):
    return d[e:e + SIG]


def outliers(d, out):
    """tags whose following u16 is unlike every other instance of the class (likely data, not a tag)"""
    from collections import Counter, defaultdict
    prof = defaultdict(Counter)
    first = {}
    for e in out:
        nx = d[e.end:e.end + 2]
        if e.kind == 'def':
            first[e.cls] = nx
        prof[e.cls][nx] += 1
    bad = set()
    for e in out:
        if e.kind != 'new':
            continue
        nx = d[e.end:e.end + 2]
        if len(nx) < 2 or nx == first.get(e.cls) or prof[e.cls][nx] > 1:
            continue
        if nx[1] in (0x00, 0x01, 0xff) or 0x80 <= nx[1] <= 0x8f:
            continue
        bad.add(e.offset)
    return bad


def numbering(d, max_fix=400, prune=True, look=False):
    """Numbering with resynchronisation. Returns (events, fixes)."""
    start = struct.unpack_from('<I', d, 0)[0]
    ev = _events(d)
    fix = {}
    reject = frozenset()
    if prune:
        for _ in range(3):
            r2 = reject | outliers(d, number(d, fix, start, ev, reject, look))
            if r2 == reject:
                break
            reject = frozenset(r2)
    for _ in range(max_fix):
        out = number(d, fix, start, ev, reject, look)
        defs = [e for e in out if e.kind == 'def']
        by_idx = {e.index: e for e in defs}
        sigs = {e.index: _sig(d, e.end) for e in defs}
        accepted = {e.offset for e in out}
        doffs = [e.offset for e in defs]
        bysig = {}
        for c, sg in sigs.items():
            bysig.setdefault(sg, []).append(c)
        ch = None
        votes = {}
        for o, k, a, _ in ev:
            if k != 1 or o in accepted or a < start or a in by_idx:
                continue
            if in_float(d, o) or is_stamp(d, o):
                continue
            nxt = d[o + 2:o + 2 + SIG]
            if len(set(nxt)) < MIN_DISTINCT:
                continue
            # a class defined before o, near index a, whose first object starts with the same bytes
            cands = [c for c in bysig.get(nxt, ()) if abs(c - a) <= RESYNC_W and by_idx[c].offset < o]
            if len(cands) == 1 and by_idx[cands[0]].offset not in fix:
                key = (by_idx[cands[0]].offset, a)
                votes.setdefault(key, []).append(o)
                if len(votes[key]) >= MIN_VOTES:
                    ch = key
                    break
        if ch is None:
            return out, fix
        fix[ch[0]] = ch[1]
    return number(d, fix, start, ev, reject, look), fix


def object_at(events, offset):
    """object index of the record that starts at/just before offset (feature header CString)."""
    offs = [e.offset for e in events]
    j = bisect_right(offs, offset) - 1
    while j >= 0 and events[j].kind == 'new' and events[j].end == offset and not events[j].name:
        j -= 1          # the external 0x8004-type holder object directly before the CString
    return events[j].obj if j >= 0 else None


# ------------------------------------------------------------------ feature objects and object refs
NON_SEED = ('Folder', 'moRefPlane_c', 'moProfileFeature_c', 'moOriginProfileFeature_c', 'moDetailCabinet_c',
            'moNotesAreaFtrFolder_c', 'moCommentsFolder_c', 'moFavoriteFolder_c', 'moHistoryFolder_c')


def feature_objects(d, headers, events):
    """feature id -> (header, object index, class name) for the first header of each feature."""
    offs = [e.offset for e in events]
    out = {}
    for h in headers:
        if h.feature_id in out:
            continue
        j = bisect_right(offs, h.offset) - 1
        while j >= 0 and events[j].kind == 'new' and events[j].end == h.offset and not events[j].name:
            j -= 1
        if j >= 0:
            out[h.feature_id] = (h, events[j].obj, events[j].name)
    return out


def list_class_tags(d):
    """the stream's object-list class: external class S-28 or S-29 (moFeatureList-like, 'T u16 n, n items')."""
    S = struct.unpack_from('<I', d, 0)[0]
    return [struct.pack('<H', 0x8000 | (S - k)) for k in (28, 29)]


def seed_list(d, h):
    """object back-references of the first object list in a pattern / mirror region (the seed features)."""
    best = None
    for t in list_class_tags(d):
        j = d.find(t, h.offset, h.region_end)
        while j >= 0:
            n = u16(d, j + 2)
            if 1 <= n <= 32 and j + 4 + 2 * n <= len(d):
                refs = list(struct.unpack_from('<%dH' % n, d, j + 4))
                if all(0 < r < 0x7fff for r in refs):
                    if best is None or j < best[0]:
                        best = (j, refs)
                    break
            j = d.find(t, j + 1, h.region_end)
    return best[1] if best else []


def resolve_objects(refs, fobj, before):
    """map object indices to the feature whose object index is nearest (numbering drifts by a few
    objects in large parts; feature objects are tens to hundreds of indices apart)."""
    cand = [(i, fid) for fid, (h, i, cls) in fobj.items()
            if h.offset < before and i is not None and not any(x in cls for x in NON_SEED)]
    out = []
    for r in refs:
        if not cand:
            out.append(None)
            continue
        i, fid = min(cand, key=lambda x: abs(x[0] - r))
        out.append((fid, r - i))
    return out


# ------------------------------------------------------------------ object tree
@dataclass
class Obj:
    index: int
    cls: int
    name: str           # class name, 'ext#<n>' for classes defined in an earlier stream
    start: int          # tag offset
    end: int            # next tag (objects are serialised depth-first, so a parent's own
                        # fields are the bytes up to its first child tag)
    parent: int = None  # index of the enclosing object (feature header object for top level)


def objects(d, events, headers=None):
    """Every numbered object with its class and byte span [start, next tag).  Objects are
    nested under the feature whose header precedes them (feature tree level)."""
    out = []
    hoffs = sorted(h.offset for h in (headers or []))
    S = struct.unpack_from('<I', d, 0)[0]
    for k, e in enumerate(events):
        end = events[k + 1].offset if k + 1 < len(events) else len(d)
        out.append(Obj(e.obj, e.cls, e.name or 'ext[S-%d]' % (S - e.cls), e.offset, end))
    if hoffs:
        owner, hi = None, 0
        for o in out:
            # the object whose span contains a feature header CString is that feature's object
            while hi < len(hoffs) and hoffs[hi] < o.start:
                hi += 1
            o.parent = owner
            if hi < len(hoffs) and o.start <= hoffs[hi] < o.end + 2:
                owner = o.index
                o.parent = None
    return out


def class_bytes(d, objs, explained=()):
    """per class: (total bytes, unexplained bytes) given explained spans [(a, b)]."""
    return _class_bytes(d, objs, explained)


def _class_bytes(d, objs, explained):
    mask = bytearray(len(d))
    for a, b in explained:
        a, b = max(0, a), min(len(d), b)
        if b > a:
            mask[a:b] = b'\x01' * (b - a)
    out = {}
    for o in objs:
        tot = o.end - o.start
        une = tot - mask[o.start:o.end].count(1)
        t = out.setdefault(o.name, [0, 0, 0])
        t[0] += tot
        t[1] += une
        t[2] += 1
    return out

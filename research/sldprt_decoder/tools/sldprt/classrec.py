"""Fixed-prefix layouts of frequent classes, located through the object numbering (objnum.py).

Every layout was inferred from column statistics over the training half (colstats.py) and is
accepted per instance only when its constant bytes are present.  Offsets are relative to the end
of the object's tag (ClassDef: end of the class name).

moFR_c          (feature / face reference)  H objref | I feature_id | I stamp | I serial      14 B
                objref = a sub-object of the referenced feature (feature object + 11 for extrusions)
sgPointHandle / sgLineHandle / sgArcHandle  H entity index | FF FF FF FF | 00 00 00 00     10 B
moPointBackedUpData_c                       d x | d y | 8 x 00  (pre-edit sketch point)       24 B
moBBoxCenterData_c                          I 1 | d cx | d cy | d cz | d size | I 0           40 B
moEdgeRef_c / moFaceRef_c                   01 00 00 00 00 00 00 00 | I kind | I flag          16 B
                                            (moFaceRef_c: 8 B constant only)
Round 8 (pair diffs fork 5 / fork 5 long and RV21 / RV21 oversize located the changed fields):
moFavoriteHandle_c  I 0 | I -1 | I 0 | d -1.0 | H 1 | H 1 | I flags | d value | d 0 | d value    52 B
                    value = the dimension's value in SI units (stored twice)
Parasolid body cache (not an MFC object): 16-byte hash | u32 raw size | u32 n | n bytes zlib
                    inflating to a Parasolid transmit file ('PS..TRANSMIT FILE') of raw size
"""
import struct
from dataclasses import dataclass

HANDLES = ('sgPointHandle', 'sgLineHandle', 'sgArcHandle')


@dataclass
class Rec:
    cls: str
    offset: int        # tag offset
    start: int         # first field byte
    end: int
    fields: dict


def ps_blobs(d):
    """Parasolid body snapshots embedded in the feature stream: [(start, end, raw size)], start at
    the 16-byte hash when the preceding u32 equals the inflated size."""
    import zlib
    from .objnum import zblobs
    out = []
    for a, b in zblobs(d):
        try:
            z = zlib.decompress(d[a + 4:b])
        except zlib.error:
            continue
        s = a
        if a >= 20 and struct.unpack_from('<I', d, a - 4)[0] == len(z):
            s = a - 20
        out.append((s, b, len(z) if z[:2] == b'PS' else -len(z)))
    return out


def decode(d, events, feature_ids=()):
    out = []
    fids = set(feature_ids)
    n = len(d)
    for e in events:
        o = e.end
        c = e.name
        if c == 'moFR_c' and o + 14 <= n:
            r, fid, st, k = struct.unpack_from('<HIII', d, o)
            if fid in fids and r < 0x7fff:
                out.append(Rec(c, e.offset, o, o + 14, {'objref': r, 'feature_id': fid, 'stamp': st, 'serial': k}))
        elif c in HANDLES and o + 10 <= n:
            if d[o + 2:o + 10] == b'\xff\xff\xff\xff\x00\x00\x00\x00':
                out.append(Rec(c, e.offset, o, o + 10, {'entity': struct.unpack_from('<H', d, o)[0]}))
        elif c == 'moPointBackedUpData_c' and o + 24 <= n:
            x, y = struct.unpack_from('<2d', d, o)
            if d[o + 16:o + 24] == b'\x00' * 8 and abs(x) < 10 and abs(y) < 10:
                out.append(Rec(c, e.offset, o, o + 24, {'x': x, 'y': y}))
        elif c == 'moBBoxCenterData_c' and o + 40 <= n:
            one, cx, cy, cz, sz, z = struct.unpack_from('<I4dI', d, o)
            if one == 1 and all(abs(v) < 10 for v in (cx, cy, cz, sz)):
                out.append(Rec(c, e.offset, o, o + 40, {'centre': (cx, cy, cz), 'size': sz}))
        elif c == 'moFavoriteHandle_c' and o + 52 <= n:
            if d[o + 4:o + 8] == b'\xff\xff\xff\xff' and d[o + 12:o + 24] == b'\x00\x00\x00\x00\x00\x00\xf0\xbf\x01\x00\x01\x00':
                v1, z0, v2 = struct.unpack_from('<3d', d, o + 28)
                if v1 == v2:
                    out.append(Rec(c, e.offset, o, o + 52, {'value': v1, 'flags': struct.unpack_from('<I', d, o + 24)[0]}))
        elif c in ('moEdgeRef_c', 'moFaceRef_c') and o + 16 <= n:
            if d[o:o + 8] == b'\x01\x00\x00\x00\x00\x00\x00\x00':
                ln = 16 if c == 'moEdgeRef_c' else 8
                f = {'kind': struct.unpack_from('<I', d, o + 8)[0]} if ln == 16 else {}
                out.append(Rec(c, e.offset, o, o + ln, f))
    return out


def spans(recs):
    # the tag itself is part of the record
    return [(r.offset, r.end) for r in recs]


# ------------------------------------------------------------------ round 8: whole-object templates
def _obj_spans(d, events):
    for k, e in enumerate(events):
        end = events[k + 1].offset if k + 1 < len(events) else len(d)
        yield e, e.end, end


def learn_templates(parts, min_n=20, min_share=0.5, const_share=0.98):
    """Learn whole-object layouts from training streams: parts = [(d, events)].
    For each class (by name, 'new' objects; external classes skipped) with >= min_n instances,
    the modal body length L (tag end to next tag) covering >= min_share of instances; the byte
    positions whose value is the same in >= const_share of the length-L instances are constant,
    the rest are variable slots (typed f64 where every training value at an 8-byte run is a
    finite double, else int)."""
    from collections import Counter, defaultdict
    bodies = defaultdict(list)
    for d, events in parts:
        for e, a, b in _obj_spans(d, events):
            if e.kind == 'new' and e.name and 0 < b - a <= 4096:
                bodies[e.name].append(d[a:b])
    out = {}
    for c, bs in bodies.items():
        if len(bs) < min_n:
            continue
        L, n = Counter(len(x) for x in bs).most_common(1)[0]
        if n < min_share * len(bs) or n < min_n:
            continue
        xs = [x for x in bs if len(x) == L]
        const = []
        for i in range(L):
            v, k = Counter(x[i] for x in xs).most_common(1)[0]
            const.append(v if k >= const_share * len(xs) else None)
        nconst = sum(v is not None for v in const)
        if nconst < 0.5 * L:          # mostly free bytes: no useful template
            continue
        out[c] = {'len': L, 'const': const, 'train_n': len(xs), 'share': round(n / len(bs), 3)}
    return out


def decode_templates(d, events, templates):
    """Objects whose body matches a learned template exactly on its constant bytes."""
    out = []
    for e, a, b in _obj_spans(d, events):
        t = templates.get(e.name) if e.kind == 'new' else None
        if t is None or b - a != t['len']:
            continue
        body = d[a:b]
        if all(v is None or body[i] == v for i, v in enumerate(t['const'])):
            out.append(Rec(e.name, e.offset, a, b, {'template': True}))
    return out


# ------------------------------------------------------------------ round 10: string-aware templates
# MFC CString (unicode form): FF FE FF <u8 n> then n UTF-16LE code units (n < 0xFF).
# Objects with name strings (moFavoriteHandle_c tails, ext classes) have one fixed byte
# layout per gap between strings; a template is keyed by (class, gap-length signature).
def class_key(e, S, ext_abs=False):
    if e.name:
        return e.name
    # round 13: external classes keep their ABSOLUTE class index across files
    # (A/B: S-105@S=109, S-106@110, S-108@112, S-99@103 are all class 4); S-k is not stable.
    return 'ext[C%d]' % e.cls if ext_abs else 'ext[S-%d]' % (S - e.cls)


def split_cstrings(body):
    """[(kind, start, end)] kind 'g' (gap bytes) | 's' (CString); strings validated as UTF-16."""
    out, i, g = [], 0, 0
    n = len(body)
    while i + 4 <= n:
        if body[i] == 0xFF and body[i + 1] == 0xFE and body[i + 2] == 0xFF:
            ln = body[i + 3]
            e = i + 4 + 2 * ln
            if ln < 0xFF and e <= n:
                try:
                    body[i + 4:e].decode('utf-16-le')
                    if i > g:
                        out.append(('g', g, i))
                    out.append(('s', i, e))
                    i = g = e
                    continue
                except UnicodeDecodeError:
                    pass
        i += 1
    if n > g:
        out.append(('g', g, n))
    return out


def _sig(body):
    parts = split_cstrings(body)
    sig = tuple(b - a if k == 'g' else -1 for k, a, b in parts)
    gaps = b''.join(body[a:b] for k, a, b in parts if k == 'g')
    return sig, gaps


def _bodies(d, events, ext_abs=False):
    import struct as _s
    S = _s.unpack_from('<I', d, 0)[0]
    for e, a, b in _obj_spans(d, events):
        if 0 < b - a <= 8192:
            yield class_key(e, S, ext_abs), e, a, b


def learn_templates2(parts, min_n=8, const_share=0.98, min_const=0.5, ext_abs=False):
    """Like learn_templates, but one template per (class, CString gap signature), for every
    signature with >= min_n training instances, 'def' (first) objects and external classes
    included.  Constant bytes are positions within the concatenated gap bytes."""
    from collections import Counter, defaultdict
    groups = defaultdict(list)
    for d, events in parts:
        for k, e, a, b in _bodies(d, events, ext_abs):
            sig, gaps = _sig(d[a:b])
            groups[(k, sig)].append(gaps)
    out = {}
    for (k, sig), xs in groups.items():
        if len(xs) < min_n or not xs[0]:
            continue
        L = len(xs[0])
        const = []
        for i in range(L):
            v, c = Counter(x[i] for x in xs).most_common(1)[0]
            const.append(v if c >= const_share * len(xs) else None)
        if sum(v is not None for v in const) < min_const * L:
            continue
        out.setdefault(k, {})[','.join(map(str, sig))] = {'const': const, 'train_n': len(xs)}
    return out


def decode_templates2(d, events, templates, ext_abs=False):
    out = []
    for k, e, a, b in _bodies(d, events, ext_abs):
        t = templates.get(k)
        if not t:
            continue
        sig, gaps = _sig(d[a:b])
        x = t.get(','.join(map(str, sig)))
        if x is None or len(x['const']) != len(gaps):
            continue
        if all(v is None or gaps[i] == v for i, v in enumerate(x['const'])):
            out.append(Rec(k, e.offset, a, b, {'template2': True, 'strings': sum(1 for s in sig if s < 0)}))
    return out

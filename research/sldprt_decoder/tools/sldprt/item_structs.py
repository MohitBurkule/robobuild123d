"""Round 11b: explicit struct readers for rare / external classes (see rare_classes.ksy).

No templates or column learning: every reader is a fixed field sequence with typed fields
and asserted constants; an instance is accepted only when every assertion holds, and a
whole external class is accepted only when >= 80 % of its instances in the file parse.

moFR_c (full)        H docref | I fid | I stamp | i32 path[k], k = (span-10)/4 <= 3
                     docref = back-ref to the moExtObject_c (document) object; this is how
                     DumpV3 GetPersistReference3 archives store it ('05 80 08 00 fid stamp seq').
                     path entries are seq or -1/0 (k=3 '[seq,-1,0]').
ext_hist_display     external class (S-97 in RV01, S-105 in RV23 ...), object after moCompFeature_c:
                     H ver=2 | u1[5] flags | I a | I b | u1[28] zero | i32[4] = -1 | u1[18] zero |
                     f32 58.0 | H 0 | [I feature_id | I stamp]  (optional, when present)
ext_named_item       external class (S-146 RV23, S-138 RV01, S-171 RV17 ...):
                     CString name | f64 kind (+-2.0) | i32 id (-1 or feature id) | I | CString | H | f64 value
moFavoriteHandle_c   52-byte head (classrec) + u1[12] 0 | f64 k (-25.0 typ.) | u1 1 | ... f64 diag @78/@110/@142 | I 1 | u1 kind |
                     u1[27] 0 | f64 1.0 | f64 0 | f64 1.0 | CString x4
"""
import struct

STAMP = (1_400_000_000, 1_900_000_000)


def cstring(d, i, end):
    """MFC CString 'FF FE FF <u8 n | FF u16 n> <n UTF-16LE units>' -> (text, next) or None."""
    if d[i:i + 3] != b'\xff\xfe\xff' or i + 4 > end:
        return None
    n, j = d[i + 3], i + 4
    if n == 0xff:
        if j + 2 > end:
            return None
        n, j = struct.unpack_from('<H', d, j)[0], j + 2
    if j + 2 * n > end:
        return None
    return d[j:j + 2 * n].decode('utf-16-le', 'replace'), j + 2 * n


def fr_full(d, a, b, fids):
    k4 = b - a - 10
    if k4 < 0 or k4 % 4 or k4 > 12:
        return None
    r, fid, st = struct.unpack_from('<HII', d, a)
    if fid not in fids or not STAMP[0] < st < STAMP[1]:
        return None
    path = list(struct.unpack_from('<%di' % (k4 // 4), d, a + 10))
    if any(not (-1 <= v < 1 << 20) for v in path):
        return None
    return b, {'docref': r, 'feature_id': fid, 'stamp': st, 'path': path}


def hist_display(d, a, b, fids):
    if b - a < 83 or struct.unpack_from('<H', d, a)[0] != 2:
        return None
    if d[a + 15:a + 43].strip(b'\x00') or d[a + 43:a + 59] != b'\xff' * 16 or d[a + 59:a + 77].strip(b'\x00'):
        return None
    if struct.unpack_from('<f', d, a + 77)[0] != 58.0 or d[a + 81:a + 83] != b'\x00\x00':
        return None
    f = {'flags': d[a + 2:a + 7].hex(), 'a': struct.unpack_from('<I', d, a + 7)[0], 'b': struct.unpack_from('<I', d, a + 11)[0]}
    e = a + 83
    if b - a >= 91:
        fid, st = struct.unpack_from('<II', d, a + 83)
        if fid in fids and STAMP[0] < st < STAMP[1]:
            f.update(feature_id=fid, stamp=st)
            e = a + 91
    return e, f


def named_item(d, a, b, fids):
    c = cstring(d, a, b)
    if not c:
        return None
    name, j = c
    if j + 16 > b or struct.unpack_from('<d', d, j)[0] not in (2.0, -2.0):
        return None
    ident, u = struct.unpack_from('<iI', d, j + 8)
    if ident < -1:
        return None
    c2 = cstring(d, j + 16, b)
    if not c2:
        return None
    s2, k = c2
    if k + 10 > b or d[k:k + 2] != b'\x00\x00':
        return None
    v = struct.unpack_from('<d', d, k + 2)[0]
    if v == 0 or 1e-12 < abs(v) < 1e6:           # dimension-like items carry a value here
        return k + 10, {'name': name, 'kind': struct.unpack_from('<d', d, j)[0], 'id': ident, 'u': u, 'text': s2, 'value': v}
    return k + 2, {'name': name, 'kind': struct.unpack_from('<d', d, j)[0], 'id': ident, 'u': u, 'text': s2}


def favorite_full(d, a, b, fids):
    """moFavoriteHandle_c from the tag end; the 52-byte head is checked like classrec."""
    if b - a < 222 or d[a + 4:a + 8] != b'\xff' * 4:
        return None
    if d[a + 12:a + 24] != b'\x00\x00\x00\x00\x00\x00\xf0\xbf\x01\x00\x01\x00':
        return None
    g = lambda o: struct.unpack_from('<d', d, a + o)[0]
    if d[a + 52:a + 64].strip(b'\x00') or d[a + 72] != 1 or struct.unpack_from('<I', d, a + 150)[0] != 1:
        return None
    m = [g(78), g(110), g(142)]   # diagonal of the stored orientation (1.0 typ.)
    if any(x != x or abs(x) > 1e6 for x in m) or d[a + 155:a + 182].strip(b'\x00') or g(182) != 1.0 or g(198) != 1.0:
        return None
    j, ss = a + 206, []
    for _ in range(4):
        c = cstring(d, j, b)
        if not c:
            return None
        ss.append(c[0]); j = c[1]
    return j, {'value': g(28), 'k': g(64), 'xform': m, 'kind': d[a + 154], 'strings': ss}


EXT_READERS = (('ext_hist_display', hist_display), ('ext_named_item', named_item))


def decode(d, spans, fids):
    """spans: [(ev, start, end)] from classrec._obj_spans.  Returns [(cls, tag_offset, end, fields)]."""
    out = []
    ext = {}
    for e, a, b in spans:
        if e.kind != 'new':
            continue
        if e.name == 'moFR_c':
            r = fr_full(d, a, b, fids)
            if r:
                out.append(('moFR_c', e.offset, r[0], r[1]))
        elif e.name == 'moFavoriteHandle_c':
            r = favorite_full(d, a, b, fids)
            if r:
                out.append(('moFavoriteHandle_c', e.offset, r[0], r[1]))
        elif not e.name:
            ext.setdefault(e.cls, []).append((e, a, b))
    for cls, objs in ext.items():
        for nm, fn in EXT_READERS:
            got = [(e, fn(d, a, b, fids)) for e, a, b in objs]
            ok = [(e, r) for e, r in got if r]
            if len(ok) >= 3 and len(ok) >= 0.8 * len(objs):
                out += [(nm, e.offset, r[0], dict(r[1], ext_class=cls)) for e, r in ok]
                break
    return out


def spans(recs):
    return [(o, e) for _, o, e, _ in recs]

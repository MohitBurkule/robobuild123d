"""Per-class column statistics over every instance in every part (cross-file layout inference).

Instances of one class are aligned at their tag (or ClassDef end) and each byte column of the
first `width` bytes is classified; runs of columns are then typed:
  const      one value in >= 95 % of instances
  f64        8-byte window decoding to |x| in 1e-9..1e7 (or 0) in >= 80 % of instances
  objref     u16 < running count (back-reference) in >= 80 %, varying
  tag        u16 with bit 15 set (child object of a known class) in >= 80 %
  u32/u16    small varying integers
  var        anything else
"""
import struct
from collections import Counter, defaultdict


def gather(streams, width=48):
    """streams: iterable of (name, data, events). Returns {class: [bytes...]} (instance bodies)."""
    from . import objnum as ON
    out = defaultdict(list)
    for nm, d, ev in streams:
        S = struct.unpack_from('<I', d, 0)[0]
        for k, e in enumerate(ev):
            body = d[e.end:e.end + width]
            key = e.name or 'ext[S-%d]' % (S - e.cls)
            out[key].append(body)
    return out


def columns(bodies, width=48):
    n = len(bodies)
    cols = []
    for i in range(width):
        c = Counter(b[i] for b in bodies if len(b) > i)
        v, k = c.most_common(1)[0] if c else (None, 0)
        cols.append((v, k / max(1, n)))
    return cols


def fields(bodies, width=48):
    n = len(bodies)
    cols = columns(bodies, width)
    out, i = [], 0
    while i < width:
        def frac(f):
            return sum(1 for b in bodies if len(b) >= i + 8 and f(b)) / max(1, n)
        if cols[i][1] >= 0.95:
            j = i
            while j < width and cols[j][1] >= 0.95:
                j += 1
            out.append((i, j - i, 'const', bytes(cols[x][0] for x in range(i, j)).hex()))
            i = j
            continue
        if frac(lambda b: (lambda x: x == 0 or 1e-9 < abs(x) < 1e7)(struct.unpack_from('<d', b, i)[0])) >= 0.8 \
                and frac(lambda b: struct.unpack_from('<d', b, i)[0] != 0) >= 0.2:
            out.append((i, 8, 'f64', ''))
            i += 8
            continue
        if frac(lambda b: b[i + 1] & 0x80 and b[i + 1] < 0x90) >= 0.8:
            out.append((i, 2, 'tag', ''))
            i += 2
            continue
        if frac(lambda b: struct.unpack_from('<I', b, i)[0] < 100000) >= 0.9:
            out.append((i, 4, 'u32', ''))
            i += 4
            continue
        if frac(lambda b: 0 < struct.unpack_from('<H', b, i)[0] < 0x7fff) >= 0.8:
            out.append((i, 2, 'objref/u16', ''))
            i += 2
            continue
        out.append((i, 1, 'var', ''))
        i += 1
    # merge adjacent var bytes
    m = []
    for f in out:
        if m and f[2] == 'var' and m[-1][2] == 'var':
            m[-1] = (m[-1][0], m[-1][1] + 1, 'var', '')
        else:
            m.append(f)
    return m

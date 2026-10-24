import struct, collections
from sldprt import objnum as ON
_orig = ON._numbering7
K = 2
def _n7(d, *a, **k):
    out, fix = _orig(d, *a, **k)
    S = struct.unpack_from('<I', d, 0)[0]
    c = collections.Counter(e.cls for e in out if e.kind == 'new' and e.cls < S)
    bad = {e.offset for e in out if e.kind == 'new' and e.cls < S and c[e.cls] <= K and not ON._ext_id(d, e.offset)}

    if not bad: return out, fix
    rej = _n7.reject | bad
    out = ON.number(d, fix, S, ON._events(d), rej)
    _n7.reject = rej
    return out, fix
ON._numbering7 = _n7
_n7.reject = None

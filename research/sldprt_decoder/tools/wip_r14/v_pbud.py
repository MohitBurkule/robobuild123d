"""Round 14: an outlier-rejected moPointBackedUpData_c tag is real when its x and y doubles also occur elsewhere in the stream."""
import struct
from sldprt import objnum as ON
_n = ON.number
def number(d, fix=None, start=None, ev=None, reject=frozenset(), look=False):
    if reject:
        S = struct.unpack_from('<I', d, 0)[0]
        ev0 = ev if ev is not None else ON._events(d)
        cls = {}
        for o, k, a, nm in ev0:
            if k == 0 and nm == 'moPointBackedUpData_c': cls = o; break
        keep = set()
        for o in reject:
            if o + 20 <= len(d) and ON._pbud(d, o):
                x, y = d[o + 2:o + 10], d[o + 10:o + 18]
                if (x == b'\0' * 8 or d.count(x) >= 2) and (y == b'\0' * 8 or d.count(y) >= 2) and x + y != b'\0' * 16:
                    keep.add(o)
        if keep: reject = frozenset(reject - keep)
    return _n(d, fix, start, ev, reject, look)
ON.number = number

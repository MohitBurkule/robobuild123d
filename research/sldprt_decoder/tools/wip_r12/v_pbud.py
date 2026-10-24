import struct
from sldprt import objnum as ON
def _f(x): return x == 0.0 or 1e-9 < abs(x) < 1e4
def pbud_ok(d, o):
    if o + 20 > len(d): return False
    x, y = struct.unpack_from('<dd', d, o + 2)
    return _f(x) and _f(y) and d[o + 18:o + 20] == b'\0\0'
old = ON._idrep_ok
def _idrep_ok(d, o, classes, cnt):
    if classes.get(ON.u16(d, o) & 0x7fff, '') == 'moPointBackedUpData_c':
        return pbud_ok(d, o)
    return old(d, o, classes, cnt)
ON._idrep_ok = _idrep_ok

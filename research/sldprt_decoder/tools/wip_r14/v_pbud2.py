"""Round 14: outlier filter never rejects a moPointBackedUpData_c tag whose struct holds (+ optional ExtensionLineIndicator)."""
import os
from sldprt import objnum as ON
_o = ON.outliers
EXT = os.environ.get('EXTLI') == '1'
def outliers(d, out):
    bad = _o(d, out)
    keep = {e.offset for e in out if e.kind == 'new' and ((e.name == 'moPointBackedUpData_c' and ON._pbud(d, e.offset))
                                                           or (EXT and e.name == 'moExtensionLineIndicator_c' and d[e.offset + 4:e.offset + 6] == b'\0\0'))}
    return bad - keep
ON.outliers = outliers

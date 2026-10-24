"""moEndSpec_c record layout (round 3, empirical, diffed across extrusions).
Anchor S = offset of b'\\x2d\\x82\\x00\\x00' inside a feature region.
  S+4   u8  dir2 flag (0 => block belongs to direction-2, layout shifted -2)
  S+18  u8  end-condition code (observed 0 blind,1,2,4,5,9; meaning partly inferred)
  S+26  'd5 81' => dimensioned blind form A; '37 82' at S+104 => form B (offset/up-to);
        'd4 82 d6 82' at S+33 => form C (up-to reference, ref id u8 at S+46)
  S+733 f64 depth [m] (form A; S+731 for dir2); form B offset at S+815..819
"""
import re, struct
from dataclasses import dataclass, asdict
ANCH = re.compile(re.escape(b'\x2d\x82\x00\x00'))
@dataclass
class EndSpec:
    offset: int; form: str; end_code: int; dir2: bool; depth_m: float | None; ref: int | None
    def json(self): return asdict(self)
def _f(d, k):
    try:
        v = struct.unpack_from('<d', d, k)[0]
        return v if 1e-6 < abs(v) < 10 else None
    except struct.error: return None
def parse_endspec(d, s):
    b = d[s:s+120]
    if len(b) < 120: return None
    dir2 = b[4] == 0
    if b[33:37] == b'\xd4\x82\xd6\x82':
        return EndSpec(s, 'C_upto_ref', b[18], dir2, None, b[46])
    if b[104:106] == b'\x37\x82':
        dep = next((v for k in (819, 815) if (v := _f(d, s+k))), None)
        return EndSpec(s, 'B_offset_or_through', b[18], dir2, dep, None)
    if b'\xd5\x81' in b[26:30] or MARK.match(b, 44) or MARK.match(b, 46):
        return EndSpec(s, 'A_blind', b[18], dir2, _f(d, s + (731 if dir2 else 733)), None)
    return EndSpec(s, 'unknown', b[18], dir2, None, None)
MARK = re.compile(re.escape(b'\xff\xff\x00\x00\x03\xff\xff\xff\xff' + b'\x00' * 6 + b'\x80\xbf'))
def endspecs(d, start, end):
    # anchor = class-ref (2d 82 in RV17; index differs per file) or ENDSPEC marker - 44
    c = {m.start() for m in ANCH.finditer(d, start, end)}
    c |= {m.start() - 44 for m in MARK.finditer(d, start, end) if m.start() >= 44}
    out = [x for s in sorted(c) if (x := parse_endspec(d, s))]
    return [x for x in out if x.form != 'unknown']
SPAN = 741  # bytes of an EndSpec record accounted for by this layout (S..S+741)

def num(v):
    m = re.fullmatch(r'\s*R?\s*(-?[0-9.]+)\s*(mm)?\s*', str(v))
    return float(m.group(1)) if m else None

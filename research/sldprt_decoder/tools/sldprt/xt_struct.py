"""Sequential, layout-driven reader for Parasolid neutral-binary transmit files.

File = text header (PS\\0\\0 ... 'SCH_<version>') | u16 0x00E7? | node records.
A node record = u16 type [schema-delta block on first occurrence] index:u16 fields.

Schema delta (first occurrence of a type whose fields differ from the base
schema SCH_xxxx_13006): 0xFF? no - the delta starts with u8 n_base_fields then
ops until 'Z':
    'C'                      copy next base field
    'D'                      delete next base field
    'I'/'A' u8 len name      insert / append a field, followed by
            u16 ftype u16 n  (ftype 0 = scalar: + u8 ? + u8 typechar)
A lone 0xFF after the type means "first occurrence, no field changes".

We do not have the base schema file, so base field lists come from LAYOUTS
below (XT Format Reference order, confirmed against bytes).  Field codes:
    p u16 pointer index    i u32 int   d f64   v 3xf64   c u8 char
    n u32 count of the trailing variable field (then var code repeated n)
Unknown node types stop the sequential walk; the parser then resyncs at the
next offset where a known record parses with an unseen index, and reports the
skipped span as a gap.  Coverage = parsed bytes / node-area bytes.
"""
import struct
from dataclasses import dataclass, field

# type: (name, fixed field codes after index, variable element code or None)
LAYOUTS = {
    13: ('SHELL', 'ipppppppp', None),
    19: ('REGION', 'ipppppccp', None),        # post-delta layout as observed (frame/owner inserted by v36 delta)
    14: ('FACE', 'ipdpppppcppppp', None),
    15: ('LOOP', 'ipppp', None),
    16: ('EDGE', 'ipdppppppp', None),
    17: ('FIN', 'pppppppppc', None),
    18: ('VERTEX', 'ipppppdp', None),
    29: ('POINT', 'ippppv', None),
    30: ('LINE', 'ipppppcvv', None),
    31: ('CIRCLE', 'ipppppcvvvd', None),
    32: ('ELLIPSE', 'ipppppcvvvdd', None),
    50: ('PLANE', 'ipppppcvvv', None),
    51: ('CYLINDER', 'ipppppcvvdv', None),
    52: ('CONE', 'ipppppcvvdddv', None),
    53: ('SPHERE', 'ipppppcvdvv', None),
    54: ('TORUS', 'ipppppcvvddv', None),
    56: ('BLENDED_EDGE', 'ipppppccpppddddpppp', None),
    60: ('OFFSET_SURF', 'ipppppcccpdd', None),
    124: ('B_SURFACE', 'ipppppcpp', None),
    126: ('NURBS_SURF', 'ccppiicciiccccpppppp', None),
    79: ('ATTRIB_DEF_ID', '', 'c'),
    81: ('ATTRIBUTE', 'ipppppp', 'p'),         # node_id, definition, owner, next, previous, next_in_class?, prev_in_class?, fields[n]
    82: ('INT_VALUES', '', 'i'),
    83: ('REAL_VALUES', '', 'd'),
    84: ('CHAR_VALUES', '', 'c'),
    45: ('BSPLINE_VERTICES', '', 'd'),
    80: ('ATTRIB_DEF', 'ppi' + 'c' * 27, 'c'),   # next, identifier, type_id, 27 bytes actions[8]+legal_owners[..] (split unverified), field types[n]
    127: ('KNOT_MULT', '', 'p'),     # count + u16 multiplicities
    133: ('TRIMMED_CURVE', 'ipppppcpvvdd', None),
    134: ('B_CURVE', 'ipppppcpp', None),
    135: ('CURVE_DATA', 'cp', None),
    136: ('NURBS_CURVE', 'pipicccccppp', None),
    137: ('SP_CURVE', 'ipppppcpppd', None),
    141: ('GEOMETRIC_OWNER', 'pppp', None),
    128: ('KNOT_SET', '', 'd'),
}
SIZE = {'p': 2, 'i': 4, 'd': 8, 'v': 24, 'c': 1}
MAXVAR = {79: 1024, 82: 4096, 83: 4096, 84: 4096, 81: 64, 80: 64, 127: 4096, 128: 4096, 45: 60000}
KNOWN_NEXT = set(LAYOUTS) | {1, 2, 3, 12, 38, 40, 60, 67, 68, 74, 70, 101, 124, 125, 126, 130, 56, 59}
VARIABLE = {t for t, (_, _, v) in LAYOUTS.items() if v}


@dataclass
class Node:
    type: int
    name: str
    offset: int
    end: int
    index: int
    fields: list = field(default_factory=list)
    var: list = field(default_factory=list)


def _read(d, i, code):
    if code == 'p':
        return struct.unpack_from('>H', d, i)[0], i + 2
    if code == 'i':
        return struct.unpack_from('>i', d, i)[0], i + 4
    if code == 'd':
        return struct.unpack_from('>d', d, i)[0], i + 8
    if code == 'v':
        return list(struct.unpack_from('>3d', d, i)), i + 24
    if code == 'c':
        return d[i], i + 1
    raise ValueError(code)


def parse_delta(d, i):
    """Parse a schema-delta block starting at d[i] (u8 count, ops..., 'Z').
    Returns (ops, end)."""
    n = d[i]
    i += 1
    ops = []
    while i < len(d):
        op = chr(d[i])
        i += 1
        if op in 'CD':
            ops.append((op,))
        elif op in 'IA':
            ln = d[i]
            name = d[i + 1:i + 1 + ln].decode('latin1')
            i += 1 + ln
            ft, cnt = struct.unpack_from('>HH', d, i)
            i += 4
            extra = None
            if ft == 0:
                extra = chr(d[i + 1])
                i += 2
            ops.append((op, name, ft, cnt, extra))
        elif op == 'Z':
            return {'n_base': n, 'ops': ops}, i
        else:
            raise ValueError('bad delta op %r at %d' % (op, i - 1))
    raise ValueError('unterminated delta')


SCALAR = {'d': 'd', 'i': 'i', 'c': 'c', 'l': 'c', 'u': 'c', 'v': 'v', 'n': 'i', 'h': 'v', 'b': 'd'}


def apply_delta(fixed, delta):
    out, k = [], 0
    for op in delta['ops']:
        if op[0] == 'C':
            if k < len(fixed):
                out.append(fixed[k])
            k += 1
        elif op[0] == 'D':
            k += 1
        else:
            _, name, ft, cnt, extra = op
            code = SCALAR.get(extra, 'c') if ft == 0 else 'p'
            out.append(code * max(1, cnt))
    out.append(fixed[k:])
    return ''.join(out)


POST_DELTA = {19: 'ipppppccp'}   # types whose base layout is unknown; observed post-delta layout
DELTAS = {}   # per-stream: type -> modified fixed layout (filled during walk)


def parse_record(d, i, layouts=LAYOUTS, deltas=None):
    t = struct.unpack_from('>H', d, i)[0]
    if t not in layouts:
        return None
    name, fixed, varc = layouts[t]
    j = i + 2
    delta = None
    if d[j] == 0xFF:
        j += 1
    elif d[j + 1:j + 2] in (b'C', b'D', b'I', b'A', b'Z') and d[j] < 64:
        try:
            delta, j = parse_delta(d, j)
        except (ValueError, IndexError, struct.error):
            return None
        # LAYOUTS already hold the layout *as observed* in SW2023 files (i.e. after
        # the embedded delta); the delta is parsed so its bytes are accounted for.
        if deltas is not None:
            deltas[t] = delta
    n = 0
    if varc:
        n = struct.unpack_from('>I', d, j)[0]
        if n > MAXVAR.get(t, 100000):
            return None
        j += 4
    idx, j = _read(d, j, 'p')
    vals = []
    for c in fixed:
        v, j = _read(d, j, c)
        vals.append(v)
    var = []
    for _ in range(n):
        v, j = _read(d, j, varc)
        var.append(v)
    if j > len(d):
        return None
    node = Node(t, name, i, j, idx, vals, var)
    node.delta = delta
    return node


NULL_DOUBLE = -31415800000000.0   # bytes c2bc928f996e0000 = XT 'null' real


def _plausible(node, seen):
    if node.index in seen or node.index < 2:
        return False
    for v in node.fields + node.var:
        if isinstance(v, float) and abs(v - NULL_DOUBLE) < 1e9:
            continue
        if isinstance(v, float) and (v != v or abs(v) > 1e6):
            return False
        if isinstance(v, list) and any(x != x or abs(x) > 1e6 for x in v):
            return False
    if node.name in ('FACE', 'FIN', 'LINE', 'CIRCLE', 'PLANE', 'CYLINDER', 'CONE'):
        sc = [v for v in node.fields if isinstance(v, int) and not isinstance(v, bool)]
        if node.name in ('FIN', 'FACE') and chr(node.fields[-1 if node.name == 'FIN' else 8]) not in '+-':
            return False
        if node.name in ('LINE', 'CIRCLE', 'PLANE', 'CYLINDER', 'CONE') and chr(node.fields[6]) not in '+-':
            return False
    return True


def walk(d, start=None):
    """Sequential walk.  Returns (nodes, gaps, coverage_pct, unknown_type_histogram)."""
    if start is None:
        k = d.find(b'SCH_')
        start = k + d[k - 1] if k > 0 else 0   # SCH string is length-prefixed (u8)
    nodes, gaps, seen = [], [], set()
    deltas = {}
    unknown = {}
    i = start
    gap_start = None
    while i < len(d) - 4:
        rec = None
        try:
            rec = parse_record(d, i, LAYOUTS, deltas)
        except (struct.error, ValueError, IndexError):
            rec = None
        if rec and _plausible(rec, seen) and (rec.end >= len(d) - 2 or
                                              struct.unpack_from('>H', d, rec.end)[0] in KNOWN_NEXT):
            if gap_start is not None:
                gaps.append((gap_start, i))
                t = struct.unpack_from('>H', d, gap_start)[0]
                unknown[t] = unknown.get(t, 0) + 1
                gap_start = None
            nodes.append(rec)
            seen.add(rec.index)
            i = rec.end
        else:
            if gap_start is None:
                gap_start = i
            i += 1
    if gap_start is not None:
        gaps.append((gap_start, len(d)))
    total = len(d) - start
    cov = 100.0 * sum(n.end - n.offset for n in nodes) / max(1, total)
    return nodes, gaps, round(cov, 2), unknown

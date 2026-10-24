"""Heuristic reader for Parasolid neutral-binary partition transmit files (v36).

Not a full schema-driven parser.  Records are located by pattern and the
field layouts below were inferred empirically, then cross-checked against the
public XT Format Reference node codes and field order:

  common prefix : <type:u16> [0xFF on first occurrence of a type]
  variable nodes: <count:u32> <index:u16> payload        (79,80,81,82,83,84)
  ATTRIB_DEF_ID 79 : count=len, index, ascii[len]
  ATTRIBUTE 81     : count=n_fields, index, node_id:u32, definition, owner,
                     next, previous, next_in_group?, prev_in_group?, fields[n]
  INT_VALUES 82    : count, index, i32[count]
  REAL_VALUES 83   : count, index, f64[count]
  CHAR_VALUES 84   : count, index, bytes[count]
  FACE 14          : index, node_id:u32, attributes, tolerance:f64, next,
                     previous, loop, shell, surface, sense:'+'/'-', ...
  SURFACE 50..54   : index, node_id:u32, attributes, owner, next, previous,
                     geometric_owner, sense, then geometry doubles (BE f64)
Pointers are u16 indices; 0 and 1 both behave as null.  An ATTRIB_DEF with
index N is immediately followed by its ATTRIB_DEF_ID (index N+1).
Indices > 0xFFFF have not been observed; files with more nodes would break.
"""
import re
import struct
import math

SURF_TYPES = {50: 'plane', 51: 'cylinder', 52: 'cone', 53: 'sphere', 54: 'torus',
              56: 'blended_edge', 60: 'offset', 67: 'swept', 68: 'spun', 124: 'b_surface'}
NDOUBLES = {50: 9, 51: 10, 52: 12, 53: 10, 54: 11}


def _u16(b, i):
    return struct.unpack_from('>H', b, i)[0]


def _ptr(v):
    return None if v in (0, 1) else v


def _unit(v, tol=1e-6):
    return abs(math.sqrt(sum(x * x for x in v)) - 1) < tol


# per-entity id attributes with int field [class, fid, stamp, 0, seq, ...]
ENTITY_ID_ATTRS = ('FACE_ID_2001', 'ATOM_ID_2001')


class XT:
    def __init__(self, data):
        self.d = data
        m = re.search(rb'modeller version (\d+)', data[:200])
        self.version = m.group(1).decode() if m else None
        m = re.search(rb'SCH_[0-9_]+', data[:300])
        self.schema = m.group(0).decode() if m else None
        self._values()
        self._names()
        self._attributes()
        self._surfaces()
        self._faces()

    # value nodes ----------------------------------------------------------
    def _values(self):
        self.values = {}
        d = self.d
        for t, sz, fmt in ((0x52, 4, 'i'), (0x53, 8, 'd'), (0x54, 1, None)):
            for m in re.finditer(struct.pack('>H', t) + rb'\xff?\x00\x00(..)(..)', d, re.S):
                n = _u16(m.group(1), 0)
                idx = _u16(m.group(2), 0)
                b = d[m.end():m.end() + n * sz]
                if len(b) != n * sz or idx in self.values:
                    continue
                self.values[idx] = b.decode('latin1') if fmt is None else list(struct.unpack('>%d%s' % (n, fmt), b))

    def _names(self):
        """ATTRIB_DEF (80): count:u32, index, next, identifier -> ATTRIB_DEF_ID (79).

        Round 11b: names are resolved through the def's identifier pointer.  The
        old rule "ID at index N+1 names def N" is off by one def in every file
        (it labelled FACE_ID_2001 values as ATOM_ID_2001 in some files and as
        ENT_TIME_STAMP_2001 in others; density came out as a feature id)."""
        ids = {}
        for m in re.finditer(rb'\x00O\xff?\x00\x00\x00(.)(..)', self.d, re.S):
            n = m.group(1)[0]
            s = self.d[m.end():m.end() + n]
            if s and all(32 <= c < 127 for c in s):
                ids[_u16(m.group(2), 0)] = s.decode()
        self.attdef_name = {}
        for m in re.finditer(rb'\x00P\xff?\x00\x00\x00[\x00-\x10](..)(..)(..)', self.d, re.S):
            idx, ident = _u16(m.group(1), 0), _u16(m.group(3), 0)
            if ident in ids and idx not in self.attdef_name:
                self.attdef_name[idx] = ids[ident]
        if not self.attdef_name:  # fallback: legacy adjacency rule
            self.attdef_name = {k - 1: v for k, v in ids.items()}

    def _attributes(self):
        self.attrs_by_owner = {}
        self.attributes = []
        for m in re.finditer(rb'\x00Q\xff?\x00\x00\x00([\x01-\x10])', self.d):
            i, n = m.end(), m.group(1)[0]
            if i + 18 + 2 * n > len(self.d):
                continue
            idx, nid, dfn, owner, nxt, prv, a, b = struct.unpack_from('>HIHHHHHH', self.d, i)
            name = self.attdef_name.get(dfn)
            if not name:
                continue
            fields = struct.unpack_from('>%dH' % n, self.d, i + 18)
            vals = [self.values.get(f) if _ptr(f) else None for f in fields]
            rec = {'index': idx, 'name': name, 'owner': owner, 'values': vals}
            self.attributes.append(rec)
            self.attrs_by_owner.setdefault(owner, []).append(rec)

    # geometry --------------------------------------------------------------
    def _surfaces(self):
        self.surfaces = {}
        types = bytes(SURF_TYPES)
        pat = rb'\x00([' + re.escape(types) + rb'])\xff?(..)(....)(..)(..)(..)(..)(..)([+-])'
        for m in re.finditer(pat, self.d, re.S):
            t = m.group(1)[0]
            idx = _u16(m.group(2), 0)
            rec = {'index': idx, 'type': SURF_TYPES[t], 'sense': m.group(9).decode()}
            if t in NDOUBLES:
                n = NDOUBLES[t]
                if m.end() + 8 * n > len(self.d):
                    continue
                v = struct.unpack_from('>%dd' % n, self.d, m.end())
                if not self._valid(t, v):
                    continue
                rec.update(self._geom(t, v))
            else:
                rec['raw_ptrs'] = [_u16(m.group(k), 0) for k in range(4, 9)]
            if idx not in self.surfaces or 'params' not in self.surfaces[idx]:
                self.surfaces[idx] = rec

    @staticmethod
    def _valid(t, v):
        if any(math.isnan(x) or abs(x) > 1e3 for x in v):
            return False
        if t == 50:
            return _unit(v[3:6]) and _unit(v[6:9])
        if t == 51:
            return _unit(v[3:6]) and v[6] > 0 and _unit(v[7:10])
        if t == 52:
            return _unit(v[3:6]) and _unit(v[9:12]) and abs(v[7] ** 2 + v[8] ** 2 - 1) < 1e-6
        if t == 53:
            return v[3] > 0 and _unit(v[4:7]) and _unit(v[7:10])
        if t == 54:
            return _unit(v[3:6]) and v[6] > 0 and _unit(v[8:11])
        return True

    @staticmethod
    def _geom(t, v):
        r = lambda x: [round(c, 9) for c in x]
        if t == 50:
            p, n = v[0:3], v[3:6]
            off = sum(a * b for a, b in zip(p, n))
            return {'params': {'point': r(p), 'normal': r(n), 'x_axis': r(v[6:9]), 'offset_along_normal': round(off, 9)}}
        if t == 51:
            return {'params': {'point': r(v[0:3]), 'axis': r(v[3:6]), 'radius': round(v[6], 9), 'x_axis': r(v[7:10])}}
        if t == 52:
            return {'params': {'point': r(v[0:3]), 'axis': r(v[3:6]), 'radius': round(v[6], 9),
                               'half_angle_deg': round(math.degrees(math.atan2(v[7], v[8])), 6), 'x_axis': r(v[9:12])}}
        if t == 53:
            return {'params': {'centre': r(v[0:3]), 'radius': round(v[3], 9), 'axis': r(v[4:7]), 'x_axis': r(v[7:10])}}
        if t == 54:
            return {'params': {'centre': r(v[0:3]), 'axis': r(v[3:6]), 'major_radius': round(v[6], 9),
                               'minor_radius': round(v[7], 9), 'x_axis': r(v[8:11])}}

    def _faces(self):
        self.faces = []
        seen = set()
        pat = rb'\x00\x0e\xff?(..)(....)(..)(.{8})(..)(..)(..)(..)(..)([+-])'
        for m in re.finditer(pat, self.d, re.S):
            idx = _u16(m.group(1), 0)
            surf = _u16(m.group(9), 0)
            if idx in seen or surf not in self.surfaces:
                continue
            seen.add(idx)
            self.faces.append({'index': idx, 'node_id': struct.unpack('>I', m.group(2))[0],
                               'shell': _u16(m.group(8), 0), 'surface': surf, 'sense': m.group(10).decode()})

    # feature attribution ------------------------------------------------------
    def face_features(self, face_idx):
        """Feature ids from ATOM_ID_2001 attributes on the face.

        ATOM_ID_2001 int field = [entity_class, feature_id, timestamp, 0, seq, ...];
        feature_id matches the Keywords feature id."""
        out = []
        for a in self.attrs_by_owner.get(face_idx, []):
            if a['name'] in ENTITY_ID_ATTRS:
                for v in a['values']:
                    if isinstance(v, list) and len(v) >= 5:
                        out.append({'class': v[0], 'feature_id': v[1], 'stamp': v[2], 'seq': v[4], 'raw': v})
        return out

    def body_attrs(self):
        return [a for a in self.attributes if a['name'] in (
            'LAST_BODY_MODIFYING_FEATURE_ID', 'SDL/TYSA_DENSITY', 'SW_INTERNAL_BODY_NAME',
            'SDL/TYSA_COLOUR_2', 'BODY_SCALING_FACTOR')]


# ---------------------------------------------------------------------------
# Topology (round 2).  Layouts inferred from bytes, consistent with XT ref:
#  LOOP 15   : index, node_id:u32, attr, fin, face, next
#  FIN 17    : index, attr, loop, forward, backward, vertex, other, edge, curve, next_at_vx, sense
#  EDGE 16   : index, node_id:u32, attr, tolerance:f64, fin, previous, next, curve, ?, ?, owner
#  VERTEX 18 : index, node_id:u32, attr, fin, previous, next, point, tolerance:f64, owner
#  POINT 29  : index, node_id:u32, attr, owner, next, previous, pvec(3 f64)
#  LINE 30   : index, node_id:u32, attr, owner, next, previous, geom_owner, sense, pvec, direction
#  CIRCLE 31 : ... sense, centre, normal, x_axis, radius
#  ELLIPSE 32: ... sense, centre, normal, x_axis, major, minor
CURVE_TYPES = {30: 'line', 31: 'circle', 32: 'ellipse', 133: 'trimmed_curve', 134: 'b_curve', 137: 'sp_curve', 38: 'intersection'}


def _topology(self):
    d = self.d
    H = lambda b: struct.unpack('>H', b)[0]
    self.loops, self.fins, self.edges, self.vertices, self.points, self.curves = {}, {}, {}, {}, {}, {}
    for m in re.finditer(rb'\x00\x0f\xff?(..)(....)(..)(..)(..)(..)', d, re.S):
        face = H(m.group(5))
        if any(f['index'] == face for f in self.faces[:0]):
            pass
        self.loops.setdefault(H(m.group(1)), {'fin': H(m.group(4)), 'face': face, 'next': H(m.group(6))})
    for m in re.finditer(rb'\x00\x11\xff?(..)(..)(..)(..)(..)(..)(..)(..)(..)(..)([+-])', d, re.S):
        g = [H(m.group(k)) for k in range(1, 11)]
        if g[2] in self.loops:
            self.fins.setdefault(g[0], {'loop': g[2], 'fwd': g[3], 'bwd': g[4], 'vertex': g[5], 'other': g[6],
                                        'edge': g[7], 'curve': g[8], 'sense': m.group(11).decode()})
    for m in re.finditer(rb'\x00\x10\xff?(..)(....)(..)(.{8})(..)(..)(..)(..)', d, re.S):
        self.edges.setdefault(H(m.group(1)), {'fin': H(m.group(5)), 'curve': H(m.group(8))})
    for m in re.finditer(rb'\x00\x12\xff?(..)(....)(..)(..)(..)(..)(..)', d, re.S):
        self.vertices.setdefault(H(m.group(1)), {'point': H(m.group(7))})
    for m in re.finditer(rb'\x00\x1d\xff?(..)(....)(..)(..)(..)(..)', d, re.S):
        v = struct.unpack_from('>3d', d, m.end())
        if all(abs(x) < 1e3 for x in v):
            self.points.setdefault(H(m.group(1)), [round(x, 9) for x in v])
    for m in re.finditer(rb'\x00([\x1e\x1f\x20])\xff?(..)(....)(..)(..)(..)(..)(..)([+-])', d, re.S):
        t = m.group(1)[0]
        n = {30: 6, 31: 10, 32: 11}[t]
        if m.end() + 8 * n > len(d):
            continue
        v = struct.unpack_from('>%dd' % n, d, m.end())
        if any(x != x or abs(x) > 1e3 for x in v) or not _unit(v[3:6]):
            continue
        r = lambda x: [round(c, 9) for c in x]
        c = {'type': CURVE_TYPES[t]}
        if t == 30:
            c.update(point=r(v[0:3]), direction=r(v[3:6]))
        else:
            c.update(centre=r(v[0:3]), normal=r(v[3:6]), x_axis=r(v[6:9]), radius=round(v[9], 9))
            if t == 32:
                c['minor_radius'] = round(v[10], 9)
        self.curves.setdefault(H(m.group(2)), c)
    for m in re.finditer(rb'\x00(\x85|\x86|\x89|\x26)\xff?(..)', d, re.S):
        self.curves.setdefault(H(m.group(2)), {'type': CURVE_TYPES[m.group(1)[0]]})


def face_loops(self, face_idx):
    if not hasattr(self, 'loops'):
        _topology(self)
    out = []
    for li, L in self.loops.items():
        if L['face'] != face_idx or L['fin'] not in self.fins:
            continue
        fin0, fin, seq, guard = L['fin'], L['fin'], [], 0
        while guard < 500:
            F = self.fins.get(fin)
            if not F:
                break
            E = self.edges.get(F['edge'], {})
            V = self.vertices.get(F['vertex'], {})
            cur = self.curves.get(E.get('curve')) or self.curves.get(F['curve'])
            seq.append({'edge': F['edge'], 'fin_sense': F['sense'],
                        'start_vertex': self.points.get(V.get('point')),
                        'curve': cur})
            fin = F['fwd']
            guard += 1
            if fin == fin0:
                break
        out.append({'loop': li, 'edges': seq})
    return out


XT.face_loops = face_loops

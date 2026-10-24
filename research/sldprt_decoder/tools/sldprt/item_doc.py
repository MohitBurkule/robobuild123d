"""Round 14: document-level fields (configurations, appearance, material, units, custom
properties, equations, named views, display states), decoded field by field from the
A/B CFG / MAT / COLOUR / UNITS / DOC / EQN / VIEW groups.

Streams and layouts (CString = FF FE FF <u8 n> <n UTF-16 chars>):
  moConfigurationMgr_c stream
      one moPartConfiguration_c object per configuration, ACTIVE FIRST, each followed by
      moNodeName_c 'CString name' and a moVisualProperties_c block.
  moVisualProperties_c (also in the moPart_c stream: part-level appearance)
      u32 COLORREF 0x00BBGGRR | u32 flags | u32 COLORREF 2 (C0C0C0 with a material) | CString texture | CString appearance-or-material
      | f64 ambient | f64 diffuse | f64 specular | f64 shininess | f64 transparency | f64 emission
      The material CString is 'database|material name|id' once a material is applied
      ('Steel' = default appearance, no material).  API COLOUR array = (r, g, b) / 255 + the 6 f64.
  moUnitsTable_c (moPart_c stream): u16 n, then n user-units records.  The record written
      with class name moAngleUserUnits_c (3rd record) carries the document linear units:
      u32 body+0 = decimal places, last u16 before the next record = swUnitsLinear (0 mm, 3 inch).
  moCusPropMgr_c stream: moAdvCusPropList_c u16 n, then n x moAdvCusProp_c + moCusPropStringElem_c:
      CString value | u32 index | u32 9 | CString name | u32 type (0 text, 1 date, 2 number,
      3 yes/no) | CString value | CString evaluated value | i32 -1 | u32 1 ...
      A configuration-specific property sits in a moCusPropMgr_c stream of its own.
  moView_c (configuration-manager stream, after suObList): CString view name | u8 1 | f64 x 4 (orientation)...
  visStateKeyData_c stream: display-state names (CStrings, '<Default>_Display State 1' ...).
  moRelation_c (moPart_c stream): equation text CString, e.g. '"L" = 15'.
"""
import re
import struct

from . import streams as S

CSTR = re.compile(rb'\xff\xfe\xff(.)', re.S)
CLS = re.compile(rb'\xff\xff\x01\x00(.)\x00([A-Za-z_]{3,60})', re.S)


def cstr(x, p):
    """(text, end) for a CString at p, else (None, p)."""
    if x[p:p + 3] != b'\xff\xfe\xff' or p + 4 > len(x):
        return None, p
    n = x[p + 3]
    e = p + 4 + 2 * n
    try:
        return x[p + 4:e].decode('utf-16-le'), e
    except UnicodeDecodeError:
        return None, p


def cstrings(x, a=0, b=None):
    out = []
    for m in CSTR.finditer(x, a, len(x) if b is None else b):
        t, e = cstr(x, m.start())
        if t is not None:
            out.append((m.start(), t, e))
    return out


def visual_block(x, p):
    """moVisualProperties_c body at p (the COLORREF)."""
    if p < 0 or p + 16 > len(x) or x[p + 3] != 0 or x[p + 11] != 0:
        return None
    tex, q = cstr(x, p + 12)
    app, q2 = cstr(x, q)
    if tex is None or app is None or q2 + 48 > len(x):
        return None
    f = struct.unpack_from('<6d', x, q2)
    if not all(-1e-9 <= v <= 1.0 + 1e-9 for v in f):
        return None
    r, g, b = x[p], x[p + 1], x[p + 2]
    mat = app.split('|') if '|' in app else None
    return dict(offset=p, rgb=(r, g, b), flags=struct.unpack_from('<I', x, p + 4)[0], rgb2=tuple(x[p + 8:p + 11]), texture=tex, appearance=app,
                material=mat[1] if mat else None, material_db=mat[0] if mat else None,
                ambient=f[0], diffuse=f[1], specular=f[2], shininess=f[3], transparency=f[4], emission=f[5],
                colour=[r / 255, g / 255, b / 255] + list(f))


def visual_blocks(x):
    out = []
    j = x.find(b'moVisualProperties_c')
    starts = [j + 20] if j >= 0 else []
    # later instances: a new-object tag 0x80xx directly before the COLORREF
    for m in CSTR.finditer(x):
        p = m.start() - 12
        if p > 2 and p not in starts and x[p - 1] & 0x80 and x[p - 1] != 0xff and (not starts or p > starts[0]):
            starts.append(p)
    for p in sorted(set(starts)):
        v = visual_block(x, p)
        if v:
            out.append(v)
    return out


def configurations(x):
    """names in stored order (active first) + per-configuration appearance."""
    out = []
    for v in visual_blocks(x):
        prev = [t for o, t, e in cstrings(x, max(0, v['offset'] - 120), v['offset']) if t]
        if prev and prev[-1] not in [c['name'] for c in out]:
            out.append(dict(name=prev[-1], visual=v))
    return out


def units(x):
    j = x.find(b'moAngleUserUnits_c')
    if j < 0:
        return None
    body = j + len('moAngleUserUnits_c')
    k = x.find(b'\xff\xff\x01\x00', body)
    if k < 0:
        return None
    return dict(decimals=struct.unpack_from('<I', x, body)[0], linear=struct.unpack_from('<H', x, k - 2)[0])


PROP_TYPES = {0: 'text', 1: 'date', 2: 'number', 3: 'yesno'}
PROP_API = {0: 30, 1: 64, 2: 3, 3: 11}


def custom_props(x):
    out = []
    for o, val, e in cstrings(x):
        if x[e:e + 4] == b'' or e + 8 > len(x):
            continue
        idx, nine = struct.unpack_from('<II', x, e)
        if nine != 9:
            continue
        name, q = cstr(x, e + 8)
        if name is None or q + 4 > len(x):
            continue
        typ = struct.unpack_from('<I', x, q)[0]
        v2, q2 = cstr(x, q + 4)
        ev, q3 = cstr(x, q2)
        out.append(dict(name=name, value=val, evaluated=ev, index=idx, type=PROP_TYPES.get(typ, typ),
                        api_type=PROP_API.get(typ)))
    return out


def decode(data):
    """dict of document-level fields of one SLDPRT file (bytes)."""
    res = dict(configurations=[], active_config=None, display_states=[], material=None, material_db=None,
               part_colour=None, units=None, custom_props=[], config_props=[], equations=[], views=[])
    for s in S.all_streams(data):
        x = s['data']
        head = x[:48]
        if b'moConfigurationMgr_c' in head:
            cf = configurations(x)
            res['configurations'] = [c['name'] for c in cf]
            res['active_config'] = cf[0]['name'] if cf else None
            res['config_visual'] = {c['name']: {k: v for k, v in c['visual'].items() if k != 'offset'} for c in cf}
            j = x.find(b'moView_c')
            while j >= 0:
                t, e = cstr(x, j + 8)
                if t:
                    res['views'].append(t)
                j = x.find(b'moView_c', j + 8)
        elif b'moPart_c' in head:
            vb = visual_blocks(x)
            if vb:
                v = vb[0]
                res['part_colour'] = v['colour']
                res['material'], res['material_db'] = v['material'], v['material_db']
            res['units'] = units(x)
            j = x.find(b'moRelation_c')
            for o, t, e in cstrings(x, j if j >= 0 else len(x)):
                if '=' in t and t.startswith('"') and t not in res['equations']:
                    res['equations'].append(t)
        elif b'moCusPropMgr_c' in head:
            # 'moFilePropContainer_c' then directly suObList: the list holds the file-level
            # properties; '00 00' (empty file container) then suObList: configuration-specific
            j = x.find(b'moFilePropContainer_c') + len('moFilePropContainer_c')
            cfg = x[j:j + 2] == b'\0\0' and x[j + 2:j + 4] == b'\xff\xff'
            (res['config_props'] if cfg else res['custom_props']).extend(custom_props(x))
        elif b'visStateKeyData_c' in head:
            res['display_states'] = [t for o, t, e in cstrings(x) if t and len(t) < 80 and '\\' not in t
                                     and t not in ('Steel', 'defaultplastic')][:16]
    return res


def decode_file(path):
    return decode(open(path, 'rb').read())

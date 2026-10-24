"""Structural record layer for the MFC CArchive feature/mate streams.

Full sequential parsing needs each class's Serialize() layout, which is
unknown for most of the ~150 moXxx_c classes.  This module therefore parses
the record types whose layout *is* known, at their exact offsets, and reports
everything else as gaps (coverage % per stream) instead of skipping silently.

Known records
  ClassDef   FF FF <schema u16> <len u16> <ascii name>         (MFC new-class tag)
  ClassRef   <u16 0x8000|n>  (only counted where it introduces a known object)
  CString    FF FE FF <len u8> <utf-16le len chars>   (len 0xFF -> u16 len follows)
  SketchPoint / SketchSegment   see sketch.py (17-byte marker + fixed fields)
  DimValue   CString 'D<n>' ... FF FE FF 00 00 00 <f64>  (dimension parameter value)
MFC numbering: every ClassDef and every new object get the next map index
(1-based); ClassDef indices are recorded so 0x8000|n tags can be resolved.
"""
import re
import struct
from dataclasses import dataclass

from . import sketch as SK

CLASSDEF = re.compile(rb'\xff\xff([\x00-\x7f][\x00-\x10])([\x01-\x40])\x00([A-Za-z_][A-Za-z0-9_]{2,63})')
CSTR = re.compile(rb'\xff\xfe\xff(.)', re.S)
DIMV = re.compile(rb'\xff\xfe\xff(.)((?:D\x00)(?:[0-9]\x00){1,3}).{0,24}?\xff\xfe\xff\x00\x00\x00(.{8})', re.S)


@dataclass
class Rec:
    kind: str
    offset: int
    end: int
    value: object = None


def class_defs(d):
    out = []
    for m in CLASSDEF.finditer(d):
        ln = m.group(2)[0]
        name = m.group(3)[:ln]
        if len(name) == ln:
            out.append(Rec('ClassDef', m.start(), m.start() + 6 + ln,
                           {'schema': struct.unpack('<H', m.group(1))[0], 'name': name.decode()}))
    return out


def cstrings(d):
    out = []
    for m in CSTR.finditer(d):
        n, j = m.group(1)[0], m.end()
        if n == 0xFF:
            n, j = struct.unpack_from('<H', d, j)[0], j + 2
        raw = d[j:j + 2 * n]
        if len(raw) == 2 * n:
            try:
                s = raw.decode('utf-16-le')
            except UnicodeDecodeError:
                continue
            if all(c.isprintable() or c in '\r\n\t' for c in s):
                out.append(Rec('CString', m.start(), j + 2 * n, s))
    return out


def dim_values(d):
    return [Rec('DimValue', m.start(), m.end(), {'name': m.group(2).decode('utf-16-le'),
                                                   'value': struct.unpack('<d', m.group(3))[0]})
            for m in DIMV.finditer(d)]


def sketch_records(d):
    out = []
    marks = list(SK.MARK.finditer(d))
    pts, segs, _ = SK.parse_records(d, 0, len(d))
    seg_pos = {s['pos'] for s in segs}
    for k, m in enumerate(marks):
        s = m.start() - 8
        kind = 'SketchSegment' if m.start() in seg_pos else 'SketchPoint'
        end = m.end() + 47 + (22 if kind == 'SketchSegment' else 18)
        out.append(Rec(kind, s, end))
    return out


def scan(d):
    recs = class_defs(d) + cstrings(d) + dim_values(d) + sketch_records(d) + endspec_records(d)
    recs.sort(key=lambda r: (r.offset, -r.end))
    covered, last = 0, 0
    gaps = []
    for r in recs:
        if r.offset > last:
            gaps.append((last, r.offset))
        if r.end > last:
            covered += r.end - max(r.offset, last)
            last = r.end
    if last < len(d):
        gaps.append((last, len(d)))
    hist = {}
    for r in recs:
        hist[r.kind] = hist.get(r.kind, 0) + 1
    return {'records': hist, 'bytes': len(d), 'coverage_pct': round(100 * covered / max(1, len(d)), 2),
            'n_gaps': len(gaps), 'largest_gaps': sorted(gaps, key=lambda g: g[0] - g[1])[:10],
            'classes': [r.value['name'] for r in recs if r.kind == 'ClassDef']}


def endspec_records(d):
    from . import mo_classes as M
    out = []
    for x in M.endspecs(d, 0, len(d)):
        if x.form != 'unknown' and (x.depth_m or x.form != 'A_blind'):  # only records with a decoded value count
            out.append(Rec('EndSpec', x.offset, x.offset + M.SPAN, x.json()))
    return out

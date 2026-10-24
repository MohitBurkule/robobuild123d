"""Structural parser for the SLDPRT/SLDASM 2015+ outer container.

Section record (little-endian), ZIP-local-header-like:
    magic     4s   14 00 06 00
    method    u16  8 = deflate (raw, wbits -15)
    dostime   u32
    crc32     u32  CRC-32 of the *uncompressed* payload
    csize     u32  compressed size
    usize     u32  uncompressed size
    namelen   u32
    name      namelen bytes, each byte nibble-rotated (ROL 4) -> ASCII
    data      csize bytes
Sections whose data does not inflate are kept as opaque (inflated=False).
Bytes outside section records are reported as gaps (the file tail holds a
directory/trailer that is not decoded yet).
"""
import struct
import zlib
from dataclasses import dataclass, field

MAGIC = b'\x14\x00\x06\x00'
HDR = struct.Struct('<4sHIIIII')


def rol4(b):
    return bytes(((c << 4) | (c >> 4)) & 0xFF for c in b)


@dataclass
class Section:
    offset: int
    method: int
    dostime: int
    crc32: int
    csize: int
    usize: int
    name: str
    data_offset: int
    payload: bytes = field(repr=False, default=b'')
    crc_ok: bool = False
    nested_offset: int = None
    inflated: bool = True


def parse(data):
    """Return (sections, gaps) where gaps = [(start, end)] not covered by any section."""
    secs, gaps = [], []
    pos = 0
    i = data.find(MAGIC)
    while i >= 0:
        if i + HDR.size > len(data):
            break
        magic, method, dt, crc, cs, us, nl = HDR.unpack_from(data, i)
        ok = method in (0, 8) and nl < 4096 and i + HDR.size + nl + cs <= len(data) and us < 1 << 30
        if ok:
            name = rol4(data[i + HDR.size:i + HDR.size + nl]).decode('latin1')
            ds = i + HDR.size + nl
            raw = data[ds:ds + cs]
            try:
                pay, inflated = (zlib.decompress(raw, -15) if method == 8 else raw), True
            except zlib.error:
                pay, inflated = b'', False   # opaque (not raw deflate; possibly encrypted)
        if ok:
            if i > pos:
                gaps.append((pos, i))
            s = Section(i, method, dt, crc, cs, us, name, ds, pay, inflated and zlib.crc32(pay) == crc, None, inflated)
            k = pay.find(b'x\x01', 0, 64)
            if 0 <= k:
                try:
                    s.payload, s.nested_offset = zlib.decompress(pay[k:]), k
                except zlib.error:
                    pass
            secs.append(s)
            pos = ds + cs
            i = data.find(MAGIC, pos)
        else:
            i = data.find(MAGIC, i + 1)
    if pos < len(data):
        gaps.append((pos, len(data)))
    return secs, gaps


def coverage(data):
    secs, gaps = parse(data)
    g = sum(b - a for a, b in gaps)
    return {'sections': len(secs), 'opaque': sum(not s.inflated for s in secs), 'crc_ok': sum(s.crc_ok for s in secs),
            'bytes': len(data), 'gap_bytes': g, 'coverage_pct': round(100 * (1 - g / max(1, len(data))), 2),
            'gaps': gaps[:20]}


def unframed_streams(data, gaps, min_len=64):
    """Raw-deflate streams found inside gaps (sections whose header we did not
    recognise, e.g. large DisplayLists).  Returned as (offset, consumed, payload)."""
    from .streams import raw_streams
    out = []
    for a, b in gaps:
        if b - a < 16:
            continue
        for off, r in raw_streams(data[a:b], min_len):
            o = zlib.decompressobj(-15)
            o.decompress(data[a + off:b])
            out.append((a + off, (b - a - off) - len(o.unused_data), r))
    return out


def full_coverage(data):
    secs, gaps = parse(data)
    unf = unframed_streams(data, gaps)
    covered = sum(HDR.size + len(s.name) + s.csize for s in secs) + sum(c for _, c, _ in unf)
    return {'sections': len(secs), 'opaque_sections': sum(not s.inflated for s in secs),
            'crc_ok': sum(s.crc_ok for s in secs), 'unframed_streams': len(unf),
            'bytes': len(data), 'coverage_pct': round(100 * covered / max(1, len(data)), 2)}

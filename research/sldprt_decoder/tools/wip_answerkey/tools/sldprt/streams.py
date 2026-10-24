"""Locate and inflate the compressed streams inside a SolidWorks 2023 SLDPRT.

SLDPRT 2015+ is a proprietary container; rather than parsing its directory we
brute-scan every byte offset for a raw-deflate stream (zlib wbits=-15).  Some
streams carry a short header (e.g. 0x14060100 ...) followed by a second,
zlib-wrapped stream ('x\\x01') within the first 64 bytes; that is inflated too.
"""
import zlib

MAX_CHUNK = 6_000_000


def raw_streams(data, min_len=64):
    i, n = 0, len(data)
    while i < n - 2:
        try:
            o = zlib.decompressobj(-15)
            chunk = data[i:i + MAX_CHUNK]
            r = o.decompress(chunk)
            if len(r) > min_len and o.eof:
                yield i, r
                i += len(chunk) - len(o.unused_data)
                continue
        except Exception:
            pass
        i += 1


def inflate_nested(r):
    """Return (payload, nested_offset or None)."""
    k = r.find(b'x\x01', 0, 64)
    while 0 <= k < 64:
        try:
            return zlib.decompress(r[k:]), k
        except Exception:
            k = r.find(b'x\x01', k + 1, 64)
    return r, None


def all_streams(data):
    """List of dicts {offset, nested, data}."""
    out = []
    for off, r in raw_streams(data):
        p, k = inflate_nested(r)
        out.append({'offset': off, 'nested': k, 'data': p})
    return out


def classify(s):
    d = s['data']
    if d.startswith(b'PS\x00\x00') and b'TRANSMIT FILE' in d[:80]:
        return 'parasolid'
    if b'<Keywords' in d[:4000]:
        return 'keywords'
    if b'moSketch_c' in d or b'moCommentsFolder_c' in d[:40]:
        return 'features'
    return 'other'

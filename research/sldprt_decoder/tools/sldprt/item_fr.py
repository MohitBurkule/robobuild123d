"""moFR_c = SolidWorks face/edge reference (topological name), round 11.

Layout: u16 objref | u32 feature_id | u32 stamp | i32 path[k].
Meaning (cross-checked against Parasolid ATOM_ID_2001 = [class, fid, stamp, 0, seq, ...]):
  feature_id/stamp = the feature that created the face/edge and that feature's creation stamp
  (14151/14151 refs whose fid has live atoms carry the same stamp), path[0] = per-feature
  entity sequence (atom field 4); a 3-word path [seq, -1, 0] matches atoms like [.., seq, -1, 0].
Round 11b: XT attribute names now resolved via the ATTRIB_DEF identifier pointer; the
per-face record is FACE_ID_2001 (3 166 values, was 2 303).
Refs to fids with no live atoms point at entities consumed by later features."""
import struct


def decode(d, spans):
    """spans: [(ev, start, end)] from classrec._obj_spans; returns list of dicts for moFR_c."""
    out = []
    for e, a, b in spans:
        if e.name != 'moFR_c' or b - a < 10:
            continue
        r, fid, st = struct.unpack_from('<HII', d, a)
        k = (b - a - 10) // 4
        out.append({'offset': a, 'objref': r, 'feature_id': fid, 'stamp': st,
                    'path': list(struct.unpack_from('<%di' % k, d, a + 10))})
    return out


def chain_triples(v):
    """Round 11b: an entity-id int field is a chain of history records; every
    (fid, stamp, 0, seq) group (stamp = plausible unix time) is one triple."""
    out = []
    for j in range(1, len(v) - 3):
        if 1_400_000_000 < v[j + 1] < 1_900_000_000 and v[j + 2] == 0:
            out.append((v[j], v[j + 1], v[j + 3]))
    return out


def match_atoms(refs, atoms):
    """atoms: tuples (class, fid, stamp, 0, seq, ...). Adds 'atom' (exact), 'stamp_ok',
    and 'chain_ok' = (fid, stamp, path[0]) occurs anywhere in an atom's history chain."""
    chain = {t for a in atoms for t in chain_triples(a)}
    full = {(a[1], a[2]) + tuple(a[4:]): a for a in atoms}
    fs = {(a[1], a[2]) for a in atoms}
    for r in refs:
        r['stamp_ok'] = (r['feature_id'], r['stamp']) in fs
        r['atom'] = None
        r['chain_ok'] = bool(r['path']) and (r['feature_id'], r['stamp'], r['path'][0]) in chain
        for k in (len(r['path']), 3, 1):
            key = (r['feature_id'], r['stamp']) + tuple(r['path'][:k])
            if k and key in full:
                r['atom'] = full[key]; break
    return refs

"""Round 11b: map DumpV3 GetPersistReference3 blobs (dumps_v3/*.refs.txt) to binary moFR_c refs and XT chains.
A pref is '5046 0000 <u32 kind> FFFEFF00 00000000' + a self-contained CArchive; its moFR_c objects are
'tag | u16 docref | u32 fid | u32 stamp | i32 seq ...' exactly as in the feature stream."""
import sys, os, glob, re, struct
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR, item_fr as IF, streams as ST
from sldprt.xt import XT, ENTITY_ID_ATTRS
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
TRI = re.compile(rb'(?=[\x00-\x7f][\x80-\xff](..)(....)(....)(....))', re.S)

def pref_triples(b):
    out = []
    for m in TRI.finditer(b):
        fid, st, seq = (struct.unpack('<I', m.group(k))[0] for k in (2, 3, 4))
        if 1_400_000_000 < st < 1_900_000_000 and fid < 100000 and struct.unpack('<H', m.group(1))[0] < 64:
            out.append((fid, st, seq if seq < 1 << 31 else seq - (1 << 32)))
    return out

def parse(path):
    recs = []
    for ln in open(path, encoding='latin-1'):
        m = re.search(r'pref=([0-9A-F]+)', ln)
        if m: recs.append((ln.split()[0], bytes.fromhex(m.group(1))))
    return recs

S = Counter(); kinds = Counter()
SUB, SRC = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('', 'corpus')
for p in sorted(glob.glob(R + 'dumps_v3/' + SUB + '*.refs.txt')):
    n = os.path.basename(p)[:-9]
    src = R + SRC + '/' + n + '.SLDPRT'
    if not os.path.exists(src): continue
    raw = open(src, 'rb').read()
    d = V.feature_stream(src)
    if d is None: continue
    ev, _ = ON.numbering(d)
    bin_t = {(r['feature_id'], r['stamp'], r['path'][0] if r['path'] else None) for r in IF.decode(d, CR._obj_spans(d, ev))}
    bin_fs = {(a, b) for a, b, c in bin_t}
    xt_t = set()
    for s in ST.all_streams(raw):
        if ST.classify(s) == 'parasolid':
            x = XT(s['data'])
            for a in x.attributes:
                if a['name'] in ENTITY_ID_ATTRS:
                    for v in a['values']:
                        if isinstance(v, list) and len(v) >= 5: xt_t.update(IF.chain_triples(v))
    for kind, b in parse(p):
        kinds[(kind, struct.unpack_from('<I', b, 4)[0])] += 1
        if kind == 'FEATURE': continue
        T = pref_triples(b)
        S[kind + '.prefs'] += 1; S[kind + '.with_triple'] += bool(T)
        for t in T:
            S['triples'] += 1
            S['in_binary_moFR_c(fid,stamp,seq)'] += t in bin_t
            S['in_binary_moFR_c(fid,stamp)'] += t[:2] in bin_fs
            S['in_XT_chain'] += t in xt_t
    print(n, dict(S), flush=True)
print('pref kinds', kinds)

"""Round 16 (4): generalization check on corpus/ parts with dumps_corpus answer keys.
Reads results_corpus/<part>.json (decode-only replay, R16_SRC=corpus run_all.py) and breps_corpus/,
scores (a) features: top-level solid features in the dump vs replay status OK/PART,
(b) faces: rebuild_dump/face_audit.py patches matched.  -> corpus_check.json / .txt"""
import os, sys, json, glob, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
NONSOLID = re.compile(r'Folder|RefPlane|ProfileFeature|RefAxis|RefPoint|Cabinet|Light|Camera|Sketch|CoordSys|MateRef|Annotation')

def dump_features(path):
    out = []
    for l in open(path, errors='replace'):
        m = re.match(r'FEATURE (\d+) \| (.*?) \| (\S+) \| id=\d+ \| suppressed=(\w+)', l)
        if m and m.group(4) == 'False' and not NONSOLID.search(m.group(3)): out.append((m.group(2), m.group(3)))
    return out

if __name__ == '__main__':
    import face_gate as FG
    res = {}; tot = dict(feat=0, ok=0, part=0, fm=0, fp=0)
    for rj in sorted(glob.glob(os.path.join(HERE, 'results_corpus', '*.json'))):
        p = os.path.basename(rj)[:-5]; d = os.path.join(ROOT, 'dumps_corpus', p + '.dump.txt')
        if not os.path.exists(d): continue
        r = json.load(open(rj)); feats = dump_features(d)
        st = {}
        for x in r.get('log', []): st[x['feature']] = x['status'] if st.get(x['feature']) != 'OK' else 'OK'
        ok = sum(st.get(n) == 'OK' for n, t in feats); pa = sum(st.get(n) == 'PART' for n, t in feats)
        fa = {}
        b = os.path.join(HERE, 'breps_corpus', p + '.brep')
        if os.path.exists(b):
            try: fa = FG.gate(b, d)
            except Exception as ex: fa = dict(error=repr(ex)[:120])
        res[p] = dict(features=len(feats), ok=ok, part=pa, oracle_iou=r.get('oracle_iou'), faces_matched=fa.get('matched'), dump_patches=fa.get('dump_patches'), face_pct=fa.get('pct'),
                      missing=[n for n, t in feats if st.get(n) not in ('OK', 'PART')][:12], note=r.get('note', ''))
        tot['feat'] += len(feats); tot['ok'] += ok; tot['part'] += pa; tot['fm'] += fa.get('matched') or 0; tot['fp'] += fa.get('dump_patches') or 0
        print(p, res[p]['ok'], res[p]['part'], res[p]['features'], res[p]['oracle_iou'], res[p]['face_pct'], flush=True)
    iou = [v['oracle_iou'] for v in res.values() if v['oracle_iou'] is not None]
    res['_total'] = dict(parts=len(res), **tot, mean_oracle_iou=round(sum(iou) / max(1, len(iou)), 4),
                         parts_all_ok=sum(1 for v in res.values() if isinstance(v, dict) and v.get('features') and v['ok'] == v['features']))
    json.dump(res, open(os.path.join(HERE, 'corpus_check.json'), 'w'), indent=1)
    print(res['_total'])

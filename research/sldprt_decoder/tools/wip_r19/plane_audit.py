"""round 18 CHECK tool: decoded sketch placements vs the SW dump SKETCH_TO_MODEL (dumps used for scoring only)."""
import sys, os, json, re, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
def dump_s2m(part):
    p = os.path.join(ROOT, 'dumps', part + '.dump.txt')
    if not os.path.exists(p): return {}
    out, cur = {}, None
    for l in open(p, errors='replace'):
        m = re.match(r'FEATURE \d+ \| (.*?) \| (\w+)', l)
        if m: cur = m.group(1) if m.group(2) in ('ProfileFeature', '3DProfileFeature') else None; continue
        if cur and l.strip().startswith('SKETCH_TO_MODEL'):
            v = [float(x) for x in l.split(None, 1)[1].strip().strip(',').split(',')]
            out[cur] = (np.array(v[:9]).reshape(3, 3), np.array(v[9:12]) * 1000)
    return out
def dec_s2m(part, dec='decoded'):
    d = json.load(open(os.path.join(ROOT, dec, part + '.json'))); out = {}
    for s in d.get('sketches') or []:
        T = ((s.get('placement') or {}).get('transform_rows_x_y_z_t')) or []
        if len(T) == 12: out[s['name']] = (np.array(T[:9]).reshape(3, 3), np.array(T[9:12]) * 1000, s['placement'].get('confidence'))
    return out
def audit(part):
    D, S = dump_s2m(part), dec_s2m(part); rows = []
    for k, (R, t) in D.items():
        if k not in S: rows.append((k, 'missing', None, None)); continue
        R2, t2, conf = S[k]; n, n2 = R[2], R2[2]
        nok = abs(abs(n @ n2) - 1) < 1e-4
        off, off2 = float(t @ n), float(t2 @ n) if nok else None
        rows.append((k, 'ok' if nok and abs(off - off2) < 1e-3 else ('normal' if not nok else 'offset'), round(off, 4), off2 if off2 is None else round(off2, 4), conf))
    return rows
if __name__ == '__main__':
    tot = {}
    for part in sys.argv[1:] or [os.path.basename(p)[:-7] for p in sorted(glob.glob(os.path.join(ROOT, 'revdev', '*.SLDPRT')))]:
        try: rows = audit(part)
        except Exception as ex: print(part, 'ERR', ex); continue
        for r in rows: tot[r[1]] = tot.get(r[1], 0) + 1
        bad = [r for r in rows if r[1] != 'ok']
        print(f'{part}: {len(rows)-len(bad)}/{len(rows)} ok', *bad[:40], sep='\n  ' if bad else ' ')
    print(tot)

def sp_s2m(part, base=os.path.join(ROOT, 'tools', 'wip_r14', 'decode_only')):
    p = os.path.join(base, part, part + '.sketchplane.json')
    if not os.path.exists(p): return {}
    out = {}
    for s in json.load(open(p))['sketches']:
        R = np.array([s['x_axis'], s['y_axis'], s['normal']], float)
        out[s['sketch']] = (R, np.array(s['origin_m']) * 1000, s['record_class'], s.get('record_offset'))
    return out
def audit_sp(part, sp=None):
    D = dump_s2m(part); S = sp if sp is not None else sp_s2m(part); rows = []
    for k, (R, t) in D.items():
        if k not in S: rows.append((k, 'missing')); continue
        R2, t2, cls, off_ = S[k]
        n = R[2]; n2 = R2[2]; nok = abs(abs(n @ n2) - 1) < 1e-4
        # dump SKETCH_TO_MODEL: rows are x,y,n? check both conventions
        rows.append((k, cls, 'ok' if nok and np.allclose(t, t2, atol=1e-3) else ('offset' if nok else 'normal'), round(float(t @ n), 3), round(float(t2 @ n2), 3) if True else None, np.round(n, 3).tolist(), np.round(n2, 3).tolist()))
    return rows

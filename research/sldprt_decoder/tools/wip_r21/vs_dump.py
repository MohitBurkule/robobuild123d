"""Round 15: decoded inputs vs the dump (truth) per feature: sketch link, sketch frame, segment
count, end condition / depth.  First divergence per part is the first feature with a mismatch."""
import sys, os, json, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import decode_replay as D
import numpy as np
DUMPS = os.path.join(D.ROOT, 'dumps_v2')
def compare(part, quiet=False):
    D.R.DEC = D.DO.regen(part); D.R.PART = part
    with contextlib.redirect_stdout(io.StringIO()):
        g = D.DO.GRebuild()
    P = D.to_part(g)
    T = D.DP.parse_dump(os.path.join(DUMPS, part + '.dump.txt'))
    rows = []
    for f in sorted(g.d['features'], key=lambda f: f['id']):
        if f['type'] not in ('Boss-Extrude', 'Cut-Extrude', 'Extrusion', 'Revolve', 'Cut-Revolve'): continue
        t = T.by_name.get(f['name'])
        if t is None: rows.append((f['name'], 'not in dump')); continue
        ts = T.sketch_of(t); e = g.ec.get(f['name']) or {}
        with contextlib.redirect_stdout(io.StringIO()):
            ds = e.get('sketch') or g.link(f['name'])
        issues = []
        if ts is None: issues.append('dump: no sketch')
        else:
            if ds != ts.name: issues.append(f'link {ds} != {ts.name}')
            dsf = P.by_name.get(ts.name)
            if dsf is None or dsf.sketch is None: issues.append('sketch not decoded')
            else:
                a, b = np.array(dsf.sketch.rot), np.array(ts.sketch.rot)
                if not np.allclose(a, b, atol=1e-4): issues.append(f'frame rot {np.round(a,3).tolist()} != {np.round(b,3).tolist()}')
                if np.linalg.norm(np.array(dsf.sketch.trans) - np.array(ts.sketch.trans)) * 1e3 > 1e-3:
                    # an in-plane origin shift is harmless only if the geometry compensates; report it
                    issues.append(f'origin {np.round(np.array(dsf.sketch.trans)*1e3,3).tolist()} != {np.round(np.array(ts.sketch.trans)*1e3,3).tolist()}')
                nd = len([s for s in dsf.sketch.segs if not s.construction]); nt = len(ts.sketch.profile_segs())
                if nd != nt: issues.append(f'segs {nd} vs {nt}')
        if t.extrude is not None:
            x = t.extrude; c = e.get('end_code_dir1'); Dm = (e.get('D_mm') or [None])[0]
            if c != x.end1: issues.append(f'end1 {c} != {x.end1}')
            if Dm is not None and abs(Dm - x.d1 * 1e3) > 1e-3 and x.end1 not in (1, 2, 3, 4, 7, 9): issues.append(f'D {Dm} != {x.d1*1e3:g}')
            if x.both: issues.append(f'dump both=True end2={x.end2} d2={x.d2*1e3:g}' + ('' if e.get('end_code_dir2') is not None else ' (decoded: one direction)'))
            if x.reverse: issues.append('dump reverse=True')
        rows.append((f['name'], '; '.join(issues) or 'ok'))
    if not quiet:
        for r in rows: print(f'  {r[0]:16s} {r[1]}')
    return rows
if __name__ == '__main__':
    for p in sys.argv[1:]: print('==', p); compare(p)

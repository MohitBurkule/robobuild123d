"""r20 diagnostic: print revolve feature dims, sketch segs and construction lines."""
import sys, os, io, contextlib, math
os.environ.setdefault('R15_OUT', os.path.dirname(os.path.abspath(__file__)))
import decode_replay as D
part = sys.argv[1]; stop = sys.argv[2:] 
D.LOG.clear(); D.R.LOG.clear(); D.R.DEC = D.DO.regen(part); D.R.PART = part
with contextlib.redirect_stdout(io.StringIO()): g = D.DO.GRebuild()
P = D.to_part(g)
for f in P.features:
    if 'Revol' in f.type or (stop and f.name in stop):
        sk = getattr(f, 'sketch', None)
        skf = next((x for x in P.features if x is not f and getattr(x,'sketch',None) is not None and x.name in (getattr(f,'sketches',None) or [])), None)
        print('==', f.name, f.type, {k: round(v,5) for k, v in f.dims.items()}, getattr(f,'sketches',None), [a for a in dir(f) if not a.startswith('_')])
        R = D.OracleReplay.__new__(D.OracleReplay); R.part = P; R.g = g
        skf = D.OracleReplay.sketch_feat(R, f)
        if skf is None: print('  no sketch'); continue
        sk = skf.sketch; print('  sketch', skf.name, 'rot', sk.rot.tolist() if hasattr(sk.rot,'tolist') else sk.rot, 'tr', sk.trans)
        for s in sk.segs: print('   seg', s.name if hasattr(s,'name') else '', s.type, s.construction, [round(x*1e3,3) for x in s.p0[:2]], [round(x*1e3,3) for x in s.p1[:2]], 'model', [round(x,2) for x in sk.to_model(s.p0)], [round(x,2) for x in sk.to_model(s.p1)])
        print('  created_faces', len(f.created_faces or []), 'faces', (f.faces or [])[:3] if isinstance(f.faces, list) else f.faces)
        for cf in (f.created_faces or [])[:12]: print('    ', str(cf)[:300])

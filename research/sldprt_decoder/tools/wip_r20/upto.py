"""r20 diagnostic: replay a part up to (and including) a named feature, debug output on."""
import sys, os, io, contextlib, time
os.environ.setdefault('R15_OUT', os.path.dirname(os.path.abspath(__file__)))
import decode_replay as D
part, last = sys.argv[1], sys.argv[2]
D.LOG.clear(); D.R.LOG.clear(); D.R.DEC = D.DO.regen(part); D.R.PART = part
ref = D.oracle_for(part); ref.init_points()
rb = D.OracleReplay(part, ref)
fs = rb.part.features; i = [f.name for f in fs].index(last); rb.part.features = fs[:i + 1]
t = time.time()
with contextlib.redirect_stdout(io.StringIO()): rb.run()
for x in D.LOG: print({k: str(v)[:150] for k, v in x.items()})
print('score', rb.cur_score(), 'VB', rb.VB, 'VT', rb.VT, 'I', rb.I, time.time() - t)
if len(sys.argv) > 3:
    from build123d import export_brep; export_brep(rb.body, sys.argv[3])

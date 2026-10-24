"""r21 diagnostic: during a greedy replay, for each named extrude/revolve: is the dump's sketch frame
(answer key, checking only) among the frame candidates, at which rank, and what did the feature log."""
import sys, os, io, re, contextlib
import numpy as np
os.environ.setdefault('R15_OUT', os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('R19_BEAM', '1'); os.environ.setdefault('R16_PASSES', '1')
import decode_replay as D
part = sys.argv[1]; names = set(sys.argv[2:])
TD = D.DP.parse_dump(os.path.join(D.ROOT, 'dumps_v2' if D.SRC == 'revdev' else 'dumps_' + D.SRC, part + '.dump.txt'))
orig = D.OracleReplay.frames
def frames(self, skf):
    fr = orig(self, skf)
    F = getattr(self, '_cur_feat', None)
    if F is not None and F.name in names and not getattr(skf, '_r21_seen', False):
        skf._r21_seen = True
        t = TD.by_name.get(skf.name); rk = None
        if t is not None and t.sketch is not None:
            Rt = np.array(t.sketch.rot, float); tt = np.array(t.sketch.trans, float)
            for i, (r, tr, nm) in enumerate(fr):
                r = np.array(r, float)
                if np.allclose(r[2], Rt[2], atol=1e-4) and abs(r[2] @ np.array(tr, float) - Rt[2] @ tt) < 1e-6:
                    rk = (i, nm, 'same-axes' if np.allclose(r, Rt, atol=1e-4) else 'plane-only'); break
            print('FRAME', F.name, skf.name, 'dump n', np.round(Rt[2], 3).tolist(), 'off', round(float(Rt[2] @ tt) * 1e3, 3), 'rank', rk, 'of', len(fr), [x[2] for x in fr][:8], file=sys.stderr, flush=True)
    return fr
D.OracleReplay.frames = frames
o1 = D.OracleReplay._run_one
def _run_one(self, f):
    self._cur_feat = f; return o1(self, f)
D.OracleReplay._run_one = _run_one
D.LOG.clear(); D.R.LOG.clear(); D.R.DEC = D.DO.regen(part); D.R.PART = part
ref = D.oracle_for(part); ref.init_points()
with contextlib.redirect_stdout(io.StringIO()):
    rb = D.OracleReplay(part, ref); rb.run()
for x in D.LOG:
    if x['feature'] in names: print('LOG', {k: str(v)[:120] for k, v in x.items()}, file=sys.stderr)
print('score', rb.cur_score(), file=sys.stderr)

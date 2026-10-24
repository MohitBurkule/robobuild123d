"""r22 diagnostic: rank of the dump sketch plane among xframes() for named features (dump used only to check)."""
import sys, os, io, re, contextlib
import numpy as np
os.environ.setdefault('R15_OUT', os.path.dirname(os.path.abspath(__file__)))
import decode_replay as D
part = sys.argv[1]; names = sys.argv[2:]
D.R.DEC = D.DO.regen(part); D.R.PART = part
with contextlib.redirect_stdout(io.StringIO()): g = D.DO.GRebuild()
P = D.to_part(g)
dump = open(os.path.join(D.ROOT, 'dumps_v2', part + '.dump.txt'), errors='replace').read()
R_ = D.OracleReplay.__new__(D.OracleReplay); R_.part = P; R_.g = g; R_.pname = part; R_.body = None
R_.frame_doubt = lambda skf: False
for n in names:
    f = P.by_name[n]; skf = R_.sketch_feat(f)
    stm = re.search(r'FEATURE -?\d+ \| ' + re.escape(skf.name) + r' \|.*?SKETCH_TO_MODEL (\S+)', dump, re.S)
    v = [float(x) for x in stm.group(1).split(',') if x]; Rm = np.array(v[:9]).reshape(3, 3); t = np.array(v[9:12]) * 1e3
    XF = R_.xframes(skf, 1000)
    hit = None
    dn = Rm[2]; off_d = float(dn @ t)
    for i, (rot, tr, lab) in enumerate(XF):
        Z = np.array(rot[2], float); c = float(dn @ Z)
        if abs(abs(c) - 1) < 1e-3 and abs(off_d - c * float(Z @ np.array(tr) * D.MM)) < 1e-2: hit = (i, lab); break
    print('   dump plane n', np.round(dn, 3), 'off', round(off_d, 3))
    print(n, skf.name, 'n_xf', len(XF), 'dump plane rank', hit, 'top5', [x[2] for x in XF[:5]])

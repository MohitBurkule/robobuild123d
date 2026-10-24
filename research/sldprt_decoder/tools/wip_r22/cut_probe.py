"""r21 diagnostic: for named (failed) extrude features, the decoded sketch plane / extent / cells next to
the dump's (answer key, checking only): plane = decoded sketch normal + offset vs dump SKETCH_TO_MODEL,
extent = decoded D/end code vs the feature's dump D1/D2, region = decoded cells / contours."""
import sys, os, io, re, contextlib
import numpy as np
os.environ.setdefault('R15_OUT', os.path.dirname(os.path.abspath(__file__)))
import decode_replay as D
ROOT = D.ROOT
part = sys.argv[1]; names = sys.argv[2:]
D.LOG.clear(); D.R.LOG.clear(); D.R.DEC = D.DO.regen(part); D.R.PART = part
with contextlib.redirect_stdout(io.StringIO()): g = D.DO.GRebuild()
P = D.to_part(g)
dump = open(os.path.join(ROOT, 'dumps_v2' if D.SRC == 'revdev' else 'dumps_' + D.SRC, part + '.dump.txt'), errors='replace').read()
def dump_feat(n):
    m = re.search(r'^FEATURE \d+ \| ' + re.escape(n) + r' \|.*?(?=^FEATURE \d+ )', dump, re.S | re.M)
    return m.group(0) if m else ''
R_ = D.OracleReplay.__new__(D.OracleReplay); R_.part = P; R_.g = g
for n in names:
    f = P.by_name.get(n)
    if f is None: print(n, 'not in part'); continue
    skf = D.OracleReplay.sketch_feat(R_, f); e = g.ec.get(n) or {}
    txt = dump_feat(n); dims = dict(re.findall(r'DIM (D\d)@' + re.escape(n) + r'@[^=]*= (\S+)', txt))
    sk_name = skf.name if skf is not None else None
    stm = re.search(r'FEATURE -?\d+ \| ' + re.escape(sk_name or '?') + r' \|.*?SKETCH_TO_MODEL (\S+)', dump, re.S) if sk_name else None
    out = dict(feature=n, sketch=sk_name, D=e.get('D_mm'), code=(e.get('end_code_dir1'), e.get('end_code_dir2')), dump_D={k: float(v) * 1e3 for k, v in dims.items()})
    if skf is not None:
        sk = skf.sketch; nrm = np.array(sk.normal, float); org = np.array(sk.trans) * D.MM
        out.update(dec_n=np.round(nrm, 3).tolist(), dec_off=round(float(nrm @ org), 3))
        try: out['cells'] = len(D.FD.sketch_cells(skf))
        except Exception as ex: out['cells'] = repr(ex)[:60]
        if stm:
            v = [float(x) for x in stm.group(1).split(',') if x]
            Rm = np.array(v[:9]).reshape(3, 3); t = np.array(v[9:12]) * 1e3
            dn = Rm[2] if abs(Rm[2] @ nrm) > abs(Rm[:, 2] @ nrm) else Rm[:, 2]
            out.update(dump_n=np.round(dn, 3).tolist(), dump_off=round(float(dn @ t), 3))
            par = abs(abs(dn @ nrm) - 1) < 1e-3; sgn = np.sign(dn @ nrm) or 1
            out['plane'] = 'same' if par and abs(sgn * float(dn @ t) - float(nrm @ org)) < 1e-3 else ('offset' if par else 'normal')
        out['contours'] = len(re.findall(r'CONTOUR \d+', stm.group(0))) if stm else None
    dd = out['dump_D'].get('D1'); dec = (out['D'] or [None])[0]
    out['extent'] = 'n/a' if dd is None else ('same' if dec is not None and abs(dec - dd) < 1e-3 else f'dec {dec} vs dump {dd}')
    print({k: v for k, v in out.items()})

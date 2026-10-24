"""CLI.
    python3 -m sw_gen <dump> [--refs R] [--out DIR] [--no-replay] [--no-audit]
    python3 -m sw_gen --all [--dumps DIR]      (every *.dump.txt, then batch macro + report)
Run from rebuild_dump/ (or with PYTHONPATH=rebuild_dump).
"""
from __future__ import annotations
import argparse, glob, json, os, sys, time, traceback, warnings
import numpy as np

from . import SLDPRT, REBUILD_DUMP
from .model import load_part, parse_refs, find_refs, part_name_from_path, parse_asm_mass, parse_edges, find_edges, edge_curves
from .plan import plan_part, Op
from . import emit

OUT = os.path.join(SLDPRT, 'deliver', 'rebuild_macros')
ASM = os.path.join(SLDPRT, 'dumps_v2', 'rvrn 2.0.asmdump.txt')
RV01_REF = os.path.join(SLDPRT, 'rebuild', 'ref_rv01_asmframe.brep')


def face_audit(dump_path, body, scratch):
    try:
        import face_audit as FA
        from build123d import export_step
        p = os.path.join(scratch, part_name_from_path(dump_path) + '_replay.step')
        export_step(body, p)
        r = FA.audit(FA.faces_from_dump(dump_path), FA.faces_from_step(p))
        c = {k: len(v) for k, v in r.items() if isinstance(v, list)}
        c['dump_patches'] = r['counts']['dump_patches']
        return c
    except Exception as ex:
        return dict(error=f'{type(ex).__name__}: {ex}'[:120])


def mc_iou(a, b, n=40000, seed=1):
    """Monte-Carlo IoU (point classification; robust where OCC booleans give up)."""
    import numpy as np
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    from OCP.gp import gp_Pnt
    bb = a.bounding_box().add(b.bounding_box())
    lo = np.array(tuple(bb.min)); hi = np.array(tuple(bb.max))
    P = lo + np.random.default_rng(seed).random((n, 3)) * (hi - lo)
    ca = BRepClass3d_SolidClassifier(a.wrapped); cb = BRepClass3d_SolidClassifier(b.wrapped)
    ia = ib = 0; both = 0
    for p in P:
        g = gp_Pnt(*p)
        ca.Perform(g, 1e-6); cb.Perform(g, 1e-6)
        x = ca.State() == TopAbs_IN; y = cb.State() == TopAbs_IN
        both += x and y; ia += x or y
    return round(both / max(ia, 1), 4)


def rv01_iou(body):
    try:
        import numpy as np
        from build123d import import_brep, Location
        sys.path.insert(0, REBUILD_DUMP)
        import rv01_from_dump as R
        refp = R.load_ref()
        return mc_iou(body, refp)
    except Exception as ex:
        return f'n/a ({type(ex).__name__})'


ORACLES = {'RV01 Chassis': os.path.join(REBUILD_DUMP, 'ckpt')}


def load_oracle(name):
    """per-feature body/tools of a reference-driven build123d run (rv01_from_dump ckpt), if any."""
    d = ORACLES.get(name)
    out = {}
    if not d or not os.path.isdir(d):
        return out
    import pickle
    for p in glob.glob(os.path.join(d, '*.pkl')):
        try:
            st = pickle.load(open(p, 'rb'))
            out[os.path.basename(p)[:-4]] = dict(body=st['body'], tools=st.get('tools', {}))
        except Exception:
            pass
    return out


STD = {'Front Plane': 2, 'Top Plane': 1, 'Right Plane': 0}     # plane -> mirrored model axis


def mirror_source(part, dump):
    """MirrorStock part -> (source dump path, mirror plane name) or None. The plane is the standard plane
    that maps the source's dump faces onto this part's dump faces."""
    import re
    ms = [f for f in part.features if f.type == 'MirrorStock']
    if not ms:
        return None
    src = re.sub(r'_Mirrored\d*$', '', ms[0].name)
    sd = os.path.join(os.path.dirname(dump), src + '.dump.txt')
    if not os.path.exists(sd):
        return None
    sp = load_part(sd)
    def key(F, ax=None):
        n = np.array(F.params['n'], float); o = np.array(F.params['o'], float)
        if ax is not None:
            n[ax] = -n[ax]; o[ax] = -o[ax]
        n = n if n[np.argmax(np.abs(n))] > 0 else -n
        return tuple(np.round(np.r_[n, n @ o], 5))
    mine = {key(F) for g in part.features for F in (g.faces or []) if F.kind == 'plane'}
    best = None
    for pln, ax in STD.items():
        k = {key(F, ax) for g in sp.features if g.idx >= 0 for F in (g.faces or []) if F.kind == 'plane'}
        sc = len(k & mine)
        if best is None or sc > best[0]:
            best = (sc, pln)
    return sd, best[1], ms[0].name


def build_one(dump, refs=None, out=OUT, replay=True, audit=True, mass=None, scratch='/tmp', use_ref=True):
    name = part_name_from_path(dump)
    part = load_part(dump)
    mirror = mirror_source(part, dump)
    rdump, rname = dump, name
    if mirror:          # derived mirror part: rebuild the source part, then mirror its body
        rdump = mirror[0]; rname = part_name_from_path(rdump)
        part_out = part
        part = load_part(rdump)
    rf = parse_refs(refs or find_refs(rdump))
    ep = find_edges(rdump)
    ed = parse_edges(ep)
    pl = plan_part(part, rf, ed, edge_curves(ep) if ep else [])
    if mirror:
        from .plan import FeatPlan
        pl.plans.append(FeatPlan(mirror[2], 'MirrorStock', 'EMIT', f'mirror of rebuilt {rname} about {mirror[1]}',
                                 [Op('MIRRORPART', [mirror[2], mirror[1]], mirror[2])], {}))
    oracle = load_oracle(rname) if use_ref else {}
    from . import refmesh, chooser
    ref = refmesh.find_ref(rname, part) if use_ref else None
    if ref is not None and ref.fit:
        ref = None      # extents-only fit: orientation ambiguous, never used to choose
    dsel = chooser.selections(rname, [f.id for f in part.features if f.sketch])
    info = dict(part=name, replay=None, oracle=bool(oracle), ref=ref.name if ref else None,
                decoder_sketches=len(dsel), edges_file=bool(ep),
                exact_blend_edges=sum(1 for v in ed.values() for x in v if not x[0].startswith('derived')),
                derived_blend_edges=sum(1 for v in ed.values() for x in v if x[0].startswith('derived')))
    body = None
    if replay:
        from .replay import Replay, insert_expect, vol
        t = time.time()
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                rp = Replay(part, pl, log=lambda *a: None, oracle=oracle, ref=ref, dsel=dsel).run(time_budget=400)
            insert_expect(pl, rp)
            body = rp.body
            if mirror and body is not None:
                import build123d as bd
                body = body.mirror({'Front Plane': bd.Plane.XY, 'Top Plane': bd.Plane.XZ, 'Right Plane': bd.Plane.YZ}[mirror[1]])
            info['replay'] = dict(vol_mm3=round(vol(body), 3), secs=round(time.time() - t, 1),
                                  ok=sum(1 for v in rp.status.values() if v == 'OK'),
                                  steps=len(rp.status),
                                  bad={k: v for k, v in rp.status.items() if v != 'OK'})
        except Exception as ex:
            info['replay'] = dict(error=f'{type(ex).__name__}: {ex}', trace=traceback.format_exc()[-600:])
    m = (mass or {}).get(name)
    rv = (info['replay'] or {}).get('vol_mm3', 0) / 1e9 if info.get('replay') else 0
    header = [Op('PART', [name]).line(),
              Op('FINAL', [rv, m['vol'] if m else 0, m['mass'] if m else 0]).line()]
    lines = emit.op_lines(pl, header)
    os.makedirs(os.path.join(out, 'ops'), exist_ok=True)
    with open(os.path.join(out, 'ops', name + '.ops.txt'), 'w', newline='\r\n', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    with open(os.path.join(out, name + '_rebuild.txt'), 'w', newline='\r\n', encoding='utf-8') as fh:
        fh.write(emit.single_macro(name, lines))
    body_types = [fp for fp in pl.plans if fp.type not in ('ProfileFeature', 'RefPlane')]
    em = [fp for fp in body_types if fp.status == 'EMIT']
    sk = [fp for fp in pl.plans if fp.type == 'ProfileFeature']
    info.update(features=len(body_types), emitted=len(em),
                skipped=[(fp.name, fp.type, fp.reason) for fp in body_types if fp.status != 'EMIT'],
                sketches=len(sk), planes=sum(1 for fp in pl.plans if fp.type == 'RefPlane'),
                mass_vol_mm3=round(m['vol'] * 1e9, 3) if m else None, ops=len(lines))
    sp_ops = [(fp.name, o.args[0], o.meta.get('src', '')) for fp in sk for o in fp.ops if o.kind == 'SPLINE']
    if sp_ops:
        info['splines'] = sp_ops
    bl = {}
    for fp in pl.plans:
        if fp.type in ('Fillet', 'Chamfer') and fp.status == 'EMIT':
            ne = sum(1 for o in fp.ops if o.kind == 'EDGE')
            hm = next((o.meta.get('v4_hints') for o in fp.ops if o.meta.get('v4_hints')), None)
            bl[fp.name] = dict(edge_ops=ne, v4=fp.meta.get('v4_edges', 0), v4_hints=hm)
    info['blends'] = bl
    st = [fp.meta.get('stats', {}) for fp in sk]
    info['sketch_rels'] = f"{sum(s.get('rels_emitted', 0) for s in st)}/{sum(s.get('rels_total', 0) - s.get('dims_total', 0) for s in st)}"
    info['sketch_dims'] = f"{sum(s.get('dims_emitted', 0) for s in st)}/{sum(s.get('dims_in_dump', 0) for s in st)}"
    if body is not None and audit:
        info['face_audit'] = face_audit(dump, body, scratch)
    if body is not None:
        tref = ref if (ref is not None and not mirror) else refmesh.find_ref(name, part_out if mirror else part)
        if tref is not None:
            try:
                info['iou_vs_refmesh'] = round(refmesh.mc_iou(tref, body), 3)
            except Exception as ex:
                info['iou_vs_refmesh'] = f'n/a ({type(ex).__name__})'
    if mirror:
        info['mirror_of'] = [rname, mirror[1]]
    if body is not None and name.startswith('RV01'):
        info['iou_vs_ref'] = rv01_iou(body)
    return info


def main(argv=None):
    ap = argparse.ArgumentParser(prog='sw_gen')
    ap.add_argument('dump', nargs='?')
    ap.add_argument('--refs')
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--no-replay', action='store_true')
    ap.add_argument('--no-audit', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--no-oracle', action='store_true', help='ignore reference meshes/ckpt; decoder region chooser + face evidence only')
    ap.add_argument('--json')
    ap.add_argument('--dumps', default=os.path.join(SLDPRT, 'dumps_v2'))
    ap.add_argument('--scratch', default=os.environ.get('TMPDIR', '/tmp'))
    a = ap.parse_args(argv)
    mass = parse_asm_mass(ASM)
    os.makedirs(a.out, exist_ok=True)
    if a.all:
        import subprocess
        res = []
        jd = os.path.join(a.scratch, 'sw_gen_json'); os.makedirs(jd, exist_ok=True)
        for d in sorted(glob.glob(os.path.join(a.dumps, '*.dump.txt'))):
            nm = part_name_from_path(d)
            jp = os.path.join(jd, nm + '.json')
            print('==', nm, flush=True)
            r = None
            for extra in ([] if a.no_replay else [[]]) + [['--no-replay']]:
                cmd = [sys.executable, '-m', 'sw_gen', d, '--out', a.out, '--scratch', a.scratch, '--json', jp] + extra
                if a.no_audit: cmd.append('--no-audit')
                if a.no_oracle: cmd.append('--no-oracle')
                try:
                    cp = subprocess.run(cmd, cwd=REBUILD_DUMP, capture_output=True, text=True, timeout=1200)
                    if cp.returncode == 0 and os.path.exists(jp):
                        r = json.load(open(jp)); os.remove(jp)
                        if extra: r['note'] = 'replay crashed/timed out; macro emitted without replay volumes'
                        break
                except subprocess.TimeoutExpired:
                    pass
            r = r or dict(part=nm, error='generation failed')
            print('  ', {k: r.get(k) for k in ('emitted', 'features', 'replay', 'mass_vol_mm3', 'note')}, flush=True)
            res.append(r)
        with open(os.path.join(a.out, 'batch_rebuild.txt'), 'w', newline='\r\n', encoding='utf-8') as fh:
            fh.write(emit.batch_macro())
        with open(os.path.join(a.out, 'coverage.json'), 'w') as fh:
            json.dump(res, fh, indent=1, default=str)
        return 0
    if not a.dump:
        ap.error('dump path required')
    r = build_one(a.dump, a.refs, a.out, not a.no_replay, not a.no_audit, mass, a.scratch, not a.no_oracle)
    if a.json:
        json.dump(r, open(a.json, 'w'), default=str)
    else:
        print(json.dumps(r, indent=1, default=str))
    return 0


if __name__ == '__main__':
    sys.exit(main())

"""Emit a SolidWorks VBA macro (late bound) that rebuilds RV01 Chassis from the API dump.

    python3 gen_sw_macro.py      -> ../deliver/RV01_rebuild_macro.txt

Uses dump_parser for sketches/feature order and the rv01_from_dump.py checkpoints (ckpt/*.pkl) for
everything the dump leaves implicit: chosen profile cells, resolved extrude intervals (up-to-* become
blind depths) and fillet/chamfer edges (edges of the body before the blend that are gone after it).
"""
import os, pickle, math
import numpy as np
from build123d import Vector
from dump_parser import parse_dump, blend_params
from rv01_from_dump import sketch_cells, DUMP, HERE, BIG

MM = 1000.0
OUT = os.path.join(HERE, '..', 'deliver', 'RV01_rebuild_macro.txt')
CK = os.path.join(HERE, 'ckpt')
STD = {0: 'Right Plane', 1: 'Top Plane', 2: 'Front Plane'}   # SW default: Right +X, Top +Y, Front +Z
# default sketch axes (x row, y row) of the std planes, from the dump's PLANE lines
STD_AX = {2: (np.array([1., 0, 0]), np.array([0., 1, 0])), 1: (np.array([1., 0, 0]), np.array([0., 0, -1])),
          0: (np.array([0., 0, -1]), np.array([0., 1, 0]))}


def f(x): return f'{x:.9g}'


def vol_of(b):
    try: return b.volume
    except Exception: return 0.0


def ck(name):
    p = os.path.join(CK, name + '.pkl')
    return pickle.load(open(p, 'rb')) if os.path.exists(p) else None


def interior_pt(cell):
    V, T = cell.tessellate(0.05)
    V = np.array([tuple(v) for v in V]); T = np.array(T)
    ar = 0.5 * np.linalg.norm(np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]), axis=1)
    return V[T[np.argmax(ar)]].mean(0)


def removed_edges(prev, new, tol=0.02):
    """midpoints (mm) of edges of prev that are not on the boundary of new (sharp edges the blend consumed)."""
    from build123d import Compound
    keys = {tuple(np.round(tuple(E.position_at(0.5)), 4)) for E in new.edges()}
    shell = Compound(new.faces())
    out = []
    for E in prev.edges():
        m = E.position_at(0.5)
        if tuple(np.round(tuple(m), 4)) in keys: continue
        try:
            if shell.distance_to(m) > tol: out.append(np.array(tuple(m)))
        except Exception:
            pass
    return out


def main():
    part = parse_dump(DUMP)
    feats = [x for x in part.features if not x.suppressed and x.idx >= 0]
    last = ck(feats[-1].name) or {}
    choice = last.get('choice', {})
    L = []; emitted = []; skipped = []
    prev_body = None
    subs = []
    for ft in feats:
        if L: subs.append(L)
        L = [f"' {ft.idx} {ft.name}"]
        st = ck(ft.name)
        body = st['body'] if st else prev_body
        if ft.extrude is not None:
            c = choice.get(ft.name); skf = part.sketch_of(ft)
            if c is None or skf is None or st is None:
                skipped.append(ft.name); L.append(f'  LogLine "SKIP {ft.name}: not resolved in build123d rebuild"')
                continue
            n = np.array(c['dir'], float); ax = int(np.argmax(np.abs(n)))
            lo = min(a for a, b in c['intervals']); hi = max(b for a, b in c['intervals'])
            T = st['tools'][ft.name][1]
            cells = sketch_cells(skf)
            origin = np.array(skf.sketch.trans) * MM
            # cells used = those whose swept interior point lies in the tool solid
            mid = (max(lo, -50) + min(hi, 50)) / 2
            pts = [interior_pt(cl) for cl in cells]
            used = [p for p in pts if T.is_inside(Vector(*(p + n * mid)))]
            thru = hi >= BIG - 1 or lo <= -BIG + 1
            if thru and lo <= -BIG + 1: mode, shift, d1, d2 = 'both_thru', 0.0, 0, 0
            elif thru: mode, shift, d1, d2 = 'thru', max(lo, 0.0), 0, 0
            elif lo < -1e-6 and hi > 1e-6: mode, shift, d1, d2 = 'two', 0.0, hi, -lo
            elif lo >= -1e-6: mode, shift, d1, d2 = 'one', lo, hi - lo, 0
            else: mode, shift, d1, d2 = 'one', hi, hi - lo, 0; n = -n
            sh = n * shift
            plane_d = (origin + sh)[ax]   # offset of the sketch plane along the std axis
            kind = 'Cut' if c['kind'] == 'cut' else 'Boss'
            L.append(f'  \' ---- {ft.name} ({kind}, {mode}, regions {len(used)}/{len(cells)})')
            zn = np.zeros(3); zn[ax] = 1.0
            L.append(f'  If BeginSketch(m, "{STD[ax]}", {f(plane_d / MM)}, {",".join(f(v) for v in zn)}) Then')
            XA, YA = STD_AX[ax]
            def P(p, sk=skf.sketch):   # dump sketch coords -> model -> std-plane sketch coords (u, v, 0)
                q = np.array(sk.to_model(p)) + sh / MM
                return np.array([q @ XA, q @ YA, 0.0])
            SM = '    m.SketchManager.'
            # draw only the boundary of the used regions (merged), so a whole-sketch extrude is valid
            ucells = [cl for cl, p in zip(cells, pts) if T.is_inside(Vector(*(p + n * mid)))] or cells
            Q = lambda v: np.array([(np.array(tuple(v)) + sh) @ XA, (np.array(tuple(v)) + sh) @ YA, 0.0]) / MM
            merged = ucells[0].fuse(*ucells[1:]).clean() if len(ucells) > 1 else ucells[0]
            nseg = 0
            for E in merged.edges():
                gt = str(E.geom_type).split('.')[-1].upper()
                if gt == 'LINE':
                    a, b = Q(E.position_at(0)), Q(E.position_at(1))
                    if np.linalg.norm(a - b) < 1e-9: continue
                    L.append(f'{SM}CreateLine {", ".join(f(v) for v in a)}, {", ".join(f(v) for v in b)}')
                elif gt == 'CIRCLE' and E.is_closed:
                    L.append(f'{SM}CreateCircleByRadius {", ".join(f(v) for v in Q(E.arc_center))}, {f(E.radius / MM)}')
                elif gt == 'CIRCLE':
                    L.append(f'{SM}Create3PointArc {", ".join(f(v) for v in Q(E.position_at(0)))}, '
                             f'{", ".join(f(v) for v in Q(E.position_at(1)))}, {", ".join(f(v) for v in Q(E.position_at(0.5)))}')
                else:   # other curve: polyline
                    ps = [Q(E.position_at(t)) for t in np.linspace(0, 1, 9)]
                    for a, b in zip(ps, ps[1:]):
                        L.append(f'{SM}CreateLine {", ".join(f(v) for v in a)}, {", ".join(f(v) for v in b)}')
                nseg += 1
            L.append(f'    EndSketch m, "{skf.name}"')
            L.append(f'    m.ClearSelection2 True')
            L.append(f'    m.Extension.SelectByID2 gSketch, "SKETCH", 0, 0, 0, False, 0, Nothing, 0')
            L.append(f'    gExpect = {f(vol_of(body))}')
            L.append(f'    DoExtrude m, "{ft.name}", {kind == "Cut"}, "{mode}", {f(d1 / MM)}, {f(d2 / MM)}, {",".join(f(v) for v in n)}')
            L.append('  End If')
            emitted.append(ft.name)
        elif ft.type == 'Fillet' or ft.type.startswith('Chamfer'):
            bp = blend_params(ft)
            es = removed_edges(prev_body, body) if (prev_body is not None and st) else []
            if not es or bp is None or bp[1] is None:
                skipped.append(ft.name); L.append(f'  LogLine "SKIP {ft.name}: no edges recovered"')
            else:
                L.append(f'  \' ---- {ft.name} ({len(es)} edges)')
                L.append('  m.ClearSelection2 True')
                L.append(f'  gExpect = {f(vol_of(body))}')
                for e in es:
                    L.append(f'  SelEdge m, {",".join(f(v / MM) for v in e)}')
                if bp[0] == 'fillet':
                    L.append(f'  DoFillet m, "{ft.name}", {f(bp[1])}, {len(es)}')
                else:
                    L.append(f'  DoChamfer m, "{ft.name}", {f(bp[1])}, {f(bp[2] or math.pi / 4)}, {len(es)}')
                emitted.append(ft.name)
        elif ft.type == 'MirrorPattern':
            pl = [nm for nm, t in ft.parents if t == 'RefPlane']
            srcs = [nm for nm, t in ft.parents if t != 'RefPlane' and nm != ft.name and nm in emitted]
            if not pl or not srcs:
                skipped.append(ft.name); L.append(f'  LogLine "SKIP {ft.name}: no plane/sources"')
            else:
                L.append(f'  gExpect = {f(vol_of(body))}')
                L.append(f'  DoMirror m, "{ft.name}", "{pl[0]}", "{"|".join(srcs)}"')
                emitted.append(ft.name)
        elif ft.type not in ('ProfileFeature', 'RefPlane', 'OriginProfileFeature', 'DetailCabinet') \
                and 'Folder' not in ft.type:
            skipped.append(ft.name); L.append(f'  LogLine "SKIP {ft.name}: type {ft.type}"')
        prev_body = body
    subs.append(L)
    calls, bodies = [], []
    for i, b in enumerate(s for s in subs if len(s) > 1):
        calls.append(f'    On Error Resume Next\n    F{i:03d} m')
        bodies.append(f'Sub F{i:03d}(ByVal m As Object)\n  On Error Resume Next\n' + '\n'.join(b[1:]) + '\nEnd Sub\n')
    tpl = open(os.path.join(HERE, 'sw_macro_template.bas')).read()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', newline='\r\n').write(tpl.replace("'@@CALLS@@", '\n'.join(calls)).replace("'@@FEATURES@@", '\n'.join(bodies)))
    print(f'emitted {len(emitted)}/{len(emitted) + len(skipped)} solid features; skipped: {skipped}')


if __name__ == '__main__':
    main()

"""run decode_replay per part in parallel processes -> results/<part>.json, then merge to decode_replay.json/.txt"""
import sys, os, json, glob, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.environ.get('R16_SRC', 'revdev'); SUF = ('' if SRC == 'revdev' else '_' + SRC) + (('_' + os.environ['R18_TAG']) if os.environ.get('R18_TAG') else '')
os.makedirs(os.path.join(HERE, 'results' + SUF), exist_ok=True); os.makedirs(os.path.join(HERE, 'breps' + SUF), exist_ok=True)
ONE = '''import sys, json, traceback; sys.argv=['x']; import decode_replay as D
p=sys.argv_part if False else %r
try: r=D.run_part(p)
except Exception as ex: r=dict(iou=0.0, note=repr(ex)[:300], tb=traceback.format_exc()[-1500:])
json.dump(r, open(%r,'w'), indent=1, default=float)'''
SNAP = None
def crash_policy(crashes, skip, fx, limit=2):
    """r18: OCC segfaults are intermittent (RV16 Fillet1 crashed 2 of 3 runs): the feature a process died
    on is retried, and skipped only after it crashed `limit` times."""
    crashes[fx] = crashes.get(fx, 0) + 1
    if crashes[fx] >= limit and fx not in skip: skip.append(fx)
    return skip
def snapshot():
    """run from a frozen copy of the wip_r18 sources so edits during a run cannot break it."""
    import shutil, tempfile
    d = tempfile.mkdtemp(prefix='r16snap_')
    for f in glob.glob(os.path.join(HERE, '*.py')): shutil.copy(f, d)
    return d
def one(p):
    out = os.path.join(HERE, 'results' + SUF, p + '.json')
    if os.path.exists(out) and os.environ.get('R16_RESUME', '1') == '1': return p, json.load(open(out))   # r18: resume by default (container restarts)
    if os.path.exists(out): os.remove(out)
    prog = os.path.join(SNAP, p + '.progress'); skip = []; crashes = {}
    import time as _t; t_start = _t.time(); tmo_all = 1.5 * int(os.environ.get('R16_TMO', 7000))
    for attempt in range(7):   # an OCC segfault kills the process: retry without the feature it died on
        tmo = int(min(int(os.environ.get('R16_TMO', 7000)), tmo_all - (_t.time() - t_start)))   # r18: retries share 1.5x the timeout
        if tmo < 30: break
        env = dict(os.environ); env.setdefault('R18_PBUDGET', str(0.55 * tmo)); env.setdefault('R18_FBUDGET', str(max(30, min(240, tmo / 10))))
        env = dict(env, R18_PARTIAL=os.path.join(SNAP, p + '.partial'), R15_OUT=HERE, R15_TOOLS=os.path.abspath(os.path.join(HERE, '..')), R15_PROGRESS=prog, R15_SKIP='|'.join(skip))
        try: subprocess.run([sys.executable, '-c', ONE % (p, out)], cwd=SNAP, env=env, timeout=tmo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.TimeoutExpired: break
        if os.path.exists(out) or not os.path.exists(prog): break
        crash_policy(crashes, skip, open(prog).read().strip())
    pj = os.path.join(SNAP, p + '.partial.json')
    if not os.path.exists(out) and os.path.exists(pj):   # r18: killed at the timeout: score the last checkpoint body
        try:
            subprocess.run([sys.executable, '-c', 'import sys, json; sys.argv=["x"]; import decode_replay as D; json.dump(D.score_partial(%r, %r), open(%r, "w"), indent=1, default=float)' % (p, pj, out)],
                           cwd=SNAP, env=dict(os.environ, R15_OUT=HERE, R15_TOOLS=os.path.abspath(os.path.join(HERE, '..'))), timeout=600, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception: pass
    r = json.load(open(out)) if os.path.exists(out) else dict(iou=0.0, note='crashed/timeout')
    if not os.path.exists(out): json.dump(r, open(out, 'w'))
    print(p, r.get('iou'), r.get('oracle_iou'), r.get('ops'), r.get('seconds'), r.get('note', ''), flush=True); return p, r
def merge():
    res = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'results' + SUF, '*.json'))): res[os.path.basename(f)[:-5]] = json.load(open(f))
    json.dump(res, open(os.path.join(HERE, 'decode_replay' + SUF + '.json'), 'w'), indent=1, default=float)
    lines = []; v = []
    for p, r in res.items():
        lines.append(f"{p}\t{r.get('iou')}\t{r.get('ref')}\toracle={r.get('oracle')} {r.get('oracle_iou')}\t{r.get('ops')}\t{r.get('note','')}")
        if r.get('ref') or (r.get('note') and r.get('iou') is not None): v.append(r.get('iou') or 0)
    lines.append(f'MEAN IoU {sum(v)/max(1,len(v)):.4f} parts {len(v)}')
    open(os.path.join(HERE, 'decode_replay' + SUF + '.txt'), 'w').write('\n'.join(lines) + '\n'); print(lines[-1])
if __name__ == '__main__':
    sel = sys.argv[1:]
    parts = sorted(os.path.basename(p)[:-7] for p in glob.glob(os.path.join(ROOT, SRC, '*.SLDPRT')))
    parts = [p for p in parts if not sel or any(p.startswith(x) for x in sel)]
    ex_ = [x for x in os.environ.get('R22_EXCLUDE', '').split('|') if x]   # r22: parts another run_all handles
    parts = [p for p in parts if not any(p.startswith(x) for x in ex_)]
    parts.sort(key=lambda p: -os.path.getsize(os.path.join(ROOT, SRC, p + '.SLDPRT')))
    SNAP = snapshot()
    with ThreadPoolExecutor(int(os.environ.get('R15_J', 4))) as ex: list(ex.map(one, parts))
    merge()

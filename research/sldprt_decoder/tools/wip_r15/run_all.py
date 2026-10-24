"""run decode_replay per part in parallel processes -> results/<part>.json, then merge to decode_replay.json/.txt"""
import sys, os, json, glob, subprocess
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
os.makedirs(os.path.join(HERE, 'results'), exist_ok=True); os.makedirs(os.path.join(HERE, 'breps'), exist_ok=True)
ONE = '''import sys, json, traceback; sys.argv=['x']; import decode_replay as D
p=sys.argv_part if False else %r
try: r=D.run_part(p)
except Exception as ex: r=dict(iou=0.0, note=repr(ex)[:300], tb=traceback.format_exc()[-1500:])
json.dump(r, open(%r,'w'), indent=1, default=float)'''
SNAP = None
def snapshot():
    """run from a frozen copy of the wip_r15 sources so edits during a run cannot break it."""
    import shutil, tempfile
    d = tempfile.mkdtemp(prefix='r15snap_')
    for f in glob.glob(os.path.join(HERE, '*.py')): shutil.copy(f, d)
    return d
def one(p):
    out = os.path.join(HERE, 'results', p + '.json')
    if os.path.exists(out): os.remove(out)
    prog = os.path.join(SNAP, p + '.progress'); skip = []
    for attempt in range(5):   # an OCC segfault kills the process: retry without the feature it died on
        env = dict(os.environ, R15_OUT=HERE, R15_TOOLS=os.path.abspath(os.path.join(HERE, '..')), R15_PROGRESS=prog, R15_SKIP='|'.join(skip))
        subprocess.run([sys.executable, '-c', ONE % (p, out)], cwd=SNAP, env=env, timeout=7000, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(out) or not os.path.exists(prog): break
        skip.append(open(prog).read().strip())
    r = json.load(open(out)) if os.path.exists(out) else dict(iou=0.0, note='crashed/timeout')
    print(p, r.get('iou'), r.get('oracle_iou'), r.get('ops'), r.get('seconds'), r.get('note', ''), flush=True); return p, r
def merge():
    res = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'results', '*.json'))): res[os.path.basename(f)[:-5]] = json.load(open(f))
    json.dump(res, open(os.path.join(HERE, 'decode_replay.json'), 'w'), indent=1, default=float)
    lines = []; v = []
    for p, r in res.items():
        lines.append(f"{p}\t{r.get('iou')}\t{r.get('ref')}\toracle={r.get('oracle')} {r.get('oracle_iou')}\t{r.get('ops')}\t{r.get('note','')}")
        if r.get('ref') or (r.get('note') and r.get('iou') is not None): v.append(r.get('iou') or 0)
    lines.append(f'MEAN IoU {sum(v)/max(1,len(v)):.4f} parts {len(v)}')
    open(os.path.join(HERE, 'decode_replay.txt'), 'w').write('\n'.join(lines) + '\n'); print(lines[-1])
if __name__ == '__main__':
    sel = sys.argv[1:]
    parts = sorted(os.path.basename(p)[:-7] for p in glob.glob(os.path.join(ROOT, 'revdev', '*.SLDPRT')))
    parts = [p for p in parts if not sel or any(p.startswith(x) for x in sel)]
    parts.sort(key=lambda p: -os.path.getsize(os.path.join(ROOT, 'revdev', p + '.SLDPRT')))
    SNAP = snapshot()
    with ThreadPoolExecutor(int(os.environ.get('R15_J', 4))) as ex: list(ex.map(one, parts))
    merge()

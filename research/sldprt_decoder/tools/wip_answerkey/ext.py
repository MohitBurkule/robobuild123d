import sys,glob,os
sys.path.insert(0,os.path.dirname(__file__)+'/tools')
from sldprt import streams as S
for p in sorted(glob.glob(os.path.dirname(__file__)+'/revdev/*.SLDPRT')):
    d=open(p,'rb').read(); best=None
    for s in S.all_streams(d):
        if S.classify(s)=='features' and (best is None or len(s['data'])>len(best)): best=s['data']
    n=os.path.basename(p)[:-7]
    if best: open(os.path.dirname(__file__)+'/fs/'+n+'.bin','wb').write(best)
    print(n, len(best) if best else None)

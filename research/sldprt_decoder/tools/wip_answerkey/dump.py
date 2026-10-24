import sys,pickle
sys.path.insert(0,'/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import streams as S
for name in sys.argv[1:]:
    data=open('/mnt/project-files/robot-cad/research/sldprt/revdev/'+name+'.SLDPRT','rb').read()
    feat=None
    for s in S.all_streams(data):
        if S.classify(s)=='features' and (feat is None or len(s['data'])>len(feat)): feat=s['data']
    open(name.split()[0]+'.feat','wb').write(feat)

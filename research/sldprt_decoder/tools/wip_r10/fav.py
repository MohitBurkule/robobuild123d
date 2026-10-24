import sys
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V, objnum as ON
R='/mnt/project-files/robot-cad/research/sldprt/revdev/'
d=V.feature_stream(R+sys.argv[1]+'.SLDPRT'); ev,_=ON.numbering(d)
k=0
for i,e in enumerate(ev):
    if e.name==sys.argv[2] and e.kind in('new','def'):
        end=ev[i+1].offset if i+1<len(ev) else len(d)
        print(hex(e.offset), end-e.end, ev[i+1].name if i+1<len(ev) else '')
        b=d[e.end:min(end,e.end+int(sys.argv[3]))]
        for j in range(0,len(b),32): print('   ',b[j:j+32].hex(' ',4))
        k+=1
        if k>=4: break

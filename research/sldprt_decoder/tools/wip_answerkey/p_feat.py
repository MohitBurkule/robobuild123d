import sys,glob,os,struct,re
sys.path.insert(0,'tools')
from sldprt import answer_key as A
tot=ok=okfirst=0; bad=[]
for p in sorted(glob.glob('dumps/*.txt')):
    D=A.parse(p); n=os.path.basename(p)[:-9]
    d=open('fs/'+n+'.bin','rb').read()
    for f in D.features+[c for f in D.features for c in f.children]:
        enc=f.name.encode('utf-16-le'); pat=b'\xff\xfe\xff'+bytes([len(f.name)])+enc
        occ=[m.end() for m in re.finditer(re.escape(pat),d)]
        tot+=1
        ids=[struct.unpack_from('<I',d,e+8)[0] for e in occ if e+12<=len(d)]
        if f.id in ids: ok+=1
        if ids and ids[0]==f.id: okfirst+=1
        else: bad.append((n[:12],f.name,f.type,f.id,ids[:4]))
print(tot,ok,okfirst)
for b in bad[:30]: print(b)

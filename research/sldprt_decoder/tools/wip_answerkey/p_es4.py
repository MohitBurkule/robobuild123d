exec(open('p_es3.py').read().split('import collections\nst=')[0])
import collections
samples=[]
for n,D,d in parts():
    R=regions(D,d); tag=es_tag(d,R); cd=d.find(CD)
    for f,s,e in R:
        if not f.extrude: continue
        anc=[]
        if s<=cd<e: anc.append(cd+len(CD)-2)
        if tag: anc+=[s+m.start() for m in re.finditer(re.escape(struct.pack('<H',tag)+b'\x00\x00')+b'[\x00\x01]\x00',d[s:e])]
        anc=sorted(set(anc))
        if anc: samples.append((f.extrude,d,anc,n,f.name))
print(len(samples), collections.Counter(len(a) for _,_,a,_,_ in samples))
for fld in ['both','reverse','end2','merge','thin']:
    best=[]
    for k in range(0,900):
        ok=sum(1 for x,d,a,_,_ in samples if a[0]+k<len(d) and d[a[0]+k]==int(x[fld]))
        best.append((ok,k))
    best.sort(reverse=True); print(fld,collections.Counter(int(x[fld]) for x,_,_,_,_ in samples),best[:5])
# depth: find offsets where f64 equals d1
for fld in ['d1','d2']:
    c=collections.Counter()
    for x,d,a,_,_ in samples:
        if x[fld]==0: continue
        for k in range(0,1200):
            if a[0]+k+8<=len(d) and abs(f64(d,a[0]+k)-x[fld])<1e-12: c[k]+=1
    print(fld,sum(1 for x,_,_,_,_ in samples if x[fld]),c.most_common(6))
DIMV = re.compile(rb'\xff\xfe\xff(.)((?:D\x00)(?:[0-9]\x00){1,3}).{0,24}?\xff\xfe\xff\x00\x00\x00(.{8})', re.S)
st=collections.Counter()
for x,d,a,n,fn in samples:
    S=a[0]
    m=DIMV.search(d,S,S+3000)
    v=struct.unpack('<d',m.group(3))[0] if m else None
    if x['d1']!=0: st['d1',v is not None and abs(v-x['d1'])<1e-12]+=1
    else: st['nod1_dim_dist', (m.start()-S) if m else None]+=0
    st['both_rule', x['both']==(d[S+22]!=0 or d[S+18]==6) ]+=1
    st['both_rule2', x['both']==(d[S+22]!=0)]+=1
    if x['both']!=(d[S+22]!=0): print(n,fn,x,d[S+18],d[S+22])
print(st)

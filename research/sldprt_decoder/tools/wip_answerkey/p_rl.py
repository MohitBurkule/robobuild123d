exec(open('p_rel5.py').read().split('st=collections')[0])
c=collections.Counter()
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        rs=[]
        for m in HDR.finditer(d,s,e):
            sl,j=IR.read_slots(d,m.end())
            if sl: rs.append((m.start(),j,len(m.group(4))==4))
        for (a,j,g),(b,_,g2) in zip(rs,rs[1:]):
            if g and g2: c[b-j]+=1
print(c.most_common(10))

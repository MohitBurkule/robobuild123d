exec(open('p_rel5.py').read().split('st=collections')[0])
shown=collections.Counter()
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        rs=[]
        for m in HDR.finditer(d,s,e):
            sl,j=IR.read_slots(d,m.end())
            if sl: rs.append((m.start(),j,len(m.group(4))==4,m.group(1)[0],len(sl)))
        for (a,j,g,t,ns),(b,_,g2,_,_) in zip(rs,rs[1:]):
            if g and g2 and shown[b-j]<2 and b-j in (68,69,28,29,31,89):
                shown[b-j]+=1; print(b-j,t,ns,d[j:b].hex(' '))

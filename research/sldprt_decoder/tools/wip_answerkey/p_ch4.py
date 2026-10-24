from choose2 import *
st=collections.Counter()
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        ch=choosers(d,s,e,f.id)
        for c in ch:
            st['orphan' if c.get('orphan') else 'chooser']+=1
            st['ncont',len(c['contours'])]+=1
        st['sk_with',bool(ch), len([x for x in f.contours if x[0]])>1]+=1
print(sorted(st.items(),key=str))

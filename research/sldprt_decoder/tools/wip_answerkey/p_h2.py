from regsel import *
pn,sn=sys.argv[1],sys.argv[2]
for n,D,d in parts():
    if n!=pn: continue
    for f,s,e in regions(D,d):
        if f.name!=sn: continue
        for m in SIG.finditer(d,s,e):
            q=m.start(); print(hex(q), d[q-16:q].hex(' '))
        print(hex(d.find(b'moContourChooser_c',s,e)))

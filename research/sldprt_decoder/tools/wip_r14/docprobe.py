import sys, struct; sys.path.insert(0, '.')
from sldprt import streams as S
R = '../dumps_ab/'
def find(f, pats):
    d = open(R + f + '.SLDPRT', 'rb').read()
    for k, s in enumerate(S.all_streams(d)):
        dd = s['data']; c = S.classify(s)
        for nm, p in pats.items():
            j = dd.find(p)
            while j >= 0:
                print(f[:28], k, c, len(dd), nm, j, dd[max(0, j-24):j].hex(), '|', dd[j:j+len(p)+40].hex())
                j = dd.find(p, j + 1)
for f in sys.argv[2:]:
    find(f, eval(sys.argv[1]))

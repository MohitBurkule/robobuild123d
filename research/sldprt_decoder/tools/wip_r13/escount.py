import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import esdiag2 as E
r=E.run(); print(sys.argv[1], sum(v[0] for v in r.values()), len(r))
for k,v in r.items():
    if not v[0]: print('  ',k,v)

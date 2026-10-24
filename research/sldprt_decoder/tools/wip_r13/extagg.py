import json,sys;from collections import Counter,defaultdict
o=json.load(open('extcensus.json'))
def key(k,S): return 'X%d'%(S-int(k[2:])) if k.startswith('S-') else k
tot=Counter(); N=Counter(); L=defaultdict(Counter); G=defaultdict(Counter); EX={}
T=sum(v['unc'] for v in o.values())
for n,v in o.items():
  g=n.split('_')[1]
  for k,u in v['U'].items():
    kk=key(k,v['S']); tot[kk]+=u; N[kk]+=v['N'][k]; G[kk][g]+=v['N'][k]
    for l,c in v['L'][k]: L[kk][l]+=c
    EX.setdefault(kk,(n,v['EX'][k]))
print('uncovered',T)
for k,u in tot.most_common(int(sys.argv[1]) if len(sys.argv)>1 else 25):
  print(f'{k:24s} {u:7d} {100*u/T:5.1f}% n={N[k]} lens={L[k].most_common(3)} groups={len(G[k])}')

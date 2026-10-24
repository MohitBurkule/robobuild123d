import json,sys
for f in sys.argv[1:]:
    c=json.load(open(f))['coverage']
    for s in ('train','validation'):
        v=[x['coverage_pct'] for x in c.values() if x['split']==s]; print(f,s,round(sum(v)/len(v),2))

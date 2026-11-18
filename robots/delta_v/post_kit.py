import json
p='robots/delta_v/spec.json'
s=json.load(open(p));K=json.load(open('robots/delta_v/kit.json'))
r=K['weapon']['radius'];t=K['weapon']['hub']
for q in s['parts']:
    if q['id']=='weapon':
        thin={'type':'place','shape':{'type':'cylinder','radius':r,'height':4.0},'at':[0,0,0],'rot':[0,0,0]}
        base=q['shape']
        q['shape']={'type':'union','items':[base,{'type':'place','shape':{'type':'cylinder','radius':12.0,'height':t},'at':[0,0,0],'rot':[0,0,0]}]}
        q['color']='#d8e04a'
    if q['id'].startswith('wheel'):
        q['color']='#d9c36a'; q['at'][2]=8.0
    if q['id'].startswith('fork'):
        q['at'][2]+=0
json.dump(s,open(p,'w'),indent=1)

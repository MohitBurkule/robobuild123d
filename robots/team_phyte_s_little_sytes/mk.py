import json,subprocess
S='robots/team_phyte_s_little_sytes'
k=json.load(open(S+'/kit.json'))
k['body'].update(height=24,ramp=90,width=112,length=118,clearance=1)
k['wheels'].update(radius=8,width=9,y=[-48],outside=True)
json.dump(k,open(S+'/kit.json','w'),indent=1)
subprocess.run(['python3','-m','robot','kit',S+'/kit.json',S+'/spec2.json'],check=True)
s=json.load(open(S+'/spec2.json'));o=json.load(open(S+'/spec.json'))
s['reference']=o['reference'];s['cluster']=2
for p in s['parts']:
    if p['kind']=='wheel': p['at'][2]=p['at'][2]+14
json.dump(s,open(S+'/spec.json','w'),indent=1)

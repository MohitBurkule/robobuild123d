"""Hand-edit after `robot gen build`: strip bridge/wedge, lay the bar across x, add purple wheel pods + disc hub."""
import json,sys
f='robots/th_under_er/spec.json'
s=json.load(open('out/hspin_bar.json'))
drop={'insert_c0','insert_c1','insert_c2','insert_c3','top_bridge','wbearing','lock_plate','wedge'}
drop|={p['id'] for p in s['parts'] if p['id'].startswith(('insert_br','insert_bl','insert_w'))and p['id']!='insert_wm'}
drop|={'bolt_wma','bolt_wmb','bolt_c0','bolt_c1','bolt_c2','bolt_c3','bolt_br0','bolt_br1','bolt_bl0','bolt_bl1','bolt_w0','bolt_w1','bolt_w2','bolt_w3'}
s['parts']=[p for p in s['parts'] if p['id'] not in drop]
s['fasteners']=[x for x in s['fasteners'] if x['id'] not in drop]
s.pop('weapon_lock',None)
for p in s['parts']:
    if p['id']=='weapon':
        p['joint']['default']=90; p['at'][0]=-10.6; p['joint']['pivot'][0]=-10.6
        sh=p['shape']['shape']
        sh['base']['points']=[[-28,-4],[22,-4],[24,-14],[30,-26],[22,-30],[14,-20],[12,4],[-28,4]]
        sh['cut']=[{"type":"place","shape":{"type":"cylinder","radius":3.0,"height":5.0},"at":[22,-16,0],"rot":[0,0,0]}]
    if p['id']=='weapon_motor': p['at'][1]=18.0
json.dump(s,open(f,'w'),indent=1)
s=json.load(open(f))
for sx,n in((1,'r'),(-1,'l')):
    s['parts'].append({"id":"pod_"+n,"kind":"structure","material":"pla","process":"fdm","color":"#5b2bd6","print_orientation":"+z",
     "shape":{"type":"box","size":[20,34,16]},"at":[sx*55.0,-20.0,0.0],"rot":[0,0,0],"label":"purple printed wheel pod"})
s['parts'].append({"id":"hub_disc","kind":"structure","material":"pla","process":"fdm","color":"#e8e8ee","print_orientation":"+z",
 "shape":{"type":"cylinder","radius":16,"height":2.0},"at":[0.0,18.0,9.9],"rot":[0,0,0],"label":"white centre disc cap over the weapon motor"})
json.dump(s,open(f,'w'),indent=1)

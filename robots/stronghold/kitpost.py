import json,sys
f=sys.argv[1]; s=json.load(open(f)); k=json.load(open('robots/stronghold/kit.json'))
L=k['body']['length'];W=k['body']['width'];H=k['body']['height'];R=k['wheels']['radius'];zb=-R+k['body']['clearance']
y1=L/2; zt=zb+H
s['parts']=[p for p in s['parts'] if not p['id'].startswith('fork_')]
def prism(pts,h,x,pid,kind,mat,proc,col):
    return {"id":pid,"kind":kind,"material":mat,"process":proc,"color":col,"at":[x,0,0],"rot":[0,0,0],
     "shape":{"type":"place","shape":{"type":"prism","points":pts,"height":h},"at":[0,0,0],"rot":[90,0,90]}}
for i,x in enumerate((-W/2+22,W/2-22)):
    # sloped tapered fork: starts on front plate, tip near floor
    s['parts'].append(prism([[y1-4,zt-14],[y1-4,zt-8],[y1+52,-R+1.5],[y1+40,-R+0.5],[y1+38,-R+6]],3.0,x,f'fork_{i}','wedge','titanium','laser','#c9cdd3'))
    # TPU arch over the top, front to rear, rising above deck
    s['parts'].append(prism([[y1-2,zt-16],[y1+8,zt-6],[y1+4,zt+8],[y1-14,zt+16],[-L/2+16,zt+16],[-L/2+16,zt+8],[y1-12,zt+8],[y1-2,zt+2],[y1-2,zt-4]],7.0,x-3.5+ (0),f'arch_{i}','armor','tpu','fdm','#111'))
    # corner foot
    xf=(-1 if i==0 else 1)*(W/2-6)
    s['parts'].append(prism([[y1,-R+0.5],[y1+22,-R+0.5],[y1+4,-R+14],[y1,-R+14]],12.0,xf,f'foot_{i}','wedge','tpu','fdm','#1a1a1a'))
# rear electronics strip
s['parts'].append({"id":"pcb","kind":"armor","material":"petg","process":"fdm","color":"#1d6b3a","at":[0,-L/2+14,zt+3],"rot":[0,0,0],"shape":{"type":"box","size":[W*0.5,12,6]}})
json.dump(s,open(f,'w'),indent=1)

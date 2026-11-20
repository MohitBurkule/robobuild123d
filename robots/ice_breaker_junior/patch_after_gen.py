import json,sys
src,dst=sys.argv[1:3]
TARGET=float(sys.argv[3]) if len(sys.argv)>3 else 6.0
HUB=float(sys.argv[4]) if len(sys.argv)>4 else 30.0
TIP=float(sys.argv[5]) if len(sys.argv)>5 else 66.0
s=json.load(open(src))
P={p['id']:p for p in s['parts']}
dy=TARGET-P['weapon_motor']['at'][1]
P['weapon_motor']['at'][1]+=dy
b=P['wbearing']['shape']; b['at'][1]+=dy
for u in('upright_r','upright_l'):
    P[u]['shape']={"type":"place","shape":P[u]['shape'],"at":[0,dy,0],"rot":[0,0,0]}
for f in('fork_l','fork_r'):
    pr=P[f]['shape']['base']['shape']['shape']
    pr['points']=[[10.0,-6.7],[10.0,0.3],[40.0,0.3],[TIP,-8.9],[TIP,-10.4]]
w=P['weapon']
w['shape']={"type":"union","items":[w['shape'],{"type":"cylinder","radius":7.0,"height":HUB}]}

for sg,n in((1,'l'),(-1,'r')):
    m=P['motor_'+n]; m['at'][0]=sg*41.4; m['at'][1]=-33.0
    w_=P['wheel_'+n]; w_['at'][0]=sg*58.4; w_['at'][1]=-33.0; w_['at'][2]=3.0
    w_['shape']=json.loads(json.dumps(w_['shape']).replace('"radius": 11.0','"radius": 14.0'))
P['wesc']['at'][1]=-8.0
json.dump(s,open(dst,'w'),indent=1)
print('dy',dy)

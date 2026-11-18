import json,sys
p=sys.argv[1]; s=json.load(open(p))
for q in s['parts']:
    if q['kind']=='wedge':
        x=q['shape']['at'][0]; L=62.0
        q['shape']={"type":"place","shape":{"type":"box","size":[9.0,L,1.5]},"at":[0,L/2,0],"rot":[0,0,0]}
        q['at']=[x*1.0,38.0,-3.0]; q['rot']=[-30,0,0]
s['reference']=[{"image":f"reference/ice_breaker_junior.{f}.webp","view":"iso","mask":f"reference/ice_breaker_junior.{f}_mask.png","approximate":True} for f in("aws74","aws76","aws77")]
json.dump(s,open(p,'w'),indent=1)

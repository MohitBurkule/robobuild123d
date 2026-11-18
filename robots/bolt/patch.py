import json,copy,sys
p=sys.argv[1]
s=json.load(open(p))
parts=s['parts']
wl=[q for q in parts if q['id']=='wheel_l'][0]
wr=[q for q in parts if q['id']=='wheel_r'][0]
def idler(src,pid,x):
    d=copy.deepcopy(src); d['id']=pid; d['at']=[x,22.0,0.0]; d.pop('joint',None); d.pop('parent',None)
    d['label']='idler wheel (unpowered, on a pin)'
    return d
parts.append(idler(wl,'idler_l',34.4))
parts.append(idler(wr,'idler_r',-34.4))
s['connections'].append({"a":"idler_l","b":"chassis_bottom","method":"pin","reason":"Unpowered idler wheel turning on a 2 mm pin set into the chassis side, carries load only, no drive torque"})
s['connections'].append({"a":"idler_r","b":"chassis_bottom","method":"pin","reason":"Unpowered idler wheel turning on a 2 mm pin set into the chassis side, carries load only, no drive torque"})
s['reference']=[
 {"image":"reference/bolt.aws57.webp","mask":"reference/bolt.aws57.webp_mask.png","view":"iso","approximate":True},
 {"image":"reference/bolt.aws63.webp","mask":"reference/bolt.aws63.webp_mask.png","view":"iso","approximate":True}]
json.dump(s,open(p,'w'),indent=1)

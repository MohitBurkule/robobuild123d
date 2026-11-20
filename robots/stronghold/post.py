# post-build patch: replace the full-width ramp with two small corner shovels (photo: forks + corner wedgelets)
import json,sys
f=sys.argv[1]; s=json.load(open(f))
for p in s['parts']:
    if p['id']=='wedge':
        def sh(x): return {"type":"place","shape":{"type":"place","shape":{"type":"prism","points":[[35.5,-2],[36,0],[50,-6],[50,-9]],"height":10.0},"at":[0,0,0],"rot":[90,0,90]},"at":[x,0,0],"rot":[0,0,0]}
        p['shape']={"type":"union","items":[sh(-36),sh(36)]}
        p['label']='two printed corner shovels'
json.dump(s,open(f,'w'),indent=1)

cd /tmp/work9_stronghold
python3 -m robot kit robots/stronghold/kit.json robots/stronghold/spec.json 2>&1|tail -1
python3 - <<'P'
import json
f='robots/stronghold/spec.json';s=json.load(open(f))
s['reference']=json.load(open('robots/stronghold/intent.json'))['reference']
json.dump(s,open(f,'w'),indent=1)
P
python3 -m robot likeness robots/stronghold/spec.json 2>&1 | grep FAIL\|PASS|cut -c1-260
python3 -m robot diff-photo robots/stronghold/spec.json >/dev/null 2>&1

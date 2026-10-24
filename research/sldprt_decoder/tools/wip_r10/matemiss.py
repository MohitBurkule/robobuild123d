import sys, json, os
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import mate_check as MC
B='/mnt/project-files/robot-cad/research/sldprt/'
comps, mates = MC.parse_asmdump(B+'dumps_v2/rvrn 2.0.asmdump.txt')
dec = json.load(open(B+'decoded/rvrn 2.0.mates_full.json'))
by={m['name']:m for m in dec['mates']}
print(sorted(comps)[:60])
for m in mates:
    dm=by[m['name']]
    for e in m['ents']:
        de=dm['entities'][e['i']] if e['i']<len(dm['entities']) else {}
        top=e['comp'].split('/')[0]
        if de.get('instance_resolved')!=top:
            print(m['name'], e['i'], 'want',top,'got',de.get('instance_resolved'), de.get('instance_how'), de.get('component_path'), de.get('instance_current'))

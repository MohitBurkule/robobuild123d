import sys,collections
sys.path.insert(0,'/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import item_relations as IR
R='/mnt/project-files/robot-cad/research/sldprt/'
for p in sys.argv[1:]:
    o=IR.decode_part(R+'revdev/'+p+'.SLDPRT',R+'decoded/'+p+'.json')
    c=collections.defaultdict(collections.Counter)
    for s in o['sketches']:
        for r in s['relations']: c[r['type']][r['verified']]+=1
    print(p,o['tag_roles'],o['totals'])
    for k,v in sorted(c.items()): print('   ',k,dict(v))

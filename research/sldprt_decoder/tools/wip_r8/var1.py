import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
import harness, json
_old = ON.ext_ok
def ext_ok2(d, o):
    if _old(d, o): return True
    if d[o + 2:o + 5] == b'\xff\xfe\xff': return True
    if d[o - 4:o] == b'\x01\x00\x00\x00' and d[o + 4:o + 6] == b'\x00\x00': return True
    return False
if 'base' not in sys.argv: ON.ext_ok = ext_ok2
r, per = harness.run(corpus='-c' in sys.argv)
print(json.dumps(r))

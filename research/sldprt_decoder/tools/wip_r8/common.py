import sys, pickle, struct
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import fstream as FS, objnum as ON
CACHE = '/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/all.pkl'
_D = None
def load():
    global _D
    if _D is None:
        _D = {k: v for k, v in pickle.load(open(CACHE, 'rb')).items() if v}
    return _D
def u16(d, o): return struct.unpack_from('<H', d, o)[0]

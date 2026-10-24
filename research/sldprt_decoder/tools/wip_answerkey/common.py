import sys,glob,os,struct,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))+'/tools')
from sldprt import answer_key as A
MARK = re.compile(rb'\xff\xff\x1f\x00\x03.{8}\x00\x00\x80\xbf', re.S)
def parts():
    for p in sorted(glob.glob(os.path.dirname(os.path.abspath(__file__))+'/dumps/*.txt')):
        n=os.path.basename(p)[:-9]
        yield n, A.parse(p), open(os.path.dirname(os.path.abspath(__file__))+'/fs/'+n+'.bin','rb').read()
def cpos(d,name):
    pat=b'\xff\xfe\xff'+bytes([len(name)])+name.encode('utf-16-le')
    return [m.start() for m in re.finditer(re.escape(pat),d)]
def regions(D,d):
    """top-level feature -> (start,end) using header CString whose id matches."""
    out=[]
    for f in D.top():
        for s in cpos(d,f.name):
            e=s+4+2*len(f.name)
            if e+12<=len(d) and struct.unpack_from('<I',d,e+8)[0]==f.id:
                out.append([s,f]); break
    out.sort(key=lambda x:x[0])
    return [(f,s,(out[k+1][0] if k+1<len(out) else len(d))) for k,(s,f) in enumerate(out)]
def u16(d,o): return struct.unpack_from('<H',d,o)[0]
def u32(d,o): return struct.unpack_from('<I',d,o)[0]
def i32(d,o): return struct.unpack_from('<i',d,o)[0]
def f64(d,o): return struct.unpack_from('<d',d,o)[0]

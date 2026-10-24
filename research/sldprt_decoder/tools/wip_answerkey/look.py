import sys,re,struct
sys.path.insert(0,'tools')
from sldprt import sketch as SK
d=open('fs/'+sys.argv[1]+'.bin','rb').read()
for m in SK.MARK.finditer(d):
    s=m.start()-8; a,i=struct.unpack_from('<II',d,s); R=m.end()+47
    u=struct.unpack_from('<H',d,R)[0]
    print(hex(s),a,i,m.group()[5:13].hex(),d[m.end():m.end()+70].hex())

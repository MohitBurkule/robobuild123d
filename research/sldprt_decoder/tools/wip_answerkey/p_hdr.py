from choose2 import *
for n,D,d in parts():
    if n not in sys.argv[1:]: continue
    cc=d.find(b'moContourChooser_c'); print(n,'CC classdef at',hex(cc))
    for m in SIG.finditer(d):
        q=m.start()
        print(hex(q), d[q-12:q].hex(' '))

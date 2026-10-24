from common import *
for n,D,d in parts():
    if n not in sys.argv[1:]: continue
    R=regions(D,d)
    for m in re.finditer(rb'moContourChooser_c|moOneContour_c',d):
        own=[f.name+'/'+f.type for f,s,e in R if s<=m.start()<e]
        print(n,hex(m.start()),m.group(),own)
    for f,s,e in R: print('   ',hex(s),hex(e),f.name,f.type)

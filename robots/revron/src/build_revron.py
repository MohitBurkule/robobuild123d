"""Revron generator v12: live weapon shaft on 684 bearings in both uprights, belt from an 1806 in the tub."""
import json, math, sys
sys.path.insert(0,'/home/user/robobuild123d')
OUT = "/home/user/robobuild123d/robot/templates/revron.json"
def place(s,at,rot=(0,0,0)): return {"type":"place","shape":s,"at":list(at),"rot":list(rot)}
def box(sx,sy,sz,at=(0,0,0),rot=(0,0,0)): return place({"type":"box","size":[sx,sy,sz]},at,rot)
def boxr(x0,x1,y0,y1,z0,z1): return box(x1-x0,y1-y0,z1-z0,((x0+x1)/2,(y0+y1)/2,(z0+z1)/2))
def cyl(r,h,at=(0,0,0),rot=(0,0,0)): return place({"type":"cylinder","radius":r,"height":h},at,rot)
def cylx(r,x0,x1,y,z): return cyl(r,x1-x0,((x0+x1)/2,y,z),(0,90,0))
def cylz(r,z0,z1,x,y): return cyl(r,z1-z0,(x,y,(z0+z1)/2))
def cyly(r,y0,y1,x,z): return cyl(r,y1-y0,(x,(y0+y1)/2,z),(90,0,0))
def intersect(*a): return {'type':'intersect','items':list(a)}
def U(*a): return {"type":"union","items":list(a)}
def S(b,*c): return {"type":"subtract","base":b,"cut":list(c)}
def fillet(s,r): return {"type":"fillet","shape":s,"radius":r}
def yz(pts,x0,x1,spline=False):
    loc=[[-z,y] for y,z in pts]
    return place({"type":"spline_prism" if spline else "prism","points":loc,"height":x1-x0},((x0+x1)/2,0,0),(0,90,0))
def xs_(s,a,b): return sorted([s*a,s*b])
def hull(pts):
    pts=sorted(set(pts))
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return lo[:-1]+up[:-1]
def circ_pts(c,r,n=36): return [(round(c[0]+r*math.cos(2*math.pi*i/n),4),round(c[1]+r*math.sin(2*math.pi*i/n),4)) for i in range(n)]

# ------------------------------------------------------------------ layout
FLOOR=-15.0
YC, ZC = 55.0, 15.0                 # live weapon shaft
YF, YRW = 16.0, -34.0               # front (motor) and rear wheel axles
WX = 47.0; MX = 28.0; RW = 15.0
TX, TY0, TY1, TZ0, TZ1 = 39.5, -42.0, 30.0, -13.0, 9.5
W = 0.9; WF = 2.0; FL = 0.9; RIB = 1.4
UX0, UX1 = 16.0, 23.0               # uprights |x|, 7 mm printed plates
UXC = (UX0+UX1)/2
DX0, DX1 = -1.5, 1.5                # disc (3 mm Ti) centred
WPX = 8.0                           # weapon belt plane x
YM, ZM, XM = 17.0, -1.4, -1.0       # weapon motor (body x -8..6, stub +x)
WPR_M, WPR_S = 5.0, 6.0             # motor / shaft pulley groove radii
BOSS = [(35.5,-38.5),(-35.5,-38.5),(35.5,1.0),(-35.5,1.0)]
SW = (20.0,-36.0)
BAT_Y = -14.0
WESC = (-20.0,-35.0)
PULX = 41.0; PR = 7.0
BOT = TZ0+FL+RIB
SL0, SL1 = 21.0, 30.0
DROP = round(math.tan(math.radians(22))*(SL1-SL0),3)
ALPHA = 7.0; TIPY = 64.0; TA = math.tan(math.radians(ALPHA))
def bl_bot(y): return FLOOR+0.5+(TIPY-y)*TA
def bl_top(y): return bl_bot(y)+1.0/math.cos(math.radians(ALPHA))
PLAT = (29.5,40.0,TZ0,-2.0)         # crossbar platform tying both uprights
PB_Y = (32.5,37.5); PB_Z = -6.0     # upright->platform bolts
POD_MID = [(-13.0,0.0),(-8.5,4.0)]  # pod mid screws (y,z), sideways
POD_REAR = (-52.0,-2.0)

# ------------------------------------------------------------------ tub
TUB=[(TY0,TZ0),(TY1,TZ0),(TY1,TZ1-DROP),(TY1-1.6,TZ1-DROP),(SL0,TZ1),(TY0,TZ1)]
TIN=[(TY0+W,TZ0+FL),(TY1-WF,TZ0+FL),(TY1-WF,TZ1+6),(TY0+W,TZ1+6)]
items=[S(fillet(yz(TUB,-TX,TX),0.7), yz(TIN,-TX+W,TX-W))]
ribs=[]
for a in (42,-42):
    ribs.append(S(place({"type":"box","size":[2.4,104,RIB]},(0,-10,TZ0+FL+RIB/2),(0,0,a)), S(boxr(-60,60,-80,80,-20,20), boxr(-TX+0.5,TX-0.5,TY0+0.5,TY1-0.5,-20,20))))
items.append(S(U(*ribs), boxr(XM-8.5,XM+7.5,YM-11,YM+11,-20,20)))          # no ribs under the weapon motor
POSTS=[(YF-11.5,YF-5.5),(YF+5.5,YF+11.5)]
for s in (1,-1):
    xa=xs_(s,15.4,TX-W+0.2)
    items.append(boxr(*xa,YF-6.6,YF-5.2,TZ0+0.5,6.0)); items.append(boxr(*xa,YF+5.2,YF+6.6,TZ0+0.5,6.0))
    items.append(boxr(*xs_(s,15.4,17.4),YF-5.2,YF+5.2,TZ0+0.5,-2.0))                   # inner end stop for the gearmotor
    for y0,y1 in POSTS: items.append(boxr(*xs_(s,29.3,35.7),y0,y1,TZ0+0.5,6.0))       # strap posts
    items.append(boxr(*xs_(s,33.0,TX-0.6),YRW-3.5,YRW+3.5,-4.0,4.0))                   # rear axle boss
    items.append(boxr(*xs_(s,TX-0.5,PX0-1 if False else 52.0),-17,-4,TZ0,-9.0))       # mid pod tab (locating ledge)
    items.append(boxr(*xs_(s,TX-3.6,TX-W+0.1),-15.5,-6.0,-4.0,7.0))                    # inner bosses for the sideways pod screws
    items.append(boxr(*xs_(s,TX-4.0,TX),-55.0,TY0+0.5,-8.5,4.0))                       # rear ear for the pod rear screw
items.append(boxr(-24,24,BAT_Y-7.4,BAT_Y-6.2,TZ0+0.5,-5.5)); items.append(boxr(-24,24,BAT_Y+6.2,BAT_Y+7.4,TZ0+0.5,-5.5))
items.append(boxr(WESC[0]-12,WESC[0]+12,WESC[1]-7.3,WESC[1]-6.1,TZ0+0.5,-7.5)); items.append(boxr(WESC[0]-12,WESC[0]+12,WESC[1]+6.1,WESC[1]+7.3,TZ0+0.5,-7.5))
items.append(boxr(XM-9.3,XM-7.0,YM-9.5,YM+9.5,TZ0+0.5,ZM+4.0))                         # stator mount wall
for x,y in BOSS: items.append(cylz(3.2,2.0,TZ1,x,y))
items.append(boxr(SW[0]-7.4,SW[0]+7.4,SW[1]-3.6,SW[1]+3.6,2.5,TZ1-0.3)); items.append(boxr(SW[0]-1,SW[0]+1,SW[1]-3.6,SW[1]+3.6,TZ0+0.5,2.6))
items.append(boxr(-UX0,UX0,PLAT[0],PLAT[1],PLAT[2],-9.5))
for s in (1,-1): items.append(boxr(*xs_(s,UX0-5.0,UX0),PLAT[0],PLAT[1],PLAT[2],PLAT[3]))
tub=U(*items)
cuts=[]
for s in (1,-1):
    cuts.append(boxr(*xs_(s,17.45,TX-W+0.05),YF-5.15,YF+5.15,-6.15,7.0))
    cuts.append(cylx(1.9,*xs_(s,36,TX+1),YF,0)); cuts.append(boxr(*xs_(s,36,TX+1),YF-1.9,YF+1.9,0,TZ1+1))
    cuts.append(cylx(1.5,*xs_(s,32,TX+1),YRW,0))
    for y0,y1 in POSTS:
        yc=(y0+y1)/2; cuts.append(cylz(1.6,2.8,6.1,s*32.5,yc)); cuts.append(cylz(1.0,-1.0,6.1,s*32.5,yc))
    for y,z in POD_MID:
        cuts.append(cylx(1.6,*xs_(s,TX-3.3,TX+0.1),y,z)); cuts.append(cylx(1.0,*xs_(s,TX-3.7,TX),y,z))
    cuts.append(cylx(1.6,*xs_(s,TX-3.3,TX+0.1),*POD_REAR)); cuts.append(cylx(1.0,*xs_(s,TX-3.9,TX),*POD_REAR))
    for y in PB_Y:
        cuts.append(cylx(1.6,*xs_(s,UX0-3.3,UX0+0.1),y,PB_Z)); cuts.append(cylx(1.0,*xs_(s,UX0-5,UX0),y,PB_Z))
for x,y in BOSS:
    cuts.append(cylz(1.6,TZ1-3.0,TZ1+1,x,y)); cuts.append(cylz(1.0,TZ1-8,TZ1,x,y))
cuts.append(boxr(SW[0]-6.05,SW[0]+6.05,SW[1]-2.05,SW[1]+2.05,2.4,TZ1+1))
cuts.append(cylx(30.2,DX0-1.2,DX1+1.2,YC,ZC))                                           # disc running slot
cuts.append(boxr(WPX-3.2,WPX+3.2,TY1-WF-1,PLAT[1]+1,TZ0+FL+0.01,TZ1+2))                  # weapon belt slot
for dy in (-7.5,7.5):
    cuts.append(cylx(1.1,XM-10,XM-6.5,YM+dy,ZM))                                          # stator screws
cuts.append(boxr(XM-10,XM-6.9,YM-3,YM+3,ZM-2,ZM+2.0))                                   # phase lead pass in the mount wall
tub=S(tub,*cuts)

# ------------------------------------------------------------------ uprights (forks), printed flat
UP=[(30.2,bl_top(34.0)),(34.0,bl_top(34.0)),(46.0,bl_top(46.0)),(62.0,bl_top(62.0)),(64.6,-11.6),(65.2,-4),(63.8,8),(61.3,19),(57,23.4),(53,23.6),(48.5,21),(43,14.5),(36,7),(30.2,5.0)]
BHOLES=[-29.0,-21.5,-14.0]
def bhole_xy(s,ly): return (s*UXC, TIPY+ly*math.cos(math.radians(ALPHA)))
def upright(s):
    x0,x1=xs_(s,UX0,UX1)
    f=fillet(yz(UP,x0,x1),1.2)
    xo = x1 if s>0 else x0
    cuts=[cylx(2.4,x0-1,x1+1,YC,ZC),
          cylx(4.5,*sorted([xo-s*4.0,xo+s*0.1]),YC,ZC),                                    # 684 bearing pocket, open to the outer face
          yz([(38.5,-6),(44.5,-6),(44.5,0.5),(38.5,0.5)],x0-1,x1+1),                        # window (ref3)
          cylx(1.15,x0-1,x1+1,YC,ZC-14.6)]                                                  # locking-pin hole
    for ly in BHOLES:
        x,y=bhole_xy(s,ly); zt=bl_top(y)
        cuts.append(cylz(1.6,zt-0.3,zt+3.2,x,y)); cuts.append(cylz(1.0,zt-0.3,zt+6.0,x,y))
    for y in PB_Y: cuts.append(cylx(1.1,x0-1,x1+1,y,PB_Z))
    return S(f,*cuts)

# ------------------------------------------------------------------ pods
def pod(s):
    xs=lambda a,b: xs_(s,a,b)
    ys=[-55+i*5.0 for i in range(21)]
    def xo(y): return 52.9+1.8*(1-((y+4)/50.0)**2)
    out=[(xo(y),y) for y in ys]; inn=[(xo(y)-1.3,y) for y in reversed(ys)]
    band=place({"type":"spline_prism","points":[[s*x,y] for x,y in out+inn],"height":40.0},(0,0,0))
    side=yz([(-56,-4),(-52,-12),(-30,-12),(-10,-12),(10,-12),(30,-12),(39,-12),(44,-6),(44,0),(41,6),(34,10.5),(26,12.5),(16,9),(4,2),(-12,2),(-22,9),(-34,13),(-46,11.5),(-54,5)],*xs(40,60),spline=True)
    skin=intersect(band,side)
    front = fillet(yz([(37.5,-12),(43,-9),(44,-3),(42.5,3),(37.5,3)],*xs(42.0,xo(41)-0.8)),0.8)
    mid=S(boxr(*xs(TX+0.05,xo(-11)-0.5),-17,-4,-9.0,6.5), boxr(*xs(PULX-1.6,PULX+1.6),-18,-3,-9,-6.0))
    rear=boxr(*xs(TX+0.05,xo(-52)-0.6),-55.0,-49.6,-8.5,4.0)
    p=U(skin,front,mid,rear)
    cut=[cylx(1.4,*xs(41,54),42.0,-5.5), cylx(1.4,*xs(41,54),42.0,-0.5)]                  # 2 round lightening holes (ref2)
    for y,z in POD_MID+[POD_REAR]:
        cut.append(cylx(1.1,*xs(TX-1,50.0),y,z)); cut.append(cylx(2.2,*xs(48.0,56),y,z))   # screw + head/driver access through the band
    for y in (-30,-24,6,12):
        cut.append(boxr(s*xo(y)-3,s*xo(y)+3,y-1.2,y+1.2,-8,-2))
    return S(p,*cut)

# ------------------------------------------------------------------ disc (3 mm Ti sheet)
DISC_T=3.0; RB=22.0; RT=29.0; TOOTH_A=90.0
# ramp up to the tip, rounded tip, near-radial leading face (5 deg rake), root fillet
TOOTH=[(-30,22.4),(-22,23.4),(-15,24.6),(-9,26.0),(-4.5,27.4),(-1.5,28.5),(0.0,28.95),(1.2,28.8),(1.6,28.0),(1.4,26.6),(1.3,25.2),(1.6,24.0),(3.2,22.9),(6.0,22.4)]
def disc_outline(o):
    cx,cy=o
    def circ(a):
        t=math.radians(a); ux,uy=math.cos(t),math.sin(t)
        b=-2*(cx*ux+cy*uy); c=cx*cx+cy*cy-RB*RB; r=(-b+math.sqrt(b*b-4*c))/2
        return (r*ux,r*uy)
    pts=[]; a=TOOTH_A+15.0
    while a<TOOTH_A+15.0+300-0.1:
        pts.append(circ(a)); a+=10.0
    for da,r in TOOTH:
        t=math.radians(TOOTH_A+da); pts.append((r*math.cos(t),r*math.sin(t)))
    return [[round(x,4),round(y,4)] for x,y in pts]
def kidney(ac):
    pts=[]
    for k in range(9):
        a=math.radians(ac-40+80*k/8); pts.append((17.5*math.cos(a),17.5*math.sin(a)))
    for k in range(9):
        a=math.radians(ac+40-80*k/8); pts.append((9.5*math.cos(a),9.5*math.sin(a)))
    return {"type":"spline_prism","points":[[round(x,4),round(y,4)] for x,y in pts],"height":DISC_T+2}
def disc_local(o):
    plate={"type":"spline_prism","points":disc_outline(o),"height":DISC_T}
    return S(plate, cyl(2.0,DISC_T+2), *[kidney(a) for a in (0,120,240)])
def solve_balance():
    from robot import shapes
    import numpy as np
    def c(o):
        q=shapes.to_solid(disc_local(tuple(o))).center(); return np.array([q.X,q.Y])
    o=np.array([0.0,-0.5]); h=0.05
    for _ in range(6):
        f=c(o)
        if np.abs(f).max()<2e-4: break
        J=np.column_stack([(c(o+[h,0])-f)/h,(c(o+[0,h])-f)/h]); o=o-np.linalg.solve(J,f)
    f=c(o); print("disc balance o=(%.4f,%.4f) centroid %.5f %.5f"%(o[0],o[1],f[0],f[1]))
    return (float(o[0]),float(o[1]))
DBAL=solve_balance()

# ------------------------------------------------------------------ blades: flat 1 mm steel needles, tilted 7 deg
def blade_shape():
    pts=[(-0.3,0),(0.3,0),(3.5,-16),(3.5,-31.5),(-3.5,-31.5),(-3.5,-16)]
    return S(place({"type":"prism","points":[list(p) for p in pts],"height":1.0},(0,0,0.5)),
             *[place(cyl(1.15,3),(0,y,0.5),(ALPHA,0,0)) for y in BHOLES])

def pulley(): return S(cylx(PR,-0.8,0.8,0,0), cylx(4.6,-1,1,0,0))
def wpulley(r,bore): return S(U(cylx(r+1.2,-1.6,-0.8,0,0),cylx(r,-0.8,0.8,0,0),cylx(r+1.2,0.8,1.6,0,0)), cylx(bore,-3,3,0,0))
def band(c1,r1,c2,r2,w):
    outer=hull(circ_pts(c1,r1+w)+circ_pts(c2,r2+w)); inner=hull(circ_pts(c1,r1)+circ_pts(c2,r2))
    return outer, inner
def belt(s):
    xs=xs_(s,PULX-0.6,PULX+0.6)
    def stad(r): return U(boxr(*xs,YRW,YF,-r,r), cylx(r,*xs,YF,0), cylx(r,*xs,YRW,0))
    return S(stad(PR+1.2), stad(PR))
LOOP=2*(YF-YRW)+2*math.pi*(PR+0.6)
BELT_L=round(LOOP*0.95,1)
def wbelt():
    o,i=band((YM,ZM),WPR_M,(YC,ZC),WPR_S,1.2)
    return S(yz(o,WPX-0.6,WPX+0.6), yz(i,WPX-1,WPX+1))
d=math.hypot(YC-YM,ZC-ZM)
WLOOP=2*math.sqrt(d*d-(WPR_S-WPR_M)**2)+math.pi*(WPR_S+WPR_M+1.2)+2*(WPR_S-WPR_M)*math.asin((WPR_S-WPR_M)/d)
WBELT_L=round(WLOOP*0.95,1)

# ------------------------------------------------------------------ top plate (0.5 mm PC, routed + cold bent)
T=0.5; RBEND=1.0; Z0=TZ1+0.2; PE=25.5
th=math.atan2(DROP,SL1-SL0)
def plate_profile():
    ri, ro = RBEND, RBEND+T
    yb = SL0 - (ri+T)*math.tan(th/2)
    cy, cz = yb, Z0 - ri
    top=[(TY0,Z0+T)]; bot=[(TY0,Z0)]
    for i in range(9):
        a=th*i/8
        top.append((cy+ro*math.sin(a), cz+ro*math.cos(a))); bot.append((cy+ri*math.sin(a), cz+ri*math.cos(a)))
    dy=math.cos(th); dz=-math.sin(th)
    yt,zt2=top[-1]; Lt=(PE-yt)/dy
    pt=(PE,zt2+dz*Lt); top.append(pt); bot.append((PE-T*math.sin(th), pt[1]-T*math.cos(th)))
    return top+list(reversed(bot))
def rslot(x0,x1,y0,y1,r,z0,z1):
    return U(boxr(x0+r,x1-r,y0,y1,z0,z1),boxr(x0,x1,y0+r,y1-r,z0,z1),*[cylz(r,z0,z1,x,y) for x in (x0+r,x1-r) for y in (y0+r,y1-r)])
top=S(yz(plate_profile(),-TX,TX), rslot(SW[0]-6.6,SW[0]+6.6,SW[1]-2.6,SW[1]+2.6,1.0,TZ1-1,TZ1+4), *[cylz(1.1,TZ1-1,TZ1+4,x,y) for x,y in BOSS])

# ------------------------------------------------------------------ parts
parts=[]
def P(**k): parts.append(k)
P(id="tub",kind="structure",material="nylon",process="fdm",print_orientation="+z",organic=True,rotates_with="fixed",shape=tub,solid_fraction=0.7,color="#2a2c30",
  label="printed nylon tub: X-rib floor, 2 mm front wall, crossbar platform, weapon-motor mount wall, strap posts, pod tabs")
for s,n in ((1,"l"),(-1,"r")):
    P(id=f"pod_{n}",kind="structure",material="nylon",process="fdm",print_orientation="+z",organic=True,rotates_with="fixed",shape=pod(s),color="#c8102e",
      label="red printed boomerang side pod: fenders over both wheels, 3 sideways screws into the tub, sits on the tub ledge")
for s,n in ((1,"l"),(-1,"r")):
    P(id=f"upright_{n}",kind="fork",material="nylon",process="fdm",print_orientation="+x",organic=True,rotates_with="fixed",shape=upright(s),solid_fraction=0.85,color="#2a2c30",
      label="7 mm printed nylon upright, printed flat (spin axis = build direction); 684 bearing seat, blade root, 2 bolts into the crossbar")
P(id="top_armour",kind="armor",material="pc",process="sheet_bent",rotates_with="fixed",shape=top,color="#c9ccd1",label="0.5 mm polycarbonate, CNC-routed, cold line-bent 22 deg over a 1 mm inside radius")
for s,n in ((1,"l"),(-1,"r")):
    P(id=f"blade_{n}",kind="wedge",material="steel",process="laser",rotates_with="fixed",shape=blade_shape(),at=[s*UXC,TIPY,FLOOR+0.5],rot=[-ALPHA,0,0],color="#d0d3d8",
      label="1 mm hardened spring-steel needle wedgelet, flat laser-cut, pointing forward; root clamped under the upright by 3 bolts 15 mm apart")
for s,n in ((1,"l"),(-1,"r")):
    P(id=f"motor_{n}",kind="motor",catalog="n10_300rpm_6v",at=[s*MX,YF,0],rot=[0,0,0 if s>0 else 180],rotates_with="fixed")
    P(id=f"strap_{n}",kind="structure",material="nylon",process="fdm",print_orientation="+z",rotates_with="fixed",
      shape=S(boxr(*xs_(s,29.0,36.0),POSTS[0][0],POSTS[1][1],6.1,7.5),*[cylz(1.1,5,9,s*32.5,(a+b)/2) for a,b in POSTS]),color="#2a2c30",label="printed motor strap over the N10 gearbox, 2 M2 screws")
    for yy,k in ((YF,"f"),(YRW,"r")):
        rb = 1.5 if k=="f" else 3.0
        hubshape=S(U(S(cylx(12.5,-4,4,0,0),cylx(11.3,-5,5,0,0)), cylx(11.3,-1,1,0,0), cylx(4.5,-4,4,0,0)), cylx(rb,-5,5,0,0))
        if k=="f":
            par=f"motor_{n}"; at=[WX-MX,0,0]; piv=[WX-MX,0,0]
        else:
            par=f"axle_{n}"; at=[s*WX,yy,0]; piv=[s*WX,yy,0]
        P(id=f"whub_{k}{n}",kind="other",material="nylon",process="fdm",print_orientation="+x",rotates_with=f"wheel_{k}{n}",shape=hubshape,at=at,parent=par,
          joint={"kind":"revolute","axis":[1,0,0],"pivot":piv,"min":0,"max":360,"default":0},color="#333333",label="printed nylon wheel hub, 25 mm")
        P(id=f"wheel_{k}{n}",kind="wheel",material="tpu",process="fdm",print_orientation="+x",tyre_of=f"whub_{k}{n}",rotates_with=f"wheel_{k}{n}",shape=S(cylx(RW,-4,4,0,0),cylx(12.5,-5,5,0,0)),at=[0,0,0],parent=f"whub_{k}{n}",color="#1b1b1b",label="printed TPU 95A tyre, 30 x 8 mm")
        P(id=f"pulley_{k}{n}",kind="pulley",material="nylon",process="fdm",print_orientation="+x",rotates_with=f"wheel_{k}{n}",shape=pulley(),at=[(PULX-WX),0,0] if k=="f" else [s*(PULX-WX),0,0],parent=f"whub_{k}{n}",color="#444444")
    for j,(a,b) in enumerate(((WX-4.0,WX-1.5),(WX+1.5,WX+4.0))):
        P(id=f"wbrg_{n}{j}",kind="bearing",process="cots",mass_g=0.3,rotates_with=f"wheel_r{n}",shape=cylx(3.0,*xs_(s,a,b),YRW,0),color="#555555",label="MR63ZZ 3x6x2.5 rear wheel bearing (drawn solid)",stock="MR63ZZ")
    P(id=f"axle_{n}",kind="pin",material="steel",process="cots",rotates_with="fixed",shape=cylx(1.5,*xs_(s,33.0,51.5),YRW,0),color="#777777",label="3 mm silver-steel rod cut to 18.5 mm (rear dead axle)",stock="3 mm silver steel rod")
    P(id=f"belt_{n}",kind="belt",material="rubber",process="cots",shape=belt(s),color="#111111",
      belt={"pulleys":[f"pulley_f{n}",f"pulley_r{n}"],"kind":"o_ring","length_mm":BELT_L,"width_mm":1.2},label=f"1.2 mm nitrile O-ring, {BELT_L} mm")
P(id="battery",kind="battery",catalog="c_typical_2s_300mah_lipo_lihv_betafpv_tbs_",at=[0,BAT_Y,BOT+6.05],retained="press_fit")
P(id="rxesc",kind="esc",catalog="c_malenki_nano_antweight_esc_receiver",at=[0,BAT_Y,BOT+12.1+1.3],retained="velcro",
  ports={"bat":[-16,-4,0],"m1":[16,4,0],"m2":[-16,4,0],"wpn":[16,-4,0]},label="Malenki-Nano drive ESC + receiver")
P(id="wesc",kind="esc",catalog="c_bbb_antweight_spinner_brushless_esc",at=[WESC[0],WESC[1],BOT+2.05],retained="press_fit",ports={"bat":[11.5,-3,0],"motor":[11.5,3,0],"rx":[-11.5,0,0]})
P(id="power_switch",kind="switch",catalog="switch_slide_12x4",at=[SW[0],SW[1],TZ1-3.0],retained="press_fit",label="ON/OFF",marked=True,tool_free=True)
# weapon: static bearings, live shaft (joint), disc + shaft pulley on the shaft
for i,(x0,x1) in enumerate(((-UX1,-UX1+4.0),(UX1-4.0,UX1))):
    P(id=f"bearing_{i+1}",kind="bearing",process="cots",mass_g=1.0,rotates_with="fixed",shape=cylx(4.5,x0,x1,YC,ZC),color="#555555",label="684ZZ 4x9x4 (drawn solid)",stock="684ZZ")
P(id="shaft",kind="shaft",material="titanium",process="cots",rotates_with="disc",shape=cylx(2.0,-UX1-0.6,UX1+0.6,YC,ZC),color="#777777",parent="bearing_1",
  joint={"kind":"revolute","axis":[1,0,0],"pivot":[-UX1+2.0,YC,ZC],"min":0,"max":360,"default":0},
  label="4 mm Ti-6Al-4V live shaft with a D-flat, 47 mm, e-clips outside both bearings",stock="4 mm Ti rod")
P(id="disc",kind="weapon",material="titanium",process="laser",organic=True,rotates_with="disc",shape=disc_local(DBAL),at=[(DX0+DX1)/2,YC,ZC],rot=[0,90,0],color="#8d9199",
  parent="shaft",
  weapon={"kind":"disc","motor":"weapon_motor","cells":2,"reduction":round(WPR_S/WPR_M,3),"spin_axis":[0,0,1],"spin_dir":"ccw","locking_bar":"lock_pin","supported_both_ends":True,"teeth":1},
  label="3 mm Ti-6Al-4V disc: one hooked tooth (5 deg rake, 0.5 mm tip radius) in the 2D outline, 3 kidney cut-outs, D-bore; laser-cut")
P(id="wpulley_s",kind="pulley",material="aluminium",process="turned",secondary_ops=["drilled","flat"],rotates_with="disc",shape=wpulley(WPR_S,2.0),at=[WPX,YC,ZC],parent="shaft",color="#b0b4ba",
  label="turned 6061 flanged O-ring pulley, D-bore on the weapon shaft")
P(id="weapon_motor",kind="weapon_motor",catalog="bl_1806_2300kv",at=[XM,YM,ZM],rot=[0,0,0],rotates_with="fixed",ports={"phases":[-7.0,0,0]},
  label="1806 outrunner in the tub; stator face bolted to the printed mount wall, bell + stub drive the O-ring")
P(id="wpulley_m",kind="pulley",material="aluminium",process="turned",secondary_ops=["drilled","flat"],rotates_with="weapon_motor",shape=wpulley(WPR_M,2.5),at=[WPX-XM,0,0],parent="weapon_motor",
  joint={"kind":"revolute","axis":[1,0,0],"pivot":[WPX-XM,0,0],"min":0,"max":360,"default":0},color="#b0b4ba",label="turned 6061 flanged pulley on the motor shaft (grub screw on the flat)")
P(id="wbelt",kind="belt",material="rubber",process="cots",shape=wbelt(),color="#111111",
  belt={"pulleys":["wpulley_m","wpulley_s"],"kind":"o_ring","length_mm":WBELT_L,"width_mm":1.2},label=f"1.2 mm nitrile O-ring weapon belt, {WBELT_L} mm")
P(id="lock_pin",kind="locking_bar",material="titanium",process="cots",color="#ff0000",tethered=True,rotates_with="fixed",
  shape=cylx(1.0,-UX1-4.0,UX1+0.5,YC,ZC-14.6),label="REMOVE BEFORE FIGHT: 2 mm Ti rod through both uprights and a disc kidney, pulled out sideways; lanyard",stock="2 mm Ti rod")
for i,(x,y) in enumerate(BOSS):
    P(id=f"insert_t{i}",kind="insert",catalog="heatset_m2",at=[x,y,TZ1-1.5])
for s,n in ((1,"l"),(-1,"r")):
    for k,ly in enumerate(BHOLES):
        x,y=bhole_xy(s,ly)
        P(id=f"insert_b{n}{k}",kind="insert",catalog="heatset_m2",at=[x,y,bl_top(y)+1.5])
    for k,y in enumerate(PB_Y):
        P(id=f"insert_x{n}{k}",kind="insert",catalog="heatset_m2",at=[s*(UX0-1.5),y,PB_Z],rot=[0,90,0])
    for k,(a,b) in enumerate(POSTS):
        P(id=f"insert_s{n}{k}",kind="insert",catalog="heatset_m2",at=[s*32.5,(a+b)/2,4.5])
    for k,(y,z) in enumerate(POD_MID+[POD_REAR]):
        P(id=f"insert_p{n}{k}",kind="insert",catalog="heatset_m2",at=[s*(TX-1.5),y,z],rot=[0,90,0])

fast=[]
def F(**k):
    k.setdefault("head","socket"); k.setdefault("tool","hex1.5"); k.setdefault("removable",True); fast.append(k)
for i,(x,y) in enumerate(BOSS):
    F(id=f"bolt_t{i}",designation="M2x5",at=[x,y,round(Z0+T,3)],dir=[0,0,-1],through=["top_armour"],threads_into=f"insert_t{i}")
for k,dy in enumerate((-7.5,7.5)):
    F(id=f"bolt_wm{k}",designation="M2x5",at=[XM-9.3,YM+dy,ZM],dir=[1,0,0],through=["tub"],threads_into="weapon_motor")
for s,n in ((1,"l"),(-1,"r")):
    for k,ly in enumerate(BHOLES):
        x,y=bhole_xy(s,ly)
        F(id=f"bolt_b{n}{k}",designation="M2x6",at=[x,y,round(bl_bot(y)-0.15,3)],dir=[0,0,1],through=[f"blade_{n}"],threads_into=f"insert_b{n}{k}",head="button")
    for k,y in enumerate(PB_Y):
        F(id=f"bolt_x{n}{k}",designation="M2x10",at=[s*UX1,y,PB_Z],dir=[-s,0,0],through=[f"upright_{n}","tub"],threads_into=f"insert_x{n}{k}")
    for k,(a,b) in enumerate(POSTS):
        F(id=f"bolt_s{n}{k}",designation="M2x6",at=[s*32.5,(a+b)/2,7.5],dir=[0,0,-1],through=[f"strap_{n}","tub"],threads_into=f"insert_s{n}{k}")
    for k,(y,z) in enumerate(POD_MID+[POD_REAR]):
        F(id=f"bolt_p{n}{k}",designation="M2x14",at=[s*50.0,y,z],dir=[-s,0,0],through=[f"pod_{n}","tub"],threads_into=f"insert_p{n}{k}")

def Wr(i,a,b,awg,kind,sl): return {"id":i,"from":a,"to":b,"awg":awg,"kind":kind,"slack_mm":sl}
wires=[Wr("w_bat_sw","battery.xt30","power_switch.in",22,"power",8),Wr("w_sw_wesc","power_switch.out","wesc.bat",22,"power",8),
       Wr("w_sw_rx","power_switch.out","rxesc.bat",26,"power",8),Wr("w_wesc_m","wesc.motor","weapon_motor.phases",24,"motor",10),
       Wr("w_rx_wesc","rxesc.wpn","wesc.rx",30,"signal",6),Wr("w_m_l","rxesc.m1","motor_l.terminals",28,"motor",6),Wr("w_m_r","rxesc.m2","motor_r.terminals",28,"motor",6)]
conn=[]
def C(a,b,m,r,**k): conn.append(dict(a=a,b=b,method=m,reason=r,**k))
for n in "lr":
    C(f"motor_{n}",f"whub_f{n}","press_fit","Printed wheel hub pressed onto the 3 mm D-shaft of the N10 gearmotor; the D flat carries the drive torque",interference_mm=0.1,mechanical_key=True)
    C(f"motor_{n}",f"strap_{n}","interlock","Gearbox clamped from above by the screwed strap, boxed in by the cradle ribs and the end stop; the flats stop it rotating")
    C(f"motor_{n}","tub","interlock","Gearmotor sits between the cradle ribs, the inner end stop and the side wall; the strap holds it down")
    C(f"strap_{n}","tub","screw","Strap screwed down onto two printed posts either side of the gearbox with M2 bolts into heat-set inserts")
    for j in "01":
        C(f"whub_r{n}",f"wbrg_{n}{j}","press_fit","MR63 bearing pressed into the rear hub bore; carries the rear corner load",interference_mm=0.02,mechanical_key=True)
        C(f"wbrg_{n}{j}",f"axle_{n}","shaft","Bearing inner race on the 3 mm dead axle; e-clip outside")
    C(f"axle_{n}","tub","press_fit","Dead axle pressed through the side wall into a printed boss 6 mm deep; carries the rear wheel load",interference_mm=0.05,mechanical_key=True)
    for k in "fr":
        C(f"pulley_{k}{n}",f"whub_{k}{n}","press_fit","Printed O-ring pulley pressed onto the wheel hub boss with three keying pegs; transmits drive torque front to rear",interference_mm=0.1,mechanical_key=True)
        C(f"wheel_{k}{n}",f"whub_{k}{n}","press_fit","TPU tyre printed 0.3 mm undersize and stretched over the 25 mm hub rim between two lips",interference_mm=0.3,mechanical_key=True)
    C(f"belt_{n}",f"pulley_f{n}","interlock","O-ring sits in the pulley grooves under 5 % stretch; couples the rear wheel to the driven front wheel")
    C(f"upright_{n}","tub","screw","Upright bolted sideways to the crossbar platform end face (2x M2 normal to the contact face); its rear edge bears on the tub front wall")
    C(f"blade_{n}",f"upright_{n}","screw","Blade root clamped flat under the upright bottom face by 3 M2 button-head screws 15 mm apart into heat-set inserts")
    C(f"pod_{n}","tub","screw","Pod sits on the tub ledge (locating lip) and is pulled against the side wall by 3 sideways M2 screws normal to the contact face")
for i,n in ((1,"r"),(2,"l")):
    C(f"bearing_{i}",f"upright_{n}","press_fit","684ZZ pressed into a 9 mm seat in the outer face of the upright; carries the shaft radial impact load into the upright and the crossbar",interference_mm=0.05,mechanical_key=True)
    C(f"bearing_{i}","shaft","shaft","Inner race on the 4 mm live shaft; e-clips outside each bearing locate it axially")
C("disc","shaft","press_fit","Disc D-bore on the shaft D-flat (torque) between two e-clips (axial)",interference_mm=0.02,mechanical_key=True)
C("wpulley_s","shaft","press_fit","Pulley D-bore on the shaft D-flat plus a grub screw",interference_mm=0.02,mechanical_key=True)
C("wpulley_m","weapon_motor","press_fit","Pulley on the 5 mm motor shaft stub, grub screw on its flat",interference_mm=0.02,mechanical_key=True)
C("wbelt","wpulley_m","interlock","O-ring in the flanged pulley grooves under 5 % stretch: drives the weapon and slips on a hard hit, protecting the motor")
C("weapon_motor","tub","screw","Stator face bolted to the printed mount wall with 2 M2 screws along the motor axis")
C("lock_pin","upright_l","pin","Locking pin through both uprights and a disc kidney; slides out sideways, tethered by a lanyard",mechanical_key=True)
C("battery","tub","press_fit","Pack is a snug fit in the floor bay between two printed ribs and trapped from above by a 2 mm EVA foam pad under the bolted top plate",interference_mm=0.1,mechanical_key=True)
C("wesc","tub","press_fit","Weapon ESC is a snug fit in a ribbed floor bay at the rear, closed above by the top plate",interference_mm=0.1,mechanical_key=True)
C("rxesc","battery","velcro","Malenki board stuck flat on the top face of the pack with hook-and-loop, under the top plate")
C("power_switch","tub","press_fit","Switch pressed into a snug printed pocket in a pillar under a slot in the top plate; slider moves across the robot",interference_mm=0.1)

ov=[dict(a="shaft",b="bearing_1",max_depth_mm=4.5,reason="bearing drawn solid: the 4 mm shaft fills the inner race bore"),
    dict(a="shaft",b="bearing_2",max_depth_mm=4.5,reason="bearing drawn solid: the 4 mm shaft fills the inner race bore"),
    dict(a="weapon_motor",b="wpulley_m",max_depth_mm=5.5,reason="pulley bore on the motor shaft stub")]
for n in "lr":
    for j in "01": ov.append(dict(a=f"axle_{n}",b=f"wbrg_{n}{j}",max_depth_mm=3.5,reason="bearing drawn solid: the 3 mm axle fills the inner race bore"))
spec=dict(name="Revron",profile="aws2025",robot_type="vertical_spinner",locomotion="roller",
  archetype="vertical_spinner_forks",
  archetype_params={"blade_lead_mm":[5,15],"axle_height_mm":[28,32],"disc_thickness_mm":[15,18],"disc_dia_mm":[50,56],"teeth":[1,1],"tub_height_mm":[20,24],
                    "wheels":[4,4],"wheel_dia_mm":[28,30],"weapon_mass_fraction":[0.25,0.5],"top_slope_deg":[20,25]},
  targets={"length_mm":140,"width_mm":115,"disc_dia_mm":51,"wheel_dia_mm":30,"tol_mm":8,"source":"robots/revron/REFERENCE.md (photo estimates, +-15 %)",
           "note":"axle 30 mm above floor, 25 mm ahead of tub; single hooked tooth; tub 22.5 mm tall; 4 driven wheels"},
  reference=[{"image":"../../robots/revron/photos/ref3.png","view":"side","mask":"../../robots/revron/reference/side_mask.png","scale_hint":0.21},
             {"image":"../../robots/revron/photos/ref2.jpg","view":"iso","mask":"../../robots/revron/reference/iso_mask.png","approximate":True}],
  parts=parts,fasteners=fast,wires=wires,
  electronics=dict(failsafe=True,weapon_remote_disable=True,radio="2.4 GHz",cells=2),can_run_inverted=False,
  allow_overlap=ov,connections=conn,
  claims=[dict(id="c_mass",text="weighs 150 g or less",metric="mass_total_g",op="<=",value=150),
          dict(id="c_fit",text="fits the 150 mm square",metric="footprint_mm",op="<=",value=150)])
json.dump(spec,open(OUT,"w"),indent=1)

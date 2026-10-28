import numpy as np, wave, sys, math
TEA = len(sys.argv)>1 and sys.argv[1]=='tea'
import json
VO=json.load(open('vo.json')); WP=VO['warp']
def Wm(t):  # story time -> real time
    for i in range(1,len(WP)):
        if t<WP[i][1]: a,b=WP[i-1],WP[i]; return a[0]+(b[0]-a[0])*(t-a[1])/(b[1]-a[1])
    return WP[-1][0]
SR=48000; D=VO['D']; N=int(SR*D); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def add(t,x,g=1.0,pan=0.0,raw=False):
    t=t if raw else Wm(t); i=int(t*SR)
    if i>=N: return; j=min(N,i+len(x)); x=x[:j-i]*g
    L[i:j]+=x*math.sqrt((1-pan)/2); R[i:j]+=x*math.sqrt((1+pan)/2)
def env(n,a=0.005,r=None):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/(r if r else n/SR/4))
def sine(f,d,r=None): n=int(d*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*env(n,r=r)
def kick(d=0.35):
    n=int(d*SR); t=np.arange(n)/SR; f=50+90*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
def lp(x,a):
    y=np.zeros(len(x))
    for k in range(1,len(x)): y[k]=y[k-1]+a*(x[k]-y[k-1])
    return y
def noise(d,a=0.2,r=None): n=int(d*SR); return lp(rng.standard_normal(n),a)*env(n,r=r)
def flat(d,a=0.2,att=.05,rel=.1):
    n=int(d*SR); t=np.arange(n)/SR; return lp(rng.standard_normal(n),a)*np.minimum(1,t/att)*np.minimum(1,(d-t)/rel)
def hat(): x=np.diff(rng.standard_normal(int(.05*SR)),prepend=0); return x*env(len(x),.001,.012)
def pop(f=900): n=int(.09*SR); t=np.arange(n)/SR; fr=f*(1+2*np.exp(-t*60)); return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,.002,.025)
def ching(b=1.0):
    x=np.zeros(int(.6*SR)); a=sine(2093*b,.5,.12)*.5; x[:len(a)]+=a; x+=sine(2637*b,.6,.15)*.4; return x
def sweep(f0,f1,d):
    n=int(d*SR); t=np.arange(n)/SR; f=f0*(f1/f0)**(t/d); return np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*np.minimum(1,t/.02)*np.minimum(1,(d-t)/.05)
def chord(fs,d,g=.1):
    n=int(d*SR); t=np.arange(n)/SR; x=sum(np.sin(2*np.pi*f*t)+.3*np.sin(4*np.pi*f*t) for f in fs)
    return x*np.minimum(1,t/.25)*np.minimum(1,(d-t)/.4)*g
# music
bt=60/128; t=0.0
while t<Wm(9.6): add(t,kick(),.85,raw=True); add(t+bt/2,hat(),.22,raw=True); t+=bt
for t0 in np.arange(0,Wm(9.6),bt*4): add(t0,chord([110,130.8,164.8],bt*4,.06),raw=True)
dr=Wm(13.6)-Wm(9.6); add(9.6,flat(dr,.05,dr*.6,.3)*np.linspace(.2,1,int(dr*SR)),.25)   # riser into the phone
bt2=60/100; t=Wm(13.6)
while t<D-0.3: add(t,kick(.3),.6,raw=True); add(t+bt2/2,hat(),.16,raw=True); t+=bt2
prog=[[130.8,164.8,196],[174.6,220,261.6],[196,246.9,293.7],[130.8,164.8,196]]
for i,t0 in enumerate(np.arange(Wm(13.6),D-0.4,bt2*4)): add(t0,chord(prog[i%4],min(bt2*4,D-t0-0.05),.075),raw=True)
# fly buzz, panned with the fly (front shot 0..9.6 and 19..21.5, back shot 9.6..13.2)
def flyx(t):
    th=(6*math.sin(t*1.25)+2*math.sin(t*2.9))*math.pi/180; bx=540+150*math.sin(th)
    return bx+120*math.cos(t*2.6)+28*math.sin(t*7.1)
tt=np.arange(N)/SR
saw=((tt*218)%1)*2-1 + 0.5*(((tt*331)%1)*2-1)
am=0.6+0.4*np.sin(2*np.pi*tt*31)
on=((tt<Wm(13.2))|((tt>=Wm(19))&(tt<Wm(21.5)))).astype(float)
on=np.convolve(on,np.ones(2400)/2400,'same')
pan=np.clip((np.array([flyx(x) for x in tt[::480]]).repeat(480)[:N]-540)/500,-1,1)
buzz=lp(saw,.25)*am*on*0.05
L+=buzz*np.sqrt((1-pan)/2); R+=buzz*np.sqrt((1+pan)/2)
# foot taps
for k in range(int(Wm(7.6)/0.449)): add(0.11+k*0.449,noise(.06,.3,.01),.18,raw=True)
# smoking / tea
if TEA:
    for a,b in ((0.65,1.3),(7.7,8.7)): add(a,flat(b-a,.08,.05,.1),.12)
else:
    for a,b in ((0.65,1.3),(7.7,8.7)):
        x=flat(b-a,.5,.05,.1); cr=(rng.random(len(x))>0.9993)*rng.standard_normal(len(x))*3
        add(a,x*.25+lp(cr,.6),.35)
    for a,b in ((1.35,2.3),(8.75,9.6)): add(a,flat(b-a,.12,.05,.4),.5)
# events
add(2.6,sweep(1200,150,.7),.1)
for i,t0 in enumerate((3.0,3.65,4.3,4.95,5.6)): add(t0,ching(1+i*.06),.45)
for t0 in (0.25,2.9,5.6,8.55,15.6): add(t0,pop(700),.3)
# phone vibration
for k in range(4): add(9.05+k*0.14,sine(150,.1,.05)*np.sign(sine(150,.1,.05)),.25)
add(9.1,sine(1568,.4,.1),.25); add(9.18,sine(2093,.4,.1),.2)
add(9.6,noise(.5,.25,.15),.8); add(10.2,noise(.8,.08,.3),.5)
for t0 in (10.7,11.0,12.2,13.6,19.2,20.6,21.0): add(t0,pop(),.45)
add(13.3,noise(.45,.15,.15),.5); add(14.9,noise(.45,.15,.15),.4)
add(16.6,sine(1318.5,.8,.2),.35); add(16.68,sine(1760,.8,.2),.3); add(17.3,sine(1568,.6,.2),.25)
for k,f in enumerate((523.3,659.3,784,1046.5)): add(23.0+k*0.12,sine(f,1.2,.3),.25)
w=wave.open('vo_track.wav'); vo=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768; vo=np.pad(vo,(0,max(0,N-len(vo))))[:N]
mx=max(np.abs(L).max(),np.abs(R).max()); L/=mx; R/=mx
ev=np.convolve(np.abs(vo),np.ones(9600)/9600,'same'); duck=1-0.62*np.clip(ev/ (ev.max()+1e-9)*3,0,1)
L=L*duck*0.55+vo; R=R*duck*0.55+vo
fl=int(.4*SR); L[-fl:]*=np.linspace(1,0,fl); R[-fl:]*=np.linspace(1,0,fl)
m=max(np.abs(L).max(),np.abs(R).max())/0.89; L/=m; R/=m
st=np.stack([(L*32767).astype(np.int16),(R*32767).astype(np.int16)],1)
w=wave.open(sys.argv[2] if len(sys.argv)>2 else 'audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close(); print('ok')

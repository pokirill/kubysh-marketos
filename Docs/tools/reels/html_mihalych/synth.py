import numpy as np, wave
SR=48000; D=27.0; N=int(SR*D); out=np.zeros(N)
rng=np.random.default_rng(7)
def add(t,x,g=1.0):
    i=int(t*SR); j=min(N,i+len(x)); out[i:j]+=g*x[:j-i]
def env(n,a=0.005,r=None):
    t=np.arange(n)/SR; e=np.minimum(1,t/a)
    return e*np.exp(-t/(r if r else n/SR/4))
def sine(f,d,r=None):
    n=int(d*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*f*t)*env(n,r=r)
def kick(d=0.35):
    n=int(d*SR); t=np.arange(n)/SR; f=50+90*np.exp(-t*30); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*9)
def noise(d,lp=0.2,r=None):
    n=int(d*SR); x=rng.standard_normal(n)
    y=np.zeros(n); a=lp
    for k in range(1,n): y[k]=y[k-1]+a*(x[k]-y[k-1])
    return y*env(n,r=r)
def hat(): x=rng.standard_normal(int(.05*SR)); x=np.diff(x,prepend=0); return x*env(len(x),.001,.012)
def pop(f=900): n=int(.09*SR); t=np.arange(n)/SR; fr=f*(1+2*np.exp(-t*60)); return np.sin(2*np.pi*np.cumsum(fr)/SR)*env(n,.002,.025)
def ching(base=1.0):
    x=np.zeros(int(.6*SR)); a=sine(2093*base,.5,.12)*0.5; x[:len(a)]+=a; x+=sine(2637*base,.6,.15)*0.4; b=noise(.05,.9,.01)*0.3; x[:len(b)]+=b; return x
def sweep(f0,f1,d):
    n=int(d*SR); t=np.arange(n)/SR; f=f0*(f1/f0)**(t/d); x=np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))
    return x*np.minimum(1,t/.02)*np.minimum(1,(d-t)/.05)
def chord(fs,d,g=.12):
    n=int(d*SR); t=np.arange(n)/SR; x=sum(np.sin(2*np.pi*f*t)+.3*np.sin(4*np.pi*f*t) for f in fs)
    return x*np.minimum(1,t/.25)*np.minimum(1,(d-t)/.4)*g
# tense part 0..10.4 : 128 bpm
bt=60/128
t=0.0
while t<10.4:
    add(t,kick(),0.9); add(t+bt/2,hat(),0.25); t+=bt
for t0 in np.arange(0,10.4,bt*4): add(t0,chord([110,130.8,164.8],bt*4,0.07))  # A minor
# calm part 12.6..27 : 100 bpm, major
bt2=60/100; t=12.6
while t<26.8:
    add(t,kick(.3),0.6); add(t+bt2/2,hat(),0.18); t+=bt2
prog=[[130.8,164.8,196],[174.6,220,261.6],[196,246.9,293.7],[130.8,164.8,196]]
for i,t0 in enumerate(np.arange(12.6,26.8,bt2*4)): add(t0,chord(prog[i%4],bt2*4,0.08))
# sfx
for t0 in (0.15,1.2,3.3,4.6): add(t0,noise(.25,.5,.06),0.35)          # skid squeak-ish
add(1.0,noise(.3,.6,.05),0.6); add(1.0,kick(.4),0.4)                  # small crack
add(10.4,noise(.7,.7,.12),1.0); add(10.4,kick(.9),1.0); add(10.45,noise(.4,.3,.15),.6)  # big crack
for t0 in (2.4,3.9,12.6,18.8,20.6,15.0,0.25,5.9,8.9,10.7): add(t0,pop(),0.45)
add(5.4,sweep(1200,150,.7),0.12)                                      # rewind
for i,t0 in enumerate((6.0,6.75,7.5,8.2,8.8)): add(t0,ching(1+i*0.06),0.5)
for t0 in (12.65,13.9,22.9): add(t0,noise(.45,.15,.15),0.5)           # whoosh
add(16.0,sine(1318.5,.8,.2),.35); add(16.08,sine(1760,.8,.2),.3); add(16.8,sine(1568,.6,.2),.25)
for k,f in enumerate((523.3,659.3,784,1046.5)): add(23.0+k*0.12,sine(f,1.2,.3),.25)
# fade
fl=int(.4*SR); out[-fl:]*=np.linspace(1,0,fl)
out/=np.max(np.abs(out))/0.89
pcm=(out*32767).astype(np.int16); st=np.stack([pcm,pcm],1)
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
print('ok')

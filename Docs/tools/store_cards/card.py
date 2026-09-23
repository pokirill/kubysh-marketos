import sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F="/Users/kirillpopov/Documents/FinAssist - ios /FinAssist/FinAssist/Fonts/"
def render(out, headline, segments, shot_path, clean_status=True, arrow_in=False, arrow_out=False, step=None):
    W,H=1290,2796
    bg=Image.new('RGB',(W,H)); bd=ImageDraw.Draw(bg)
    top=(232,245,238); bot=(250,250,246)
    for y in range(H):
        t=y/H; bd.line([(0,y),(W,y)],fill=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3)))
    card=bg.convert('RGBA'); d=ImageDraw.Draw(card)
    size=118
    while True:
        bold=ImageFont.truetype(F+"Montserrat-Bold.ttf",size)
        if max(d.textlength(l,font=bold) for l in headline)<=W-180 or size<80: break
        size-=4
    reg=ImageFont.truetype(F+"Montserrat-Medium.ttf",52)
    hi=ImageFont.truetype(F+"Montserrat-Bold.ttf",52)
    green=(30,130,88); ink=(16,28,22); sub=(78,98,88)
    y=160
    for line in headline:
        d.text((90,y),line,font=bold,fill=ink); y+=int(size*1.12)
    # rich wrap: segments = [(text, highlighted)]
    words=[]
    for text,h in segments:
        for w_ in text.split(): words.append((w_,h))
    lines=[[]]; x=0; maxw=W-180; space=d.textlength(" ",font=reg)
    for w_,h in words:
        wl=d.textlength(w_,font=hi if h else reg)
        if lines[-1] and x+space+wl>maxw: lines.append([]); x=0
        x+= (space if lines[-1] else 0)+wl; lines[-1].append((w_,h))
    y+=34
    for ln in lines:
        x=90
        for i,(w_,h) in enumerate(ln):
            if i: x+=space
            f=hi if h else reg
            d.text((x,y),w_,font=f,fill=green if h else sub); x+=d.textlength(w_,font=f)
        y+=70
    shot=Image.open(shot_path).convert('RGB')
    if clean_status:
        s=shot.width/923
        sd=ImageDraw.Draw(shot)
        sd.rectangle([60*s,30*s,250*s,110*s],fill=shot.getpixel((int(70*s),int(40*s))))
        sd.rectangle([660*s,30*s,880*s,110*s],fill=shot.getpixel((int(670*s),int(40*s))))
        st=ImageFont.truetype(F+"Montserrat-SemiBold.ttf",int(38*s))
        sd.text((100*s,48*s),"9:41",font=st,fill=(255,255,255))
        for i,h in enumerate([10,16,22,28]):
            sd.rounded_rectangle([(690+i*14)*s,(86-h)*s,(699+i*14)*s,86*s],radius=2,fill=(255,255,255))
        sd.rounded_rectangle([780*s,56*s,838*s,86*s],radius=8,outline=(255,255,255),width=max(2,int(3*s)))
        sd.rounded_rectangle([786*s,62*s,832*s,80*s],radius=4,fill=(255,255,255))
        sd.rectangle([841*s,65*s,845*s,77*s],fill=(255,255,255))
    pw=960; ph=int(shot.height*pw/shot.width); shot=shot.resize((pw,ph),Image.LANCZOS)
    bez=26; r=118; px=(W-pw)//2; py=max(y+60, 770)
    phone=Image.new('RGBA',(pw+2*bez,ph+2*bez),(0,0,0,0)); pd=ImageDraw.Draw(phone)
    pd.rounded_rectangle([0,0,pw+2*bez-1,ph+2*bez-1],radius=r+bez,fill=(18,20,22,255))
    mask=Image.new('L',(pw,ph),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,pw-1,ph-1],radius=r,fill=255)
    phone.paste(shot,(bez,bez),mask)
    sh=Image.new('RGBA',card.size,(0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([px-bez+10,py-bez+40,px+pw+bez+10,py+ph+bez+40],radius=r+bez,fill=(20,60,40,70))
    card=Image.alpha_composite(card,sh.filter(ImageFilter.GaussianBlur(45)))
    card.alpha_composite(phone,(px-bez,py-bez))
    # панорама: стрелка в полях между телефонами на соседних карточках
    ad=ImageDraw.Draw(card); ay=py+700
    if arrow_out:
        for x0 in range(W-150,W,34): ad.line([(x0,ay),(min(x0+20,W),ay)],fill=green,width=8)
    if arrow_in:
        for x0 in range(0,120,34): ad.line([(x0,ay),(x0+20,ay)],fill=green,width=8)
        ad.polygon([(118,ay-24),(150,ay),(118,ay+24)],fill=green)
    if step:
        ad.ellipse([W-90-84,160,W-90,244],fill=green)
        sf=ImageFont.truetype(F+"Montserrat-Bold.ttf",46)
        ad.text((W-90-42,202),step,font=sf,fill=(255,255,255),anchor="mm")
    card.convert('RGB').save(out)
    return card
def batch(cfg_path):
    import os
    cfg=json.load(open(cfg_path))
    os.makedirs(cfg["out_dir"],exist_ok=True)
    for c in cfg["cards"]:
        shot=c["shot"] if c["shot"].startswith("/") else os.path.join(cfg["shots_dir"],c["shot"])
        render(os.path.join(cfg["out_dir"],c["name"]+".png"),c["headline"],[tuple(x) for x in c["segments"]],
               shot,c.get("clean",False),c.get("arrow_in",False),c.get("arrow_out",False))
        print("ok",c["name"])

if __name__=="__main__" and sys.argv[1]=="--config":
    batch(sys.argv[2]); sys.exit()
if __name__=="__main__":
    a=json.loads(sys.argv[1])
    c=render(a["out"],a["headline"],[tuple(x) for x in a["segments"]],a["shot"],a.get("clean",True),a.get("ain",False),a.get("aout",False),a.get("step"))
    c.convert('RGB').crop((0,0,1290,1500)).resize((645,750)).save(a["preview"],quality=80)

"""Инфографика «Петля Кубыша» 1600x1000."""
from PIL import Image, ImageDraw, ImageFont
from card import F
W,H=1600,1000; GREEN=(30,130,88); INK=(16,28,22); SUB=(78,98,88); MINT=(220,240,229)
OUT='/Users/kirillpopov/Documents/Кубыш доки и артефакты /Хабр 07.10/'
def f(n,s): return ImageFont.truetype(F+f"Montserrat-{n}.ttf",s)
im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
for y in range(H): t=y/H; d.line([(0,y),(W,y)],fill=tuple(int((232,245,238)[i]*(1-t)+(250,250,246)[i]*t) for i in range(3)))
d.text((80,50),'Как Кубыш работает от получки до получки',font=f('Bold',52),fill=INK)
S=['За 2 минуты|настроен под тебя','План до получки:|категории|и бюджет дня','Траты скриншотом|или вручную,|бюджет пересчитан','Пятница:|итоги недели и|план на выходные','Получка:|итоги двух недель','Новая получка|разложена: сколько|тратить и отложить','Цели стали ближе:|даты пересчитаны','Вклады под цели:|деньги не сгорают','Спроси ИИ|о своих деньгах']
bw,bh=440,200; xs=[80,580,1080]; ys=[170,430,690]
pos=[]
for r in range(3):
    cols=[0,1,2] if r%2==0 else [2,1,0]
    for c in cols: pos.append((xs[c],ys[r]))
for i,(x,y) in enumerate(pos):
    hi=i in (2,3,4,5)
    d.rounded_rectangle([x,y,x+bw,y+bh],radius=26,fill=GREEN if hi else (255,255,255),outline=MINT,width=3)
    d.ellipse([x+24,y+24,x+84,y+84],fill=(255,255,255) if hi else GREEN)
    d.text((x+54,y+54),str(i+1),font=f('Bold',34),fill=GREEN if hi else (255,255,255),anchor='mm')
    yy=y+30
    for l in S[i].split('|'):
        d.text((x+104,yy),l,font=f('SemiBold',26),fill=(255,255,255) if hi else INK); yy+=36
for i in range(8):
    (x1,y1),(x2,y2)=pos[i],pos[i+1]
    if y1==y2:
        a,b=(x1+bw,y1+bh/2),(x2,y2+bh/2) if x2>x1 else ((x1,y1+bh/2),(x2+bw,y2+bh/2))
        if x2<x1: a,b=(x1,y1+bh/2),(x2+bw,y2+bh/2)
    else: a,b=(x1+bw/2,y1+bh),(x2+bw/2,y2)
    d.line([a,b],fill=GREEN,width=6)
d.text((80,920),'Зеленые шаги повторяются каждую получку',font=f('SemiBold',32),fill=GREEN)
im.save(OUT+'loop.png'); print('ok')

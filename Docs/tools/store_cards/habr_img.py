"""Картинки для Хабра 07.10 (1600x900)."""
from PIL import Image, ImageDraw, ImageFont
from card import F
W,H=1600,900; GREEN=(30,130,88); INK=(16,28,22); SUB=(78,98,88); MINT=(220,240,229)
OUT='/Users/kirillpopov/Documents/Кубыш доки и артефакты /Хабр 07.10/'
def f(n,s): return ImageFont.truetype(F+f"Montserrat-{n}.ttf",s)
def bg():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im); a=(232,245,238); b=(250,250,246)
    for y in range(H): t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3)))
    return im,ImageDraw.Draw(im)
def box(d,x,y,w,h,txt,fill=(255,255,255),col=INK,size=36):
    d.rounded_rectangle([x,y,x+w,y+h],radius=24,fill=fill,outline=MINT,width=3)
    lines=txt.split('\n'); yy=y+(h-len(lines)*size*1.25)/2
    for l in lines:
        tw=d.textlength(l,font=f('Bold',size)); d.text((x+(w-tw)/2,yy),l,font=f('Bold',size),fill=col); yy+=size*1.25
def arrow(d,x1,y1,x2,y2):
    d.line([x1,y1,x2,y2],fill=GREEN,width=6); d.polygon([(x2,y2),(x2-18,y2-12),(x2-18,y2+12)],fill=GREEN)
# 1. cover attribution
im,d=bg(); d.text((90,70),'Откуда приходят установки',font=f('Bold',64),fill=INK); d.text((90,150),'iOS-приложения без SDK атрибуции',font=f('Bold',64),fill=INK)
for i,t in enumerate(['Хабр','vc.ru','LinkedIn']): box(d,90,330+i*150,300,110,t)
for i,t in enumerate(['01 · ppid','02 · ppid','06 · ppid']): box(d,560,330+i*150,320,110,t,fill=MINT,col=GREEN)
for i in range(3): arrow(d,395,385+i*150,550,385+i*150); arrow(d,885,385+i*150,1040,535)
box(d,1050,420,460,230,'App Store Connect\nпросмотры\nи загрузки\nпо страницам',fill=GREEN,col=(255,255,255),size=34)
d.text((90,800),'Специальные страницы продукта вместо UTM',font=f('SemiBold',34),fill=GREEN); im.save(OUT+'2_cover.png')
# 2. checklist
im,d=bg(); d.text((90,70),'Шаблон: атрибуция без SDK',font=f('Bold',60),fill=INK)
items=['Спецстраница на каждый канал, номер в названии','Ссылку проверить после одобрения Apple','Дневная база загрузок до поста, сравнение через 48 часов','Выводы только на сотнях просмотров']
for i,t in enumerate(items):
    y=210+i*150; d.rounded_rectangle([90,y,W-90,y+120],radius=24,fill=(255,255,255),outline=MINT,width=3)
    d.ellipse([125,y+30,185,y+90],fill=GREEN); d.text((143,y+33),str(i+1),font=f('Bold',40),fill=(255,255,255)); d.text((220,y+38),t,font=f('SemiBold',38),fill=INK)
im.save(OUT+'2_checklist.png')
# 3. limits humor
im,d=bg(); d.text((90,70),'Кто у соло-разработчика тимлид',font=f('Bold',62),fill=INK)
box(d,90,230,680,420,'5-часовой лимит\n\n= обед',size=58); box(d,830,230,680,420,'Недельный лимит\n\n= выходной',fill=GREEN,col=(255,255,255),size=58)
d.text((90,730),'Задача в файле и коммит после каждого шага: обрыв ничего не стоит',font=f('SemiBold',34),fill=GREEN); im.save(OUT+'3_cover.png')
print('ok')

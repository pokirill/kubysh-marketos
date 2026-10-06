"""Картинки для статей Дзен/vc.ru 1600x900 в стиле карточек стора. Запуск: python3 article_img.py"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from card import F
W, H = 1600, 900
GREEN=(30,130,88); INK=(16,28,22); SUB=(78,98,88); MINT=(220,240,229); ORANGE=(214,120,48)
OUT='/Users/kirillpopov/Documents/Кубыш доки и артефакты /Статьи поиск 06.10/'
SC='/Users/kirillpopov/Documents/Кубыш доки и артефакты /Скриншоты 1.7/Карточки для стора 1.7 (сборка 100)/'
def f(n,s): return ImageFont.truetype(F+f"Montserrat-{n}.ttf",s)
def bg():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im); a=(232,245,238); b=(250,250,246)
    for y in range(H): t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3)))
    return im
def wrap(d,text,font,maxw):
    out=[];cur=''
    for w in text.split(' '):
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)>maxw and cur: out.append(cur); cur=w
        else: cur=t
    return out+[cur]
def text_block(d,x,y,title,sub,maxw,ts=72):
    for l in wrap(d,title,f('Bold',ts),maxw): d.text((x,y),l,font=f('Bold',ts),fill=INK); y+=int(ts*1.15)
    y+=20
    for l in wrap(d,sub,f('SemiBold',34),maxw): d.text((x,y),l,font=f('SemiBold',34),fill=GREEN); y+=46
    return y
def card(im,name,x,y,h):
    c=Image.open(SC+name).convert('RGB'); w=int(c.width*h/c.height); c=c.resize((w,h),Image.LANCZOS)
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],radius=28,fill=255)
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([x+6,y+18,x+w+6,y+h+18],radius=28,fill=(20,60,40,60))
    base=Image.alpha_composite(im.convert('RGBA'),sh.filter(ImageFilter.GaussianBlur(22))); base.paste(c,(x,y),m); return base.convert('RGB'),w
def mark(d): d.rounded_rectangle([90,H-80,180,H-72],radius=4,fill=GREEN); d.text((200,H-96),'Кубыш',font=f('Bold',30),fill=GREEN)
def cover(name,title,sub,cards):
    im=bg(); d=ImageDraw.Draw(im); text_block(d,90,200,title,sub,620,ts=62); mark(d)
    x=W-60
    for c in reversed(cards):
        w=int(1290*760/2796); x-=w+30; im,_=card(im,c,x,70,760)
    im.save(OUT+name)
def screens(name,title,sub,cards):
    im=bg(); d=ImageDraw.Draw(im); d.text((90,60),title,font=f('Bold',56),fill=INK); d.text((90,135),sub,font=f('SemiBold',32),fill=GREEN)
    h=650; w=int(1290*h/2796); gap=60; x=(W-(len(cards)*w+(len(cards)-1)*gap))//2
    for c in cards: im,_=card(im,c,x,210,h); x+=w+gap
    im.save(OUT+name)
def flow(name,title,steps,result):
    im=bg(); d=ImageDraw.Draw(im); d.text((90,70),title,font=f('Bold',56),fill=INK)
    x=90; y=260; bw=(W-180-3*40)//4
    for i,(a,b) in enumerate(steps):
        d.rounded_rectangle([x,y,x+bw,y+260],radius=28,fill=(255,255,255),outline=MINT,width=3)
        yy=y+40
        for l in wrap(d,a,f('SemiBold',30),bw-60): d.text((x+30,yy),l,font=f('SemiBold',30),fill=SUB); yy+=40
        d.text((x+30,y+170),b,font=f('Bold',46),fill=INK if i<3 else GREEN)
        if i<3: d.text((x+bw+4,y+105),'→',font=f('Bold',40),fill=GREEN)
        x+=bw+40
    d.rounded_rectangle([90,600,W-90,760],radius=28,fill=GREEN)
    d.text((140,640),result,font=f('Bold',52),fill=(255,255,255)); mark(d); im.save(OUT+name)
def compare(name,title,cols):
    im=bg(); d=ImageDraw.Draw(im); d.text((90,60),title,font=f('Bold',54),fill=INK)
    cw=(W-180-2*40)//3; x=90
    for i,(h,rows) in enumerate(cols):
        hi=i==2; d.rounded_rectangle([x,170,x+cw,800],radius=32,fill=GREEN if hi else (255,255,255),outline=MINT,width=3)
        d.text((x+40,210),h,font=f('Bold',44),fill=(255,255,255) if hi else INK); y=300
        for k,v in rows:
            d.text((x+40,y),k,font=f('Medium',26),fill=(210,240,225) if hi else SUB); y+=38
            for l in wrap(d,v,f('SemiBold',32),cw-80): d.text((x+40,y),l,font=f('SemiBold',32),fill=(255,255,255) if hi else INK); y+=42
            y+=28
        x+=cw+40
    im.save(OUT+name)
def bars(name,title,rows):
    im=bg(); d=ImageDraw.Draw(im); d.text((90,60),title,font=f('Bold',54),fill=INK)
    cols=[GREEN,(120,190,150),(200,225,210)]; y=220
    for label,parts,note in rows:
        d.text((90,y),label,font=f('Bold',38),fill=INK); y+=60; x=90; tw=W-180
        for j,(p,t) in enumerate(parts):
            w=int(tw*p/100); d.rounded_rectangle([x,y,x+w-6,y+130],radius=18,fill=cols[j])
            a,b=t.rsplit(' ',2)[0],' '.join(t.rsplit(' ',2)[1:])
            d.text((x+24,y+18),a,font=f('SemiBold',30),fill=(255,255,255) if j<2 else INK)
            d.text((x+24,y+62),b,font=f('Bold',40),fill=(255,255,255) if j<2 else INK); x+=w
        y+=150; d.text((90,y),note,font=f('SemiBold',30),fill=ORANGE if 'не' in note else GREEN); y+=90
    mark(d); im.save(OUT+name)

cover('1_cover.png','Какое приложение помогает копить деньги','5 вариантов и кому какой подходит',['02_План_с_получки.png','03_Когда_накопишь.png'])
compare('1_compare.png','Три подхода к деньгам',[
 ('Копилка банка',[('Что делает','Откладывает округления или процент'),('Отвечает на вопрос','«Сколько уже отложено?»')]),
 ('Учет трат',[('Что делает','Собирает траты по категориям'),('Отвечает на вопрос','«Куда ушли деньги?»')]),
 ('Планировщик',[('Что делает','Считает от получки, ведет цели с датами'),('Отвечает на вопрос','«Сколько отложить и когда накоплю?»')])])
screens('1_kubysh.png','Как это выглядит в Кубыше','План с каждой получки, дата каждой цели, доход от вкладов',['02_План_с_получки.png','03_Когда_накопишь.png','04_Накопления_приносят_доход.png'])
cover('2_cover.png','Как сделать, чтобы денег хватало до зарплаты','Расчет на 10 минут и одна цифра на каждый день',['01_Сколько_тратить.png','08_Можно_ли_купить.png'])
flow('2_flow.png','Бюджет на день: пример с аванса',[('Пришел аванс','32 000'),('Кредит и связь до зарплаты','− 8 500'),('Сразу на цели','− 6 000'),('На жизнь 15 дней','17 500')],'1 167 ₽ в день до зарплаты')
screens('2_kubysh.png','Кубыш считает это каждый день','Сумма на сегодня, «хватит ли» в днях, ответ перед покупкой',['01_Сколько_тратить.png','08_Можно_ли_купить.png','05_Траты_скриншотом.png'])
cover('3_cover.png','Правило 50/30/20 на российскую зарплату','Почему не сходится и как поправить',['07_Куда_уходят_деньги.png','03_Когда_накопишь.png'])
bars('3_bars.png','Зарплата 80 000 ₽: правило и реальность',[
 ('По правилу 50/30/20',[(50,'Нужды 40 000'),(30,'Желания 24 000'),(20,'Копить 16 000')],'Аренда, кредит, связь и проезд уже 35 000: на еду остается 5 000, не хватает'),
 ('Поправка 60/25/15',[(60,'Нужды 48 000'),(25,'Желания 20 000'),(15,'Копить 12 000')],'Нужды закрыты, накопления остаются')])
screens('3_kubysh.png','Конверты и бюджет на день в Кубыше','Цели на одном счете, траты по категориям, сумма на сегодня',['03_Когда_накопишь.png','07_Куда_уходят_деньги.png','01_Сколько_тратить.png'])
print('ok')

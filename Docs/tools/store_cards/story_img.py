"""Картинки к статье о Кубыше (1600x900)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from card import F
W,H=1600,900; GREEN=(30,130,88); INK=(16,28,22); SUB=(78,98,88); MINT=(220,240,229); OR=(214,120,48)
OUT='/Users/kirillpopov/Documents/Кубыш доки и артефакты /Статья о Кубыше/'
SC='/Users/kirillpopov/Documents/Кубыш доки и артефакты /Скриншоты 1.7/Карточки для стора 1.7 (сборка 100)/'
def f(n,s): return ImageFont.truetype(F+f"Montserrat-{n}.ttf",s)
def bg():
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H): t=y/H; d.line([(0,y),(W,y)],fill=tuple(int((232,245,238)[i]*(1-t)+(250,250,246)[i]*t) for i in range(3)))
    return im
def card(im,name,x,y,h):
    c=Image.open(SC+name).convert('RGB'); w=int(c.width*h/c.height); c=c.resize((w,h),Image.LANCZOS)
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],radius=26,fill=255)
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([x+6,y+16,x+w+6,y+h+16],radius=26,fill=(20,60,40,60))
    b=Image.alpha_composite(im.convert('RGBA'),sh.filter(ImageFilter.GaussianBlur(20))); b.paste(c,(x,y),m); return b.convert('RGB'),w
def step(name,num,title,lines,cards):
    im=bg(); d=ImageDraw.Draw(im)
    d.ellipse([90,120,170,200],fill=GREEN); d.text((130,160),num,font=f('Bold',44),fill=(255,255,255),anchor='mm')
    y=240
    for l in title: d.text((90,y),l,font=f('Bold',58),fill=INK); y+=70
    y+=20
    for l in lines: d.text((90,y),l,font=f('SemiBold',32),fill=GREEN); y+=46
    d.rounded_rectangle([90,H-80,180,H-72],radius=4,fill=GREEN); d.text((200,H-96),'Кубыш',font=f('Bold',30),fill=GREEN)
    h=780; w=int(1290*h/2796); x=W-60
    for c in reversed(cards): x-=w+30; im,_=card(im,c,x,60,h)
    im.save(OUT+name)
def ritual(name,title,cols):
    im=bg(); d=ImageDraw.Draw(im); d.text((90,60),title,font=f('Bold',56),fill=INK)
    cw=(W-180-40)//2
    for j,(h,steps) in enumerate(cols):
        x=90+j*(cw+40); d.rounded_rectangle([x,170,x+cw,820],radius=30,fill=(255,255,255),outline=MINT,width=3)
        d.text((x+40,200),h,font=f('Bold',44),fill=GREEN); y=290
        for i,s in enumerate(steps):
            d.ellipse([x+40,y,x+90,y+50],fill=GREEN); d.text((x+65,y+25),str(i+1),font=f('Bold',28),fill=(255,255,255),anchor='mm')
            yy=y+4
            for l in s.split('|'): d.text((x+110,yy),l,font=f('SemiBold',30),fill=INK); yy+=40
            y+=125
    im.save(OUT+name)
def compare(name):
    im=bg(); d=ImageDraw.Draw(im); d.text((90,60),'Таблица, заметки или Кубыш',font=f('Bold',56),fill=INK)
    rows=[('Сколько можно сегодня','считать самому','считать самому','на экране сразу'),
          ('Хватит ли до зарплаты','формулы','в голове','в днях запаса'),
          ('Ввод трат','каждая строка','каждая строка','скриншот банка'),
          ('Даты целей','формулы','нет','считаются сами'),
          ('Перерасход','план сломан','план сломан','пересчитан сам')]
    xs=[90,560,900,1240]; d.text((xs[1],180),'Таблица',font=f('Bold',38),fill=SUB); d.text((xs[2],180),'Заметки',font=f('Bold',38),fill=SUB); d.text((xs[3],180),'Кубыш',font=f('Bold',38),fill=GREEN)
    d.rounded_rectangle([xs[3]-30,160,W-60,830],radius=28,outline=GREEN,width=4)
    y=270
    for r in rows:
        d.text((xs[0],y),r[0],font=f('Bold',32),fill=INK); d.text((xs[1],y),r[1],font=f('SemiBold',30),fill=SUB); d.text((xs[2],y),r[2],font=f('SemiBold',30),fill=SUB); d.text((xs[3],y),r[3],font=f('Bold',30),fill=GREEN)
        y+=110
    im.save(OUT+name)
step('01_plan.png','1',['2 минуты,','и план готов'],['Сколько тратить в день,','сколько отложить с получки'],['02_План_с_получки.png','01_Сколько_тратить.png'])
step('02_traty.png','2',['Траты','скриншотом,','бюджет','пересчитан'],['Видно темп: останутся деньги','на удовольствия или пора','притормозить'],['05_Траты_скриншотом.png','07_Куда_уходят_деньги.png'])
step('03_pokupka.png','3',['Можно ли','это купить?'],['Откуда деньги и сколько','останется на день.','Не хватает: перенести','на следующую получку'],['08_Можно_ли_купить.png'])
ritual('04_ritual.png','Пятница и получка: два ритуала',[('Пятница',['Загрузи выписку за неделю','Кубыш сверил: новые траты|уже разложены','Итоги недели: план и факт,|сравнение, совет']),('День зарплаты',['Итоги двух недель:|куда ушли деньги','Сверка остатков,|потрачено и отложено','Новая получка разложена|по категориям и целям'])])
step('05_celi.png','4',['Цели','стали ближе'],['Даты пересчитаны после','каждого пополнения,','с учетом приоритетов и премий'],['03_Когда_накопишь.png','09_Загляни_в_будущее.png'])
step('06_vklady.png','5',['Деньги','не сгорают'],['Вклады и накопительные','счета под сроки целей','и доход по каждому'],['04_Накопления_приносят_доход.png'])
compare('07_compare.png')
print('ok')

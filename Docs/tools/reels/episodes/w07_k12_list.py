"""К12 · сб 07.11 18:00 · «Список в голове» (сценарий 82 v3). Жабы на риге, стикеры и «Плановые покупки» кодом."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
import frog
from episodes.scr import STY
from episodes.w07_common import setup, sayer, finale

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W07/"
STICK = [("подарок маме", 250, 330), ("ТО машины", 760, 300), ("курсы", 520, 420), ("билеты", 300, 520), ("зимняя резина", 760, 540),
         ("ДР друга", 520, 640), ("стоматолог", 260, 730), ("подписки", 780, 760)]
SLOTS = [("Аванс · 5 ноя", ["подарок маме"]), ("Зарплата · 20 ноя", ["ТО машины", "зимняя резина"]), ("Аванс · 5 дек", ["билеты"])]


def build():
    ep = Ep("W07_K12_Список_в_голове", "room"); ep.sfxgain = 0.5; setup(ep)
    say = sayer(ep, V)
    kub = ep.actor("kub", "kubysh", 800, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)
    kub.expr(0, "worried")
    a0, a1 = say("hero", "hk", "В голове 15 вкладок, и *все горят*", at=0.2)
    st = [0.1 + 0.25 * i for i in range(len(STICK))]
    # 2 · Душная
    dush.show(a1 - 0.3); dush.go(a1 - 0.3, 270, hop=60, step=300); dush.expr(a1 - 0.3, "teacher")
    b0, b1 = say("dush", "d1", "Запиши на руке. И *не мой руки до зарплаты*", at=a1 + 0.2, a=dush)
    ep.shot(b0, ("dush", "kub"), dur=0.4); kub.react(b0 + 0.8, "shudder")
    # 3 · Кубыш раскладывает по получкам
    c0, c1 = say("kubysh", "s1", "Смотри: подарок маме с аванса, ТО с зарплаты, билеты со следующей. *Напомню, когда будем планировать получку*", at=b1 + 0.3, a=kub)
    kub.expr(c0, "proud"); dush.expr(c0, "skeptic"); ep.shot(c0, "wide")
    t_in = [c0 + (c1 - c0) * k for k in (0.12, 0.3, 0.45)]

    def stickers(img, t, cam):
        gone = seg(t, c0 - 0.2, c0 + 0.3)
        for i, (s, x, y) in enumerate(STICK):
            k = back(seg(t, st[i], st[i] + 0.3))
            if k <= 0.02 or gone >= 1: continue
            col = (200, 50, 50) if (t * 3 + i) % 2 < 1 else (230, 90, 40)
            im = PH.chip(s, PH.WHITE, 44); sh = 6 * math.sin(t * 30 + i) if t < b1 else 0
            bg = Image.new("RGBA", (im.width + 16, im.height + 16), (0, 0, 0, 0)); ImageDraw.Draw(bg).rounded_rectangle([0, 0, bg.width - 1, bg.height - 1], 30, fill=col + (235,))
            bg.alpha_composite(im, (8, 8)); bg = fade(scaled(bg, k), 1 - gone)
            comp(img, bg, x - bg.width / 2 + sh, y - bg.height / 2)
    ep.add(0, c0 + 0.4, "screen", stickers)
    for x in st: ep.sfx(x, "pop", 0.3)

    def plan(img, t, cam):
        k = eout(seg(t, c0, c0 + 0.4)) * (1 - ease(seg(t, d1 + 0.1, d1 + 0.4)))
        if k <= 0.02: return
        cv, pad = PH.card(960, 700, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 34, pad + 30
        d.text((x0, y0), "Плановые покупки", font=PH.font("Bold", 48), fill=PH.WHITE)
        for i, (slot, items) in enumerate(SLOTS):
            yy = y0 + 90 + i * 190; d.rounded_rectangle([x0, yy, x0 + 890, yy + 170], 24, fill=(30, 40, 37))
            d.text((x0 + 26, yy + 18), slot, font=PH.font("SemiBold", 38), fill=PH.SUB)
            if t >= t_in[i]:
                d.text((x0 + 26, yy + 74), " · ".join(items), font=PH.font("Bold", 46), fill=PH.WHITE)
                d.line([(x0 + 840, yy + 92), (x0 + 854, yy + 106), (x0 + 878, yy + 76)], fill=PH.GREEN, width=7)
        if t >= c0 + (c1 - c0) * 0.62:
            d.text((x0, y0 + 680 - 60), "Напомню при планировании получки", font=PH.font("SemiBold", 34), fill=PH.AMBER)
        comp(img, fade(cv, k), 540 - cv.width / 2, 180)
    ep.add(c0, 999, "screen", plan)
    for x in t_in: ep.sfx(x, "tick", 0.45)
    ep.sfx(c0 + (c1 - c0) * 0.62, "ding", 0.4)
    # 4 · голова свободна
    d0, d1 = say("kubysh", "s2", "Голова для жизни, а не *для списка покупок*", at=c1 + 0.3, a=kub)
    kub.expr(d0, "happy"); dush.go(d0, -380, hop=60, step=320)
    ep.pill(d1 - 0.6, d1 + 1.0, "в голове: тишина", 540, 560, size=56, **STY["green"]); ep.sfx(d1 - 0.6, "pop", 0.4)
    finale(ep, say, d1 + 1.1, (kub, dush))
    ep.cover_t = 1.4
    return ep

"""Т2 «Кредиты: стресс» (сценарий 85 v2). Душная = ты (паника, пот, сердце), Кубыш = сын маминой подруги (блеск).
Числа: доход 160 000 = платежи 38 + обязательное 50 + кошелек 10 + подушка 10 + на дни 52; 52 000 / 22 ≈ 2 400."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
import frog
from episodes.scr import STY
from episodes.w07_common import setup, sayer, finale

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W11_Банки/"
DATES = ["3", "10", "15", "22", "28"]
ROWS = [("Кредиты и рассрочки", 38, PH.RED, "платеж 3, 10, 15, 22, 28 · напомню"), ("Обязательное", 50, PH.BLUE, ""),
        ("Кошелек", 10, PH.AMBER, "на непредвиденное"), ("Подушка", 10, PH.GREEN, ""), ("На дни", 52, PH.GREEN, "≈ 2 400 в день")]


def plan(t, t0):
    cv, pad = PH.card(960, 820, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 36, pad + 30
    d.text((x0, y0), "Получка 160 000 ₽", font=PH.font("Bold", 50), fill=PH.WHITE)
    for i, (a, v, col, sub) in enumerate(ROWS):
        k = eout(seg(t, t0 + 0.3 + 0.55 * i, t0 + 0.75 + 0.55 * i))
        if k <= 0: continue
        y = y0 + 100 + i * 140
        d.text((x0, y), a, font=PH.font("Bold", 42), fill=PH.WHITE); d.text((x0 + 880, y), f"{v} 000", font=PH.font("Bold", 42), fill=col, anchor="ra")
        d.rounded_rectangle([x0, y + 56, x0 + max(30, int(880 * v / 52 * k)), y + 84], 14, fill=col)
        if sub: d.text((x0, y + 92), sub, font=PH.font("SemiBold", 30), fill=PH.SUB)
    return cv


def build():
    ep = Ep("W11_T2_Кредиты_стресс", "night_lamp"); ep.sfxgain = 0.5; setup(ep)
    say = sayer(ep, V, Y=1470, SZ=54)
    dush = ep.actor("dush", "dush", 540, s=0.7)
    kub = ep.actor("kub", "kubysh", 1500, s=0.62, hidden=True)
    # 1 · 3 ночи, паника
    dush.expr(0, "shock"); dush.mood(0, 13, "heart"); dush.mood(0.6, 13, "sweat"); dush.mood(0, 4, "tremble")
    ep.pill(0.0, 2.6, "3:07", 540, 300, size=90, **STY["dark"])
    for i in range(6): ep.sfx(0.05 + 0.43 * i, "tick", 0.5)
    a0, a1 = say("dush", "d1", "Три кредита, две кредитки *и рассрочка на пылесос!*", at=0.2, a=dush)
    dush.react(a1 - 0.6, "shudder")

    def orbit(img, t, cam):
        for i, s in enumerate(DATES):
            k = back(seg(t, a1 + 0.1 * i, a1 + 0.1 * i + 0.3))
            if k < 0.02: continue
            ang = t * 1.6 + i * 2 * math.pi / 5; x = 540 + 360 * math.cos(ang); y = 560 + 150 * math.sin(ang)
            ch = PH.chip(s + "-го", PH.RED, 52); ch = ch.resize((max(1, int(ch.width * k)), max(1, int(ch.height * k))))
            comp(img, ch, x - ch.width / 2, y - ch.height / 2)
    b0, b1 = say("dush", "d2", "Деньги есть. Я боюсь забыть! Один раз забыла, и пени, и звонки, *и кредитная история*", at=a1 + 0.3, a=dush)
    dush.expr(b0, "worried"); dush.mood(b0 + 3.5, b1, "tremble"); ep.shake(b0 + 3.6, 14)
    c0, c1 = say("dush", "d3", "Пять будильников. *И все равно не сплю*", at=b1 + 0.3, a=dush)
    ep.add(a1, c0 + 0.1, "front", orbit)
    for i in range(5):
        tt = c0 + 0.15 + 0.22 * i; ep.pill(tt, c1 + 0.2, f"будильник {['06:30', '07:00', '07:10', '07:20', '07:30'][i]}", 540, 380 + 95 * i, size=44, **STY["dark"]); ep.sfx(tt, "pop", 0.3)
    dush.expr(c0, "sleepy")
    # 2 · Кубыш, план
    kub.show(c1); kub.go(c1, 770, hop=90, step=350); kub.expr(c1, "proud"); kub.mood(c1, 999, "sparkle")
    dush.go(c1, 260, hop=50, step=300)
    k0, _ = say("kubysh", "k1", "Внеси кредиты и рассрочки один раз. Платежи будут в плане до каждой получки, *и я напомню в день платежа*", at=c1 + 0.8, a=kub)
    _, k1 = say("kubysh", "k2", "А остаток разложу на дни. Сегодня оптимально *около 2 400*", at=None, a=kub)
    dush.expr(k0, "skeptic"); dush.expr(k0 + 4, "neutral")
    ep.add(k0, k1 + 0.3, "screen", lambda img, t, cam: comp(img, fade(plan(t, k0), eout(seg(t, k0, k0 + 0.3)) * (1 - ease(seg(t, k1 + 0.05, k1 + 0.3)))), 40, 170))
    for i in range(5): ep.sfx(k0 + 0.3 + 0.55 * i, "tick", 0.4)
    # 3 · облегчение
    e0, e1 = say("kubysh", "k3", "Тебе останется *только проверить*", at=k1 + 0.35, a=kub)
    dush.expr(e0, "happy"); dush.jump(e0 + 0.3, h=120); kub.expr(e0, "wink"); ep.sfx(e0 + 0.3, "ding", 0.4)
    h0 = finale(ep, say, e1 + 0.6, actors=(dush, kub), pill_y=1420)
    ep.cover_t = 1.5
    return ep

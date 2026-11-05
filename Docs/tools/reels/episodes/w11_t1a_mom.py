"""Т1а «Мама сравнивает» (сценарий 85 v2 + критик). Душная = ты, Кубыш = сын маминой подруги (видеосвязь с моря).
Голоса: мама Vera, Душная клон, Кубыш Holden. Лестница частоты из 4 ступеней (идея Кирилла)."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
import frog
from episodes.scr import STY
from episodes.w07_common import setup, sayer, finale, badge

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W11_Банки/"
BEACH = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы маскот/пляж.png"
LADDER = [("Раз в день", "полный контроль"), ("Раз в 3 дня", "сколько тратить на день"), ("Раз в неделю", "хватит ли до зарплаты"), ("Раз в 2 недели", "сколько отложить")]


def ladder(t, ts):
    cv, pad = PH.card(960, 700, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 36, pad + 34
    d.text((x0, y0), "Выбери свой ритм", font=PH.font("Bold", 48), fill=PH.WHITE)
    for i, (a, b) in enumerate(LADDER):
        st = ts[i]; k = eout(seg(t, st, st + 0.4))
        if k <= 0: continue
        y = y0 + 110 + i * 140; x = x0 + (3 - i) * 50
        d.rounded_rectangle([x, y, x + 620, y + 116], 24, fill=(34, 66, 52) if i else (30, 130, 88))
        d.text((x + 28, y + 18), a, font=PH.font("Bold", 42), fill=PH.WHITE); d.text((x + 28, y + 70), b, font=PH.font("SemiBold", 32), fill=PH.GREEN if i else PH.WHITE)
    return cv


def build():
    ep = Ep("W11_T1a_Мама_сравнивает", "room"); ep.sfxgain = 0.5; setup(ep)
    ep.avatars["mom"] = badge("М", (200, 80, 140)); ep.vnorm = {"kubysh": -18, "dush": -23, "mom": -21}
    say = sayer(ep, V, Y=1470, SZ=54)
    dush = ep.actor("dush", "dush", 540, s=0.7)
    kub = ep.actor("kub", "kubysh", 560, s=0.7, hidden=True)
    # 1 · звонок мамы
    for i in range(3): ep.sfx(0.05 + 0.5 * i, "ding", 0.35)
    m0, m1 = say("mom", "m1", "Алло. А вот Кубыш опять на море! *Второй раз за год!*", at=0.2)
    ep.notif(0.0, m1 + 0.2, "Мама", "входящий звонок", icon="М", color=(200, 80, 140))
    dush.expr(0, "neutral"); dush.expr(m1 - 1.4, "eyeroll")
    a0, a1 = say("dush", "e1", "Мам, ему *просто везет*", at=m1 + 0.25, a=dush)
    b0, b1 = say("mom", "m2", "И айфон новый купил. *Без всяких рассрочек*", at=a1 + 0.25)
    ep.pill(b0 + 0.6, b1 + 0.2, "айфон без рассрочки", 540, 420, size=56, **STY["dark"]); ep.sfx(b0 + 0.6, "pop", 0.4)
    dush.expr(b0, "shock"); dush.mood(b0, b1 + 0.3, "tremble")
    c0, c1 = say("dush", "e2", "Да он, наверное, *на гречке сидит!*", at=b1 + 0.25, a=dush)
    dush.expr(c0, "dush_mad"); dush.jump(c0 + 0.3, h=100)
    # 2 · видеосвязь с моря
    tb = c1 + 0.3; ep.sfx(tb, "swish", 0.5)
    dush.show(tb, False); kub.show(tb); kub.expr(tb, "proud"); kub.mood(tb, 999, "sparkle")
    ep.pill(tb, tb + 2.5, "видеозвонок", 540, 300, size=48, **STY["green"])
    d0, d1 = say("kubysh", "q1", "Без гречки. Я знаю, сколько оптимально тратить в день, *а у отпуска есть дата*", at=tb + 0.3, a=kub)
    ep.pill(d0 + 3.2, d1 + 0.3, "отпуск: 15 марта", 540, 420, size=56, **STY["green"]); ep.sfx(d0 + 3.2, "ding", 0.4)
    e0, e1 = say("dush", "e3", "Ага, и каждую копейку записываешь. *Душно*", at=d1 + 0.3)
    kub.expr(e0, "wink")
    f0, f1 = say("kubysh", "q2", "Ничего не записываю. *Траты сами приходят из банка*, я просто заглядываю", at=e1 + 0.3, a=kub)
    for i, s in enumerate(["Кофе 350", "Продукты 2 150", "Такси 640"]):
        tt = f0 + 1.6 + 0.4 * i; ep.pill(tt, f1 + 0.2, s, 300 + 240 * i, 380 + 90 * i, size=46, **STY["dark"]); ep.sfx(tt, "tick", 0.4)
    g0, gx = say("kubysh", "l0", "Я заглядываю, *когда мне нужно*", at=f1 + 0.3, a=kub)
    ts = []
    for f, cap in [("l1", "Хочешь полный контроль: *раз в день*"), ("l2", "Знать, сколько тратить на день: *раз в три дня*"),
                   ("l3", "Хватит ли до зарплаты: *раз в неделю*"), ("l4", "Сколько отложить: *раз в две недели*")]:
        a_, gx = say("kubysh", f, cap, at=gx + 0.15, a=kub); ts.append(a_)
    g1 = gx
    ep.add(g0, g1 + 0.3, "screen", lambda img, t, cam: comp(img, fade(ladder(t, ts), eout(seg(t, g0, g0 + 0.3)) * (1 - ease(seg(t, g1 + 0.05, g1 + 0.3)))), 40, 170))
    for x in ts: ep.sfx(x, "tick", 0.45)
    ep.clip(tb, g1 + 0.3, BEACH, "пляж")
    # 3 · Душная тайком
    th = g1 + 0.3; kub.show(th, False); dush.show(th); dush.expr(th, "side"); ep.sfx(th, "swish", 0.45)
    h0, h1 = say("dush", "e4", "Мам, я перезвоню. *А как он называется?*", at=th + 0.3, a=dush)
    dush.expr(h0 + 1.4, "skeptic")
    finale(ep, say, h1 + 0.5, actors=(dush, kub), pill_y=1420)
    ep.cover_t = 1.6
    return ep

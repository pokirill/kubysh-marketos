"""Э2 · вс 08.11 12:00 · «Статистика без выводов» (сценарий 82 v3). Инфографика: круговая диаграмма, вопросы без ответов, ответы Кубыша."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
from episodes.w07_common import setup, sayer, finale

V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W08/"
PIE = [("Продукты", 28, (110, 160, 255)), ("Маркетплейсы", 19, (255, 190, 90)), ("Кафе", 12, (255, 116, 116)), ("Транспорт", 9, (150, 120, 255)),
       ("Связь", 5, (90, 200, 200)), ("Прочее", 27, (120, 130, 125))]


def pie(t, t0, hi=False):
    im = Image.new("RGBA", (900, 900), (0, 0, 0, 0)); d = ImageDraw.Draw(im); a = -90; grow = eio(seg(t, t0, t0 + 1.2))
    for i, (n, p, c) in enumerate(PIE):
        sw = 360 * p / 100 * grow; off = 30 if hi and i == 0 else 0
        mid = math.radians(a + sw / 2); dx, dy = off * math.cos(mid), off * math.sin(mid)
        d.pieslice([150 + dx, 50 + dy, 750 + dx, 650 + dy], a, a + sw, fill=c + ((255,) if not hi or i == 0 else (110,)))
        a += sw
    d.ellipse([330, 230, 570, 470], fill=(12, 18, 16, 255))
    for i, (n, p, c) in enumerate(PIE[:4]):
        y = 700 + (i // 2) * 70; x = 120 + (i % 2) * 380
        d.rounded_rectangle([x, y + 10, x + 30, y + 40], 8, fill=c); d.text((x + 46, y + 25), f"{n} {p}%", font=PH.font("SemiBold", 38), fill=PH.WHITE, anchor="lm")
    return im


def build():
    ep = Ep("W08_E2_Статистика_без_выводов", "studio"); ep.sfxgain = 0.45; setup(ep)
    say = sayer(ep, V, Y=1400, SZ=54)
    a0, a1 = say("hero", "e1", "Красивый график трат. И что мне с ним делать, *бл**ь?*", at=0.15)
    b0, b1 = say("hero", "e2", "Как в банке, только размечено. Продукты 28 процентов. *Окей. И?*", at=a1 + 0.3)
    c0, c1 = say("hero", "e3", "А хватит ли до 20-го? А если куплю куртку? *Выводы делаешь сам* и считаешь варианты руками", at=b1 + 0.3)
    d0, d1 = say("kubysh", "k4", "Смотри: хватит, с запасом в 2 дня. Сегодня оптимально 2 100. Куртку прикинул. *Отпуск 15 мая*", at=c1 + 0.4)
    Q = [("хватит до 20-го?", 290, 330), ("сколько сегодня?", 790, 430), ("а если куплю куртку?", 330, 560), ("когда накоплю?", 780, 680)]
    A = [("Хватит до 20-го", "запас 2 дня"), ("Сегодня оптимально", "≈ 2 100 ₽"), ("Куртка", "прикинул, цели на месте"), ("Отпуск", "15 мая")]

    def fn(img, t, cam):
        cv = PH.background(t).convert("RGBA")
        if t < b1 + 0.3:
            PH.put(cv, pie(t, 0.2, hi=t > b0 + (b1 - b0) * 0.4), PH.W / 2, 700)
            if t > b0 + (b1 - b0) * 0.75: PH.put(cv, PH.text_img("Окей. И?", 96, PH.AMBER), PH.W / 2, 220)
        elif t < c1 + 0.3:
            PH.put(cv, fade(pie(t, -9), 0.25), PH.W / 2, 700)
            for i, (s, x, y) in enumerate(Q):
                st = c0 + (c1 - c0) * (0.03 + 0.17 * i); k = back(seg(t, st, st + 0.3))
                if k > 0.02: PH.put(cv, PH.chip(s, PH.WHITE, 50), x, y + 120, scale=k)
            if t > c0 + (c1 - c0) * 0.6: PH.put(cv, PH.chip("считаешь руками", PH.RED, 58), PH.W / 2, 1060)
        else:
            PH.title(cv, t, d0, 999, ["Кубыш делает *выводы*"], y=230)
            for i, (a, b) in enumerate(A):
                st = d0 + (d1 - d0) * (0.05 + 0.24 * i); k = eout(seg(t, st, st + 0.4))
                if k <= 0: continue
                card, pad = PH.card(920, 150, 32, glow=PH.GREEN); dd = ImageDraw.Draw(card)
                dd.line([(pad + 34, pad + 78), (pad + 50, pad + 94), (pad + 80, pad + 58)], fill=PH.GREEN, width=8)
                dd.text((pad + 110, pad + 50), a, font=PH.font("Bold", 46), fill=PH.WHITE, anchor="lm"); dd.text((pad + 110, pad + 106), b, font=PH.font("SemiBold", 38), fill=PH.GREEN, anchor="lm")
                PH.put(cv, card, PH.W / 2 + 80 * (1 - k), 460 + i * 190, a=k)
        img.paste(cv.convert(img.mode), (0, 0))
    ep.add(0, 999, "screen", fn)
    ep.sfx(0.2, "whoosh", 0.4); ep.sfx(b0 + (b1 - b0) * 0.4, "pop", 0.4)
    for i in range(4): ep.sfx(c0 + (c1 - c0) * (0.03 + 0.17 * i), "pop", 0.35); ep.sfx(d0 + (d1 - d0) * (0.05 + 0.24 * i), "tick", 0.45)
    h0 = finale(ep, say, d1 + 0.7, pill_y=1190)
    ep.ov[0] = (0, h0 - 0.05, "screen", fn)
    ep.cover_t = 1.4
    return ep

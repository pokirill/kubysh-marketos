"""К13 · чт 05.11 12:00 · «Британские ученые», ч.1: сколько ты можешь откладывать (сценарий 82 v3).
Инфографика в темном стиле, заставка журнальной версткой (New York), голос героя Archie от первого лица."""
from PIL import Image, ImageDraw, ImageFont
from studio import *  # noqa
import promo_hero as PH
from episodes.scr import STY
from episodes.lib import PHONE

V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W05/"
V3 = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
Y = 1380
SERIF = "/System/Library/Fonts/NewYork.ttf"
INPUT = [("Зарплата", "150 000"), ("Кредит", "27 000"), ("Аренда", "45 000")]
CATS = [("Продукты", "24 000"), ("Кафе и доставка", "10 000"), ("Маркетплейсы", "9 000"), ("Транспорт", "6 000"), ("Связь и подписки", "3 000"), ("Прочее", "12 000")]


def serif(size, var="Bold"):
    return ImageFont.truetype("/System/Library/Fonts/Times.ttc", size, index=1 if var == "Bold" else 0)


def build():
    ep = Ep("W05_K13_Британские_ученые_1", "studio"); ep.sfxgain = 0.4
    say = lambda f, cap, at=None, v=V, who="hero": ep.say(who, "", cap=cap, at=at, y=Y, size=54, file=v + f + "_t_48k.wav")
    a0, a1 = say("h1", "Британские ученые выяснили, сколько ты можешь откладывать. *Проверяю на себе*", at=0.15)
    b0, b1 = say("h2", "Ввожу зарплату, кредит и аренду. *Все*", at=a1 + 0.3)
    c0, c1 = say("h3", "Траты по категориям он подставил сам, средние. Мне только проверить, *согласен ли я так жить*", at=b1 + 0.3)
    d0, d1 = say("h4", "Согласен. Получается *14 тысяч в месяц*", at=c1 + 0.3)
    e0, e1 = say("h5", "Сверь со своими суммами и напиши, *сколько выходит у тебя*", at=d1 + 0.35)
    g0, g1 = say("h6", "Через две недели покажу, *что вышло у меня*", at=e1 + 0.2)
    f0, f1 = say("w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=g1 + 0.5, v=V3, who="kubysh")
    end = f1 + 1.4

    def row(d, x, y, w, a, b, col=PH.WHITE, fill=(30, 40, 37), h=84):
        d.rounded_rectangle([x, y, x + w, y + h], 22, fill=fill)
        d.text((x + 30, y + h // 2), a, font=PH.font("SemiBold", 40), fill=PH.WHITE, anchor="lm")
        d.text((x + w - 30, y + h // 2), b, font=PH.font("Bold", 42), fill=col, anchor="rm")

    def fn(img, t, cam):
        cv = PH.background(t).convert("RGBA")
        if t < a1 + 0.3:   # заставка: журнальная верстка
            k = eout(seg(t, 0.0, 0.5)); d = ImageDraw.Draw(cv)
            d.line([(90, 300), (990, 300)], fill=(200, 200, 190), width=3); d.line([(90, 312), (990, 312)], fill=(200, 200, 190), width=1)
            d.text((540, 250), "ВЕСТНИК НАУКИ · ЛОНДОН", font=serif(34, "Regular"), fill=(200, 200, 190), anchor="mm")
            for i, s in enumerate(["Британские", "ученые", "выяснили*"]):
                ki = eout(seg(t, 0.1 + 0.15 * i, 0.5 + 0.15 * i))
                if ki > 0: d.text((540, 430 + i * 150 + int(30 * (1 - ki))), s, font=serif(130), fill=(245, 242, 232), anchor="mm")
            if t > a0 + 1.0:
                d.text((540, 900), "сколько ты можешь откладывать", font=serif(52, "Regular"), fill=PH.GREEN, anchor="mm")
            if t > a0 + 1.8:
                d.text((540, 1010), "*ученые это мы", font=serif(36, "Regular"), fill=(150, 150, 140), anchor="mm")
        elif t < b1 + 0.3:   # ввожу 3 поля
            PH.title(cv, t, b0, b1 + 0.3, ["Ввожу *три числа*"], y=300)
            card, pad = PH.card(940, 420, 40); d = ImageDraw.Draw(card)
            for i, (a, b) in enumerate(INPUT):
                if t >= b0 + 0.3 + 0.55 * i: row(d, pad + 30, pad + 40 + i * 116, 880, a, b, PH.BLUE if i else PH.GREEN)
            PH.put(cv, card, PH.W / 2, 700)
        elif t < c1 + 0.3:   # средние по категориям, проверяю
            PH.title(cv, t, c0, c1 + 0.3, ["Кубыш подставил", "*средние траты*"], y=230)
            card, pad = PH.card(940, 760, 40); d = ImageDraw.Draw(card)
            for i, (a, b) in enumerate(CATS):
                if t < c0 + 0.25 + 0.3 * i: continue
                y = pad + 30 + i * 116; row(d, pad + 30, y, 880, a, b)
                if t >= c0 + (c1 - c0) * 0.62 + 0.15 * i:
                    x = pad + 30 + 880 - 250; d.line([(x, y + 44), (x + 14, y + 58), (x + 38, y + 28)], fill=PH.GREEN, width=7)
            PH.put(cv, card, PH.W / 2, 800)
        elif t < d1 + 0.35:   # итог
            k = eout(seg(t, d0, d0 + 0.5))
            PH.put(cv, PH.text_img("откладывать в месяц", 48, PH.SUB, "SemiBold"), PH.W / 2, 560, a=k)
            v = 14000 * eio(seg(t, d0 + 0.3, d0 + 1.4))
            PH.big_number(cv, round(v / 100) * 100, 760, size=220, color=PH.GREEN, scale=1 + 0.06 * max(0, 1 - abs(t - d0 - 1.5) * 4))
            if t > d0 + 1.6: PH.put(cv, PH.chip("150 000 − обязательное − траты", PH.SUB, 40), PH.W / 2, 960)
        else:   # челлендж
            PH.title(cv, t, e0, f0, ["Сверь свои *суммы*", "Сколько выходит у тебя?"], y=380, size=78)
            if t > e0 + 0.8: PH.put(cv, PH.chip("пиши в комменты", PH.GREEN, 58), PH.W / 2, 720)
            if t > g0 + 0.2: PH.put(cv, PH.chip("итог через 2 недели: ч.2", PH.AMBER, 50), PH.W / 2, 880)
        img.paste(cv.convert(img.mode), (0, 0))
    ep.add(0, f0 - 0.05, "screen", fn)
    ep.sfx(0.1, "boom", 0.4)
    for i in range(3): ep.sfx(b0 + 0.3 + 0.55 * i, "tick", 0.5)
    for i in range(6): ep.sfx(c0 + 0.25 + 0.3 * i, "pop", 0.35)
    ep.sfx(d0 + 1.4, "kaching", 0.4)
    ep.clip(f0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - f0)))
    ep.pill(f0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, 1190, size=46, **STY["green"]); ep.sfx(f0 + 1.0, "pop", 0.4)
    ep.dur = end; ep.cover_t = 1.2
    return ep

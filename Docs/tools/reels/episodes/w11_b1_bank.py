"""Б1 «Вошла в банк, и все» (сценарий 85 v2 + критик). Экран подключения банков нарисован инфографикой (скринов нет).
Банки: Т-Банк, Сбер, Яндекс (Кирилл 05.11), без логотипов. «Пароль Кубыш не видит» только мелким текстом на экране."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
import frog
from episodes.scr import STY
from episodes.w07_common import setup, sayer, finale

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W11_Банки/"
BANKS = ["Т-Банк", "Сбер", "Яндекс"]
FEED = [("Кофе", "Кафе", "350"), ("Продукты", "Еда", "2 150"), ("Такси", "Транспорт", "640"), ("Аптека", "Здоровье", "890"),
        ("Маркетплейс", "Покупки", "1 990"), ("Кино", "Развлечения", "700")]


def check(d, x, y, s=1.0, col=PH.GREEN):
    d.line([(x, y), (x + 14 * s, y + 14 * s), (x + 38 * s, y - 16 * s)], fill=col, width=int(8 * s))


def banks(t, t0, t_ok):
    cv, pad = PH.card(940, 640, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 36, pad + 30
    d.text((x0, y0), "Банки и счета", font=PH.font("Bold", 52), fill=PH.WHITE)
    for i, b in enumerate(BANKS):
        k = eout(seg(t, t0 + 0.3 + 0.3 * i, t0 + 0.7 + 0.3 * i))
        if k <= 0: continue
        y = y0 + 100 + i * 140; ok = i == 0 and t >= t_ok
        d.rounded_rectangle([x0, y, x0 + 868, y + 116], 26, fill=(30, 40, 37))
        d.text((x0 + 30, y + 58), b, font=PH.font("Bold", 46), fill=PH.WHITE, anchor="lm")
        if ok:
            check(d, x0 + 560, y + 60); d.text((x0 + 840, y + 58), "Подключено", font=PH.font("Bold", 38), fill=PH.GREEN, anchor="rm")
        else:
            d.rounded_rectangle([x0 + 620, y + 26, x0 + 840, y + 90], 32, fill=(30, 130, 88)); d.text((x0 + 730, y + 58), "Войти", font=PH.font("Bold", 36), fill=PH.WHITE, anchor="mm")
    d.text((x0, y0 + 540), "вход на странице банка · пароль Кубыш не видит", font=PH.font("SemiBold", 30), fill=PH.SUB)
    return cv


def feed(t, t0):
    cv, pad = PH.card(940, 900, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 36, pad + 30
    d.text((x0, y0), "Траты за неделю", font=PH.font("Bold", 52), fill=PH.WHITE); d.text((x0 + 868, y0 + 30), "из банка", font=PH.font("SemiBold", 34), fill=PH.GREEN, anchor="rm")
    for i, (a, c, v) in enumerate(FEED):
        st = t0 + 0.2 + 0.32 * i; k = eout(seg(t, st, st + 0.35))
        if k <= 0: continue
        y = y0 + 100 + i * 128 - int(80 * (1 - k))
        d.rounded_rectangle([x0, y, x0 + 868, y + 108], 24, fill=(30, 40, 37))
        d.text((x0 + 30, y + 30), a, font=PH.font("Bold", 42), fill=PH.WHITE, anchor="lm"); d.text((x0 + 30, y + 78), c, font=PH.font("SemiBold", 30), fill=PH.SUB, anchor="lm")
        d.text((x0 + 840, y + 54), f"−{v} ₽", font=PH.font("Bold", 42), fill=PH.WHITE, anchor="rm")
    return cv


def today(t, t0):
    cv, pad = PH.card(900, 300, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 40, pad + 40
    d.text((x0, y0), "Сегодня оптимально", font=PH.font("SemiBold", 44), fill=PH.SUB)
    d.text((x0, y0 + 70), "≈ 2 300 ₽", font=PH.font("Bold", 110), fill=PH.GREEN)
    return cv


def card_at(ep, t0, t1, fn, x, y):
    ep.add(t0, t1, "screen", lambda img, t, cam: comp(img, fade(fn(t), eout(seg(t, t0, t0 + 0.3)) * (1 - ease(seg(t, t1 - 0.25, t1)))), x, y))


def build():
    ep = Ep("W11_B1_Вошла_в_банк", "room"); ep.sfxgain = 0.5; setup(ep); ep.vnorm = {"kubysh": -18, "dush": -23}
    say = sayer(ep, V, Y=1470, SZ=54)
    dush = ep.actor("dush", "dush", 540, s=0.7)
    kub = ep.actor("kub", "kubysh", 1500, s=0.62, hidden=True)
    # 1 · Душная не хочет вносить
    dush.expr(0, "eyeroll")
    ep.pill(0.0, 4.4, "дневник трат: день 3", 540, 360, size=56, **STY["red"]); ep.sfx(0.1, "pop", 0.4)
    a0, a1 = say("dush", "e5", "Вносить каждую трату руками? *Да я на третий день брошу*", at=0.2, a=dush)
    dush.expr(a1 - 1.2, "sleepy")
    # 2 · Кубыш: войди в банк один раз
    kub.show(a1); kub.go(a1, 790, hop=90, step=350); kub.expr(a1, "proud"); kub.mood(a1, 999, "sparkle"); dush.go(a1, 270, hop=50, step=300)
    b0, b1 = say("kubysh", "q4", "И не надо. Один раз войди в свой банк: Т-Банк, Сбер или Яндекс. *Дальше траты приходят сами*", at=a1 + 0.7, a=kub)
    t_ok = b0 + 4.6; card_at(ep, b0, b1 + 0.3, lambda t: banks(t, b0, t_ok), 70, 200); ep.sfx(t_ok, "ding", 0.45)
    dush.expr(b0, "skeptic")
    # 3 · лента трат
    c0, c1 = say("kubysh", "q5", "Смотри, вся неделя уже в ленте, *по категориям*", at=b1 + 0.3, a=kub)
    card_at(ep, c0, c1 + 1.0, lambda t: feed(t, c0), 70, 120)
    for i in range(len(FEED)): ep.sfx(c0 + 0.2 + 0.32 * i, "tick", 0.35)
    # 4 · удивление
    d0, d1 = say("dush", "e6", "Подожди. *Я же ничего не вносила!*", at=c1 + 1.1, a=dush)
    dush.expr(d0, "shock"); dush.jump(d0 + 0.6, h=140); ep.shake(d0 + 0.6, 12)
    e0, e1 = say("kubysh", "q6", "И не нужно. Тебе только глянуть, *сколько оптимально сегодня*", at=d1 + 0.3, a=kub)
    card_at(ep, e0 + 1.2, e1 + 0.4, lambda t: today(t, e0), 90, 300); ep.sfx(e0 + 1.2, "ding", 0.4)
    dush.expr(e0 + 1.2, "happy"); kub.expr(e0 + 1.2, "wink")
    finale(ep, say, e1 + 0.6, actors=(dush, kub), pill_y=1420)
    ep.cover_t = 1.5
    return ep

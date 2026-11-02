"""Э1 · сб 07.11 12:00 · «Кофе в экселе» (сценарий 82 v3). Инфографика: таймер, окно таблицы, пуши трат, три способа ввода."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
from episodes.w07_common import setup, sayer, finale

V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W07/"
STEPS = ["Найти файл", "Лист «Ноябрь»", "Дата 07.11", "Категория ▾", "#ЗНАЧ!"]


def sheet(t, t0, n_on):
    """Окно таблицы: белая сетка, сверху шаги, последний — ошибка формулы."""
    im = Image.new("RGBA", (940, 620), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 939, 619], 30, fill=(250, 250, 252)); d.rounded_rectangle([0, 0, 939, 70], 30, fill=(32, 120, 70)); d.rectangle([0, 40, 939, 70], fill=(32, 120, 70))
    d.text((30, 35), "Бюджет_2026_финал_v7.xlsx", font=PH.font("SemiBold", 32), fill=(255, 255, 255), anchor="lm")
    for r in range(8):
        for c in range(4):
            d.rectangle([20 + c * 225, 90 + r * 62, 20 + (c + 1) * 225, 90 + (r + 1) * 62], outline=(214, 216, 222), width=2)
    if n_on >= 5:
        d.rectangle([245, 400, 470, 462], fill=(255, 225, 225)); d.text((357, 431), "#ЗНАЧ!", font=PH.font("Bold", 36), fill=(200, 30, 40), anchor="mm")
    return im


def build():
    ep = Ep("W07_E1_Кофе_в_экселе", "studio"); ep.sfxgain = 0.45; setup(ep)
    say = sayer(ep, V, Y=1380, SZ=54)
    a0, a1 = say("hero", "c1", "Купил кофе за 290. Теперь 4 минуты *вношу его в эксель*", at=0.15)
    b0, b1 = say("hero", "c2", "Найти файл. Найти лист. Найти дату. Найти, бл**ь, категорию. *Почему опять поехала формула?*", at=a1 + 0.3)
    c0, c1 = say("hero", "c3", "Пока вносил одну трату, *сделал еще три*", at=b1 + 0.3)
    d0, d1 = say("kubysh", "s3", "Траты из банка подтягиваются сами. Нет банка? Скинь скриншот или *впиши в два касания*", at=c1 + 0.4)
    ts = [b0 + (b1 - b0) * k for k in (0.02, 0.17, 0.32, 0.47, 0.75)]

    def fn(img, t, cam):
        cv = PH.background(t).convert("RGBA")
        # таймер: от начала до конца жалобы — 0:00 → 4:12
        sec = int(252 * eio(seg(t, a0 + 1.5, c0)))
        if t < d0 - 0.1:
            PH.put(cv, PH.text_img(f"{sec // 60}:{sec % 60:02d}", 110, PH.RED if sec > 120 else PH.WHITE), PH.W / 2, 230)
        if t < a1 + 0.3:
            k = eout(seg(t, 0, 0.4)); PH.put(cv, PH.chip("Кофе · 290 ₽", PH.AMBER, 64), PH.W / 2, 620, a=k, scale=lerp(1.3, 1, k))
            if t > a0 + (a1 - a0) * 0.55: PH.put(cv, PH.text_img("→ в таблицу", 56, PH.SUB, "SemiBold"), PH.W / 2, 780)
        elif t < c0:
            n = sum(t >= x for x in ts)
            PH.put(cv, sheet(t, b0, n), PH.W / 2, 760)
            if n: PH.put(cv, PH.chip(STEPS[n - 1], PH.RED if n == 5 else PH.WHITE, 54), PH.W / 2, 400)
        elif t < d0 - 0.1:
            for i, (amt, what) in enumerate([("−450 ₽", "Такси"), ("−1 200 ₽", "Продукты"), ("−390 ₽", "Самокат")]):
                st = c0 + 0.2 + 0.5 * i; k = eout(seg(t, st, st + 0.35))
                if k > 0:
                    card, pad = PH.card(900, 130, 30); dd = ImageDraw.Draw(card)
                    dd.text((pad + 34, pad + 65), "Банк · " + what, font=PH.font("SemiBold", 42), fill=PH.WHITE, anchor="lm")
                    dd.text((pad + 866, pad + 65), amt, font=PH.font("Bold", 46), fill=PH.RED, anchor="rm")
                    PH.put(cv, card, PH.W / 2, 520 + i * 170, a=k)
        else:
            PH.title(cv, t, d0, d1 + 0.6, ["Как траты", "попадают в *Кубыш*"], y=250)
            for i, (a, b) in enumerate([("Из банка", "подтягиваются сами"), ("Скриншот", "из приложения банка"), ("Вручную", "в два касания")]):
                st = d0 + (d1 - d0) * (0.05 + 0.33 * i); k = eout(seg(t, st, st + 0.4))
                if k <= 0: continue
                card, pad = PH.card(900, 150, 32, glow=PH.GREEN); dd = ImageDraw.Draw(card)
                dd.line([(pad + 34, pad + 78), (pad + 50, pad + 94), (pad + 80, pad + 58)], fill=PH.GREEN, width=8)
                dd.text((pad + 110, pad + 50), a, font=PH.font("Bold", 48), fill=PH.WHITE, anchor="lm"); dd.text((pad + 110, pad + 106), b, font=PH.font("Medium", 36), fill=PH.SUB, anchor="lm")
                PH.put(cv, card, PH.W / 2 + 80 * (1 - k), 560 + i * 190, a=k)
        img.paste(cv.convert(img.mode), (0, 0))
    ep.add(0, 999, "screen", fn)
    for x in ts: ep.sfx(x, "tick", 0.5)
    ep.sfx(ts[-1], "marker", 0.5)
    for i in range(3): ep.sfx(c0 + 0.2 + 0.5 * i, "ding", 0.35)
    for i in range(3): ep.sfx(d0 + (d1 - d0) * (0.05 + 0.33 * i), "pop", 0.4)
    h0 = finale(ep, say, d1 + 0.7, pill_y=1190)
    ep.ov[-0 if False else 0] = (0, h0 - 0.05, "screen", fn)
    ep.cover_t = 1.0
    return ep

"""«Если завтра сократят» (сценарий 84). Инфографика без упоминания бренда, призыв: слово «подушка» в комментариях.
VAR=A: накопления делят на зарплату (0,8 мес) → считать от обязательного (1,5 мес), финал: обязательное / жизнь / подушка.
VAR=B: подушка «6 зарплат» = 900 000 демотивирует → от трат 300 000, финал: траты с кофе и баром / кошелек / подушка.
Числа: доход 150 000, накоплено 120 000, в подушку 15 000 с аванса и с зарплаты = 30 000 в месяц.
A: цель 3 × 80 000 = 240 000, не хватает 120 000 → 4 месяца, к марту. B: 3 × 100 000 = 300 000, не хватает 180 000 → 6 месяцев, к маю."""
import os
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
from episodes.w07_common import sayer

V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W10_Подушка/"
VAR = os.environ.get("VAR", "A")
HEAD = [("сокращает штат", 300, 330), ("оптимизация расходов", 760, 470), ("волна увольнений", 330, 620), ("заморозка найма", 760, 770)]


def struck(s, size, color):
    im = PH.text_img(s, size, color); d = ImageDraw.Draw(im)
    d.line([(0, im.height * 0.55), (im.width, im.height * 0.5)], fill=PH.RED + (255,), width=max(6, size // 10)); return im


def rows(cv, t, t0, t1, items, total, y0, step=150):
    """Строки-столбики: подпись, сумма, полоса пропорционально сумме. items: (подпись, тыс, цвет, подпись мелко)."""
    for i, (lab, v, col, sub) in enumerate(items):
        st = t0 + (t1 - t0) * (0.08 + 0.8 * i / max(1, len(items))); k = eout(seg(t, st, st + 0.45))
        if k <= 0: continue
        y = y0 + i * step; w = int(860 * v / total * k)
        bar = Image.new("RGBA", (900, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(bar)
        d.text((0, 22), lab, font=PH.font("Bold", 44), fill=PH.WHITE, anchor="lm")
        d.text((880, 22), f"{v} 000 ₽", font=PH.font("Bold", 44), fill=col, anchor="rm")
        d.rounded_rectangle([0, 56, max(24, w), 92], 18, fill=col + (255,))
        if sub: d.text((0, 140), sub, font=PH.font("SemiBold", 32), fill=PH.SUB, anchor="lb")
        PH.put(cv, bar, PH.W / 2, y, a=k)


def build():
    ep = Ep(f"W10_Если_завтра_сократят_{VAR}", "studio"); ep.sfxgain = 0.45
    say = sayer(ep, V, Y=1420, SZ=54)
    A = VAR == "A"
    s1 = say("narr", "a1", "Если завтра сократят, *на сколько тебе хватит?*", at=0.2)
    if A:
        s2 = say("narr", "a2", "Обычно считают так: накопления делят на зарплату. Выходит *меньше месяца*. Паника", at=s1[1] + 0.35)
        s3 = say("narr", "a3", "Но без работы ты живешь не на зарплату, а на обязательное. 80 000. Значит, уже *полтора месяца*", at=s2[1] + 0.35)
    else:
        s2 = say("narr", "b2", "Обычно смотрят на сумму: шесть зарплат, *900 000*. Цифра такая большая, что руки опускаются", at=s1[1] + 0.35)
        s3 = say("narr", "b3", "Но подушка нужна не на зарплату, а на твои траты. 100 000 в месяц, три месяца: 300 000. *Втрое меньше*", at=s2[1] + 0.35)
    s4 = say("narr", "a4", "Есть приложение, которое *бесплатно за две минуты* посчитает подушку по твоим тратам и покажет дату, когда она соберется", at=s3[1] + 0.35)
    if A:
        s5 = say("narr", "a5", "А дальше раскладывает каждую зарплату так, чтобы копить, *не урезая привычную жизнь*", at=s4[1] + 0.35)
    else:
        s5 = say("narr", "b5", "А дальше раскладывает каждую зарплату: кофе, бары и такси уже в тратах, сверху *кошелек на непредвиденное*, и только потом подушка", at=s4[1] + 0.35)
    s6 = say("narr", "a6", "Напиши в комментах слово *«подушка»*, пришлю ссылку", at=s5[1] + 0.4)
    end = s6[1] + 1.6
    target, months, date, fill = (240, 3, "к марту", 0.5) if A else (300, 3, "к маю", 0.4)

    def fn(img, t, cam):
        cv = PH.background(t).convert("RGBA")
        if t < s2[0] - 0.1:   # лента новостей → вопрос
            for i, (s, x, y) in enumerate(HEAD):
                st = 0.1 + 0.28 * i; k = back(seg(t, st, st + 0.3)); fo = 1 - seg(t, s1[1] - 0.5, s1[1])
                if k > 0.02: PH.put(cv, PH.chip(s, PH.RED, 46), x + 6 * math.sin(t * 40 + i), y, a=fo * 0.9, scale=k)
            k = back(seg(t, 1.2, 1.6))
            if k > 0.02: PH.put(cv, PH.text_img("Если завтра", 104, PH.WHITE), PH.W / 2, 1000, scale=k); PH.put(cv, PH.text_img("сократят?", 120, PH.AMBER), PH.W / 2, 1130, scale=k)
        elif t < s3[0] - 0.1:
            a0, a1 = s2
            if A:
                PH.title(cv, t, a0, 999, ["Как обычно *считают*"], y=230)
                for i, (lab, v, y) in enumerate([("накоплено", "120 000 ₽", 470), ("зарплата", "150 000 ₽", 760)]):
                    k = eout(seg(t, a0 + 0.3 + 0.9 * i, a0 + 0.8 + 0.9 * i))
                    if k <= 0: continue
                    card, pad = PH.card(760, 210, 36); d = ImageDraw.Draw(card)
                    d.text((pad + 40, pad + 60), lab, font=PH.font("SemiBold", 40), fill=PH.SUB, anchor="lm"); d.text((pad + 40, pad + 140), v, font=PH.font("Bold", 76), fill=PH.WHITE, anchor="lm")
                    PH.put(cv, card, PH.W / 2, y, a=k)
                if t > a0 + 1.4: PH.put(cv, PH.text_img("÷", 90, PH.SUB), PH.W / 2, 615)
                k = back(seg(t, a0 + (a1 - a0) * 0.62, a0 + (a1 - a0) * 0.62 + 0.35))
                if k > 0.02: PH.put(cv, PH.text_img("0,8 месяца", 120, PH.RED), PH.W / 2, 1060, scale=k)
                if t > a0 + (a1 - a0) * 0.88: PH.put(cv, PH.chip("паника", PH.RED, 58), PH.W / 2, 1220)
            else:
                PH.title(cv, t, a0, 999, ["Подушка = *6 зарплат*"], y=230)
                k = seg(t, a0 + 0.8, a0 + (a1 - a0) * 0.45); v = int(900 * eout(k)) * 1000
                if k > 0: PH.put(cv, PH.text_img(f"{v:,} ₽".replace(",", " "), 150, PH.RED), PH.W / 2, 560)
                k2 = eout(seg(t, a0 + (a1 - a0) * 0.45, a0 + (a1 - a0) * 0.6))
                if k2 > 0:
                    bar = Image.new("RGBA", (880, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(bar)
                    d.rounded_rectangle([0, 0, 880, 56], 28, fill=(40, 52, 47, 255)); d.rounded_rectangle([0, 0, int(880 * 0.133 * k2) + 30, 56], 28, fill=PH.GREEN + (255,))
                    d.text((0, 110), "есть 120 000 из 900 000", font=PH.font("SemiBold", 40), fill=PH.SUB, anchor="lm"); PH.put(cv, bar, PH.W / 2, 800)
                if t > a0 + (a1 - a0) * 0.72: PH.put(cv, PH.chip("руки опускаются", PH.RED, 58), PH.W / 2, 1060)
        elif t < s4[0] - 0.1:
            a0, a1 = s3
            if A:
                PH.put(cv, struck("зарплата 150 000", 64, PH.SUB), PH.W / 2, 230)
                PH.title(cv, t, a0 + 1.0, 999, ["Живешь на *обязательное*"], y=360, size=66)
                rows(cv, t, a0 + 1.4, a0 + (a1 - a0) * 0.55, [("Аренда", 40, PH.BLUE, ""), ("Еда", 25, PH.BLUE, ""), ("Кредит", 12, PH.BLUE, ""), ("Связь", 3, PH.BLUE, "")], 40, 520, 135)
                k = back(seg(t, a0 + (a1 - a0) * 0.62, a0 + (a1 - a0) * 0.62 + 0.35))
                if k > 0.02: PH.put(cv, PH.text_img("120 000 ÷ 80 000", 64, PH.WHITE), PH.W / 2, 1100, scale=k); PH.put(cv, PH.text_img("1,5 месяца", 120, PH.GREEN), PH.W / 2, 1240, scale=k)
            else:
                PH.title(cv, t, a0, 999, ["Подушка на *твои траты*"], y=230, size=66)
                rows(cv, t, a0 + 0.8, a0 + (a1 - a0) * 0.5, [("Аренда", 40, PH.BLUE, ""), ("Еда", 25, PH.BLUE, ""), ("Кофе, бары, такси", 18, PH.AMBER, ""), ("Кредит", 12, PH.BLUE, ""), ("Связь и прочее", 5, PH.BLUE, "")], 40, 400, 125)
                k = back(seg(t, a0 + (a1 - a0) * 0.6, a0 + (a1 - a0) * 0.6 + 0.35))
                if k > 0.02:
                    PH.put(cv, PH.text_img("100 000 × 3 месяца", 60, PH.WHITE), PH.W / 2, 1040, scale=k)
                    PH.put(cv, PH.text_img("300 000 ₽", 130, PH.GREEN), PH.W / 2, 1180, scale=k)
                if t > a0 + (a1 - a0) * 0.85: PH.put(cv, struck("900 000", 56, PH.SUB), PH.W / 2, 1300)
        elif t < s5[0] - 0.1:
            a0, a1 = s4
            k = eout(seg(t, a0 + 0.2, a0 + 0.7))
            card, pad = PH.card(900, 620, 44, glow=PH.GREEN); d = ImageDraw.Draw(card)
            d.text((pad + 50, pad + 70), "Твоя подушка", font=PH.font("SemiBold", 44), fill=PH.SUB, anchor="lm")
            d.text((pad + 50, pad + 170), f"{target} 000 ₽", font=PH.font("Bold", 110), fill=PH.WHITE, anchor="lm")
            d.text((pad + 50, pad + 265), f"{months} месяца твоих трат", font=PH.font("SemiBold", 42), fill=PH.GREEN, anchor="lm")
            g = fill * eio(seg(t, a0 + (a1 - a0) * 0.55, a0 + (a1 - a0) * 0.85)) if t > a0 else 0
            d.rounded_rectangle([pad + 50, pad + 350, pad + 850, pad + 410], 30, fill=(40, 52, 47, 255))
            d.rounded_rectangle([pad + 50, pad + 350, pad + 50 + max(60, int(800 * g)), pad + 410], 30, fill=PH.GREEN + (255,))
            if t > a0 + (a1 - a0) * 0.8:
                d.text((pad + 50, pad + 500), "соберется", font=PH.font("SemiBold", 46), fill=PH.SUB, anchor="lm")
                d.text((pad + 290, pad + 500), date, font=PH.font("Bold", 64), fill=PH.GREEN, anchor="lm")
            PH.put(cv, card, PH.W / 2, 640, a=k)
            for i, s in enumerate(["бесплатно", "2 минуты"]):
                kk = back(seg(t, a0 + 0.9 + 0.3 * i, a0 + 1.2 + 0.3 * i))
                if kk > 0.02: PH.put(cv, PH.chip(s, PH.GREEN, 52, check=True), 330 + 420 * i, 1080, scale=kk)
        elif t < s6[0] - 0.1:
            a0, a1 = s5
            PH.title(cv, t, a0, 999, ["Каждая зарплата *150 000*"], y=230, size=66)
            if A: items = [("Обязательное", 80, PH.BLUE, ""), ("Жизнь как привык", 40, PH.AMBER, "кофе, бар, такси"), ("Подушка", 30, PH.GREEN, "15 000 с аванса и с зарплаты")]
            else: items = [("Траты", 100, PH.BLUE, "кофе, бары и такси уже здесь"), ("Кошелек", 20, PH.AMBER, "на непредвиденное"), ("Подушка", 30, PH.GREEN, "15 000 с аванса и с зарплаты")]
            rows(cv, t, a0 + 0.4, a0 + (a1 - a0) * 0.8, items, items[0][1], 470, 230)
            if A and t > a0 + (a1 - a0) * 0.7: PH.put(cv, PH.chip("ничего не урезали", PH.GREEN, 54, check=True), PH.W / 2, 1200)
        else:
            a0, a1 = s6
            PH.title(cv, t, a0, 999, ["Напиши в *комментах*"], y=300, size=78)
            k = back(seg(t, a0 + 0.2, a0 + 0.55))
            if k > 0.02:
                n = int(len("подушка") * seg(t, a0 + 0.6, a0 + 1.6)); cur = "|" if int(t * 3) % 2 else " "
                bub, pad = PH.card(820, 220, 60, glow=PH.GREEN); d = ImageDraw.Draw(bub)
                d.ellipse([pad + 40, pad + 60, pad + 140, pad + 160], fill=(230, 120, 40, 255))
                d.text((pad + 180, pad + 110), "подушка"[:n] + cur, font=PH.font("Bold", 92), fill=PH.WHITE, anchor="lm")
                PH.put(cv, bub, PH.W / 2, 640, scale=k)
            if t > a0 + 1.7:
                PH.put(cv, PH.text_img("пришлю ссылку", 70, PH.GREEN), PH.W / 2, 900)
                PH.put(cv, PH.text_img("↓", 140, PH.GREEN), PH.W / 2, 1060 + 20 * math.sin(t * 6))
        img.paste(cv.convert(img.mode), (0, 0))

    ep.add(0, end, "screen", fn)
    ep.sfx(0.1, "whoosh", 0.4)
    for i in range(4): ep.sfx(0.1 + 0.28 * i, "pop", 0.3)
    for s in (s2, s3, s4, s5, s6): ep.sfx(s[0] - 0.1, "whoosh", 0.3)
    ep.sfx(s6[0] + 0.2, "pop", 0.45)
    ep.dur = end; ep.cover_t = 1.9
    return ep

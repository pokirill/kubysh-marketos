"""Запас · пн 09.11 12:00 · «Британские ученые: сколько проживешь без зарплаты» (подушка по тратам, а не по доходу). Инфографика."""
from PIL import Image, ImageDraw, ImageFont
from studio import *  # noqa
import promo_hero as PH
from episodes.w07_common import setup, sayer, finale

V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W09/"


def serif(size, bold=True): return ImageFont.truetype("/System/Library/Fonts/Times.ttc", size, index=1 if bold else 0)


def build():
    ep = Ep("W09_Британские_ученые_подушка", "studio"); ep.sfxgain = 0.4; setup(ep)
    say = sayer(ep, V, Y=1400, SZ=54)
    a0, a1 = say("hero", "b1", "Британские ученые выяснили, сколько ты проживешь без зарплаты. *Проверяю на себе*", at=0.15)
    b0, b1 = say("hero", "b2", "Накоплено 90 тысяч. Зарплата 150. Выходит, меньше месяца. *Паника*", at=a1 + 0.3)
    c0, c1 = say("kubysh", "p1", "Не дели на зарплату. Без нее ты тратишь меньше: обязательное и еда, примерно 60 тысяч в месяц. Значит, *полтора месяца*", at=b1 + 0.4)
    d0, d1 = say("kubysh", "p2", "Хочешь три месяца? По 7 тысяч с каждой получки, и *к маю готово*", at=c1 + 0.4)
    e0, e1 = say("hero", "b5", "А на сколько месяцев хватит тебе? *Пиши в комменты*", at=d1 + 0.4)

    def fn(img, t, cam):
        cv = PH.background(t).convert("RGBA"); d = ImageDraw.Draw(cv)
        if t < a1 + 0.3:
            d.text((540, 250), "ВЕСТНИК НАУКИ · ЛОНДОН", font=serif(34, False), fill=(200, 200, 190), anchor="mm")
            d.line([(90, 300), (990, 300)], fill=(200, 200, 190), width=3)
            for i, s in enumerate(["Британские", "ученые", "выяснили*"]):
                if t > 0.1 + 0.15 * i: d.text((540, 430 + i * 150), s, font=serif(130), fill=(245, 242, 232), anchor="mm")
            if t > a0 + 1.2: d.text((540, 900), "сколько ты проживешь без зарплаты", font=serif(50, False), fill=PH.GREEN, anchor="mm")
            if t > a0 + 2.0: d.text((540, 1000), "*ученые это мы", font=serif(36, False), fill=(150, 150, 140), anchor="mm")
        elif t < b1 + 0.4:
            p = (t - b0) / max(0.1, b1 - b0)
            PH.put(cv, PH.text_img("90 000 ÷ 150 000", 96, PH.WHITE), PH.W / 2, 500)
            if p > 0.55: PH.put(cv, PH.text_img("= 0,6 месяца", 110, PH.RED), PH.W / 2, 680)
            if p > 0.8: PH.put(cv, PH.chip("паника", PH.RED, 70), PH.W / 2, 880)
        elif t < c1 + 0.4:
            p = (t - c0) / max(0.1, c1 - c0)
            PH.put(cv, PH.text_img("делим не на доход,", 60, PH.SUB, "SemiBold"), PH.W / 2, 330)
            PH.put(cv, PH.text_img("а на траты без зарплаты", 60, PH.WHITE, "SemiBold"), PH.W / 2, 410)
            if p > 0.35: PH.put(cv, PH.chip("обязательное и еда ≈ 60 000 / мес", PH.BLUE, 50), PH.W / 2, 560)
            if p > 0.55: PH.put(cv, PH.text_img("90 000 ÷ 60 000", 96, PH.WHITE), PH.W / 2, 740)
            if p > 0.75:
                k = eout(seg(t, c0 + (c1 - c0) * 0.75, c0 + (c1 - c0) * 0.75 + 0.4)); PH.put(cv, PH.text_img("= 1,5 месяца", 130, PH.GREEN), PH.W / 2, 930, a=k, scale=lerp(1.3, 1, k))
        elif t < d1 + 0.4:
            p = (t - d0) / max(0.1, d1 - d0)
            PH.title(cv, t, d0, d1 + 0.4, ["Цель: *3 месяца*", "180 000 ₽"], y=320)
            card, pad = PH.card(900, 260, 36, glow=PH.GREEN); dd = ImageDraw.Draw(card); x0, y0 = pad + 34, pad + 30
            v = lerp(90000, 180000, eio(seg(t, d0 + 0.8, d1)))
            dd.text((x0, y0), "+ 7 000 с каждой получки", font=PH.font("SemiBold", 42), fill=PH.WHITE)
            dd.rounded_rectangle([x0, y0 + 90, x0 + 830, y0 + 126], 18, fill=(44, 54, 50)); dd.rounded_rectangle([x0, y0 + 90, x0 + int(830 * v / 180000), y0 + 126], 18, fill=PH.GREEN)
            dd.text((x0, y0 + 150), f"{int(v):,} ₽".replace(",", " "), font=PH.font("Bold", 50), fill=PH.GREEN)
            if p > 0.7: dd.text((x0 + 830, y0 + 156), "готово к маю", font=PH.font("Bold", 44), fill=PH.AMBER, anchor="ra")
            PH.put(cv, card, PH.W / 2, 720)
        else:
            PH.title(cv, t, e0, 999, ["А на сколько месяцев", "*хватит тебе?*"], y=420, size=80)
            if t > e0 + 0.8: PH.put(cv, PH.chip("пиши в комменты", PH.GREEN, 60), PH.W / 2, 700)
        img.paste(cv.convert(img.mode), (0, 0))
    ep.add(0, 999, "screen", fn)
    ep.sfx(0.1, "boom", 0.4); ep.sfx(b0 + (b1 - b0) * 0.8, "marker", 0.5); ep.sfx(c0 + (c1 - c0) * 0.75, "kaching", 0.45); ep.sfx(d1 - 0.3, "ding", 0.4)
    h0 = finale(ep, say, e1 + 0.6, pill_y=1190)
    ep.ov[0] = (0, h0 - 0.05, "screen", fn)
    ep.cover_t = 1.4
    return ep

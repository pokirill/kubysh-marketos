"""К15 · вт 03.11 12:00 · «Куда уходят 150 000» (сценарий 82, v3). Инфографика в темном стиле промо, голос Holden."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as P
from episodes.scr import STY, RK
from episodes.lib import PHONE

V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
Y = 1360
ROWS = [("Аренда", 45000, P.BLUE), ("Кредит", 27000, P.BLUE), ("Коммуналка", 8000, P.BLUE), ("Связь и транспорт", 6000, P.BLUE)]


def build():
    ep = Ep("W03_K15_Куда_уходят_150", "studio"); ep.sfxgain = 0.4
    ep.avatars = {"kubysh": Image.open(RK + "Референсы/avatar_kubysh.png").convert("RGBA")}
    say = lambda f, cap, at=None, **kw: ep.say("kubysh", "", cap=cap, at=at, y=Y, size=kw.get("size", 54), file=V + f + "_f_48k.wav")
    h0, h1 = say("w15_hook", "Зарплата *150 тысяч.* Куда она делась за неделю?", at=0.15)
    r0, r1 = say("w15_rent", "Аренда, кредит, коммуналка, дорога. Это даже не траты, это уже *чужие деньги*", at=h1 + 0.35)
    l0, l1 = say("w15_left", "Остается *64.* Десять в подушку, остальное на 30 дней", at=r1 + 0.35)
    d0, d1 = say("w15_daily", "Примерно *1 800 в день.* Это твои деньги, без чувства вины", at=l1 + 0.35)
    f0, f1 = say("w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=d1 + 0.45)
    end = f1 + 1.6
    rt = [r0 + (r1 - r0) * k for k in (0.0, 0.13, 0.26, 0.42)]   # строки въезжают под слова
    lt_p, lt_d = l0 + (l1 - l0) * 0.3, l0 + (l1 - l0) * 0.62

    def value(t):
        v = 150000
        for (n, amt, c), st in zip(ROWS, rt): v -= amt * P.eio(P.span(t, st + 0.1, st + 0.6))
        v -= 10000 * P.eio(P.span(t, lt_p + 0.1, lt_p + 0.6))
        return v

    def fn(img, t, cam):
        cv = P.background(t).convert("RGBA")
        if t < h1 + 0.3:   # хук: зарплата крупно, резкий зум
            k = P.eout(P.span(t, 0.0, 0.5))
            P.title(cv, t, 0.6, h1 + 0.3, ["Куда она делась", "*за неделю?*"], y=420, accent=P.RED)
            P.big_number(cv, 150000, 860, a=k, scale=P.lerp(1.35, 1, k), size=200)
            P.put(cv, P.text_img("пришла зарплата", 46, P.GREEN, "SemiBold"), P.W / 2, 1010, a=k)
        elif t < l1 + 0.3:   # водопад обязательного, затем подушка и остаток на 30 дней
            v = value(t); kk = P.span(t, l0, l0 + 0.4)
            P.put(cv, P.text_img("осталось" if t > rt[0] + 0.3 else "зарплата", 44, P.SUB, "SemiBold"), P.W / 2, 330)
            P.big_number(cv, v, 470, size=160, color=P.GREEN if t > l0 else P.WHITE)
            if t < l0 + 0.4:
                for i, ((n, amt, c), st) in enumerate(zip(ROWS, rt)):
                    k = P.eout(P.span(t, st, st + 0.45)) * (1 - kk)
                    if k <= 0: continue
                    im, pad = P.card(940, 150, 36); d = ImageDraw.Draw(im); x0, y0 = pad + 34, pad + 30
                    d.rounded_rectangle([x0, y0, x0 + 16, y0 + 90], 8, fill=c)
                    d.text((x0 + 44, y0 + 18), n, font=P.font("Bold", 48), fill=P.WHITE)
                    d.text((pad + 940 - 34, y0 + 18), "−" + P.rub(amt), font=P.font("Bold", 50), fill=P.WHITE, anchor="ra")
                    P.put(cv, im, P.W / 2 + 120 * (1 - k), 660 + i * 150, a=k)
                ka = P.eout(P.span(t, r0 + (r1 - r0) * 0.55, r0 + (r1 - r0) * 0.55 + 0.4)) * (1 - kk)
                if ka > 0: P.put(cv, P.chip("это уже чужие деньги", P.RED, 52), P.W / 2, 1260, a=ka, scale=P.lerp(1.2, 1, ka))
            else:
                k = P.eout(P.span(t, lt_p, lt_p + 0.45))
                if k > 0:
                    im, pad = P.card(940, 150, 36); d = ImageDraw.Draw(im); x0, y0 = pad + 34, pad + 30
                    d.rounded_rectangle([x0, y0, x0 + 16, y0 + 90], 8, fill=P.GREEN)
                    d.text((x0 + 44, y0 + 18), "В подушку", font=P.font("Bold", 48), fill=P.WHITE)
                    d.text((pad + 940 - 34, y0 + 18), "−10 000", font=P.font("Bold", 50), fill=P.WHITE, anchor="ra")
                    P.put(cv, im, P.W / 2 + 120 * (1 - k), 700, a=k)
                k = P.eout(P.span(t, lt_d, lt_d + 0.45))
                if k > 0: P.put(cv, P.chip("54 000 ₽ на 30 дней", P.GREEN, 56), P.W / 2, 940, a=k, scale=P.lerp(1.2, 1, k))
        else:   # итог: сумма в день
            k = P.eout(P.span(t, l1 + 0.3, l1 + 1.0))
            P.put(cv, P.text_img("твои деньги на день", 46, P.SUB, "SemiBold"), P.W / 2, 560, a=k)
            v = 1800 * P.eio(P.span(t, l1 + 0.3, l1 + 1.2))
            P.big_number(cv, round(v / 10) * 10, 760, size=220, color=P.GREEN, suffix=" ₽", scale=1 + 0.06 * P.clamp(1 - abs(t - l1 - 1.3) * 4))
            kc = P.eout(P.span(t, d0 + (d1 - d0) * 0.55, d0 + (d1 - d0) * 0.55 + 0.4))
            if kc > 0: P.put(cv, P.chip("без чувства вины", P.GREEN, 56, check=True), P.W / 2, 1000, a=kc, scale=P.lerp(1.2, 1, kc))
        img.paste(cv.convert(img.mode), (0, 0))
    ep.add(0, f0 - 0.05, "screen", fn)
    ep.sfx(0.1, "boom", 0.4)
    for st in rt: ep.sfx(st, "pop", 0.4)
    ep.sfx(lt_p, "pop", 0.4); ep.sfx(lt_d, "pop", 0.4); ep.sfx(l1 + 1.2, "kaching", 0.4)
    ep.clip(f0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - f0)))
    ep.pill(f0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, 1190, size=46, **STY["green"]); ep.sfx(f0 + 1.0, "pop", 0.4)
    ep.dur = end; ep.cover_t = 1.0
    return ep

"""V1 · «Зарплата — это пицца» (серия «Осознанно = круто», ~28 с). Понятно даже ребенку: зарплату режем как пиццу —
кусок на обязательное, кусок сразу в копилку, остальное на дни до аванса; сегодняшний кусок — 4 250, его едим спокойно.
Финал — настоящий «стартовый план» Ксюши из приложения. CTA: «напиши ПЛАН». Голоса: Кубыш Holden, Душная — клон.
"""
import math
from PIL import ImageDraw
from studio import *  # noqa

R = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/"
VO = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/V_серия/"
PLAN = R + "Запись_экрана/стартовый_план_ксюши.png"
BG = (246, 240, 230)
CX, CY, RAD = 540, 790, 330
TOTAL, MUST, PIG = 138000, 30000, 40000
DAYS = 16
GREEN = dict(bg=(30, 130, 88), fg=WHITE)
DARK = dict(bg=(60, 50, 90), fg=WHITE)


def angles():
    a_must = 360 * MUST / TOTAL; a_pig = 360 * PIG / TOTAL
    return (-90, -90 + a_must), (-90 + a_must, -90 + a_must + a_pig), (-90 + a_must + a_pig, 270)


def pizza_layer(ep, t0, t1, tm, tp, tc, tt):
    """tm — уходит кусок «обязательное», tp — кусок в копилку, tc — режем остаток на дни, tt — сегодняшний кусок."""
    (m0, m1), (p0, p1), (r0, r1) = angles()
    step = (r1 - r0) / DAYS
    def slice_(d, a0, a1, off, color, k=1.0):
        mid = math.radians((a0 + a1) / 2); dx, dy = math.cos(mid) * off, math.sin(mid) * off
        rr = RAD * k
        box = [CX + dx - rr, CY + dy - rr, CX + dx + rr, CY + dy + rr]
        d.pieslice(box, a0, a1, fill=(214, 150, 74))
        inner = [box[0] + 22 * k, box[1] + 22 * k, box[2] - 22 * k, box[3] - 22 * k]
        d.pieslice(inner, a0, a1, fill=color)
        for j in range(3):  # пепперони
            ang = math.radians(a0 + (a1 - a0) * (j + 0.5) / 3); r = rr * (0.45 + 0.18 * (j % 2))
            px, py = CX + dx + math.cos(ang) * r, CY + dy + math.sin(ang) * r
            if (a1 - a0) > 12: d.ellipse([px - 26 * k, py - 26 * k, px + 26 * k, py + 26 * k], fill=(196, 60, 48))
    def fn(img, t, cam):
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, W, H], fill=BG)
        pin = back(seg(t, t0, t0 + 0.45), 1.4)
        if pin < 0.02: return
        cheese = (250, 214, 120)
        om = 160 * eio(seg(t, tm, tm + 0.6)); op = 160 * eio(seg(t, tp, tp + 0.6))
        slice_(d, m0, m1, om, (236, 236, 236) if t > tm else cheese, pin)
        slice_(d, p0, p1, op, (255, 190, 200) if t > tp else cheese, pin)
        cut = seg(t, tc, tc + 1.4)
        for i in range(DAYS):
            a0 = r0 + i * step; a1 = a0 + step
            pop = 90 * back(seg(t, tt, tt + 0.5), 1.6) if i == 0 else 0
            col = MINT if (i == 0 and t > tt) else cheese
            slice_(d, a0, a1, pop, col, pin)
        if cut > 0:  # линии разреза появляются по кругу
            for i in range(int(DAYS * cut) + 1):
                ang = math.radians(r0 + i * step)
                d.line([CX, CY, CX + math.cos(ang) * RAD * pin, CY + math.sin(ang) * RAD * pin], fill=(150, 98, 40), width=6)
        if t < tm:
            s = scaled(word_img("138 000 ₽", 110, fill=WHITE), pin); comp(img, s, CX - s.width / 2, CY - s.height / 2)
    ep.add(t0, t1, "screen", fn)


def build():
    ep = Ep("V01_Зарплата_пицца", "studio")
    ep.vgain = 0.95
    from PIL import Image as _I
    ep.avatars = {w: _I.open(R + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("ksy", "kubysh", "dush")}

    # 1 · хук: огромное число на светлом фоне
    a0, a1 = ep.say("kubysh", "", cap="Пришла зарплата. Сколько можно потратить *сегодня?*", at=0.2, file=VO + "п1.wav", y=1450)
    def big(img, t, cam):
        d = ImageDraw.Draw(img); d.rectangle([0, 0, W, H], fill=BG)
        k = back(seg(t, 0.0, 0.4), 1.6)
        s = scaled(word_img("138 000 ₽", 170, fill=INK, stroke=BG), k); comp(img, s, 540 - s.width / 2, 760)
    ep.add(0, a1 + 0.1, "screen", big)

    # 2 · Душная на своем крупном плане (клип К2: губы на 0,7–2,0 и 3,5–5,0 с)
    s2 = a1 + 0.1
    b0, b1 = ep.say("dush", "", cap="Нисколько… а вдруг не *хватит?*", at=s2 + 0.1, file=VO + "д_нисколько.mp3", y=1400)
    cut = b0 + 1.15; s3 = b1 + 0.15
    ep.clip(s2, cut, R + "K02_клипы/S1b.mp4", "D1", src_t0=0.6)
    ep.clip(cut, s3, R + "K02_клипы/S1b.mp4", "D2", src_t0=3.45)

    # 3 · пицца: обязательное, копилка, дни, сегодняшний кусок
    c0, c1 = ep.say("kubysh", "", cap="Смотри, зарплата — это *пицца*", at=s3 + 0.15, file=VO + "п2.wav", y=1450)
    d0, d1 = ep.say("kubysh", "", cap="Первый кусок — *обязательное*", at=c1 + 0.2, file=VO + "п3.wav", y=1450)
    e0, e1 = ep.say("kubysh", "", cap="Второй — в *копилку,* сразу, пока не съели", at=d1 + 0.2, file=VO + "п4.wav", y=1450)
    f0, f1 = ep.say("kubysh", "", cap="Остальное режем на *дни* до аванса", at=e1 + 0.2, file=VO + "п5.wav", y=1450)
    g0, g1 = ep.say("kubysh", "", cap="Сегодня твой кусок — *4 250.* И его можно съесть *спокойно*", at=f1 + 0.2, file=VO + "п6.wav", y=1450, size=74)
    pizza_layer(ep, s3, g1 + 0.3, d0 + 0.3, e0 + 0.3, f0 + 0.2, g0 + 0.8)
    ep.pill(d0 + 0.6, g1 + 0.3, "Обязательное 30 000", 790, 330, size=40, bg=(90, 90, 96), fg=WHITE)
    ep.pill(e0 + 0.6, g1 + 0.3, "Копилка 40 000", 800, 1090, size=40, bg=(214, 80, 110), fg=WHITE)
    ep.pill(f0 + 0.8, g1 + 0.3, "16 дней до аванса", 540, 1330, size=46, **DARK)
    ep.counter(g0 + 0.9, g1 + 0.3, 0, 4250, 540, 1225, size=110, color=MINT)
    ep.sfx(d0 + 0.3, "swish", 0.4); ep.sfx(e0 + 0.3, "kaching", 0.5); ep.sfx(f0 + 0.2, "scribble", 0.4)

    # 4 · настоящий план Ксюши в приложении + призыв
    h0, h1 = ep.say("kubysh", "", cap="Я режу так каждую зарплату. За *две минуты*", at=g1 + 0.4, file=VO + "п7.wav", y=1480, size=68)
    tE = h1 + 2.4
    def bg2(img, t, cam):
        ImageDraw.Draw(img).rectangle([0, 0, W, H], fill=BG)
    ep.add(g1 + 0.3, tE, "screen", bg2)
    ep.card(g1 + 0.35, tE, PLAN, keys=[(g1 + 0.35, (0, 330, 1206, 2100), 540, 760, 760)], marks=[(h0 + 0.8, (60, 1330, 1150, 1700), MINT)])
    ep.pill(h1 + 0.2, tE, "Напиши ПЛАН — пришлю, как разрезать твою", 540, 1720, size=40, **DARK)
    ep.pill(h1 + 0.5, tE, "Кубыш · бесплатно до следующей зарплаты", 540, 1820, size=36, **GREEN)
    ep.dur = tE; ep.cover_t = 0.6
    return ep

"""К6 · вс 08.11 18:00 · «Отпуск когда-нибудь» (сценарий 82 v3). Жабы на риге, отпуск 240 000 частями, «Египет», поворот: Душная гуглит шезлонг."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
import frog
from episodes.scr import STY
from episodes.w07_common import setup, sayer, finale

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W08/"


def beach():
    im = Image.new("RGBA", (520, 900), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 519, 899], 60, fill=(20, 20, 24)); w = Image.new("RGB", (480, 860))
    dw = ImageDraw.Draw(w)
    for y in range(860):
        c = (int(120 + 100 * y / 500), int(190 + 40 * y / 500), 255) if y < 480 else ((40, 150, 200) if y < 620 else (240, 214, 160))
        dw.line([(0, y), (480, y)], fill=c)
    dw.ellipse([330, 80, 430, 180], fill=(255, 220, 90)); m = Image.new("L", (480, 860), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 479, 859], 46, fill=255)
    im.paste(w, (20, 20), m); return im


def build():
    ep = Ep("W08_K6_Отпуск_когда-нибудь", "room"); ep.sfxgain = 0.5; setup(ep)
    say = sayer(ep, V)
    kub = ep.actor("kub", "kubysh", 800, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)
    kub.expr(0, "worried")
    a0, a1 = say("hero", "v1", "Каждый год говоришь: в этом году точно отпуск. И каждый год *х**ня*", at=0.2)
    bch = beach()
    ep.add(0, a1 + 0.2, "screen", lambda img, t, cam: comp(img, fade(scaled(bch, 0.7), eout(seg(t, 0, 0.4)) * (1 - ease(seg(t, a1, a1 + 0.2)))), 540 - 182, 140))
    for i, y in enumerate(("2024", "2025", "2026")):
        tt = a0 + (a1 - a0) * (0.35 + 0.18 * i); ep.pill(tt, a1 + 0.2, f"{y}: нет" if i < 2 else f"{y}: ?", 270 + 270 * i, 860, size=44, **STY["red" if i < 2 else "dark"]); ep.sfx(tt, "pop", 0.35)
    # 2 · Душная
    dush.show(a1 - 0.3); dush.go(a1 - 0.3, 270, hop=60, step=300); dush.expr(a1 - 0.3, "teacher")
    b0, b1 = say("dush", "d1", "Отпуск для богатых. Твой пляж это ванна, а море это *соль для ванны*", at=a1 + 0.2, a=dush)
    ep.shot(b0, ("dush", "kub"), dur=0.4)
    ep.pill(b0 + (b1 - b0) * 0.4, b1 + 0.2, "пляж = ванна", 540, 420, size=56, **STY["dark"]); ep.pill(b0 + (b1 - b0) * 0.75, b1 + 0.2, "море = соль для ванны", 540, 540, size=56, **STY["dark"])
    # 3 · Кубыш: частями
    c0, c1 = say("kubysh", "k1", "Давай не копить год с нуля. Билеты с этой получки, отель потом, на месте к маю. Бюджет дня *около 1 900* вместо 2 300", at=b1 + 0.3, a=kub)
    kub.expr(c0, "proud"); dush.expr(c0, "skeptic"); ep.shot(c0, "wide")
    rows = [("Билеты", "60 000", "с получек ноября"), ("Отель", "120 000", "декабрь – март"), ("На месте", "60 000", "к маю")]
    rt = [c0 + (c1 - c0) * k for k in (0.2, 0.37, 0.5)]

    def plan(img, t, cam, t1=None):
        k = eout(seg(t, c0, c0 + 0.4)) * (1 - ease(seg(t, ep.PE - 0.2, ep.PE)))
        if k <= 0.02: return
        cv, pad = PH.card(960, 700, 40, glow=PH.AMBER); d = ImageDraw.Draw(cv); x0, y0 = pad + 34, pad + 30
        d.text((x0, y0), "Отпуск · 240 000 ₽", font=PH.font("Bold", 50), fill=PH.WHITE)
        for i, (a, b, c) in enumerate(rows):
            if t < rt[i]: continue
            yy = y0 + 90 + i * 140; d.rounded_rectangle([x0, yy, x0 + 890, yy + 120], 24, fill=(30, 40, 37))
            d.rounded_rectangle([x0 + 20, yy + 20, x0 + 32, yy + 100], 6, fill=PH.AMBER)
            d.text((x0 + 56, yy + 16), a, font=PH.font("Bold", 46), fill=PH.WHITE); d.text((x0 + 56, yy + 72), c, font=PH.font("Medium", 34), fill=PH.SUB)
            d.text((x0 + 870, yy + 34), b, font=PH.font("Bold", 50), fill=PH.AMBER, anchor="ra")
        if t >= c0 + (c1 - c0) * 0.68:
            d.text((x0, y0 + 540), "в день ≈ 1 900", font=PH.font("Bold", 56), fill=PH.GREEN); d.text((x0 + 450, y0 + 556), "было 2 300", font=PH.font("Medium", 38), fill=PH.SUB)
        if t >= ep.TD:
            d.rounded_rectangle([x0 + 560, y0 - 6, x0 + 890, y0 + 64], 30, fill=(30, 130, 88)); d.text((x0 + 725, y0 + 29), "15 мая", font=PH.font("Bold", 44), fill=PH.WHITE, anchor="mm")
        comp(img, fade(cv, k), 540 - cv.width / 2, 160)
    ep.add(c0, 999, "screen", plan)
    for x in rt: ep.sfx(x, "tick", 0.45)
    # 4 · «А когда я поеду в Египет?» — «15 мая»
    e0, e1 = say("hero", "v2", "А когда я поеду *в Египет?*", at=c1 + 0.3)
    f0, f1 = say("kubysh", "k2", "*15 мая*", at=e1 + 0.2, a=kub)
    ep.TD = f0 + 0.1; ep.sfx(f0 + 0.1, "kaching", 0.5); kub.expr(f0, "happy")
    ep.PE = f1 + 0.6
    # 5 · поворот: Душная гуглит шезлонг в Хургаде
    g0, g1 = say("kubysh", "k3", "Когда у отпуска есть дата, *он перестает быть мечтой*", at=f1 + 0.7, a=kub)
    q = "сколько стоит шезлонг в Хургаде"
    def search(img, t, cam, t0=f1 + 0.6):
        if t < t0: return
        n = int(len(q) * seg(t, t0 + 0.2, t0 + 2.2))
        cv, pad = PH.card(940, 140, 70); d = ImageDraw.Draw(cv)
        d.ellipse([pad + 34, pad + 44, pad + 74, pad + 84], outline=PH.SUB, width=5); d.line([(pad + 70, pad + 80), (pad + 88, pad + 98)], fill=PH.SUB, width=5)
        d.text((pad + 110, pad + 70), q[:n] + ("|" if int(t * 3) % 2 else ""), font=PH.font("Medium", 42), fill=PH.WHITE, anchor="lm")
        comp(img, cv, 540 - cv.width / 2, 420)
    ep.add(f1 + 0.6, 999, "screen", lambda img, t, cam: search(img, t, cam) if t < ep.FIN else None)
    dush.expr(f1 + 0.6, "side"); ep.shot(f1 + 0.6, "dush", z=1.25); ep.pill(f1 + 0.8, g1 + 0.6, "Душная тайком", 540, 330, size=46, **STY["yellow"])
    for i in range(8): ep.sfx(f1 + 0.8 + 0.25 * i, "tick", 0.25)
    ep.FIN = g1 + 0.6
    finale(ep, say, g1 + 0.7, (kub, dush))
    ep.cover_t = 1.2
    return ep

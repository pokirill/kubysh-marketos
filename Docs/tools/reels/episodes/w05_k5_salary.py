"""К5 · чт 05.11 18:00 · «Зарплата пришла» (сценарий 82 v3). Жабы на риге, три стопки кодом. Голоса Holden и клон Душной."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
import audio
import frog
from episodes.scr import STY, RK
from episodes.lib import PHONE

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W05/"
V3 = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
Y, SZ = 1100, 54
STACKS = [("Обязательное и жизнь", "58 000", PH.BLUE, ["кредит · коммуналка", "продукты · транспорт", "маркетплейсы"]),
          ("Кошелек", "5 000", PH.AMBER, ["на непредвиденное"]),
          ("Накопления", "12 000", PH.GREEN, ["подушка 7 000", "отпуск 5 000"])]


def stacks_card(t, ts, warn=None, glow_wallet=None):
    cv, pad = PH.card(980, 760, 40); d = ImageDraw.Draw(cv); x0, y0 = pad + 34, pad + 30
    d.text((x0, y0), "Зарплата 75 000 ₽", font=PH.font("Bold", 46), fill=PH.WHITE)
    for i, (name, amt, col, subs) in enumerate(STACKS):
        if t < ts[i]: continue
        k = eout(seg(t, ts[i], ts[i] + 0.4)); yy = y0 + 90 + i * 215; xx = x0 + int(60 * (1 - k))
        fill = (30, 40, 37)
        if i == 1 and glow_wallet and t >= glow_wallet: fill = (60, 52, 26)
        if i == 2 and warn and warn[0] <= t < warn[1]: fill = (70, 30, 34)
        d.rounded_rectangle([xx, yy, xx + 900, yy + 195], 26, fill=fill)
        d.rounded_rectangle([xx + 20, yy + 22, xx + 34, yy + 172], 7, fill=col)
        d.text((xx + 60, yy + 22), name, font=PH.font("Bold", 46), fill=PH.WHITE)
        d.text((xx + 880, yy + 22), amt, font=PH.font("Bold", 50), fill=col, anchor="ra")
        for j, s in enumerate(subs): d.text((xx + 60, yy + 86 + j * 36), s, font=PH.font("Medium", 36), fill=PH.SUB)
        if i == 2 and warn and warn[0] <= t < warn[1]:
            d.text((xx + 880, yy + 110), "−4 000 бар", font=PH.font("Bold", 42), fill=PH.RED, anchor="ra")
    return cv


def build():
    ep = Ep("W05_K5_Зарплата_пришла", "room"); ep.sfxgain = 0.5
    ep.avatars = {w: Image.open(RK + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("kubysh", "dush")}
    kub = ep.actor("kub", "kubysh", 800, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)

    def say(who, f, cap, at, a=None, v=V):
        t0, t1 = ep.say(who, "", cap=cap, at=at, y=Y, size=SZ, file=v + f + "_t_48k.wav")
        if a is not None:
            smp = ep.voice[-1][1]; env = audio.envelope(smp, FPS); e = ep.env.setdefault(a.name, [0.0] * int(400 * FPS)); f0 = int(t0 * FPS)
            for i, x in enumerate(env):
                if f0 + i < len(e): e[f0 + i] = max(e[f0 + i], x)
        return t0, t1

    # 1 · пришла зарплата, Душная спорит
    ep.notif(0.1, 2.6, "Банк · сейчас", "Зарплата +75 000 ₽", icon="₽", color=(40, 160, 96)); ep.coins(0.3, n=30, dur=1.8)
    kub.expr(0, "happy"); kub.jump(0.4)
    dush.show(0.6); dush.go(0.6, 270, hop=60, step=300); dush.expr(0.6, "smug")
    a0, a1 = say("dush", "d1", "Пришла зарплата. Спорим, через три дня ее *уже не будет?*", at=0.8, a=dush)
    ep.shot(a0 + 1.0, ("dush", "kub"), dur=0.4); kub.expr(a1 - 0.6, "worried")
    b0, b1 = say("dush", "d2", "Все в копилку. А жить будешь *на дошиках*", at=a1 + 0.2, a=dush)
    dush.expr(b0, "teacher"); ep.pill(b0 + 0.2, b1 + 0.2, "75 000 → в копилку", 540, 420, size=54, **STY["dark"])
    ep.pill(b0 + (b1 - b0) * 0.6, b1 + 0.2, "на жизнь: дошики", 540, 540, size=54, **STY["red"]); ep.sfx(b0 + (b1 - b0) * 0.6, "pop", 0.4)
    # 2 · Кубыш: три стопки
    c0, c1 = say("kubysh", "k1", "Давай так, три стопки. Обязательное и все на жизнь. Кошелек на непредвиденное. И накопления, там уже *подушка и отпуск*", at=b1 + 0.3, a=kub)
    kub.expr(c0, "proud"); ep.shot(c0, "wide")
    ts = [c0 + (c1 - c0) * k for k in (0.2, 0.47, 0.68)]
    for x in ts: ep.sfx(x, "pop", 0.45)
    # 3 · Душная тянется к кошельку
    d0, d1 = say("dush", "d3", "Кошелек лишний, давай тоже *в копилку*", at=c1 + 0.25, a=dush)
    dush.expr(d0, "dush_mad"); dush.react(d0 + 0.3, "lean")
    # 4 · Кубыш: без кошелька бар из копилки
    e0, e1 = say("kubysh", "k2", "Без кошелька первый же бар с друзьями ты оплатишь из копилки. И скажешь: *доложу потом*", at=d1 + 0.25, a=kub)
    kub.expr(e0, "teacher"); ep.sfx(e0 + (e1 - e0) * 0.5, "crunch", 0.4)
    f0, f1 = say("kubysh", "k3", "Кошелек нужен, чтобы *копилка не стала кошельком*", at=e1 + 0.2, a=kub)
    kub.expr(f0, "proud"); dush.expr(f0, "skeptic"); ep.sfx(f0 + 0.3, "ding", 0.4)
    warn = (e0 + (e1 - e0) * 0.35, f0)
    ep.add(c0 - 0.1, f1 + 0.3, "screen", lambda img, t, cam: comp(img, fade(stacks_card(t, ts, warn, f0 + 0.2), eout(seg(t, c0 - 0.1, c0 + 0.3)) * (1 - ease(seg(t, f1 + 0.1, f1 + 0.3)))), 30, 150))
    # 5 · копишь без отказов: полоса до аванса и рост накоплений
    g0, g1 = say("kubysh", "k4", "И копишь, *не отказывая себе в жизни*", at=f1 + 0.35, a=kub)
    kub.expr(g0, "happy"); dush.go(g0, -380, hop=60, step=320)
    def grow(img, t, cam, t0=g0 - 0.1, t1=g1 + 1.0):
        k = eout(seg(t, t0, t0 + 0.3)) * (1 - ease(seg(t, t1 - 0.2, t1)))
        cv, pad = PH.card(900, 330, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 34, pad + 30
        p = eio(seg(t, t0 + 0.2, t1 - 0.4))
        d.text((x0, y0), "Накопления", font=PH.font("SemiBold", 40), fill=PH.SUB)
        d.text((x0, y0 + 56), f"{int(12000 * p):,} ₽".replace(",", " "), font=PH.font("Bold", 90), fill=PH.GREEN)
        d.rounded_rectangle([x0, y0 + 190, x0 + 830, y0 + 222], 16, fill=(44, 54, 50)); d.rounded_rectangle([x0, y0 + 190, x0 + int(830 * max(0.03, p)), y0 + 222], 16, fill=PH.GREEN)
        comp(img, fade(cv, k), 540 - cv.width / 2, 300)
    ep.add(g0 - 0.1, g1 + 1.0, "screen", grow); ep.sfx(g1 + 0.6, "kaching", 0.4)
    # 6 · финал
    h0, h1 = say("kubysh", "w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=g1 + 1.1, v=V3)
    end = h1 + 1.4
    for a in (kub, dush): a.show(h0 - 0.05, False)
    ep.clip(h0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - h0)))
    ep.pill(h0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, 1420, size=46, **STY["green"]); ep.sfx(h0 + 1.0, "pop", 0.4)
    ep.dur = end; ep.cover_t = 1.0
    return ep

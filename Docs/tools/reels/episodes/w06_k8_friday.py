"""К8 · пт 06.11 18:00 · «Пятница, до зарплаты 5 дней» (сценарий 82 v3). Жабы на риге, бар — фон Higgsfield.
Голоса: герой Archie (мат запикан), Душная клон, Кубыш Holden."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
import props as P
import audio
import frog
from episodes.scr import STY, RK
from episodes.lib import PHONE

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W06/"
V3 = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
BAR = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы маскот/бар.png"
Y, SZ = 1100, 54


def plan_card(t, t0, t_hi):
    cv, pad = PH.card(940, 560, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 34, pad + 30
    d.text((x0, y0), "До зарплаты 5 дней · 11 400 ₽", font=PH.font("Bold", 42), fill=PH.WHITE)
    rows = [("Платежи", "2 600", "отложено", PH.BLUE), ("Еда и жизнь", "5 000", "отложено", PH.BLUE), ("Развлечения", "3 000", "не тронуто", PH.AMBER)]
    for i, (a, b, c, col) in enumerate(rows):
        if t < t0 + 0.3 + 0.5 * i: continue
        yy = y0 + 90 + i * 140; hi = i == 2 and t >= t_hi
        d.rounded_rectangle([x0, yy, x0 + 870, yy + 120], 24, fill=(70, 58, 26) if hi else (30, 40, 37))
        d.rounded_rectangle([x0 + 20, yy + 20, x0 + 32, yy + 100], 6, fill=col)
        d.text((x0 + 56, yy + 18), a, font=PH.font("Bold", 44), fill=PH.WHITE)
        d.text((x0 + 56, yy + 72), c if i < 2 else "было 3 500 · " + c, font=PH.font("Medium", 32), fill=PH.SUB)
        d.text((x0 + 850, yy + 40), b, font=PH.font("Bold", 50), fill=col if i == 2 else PH.WHITE, anchor="ra")
    return cv


def build():
    ep = Ep("W06_K8_Пятница", "room"); ep.sfxgain = 0.5
    ep.avatars = {w: Image.open(RK + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("kubysh", "dush")}
    def badge(txt, col):   # аватар для голосов без персонажа в кадре: кружок с подписью
        im = Image.new("RGBA", (104, 104), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse([2, 2, 101, 101], fill=col + (255,), outline=(255, 255, 255, 255), width=5)
        d.text((52, 54), txt, font=PH.font("Bold", 38 if len(txt) > 1 else 50), fill=(255, 255, 255), anchor="mm"); return im
    ep.avatars["hero"] = badge("ТЫ", (230, 120, 40)); ep.avatars["friend"] = badge("П", (60, 110, 230))
    kub = ep.actor("kub", "kubysh", 800, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)

    def say(who, f, cap, at, a=None, v=V):
        t0, t1 = ep.say(who, "", cap=cap, at=at, y=Y, size=SZ, file=v + f + "_t_48k.wav")
        if a is not None:
            smp = ep.voice[-1][1]; env = audio.envelope(smp, FPS); e = ep.env.setdefault(a.name, [0.0] * int(400 * FPS)); f0 = int(t0 * FPS)
            for i, x in enumerate(env):
                if f0 + i < len(e): e[f0 + i] = max(e[f0 + i], x)
        return t0, t1

    # 1 · пятница, зовут в бар, на карте 11 400
    kub.expr(0, "worried")
    q0, q1 = say("friend", "fr", "Братан, сегодня в восемь *в бар.* Ты с нами?", at=0.25)
    ep.notif(0.1, q1 + 0.6, "Пацаны · 17:58", "Сегодня в 20:00 в бар. Ты с нами?", icon="П", color=(60, 110, 230))
    kub.react(q1 - 0.3, "shudder")
    a0, a1 = say("hero", "f1", "Пятница. До зарплаты 5 дней, на карте 11 тысяч. И х*р его знает, *сколько из них мои*", at=q1 + 0.25)
    ep.pill(a0 + 1.6, a1 + 0.2, "до зарплаты 5 дней", 540, 560, size=54, **STY["red"]); ep.pill(a0 + 2.6, a1 + 0.2, "на карте 11 400 ₽", 540, 680, size=54, **STY["dark"])
    ep.sfx(a0 + 1.6, "pop", 0.4); ep.sfx(a0 + 2.6, "pop", 0.4)
    # 2 · Душная
    dush.show(a1 - 0.3); dush.go(a1 - 0.3, 270, hop=60, step=300); dush.expr(a1 - 0.3, "smug")
    b0, b1 = say("dush", "d1", "Сиди дома. Посмотришь их сторис, *почти как был*", at=a1 + 0.2, a=dush)
    ep.shot(b0, ("dush", "kub"), dur=0.4)
    # 3 · герой прикидывает в голове
    c0, c1 = say("hero", "f2", "Проезд, продукты, еще интернет 18-го… Вроде хватает. А вроде, бл**ь, *и нет*", at=b1 + 0.25)
    for i, (txt, x, y) in enumerate([("проезд ?", 300, 420), ("продукты ?", 760, 520), ("интернет 18-го ?", 470, 640)]):
        tt = c0 + 0.2 + 0.7 * i; ep.pill(tt, c1 + 0.2, txt, x, y, size=50, **STY["dark"]); ep.sfx(tt, "pop", 0.35)
    ep.pill(c0 + (c1 - c0) * 0.62, c1 + 0.2, "хватает???", 540, 800, size=64, **STY["red"]); kub.react(c0 + (c1 - c0) * 0.62, "shudder")
    # 4 · Кубыш показывает план
    d0, _ = say("kubysh", "k1", "Смотри. Платежи и еда до зарплаты *уже отложены*", at=c1 + 0.3, a=kub)
    _, d1 = say("kubysh", "k2", "На развлечения у тебя было 3 500, и *3 000 еще не тронуто*", at=None, a=kub)
    kub.expr(d0, "proud"); dush.expr(d0, "skeptic"); ep.shot(d0, "wide")
    t_hi = d1 - 1.6
    ep.add(d0 - 0.1, d1 + 0.3, "screen", lambda img, t, cam: comp(img, fade(plan_card(t, d0, t_hi), eout(seg(t, d0 - 0.1, d0 + 0.3)) * (1 - ease(seg(t, d1 + 0.1, d1 + 0.3)))), 70, 200))
    for i in range(3): ep.sfx(d0 + 0.3 + 0.5 * i, "tick", 0.45)
    ep.sfx(t_hi, "ding", 0.4)
    # 5 · бар; поворот: Душная за соседним столом с водой
    tb = d1 + 0.35
    ep.TB = tb; ep.sfx(tb, "swish", 0.5)
    kub.expr(tb, "happy"); dush.place(tb, 230); dush.expr(tb, "neutral"); ep.shot(tb, "wide")
    e0, e1 = say("kubysh", "k3", "Бар влезает в план. *Решать тебе*", at=tb + 0.3, a=kub)
    glass = Image.new("RGBA", (90, 130), (0, 0, 0, 0)); g = ImageDraw.Draw(glass)
    g.polygon([(8, 4), (82, 4), (72, 126), (18, 126)], fill=(200, 230, 255, 150), outline=(255, 255, 255, 230)); g.rectangle([16, 50, 74, 120], fill=(170, 210, 250, 150))
    ep.add(e1, 999, "front", lambda img, t, cam: comp(img, glass, 380, 1270) if t < ep.TBE else None)
    dush.expr(e1 + 0.1, "smug"); ep.shot(e1 + 0.1, "dush", z=1.25)
    w0, w1 = say("dush", "d2", "Что? Вода из-под крана. *Зато бесплатно*", at=e1 + 0.5, a=dush)
    tbe = w1 + 0.6
    ep.pill(e1 + 0.1, w1 + 0.5, "Душная: вода из-под крана", 540, 560, size=50, **STY["dark"]); ep.sfx(e1 + 0.1, "pop", 0.45)
    # 6 · финал
    h0, h1 = say("kubysh", "w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=tbe + 0.05, v=V3)
    end = h1 + 1.4
    ep.TBE = tbe; ep.clip(tb, tbe, BAR, "бар")
    for a in (kub, dush): a.show(h0 - 0.05, False)
    ep.clip(h0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - h0)))
    ep.pill(h0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, 1420, size=46, **STY["green"]); ep.sfx(h0 + 1.0, "pop", 0.4)
    ep.dur = end; ep.cover_t = 1.2
    return ep

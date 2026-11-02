"""К1б · пн 09.11 18:00 (запас) · «4 дня, а на карте 312» (сценарий 82 v3). Жабы на риге, календарь перерасхода и отмотка."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
import frog
from episodes.scr import STY
from episodes.w07_common import setup, sayer, finale

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W09/"
DAYS = list(range(8, 17))


def strip(t, mode, t0):
    """Дни 8–16: mode='red' — каждый день +600 (красные по очереди), 'green' — утренний бюджет и темп в норме."""
    im = Image.new("RGBA", (1000, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, day in enumerate(DAYS):
        x = 10 + i * 108; on = t >= t0 + 0.25 * i
        col = ((170, 48, 60) if mode == "red" else (30, 130, 88)) if on else (36, 44, 42)
        d.rounded_rectangle([x, 0, x + 98, 98], 16, fill=col + (240,))
        d.text((x + 49, 49), str(day), font=PH.font("Bold", 44), fill=(255, 255, 255), anchor="mm")
        if on: d.text((x + 49, 130), "+600" if mode == "red" else "ок", font=PH.font("Bold", 32), fill=PH.RED if mode == "red" else PH.GREEN, anchor="mm", stroke_width=3, stroke_fill=(20, 24, 22))
    return im


def build():
    ep = Ep("W09_K1b_4_дня_312", "room"); ep.sfxgain = 0.5; setup(ep)
    say = sayer(ep, V)
    kub = ep.actor("kub", "kubysh", 800, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)
    kub.expr(0, "shock"); kub.react(0.3, "shudder")
    a0, a1 = say("hero", "h1", "До зарплаты 4 дня. На карте 312 рублей. *Как, бл**ь?*", at=0.2)
    ep.pill(0.1, a1 + 0.2, "На карте 312 ₽", 540, 400, size=80, **STY["red"])
    ep.pill(a0 + 1.2, a1 + 0.2, "до зарплаты 4 дня", 540, 560, size=54, **STY["dark"]); ep.sfx(0.1, "boom", 0.5)
    dush.show(a1 - 0.3); dush.go(a1 - 0.3, 270, hop=60, step=300); dush.expr(a1 - 0.3, "smug")
    b0, b1 = say("dush", "d1", "Зато сколько впечатлений. *Ими и поужинаешь*", at=a1 + 0.2, a=dush)
    ep.shot(b0, ("dush", "kub"), dur=0.4)
    # Кубыш отматывает к 8-му: перерасход по 600
    c0, c1 = say("kubysh", "r1", "Смотри, это началось 8-го. Каждый день плюс 600, по чуть-чуть. *Утром 8-го это уже было видно*", at=b1 + 0.3, a=kub)
    kub.expr(c0, "teacher"); ep.shot(c0, "wide"); ep.set(c0, "night_lamp", fade=0.2); ep.sfx(c0, "whoosh", 0.5)
    ep.pill(c0, c0 + 1.6, "отмотаем к 8-му", 540, 330, size=54, **STY["yellow"])
    ep.add(c0 + 0.3, c1 + 0.2, "screen", lambda img, t, cam: comp(img, strip(t, "red", c0 + 0.6), 40, 520))
    for i in range(9): ep.sfx(c0 + 0.6 + 0.25 * i, "tick", 0.35)
    ep.pill(c0 + (c1 - c0) * 0.72, c1 + 0.2, "утро 8-го: оптимально 1 900 · темп −600", 540, 820, size=44, **STY["red"])
    # поворот: та же неделя, но утром видно
    tp = c1 + 0.3; ep.set(tp, "room", fade=0.2); ep.sfx(tp, "swish", 0.5)
    ep.pill(tp, tp + 3.2, "та же неделя, но видно заранее", 540, 330, size=50, **STY["green"])
    ep.add(tp, tp + 3.4, "screen", lambda img, t, cam: comp(img, strip(t, "green", tp + 0.2), 40, 520))
    ep.add(tp + 2.6, tp + 6.0, "screen", lambda img, t, cam: comp(img, fade(PH.chip("К зарплате на карте 2 000 ₽", PH.GREEN, 62), eout(seg(t, tp + 2.6, tp + 3.0))), 540 - PH.chip("К зарплате на карте 2 000 ₽", PH.GREEN, 62).width / 2, 760))
    for i in range(9): ep.sfx(tp + 0.2 + 0.25 * i, "pop", 0.3)
    ep.sfx(tp + 2.6, "kaching", 0.5); kub.expr(tp, "happy"); dush.expr(tp + 2.6, "shock")
    d0, d1 = say("kubysh", "r2", "Ничего не урезал. *Просто увидел заранее*", at=tp + 3.3, a=kub)
    ep.ov = [o if o[1] != tp + 6.0 else (o[0], d1 + 0.4, o[2], o[3]) for o in ep.ov]
    finale(ep, say, d1 + 0.6, (kub, dush))
    ep.cover_t = 0.8
    return ep

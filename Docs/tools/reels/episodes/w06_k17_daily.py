"""К17 · пт 06.11 12:00 · «Сумма на день» (сценарий 82 v3). Инфографика в темном стиле, голос Holden."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
from episodes.scr import STY, RK
from episodes.lib import PHONE

V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W06/"
V3 = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
Y = 1360


def eq(cv, y, parts, k=1.0, size=96):
    """Строка-уравнение из кусков (текст, цвет), по центру."""
    ims = [PH.text_img(s, size, c) for s, c in parts]; w = sum(i.width for i in ims) + 24 * (len(ims) - 1); x = (PH.W - w) / 2
    for im in ims: PH.put(cv, im, x + im.width / 2, y, a=k); x += im.width + 24


def build():
    ep = Ep("W06_K17_Сумма_на_день", "studio"); ep.sfxgain = 0.4
    ep.avatars = {"kubysh": Image.open(RK + "Референсы/avatar_kubysh.png").convert("RGBA")}
    say = lambda f, cap, at=None, v=V: ep.say("kubysh", "", cap=cap, at=at, y=Y, size=56, file=v + f + "_t_48k.wav")
    a0, a1 = say("m1", "24 тысячи на 10 дней. Сколько в день? *Только не 2 400*", at=0.15)
    b0, b1 = say("m2", "Сначала платежи до зарплаты. Осталось 18, значит *1 800 в день*", at=a1 + 0.3)
    c0, c1 = say("m3", "Вчера ушло больше? Сумма просто *пересчиталась на оставшиеся дни*", at=b1 + 0.3)
    f0, f1 = say("w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=c1 + 0.9, v=V3)
    end = f1 + 1.4

    def fn(img, t, cam):
        cv = PH.background(t).convert("RGBA"); d = ImageDraw.Draw(cv)
        if t < a1 + 0.3:
            k = eout(seg(t, 0, 0.4)); eq(cv, 560, [("24 000", PH.WHITE), ("÷", PH.SUB), ("10", PH.WHITE)], k, 110)
            if t > a0 + (a1 - a0) * 0.45: eq(cv, 760, [("=", PH.SUB), ("?", PH.AMBER)], 1, 130)
            if t > a0 + (a1 - a0) * 0.7:
                eq(cv, 960, [("2 400", PH.RED)], 1, 130); s = seg(t, a0 + (a1 - a0) * 0.8, a0 + (a1 - a0) * 0.95)
                d.line([(370, 960), (370 + 340 * s, 960)], fill=PH.RED, width=12)
        elif t < b1 + 0.3:
            p = (t - b0) / max(0.1, b1 - b0)
            eq(cv, 420, [("24 000", PH.WHITE), ("−", PH.SUB), ("6 000", PH.BLUE)], 1, 96)
            if p > 0.05: PH.put(cv, PH.chip("платежи до зарплаты", PH.BLUE, 44), PH.W / 2, 540)
            if p > 0.4: eq(cv, 720, [("18 000", PH.WHITE), ("÷", PH.SUB), ("10", PH.WHITE)], 1, 96)
            if p > 0.65:
                k = eout(seg(t, b0 + (b1 - b0) * 0.65, b0 + (b1 - b0) * 0.65 + 0.4)); eq(cv, 920, [("1 800 ₽", PH.GREEN)], k, 170)
                PH.put(cv, PH.text_img("в день", 48, PH.SUB, "SemiBold"), PH.W / 2, 1060, a=k)
        elif t < f0 - 0.05:
            p = (t - c0) / max(0.1, c1 - c0)
            PH.put(cv, PH.chip("вчера ушло 3 000", PH.RED, 50), PH.W / 2, 400)
            if p > 0.3: eq(cv, 600, [("15 000", PH.WHITE), ("÷", PH.SUB), ("9", PH.WHITE)], 1, 96)
            if p > 0.55:
                k = eout(seg(t, c0 + (c1 - c0) * 0.55, c0 + (c1 - c0) * 0.55 + 0.4)); v = lerp(1800, 1670, eio(seg(t, c0 + (c1 - c0) * 0.55, c0 + (c1 - c0) * 0.9)))
                eq(cv, 820, [(f"≈ {int(round(v / 10) * 10):,} ₽".replace(",", " "), PH.GREEN)], k, 160)
                PH.put(cv, PH.chip("пересчитано само", PH.GREEN, 48, check=True), PH.W / 2, 1000, a=k)
        img.paste(cv.convert(img.mode), (0, 0))
    ep.add(0, f0 - 0.05, "screen", fn)
    ep.sfx(0.1, "boom", 0.35); ep.sfx(a0 + (a1 - a0) * 0.8, "marker", 0.5)
    ep.sfx(b0 + (b1 - b0) * 0.65, "kaching", 0.4); ep.sfx(c0 + (c1 - c0) * 0.55, "pop", 0.45)
    ep.clip(f0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - f0)))
    ep.pill(f0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, 1190, size=46, **STY["green"]); ep.sfx(f0 + 1.0, "pop", 0.4)
    ep.dur = end; ep.cover_t = 1.0
    return ep

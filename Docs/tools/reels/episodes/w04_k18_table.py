"""К18 · ср 04.11 12:00 · «Эксель, заметки, голова» (сценарий 82, v3). Инфографика в темном стиле, голос Holden."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import promo_hero as PH
from episodes.scr import STY, RK
from episodes.lib import PHONE

V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W04/"
V3 = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
Y = 1360
COLS = ["Эксель", "Заметки", "Голова", "Кубыш"]
ROWS = ["Пересчитает день после пиццы", "Скажет, хватит ли до зарплаты", "Траты вносятся сами"]


def mark(d, x, y, ok, k=1.0):
    if ok: d.line([(x - 22, y), (x - 6, y + 18), (x + 26, y - 20)], fill=PH.GREEN, width=9)
    else:
        d.line([(x - 18, y - 18), (x + 18, y + 18)], fill=PH.RED, width=9); d.line([(x - 18, y + 18), (x + 18, y - 18)], fill=PH.RED, width=9)


def tile(name, sub, col):
    cv, pad = PH.card(300, 300, 36); d = ImageDraw.Draw(cv)
    d.text((pad + 150, pad + 120), name, font=PH.font("Bold", 46), fill=PH.WHITE, anchor="mm")
    d.text((pad + 150, pad + 200), sub, font=PH.font("SemiBold", 34), fill=col, anchor="mm")
    return cv


def build():
    ep = Ep("W04_K18_Эксель_заметки_голова", "studio"); ep.sfxgain = 0.4
    ep.avatars = {"kubysh": Image.open(RK + "Референсы/avatar_kubysh.png").convert("RGBA")}
    say = lambda f, cap, at=None, v=V: ep.say("kubysh", "", cap=cap, at=at, y=Y, size=54, file=v + f + "_t_48k.wav")
    h0, h1 = say("k18a", "Эксель, заметки, голова. Кто из них скажет, *хватит ли до 20-го?*", at=0.15)
    r0, r1 = say("k18b", "Таблица не пересчитает день после вчерашней пиццы. Заметки не скажут, хватит ли до зарплаты. *Траты в обоих руками*", at=h1 + 0.3)
    k0, k1 = say("k18c", "Тут траты подтягиваются из банка, а *сумма на день считается сама*", at=r1 + 0.3)
    f0, f1 = say("w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=k1 + 0.45, v=V3)
    end = f1 + 1.4
    tiles = [tile("Эксель", "#ЗНАЧ!", PH.RED), tile("Заметки", "−3 400 ?", PH.AMBER), tile("Голова", "…или 10 дней?", PH.SUB)]
    rt = [r0 + (r1 - r0) * k for k in (0.05, 0.42, 0.75)]

    def fn(img, t, cam):
        cv = PH.background(t).convert("RGBA")
        if t < h1 + 0.25:
            for i, im in enumerate(tiles):
                k = PH.eout(PH.span(t, 0.1 + 0.45 * i, 0.55 + 0.45 * i))
                if k > 0: PH.put(cv, im, 190 + 350 * i, 640, a=k, scale=PH.lerp(1.3, 1, k))
            PH.title(cv, t, h0 + (h1 - h0) * 0.45, h1 + 0.25, ["Кто скажет,", "*хватит ли до 20-го?*"], y=330)
        else:
            card, pad = PH.card(980, 860, 40); d = ImageDraw.Draw(card); x0, y0 = pad + 30, pad + 40
            cx = [x0 + 230 + 225 * i for i in range(4)]; cx = [x0 + 120 + 240 * i for i in range(4)]
            for i, c in enumerate(COLS):
                hl = i == 3 and t >= k0 + 0.3
                if hl: d.rounded_rectangle([cx[i] - 110, y0 - 20, cx[i] + 110, y0 + 780], 30, fill=(30, 70, 52))
                d.text((cx[i], y0 + 20), c, font=PH.font("Bold", 40), fill=PH.GREEN if i == 3 else PH.WHITE, anchor="mm")
            for j, row in enumerate(ROWS):
                if t < rt[j]: continue
                yy = y0 + 120 + j * 230
                d.text((x0 + 10, yy), row, font=PH.font("SemiBold", 40), fill=PH.WHITE)
                for i in range(3): mark(d, cx[i], yy + 120, False)
                if t >= k0 + 0.3 + 0.35 * j: mark(d, cx[3], yy + 120, True)
            PH.put(cv, card, PH.W / 2, 730, a=PH.eout(PH.span(t, h1 + 0.25, h1 + 0.6)))
        img.paste(cv.convert(img.mode), (0, 0))
    ep.add(0, f0 - 0.05, "screen", fn)
    for i in range(3): ep.sfx(0.1 + 0.45 * i, "pop", 0.4)
    for x in rt: ep.sfx(x, "marker", 0.45)
    for j in range(3): ep.sfx(k0 + 0.3 + 0.35 * j, "tick", 0.5)
    ep.clip(f0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - f0)))
    ep.pill(f0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, 1190, size=46, **STY["green"]); ep.sfx(f0 + 1.0, "pop", 0.4)
    ep.dur = end; ep.cover_t = 1.4
    return ep

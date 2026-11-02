"""Батракан Жабович · ремейк «Никиты Сплитовича» (сценарий 83 v2). Кадры Higgsfield как катсцена старой 3D-игры,
голос Knox ×0,92, пиксельные моноширинные подписи, петля «Пятнадцатого мая». Экраны Кубыша — настоящие скриншоты."""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from studio import *  # noqa
import promo_hero as PH

A = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /"
K = A + "Рилсы маскот/W04_Батракан/кадры/"
V = A + "Голоса/W04/"
SHOT = A + "Промо/Герой/кадры/получка_26окт.png"
LINES = [("01", "Пятнадцатого мая"), ("02", "Это Батракан Жабович"), ("03", "Колупает циферки в конторке"),
         ("04", "Получает 180 000. Двумя частями"), ("05", "Раньше аванс жил три дня"), ("05", "Зарплата жила неделю"),
         ("07", "Кроссовки четырьмя платежами"), ("08", "Подушка безопасности была. Диванная"),
         ("09", "Каждый месяц до зарплаты интервальное голодание"), ("10", "По вечерам считал, сколько тратить завтра"),
         ("11", "Таблица говорила: 2 400"), ("12", "Пацаны говорили: бар"), ("13", "До зарплаты, бл**ь, девять дней"),
         ("P1", "Теперь за Батракана считает Кубыш"), ("P2", "Утром пишет, сколько сегодня оптимально"),
         ("16", "Батракан ходит в бары"), ("17", "И не забывает о покупках"), ("18", "Подушка теперь не диванная"),
         ("19", "Коллеги спрашивают, когда он в отпуск"), ("P3", "Батракан открывает план")]
MONO = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22, index=1)
_IMG, _SUB = {}, {}


def img(k):
    if k not in _IMG:
        im = Image.open(K + k + ".png").convert("RGB"); s = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
        _IMG[k] = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    return _IMG[k]


def pixel_sub(text):
    """Пиксельная подпись: моноширинный текст мелко, увеличенный без сглаживания, белый с темной обводкой."""
    if text in _SUB: return _SUB[text]
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur + " " + w) > 22 and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    lw = max(int(MONO.getlength(l)) for l in lines) + 8; lh = 28
    im = Image.new("RGBA", (lw, lh * len(lines) + 6), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        d.text((lw // 2, 3 + i * lh), l, font=MONO, fill=(255, 255, 255, 255), anchor="ma", stroke_width=2, stroke_fill=(20, 20, 20, 255))
    im = im.resize((im.width * 3, im.height * 3), Image.NEAREST); _SUB[text] = im
    return im


def pill(text, bg, fg=(255, 255, 255), size=48):
    f = PH.font("Bold", size); w = int(f.getlength(text)) + 64; h = int(size * 1.8)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=bg + (245,)); d.text((w // 2, h // 2), text, font=f, fill=fg, anchor="mm")
    return im


def phone_frame(screen, w=640):
    s = screen.convert("RGB"); h = int(s.height * w / s.width); s = s.resize((w, h), Image.LANCZOS)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 70, fill=255)
    out = Image.new("RGBA", (w + 36, h + 36), (0, 0, 0, 0)); ImageDraw.Draw(out).rounded_rectangle([0, 0, w + 35, h + 35], 86, fill=(18, 18, 20, 255))
    out.paste(s, (18, 18), m); return out


def plan_screen():
    cv = Image.new("RGB", (1170, 2532), (14, 18, 17)); d = ImageDraw.Draw(cv)
    d.text((80, 220), "Цели", font=PH.font("Bold", 96), fill=PH.WHITE)
    d.rounded_rectangle([60, 400, 1110, 1000], 60, fill=(26, 34, 32))
    d.text((120, 470), "Отпуск", font=PH.font("Bold", 84), fill=PH.WHITE)
    d.rounded_rectangle([120, 590, 430, 660], 34, fill=(30, 90, 62)); d.text((275, 625), "в плане", font=PH.font("SemiBold", 44), fill=PH.GREEN, anchor="mm")
    d.rounded_rectangle([120, 720, 1050, 750], 15, fill=(44, 54, 50)); d.rounded_rectangle([120, 720, 760, 750], 15, fill=PH.GREEN)
    d.text((120, 800), "Поедешь", font=PH.font("Medium", 48), fill=PH.SUB); d.text((120, 860), "15 мая", font=PH.font("Bold", 96), fill=PH.GREEN)
    return cv


def build():
    ep = Ep("W04_Батракан_Жабович", "studio"); ep.sfxgain = 0.3; ep.progress = False
    t = 0.0; segs = []
    for i, (k, cap) in enumerate(LINES):
        a0, a1 = ep.say("hero", "", cap=cap, at=t, file=V + f"b{i + 1:02d}_t_48k.wav")
        e = a1 + (0.25 if i < len(LINES) - 1 else 0.6); segs.append((t, e, k, cap)); t = e
    ep.caps = []   # подписи рисуем сами, пиксельные
    ep.dur = t; ep.cover_t = 1.5
    shot = Image.open(SHOT); ph1 = phone_frame(shot); ph3 = phone_frame(plan_screen())
    ins = shot.crop((0, 560, shot.width, 1040))

    def fn(im, tt, cam):
        for s0, s1, k, cap in segs:
            if s0 <= tt < s1: break
        p = (tt - s0) / max(0.1, s1 - s0)
        if k.startswith("P"):
            bg = img("03" if k != "P3" else "19").filter(ImageFilter.GaussianBlur(10))
            cv = bg.copy().convert("RGBA"); cv.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
            if k == "P2":
                z = ins.resize((1000, int(ins.height * 1000 / ins.width)), Image.LANCZOS)
                card = Image.new("RGBA", (z.width + 20, z.height + 20), (18, 18, 20, 255)); card.paste(z, (10, 10))
                sc = 1 + 0.04 * p; c2 = card.resize((int(card.width * sc), int(card.height * sc)), Image.LANCZOS)
                cv.alpha_composite(c2, ((W - c2.width) // 2, 640))
            else:
                f = ph1 if k == "P1" else ph3; sc = 0.98 + 0.05 * p
                f2 = f.resize((int(f.width * sc), int(f.height * sc)), Image.LANCZOS)
                cv.alpha_composite(f2, ((W - f2.width) // 2, 230 - int(40 * p)))
        else:
            z = 1.0 + 0.07 * p; src = img(k); w, h = W / z, H / z
            jx = 3 * math.sin(tt * 1.7); jy = 2 * math.cos(tt * 1.3)
            cv = src.crop((int((W - w) / 2 + jx), int((H - h) / 2 + jy), int((W + w) / 2 + jx), int((H + h) / 2 + jy))).resize((W, H), Image.BILINEAR).convert("RGBA")
            d = ImageDraw.Draw(cv)
            if k == "04":   # пуш зарплаты поверх баннера
                n = PH.text_img("+90 000 ₽", 56, (20, 120, 70)); cv.alpha_composite(n, (590 - n.width // 2, 640))
            if k == "05":
                n = pill("аванс: 5-е → 8-е" if "аванс" in cap else "зарплата: 20-е → 27-е", (190, 40, 50), size=56); cv.alpha_composite(n, ((W - n.width) // 2, 1050))
            if k == "11":
                n = PH.text_img("2 400", 120, (20, 20, 120)); cv.alpha_composite(n, ((W - n.width) // 2, 760))
            if k == "12":
                n = pill("Пацаны: бар в 20:00?", (60, 110, 230), size=44); cv.alpha_composite(n, ((W - n.width) // 2, 900))
            if k == "17":
                n = pill("Плановая покупка: подарок маме", (30, 130, 88), size=40); cv.alpha_composite(n, ((W - n.width) // 2, 260))
        sub = pixel_sub(cap); cv.alpha_composite(sub, ((W - sub.width) // 2, 1380))
        im.paste(cv.convert(im.mode), (0, 0))
    ep.add(0, ep.dur, "screen", fn)
    return ep

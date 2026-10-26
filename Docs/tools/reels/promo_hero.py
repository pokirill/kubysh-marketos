"""Промо-ролик «Копить без тревоги» для карточки стора, Reels и Shorts (9:16, тёмная тема как в приложении).
Жанр референса конкурента: кинетическая типографика — пуш зарплаты, огромная цифра тает, строки плана въезжают по одной,
делим на дни, пересчёт после траты, телефон с настоящим экраном «Получки». Без голоса, смысл — текстом.
Запуск: python3 promo_hero.py [--preview 1,3,6] → «Кубыш доки и артефакты /Промо/Герой/»."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import audio

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = "/Users/kirillpopov/Documents/FinAssist - ios /FinAssist/FinAssist/Fonts/"
A = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /"
OUT = A + "Промо/Герой/"
SHOT = A + "Промо/Герой/кадры/получка_26окт.png"   # реальная «Получка» Кирилла 22.10: «Сегодня оптимально ещё 989», темп +1,8к
MASCOT = A + "Рилсы Ксюша/Референсы/cut_kubysh.png"
ICON = "/Users/kirillpopov/Documents/FinAssist - ios /FinAssist/FinAssist/Assets.xcassets/AppIcon.appiconset/"

BG0, BG1 = (9, 14, 12), (3, 6, 5)
CARD, LINE = (22, 29, 27), (255, 255, 255, 22)
WHITE, SUB, MUTED = (244, 247, 245), (150, 164, 157), (96, 108, 102)
GREEN, GREEN2 = (62, 207, 134), (30, 130, 88)
BLUE, AMBER, RED = (110, 160, 255), (255, 190, 90), (255, 116, 116)

# сценарий v2: числа сходятся (150 − 61 − 20 − 15 = 54; 54 000 / 15 = 3 600; 3 600 − 350 − 2 150 = 1 100)
INCOMES = {   # доход → обязательное, подушка, отпуск, траты сегодня; остаток делится на 15 дней без остатка
    150: dict(income=150000, mand=61000, cushion=20000, trip=15000, spends=[("Кофе", 350), ("Продукты", 2150)]),
    180: dict(income=180000, mand=70000, cushion=25000, trip=17500, spends=[("Кофе", 350), ("Продукты", 2650)]),
    230: dict(income=230000, mand=85000, cushion=35000, trip=20000, spends=[("Кофе", 450), ("Продукты", 3350)]),
}
HOOKS = {   # первая строка — кинокадр ночи, вторая — после пушей трат
    "A": (["До зарплаты 9 дней,", "*а денег уже нет*"], ["И накопления *опять*", "ушли на повседневку"]),
    "B": (["Зарабатываешь больше,", "*а накопить на мечту*", "*не получается*"], ["Каждая прибавка", "*растворяется* в тратах"]),
    "C": (["Все говорят: нужна подушка.", "*А у тебя не получается*", "*скопить*"], ["И накопления *опять*", "ушли на повседневку"]),
}
HOOK = os.environ.get("HOOK", "A"); S = dict(INCOMES[int(os.environ.get("INC", "150"))], days=15)
S["life"] = S["income"] - S["mand"] - S["cushion"] - S["trip"]; S["daily"] = S["life"] // S["days"]
S["left"] = S["daily"] - sum(a for _, a in S["spends"]); S["tomorrow"] = round((S["daily"] + S["left"] / 14) / 10) * 10
TS = float(os.environ.get("TS", "1.3"))   # замедление: зритель успевает прочитать и погрузиться в проблему
C1, C2, C3 = 0.0, 3.4, 16.4          # кинокадры Higgsfield: тревога, поворот (Кубыш щелкает), облегчение
D0 = 2.0                             # «накопления опять ушли» — кинетика между кадрами
T0, T1, T2, T3, T4, END = 5.0, 7.0, 10.4, 12.6, 18.4, 21.8   # план → конверты → в день → пересчет → облегчение → финал
CL = A + "Промо/Герой/клипы/"


# ---------- помощники ----------
_F = {}
def font(w, s):
    """SF Pro (системный шрифт Apple, вариативный SFNS) — как в iOS."""
    k = (w, int(s))
    if k not in _F:
        f = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", int(s))
        f.set_variation_by_name({"SemiBold": "Semibold"}.get(w, w)); _F[k] = f
    return _F[k]

clamp = lambda x: max(0.0, min(1.0, x))
span = lambda t, a, b: clamp((t - a) / (b - a))
eout = lambda x: 1 - (1 - clamp(x)) ** 3
eio = lambda x: (lambda k: 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2)(clamp(x))
def eback(x, s=1.6):
    x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
rub = lambda v: f"{int(round(v)):,}".replace(",", " ")
lerp = lambda a, b, k: a + (b - a) * k


def text_img(s, size, color=WHITE, w="Bold"):
    f = font(w, size); bb = f.getbbox(s)
    im = Image.new("RGBA", (bb[2] - bb[0] + 4, int(size * 1.3)), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((-bb[0] + 2, int(size * 0.12)), s, font=f, fill=color)
    return im


def put(cv, im, x, y, a=1.0, scale=1.0, anchor="mm"):
    if a <= 0.01: return
    if abs(scale - 1) > 0.005: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if a < 0.999:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    ox = {"l": 0, "m": im.width / 2, "r": im.width}[anchor[0]]; oy = {"t": 0, "m": im.height / 2, "b": im.height}[anchor[1]]
    cv.alpha_composite(im, (int(x - ox), int(y - oy))) if 0 <= x - ox and x - ox + im.width <= W and 0 <= y - oy and y - oy + im.height <= H else _clip(cv, im, int(x - ox), int(y - oy))


def _clip(cv, im, x, y):
    l, t = max(0, -x), max(0, -y); r, b = min(im.width, W - x), min(im.height, H - y)
    if r > l and b > t: cv.alpha_composite(im, (x + l, y + t), (l, t, r, b))


def card(w, h, r=40, fill=CARD, glow=None):
    pad = 60
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle([pad, pad, pad + w, pad + h], r, fill=glow + (70,))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(34)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad, pad, pad + w, pad + h], r, fill=fill + (245,), outline=LINE, width=2)
    return im, pad


def chip(s, color=GREEN, size=40, check=False):
    t = text_img(s, size, color, "SemiBold"); ic = int(size * 1.05) if check else 0
    im = Image.new("RGBA", (t.width + 56 + (ic + 16 if check else 0), int(size * 1.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], im.height // 2, fill=color + (38,), outline=color + (120,), width=2)
    if check:   # галочка в кружке: в Montserrat нет глифа ✓
        cx, cy = 28 + ic / 2, im.height / 2; d.ellipse([cx - ic / 2, cy - ic / 2, cx + ic / 2, cy + ic / 2], fill=color)
        d.line([(cx - ic * 0.24, cy), (cx - ic * 0.06, cy + ic * 0.2), (cx + ic * 0.26, cy - ic * 0.2)], fill=(6, 30, 18), width=max(3, ic // 9), joint="curve")
    im.alpha_composite(t, (28 + (ic + 16 if check else 0), (im.height - t.height) // 2)); return im


_BG = None
def background(t):
    global _BG
    if _BG is None:
        _BG = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(_BG)
        for y in range(0, H, 4): d.rectangle([0, y, W, y + 4], fill=tuple(int(lerp(a, b, y / H)) for a, b in zip(BG0, BG1)) + (255,))
    cv = _BG.copy()
    glow = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for cx, cy, r, col, ph in ((0.2, 0.18, 0.55, GREEN2, 0.0), (0.85, 0.75, 0.5, (40, 70, 120), 1.7)):
        x = (cx + 0.04 * math.sin(t * 0.5 + ph)) * W / 4; y = (cy + 0.03 * math.cos(t * 0.4 + ph)) * H / 4; rr = r * W / 4
        g.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col + (60,))
    cv.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)).resize((W, H), Image.BILINEAR))
    return cv


def rich(s, size, accent=GREEN):
    """Строка с акцентами *так*: части склеиваются в одну картинку."""
    parts = s.split("*"); ims = [text_img(p, size, accent if i % 2 else WHITE) for i, p in enumerate(parts) if p]
    im = Image.new("RGBA", (sum(x.width for x in ims) - 4 * (len(ims) - 1), max(x.height for x in ims)), (0, 0, 0, 0)); x = 0
    for p in ims: im.alpha_composite(p, (x, 0)); x += p.width - 4
    return im


def title(cv, t, t0, t1, lines, y=250, accent=GREEN, size=74):
    """Заголовок: строки въезжают снизу с затуханием, уходят вверх. *слово* — акцентом."""
    k_out = span(t, t1 - 0.3, t1)
    for i, s in enumerate(lines):
        im = rich(s, size, accent)
        ki = eout(span(t, t0 + 0.08 * i, t0 + 0.08 * i + 0.45))
        put(cv, im, W / 2, y + i * int(size * 1.25) + 40 * (1 - ki) - 40 * k_out, a=ki * (1 - k_out))


def big_number(cv, v, y, a=1.0, scale=1.0, color=WHITE, size=200, suffix=" ₽"):
    put(cv, text_img(rub(v) + suffix, size, color), W / 2, y, a=a, scale=scale)


# ---------- сцены ----------
_CL = {}
def clip_frame(name, t, speed=1.0):
    """Кадр клипа Higgsfield (vframes → кэш), заполняет весь кадр 9:16."""
    if not os.path.exists(CL + name):   # клипа еще нет — стартовый кадр с медленным наездом
        im = Image.open(A + "Промо/Герой/кадры/" + name.replace(".mp4", ".png")).convert("RGBA").resize((W, H), Image.LANCZOS)
        z = 1 + 0.06 * t / 2.0; w2, h2 = int(W * z), int(H * z)
        return im.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
    if name not in _CL:
        import hashlib
        path = CL + name; d = os.path.join(HERE, ".cache", "clips", hashlib.md5((path + f"{W}x{H}").encode()).hexdigest()[:10])
        if not os.path.isdir(d) or not os.listdir(d):
            os.makedirs(d, exist_ok=True)
            subprocess.run([os.path.join(HERE, "vframes"), path, d, str(FPS), str(W), str(H)], check=True, capture_output=True)
        _CL[name] = sorted(os.path.join(d, f) for f in os.listdir(d))
    fr = _CL[name]; return Image.open(fr[min(len(fr) - 1, max(0, int(t * speed * FPS)))]).convert("RGBA")


def shade(cv, top=0.0, bottom=0.75):
    """Затемнение снизу под текст поверх кинокадра."""
    g = Image.new("L", (1, H))
    for y in range(H): g.putpixel((0, y), int(255 * (top + (bottom - top) * clamp((y / H - 0.35) / 0.65)) ** 1))
    cv.alpha_composite(Image.merge("RGBA", (Image.new("L", (W, H), 0),) * 3 + (g.resize((W, H)),)))


def push(cv, t, t0, t1, amount, label, color=GREEN, y=210, sign="+", sub="БАНК · сейчас"):
    k = eback(span(t, t0, t0 + 0.45)); out = eout(span(t, t1 - 0.3, t1))
    if k <= 0 or out >= 1: return
    im, pad = card(940, 170, 44, (34, 40, 38))
    d = ImageDraw.Draw(im); x0, y0 = pad + 30, pad + 30
    d.rounded_rectangle([x0, y0, x0 + 110, y0 + 110], 26, fill=(52, 120, 246))
    d.text((x0 + 55, y0 + 55), "₽", font=font("Bold", 64), fill=WHITE, anchor="mm")
    d.text((x0 + 140, y0 + 6), sub, font=font("SemiBold", 30), fill=SUB)
    d.text((x0 + 140, y0 + 46), label, font=font("SemiBold", 38), fill=WHITE)
    d.text((x0 + 140, y0 + 96), sign + rub(amount) + " ₽", font=font("Bold", 40), fill=color)
    put(cv, im, W / 2, lerp(y - 360, y, k) - 260 * out, a=1 - out)


def scene_night(cv, t):
    cv.alpha_composite(clip_frame("night.mp4", t, 0.8)); shade(cv)
    l = HOOKS[HOOK][0]; title(cv, t, 0.25, D0 + 0.2, l, y=1520 - 50 * len(l), accent=RED, size=74 if len(l) > 2 else 78)


DRAIN = [(0.0, 2400, "Маркетплейс"), (0.25, 1800, "Доставка"), (0.5, 1200, "Такси"), (0.85, 10000, "С накопительного на карту")]
def scene_drain(cv, t):
    for i, (dt, a, lab) in enumerate(DRAIN):
        push(cv, t, D0 + dt, C2, a, lab, RED, y=330 + i * 250, sign="−", sub="БАНК · только что")
    title(cv, t, D0 + 0.9, C2 + 0.1, HOOKS[HOOK][1], y=1430, accent=RED)


def scene_turn(cv, t):
    cv.alpha_composite(clip_frame("turn.mp4", t - C2 + 2.9, 1.0)); shade(cv, 0, 0.65)
    title(cv, t, C2 + 0.5, T0 + 0.1, ["Знакомься: *Кубыш*", "считает деньги за тебя"], y=1480)


def scene_hook(cv, t):
    push(cv, t, T0, T1 + 0.3, S["income"], "Зачисление зарплаты")
    k = span(t, T0 + 0.35, T0 + 1.0)
    sc = lerp(1.35, 1.0, eout(span(t, T0 + 0.35, T0 + 0.7)))          # резкий зум: цифра «падает» в кадр
    big_number(cv, S["income"] * eout(k), 820, a=eout(span(t, T0 + 0.3, T0 + 0.5)), scale=sc)
    put(cv, text_img("Пришла зарплата", 44, SUB, "SemiBold"), W / 2, 660, a=eout(span(t, T0 + 0.4, T0 + 0.7)))
    title(cv, t, T0 + 0.8, T1 + 0.3, ["Кубыш делает план", "*с каждой зарплаты*"], y=1150)


ROWS = [("Обязательное", "аренда · коммуналка · связь", "mand", BLUE, None),
        ("Подушка", "к марту 2027", "cushion", GREEN, 0.62),
        ("Отпуск", "к июлю 2027", "trip", AMBER, 0.35)]


def scene_plan(cv, t):
    title(cv, t, T1, T2, ["Раскладывает", "по *конвертам*"], y=230)
    starts = [T1 + 0.5, T1 + 1.2, T1 + 1.9]
    v = S["income"]
    for (name, sub, key, col, prog), st in zip(ROWS, starts):
        v -= S[key] * eio(span(t, st + 0.1, st + 0.6))
    final = span(t, T1 + 2.6, T1 + 3.0)
    lab = "На жизнь до 25 октября" if final > 0.5 else "Зарплата"
    put(cv, text_img(lab, 44, GREEN if final > 0.5 else SUB, "SemiBold"), W / 2, 520)
    big_number(cv, v, 660, color=GREEN if final > 0.5 else WHITE, scale=1 + 0.06 * math.sin(math.pi * final))
    for i, ((name, sub, key, col, prog), st) in enumerate(zip(ROWS, starts)):
        k = eout(span(t, st, st + 0.45))
        if k <= 0: continue
        im, pad = card(940, 190, 36)
        d = ImageDraw.Draw(im); x0, y0 = pad + 34, pad + 34
        d.rounded_rectangle([x0, y0, x0 + 18, y0 + 122], 9, fill=col)
        d.text((x0 + 46, y0 + 2), name, font=font("Bold", 46), fill=WHITE)
        d.text((x0 + 46, y0 + 66), sub, font=font("Medium", 34), fill=col if prog else SUB)
        d.text((pad + 940 - 34, y0 + 30), "−" + rub(S[key]), font=font("Bold", 50), fill=WHITE, anchor="ra")
        if prog:   # мини-прогресс цели
            bx = pad + 940 - 34 - 300; by = y0 + 104
            d.rounded_rectangle([bx, by, bx + 300, by + 14], 7, fill=(255, 255, 255, 30))
            d.rounded_rectangle([bx, by, bx + 300 * prog * eout(span(t, st + 0.3, st + 1.1)), by + 14], 7, fill=col)
        put(cv, im, W / 2 + 120 * (1 - k), 940 + i * 230, a=k)


def scene_daily(cv, t):
    title(cv, t, T2, T3, ["И делит остаток", "на *каждый день*"], y=260)
    k = eio(span(t, T2 + 0.4, T2 + 1.3))
    put(cv, text_img(f"{rub(S['life'])} ₽ ÷ {S['days']} дней", 60, SUB, "SemiBold"), W / 2, 700, a=1 - 0.6 * k)
    v = lerp(S["life"], S["daily"], eout(span(t, T2 + 0.4, T2 + 1.2)))
    big_number(cv, v, 900, color=GREEN, scale=1 + 0.08 * math.sin(math.pi * span(t, T2 + 1.2, T2 + 1.6)))
    put(cv, text_img("в день", 54, WHITE, "SemiBold"), W / 2, 1060, a=eout(span(t, T2 + 1.1, T2 + 1.5)))
    put(cv, chip("оптимально, чтобы хватило до зарплаты", GREEN, 50), W / 2, 1190, a=eout(span(t, T2 + 1.4, T2 + 1.8)))


def scene_recalc(cv, t):
    title(cv, t, T3, C3, ["Пересчитывает", "после *каждой траты*"], y=250)
    im, pad = card(940, 760, 48, glow=GREEN2)
    d = ImageDraw.Draw(im); x0, y0 = pad + 50, pad + 50
    d.text((x0, y0), "Сегодня", font=font("SemiBold", 44), fill=SUB)
    st = [T3 + 0.7, T3 + 1.4]
    v = S["daily"] - sum(a * eio(span(t, s0 + 0.15, s0 + 0.6)) for (_, a), s0 in zip(S["spends"], st))
    d.text((x0, y0 + 64), rub(v) + " ₽", font=font("Bold", 120), fill=WHITE)
    d.text((x0, y0 + 205), "оптимально потратить ещё", font=font("SemiBold", 46), fill=GREEN)
    for i, ((name, amt), s0) in enumerate(zip(S["spends"], st)):
        k = eout(span(t, s0, s0 + 0.4))
        if k <= 0: continue
        y = y0 + 300 + i * 120
        d.rounded_rectangle([x0, y, x0 + 840, y + 96], 24, fill=(255, 255, 255, int(16 * k)))
        d.text((x0 + 30, y + 48), name, font=font("SemiBold", 42), fill=WHITE + (int(255 * k),), anchor="lm")
        d.text((x0 + 810, y + 48), "−" + rub(amt) + " ₽", font=font("Bold", 42), fill=RED + (int(255 * k),), anchor="rm")
    kt = eout(span(t, T3 + 2.1, T3 + 2.5))   # завтра пересчитано с учетом сегодняшних трат
    if kt > 0:
        y = y0 + 560; d.line([x0, y - 14, x0 + 840, y - 14], fill=(255, 255, 255, 30), width=2)
        d.text((x0, y + 40), "Завтра", font=font("SemiBold", 44), fill=SUB + (int(255 * kt),), anchor="lm")
        d.text((x0 + 840, y + 40), rub(lerp(S["daily"], S["tomorrow"], kt)) + " ₽", font=font("Bold", 56), fill=GREEN + (int(255 * kt),), anchor="rm")
        d.text((x0 + 840, y + 100), "пересчитано с учётом сегодня", font=font("Medium", 30), fill=SUB + (int(255 * kt),), anchor="rm")
    put(cv, im, W / 2, 900, a=eout(span(t, T3 + 0.1, T3 + 0.5)), scale=lerp(0.94, 1.0, eout(span(t, T3 + 0.1, T3 + 0.6))))
    put(cv, chip(f"Темп экономнее плана · запас {rub(S['left'])} ₽", GREEN, 50), W / 2, 1420, a=eout(span(t, T3 + 2.7, T3 + 3.1)), scale=lerp(1.2, 1.0, eout(span(t, T3 + 2.7, T3 + 3.0))))
    put(cv, chip("Хватит до 25-го", GREEN, 52, check=True), W / 2, 1560, a=eout(span(t, T3 + 3.2, T3 + 3.6)), scale=lerp(1.2, 1.0, eout(span(t, T3 + 3.2, T3 + 3.5))))


def scene_relief(cv, t):
    cv.alpha_composite(clip_frame("relief.mp4", t - C3, 1.0)); shade(cv)
    title(cv, t, C3 + 0.2, T4 + 0.1, ["Тратишь *спокойно*.", "Подушка и цели по плану"], y=1470, size=70)


_PH = {}
def phone():
    if "img" not in _PH:
        shot = Image.open(SHOT).convert("RGB"); pw = 540; ph = int(shot.height * pw / shot.width); r = 76; b = 16
        m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, pw - 1, ph - 1], r, fill=255)
        scr = shot.resize((pw, ph), Image.LANCZOS).convert("RGBA"); scr.putalpha(m)
        body = Image.new("RGBA", (pw + 2 * b, ph + 2 * b), (0, 0, 0, 0))
        ImageDraw.Draw(body).rounded_rectangle([0, 0, body.width - 1, body.height - 1], r + b, fill=(40, 44, 46), outline=(90, 96, 98), width=3)
        body.alpha_composite(scr, (b, b)); _PH["img"] = body
        mas = Image.open(MASCOT).convert("RGBA"); _PH["mas"] = mas.resize((420, int(mas.height * 420 / mas.width)), Image.LANCZOS)
        icon = Image.open(ICON + "AppStore-1024.png").convert("RGBA").resize((130, 130), Image.LANCZOS)
        mk = Image.new("L", (130, 130), 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, 129, 129], 30, fill=255); icon.putalpha(mk); _PH["icon"] = icon
    return _PH


def scene_end(cv, t):
    p = phone(); k = eout(span(t, T4, T4 + 0.7))
    put(cv, p["img"], W / 2, lerp(1450, 760, k), scale=lerp(0.9, 0.96, span(t, T4, END)))     # медленный наезд
    put(cv, p["mas"], 880, lerp(1950, 1150, eback(span(t, T4 + 0.5, T4 + 1.0))), scale=0.8)
    title(cv, t, T4 + 0.8, END + 1, ["Комфортно *сегодня*,", "спокойно *завтра*"], y=1380)   # обещание, итог 27.10
    put(cv, text_img("Сумма на день, подушка и цели по плану", 40, SUB, "SemiBold"), W / 2, 1560, a=eout(span(t, T4 + 1.1, T4 + 1.5)))
    kb = eout(span(t, T4 + 1.5, T4 + 1.9))
    put(cv, p["icon"], 235, 1720, a=kb)
    btn = Image.new("RGBA", (560, 120), (0, 0, 0, 0)); ImageDraw.Draw(btn).rounded_rectangle([0, 0, 559, 119], 60, fill=GREEN)
    ImageDraw.Draw(btn).text((280, 60), "Бесплатно в App Store", font=font("Bold", 40), fill=(6, 30, 18), anchor="mm")
    put(cv, btn, 610, 1720, a=kb, scale=lerp(0.9, 1.0, kb))


def frame(t):
    cv = background(t)
    if t < D0: scene_night(cv, t)
    elif t < C2: scene_drain(cv, t)
    elif t < T0: scene_turn(cv, t)
    elif t < T1: scene_hook(cv, t)
    elif t < T2: scene_plan(cv, t)
    elif t < T3: scene_daily(cv, t)
    elif t < C3: scene_recalc(cv, t)
    elif t < T4: scene_relief(cv, t)
    else: scene_end(cv, t)
    ImageDraw.Draw(cv).rounded_rectangle([60, 60, 60 + (W - 120) * t / END, 66], 3, fill=GREEN + (200,))
    return cv


SFX = [(D0 + dt, "msg", 0.45) for dt, *_ in DRAIN] + [
       (C2 + 0.3, "boom", 0.3), (T0, "msg", 0.6), (T0 + 0.35, "whoosh", 0.4), (T1 + 0.5, "pop", 0.5), (T1 + 1.2, "pop", 0.5),
       (T1 + 1.9, "pop", 0.5), (T1 + 2.6, "ding", 0.5), (T2 + 0.4, "whoosh", 0.4), (T2 + 1.2, "kaching", 0.45),
       (T3 + 0.7, "tick", 0.5), (T3 + 1.4, "tick", 0.5), (T3 + 2.1, "pop", 0.5), (T3 + 3.2, "ding", 0.6), (C3, "whoosh", 0.4), (T4, "whoosh", 0.5), (T4 + 1.5, "pop", 0.4)]


def music(total, drop):
    """Трек Higgsfield (sonilo_music): тревожное вступление, дроп на 5,0 с. Дроп ставим на щелчок Кубыша,
    середину (7–13 с) повторяем с кроссфейдом до нужной длины, в конце затухание."""
    src = audio.load(OUT + "music_48k.wav"); SR = audio.SR; c = lambda a, b: list(src[int(a * SR):int(b * SR)])
    x = c(5.0 - drop, 5.0) + c(5.0, 13.0); xf = int(0.25 * SR)
    while len(x) < total * SR:
        nxt = c(7.0, 13.0)
        for i in range(xf): x[-xf + i] = x[-xf + i] * (1 - i / xf) + nxt[i] * (i / xf)
        x += nxt[xf:]
    x = x[:int(total * SR)]; fo = int(1.5 * SR)
    for i in range(fo): x[-fo + i] *= 1 - i / fo
    return x


def main():
    os.makedirs(OUT, exist_ok=True)
    if "--preview" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1].split(",")]
        for t in ts: frame(t).convert("RGB").save(OUT + f"_preview_{t:05.2f}.png")
        return
    silent = OUT + "_video.mp4"
    enc = subprocess.Popen([os.path.join(os.path.dirname(HERE), "store_cards", "mp4enc"), silent, str(W), str(H), str(FPS)], stdin=subprocess.PIPE)
    n = int(END * TS * FPS)
    for i in range(n):
        im = frame(i / FPS / TS); enc.stdin.write(im.tobytes("raw", "BGRA"))
        if i == int((T1 + 2.8) * FPS): im.convert("RGB").save(OUT + "Обложка.png")
    enc.stdin.close(); enc.wait()
    ev = [(t * TS, audio.sfx(nm), g) for t, nm, g in SFX]
    ev.append((0.0, music(END * TS, C2 * TS), 0.75))
    wav = OUT + "_mix.wav"; audio.mix(ev, END * TS, wav)
    name = OUT + f"Промо_герой_{HOOK}_{S['income'] // 1000}к.mp4"; audio.mux(silent, wav, name)
    for f in ("_video.mp4", "_mix.wav", "_mix.m4a"):
        if os.path.exists(OUT + f): os.remove(OUT + f)
    print(name)


if __name__ == "__main__":
    main()

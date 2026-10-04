"""Риг маскота Кубыша для рилсов: вырезка из иконки приложения + рисованные глаза, веки и брови.

Облик берем из AppStore-1024.png (тот же, что в сторе). Выражение задается словарем EXPR
или своими параметрами: look (куда смотрят зрачки), lid (верхнее веко 0..1), tilt (наклон века),
low (нижнее веко), brow (None или (сдвиг по y, угол)), wink, pupil (масштаб зрачка).
Душная жаба: тот же риг, серая перекраска, очки, тяжелые веки.

Пример: python3 frog.py --sheet out.png  (лист выражений для согласования)
"""
import os, sys, math
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageChops

ICON = "/Users/kirillpopov/Documents/FinAssist - ios /FinAssist/FinAssist/Assets.xcassets/AppIcon.appiconset/AppStore-1024.png"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")

# Геометрия глаз в координатах иконки 1024: центр, полуоси
# Глаза увеличены в 1.4 раза против иконки: в рилсе эмоция читается глазами и бровями
EYES = {"L": ((443, 262), (43, 60)), "R": ((524, 280), (38, 62))}
LIDSAMPLE = {"L": (378, 236, 392, 250), "R": (578, 272, 592, 286)}
WHITE = (247, 240, 214); RIM = (160, 146, 96); PUPIL = (22, 28, 24)
BROW = (24, 92, 34); LIDLINE = (28, 104, 36)
SS = 4  # суперсэмплинг для гладких краев

EXPR = {
    "neutral": dict(),
    "smug":    dict(look=(3, 1), lid=0.42, tilt=-8, brow={"L": (-16, -12), "R": (-4, 6)}),
    "wink":    dict(look=(4, 0), lid=0.25, brow={"L": (-18, -10), "R": (-6, 8)}, wink="R"),
    "side":    dict(look=(-11, 2), lid=0.48, tilt=0, brow={"L": (-2, 4), "R": (-2, -4)}),
    "shock":   dict(look=(0, -2), lid=0.0, pupil=0.62, brow={"L": (-30, -6), "R": (-30, 6)}),
    "laugh":   dict(look=(0, 0), lid=0.0, low=0.0, wink="LR", brow={"L": (-24, -8), "R": (-24, 8)}),
    "talk":    dict(look=(2, 0), lid=0.18, brow={"L": (-12, -4), "R": (-12, 4)}),
    # душная: веки тяжелые, брови сведены к переносице, смотрит свысока
    "dush":    dict(look=(-2, 5), lid=0.55, tilt=6, brow={"L": (-6, 14), "R": (-6, -14)}),
    "dush_mad": dict(look=(4, 2), lid=0.35, tilt=10, brow={"L": (-2, 22), "R": (-2, -22)}),
    "eyeroll": dict(look=(6, -17), lid=0.28, brow={"L": (-22, -6), "R": (-10, 4)}),
    "angry":   dict(look=(0, 2), lid=0.32, tilt=8, brow={"L": (2, 20), "R": (2, -20)}),
    "worried": dict(look=(0, 0), lid=0.05, pupil=0.8, brow={"L": (-22, -16), "R": (-22, 16)}),
    "happy":   dict(look=(0, 0), lid=0.0, wink="LR", brow={"L": (-26, -6), "R": (-26, 6)}),
    "sleepy":  dict(look=(0, 6), lid=0.66, brow={"L": (-4, -4), "R": (-4, 4)}),
    "teacher": dict(look=(0, -3), lid=0.4, tilt=4, brow={"L": (-24, -8), "R": (-4, -12)}),
    "skeptic": dict(look=(-4, 0), lid=0.45, tilt=-6, brow={"L": (-24, -12), "R": (0, 8)}),
    "proud":   dict(look=(3, -2), lid=0.38, tilt=-8, brow={"L": (-20, -8), "R": (-20, 8)}),
}


def _cutout():
    """Лягушка с прозрачным фоном (фон иконки черный: альфа из яркости, цвет без темной каймы)."""
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, "frog_cut.png")
    if os.path.exists(p):
        return Image.open(p).convert("RGBA")
    src = Image.open(ICON).convert("RGB")
    r, g, b = src.split()
    mx = ImageChops.lighter(ImageChops.lighter(r, g), b)
    alpha = mx.point(lambda v: 0 if v < 14 else min(255, (v - 14) * 5))
    # темные тени между лапами не фон: все, что не связано с краем картинки, делаем непрозрачным
    ext = mx.point(lambda v: 255 if v >= 14 else 0)
    ImageDraw.floodfill(ext, (0, 0), 128, thresh=0)
    inside = ext.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(5))
    alpha = ImageChops.lighter(alpha, inside)
    # unpremultiply: на черном фоне наблюдаемый цвет = цвет * альфа
    px = src.load(); ap = alpha.load()
    out = Image.new("RGBA", src.size)
    op = out.load()
    for y in range(src.height):
        for x in range(src.width):
            a = ap[x, y]
            if a == 0:
                continue
            c = px[x, y]
            if a < 255:
                k = 255 / a
                c = (min(255, int(c[0] * k)), min(255, int(c[1] * k)), min(255, int(c[2] * k)))
            op[x, y] = (c[0], c[1], c[2], a)
    out.save(p)
    return out


COIN_POS = (150, 314)  # левый верх спрайта монеты в координатах иконки (как на иконке, во рту)
MOUTH = [(247, 318), (275, 322), (310, 330), (350, 343), (390, 362), (424, 384)]  # линия рта от кончика морды к углу
CROP = None  # постоянная рамка кадра лягушки, чтобы выражение не сдвигало картинку


def _coin_mask(size=(1024, 1024)):
    m = Image.new("L", (size[0] * SS, size[1] * SS), 0); d = ImageDraw.Draw(m)
    E = lambda b: [v * SS for v in b]
    d.ellipse(E([154, 318, 402, 426]), fill=255); d.ellipse(E([154, 354, 402, 463]), fill=255)
    d.polygon(E([154, 372, 402, 371, 402, 408, 154, 409]), fill=255)
    return m.resize(size, Image.LANCZOS)


def _parts():
    """(тело без монеты, спрайт монеты). Под монетой дорисованы челюсть, подбородок и линия рта."""
    os.makedirs(CACHE, exist_ok=True)
    pb, pc = os.path.join(CACHE, "body.png"), os.path.join(CACHE, "coin.png")
    if os.path.exists(pb) and os.path.exists(pc):
        return Image.open(pb).convert("RGBA"), Image.open(pc).convert("RGBA")
    full = _cutout(); cm = _coin_mask()
    cmd = cm.filter(ImageFilter.MaxFilter(7))  # с запасом, чтобы не остался ободок монеты
    coin = Image.new("RGBA", full.size, (0, 0, 0, 0)); coin.paste(full, (0, 0), cm.filter(ImageFilter.MaxFilter(3)))
    coin = coin.crop((COIN_POS[0], COIN_POS[1], 406, 468))
    cpx = coin.load()
    for y in range(coin.height):
        for x in range(coin.width):
            r, g, b, a = cpx[x, y]
            if a and (g > r or r + g + b < 160): cpx[x, y] = (r, g, b, 0)
    body = full.copy()
    body.putalpha(ImageChops.subtract(body.getchannel("A"), cmd))
    # силуэт морды за монетой: кончик морды, круглый подбородок, горло
    sil = Image.new("L", (1024 * SS, 1024 * SS), 0)
    ImageDraw.Draw(sil).polygon([(x * SS, y * SS) for x, y in [(246, 290), (241, 306), (240, 322), (246, 338), (255, 362),
                                (263, 392), (268, 424), (268, 456), (266, 492), (444, 492), (444, 290)]], fill=255)
    sil = sil.resize((1024, 1024), Image.LANCZOS)
    # зона дорисовки шире монеты на ~10 px с плавным краем: прячет шов и тень монеты на животе
    soft = cm.filter(ImageFilter.MaxFilter(19)).filter(ImageFilter.GaussianBlur(5))
    region = ImageChops.multiply(ImageChops.lighter(cmd, soft), sil)
    # линия рта как функция x
    def mouth_y(x):
        for (x0, y0), (x1, y1) in zip(MOUTH, MOUTH[1:]):
            if x0 <= x <= x1: return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return MOUTH[0][1] if x < MOUTH[0][0] else MOUTH[-1][1]
    src = full.load(); bp = body.load(); rp = region.load(); cp = cmd.load()
    def first_visible(x, y, step):
        while 0 < y < 1023:
            if cp[x, y] == 0 and src[x, y][3] > 200: return src[x, y][:3]
            y += step
        return None
    def avg(cs):
        cs = [c for c in cs if c]; return tuple(sum(c[i] for c in cs) // len(cs) for i in range(3))
    G = avg([first_visible(x, 320, -1) for x in range(252, 400, 4)])
    B = avg([src[x, y][:3] for x in range(285, 400, 3) for y in range(476, 500) if src[x, y][3] > 200 and src[x, y][0] > 200])
    D = (int(B[0] * 0.84), int(B[1] * 0.74), int(B[2] * 0.62))
    lay = Image.new("RGBA", full.size, (0, 0, 0, 0)); lp = lay.load()
    for x in range(150, 444):
        my = mouth_y(x)
        for y in range(300, 492):
            if rp[x, y] == 0: continue
            if y < my:
                k = max(0, min(1, (y - (my - 22)) / 22)); c = tuple(int(v * (1 - 0.16 * k)) for v in G)
            else:
                k = max(0, min(1, (y - my) / 70)); k = k * k * (3 - 2 * k)
                c = tuple(int(D[i] * (1 - k) + B[i] * k) for i in range(3))
            lp[x, y] = c + (rp[x, y],)
    body.alpha_composite(lay)
    # линия рта и мягкая тень под ней
    L = Image.new("RGBA", (1024 * SS, 1024 * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line([(x * SS, (y + 7) * SS) for x, y in MOUTH], fill=(150, 110, 30, 90), width=12 * SS, joint="curve")
    d.line([(x * SS, y * SS) for x, y in MOUTH], fill=(30, 104, 36, 255), width=6 * SS, joint="curve")
    L = L.resize((1024, 1024), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6))
    g = _grain((1024, 1024)); shade = Image.merge("RGBA", (g, g, g, region.point(lambda v: v * 26 // 255)))
    body.alpha_composite(L); body.alpha_composite(shade)
    body.save(pb); coin.save(pc)
    return body, coin


def coin_sprite(flip=1.0, bite=False, rot=0):
    """Монета: flip — сжатие по вертикали (вращение в полете, 1 = как на иконке), bite — след укуса."""
    c = _parts()[1].copy()
    if bite:
        m = c.getchannel("A"); d = ImageDraw.Draw(m)
        for i, r in enumerate((26, 22, 24)):
            cx = 214 + i * 22; d.ellipse([cx - r, -r + 6, cx + r, r + 6], fill=0)
        c.putalpha(m)
    if flip != 1.0:
        f = max(0.06, abs(flip)); c = c.resize((c.width, max(2, int(c.height * f))), Image.LANCZOS)
        if flip < 0: c = c.transpose(Image.FLIP_TOP_BOTTOM)
    if rot:
        c = c.rotate(rot, resample=Image.BICUBIC, expand=True)
    return c


def _lid_color(img, eye):
    cols = [c for c in img.crop(LIDSAMPLE[eye]).getdata() if c[3] > 200]
    return tuple(sum(c[i] for c in cols) // len(cols) for i in range(3))


def _grain(size, strength=22):
    n = Image.effect_noise(size, 40).convert("L")
    return n.point(lambda v: 128 + (v - 128) * strength // 64)


def _draw_eye(layer, eye, ox, oy, lidc, look=(0, 0), lid=0.15, tilt=0, low=0.0, pupil=1.0, closed=False):
    """Рисует один глаз в слой layer (суперсэмпл), ox/oy — смещение слоя в координатах иконки."""
    (cx, cy), (rx, ry) = EYES[eye]
    s = SS
    X = lambda v: (v - ox) * s
    Y = lambda v: (v - oy) * s
    d = ImageDraw.Draw(layer)
    rim = 3
    d.ellipse([X(cx - rx - rim), Y(cy - ry - rim), X(cx + rx + rim), Y(cy + ry + rim)], fill=RIM + (255,))
    eye_mask = Image.new("L", layer.size, 0)
    ImageDraw.Draw(eye_mask).ellipse([X(cx - rx), Y(cy - ry), X(cx + rx), Y(cy + ry)], fill=255)
    inner = Image.new("RGBA", layer.size, (0, 0, 0, 0)); di = ImageDraw.Draw(inner)
    di.rectangle([0, 0, layer.size[0], layer.size[1]], fill=WHITE + (255,))
    if closed:
        lid = 1.0
    if not closed:
        prx, pry = 21 * pupil, 39 * pupil
        px_, py_ = cx + look[0], cy + look[1]
        di.ellipse([X(px_ - prx), Y(py_ - pry), X(px_ + prx), Y(py_ + pry)], fill=PUPIL + (255,))
        hl = 7
        di.ellipse([X(px_ - prx * 0.45 - hl), Y(py_ - pry * 0.5 - hl), X(px_ - prx * 0.45 + hl), Y(py_ - pry * 0.5 + hl)], fill=(255, 255, 255, 235))
    # верхнее веко: полуплоскость над наклонной линией
    if lid > 0:
        ly = cy - ry + 2 * ry * lid
        dy = math.tan(math.radians(tilt)) * rx * (1 if eye == "L" else -1)
        poly = [(X(cx - rx - 6), Y(cy - ry - 8)), (X(cx + rx + 6), Y(cy - ry - 8)), (X(cx + rx + 6), Y(ly - dy)), (X(cx - rx - 6), Y(ly + dy))]
        di.polygon(poly, fill=lidc + (255,))
        if lid < 0.99:
            di.line([(X(cx - rx - 6), Y(ly + dy)), (X(cx + rx + 6), Y(ly - dy))], fill=LIDLINE + (255,), width=4 * s)
    if low > 0:
        ly = cy + ry - 2 * ry * low
        di.rectangle([X(cx - rx - 6), Y(ly), X(cx + rx + 6), Y(cy + ry + 8)], fill=lidc + (255,))
        di.line([(X(cx - rx - 6), Y(ly)), (X(cx + rx + 6), Y(ly))], fill=LIDLINE + (255,), width=3 * s)
    layer.paste(inner, (0, 0), eye_mask)
    if closed:
        # закрытый глаз-улыбка: дуга
        d.arc([X(cx - rx + 6), Y(cy - 22), X(cx + rx - 6), Y(cy + 30)], start=200, end=340, fill=LIDLINE + (255,), width=8 * s)


def _draw_brow(layer, eye, ox, oy, dy, ang):
    (cx, cy), (rx, ry) = EYES[eye]
    s = SS
    by = cy - ry - 22 + dy
    half = rx + 8
    a = math.radians(ang)
    x0, y0 = cx - half * math.cos(a), by - half * math.sin(a)
    x1, y1 = cx + half * math.cos(a), by + half * math.sin(a)
    d = ImageDraw.Draw(layer); w = 15
    d.line([((x0 - ox) * s, (y0 - oy) * s), ((x1 - ox) * s, (y1 - oy) * s)], fill=BROW + (255,), width=w * s)
    for (x, y) in ((x0, y0), (x1, y1)):
        d.ellipse([(x - ox - w / 2) * s, (y - oy - w / 2) * s, (x - ox + w / 2) * s, (y - oy + w / 2) * s], fill=BROW + (255,))


def _dush_recolor(img):
    """Серо-оливковая перекраска для Душной жабы."""
    rgb = img.convert("RGB"); a = img.getchannel("A")
    gray = ImageOps.grayscale(rgb)
    tint = ImageOps.colorize(gray, black=(44, 46, 40), mid=(122, 126, 106), white=(222, 216, 190)).convert("RGBA")
    tint.putalpha(a)
    return tint


class _Box:
    """Суперсэмпл-слой только на нужный участок иконки (рисовать весь холст 4096 px на кадр слишком дорого)."""
    def __init__(self, box, ss=3):
        self.x0, self.y0, x1, y1 = [int(v) for v in box]; self.ss = ss
        self.size = (max(1, x1 - self.x0), max(1, y1 - self.y0))
        self.L = Image.new("RGBA", (self.size[0] * ss, self.size[1] * ss), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.L)

    def P(self, pts):
        return [((x - self.x0) * self.ss, (y - self.y0) * self.ss) for x, y in pts]

    def w(self, v):
        return max(1, int(v * self.ss))

    def paste(self, img):
        img.alpha_composite(self.L.resize(self.size, Image.LANCZOS), (self.x0, self.y0))


def _mouth(img, open_, lip=None):
    """Открытый рот: клин от угла рта к кончику морды, внутри язык. lip — цвет губ (помада)."""
    b = _Box((226, 296, 446, 486)); d = b.d
    x0, x1 = MOUTH[0][0], MOUTH[-1][0]
    low = [(x, y + open_ * 64 * (1 - (x - x0) / (x1 - x0)) ** 1.3) for x, y in MOUTH]
    lc = (30, 104, 36, 255) if not lip else lip + (255,)
    if open_ > 0.02:
        d.polygon(b.P(MOUTH + low[::-1]), fill=(74, 18, 30, 255))
        tx, ty = low[1]
        d.ellipse(b.P([(tx - 6, ty - 26 * open_ - 4), (tx + 70, ty + 6)]), fill=(222, 96, 112, 255))
        d.line(b.P(low), fill=lc, width=b.w(6), joint="curve")
    d.line(b.P(MOUTH), fill=lc, width=b.w(6 if not lip else 9), joint="curve")
    b.paste(img)


def _tongue(img, target, t):
    """Язык выстреливает из кончика рта к target (координаты иконки), t — доля длины 0..1."""
    if t <= 0: return
    sx, sy = 252, 336
    ex, ey = sx + (target[0] - sx) * t, sy + (target[1] - sy) * t
    pad = 24
    b = _Box((max(0, min(sx, ex) - pad), max(0, min(sy, ey) - pad), min(1024, max(sx, ex) + pad), min(1024, max(sy, ey) + pad))); d = b.d
    d.line(b.P([(sx, sy), (ex, ey)]), fill=(206, 78, 98, 255), width=b.w(20))
    d.line(b.P([(sx, sy - 3), (ex, ey - 3)]), fill=(236, 120, 136, 255), width=b.w(8))
    d.ellipse(b.P([(ex - 17, ey - 17), (ex + 17, ey + 17)]), fill=(222, 92, 110, 255))
    b.paste(img)


_TEACHER = {}


def _teacher(img, pointer=False):
    """Карикатурная училка: пучок с карандашом, очки-«кошки» на цепочке, кружевной воротник, брошь."""
    if pointer not in _TEACHER:
        b = _Box((300, 50, 960, 920), ss=2); d = b.d
        hair, hair_dk = (92, 80, 78, 255), (60, 52, 52, 255)
        d.ellipse(b.P([(400, 150), (560, 196)]), fill=hair)
        d.ellipse(b.P([(430, 72), (530, 166)]), fill=hair)
        for i in range(4):
            d.arc(b.P([(440 + i * 6, 84 + i * 8), (520 - i * 6, 156 - i * 6)]), start=200, end=330, fill=hair_dk, width=b.w(4))
        d.line(b.P([(412, 70), (548, 152)]), fill=(240, 196, 60, 255), width=b.w(12))
        d.line(b.P([(412, 70), (426, 78)]), fill=(232, 140, 150, 255), width=b.w(12))
        d.polygon(b.P([(548, 152), (566, 156), (552, 144)]), fill=(70, 60, 50, 255))
        for cx, cy, w in ((372, 452, 118), (476, 470, 126)):
            d.ellipse(b.P([(cx - w // 2, cy - 30), (cx + w // 2, cy + 34)]), fill=(250, 248, 240, 255), outline=(200, 196, 186, 255), width=b.w(3))
            for k in range(7):
                a = math.pi * (0.15 + 0.7 * k / 6); px, py = cx + w / 2 * math.cos(a), cy + 34 * math.sin(a)
                d.ellipse(b.P([(px - 7, py - 7), (px + 7, py + 7)]), fill=(250, 248, 240, 255), outline=(200, 196, 186, 255), width=b.w(2))
        d.ellipse(b.P([(410, 448), (448, 494)]), fill=(120, 48, 120, 255), outline=(214, 170, 60, 255), width=b.w(5))
        fr = (112, 28, 52, 255)
        for e in ("L", "R"):
            (cx, cy), (rx, ry) = EYES[e]
            gy = cy + 34
            d.ellipse(b.P([(cx - rx - 12, gy - 30), (cx + rx + 12, gy + 30)]), outline=fr, width=b.w(8))
            wx = cx - rx - 10 if e == "L" else cx + rx + 10
            d.polygon(b.P([(wx, gy - 30), (wx + (-22 if e == "L" else 22), gy - 44), (wx + (6 if e == "L" else -6), gy - 12)]), fill=fr)
        d.line(b.P([(EYES["L"][0][0] + 44, EYES["L"][0][1] + 30), (EYES["R"][0][0] - 40, EYES["R"][0][1] + 30)]), fill=fr, width=b.w(7))
        for (x0, y0), (x1, y1) in (((388, 300), (352, 452)), ((574, 320), (520, 468))):
            for k in range(15):
                t = k / 14; x = x0 + (x1 - x0) * t - 26 * math.sin(math.pi * t); y = y0 + (y1 - y0) * t
                d.ellipse(b.P([(x - 3, y - 3), (x + 3, y + 3)]), fill=(210, 170, 60, 255))
        if pointer:
            d.line(b.P([(930, 900), (760, 330)]), fill=(132, 88, 52, 255), width=b.w(12))
            d.ellipse(b.P([(752, 318), (770, 336)]), fill=(240, 236, 220, 255))
        layer = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0)); b.paste(layer); _TEACHER[pointer] = layer
    img.alpha_composite(_TEACHER[pointer])


_DUSH = {}


def frog(expr="neutral", who="kubysh", coin=True, mouth=0.0, tongue=None, chew=0.0, pointer=False, coin_bite=False, **over):
    """Холст 1024x1024 (координаты иконки, фон прозрачный).
    coin — монета во рту; mouth — открытый рот 0..1 (с монетой: челюсть опускает монету);
    tongue — (target_x, target_y, t) язык к точке; chew — надутые щеки при жевании 0..1."""
    p = dict(EXPR.get(expr, {})); p.update(over)
    body, coin_img = _parts()
    base = body.copy()
    if who == "dush":
        if "b" not in _DUSH: _DUSH["b"] = _dush_recolor(body)
        base = _DUSH["b"].copy()
    if chew > 0:
        r = 30 + 22 * chew
        b = _Box((330 - r - 2, 372 - r - 2, 330 + r + 2, 372 + r + 2))
        b.d.ellipse(b.P([(330 - r, 372 - r * 0.8), (330 + r, 372 + r * 0.8)]), fill=(250, 222, 80, 255)); b.paste(base)
    lip = (178, 30, 52) if who == "dush" else None
    if not coin or who == "dush":
        _mouth(base, mouth, lip)
    elif mouth > 0.04:
        _mouth(base, mouth * 0.55)  # говорит с монетой во рту: челюсть приоткрыта
    ox, oy, ex, ey = 380, 150, 600, 360
    layer = Image.new("RGBA", ((ex - ox) * SS, (ey - oy) * SS), (0, 0, 0, 0))
    wink = p.get("wink", "")
    for e in ("L", "R"):
        lidc = _lid_color(base, e)
        _draw_eye(layer, e, ox, oy, lidc, look=p.get("look", (0, 0)), lid=p.get("lid", 0.15), tilt=p.get("tilt", 0),
                  low=p.get("low", 0.0), pupil=p.get("pupil", 1.0), closed=e in wink)
    brow = p.get("brow")
    if brow:
        for e, (dy, ang) in brow.items():
            _draw_brow(layer, e, ox, oy, dy, ang)
    layer = layer.resize((ex - ox, ey - oy), Image.LANCZOS)
    g = _grain(layer.size)
    shade = Image.merge("RGBA", (g, g, g, layer.getchannel("A").point(lambda v: v * 18 // 255)))
    base.alpha_composite(layer, (ox, oy))
    base.alpha_composite(shade, (ox, oy))
    if who == "dush":
        _teacher(base, pointer)
    elif coin:
        ci = coin_sprite(bite=True) if coin_bite else coin_img
        base.alpha_composite(ci, (COIN_POS[0], COIN_POS[1] + int(10 * mouth)))
    if tongue:
        _tongue(base, tongue[:2], tongue[2])
    return base


def bbox_crop(img):
    return img.crop(img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())


def sheet(out):
    import importlib.util
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "store_cards"))
    from card import F
    from PIL import ImageFont
    W, H = 1080, 1920
    bg = Image.new("RGB", (W, H)); d = ImageDraw.Draw(bg)
    top, bot = (232, 245, 238), (250, 250, 246)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    img = bg.convert("RGBA"); d = ImageDraw.Draw(img)
    k = ImageFont.truetype(F + "Montserrat-Bold.ttf", 34); h1 = ImageFont.truetype(F + "Montserrat-Bold.ttf", 76)
    cap = ImageFont.truetype(F + "Montserrat-SemiBold.ttf", 34)
    d.text((70, 70), "КУБЫШ · СТИЛЬ-КАДР", font=k, fill=(30, 130, 88))
    d.text((70, 120), "Жаба, которая", font=h1, fill=(16, 28, 22)); d.text((70, 205), "не душит", font=h1, fill=(30, 130, 88))
    cells = [("smug", "Не душу. Считаю."), ("wink", "Подмигнул"), ("side", "Серьезно? Таблица?"), ("shock", "Переводы 62%?!")]
    cw = 470
    for i, (e, t) in enumerate(cells):
        f = bbox_crop(frog(e)); f = f.resize((cw - 40, int((cw - 40) * f.height / f.width)), Image.LANCZOS)
        x = 70 + (i % 2) * (cw + 20); y = 330 + (i // 2) * 520
        img.alpha_composite(f, (x + 20, y))
        d.text((x + 20, y + f.height + 10), t, font=cap, fill=(78, 98, 88))
    # дуэль внизу
    y0 = 1390
    dz = bbox_crop(frog("dush", who="dush", pointer=True)).transpose(Image.FLIP_LEFT_RIGHT)
    dz = dz.resize((400, int(400 * dz.height / dz.width)), Image.LANCZOS)
    kb = bbox_crop(frog("smug")); kb = kb.resize((400, int(400 * kb.height / kb.width)), Image.LANCZOS)
    img.alpha_composite(dz, (70, y0)); img.alpha_composite(kb, (W - 70 - 400, y0))
    vs = ImageFont.truetype(F + "Montserrat-Bold.ttf", 60)
    d.text((W // 2 - 40, y0 + 120), "vs", font=vs, fill=(160, 170, 160))
    d.text((70, y0 + dz.height + 14), "Душная жаба", font=cap, fill=(90, 96, 80))
    d.text((W - 70 - 400, y0 + kb.height + 14), "Кубыш", font=cap, fill=(30, 130, 88))
    img.convert("RGB").save(out)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--sheet":
        sheet(sys.argv[2])

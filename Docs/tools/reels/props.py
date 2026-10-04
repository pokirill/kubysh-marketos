"""Декорации и реквизит рилсов: плоская иллюстрация с мягкими тенями и зерном, как у иконки Кубыша.

Декорации рисуются в мировых координатах 1080x1920 с разрешением SC (для наездов камеры) и кэшируются.
Реквизит — RGBA-спрайты; все свое, без чужих эмодзи и логотипов.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache")
FONTS = "/Users/kirillpopov/Documents/FinAssist - ios /FinAssist/FinAssist/Fonts/"
SC = 1.5
WW, WH = 1080, 1920
GROUND = 1560
_F = {}


def font(size, w="Bold"):
    k = (int(size), w)
    if k not in _F: _F[k] = ImageFont.truetype(FONTS + f"Montserrat-{w}.ttf", int(size))
    return _F[k]


def grain(img, amount=14, seed=0):
    n = Image.effect_noise(img.size, 60).point(lambda v: 128 + (v - 128) * amount // 32)
    base = img.convert("RGB")
    out = ImageChops.overlay(base, Image.merge("RGB", (n, n, n)))
    if img.mode == "RGBA": out = out.convert("RGBA"); out.putalpha(img.getchannel("A"))
    return out


def vgrad(d, box, c0, c1):
    x0, y0, x1, y1 = [int(v) for v in box]
    for y in range(y0, y1):
        k = (y - y0) / max(1, y1 - y0 - 1)
        d.line([(x0, y), (x1, y)], fill=tuple(int(c0[i] + (c1[i] - c0[i]) * k) for i in range(3)))


def soft(img, box, color, blur, alpha=255):
    """Мягкое пятно (тень или свет) поверх img."""
    L = Image.new("RGBA", img.size, color + (0,))
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).ellipse(box, fill=alpha)
    L.putalpha(m.filter(ImageFilter.GaussianBlur(blur)))
    img.alpha_composite(L)


# ---------- декорации ----------
class _S:
    """Холст декорации: рисуем в мировых координатах, пиксели в SC раз больше."""
    def __init__(self):
        self.img = Image.new("RGBA", (int(WW * SC), int(WH * SC)), (0, 0, 0, 255)); self.d = ImageDraw.Draw(self.img)

    def p(self, *xy): return [v * SC for v in xy]

    def rect(self, box, fill, r=0, outline=None, width=0):
        if r: self.d.rounded_rectangle(self.p(*box), radius=r * SC, fill=fill, outline=outline, width=int(width * SC))
        else: self.d.rectangle(self.p(*box), fill=fill, outline=outline, width=int(width * SC))

    def ell(self, box, fill, outline=None, width=0):
        self.d.ellipse(self.p(*box), fill=fill, outline=outline, width=int(width * SC))

    def grad(self, box, c0, c1): vgrad(self.d, self.p(*box), c0, c1)

    def poly(self, pts, fill): self.d.polygon([(x * SC, y * SC) for x, y in pts], fill=fill)

    def line(self, pts, fill, width): self.d.line([(x * SC, y * SC) for x, y in pts], fill=fill, width=int(width * SC))

    def soft(self, box, color, blur, alpha=255): soft(self.img, self.p(*box), color, blur * SC, alpha)

    def text(self, xy, s, size, fill, w="Bold", anchor="la"):
        self.d.text(self.p(*xy), s, font=font(size * SC, w), fill=fill, anchor=anchor)


def _floor_shadow(s):
    s.soft((0, GROUND - 40, WW, GROUND + 30), (0, 0, 0), 18, 60)


def set_studio(s):
    s.grad((0, 0, WW, GROUND - 150), (224, 242, 233), (242, 247, 243))
    s.grad((0, GROUND - 150, WW, WH), (222, 236, 228), (232, 241, 235))
    s.soft((-300, -200, WW + 300, 800), (255, 255, 255), 120, 120)


def set_classroom(s):
    s.grad((0, 0, WW, 1240), (196, 214, 202), (182, 202, 188))
    s.grad((0, 1240, WW, GROUND), (208, 182, 142), (190, 162, 122))
    s.rect((0, 1232, WW, 1250), (164, 132, 94))
    for x in range(60, WW, 240): s.rect((x, 1290, x + 180, GROUND - 40), None, r=10, outline=(176, 148, 108), width=4)
    s.grad((0, GROUND, WW, WH), (178, 136, 96), (146, 108, 74))
    for i, y in enumerate(range(GROUND + 40, WH, 70)): s.line([(0, y), (WW, y + (i % 2) * 6)], (134, 98, 66), 3)
    # доска
    s.soft((60, 250, 1040, 1010), (0, 0, 0), 24, 90)
    s.rect((62, 222, 1018, 972), (126, 86, 52), r=22)
    s.grad((92, 252, 988, 942), (44, 80, 62), (34, 66, 52))
    rnd = random.Random(3)
    for _ in range(9):
        x, y = rnd.randint(120, 900), rnd.randint(280, 860); w = rnd.randint(140, 360)
        s.soft((x, y, x + w, y + w * 0.4), (255, 255, 255), 30, 26)
    s.rect((80, 942, 1000, 966), (104, 72, 44), r=6)
    for x, c in ((180, (250, 250, 240)), (232, (250, 226, 150)), (760, (250, 250, 240))):
        s.rect((x, 930, x + 46, 944), c, r=5)
    # часы
    s.soft((110, 1040, 270, 1200), (0, 0, 0), 12, 70)
    s.ell((112, 1030, 262, 1180), (250, 248, 240), outline=(90, 70, 50), width=8)
    for k in range(12):
        a = math.pi * 2 * k / 12; s.line([(187 + 58 * math.cos(a), 1105 + 58 * math.sin(a)), (187 + 66 * math.cos(a), 1105 + 66 * math.sin(a))], (60, 50, 40), 4)
    s.line([(187, 1105), (187, 1058)], (40, 34, 30), 6); s.line([(187, 1105), (222, 1118)], (40, 34, 30), 6)
    _floor_shadow(s)


def set_store(s):
    s.grad((0, 0, WW, GROUND), (238, 240, 244), (220, 224, 232))
    for y in (560, 860):
        s.soft((40, y - 10, 1040, y + 40), (0, 0, 0), 12, 40)
        s.rect((40, y, 1040, y + 22), (250, 250, 252), r=6)
        rnd = random.Random(y)
        x = 70
        while x < 1000:
            w = rnd.randint(90, 150); h = rnd.randint(90, 140)
            c = rnd.choice([(240, 120, 100), (120, 170, 230), (250, 210, 110), (150, 200, 160), (220, 220, 225)])
            s.rect((x, y - h, x + w, y), c, r=10); s.rect((x + 10, y - h + 16, x + w - 10, y - h + 30), (255, 255, 255), r=4)
            x += w + rnd.randint(20, 50)
    s.grad((0, GROUND, WW, WH), (214, 218, 226), (196, 200, 210))
    # подиум и луч
    beam = Image.new("RGBA", s.img.size, (255, 252, 230, 0)); m = Image.new("L", s.img.size, 0)
    ImageDraw.Draw(m).polygon([(v[0] * SC, v[1] * SC) for v in [(420, 0), (660, 0), (780, 1290), (300, 1290)]], fill=90)
    beam.putalpha(m.filter(ImageFilter.GaussianBlur(40 * SC))); s.img.alpha_composite(beam)
    s.soft((330, 1520, 750, 1610), (0, 0, 0), 20, 90)
    s.rect((370, 1250, 710, GROUND + 20), (250, 250, 252), r=14)
    s.ell((370, 1222, 710, 1278), (255, 255, 255), outline=(220, 222, 230), width=3)
    s.grad((370, 1300, 710, 1316), (230, 232, 238), (230, 232, 238))
    _floor_shadow(s)


def set_room(s, calendar=False):
    s.grad((0, 0, WW, GROUND), (246, 234, 216), (232, 216, 194))
    s.soft((640, 300, 960, 800), (255, 255, 255), 60, 120)
    s.rect((620, 280, 980, 820), (250, 250, 250), r=16)
    s.grad((644, 304, 956, 796), (150, 204, 238), (206, 232, 246))
    for cx, cy, r in ((720, 420, 46), (770, 400, 60), (830, 425, 44), (880, 560, 36), (920, 545, 48)):
        s.ell((cx - r, cy - r * 0.6, cx + r, cy + r * 0.6), (255, 255, 255))
    s.rect((796, 304, 806, 796), (250, 250, 250)); s.rect((644, 545, 956, 555), (250, 250, 250))
    s.rect((600, 820, 1000, 846), (236, 228, 214), r=6)
    # полка с книгами
    s.rect((70, 610, 430, 630), (170, 124, 84), r=4)
    x = 90
    for w, h, c in ((34, 120, (210, 90, 80)), (28, 140, (80, 120, 180)), (40, 110, (230, 180, 80)), (30, 130, (90, 160, 120)), (36, 100, (180, 140, 200))):
        s.rect((x, 610 - h, x + w, 610), c, r=4); x += w + 6
    s.ell((300, 520, 390, 612), (120, 170, 110)); s.rect((318, 560, 372, 610), (210, 150, 110), r=8)
    # растение у окна
    s.rect((900, 1400, 1010, GROUND), (200, 120, 90), r=14)
    for a in range(-60, 61, 30):
        rad = math.radians(a - 90); s.ell((955 + 120 * math.cos(rad) - 40, 1400 + 120 * math.sin(rad) - 70, 955 + 120 * math.cos(rad) + 40, 1400 + 120 * math.sin(rad) + 70), (90, 160, 100))
    s.grad((0, GROUND, WW, WH), (212, 176, 134), (190, 150, 108))
    for i, y in enumerate(range(GROUND + 50, WH, 80)): s.line([(0, y), (WW, y)], (180, 140, 100), 3)
    _floor_shadow(s)


def set_night(s, lamp=False):
    s.grad((0, 0, WW, GROUND), (38, 44, 78), (26, 30, 56))
    s.rect((590, 250, 970, 830), (70, 80, 122), r=14)
    s.grad((612, 272, 948, 808), (18, 26, 64), (48, 58, 108))
    rnd = random.Random(7)
    for _ in range(26):
        x, y = rnd.randint(620, 940), rnd.randint(280, 780); r = rnd.choice((2, 2, 3, 4))
        s.ell((x - r, y - r, x + r, y + r), (230, 230, 255))
    s.soft((770, 300, 950, 480), (250, 244, 210), 30, 90)
    s.ell((820, 340, 910, 430), (248, 242, 212))
    s.rect((774, 272, 784, 808), (70, 80, 122)); s.rect((612, 530, 948, 540), (70, 80, 122))
    for x0 in (560, 940):
        s.rect((x0, 220, x0 + 70, 900), (64, 54, 104), r=20)
        for k in range(3): s.line([(x0 + 15 + k * 20, 240), (x0 + 15 + k * 20, 880)], (52, 44, 88), 6)
    # кровать
    s.rect((-60, 1040, 520, 1330), (92, 72, 112), r=40)
    s.rect((-60, 1280, 610, 1650), (74, 94, 168), r=50)
    s.ell((40, 1210, 330, 1330), (206, 210, 234))
    s.line([(0, 1420), (600, 1400)], (90, 112, 190), 10)
    # тумбочка и часы 02:00
    s.rect((660, 1360, 880, GROUND), (82, 66, 92), r=12)
    s.rect((690, 1290, 850, 1360), (20, 20, 26), r=10)
    s.soft((690, 1290, 850, 1360), (255, 60, 60), 18, 70)
    s.text((770, 1325), "02:00", 52, (255, 80, 80), anchor="mm")
    if lamp:
        s.rect((740, 1180, 800, 1290), (200, 190, 170), r=6)
        s.poly([(690, 1180), (850, 1180), (810, 1080), (730, 1080)], (255, 220, 150))
        s.soft((300, 700, 1200, 1700), (255, 200, 120), 160, 120)
    else:
        s.rect((740, 1180, 800, 1290), (90, 84, 100), r=6)
        s.poly([(690, 1180), (850, 1180), (810, 1080), (730, 1080)], (110, 96, 120))
    s.grad((0, GROUND, WW, WH), (30, 32, 58), (22, 24, 44))
    _floor_shadow(s)


SETS = {"studio": set_studio, "classroom": set_classroom, "store": set_store, "room": set_room,
        "night": set_night, "night_lamp": lambda s: set_night(s, lamp=True)}
_SET_MEM = {}


def get_set(name):
    if name in _SET_MEM: return _SET_MEM[name]
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, f"set_{name}.png")
    if os.path.exists(p):
        img = Image.open(p).convert("RGB")
    else:
        s = _S(); SETS[name](s)
        img = grain(s.img.convert("RGB"), 10)
        # виньетка
        m = Image.new("L", (img.width // 8, img.height // 8), 0)
        ImageDraw.Draw(m).ellipse([m.width * 0.02, m.height * 0.1, m.width * 0.98, m.height * 0.92], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(m.width // 7)).resize(img.size, Image.BICUBIC)
        dark = ImageChops.multiply(img, Image.new("RGB", img.size, (170, 176, 182)))
        img = Image.composite(img, dark, m.point(lambda v: 120 + v * 135 // 255))
        img.save(p)
    _SET_MEM[name] = img
    return img


# ---------- реквизит ----------
def _canvas(w, h, ss=2):
    im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0)); return im, ImageDraw.Draw(im), ss


def _fin(im, ss, g=8):
    im = im.resize((im.width // ss, im.height // ss), Image.LANCZOS)
    return grain(im, g)


def sneaker():
    im, d, k = _canvas(460, 250)
    P = lambda pts: [(x * k, y * k) for x, y in pts]
    upper = [(30, 170), (24, 140), (40, 118), (90, 104), (150, 96), (200, 70), (232, 34), (262, 26), (300, 40), (340, 44), (382, 52), (420, 70), (432, 120), (430, 176)]
    d.polygon(P(upper), fill=(255, 112, 86, 255))
    d.polygon(P([(300, 40), (340, 44), (382, 52), (420, 70), (432, 120), (430, 150), (380, 150), (340, 110)]), fill=(232, 88, 70, 255))
    d.polygon(P([(80, 150), (140, 120), (230, 118), (330, 132), (400, 120), (420, 140), (330, 160), (220, 152), (120, 168)]), fill=(255, 255, 255, 255))
    for i in range(5):
        x = 150 + i * 22; d.line(P([(x, 100 - i * 8), (x + 30, 92 - i * 8)]), fill=(255, 255, 255, 255), width=6 * k)
    d.rounded_rectangle([20 * k, 168 * k, 440 * k, 206 * k], radius=18 * k, fill=(250, 250, 250, 255))
    d.rounded_rectangle([20 * k, 196 * k, 440 * k, 214 * k], radius=8 * k, fill=(214, 216, 222, 255))
    d.line(P([(40, 186), (420, 186)]), fill=(225, 226, 232, 255), width=3 * k)
    return _fin(im, k)


def price_tag(text="12 000 ₽"):
    im, d, k = _canvas(300, 150)
    d.rounded_rectangle([40 * k, 20 * k, 290 * k, 130 * k], radius=18 * k, fill=(255, 255, 255, 255), outline=(220, 220, 226, 255), width=3 * k)
    d.polygon([(40 * k, 20 * k), (10 * k, 75 * k), (40 * k, 130 * k)], fill=(255, 255, 255, 255))
    d.ellipse([28 * k, 66 * k, 46 * k, 84 * k], fill=(200, 200, 206, 255))
    d.text((165 * k, 76 * k), text, font=font(46 * k), fill=(20, 28, 24, 255), anchor="mm")
    return _fin(im, k, 4)


def grade_stamp(text="2", color=(214, 36, 52)):
    im, d, k = _canvas(300, 300)
    d.ellipse([18 * k, 18 * k, 282 * k, 282 * k], outline=color + (255,), width=16 * k)
    d.text((150 * k, 158 * k), text, font=font(200 * k), fill=color + (255,), anchor="mm")
    im = im.resize((300, 300), Image.LANCZOS)
    n = Image.effect_noise(im.size, 90).point(lambda v: 255 if v > 70 else 120)
    im.putalpha(ImageChops.multiply(im.getchannel("A"), n))
    return im


def word_stamp(text, color=(36, 168, 96)):
    f = font(96); w = int(f.getlength(text)) + 90
    im, d, k = _canvas(w, 170)
    d.rounded_rectangle([8 * k, 8 * k, (w - 8) * k, 162 * k], radius=22 * k, outline=color + (255,), width=12 * k)
    d.text((w // 2 * k, 88 * k), text, font=font(96 * k), fill=color + (255,), anchor="mm")
    im = im.resize((w, 170), Image.LANCZOS)
    n = Image.effect_noise(im.size, 90).point(lambda v: 255 if v > 70 else 120)
    im.putalpha(ImageChops.multiply(im.getchannel("A"), n))
    return im


def anger():
    im, d, k = _canvas(120, 120)
    c = (226, 40, 54, 255)
    for a in range(4):
        ang = math.pi / 2 * a + math.pi / 4
        cx, cy = 60 + 26 * math.cos(ang), 60 + 26 * math.sin(ang)
        d.arc([(cx - 30) * k, (cy - 30) * k, (cx + 30) * k, (cy + 30) * k], start=math.degrees(ang) + 120, end=math.degrees(ang) + 240, fill=c, width=11 * k)
    return im.resize((120, 120), Image.LANCZOS)


def sweat():
    im, d, k = _canvas(80, 120)
    d.polygon([(40 * k, 6 * k), (12 * k, 74 * k), (68 * k, 74 * k)], fill=(120, 190, 250, 255))
    d.ellipse([12 * k, 48 * k, 68 * k, 110 * k], fill=(120, 190, 250, 255))
    d.ellipse([26 * k, 66 * k, 40 * k, 86 * k], fill=(230, 245, 255, 255))
    return im.resize((80, 120), Image.LANCZOS)


def sparkle(color=(255, 222, 90)):
    im, d, k = _canvas(100, 100)
    pts = []
    for i in range(8):
        r = 48 if i % 2 == 0 else 12; a = math.pi / 4 * i - math.pi / 2
        pts.append(((50 + r * math.cos(a)) * k, (50 + r * math.sin(a)) * k))
    d.polygon(pts, fill=color + (255,))
    return im.resize((100, 100), Image.LANCZOS)


def glyph_bubble(ch, color=(255, 255, 255), fg=(20, 28, 24)):
    im, d, k = _canvas(120, 120)
    d.ellipse([6 * k, 6 * k, 114 * k, 114 * k], fill=color + (255,))
    d.text((60 * k, 62 * k), ch, font=font(76 * k), fill=fg + (255,), anchor="mm")
    return im.resize((120, 120), Image.LANCZOS)


def buckwheat():
    im, d, k = _canvas(260, 340)
    bag = (196, 150, 98, 255)
    d.rounded_rectangle([20 * k, 60 * k, 240 * k, 330 * k], radius=16 * k, fill=bag)
    zz = [(20 + i * 22, 60 - (14 if i % 2 else 0)) for i in range(11)]
    d.polygon([(x * k, y * k) for x, y in zz] + [(240 * k, 80 * k), (20 * k, 80 * k)], fill=bag)
    d.rounded_rectangle([40 * k, 140 * k, 220 * k, 250 * k], radius=10 * k, fill=(250, 240, 220, 255))
    d.text((130 * k, 178 * k), "ГРЕЧКА", font=font(34 * k), fill=(110, 70, 40, 255), anchor="mm")
    d.text((130 * k, 220 * k), "1 кг", font=font(26 * k, "SemiBold"), fill=(140, 100, 70, 255), anchor="mm")
    rnd = random.Random(2)
    for _ in range(40):
        x, y = rnd.randint(40, 220), rnd.randint(262, 320); d.ellipse([x * k, y * k, (x + 7) * k, (y + 5) * k], fill=(150, 104, 60, 255))
    return _fin(im, k)


def calendar(month="ОКТЯБРЬ", day="7"):
    im, d, k = _canvas(360, 420)
    d.rounded_rectangle([10 * k, 30 * k, 350 * k, 410 * k], radius=24 * k, fill=(255, 255, 255, 255))
    d.rounded_rectangle([10 * k, 30 * k, 350 * k, 130 * k], radius=24 * k, fill=(220, 58, 64, 255))
    d.rectangle([10 * k, 100 * k, 350 * k, 130 * k], fill=(220, 58, 64, 255))
    for x in (90, 180, 270):
        d.rounded_rectangle([(x - 8) * k, 6 * k, (x + 8) * k, 56 * k], radius=8 * k, fill=(90, 90, 96, 255))
    d.text((180 * k, 82 * k), month, font=font(46 * k), fill=(255, 255, 255, 255), anchor="mm")
    d.text((180 * k, 268 * k), day, font=font(200 * k), fill=(30, 34, 40, 255), anchor="mm")
    return _fin(im, k, 4)


def notes_card(lines, scroll=0.0, w=760, h=980):
    """Карточка заметок с длинным списком трат; scroll — сдвиг списка в пикселях."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=44, fill=(255, 253, 246, 255))
    body = Image.new("RGBA", (w, h - 170), (0, 0, 0, 0)); bd = ImageDraw.Draw(body)
    y = 10 - scroll
    for i, (a, b) in enumerate(lines):
        if -60 < y < body.height:
            bd.text((50, y), f"{i + 1}. {a}", font=font(40, "Medium"), fill=(40, 40, 44, 255))
            bd.text((w - 50, y), b, font=font(40, "SemiBold"), fill=(40, 40, 44, 255), anchor="ra")
        y += 62
    im.alpha_composite(body, (0, 150))
    d.rounded_rectangle([0, 0, w - 1, 140], radius=44, fill=(255, 214, 90, 255)); d.rectangle([0, 100, w - 1, 140], fill=(255, 214, 90, 255))
    d.text((50, 70), "Заметки · траты", font=font(52), fill=(60, 44, 10, 255), anchor="lm")
    return im


def notification(title, body, w=980):
    im = Image.new("RGBA", (w, 210), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 209], radius=48, fill=(250, 250, 252, 246))
    d.rounded_rectangle([36, 46, 156, 166], radius=30, fill=(40, 160, 96, 255))
    d.text((96, 106), "₽", font=font(80), fill=(255, 255, 255, 255), anchor="mm")
    d.text((188, 76), title, font=font(44), fill=(20, 22, 26, 255), anchor="lm")
    d.text((w - 40, 76), "сейчас", font=font(34, "Medium"), fill=(140, 142, 150, 255), anchor="rm")
    d.text((188, 140), body, font=font(42, "Medium"), fill=(40, 42, 48, 255), anchor="lm")
    return im


def avatar_max(size=104):
    im, d, k = _canvas(size, size, 4)
    s = size
    d.ellipse([0, 0, s * k, s * k], fill=(122, 172, 238, 255))
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse([0, 0, s * k, s * k], fill=255)
    L = Image.new("RGBA", im.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
    ld.ellipse([0.14 * s * k, 0.66 * s * k, 0.86 * s * k, 1.3 * s * k], fill=(62, 70, 92, 255))
    ld.ellipse([0.3 * s * k, 0.2 * s * k, 0.7 * s * k, 0.68 * s * k], fill=(244, 204, 172, 255))
    ld.chord([0.27 * s * k, 0.12 * s * k, 0.73 * s * k, 0.52 * s * k], start=180, end=360, fill=(70, 46, 34, 255))
    im.paste(L, (0, 0), ImageChops.multiply(L.getchannel("A"), m))
    return im.resize((size, size), Image.LANCZOS)


def kubysh_avatar(size=104):
    p = "/Users/kirillpopov/Documents/FinAssist - ios /FinAssist/FinAssist/Assets.xcassets/KubyshTabIcon.imageset/pepe@3x.png"
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, size - 1, size - 1], fill=(222, 244, 230, 255))
    ic = Image.open(p).convert("RGBA").resize((int(size * 0.82), int(size * 0.82)), Image.LANCZOS)
    im.alpha_composite(ic, ((size - ic.width) // 2, (size - ic.height) // 2 + 2))
    return im


def bubble(text, side="l", w_max=760):
    """Пузырь чата: me — свое сообщение зрителя (справа, мятный), l — собеседник (белый), r — Кубыш (зеленый)."""
    f = font(44, "Medium")
    words = text.split(); lines = [""]
    for wd in words:
        t = (lines[-1] + " " + wd).strip()
        if f.getlength(t) > w_max - 80 and lines[-1]: lines.append(wd)
        else: lines[-1] = t
    tw = max(f.getlength(l) for l in lines); w = int(tw) + 76; h = 60 * len(lines) + 46
    im = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bg, fg = {"l": ((255, 255, 255, 250), (24, 26, 30, 255)), "me": ((214, 246, 226, 252), (20, 40, 28, 255))}.get(side, ((38, 158, 98, 255), (255, 255, 255, 255)))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([6, 12, w + 6, h + 12], radius=38, fill=(0, 0, 0, 60))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d.rounded_rectangle([0, 0, w, h], radius=38, fill=bg)
    for i, l in enumerate(lines): d.text((38, 24 + i * 60), l, font=f, fill=fg)
    return im


def typing_dots(phase):
    im = Image.new("RGBA", (170, 100), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 160, 92], radius=40, fill=(255, 255, 255, 245))
    for i in range(3):
        a = 0.5 + 0.5 * math.sin(phase * 2 * math.pi - i * 0.9)
        d.ellipse([34 + i * 34, 34 - 8 * a, 54 + i * 34, 54 - 8 * a], fill=(150, 152, 160, 255))
    return im


def chalk_text(text, size, color=(236, 240, 228)):
    f = font(size, "SemiBold")
    w = int(f.getlength(text)) + 30; h = int(size * 1.4)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(im).text((10, h // 2), text, font=f, fill=color + (255,), anchor="lm")
    n = Image.effect_noise(im.size, 80).point(lambda v: 255 if v > 60 else 90)
    im.putalpha(ImageChops.multiply(im.getchannel("A"), n).filter(ImageFilter.GaussianBlur(0.6)))
    return im


def zzz():
    im = Image.new("RGBA", (220, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (x, y, s) in enumerate(((20, 130, 50), (80, 70, 64), (150, 10, 80))):
        d.text((x, y), "z", font=font(s), fill=(230, 236, 255, 255))
    return im

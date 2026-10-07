"""Студия рилсов v2: декорации, камера, живые персонажи, субтитры по словам, графика и сюжет.

Эпизод — файл в episodes/ с функцией build(ep). Внутри — реплики (ep.line), действия персонажей,
планы камеры, карточки экранов, чат Макса, штампы, счетчики. Время задается секундами, удобно
привязывать к репликам: t0, t1 = ep.line(...).
Запуск: python3 studio.py episodes/e01_zhaba.py [--preview 1.0,4.5]
"""
import importlib.util, math, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from frog import frog, coin_sprite  # noqa: E402
import props as P  # noqa: E402
import audio  # noqa: E402

W, H, FPS = 1080, 1920, 30
GROUND = P.GROUND
PIV = (540, 880); COIN_C = (278, 391); HEAD = (520, 160); EYE_C = (483, 270)
INK = (18, 26, 22); YEL = (255, 214, 74); PINK = (255, 132, 150); MINT = (96, 222, 150); WHITE = (255, 255, 255)
ENC = os.path.join(HERE, "..", "store_cards", "mp4enc")
OUT_ROOT = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы маскот"
OUT_KSY = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша"
SHOTS = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Скриншоты 1.7/"
SET_TINT = {"night": (150, 160, 225), "night_lamp": (255, 238, 214)}
VO_CACHE = os.path.join(HERE, ".cache", "vo")
audio.CAST = audio.CASTS["yandex"]


# ---------- время ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eio(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x, s=1.8): x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def seg(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def pulse(t, a, b): return math.sin(math.pi * seg(t, a, b)) if a <= t <= b else 0.0
def lerp(a, b, k): return a + (b - a) * k


def comp(img, src, x, y):
    x, y = int(round(x)), int(round(y))
    sx0, sy0 = max(0, -x), max(0, -y); sx1, sy1 = min(src.width, img.width - x), min(src.height, img.height - y)
    if sx1 > sx0 and sy1 > sy0: img.alpha_composite(src.crop((sx0, sy0, sx1, sy1)), (x + sx0, y + sy0))


def fade(im, a):
    if a >= 0.999: return im
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a))); return im


def scaled(im, k, rot=0):
    if abs(k - 1) > 0.01: im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    return im


# ---------- текст ----------
_TX = {}
def word_img(s, size, fill=WHITE, stroke=INK):
    """Слово белым с темной обводкой и мягкой тенью — читается на любой декорации."""
    k = (s, size, fill, stroke)
    if k in _TX: return _TX[k]
    f = P.font(size); sw = max(5, size // 9)
    asc, desc = f.getmetrics(); w = int(f.getlength(s)) + 2 * sw + 8; h = asc + desc + 2 * sw + 8
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((sw + 4, sw + 4), s, font=f, fill=fill + (255,), stroke_width=sw, stroke_fill=stroke + (255,))
    sh = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0)); a = im.getchannel("A").filter(ImageFilter.GaussianBlur(6))
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0)); shadow.putalpha(a.point(lambda v: v * 90 // 255))
    sh.alpha_composite(shadow, (6, 12)); sh.alpha_composite(im, (0, 0))
    _TX[k] = sh
    return sh


# ---------- камера ----------
class Camera:
    def __init__(self):
        self.keys = []; self.shakes = []

    def state(self, t):
        cx, cy, z = 540.0, 960.0, 1.04; tk_last = 0.0
        for tk, kx, ky, kz, dur in sorted(self.keys, key=lambda k: k[0]):
            if tk > t: break
            if dur <= 0: cx, cy, z = kx, ky, kz
            else:
                p = eio(seg(t, tk, tk + dur)); cx, cy, z = lerp(cx, kx, p), lerp(cy, ky, p), lerp(z, kz, p)
            tk_last = tk
        z *= 1 + min(0.05, 0.012 * (t - tk_last))
        dx = 3 * math.sin(0.7 * t) + 2 * math.sin(1.9 * t + 1); dy = 3 * math.sin(0.5 * t + 2) + 2 * math.sin(1.3 * t)
        for t0, amp in self.shakes:
            if 0 <= t - t0 < 0.6:
                k = math.exp(-(t - t0) * 8) * amp; dx += k * math.sin(2 * math.pi * 14 * (t - t0)); dy += k * math.cos(2 * math.pi * 11 * (t - t0))
        z = max(1.02, z)
        hw, hh = 540 / z + 8, 960 / z + 8
        cx = clamp(cx, hw, 1080 - hw); cy = clamp(cy, hh, 1920 - hh)
        return cx, cy, z, dx, dy


def to_screen(cam, x, y):
    cx, cy, z, dx, dy = cam; return (x - cx) * z + 540 + dx, (y - cy) * z + 960 + dy


def to_world(cam, sx, sy):
    cx, cy, z, dx, dy = cam; return (sx - 540 - dx) / z + cx, (sy - 960 - dy) / z + cy


# ---------- лягушки в кадре ----------
def icon_to_screen(ix, iy, x, y, s, sq=0.0, tilt=0.0, mirror=False, hop=0.0):
    pivx = PIV[0]
    if mirror: ix = 1024 - ix; pivx = 1024 - PIV[0]
    dx = (ix - pivx) * s * (1 + sq); dy = (iy - PIV[1]) * s * (1 - sq); a = math.radians(tilt)
    return x + dx * math.cos(a) + dy * math.sin(a), y - hop - dx * math.sin(a) + dy * math.cos(a)


def screen_to_icon(sx, sy, x, y, s, sq=0.0, tilt=0.0, mirror=False, hop=0.0):
    dx, dy = sx - x, sy - (y - hop); a = math.radians(-tilt)
    rx, ry = dx * math.cos(a) + dy * math.sin(a), -dx * math.sin(a) + dy * math.cos(a)
    ix = rx / (s * (1 + sq)) + (1024 - PIV[0] if mirror else PIV[0]); iy = ry / (s * (1 - sq)) + PIV[1]
    return (1024 - ix if mirror else ix), iy


_ELL = {}
def shadow_ellipse(w, h, a):
    key = (w // 6, h // 3, a // 8)
    if key not in _ELL:
        s = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
        ImageDraw.Draw(s).ellipse([40, 40, 40 + w, 40 + h], fill=(14, 40, 28, a))
        _ELL[key] = s.filter(ImageFilter.GaussianBlur(max(6, h // 3)))
    return _ELL[key]


def put_frog(img, fr, x, y, s, sq=0.0, tilt=0.0, mirror=False, hop=0.0, tint=None, floor=True):
    if mirror: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    pivx = 1024 - PIV[0] if mirror else PIV[0]
    sw, sh = max(2, int(1024 * s * (1 + sq))), max(2, int(1024 * s * (1 - sq)))
    f = fr.resize((sw, sh), Image.BILINEAR if s < 0.5 else Image.LANCZOS)
    if tint:
        a = f.getchannel("A"); f = ImageChops.multiply(f.convert("RGB"), Image.new("RGB", f.size, tint)).convert("RGBA"); f.putalpha(a)
    px, py = pivx * sw / 1024, PIV[1] * sh / 1024
    if tilt: f = f.rotate(tilt, resample=Image.BICUBIC, center=(px, py))
    k = clamp(1 - hop / (500 * s + 1))
    e = shadow_ellipse(int(620 * s * (0.55 + 0.45 * k)), int(70 * s * (0.6 + 0.4 * k)) + 4, int((130 if floor else 90) * k))
    comp(img, e, x - e.width / 2, y - e.height / 2 + 6 * s)
    a = f.getchannel("A").resize((max(1, sw // 6), max(1, sh // 6))).filter(ImageFilter.GaussianBlur(3)).resize((sw, sh), Image.BILINEAR)
    ds = Image.new("RGBA", (sw, sh), (10, 40, 26, 0)); ds.putalpha(a.point(lambda v: v * 60 // 255))
    comp(img, ds, x - px + 24 * s, y - hop - py + 14 * s)
    comp(img, f, x - px, y - hop - py)


class Actor:
    """Персонаж: прыжки, моргание, взгляд на собеседника, речь, реакции, трюки с монетой (Кубыш)."""
    BLEND = 0.09

    def __init__(self, ep, name, who, x, s=0.72, mirror=False, coin=True, pointer=False, hidden=False, ground=GROUND, floor=True):
        self.ep, self.name, self.who, self.x0, self.s, self.mirror = ep, name, who, x, s, mirror
        self.ground, self.floor = ground, floor
        self.coin_default, self.pointer = coin, pointer
        self.moves, self.exprs, self.looks, self.reacts, self.coin_ev = [], [(0, {})], [], [], []
        self.vis = [(0, not hidden)]
        r = random.Random(name); t = r.uniform(0.6, 2.0); self.blinks = []
        while t < 120: self.blinks.append(t); t += r.uniform(2.0, 4.6)
        r2 = random.Random(name + "s"); self.sacc = [(i * 1.3, r2.uniform(-4, 4), r2.uniform(-3, 3)) for i in range(100)]
        self.phase = r.uniform(0, 6)
        self.cur = None; self.bite = False

    # --- команды сценария ---
    def go(self, t, x1, hop=70, step=170, dur=0.34):
        x = self.x_at_end(t); n = max(1, math.ceil(abs(x1 - x) / step))
        for i in range(n):
            self.moves.append((t + i * (dur + 0.05), x + (x1 - x) * (i + 1) / n, dur, hop))
        self.ep.sfx(t, "hop", 0.35); return t + n * (dur + 0.05)

    def jump(self, t, h=150, dur=0.46): self.moves.append((t, self.x_at_end(t), dur, h)); self.ep.sfx(t, "boing", 0.45)
    def place(self, t, x): self.moves.append((t, x, 0, 0))
    def expr(self, t, name="neutral", **kw): p = dict(__import__("frog").EXPR.get(name, {})); p.update(kw); self.exprs.append((t, p))
    def look(self, t, target=None): self.looks.append((t, target))
    def react(self, t, kind): self.reacts.append((t, kind))
    def show(self, t, on=True): self.vis.append((t, on))
    def spit_catch(self, t): self.coin_ev.append((t, "spit")); self.ep.sfx(t - 0.02, "thwip", 0.5); self.ep.sfx(t, "whoosh", 0.3)
    def toss(self, t): self.coin_ev.append((t, "toss")); self.ep.sfx(t, "thwip", 0.35); self.ep.sfx(t + 0.4, "clink", 0.55)
    def bite_coin(self, t):
        self.coin_ev.append((t, "bite")); self.ep.sfx(t, "crunch", 0.7); self.ep.sfx(t + 0.22, "crunch", 0.6)

    def x_at_end(self, t):
        """Куда персонаж придет после всех прыжков, начатых до t (для следующей команды go)."""
        x = self.x0
        for m in sorted(self.moves, key=lambda m: m[0]):
            if m[0] <= t + 1e-3: x = m[1]
        return x

    # --- состояние ---
    def visible(self, t):
        v = True
        for tv, on in self.vis:
            if tv <= t: v = on
        return v

    def body(self, t):
        x, h, sq, tilt = self.x0, 0.0, 0.0, 0.0
        for t0, x1, dur, height in sorted(self.moves, key=lambda m: m[0]):
            if dur == 0:
                if t >= t0: x = x1
                continue
            if t < t0:
                sq += 0.08 * pulse(t, t0 - 0.09, t0); break
            if t < t0 + dur:
                p = (t - t0) / dur; xa = x; x = lerp(xa, x1, eio(p)); h = height * 4 * p * (1 - p)
                sq += -0.07 * math.sin(math.pi * p) * (1 if height > 0 else 0)
                tilt += (-1 if x1 > xa else 1 if x1 < xa else 0) * 7 * math.sin(math.pi * p); break
            x = x1; sq += 0.11 * pulse(t, t0 + dur, t0 + dur + 0.22)
        return x, h, sq, tilt

    def target(self, t):
        p = {}
        for te, pe in self.exprs:
            if te <= t: p = pe
        return p

    def update(self, t, dt, actors, cam):
        tg = self.target(t)
        look = None
        lt = [lt for lt in self.looks if lt[0] <= t]
        tgt = lt[-1][1] if lt else None
        x, h, _, _ = self.body(t)
        sx, sy = to_screen(cam, x, self.ground); s = self.s * cam[2]
        if tgt is None and "look" not in tg:
            for a in actors:
                if a is not self and a.visible(t) and a.talk(t) > 0.08: tgt = a.name
        if isinstance(tgt, str) and tgt in self.ep.actors:
            o = self.ep.actors[tgt]; ox, oh, _, _ = o.body(t)
            px, py = icon_to_screen(*EYE_C, *to_screen(cam, ox, o.ground), o.s * cam[2], mirror=o.mirror, hop=oh * cam[2])
        elif isinstance(tgt, tuple) and len(tgt) == 3 and tgt[0] == "screen":
            px, py = tgt[1], tgt[2]
        elif isinstance(tgt, tuple):
            px, py = to_screen(cam, *tgt)
        else:
            px = py = None
        if px is not None:
            ix, iy = screen_to_icon(px, py, sx, sy, s, mirror=self.mirror, hop=h * cam[2])
            vx, vy = ix - EYE_C[0], iy - EYE_C[1]; n = math.hypot(vx, vy) or 1
            look = (13 * vx / n, 15 * vy / n)
        else:
            i = min(len(self.sacc) - 1, int(t / 1.3)); look = (self.sacc[i][1], self.sacc[i][2])
        if "look" in tg and tgt is None: look = tg["look"]
        want = dict(look=look, lid=tg.get("lid", 0.16), tilt=tg.get("tilt", 0), low=tg.get("low", 0.0), pupil=tg.get("pupil", 1.0),
                    bl=tg.get("brow", {}).get("L", (-8, -2)), br=tg.get("brow", {}).get("R", (-8, 2)))
        if self.cur is None: self.cur = {k: v for k, v in want.items()}
        a = 1 - math.exp(-dt / self.BLEND); al = 1 - math.exp(-dt / 0.035)
        for k, v in want.items():
            c = self.cur[k]; r = al if k == "look" else a
            self.cur[k] = tuple(lerp(ci, vi, r) for ci, vi in zip(c, v)) if isinstance(v, tuple) else lerp(c, v, r)
        self.wink = tg.get("wink", "")

    def talk(self, t):
        i = int(t * FPS); e = self.ep.env.get(self.name)
        return e[i] if e and 0 <= i < len(e) else 0.0

    # --- монета ---
    def coin_state(self, t, mouth_screen, s):
        """('mouth'|'air'|'tongue', позиция на экране, flip)"""
        for t0, kind in self.coin_ev:
            if kind == "spit":
                Hh, Tu = 620 * s, 0.4; V = 2 * Hh / Tu; G = 2 * Hh / Tu ** 2
                tc = t0 + (V + math.sqrt(V * V - 2 * G * 0.62 * Hh)) / G; tin = tc + 0.2
                if t0 <= t < tc:
                    dt = t - t0; return "air", (mouth_screen[0] - 40 * s * dt, mouth_screen[1] - V * dt + G * dt * dt / 2), math.cos(2 * math.pi * 2.6 * dt), (tc, tin)
                if tc <= t < tin:
                    dt = tc - t0; cpos = (mouth_screen[0] - 40 * s * dt, mouth_screen[1] - V * dt + G * dt * dt / 2)
                    return "tongue", cpos, 1 - eout(seg(t, tc, tin)), (tc, tin)
                if tc - 0.07 <= t < tc:
                    pass
            if kind == "toss" and t0 <= t < t0 + 0.4:
                dt = t - t0; return "air", (mouth_screen[0], mouth_screen[1] - 170 * s * math.sin(math.pi * dt / 0.4)), math.cos(2 * math.pi * 1.25 * dt), None
        return "mouth", mouth_screen, 1, None

    # --- кадр ---
    def draw(self, img, t, cam):
        if not self.visible(t): return
        x, h, sq, tilt = self.body(t)
        sx, sy = to_screen(cam, x, self.ground); s = self.s * cam[2]; hop = h * cam[2]
        talk = self.talk(t)
        sq += 0.012 * math.sin(2 * math.pi * t / 2.4 + self.phase) + 0.03 * talk
        tilt += 0.8 * math.sin(2 * math.pi * t / 3.7 + self.phase) + 2.4 * talk * math.sin(2 * math.pi * 2.7 * t + self.phase)
        sc = self.s
        for t0, kind in self.reacts:
            d = t - t0
            if d < 0 or d > 0.8: continue
            if kind == "shake": tilt += 8 * math.sin(2 * math.pi * 4.5 * d) * math.exp(-d * 4)
            elif kind == "nod": sq += 0.07 * pulse(t, t0, t0 + 0.2) + 0.06 * pulse(t, t0 + 0.24, t0 + 0.44)
            elif kind == "shudder": sx += 8 * math.sin(2 * math.pi * 18 * d) * (1 - seg(t, t0, t0 + 0.5))
            elif kind == "puff": s *= 1 + 0.08 * pulse(t, t0, t0 + 0.4)
            elif kind == "recoil": tilt += (-10 if not self.mirror else 10) * pulse(t, t0, t0 + 0.5); sx += (30 if not self.mirror else -30) * pulse(t, t0, t0 + 0.5) * cam[2]
            elif kind == "lean": tilt += (6 if not self.mirror else -6) * pulse(t, t0, t0 + 0.8)
        c = self.cur
        lid = c["lid"]
        for tb in self.blinks:
            if tb <= t <= tb + 0.13: lid = max(lid, pulse(t, tb, tb + 0.13))
        mouth = talk * 0.85
        p = dict(look=c["look"], lid=lid, tilt=c["tilt"], low=c["low"], pupil=c["pupil"],
                 brow={"L": (c["bl"][0] - 6 * talk, c["bl"][1]), "R": (c["br"][0] - 6 * talk, c["br"][1])}, wink=self.wink)
        coin_in, tongue, cstate = True, None, None
        if self.who == "kubysh":
            mx, my = icon_to_screen(*COIN_C, sx, sy, s, sq, tilt, self.mirror, hop)
            cstate = self.coin_state(t, (mx, my), s)
            if cstate[0] == "air": coin_in = False; mouth = max(mouth, 0.35)
            elif cstate[0] == "tongue":
                coin_in = False; tc, tin = cstate[3]
                ix, iy = screen_to_icon(*cstate[1], sx, sy, s, sq, tilt, self.mirror, hop)
                tongue = (ix, iy, cstate[2]); mouth = max(mouth, 0.5)
            for t0, kind in self.coin_ev:
                if kind == "spit":
                    Hh, Tu = 620 * s, 0.4; V = 2 * Hh / Tu; G = 2 * Hh / Tu ** 2
                    tc = t0 + (V + math.sqrt(V * V - 2 * G * 0.62 * Hh)) / G
                    if tc - 0.07 <= t < tc:
                        dt = tc - t0; cp = (mx - 40 * s * dt, my - V * dt + G * dt * dt / 2)
                        ix, iy = screen_to_icon(*cp, sx, sy, s, sq, tilt, self.mirror, hop); tongue = (ix, iy, seg(t, tc - 0.07, tc)); mouth = max(mouth, 0.5)
                    if t0 - 0.02 <= t < t0 + 0.2: mouth = max(mouth, 0.6 * pulse(t, t0 - 0.02, t0 + 0.2))
                if kind == "bite":
                    if t0 <= t < t0 + 0.45: mouth = max(mouth, 0.5 * pulse(t, t0, t0 + 0.18) + 0.5 * pulse(t, t0 + 0.22, t0 + 0.4))
                    if t >= t0 + 0.1: self.bite = True
            if not self.coin_default: coin_in = False
        tint = SET_TINT.get(self.ep.set_at(t))
        fr = frog(who="dush" if self.who == "dush" else "kubysh", coin=coin_in, mouth=mouth, tongue=tongue,
                  pointer=self.pointer, coin_bite=self.bite, **p)
        put_frog(img, fr, sx, sy, s, sq, tilt, self.mirror, hop, tint, self.floor)
        if cstate and cstate[0] in ("air", "tongue"):
            cs = coin_sprite(flip=cstate[2] if cstate[0] == "air" else 0.85, bite=self.bite, rot=8 * math.sin(t * 9))
            cs = cs.resize((max(1, int(cs.width * s)), max(1, int(cs.height * s))), Image.LANCZOS)
            if cstate[0] == "tongue":
                tc, tin = cstate[3]; k = 1 - eout(seg(t, tc, tin))
                ix, iy = 252 + (tongue[0] - 252) * k, 336 + (tongue[1] - 336) * k
                cp = icon_to_screen(ix, iy, sx, sy, s, sq, tilt, self.mirror, hop)
            else:
                cp = cstate[1]
            comp(img, cs, cp[0] - cs.width / 2, cp[1] - cs.height / 2)
        self.last = (sx, sy, s, sq, tilt, hop)

    def head(self):
        sx, sy, s, sq, tilt, hop = self.last
        return icon_to_screen(*HEAD, sx, sy, s, sq, tilt, self.mirror, hop)


# ---------- эпизод ----------
def _nodot(words):
    """Точку в конце подписи не ставим (Кирилл, 07.10): «…», «?» и «!» остаются."""
    if words:
        w = words[-1]; core = w.rstrip("*")
        if core.endswith(".") and not core.endswith("..") and not core.endswith("…"):
            words[-1] = core[:-1] + w[len(core):]
    return words


class Ep:
    def __init__(self, name, set_name="studio"):
        self.name, self.cursor, self.dur = name, 0.0, 10.0
        self.actors, self.order = {}, []
        self.cam = Camera(); self.sets = [(0, set_name, 0.0)]
        self.voice, self.sfx_ev, self.caps, self.ov = [], [], [], []
        self.env = {}; self.chat_slots = []; self.cover_t = 0.8; self.clips = []

    # персонажи и декорации
    def actor(self, name, who, x, **kw):
        a = Actor(self, name, who, x, **kw); self.actors[name] = a; self.order.append(a); return a

    def set(self, t, name, fade=0.0): self.sets.append((t, name, fade))

    def set_at(self, t):
        n = self.sets[0][1]
        for ts, nm, f in self.sets:
            if ts <= t: n = nm
        return n

    # звук и реплики
    def sfx(self, t, name, g=0.5): self.sfx_ev.append((t, name, g))

    def line(self, who, text, cap=None, at=None, gap=0.16, y=None, size=84):
        """who — имя персонажа. text: TTS-строка, «+» перед ударной гласной, *слово* — выделить в субтитрах."""
        vo = text.replace("*", "")
        a = self.actors[who]
        smp = audio.voice(vo, "dush" if a.who == "dush" else "kubysh", VO_CACHE)
        t0 = self.cursor if at is None else at
        d = len(smp) / audio.SR
        self.voice.append((t0, smp))
        env = audio.envelope(smp, FPS); e = self.env.setdefault(who, [0.0] * int(400 * FPS)); f0 = int(t0 * FPS)
        for i, v in enumerate(env):
            if f0 + i < len(e): e[f0 + i] = max(e[f0 + i], v)
        words = (cap if cap is not None else text).replace("+", "").split(" ")
        words = _nodot([w for w in words if w])
        wts = [max(1, sum(ch in "аеёиоуыэюяАЕЁИОУЫЭЮЯ" for ch in w)) + (0.6 if w[-1] in ".,?!:" else 0) for w in words]
        tot = sum(wts); acc = 0; times = []
        for w in wts: times.append(t0 + 0.05 + (d - 0.15) * acc / tot); acc += w
        self.caps.append(dict(t0=t0, t1=t0 + d + 0.3, words=words, times=times, who=a.who, y=y, size=size))
        self.cursor = t0 + d + gap
        return t0, t0 + d

    def duck(self, smp, depth=0.25, pad=0.15):
        """Фон под голосами: где звучит реплика, громкость фона падает до depth (плавно)."""
        import array as _a
        SR = audio.SR; g = _a.array("f", [1.0]) * len(smp)
        for t0, v in self.voice:
            a, b = int((t0 - pad) * SR), int((t0 + len(v) / SR + pad) * SR)
            for i in range(max(0, a), min(len(g), b)): g[i] = depth
        k = 0.0005; out = []; cur = 1.0
        for i, x in enumerate(smp):
            cur += (g[i] - cur) * k; out.append(x * cur)
        return out

    def say(self, who, text, cap=None, at=None, gap=0.16, y=None, size=84, file=None):
        """Реплика героини в кадре клипа (Ксюша): file — ее живая запись, иначе черновой синтез (CAST[who])."""
        smp = audio.load(file) if file and os.path.exists(file) else audio.voice(text.replace("*", ""), who, VO_CACHE)
        t0 = self.cursor if at is None else at; d = len(smp) / audio.SR
        self.voice.append((t0, smp))
        words = (cap if cap is not None else text).replace("+", "").split(" ")
        words = _nodot([w for w in words if w])
        wts = [max(1, sum(ch in "аеёиоуыэюяАЕЁИОУЫЭЮЯ" for ch in w)) + (0.6 if w[-1] in ".,?!:" else 0) for w in words]
        tot = sum(wts); acc = 0; times = []
        for w in wts: times.append(t0 + 0.05 + (d - 0.15) * acc / tot); acc += w
        self.caps.append(dict(t0=t0, t1=t0 + d + 0.3, words=words, times=times, who=who, y=y, size=size))
        self.cursor = t0 + d + gap
        return t0, t0 + d

    def wait(self, s): self.cursor += s; return self.cursor

    # камера
    def shot(self, t, target="wide", z=None, dur=0.0, dy=0):
        if target == "wide": cx, cy, zz = 540, 960, 1.04
        elif target in self.actors:
            a = self.actors[target]; x, _, _, _ = a.body(t + dur)
            cx, cy, zz = x, a.ground - 420 * a.s + dy, 1.42
        elif isinstance(target, tuple) and len(target) == 2 and isinstance(target[0], str):
            a, b = self.actors[target[0]], self.actors[target[1]]
            cx, cy, zz = (a.body(t)[0] + b.body(t)[0]) / 2, max(a.ground, b.ground) - 380 * max(a.s, b.s) + dy, 1.12
        else:
            cx, cy, zz = target[0], target[1], 1.2
        self.cam.keys.append((t, cx, cy, z or zz, dur))
        if dur > 0: self.sfx(t, "swish", 0.25)

    def shake(self, t, amp=16): self.cam.shakes.append((t, amp))

    # графика
    def add(self, t0, t1, layer, fn): self.ov.append((t0, t1, layer, fn))

    def chalk(self, t0, text, x, y, size=72, dur=0.7, t1=999, color=(236, 240, 228)):
        im = P.chalk_text(text, size, color); self.sfx(t0, "scribble", 0.45)
        def fn(img, t, cam):
            k = seg(t, t0, t0 + dur); w = int(im.width * k)
            if w < 2: return
            c = im.crop((0, 0, w, im.height)); z = cam[2]; sx, sy = to_screen(cam, x, y)
            comp(img, scaled(c, z), sx, sy - im.height * z / 2)
        self.add(t0, t1, "back", fn)

    def prop(self, t0, t1, sprite, x, y, anim="pop", layer="back", s=1.0):
        """Реквизит в мире; (x, y) — середина низа. anim: pop | drop | none."""
        if anim == "drop": self.sfx(t0 + 0.32, "thump", 0.6)
        if anim == "pop": self.sfx(t0, "pop", 0.4)
        def fn(img, t, cam):
            z = cam[2]; k = s; dy = 0
            if anim == "pop": k *= back(seg(t, t0, t0 + 0.3))
            if anim == "drop":
                p = seg(t, t0, t0 + 0.32); dy = -(1 - p * p) * 1200
                k *= 1 + 0.08 * pulse(t, t0 + 0.32, t0 + 0.5)
            if t > t1 - 0.2: k *= 1 - eout(seg(t, t1 - 0.2, t1))
            if k <= 0.02: return
            im = scaled(sprite, k * z); sx, sy = to_screen(cam, x, y + dy)
            if layer != "screen":
                e = shadow_ellipse(int(im.width * 0.8), int(30 * z) + 4, 90)
                comp(img, e, sx - e.width / 2, to_screen(cam, x, y)[1] - e.height / 2)
            comp(img, im, sx - im.width / 2, sy - im.height)
        self.add(t0, t1, layer, fn)

    def card(self, t0, t1, shot, keys, marks=(), radius=40):
        """Кусок настоящего экрана на карточке. keys: [(t, (x0,y0,x1,y1) в пикселях скрина, cx, cy, ширина)].
        marks: [(t, (x0,y0,x1,y1), цвет)] — от руки обводим место на экране."""
        src = Image.open(shot if shot.startswith("/") else SHOTS + shot).convert("RGB")
        self.sfx(t0, "whoosh", 0.35)
        for tm, *_ in marks: self.sfx(tm, "marker", 0.4)
        def at(t):
            k = keys[0]
            for i, kk in enumerate(keys):
                if kk[0] <= t:
                    if i == 0: k = kk
                    else:
                        p = eio(seg(t, kk[0], kk[0] + 0.5)); a = keys[i - 1]
                        k = (t, tuple(lerp(u, v, p) for u, v in zip(a[1], kk[1])), lerp(a[2], kk[2], p), lerp(a[3], kk[3], p), lerp(a[4], kk[4], p))
            return k
        def fn(img, t, cam):
            _, box, cx, cy, wd = at(t)
            pin = back(seg(t, t0, t0 + 0.38), 1.4); pout = 1 - ease(seg(t, t1 - 0.25, t1))
            sc = pin * pout
            if sc < 0.02: return
            bw = box[2] - box[0]; bh = box[3] - box[1]; ww = wd * sc; hh = ww * bh / bw
            if ww < 4: return
            crop = src.resize((max(1, int(ww)), max(1, int(hh))), Image.BICUBIC, box=box)
            r = int(radius * sc); bez = int(12 * sc)
            card = Image.new("RGBA", (crop.width + 2 * bez, crop.height + 2 * bez), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
            d.rounded_rectangle([0, 0, card.width - 1, card.height - 1], radius=r + bez, fill=(14, 16, 18, 255))
            m = Image.new("L", crop.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, crop.width - 1, crop.height - 1], radius=r, fill=255)
            card.paste(crop, (bez, bez), m)
            for tm, mb, col in marks:
                if t < tm: continue
                q = eout(seg(t, tm, tm + 0.35))
                mx0 = bez + (mb[0] - box[0]) * ww / bw; my0 = bez + (mb[1] - box[1]) * hh / bh
                mx1 = bez + (mb[2] - box[0]) * ww / bw; my1 = bez + (mb[3] - box[1]) * hh / bh
                pad = 14 * sc; ex = [mx0 - pad, my0 - pad, mx1 + pad, my1 + pad]
                d.arc(ex, start=200, end=200 + 380 * q, fill=col + (255,), width=max(3, int(9 * sc)))
            sh = Image.new("RGBA", (card.width + 120, card.height + 120), (0, 0, 0, 0))
            ImageDraw.Draw(sh).rounded_rectangle([60, 76, 60 + card.width, 76 + card.height], radius=r + bez, fill=(0, 0, 0, 120))
            comp(img, sh.filter(ImageFilter.GaussianBlur(26)), cx - card.width / 2 - 60, cy - card.height / 2 - 60)
            comp(img, card, cx - card.width / 2, cy - card.height / 2)
        self.add(t0, t1, "screen", fn)

    def stamp(self, t0, t1, sprite, x, y, rot=-12, world=False):
        self.sfx(t0 + 0.12, "thump", 0.8); self.shake(t0 + 0.12, 18)
        def fn(img, t, cam):
            p = seg(t, t0, t0 + 0.13); k = lerp(2.4, 1.0, eout(p)) * (1 - 0.4 * ease(seg(t, t1 - 0.2, t1)))
            a = clamp(p * 1.6) * (1 - seg(t, t1 - 0.2, t1))
            im = fade(scaled(sprite, k * (cam[2] if world else 1), rot), a)
            px, py = to_screen(cam, x, y) if world else (x, y)
            comp(img, im, px - im.width / 2, py - im.height / 2)
        self.add(t0, t1, "front" if world else "screen", fn)

    def counter(self, t0, t1, a, b, x, y, size=150, suffix=" ₽", color=WHITE, dur=0.6, prefix="", sound=True, pop=True):
        if sound: self.sfx(t0, "tick", 0.3); self.sfx(t0 + dur, "ding", 0.4)
        def fn(img, t, cam):
            p = eout(seg(t, t0, t0 + dur)); v = int(round(lerp(a, b, p)))
            s = prefix + f"{v:,}".replace(",", " ") + suffix
            k = (back(seg(t, t0, t0 + 0.25)) if pop else 1) * (1 + 0.1 * pulse(t, t0 + dur, t0 + dur + 0.25)) * (1 - ease(seg(t, t1 - 0.2, t1)))
            if k < 0.02: return
            im = scaled(word_img(s, size, fill=color), k)
            comp(img, im, x - im.width / 2, y - im.height / 2)
        self.add(t0, t1, "screen", fn)

    def sticker(self, t0, t1, sprite, who, dx=0, dy=-40, wobble=True):
        self.sfx(t0, "pop", 0.35)
        def fn(img, t, cam):
            a = self.actors[who]
            if not hasattr(a, "last") or not a.visible(t): return
            hx, hy = a.head(); k = back(seg(t, t0, t0 + 0.25)) * (1 - ease(seg(t, t1 - 0.15, t1))) * a.last[2] / 0.75
            if k < 0.02: return
            im = scaled(sprite, k, 10 * math.sin(t * 7) if wobble else 0)
            comp(img, im, hx + dx * a.last[2] / 0.75 - im.width / 2, hy + dy * a.last[2] / 0.75 - im.height / 2)
        self.add(t0, t1, "screen", fn)

    def chat(self, t, side, text, typing=0.55, t1=None, y0=190):
        """Сообщение в чате поверх сцены. me — пишет сам зритель (справа, без аватара), l — герой, r — Кубыш.
        Сообщения встают стопкой сверху вниз."""
        b = P.bubble(text, side); av = P.avatar_max(92) if side == "l" else P.kubysh_avatar(92)
        if side == "me": typing = 0.0
        ty = t; tin = t + typing
        y = y0 + sum(c["h"] + 22 for c in self.chat_slots if c["t0"] <= t < c["t1"])
        slot = {"t0": t, "t1": t1 or 999, "h": b.height}; self.chat_slots.append(slot)
        self.sfx(t, "tick", 0.25); self.sfx(tin, "msg", 0.5)
        def fn(img, tt, cam):
            end = slot["t1"]; out = 1 - ease(seg(tt, end - 0.2, end))
            if out <= 0: return
            if side == "me":
                k = back(seg(tt, tin, tin + 0.28), 1.3)
                im = fade(scaled(b, 0.85 + 0.15 * k), clamp(k * 1.5) * out)
                comp(img, im, W - 60 - im.width, y + (1 - k) * 24); return
            x = 40 if side == "l" else W - 40 - b.width - 110
            ax = x if side == "l" else W - 40 - 92
            bx = x + 110 if side == "l" else x
            if tt < tin:
                k = back(seg(tt, ty, ty + 0.2)); dots = scaled(P.typing_dots(tt * 1.6), k)
                comp(img, fade(av, out), ax, y); comp(img, fade(dots, out), bx, y + 4)
                return
            k = back(seg(tt, tin, tin + 0.28), 1.3)
            im = fade(scaled(b, 0.85 + 0.15 * k), clamp(k * 1.5) * out)
            comp(img, fade(av, out), ax, y); comp(img, im, bx, y + (1 - k) * 24)
        self.add(t, 999, "screen", fn)

    def chat_clear(self, t):
        for c in self.chat_slots:
            if c["t1"] > t: c["t1"] = t + 0.2

    def notif(self, t0, t1, title, body, **kw):
        im = P.notification(title, body, **kw); self.sfx(t0, "ding", 0.5)
        def fn(img, t, cam):
            p = back(seg(t, t0, t0 + 0.35), 1.2) * (1 - eio(seg(t, t1 - 0.3, t1)))
            comp(img, im, (W - im.width) / 2, lerp(-240, 170, p))
        self.add(t0, t1, "screen", fn)

    def balance(self, steps, t1, x=540, y=1170, size=120):
        """Баланс, который меняется ступеньками: steps = [(t, сумма)], каждая ступень — короткий пересчет."""
        for i, (t, v) in enumerate(steps):
            if i == 0: continue
            nt = steps[i + 1][0] if i + 1 < len(steps) else t1
            self.counter(t, nt, steps[i - 1][1], v, x, y, size=size, dur=0.3, sound=False, pop=(i == 1))

    def pushes(self, items, t1, y0=150, scale=0.86, **kw):
        """Каскад пушей: items = [(t, title, body)], новый въезжает сверху и сдвигает старые вниз, видно до 4."""
        ims = [scaled(P.notification(ti, bo, **kw), scale) for _, ti, bo in items]
        step = ims[0].height + 14
        for t, _, _ in items: self.sfx(t, "ding", 0.35)
        def fn(img, t, cam):
            out = 1 - eio(seg(t, t1 - 0.3, t1))
            shown = [i for i, it in enumerate(items) if it[0] <= t]
            for rank, i in enumerate(reversed(shown)):
                if rank > 3: break
                p = back(seg(t, items[i][0], items[i][0] + 0.3), 1.2)
                slot = rank - 1 + p if rank == 0 else rank
                if rank > 0:  # сдвиг вниз, пока въезжает новый
                    nt = items[shown[-1]][0]; slot = rank - 1 + back(seg(t, nt, nt + 0.3), 1.2)
                y = y0 + slot * step if rank > 0 else lerp(-step, y0, p)
                comp(img, ims[i], (W - ims[i].width) / 2, y + (1 - out) * -400)
        self.add(items[0][0], t1, "screen", fn)

    def title(self, t0, t1, lines, sub=None, bg=(14, 22, 18)):
        self.sfx(t0, "boom", 0.7)
        def fn(img, t, cam):
            a = ease(seg(t, t0, t0 + 0.2)) * (1 - ease(seg(t, t1 - 0.2, t1)))
            ov = Image.new("RGBA", (W, H), bg + (int(215 * a),)); img.alpha_composite(ov)
            y = 700
            for i, (s, col) in enumerate(lines):
                k = back(seg(t, t0 + 0.08 * i, t0 + 0.08 * i + 0.3))
                im = fade(scaled(word_img(s, 120, fill=col), k), a); comp(img, im, (W - im.width) / 2, y); y += 150
            for j, line in enumerate([sub] if isinstance(sub, str) else (sub or [])):
                im = fade(word_img(line, 54, fill=(220, 230, 224)), a * seg(t, t0 + 0.3 + 0.1 * j, t0 + 0.5 + 0.1 * j)); comp(img, im, (W - im.width) / 2, y + 20 + j * 80)
        self.add(t0, t1, "screen", fn)

    def coins(self, t0, n=26, dur=1.6):
        rnd = random.Random(int(t0 * 100)); parts = [(rnd.uniform(60, 1020), rnd.uniform(-400, -60), rnd.uniform(0.25, 0.45), rnd.uniform(0, 6), rnd.uniform(500, 900)) for _ in range(n)]
        self.sfx(t0, "kaching", 0.6)
        def fn(img, t, cam):
            d = t - t0
            for x, y, s, ph, vy in parts:
                yy = y + vy * d + 500 * d * d
                if yy > H + 100: continue
                cs = coin_sprite(flip=math.cos(ph + d * 9)); cs = cs.resize((max(1, int(cs.width * s)), max(1, int(cs.height * s))), Image.BILINEAR)
                comp(img, cs, x - cs.width / 2, yy)
        self.add(t0, t0 + dur, "screen", fn)

    def pill(self, t0, t1, text, x, y, size=46, bg=(255, 255, 255), fg=INK):
        f = P.font(size); w = int(f.getlength(text)) + 60; h = int(size * 1.7)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=bg + (240,)); d.text((w // 2, h // 2), text, font=f, fill=fg + (255,), anchor="mm")
        def fn(img, t, cam):
            k = back(seg(t, t0, t0 + 0.3)) * (1 - ease(seg(t, t1 - 0.2, t1)))
            if k > 0.02: s = scaled(im, k); comp(img, s, x - s.width / 2, y - s.height / 2)
        self.add(t0, t1, "screen", fn)

    def clip(self, t0, t1, path, label, src_t0=0.0, speed=1.0):
        """Видео вместо декорации на [t0, t1): клип Higgsfield (mp4) или заглушка с описанием, если файла еще нет.
        speed < 0 — перемотка назад от src_t0."""
        self.clips.append(dict(t0=t0, t1=t1, path=path, label=label, src=src_t0, speed=speed, frames=None))

    def _clip_frame(self, c, t):
        if c["frames"] is None:
            if c["path"] and c["path"].lower().endswith(".png") and os.path.exists(c["path"]):
                c["frames"] = [Image.open(c["path"]).convert("RGB").resize((W, H), Image.LANCZOS)]
            elif c["path"] and os.path.exists(c["path"]):
                import hashlib
                d = os.path.join(HERE, ".cache", "clips", hashlib.md5(c["path"].encode()).hexdigest()[:10])
                if not os.path.isdir(d) or not os.listdir(d):
                    os.makedirs(d, exist_ok=True)
                    subprocess.run([os.path.join(HERE, "vframes"), c["path"], d, str(FPS), str(W), str(H)], check=True, capture_output=True)
                c["frames"] = sorted(os.path.join(d, f) for f in os.listdir(d))
            else:
                ph = Image.new("RGB", (W, H)); d = ImageDraw.Draw(ph); P.vgrad(d, (0, 0, W, H), (58, 66, 80), (28, 32, 40))
                d.rounded_rectangle([60, 300, W - 60, 900], radius=40, outline=(120, 130, 150), width=4)
                d.text((W // 2, 380), "ЗАГЛУШКА · клип Higgsfield", font=P.font(40, "SemiBold"), fill=(170, 180, 200), anchor="mm")
                y = 470
                words = c["label"].split(); line = ""
                for wd in words:
                    if P.font(52).getlength(line + " " + wd) > W - 200: d.text((W // 2, y), line.strip(), font=P.font(52), fill=(240, 240, 245), anchor="mm"); y += 70; line = ""
                    line += " " + wd
                d.text((W // 2, y), line.strip(), font=P.font(52), fill=(240, 240, 245), anchor="mm")
                c["frames"] = [ph]
        fr = c["frames"]; i = min(len(fr) - 1, max(0, int((c["src"] + (t - c["t0"]) * c.get("speed", 1.0)) * FPS)))
        f = fr[i]
        return f if isinstance(f, Image.Image) else Image.open(f).convert("RGB")

    # ---------- кадр ----------
    def background(self, t, cam):
        cx, cy, z, dx, dy = cam
        for c in self.clips:
            if c["t0"] <= t < c["t1"]:
                f = self._clip_frame(c, t)
                box = [cx + (0 - 540 - dx) / z, cy + (0 - 960 - dy) / z, cx + (W - 540 - dx) / z, cy + (H - 960 - dy) / z]
                return f.resize((W, H), Image.BILINEAR, box=box).convert("RGBA")
        box = [(cx + (0 - 540 - dx) / z) * P.SC, (cy + (0 - 960 - dy) / z) * P.SC, (cx + (W - 540 - dx) / z) * P.SC, (cy + (H - 960 - dy) / z) * P.SC]
        cur, prev, fd, ts = self.sets[0][1], None, 0, 0
        for tt, nm, f in self.sets:
            if tt <= t: prev, cur, fd, ts = cur, nm, f, tt
        bg = P.get_set(cur).resize((W, H), Image.BILINEAR, box=box)
        if prev and fd > 0 and t < ts + fd:
            bp = P.get_set(prev).resize((W, H), Image.BILINEAR, box=box); bg = Image.blend(bp, bg, seg(t, ts, ts + fd))
        return bg.convert("RGBA")

    def captions(self, img, t):
        for i, c in enumerate(self.caps):
            nxt = self.caps[i + 1]["t0"] if i + 1 < len(self.caps) else 999
            if not (c["t0"] <= t < min(c["t1"], nxt)): continue
            size = c["size"]; hi = {"kubysh": YEL, "dush": PINK}.get(c["who"], (150, 215, 255))
            ims = []
            for w, tw in zip(c["words"], c["times"]):
                emph = w.startswith("*") or w.endswith("*") or "*" in w
                clean = w.replace("*", "")
                ims.append((word_img(clean, int(size * (1.1 if emph else 1)), fill=hi if emph else WHITE), tw))
            sp = int(size * 0.28); lines = [[]]; cw = 0
            for im, tw in ims:
                if lines[-1] and cw + sp + im.width > 940: lines.append([]); cw = 0
                cw += (sp if lines[-1] else 0) + im.width; lines[-1].append((im, tw))
            y0 = c["y"] if c["y"] is not None else 1290
            lh = int(size * 1.25); out = seg(t, min(c["t1"], nxt) - 0.12, min(c["t1"], nxt))
            av = getattr(self, "avatars", {}).get(c["who"])
            if av is not None and lines and t >= c["times"][0]:   # портрет говорящего слева от первой строки
                w0 = sum(im.width for im, _ in lines[0]) + sp * (len(lines[0]) - 1); x0 = (W - w0) / 2 - 20
                k = back(seg(t, c["t0"], c["t0"] + 0.2), 1.6)
                a = fade(scaled(av, max(0.05, k)), 1 - out)
                comp(img, a, max(10, x0 - a.width - 6), y0 + (int(size * 1.1) - a.height) / 2 + 10)
            for li, ln in enumerate(lines):
                width = sum(im.width for im, _ in ln) + sp * (len(ln) - 1); x = (W - width) / 2 - 20
                for im, tw in ln:
                    if t >= tw:
                        k = back(seg(t, tw, tw + 0.16), 2.2)
                        s = scaled(im, max(0.05, k)); s = fade(s, clamp(seg(t, tw, tw + 0.08)) * (1 - out))
                        comp(img, s, x + (im.width - s.width) / 2, y0 + li * lh + (im.height - s.height) / 2)
                    x += im.width + sp

    def frame(self, t):
        cam = self.cam.state(t)
        img = self.background(t, cam)
        for t0, t1, layer, fn in self.ov:
            if layer == "back" and t0 <= t < t1: fn(img, t, cam)
        for a in self.order: a.draw(img, t, cam)
        for t0, t1, layer, fn in self.ov:
            if layer == "front" and t0 <= t < t1: fn(img, t, cam)
        for t0, t1, layer, fn in self.ov:
            if layer == "screen" and t0 <= t < t1: fn(img, t, cam)
        self.captions(img, t)
        return img

    def render(self, preview=None):
        out_dir = os.path.join(OUT_KSY if self.name.startswith("K") else OUT_ROOT, self.name); os.makedirs(out_dir, exist_ok=True)
        N = int(self.dur * FPS); dt = 1 / FPS
        enc = None
        if preview is None:
            silent = os.path.join(out_dir, "_video.mp4")
            enc = subprocess.Popen([ENC, silent, str(W), str(H), str(FPS)], stdin=subprocess.PIPE)
        want = sorted(int(p * FPS) for p in (preview or []))
        cover = int(self.cover_t * FPS)
        for i in range(N):
            t = i * dt; cam = self.cam.state(t)
            for a in self.order: a.update(t, dt, self.order, cam)
            if enc is None and i not in want: continue
            img = self.frame(t)
            if enc is not None:
                enc.stdin.write(img.tobytes("raw", "BGRA"))
                if i == cover: img.convert("RGB").save(os.path.join(out_dir, "Обложка.png"))
            else:
                img.convert("RGB").save(os.path.join(out_dir, f"_preview_{t:05.2f}.png"))
            if preview is not None and i >= want[-1]: break
        if enc is None: return out_dir
        enc.stdin.close(); enc.wait()
        soft = {"tick": 0.5, "pop": 0.6, "msg": 0.6, "ding": 0.6, "marker": 0.5, "clink": 0.6, "swish": 0.5, "hop": 0.6, "whoosh": 0.7}
        ev = [(t, smp, getattr(self, "vgain", 1.0)) for t, smp in self.voice] + list(getattr(self, "extra", [])) + [(t, audio.sfx(n), g * soft.get(n, 1.0)) for t, n, g in self.sfx_ev]
        wav = os.path.join(out_dir, "_mix.wav"); audio.mix(ev, self.dur, wav)
        label = {"yandex": "Яндекс", "edge": "Edge"}.get(getattr(self, "cast", ""), "")
        final = os.path.join(out_dir, f"{self.name}{'_' + label if label else ''}.mp4"); audio.mux(silent, wav, final)
        for f in ("_video.mp4", "_mix.wav", "_mix.m4a"):
            try: os.remove(os.path.join(out_dir, f))
            except OSError: pass
        return final


def load(path, cast="yandex"):
    """cast: yandex (SpeechKit) | edge (бесплатные многоязычные). Голоса синтезируются при сборке сценария."""
    audio.CAST = audio.CASTS[cast]
    spec = importlib.util.spec_from_file_location("ep", path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    ep = m.build(); ep.cast = cast; return ep


if __name__ == "__main__":
    prev = None
    if "--preview" in sys.argv: prev = [float(v) for v in sys.argv[sys.argv.index("--preview") + 1].split(",")]
    casts = sys.argv[sys.argv.index("--cast") + 1].split(",") if "--cast" in sys.argv else ["yandex"]
    for c in casts:
        print(load(sys.argv[1], c).render(prev))

"""Анимированные карточки 4:5 (1080x1350) для поста о релизе: Телеграм-альбом и карусель Инстаграма.

Стиль карточек стора: мятный фон, Montserrat, телефон со скриншотом. Сюжет каждой карточки:
жизненный случай (заголовок виден с первого кадра — он же превью) → телефон → главное место экрана
выезжает крупным планом → ответ Кубыша. Кодирование в MP4 без ffmpeg: mp4enc.swift (AVFoundation).

Запуск: python3 release_anim.py --config anim_release_1.7.json [--only 02_name] [--posters]
"""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from card import F
from social import _bg, _rich, GREEN, INK, SUB

W, H, FPS = 1080, 1350, 30
MINT = (232, 245, 238)
X0 = 72


def font(weight, size):
    return ImageFont.truetype(F + f"Montserrat-{weight}.ttf", size)


def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def ease_back(t, s=1.5):
    t = min(max(t, 0.0), 1.0) - 1
    return t * t * ((s + 1) * t + s) + 1


def span(t, a, b):
    return min(max((t - a) / (b - a), 0.0), 1.0)


def fade(layer, a):
    if a >= 0.999:
        return layer
    out = layer.copy()
    out.putalpha(layer.getchannel('A').point(lambda v: int(v * a)))
    return out


def paste(canvas, img, x, y):
    """alpha_composite с обрезкой по краям холста."""
    x, y = int(round(x)), int(round(y))
    l, t = max(0, -x), max(0, -y)
    r, b = min(img.width, W - x), min(img.height, H - y)
    if r <= l or b <= t:
        return
    canvas.alpha_composite(img, dest=(x + l, y + t), source=(l, t, r, b))


def rounded(img, radius):
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=radius, fill=255)
    out = img.convert('RGBA')
    out.putalpha(mask)
    return out


def shadow(w, h, radius, blur=34, alpha=80, spread=0):
    pad = blur * 2
    sh = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad - spread, pad - spread, pad + w + spread, pad + h + spread],
                                         radius=radius, fill=(20, 60, 40, alpha))
    return sh.filter(ImageFilter.GaussianBlur(blur)), pad


def text_layer(lines, size, color, weight="Bold", line_h=None):
    f = font(weight, size)
    line_h = line_h or int(size * 1.17)
    layer = Image.new('RGBA', (W - 2 * X0, line_h * len(lines) + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, l in enumerate(lines):
        d.text((0, i * line_h), l, font=f, fill=color)
    return layer


def rich_layer(segments, size=34, line_h=46):
    layer = Image.new('RGBA', (W - 2 * X0, line_h * 5), (0, 0, 0, 0))
    y = _rich(ImageDraw.Draw(layer), segments, 0, 0, W - 2 * X0, size, line_h)
    return layer.crop((0, 0, layer.width, y + 8)), y


def pill(text, fill=GREEN, color=(255, 255, 255), size=28):
    f = font("Bold", size)
    tw = int(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(text, font=f))
    p = Image.new('RGBA', (tw + 44, size + 26), (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    d.rounded_rectangle([0, 0, p.width - 1, p.height - 1], radius=p.height // 2, fill=fill)
    d.text((22, 9), text, font=f, fill=color)
    return p


class Phone:
    def __init__(self, shot_path, width=540):
        shot = Image.open(shot_path).convert('RGB')
        self.src_w = shot.width
        self.k = width / shot.width
        self.pw, self.ph = width, int(shot.height * self.k)
        self.bez = 15
        r = int(width * 0.135)
        screen = rounded(shot.resize((self.pw, self.ph), Image.LANCZOS), r)
        body = Image.new('RGBA', (self.pw + 2 * self.bez, self.ph + 2 * self.bez), (0, 0, 0, 0))
        ImageDraw.Draw(body).rounded_rectangle([0, 0, body.width - 1, body.height - 1], radius=r + self.bez,
                                               fill=(18, 20, 22, 255))
        body.alpha_composite(screen, (self.bez, self.bez))
        self.img = body
        self.shadow, self.spad = shadow(body.width, body.height, r + self.bez, blur=40, alpha=70)

    def screen_rect(self, x, y, box):
        """Прямоугольник box (пиксели скриншота) на холсте при телефоне в точке (x, y)."""
        k, b = self.k, self.bez
        return (x + b + box[0] * k, y + b + box[1] * k, x + b + box[2] * k, y + b + box[3] * k)


class ShotCard:
    """Карточка: случай → телефон → крупный план → ответ."""

    def __init__(self, cfg, shots_dir):
        p = lambda s: s if s.startswith('/') else os.path.join(shots_dir, s)
        self.bg = _bg().convert('RGBA')
        self.tag = pill(cfg["tag"])
        self.hook = text_layer(cfg["hook"], cfg.get("hook_size", 62), INK, line_h=int(cfg.get("hook_size", 62) * 1.16))
        self.answer, ans_h = rich_layer([tuple(s) for s in cfg["answer"]])
        self.hook_y = 150
        self.ans_y = self.hook_y + self.hook.height + 14
        self.phone = Phone(p(cfg["shot"]), cfg.get("phone_w", 540))
        self.ph_x = (W - self.phone.img.width) // 2
        self.ph_y = self.ans_y + ans_h + 50
        self.anchor = cfg.get("anchor", cfg["box"])
        pop_src = Image.open(p(cfg.get("pop_shot", cfg["shot"]))).convert('RGB').crop(tuple(cfg["box"]))
        self.pop_w = cfg.get("pop_w", W - 2 * X0)
        k = self.pop_w / pop_src.width
        self.pop_h = int(pop_src.height * k)
        self.pop_r = 34
        self.pop_full = rounded(pop_src.resize((self.pop_w, self.pop_h), Image.LANCZOS), self.pop_r)
        self.pop_src = rounded(pop_src, int(self.pop_r / k))
        self.pop_shadow, self.pop_pad = shadow(self.pop_w, self.pop_h, self.pop_r, blur=36, alpha=110)
        cy = cfg.get("pop_cy", (self.ph_y + H) // 2 + 30)
        self.pop_target = (X0 + (W - 2 * X0 - self.pop_w) // 2, int(cy - self.pop_h / 2))
        self.badge = cfg.get("badge")
        if self.badge:
            bw, bh = W - 2 * X0, 128
            base = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
            d = ImageDraw.Draw(base)
            d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=30, fill=(255, 255, 255, 245))
            d.text((32, 24), self.badge["label"], font=font("Bold", 34), fill=INK)
            d.text((32, 70), self.badge["note"], font=font("Medium", 28), fill=SUB)
            self.badge_img = base
            self.badge_sh, self.badge_pad = shadow(bw, bh, 30, blur=26, alpha=70)
            self.badge_y = self.pop_target[1] + self.pop_h + 30

    def frame(self, t):
        c = self.bg.copy()
        paste(c, self.tag, X0, 66)
        paste(c, self.hook, X0, self.hook_y)
        # Телефон выезжает снизу.
        a = ease_out(span(t, 0.15, 1.0))
        py = self.ph_y + (1 - a) * 300
        if a > 0:
            paste(c, fade(self.phone.shadow, a), self.ph_x - self.phone.spad + 10, py - self.phone.spad + 34)
            paste(c, fade(self.phone.img, a), self.ph_x, py)
        ax0, ay0, ax1, ay1 = self.phone.screen_rect(self.ph_x, py, self.anchor)
        # Касание по нужному месту экрана.
        tp = span(t, 1.05, 1.5)
        if 0 < tp < 1:
            ring = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
            rr = 20 + 60 * tp
            ImageDraw.Draw(ring).ellipse([80 - rr, 80 - rr, 80 + rr, 80 + rr], fill=(255, 255, 255, int(150 * (1 - tp))))
            paste(c, ring, (ax0 + ax1) / 2 - 80, (ay0 + ay1) / 2 - 80)
        hl = span(t, 1.15, 1.45) * (1 - span(t, 2.0, 2.3))
        if hl > 0:
            box = Image.new('RGBA', (int(ax1 - ax0) + 16, int(ay1 - ay0) + 16), (0, 0, 0, 0))
            ImageDraw.Draw(box).rounded_rectangle([2, 2, box.width - 3, box.height - 3], radius=18,
                                                  outline=(46, 190, 120, int(255 * hl)), width=5)
            paste(c, box, ax0 - 8, ay0 - 8)
        # Крупный план: из места на экране в центр карточки, телефон приглушается.
        m = span(t, 1.45, 2.2)
        if m > 0:
            dim = Image.new('RGBA', (W, H), MINT + (int(120 * ease_out(m)),))
            paste(c, dim.crop((0, int(self.ph_y - 40), W, H)), 0, int(self.ph_y - 40))
            e = ease_back(m, 1.25)
            tx, ty = self.pop_target
            x0 = ax0 + (tx - ax0) * e
            y0 = ay0 + (ty - ay0) * e
            w = max(8, (ax1 - ax0) + (self.pop_w - (ax1 - ax0)) * e)
            h = max(8, (ay1 - ay0) + (self.pop_h - (ay1 - ay0)) * e)
            if t > 2.25:
                y0 += math.sin((t - 2.25) / 2.6 * 2 * math.pi) * 5
            sh_k = w / self.pop_w
            shw = self.pop_shadow.resize((int(self.pop_shadow.width * sh_k), int(self.pop_shadow.height * sh_k)))
            paste(c, fade(shw, min(1, m * 1.6)), x0 - self.pop_pad * sh_k, y0 - self.pop_pad * sh_k + 22)
            img = self.pop_full if abs(w - self.pop_w) < 1 and abs(h - self.pop_h) < 1 else \
                self.pop_src.resize((int(w), int(h)), Image.BILINEAR)
            paste(c, fade(img, min(1, 0.35 + m)), x0, y0)
            rp = span(t, 2.15, 2.75)
            if 0 < rp < 1:
                g = int(30 * rp)
                ring = Image.new('RGBA', (self.pop_w + 2 * g + 8, self.pop_h + 2 * g + 8), (0, 0, 0, 0))
                ImageDraw.Draw(ring).rounded_rectangle([4, 4, ring.width - 5, ring.height - 5], radius=self.pop_r + g,
                                                       outline=(46, 190, 120, int(220 * (1 - rp))), width=4)
                paste(c, ring, x0 - g - 4, y0 - g - 4)
        if self.badge:
            b = ease_out(span(t, 2.4, 2.9))
            if b > 0:
                by = self.badge_y + (1 - b) * 40
                paste(c, fade(self.badge_sh, b), X0 - self.badge_pad, by - self.badge_pad + 14)
                img = self.badge_img.copy()
                k = ease_out(span(t, 2.7, 3.7))
                v = self.badge["from"] + (self.badge["to"] - self.badge["from"]) * k
                num = f"{int(round(v)):,}".replace(",", " ") + self.badge.get("suffix", "")
                f = font("Bold", 60)
                d = ImageDraw.Draw(img)
                d.text((img.width - 32 - d.textlength(num, font=f), 30), num, font=f, fill=GREEN)
                paste(c, fade(img, b), X0, by)
        an = span(t, 2.2, 2.8)
        if an > 0:
            paste(c, fade(self.answer, ease_out(an)), X0, self.ans_y + (1 - ease_out(an)) * 18)
        return c


class FixesCard:
    """Карточка «Починили»: пункты появляются по одному с галочкой."""

    def __init__(self, cfg, _):
        self.bg = _bg().convert('RGBA')
        self.tag = pill(cfg["tag"])
        self.hook = text_layer(cfg["hook"], 62, INK, line_h=72)
        self.items = []
        f, fv = font("SemiBold", 36), font("Bold", 24)
        maxw = W - 2 * X0 - 100 - 120
        probe = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        for text, ver in cfg["items"]:
            words, lines = text.split(), [""]
            for w_ in words:
                cand = (lines[-1] + " " + w_).strip()
                if probe.textlength(cand, font=f) > maxw and lines[-1]:
                    lines.append(w_)
                else:
                    lines[-1] = cand
            h = 30 + 46 * len(lines) + 30
            row = Image.new('RGBA', (W - 2 * X0, h), (0, 0, 0, 0))
            d = ImageDraw.Draw(row)
            d.rounded_rectangle([0, 0, row.width - 1, h - 1], radius=28, fill=(255, 255, 255, 235))
            for i, l in enumerate(lines):
                d.text((100, 30 + i * 46), l, font=f, fill=INK)
            vt = pill(ver, fill=(226, 242, 233), color=GREEN, size=24)
            row.alpha_composite(vt, (row.width - vt.width - 24, (h - vt.height) // 2))
            self.items.append((row, h))
        self.start_y = 150 + self.hook.height + 40
        check = Image.new('RGBA', (56, 56), (0, 0, 0, 0))
        d = ImageDraw.Draw(check)
        d.ellipse([0, 0, 55, 55], fill=GREEN)
        d.line([(15, 29), (24, 38), (41, 19)], fill=(255, 255, 255), width=6, joint="curve")
        self.check = check

    def frame(self, t):
        c = self.bg.copy()
        paste(c, self.tag, X0, 66)
        paste(c, self.hook, X0, 150)
        y = self.start_y
        for i, (row, h) in enumerate(self.items):
            a = span(t, 0.5 + i * 0.42, 0.95 + i * 0.42)
            if a > 0:
                e = ease_out(a)
                paste(c, fade(row, e), X0 + (1 - e) * 120, y)
                s = ease_back(span(t, 0.75 + i * 0.42, 1.1 + i * 0.42), 2.2)
                if s > 0:
                    k = max(1, int(56 * s))
                    ck = self.check.resize((k, k), Image.BILINEAR)
                    paste(c, ck, X0 + (1 - e) * 120 + 26 + (56 - k) / 2, y + (h - k) / 2)
            y += h + 18
        return c


class CoverCard:
    """Обложка: иконка, версии прокручиваются 1.6.1 → 1.7, фичи появляются плашками."""

    def __init__(self, cfg, _):
        self.bg = _bg().convert('RGBA')
        icon = Image.open(cfg["icon"]).convert('RGB').resize((200, 200), Image.LANCZOS)
        self.icon = rounded(icon, 46)
        self.icon_sh, self.icon_pad = shadow(200, 200, 46, blur=28, alpha=90)
        self.kicker = text_layer([cfg["kicker"]], 44, GREEN)
        self.versions = [text_layer([v], 190, INK, line_h=210) for v in cfg["versions"]]
        self.sub = text_layer(cfg["sub"], 46, SUB, weight="SemiBold", line_h=58)
        self.chips = [pill(ch, fill=(255, 255, 255), color=INK, size=34) for ch in cfg["chips"]]

    def frame(self, t):
        c = self.bg.copy()
        paste(c, self.icon_sh, X0 - self.icon_pad, 170 - self.icon_pad + 16)
        paste(c, self.icon, X0, 170)
        paste(c, self.kicker, X0, 420)
        vy = 490
        n = len(self.versions)
        step = 0.42
        pos = min(max((t - 0.6) / step, 0), n - 1)
        i = int(pos)
        frac = ease_out(pos - i) if i < n - 1 else 0
        window = Image.new('RGBA', (W, 220), (0, 0, 0, 0))
        window.alpha_composite(fade(self.versions[i], 1 - frac), (X0, int(-frac * 200)))
        if i < n - 1 and frac > 0:
            window.alpha_composite(fade(self.versions[i + 1], frac), (X0, int((1 - frac) * 200)))
        paste(c, window, 0, vy)
        a = ease_out(span(t, 2.6, 3.2))
        if a > 0:
            paste(c, fade(self.sub, a), X0, 750 + (1 - a) * 20)
        x, y = X0, 930
        for j, ch in enumerate(self.chips):
            if x + ch.width > W - X0:
                x, y = X0, y + ch.height + 18
            e = ease_back(span(t, 3.0 + j * 0.16, 3.4 + j * 0.16), 1.8)
            if e > 0:
                k = max(0.01, e)
                img = ch.resize((max(1, int(ch.width * k)), max(1, int(ch.height * k))), Image.BILINEAR)
                paste(c, fade(img, min(1, e)), x + ch.width * (1 - k) / 2, y + ch.height * (1 - k) / 2)
            x += ch.width + 16
        return c


class EndCard:
    """Финал: иконка и призыв обновиться."""

    def __init__(self, cfg, _):
        self.bg = _bg().convert('RGBA')
        icon = Image.open(cfg["icon"]).convert('RGB').resize((280, 280), Image.LANCZOS)
        self.icon = rounded(icon, 64)
        self.icon_sh, self.icon_pad = shadow(280, 280, 64, blur=34, alpha=100)
        self.title = text_layer(cfg["title"], 84, INK, line_h=96)
        self.sub = text_layer(cfg["sub"], 42, SUB, weight="SemiBold", line_h=56)
        self.foot = pill(cfg["foot"], size=32)

    def frame(self, t):
        c = self.bg.copy()
        e = ease_back(span(t, 0.1, 0.7), 1.8)
        if e > 0:
            k = max(0.01, e)
            ic = self.icon.resize((max(1, int(280 * k)), max(1, int(280 * k))), Image.BILINEAR)
            paste(c, fade(self.icon_sh, min(1, e)), (W - 280) / 2 - self.icon_pad, 230 - self.icon_pad + 20)
            paste(c, ic, (W - 280 * k) / 2, 230 + 280 * (1 - k) / 2)
        a = ease_out(span(t, 0.6, 1.2))
        if a > 0:
            paste(c, fade(self.title, a), X0, 590 + (1 - a) * 24)
        b = ease_out(span(t, 1.1, 1.7))
        if b > 0:
            paste(c, fade(self.sub, b), X0, 600 + self.title.height + 10 + (1 - b) * 20)
        f = ease_out(span(t, 1.6, 2.2))
        if f > 0:
            paste(c, fade(self.foot, f), X0, 1010)
        return c


KINDS = {"shot": ShotCard, "fixes": FixesCard, "cover": CoverCard, "end": EndCard}


def render(card, out_mp4, seconds, encoder):
    p = subprocess.Popen([encoder, out_mp4, str(W), str(H), str(FPS)], stdin=subprocess.PIPE)
    for i in range(int(seconds * FPS)):
        p.stdin.write(card.frame(i / FPS).tobytes('raw', 'BGRA'))
    p.stdin.close()
    p.wait()


def render_reel(cfg, out_mp4, encoder):
    """Reels 9:16: те же сцены подряд, карточка 4:5 на мятном поле, сверху полоски прогресса как в сторис."""
    RW, RH, top = 1080, 1920, 190
    cards = [(KINDS[s["kind"]](s, cfg["shots_dir"]), s.get("reel_seconds", 4.4)) for s in cfg["cards"]]
    total = sum(d for _, d in cards)
    field = Image.new('RGBA', (RW, RH), (250, 250, 246, 255))
    ImageDraw.Draw(field).rectangle([0, 0, RW, top], fill=MINT + (255,))
    n, gap, x0 = len(cards), 10, 48
    seg = (RW - 2 * x0 - gap * (n - 1)) / n
    p = subprocess.Popen([encoder, out_mp4, str(RW), str(RH), str(FPS)], stdin=subprocess.PIPE)
    start = 0.0
    for i, (card, dur) in enumerate(cards):
        for f in range(int(dur * FPS)):
            t = f / FPS
            frame = field.copy()
            frame.alpha_composite(card.frame(t), (0, top))
            d = ImageDraw.Draw(frame)
            for j in range(n):
                sx = x0 + j * (seg + gap)
                d.rounded_rectangle([sx, 96, sx + seg, 104], radius=4, fill=(198, 224, 208, 255))
                k = 1 if j < i else (t / dur if j == i else 0)
                if k > 0:
                    d.rounded_rectangle([sx, 96, sx + seg * k, 104], radius=4, fill=GREEN)
            p.stdin.write(frame.tobytes('raw', 'BGRA'))
        start += dur
    p.stdin.close()
    p.wait()
    print(f"reel {total:.1f}s")


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[sys.argv.index("--config") + 1]))
    if "--reel" in sys.argv:
        enc = cfg["encoder"] if os.path.isabs(cfg["encoder"]) else \
            os.path.join(os.path.dirname(os.path.abspath(__file__)), cfg["encoder"])
        render_reel(cfg, sys.argv[sys.argv.index("--reel") + 1], enc)
        sys.exit(0)
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    os.makedirs(cfg["out_dir"], exist_ok=True)
    for s in cfg["cards"]:
        if only and s["name"] != only:
            continue
        card = KINDS[s["kind"]](s, cfg["shots_dir"])
        dur = s.get("seconds", cfg.get("seconds", 6))
        poster = card.frame(dur - 0.1).convert('RGB')
        poster.save(os.path.join(cfg["out_dir"], s["name"] + ".png"))
        if "--posters" not in sys.argv:
            enc = cfg["encoder"] if os.path.isabs(cfg["encoder"]) else \
                os.path.join(os.path.dirname(os.path.abspath(__file__)), cfg["encoder"])
            render(card, os.path.join(cfg["out_dir"], s["name"] + ".mp4"), dur, enc)
        print("ok", s["name"])

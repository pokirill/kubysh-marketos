"""Слайды для Инстаграма/Тредса 1080x1350 (4:5) в стиле карточек стора 1.6.3.
hook: крупная фраза на мятном фоне, без картинок от ГПТ.
phone: верх карточки стора (заголовок + верх экрана), кадрированный в 4:5.
Запуск: python3 social.py --config posts_X.json
"""
import sys, json, os, tempfile
from PIL import Image, ImageDraw, ImageFont
from card import F

W, H = 1080, 1350
GREEN = (30, 130, 88); INK = (16, 28, 22); SUB = (78, 98, 88)

def _bg():
    bg = Image.new('RGB', (W, H)); d = ImageDraw.Draw(bg)
    top = (232, 245, 238); bot = (250, 250, 246)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    return bg

def _rich(d, segments, x, y, maxw, size, line_h):
    reg = ImageFont.truetype(F + "Montserrat-Medium.ttf", size)
    hi = ImageFont.truetype(F + "Montserrat-Bold.ttf", size)
    words = [(w, h) for t, h in segments for w in t.split()]
    space = d.textlength(" ", font=reg); lines = [[]]; cx = 0
    for w, h in words:
        wl = d.textlength(w, font=hi if h else reg)
        if lines[-1] and cx + space + wl > maxw: lines.append([]); cx = 0
        cx += (space if lines[-1] else 0) + wl; lines[-1].append((w, h))
    for ln in lines:
        cx = x
        for i, (w, h) in enumerate(ln):
            if i: cx += space
            f = hi if h else reg
            d.text((cx, y), w, font=f, fill=GREEN if h else SUB); cx += d.textlength(w, font=f)
        y += line_h
    return y

def hook(out, lines, segments=None, kicker=None):
    img = _bg(); d = ImageDraw.Draw(img)
    size = 104
    while True:
        bold = ImageFont.truetype(F + "Montserrat-Bold.ttf", size)
        if max(d.textlength(l, font=bold) for l in lines) <= W - 160 or size < 60: break
        size -= 4
    block = len(lines) * int(size * 1.15) + (220 if segments else 0)
    y = (H - block) // 2 - 40
    if kicker:
        kf = ImageFont.truetype(F + "Montserrat-Bold.ttf", 40)
        d.text((80, y - 90), kicker, font=kf, fill=GREEN)
    for l in lines:
        d.text((80, y), l, font=bold, fill=INK); y += int(size * 1.15)
    if segments:
        _rich(d, segments, 80, y + 40, W - 160, 46, 62)
    d.rounded_rectangle([80, H - 120, 80 + 90, H - 112], radius=4, fill=GREEN)
    img.save(out)

def _clean_status(shot):
    s = shot.width / 923; sd = ImageDraw.Draw(shot)
    sd.rectangle([60*s, 30*s, 250*s, 110*s], fill=shot.getpixel((int(70*s), int(40*s))))
    sd.rectangle([660*s, 30*s, 880*s, 110*s], fill=shot.getpixel((int(670*s), int(40*s))))
    sd.text((100*s, 48*s), "9:41", font=ImageFont.truetype(F + "Montserrat-SemiBold.ttf", int(38*s)), fill=(255, 255, 255))
    for i, h in enumerate([10, 16, 22, 28]):
        sd.rounded_rectangle([(690+i*14)*s, (86-h)*s, (699+i*14)*s, 86*s], radius=2, fill=(255, 255, 255))
    sd.rounded_rectangle([780*s, 56*s, 838*s, 86*s], radius=8, outline=(255, 255, 255), width=max(2, int(3*s)))
    sd.rounded_rectangle([786*s, 62*s, 832*s, 80*s], radius=4, fill=(255, 255, 255))
    sd.rectangle([841*s, 65*s, 845*s, 77*s], fill=(255, 255, 255))
    return shot

def phone(out, headline, segments, shot_path, clean=False):
    """Слайд с экраном: заголовок в одну-две строки, телефон показан почти целиком."""
    from PIL import ImageFilter
    img = _bg().convert('RGBA'); d = ImageDraw.Draw(img)
    bold = ImageFont.truetype(F + "Montserrat-Bold.ttf", 66)
    y = 70
    d.text((80, y), " ".join(headline), font=bold, fill=INK)
    if d.textlength(" ".join(headline), font=bold) > W - 160:
        y2 = y
        for l in headline: d.text((80, y2), l, font=bold, fill=INK); y2 += 76
        img = _bg().convert('RGBA'); d = ImageDraw.Draw(img); y2 = y
        for l in headline: d.text((80, y2), l, font=bold, fill=INK); y2 += 76
        y = y2
    else:
        y += 80
    y = _rich(d, segments, 80, y + 6, W - 160, 36, 48)
    shot = Image.open(shot_path).convert('RGB')
    if clean: shot = _clean_status(shot)
    pw = 600; ph = int(shot.height * pw / shot.width); shot = shot.resize((pw, ph), Image.LANCZOS)
    bez = 18; r = 76; px = (W - pw) // 2; py = y + 40
    ph_img = Image.new('RGBA', (pw + 2*bez, ph + 2*bez), (0, 0, 0, 0))
    ImageDraw.Draw(ph_img).rounded_rectangle([0, 0, pw + 2*bez - 1, ph + 2*bez - 1], radius=r + bez, fill=(18, 20, 22, 255))
    mask = Image.new('L', (pw, ph), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=r, fill=255)
    ph_img.paste(shot, (bez, bez), mask)
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([px - bez + 8, py - bez + 30, px + pw + bez + 8, py + ph + bez + 30], radius=r + bez, fill=(20, 60, 40, 70))
    img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(35)))
    img.alpha_composite(ph_img, (px - bez, py - bez))
    img.convert('RGB').save(out)

if __name__ == "__main__" and sys.argv[1] == "--config":
    cfg = json.load(open(sys.argv[2])); os.makedirs(cfg["out_dir"], exist_ok=True)
    for s in cfg["slides"]:
        o = os.path.join(cfg["out_dir"], s["name"] + ".png")
        if s["kind"] == "hook":
            hook(o, s["lines"], [tuple(x) for x in s.get("segments", [])] or None, s.get("kicker"))
        else:
            shot = s["shot"] if s["shot"].startswith("/") else os.path.join(cfg["shots_dir"], s["shot"])
            phone(o, s["headline"], [tuple(x) for x in s["segments"]], shot, s.get("clean", False))
        print("ok", s["name"])

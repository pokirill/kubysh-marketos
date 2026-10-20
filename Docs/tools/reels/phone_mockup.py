"""Мокап: в клип «Кубыш показывает телефон» вклеить настоящий экран приложения с перспективой.
python3 phone_mockup.py экран.png — экран ищется по светлому цвету, углы сглаживаются по ±2 кадрам; результат —
папка кадров «Кубыш_библиотека/телефон_мокап/» (движок читает папки кадров как клип)."""
import os, sys, hashlib, numpy as np
from PIL import Image, ImageDraw, ImageFilter
LIB = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы маскот/Кубыш_библиотека/"
CLIP = LIB + "телефон.mp4"


def quad(a):
    a = a.astype(int); R, G, B = a[..., 0], a[..., 1], a[..., 2]
    m = (B > 170) & (B >= G - 5) & (R > 150) & (a.sum(-1) > 540); m[:, 700:] = False
    m &= (m.sum(0) > 60)[None, :] & (m.sum(1) > 30)[:, None]
    ys, xs = np.nonzero(m)
    if len(xs) < 30000: return None
    s, df = xs + ys, xs - ys
    return np.array([(xs[s.argmin()], ys[s.argmin()]), (xs[df.argmax()], ys[df.argmax()]), (xs[s.argmax()], ys[s.argmax()]), (xs[df.argmin()], ys[df.argmin()])], float)


def coeffs(src, dst):
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; b += [u, v]
    return np.linalg.solve(np.array(A), np.array(b))


def build(scr, out=LIB + "телефон_мокап"):
    d = os.path.join(os.path.dirname(__file__), ".cache", "clips", hashlib.md5((CLIP + "1080x1920").encode()).hexdigest()[:10])
    fs = sorted(os.listdir(d)); os.makedirs(out, exist_ok=True)
    frames = [np.asarray(Image.open(os.path.join(d, f)).convert("RGB")) for f in fs]
    qs = [quad(a) for a in frames]
    S = Image.open(scr).convert("RGB"); sw, sh = S.size; src = [(0, 0), (sw, 0), (sw, sh), (0, sh)]
    for i, (a, q) in enumerate(zip(frames, qs)):
        im = Image.fromarray(a)
        if q is not None:
            q = np.median([qs[j] for j in range(max(0, i - 2), min(len(qs), i + 3)) if qs[j] is not None], axis=0)
            c = q.mean(0); q = c + (q - c) * 1.03
            w = S.transform(im.size, Image.PERSPECTIVE, tuple(coeffs(src, q)), Image.BICUBIC)
            mk = Image.new("L", im.size, 0); ImageDraw.Draw(mk).polygon([tuple(p) for p in q], fill=255)
            im.paste(w, (0, 0), mk.filter(ImageFilter.GaussianBlur(1.5)))
        im.save(os.path.join(out, f"f_{i}.png"))


if __name__ == "__main__":
    build(sys.argv[1])

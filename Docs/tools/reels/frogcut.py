"""Вырезка жаб из референсов на сером фоне (заливка от углов) и выравнивание вариантов позы (рот, моргание) под базовый кадр."""
import collections, sys
from PIL import Image, ImageFilter

def cut(im, thr=46):
    im = im.convert("RGB"); w, h = im.size; px = im.load(); bg = px[2, 2]
    mask = Image.new("L", (w, h), 255); m = mask.load(); seen = set()
    q = collections.deque([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])
    while q:
        x, y = q.popleft()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h): continue
        seen.add((x, y))
        if sum(abs(px[x, y][i] - bg[i]) for i in range(3)) >= thr: continue
        m[x, y] = 0; q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    mask = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = im.convert("RGBA"); rgba.putalpha(mask)
    return rgba.crop(rgba.getbbox())

if __name__ == "__main__":
    base_path, out_dir, name = sys.argv[1], sys.argv[2], sys.argv[3]
    base = cut(Image.open(base_path)); base.save(f"{out_dir}/cut_{name}.png")
    for v in sys.argv[4:]:
        tag, path = v.split("=")
        cut(Image.open(path)).resize(base.size, Image.LANCZOS).save(f"{out_dir}/cut_{name}_{tag}.png")
    print(base.size)

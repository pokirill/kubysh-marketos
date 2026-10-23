"""Превью App Store 1.7.5 (886×1920, 30 с, без звука): запись экрана во весь кадр под тёмной полосой с подписью.
Сегмент = (запись, начало, скорость, длительность, фокус по высоте 0..1, зум, подпись, мелкая строка).
Кадры исходника вынимаются frameat только для нужных отрезков (15 к/с, сразу уменьшаются). Запуск: python3 store_preview.py"""
import os, subprocess, glob
from PIL import Image, ImageDraw
from promo_hero import font, rich, text_img, put, eout, span, lerp, WHITE, SUB, GREEN, BG0, ICON

W, H, FPS, SRC_FPS = 886, 1920, 30, 30
BAND = 380                                  # тёмная полоса с подписью
A = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Промо/"
R = A + "Стор_1.7.5/"
FRAMEAT = "/private/tmp/claude-501/-Users-kirillpopov-Documents/813dd944-c9c8-41ec-af80-2d6c9361f624/scratchpad/frameat"
SHOT = A + "Герой/кадры/получка_26окт.png"   # реальная «Получка» Кирилла: серия 20, «оптимально ещё 989»

SEG = [  # запись, старт, скорость, длительность, фокус, зум, подпись, мелкая строка
    (SHOT, 0, 0, 2.5, 0.36, 1.25, "Сколько тратить *сегодня*,", "чтобы накопить на мечту?"),
    ("S1_онбординг.mp4", 13, 3, 2.0, 0.30, 1.0, "План *за 3 минуты*", "доход, кредиты, обязательное"),
    ("S1_онбординг.mp4", 145, 1, 2.5, 0.62, 1.2, "Сколько можешь *копить*", "с учётом кредитов, аренды и базовых трат"),
    ("S1_онбординг.mp4", 279, 1, 2.5, 0.50, 1.15, "Когда накопишь *на цели*", "подушка и мечты — с прогнозными датами"),
    ("S1_онбординг.mp4", 307, 1, 2.5, 0.68, 1.2, "Бюджет *на каждый день*", "до следующей получки"),
    ("S1_онбординг.mp4", 319, 1, 2.5, 0.35, 1.1, "Отложил — *цель ближе*", "новая дата сразу"),
    ("S2_трата.mp4", 13, 2.0, 5.0, 0.45, 1.05, "Пересчёт *после каждой траты*", "и совет, что делать дальше"),
    ("S3_получка_обзор_игра.mp4", 57, 2.5, 4.0, 0.45, 1.0, "Видно, *куда уходят деньги*", "без таблиц и духоты"),
    ("S3_получка_обзор_игра.mp4", 8.5, 1, 2.5, 0.45, 1.0, "Копить, *как в игре*", "серии, уровни, награды"),
    ("S3_получка_обзор_игра.mp4", 90, 1, 2.0, 0.40, 1.0, "Копить, *как в игре*", "соревнуйся с друзьями"),
    (SHOT, 0, 0, 2.0, 0.45, 1.0, "Кубыш. *Копить без тревоги*", ""),
]
SW, SH = W, H - BAND
CACHE = R + "_кадры/"


def src_frames(i, seg):
    """Кадры отрезка: уменьшенные JPEG в кэше (кроп под окно и зум делаем при сборке)."""
    path, t0, sp, dur = seg[:4]; d = CACHE + f"{i:02d}/"
    if path.endswith(".png"): return [Image.open(path).convert("RGB")]
    if not os.path.isdir(d) or not os.listdir(d):
        os.makedirs(d, exist_ok=True)
        n = max(1, int(dur * SRC_FPS)); ts = [round(t0 + k / SRC_FPS * sp, 3) for k in range(n)]
        for c in range(0, n, 40):
            subprocess.run([FRAMEAT, R + path, d + "f"] + [str(x) for x in ts[c:c + 40]], capture_output=True)
            for k in range(min(40, n - c)):
                p = d + f"f_{k}.png"
                if os.path.exists(p):
                    Image.open(p).convert("RGB").resize((900, int(900 * 2622 / 1206)), Image.LANCZOS).save(d + f"{c + k:04d}.jpg", quality=90); os.remove(p)
    return [Image.open(f).convert("RGB") for f in sorted(glob.glob(d + "*.jpg"))]


_MASK = {}
def screen(img, focus, zoom, t, dur):
    """Экран целиком (скругленный, с тенью) в зоне под полосой; камера плавно наезжает на фокус (zoom) за 0,7 с."""
    sh = SH - 60; sw = int(sh * img.width / img.height)
    k = eout(span(t, 0.1, 0.8)); z = lerp(1.0, zoom, k) * lerp(1.0, 1.02, t / max(dur, 0.01))
    w2, h2 = int(sw * z), int(sh * z)
    key = (w2, h2)
    if key not in _MASK:
        m = Image.new("L", key, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w2 - 1, h2 - 1], int(52 * z), fill=255); _MASK[key] = m
    scr = img.resize(key, Image.BILINEAR)
    fy = lerp(0.5, focus, k)                                  # точка фокуса уезжает к центру кадра
    x = (SW - w2) / 2; y = SH / 2 - fy * h2
    y = min(30, max(SH - 30 - h2, y)) if h2 > SH - 60 else (SH - h2) / 2
    lay = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); lay.paste(scr, (int(x), int(y)), _MASK[key])
    return lay


def build():
    os.makedirs(R, exist_ok=True)
    frames = [src_frames(i, s) for i, s in enumerate(SEG)]
    out = R + "_video.mp4"
    enc = subprocess.Popen([os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "store_cards", "mp4enc"), out, str(W), str(H), str(FPS)], stdin=subprocess.PIPE)
    icon = Image.open(ICON + "AppStore-1024.png").convert("RGBA").resize((170, 170), Image.LANCZOS)
    mk = Image.new("L", (170, 170), 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, 169, 169], 38, fill=255); icon.putalpha(mk)
    bg = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(bg)
    for y in range(0, H, 4): d.rectangle([0, y, W, y + 4], fill=(int(lerp(14, 4, y / H)), int(lerp(26, 8, y / H)), int(lerp(22, 7, y / H)), 255))
    from PIL import ImageFilter
    gl = Image.new("RGBA", (W // 4, H // 4)); ImageDraw.Draw(gl).ellipse([-40, 120, 200, 360], fill=(30, 130, 88, 70)); bg.alpha_composite(gl.filter(ImageFilter.GaussianBlur(40)).resize((W, H)))
    prev = None
    T = 0.0
    for i, (path, t0, sp, dur, focus, zoom, cap, sub) in enumerate(SEG):
        fr = frames[i]
        for k in range(int(dur * FPS)):
            t = k / FPS
            src = fr[min(len(fr) - 1, int(t * SRC_FPS))]
            cv = bg.copy()
            lay = screen(src, focus, zoom, t, dur)
            kin = eout(span(t, 0.0, 0.3)) if i > 0 else 1.0       # переход: новый экран въезжает и проявляется
            if kin < 1 and prev is not None:
                cv.alpha_composite(prev, (0, BAND))
                lay = lay.resize((int(SW * lerp(1.06, 1, kin)), int(SH * lerp(1.06, 1, kin))), Image.BILINEAR)
                lay.putalpha(lay.getchannel("A").point(lambda v: int(v * kin)))
                cv.alpha_composite(lay, (int((W - lay.width) / 2), BAND + int((SH - lay.height) / 2) + int(60 * (1 - kin))))
            else:
                cv.alpha_composite(lay, (0, BAND))
            last = lay
            g = Image.new("RGBA", (W, 60)); ImageDraw.Draw(g)   # мягкий переход полосы в экран
            for y in range(60): ImageDraw.Draw(g).line([0, y, W, y], fill=BG0 + (int(255 * (1 - y / 60)),))
            cv.alpha_composite(g, (0, BAND))
            same = i > 0 and SEG[i - 1][6] == cap      # та же подпись — без повторной анимации
            ka = 1.0 if same else eout(span(t, 0.0, 0.35))
            put(cv, rich(cap, 60), W / 2, 150 + 20 * (1 - ka), a=ka)
            if sub: put(cv, text_img(sub, 38, SUB, "Medium"), W / 2, 250 + 20 * (1 - ka), a=ka)
            if i == len(SEG) - 1:   # финал: иконка
                kb = eout(span(t, 0.3, 0.8)); put(cv, icon, W / 2, BAND + SH / 2, a=kb, scale=lerp(0.8, 1.0, kb))
            enc.stdin.write(cv.tobytes("raw", "BGRA"))
            if i == 0 and k == 0: cv.convert("RGB").save(R + "Постер.png")
        prev = last; T += dur
    enc.stdin.close(); enc.wait()
    final = R + "Превью_стора_1.7.5.mp4"; os.replace(out, final); print(final, round(T, 1), "с")


if __name__ == "__main__":
    build()

"""Инфографика для сюжетных роликов вместо записи экрана (Кирилл 26.10): тёмный стиль промо, SF Pro.
plan(ep, t0, t1, cfg) — зарплата → строки плана → «≈ N на день»; chips(ep, t0, t1, items) — крупные чипы-выводы по очереди."""
import math
from PIL import Image, ImageDraw
import promo_hero as P


def _bg(t):
    return P.background(t).convert("RGBA")


def plan(ep, t0, t1, cfg):
    """cfg: income, rows=[(название, подпись, сумма, цвет)], daily, days. Число тает по строкам, итог — сумма на день."""
    rows = cfg["rows"]; n = len(rows); step = (t1 - t0 - 2.2) / max(n, 1)
    def fn(img, t, cam):
        cv = _bg(t)
        fin = P.span(t, t1 - 1.8, t1 - 1.4) > 0.5
        P.put(cv, P.text_img("На жизнь до зарплаты" if fin else "Зарплата пришла", 44, P.GREEN if fin else P.SUB, "SemiBold"), P.W / 2, 330)
        v = cfg["income"]
        for i, (name, sub, amt, col) in enumerate(rows):
            st = t0 + 0.5 + i * step; v -= amt * P.eio(P.span(t, st + 0.1, st + 0.6))
            k = P.eout(P.span(t, st, st + 0.45))
            if k <= 0: continue
            im, pad = P.card(940, 170, 36); d = ImageDraw.Draw(im); x0, y0 = pad + 34, pad + 30
            d.rounded_rectangle([x0, y0, x0 + 16, y0 + 110], 8, fill=col)
            d.text((x0 + 44, y0), name, font=P.font("Bold", 46), fill=P.WHITE)
            d.text((x0 + 44, y0 + 62), sub, font=P.font("Medium", 34), fill=P.SUB)
            d.text((pad + 940 - 34, y0 + 26), "−" + P.rub(amt), font=P.font("Bold", 50), fill=P.WHITE, anchor="ra")
            P.put(cv, im, P.W / 2 + 120 * (1 - k), 700 + i * 210, a=k)
        P.big_number(cv, v, 470, color=P.WHITE, size=160)
        kd = P.eout(P.span(t, t1 - 1.6, t1 - 1.1))
        if kd > 0:
            P.put(cv, P.chip(f"≈ {P.rub(cfg['daily'])} ₽ на день · {cfg['days']} дней", P.GREEN, 54), P.W / 2, 700 + n * 210 + 40, a=kd, scale=P.lerp(1.2, 1, kd))
        img.paste(cv.convert(img.mode), (0, 0))
    ep.add(t0, t1, "screen", fn)


def chips(ep, t0, t1, items):
    """items: [(текст, цвет)] — крупные чипы друг под другом, каждый держится до конца отрезка."""
    step = (t1 - t0 - 0.4) / max(len(items), 1)
    def fn(img, t, cam):
        cv = _bg(t)
        for i, (s, col) in enumerate(items):
            k = P.eout(P.span(t, t0 + 0.2 + i * step, t0 + 0.6 + i * step))
            if k > 0: P.put(cv, P.chip(s, col, 62, check=(i == 0)), P.W / 2, 760 + i * 180, a=k, scale=P.lerp(1.25, 1, k))
        img.paste(cv.convert(img.mode), (0, 0))
    ep.add(t0, t1, "screen", fn)

"""Визуальные метафоры серии Т (рисуются кодом, без генераций): табло с перещелкиванием, таблица на холодильнике,
крошечные ячейки таблицы в телефоне с промахом пальцем, секундомер. Каждая — fn(ep, t0, t1, ...) поверх всего кадра."""
import math
from PIL import Image, ImageDraw
from studio import *  # noqa
import props as P


def _bg(img, top, bot):
    d = ImageDraw.Draw(img)
    for y in range(0, H, 8):
        k = y / H; d.rectangle([0, y, W, y + 8], fill=tuple(int(lerp(a, b, k)) for a, b in zip(top, bot)))
    return d


def flipboard(ep, t0, t1, rows, title=None, flip_at=None):
    """Табло, как на вокзале. rows: [(было, стало, y, размер, цвет)]. С flip_at буквы перещелкиваются по одной."""
    TW = {}
    def tile(ch, size, col):
        key = (ch, size, col)
        if key not in TW:
            w, h = int(size * 0.72), int(size * 1.25)
            im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(size * 0.12), fill=(34, 36, 40, 255))
            d.text((w / 2, h / 2), ch, font=P.font(size), fill=col + (255,), anchor="mm")
            d.line([0, h / 2, w, h / 2], fill=(12, 12, 14, 255), width=max(2, size // 22))
            TW[key] = im
        return TW[key]
    for _, b, *_ in rows:
        for i in range(len(b)): ep.sfx((flip_at or t0) + 0.05 * i, "tick", 0.08)
    def fn(img, t, cam):
        _bg(img, (18, 20, 24), (6, 7, 9))
        d = ImageDraw.Draw(img)
        if title:
            d.text((W / 2, 300), title, font=P.font(46, "SemiBold"), fill=(255, 196, 64), anchor="mm")
        for a, b, y, size, col in rows:
            n = max(len(a), len(b)); a, b = a.rjust(n), b.rjust(n)
            tw = int(size * 0.72) + 8; x0 = W / 2 - n * tw / 2
            for i in range(n):
                tf = (flip_at if flip_at is not None else -99) + 0.05 * i
                ch = b[i] if t >= tf + 0.12 else a[i]
                k = 1.0
                if tf <= t < tf + 0.24: k = abs(math.cos(math.pi * seg(t, tf, tf + 0.24)))  # щелчок: плитка схлопывается и раскрывается
                im = tile(ch, size, col)
                if k < 0.98: im = im.resize((im.width, max(1, int(im.height * k))))
                img.alpha_composite(im, (int(x0 + i * tw), int(y - im.height / 2))) if img.mode == "RGBA" else img.paste(im, (int(x0 + i * tw), int(y - im.height / 2)), im)
    ep.add(t0, t1, "screen", fn)


def fridge(ep, t0, t1, budget="5 418", spent="7 400", spent_t=None):
    """Бумажная таблица на холодильнике: бюджет дня написан от руки, трата приклеена стикером, а цифра стоит."""
    def fn(img, t, cam):
        d = _bg(img, (232, 236, 238), (198, 204, 208))
        d.rounded_rectangle([60, 120, W - 60, H + 40], radius=60, fill=(244, 246, 247), outline=(205, 210, 214), width=6)
        d.rounded_rectangle([W - 150, 620, W - 112, 1100], radius=18, fill=(200, 205, 210))  # ручка
        for (x, y, c) in ((200, 330, (230, 80, 90)), (820, 360, (80, 160, 230)), (260, 1180, (250, 190, 60))):
            d.ellipse([x - 34, y - 34, x + 34, y + 34], fill=c)
        sx, sy = 170 + 6 * math.sin(t * 1.3), 420
        d.rectangle([sx, sy, sx + 700, sy + 760], fill=(255, 253, 240), outline=(214, 208, 180), width=3)
        for i in range(1, 9): d.line([sx + 20, sy + 80 * i, sx + 680, sy + 80 * i], fill=(200, 210, 230), width=2)
        d.line([sx + 330, sy + 20, sx + 330, sy + 740], fill=(230, 160, 160), width=2)
        d.text((sx + 40, sy + 40), "Бюджет на день", font=P.font(44, "Medium"), fill=(60, 70, 110))
        d.text((sx + 40, sy + 130), budget, font=P.font(150), fill=(40, 50, 120))
        for i, row in enumerate(["еда", "кафе", "такси", "разное"]):
            d.text((sx + 40, sy + 360 + 80 * i), row, font=P.font(38, "Medium"), fill=(110, 110, 130))
        if spent_t is not None and t >= spent_t:
            k = back(seg(t, spent_t, spent_t + 0.35), 1.8)
            note = Image.new("RGBA", (420, 300), (0, 0, 0, 0)); nd = ImageDraw.Draw(note)
            nd.rectangle([0, 0, 419, 299], fill=(255, 226, 90, 255))
            nd.text((210, 95), "Потратил", font=P.font(44, "Medium"), fill=(90, 60, 10), anchor="mm")
            nd.text((210, 190), spent, font=P.font(96), fill=(170, 40, 40), anchor="mm")
            note = scaled(note.rotate(-8, expand=True, resample=Image.BICUBIC), k)
            comp(img, note, 640 - note.width / 2, 1000 - note.height / 2)
            if t > spent_t + 0.6 and int(t * 2.5) % 2 == 0:  # цифра стоит: мигает знак вопроса
                d.text((sx + 620, sy + 190), "?", font=P.font(110), fill=(200, 50, 50), anchor="mm")
    ep.add(t0, t1, "screen", fn)


def tiny_cells(ep, t0, t1, miss_t=None):
    """Таблица в телефоне: крошечные ячейки, палец, промах — подсветилась не та строка."""
    def fn(img, t, cam):
        d = _bg(img, (30, 34, 40), (14, 16, 20))
        z = lerp(1.0, 1.35, eio(seg(t, t0, t0 + 1.2)))
        px, py, pw, ph = W / 2 - 330 * z, 260 - 80 * (z - 1), 660 * z, 1360 * z
        d.rounded_rectangle([px, py, px + pw, py + ph], radius=int(70 * z), fill=(250, 250, 252), outline=(60, 64, 72), width=int(14 * z))
        cw, chh = 58 * z, 30 * z; gx, gy = px + 40 * z, py + 140 * z
        for r in range(36):
            for c in range(10):
                x, y = gx + c * cw, gy + r * chh
                if y + chh > py + ph - 60 * z or x + cw > px + pw - 30 * z: continue
                fill = (255, 255, 255)
                if miss_t is not None and t >= miss_t and r == 17: fill = (255, 205, 205)
                if r == 0: fill = (226, 232, 240)
                d.rectangle([x, y, x + cw, y + chh], fill=fill, outline=(150, 158, 170), width=2)
                if r > 0 and (r * 7 + c * 3) % 5 < 3:  # «текст» в ячейках
                    d.rectangle([x + 6 * z, y + chh * 0.35, x + cw * (0.4 + 0.1 * ((r + c) % 4)), y + chh * 0.65], fill=(120, 128, 140))
        fx, fy = lerp(W / 2 + 260, gx + 4.5 * cw, eio(seg(t, t0 + 0.6, (miss_t or t1) - 0.1))), lerp(1700, gy + 17.5 * chh, eio(seg(t, t0 + 0.6, (miss_t or t1) - 0.1)))
        if miss_t is not None and t >= miss_t: fx += 10 * math.sin(t * 50) * (1 - seg(t, miss_t, miss_t + 0.4))
        d.ellipse([fx - 70, fy - 70, fx + 70, fy + 70], fill=(236, 190, 160), outline=(190, 140, 110), width=6)
        d.ellipse([fx - 30, fy - 52, fx + 30, fy - 8], fill=(248, 220, 205))
        if miss_t is not None and t >= miss_t:
            d.text((W / 2, py - 40 + 0 * z if py > 120 else 120), "Не та строка", font=P.font(64), fill=(255, 110, 110), anchor="mm")
    ep.add(t0, t1, "screen", fn)


def stopwatch(ep, t0, t1, secs=10, run=(None, None), label="3 траты"):
    """Секундомер: стрелка пробегает secs за run, крупно счетчик и подпись."""
    r0, r1 = run
    def fn(img, t, cam):
        d = _bg(img, (16, 40, 32), (8, 20, 16))
        cx, cy, R = W / 2, 820, 330
        d.ellipse([cx - R - 30, cy - R - 30, cx + R + 30, cy + R + 30], fill=(240, 242, 240))
        d.rounded_rectangle([cx - 40, cy - R - 110, cx + 40, cy - R - 20], radius=14, fill=(220, 224, 220))
        for i in range(60):
            a = math.radians(i * 6 - 90); l = 40 if i % 5 == 0 else 18
            d.line([cx + math.cos(a) * (R - l), cy + math.sin(a) * (R - l), cx + math.cos(a) * R, cy + math.sin(a) * R], fill=(40, 44, 40), width=6 if i % 5 == 0 else 3)
        s = secs * eio(seg(t, r0 if r0 is not None else t0, r1 if r1 is not None else t1))
        a = math.radians(s * 6 - 90)
        d.line([cx, cy, cx + math.cos(a) * (R - 50), cy + math.sin(a) * (R - 50)], fill=(220, 50, 50), width=12)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(220, 50, 50))
        d.text((cx, cy + R + 150), f"00:{int(s):02d}", font=P.font(130), fill=WHITE, anchor="mm")
        d.text((cx, 230), label, font=P.font(90), fill=(255, 214, 74), anchor="mm")
    ep.add(t0, t1, "screen", fn)


def excel(ep, t0, t1, add_t, cons_t, budget="5 418", spent="7 400", minus="≈ −2 000"):
    """Ноутбук с таблицей в экселе: «На день 5 418», добавилась строка «Ресторан 7 400», а ячейка та же.
    С cons_t — следствие: дни до зарплаты листаются с той же цифрой, в день зарплаты красный минус."""
    def fn(img, t, cam):
        d = _bg(img, (226, 230, 234), (190, 196, 202))
        if t < cons_t:
            lx, ly, lw, lh = 70, 420, W - 140, 900
            d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=30, fill=(40, 42, 46))
            sx, sy, sw, sh = lx + 26, ly + 26, lw - 52, lh - 70
            d.rectangle([sx, sy, sx + sw, sy + sh], fill=WHITE)
            d.rectangle([sx, sy, sx + sw, sy + 70], fill=(33, 115, 70))
            d.text((sx + 24, sy + 35), "Бюджет.xlsx", font=P.font(34, "SemiBold"), fill=WHITE, anchor="lm")
            cols = [0, 330, 640, sw]; rows = ["Дата", "Еда", "Кафе", "Такси"]
            if t >= add_t: rows = rows + ["Ресторан"]
            for i in range(9):
                y = sy + 110 + i * 70
                d.line([sx, y, sx + sw, y], fill=(205, 210, 215), width=2)
                if i < len(rows):
                    hl = rows[i] == "Ресторан"
                    if hl:
                        k = eout(seg(t, add_t, add_t + 0.3)); d.rectangle([sx, y, sx + sw, y + 70], fill=(255, int(lerp(255, 236, k)), int(lerp(255, 180, k))))
                    d.text((sx + 20, y + 35), rows[i], font=P.font(34, "Medium"), fill=(40, 40, 50), anchor="lm")
                    if i > 0: d.text((sx + 360, y + 35), {"Еда": "1 200", "Кафе": "650", "Такси": "480", "Ресторан": spent}[rows[i]], font=P.font(34, "Medium"), fill=(40, 40, 50), anchor="lm")
            for x in cols[1:3]: d.line([sx + x, sy + 110, sx + x, sy + sh], fill=(205, 210, 215), width=2)
            d.rectangle([sx + 640, sy + 110, sx + sw, sy + 250], fill=(232, 245, 236), outline=(33, 115, 70), width=4)
            d.text((sx + 660, sy + 140), "На день", font=P.font(32, "Medium"), fill=(33, 115, 70))
            d.text((sx + 660, sy + 185), budget, font=P.font(60), fill=(20, 60, 40))
            if t > add_t + 0.6 and int(t * 2.5) % 2 == 0:
                d.text((sx + sw - 50, sy + 200), "?", font=P.font(80), fill=(200, 50, 50), anchor="mm")
        else:  # следствие: дни с той же цифрой и минус в день зарплаты
            n = 6; k = seg(t, cons_t, t1 - 0.8)
            for i in range(n):
                x = 90 + i * 155; y = 700
                on = k * n > i
                d.rounded_rectangle([x, y, x + 140, y + 220], radius=20, fill=WHITE if on else (230, 232, 236), outline=(190, 195, 200), width=3)
                d.text((x + 70, y + 50), f"{21 + i}", font=P.font(48), fill=(90, 90, 100), anchor="mm")
                if on: d.text((x + 70, y + 150), budget.replace(" ", " "), font=P.font(34, "Medium"), fill=(40, 50, 120), anchor="mm")
            if t > t1 - 0.9:
                kk = back(seg(t, t1 - 0.9, t1 - 0.6), 1.8)
                s = scaled(word_img(f"К зарплате {minus}", 84, fill=(255, 90, 90)), kk); comp(img, s, W / 2 - s.width / 2, 1050)
    ep.add(t0, t1, "screen", fn)


def envelopes(ep, t0, t1, mode, split_t=None):
    """Метод конвертов. mode="many": десяток конвертов по категориям, купюры путаются. mode="three": лишние улетают
    (с split_t), остаются три большие «Обязательное · Кошелек · Накопления». mode="done": три закрытых с галочками."""
    many = ["Еда", "Кафе", "Такси", "Подарки", "Коммуналка", "Связь", "Одежда", "Здоровье", "Отпуск", "Разное"]
    three = [("Обязательное", (90, 110, 170)), ("Кошелек", (220, 150, 50)), ("Накопления", (40, 150, 100))]
    def env(d, x, y, w, h, label, col, closed=False, check=False):
        d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=(250, 244, 228), outline=col, width=5)
        d.polygon([(x + 6, y + 6), (x + w / 2, y + h * (0.55 if closed else 0.3)), (x + w - 6, y + 6)], fill=(236, 226, 200), outline=col)
        d.text((x + w / 2, y + h * 0.78), label, font=P.font(max(24, int(w / 9)), "SemiBold"), fill=col, anchor="mm")
        if check: d.text((x + w - 40, y + 40), "✓", font=P.font(int(w / 6)), fill=(40, 150, 100), anchor="mm")
    def fn(img, t, cam):
        d = _bg(img, (54, 44, 36), (30, 24, 20))
        if mode == "many":
            for i, lab in enumerate(many):
                x = 70 + (i % 3) * 320 + 10 * math.sin(t * 3 + i); y = 260 + (i // 3) * 300
                env(d, x, y, 280, 190, lab, (120, 100, 80))
            for j in range(6):  # купюры мечутся между конвертами
                a = t * 2.2 + j * 1.1; x = W / 2 + 380 * math.sin(a); y = 760 + 360 * math.sin(a * 1.3 + j)
                d.rounded_rectangle([x - 70, y - 34, x + 70, y + 34], radius=6, fill=(140, 190, 140), outline=(70, 120, 70), width=3)
        else:
            go = eio(seg(t, split_t or t0, (split_t or t0) + 0.8)) if mode == "three" else 1.0
            for i, lab in enumerate(many[:7]):
                x = 70 + (i % 3) * 320; y = 260 + (i // 3) * 300 - 1400 * go
                if y > -200: env(d, x, y, 280, 190, lab, (120, 100, 80))
            for i, (lab, col) in enumerate(three):
                k = eout(seg(t, (split_t or t0) + 0.4 + 0.25 * i, (split_t or t0) + 0.8 + 0.25 * i)) if mode == "three" else 1.0
                if k <= 0: continue
                w, h = 860 * k, 330 * k; x = W / 2 - w / 2; y = 380 + i * 400
                env(d, x, y, w, h, lab, col, closed=(mode == "done"), check=(mode == "done"))
    ep.add(t0, t1, "screen", fn)


def bucket(ep, t0, t1, first_t=None):
    """Дырявое ведро: зарплата льется водой и утекает через дырки «такси», «доставка», «маркетплейс».
    С first_t: сначала монеты в банку «Накопления», остаток — в ведро."""
    holes = [("такси", 0.25), ("доставка", 0.5), ("маркетплейс", 0.75)]
    def fn(img, t, cam):
        d = _bg(img, (40, 52, 70), (18, 24, 34))
        bx, by, bw, bh = 260, 820, 560, 620
        d.polygon([(bx, by), (bx + bw, by), (bx + bw - 70, by + bh), (bx + 70, by + bh)], fill=(150, 160, 175), outline=(90, 100, 115))
        lvl = 0.55 + 0.1 * math.sin(t * 2) if first_t is None or t < first_t else 0.35
        wy = by + bh * (1 - lvl)
        d.polygon([(bx + 70 * (1 - lvl) + 8, wy), (bx + bw - 70 * (1 - lvl) - 8, wy), (bx + bw - 78, by + bh - 6), (bx + 78, by + bh - 6)], fill=(80, 160, 230))
        for x in range(int(bx + 200), int(bx + 360), 8):  # струя сверху
            d.line([x, 380, x + 20 * math.sin(t * 6 + x), wy], fill=(110, 180, 240), width=6)
        d.text((W / 2, 330), "Зарплата", font=P.font(64), fill=WHITE, anchor="mm")
        for lab, k in holes:
            hx, hy = bx + bw - 70 * k + 4, by + bh * k
            for j in range(5):
                ph = (t * 3 + j * 0.2) % 1
                d.ellipse([hx + 40 + 180 * ph - 9, hy + 260 * ph * ph - 9, hx + 40 + 180 * ph + 9, hy + 260 * ph * ph + 9], fill=(110, 180, 240))
            d.text((hx + 70, hy - 40), lab, font=P.font(40, "Medium"), fill=(255, 140, 140))
        if first_t is not None and t >= first_t:  # банка накоплений слева
            k = eout(seg(t, first_t, first_t + 0.5)); jx, jy = 90, 520
            d.rounded_rectangle([jx, jy, jx + 230, jy + 380], radius=40, outline=(220, 240, 230), width=8)
            f = min(1, seg(t, first_t + 0.3, t1 - 0.5))
            if f > 0.01: d.rectangle([jx + 12, jy + 368 - 340 * f, jx + 218, jy + 368], fill=(255, 200, 60))
            d.text((jx + 115, jy - 50), "Накопления", font=P.font(40, "SemiBold"), fill=(140, 240, 180), anchor="mm")
    ep.add(t0, t1, "screen", fn)


def jar_counter(ep, t0, t1, value=81500, label="каждый месяц"):
    """Итог Б1: полная банка и счетчик «+81 500 каждый месяц»."""
    def fn(img, t, cam):
        d = _bg(img, (18, 50, 38), (8, 24, 18))
        jx, jy = W / 2 - 220, 640
        d.rounded_rectangle([jx, jy, jx + 440, jy + 640], radius=70, outline=(230, 245, 235), width=12)
        d.rectangle([jx + 22, jy + 120, jx + 418, jy + 620], fill=(255, 200, 60))
        v = int(value * eout(seg(t, t0 + 0.1, t0 + 1.2)) / 100) * 100
        s = word_img("+" + f"{v:,}".replace(",", " ") + " ₽", 120, fill=(255, 214, 74)); comp(img, s, W / 2 - s.width / 2, 300)
        s2 = word_img(label, 70, fill=WHITE); comp(img, s2, W / 2 - s2.width / 2, 470)
    ep.add(t0, t1, "screen", fn)


def odometer(ep, t0, t1, value=116992):
    """Обычное приложение — одометр: барабаны крутят «Потрачено 116 992», серые столбики прошлого."""
    def fn(img, t, cam):
        d = _bg(img, (34, 34, 38), (14, 14, 16))
        d.text((W / 2, 420), "Потрачено", font=P.font(64, "Medium"), fill=(170, 170, 180), anchor="mm")
        v = int(value * eout(seg(t, t0, t0 + 2.0))); s = f"{v:06d}"
        for i, ch in enumerate(s):
            x = 150 + i * 135
            d.rounded_rectangle([x, 520, x + 120, 700], radius=14, fill=(20, 20, 22), outline=(90, 90, 96), width=4)
            d.text((x + 60, 610), ch, font=P.font(110), fill=WHITE, anchor="mm")
        for i, h in enumerate([220, 340, 180, 300, 260, 380]):
            d.rectangle([180 + i * 125, 1350 - h, 260 + i * 125, 1350], fill=(110, 110, 118))
        d.text((W / 2, 1420), "и что с этим делать?", font=P.font(52, "Medium"), fill=(150, 150, 160), anchor="mm")
    ep.add(t0, t1, "screen", fn)


def navigator(ep, t0, t1, eta="Япония · 10.08.2027"):
    """Кубыш — навигатор: дорога к цели, точка едет, время прибытия — прогнозная дата цели."""
    def fn(img, t, cam):
        d = _bg(img, (230, 236, 228), (206, 214, 204))
        pts = [(200, 1650), (300, 1350), (650, 1200), (520, 900), (800, 700), (700, 420)]
        d.line(pts, fill=(255, 255, 255), width=70, joint="curve"); d.line(pts, fill=(60, 170, 110), width=30, joint="curve")
        k = eio(seg(t, t0 + 0.2, t1 - 0.6)); n = len(pts) - 1; i = min(int(k * n), n - 1); f = k * n - i
        x, y = lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)
        d.ellipse([x - 34, y - 34, x + 34, y + 34], fill=(40, 120, 230), outline=WHITE, width=8)
        d.ellipse([680, 370, 740, 430], fill=(230, 70, 70))
        d.rounded_rectangle([90, 120, W - 90, 300], radius=40, fill=(255, 255, 255))
        d.text((W / 2, 170), "Прибытие к цели", font=P.font(40, "Medium"), fill=(110, 120, 115), anchor="mm")
        d.text((W / 2, 245), eta, font=P.font(60), fill=(30, 110, 70), anchor="mm")
    ep.add(t0, t1, "screen", fn)


def analytics_then_nav(ep, t0, t1, card="/Users/kirillpopov/Documents/Кубыш доки и артефакты /Скриншоты 1.7/Карточки для стора 1.7 (сборка 100)/07_Куда_уходят_деньги.png"):
    """С1: сначала аналитика «куда ушли» (карточка 07, телефон крупно), затем навигатор к цели."""
    mid = t0 + (t1 - t0) * 0.45
    im = Image.open(card).convert("RGB")
    ph = im.crop((90, 700, 1200, 2796)).resize((760, int(760 * 2096 / 1110))).convert("RGBA")
    def fn(img, t, cam):
        d = _bg(img, (238, 242, 238), (214, 222, 214))
        k = back(seg(t, t0, t0 + 0.4), 1.4); s = scaled(ph, k * lerp(1.0, 1.08, seg(t, t0, mid)))
        comp(img, s, W / 2 - s.width / 2, 260)
        d.rounded_rectangle([170, 120, W - 170, 220], radius=50, fill=(40, 52, 46)); d.text((W / 2, 170), "Куда ушли деньги", font=P.font(52), fill=WHITE, anchor="mm")
    ep.add(t0, mid, "screen", fn)
    navigator(ep, mid, t1)


JARS = [("Подушка", "25.11.2026"), ("Отпуск", "10.08.2027"), ("Айфон", "10.03.2027"), ("Ремонт", None)]


def jars(ep, t0, t1, mode):
    """Б2: банки целей. spread — одна струя мечется по всем банкам, в каждой по капле;
    queue — Кубыш наполняет по очереди: подушка доверху, потом отпуск, у каждой дата; done — итог: две даты крупно."""
    n = 4 if mode == "spread" else 2 if mode == "done" else 3
    def fn(img, t, cam):
        d = _bg(img, (34, 44, 66), (14, 18, 30))
        jw, gap = (200, 50) if n == 4 else (250, 70) if n == 3 else (360, 100)
        x0 = (W - n * jw - (n - 1) * gap) / 2; jy, jh = 900, 520
        k = seg(t, t0, t1)
        for i in range(n):
            name, date = JARS[i]; x = x0 + i * (jw + gap)
            if mode == "spread": lvl = 0.06 + 0.03 * math.sin(t * 3 + i)
            elif mode == "queue": lvl = [eout(seg(k, 0.1, 0.55)), 0.35 * eout(seg(k, 0.55, 0.95)), 0.0][i]
            else: lvl = [1.0, 0.45][i]
            if lvl > 0.01: d.rectangle([x + 14, jy + jh - 14 - (jh - 40) * lvl, x + jw - 14, jy + jh - 14], fill=(255, 200, 60))
            d.rounded_rectangle([x, jy, x + jw, jy + jh], radius=40, outline=(225, 235, 245), width=10)
            d.text((x + jw / 2, jy - 60), name, font=P.font(52 if n < 4 else 42, "SemiBold"), fill=WHITE, anchor="mm")
            if mode != "spread" and date and (mode == "done" or k > [0.3, 0.7, 0.85][i]):
                d.text((x + jw / 2, jy + jh + 70), date, font=P.font(64 if n == 2 else 46), fill=(140, 240, 180), anchor="mm")
        if mode != "done":  # карточка «Зарплата», из нее падают монеты: spread — по всем банкам вразброс, queue — в одну
            d.rounded_rectangle([W / 2 - 230, 230, W / 2 + 230, 420], radius=30, fill=(52, 120, 246))
            d.text((W / 2, 290), "Зарплата", font=P.font(52, "SemiBold"), fill=WHITE, anchor="mm")
            d.text((W / 2, 365), "+150 000 ₽", font=P.font(56), fill=WHITE, anchor="mm")
            for j in range(10):
                ph = (t * 1.1 + j / 10) % 1
                tgt = j % n if mode == "spread" else (0 if k < 0.55 else 1)
                cx = lerp(W / 2, x0 + tgt * (jw + gap) + jw / 2, ph); cy = lerp(430, jy + jh - 80, ph * ph)
                d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(255, 200, 60), outline=(200, 140, 30), width=4)
                d.text((cx, cy), "₽", font=P.font(34), fill=(120, 80, 10), anchor="mm")
    ep.add(t0, t1, "screen", fn)


def pocket(ep, t0, t1, value=2000):
    """Б4: дырявый карман джинсов — сэкономленные 2 000 высыпаются монетами «кофе», «доставка», «мелочи», счетчик тает до нуля."""
    labs = ["кофе", "доставка", "мелочи", "такси"]
    def fn(img, t, cam):
        d = _bg(img, (40, 58, 96), (16, 22, 40))
        px, py = 290, 560
        d.rounded_rectangle([px, py, px + 500, py + 560], radius=60, fill=(60, 90, 150), outline=(30, 50, 90), width=10)
        d.line([px + 40, py + 70, px + 460, py + 70], fill=(220, 180, 90), width=8)
        d.ellipse([px + 200, py + 520, px + 300, py + 590], fill=(16, 22, 40))  # дырка
        k = seg(t, t0 + 0.3, t1 - 0.3)
        for j in range(8):
            ph = (t * 1.3 + j / 8) % 1; x = px + 250 + 30 * math.sin(j * 2.1); y = py + 560 + 700 * ph * ph
            d.ellipse([x - 40, y - 40, x + 40, y + 40], fill=(255, 200, 60), outline=(200, 140, 30), width=5)
            if j % 2 == 0: d.text((x + 70, y), labs[(j // 2) % 4], font=P.font(40, "Medium"), fill=(255, 150, 150), anchor="lm")
        v = int(value * (1 - eio(k)) / 10) * 10
        s = word_img("Сэкономил " + f"{v:,}".replace(",", " ") + " ₽", 84, fill=(255, 214, 74)); comp(img, s, W / 2 - s.width / 2, 300)
    ep.add(t0, t1, "screen", fn)


def fork(ep, t0, t1, value=2000):
    """Итог Б4: монета «2 000» на развилке, два указателя «Отпуск» и «Выходные» — выбор за человеком."""
    def fn(img, t, cam):
        d = _bg(img, (22, 70, 52), (8, 26, 20))
        d.polygon([(460, 1700), (620, 1700), (560, 1000), (520, 1000)], fill=(200, 190, 160))
        d.polygon([(520, 1000), (560, 1000), (300, 620), (220, 640)], fill=(200, 190, 160))
        d.polygon([(520, 1000), (560, 1000), (860, 640), (780, 620)], fill=(200, 190, 160))
        for x, y, lab, col in [(120, 470, "Цель", (60, 170, 110)), (640, 470, "Выходные", (240, 150, 60))]:
            d.rounded_rectangle([x, y, x + 320, y + 110], radius=24, fill=col)
            d.text((x + 160, y + 55), lab, font=P.font(52, "SemiBold"), fill=WHITE, anchor="mm")
        sw = 40 * math.sin(t * 2.2); cx, cy = 540 + sw, 1080
        d.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], fill=(255, 200, 60), outline=(200, 140, 30), width=10)
        d.text((cx, cy), f"{value:,}".replace(",", " "), font=P.font(64), fill=(90, 60, 10), anchor="mm")
    ep.add(t0, t1, "screen", fn)

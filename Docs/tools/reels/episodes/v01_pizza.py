"""V1 · «Зарплата — это пицца» v3 (~30 с, петля). Фотореалистичная пицца режется маской по фото, под куском — пустая доска.
Крючки СДВГ: старт с результата и перемотка назад, вопрос в первой секунде, стоп-кадр с ответом, петля в конце.
Голос = подпись дословно. Камера (скилл camera-moves): отъезд-удар в хуке, перемотка, переброска к Душной, наезд,
поворот за ножом, стоп-кадр, таймлапс дня, склейка по форме в экран плана, наплыв в первый кадр.
"""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from studio import *  # noqa

R = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/"
F = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы маскот/V01_Зарплата_пицца/"
VO = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/V_серия/"
PLAN = R + "Запись_экрана/стартовый_план_ксюши.png"
CX, CY, RAD = 545, 880, 470
TOTAL, MUST, PIG, DAYS = 138000, 30000, 40000, 16
GREEN = dict(bg=(30, 130, 88), fg=WHITE)
DARK = dict(bg=(40, 34, 30), fg=WHITE)
TABLE = (236, 222, 200)


class Pizza:
    def __init__(self):
        self.board = Image.open(F + "board_toon.png").convert("RGBA").resize((W, H), Image.LANCZOS)
        self.photo = Image.open(F + "pizza_toon.png").convert("RGB").resize((W, H), Image.LANCZOS)
        am = 360 * MUST / TOTAL; ap = 360 * PIG / TOTAL
        self.must = self.wedge(-90, -90 + am)
        self.pig = self.wedge(-90 + am, -90 + am + ap)
        r0 = -90 + am + ap; st = (270 - r0) / DAYS
        self.days = [self.wedge(r0 + i * st, r0 + (i + 1) * st) for i in range(DAYS)]

    def wedge(self, a0, a1):
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).pieslice([CX - RAD, CY - RAD, CX + RAD, CY + RAD], a0, a1, fill=255)
        box = m.getbbox(); piece = self.photo.crop(box).convert("RGBA"); piece.putalpha(m.crop(box))
        sh = Image.new("RGBA", piece.size, (0, 0, 0, 0)); sh.putalpha(piece.getchannel("A").point(lambda v: int(v * 0.45)))
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        mid = math.radians((a0 + a1) / 2)
        return dict(img=piece, shadow=sh, dir=(math.cos(mid), math.sin(mid)), c=((box[0] + box[2]) / 2, (box[1] + box[3]) / 2))

    def place(self, cv, w, dx=0.0, dy=0.0, k=1.0, lift=0.0, alpha=1.0, ring=None):
        img, sh = w["img"], w["shadow"]
        if abs(k - 1) > 0.003:
            img = img.resize((max(1, int(img.width * k)), max(1, int(img.height * k))), Image.BILINEAR); sh = sh.resize(img.size, Image.BILINEAR)
        if alpha < 0.999:
            if alpha <= 0.01: return
            img = img.copy(); img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))
        x = int(w["c"][0] + dx - img.width / 2); y = int(w["c"][1] + dy - img.height / 2)
        if lift > 0.01: cv.alpha_composite(sh, (x + int(18 * lift), y + int(26 * lift)))
        ox, oy = x - int(4 * lift), y - int(8 * lift)
        cv.alpha_composite(img, (ox, oy))
        if ring:
            a = img.getchannel("A"); o = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(17)), a)
            col = Image.new("RGBA", img.size, ring + (255,)); col.putalpha(o); cv.alpha_composite(col, (ox, oy))

    def frame(self, s):
        """Куски дней рисуются первыми, отрезанные куски — поверх пиццы и без уменьшения: поднимаются и уезжают к краю."""
        cv = self.board.copy()
        for i, w in enumerate(self.days):
            g = eio(seg(s["cut"], i / DAYS * 0.8, i / DAYS * 0.8 + 0.25))  # куски расходятся по очереди
            dx, dy, k, lift, ring = w["dir"][0] * 24 * g, w["dir"][1] * 24 * g, 1.0, 0.35 * g, None
            if i == 0 and s["today"] > 0:
                tk = back(s["today"], 1.6); dx += w["dir"][0] * 120 * tk; dy += w["dir"][1] * 120 * tk; k = 1 + 0.14 * tk; lift = tk; ring = MINT
            if i == 1 and s["tomorrow"] > 0:
                tk = back(s["tomorrow"], 1.6); dx += w["dir"][0] * 60 * tk; dy += w["dir"][1] * 60 * tk; k = 1 + 0.12 * tk; lift = 0.7 * tk; ring = YEL
            self.place(cv, w, dx, dy, k, lift=lift, ring=ring)
        for key, w in (("must", self.must), ("pig", self.pig)):
            m = s[key]
            if m <= 0: self.place(cv, w); continue
            up = eout(seg(m, 0, 0.3)); go = eio(seg(m, 0.25, 1.0))
            self.place(cv, w, w["dir"][0] * 330 * go, w["dir"][1] * 330 * go, 1 + 0.05 * up * (1 - go), lift=0.4 + up)
        return cv


def build():
    ep = Ep("V01_Зарплата_пицца", "studio")
    ep.vgain = 0.95
    ep.avatars = {w: Image.open(R + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("ksy", "kubysh", "dush")}
    pz = Pizza()

    # голоса и тайминг (подпись = голос дословно)
    a0, a1 = ep.say("kubysh", "", cap="Сто тридцать восемь тысяч. Сколько можно потратить *сегодня?*", at=0.25, file=VO + "v3f_1.wav", y=1560, size=70)
    d0 = a1 + 0.35
    b0, b1 = ep.say("dush", "", cap="Нисколько… Потратишь сейчас — и не увидишь, как цветет *сакура* в Японии", at=d0 + 0.1, file=VO + "д_сакура_f.wav", y=1400, size=70)
    p0 = b1 + 0.25
    caps = ["Первый кусок — *обязательное:* аренда и коммуналка",
            "Второй — сразу в *копилку:* подушка и Япония", "Остальное режу на *шестнадцать дней* до аванса",
            "Сегодня твой кусок — *четыре двести пятьдесят*",
            "Потратила меньше — я пересчитал. Завтра кусок *больше,* а сэкономленное — *твое*"]
    c, t = [], p0
    for i, cap in enumerate(caps):
        x0, x1 = ep.say("kubysh", "", cap=cap, at=t, file=VO + f"v3f_{i + 3}.wav", y=1560, size=68)
        c.append((x0, x1)); t = x1 + (0.3 if i != 3 else 0.7)
    (s3a, s3b), (s4a, s4b), (s5a, s5b), (s6a, s6b), (s7a, s7b) = c; s2a = p0
    s8a = s7b + 0.3; s8b = s8a + 3.4  # экран плана: «Япония к апрелю» без голоса
    cta0 = s8b + 0.2
    g0, g1 = ep.say("kubysh", "", cap="Напиши в комментариях слово «план» — пришлю приложение. До следующей зарплаты — бесплатно",
                    at=cta0 + 0.3, file=VO + "v3f_9.wav", y=1400, size=64)
    loop0 = g1 + 0.3; ep.dur = loop0 + 0.9

    def state(t):
        if t < d0:  # хук: результат, затем перемотка к целой пицце
            r = 1 - eio(seg(t, 1.7, 2.5))
            return dict(must=r, pig=r, cut=r, today=r, tomorrow=0)
        return dict(must=seg(t, s3a + 0.4, s3a + 1.6), pig=seg(t, s4a + 0.4, s4a + 1.7), cut=seg(t, s5a + 0.3, s5a + 2.2),
                    today=seg(t, s6a + 0.3, s6a + 0.8), tomorrow=seg(t, s7a + 3.0, s7a + 3.6))

    today_c = pz.days[0]["c"]
    def cam(t):
        if t < d0:
            k = eout(seg(t, 0.0, 0.55))
            return lerp(1.9, 1.0, k) * (1 + 0.04 * seg(t, 2.5, d0)), lerp(today_c[0], CX, k), lerp(today_c[1], CY, k), 0.0
        z = 1.0 + 0.06 * seg(t, s2a, s3a); rot = -7 * eio(seg(t, s5a + 0.3, s5a + 2.2))
        k = eio(seg(t, s6a + 0.3, s6a + 0.9)) * (1 - eio(seg(t, s7a, s7a + 0.6)))
        return z + 0.35 * k, lerp(CX, today_c[0], k), lerp(CY, today_c[1], k), rot

    def view(t):
        cv = pz.frame(state(t)).convert("RGB")
        z, fx, fy, rot = cam(t)
        if abs(rot) > 0.05: cv = cv.rotate(rot, resample=Image.BICUBIC, center=(CX, CY), fillcolor=TABLE)
        if abs(z - 1) > 0.002:
            w, h = W / z, H / z; x0 = min(max(0, fx - w / 2), W - w); y0 = min(max(0, fy - h / 2), H - h)
            cv = cv.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BILINEAR)
        return cv

    first = view(0.0)
    def layer(img, t, cam_):
        if d0 <= t < p0 or s8a <= t < loop0: return
        if t >= loop0:  # петля: наплыв в первый кадр
            cur = img.convert("RGB"); img.paste(Image.blend(cur, first, seg(t, loop0, loop0 + 0.8)).convert(img.mode), (0, 0)); return
        img.paste(view(t).convert(img.mode), (0, 0))
    ep.add(0, ep.dur, "screen", layer)

    # Душная: переброска и три окна губ клипа S1b
    ep.sfx(d0 - 0.05, "whoosh", 0.7); ep.sfx(p0 - 0.05, "whoosh", 0.7)
    q1 = b0 + 2.0
    ep.clip(d0, q1, R + "K02_клипы/S1b.mp4", "D1", src_t0=0.6)
    ep.clip(q1, p0, R + "K02_клипы/S1b.mp4", "D2", src_t0=2.65, speed=0.75)

    # числа = голос
    ep.pill(0.6, 1.7, "?", 540, 330, size=90, **DARK)
    ep.pill(s3a + 1.4, s8a, "Обязательное · 30 000", 640, 230, size=44, **DARK)
    ep.pill(s4a + 1.5, s8a, "Копилка · 40 000", 760, 1000, size=44, **GREEN)
    ep.pill(s5a + 2.0, s7a, "16 дней до аванса", 540, 1330, size=46, **DARK)
    ep.counter(s6a + 0.6, s7a, 0, 4250, 540, 430, size=120, color=MINT)
    ep.sfx(s3a + 0.4, "swish", 0.4); ep.sfx(s4a + 1.5, "kaching", 0.5); [ep.sfx(s5a + 0.3 + (i / DAYS * 0.8 + 0.1) * 1.9, "tick", 0.3) for i in range(DAYS)]; ep.sfx(s6a + 0.5, "ding", 0.5)
    for i, hh in enumerate(["10:00", "13:00", "16:00", "19:00", "21:00"]):  # таймлапс дня
        ep.pill(s7a + 0.2 + i * 0.35, s7a + 0.55 + i * 0.35, hh, 540, 430, size=64, **DARK); ep.sfx(s7a + 0.2 + i * 0.35, "tick", 0.3)
    ep.notif(s7a + 2.0, s8a, "Кубыш", "Потрачено 2 800 из 4 250", icon="К", color=(30, 130, 88))
    ep.pill(s7a + 3.2, s8a, "Завтра 4 347", 540, 1330, size=56, bg=(200, 160, 30), fg=INK)
    ep.pill(s7a + 3.6, s8a, "Экономия +1 450 — твоя", 540, 1440, size=46, **GREEN)

    # склейка по форме: сегодняшний кусок → экран плана Ксюши
    def bg(img, t, cam_): ImageDraw.Draw(img).rectangle([0, 0, W, H], fill=TABLE)
    ep.add(s8a, cta0, "screen", bg)
    ep.card(s8a, cta0, PLAN, keys=[(s8a, (0, 330, 1206, 2100), 540, 700, 760), (s8a + 0.9, (0, 1150, 1206, 1760), 540, 640, 1000)],
            marks=[(s8a + 1.2, (60, 1330, 1150, 1700), MINT)])
    ep.pill(s8a + 0.2, cta0, "У каждой цели — своя дата", 540, 230, size=50, **DARK)
    for i, txt in enumerate(["Подушка — к декабрю", "Япония — к апрелю", "Алтай — к августу", "Новый айфон — к сентябрю"]):
        ep.pill(s8a + 1.3 + i * 0.45, cta0, txt, 540, 1060 + i * 100, size=46, **GREEN); ep.sfx(s8a + 1.3 + i * 0.45, "pop", 0.4)
    ep.sfx(s8a, "boom", 0.4)

    # призыв: Кубыш в кадре
    ep.clip(cta0, loop0 + 1.0, R + "K03_клипы/C5.mp4", "C5", src_t0=0.6)
    ep.pill(g0 + 0.3, loop0, "Напиши «план» — пришлю приложение", 540, 330, size=46, **DARK)
    ep.pill(g0 + 2.5, loop0, "До следующей зарплаты — бесплатно", 540, 440, size=40, **GREEN)
    ep.cover_t = 0.9
    return ep

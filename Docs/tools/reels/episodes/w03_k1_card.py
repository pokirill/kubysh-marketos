"""К1 · вт 03.11 18:00 · «Карта не прошла» (сценарий 82, v3, правки Кирилла 02.11).
Касса — фон Higgsfield (кассирша и терминал), голоса: кассирша Vera, герой за кадром Archie (мат запикан),
Кубыш Holden, Душная клон. Душная упрощена: серая жаба в очках (frog.DUSH_SIMPLE)."""
from PIL import Image, ImageDraw
import promo_hero as PH
from studio import *  # noqa
import props as P
import audio
import frog
from episodes.scr import STY, RK
from episodes.lib import PHONE

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
BG = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы маскот/W03_K1_Карта_не_прошла/касса.png"
Y, SZ = 1100, 54
ITEMS = [("сыр", "690", 210, 300), ("колбаса", "540", 210, 375), ("хлеб", "90", 210, 450), ("молоко", "120", 210, 525)]
DAYS = list(range(10, 20))
MARK = {14: "бар", 17: "ДР мамы"}


def _tag(name, price, red=False):
    f = PH.font("Bold", 34); w = int(f.getlength(f"{name} {price} ₽")) + 40
    im = Image.new("RGBA", (w, 62), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 61], 18, fill=(255, 255, 255, 245), outline=(214, 36, 52, 255) if red else (220, 220, 225, 255), width=3)
    d.text((w // 2, 31), f"{name} {price} ₽", font=f, fill=(30, 30, 34), anchor="mm")
    return im


def _strip(t, x0, y, cell, done_t=None, labels=True):
    """Календарь до зарплаты: 10 дней + день зарплаты; done_t(i) — момент, когда день становится зеленым."""
    im = Image.new("RGBA", (W, cell + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f, fs = PH.font("Bold", int(cell * 0.42)), PH.font("SemiBold", 26)
    for i, day in enumerate(DAYS + [20]):
        x = x0 + i * (cell + 8); pay = day == 20
        g = done_t is not None and not pay and t >= done_t(i)
        fill = (30, 130, 88, 255) if g else ((255, 214, 74, 255) if pay else (36, 44, 42, 235))
        if day in MARK and not g: fill = (170, 48, 60, 255)
        d.rounded_rectangle([x, 0, x + cell, cell], 14, fill=fill)
        d.text((x + cell / 2, cell / 2), str(day), font=f, fill=(20, 24, 22) if pay else (255, 255, 255), anchor="mm")
        if labels and (day in MARK or pay):
            d.text((x + cell / 2, cell + 30), "зарплата" if pay else MARK[day], font=fs, fill=(255, 255, 255), anchor="mm", stroke_width=3, stroke_fill=(20, 24, 22))
    return im


def build():
    ep = Ep("W03_K1_Карта_не_прошла", "store"); ep.sfxgain = 0.5
    ep.avatars = {w: Image.open(RK + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("kubysh", "dush")}
    ep.extra = []
    kub = ep.actor("kub", "kubysh", 800, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.58, mirror=True, hidden=True, pointer=False) if False else ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)

    def say(who, f, cap, at, a=None):
        t0, t1 = ep.say(who, "", cap=cap, at=at, y=Y, size=SZ, file=V + f + "_t_48k.wav")
        if a is not None:
            smp = ep.voice[-1][1]; env = audio.envelope(smp, FPS); e = ep.env.setdefault(a.name, [0.0] * int(400 * FPS)); f0 = int(t0 * FPS)
            for i, v in enumerate(env):
                if f0 + i < len(e): e[f0 + i] = max(e[f0 + i], v)
        return t0, t1

    # 1 · касса: писк сканера, ошибка терминала, кассирша
    ep.extra.append((0.0, audio.load(V + "kassa_err.wav"), 0.5))
    kub.expr(0, "neutral"); ep.shot(0, "wide")
    tags = [(_tag(n, p), _tag(n, p, True), x, y) for n, p, x, y in ITEMS]
    def kassa(img, t, cam, t_end=None):
        for i, (im, imr, x, y) in enumerate(tags):
            k = back(seg(t, 0.05 + 0.12 * i, 0.3 + 0.12 * i))
            gone = seg(t, ep.T_out + 0.25 * i, ep.T_out + 0.25 * i + 0.4)
            if k <= 0.02 or gone >= 1: continue
            sp = scaled(imr if t > ep.T_out else im, k); comp(img, fade(sp, 1 - gone), x - sp.width / 2 - 260 * eio(gone), y - sp.height / 2 - 120 * gone)
            if t > ep.T_out - 0.1:
                dd = ImageDraw.Draw(img); ww = sp.width * min(1, seg(t, ep.T_out - 0.1 + 0.25 * i, ep.T_out + 0.1 + 0.25 * i))
                dd.line([(x - sp.width / 2 - 260 * eio(gone), y - 120 * gone), (x - sp.width / 2 + ww - 260 * eio(gone), y - 120 * gone)], fill=(214, 36, 52), width=6)
        k = back(seg(t, 0.55, 0.85))
        if k > 0.02:
            tot = PH.chip("Итого 1 440 ₽", PH.RED, 44); comp(img, scaled(tot, k), 210 - tot.width * k / 2, 575)
    c0, c1 = say("cashier", "cashier", "Оплата не прошла. Недостаточно средств", at=0.75)
    ep.stamp(0.85, c1 + 0.4, P.word_stamp("ОТКАЗ", (214, 36, 52)), 540, 860)
    h0, h1 = say("hero", "w1_hero1", "Отказ? До зарплаты еще *5 дней.* Пи**ец", at=c1 + 0.15)
    kub.expr(h0, "shock"); kub.react(h0 + 0.2, "shudder")
    ep.pill(h0 + 0.5, h1 + 0.3, "до зарплаты 5 дней", 540, 880, size=56, **STY["red"])
    # 2 · Душная в очереди
    dush.show(h1 - 0.4); dush.go(h1 - 0.4, 280, hop=60, step=300); dush.expr(h1 - 0.4, "dush")
    a0, a1 = say("dush", "w1_dush", "Выложи сыр. И колбасу. И себя *выложи обратно*", at=h1 + 0.2, a=dush)
    ep.T_out = a0 + 0.2; ep.add(0, a1 + 0.3, "screen", kassa); ep.sfx(a0 + 0.2, "whoosh", 0.4)
    ep.shot(a0, ("dush", "kub"), dur=0.4); kub.expr(a0 + 0.3, "worried")
    ep.clip(0, a1 + 0.3, BG, "касса")
    # 3 · отмотка на 10 дней назад: листок
    tb = a1 + 0.3
    ep.set(tb, "night_lamp", fade=0.2); ep.sfx(tb, "whoosh", 0.6)
    ep.pill(tb, tb + 1.6, "10 дней назад", 540, 330, size=54, **STY["yellow"])
    dush.go(tb, -380, hop=60, step=320)
    b0, b1 = say("kubysh", "w1_flash2", "10 дней назад. Ты посчитал на листке, и все *сходилось*", at=tb + 0.2, a=kub)
    ep.shot(b0, "wide"); kub.expr(b0, "talk")
    note = P.notes_card([("Остаток", "24 000"), ("До зарплаты", "10 дней"), ("В день", "2 400")], w=760, h=520)
    g0, g1 = say("hero", "w1_hero2", "Бл**ь, я же с пацанами *в бар* в субботу. И у мамы *день рождения*", at=b1 + 0.15)
    def paper(img, t, cam, t0=b0, t1=g1 + 0.2):
        k = back(seg(t, t0, t0 + 0.35)) * (1 - ease(seg(t, t1 - 0.2, t1)))
        if k > 0.02: im = scaled(note, 0.9 * k); comp(img, im, 540 - im.width / 2, 560 - im.height / 2)
    ep.add(b0, g1 + 0.2, "screen", paper)
    def cal(img, t, cam, t0=b0 + 0.6, t1=g1 + 0.2):
        k = eout(seg(t, t0, t0 + 0.4)) * (1 - ease(seg(t, t1 - 0.2, t1)))
        if k > 0.02: comp(img, fade(_strip(t, 52, 0, 80), k), 0, 880)
        if t > g0 + 0.5:   # 2 400 в день перечеркнуто: бар и подарок не учтены
            dd = ImageDraw.Draw(img); w = 150 * min(1, seg(t, g0 + 0.5, g0 + 0.9)); dd.line([(780, 640), (780 + w, 640)], fill=(214, 36, 52), width=8)
    ep.add(b0 + 0.6, g1 + 0.2, "screen", cal); ep.sfx(g0 + 0.5, "marker", 0.5)
    kub.expr(g0, "worried")
    # 4 · тот же вечер, Кубыш считает
    d0, d1 = say("kubysh", "w1_count2", "Смотри. С баром и подарком выходит примерно *1 500 в день.* И до зарплаты хватает", at=g1 + 0.35, a=kub)
    kub.expr(d0, "proud"); ep.shot(d0, "kub", z=1.15)
    rows = [("сб 14 · бар с пацанами", "4 000"), ("17 · подарок маме", "5 000")]
    def plan(img, t, cam, t0=d0, t1=d1 + 0.3):
        k = eout(seg(t, t0, t0 + 0.4)) * (1 - ease(seg(t, t1 - 0.2, t1)))
        if k <= 0.02: return
        cv, pad = PH.card(940, 600, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 40, pad + 34
        d.text((x0, y0), "План до 20-го", font=PH.font("Bold", 46), fill=PH.WHITE)
        for i, (big, sub, col) in enumerate([("≈ 1 500 ₽", "в день", PH.GREEN), ("10 дней", "до зарплаты", PH.WHITE)]):
            kk = seg(t, t0 + 0.4 + 0.3 * i, t0 + 0.7 + 0.3 * i)
            if kk > 0:
                d.text((x0 + i * 440, y0 + 90), big, font=PH.font("Bold", 74), fill=col); d.text((x0 + i * 440, y0 + 180), sub, font=PH.font("Medium", 36), fill=PH.SUB)
        for i, (a, b) in enumerate(rows):
            if t < t0 + 1.2 + 0.4 * i: continue
            yy = y0 + 280 + i * 100; d.rounded_rectangle([x0, yy, x0 + 860, yy + 80], 20, fill=(30, 40, 37))
            d.line([(x0 + 24, yy + 42), (x0 + 38, yy + 56), (x0 + 62, yy + 26)], fill=PH.GREEN, width=7)
            d.text((x0 + 84, yy + 40), a, font=PH.font("SemiBold", 38), fill=PH.WHITE, anchor="lm"); d.text((x0 + 836, yy + 40), b, font=PH.font("Bold", 40), fill=PH.WHITE, anchor="rm")
        comp(img, fade(scaled(cv, 0.9 + 0.1 * k), k), 540 - cv.width * (0.9 + 0.1 * k) / 2, 250)
    ep.add(d0, d1 + 0.3, "screen", plan)
    for i in range(2): ep.sfx(d0 + 0.4 + 0.3 * i, "pop", 0.4)
    for i in range(2): ep.sfx(d0 + 1.2 + 0.4 * i, "tick", 0.5)
    # 5 · снова касса, через 10 дней
    tm = d1 + 0.35; step = 0.22; tmo = tm + 10 * step + 0.6
    ep.pill(tm, tmo, "10 дней по плану", 540, 330, size=54, **STY["green"])
    def montage(img, t, cam):
        comp(img, _strip(t, 52, 0, 80, done_t=lambda i: tm + 0.2 + i * step), 0, 700)
        i = int((t - tm - 0.2) / step)
        if 0 <= i < 10:
            day = DAYS[i]; txt = {14: "бар с пацанами", 17: "подарок маме"}.get(day, "≈ 1 500 ₽ в день")
            st = PH.chip(txt, PH.AMBER if day in MARK else PH.GREEN, 54); comp(img, st, 540 - st.width / 2, 860)
    ep.add(tm, tmo, "screen", montage)
    for i in range(10): ep.sfx(tm + 0.2 + i * step, "clink" if DAYS[i] in MARK else "tick", 0.45)
    kub.expr(tm, "happy"); ep.shot(tm, "wide")
    td = tmo
    ep.sfx(td, "swish", 0.5); ep.extra.append((td + 0.3, audio.load(V + "kassa_ok.wav"), 0.5))
    ep.pill(td, td + 1.6, "10 дней спустя", 540, 330, size=54, **STY["yellow"])
    ep.stamp(td + 0.45, td + 2.6, P.word_stamp("ОПЛАЧЕНО", (36, 168, 96)), 540, 860); ep.sfx(td + 0.45, "kaching", 0.5)
    dush.place(td, -380)
    kub.expr(td + 0.3, "happy"); ep.shot(td, "wide")
    e0, e1 = say("kubysh", "w1_poor", "Ты не нищий. Ты просто *считал без бара*", at=td + 0.6, a=kub)
    # 6 · поворот: у Душной тоже отказ
    dush.go(e1 - 0.6, 280, hop=60, step=320); dush.expr(e1, "neutral")
    x0, x1 = say("cashier", "cashier2", "Следующий! Ой… А у вас тоже *отказ*", at=e1 + 0.25)
    ep.extra.append((x0 + 0.9, audio.load(V + "kassa_err.wav"), 0.45))
    ep.stamp(x1 - 0.5, x1 + 1.2, P.word_stamp("ОТКАЗ", (214, 36, 52)), 540, 860)
    dush.expr(x1 - 0.5, "shock"); dush.react(x1 - 0.4, "shudder"); kub.expr(x1 - 0.3, "laugh"); ep.shot(x1 - 0.5, "dush", z=1.3)
    # 7 · финал
    f0, f1 = say("kubysh", "w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=x1 + 1.0)
    ep.clip(td, f0 - 0.05, BG, "касса2")
    end = f1 + 1.4
    for a in (kub, dush): a.show(f0 - 0.05, False)
    ep.clip(f0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - f0)))
    ep.pill(f0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, 1420, size=46, **STY["green"]); ep.sfx(f0 + 1.0, "pop", 0.4)
    ep.dur = end; ep.cover_t = 1.4
    return ep

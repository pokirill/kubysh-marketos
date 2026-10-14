"""V3 · «Зарплата живет 7 дней» v2 (серия «Осознанно = круто», петля). Уроки V1: результат в первом кадре и перемотка,
голос = подпись, тревога привязана к цели, продукт живой записью, бренд и «напиши „план“» в финале, звуки тише.
Суммы по легенде Ксюши: аванс 10-го 92 000. Клипы К3, голоса Кубыша ×1,2.
"""
from PIL import Image, ImageDraw
from studio import *  # noqa

R = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/"
CL, CL2 = R + "K03_клипы/", R + "K02_клипы/"
K3 = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/K03/"
VS = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/V_серия/"
BANK = dict(icon="₽", color=(52, 120, 246))
DARK = dict(bg=(60, 50, 90), fg=WHITE)
GREEN = dict(bg=(30, 130, 88), fg=WHITE)
RED = dict(bg=(150, 40, 60), fg=WHITE)
TABLE = (236, 222, 200)


def date(ep, t0, t1, text):
    ep.pill(t0, t1, text, 540, 1030, size=42, **DARK)


def build():
    ep = Ep("V03_Зарплата_7_дней", "studio")
    ep.vgain = 0.95; ep.sfxgain = 0.4
    ep.avatars = {w: Image.open(R + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("ksy", "kubysh", "dush")}

    # 0 · хук: сначала итог (17-е, 11 300, Япония — ноль), потом перемотка к 10-му
    ep.pill(0.05, 1.6, "Зарплата прожила 7 дней", 540, 760, size=56, **RED)
    ep.pill(0.3, 1.6, "17 октября · на карте 11 300", 540, 870, size=44, **DARK)
    ep.clip(0, 1.6, CL + "C3.mp4", "H", src_t0=2.5)
    ep.clip(1.6, 2.2, CL + "C3.mp4", "Hr", src_t0=2.5, speed=-5); ep.sfx(1.6, "whoosh", 0.6)

    # 1 · 10-е: аванс пришел, Кубыш в кадре и иронизирует
    s1 = 2.2
    a0, a1 = ep.say("kubysh", "", cap="Десятое. Ксюша *богатая.* Ровно на *неделю*", at=s1 + 0.15, file=VS + "7д_богатая_f.wav", y=1400)
    s2 = a1 + 0.1
    spree = [(s1 + 0.05, "Банк", "Зачисление +92 000 ₽"), (s1 + 2.2, "Банк", "Аренда −45 000 ₽"), (s2 + 0.1, "Банк", "Маркетплейс −8 400 ₽"),
             (s2 + 0.5, "Банк", "Бар −4 600 ₽"), (s2 + 0.9, "Банк", "Суши −2 900 ₽"), (s2 + 1.3, "Банк", "Такси −1 100 ₽")]
    ep.pushes(spree, s2 + 2.1, **BANK)
    ep.balance([(s1, 0)] + [(t, v) for (t, _, _), v in zip(spree, [92000, 47000, 38600, 34000, 31100, 30000])], s2 + 2.1)
    date(ep, s1, s2, "10 октября"); date(ep, s2, s2 + 2.1, "12 октября")
    ep.clip(s1, s2, CL + "C1.mp4", "C1")
    s3 = s2 + 2.1; ep.clip(s2, s3, CL + "C2.mp4", "C2")

    # 2 · Душная — одним планом (второе окно губ замедлено)
    b0, b1 = ep.say("dush", "", cap="Ну что, *богачка…* увидимся через *неделю*", at=s3 + 0.1, file=K3 + "д1_богачка.wav", y=1400)
    s4 = b1 + 0.15; q = b0 + 1.35
    ep.clip(s3, q, CL2 + "S1b.mp4", "D1", src_t0=0.6)
    ep.clip(q, s4, CL2 + "S1b.mp4", "D2", src_t0=1.95 + 0.6, speed=0.8)

    # 3 · обязательное всплывает, на Японию ноль
    bills = [(s4 + 0.1, "Банк", "Коммуналка −7 800 ₽"), (s4 + 0.5, "Банк", "Сплит за макбук −9 000 ₽"), (s4 + 0.9, "Банк", "Связь и подписки −1 900 ₽")]
    ep.pushes(bills, s4 + 3.0, **BANK)
    ep.balance([(s4, 30000)] + [(t, v) for (t, _, _), v in zip(bills, [22200, 13200, 11300])], s4 + 3.0)
    date(ep, s4 + 0.1, s4 + 3.0, "17 октября")
    c0, c1 = ep.say("ksy", "", cap="Ой… *коммуналка.* А на Японию *ноль*", at=s4 + 0.3, file=K3 + "кс1_коммуналка.wav", y=1400)
    ep.pill(c1 - 0.5, c1 + 0.9, "Сакура в Японии ускользает", 540, 840, size=52, **DARK)
    ep.pill(c1 - 0.2, c1 + 0.9, "До зарплаты 1 410 ₽ в день", 540, 1170, size=52, **RED)
    s5 = c1 + 1.0; ep.clip(s4, s5, CL + "C3.mp4", "C3")

    # 4 · Кубыш щелкает, перемотка к 10-му
    d0, d1 = ep.say("kubysh", "", cap="Давай *отмотаем*", at=s5 + 0.1, file=VS + "7д_отмотаем_f.wav", y=1400)
    rw = d1 + 0.25; ep.clip(s5, rw, CL + "C5.mp4", "C5", src_t0=2.2)
    ep.sfx(rw, "whoosh", 0.7); ep.sfx(rw + 0.5, "whoosh", 0.6)
    ep.clip(rw, rw + 0.5, CL + "C2.mp4", "R1", src_t0=2.4, speed=-4)
    ep.clip(rw + 0.5, rw + 1.0, CL + "C1.mp4", "R2", src_t0=4.4, speed=-6)
    s6 = rw + 1.0; date(ep, rw, s6 + 1.2, "10 октября")

    # 5 · решение живой записью: Кубыш раскладывает получку
    e0, e1 = ep.say("kubysh", "", cap="Десятого: обязательное и Япония — *сразу.* Остальное — *поровну* на каждый день",
                    at=s6 + 0.2, file=VS + "7д_десятого_f.wav", y=1720, size=60)
    s7 = e1 + 0.4
    sp = s6 + 2.6
    ep.clip(s6, sp, R + "Запись_экрана/raspredelenie_P", "P", src_t0=1.6, phone=(700, 540, 830, TABLE))
    ep.clip(sp, s7, R + "Запись_экрана/poluchka_P2b", "P2", src_t0=0.0, phone=(700, 540, 830, TABLE))
    ep.pill(s6 + 0.3, s7, "Кубыш раскладывает сам", 540, 120, size=48, **GREEN)

    # 6 · итог: суши в плане, Душная спит
    ep.pill(s7 + 0.2, s7 + 2.4, "17 октября · суши в плане, Япония отложена", 540, 330, size=40, **GREEN)
    s8 = s7 + 2.5; ep.clip(s7, s8, CL + "C8.mp4", "C8", src_t0=0.5)

    # 7 · бренд и призыв
    g0, g1 = ep.say("kubysh", "", cap="Я — *Кубыш,* приложение для денег на айфоне. Напиши в комментариях слово *«план»* — пришлю ссылку",
                    at=s8 + 0.2, file=VS + "бренд_f.wav", y=1400, size=64)
    loop0 = g1 + 0.3
    ep.clip(s8, loop0 + 0.9, CL + "C5.mp4", "C5b", src_t0=0.4)
    from episodes.k00_ad import icon as _icon
    _icon(ep, g0, loop0, y=700, size=240)
    ep.pill(g0 + 0.2, loop0, "Кубыш · приложение для денег на iPhone", 540, 330, size=42, **DARK)
    ep.pill(g0 + 2.6, loop0, "Напиши в комментариях «план»", 540, 440, size=46, **GREEN)
    ep.dur = loop0 + 0.9

    # петля: наплыв в первый кадр
    first = {}
    def fade(img, t, cam_):
        if "f" not in first: first["f"] = ep._clip_frame(ep.clips[0], 0.0)
        k = seg(t, loop0, loop0 + 0.8)
        img.paste(Image.blend(img.convert("RGB"), first["f"], k).convert(img.mode), (0, 0))
    ep.add(loop0, ep.dur, "screen", fade)
    ep.cover_t = 0.8
    return ep

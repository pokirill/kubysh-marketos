"""М1 / П8 · «Я же всё посчитал», ~27 с. Макс 3-го не может оплатить такси; Кубыш отматывает на 26-е и показывает,
что 8 000 из 30 000 уже были заняты обязательными, а темп 2 600 в день съел остальное к 3-му.
Мир Ксюши: Макс мультяшный по буку персонажей, жабы — вырезки из референсов. Клипы Kling 3.0, голоса ElevenLabs
(Кубыш Holden, Душная — клон). Сценарий v6 — `publications/53_Reels_scripts_v2.md`.
"""
from studio import *  # noqa

A = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /"
CL = A + "Рилсы Макс/M01_клипы/"
VO = A + "Голоса/M01/"
RF = A + "Рилсы Ксюша/Референсы/"
RED, GRN, DARK = (214, 64, 64), (30, 130, 88), (24, 26, 34)


def build():
    ep = Ep("M01_Я_же_всё_посчитал", "studio")
    ep.vgain = 0.95
    from PIL import Image as _I
    ep.avatars = {w: _I.open(RF + f"avatar_{w}.png").convert("RGBA") for w in ("ksy", "kubysh", "dush")}
    frog = {"kubysh": _I.open(RF + "cut_kubysh.png").convert("RGBA"), "dush": _I.open(RF + "cut_dush.png").convert("RGBA")}
    talk = []  # (t0, t1, who) — жаба покачивается, пока говорит

    def mascot(who, t0, t1, x, y, s):
        im = frog[who]
        def fn(img, t, cam):
            k = s * back(seg(t, t0, t0 + 0.35)) * (1 - ease(seg(t, t1 - 0.25, t1)))
            if k < 0.02: return
            bob = sum(math.sin((t - a) * 18) * 0.025 for a, b, w in talk if w == who and a <= t < b)
            im2 = scaled(im, k * (1 + bob))
            comp(img, im2, x - im2.width / 2, y - im2.height)
        ep.add(t0, t1, "screen", fn); ep.sfx(t0, "pop", 0.4)

    def line(who, file, cap, at, y=1400, size=78):
        a, b = ep.say(who, "", cap=cap, at=at, file=VO + file, y=y, size=size); talk.append((a, b, who)); return a, b

    # 1 · хук: 3-е, такси, отказ
    ep.clip(0, 2.9, CL + "S1.mp4", "S1 такси, терминал красный")
    ep.pill(0.1, 2.8, "3-е · на карте 240 ₽ · зарплата 5-го", 540, 300, size=44, bg=DARK, fg=WHITE)
    ep.notif(0.5, 2.6, "Оплата отклонена", "Такси 680 ₽ · на карте 240 ₽", icon="!", color=RED)
    mascot("kubysh", 0.7, 40, 840, 1900, 0.78)
    line("kubysh", "к1_отмотаем.wav", "*Классика.* Давай отмотаем", 0.8)

    # 2 · перемотка на 26-е
    ep.sfx(2.9, "whoosh", 0.6)
    ep.clip(2.9, 3.5, CL + "S1.mp4", "S1 назад", src_t0=2.9, speed=-4.0)
    ep.pill(2.9, 6.6, "Отматываем: 26-е · до зарплаты 10 дней", 540, 300, size=44, bg=DARK, fg=WHITE)
    ep.clip(3.5, 22.5, CL + "S2v2.mp4", "S2v2 дом, 15 с", speed=0.79)
    ep.pill(3.7, 6.6, "30 000 ÷ 10 = 3 000 в день. Норм", 540, 620, size=54)
    ep.chat(4.4, "me", "Я же всё посчитал", t1=6.5, y0=1150)

    # 3 · Душная винит радости
    mascot("dush", 6.5, 11.5, 230, 1900, 0.95)
    line("dush", "д1_посчитал.wav", "Посчитал он. А *такси?* А пивко в пятницу? Сидел бы дома", 6.6)

    # 4 · настоящая причина: обязательные
    ep.counter(11.5, 16.1, 30000, 22000, 540, 760, size=140, dur=2.6)
    ep.pill(12.0, 16.1, "− Кредитка 3 500", 540, 900, size=48, bg=RED, fg=WHITE)
    ep.pill(12.7, 16.1, "− Связь и интернет 1 500", 540, 1000, size=48, bg=RED, fg=WHITE)
    ep.pill(13.4, 16.1, "− Коммуналка 3 000", 540, 1100, size=48, bg=RED, fg=WHITE)
    ep.pill(14.3, 16.1, "Свободно 22 000, а не 30", 540, 1220, size=52, bg=GRN, fg=WHITE)
    line("kubysh", "к2_пивко.wav", "Пивко ни при чём. *Восемь тысяч* были не твои с самого начала", 11.6)

    # 5 · темп без контроля
    ep.pill(16.3, 22.4, "Тратил по 2 600 в день", 540, 860, size=54)
    ep.pill(17.0, 22.4, "22 000 ÷ 2 600 = 8 дней", 540, 980, size=50, bg=DARK, fg=WHITE)
    line("kubysh", "к3_тратил.wav", "А тратил по *2 600* в день. И никто не следил", 16.4)
    ep.pill(19.9, 22.4, "Хватит до 3-го · зарплата 5-го", 540, 1110, size=50, bg=RED, fg=WHITE)
    line("kubysh", "к4_сразу.wav", "Я бы показал это *сразу.* За неделю до такси", 19.9)

    # 6 · развязка и призыв
    ep.sfx(22.5, "swish", 0.4)
    k0, k1 = line("kubysh", "к5_жаба.wav", "Спокойно до зарплаты. Напиши *«жаба»* в комментах, пришлю ссылку", 23.0, y=1560, size=70)
    end = max(27.5, k1 + 0.7)
    ep.clip(22.5, end, CL + "S3.mp4", "S3 такси, терминал зелёный", speed=5.0 / (end - 22.5))
    ep.pill(22.6, 23.9, "Знать заранее — и решать самому", 540, 1050, size=46, bg=DARK, fg=WHITE)
    ep.pill(24.0, end, "Спокойно до зарплаты", 540, 1000, size=56, bg=GRN, fg=WHITE)
    ep.pill(24.4, end, "Кубыш · бесплатно в App Store", 540, 1110, size=44)
    ep.pill(24.8, end, "Напиши ЖАБА — пришлю ссылку", 540, 1220, size=50, bg=(60, 50, 90), fg=WHITE)
    ep.dur = end
    ep.cover_t = 1.4
    return ep

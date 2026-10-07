"""Продающий ролик «Кубыш» v3 (~29 с; v2 — 20 с), из клипов К1–К3 без новых генераций видео.
Разбор v1 (07.10): хук без числа и на незнакомом персонаже, продукт только на 12-й секунде, четыре функции вместо одного
«ага», нечитаемые карточки стора, нет облегчения и идентичности, слабый призыв, без музыки.
v2: хук-ситуация с числом (читается без звука) → отказы на бит → одна демонстрация на весь экран: зарплата сама
раскладывается, крупно 2 330 в день и Япония сразу (считать ничего не нужно) → «Я больше не боюсь своих денег» →
иконка, оффер, «карта не нужна». Подложка — своя синтетическая (audio.beat), склейки по долям такта.
v3 (Кирилл): кадры медленнее, хук с парадоксом и числами, цели Ксюши с датами (подушка, айфон, Япония).
"""
from studio import *  # noqa
import audio

R = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/"
K1, K2, K3 = R + "K01_клипы/", R + "K02_клипы/", R + "K03_клипы/"
VO = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/Реклама/"
SH = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Скриншоты 1.7/Из симулятора/"
ICON = "/Users/kirillpopov/Documents/FinAssist - ios /FinAssist/FinAssist/Assets.xcassets/AppIcon.appiconset/AppStore-1024.png"
DARK = dict(bg=(60, 50, 90), fg=WHITE)
BPM = 126; B = 60 / BPM  # доля такта, склейки кратны ей


def icon(ep, t0, t1, y=1020, size=300):
    from PIL import Image as _I, ImageDraw as _D
    im = _I.open(ICON).convert("RGBA").resize((size, size), _I.LANCZOS)
    m = _I.new("L", im.size, 0); _D.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=255)
    im.putalpha(m); ep.sfx(t0, "pop", 0.5)
    def fn(img, t, cam):
        k = back(seg(t, t0, t0 + 0.35), 1.6) * (1 - ease(seg(t, t1 - 0.2, t1)))
        if k < 0.02: return
        s = scaled(im, k); comp(img, s, 540 - s.width / 2, y - s.height / 2)
    ep.add(t0, t1, "screen", fn)


def build():
    ep = Ep("K00_Реклама_Кубыш", "studio")
    ep.vgain = 0.95
    from PIL import Image as _I
    ep.avatars = {w: _I.open(R + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("ksy", "kubysh", "dush")}
    OFF = 3000  # подпись за кадром: текст хука уже крупно на экране

    # 1 · хук-парадокс с числами, один спокойный кадр
    h0, h1 = ep.say("kubysh", "", cap="Зарплата", at=0.15, file=VO + "v3_хук.wav", y=OFF)
    ep.pushes([(0.05, "Банк", "Зачисление зарплаты +95 000 ₽")], h1, icon="₽", color=(52, 120, 246))
    ep.pill(0.0, h1 + 0.1, "Зарплата 95 000,", 540, 700, size=68)
    ep.pill(h0 + 2.3, h1 + 0.1, "а суши за 1 200 — «дорого»?", 540, 810, size=60)
    s1 = h1 + 0.1; ep.clip(0, s1, K3 + "C1.mp4", "C1", src_t0=0.0)

    # 2 · два отказа по 4 доли, Кубыш называет причину
    a0, a1 = ep.say("kubysh", "", cap="Это не жадность. Это тревога *без плана*", at=s1 + 0.15, file=VO + "v3_тревога.wav", y=1400)
    cuts = [(K1 + "S3a.mp4", 0.3, "Обед с коллегами? Нет"), (K2 + "S2.mp4", 0.8, "Питер? Я пас")]
    for i, (path, src, label) in enumerate(cuts):
        t = s1 + i * 4 * B; ep.clip(t, t + 4 * B, path, f"N{i}", src_t0=src)
        ep.pill(t + 0.1, t + 4 * B - 0.1, label, 540, 330, size=54, **DARK)
    s2 = max(s1 + 8 * B, a1 + 0.2)

    # 3 · Кубыш щелкает
    b0, b1 = ep.say("kubysh", "", cap="Я раскладываю зарплату *сам*", at=s2 + 0.15, file=VO + "v3_сам.wav", y=1400)
    s3 = b1 + 0.25; ep.clip(s2, s3, K3 + "C5.mp4", "C5", src_t0=1.4)

    # 4 · план получки на весь экран
    c0, c1 = ep.say("kubysh", "", cap="Обязательное, подушка и цели — *сразу.* Остальное — по *2\u00a0330* в день", at=s3 + 0.15, file=VO + "v3_план.wav", y=1560, size=68)
    ep.pill(s3 + 0.1, c1 + 0.1, "Считать ничего не нужно", 540, 250, size=52, bg=(30, 130, 88), fg=WHITE)
    ep.card(s3, c1 + 0.15, SH + "plan.png", keys=[(s3, (38, 1400, 1168, 2215), 540, 900, 1040)],
            marks=[(c0 + 1.6, (113, 2029, 1127, 2179), YEL), (c0 + 4.0, (450, 1390, 752, 1522), MINT)])
    s4 = c1 + 0.2; ep.clip(s3, s4, K2 + "S4.mp4", "S4")

    # 5 · цели Ксюши с датами: подушка, айфон, Япония
    d0, d1 = ep.say("kubysh", "", cap="Подушка — к *ноябрю.* Айфон — к *февралю.* Япония — к *июлю*", at=s4 + 0.2, file=VO + "v3_цели.wav", y=1600, size=68)
    ep.pill(s4 + 0.1, d1 + 0.2, "Ксюша копит на подушку, айфон и Японию", 540, 250, size=44, **DARK)
    jp = d0 + 3.3
    ep.card(s4, jp, SH + "goals_top_100.png", keys=[(s4, (30, 330, 1290, 1680), 540, 920, 960), (d0 + 1.7, (30, 1290, 1290, 2290), 540, 920, 960)],
            marks=[(d0 + 0.3, (860, 1555, 1265, 1650), YEL), (d0 + 2.0, (100, 2110, 330, 2205), YEL)])
    ep.card(jp, d1 + 0.3, SH + "сим_цели_96.png", keys=[(jp, (30, 1900, 1290, 2490), 540, 900, 1000)],
            marks=[(jp + 0.3, (90, 2350, 320, 2440), YEL)])
    s5 = d1 + 0.35; ep.clip(s4, s5, K2 + "S5.mp4", "S5")

    # 6 · облегчение и новая идентичность
    e0, e1 = ep.say("ksy", "", cap="Я больше не боюсь *своих денег*", at=s5 + 0.3, file=VO + "кс_небоюсь.mp3", y=1400, size=80)
    s6 = e1 + 0.8; ep.clip(s5, s6, K2 + "S6.mp4", "S6", src_t0=0.5)

    # 7 · бренд и оффер
    f0, f1 = ep.say("kubysh", "", cap="Бюджет под твою *жизнь,* а не наоборот", at=s6 + 0.2, file=VO + "v3_слоган.wav", y=1400, size=74)
    icon(ep, s6 + 0.1, f1 + 2.2, y=760, size=260)
    ep.pill(s6 + 0.3, f1 + 2.2, "Кубыш · для iPhone", 540, 330, size=56)
    ep.pill(f1 + 0.1, f1 + 2.2, "Бесплатно до следующей зарплаты", 540, 1600, size=48, bg=(30, 130, 88), fg=WHITE)
    ep.pill(f1 + 0.3, f1 + 2.2, "Карта не нужна · Скачай в App Store", 540, 1700, size=44)
    ep.dur = f1 + 2.2; ep.clip(s6, ep.dur, K2 + "S7.mp4", "S7")

    bt = audio.beat(ep.dur + 0.5, bpm=BPM)[:int(ep.dur * audio.SR)]
    ep.extra = [(0.0, ep.duck(bt, depth=0.4), 0.3)]
    ep.cover_t = 2.6
    return ep

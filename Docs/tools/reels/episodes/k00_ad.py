"""Продающий ролик «Кубыш» v2 (~20 с), из клипов К1–К3 без новых генераций видео.
Разбор v1 (07.10): хук без числа и на незнакомом персонаже, продукт только на 12-й секунде, четыре функции вместо одного
«ага», нечитаемые карточки стора, нет облегчения и идентичности, слабый призыв, без музыки.
v2: хук-ситуация с числом (читается без звука) → отказы на бит → одна демонстрация на весь экран: зарплата сама
раскладывается, крупно 2 330 в день и Япония сразу (считать ничего не нужно) → «Я больше не боюсь своих денег» →
иконка, оффер, «карта не нужна». Подложка — своя синтетическая (audio.beat), склейки по долям такта.
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

    # 1 · хук: зарплата пришла, а ты все равно отказываешь себе (читается без звука)
    s1 = 4 * B
    ep.pushes([(0.05, "Банк", "Зачисление зарплаты +95 000 ₽")], s1 - 0.1, icon="₽", color=(52, 120, 246))
    ep.pill(0.35, s1, "…и все равно отказываешь", 540, 700, size=58)
    ep.pill(0.55, s1, "себе в суши?", 540, 800, size=58)
    ep.clip(0, s1, K3 + "C1.mp4", "C1", src_t0=0.3)

    # 2 · отказы на бит, Кубыш называет причину
    cuts = [(K1 + "S3a.mp4", 0.5, "Обед с коллегами? Нет"), (K1 + "S3b.mp4", 0.5, "Корзина? Удалить"), (K2 + "S2.mp4", 1.0, "Питер? Я пас")]
    for i, (path, src, label) in enumerate(cuts):
        t = s1 + i * 2 * B; ep.clip(t, t + 2 * B, path, f"N{i}", src_t0=src)
        ep.pill(t + 0.05, t + 2 * B - 0.05, label, 540, 330, size=50, **DARK)
    a0, a1 = ep.say("kubysh", "", cap="Это не жадность. Это тревога *без плана*", at=s1 + 0.1, file=VO + "v2_тревога.wav", y=1400)
    s2 = s1 + 6 * B

    # 3 · Кубыш щелкает — зарплата раскладывается сама
    b0, b1 = ep.say("kubysh", "", cap="Я раскладываю зарплату *сам*", at=a1 + 0.1, file=VO + "v2_сам.wav", y=1400)
    s3 = s2 + 2 * B; ep.clip(s2, s3, K3 + "C5.mp4", "C5", src_t0=2.2)

    # 4 · демонстрация на весь экран: настоящий план 1.7
    c0, c1 = ep.say("kubysh", "", cap="Обязательное и Япония — *сразу.* Остальное — по *2\u00a0330* в день", at=b1 + 0.1, file=VO + "v2_план.wav", y=1560, size=70)
    ep.pill(s3 + 0.1, c1, "Считать ничего не нужно", 540, 250, size=52, bg=(30, 130, 88), fg=WHITE)
    ep.card(s3, c1 + 0.1, SH + "plan.png", keys=[(s3, (38, 1400, 1168, 2215), 540, 900, 1040)],
            marks=[(c0 + 1.0, (113, 2029, 1127, 2179), YEL), (c0 + 3.3, (450, 1390, 752, 1522), MINT)])
    s4 = c1 + 0.15; ep.clip(s3, s4, K2 + "S4.mp4", "S4")

    # 5 · облегчение и новая идентичность
    d0, d1 = ep.say("ksy", "", cap="Я больше не боюсь *своих денег*", at=s4 + 0.25, file=VO + "кс_небоюсь.mp3", y=1400, size=80)
    s5 = d1 + 0.5; ep.clip(s4, s5, K2 + "S6.mp4", "S6", src_t0=1.0)

    # 6 · бренд и оффер
    e0, e1 = ep.say("kubysh", "", cap="Бюджет под твою *жизнь,* а не наоборот", at=s5 + 0.15, file=VO + "v2_слоган.wav", y=1400, size=74)
    icon(ep, s5 + 0.1, e1 + 2.0, y=760, size=260)
    ep.pill(s5 + 0.3, e1 + 2.0, "Кубыш · для iPhone", 540, 330, size=56)
    ep.pill(e1 + 0.1, e1 + 2.0, "Бесплатно до следующей зарплаты", 540, 1600, size=48, bg=(30, 130, 88), fg=WHITE)
    ep.pill(e1 + 0.3, e1 + 2.0, "Карта не нужна · Скачай в App Store", 540, 1700, size=44)
    ep.dur = e1 + 2.0; ep.clip(s5, ep.dur, K2 + "S7.mp4", "S7")

    bt = audio.beat(ep.dur + 0.5, bpm=BPM)[:int(ep.dur * audio.SR)]
    ep.extra = [(0.0, ep.duck(bt, depth=0.4), 0.32)]
    ep.cover_t = 0.9
    return ep

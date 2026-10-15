"""П10 · пробник нового формата (12.10, после фокус-группы): «12 000 на ботинки — это конец?», ~23 с, без Higgsfield.
Холодная аудитория: к 3-й секунде сказано, что такое Кубыш; дальше настоящий экран «Прикинуть покупку» из симулятора
(12 000 = 4 064 из бюджета на сегодня + 7 000 из кошелька + 936 экономии; в день 4 064 → 3 947).
СДВГ: хук числом в 1-ю секунду, открытая петля, смена плана каждые 1–1,5 с, прогресс-бар, удары звука.
Кубыш — позы из листов референсов (`Референсы/poses`), голоса Яндекса (kirill / omazh).
"""
from studio import *  # noqa
from mascot import Mascot

A = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /"
PZ = A + "Рилсы Ксюша/Референсы/poses/"
RF = A + "Рилсы Ксюша/Референсы/"
SHOT = A + "Скриншоты 1.7/Из симулятора/afford_100.png"
RED, GRN, DARK, YEL2 = (226, 64, 64), (36, 150, 98), (24, 26, 34), (255, 214, 64)


def build():
    ep = Ep("P10_Ботинки_проба", "studio")
    ep.vgain = 1.0
    from PIL import Image as _I
    ep.avatars = {w: _I.open(RF + f"avatar_{w}.png").convert("RGBA") for w in ("kubysh", "dush")}
    pose = {n: _I.open(PZ + n + ".png").convert("RGBA") for n in
            ("k_coin_front", "k_coins_front", "k_coins_34", "k_profile", "k_close", "k_close_coin", "d2_front", "d_34", "d2_side")}
    talk = []

    def show(name, t0, t1, x, y, s, enter="hop", flip=False):
        """Поза на экране: прыжок / слэм / выезд снизу; покачивание, пока говорит хозяин позы."""
        im0 = pose[name].transpose(_I.FLIP_LEFT_RIGHT) if flip else pose[name]
        who = "kubysh" if name.startswith("k") else "dush"
        def fn(img, t, cam):
            p = seg(t, t0, t0 + 0.3); out = 1 - ease(seg(t, t1 - 0.18, t1))
            k = s * out * (back(p, 2.0) if enter != "rise" else 1.0)
            if k < 0.02: return
            dy = 0
            if enter == "hop": dy = -90 * math.sin(math.pi * p)
            if enter == "rise": dy = (1 - eout(p)) * 600
            rot = 0.0
            if any(a <= t < b and w == who for a, b, w in talk):
                rot = 2.5 * math.sin(t * 9); k *= 1 + 0.02 * math.sin(t * 17)
            k *= 1 + 0.012 * math.sin(t * 3.4)
            im = scaled(im0, k, rot); comp(img, im, x - im.width / 2, y - im.height + dy)
        ep.add(t0, t1, "screen", fn)
        ep.sfx(t0, {"hop": "boing", "slam": "thump", "rise": "whoosh"}[enter], 0.45)

    def slam(t0, t1, text, y, size, color=WHITE, shake=True):
        im = word_img(text, size, fill=color)
        def fn(img, t, cam):
            p = seg(t, t0, t0 + 0.22); out = 1 - ease(seg(t, t1 - 0.15, t1))
            k = min((2.2 - 1.2 * eout(p)) * out, 1010 / im.width)
            if k < 0.02 or p <= 0: return
            jx = 14 * math.sin(t * 90) * (1 - p) if shake else 0
            s = fade(scaled(im, k), min(1, p * 3) * out); comp(img, s, W / 2 - s.width / 2 + jx, y - s.height / 2)
        ep.add(t0, t1, "screen", fn); ep.sfx(t0 + 0.05, "thump", 0.6)

    def say(who, text, at, cap=None, y=1430, size=74):
        a, b = ep.say(who, text, cap=cap, at=at, y=y, size=size); talk.append((a, b, who)); return a, b

    ep.clip(0, 60, PZ + "bg_room.png", "фон: комната Ксюши, размыто")

    # 0 · ХУК: число + боль, Кубыш влетает крупно
    slam(0.0, 2.9, "−12 000 ₽", 430, 190, RED)
    ep.pill(0.25, 2.9, "Зимние ботинки", 540, 610, size=52, bg=DARK, fg=WHITE)
    a, b = say("kubysh", "Двенадцать тысяч на ботинки. До зарплаты не дожить?", 0.3, cap="12 000 на ботинки. До зарплаты не *дожить?*", y=1480)
    show("k_coin_front", 0.3, b + 0.1, 540, 1400, 1.7, "hop")

    # 1 · Душная (одна реплика из банка)
    t1 = b + 0.1
    a, b = say("dush", "Не доживёшь. Ходи в старых.", t1 + 0.05, cap="Не доживёшь. Ходи в *старых*", y=1480)
    show("d2_front", t1, b + 0.15, 540, 1400, 1.6, "slam")

    # 2 · КТО ТАКОЙ КУБЫШ + открытая петля
    t2 = b + 0.15
    ep.pill(t2 + 0.05, t2 + 3.6, "Кубыш — приложение для iPhone", 540, 300, size=52, bg=GRN, fg=WHITE)
    ep.pill(t2 + 0.4, t2 + 3.6, "считает, хватит ли денег до зарплаты", 540, 410, size=44)
    a, b = say("kubysh", "Я Кубыш, приложение. Считаю, хватит ли до зарплаты.", t2 + 0.1, cap="Я *Кубыш,* приложение. Считаю, хватит ли до *зарплаты*", y=1480)
    ep.pill(b - 0.6, b + 0.9, "В конце — цена в день", 540, 530, size=48, bg=(60, 50, 90), fg=WHITE)
    show("k_coins_front", t2, b + 0.9, 540, 1400, 1.55, "rise")

    # 3 · НАСТОЯЩИЙ ЭКРАН: откуда деньги
    t3 = b + 0.9
    keys = [(t3, (0, 160, 1206, 1350), 540, 700, 960), (t3 + 2.2, (40, 1120, 1170, 1750), 540, 640, 1000)]
    a, b = say("kubysh", "Смотри: четыре тысячи из бюджета на сегодня, семь из кошелька, остальное экономия.", t3 + 0.3,
               cap="*4 064* из бюджета на сегодня, *7 000* из кошелька, остальное — *экономия*", y=1240, size=70)
    ep.card(t3, b + 1.3, SHOT, keys, marks=[(t3 + 0.9, (95, 1180, 830, 1280), YEL), (a + 0.6, (100, 1440, 560, 1540), MINT),
                                             (a + 2.4, (600, 1440, 1100, 1540), MINT), (a + 3.9, (100, 1560, 560, 1650), MINT)])
    show("k_profile", t3 + 0.2, b + 1.3, 820, 1900, 1.0, "hop", flip=True)
    ep.pill(b - 0.3, b + 1.3, "Накопления не тронуты", 540, 260, size=52, bg=GRN, fg=WHITE)

    # 4 · ОТВЕТ НА ПЕТЛЮ: цена в день
    t4 = b + 1.35
    ep.pill(t4, t4 + 3.6, "Бюджет на день", 540, 300, size=46, bg=DARK, fg=WHITE)
    ep.counter(t4, t4 + 3.6, 4064, 3947, 540, 470, size=150, suffix=" ₽", dur=1.0)
    slam(t4 + 1.2, t4 + 3.6, "−117 ₽ в день", 680, 120, YEL2)
    a, b = say("kubysh", "Итого минус сто семнадцать рублей в день.", t4 + 0.6, cap="Итого *−117 ₽* в день", y=1480)
    show("k_coins_34", t4, max(b, t4 + 3.6), 540, 1400, 1.5, "slam")

    # 5 · поворот Душной + призыв голосом
    t5 = max(b, t4 + 3.6)
    a, b = say("dush", "Сто семнадцать? Я думала, конец.", t5 + 0.05, cap="*117?* Я думала, конец", y=1480)
    show("d_34", t5, b + 0.15, 540, 1400, 1.6, "hop")
    t6 = b + 0.15
    show("k_close", t6, 60, 540, 1920, 1.9, "rise")
    a, b = say("kubysh", "Спокойно до зарплаты. Напиши «жаба» в комментах, пришлю ссылку.", t6 + 0.1, y=880, size=66,
               cap="Спокойно до зарплаты. Напиши *«жаба»* в комментах, пришлю ссылку")
    end = b + 0.7
    ep.pill(t6 + 0.2, end, "Кубыш · бесплатно в App Store", 540, 300, size=50, bg=GRN, fg=WHITE)
    ep.pill(t6 + 0.6, end, "Напиши ЖАБА — пришлю ссылку", 540, 420, size=52, bg=(60, 50, 90), fg=WHITE)

    # прогресс-бар сверху: держит до конца
    def bar(img, t, cam):
        d = ImageDraw.Draw(img); d.rectangle([0, 0, W, 12], fill=(255, 255, 255, 60)); d.rectangle([0, 0, int(W * t / end), 12], fill=YEL2 + (255,))
    ep.add(0, end, "screen", bar)
    ep.dur = end
    ep.cover_t = 0.9
    return ep

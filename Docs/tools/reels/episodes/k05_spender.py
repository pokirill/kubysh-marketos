"""К5 / П9 · «Я транжира?», ~31 с. 18-е, Ксюша готова отменить заказ на 7 400; Душная на плече давит,
Кубыш проверяет: маркетплейсы выше плана на 3 100, зато кафе и доставка ниже на 5 400 — корзина закрыта экономией.
Сценарий v6 — `publications/53_Reels_scripts_v2.md`. Жабы-авторы анимированы `mascot.py` (рот, моргание).
"""
from studio import *  # noqa
from mascot import Mascot

A = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /"
CL = A + "Рилсы Ксюша/K05_клипы/"
VO = A + "Голоса/K05/"
RF = A + "Рилсы Ксюша/Референсы/"
RED, GRN, DARK = (214, 64, 64), (30, 130, 88), (24, 26, 34)


def build():
    ep = Ep("K05_Я_транжира", "studio")
    ep.vgain = 0.95
    from PIL import Image as _I
    ep.avatars = {w: _I.open(RF + f"avatar_{w}.png").convert("RGBA") for w in ("ksy", "kubysh", "dush")}
    kub = Mascot(ep, "kubysh", 840, 1900, 0.78, 0.3, 40)

    def say(who, file, cap, at, y=1400, size=78):
        a, b = ep.say(who, "", cap=cap, at=at, file=file if file.startswith("/") else VO + file, y=y, size=size)
        if who == "kubysh": kub.say(a, b)
        return a, b

    # 1 · хук: заказ почти отменён, Ксюша винит себя, Душная давит
    ep.clip(0, 5.0, CL + "S1.mp4", "S1 отмена заказа")
    ep.pill(0.1, 7.6, "18-е · заказ 7 400 · до зарплаты 7 дней", 540, 300, size=44, bg=DARK, fg=WHITE)
    ep.pill(0.4, 7.6, "Отменить заказ?", 540, 420, size=48, bg=RED, fg=WHITE)
    a, b = say("ksy", "кс1_косарей.wav", "Опять мелочей на семь *косарей.* Я транжира", 0.3)
    a, b = say("dush", "д1_корзину.wav", "Никаких *доставок.* Корзину удали. Приложение тоже", b + 0.12)
    ep.clip(5.0, b + 0.15, CL + "S1.mp4", "S1 назад", src_t0=5.0, speed=-1.0)

    # 2 · Кубыш перебивает и проверяет
    s2 = b + 0.15
    a, b = say("kubysh", "к1_стоп.wav", "*Стоп.* Обвинение серьёзное. Проверим", s2 + 0.05)
    ep.sfx(b + 0.1, "ding", 0.5); red0 = b + 0.1
    a3, b3 = say("kubysh", "к3_мимо.wav", "Зато мимо кафе и доставки весь месяц. *Минус 5 400*", b + 1.2)
    a4, b = say("kubysh", "к4_япония.wav", "Корзина закрывается этой экономией. *Япония* на месте", b3 + 0.12)
    ep.pill(red0, a4 + 0.3, "Маркетплейсы: +3 100 к плану", 540, 1080, size=50, bg=RED, fg=WHITE)
    ep.pill(a3 + 0.3, a4 + 0.3, "Кафе и доставка: −5 400 к плану", 540, 1190, size=50, bg=GRN, fg=WHITE)
    ep.pill(a4 + 0.4, b + 0.2, "Корзина закрыта экономией · Япония не тронута", 540, 1080, size=40, bg=DARK, fg=WHITE)
    ep.pill(a4 + 1.4, b + 0.2, "Хватит до 25-го", 540, 1190, size=48, bg=GRN, fg=WHITE)
    s3 = b + 0.2
    ep.clip(s2, s3, CL + "S2.mp4", "S2 удивление → улыбка", speed=10.0 / (s3 - s2))

    # 3 · развязка: курьер, «не транжира», экономия — на себя, призыв голосом
    a, b = say("ksy", "кс2_нетранжира.wav", "То есть я не *транжира?*", s3 + 0.1)
    a, b = say("kubysh", "к5_дома.wav", "Ты просто ела дома. *Экономия — на себя*", b + 0.12)
    a, b = say("kubysh", A + "Голоса/M01/к5_жаба.wav", "Спокойно до зарплаты. Напиши *«жаба»* в комментах, пришлю ссылку", b + 0.15, y=1420, size=66)
    end = b + 0.6
    ep.pill(a, end, "Спокойно до зарплаты", 540, 1000, size=56, bg=GRN, fg=WHITE)
    ep.pill(a + 0.4, end, "Кубыш · бесплатно в App Store", 540, 1110, size=44)
    ep.pill(a + 0.8, end, "Напиши ЖАБА — пришлю ссылку", 540, 1220, size=50, bg=(60, 50, 90), fg=WHITE)
    ep.clip(s3, end, CL + "S4.mp4", "S4 курьер 10 с", speed=min(1.0, 10.0 / (end - s3)))
    ep.dur = end
    ep.cover_t = 1.0
    return ep

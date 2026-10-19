"""Перевыпуск «Пиццы» 19.10 (победитель: ~2 500 в Инсте, 1 057 в Shorts за сутки): новый хук на первые 2,5 с —
число-итог «138 000 → 4 250 в день» вместо «?», прогресс-бар (движок), финал A «бесплатно» (эксперимент из 66_*)."""
from studio import *  # noqa
from episodes.v01_pizza import build as base

DARK = dict(bg=(40, 34, 30), fg=WHITE)
GREEN = dict(bg=(30, 130, 88), fg=WHITE)


def build():
    ep = base(); ep.name = "V01b_Пицца_хук2"
    ep.ov = [o for o in ep.ov if not (abs(o[0] - 0.6) < 1e-6 and abs(o[1] - 1.7) < 1e-6)]   # старый «?»
    ep.pill(0.1, 2.5, "138 000 → 4 250 в день", 540, 300, size=66, **DARK)
    ep.pill(0.5, 2.5, "Как?", 540, 420, size=80, bg=(255, 214, 74), fg=INK)
    ep.pill(ep.dur - 4.2, ep.dur, "Скачай бесплатно в App Store", 540, 1660, size=46, **GREEN)
    ep.cover_t = 1.2
    return ep

"""Перевыпуск П7 «Зарплата» 19.10 (2 352 в Инсте, 1 062 в Shorts): хук-итог «2 330 в день» первым кадром и перемотка
к пушу зарплаты (движок hook_result), прогресс-бар, финал B «Посчитай свой план за 3 минуты» (эксперимент из 66_*)."""
from studio import *  # noqa
from episodes.e07_payday import build as base


def build():
    ep = base(); ep.name = "E07b_Зарплата_хук"
    t_res = [c for c in ep.caps if "2 330" in " ".join(c["words"])][0]["t1"]
    ep.hook_result(t_res, text="2 330 в день до аванса", sub="Как это посчитать за минуту?")
    ep.pill(ep.dur - 2.6, ep.dur, "Посчитай свой план за 3 минуты", 540, 1010, size=44, bg=(30, 130, 88), fg=WHITE)
    return ep

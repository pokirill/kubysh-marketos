"""Перевыпуск К2 «Питер» 19.10 (2 403 в Инсте): холодное открытие — решение Ксюши «Сто рублей в день за Питер с
девочками? Все, я еду!» с ее голосом, перемотка к началу, дальше сюжет. Финал B (эксперимент 66_*)."""
from studio import *  # noqa
from episodes.k02_friday import build as base


def build():
    ep = base(); ep.name = "K02b_Питер_холодное_открытие"
    a = [x for x in ep.caps if any("рублей" in w for w in x["words"])][0]
    b = [x for x in ep.caps if any("еду!" in w for w in x["words"])][0]
    ep.hook_clip(a["t0"] - 0.15, b["t1"] + 0.2)
    ep.pill(ep.dur - 2.4, ep.dur, "Посчитай свой план за 3 минуты", 540, 1010, size=44, bg=(30, 130, 88), fg=WHITE)
    return ep

"""Перевыпуск «Пиццы» 19.10, v2 (Кирилл: «хук 2» почти не отличается): холодное открытие — кусок «Сегодня твой кусок —
четыре двести пятьдесят» со своим голосом Holden и кадром поднятого куска, перемотка к целой пицце, дальше сюжет.
Финал A «бесплатно» (эксперимент 66_*)."""
from studio import *  # noqa
from episodes.v01_pizza import build as base


def build():
    ep = base(); ep.name = "V01c_Пицца_холодное_открытие"
    c = [x for x in ep.caps if any("четыре" in w for w in x["words"])][0]
    ep.hook_clip(c["t0"] - 0.15, c["t1"] - 0.1)
    ep.pill(ep.dur - 4.2, ep.dur, "Скачай бесплатно в App Store", 540, 1660, size=46, bg=(30, 130, 88), fg=WHITE)
    return ep

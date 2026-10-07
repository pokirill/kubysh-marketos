"""Сравнение озвучки К1: HOOK_VO=clone (клоны ElevenLabs) | record (куски живых записей). Три героя."""
import os
from studio import *  # noqa

G = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/Клоны_пробы/"
R = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/"


def build():
    v = os.environ.get("HOOK_VO", "clone"); k = "клон" if v == "clone" else "запись"
    ext = ".mp3" if v == "clone" else ".wav"
    ep = Ep("K01_сравнение_" + k, "studio")
    ep.pill(0.0, 4.3, "Жаба душит даже за кофе", 540, 230, size=58)
    t0, t1 = ep.say("dush", "", cap="Триста девяносто за кофе? А вдруг до *аванса* не хватит?", at=0.4,
                    file=G + "Душная_хук_" + k + ext, y=1400)
    s1 = t1 + 0.3; ep.clip(0, s1, R + "K01_клипы/S1.mp4", "S1")
    a0, a1 = ep.say("ksy", "", cap="Знаешь это чувство? Десятого ты богатая, покупаешь матчу и смотришь билеты в Японию. А двадцатого уже считаешь, сколько стоит *гречка.*",
                    at=s1 + 0.2, file=G + "Ксюша_сравн_" + k + ext, y=1300, size=68)
    mid = s1 + (a1 - s1) * 0.55
    ep.clip(s1, mid, R + "K01_клипы/S2.mp4", "S2"); ep.clip(mid, a1 + 0.3, R + "K01_кадры/S2b_календарь.png", "S2b")
    b0, b1 = ep.say("kub", "", cap="Не волнуйся, я не буду тебя ругать. Давай просто посмотрим на *цифры.*",
                    at=a1 + 0.5, file=G + "Кубыш_сравн_" + k + ext, y=1300, size=70)
    ep.clip(a1 + 0.3, b1 + 0.6, R + "K01_кадры/S4_Кубыш.png", "S4")
    for c in ep.caps:
        if c["who"] == "kub": c["who"] = "kubysh"
    ep.dur = b1 + 0.6; ep.cover_t = 1.0
    return ep

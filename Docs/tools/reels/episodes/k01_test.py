"""Тест К1: хук и признание с клипами Kling и голосами ElevenLabs (закадрово, без липсинка)."""
from studio import *  # noqa

CL = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/K01_клипы/"
PR = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/Пробы голосов/"


def build():
    ep = Ep("K01_тест_голоса", "studio")
    ep.pill(0.0, 3.9, "Жаба душит даже за кофе", 540, 230, size=58)
    t0, t1 = ep.say("dush", "Триста девяносто… а вдруг до аванса не хватит?", cap="Триста девяносто… а вдруг до *аванса* не хватит?",
                    at=0.5, file=PR + "Душная_2_ElevenLabs.mp3", y=1400)
    s1 = max(4.0, t1 + 0.3); ep.clip(0, s1, CL + "S1.mp4", "S1")
    a0, a1 = ep.say("ksy", "От зарплаты до аванса я живу как на качелях.", cap="От зарплаты до аванса я живу как на *качелях*",
                    at=s1 + 0.4, file=PR + "Ксюша_3_ElevenLabs.mp3", y=1400)
    ep.clip(s1, a1 + 0.6, CL + "S2.mp4", "S2")
    ep.dur = a1 + 0.6; ep.cover_t = 1.0
    return ep

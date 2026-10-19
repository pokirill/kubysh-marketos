"""Шаблон серий Б, Т, С (`publications/66_Content_plan_from_19.10.md`, правила рилса v5):
итог первым кадром → перемотка → 3D-Кубыш «я приложение…» → проблема → запись экрана с наездами → итог → финал A/B.
Ролик — конфиг make(dict(...)), см. b*/t*/c*.py. Голос — Яндекс kirill ×1,2 (Holden только через генерацию Higgsfield).
Записи экрана — профиль 150 тыс. (`UITEST_SEED_DATA`), «Рилсы маскот/Записи_экрана_150/».
"""
from PIL import Image
from studio import *  # noqa
import audio
from episodes.k00_ad import icon

RK = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/"
REC = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы маскот/Записи_экрана_150/"
KUB = RK + "K03_клипы/C5.mp4"      # 3D-Кубыш один в кадре: вступление и проблема
BG = (14, 30, 24)
PH = (900, 540, 960, BG)
STY = {"dark": dict(bg=(24, 40, 34), fg=WHITE), "green": dict(bg=(30, 130, 88), fg=WHITE),
       "yellow": dict(bg=(255, 214, 74), fg=INK), "red": dict(bg=(170, 48, 60), fg=WHITE)}
INTRO = "Я Кубыш. Считаю, хватит ли денег до зарплаты"
CTA = {"A": ("Скачай Кубыш бесплатно в Эп Стор", "Скачай Кубыш *бесплатно* в App Store"),
       "B": ("Посчитай свой план за три минуты", "Посчитай свой план за *3 минуты*")}
Y = 1560


def make(c):
    audio.CAST = dict(audio.CAST, kubysh=("yandex", "kirill", "good", 1.2))
    ep = Ep(c["name"], "studio"); ep.sfxgain = 0.4
    ep.avatars = {"kubysh": Image.open(RK + "Референсы/avatar_kubysh.png").convert("RGBA")}

    # 1–2 · Кубыш представляется и называет проблему (клип C5, замедленный под длину реплик)
    a0, a1 = ep.say("kubysh", INTRO, y=Y, size=64, at=0.1)
    t = a1 + 0.12
    for line, pills in c["problem"]:
        b0, b1 = ep.say("kubysh", line, y=Y, size=64, at=t)
        for k, p in enumerate(pills):
            ep.pill(b0 + 0.15 + 0.45 * k, b1 + 0.25, p, 540, 380 + 115 * k, size=50, **STY["red" if k == len(pills) - 1 else "dark"])
            ep.sfx(b0 + 0.15 + 0.45 * k, "pop", 0.5)
        t = b1 + 0.12
    ep.clip(0, t, KUB, "kub", speed=min(1.0, 4.9 / t))

    # 3 · запись экрана: реплика на сегмент, наезды на нужный блок
    for s in c["screen"]:
        d0, d1 = ep.say("kubysh", s["say"], cap=s.get("cap"), y=1720, size=58, at=t + 0.1)
        dur = max(d1 + 0.25 - t, s.get("min", 0.0))
        ep.clip(t, t + dur, REC + s["rec"], s["rec"], src_t0=s["src"], speed=s.get("speed", 1.0), phone=PH)
        ep.clips[-1]["zoom"] = [(t + a, t + b, za, zb, fy) for a, b, za, zb, fy in s.get("zoom", ())]
        for a, b, text, y, st in s.get("pills", ()):
            ep.pill(t + a, t + b, text, 540, y, size=52, **STY[st]); ep.sfx(t + a, "pop", 0.5)
        ep.sfx(t, "swish", 0.5)
        t += dur

    # 4 · итог крупно (с него же начинается ролик)
    r0, r1 = ep.say("kubysh", c["result"][0], cap=c["result"][1] if len(c["result"]) > 2 else None, y=Y, size=64, at=t + 0.1)
    ep.pill(t + 0.05, r1 + 0.3, c["result"][-1], 540, 470, size=78, **STY["yellow"]); ep.sfx(t + 0.1, "ding", 0.6)
    t_res = r1 - 0.15
    t = r1 + 0.2

    # 5 · финал A/B: Кубыш представляется как приложение, призыв, слоган
    e0, e1 = ep.say("kubysh", CTA[c["cta"]][0], cap=CTA[c["cta"]][1], y=Y, size=62, at=t)
    end = e1 + 1.8
    icon(ep, e0, end, y=820, size=230)
    ep.pill(e0 + 0.1, end, "Кубыш · приложение для денег на iPhone", 540, 300, size=42, **STY["dark"])
    ep.pill(e1 - 0.2, end, "Напиши «план» — пришлю ссылку", 540, 1080, size=48, **STY["green"])
    ep.pill(e1 + 0.3, end, "Бюджет под твою жизнь, а не наоборот", 540, 1190, size=40, **STY["dark"])
    ep.clip(r0 - 0.1, end, KUB, "kub2", src_t0=4.95, speed=-min(1.0, 4.9 / (end - r0 + 0.1)))   # тот же Кубыш задом наперед: без повтора кадров
    ep.dur = end
    ep.hook_result(t_res, sub=c["hook"]); ep.hook["y"] = 640
    return ep

"""К1 · 11.10 · «Ксюша и жаба», монтаж v2 (~24 с). Клипы Kling 3.0, голоса ElevenLabs: Ксюша Xenia и Кубыш Holden
(каждый одним дублем, нарезан по паузам — тембр не гуляет), Душная — клон. Фон — «Cafe ambiance», Wikimedia Commons, CC0.
"""
from studio import *  # noqa
import audio

R = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/"
CL, FR = R + "K01_клипы/", R + "K01_кадры/"
VO = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/K01v2/"
AMB = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/Фон/cafe_45s.wav"
SH = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Скриншоты 1.7/Из симулятора/"


def build():
    ep = Ep("K01_Ксюша_и_жаба", "studio")
    ep.vgain = 0.95
    REF = R + "Референсы/"
    from PIL import Image as _I
    ep.avatars = {w: _I.open(REF + f"avatar_{w}.png").convert("RGBA") for w in ("ksy", "kubysh", "dush")}

    # 1 · хук
    ep.pill(0.0, 2.6, "Жаба душит даже за кофе", 540, 760, size=72)
    t0, t1 = ep.say("dush", "", cap="Триста девяносто… а вдруг не *хватит?*", at=0.25, file=VO + "д1_хук.mp3", y=1400)
    s1 = t1 + 0.15; ep.clip(0, s1, CL + "S1.mp4", "S1")

    # 2 · качели
    a0, a1 = ep.say("ksy", "", cap="От зарплаты до аванса как на *качелях*", at=s1 + 0.1, file=VO + "кс1_качели.wav", y=1400)
    mid = s1 + 1.3; ep.clip(s1, mid, FR + "S2_признание.png", "S2")
    ep.clip(mid, a1 + 0.15, FR + "S2b_календарь.png", "S2b"); ep.sfx(mid, "swish", 0.35)

    # 3 · нарезка отказов: по 2 с на кадр, Душная объясняет, почему
    m0 = a1 + 0.15
    ep.clip(m0, m0 + 2.0, CL + "S3a.mp4", "S3a"); ep.pill(m0 + 0.1, m0 + 1.95, "Обед с коллегами? Нет, контейнер", 540, 330, size=46, bg=(60, 50, 90), fg=WHITE)
    ep.clip(m0 + 2.0, m0 + 4.0, CL + "S3b.mp4", "S3b"); ep.pill(m0 + 2.1, m0 + 3.95, "Корзина? Удалить", 540, 330, size=50, bg=(60, 50, 90), fg=WHITE)
    ep.sfx(m0, "swish", 0.3); ep.sfx(m0 + 2.0, "swish", 0.3)
    ep.say("dush", "", cap="А вдруг… а вдруг не *хватит*…", at=m0 + 0.6, file=VO.replace("K01v2", "K01") + "3_душная_авдруг.mp3", y=1400)
    m1 = m0 + 4.0

    # 4 · Кубыш: одна цифра на сегодня
    b0, b1 = ep.say("kubysh", "", cap="Смотри. Сегодня у тебя *4 100.* И ты в *плюсе.*", at=m1 + 0.2, file=VO + "к1_смотри.wav", y=170, size=74)
    ep.clip(m1, m1 + 1.0, CL + "S4.mp4", "S4")
    s5 = b1 + 0.3; ep.clip(m1 + 1.0, s5, CL + "S5.mp4", "S5")
    ep.card(m1 + 1.0, s5, SH + "free_day_100.png", keys=[(m1 + 1.0, (20, 380, 1190, 780), 540, 860, 960)],
            marks=[(b0 + 1.6, (616, 420, 882, 726), YEL), (b0 + 3.0, (906, 420, 1176, 726), MINT)])

    # 5 · решение, оплата и доказательство: дата Японии не двигается
    c0, c1 = ep.say("ksy", "", cap="Тогда латте. *Большой.*", at=s5 + 0.15, file=VO + "кс2_латте.wav", y=1400)
    pay = c1 + 0.15; ep.sfx(pay, "beep", 0.6)
    d0, d1 = ep.say("kubysh", "", cap="Япония уже *отложена.*", at=pay + 0.35, file=VO + "к2_япония.wav", y=170, size=74)
    ep.card(pay + 0.1, d1 + 0.5, SH + "сим_цели_96.png", keys=[(pay + 0.1, (40, 1920, 1280, 2490), 540, 820, 940)],
            marks=[(pay + 0.4, (100, 2355, 300, 2435), YEL)])
    s6 = d1 + 0.5; ep.clip(s5, s6, CL + "S6.mp4", "S6")

    # 6 · панчлайн
    e0, e1 = ep.say("dush", "", cap="*Так!* Кто разрешил?", at=s6 + 0.1, file=VO + "д2_так.mp3", y=1400)
    f0, f1 = ep.say("kubysh", "", cap="Тут решают *не жабы.*", at=e1 + 0.2, file=VO + "к3_нежабы.wav", y=1400)
    ep.clip(s6, e1 + 0.15, CL + "S6.mp4", "S6b", src_t0=3.5)
    ep.clip(e1 + 0.15, f1 + 0.3, CL + "S4.mp4", "S4b", src_t0=2.0)

    # 7 · финал: Кубыш представляется
    s7 = f1 + 0.3
    g0, g1 = ep.say("kubysh", "", cap="Я *Кубыш.* Бюджет под твою *жизнь,* а не наоборот.", at=s7 + 0.3, file=VO + "к4_финал.wav", y=1400, size=70)
    ep.clip(s7, g1 + 1.2, CL + "S7.mp4", "S7")
    ep.pill(s7 + 0.4, g1 + 1.2, "Копи на цели без вреда для жизни", 540, 330, size=50)
    ep.pill(s7 + 1.0, g1 + 1.2, "Кубыш · бесплатно до следующей зарплаты", 540, 450, size=40, bg=(30, 130, 88), fg=WHITE)
    ep.dur = g1 + 1.2; ep.cover_t = 1.0
    amb = audio.load(AMB)[:int(ep.dur * audio.SR)]
    ep.extra = [(0.0, ep.duck(amb, depth=0.22), 0.3)]
    return ep

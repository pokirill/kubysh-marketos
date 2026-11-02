"""К1 · вт 03.11 18:00 · «Карта не прошла» (сценарий 82, v3). Жабы на риге, голоса Holden + клон Душной, герой за кадром в чате."""
from PIL import Image
from studio import *  # noqa
import props as P
import audio
from episodes import infog
from episodes.scr import STY, RK
from episodes.lib import PHONE
import promo_hero as PH

V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
Y = 1560


def build():
    ep = Ep("W03_K1_Карта_не_прошла", "store"); ep.sfxgain = 0.5
    ep.avatars = {w: Image.open(RK + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("kubysh", "dush")}
    kub = ep.actor("kub", "kubysh", 800, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)

    def say(a, f, cap, at, size=62):
        t0, t1 = ep.say(a.who, "", cap=cap, at=at, y=Y, size=size, file=V + f + "_f_48k.wav")
        smp = ep.voice[-1][1]; env = audio.envelope(smp, FPS); e = ep.env.setdefault(a.name, [0.0] * int(400 * FPS)); f0 = int(t0 * FPS)
        for i, v in enumerate(env):
            if f0 + i < len(e): e[f0 + i] = max(e[f0 + i], v)
        return t0, t1

    # 1 · касса: отказ
    kub.expr(0, "shock"); kub.react(0.3, "shudder"); ep.shot(0, "kub", z=1.3)
    ep.stamp(0.15, 2.6, P.word_stamp("ОТКАЗ", (214, 36, 52)), 540, 640)
    ep.sfx(0.15, "boom", 0.6)
    ep.chat(0.5, "me", "Отказ. До зарплаты еще 5 дней. Пи**ец", t1=3.2)
    ep.pill(0.9, 3.2, "до зарплаты 5 дней", 540, 1000, size=50, **STY["red"])
    # 2 · Душная в очереди
    dush.show(1.9); dush.go(1.9, 270, hop=60, step=300); dush.expr(1.9, "dush")
    a0, a1 = say(dush, "w1_dush", "Выложи сыр. И колбасу. И себя *выложи обратно*", at=2.6)
    ep.shot(a0, ("dush", "kub"), dur=0.4); kub.expr(a0 + 0.3, "worried")
    # 3 · отмотка на 10 дней назад: листок
    tb = a1 + 0.3
    ep.set(tb, "night_lamp", fade=0.2); ep.sfx(tb, "whoosh", 0.6)
    ep.pill(tb, tb + 1.6, "10 дней назад", 540, 330, size=54, **STY["yellow"])
    b0, b1 = say(kub, "w1_flash", "10 дней назад. Ты посчитал на листке, и все сходилось. А про *бар и подарок маме* забыл", at=tb + 0.2)
    ep.shot(b0, "wide"); kub.expr(b0, "talk"); dush.go(b0, -380, hop=60, step=320)
    note = P.notes_card([("Остаток", "24 000"), ("До зарплаты", "10 дней"), ("В день", "2 400")], w=760, h=520)
    def paper(img, t, cam, t0=b0, t1=b1 + 0.2):
        k = back(seg(t, t0, t0 + 0.35)) * (1 - ease(seg(t, t1 - 0.2, t1)))
        if k > 0.02: im = scaled(note, 0.9 * k); comp(img, im, 540 - im.width / 2, 640 - im.height / 2)
    ep.add(b0, b1 + 0.2, "screen", paper)
    ep.chat(b0 + (b1 - b0) * 0.55, "me", "Бл**ь, я же с пацанами в бар в субботу. И у мамы ДР", t1=b1 + 0.2)
    ep.pill(b0 + (b1 - b0) * 0.65, b1 + 0.2, "бар ≈ 4 000", 330, 900, size=48, **STY["red"])
    ep.pill(b0 + (b1 - b0) * 0.75, b1 + 0.2, "подарок маме ≈ 5 000", 650, 1000, size=48, **STY["red"])
    # 4 · тот же вечер, но с Кубышем
    c0, c1 = say(kub, "w1_count", "Давай посчитаем вместе. Бар и подарок маме я учел. Оптимально примерно *1 500 в день,* и до зарплаты хватает", at=b1 + 0.35)
    kub.expr(c0, "proud"); ep.shot(c0, "kub", z=1.15)
    for k, (txt, st, y) in enumerate([("бар и подарок маме учтены", "dark", 560), ("≈ 1 500 ₽ в день", "green", 720), ("до зарплаты хватает", "green", 880)]):
        tk = c0 + (c1 - c0) * (0.35 + 0.25 * k); ep.pill(tk, c1 + 0.25, txt, 540, y, size=58, **STY[st]); ep.sfx(tk, "pop", 0.4)
    # 5 · снова касса, через 10 дней
    td = c1 + 0.3
    ep.set(td, "store", fade=0.2); ep.sfx(td, "swish", 0.5)
    ep.pill(td, td + 1.4, "10 дней спустя", 540, 330, size=54, **STY["yellow"])
    ep.stamp(td + 0.2, td + 2.6, P.word_stamp("ОПЛАЧЕНО", (36, 168, 96)), 540, 640); ep.sfx(td + 0.2, "kaching", 0.5)
    dush.place(td, 270); dush.expr(td, "dush_mad"); dush.go(td + 0.8, -380, hop=60, step=320)
    kub.expr(td + 0.2, "happy"); ep.shot(td, "wide")
    d0, d1 = say(kub, "w1_poor", "Ты не нищий. Ты просто *считал без бара*", at=td + 0.5)
    # 6 · финал
    f0, f1 = say(kub, "w_final", "Я Кубыш, приложение на айфон. *Считаю за тебя*", at=d1 + 0.45)
    end = f1 + 1.6
    ep.clip(f0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - f0)))
    ep.pill(f1 - 0.4, end, "Комфортно сегодня, спокойно завтра", 540, 1190, size=46, **STY["green"]); ep.sfx(f1 - 0.4, "pop", 0.4)
    ep.dur = end; ep.cover_t = 0.8
    return ep

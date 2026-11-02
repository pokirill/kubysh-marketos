"""К1 · вт 03.11 18:00 · «Карта не прошла» (сценарий 82, v3, правки Кирилла 02.11).
Касса — фон Higgsfield (кассирша и терминал), голоса: кассирша Vera, герой за кадром Archie (мат запикан),
Кубыш Holden, Душная клон. Душная упрощена: серая жаба в очках (frog.DUSH_SIMPLE)."""
from PIL import Image
from studio import *  # noqa
import props as P
import audio
import frog
from episodes.scr import STY, RK
from episodes.lib import PHONE

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
BG = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы маскот/W03_K1_Карта_не_прошла/касса.png"
Y, SZ = 1100, 54


def build():
    ep = Ep("W03_K1_Карта_не_прошла", "store"); ep.sfxgain = 0.5
    ep.avatars = {w: Image.open(RK + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("kubysh", "dush")}
    ep.extra = []
    kub = ep.actor("kub", "kubysh", 800, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.58, mirror=True, hidden=True, pointer=False) if False else ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)

    def say(who, f, cap, at, a=None):
        t0, t1 = ep.say(who, "", cap=cap, at=at, y=Y, size=SZ, file=V + f + "_f_48k.wav")
        if a is not None:
            smp = ep.voice[-1][1]; env = audio.envelope(smp, FPS); e = ep.env.setdefault(a.name, [0.0] * int(400 * FPS)); f0 = int(t0 * FPS)
            for i, v in enumerate(env):
                if f0 + i < len(e): e[f0 + i] = max(e[f0 + i], v)
        return t0, t1

    # 1 · касса: писк сканера, ошибка терминала, кассирша
    ep.extra.append((0.0, audio.load(V + "kassa_err.wav"), 0.5))
    kub.expr(0, "neutral"); ep.shot(0, "wide")
    c0, c1 = say("cashier", "cashier", "Оплата не прошла. Недостаточно средств", at=0.75)
    ep.stamp(0.85, c1 + 0.4, P.word_stamp("ОТКАЗ", (214, 36, 52)), 540, 860)
    h0, h1 = say("hero", "w1_hero1", "Отказ? До зарплаты еще *5 дней.* Пи**ец", at=c1 + 0.15)
    kub.expr(h0, "shock"); kub.react(h0 + 0.2, "shudder")
    ep.pill(h0 + 0.5, h1 + 0.3, "до зарплаты 5 дней", 540, 330, size=50, **STY["red"])
    # 2 · Душная в очереди
    dush.show(h1 - 0.4); dush.go(h1 - 0.4, 280, hop=60, step=300); dush.expr(h1 - 0.4, "dush")
    a0, a1 = say("dush", "w1_dush", "Выложи сыр. И колбасу. И себя *выложи обратно*", at=h1 + 0.2, a=dush)
    ep.shot(a0, ("dush", "kub"), dur=0.4); kub.expr(a0 + 0.3, "worried")
    ep.clip(0, a1 + 0.3, BG, "касса")
    # 3 · отмотка на 10 дней назад: листок
    tb = a1 + 0.3
    ep.set(tb, "night_lamp", fade=0.2); ep.sfx(tb, "whoosh", 0.6)
    ep.pill(tb, tb + 1.6, "10 дней назад", 540, 330, size=54, **STY["yellow"])
    dush.go(tb, -380, hop=60, step=320)
    b0, b1 = say("kubysh", "w1_flash2", "10 дней назад. Ты посчитал на листке, и все *сходилось*", at=tb + 0.2, a=kub)
    ep.shot(b0, "wide"); kub.expr(b0, "talk")
    note = P.notes_card([("Остаток", "24 000"), ("До зарплаты", "10 дней"), ("В день", "2 400")], w=760, h=520)
    g0, g1 = say("hero", "w1_hero2", "Бл**ь, я же с пацанами *в бар* в субботу. И у мамы *день рождения*", at=b1 + 0.15)
    def paper(img, t, cam, t0=b0, t1=g1 + 0.2):
        k = back(seg(t, t0, t0 + 0.35)) * (1 - ease(seg(t, t1 - 0.2, t1)))
        if k > 0.02: im = scaled(note, 0.9 * k); comp(img, im, 540 - im.width / 2, 560 - im.height / 2)
    ep.add(b0, g1 + 0.2, "screen", paper)
    ep.pill(g0 + 0.6, g1 + 0.2, "бар ≈ 4 000", 330, 860, size=50, **STY["red"]); ep.sfx(g0 + 0.6, "pop", 0.4)
    ep.pill(g0 + (g1 - g0) * 0.65, g1 + 0.2, "подарок маме ≈ 5 000", 650, 950, size=50, **STY["red"]); ep.sfx(g0 + (g1 - g0) * 0.65, "pop", 0.4)
    kub.expr(g0, "worried")
    # 4 · тот же вечер, Кубыш считает
    d0, d1 = say("kubysh", "w1_count2", "Смотри. С баром и подарком выходит примерно *1 500 в день.* И до зарплаты хватает", at=g1 + 0.35, a=kub)
    kub.expr(d0, "proud"); ep.shot(d0, "kub", z=1.15)
    ep.pill(d0 + (d1 - d0) * 0.4, d1 + 0.25, "≈ 1 500 ₽ в день", 540, 600, size=64, **STY["green"]); ep.sfx(d0 + (d1 - d0) * 0.4, "pop", 0.4)
    ep.pill(d0 + (d1 - d0) * 0.8, d1 + 0.25, "до зарплаты хватает", 540, 760, size=54, **STY["dark"]); ep.sfx(d0 + (d1 - d0) * 0.8, "pop", 0.4)
    # 5 · снова касса, через 10 дней
    td = d1 + 0.3
    ep.sfx(td, "swish", 0.5); ep.extra.append((td + 0.3, audio.load(V + "kassa_ok.wav"), 0.5))
    ep.pill(td, td + 1.6, "10 дней спустя", 540, 330, size=54, **STY["yellow"])
    ep.stamp(td + 0.45, td + 2.6, P.word_stamp("ОПЛАЧЕНО", (36, 168, 96)), 540, 860); ep.sfx(td + 0.45, "kaching", 0.5)
    dush.place(td, 280); dush.expr(td, "dush_mad"); dush.go(td + 0.9, -380, hop=60, step=320)
    kub.expr(td + 0.3, "happy"); ep.shot(td, "wide")
    e0, e1 = say("kubysh", "w1_poor", "Ты не нищий. Ты просто *считал без бара*", at=td + 0.6, a=kub)
    # 6 · финал
    f0, f1 = say("kubysh", "w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=e1 + 0.45)
    ep.clip(td, f0 - 0.05, BG, "касса2")
    end = f1 + 1.4
    ep.clip(f0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - f0)))
    ep.pill(f0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, 1190, size=46, **STY["green"]); ep.sfx(f0 + 1.0, "pop", 0.4)
    ep.dur = end; ep.cover_t = 1.4
    return ep

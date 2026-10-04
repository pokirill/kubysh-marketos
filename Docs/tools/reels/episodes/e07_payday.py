"""П7 · 10.10 · «Зарплата». Душная требует гречку, зритель хочет нормально, Кубыш раскладывает план вместе с ним."""
from studio import *  # noqa
import props as P


def build():
    ep = Ep("E07_Зарплата", "room")
    kub = ep.actor("kub", "kubysh", 1320, s=0.7)
    dush = ep.actor("dush", "dush", -320, s=0.7, mirror=True, hidden=True)
    ep.notif(0.0, 2.4, "Банк", "Зачисление зарплаты +55 928 ₽")
    ep.coins(0.25, n=24, dur=1.8)
    ep.chat(0.6, "me", "ЗАРПЛАТА!", t1=3.4, y0=420)
    ep.shot(0, "wide", z=1.08)
    dush.show(1.4); dush.go(1.4, 230, hop=100, step=300); dush.expr(1.4, "teacher")
    ep.prop(2.2, 99, P.buckwheat(), 470, 1575, anim="drop", s=0.8)
    t0, t1 = ep.line("dush", "Отложи всё до копейки. До ав+анса *гречка.*", cap="Отложи все до копейки. До аванса *гречка*", at=2.3)
    ep.shot(t0, "dush")
    ep.chat(t1 + 0.2, "me", "А можно как-то нормально?", t1=t1 + 2.8, y0=190)
    kub.go(t1 + 0.6, 820, hop=150, step=320); kub.expr(t1, "neutral")
    ep.cursor = t1 + 1.5
    t0, t1 = ep.line("kub", "Давай разложим *вм+есте.*")
    ep.shot(t0, ("dush", "kub"), dur=0.3); kub.expr(t0, "proud")
    shot = "Из симулятора/plan.png"
    tc = t1 + 0.25
    ep.shot(tc, "wide", z=1.04)
    for a in (kub, dush): a.look(tc + 0.3, ("screen", 520, 720))
    ep.cursor = tc + 0.45
    a0, a1 = ep.line("kub", "Сначала обязательные, потом *накопл+ения.*", y=170, size=76)
    b0, b1 = ep.line("kub", "На жизнь остаётся *две тысячи триста тридцать* в день.", cap="На жизнь остается *2 330* в день", y=170, size=76)
    ep.card(tc, b1 + 0.4, shot,
            keys=[(tc, (0, 330, 1206, 2200), 520, 820, 540), (a0 + 0.1, (20, 1320, 1190, 2160), 520, 760, 960)],
            marks=[(a0 + 0.3, (40, 1700, 1180, 1830), MINT), (a0 + 1.2, (40, 2025, 1180, 2140), MINT), (b0 + 0.4, (240, 1400, 960, 1530), YEL)])
    ep.counter(b0 + 0.8, b1 + 0.4, 0, 2330, 540, 1270, size=140)
    for a in (kub, dush): a.look(b1 + 0.3, None)
    ep.cursor = b1 + 0.4
    t0, t1 = ep.line("kub", "Это твой план. Поменяется жизнь, поменяется и *он.*")
    ep.shot(t0, "kub", z=1.3, dur=0.4); kub.expr(t0, "talk")
    ep.chat(t1 + 0.2, "me", "2 330 в день… посмотрим", t1=t1 + 3.6)
    dush.expr(t1, "skeptic")
    te = t1 + 1.4
    ep.shot(te, "wide", dur=0.4)
    ep.pill(te, te + 2.6, "Тебе обычно хватает до аванса?", 540, 640, size=50)
    ep.pill(te + 0.3, te + 2.6, "ДА", 400, 770, size=70, bg=(36, 168, 96), fg=(255, 255, 255))
    ep.pill(te + 0.45, te + 2.6, "НЕТ", 680, 770, size=70, bg=(214, 44, 60), fg=(255, 255, 255))
    ep.pill(te + 0.7, te + 2.6, "Пиши в комментах", 540, 890, size=40)
    ep.dur = te + 2.7; ep.cover_t = 1.0
    return ep

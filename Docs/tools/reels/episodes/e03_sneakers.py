"""П3 · 06.10 · «Кроссовки». Кубыш не разрешает: показывает цену решения (−117 ₽ в день), зритель решает сам."""
from studio import *  # noqa
import props as P


def build():
    ep = Ep("E03_Кроссовки", "store")
    dush = ep.actor("dush", "dush", -320, s=0.66, mirror=True, hidden=True)
    kub = ep.actor("kub", "kubysh", 1320, s=0.66)
    ep.prop(0, 99, P.sneaker(), 540, 1238, anim="none", s=0.9)
    ep.prop(0.4, 99, P.price_tag(), 770, 1110, anim="pop", s=0.9)
    ep.chat(0.0, "me", "Кроссовки за 12 000. Хочу. Но страшно", t1=4.6)
    ep.shot(0, (540, 1130), z=1.55); ep.shot(0.9, (540, 1200), z=1.2, dur=0.5)
    dush.show(0.8); dush.go(0.8, 150, hop=120, step=320); dush.expr(0.8, "teacher")
    t0, t1 = ep.line("dush", "Ходи в старых. Им всего *три г+ода.*", at=1.5)
    ep.shot(t0, "dush")
    kub.go(t1 + 0.05, 900, hop=150, step=320); kub.expr(t1, "neutral")
    ep.cursor = t1 + 0.85
    t0, t1 = ep.line("kub", "Давай посчитаем, что будет, если *куп+ить.*")
    ep.shot(t0, ("dush", "kub"), dur=0.3); kub.expr(t0, "proud")
    shot = "Из симулятора/afford_100.png"
    tc = t1 + 0.25
    ep.shot(tc, "wide", z=1.04)
    for a in (kub, dush): a.look(tc + 0.3, ("screen", 520, 700))
    ep.cursor = tc + 0.45
    a0, a1 = ep.line("kub", "Двенадцать тысяч *есть.*", cap="*12 000* есть", y=170, size=78)
    b0, b1 = ep.line("kub", "В день станет на сто семнадцать рублей *м+еньше.*", cap="В день станет на *117 ₽* меньше", y=170, size=76)
    ep.card(tc, b1 + 0.4, shot,
            keys=[(tc, (0, 330, 1206, 2400), 520, 800, 560), (a0 + 0.1, (60, 1150, 1180, 1820), 520, 700, 960)],
            marks=[(a0 + 0.3, (90, 1175, 760, 1285), YEL), (a0 + 0.9, (90, 1420, 1120, 1640), MINT), (b0 + 0.4, (90, 1700, 1120, 1790), YEL)])
    for a in (kub, dush): a.look(b1 + 0.2, None)
    ep.cursor = b1 + 0.3
    t0, t1 = ep.line("kub", "Дорого это или нет, решать *теб+е.*", cap="Дорого это или нет, решать *тебе*")
    ep.shot(t0, "kub", z=1.3, dur=0.4); kub.expr(t0, "talk")
    ep.chat(t1 + 0.2, "me", "Сто рублей в день за новые кроссовки? Беру", t1=t1 + 3.8)
    kub.expr(t1 + 0.8, "happy"); ep.prop(t1 + 0.8, t1 + 2.6, P.sparkle(), 440, 1110, anim="pop", s=0.8)
    ep.cursor = t1 + 2.0
    t0, t1 = ep.line("dush", "Три г+ода им было…", cap="Три года им было…")
    ep.shot(t0, "dush"); dush.expr(t0, "worried")
    te = t1 + 0.3
    ep.shot(te, "wide", dur=0.4)
    ep.pill(te, te + 2.3, "А ты что не купил из-за жабы?", 540, 520, size=46)
    ep.pill(te + 0.3, te + 2.3, "Завтра: «когда-нибудь» не дата", 540, 640, size=50, bg=(30, 130, 88), fg=(255, 255, 255))
    ep.dur = te + 2.4; ep.cover_t = 0.5
    return ep

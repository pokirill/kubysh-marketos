"""П6 · 09.10 · «2 ночи». Душная шепчет страхи, Кубыш включает свет и считает. Зритель выдыхает. Анонс зарплаты."""
from studio import *  # noqa
import props as P


def build():
    ep = Ep("E06_Тревога", "night")
    kub = ep.actor("kub", "kubysh", 830, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)
    kub.expr(0, "worried")
    for t in (0.0, 1.0, 2.0, 3.0): ep.sfx(t, "heartbeat", 0.6)
    ep.chat(0.0, "me", "02:00. Не сплю. Хватит ли до зарплаты?", t1=5.0)
    ep.shot(0, "kub", z=1.35)
    dush.show(0.9); dush.go(0.9, 260, hop=60, step=300); dush.expr(0.9, "teacher")
    t0, t1 = ep.line("dush", "А вдруг *не хв+атит?* А подписки? А день рождения *м+амы?*", at=1.6)
    ep.shot(t0, ("dush", "kub"), dur=0.4); kub.react(t0 + 1.0, "shudder")
    ep.pill(t0 + 1.0, t1 + 0.6, "подписки 899 ₽", 330, 680, size=40, bg=(60, 50, 90), fg=(255, 255, 255))
    ep.pill(t0 + 1.7, t1 + 0.6, "ДР мамы", 760, 600, size=40, bg=(60, 50, 90), fg=(255, 255, 255))
    ep.pill(t0 + 2.2, t1 + 0.6, "ЖКХ 6 400 ₽", 560, 800, size=40, bg=(60, 50, 90), fg=(255, 255, 255))
    ep.sticker(t0 + 0.6, t1 + 1.0, P.sweat(), "kub", dx=150, dy=0)
    t0, t1 = ep.line("kub", "Давай не *гад+ать.*")
    ep.shot(t0, "kub"); kub.expr(t0, "proud")
    ep.set(t0 + 0.4, "night_lamp", fade=0.12); ep.sfx(t0 + 0.38, "tick", 0.8)
    dush.expr(t0 + 0.5, "worried")
    shot = "Из симулятора/chat_enough_100.png"
    tc = t1 + 0.25
    ep.shot(tc, "wide", z=1.04); ep.chat_clear(tc)
    for a in (kub, dush): a.look(tc + 0.3, ("screen", 540, 720))
    ep.cursor = tc + 0.45
    a0, a1 = ep.line("kub", "Хватит на *восемь дней.* До получки как раз восемь.", cap="Хватит на *8 дней.* До получки как раз *8*", y=170, size=72)
    ep.card(tc, a1 + 0.4, shot, keys=[(tc, (20, 1280, 1186, 1770), 540, 720, 960)], marks=[(a0 + 0.5, (30, 1505, 1150, 1600), YEL)])
    for a in (kub, dush): a.look(a1 + 0.2, None)
    ep.chat(a1 + 0.4, "me", "Фух. Можно спать", t1=a1 + 3.4)
    kub.expr(a1 + 0.9, "happy")
    ep.set(a1 + 1.4, "night", fade=0.3); ep.sfx(a1 + 1.4, "tick", 0.7)
    dush.go(a1 + 1.3, -380, hop=60, step=320)
    kub.expr(a1 + 1.6, "sleepy"); ep.sticker(a1 + 1.7, a1 + 3.2, P.zzz(), "kub", dx=170, dy=-80)
    tt = a1 + 2.8
    ep.title(tt, tt + 3.0, [("ЗАВТРА", (255, 255, 255)), ("ЗАРПЛАТА", (255, 214, 74))], sub=["у многих 10-го числа", "разложим ее без паники"])
    ep.dur = tt + 3.0; ep.cover_t = 1.2
    return ep

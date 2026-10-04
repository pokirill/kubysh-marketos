"""П1 · 04.10 · «Жаба душит». Корзина на маркетплейсе висит две недели, а по темпу зритель в плюсе. Решает сам."""
from studio import *  # noqa
import props as P


def build():
    ep = Ep("E01_Жаба_не_душит", "room")
    kub = ep.actor("kub", "kubysh", 700, s=0.74)
    dush = ep.actor("dush", "dush", -320, s=0.7, mirror=True, hidden=True)

    # хук: Макс жалуется, Кубыш впрыгивает
    ep.chat(0.0, "me", "В корзине на маркетплейсе мелочей на 2 300", t1=5.6)
    ep.chat(0.7, "me", "Две недели не оформляю. Жалко денег", t1=5.6)
    kub.place(0, 1260); kub.go(0.05, 700, hop=150, step=300, dur=0.36); kub.expr(0, "skeptic")
    t0, t1 = ep.line("kub", "Жаба *д+ушит?* Знакомо.", at=0.65)
    ep.shot(t0, "wide", z=1.1, dur=0.6)
    t0, t1 = ep.line("kub", "Я тоже жаба. Только я не *душ+у,* я *считаю.*")
    ep.shot(t0, "kub"); kub.expr(t0, "smug"); kub.react(t0 + 0.1, "nod")
    kub.spit_catch(t1 + 0.05)
    ep.shot(t1 + 0.05, (kub.x_at_end(t1) - 60, 820), z=1.18, dur=0.3)
    ep.shot(t1 + 0.75, "kub", dur=0.2); ep.shake(t1 + 0.78, 6)
    ep.chat_clear(t1 + 0.8)
    ep.cursor = t1 + 0.85

    # экран «Получки»: темп в плюсе, до получки хватает
    shot = "Из симулятора/free_day_100.png"
    t0, t1 = ep.line("kub", "Давай посмотрим.")
    tc = t0
    ep.shot(tc, "wide", z=1.04); kub.go(tc, 900, hop=70); kub.expr(tc + 0.4, "proud")
    kub.look(tc + 0.4, ("screen", 520, 720))
    a0, a1 = ep.line("kub", "По темпу ты в *плюсе* на четыре с половиной тысячи.", cap="По темпу ты в *плюсе* на *4 500*", y=170, size=76)
    b0, b1 = ep.line("kub", "И до получки *хватает.*", y=170, size=76)
    ep.card(tc + 0.2, b1 + 0.5, shot,
            keys=[(tc + 0.2, (0, 0, 1206, 1500), 500, 820, 620), (a0 + 0.1, (20, 380, 1190, 780), 500, 760, 960)],
            marks=[(a0 + 0.6, (906, 420, 1176, 726), YEL), (b0 + 0.2, (326, 420, 592, 726), MINT)])
    ep.counter(a0 + 0.7, b0 + 0.2, 0, 4500, 440, 1080, size=150, prefix="+")
    kub.look(b1 + 0.3, None)

    # поворот: зритель понимает, что зря себе отказывал
    tm = b1 + 0.35
    ep.chat(tm, "me", "Подожди. Я себе во всем отказываю, а я в плюсе?", t1=tm + 5.3)
    kub.expr(tm + 0.5, "worried")
    ep.cursor = tm + 1.6
    t0, t1 = ep.line("kub", "Бывает. Голова всегда считает с запасом на *худшее.*")
    ep.shot(t0, "kub", z=1.3, dur=0.4); kub.expr(t0, "talk")
    ep.chat(t1 + 0.4, "me", "Оформляю корзину", t1=t1 + 4.5)
    kub.expr(t1 + 0.7, "happy"); kub.jump(t1 + 0.7, h=110, dur=0.42)
    ep.sticker(t1 + 0.8, t1 + 2.0, P.sparkle(), "kub", dx=150, dy=-30)

    # Душная
    td = t1 + 1.3
    ep.shot(td - 0.1, "wide")
    kub.go(td - 0.1, 780, hop=50); kub.expr(td, "smug")
    dush.show(td); dush.go(td, 190, hop=60, step=260); dush.expr(td, "angry")
    t0, t1 = ep.line("dush", "*Так!* Кто *разреш+ил?*", at=td + 0.55)
    ep.shot(t0, "dush"); dush.react(t0, "puff")
    t0, t1 = ep.line("kub", "Никто. Тут решают *не жабы.*", gap=0.1)
    ep.shot(t0, "kub"); kub.look(t0, "dush"); kub.expr(t0, "proud")
    te = t1 + 0.3
    ep.shot(te, ("dush", "kub"), dur=0.4); dush.expr(te, "skeptic")
    ep.pill(te + 0.1, te + 2.3, "Кубыш · жаба, которая не душит", 540, 520, size=48)
    ep.pill(te + 0.3, te + 2.3, "Завтра: знакомься, Душная", 540, 640, size=52, bg=(112, 28, 52), fg=(255, 255, 255))
    ep.dur = te + 2.4
    ep.cover_t = 1.6
    return ep

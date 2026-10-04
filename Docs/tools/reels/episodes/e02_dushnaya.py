"""П2 · 05.10 · «Сорвался». Душная: гречка и вода. Кубыш: один дорогой день еще не провал, с завтра 3 658 в день."""
from studio import *  # noqa
import props as P


def build():
    ep = Ep("E02_Душная_жаба", "classroom")
    dush = ep.actor("dush", "dush", 300, s=0.76, mirror=True, pointer=True)
    kub = ep.actor("kub", "kubysh", 1300, s=0.72)
    dush.expr(0, "teacher")
    ep.chat(0.0, "me", "Перерасход 2 836 ₽. Все, конец?", t1=5.2)
    ep.shot(0, "wide", z=1.1)
    t0, t1 = ep.line("dush", "Перерасх+од? Значит, до зарпл+аты *гречка* и вода.", at=0.8)
    ep.shot(t0, "dush"); dush.expr(t0 + 0.6, "skeptic")
    ep.chalk(t0 + 1.0, "Гречка + вода", 130, 640, 76)
    ep.stamp(t1 - 0.2, 99, P.grade_stamp("2"), 840, 640, rot=-12, world=True)
    ep.chat(t1 + 0.2, "me", "Может, она права…", t1=t1 + 2.6)
    tk = t1 + 1.0
    kub.go(tk, 790, hop=150, step=320); kub.expr(tk, "neutral")
    ep.cursor = tk + 0.8
    t0, t1 = ep.line("kub", "Один дорогой день ещё не *пров+ал.* Смотри.", cap="Один дорогой день еще не *провал.* Смотри.")
    ep.shot(t0, ("dush", "kub"), dur=0.3); kub.expr(t0, "proud")
    shot = "Из симулятора/overspend_explainer_100.png"
    tc = t1 + 0.2
    ep.shot(tc, "wide", z=1.04)
    for a in (kub, dush): a.look(tc + 0.3, ("screen", 520, 760))
    ep.cursor = tc + 0.45
    a0, a1 = ep.line("kub", "Я разложил перерасх+од на оставшиеся дни.", cap="Я разложил *2 836* на оставшиеся дни", y=170, size=72)
    b0, b1 = ep.line("kub", "С завтра *три шестьсот пятьдесят восемь* в день. И до получки хватает.", cap="С завтра *3 658* в день. И до получки *хватает*", y=170, size=72)
    ep.card(tc, b1 + 0.4, shot,
            keys=[(tc, (0, 120, 1206, 1950), 520, 820, 560), (a0 + 0.1, (30, 430, 1180, 900), 520, 720, 960)],
            marks=[(a0 + 0.5, (40, 720, 1160, 880), MINT), (b0 + 0.4, (50, 545, 420, 680), YEL)])
    ep.counter(b0 + 0.5, b1 + 0.4, 0, 3658, 540, 1080, size=150)
    for a in (kub, dush): a.look(b1 + 0.2, None)
    ep.chat(b1 + 0.3, "me", "То есть гречка не обязательна?", t1=b1 + 3.4)
    ep.cursor = b1 + 1.5
    t0, t1 = ep.line("kub", "Только если ты *её л+юбишь.*", cap="Только если ты ее *любишь*")
    ep.shot(t0, "kub"); kub.expr(t0, "smug", wink="R")
    t0, t1 = ep.line("dush", "*Непедагог+ично.*")
    ep.shot(t0, "dush"); dush.expr(t0, "skeptic")
    t0, t1 = ep.line("kub", "Зато *спок+ойно.*", gap=0.1)
    ep.shot(t0, "kub"); kub.expr(t0, "proud")
    te = t1 + 0.3
    ep.shot(te, ("dush", "kub"), dur=0.4)
    ep.pill(te, te + 2.3, "Кого слушаешь ты: Душную или Кубыша?", 540, 520, size=44)
    ep.pill(te + 0.3, te + 2.3, "Завтра: кроссовки за 12 000", 540, 640, size=52, bg=(30, 130, 88), fg=(255, 255, 255))
    ep.dur = te + 2.4; ep.cover_t = 1.6
    return ep

"""П4 · 07.10 · «Когда-нибудь». Календарь листает годы, Кубыш находит настоящую дату цели."""
from studio import *  # noqa
import props as P

PAGES = [("ОКТЯБРЬ", "?"), ("НОЯБРЬ", "?"), ("ДЕКАБРЬ", "?"), ("ЯНВАРЬ", "?"), ("МАРТ", "?"), ("ИЮНЬ", "?"), ("2029", "?"), ("2033", "?"), ("2040", "?")]


def build():
    ep = Ep("E04_Когда_нибудь", "room")
    kub = ep.actor("kub", "kubysh", 780, s=0.72)
    dush = ep.actor("dush", "dush", -320, s=0.7, mirror=True, hidden=True)
    sprites = {p: P.calendar(*p) for p in PAGES + [("ФЕВРАЛЬ", "10"), ("ФЕВРАЛЬ", "14")]}
    st = {"stop": 99, "shift": 99}

    def cal(img, t, cam):
        if t < st["stop"]:
            page = PAGES[int(max(0, t - 0.3) * 6) % len(PAGES)] if t > 0.3 else PAGES[0]
            wob = 3 * math.sin(t * 20) if t > 0.3 else 0
        else:
            page = ("ФЕВРАЛЬ", "14") if t >= st["shift"] else ("ФЕВРАЛЬ", "10"); wob = 0
        z = cam[2]; s = scaled(sprites[page], 0.8 * z, wob); sx, sy = to_screen(cam, 300, 1000)
        comp(img, s, sx - s.width / 2, sy - s.height)
        if t >= st["stop"]:
            q = eout(seg(t, st["stop"] + 0.2, st["stop"] + 0.55)); d = ImageDraw.Draw(img)
            cx, cy = to_screen(cam, 300, 880); r = 95 * z
            d.arc([cx - r, cy - r * 0.9, cx + r, cy + r * 0.9], start=200, end=200 + 380 * q, fill=(220, 40, 52, 255), width=int(10 * z))
    ep.add(0, 99, "back", cal)

    ep.chat(0.0, "me", "Хочу новый айфон. Когда-нибудь", t1=4.4)
    ep.shot(0, (300, 900), z=1.5); ep.shot(1.0, "wide", z=1.08, dur=0.4)
    ep.sfx(0.3, "swish", 0.3); ep.sfx(0.8, "swish", 0.3)
    dush.show(0.6); dush.go(0.6, 170, hop=100, step=300); dush.expr(0.6, "teacher")
    t0, t1 = ep.line("dush", "Когда-нибудь значит *никогд+а.*", at=1.3)
    ep.shot(t0, "dush")
    t0, t1 = ep.line("kub", "Когда-нибудь не дата. Давай найдём *насто+ящую.*", cap="«Когда-нибудь» не дата. Давай найдем *настоящую.*")
    ep.shot(t0, "kub"); kub.expr(t0, "proud")
    shot = "Из симулятора/goals_top_100.png"
    tc = t1 + 0.3
    ep.shot(tc, "wide", z=1.04); ep.chat_clear(tc)
    for a in (kub, dush): a.look(tc + 0.3, ("screen", 600, 700))
    ep.cursor = tc + 0.45
    a0, a1 = ep.line("kub", "Новый айфон: *десятое февраля* двадцать седьмого.", cap="Новый айфон: *10 февраля 2027*", y=170, size=76)
    st["stop"] = a0 + 0.6; ep.sfx(a0 + 0.6, "thump", 0.4)
    b0, b1 = ep.line("kub", "Если до получки выйдет дороже, дата *подв+инется,* и ты это сразу увидишь.",
                     cap="Если до получки выйдет дороже, дата *подвинется,* и ты это сразу увидишь", y=150, size=64)
    st["shift"] = b0 + 1.4; ep.sfx(b0 + 1.4, "swish", 0.3)
    ep.card(tc, b1 + 0.3, shot,
            keys=[(tc, (0, 700, 1320, 2560), 600, 800, 560), (a0 + 0.1, (40, 1690, 1280, 2250), 600, 700, 880)],
            marks=[(a0 + 0.5, (90, 2095, 360, 2195), YEL)])
    for a in (kub, dush): a.look(b1 + 0.2, None)
    ep.chat(b1 + 0.3, "me", "Февраль… это же почти скоро", t1=b1 + 3.4)
    kub.expr(b1 + 0.8, "happy")
    ep.cursor = b1 + 1.6
    t0, t1 = ep.line("dush", "Подозр+ительно реально.")
    ep.shot(t0, "dush"); dush.expr(t0, "skeptic")
    te = t1 + 0.3
    ep.shot(te, "wide", dur=0.4)
    ep.pill(te, te + 2.3, "На что копишь ты? Пиши цель", 540, 520, size=48)
    ep.pill(te + 0.3, te + 2.3, "Завтра: 47 трат в заметках", 540, 640, size=50, bg=(30, 130, 88), fg=(255, 255, 255))
    ep.dur = te + 2.4; ep.cover_t = 0.9
    return ep

"""К4 · ср 04.11 18:00 · «Корзина» (сценарий 82, v3). Жабы на риге, графика корзины и «Прикинуть покупку» кодом.
Голоса: герой Archie (мат запикан), Душная клон, Кубыш Holden."""
from PIL import Image, ImageDraw
from studio import *  # noqa
import props as P
import promo_hero as PH
import audio
import frog
from episodes.scr import STY, RK
from episodes.lib import PHONE

frog.DUSH_SIMPLE = True
V = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W04/"
V3 = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/W03/"
Y, SZ = 1100, 54
SNK = P.sneaker()


def cart_card(t, ordered_t, del_t):
    """Корзина маркетплейса: кроссовки, 14 дней в корзине, кнопка «Оформить» (качели), после — «Заказ оформлен»."""
    cv = Image.new("RGBA", (900, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(cv)
    d.rounded_rectangle([0, 0, 899, 559], 44, fill=(255, 255, 255, 250))
    d.text((40, 36), "Корзина", font=PH.font("Bold", 50), fill=(20, 20, 24))
    d.rounded_rectangle([40, 120, 300, 380], 30, fill=(242, 243, 247))
    s = SNK.copy(); s.thumbnail((230, 230)); cv.alpha_composite(s, (170 - s.width // 2, 250 - s.height // 2))
    d.text((330, 140), "Кроссовки", font=PH.font("SemiBold", 44), fill=(20, 20, 24))
    d.text((330, 200), "12 000 ₽", font=PH.font("Bold", 60), fill=(20, 20, 24))
    d.rounded_rectangle([330, 290, 640, 346], 28, fill=(255, 236, 236)); d.text((485, 318), "в корзине 14 дней", font=PH.font("SemiBold", 30), fill=(200, 40, 50), anchor="mm")
    if t >= ordered_t:
        d.rounded_rectangle([40, 420, 860, 520], 36, fill=(30, 160, 96)); d.text((450, 470), "Заказ оформлен", font=PH.font("Bold", 46), fill=(255, 255, 255), anchor="mm")
    else:
        sw = 0.5 + 0.5 * math.sin(t * 7)   # качели: кнопка то тянет, то отпускает
        col = (120 + int(80 * sw), 60, 200) if t < del_t else (200, 40, 50)
        d.rounded_rectangle([40, 420, 860, 520], 36, fill=col); d.text((450, 470), "Оформить" if t < del_t else "Удалить?", font=PH.font("Bold", 46), fill=(255, 255, 255), anchor="mm")
    return cv


def afford_card(t, t0):
    cv, pad = PH.card(940, 640, 40, glow=PH.GREEN); d = ImageDraw.Draw(cv); x0, y0 = pad + 40, pad + 34
    d.text((x0, y0), "Прикинуть покупку", font=PH.font("Bold", 46), fill=PH.WHITE)
    d.text((x0, y0 + 70), "Кроссовки · 12 000 ₽", font=PH.font("Medium", 38), fill=PH.SUB)
    rows = [("из кошелька", "10 000", PH.AMBER), ("из бюджета дня", "2 000", PH.BLUE)]
    for i, (a, b, c) in enumerate(rows):
        if t < t0 + 0.6 + 0.4 * i: continue
        yy = y0 + 140 + i * 90; d.rounded_rectangle([x0, yy, x0 + 860, yy + 74], 20, fill=(30, 40, 37))
        d.rounded_rectangle([x0 + 20, yy + 16, x0 + 32, yy + 58], 6, fill=c)
        d.text((x0 + 56, yy + 37), a, font=PH.font("SemiBold", 38), fill=PH.WHITE, anchor="lm"); d.text((x0 + 836, yy + 37), b, font=PH.font("Bold", 40), fill=PH.WHITE, anchor="rm")
    if t >= t0 + 2.0:
        v = round(lerp(2400, 2100, eio(seg(t, t0 + 2.0, t0 + 2.8))) / 10) * 10
        d.text((x0, y0 + 340), "в день", font=PH.font("Medium", 36), fill=PH.SUB)
        d.text((x0, y0 + 384), f"{v:,} ₽".replace(",", " "), font=PH.font("Bold", 80), fill=PH.GREEN)
        d.text((x0 + 330, y0 + 410), "было 2 400", font=PH.font("Medium", 34), fill=PH.SUB)
    if t >= t0 + 4.4:
        d.line([(x0 + 4, y0 + 530), (x0 + 18, y0 + 544), (x0 + 42, y0 + 514)], fill=PH.GREEN, width=7)
        d.text((x0 + 60, y0 + 530), "Отпуск остается в мае", font=PH.font("SemiBold", 40), fill=PH.WHITE, anchor="lm")
    return cv


def build():
    ep = Ep("W04_K4_Корзина", "room"); ep.sfxgain = 0.5
    ep.avatars = {w: Image.open(RK + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("kubysh", "dush")}
    kub = ep.actor("kub", "kubysh", 800, s=0.66)
    dush = ep.actor("dush", "dush", -320, s=0.64, mirror=True, hidden=True)

    def say(who, f, cap, at, a=None, v=V):
        t0, t1 = ep.say(who, "", cap=cap, at=at, y=Y, size=SZ, file=v + f + "_t_48k.wav")
        if a is not None:
            smp = ep.voice[-1][1]; env = audio.envelope(smp, FPS); e = ep.env.setdefault(a.name, [0.0] * int(400 * FPS)); f0 = int(t0 * FPS)
            for i, x in enumerate(env):
                if f0 + i < len(e): e[f0 + i] = max(e[f0 + i], x)
        return t0, t1

    # 1 · хук: качели «Оформить»
    kub.expr(0, "worried"); ep.shot(0, "wide")
    h0, h1 = say("hero", "h4a", "Оформить или нет? Две недели, бл**ь, *думаю*", at=0.15)
    # 2 · Душная
    dush.show(h1 - 0.3); dush.go(h1 - 0.3, 270, hop=60, step=300); dush.expr(h1 - 0.3, "dush_mad")
    a0, a1 = say("dush", "d4a", "Удали корзину. Удали приложение. И телефон выкинь *нах**", at=h1 + 0.15, a=dush)
    ep.shot(a0, ("dush", "kub"), dur=0.4); ep.shake(a1 - 0.5, 14)
    # 3 · страх
    b0, b1 = say("hero", "h4b", "Хочется пи**ец. Но страшно: а вдруг до зарплаты *не хватит*", at=a1 + 0.2)
    ep.pill(b0 + 1.4, b1 + 0.2, "до зарплаты 9 дней", 540, 900, size=54, **STY["red"]); ep.sfx(b0 + 1.4, "pop", 0.4)
    T_ord = 999.0
    # 4 · Кубыш прикидывает
    c0, _ = say("kubysh", "k4a1", "Давай прикинем. Возьмем *из кошелька*", at=b1 + 0.3, a=kub)
    _, _ = say("kubysh", "k4a2", "На день будет примерно *2 100* вместо 2 400", at=None, a=kub)
    _, c1 = say("kubysh", "k4a3", "Отпуск остается в мае. *Решать тебе*", at=None, a=kub)
    kub.expr(c0, "proud"); dush.expr(c0, "skeptic"); ep.shot(c0, "wide")
    ep.add(c0, c1 + 0.3, "screen", lambda img, t, cam: comp(img, fade(afford_card(t, c0), eout(seg(t, c0, c0 + 0.4)) * (1 - ease(seg(t, c1 + 0.1, c1 + 0.3)))), 540 - 500, 200))
    for k in (0.6, 1.0, 2.0, 4.4): ep.sfx(c0 + k, "pop", 0.4)
    # 5 · решение: оформил, Душная в обмороке
    T_ord = c1 + 0.6
    ep.sfx(T_ord, "kaching", 0.6); kub.expr(T_ord, "happy")
    dush.expr(T_ord, "shock"); dush.react(T_ord + 0.1, "recoil"); dush.go(T_ord + 0.3, 200, hop=0, step=200)
    ep.stamp(T_ord + 0.1, T_ord + 1.6, P.word_stamp("ОФОРМЛЕНО", (36, 168, 96)), 540, 920)
    d0, d1 = say("kubysh", "k4b", "Решил ты. Цифры просто показали, *во что это обойдется*", at=T_ord + 0.5, a=kub)
    # 6 · поворот: Душная приходит в себя
    e0, e1 = say("dush", "d4b", "А *43-й размер* остался?", at=d1 + 0.3, a=dush)
    dush.expr(e0, "smug"); dush.react(e0, "lean"); ep.shot(e0, "dush", z=1.3); kub.expr(e0 + 0.4, "laugh")
    ep.add(0, T_ord + 1.8, "screen", lambda img, t, cam: None if c0 - 0.1 < t < c1 + 0.4 else comp(img, fade(cart_card(t, T_ord, a0 + 0.3), eout(seg(t, 0, 0.35)) * (1 - ease(seg(t, T_ord + 1.5, T_ord + 1.8)))), 90, 200))
    ep.sfx(0.1, "ding", 0.4)
    # 7 · финал
    f0, f1 = say("kubysh", "w_final2", "Я Кубыш, приложение на айфон. *Комфортно сегодня, спокойно завтра*", at=e1 + 0.5, v=V3)
    end = f1 + 1.4
    for a in (kub, dush): a.show(f0 - 0.05, False)
    ep.clip(f0 - 0.05, end, PHONE, "kub_cta", speed=min(1.0, 4.9 / (end - f0)))
    ep.pill(f0 + 1.0, end, "Комфортно сегодня, спокойно завтра", 540, 1420, size=46, **STY["green"]); ep.sfx(f0 + 1.0, "pop", 0.4)
    ep.dur = end; ep.cover_t = 1.0
    return ep

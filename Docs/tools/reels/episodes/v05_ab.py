"""V5 · «Найди отличие» (серия «Осознанно = круто», разделенный экран, петля). Одна зарплата 138 000, две Ксюши.
А — «отложу, что останется», Б — Кубыш в день зарплаты сразу откладывает 40 000 (подушка и Япония), остальное по 4 250 в
день (числа как в «Пицце»). Радости одинаковые, разница — мелочи без радости, которые А не заметила. Финал: Кубыш
представляется как приложение, «напиши „план“», вопрос «Ты А или Б?». Уроки V1 из 53_Reels_scripts_v2.md.
"""
from PIL import Image, ImageDraw
from studio import *  # noqa

R = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/"
K2C, K3C, K4C, V5C = R + "K02_клипы/", R + "K03_клипы/", R + "K04_клипы/", R + "V05_клипы/"
VS = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Голоса/V_серия/"
DARK = dict(bg=(60, 50, 90), fg=WHITE)
GREEN = dict(bg=(30, 130, 88), fg=WHITE)
RED = dict(bg=(160, 44, 64), fg=WHITE)
BANK = dict(icon="₽", color=(52, 120, 246))


def half(ep, t0, t1, path, src=0.0, top=True, speed=1.0, pause=False):
    """Половина экрана: середина клипа 9:16 (1080×960) сверху (А) или снизу (Б).
    pause=True — стоп-кадр и легкое затемнение: сюжет сейчас в другой половине."""
    c = dict(t0=t0, t1=t1, path=path, label="half", src=src, speed=0.0 if pause else speed, frames=None, phone=None)
    def fn(img, t, cam):
        f = ep._clip_frame(c, t).crop((0, 480, 1080, 1440))
        if pause:
            k = 0.5 * eio(seg(t, t0, t0 + 0.3)); f = Image.blend(f, Image.new("RGB", f.size, (0, 0, 0)), k)
        img.paste(f.convert(img.mode), (0, 0 if top else 960))
    ep.add(t0, t1, "back", fn)


def build():
    ep = Ep("V05_Найди_отличие", "studio")
    ep.vgain = 0.95; ep.sfxgain = 0.4
    ep.avatars = {w: Image.open(R + f"Референсы/avatar_{w}.png").convert("RGBA") for w in ("ksy", "kubysh", "dush")}
    CY = 930  # подписи на линии раздела

    # 1 · хук: одна зарплата, две Ксюши
    a0, a1 = ep.say("kubysh", "", cap="Одна зарплата — *138 000.* Две Ксюши. Найди *отличие*", at=0.2, file=VS + "ab1f.wav", y=CY, size=64)
    s2 = a1 + 0.2
    half(ep, 0, s2, K3C + "C1.mp4", 0.0, True); half(ep, 0, s2, K3C + "C1.mp4", 0.0, False)
    ep.notif(0.1, s2, "Банк", "Зачисление зарплаты +138 000 ₽", icon="₽", color=(52, 120, 246))

    # 2 · Б: Кубыш сразу откладывает; А: «отложу, что останется»
    b0, b1 = ep.say("kubysh", "", cap="Внизу я в день зарплаты сразу отложил *сорок тысяч:* подушка и Япония. Остальное — по *4 250* в день",
                    at=s2 + 0.1, file=VS + "ab2f.wav", y=CY, size=58)
    s3 = b1 + 0.2
    half(ep, s2, s3, K3C + "C1.mp4", s2, True, pause=True); half(ep, s2, s3, V5C + "G1.mp4", 0.0, False)
    ep.pill(s2 + 1.2, s3, "Отложено 40 000", 540, 1700, size=52, **GREEN); ep.sfx(s2 + 1.2, "kaching", 0.5)
    ep.pill(s2 + 4.6, s3, "4 250 в день", 540, 1800, size=44, **DARK)
    ep.pill(s2 + 0.6, s3, "Отложу, что останется", 540, 760, size=44, **RED)

    # 3 · радости одинаковые
    c0, c1 = ep.say("kubysh", "", cap="Радости *одинаковые:* суши, караоке, бар", at=s3 + 0.1, file=VS + "ab3f.wav", y=CY, size=64)
    s4 = c1 + 0.15; m = (s3 + s4) / 2
    half(ep, s3, m, K3C + "C2.mp4", 0.2, True); half(ep, s3, m, K3C + "C2.mp4", 0.2, False)
    half(ep, m, s4, K4C + "C7.mp4", 0.3, True); half(ep, m, s4, K4C + "C7.mp4", 0.3, False)
    ep.pill(s3 + 0.3, s4, "Те же суши и караоке", 540, 1700, size=46, **GREEN)

    # 4 · сверху — мелочи без радости
    d0, d1 = ep.say("kubysh", "", cap="Только сверху еще *такси, доставки и корзины,* которых она даже не заметила", at=s4 + 0.1, file=VS + "ab4f.wav", y=CY, size=58)
    s5 = d1 + 0.2
    half(ep, s4, s5, K3C + "C2.mp4", 2.4, True); half(ep, s4, s5, K4C + "C7.mp4", 0.3 + (s4 - m), False, pause=True)
    leaks = [(s4 + 0.3, "Такси −640 ₽"), (s4 + 0.9, "Доставка −890 ₽"), (s4 + 1.5, "Маркетплейс −2 300 ₽"), (s4 + 2.1, "Такси −580 ₽"), (s4 + 2.7, "Доставка −1 100 ₽")]
    for i, (t, txt) in enumerate(leaks):
        ep.pill(t, s5, txt, 300 if i % 2 == 0 else 780, 140 + 110 * (i // 2) + (55 if i % 2 else 0), size=38, **RED); ep.sfx(t, "tick", 0.15)

    # 5 · итог: А — пустая банка и Душная, Б — полная банка
    e0, e1 = ep.say("dush", "", cap="Ничего… с аванса отложишь. *Как всегда*", at=s5 + 0.1, file=VS + "д_аванс.mp3", y=CY, size=64)
    q = e0 + 1.5; s6 = e1 + 0.2
    half(ep, s5, q, K2C + "S1b.mp4", 0.6, True); half(ep, q, s6, K2C + "S1b.mp4", 3.3, True, speed=0.9)
    half(ep, s5, s6, V5C + "G4.mp4", 0.0, False, pause=True)
    f0, f1 = ep.say("kubysh", "", cap="Радости те же. Разница — отложить *в день зарплаты,* а не «что останется»", at=s6 + 0.1, file=VS + "ab5f.wav", y=CY, size=58)
    s7 = f1 + 0.4
    half(ep, s6, s7, V5C + "G3.mp4", 0.0, True); half(ep, s6, s7, V5C + "G4.mp4", 1.6, False)
    ep.pill(s5 + 0.2, s7, "Отложено: 0", 540, 760, size=56, **RED)
    ep.pill(s5 + 0.4, s7, "Отложено: 40 000", 540, 1700, size=56, **GREEN)

    # разметка А/Б и линия раздела — весь сплит
    def split(img, t, cam):
        ImageDraw.Draw(img).rectangle([0, 954, W, 966], fill=(255, 255, 255))
    ep.add(0, s7, "screen", split)
    ep.pill(0.2, s7, "А", 70, 70, size=60, **RED)
    ep.pill(0.2, s7, "Б", 70, 1860, size=60, **GREEN)

    # 6 · бренд, призыв и вопрос
    g0, g1 = ep.say("kubysh", "", cap="Я — *Кубыш,* приложение для денег на айфоне. Напиши в комментариях слово *«план»* — пришлю ссылку",
                    at=s7 + 0.2, file=VS + "бренд_f.wav", y=1400, size=64)
    loop0 = g1 + 1.4
    ep.clip(s7, loop0 + 0.9, K3C + "C5.mp4", "C5", src_t0=0.4)
    from episodes.k00_ad import icon as _icon
    _icon(ep, g0, loop0, y=700, size=240)
    ep.pill(g0 + 0.2, loop0, "Кубыш · приложение для денег на iPhone", 540, 330, size=42, **DARK)
    ep.pill(g0 + 2.6, loop0, "Напиши в комментариях «план»", 540, 440, size=46, **GREEN)
    ep.pill(g1 - 0.4, loop0, "А ты — А или Б?", 540, 1650, size=64, bg=(255, 214, 74), fg=INK)
    ep.dur = loop0 + 0.9
    ep.cover_t = 1.0
    return ep

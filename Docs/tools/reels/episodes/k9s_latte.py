"""Ксюша «Латте не отменяю» (сегмент Ксюша, тест 27.10–02.11): кинокадры Higgsfield (кофейня, календарь с сакурой),
инфографика плана. Цель — подушка + Япония (аналитика: цель без подушки не удерживает). Финал: VARIANT A/B."""
import os
from episodes.story import make
from episodes.lib import TALK, LAUGH
from episodes import infog
import promo_hero as P

K = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Ксюша/K9s_клипы/"
CTA_ = os.environ.get("VARIANT", "B")
PLAN = dict(income=138000, daily=3000, days=15, rows=[("Обязательное", "аренда · коммуналка · связь", 60000, P.BLUE),
            ("Подушка", "по плану", 15000, P.GREEN), ("Япония", "к сакуре", 18000, P.AMBER)])


def build():
    return make("K9s_Латте_и_Япония", [
        dict(who="ksy", vo="fk_hook", cap="Каждый день беру латте. И лечу в Японию к сакуре. *Как?*", vis=[(K + "coffee.mp4", 0.0, 1.0)]),
        dict(who="ksy", vo="fk_loss", cap="Сакура цветёт две недели в году. *Я пропустила уже две*", vis=[(K + "calendar_sad.mp4", 0.0, 0.9)]),
        dict(who="kubysh", vo="k9_intro", cap="Я Кубыш, приложение на айфон. Помогаю копить на цели, *не урезая привычные траты*", vis=[(TALK, 0.0, 0.9)]),
        dict(who="kubysh", vo="fk_plan", size=56, cap="С каждой зарплаты Япония и подушка по плану. А на жизнь — сумма на день. *Латте в ней уже учтён*",
             vis=[], fn=lambda ep, a, b: infog.plan(ep, a, b, PLAN)),
        dict(who="kubysh", vo="fk_guilt", cap="Тратишь *без вины.* Копишь по плану", vis=[],
             fn=lambda ep, a, b: infog.chips(ep, a, b, [("≈ 3 000 ₽ на день", P.GREEN), ("Япония: весна, сакура", P.AMBER)])),
        dict(who="ksy", vo="fk_mine", cap="В этот раз *сакура — моя*", vis=[(K + "calendar_date3.mp4", 0.3, 1.0)]),
        dict(who="kubysh", vo="m2s_slogan", cap="*Комфортно сегодня, спокойно завтра*", vis=[(LAUGH, 0.5, 0.9)]),
    ], CTA_, "")

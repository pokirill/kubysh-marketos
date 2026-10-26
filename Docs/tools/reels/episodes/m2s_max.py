"""Макс «До зарплаты без кредитки» (сегмент Макс, тест 27.10–02.11). Кинокадры Higgsfield (кухня, ящик), готовый клип
кредитки, инфографика плана вместо записи экрана. Голос Макса — Archie (за кадром), Кубыш — Holden. Финал: VARIANT A/B."""
import os
from episodes.story import make
from episodes.lib import TALK, LAUGH
from episodes import infog
import promo_hero as P

M = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы Макс/"
CTA_ = os.environ.get("VARIANT", "A")
PLAN = dict(income=60000, daily=1800, days=15, rows=[("Обязательное", "половина аренды · кредитка · связь", 27000, P.BLUE), ("В подушку", "сразу, с зарплаты", 6000, P.GREEN)])


def build():
    return make("M2s_Без_кредитки", [
        dict(who="max", vo="m2s_hook", cap="До зарплаты ещё 2 дня, а деньги остались. Могу *отложить или потратить на ништяки*",
             vis=[(M + "M2s_клипы/kitchen.mp4", 0.0, 1.0)], pills=[(0.0, "≈ 1 800 ₽ на день · хватит до 5-го", 200, "green")]),
        dict(who="kubysh", vo="m2s_intro", cap="Я Кубыш, приложение на айфон. Помогаю *комфортно жить до зарплаты* и накопить на подушку", vis=[(TALK, 0.0, 0.9)]),
        dict(who="max", vo="m2s_past", cap="Раньше к двадцатому пусто. *И снова кредитка*",
             vis=[(M + "M1b_клипы/C1_кредитка.mp4", 0.0, 0.7)], pills=[(0.0, "месяц назад · 20-е · на карте 240 ₽", 200, "red")]),
        dict(who="kubysh", vo="m2s_plan", size=56, cap="После каждой зарплаты у тебя план: обязательное, накопления в подушку, а остальное — *сумма на день.* Примерно 1 800, и к двадцатому не пусто",
             vis=[], fn=lambda ep, a, b: infog.plan(ep, a, b, PLAN)),
        dict(who="kubysh", vo="m2s_pod", cap="И подушка копится *по плану*", vis=[],
             fn=lambda ep, a, b: infog.chips(ep, a, b, [("Хватит до 5-го", P.GREEN), ("Подушка: +6 000 каждый месяц", P.GREEN)])),
        dict(who="max", vo="m2s_drawer", cap="Кредитка в ящике. *А подушка уже копится*", vis=[(M + "M2s_клипы/drawer.mp4", 0.0, 1.0)]),
        dict(who="kubysh", vo="m2s_slogan", cap="*Комфортно сегодня, спокойно завтра*", vis=[(LAUGH, 0.5, 0.9)]),
    ], CTA_, "")

"""Т3 «Формула слетела» (финал A). Холодное открытие — «Ни одной формулы, а цифра на сегодня всегда точная».
Проблема — таблица: строка сдвинулась, итоги в «#ЗНАЧ!». Решение — трата 450 → «Идешь с запасом, осталось 1 490» (R10)."""
from episodes.story import make
from episodes.meta import broken_excel
from episodes.lib import TALK

REC = "/Users/kirillpopov/Documents/Кубыш доки и артефакты /Рилсы маскот/Записи_экрана_150/"


def build():
    return make("T3_Формула", [
        dict(who="kubysh", vo="t3_hook", cap="Вечер ушел на то, чтобы вспомнить, *как это считалось*", vis=[], fn=lambda ep, a, b: broken_excel(ep, a, b, "broken")),
        dict(who="kubysh", vo="t3_problem", cap="Ведешь бюджет в таблице. Одна строка сдвинулась, и *формулы слетели*", vis=[],
             fn=lambda ep, a, b: broken_excel(ep, a, b, "ok", shift_t=a + 1.6)),
        dict(who="kubysh", vo="t3_intro", cap="Я Кубыш, приложение на айфон. Считаю бюджет за тебя, *без формул*", vis=[(TALK, 0.0, 0.9)]),
        dict(who="kubysh", vo="t3_solution", size=56,
             cap="Ты вносишь зарплату и обязательные, я делю остаток *на дни до получки.* Внес трату, и сразу видно, *сколько осталось* на сегодня",
             vis=[(REC + "R10_трата_450.mp4", 11.0, 1.0, 1)]),
        dict(who="kubysh", vo="t3_result", cap="Ни одной формулы. А цифра на сегодня *всегда точная*", vis=[(REC + "R10_трата_450.mp4", 20.0, 0.5, 1)], hook=True,
             pills=[(0.0, "Осталось на сегодня 1 490", 1420, "green")]),
    ], "A", "Сколько формул нужно для бюджета?")

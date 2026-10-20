"""С1 «Одометр и навигатор» (финал A). Обычное приложение — одометр (сколько уже потратил), Кубыш — навигатор: ведет к
целям и после каждой зарплаты показывает прогнозные даты (запись R4: цели). Итог — «когда ты будешь у цели»."""
from episodes.scr import make
from episodes.meta import odometer, navigator, analytics_then_nav
from episodes.lib import TALK, LAUGH


def build():
    return make(dict(
        name="C1_Навигатор", cta="A", intro_v2=True, hook_y=1460, kub_intro=TALK, kub_cta=LAUGH,
        hook="Что должно показывать приложение для денег",
        vo={"problem0": "c1v2_problem", "insert": "c1v2_solution", "result": "c1v2_result2"},
        problem=[("Обычное приложение как одометр: показывает только, сколько уже потратил", [])],
        problem_cap="Обычное приложение как *одометр:* показывает только, сколько уже потратил",
        problem_fn=lambda ep, t0, t1: odometer(ep, t0, t1),
        insert=dict(say="Я тоже показываю, куда ушли деньги. Но главное, веду к целям и после каждой зарплаты показываю, когда ты до них доедешь",
                    cap="Я тоже показываю, *куда ушли деньги.* Но главное, веду *к целям* и после каждой зарплаты показываю, когда ты до них доедешь",
                    fn=lambda ep, t0, t1: analytics_then_nav(ep, t0, t1), split=0.8, rec="R4_цели.mp4", src=0.5),
        screen=[],
        result=("Видишь не только, куда ушли деньги, но и когда будешь у цели", "Видишь не только, куда ушли деньги, но и *когда будешь у цели*", ""),
        result_fn=lambda ep, t0, t1: navigator(ep, t0, t1),
    ))

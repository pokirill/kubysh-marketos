# ASO 1.6.1 — «финансовый навигатор: спокойно до получки и к целям» (15.09.2026)

Решение основателя 15.09.2026: поднять скачивания из стора. Первая редакция ушла радикально в
накопления — Кирилл поправил в тот же день:

> Мы решаем боль людей со стрессом — за счёт плана до получки и ежедневных актуальных метрик.
> Продавать нужно экран «Получка»: с ним человек взаимодействует постоянно, он даёт спокойствие
> и понятные цифры, с которыми идёшь к целям. Цели — долгосрочная мотивация не бросать приложение.

Заменяет русскую и английскую карточку из iOS `Docs/ASO_V1.6.1.md` (там остаётся «Что нового»).

## Иерархия обещания (порядок во всех полях)

1. **Спокойствие** — меньше переживать из-за денег (топ-запрос опроса).
2. **«Получка»** — план до получки за пару минут и каждый день понятные цифры: сколько можно
   сегодня, хватает ли до зарплаты, темп. Ежедневный экран, главный аргумент.
3. **Цели** — ради чего это всё: план с каждой получки ведёт к отпуску, подушке, ремонту.
   Долгосрочная мотивация, а не первое обещание.

Навигатор объединяет оба уровня: маршрут до получки (дорога сегодня) и к целям (пункт назначения).

## Гипотеза влияния (метрик-гейт)

Число установок из поиска App Store. База 14.08–12.09: показы ~220/день, просмотры страницы
13/день (11 из поиска), конверсия «страница → загрузка» ~50%, первые загрузки ~50–60/нед.
Ставка: обещание «спокойно до получки» + готовый план сразу поднимает конверсию страницы, а ключи
«накопления/копить/лимит» добавляют показы там, где лидеры по учёту трат не стоят.
Замер через 7 и 14 дней после выхода 1.6.1. Откат подзаголовка, если показы < 200/день через 14 дней.

## Рамка текста (проверено об MANIFEST.md, PRODUCT.md, JOBS.md)

- Эмоция важнее функции; против таблиц и пустого приложения, а не против других приложений.
- Никаких цен, подписки, оплаты (App Store 3.1.1), абсолютных чисел, штампов.
- Экономию не связываем с целями (iOS `AGENTS.md` п. 12): цели копятся ПЛАНОМ с каждой получки.

## Порядок блоков ниже (скрипт записи в ASC читает их по порядку)

1. RU subtitle 2. RU keywords 3. RU promo 4. RU description
5. EN subtitle 6. EN keywords 7. EN promo 8. EN description

```
Навигатор до получки и к целям
```

```
накопления,копилка,копить,подушка,учет,расходов,трат,зарплата,контроль,деньги,лимит,кубышка
```

```
Меньше переживать из-за денег: Кубыш строит план до получки и каждый день показывает, сколько можно тратить и хватает ли до зарплаты. А цели копятся по плану.
```

```
Кубыш - финансовый навигатор, с которым спокойнее жить от получки до получки. Каждый день видно, сколько можно потратить сегодня и хватает ли денег до зарплаты. А план с каждой получки ведет к тому, чего ты хочешь: отпуск, подушка, ремонт, машина.

ПЛАН ДО ПОЛУЧКИ ЗА ПАРУ МИНУТ
Не нужно заполнять пустое приложение и разбираться в таблицах. Ответь на несколько вопросов про доход, обязательные платежи и цели - Кубыш сразу соберет план под тебя: бюджет на каждый день, обязательные платежи и сколько отложить с этой получки.

КАЖДЫЙ ДЕНЬ ПОНЯТНЫЕ ЦИФРЫ
• Сколько можно потратить сегодня - лимит пересчитывается после каждой траты
• На сколько дней хватит денег и хватает ли до зарплаты
• Темп: тратишь по плану, экономнее или быстрее
• Инсайт дня простыми словами: как идет период и что это значит
• «Могу ли я себе это позволить?» - ответ по твоим деньгам за пару секунд
• Не было трат - отметь бесплатный день

ТРАТЫ СО СКРИНШОТА
• Отправь скриншот из банка - Кубыш сам разложит операции по категориям
• Распознавание работает на телефоне, скриншот никуда не уходит
• Все найденное показывается на проверку перед записью

СПОКОЙНО ДЕРЖАТЬ КУРС
• По субботам итоги недели: сколько сэкономил, куда ушли деньги, хватает ли до получки
• Утром план на день, вечером короткий разбор. Не больше двух уведомлений в день
• В конце периода разбор: что получилось и какой план дальше

ЦЕЛИ, РАДИ КОТОРЫХ ВСЕ ЭТО
• Подушка и цели с понятной датой, а не «когда-нибудь»
• План сам откладывает часть каждой получки, рост накоплений виден на графике
• «Загляни в будущее»: выбери дату и увидишь, сколько накопишь к ней

СПРОСИ КУБЫША
• «Сколько можно потратить до получки?», «Успею накопить к отпуску?», «Где ужаться?»
• Считает приложение, ИИ объясняет ответ простыми словами и ничего не записывает без твоего подтверждения

ПРИВАТНОСТЬ
• Банк подключать не нужно, доступ к СМС не нужен
• Финансовые данные хранятся на устройстве
• Приложение закрывается кодом и Face ID

Кубыш подойдет, если зарплата приходит раз или два в месяц, хочется меньше переживать из-за денег и спокойно копить на то, что важно.
```

```
Money navigator until payday
```

```
планировщик,помощник,накопить,копилка,конверты,кошелек,expense,tracker,planner,saving,limit,calm
```

```
Worry less about money: Kubysh builds a plan until payday and shows every day how much you can spend and whether it lasts. Your goals grow along the way.
```

```
Kubysh is a money navigator that makes life between paychecks calmer. Every day you see how much you can spend today and whether the money lasts until payday. And the plan from each paycheck takes you towards what you want: a holiday, a safety net, a renovation, a car.

A PLAN UNTIL PAYDAY IN MINUTES
No empty app to fill in and no spreadsheets. Answer a few questions about your income, fixed payments and goals, and Kubysh builds your plan right away: a daily budget, fixed payments and how much to set aside from this paycheck.

CLEAR NUMBERS EVERY DAY
• How much you can spend today - the limit updates after every expense
• How many days the money lasts and whether it reaches payday
• Your pace: on plan, slower or faster
• A daily insight in plain words: how the period is going and what it means
• "Can I afford this?" - an answer based on your own money in seconds
• No spending today? Mark a no-spend day

EXPENSES FROM A SCREENSHOT
• Share a screenshot from your bank and Kubysh sorts the transactions into categories
• Recognition runs on your phone, the screenshot never leaves it
• Everything found is shown for review before it is recorded

STAY ON COURSE CALMLY
• Every Saturday a weekly recap: how much you saved, where the money went, whether it lasts until payday
• A plan for the day in the morning, a short recap in the evening. No more than two notifications a day
• At the end of each period: what worked and what the next plan looks like

THE GOALS IT IS ALL FOR
• A safety net and goals with a real date, not "someday"
• The plan sets aside part of every paycheck, and you see your savings grow on a chart
• "Look into the future": pick a date and see how much you will have saved by then

ASK KUBYSH
• "How much can I spend before payday?", "Will I save enough for my holiday?", "Where do I cut back?"
• The app does the maths, the AI explains it in plain words and never records anything without your confirmation

PRIVACY
• No bank login, no SMS access
• Financial data is stored on your device
• The app locks with a passcode and Face ID

Amounts are in roubles: Kubysh is built for people who are paid once or twice a month.
```

## Скриншоты: менять ли

Да, первые три кадра стоит заменить: текущие сделаны под старый интерфейс (до инсайта из трёх
блоков и без итогов недели). В выдаче поиска видны первые 2–3 кадра — они продают «Получку».

| # | Заголовок кадра | Экран |
|---|---|---|
| 1 | Спокойно до получки | «Получка»: сколько можно сегодня, «хватит», темп |
| 2 | План под тебя за пару минут | Готовый план после онбординга |
| 3 | Каждый день понятные цифры | Инсайт дня: темп периода, дневные траты, хватит ли |
| 4 | Цели копятся по плану | Цели: отпуск/подушка с датой и взносом с получки |
| 5 | Траты со скриншота из банка | Разбор скриншота |
| 6 | Итоги недели по субботам | Разбор недели |

Кадры 4–6 можно оставить старыми, если нет времени. Скриншоты меняются только вместе с версией
(до отправки на ревью), промотекст — в любой момент.

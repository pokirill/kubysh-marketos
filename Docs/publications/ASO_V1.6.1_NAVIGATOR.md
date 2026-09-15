# ASO 1.6.1 — «финансовый навигатор к целям» (15.09.2026)

Решение основателя 15.09.2026: поднять скачивания из стора, вернуть в описание накопления и
продвигать финансовый навигатор, который помогает прийти к целям: план настроен под человека
сразу, не нужно смотреть на пустое приложение. Заменяет русскую и английскую карточку из
iOS `Docs/ASO_V1.6.1.md` (там остаётся «Что нового» и история решений).

## Гипотеза влияния (метрик-гейт)

Число установок из поиска App Store. База 14.08–12.09: показы ~220/день, просмотры
страницы 13/день (11 из поиска), конверсия «страница → загрузка» ~50%, первые загрузки
~50–60/нед. Ставка: подзаголовок и первые строки описания про цели и накопления дают
показы по запросам «копить», «накопления», «копилка на цели», где лидеры по учёту трат не стоят,
и повышают конверсию страницы за счёт понятного обещания «план под тебя сразу».
Проверка через 7 и 14 дней после выхода 1.6.1: показы из поиска и конверсия страницы.
Откат: показы < 200/день через 14 дней → вернуть прежний подзаголовок, ключи оставить.

## Рамка текста (проверено об MANIFEST.md, PRODUCT.md, JOBS.md)

- Навигатор ведёт вперёд: цель → маршрут по получкам → дорога и пробки сегодня.
- Эмоция важнее функции: «меньше переживать из-за денег» (топ-запрос опроса).
- Против таблиц и пустого приложения, а не против других приложений.
- Никаких цен, подписки, оплаты (App Store 3.1.1), абсолютных чисел, штампов «лучший/уникальный».
- Экономию не связываем с целями (iOS `AGENTS.md` п. 12): цели копятся ПЛАНОМ с каждой получки.
- Закрытой называем только работу «понять, что реально могу позволить»; остальное — без обещаний «гарантированно».

## Порядок блоков ниже (скрипт записи в ASC читает их по порядку)

1. RU subtitle 2. RU keywords 3. RU promo 4. RU description
5. EN subtitle 6. EN keywords 7. EN promo 8. EN description

```
Финансовый навигатор к целям
```

```
накопления,копилка,копить,подушка,учет,расходов,трат,получка,зарплата,контроль,деньги,кубышка
```

```
Укажи цель, и Кубыш построит маршрут: сколько откладывать с каждой получки и сколько можно тратить сегодня. План под тебя готов за пару минут, без таблиц.
```

```
Кубыш - финансовый навигатор. Ты говоришь, куда хочешь прийти: отпуск, подушка, ремонт, машина. Кубыш строит маршрут от получки до получки и ведет по нему: сколько отложить, сколько можно потратить сегодня и хватает ли денег до зарплаты.

ПЛАН ПОД ТЕБЯ С ПЕРВЫХ МИНУТ
Не нужно заполнять пустое приложение и разбираться в таблицах. Ответь на несколько вопросов про доход, обязательные платежи и цели - Кубыш сразу соберет план: бюджет на каждый день, взнос в накопления с каждой получки и дату, к которой накопишь.

НАКОПЛЕНИЯ, КОТОРЫЕ ПРАВДА КОПЯТСЯ
• Подушка и цели с понятной датой, а не «когда-нибудь»
• План сам откладывает часть каждой получки, рост накоплений виден на графике
• Сначала подушка, потом цели: Кубыш покажет, когда начнется каждая
• «Загляни в будущее»: выбери дату и увидишь, сколько накопишь к ней

СКОЛЬКО МОЖНО ТРАТИТЬ СЕГОДНЯ
• Лимит на день пересчитывается после каждой траты
• Инсайт дня: сколько можно еще сегодня, как идет период и хватает ли до получки
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

СПРОСИ КУБЫША
• «Сколько можно потратить до получки?», «Успею накопить к отпуску?», «Где ужаться?»
• Считает приложение, ИИ объясняет ответ простыми словами и ничего не записывает без твоего подтверждения

ПРИВАТНОСТЬ
• Банк подключать не нужно, доступ к СМС не нужен
• Финансовые данные хранятся на устройстве
• Приложение закрывается кодом и Face ID

Кубыш подойдет, если зарплата приходит раз или два в месяц, хочется копить на несколько целей и меньше переживать из-за денег.
```

```
Money navigator: spend, save
```

```
планировщик,помощник,накопить,копилка,конверты,кошелек,expense,tracker,planner,payday,saving,budget
```

```
Set a goal and Kubysh builds the route: how much to save from each paycheck and how much you can spend today. A plan made for you in minutes, no spreadsheets.
```

```
Kubysh is a money navigator. You say where you want to get to: a holiday, a safety net, a renovation, a car. Kubysh builds the route from paycheck to paycheck and guides you along it: how much to set aside, how much you can spend today and whether the money lasts until payday.

A PLAN MADE FOR YOU FROM MINUTE ONE
No empty app to fill in and no spreadsheets. Answer a few questions about your income, fixed payments and goals, and Kubysh builds your plan right away: a daily budget, a savings contribution from each paycheck and the date you will reach your goal.

SAVINGS THAT ACTUALLY GROW
• A safety net and goals with a real date, not "someday"
• The plan sets aside part of every paycheck, and you see your savings grow on a chart
• Safety net first, then goals: Kubysh shows when each one starts
• "Look into the future": pick a date and see how much you will have saved by then

HOW MUCH CAN I SPEND TODAY
• Your daily limit updates after every expense
• Daily insight: what is left for today, how the period is going and whether money lasts until payday
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

Да, первые три кадра стоит заменить: текущие сделаны под обещание «сколько можно тратить сегодня»
и старый интерфейс (до инсайта из трёх блоков и без итогов недели). В выдаче поиска видны первые
2–3 кадра — они должны говорить то же, что подзаголовок, иначе обещание «навигатор к целям» не
подтверждается картинкой и конверсия страницы падает.

| # | Заголовок кадра | Экран |
|---|---|---|
| 1 | Финансовый навигатор к твоим целям | Цели: отпуск/подушка с датой и взносом с получки |
| 2 | План под тебя за пару минут | Готовый план после онбординга: бюджет на день, взнос, дата |
| 3 | Сколько можно тратить сегодня | «Получка»: плитки и инсайт дня |
| 4 | Накопления растут на глазах | Обзор: график накоплений с датами |
| 5 | Траты со скриншота из банка | Разбор скриншота |
| 6 | Итоги недели по субботам | Разбор недели |

Кадры 4–6 можно оставить старыми, если нет времени: они уже про реальные функции.
Скриншоты меняются только вместе с версией (на ревью), промотекст — в любой момент.

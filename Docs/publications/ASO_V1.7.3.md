# ASO 1.7.3 (сборка 114) — подготовка к отправке, 13.10.2026

**Статус 14.10.2026 01:2x MSK:** тексты загружены через ASC API (meta.py), 1.7.3 со сборкой 114 отправлена основателем через интерфейс — WAITING_FOR_REVIEW, выпуск сразу после одобрения.

## Метаданные: возврат к 1.7.1 (решение основателя 13.10.2026)
Причина: после выхода 1.7.2 с новыми полями установки упали (дашборд — 3 за день; по серверу 8 и 7 против 10–27
в предыдущие дни, малые числа). Возвращаем поля 1.7.1 целиком; замер 21.10 сравнивает уже 1.7.1-поля.
| Поле | 1.7.3 (= 1.7.1) |
|---|---|
| ru Name | Кубыш: финансы и накопления |
| ru Subtitle | Копилка, цели и учет расходов |
| ru Keywords | `личные,деньги,денег,накопить,накоплений,мечту,подушка,безопасности,бюджет,семейный,траты,кубышка` |
| en-GB Name | Кубыш: финансовый помощник |
| en-GB Subtitle | Контроль расходов до зарплаты |
| en-GB Keywords | `учет,трат,экономия,денег,планировщик,бюджета,дневной,лимит,трекер,получки,аванс,бесплатно,виджет` |
Источник: ключевые слова — ASC API, версия 1.7.1 (13.10); название/подзаголовок — колонка «Сейчас» в `ASO_V1.7.2.md`
(Apple не хранит их историю). Внимание: в ru-ключах есть «семейный», а семейного режима нет — оставлено как в 1.7.1
по решению вернуть «как было»; заменить на «копилка» — одно слово, если основатель скажет.

## Промотекст (≤170, меняется без ревью)
**ru:** Спокойно до зарплаты: сколько можно тратить сегодня и когда накопишь на мечту. Новое: путь к цели в получках и сундуки за неделю.
**en:** Calm until payday: how much you can spend today and when you reach your dream. New: your goal path in paychecks and weekly chests.

## Что нового (ru)
Кубыш 1.7.3
• Лидерборд, чат и синхронизация снова работают на мобильном интернете и Wi-Fi без VPN
• Путь к мечте: цель в получках. Каждая закрытая получка двигает Кубыша на шаг
• Сундук недели в пятницу и сундук получки в конце периода
• Итоги недели короче: как прошла неделя и сколько можно на выходные
• Итоги получки: куда разошлись деньги, итог Кубыша и сравнение с прошлой получкой
• Взял из накоплений? Кубыш предложит вернуть себе частями с ближайших получек
• Долги в Обзоре: кто должен тебе и кому должен ты, с напоминанием о сроке
• Категории истории можно удалить, траты сохранятся в «Другое»
• Даты целей в плане и на экране целей теперь совпадают

## What's New (en)
Kubysh 1.7.3
• Leaderboard, chat and sync work again on mobile internet and Wi-Fi without a VPN
• Dream path: your goal measured in paychecks. Each closed paycheck moves Kubysh a step forward
• Weekly chest on Friday and a paycheck chest at the end of the period
• Shorter weekly summary: how the week went and what you can spend this weekend
• Paycheck summary: where the money went, Kubysh's takeaway and a comparison with last paycheck
• Took money from savings? Kubysh offers to pay yourself back over the next paychecks
• Debts in Overview: who owes you and whom you owe, with due date reminders
• History categories can be deleted, expenses move to Other
• Goal dates in the plan and on the Goals screen now match

## Заметки для App Review (en) — как в прошлых одобренных версиях, без упоминания сайта и оплаты
Sign in with Apple is optional: all features of the app work without an account. No login is needed to review the
app — complete the short onboarding and every screen is available.

## После одобрения 1.7.3
1. Пуш «обнови Кубыш» (266 устройств на старых версиях): `send_update_push.py --send` — по команде основателя.
2. 4 спецстраницы под запросы и перезапуск A/B «Цели первыми» — из плана 1.7.2 (`ASO_V1.7.2.md`), если ещё не сделаны.
3. Замер 21.10 — по таблице 1.7.2.

## Скриншоты
Текущие кадры 1.7.x остаются. Новый кадр «Путь к мечте» — кандидат в первую пятёрку после приёмки экрана основателем
(генератор `Docs/tools/store_cards`), в 1.7.3 не блокирует отправку.

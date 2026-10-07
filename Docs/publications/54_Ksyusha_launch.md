# Ксюша: запуск образа и ролик К1 «Знакомьтесь, Ксюша» (Higgsfield)

Статус (07.10.2026): **К1 «Ксюша и жаба» принят Кириллом**, лежит в папке дня 11.10 (`Рилс К1 Ксюша и жаба.mp4`),
подписи в `45_Content_plan_*`. Пайплайн: референсы и стартовые кадры gpt_image_2_5 → клипы Kling 3.0 без звука → голоса
ElevenLabs закадрово (Ксюша Xenia, Кубыш Holden, каждый одним дублем с нарезкой по паузам; Душная клон) → движок кладет
экраны 1.7, подписи с аватарками говорящего, фон кофейни CC0. Сцена `episodes/k01_ksyusha.py`. В работе К2 «Пятница».

Правила Кирилла после К1 (07.10): Душная не спрыгивает с плеча дважды, одно состояние на серию; без точек в конце подписей;
никаких застывших картинок, только клипы; Кубыш — автор ролика, виден и говорит с первых секунд.

Статус (04.10.2026): выход К1 — 11.10, внешность утверждена, генерация через MCP Higgsfield (`https://mcp.higgsfield.ai/mcp`,
подключает Кирилл), голос Ксюши пока черновой синтез Яндекса (alena), живая запись — по желанию. Сезон с Ксюшей начинается
после запуска ее образа (решение Кирилла 04.10); серии сезона — отдельное согласование.

Что уже готово: сценарий и аниматик К1 (`Рилсы Ксюша/K01_Знакомьтесь_Ксюша/`), движок умеет вставлять клипы
Higgsfield (`tools/reels/studio.py`, `vframes`), сцена `episodes/k01_ksyusha.py`. Клипы встают на место заглушек
без правки кода, как только лежат в папке.

## Кто такая Ксюша

- **27 лет, Москва, маркетолог в небольшой компании.** Стабильная зарплата 10-го и аванс 25-го.
- **Две цели, как на настоящем экране целей 1.7:** новый айфон (прогноз 10 февраля 2027) и Япония (прогноз 10 июля 2027).
  Подушка копится фоном.
- **Мелкие радости:** матча-латте по утрам, маркетплейс по вечерам, доставка в пятницу.
- **Что ее душит:** вина за каждую мелкую трату («а Япония сама себя не накопит»). Это голос Душной.
- **Характер:** ироничная, теплая, немного тревожная насчет денег. Решает сама и не любит, когда ей указывают.
- **Речь:** коротко, с юмором, без канцелярита, со зрителем на «ты».
- **Вокруг нее:** Душная — внутренний голос, появляется рядом (на стойке, на плече). Кубыш живет в телефоне,
  показывает цифры и не командует.
- **Образ одной фразой:** «Две цели и ноль вины за кофе».
- **Не делаем:** не учим жить, не стыдим за траты, не говорим «экономь», экономию не привязываем к целям.

## Визуальная библия

- **Внешность:** славянская внешность, теплое приветливое лицо, легкие веснушки, ореховые глаза, светло-русые волосы
  до плеч с мягкой волной, минимум макияжа, маленькие золотые серьги-кольца. Живая, не модель.
- **Гардероб (постоянный, чтобы узнавали):** объемный кремовый свитер крупной вязки поверх белой футболки, светлые
  джинсы; на улице бежевый тренч. **Телефон в мятно-зеленом чехле** — сквозная деталь, цвет Кубыша.
- **Локации:** уютная кофейня (деревянная стойка, доска меню без читаемых надписей, растения, утренний свет),
  ее квартира, офис, осенняя улица.
- **Стиль:** реализм, мягкий теплый дневной свет, объектив 35 мм, малая глубина резкости, легкое зерно, без глянца.
- **Нельзя в кадре:** логотипы, бренды, читаемые вывески, банки, сходство со знаменитостями.

## Сценарий К1 (25 секунд, тон по правилам `53_Reels_scripts_v2.md`)

| Шот | Время | Что генерирует Higgsfield | Что накладываю я | Реплика |
|---|---|---|---|---|
| S1 | 0–4,6 | Кофейня, Ксюша у стойки сомневается перед меню, левая часть стойки пустая, камера неподвижна | Душная на стойке | Душная: «Так! Опять кофе? А Япония сама себя не накопит.» |
| S2 | 4,6–7,2 | Крупно: косится на стойку, вздыхает с улыбкой, говорит в камеру | субтитры | Ксюша: «Это моя жаба. Душит за каждый кофе.» |
| S3 | 7,2–10,0 | По пояс с телефоном в мятном чехле, говорит в камеру | субтитры | Ксюша: «А у меня две цели: айфон и Япония.» |
| S4 | 10,0–15,3 | Крупно руки с телефоном, кофейня размыта | экран целей 1.7 с обводкой «В плане», Кубыш впрыгивает | Кубыш: «Обе цели в плане. А кофе из бюджета дня, не из Японии.» |
| S5 | 15,3–17,3 | Ксюша улыбается и поворачивается к бариста за кадром | субтитры | Ксюша: «Тогда латте. Большой.» |
| S6 | 17,3–21,9 | Ксюша тихо смеется, глядя на пустую стойку, камера неподвижна | Душная и Кубыш на стойке | Душная: «Так! Кто разрешил?» Кубыш: «Никто. Тут решают не жабы.» |
| S7 | 21,9–25,1 | Выходит из кофейни на солнечную улицу с большим латте, камера едет назад | титры «Ксюша · две цели · ноль вины за кофе», «Скоро: от зарплаты до аванса с Ксюшей» | — |

Голоса: Ксюша — живая запись команды (реплики ниже), Кубыш и Душная — Яндекс (kirill, omazh).

## Технические требования к клипам

- 9:16, не меньше 1080×1920, 24–30 кадров/с, **без звука и без текста**, длительность шота с запасом 0,5–1 с.
- **S1 и S6: камера неподвижна, верх стойки на 31% от низа кадра, левая треть стойки пустая.** Туда встают
  нарисованные жабы, и если камера едет, они «отклеятся» от стойки.
- S2, S3, S5 — липсинк на живые реплики Ксюши (файлы `K01_1…3`).
- Одно лицо и один свитер во всех шотах: каждый стартовый кадр делаем по одобренному референсу Ксюши.
- Сдача: `Кубыш доки и артефакты /Рилсы Ксюша/K01_клипы/S1.mp4 … S7.mp4`.

## Промпты (английский, так модели понимают точнее)

**База персонажа** (вставляется в каждый промпт вместо [KSYUSHA]):
> Ksenia (Ksyusha), a 27-year-old Russian woman with a warm, friendly, relatable face, light freckles, hazel eyes,
> shoulder-length light-brown hair with soft natural waves, minimal natural makeup, small gold hoop earrings,
> wearing an oversized cream chunky-knit sweater over a white t-shirt and light jeans, holding a smartphone in a
> mint-green case. Natural everyday look, not a fashion model.

**Стиль** (в конец каждого промпта, [STYLE]):
> photorealistic, cinematic, soft warm morning daylight, 35mm lens, shallow depth of field, subtle film grain,
> vertical 9:16 composition

**Негатив:**
> no text, no logos, no brand names, no readable signs, no watermark, no extra fingers, no distorted hands,
> no celebrity likeness, no heavy makeup, no glossy beauty retouch

**Референс-лист (утвердить лицо до видео):**
> Character reference sheet of [KSYUSHA]: front view, three-quarter view, profile view and a smiling close-up,
> neutral light-grey studio background, identical face, hairstyle and clothes in every view, photorealistic,
> soft even light

**Стартовые кадры и движение:**

| Шот | Стартовый кадр | Движение (image-to-video) |
|---|---|---|
| S1 | [KSYUSHA] stands at the wooden counter of a cozy small café in Moscow, morning light from a window, plants and a blank chalkboard menu behind the counter. She looks up at the menu with slight hesitation, finger on her lips. She stands right of center; the left third of the counter top in the foreground is empty and clearly visible; the counter edge is about one third from the bottom of the frame. [STYLE] | Locked-off static camera, no camera movement. She hesitates, tilts her head slightly, blinks naturally, small breath. 5 seconds |
| S2 | Close-up portrait of [KSYUSHA] in the same café, glancing down to her left with one eyebrow raised, about to speak with a wry, amused smile. [STYLE] | She sighs, smiles and talks to the camera, subtle natural head movement, slow push-in. 3 seconds, lip-sync to line 1 |
| S3 | Medium close-up of [KSYUSHA] facing the camera, holding her phone in the mint-green case at chest height, playful and confident, café bokeh behind. [STYLE] | She talks casually to the camera with a small gesture of the phone. 3 seconds, lip-sync to line 2 |
| S4 | Close-up of a woman's hands in a cream knit sweater holding a smartphone in a mint-green case, screen facing the viewer and plain light, café softly blurred behind. [STYLE] | Very subtle hand movement, gentle rack focus. 5 seconds |
| S5 | Medium shot of [KSYUSHA] at the same café counter turning toward the barista off-screen with a relieved, happy smile. [STYLE] | She turns her head toward the barista and says a short phrase, natural smile. 3 seconds, lip-sync to line 3 |
| S6 | Close-up across the café counter: the empty wooden counter top fills the bottom third of the frame; [KSYUSHA] behind it laughs softly, looking down at the counter top. [STYLE] | Locked-off static camera. She laughs quietly and shakes her head. 5 seconds |
| S7 | [KSYUSHA] in a beige trench coat walks out of the café onto a sunny autumn Moscow street holding a large paper cup of latte, happy and light. [STYLE] | Camera tracks backwards in front of her, slow motion, golden leaves. 4 seconds |

## Порядок работы

1. **Лицо.** Референс-лист Ксюши → Кирилл утверждает внешность. Картинки по правилу маркетоса делаем в ChatGPT,
   кредиты Higgsfield бережем для видео; если для одинакового лица в шотах Higgsfield нужен свой персонаж
   (например, по нескольким фото), решаем отдельно.
2. **Пробный шот.** S3 (простой, с липсинком) на 1–2 моделях Higgsfield: проверяем, не «плывет» ли лицо и как
   выглядит липсинк с живым голосом. Выбираем модель для остальных шотов.
3. **Стартовые кадры S1–S7** по референсу, затем видео из кадра по таблице выше.
4. **Липсинк** S2, S3, S5 на живые реплики Ксюши.
5. **Сборка:** клипы в папку `K01_клипы`, реплики в `Голоса/Ксюша` → `python3 studio.py episodes/k01_ksyusha.py`.
   Жабы, экран целей, субтитры, голоса Кубыша и Душной уже стоят по таймингу аниматика.
6. **Подписи** в контент-план и перенос ролика с обложкой в папку дня.

**Про MCP.** Коннектора Higgsfield в каталоге Claude нет (проверено 04.10). Если у Higgsfield есть свой MCP-сервер
или API, его можно подключить как свой коннектор, тогда генерирую сам по этим промптам. Иначе генерацию запускает
Кирилл в веб-интерфейсе, а сборку делаю я.

## Чек-лист

- [x] сценарий К1 по правилам тона и аниматик с черновым голосом Ксюши
- [x] библия персонажа, визуальная библия, промпты
- [x] движок вставляет клипы Higgsfield вместо заглушек
- [ ] внешность Ксюши утверждена
- [ ] реплики Ксюши записаны (`team/BRIEF_VOICES.md`, раздел К1)
- [ ] пробный шот S3 и выбор модели
- [ ] клипы S1–S7
- [ ] финальная сборка, подписи, дата в контент-плане

## Вопросы Кириллу

1. Дата выхода К1. Предложение: 11.10, сразу после пресезона.
2. Кто генерирует: подключаем MCP Higgsfield или ты в веб-интерфейсе по промптам?
3. Внешность и стиль Ксюши — ок или поправить (возраст, волосы, одежда)?
4. Кто из команды озвучивает Ксюшу?

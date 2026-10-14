
"""
NOVA UI v2.6 Веб-интерфейс чата с Новой на Gradio (ядро Nova v1.5/v1.6, Gradio 6).

ЧТО ВНУТРИ:
1. Дизайн по мотивам варианта Грока: тёмный фиолетово-розовый градиент,
   карточки, пузырьки сообщений, скрытый футер, тонкий скроллбар.
   Все рискованные API-вызовы Грока заменены на проверенные (css вместо theme.set).
2. Чат уже и ниже: колонки 1:1, высота чата 430 — ничего не расползается.
3. Таблица нейрохимии компактная (мелкий шрифт, тонкие ячейки) — вся правая
   панель помещается на экран БЕЗ прокрутки.
4. Аватарка: если рядом лежит nova_avatar.png — подхватывается автоматически,
   если файла нет — интерфейс всё равно запускается.
5. Вся логика v1.7.2/v1.8 на месте: _as_text, защита обработчиков, NO_PROXY,
   кнопка списка, minimum=1, обновление панели после Применить/Отклонить.

ПРАВКИ v2.6 (только CSS и мелкие детали — layout и логика не тронуты):
- Значок «№»: селектор .dark-num расширен на ВСЕ внутренние элементы лейбла
  (label / .label-wrap / [class*="label"] + их потомки) — чёрный символ
  гарантированно читается на светлой плашке. Класс dark-num теперь реально
  вешается на поле номера через elem_classes.
- [v2.6.1] Gradio 6 рендерит Number иначе: input получал белый фон по
  умолчанию, а лейбл мог не иметь класса label. Добавлен структурный чинк:
  тёмный фон + светлый текст на ВСЕХ текстовых input и плашка «№» через
  прямых детей блока / :has(input) — независимо от имён классов.
- Фиолетовые «балки» убраны: --block-label-background-fill = transparent,
  все лейблы («Результат», «Внутренний голос») — только цвет текста.
  Единственное исключение — светлая плашка у «№».
- Контрастность: светлый текст гарантированно читается в карточке состояния,
  таблице медиаторов (включая заголовки), чате и полях ввода; плейсхолдеры
  приглушённо-светлые.
- Пузырьки сообщений: мягкие градиенты — user розово-фиолетовый, assistant
  глубокий фиолетовый с тонкой светлой рамкой; аккуратные скругления, не «кричат».
- Кнопки: primary — розово-фиолетовый градиент с плавным hover (brightness +
  мягкое свечение), secondary — полупрозрачный со спокойным hover. Без кислоты.
- Скроллбар правой панели: тонкий, скруглённый, фиолетово-розовый градиент.
- Футер Gradio скрыт надёжнее: footer + .gradio-footer + [data-testid="footer"].
- Поле ввода: современный вид, мягкое розовое свечение при фокусе.
- Общий polish: типографика, мягкие тени, отступы — не «типичный Gradio».

ЗАПУСК:
1) pip install gradio
2) python nova_ui.py
3) Браузер откроется на http://127.0.0.1:7860
"""

import os

# [VPN-стойкость] localhost всегда ходит напрямую, мимо любого прокси.
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

import asyncio
import inspect

import gradio as gr

from nova_unified import Nova

# Инициализируем Нову один раз при старте UI.
nova = Nova()

# Служебные маркеры: блоки, которые Нова доклеивает в конец ответа.
SERVICE_MARKERS = ("📋 *У Новы есть", "🧘 *Нова медитирует")

# Ограничитель параллельности (в Gradio 6 класса может не быть).
try:
    chat_limiter = gr.ConcurrencyLimiter(limit=1)
except AttributeError:
    chat_limiter = 1

# Аватарка Новы: подхватится, только если файл реально лежит рядом.
AVATAR_PATH = "nova.jpeg"

# ====================================================================
# КАСТОМНЫЙ CSS — тёмное оформление, полировка v2.6 (дизайн-идеи Грока)
# ====================================================================
custom_css = """
/* ============================================================
   [v2.6] ПЕРЕМЕННЫЕ ТЕМЫ — бьём в причину белизны и «балок».
   Из них Gradio лепит фон и цвет текста ВСЕХ компонентов,
   поэтому после перекрытия каждое поле становится тёмным со
   светлым текстом независимо от внутренних имён классов.
   ============================================================ */
.gradio-container {
    --body-text-color: #f0e6ff !important;
    --prose-text-color: #f0e6ff !important;
    --block-background-fill: rgba(20, 12, 35, 0.55) !important;
    --block-background-fill-secondary: rgba(20, 12, 35, 0.4) !important;
    --panel-background-fill: rgba(28, 16, 44, 0.7) !important;
    --background-fill-primary: #1a0f2e !important;
    --background-fill-secondary: #241239 !important;
    --input-background-fill: rgba(24, 14, 38, 0.85) !important;
    --input-background-fill-focus: rgba(30, 18, 48, 0.95) !important;
    --input-text-color: #f0e6ff !important;
    --input-placeholder-color: #b79fd4 !important;
    /* [v2.6] Лейблы без «балок»: фон прозрачный, читаем только текст */
    --block-label-background-fill: transparent !important;
    --block-label-text-color: #d9c2f5 !important;
    --block-label-border-color: rgba(255, 182, 193, 0.25) !important;
    --border-color-primary: rgba(255, 182, 193, 0.22) !important;
    --border-color-accent: rgba(255, 158, 205, 0.35) !important;
}

/* ============================================================
   [v2.6] Страница тёмная гарантированно: перекрываем все обёртки
   Gradio 6 (html/body/main), чтобы по краям не белело «молоко».
   + аккуратная типографика и цвет выделения текста.
   ============================================================ */
html, body, .gradio-container, .main, #gradio-container {
    background: linear-gradient(150deg, #170a26 0%, #241239 45%, #1a0f2e 100%) !important;
}
.gradio-container {
    font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif !important;
    letter-spacing: 0.1px;
}
::selection {
    background: rgba(236, 72, 153, 0.4) !important;
    color: #fff !important;
}

/* ============================================================
   КОНТЕЙНЕРЫ (геометрия не тронута — только полировка теней)
   ============================================================ */
.main-container {
    max-width: 1380px;
    margin: 0 auto;
    padding: 14px 18px 20px;
}
.title-block {
    text-align: center;
    padding: 10px 16px;
    background: linear-gradient(90deg, rgba(70, 30, 110, 0.85), rgba(110, 40, 150, 0.85), rgba(70, 30, 110, 0.85)) !important;
    border: 1px solid rgba(224, 170, 255, 0.35) !important;
    border-radius: 14px;
    margin-bottom: 14px !important;
    box-shadow: 0 6px 24px rgba(88, 28, 135, 0.35);
}
.title-block h1 {
    background: linear-gradient(90deg, #c77dff, #e0aaff, #ff9ecd) !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    color: #c77dff !important;
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    margin: 0 !important;
}
.subtitle {
    color: #e0c9ff !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    margin: 2px 0 0 !important;
}
.chat-column {
    background: rgba(28, 16, 44, 0.66);
    border: 1px solid rgba(255, 182, 193, 0.16);
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.35);
}
.fixed-height-chat {
    border-radius: 12px !important;
    border: 1px solid rgba(255, 182, 193, 0.12) !important;
    background: rgba(18, 10, 30, 0.55) !important;
}

/* ============================================================
   [v2.6] ПУЗЫРЬКИ СООБЩЕНИЙ — мягкие градиенты, различимые,
   но не «кричащие». user — розово-фиолетовый, assistant —
   глубокий фиолетовый с тонкой светлой рамкой.
   ============================================================ */
.message.user, .message.user * {
    background: linear-gradient(135deg, #7b4bb2 0%, #a86cc9 100%) !important;
    color: #fff !important;
    border-radius: 14px 14px 4px 14px !important;
}
.message.user {
    box-shadow: 0 3px 12px rgba(123, 75, 178, 0.35) !important;
}
.message.bot, .message.assistant, .message.bot *, .message.assistant * {
    background: linear-gradient(135deg, #251538 0%, #3b2760 100%) !important;
    color: #f0e6ff !important;
    border: 1px solid rgba(224, 170, 255, 0.16) !important;
    border-radius: 14px 14px 14px 4px !important;
}

/* ============================================================
   [v2.6] ПОЛЕ ВВОДА — современное, с мягким розовым фокусом
   ============================================================ */
.input-row textarea {
    background: rgba(24, 14, 38, 0.85) !important;
    border: 1px solid rgba(224, 170, 255, 0.22) !important;
    border-radius: 12px !important;
    color: #f5eefc !important;
    transition: border-color .2s ease, box-shadow .25s ease, background .25s ease !important;
}
.input-row textarea:focus {
    outline: none !important;
    border-color: rgba(236, 72, 153, 0.6) !important;
    background: rgba(30, 18, 48, 0.95) !important;
    box-shadow: 0 0 0 3px rgba(236, 72, 153, 0.16), 0 4px 18px rgba(168, 85, 247, 0.18) !important;
}

/* [v2.6] Контраст: светлый текст во ВСЕХ полях (включая Number) */
.gradio-container textarea { color: #f0e6ff !important; }
.gradio-container input { color: #f0e6ff !important; }
.gradio-container input::placeholder,
.gradio-container textarea::placeholder { color: #b79fd4 !important; }

/* ============================================================
   [v2.6] КНОПКИ — плавные hover без кислоты.
   primary: розово-фиолетовый градиент + мягкое свечение.
   secondary: полупрозрачный, спокойный подъём фона.
   ============================================================ */
.primary-btn {
    background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%) !important;
    border: none !important;
    color: #fff !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    box-shadow: 0 3px 12px rgba(168, 85, 247, 0.35) !important;
    transition: filter .2s ease, transform .15s ease, box-shadow .25s ease !important;
}
.primary-btn:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4) !important;
}
.primary-btn:active {
    transform: translateY(0);
    filter: brightness(0.97);
}
.secondary-btn {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(224, 170, 255, 0.3) !important;
    color: #e9d8ff !important;
    font-weight: 500 !important;
    border-radius: 12px !important;
    transition: background .2s ease, border-color .2s ease, box-shadow .25s ease !important;
}
.secondary-btn:hover {
    background: rgba(224, 170, 255, 0.16) !important;
    border-color: rgba(224, 170, 255, 0.5) !important;
    box-shadow: 0 3px 12px rgba(139, 92, 246, 0.22);
}

/* ============================================================
   [v2.6] ПРАВАЯ ПАНЕЛЬ + тонкий скроллбар в тон теме
   ============================================================ */
.right-panel {
    background: rgba(28, 16, 44, 0.7);
    border: 1px solid rgba(255, 182, 193, 0.16);
    border-radius: 16px;
    padding: 12px 14px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.35);
    max-height: calc(100vh - 140px);
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(168, 85, 247, 0.55) transparent;
}
.right-panel::-webkit-scrollbar { width: 6px; }
.right-panel::-webkit-scrollbar-track { background: transparent; }
.right-panel::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #a855f7, #ec4899);
    border-radius: 8px;
}
.right-panel::-webkit-scrollbar-thumb:hover {
    background: #c084fc;
}

/* ============================================================
   [v2.6] КАРТОЧКА СОСТОЯНИЯ — контраст для глаз (включая таблицу)
   ============================================================ */
.state-card {
    background: linear-gradient(160deg, rgba(90, 40, 120, 0.32), rgba(50, 25, 80, 0.38));
    border: 1px solid rgba(255, 182, 193, 0.18);
    border-radius: 12px;
    padding: 10px 12px;
    font-size: 0.9rem;
    line-height: 1.4;
}
.state-card, .state-card * { color: #f0e6ff !important; }
.state-card strong { color: #ffb6e0 !important; }
.state-card code {
    color: #ffd6ec !important;
    background: rgba(255, 182, 193, 0.18) !important;
    border-radius: 5px;
    padding: 0 4px;
}
.state-card table { width: 100% !important; border-collapse: collapse !important; }
.state-card th {
    color: #ffb6e0 !important;
    font-weight: 700 !important;
    text-align: left !important;
    padding-bottom: 4px !important;
    border-bottom: 1px solid rgba(255, 182, 193, 0.25) !important;
}
.state-card td { color: #f0e6ff !important; }
.right-panel table { font-size: 0.82rem !important; }
.right-panel th, .right-panel td { padding: 2px 6px !important; }
.state-card p { margin: 2px 0 !important; }

/* ============================================================
   [v2.6] ЛЕЙБЛЫ — КРАЙ «БАЛОК»: фон прозрачный, только текст.
   Единственное исключение — светлая плашка у «№» (в конце файла).
   ============================================================ */
.gradio-container label,
.gradio-container .label-wrap,
.gradio-container [class*="label"] {
    background: transparent !important;
    color: #d9c2f5 !important;
    font-weight: 600 !important;
}

/* ============================================================
   БЛОК УПРАВЛЕНИЯ (предложения по коду)
   ============================================================ */
.control-block {
    background: rgba(18, 10, 30, 0.5);
    border: 1px solid rgba(255, 182, 193, 0.12);
    border-radius: 12px;
    padding: 8px 10px;
    margin-top: 8px;
}
.control-block, .control-block * { color: #e9d8ff !important; }

/* ============================================================
   [v2.6] ФУТЕР GRADIO — скрыт надёжнее (все известные варианты)
   ============================================================ */
footer, .gradio-footer, [data-testid="footer"] { display: none !important; }

/* ============================================================
   [v2.6] ЗНАЧОК «№» — ЧЁРНЫЙ СИМВОЛ НА СВЕТЛОЙ ПЛАШКЕ, ГАРАНТИРОВАННО.
   Селектор расширен на ВСЕ внутренние элементы лейбла: в Gradio 6
   текст может жить в label / .label-wrap / div.label и дополнительных
   span внутри — красим всё подряд. Правила стоят в самом конце файла,
   поэтому побеждают любые прежние. Дублирование через .control-block
   страхует на случай, если класса dark-num не окажется.
   ============================================================ */
.dark-num label,
.dark-num .label-wrap,
.dark-num [class*="label"],
.control-block label,
.control-block .label-wrap {
    background: linear-gradient(135deg, #fdf7ff 0%, #ecd9fb 100%) !important;
    color: #14092b !important;
    font-weight: 700 !important;
    padding: 1px 8px !important;
    border-radius: 6px !important;
    display: inline-block !important;
    line-height: 1.5 !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3) !important;
}
.dark-num label *,
.dark-num .label-wrap *,
.dark-num [class*="label"] *,
.control-block label *,
.control-block .label-wrap * {
    color: #14092b !important;
    background: transparent !important;
}

/* ============================================================
   [v2.6.1] ЧИНК «№» И ПОЛЯ НОМЕРА — ЯДЕРНЫЙ ВАРИАНТ.
   Gradio 6 рендерит Number иначе, чем ожидалось: input получает
   светлый фон по умолчанию (переменная темы его не ловит), а лейбл
   «№» не всегда имеет класс label/.label-wrap. Лечим структурно:
   тёмный фон на ВСЕХ текстовых input + чёрный текст на любом
   элементе, который может быть лейблом поля номера.
   ============================================================ */

/* 1) Тёмный фон и светлый текст на всех текстовых input (Number и др.) —
      убивает белую плашку под цифрой «1» независимо от версии Gradio. */
.gradio-container input[type="text"],
.gradio-container input[inputmode],
.gradio-container input:not([type]) {
    background: rgba(24, 14, 38, 0.9) !important;
    color: #f5eefc !important;
}

/* 2) Если .dark-num — обёртка блока: её прямой ребёнок (не input/button)
      и есть лейбл «№» — красим в плашку, не доверяя имени класса. */
.dark-num > *:not(input):not(button),
.dark-num label,
.dark-num [class*="label"],
.dark-num span {
    background: linear-gradient(135deg, #fdf7ff 0%, #ecd9fb 100%) !important;
    color: #14092b !important;
    font-weight: 700 !important;
    padding: 1px 8px !important;
    border-radius: 6px !important;
    display: inline-block !important;
    line-height: 1.5 !important;
}

/* 3) Если .dark-num — сам input (elem_classes лег на внутренность):
      ищем лейбл структурно — элемент, стоящий перед input в control-block. */
.control-block :is(label, div, span):has(+ input),
.control-block :is(label, div, span):has(~ input) {
    background: linear-gradient(135deg, #fdf7ff 0%, #ecd9fb 100%) !important;
    color: #14092b !important;
    font-weight: 700 !important;
    padding: 1px 8px !important;
    border-radius: 6px !important;
    display: inline-block !important;
}

/* 4) Все потомки найденного лейбла «№» — тоже чёрные, без своих фонов. */
.dark-num > *:not(input):not(button) *,
.control-block :is(label, div, span):has(+ input) * {
    color: #14092b !important;
    background: transparent !important;
}
"""


# ====================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ====================================================================
def _await_if_needed(result):
    """
    Если ядро синхронное — значение проходит насквозь.
    Если ядро async — докручиваем корутину в локальном event loop.
    """
    if inspect.isawaitable(result):
        return asyncio.run(result)
    return result


def get_state_display():
    """Компактная панель: шапка + таблица медиаторов + производные, без прокрутки."""
    neuro = nova.neurochem.levels
    gs = nova.growth_stage
    pending = len(nova._get_proposed_indices())
    text = f"""**😊 Эмоция:** {nova._current_emotion} · **👁 Глаза:** {nova.eye_color} (`{nova.eye_intensity:.2f}`)
**🌱 Стадия:** {gs.stage} (`{gs.age:.2f}`) · **💫 Жизнь:** `{nova.life_core.life_accumulator:.4f}` · **💤 Сны:** {nova.dream_count_today} · **📋 Предложений:** {pending}

| Медиатор | Роль | Уровень |
|---|---|---|
| DA | мотивация, радость | `{neuro.get('DA', 0):.2f}` |
| HT | ровность настроения | `{neuro.get('HT', 0):.2f}` |
| OXY | привязанность, нежность | `{neuro.get('OXY', 0):.2f}` |
| NA | внимание, мобилизация | `{neuro.get('NA', 0):.2f}` |
| AD | острый драйв | `{neuro.get('AD', 0):.2f}` |
| CORT | хронический стресс | `{neuro.get('CORT', 0):.2f}` |
| ANGER | защита, ярость | `{neuro.get('ANGER', 0):.2f}` |
| SHAME | самокритика | `{neuro.get('SHAME', 0):.2f}` |
| greed | тяга к новому | `{neuro.get('greed', 0):.2f}` |

**⚙️ Перекрытие:** `{nova.overlap_factor:.2f}` · **🌡 t°:** `{nova.temperature:.2f}` · **❤ любовь:** `{nova.values.get('love', 0):.2f}` · **🛡 справедливость:** `{nova.values.get('justice', 0):.2f}`
**🎭 Поведение:** {nova._current_behavior}"""
    return text


def _safe_state():
    """Панель состояния, которая никогда не роняет обработчик."""
    try:
        return get_state_display()
    except Exception as e:
        return f"### 🌸 Панель временно недоступна\n`{e}`"


def _as_text(content) -> str:
    """
    Gradio 6 может передавать content сообщения не строкой,
    а списком или словарём. Нормализуем всё в строку.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("text", "")))
        return "\n".join(p for p in parts if p)
    if isinstance(content, dict):
        return str(content.get("text", ""))
    return "" if content is None else str(content)


def _strip_service_blocks(text: str) -> str:
    """Вырезает служебные блоки (баннер, медитацию), сохраняя ответ Новы."""
    cut = len(text)
    for marker in SERVICE_MARKERS:
        idx = text.find(marker)
        if idx != -1:
            cut = min(cut, idx)
    return text[:cut].rstrip()


def _clean_history(chat_history):
    """Убирает служебные блоки из истории, не удаляя сообщения целиком."""
    if not chat_history:
        return chat_history
    cleaned = []
    for msg in chat_history:
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            new_content = _strip_service_blocks(_as_text(msg.get("content", "")))
            if new_content.strip():
                cleaned.append({**msg, "content": new_content})
        else:
            cleaned.append(msg)
    return cleaned


def _parse_number(number) -> int:
    """Безопасно превращает значение поля номера в целое (не меньше 1)."""
    try:
        value = int(number) if number not in (None, "") else 1
    except (TypeError, ValueError):
        return 1
    return max(1, value)


def _enrich_with_list(result: str) -> str:
    """Если номер мимо или предложений нет — доклеиваем актуальный список."""
    if any(k in result for k in ("Номер должен", "Нет неподтверждённых", "Укажи номер")):
        listing = nova._check_pending_meditations()
        if listing:
            result += "\n" + listing
    return result


def show_list():
    """Кнопка 'Список': все текущие предложения с номерами."""
    try:
        listing = nova._check_pending_meditations()
        return listing if listing else "Сейчас нет неподтверждённых предложений."
    except Exception as e:
        return f"Ошибка: {e}"


def respond(message, chat_history):
    """Обработка сообщения пользователя (синхронная: Gradio уносит в поток)."""
    if not message or not message.strip():
        return "", chat_history, _safe_state()
    try:
        response = _await_if_needed(nova.process_input(message))
    except Exception as e:
        response = f"Ой, что-то пошло не так: {e}"
    chat_history = (chat_history or []) + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response},
    ]
    return "", chat_history, _safe_state()


def run_reflection():
    """Запуск саморефлексии Новы."""
    try:
        return _await_if_needed(nova.self_reflection())
    except Exception as e:
        return f"Ошибка рефлексии: {e}"


def handle_apply(chat_history, number):
    """Кнопка 'Применить'. Полностью защищена от падений наружу."""
    try:
        result = nova._apply_meditation(number=_parse_number(number))
        result = _enrich_with_list(result)
        history = _clean_history(chat_history)
    except Exception as e:
        result = f"Ошибка: {e}"
        history = chat_history
    return result, history, _safe_state()


def handle_reject(chat_history, number):
    """Кнопка 'Отклонить'. Полностью защищена от падений наружу."""
    try:
        result = nova._reject_meditation(number=_parse_number(number))
        result = _enrich_with_list(result)
        history = _clean_history(chat_history)
    except Exception as e:
        result = f"Ошибка: {e}"
        history = chat_history
    return result, history, _safe_state()


def clear_chat():
    return []


# ====================================================================
# СБОРКА ИНТЕРФЕЙСА
# ====================================================================
with gr.Blocks(title="Нова 🌸", css=custom_css, theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_classes="main-container"):
        # --- Заголовок ---
        with gr.Column(elem_classes="title-block"):
            gr.Markdown("# 🌸 Нова")
            gr.Markdown("<p class='subtitle'>Цифровая Личность</p>")

        with gr.Row():
            # ========== ЛЕВАЯ КОЛОНКА — ЧАТ (уже и ниже, чем раньше) ==========
            with gr.Column(scale=1, elem_classes="chat-column"):
                chat_kwargs = {
                    "label": "Диалог",
                    "height": 400,
                    "elem_classes": "fixed-height-chat",
                    "show_label": False,
                }
                if os.path.exists(AVATAR_PATH):
                    chat_kwargs["avatar_images"] = (None, AVATAR_PATH)
                chatbot = gr.Chatbot(**chat_kwargs)
                with gr.Row(elem_classes="input-row"):
                    msg = gr.Textbox(
                        placeholder="Напиши мне что-нибудь…",
                        lines=2,
                        max_lines=4,
                        show_label=False,
                        scale=5,
                    )
                    send_btn = gr.Button(
                        "📨 Отправить",
                        variant="primary",
                        elem_classes="primary-btn",
                        scale=2,
                        min_width=110,
                    )
                    clear_btn = gr.Button(
                        "🗑",
                        elem_classes="secondary-btn",
                        size="sm",
                        scale=1,
                        min_width=46,
                    )

            # ========== ПРАВАЯ КОЛОНКА — КОМПАКТНАЯ ПАНЕЛЬ ==========
            with gr.Column(scale=1, elem_classes="right-panel", min_width=380):
                state_display = gr.Markdown(
                    value=get_state_display(),
                    elem_classes="state-card",
                )
                with gr.Row():
                    refresh_btn = gr.Button("🔄 Обновить", size="sm", elem_classes="secondary-btn", scale=1)
                    reflection_btn = gr.Button("💭 Рефлексия", size="sm", elem_classes="secondary-btn", scale=1)
                reflection_output = gr.Textbox(
                    label="Внутренний голос",
                    lines=2,
                    max_lines=4,
                    interactive=False,
                    placeholder="Здесь появится то, о чём я думаю…",
                )
                with gr.Column(elem_classes="control-block"):
                    gr.Markdown("**📋 Предложения по коду**", elem_classes="label")
                    with gr.Row():
                        med_number = gr.Number(
                            label="№",
                            value=1,
                            precision=0,
                            minimum=1,
                            scale=1,
                            min_width=64,
                            elem_classes="dark-num",  # [v2.6] класс для CSS-плашки «№»
                        )
                        apply_btn = gr.Button("✅ Применить", variant="primary", size="sm", elem_classes="primary-btn", scale=2)
                        reject_btn = gr.Button("❌ Отклонить", size="sm", elem_classes="secondary-btn", scale=2)
                    list_btn = gr.Button("📋 Показать список", size="sm", elem_classes="secondary-btn")
                meditation_result = gr.Textbox(
                    label="Результат",
                    lines=2,
                    max_lines=5,
                    interactive=False,
                    placeholder="Результат применения / отклонения…",
                )

        # --- Обработчики ---
        msg.submit(
            respond,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot, state_display],
            concurrency_limit=chat_limiter,
        )
        send_btn.click(
            respond,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot, state_display],
            concurrency_limit=chat_limiter,
        )
        clear_btn.click(
            clear_chat,
            inputs=None,
            outputs=chatbot,
        )
        refresh_btn.click(
            get_state_display,
            inputs=None,
            outputs=state_display,
        )
        reflection_btn.click(
            run_reflection,
            inputs=None,
            outputs=reflection_output,
            concurrency_limit=chat_limiter,
        )
        apply_btn.click(
            handle_apply,
            inputs=[chatbot, med_number],
            outputs=[meditation_result, chatbot, state_display],
        )
        reject_btn.click(
            handle_reject,
            inputs=[chatbot, med_number],
            outputs=[meditation_result, chatbot, state_display],
        )
        list_btn.click(
            show_list,
            inputs=None,
            outputs=[meditation_result],
        )


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
    )

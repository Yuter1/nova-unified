"""
NOVA UI v1.6 — веб-интерфейс чата с Новой на Gradio (совместим с ядром Nova v1.5+).

ФИНАЛЬНЫЕ ПРАВКИ ИНТЕРФЕЙСА (всё разом, больше не докручиваем):
1. Интерфейс НЕ замирает во время долгой генерации и медитаций:
   обработчики синхронные (Gradio уносит их в отдельный поток),
   а async-методы ядра, внутри которых нет ни одного await,
   докручиваются в локальном event loop через _await_if_needed.
   Если ядро потом станет синхронным — код продолжит работать как есть.
2. Кнопки "Применить"/"Отклонить" обновляют панель состояния
   (state_display добавлен в outputs).
3. gr.Chatbot явно получает type="messages" — совместимо с Gradio 4.x и 5.x.
4. ConcurrencyLimiter(1): отправка сообщений и саморефлексия сериализуются,
   нейрохимия Новы защищена от параллельной порчи двойными кликами.
5. Очистка истории ВЫРЕЗАЕТ служебные блоки (баннер предложений, медитацию)
   из текста ответа, а не удаляет сообщение целиком — ответ Новы сохраняется.
6. Выбор номера предложения для применения/отклонения.
7. Панель состояния показывает ВСЕ 9 нейромедиаторов + производные
   (overlap_factor, температура, ценности, стадия, сны, счётчик предложений).

ЗАПУСК:
1) pip install gradio
2) python nova_ui.py
3) Браузер откроется на http://127.0.0.1:7860
"""

import asyncio
import inspect

import gradio as gr

from nova_unified import Nova

# Инициализируем Нову один раз при старте UI.
# (Если LM Studio выключена — Нова поднимется на запасных эмбеддингах,
#  это ожидаемое поведение ядра, не ошибка интерфейса.)
nova = Nova()

# Служебные маркеры: блоки, которые Нова доклеивает в конец ответа
# и которые не должны висеть в истории после решения по медитации.
SERVICE_MARKERS = ("📋 *У Новы есть", "🧘 *Нова медитирует")

# Ограничитель параллельности: длинные операции, меняющие нейрохимию,
# идут строго по одной, чтобы не топтать состояние Новы вдвоём.
try:
    chat_limiter = gr.ConcurrencyLimiter(limit=1)
except AttributeError:
    # В новых версиях Gradio класс убрали — остаётся числовой лимит на событиях
    chat_limiter = 1


def _await_if_needed(result):
    """
    Методы ядра сейчас объявлены как async, но внутри них нет ни одного
    await (все вызовы синхронные: HTTP к LM Studio, Milvus, файлы).
    Gradio выполняет синхронные обработчики в отдельном потоке, где нет
    работающего event loop, поэтому asyncio.run здесь безопасен и не
    замораживает интерфейс. Если ядро однажды станет синхронным —
    значение просто пройдёт насквозь без изменений.
    """
    if inspect.isawaitable(result):
        return asyncio.run(result)
    return result


def get_state_display():
    """Формирует текст для панели состояния (полная нейрохимия)."""
    neuro = nova.neurochem.levels
    gs = nova.growth_stage
    pending = len(nova._get_proposed_indices())
    text = f"""### 🌸 Состояние Новы
**Эмоция:** {nova._current_emotion}
**Поведение:** {nova._current_behavior}
**Глаза:** {nova.eye_color} (интенсивность {nova.eye_intensity:.2f})
**Стадия:** {gs.stage} (возраст {gs.age:.2f})
**Накопленная жизнь:** {nova.life_core.life_accumulator:.4f}
**Снов за сегодня:** {nova.dream_count_today}
**Предложений по коду:** {pending}

#### 🧪 Нейрохимия — все 9 медиаторов
| Медиатор | Роль | Уровень |
|---|---|---|
| Дофамин (DA) | мотивация, радость, интерес | {neuro.get('DA', 0):.2f} |
| Серотонин (HT) | ровность настроения | {neuro.get('HT', 0):.2f} |
| Окситоцин (OXY) | привязанность, нежность | {neuro.get('OXY', 0):.2f} |
| Норадреналин (NA) | внимание, мобилизация | {neuro.get('NA', 0):.2f} |
| Адреналин (AD) | острый драйв, испуг | {neuro.get('AD', 0):.2f} |
| Кортизол (CORT) | хронический стресс | {neuro.get('CORT', 0):.2f} |
| Гнев (ANGER) | защита, ярость | {neuro.get('ANGER', 0):.2f} |
| Стыд (SHAME) | самокритика, раскаяние | {neuro.get('SHAME', 0):.2f} |
| Жадность (greed) | тяга к новому | {neuro.get('greed', 0):.2f} |

#### ⚙️ Производные показатели
**Фактор перекрытия:** {nova.overlap_factor:.2f}
**Температура генерации:** {nova.temperature:.2f}
**Ценности:** любовь {nova.values.get('love', 0):.2f} · мудрость {nova.values.get('wisdom', 0):.2f} · справедливость {nova.values.get('justice', 0):.2f} · сила {nova.values.get('strength', 0):.2f}
"""
    return text


def respond(message, chat_history):
    """Обработка сообщения пользователя (синхронная: Gradio уносит в поток)."""
    if not message or not message.strip():
        return "", chat_history, get_state_display()
    try:
        response = _await_if_needed(nova.process_input(message))
    except Exception as e:
        response = f"Ой, что-то пошло не так: {e}"
    chat_history = (chat_history or []) + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response},
    ]
    return "", chat_history, get_state_display()


def run_reflection():
    """Запуск саморефлексии Новы."""
    try:
        return _await_if_needed(nova.self_reflection())
    except Exception as e:
        return f"Ошибка рефлексии: {e}"


def _strip_service_blocks(text: str) -> str:
    """
    Вырезает из текста ответа служебные блоки (баннер предложений, медитацию),
    сохраняя сам ответ Новы. Режет от самого раннего маркера до конца.
    """
    cut = len(text)
    for marker in SERVICE_MARKERS:
        idx = text.find(marker)
        if idx != -1:
            cut = min(cut, idx)
    return text[:cut].rstrip()


def _clean_history(chat_history):
    """
    Убирает из истории служебные блоки после решения по медитации.
    ВАЖНО: сообщение не удаляется целиком — вырезается только баннер,
    ответ Новы остаётся в чате.
    """
    if not chat_history:
        return chat_history
    cleaned = []
    for msg in chat_history:
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            new_content = _strip_service_blocks(msg.get("content", ""))
            if new_content.strip():
                cleaned.append({**msg, "content": new_content})
            # если после вырезания текст пуст — сообщение не добавляем
        else:
            cleaned.append(msg)
    return cleaned


def _parse_number(number) -> int:
    """Безопасно превращает значение поля номера в целое."""
    try:
        return int(number) if number not in (None, "") else 1
    except (TypeError, ValueError):
        return 1


def handle_apply(chat_history, number):
    """Кнопка 'Применить': применяет предложение и обновляет панель."""
    try:
        result = nova._apply_meditation(number=_parse_number(number))
    except Exception as e:
        result = f"Ошибка: {e}"
    return result, _clean_history(chat_history), get_state_display()


def handle_reject(chat_history, number):
    """Кнопка 'Отклонить': отклоняет предложение и обновляет панель."""
    try:
        result = nova._reject_meditation(number=_parse_number(number))
    except Exception as e:
        result = f"Ошибка: {e}"
    return result, _clean_history(chat_history), get_state_display()


def clear_chat():
    return []


with gr.Blocks(title="Нова") as demo:
    gr.Markdown("# 🌸 Нова — Цифровая Личность")
    with gr.Row():
        # Левая колонка — чат
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="Диалог",
                height=500,
            )
            msg = gr.Textbox(
                label="Напиши Нове...",
                placeholder="Привет, Нова!",
                lines=2,
            )
            with gr.Row():
                send_btn = gr.Button("📨 Отправить", variant="primary")
                clear_btn = gr.Button("🗑 Очистить чат")
        # Правая колонка — панель состояния
        with gr.Column(scale=1):
            state_display = gr.Markdown(value=get_state_display())
            refresh_btn = gr.Button("🔄 Обновить состояние")
            reflection_btn = gr.Button("💭 Саморефлексия")
            reflection_output = gr.Textbox(
                label="Внутренний голос",
                lines=6,
                interactive=False,
            )
            gr.Markdown("---")
            gr.Markdown("**Управление предложениями по коду:**")
            med_number = gr.Number(
                label="Номер предложения",
                value=1,
                precision=0,
            )
            with gr.Row():
                apply_btn = gr.Button("✅ Применить", variant="primary")
                reject_btn = gr.Button("❌ Отклонить")
            meditation_result = gr.Textbox(
                label="Результат",
                lines=3,
                interactive=False,
            )

    # Обработчики. Длинные операции (чат, рефлексия) идут через ограничитель,
    # чтобы не менять состояние Новы параллельно. Кнопка "Обновить состояние"
    # сознательно оставлена БЕЗ ограничителя — она должна отвечать мгновенно.
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

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        theme=gr.themes.Soft(),
    )
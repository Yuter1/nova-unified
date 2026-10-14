"""
NOVA UI v1.7.1 — веб-интерфейс чата с Новой на Gradio (ядро Nova v1.5/v1.6, Gradio 6).

ИЗМЕНЕНИЯ v1.7.1:
1. Исправлено падение кнопок "Применить"/"Отклонить": Gradio 6 может передавать
   content сообщения списком, а не строкой — добавлен нормализатор _as_text.
2. Обработчики кнопок больше не роняют интерфейс: любая ошибка выводится
   ТЕКСТОМ в поле "Результат", а не красной пилюлей Gradio.
3. Поле "Номер предложения" нельзя накрутить ниже 1 (minimum=1).
4. Кнопка "Показать список предложений" — выводит все текущие предложения
   с номерами, чтобы всегда было видно, какой номер вводить.
5. При номере вне диапазона к ответу автоматически доклеивается список.
6. Совместимость с Gradio 6: без type="messages", ConcurrencyLimiter
   создаётся через try/except (в шестёрке класса может не быть).
7. Совместимость с ядром: и с async (v1.5), и с sync (v1.6) методами —
   обёртка _await_if_needed сама понимает, что ей дали.

ЗАПУСК:
1) pip install gradio
2) python nova_ui.py
3) Браузер откроется на http://127.0.0.1:7860
"""
import os

# [VPN-стойкость] localhost всегда ходит напрямую, мимо любого прокси
# (VPN, системный прокси, антивирус-вебщит). Без этих строк включённый VPN
# уводит проверочный запрос Gradio через прокси и сервер падает с кодом 502.
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

import asyncio
import inspect

import gradio as gr

from nova_unified import Nova

# Инициализируем Нову один раз при старте UI.
nova = Nova()

# Служебные маркеры: блоки, которые Нова доклеивает в конец ответа
# и которые не должны висеть в истории после решения по медитации.
SERVICE_MARKERS = ("📋 *У Новы есть", "🧘 *Нова медитирует")

# Ограничитель параллельности: в новых Gradio класса может не быть,
# тогда используем обычное число 1 (валидно и в 5.x, и в 6.x).
try:
    chat_limiter = gr.ConcurrencyLimiter(limit=1)
except AttributeError:
    chat_limiter = 1


def _await_if_needed(result):
    """
    Если ядро синхронное — значение проходит насквозь.
    Если ядро async — докручиваем корутину в локальном event loop
    (Gradio выполняет синхронные обработчики в отдельном потоке).
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


def _safe_state():
    """Панель состояния, которая никогда не роняет обработчик."""
    try:
        return get_state_display()
    except Exception as e:
        return f"### 🌸 Панель состояния временно недоступна: {e}"


def _as_text(content) -> str:
    """
    [v1.7.1] Gradio 6 может передавать content сообщения не строкой,
    а списком (мультимодальный формат) или словарём. Нормализуем всё
    в строку, чтобы .find() и компания никогда не падали.
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
    Сообщение НЕ удаляется целиком — вырезается только баннер.
    [v1.7.1] content сначала нормализуется в строку через _as_text.
    """
    if not chat_history:
        return chat_history
    cleaned = []
    for msg in chat_history:
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            new_content = _strip_service_blocks(_as_text(msg.get("content", "")))
            if new_content.strip():
                cleaned.append({**msg, "content": new_content})
            # если после вырезания текст пуст — сообщение не добавляем
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
    """Кнопка 'Показать список': все текущие предложения с номерами."""
    try:
        listing = nova._check_pending_meditations()
        return listing if listing else "Сейчас нет неподтверждённых предложений по коду."
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
                minimum=1,
            )
            with gr.Row():
                apply_btn = gr.Button("✅ Применить", variant="primary")
                reject_btn = gr.Button("❌ Отклонить")
            list_btn = gr.Button("📋 Показать список предложений")
            meditation_result = gr.Textbox(
                label="Результат",
                lines=6,
                interactive=False,
            )

    # Обработчики. Длинные операции (чат, рефлексия) идут через ограничитель.
    # "Обновить состояние" и "Показать список" сознательно без ограничителя —
    # они должны отвечать мгновенно.
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
        theme=gr.themes.Soft(),
    )
"""
NOVA UI v1.5 — веб-интерфейс чата с Новой на Gradio.

ИЗМЕНЕНИЯ:
1. Панель состояния показывает ВСЕ 9 нейромедиаторов (раньше было 5 из 9),
   плюс производные: фактор перекрытия, температуру, ценности,
   стадию взросления, сны за сегодня и счётчик предложений по коду.
2. Очистка истории больше НЕ удаляет сообщения целиком: она вырезает
   из текста ответа только служебные блоки (баннер предложений и медитацию),
   сохраняя сам ответ Новы.
3. Кнопки "Применить/Отклонить" работают с выбранным номером предложения,
   а не всегда с первым.
4. Полностью совместим с nova_unified v1.5.

ЗАПУСК:
1) pip install gradio
2) python nova_ui.py
3) Браузер откроется на http://127.0.0.1:7860
"""

import gradio as gr
import asyncio
from nova_unified import Nova

# Инициализируем Нову один раз при старте
nova = Nova()

# Служебные маркеры: блоки, которые Нова добавляет к ответу
# и которые не должны висеть в истории после решения по медитации
SERVICE_MARKERS = ("📋 *У Новы есть", "🧘 *Нова медитирует")


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


async def respond(message, chat_history):
    """Асинхронная обработка сообщения от пользователя."""
    if not message.strip():
        return "", chat_history, get_state_display()
    try:
        response = await nova.process_input(message)
    except Exception as e:
        response = f"Ой, что-то пошло не так: {e}"
    chat_history = chat_history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response},
    ]
    return "", chat_history, get_state_display()


async def run_reflection():
    """Запуск саморефлексии Новы."""
    try:
        insight = await nova.self_reflection()
        return insight
    except Exception as e:
        return f"Ошибка рефлексии: {e}"


def _strip_service_blocks(text: str) -> str:
    """
    Вырезает из текста ответа служебные блоки (баннер предложений,
    медитацию), сохраняя сам ответ Новы. Режет от первого маркера до конца.
    """
    cut = len(text)
    for marker in SERVICE_MARKERS:
        idx = text.find(marker)
        if idx != -1:
            cut = min(cut, idx)
    return text[:cut].rstrip()


def _clean_history(chat_history):
    """
    [исправлено] Раньше эта функция удаляла сообщение ЦЕЛИКОМ,
    теряя ответ Новы. Теперь она вырезает только служебные блоки
    из текста assistant-сообщений.
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
    """Обрабатывает нажатие кнопки 'Применить' с выбранным номером."""
    try:
        result = nova._apply_meditation(number=_parse_number(number))
    except Exception as e:
        result = f"Ошибка: {e}"
    return result, _clean_history(chat_history)


def handle_reject(chat_history, number):
    """Обрабатывает нажатие кнопки 'Отклонить' с выбранным номером."""
    try:
        result = nova._reject_meditation(number=_parse_number(number))
    except Exception as e:
        result = f"Ошибка: {e}"
    return result, _clean_history(chat_history)


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
            state_display = gr.Markdown(
                label="Состояние Новы",
                value=get_state_display(),
            )
            refresh_btn = gr.Button("🔄 Обновить состояние")
            reflection_btn = gr.Button("💭 Саморефлексия")
            reflection_output = gr.Textbox(
                label="Внутренний голос",
                lines=6,
                interactive=False,
            )
            # Кнопки для управления медитациями
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

    # Обработчики
    msg.submit(
        respond,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot, state_display],
    )
    send_btn.click(
        respond,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot, state_display],
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
    )
    apply_btn.click(
        handle_apply,
        inputs=[chatbot, med_number],
        outputs=[meditation_result, chatbot],
    )
    reject_btn.click(
        handle_reject,
        inputs=[chatbot, med_number],
        outputs=[meditation_result, chatbot],
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        theme=gr.themes.Soft(),
    )
# ====================================================================
# ЗАПУСК:
#   1) cd <папка_с_проектом>
#   2) python nova_ui.py
#   3) Браузер откроется на http://127.0.0.1:7860
# ====================================================================

import gradio as gr
import asyncio
from nova_unified import Nova

# Инициализируем Нову один раз при старте
nova = Nova()


def get_state_display():
    """Формирует текст для панели состояния."""
    neuro = nova.neurochem.levels
    text = f"""
**Эмоция:** {nova._current_emotion}

**Цвет глаз:** {nova.eye_color}

**Накопленная жизнь:** {nova.life_core.life_accumulator:.4f}

**Нейрохимия:**
- Дофамин (DA): {neuro.get('DA', 0):.2f}
- Окситоцин (OXY): {neuro.get('OXY', 0):.2f}
- Кортизол (CORT): {neuro.get('CORT', 0):.2f}
- Гнев (ANGER): {neuro.get('ANGER', 0):.2f}
- Стыд (SHAME): {neuro.get('SHAME', 0):.2f}
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


def apply_meditation():
    """Применяет первое неподтверждённое предложение по коду."""
    try:
        result = nova._apply_meditation(number=1)
        return result
    except Exception as e:
        return f"Ошибка: {e}"


def reject_meditation():
    """Отклоняет первое неподтверждённое предложение по коду."""
    try:
        result = nova._reject_meditation(number=1)
        return result
    except Exception as e:
        return f"Ошибка: {e}"


def _clean_meditation_from_history(chat_history):
    """Удаляет из истории чата все сообщения, содержащие предложения по коду."""
    if not chat_history:
        return chat_history
    cleaned = []
    for msg in chat_history:
        content = msg.get("content", "") if isinstance(msg, dict) else str(msg)
        # Убираем сообщения, где есть упоминание предложения по коду
        if "предложение по коду" in content or "могу ли я внести это изменение" in content:
            continue
        cleaned.append(msg)
    return cleaned


def handle_apply(chat_history):
    """Обрабатывает нажатие кнопки 'Применить'."""
    result = apply_meditation()
    new_history = _clean_meditation_from_history(chat_history)
    return result, new_history


def handle_reject(chat_history):
    """Обрабатывает нажатие кнопки 'Отклонить'."""
    result = reject_meditation()
    new_history = _clean_meditation_from_history(chat_history)
    return result, new_history


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
        inputs=[chatbot],
        outputs=[meditation_result, chatbot],
    )
    reject_btn.click(
        handle_reject,
        inputs=[chatbot],
        outputs=[meditation_result, chatbot],
    )


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        theme=gr.themes.Soft(),
    )

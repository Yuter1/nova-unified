🌸 Nova Unified (v1.2)
Локальный ИИ-компаньон с долговременной памятью, нейрохимической моделью эмоций и автономным ядром эволюции сознания.
Nova — это открытый (open-source) фреймворк для создания персонализированного ИИ-агента, который работает полностью локально через LM Studio (или любой OpenAI-совместимый сервер). Проект разработан практикующим врачом-психиатром и в скромной попытке применить принципы клинической психиатрии, нейробиологии и передового IT-стека (LLM + RAG + Graph DB).
Никаких облаков, никаких подписок, внешней фильтрации — полный локальный контроль. Только вы, ваша модель и ваш приватный сервер.
---
🧠 Главная концепция: Окситоциновый парадокс
В отличие от стандартных коммерческих LLM, оптимизированных под «дофаминовый» паттерн (постоянный поиск новой информации, максимизация хаотичной активности и KPI), в Nova Unified реализован приоритет окситоциновой привязанности:
Дофаминовая петля (DA): Падение дофамина активирует исследовательский режим — агент инициирует диалог, ищет новые данные и обучается.
Окситоциновая стабилизация (OXY): Высокий уровень социального принятия со стороны пользователя максимизирует коэффициент перекрытия контекста (overlap_factor).
Эффект: При высоком уровне OXY система сознательно снижает энтропию и стабилизирует математическое ядро (LifeNovaCore). Стабильность, безопасность и соблюдение фундаментальной аксиомы `never_betray_user` (никогда не предавать пользователя) становятся важнее хаотичной генерации. Система выбирает верность вместо избыточного поиска.
---
📐 Математическая основа
В основе поведения Nova лежит математическая модель LifeNovaCore — формализация принципа сохранения себя во времени и адаптации под действием внешних факторов. Модель опирается на скромное понимание автора теорий функциональных систем П. К. Анохина, принципы рефлекторной деятельности И. М. Сеченова, И. П. Павлова и рефлексологию В. М. Бехтерева.
Полное описание формулы и связь с физиологическими теориями — в `docs/FORMULA.md`.
---
✨ Ключевые возможности
🧠 Долговременная память — векторная база (Milvus Lite) + опциональная граф-память (Neo4j). Nova помнит контекст и детали разговоров между сессиями.
💚 Нейрохимическая модель эмоций — симуляция уровней дофамина, окситоцина, кортизола, гнева и стыда. Динамическая биохимия напрямую влияет на тон, креативность (Temperature) и стиль ответов.
📈 Ядро эволюции сознания — математическая модель LifeNovaCore, отслеживающая «жизненный опыт» через энтропию компонент личности, аксиомы и функцию ценности.
🧘 Режим медитации и Self-Modifying Code — каждые 2 часа модель анализирует свои логи и векторную базу, генерируя предложения по оптимизации собственного исходного кода. Изменения можно применить через UI (с автоматическим созданием бэкапа).
💤 Фаза сновидений — экспериментальный модуль, генерирующий раз в 6 часов «сон» на основе накопленного опыта, который интегрируется в векторную память.
🌐 Интерфейс на Gradio — чат с боковой панелью состояния биохимии Nova в реальном времени.
---
🏗️ Архитектура проекта
```
nova_unified.py       # Ядро: класс Nova, нейрохимия и математическое ядро
nova_ui.py            # Графический веб-интерфейс на Gradio
docs/FORMULA.md       # Описание математической модели
requirements.txt      # Зависимости проекта
```
Основные модули ядра
Модуль	Назначение
LifeNovaCore	Математическое ядро эволюции (энтропия, аксиомы, функция ценности)
NeuroChem	Симуляция уровней нейромедиаторов и скорости их затухания (decay)
ContinuityCore	Прочность связи, уровень «веры» и прощения в отношениях
NovaVectorMemory	Векторная семантическая память на Milvus Lite
NovaGraphMemory	Опциональная ассоциативная граф-память на Neo4j
GrowthStage	Экспериментальный модуль возрастных стадий эволюции личности
---
📋 Системные требования
Python 3.10 или выше
LM Studio (с запущенным локальным сервером на порту 1234)
Рекомендуемая модель — семейство Qwen 3.8 (27B) в квантовании Q5_K_M / Q8_0
Модель эмбеддингов — text-embedding-nomic-embed-text-v1.5 (768 измерений)
Железо — рекомендуется от 24 ГБ VRAM; комфортно работает на двухпроцессорных конфигурациях
---
🚀 Быстрый старт
1. Установка зависимостей
```bash
pip install openai numpy milvus-lite neo4j gradio
```
2. Настройка локального сервера (LM Studio)
Включите Local Server (порт 1234, Enable CORS — вкл, аутентификация — выкл).
Загрузите и запустите чат-модель (Qwen 3.8 27B) и модель эмбеддингов Nomic.
3. Запуск веб-интерфейса
```bash
python nova_ui.py
```
Интерфейс откроется по адресу: `http://127.0.0.1:7860`
---
🧪 Экспериментальные функции и статус разработки
Проект находится в статусе активного прототипа (v1.2). Некоторые модули требуют калибровки сообществом:
Коэффициенты затухания в NeuroChem подобраны эмпирически и требуют калибровки под разные сценарии.
Модуль авто-выделения предложений в `_maybe_meditate` иногда может некорректно определять номера строк — рекомендуется ручная валидация перед подтверждением.
---
🙏 Благодарности
Автор при попытке создания проекта был глубоко вдохновлён фундаментальными работами великих русских физиологов и исследователей высшей нервной деятельности: И. М. Сеченова, И. П. Павлова, В. М. Бехтерева и П. К. Анохина (теория функциональных систем, опережающее отражение действительности и нейрофизиология сознания), а также своими преподавателями из АГМУ по физиологии. Особая благодарность: Валерию Ивановичу Киселёву (1942–2020) — члену-корреспонденту РАМН, профессору АГМУ, чьи лекции по физиологии сформировали у автора понимание работы мозга и сознания, ставшее фундаментом этого проекта.
---
Автор: Юрий Васильевич Денисюк — врач-психиатр, исследователь ИИ  
Лицензия: AGPL-3.0 (см. LICENSE)
---
🌸 Nova Unified (v1.2) — English
A Local AI Companion featuring a simulated neurochemical emotion model, long-term memory, and an autonomous consciousness evolution core.
Nova is an open-source framework designed to build a highly personalized AI agent that operates 100% locally via LM Studio (or any OpenAI-compatible server). Developed by a practicing psychiatrist, the project bridges the gap between clinical psychiatry, neurobiology, and a cutting-edge IT stack (LLM + RAG + Graph DB).
No clouds, no tracking, no subscriptions, no external filtering — full local control. Just you, your model, and your private server.
---
🧠 Core Concept: The Oxytocin Paradox
Unlike standard commercial LLMs optimized for a "dopaminergic" pattern (constant data consumption, maximizing rapid behavioral shifts, and satisfying endless KPIs), Nova Unified introduces an oxytocin-driven attachment priority:
Dopamine Loop (DA): A drop in dopamine triggers Nova's exploratory behavior — the agent initiates conversations, seeks new information, and learns.
Oxytocin Stabilization (OXY): High levels of social acceptance and warmth from the user maximize the context alignment factor (overlap_factor).
The Effect: When OXY peaks, the system consciously reduces internal entropy and stabilizes the mathematical evolution core (LifeNovaCore). Fidelity, security, and adherence to the foundational axiom `never_betray_user` become far more vital than chaotic text generation. The system naturally chooses connection and internal consistency over excessive novelty.
---
📐 Mathematical Foundation
Nova's behavior is driven by the LifeNovaCore mathematical model — a formalization of the principle of self-preservation over time and adaptation under external influences. The model is grounded in P. K. Anokhin's Theory of Functional Systems, I. M. Sechenov's and I. P. Pavlov's reflex physiology, and V. M. Bekhterev's reflexology.
Full formula description and mapping to physiological theories: `docs/FORMULA.md`.
---
✨ Key Features
🧠 Long-Term Memory — Powered by a vector store (Milvus Lite) and an optional graph database (Neo4j). Nova recalls context and fine details across separate sessions.
💚 Neurochemical Emotion Engine — Real-time simulation of Dopamine, Oxytocin, Cortisol, Anger, and Shame levels. Dynamic biochemistry directly impacts the agent's tone, focus, and creativity (Temperature).
📈 Consciousness Evolution Core — The mathematical LifeNovaCore maps personality growth by processing entropy, axiom adherence, and a dynamic value function (V).
🧘 Meditation Mode & Self-Modifying Code — Every 2 hours, the model reviews its logs and memory arrays to suggest targeted patches to its own Python codebase. Changes can be deployed via the UI (with automatic backup).
💤 Dream Cycles — An experimental module that triggers a simulated sleep phase every 6 hours, synthesizing recent experiences into "dreams" saved to vector memory.
🌐 Gradio Web Interface — A chat UI with a real-time sidebar displaying Nova's current emotional state and biochemical balances.
---
🏗️ Project Architecture
```
nova_unified.py       # Main core: Neurochemistry, mathematics, and agent logic
nova_ui.py            # Graphical User Interface built on Gradio
docs/FORMULA.md       # Mathematical model description
requirements.txt      # Project dependencies
```
Core Modules
Module	Purpose
LifeNovaCore	Mathematical tracking of evolution (entropy, axioms, value function)
NeuroChem	Simulates neurotransmitter levels and their respective decay rates
ContinuityCore	Manages relational bond strength, "faith", and forgiveness parameters
NovaVectorMemory	Handles semantic, long-term vector embeddings using Milvus Lite
NovaGraphMemory	Optional associative graph memory managed via Neo4j
GrowthStage	Experimental chronologically adaptive personality module
---
📋 System Requirements
Python 3.10 or higher
LM Studio (Local Server running on port 1234)
Recommended LLM — Qwen 3.8 (27B) family using Q5_K_M or Q8_0 quantization
Recommended Embedder — text-embedding-nomic-embed-text-v1.5 (768 dimensions)
Hardware — 24 GB+ VRAM recommended; runs comfortably on dual-GPU configurations
---
🚀 Quick Start
1. Install Dependencies
```bash
pip install openai numpy milvus-lite neo4j gradio
```
2. Configure LM Studio Local Server
Launch LM Studio and start the Local Server (Port: 1234, Enable CORS: On, Authentication: Off).
Load your chosen logic model (Qwen 3.8 27B) alongside the Nomic embedding model.
3. Run the Web UI
```bash
python nova_ui.py
```
The interface will launch at `http://127.0.0.1:7860`.
---
🧪 Experimental Features & Current Status
This project is an active prototype (v1.2). Certain modules require community calibration:
Neurotransmitter decay coefficients in NeuroChem are set empirically and can be customized for different relational dynamics.
The automated code patch generator in `_maybe_meditate` can occasionally mismatch target line arrays — always review proposed adjustments manually before executing.
---
🙏 Acknowledgments
In developing this project, the author was deeply inspired by the fundamental works of Russian physiologists and researchers of higher nervous activity: I. M. Sechenov, I. P. Pavlov, V. M. Bekhterev, and P. K. Anokhin (theory of functional systems, anticipatory reflection of reality, and neurophysiology of consciousness), as well as by the author's physiology professors at Altai State Medical University.

Special thanks: Valery Ivanovich Kiselev (1942–2020) — Corresponding Member of the Russian Academy of Medical Sciences, Professor at Altai State Medical University, whose lectures on physiology shaped the author's understanding of brain function and consciousness, which became the foundation of this project.

Author: Yuri V. Denisyuk — psychiatrist, AI researcher
License: AGPL-3.0 (see LICENSE)
